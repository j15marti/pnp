#!/usr/bin/env python3
"""Finite red-team models for short-digest residual caches.

Status: COMPUTATIONAL.  This program does not claim an asymptotic SAT result.
It constructs a source-checkable CNF family with many distinct normalized
residuals, searches bounded prefixes for collisions in truncated SHA-256, and
compares exact and inexact cache policies with explicit work/storage counters.

Every invocation installs a wall-clock alarm (24 seconds by default).  Large
collision searches should be run as separate invocations, one digest length at
a time, so a single run remains inside the requested time budget.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools as it
import json
import math
import signal
import time
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


Clause = Tuple[int, ...]
Formula = Tuple[Clause, ...]


def canon(formula: Iterable[Iterable[int]]) -> Formula:
    """Match the syntactic canonicalization used by matched_double_wrapper.py."""
    return tuple(sorted(set(tuple(sorted(set(clause))) for clause in formula)))


def normalize(formula: Iterable[Iterable[int]]) -> Formula:
    formula = canon(formula)
    variables = sorted({abs(lit) for clause in formula for lit in clause})
    renaming = {variable: index + 1 for index, variable in enumerate(variables)}
    return canon(
        tuple(renaming[abs(lit)] * (1 if lit > 0 else -1) for lit in clause)
        for clause in formula
    )


def terminal(formula: Formula):
    if () in formula:
        return False
    if not formula:
        return True
    return None


def restrict(formula: Formula, assignment: Dict[int, bool]) -> Formula:
    out = []
    for clause in formula:
        if any(
            abs(lit) in assignment and assignment[abs(lit)] == (lit > 0)
            for lit in clause
        ):
            continue
        out.append(tuple(lit for lit in clause if abs(lit) not in assignment))
    return canon(out)


def simplify(formula: Formula) -> Formula:
    formula = canon(formula)
    while terminal(formula) is None:
        units = [clause[0] for clause in formula if len(clause) == 1]
        if not units:
            break
        if any(-lit in units for lit in units):
            return ((),)
        formula = restrict(
            formula, {abs(lit): lit > 0 for lit in units}
        )
    return normalize(formula)


def xor_triangle(odd: bool, offset: int = 0) -> Formula:
    """Three 2-XORs.  Even is satisfiable; odd is contradictory."""
    formula = []
    for a, b, parity in (
        (1 + offset, 2 + offset, 0),
        (2 + offset, 3 + offset, 0),
        (1 + offset, 3 + offset, int(odd)),
    ):
        for x, y in it.product((0, 1), repeat=2):
            if x ^ y != parity:
                formula.append(
                    (a if not x else -a, b if not y else -b)
                )
    return canon(formula)


def delayed_parent(tag_bits: int) -> Formula:
    """One parent whose complete selector histories leave distinct residuals.

    Selector p chooses a satisfiable or contradictory XOR triangle.  Each tag
    selector x_j leaves either (y_j OR z_j) or (-y_j OR -z_j), which records a
    history bit without creating units.  The residual therefore has tag_bits+1
    independent components.
    """
    control = 1
    selectors = list(range(2, 2 + tag_bits))
    first_tag_variable = 2 + tag_bits
    formula: List[Clause] = []
    for j, selector in enumerate(selectors):
        y = first_tag_variable + 2 * j
        z = y + 1
        formula.extend(((selector, y, z), (-selector, -y, -z)))

    core_offset = first_tag_variable + 2 * tag_bits - 1
    for clause in xor_triangle(False, core_offset):
        formula.append((control,) + clause)       # active for p = False
    for clause in xor_triangle(True, core_offset):
        formula.append((-control,) + clause)      # active for p = True
    return canon(formula)


def history_assignment(history: int, tag_bits: int) -> Dict[int, bool]:
    assignment = {1: bool(history & 1)}
    tags = history >> 1
    for j in range(tag_bits):
        assignment[2 + j] = bool((tags >> j) & 1)
    return assignment


def direct_residual(history: int, tag_bits: int) -> Formula:
    """Residual after the selector history, already in normalized variable IDs."""
    tags = history >> 1
    formula: List[Clause] = []
    for j in range(tag_bits):
        y = 2 * j + 1
        z = y + 1
        if (tags >> j) & 1:
            formula.append((-y, -z))
        else:
            formula.append((y, z))
    core_offset = 2 * tag_bits
    formula.extend(xor_triangle(bool(history & 1), core_offset))
    return canon(formula)


def known_answer(history: int) -> bool:
    """The tag components are SAT; only the selected XOR core decides SAT."""
    return not bool(history & 1)


def formula_bytes(formula: Formula) -> bytes:
    return repr(formula).encode("ascii")


def digest_int(formula: Formula, hex_digits: int) -> int:
    if hex_digits not in (4, 6, 8):
        raise ValueError("hex_digits must be one of 4, 6, 8")
    byte_count = hex_digits // 2
    return int.from_bytes(
        hashlib.sha256(formula_bytes(formula)).digest()[:byte_count], "big"
    )


def formula_tokens(formula: Formula) -> int:
    """One length token per sequence plus one token per literal."""
    return 1 + sum(1 + len(clause) for clause in formula)


def equality_token_work(left: Formula, right: Formula) -> Tuple[bool, int]:
    """Exact structural equality with a reproducible token-visit charge."""
    work = 1
    if len(left) != len(right):
        return False, work
    for left_clause, right_clause in zip(left, right):
        work += 1
        if len(left_clause) != len(right_clause):
            return False, work
        for left_lit, right_lit in zip(left_clause, right_clause):
            work += 1
            if left_lit != right_lit:
                return False, work
    return True, work


def component_count(formula: Formula) -> int:
    vertices = {abs(lit) for clause in formula for lit in clause}
    adjacency = {vertex: set() for vertex in vertices}
    for clause in formula:
        clause_vertices = [abs(lit) for lit in clause]
        for vertex in clause_vertices[1:]:
            adjacency[clause_vertices[0]].add(vertex)
            adjacency[vertex].add(clause_vertices[0])
    count = 0
    while vertices:
        count += 1
        todo = [next(iter(vertices))]
        seen = set()
        while todo:
            vertex = todo.pop()
            if vertex in seen:
                continue
            seen.add(vertex)
            vertices.discard(vertex)
            todo.extend(adjacency[vertex] - seen)
    return count


def verify_family(tag_bits: int) -> dict:
    parent = delayed_parent(tag_bits)
    probes = sorted(
        {
            0,
            1,
            2,
            3,
            (1 << tag_bits) - 2,
            (1 << tag_bits) - 1,
            (1 << (tag_bits + 1)) - 2,
            (1 << (tag_bits + 1)) - 1,
        }
    )
    direct_matches = 0
    for history in probes:
        actual = simplify(restrict(parent, history_assignment(history, tag_bits)))
        expected = direct_residual(history, tag_bits)
        if actual != expected:
            raise AssertionError((history, actual, expected))
        direct_matches += 1

    core_truth = {}
    for odd in (False, True):
        core = xor_triangle(odd)
        answers = []
        for values in it.product((False, True), repeat=3):
            assignment = dict(zip((1, 2, 3), values))
            answers.append(
                all(
                    any(assignment[abs(lit)] == (lit > 0) for lit in clause)
                    for clause in core
                )
            )
        core_truth["odd" if odd else "even"] = any(answers)
    if core_truth != {"even": True, "odd": False}:
        raise AssertionError(core_truth)

    sample = direct_residual(0, tag_bits)
    return {
        "parent_clauses": len(parent),
        "parent_variables": max(abs(lit) for clause in parent for lit in clause),
        "residual_clauses": len(sample),
        "residual_variables": max(abs(lit) for clause in sample for lit in clause),
        "residual_components": component_count(sample),
        "direct_restriction_probes": direct_matches,
        "core_truth_by_exhaustive_3var_check": core_truth,
        "distinctness_reason": (
            "each history tag selects the sign of its own disjoint 2-clause; "
            "control selects the even/odd XOR core"
        ),
    }


def collision_search(hex_digits: int, samples: int, tag_bits: int) -> dict:
    capacity = 1 << (4 * hex_digits)
    if samples > (1 << (tag_bits + 1)):
        raise ValueError("samples exceed the finite history family")
    first: Dict[int, int] = {}
    buckets: Dict[int, List[int]] = {}
    started = time.perf_counter()
    for history in range(samples):
        digest = digest_int(direct_residual(history, tag_bits), hex_digits)
        if digest not in first:
            first[digest] = history
        else:
            if digest not in buckets:
                buckets[digest] = [first[digest]]
            buckets[digest].append(history)
    elapsed = time.perf_counter() - started

    bucket_sizes = Counter(len(histories) for histories in buckets.values())
    cross_answer = {
        digest: histories
        for digest, histories in buckets.items()
        if len({known_answer(history) for history in histories}) > 1
    }
    same_answer = {
        digest: histories
        for digest, histories in buckets.items()
        if len({known_answer(history) for history in histories}) == 1
    }
    expected_pairs = samples * (samples - 1) / (2 * capacity)
    actual_pairs = sum(
        len(histories) * (len(histories) - 1) // 2
        for histories in buckets.values()
    )

    ranked = sorted(
        buckets.items(),
        key=lambda item: (
            -(len({known_answer(h) for h in item[1]}) > 1),
            -len(item[1]),
            item[0],
        ),
    )
    selected = ranked[:96]
    selected_digests = {digest for digest, _ in selected}
    singletons = [
        history
        for digest, history in first.items()
        if digest not in buckets and digest not in selected_digests
    ][:256]

    return {
        "hex_digits": hex_digits,
        "digest_bits": 4 * hex_digits,
        "samples": samples,
        "digest_space": capacity,
        "unique_digests": len(first),
        "collision_insertions": samples - len(first),
        "colliding_buckets": len(buckets),
        "cross_answer_buckets": len(cross_answer),
        "same_answer_buckets": len(same_answer),
        "max_bucket_size": max(map(len, buckets.values()), default=1),
        "bucket_size_histogram": dict(sorted(bucket_sizes.items())),
        "actual_colliding_pairs": actual_pairs,
        "birthday_expected_colliding_pairs": expected_pairs,
        "search_seconds": elapsed,
        "selected_buckets": [
            {
                "digest_hex": f"{digest:0{hex_digits}x}",
                "histories": histories,
                "answers": [known_answer(history) for history in histories],
            }
            for digest, histories in selected
        ],
        "singleton_histories": singletons,
    }


def selected_workload(search: dict, repeats: int = 4) -> List[int]:
    one_pass: List[int] = []
    for bucket in search["selected_buckets"]:
        histories = bucket["histories"]
        # Put both truth values early when possible, making unsafe reuse visible.
        ordered = sorted(histories, key=lambda history: (known_answer(history), history))
        one_pass.extend(ordered)
    one_pass.extend(search["singleton_histories"])
    if not one_pass:
        return []
    return one_pass * repeats


def cache_comparison(search: dict, tag_bits: int, repeats: int = 4) -> dict:
    hex_digits = search["hex_digits"]
    digest_bytes = hex_digits // 2
    workload = selected_workload(search, repeats)
    unique_histories = sorted(set(workload))
    materialized = {
        history: direct_residual(history, tag_bits) for history in unique_histories
    }
    serialized_lengths = {
        history: len(formula_bytes(formula))
        for history, formula in materialized.items()
    }
    token_lengths = {
        history: formula_tokens(formula)
        for history, formula in materialized.items()
    }
    total_lookup_serialized_bytes = sum(
        serialized_lengths[history] for history in workload
    )

    # No cache: exact, but every request evaluates the selected core again.
    no_cache = {
        "correct": True,
        "wrong_answers": 0,
        "leaf_evaluations": len(workload),
        "cache_hits": 0,
        "logical_stored_bytes": 0,
        "verification_comparisons": 0,
        "verification_token_visits": 0,
    }

    # Unsafe cache: digest equality is treated as formula equality.
    unsafe_table: Dict[int, bool] = {}
    unsafe_wrong = 0
    unsafe_hits = 0
    unsafe_evaluations = 0
    for history in workload:
        formula = materialized[history]
        digest = digest_int(formula, hex_digits)
        if digest in unsafe_table:
            answer = unsafe_table[digest]
            unsafe_hits += 1
        else:
            answer = known_answer(history)
            unsafe_table[digest] = answer
            unsafe_evaluations += 1
        unsafe_wrong += answer != known_answer(history)
    unsafe = {
        "correct": unsafe_wrong == 0,
        "wrong_answers": unsafe_wrong,
        "leaf_evaluations": unsafe_evaluations,
        "cache_hits": unsafe_hits,
        "logical_stored_bytes": len(unsafe_table) * (digest_bytes + 1),
        "digest_hash_input_bytes": total_lookup_serialized_bytes,
        "verification_comparisons": 0,
        "verification_token_visits": 0,
    }

    # Verified short-hash buckets: retain and compare complete normalized keys.
    verified_table: Dict[int, List[Tuple[Formula, bool]]] = {}
    verified_wrong = 0
    verified_hits = 0
    verified_evaluations = 0
    verified_comparisons = 0
    verified_token_visits = 0
    for history in workload:
        formula = materialized[history]
        digest = digest_int(formula, hex_digits)
        answer = None
        for stored_formula, stored_answer in verified_table.get(digest, []):
            verified_comparisons += 1
            equal, work = equality_token_work(formula, stored_formula)
            verified_token_visits += work
            if equal:
                answer = stored_answer
                verified_hits += 1
                break
        if answer is None:
            answer = known_answer(history)
            verified_table.setdefault(digest, []).append((formula, answer))
            verified_evaluations += 1
        verified_wrong += answer != known_answer(history)
    verified_storage = (
        len(verified_table) * digest_bytes
        + sum(serialized_lengths[history] + 1 for history in unique_histories)
    )
    verified = {
        "correct": verified_wrong == 0,
        "wrong_answers": verified_wrong,
        "leaf_evaluations": verified_evaluations,
        "cache_hits": verified_hits,
        "logical_stored_bytes": verified_storage,
        "digest_hash_input_bytes": total_lookup_serialized_bytes,
        "verification_comparisons": verified_comparisons,
        "verification_token_visits": verified_token_visits,
    }

    # Full-key table: exact lookup, charging all key tokens as hashing work.
    full_table: Dict[Formula, bool] = {}
    full_wrong = 0
    full_hits = 0
    full_evaluations = 0
    full_hash_tokens = 0
    for history in workload:
        formula = materialized[history]
        full_hash_tokens += token_lengths[history]
        if formula in full_table:
            answer = full_table[formula]
            full_hits += 1
        else:
            answer = known_answer(history)
            full_table[formula] = answer
            full_evaluations += 1
        full_wrong += answer != known_answer(history)
    full = {
        "correct": full_wrong == 0,
        "wrong_answers": full_wrong,
        "leaf_evaluations": full_evaluations,
        "cache_hits": full_hits,
        "logical_stored_bytes": sum(
            serialized_lengths[history] + 1 for history in unique_histories
        ),
        "full_key_hash_token_visits": full_hash_tokens,
        "full_key_serialized_input_bytes_proxy": total_lookup_serialized_bytes,
        "verification_comparisons": 0,
        "verification_token_visits": 0,
    }

    # Compact source/history records, with regeneration on digest collision.
    # This is exact only for this fixed injective residual generator.
    replay_table: Dict[int, List[Tuple[int, bool]]] = {}
    replay_wrong = 0
    replay_hits = 0
    replay_evaluations = 0
    replay_comparisons = 0
    replay_token_visits = 0
    replay_regenerations = 0
    replay_regeneration_output_tokens = 0
    for history in workload:
        formula = materialized[history]
        digest = digest_int(formula, hex_digits)
        answer = None
        for stored_history, stored_answer in replay_table.get(digest, []):
            replay_comparisons += 1
            if stored_history == history:
                # Injectivity of direct_residual has been proved syntactically.
                answer = stored_answer
                replay_hits += 1
                replay_token_visits += 1
                break
            regenerated = direct_residual(stored_history, tag_bits)
            replay_regenerations += 1
            replay_regeneration_output_tokens += formula_tokens(regenerated)
            equal, work = equality_token_work(formula, regenerated)
            replay_token_visits += work
            if equal:
                answer = stored_answer
                replay_hits += 1
                break
        if answer is None:
            answer = known_answer(history)
            replay_table.setdefault(digest, []).append((history, answer))
            replay_evaluations += 1
        replay_wrong += answer != known_answer(history)
    history_bytes = math.ceil((tag_bits + 1) / 8)
    shared_source_bytes = len(formula_bytes(delayed_parent(tag_bits)))
    replay = {
        "correct": replay_wrong == 0,
        "wrong_answers": replay_wrong,
        "leaf_evaluations": replay_evaluations,
        "cache_hits": replay_hits,
        "logical_stored_bytes": (
            shared_source_bytes
            + len(replay_table) * digest_bytes
            + len(unique_histories) * (history_bytes + 1)
        ),
        "shared_source_bytes": shared_source_bytes,
        "history_descriptor_bytes_each": history_bytes,
        "digest_hash_input_bytes": total_lookup_serialized_bytes,
        "verification_comparisons": replay_comparisons,
        "verification_token_visits": replay_token_visits,
        "residual_regenerations": replay_regenerations,
        "residual_regeneration_output_tokens": replay_regeneration_output_tokens,
        "scope": (
            "exact for the fixed parent and the proved-injective history-to-residual "
            "map; a generic cache must retain or regenerate enough source data to "
            "verify full residual equality"
        ),
    }

    return {
        "requests": len(workload),
        "unique_residuals": len(unique_histories),
        "repeat_count": repeats,
        "mean_serialized_key_bytes": (
            sum(serialized_lengths.values()) / len(serialized_lengths)
            if serialized_lengths
            else 0
        ),
        "total_lookup_serialized_bytes": total_lookup_serialized_bytes,
        "accounting_note": (
            "logical serialized payload only; excludes Python object, dict, allocator, "
            "and process overhead; answer charged as one byte"
        ),
        "no_cache": no_cache,
        "unsafe_hash_only": unsafe,
        "verified_hash_full_key": verified,
        "full_key": full,
        "verified_hash_source_replay": replay,
    }


def delayed_history_audit(search: dict, tag_bits: int) -> dict:
    """Find same-answer collisions whose future restrictions separate."""
    tests = []
    checked_pairs = 0
    for bucket in search["selected_buckets"]:
        histories = bucket["histories"]
        for left_index, left in enumerate(histories):
            for right in histories[left_index + 1 :]:
                if known_answer(left) != known_answer(right):
                    continue
                tag_difference = (left >> 1) ^ (right >> 1)
                if not tag_difference:
                    continue
                checked_pairs += 1
                bit = (tag_difference & -tag_difference).bit_length() - 1
                left_formula = direct_residual(left, tag_bits)
                right_formula = direct_residual(right, tag_bits)
                y, z = 2 * bit + 1, 2 * bit + 2
                left_next = simplify(restrict(left_formula, {y: False, z: False}))
                right_next = simplify(restrict(right_formula, {y: False, z: False}))
                if left_next == right_next:
                    raise AssertionError("differing tag component failed to separate")
                left_positive = not bool(((left >> 1) >> bit) & 1)
                right_positive = not bool(((right >> 1) >> bit) & 1)
                tests.append(
                    {
                        "digest_hex": bucket["digest_hex"],
                        "histories": [left, right],
                        "current_answer": known_answer(left),
                        "differing_tag_bit": bit,
                        "forced_false_clause_side": (
                            "left" if left_positive else "right"
                        ),
                        "restricted_formulas_distinct": True,
                        "future_answers_separate_if_current_answer_is_SAT": (
                            known_answer(left) and left_positive != right_positive
                        ),
                    }
                )
                if len(tests) >= 32:
                    break
            if len(tests) >= 32:
                break
        if len(tests) >= 32:
            break
    return {
        "same_answer_pairs_checked": checked_pairs,
        "separating_examples_recorded": len(tests),
        "sat_pairs_with_different_future_answers": sum(
            test["future_answers_separate_if_current_answer_is_SAT"] for test in tests
        ),
        "examples": tests,
        "interpretation": (
            "same current SAT bit does not certify interchangeable residual state; "
            "a later restriction can expose a tag clause hidden by that bit"
        ),
    }


def run_collision(hex_digits: int, samples: int, tag_bits: int, repeats: int) -> dict:
    started = time.perf_counter()
    family = verify_family(tag_bits)
    search = collision_search(hex_digits, samples, tag_bits)
    cache = cache_comparison(search, tag_bits, repeats)
    delayed = delayed_history_audit(search, tag_bits)
    return {
        "status": "COMPUTATIONAL",
        "experiment": "short_digest_normalized_residual_cache",
        "parameters": {
            "hex_digits": hex_digits,
            "samples": samples,
            "tag_bits": tag_bits,
            "repeats": repeats,
        },
        "family_verification": family,
        "collision_search": search,
        "cache_comparison": cache,
        "delayed_history_audit": delayed,
        "total_seconds": time.perf_counter() - started,
        "limitations": [
            "bounded chosen-input search, not an asymptotic collision lower bound",
            "truncated SHA-256 is treated empirically as a digest map; no random-oracle theorem is assumed",
            "syntactic normalization renames variables but is not graph-isomorphism or semantic canonicalization",
            "logical payload counters exclude interpreter and hash-table implementation overhead",
            "known SAT answers use the proved structure of this finite family, not a general SAT solver",
        ],
    }


def php(pigeons: int, holes: int) -> Formula:
    variable = lambda pigeon, hole: pigeon * holes + hole + 1
    return canon(
        [
            tuple(variable(pigeon, hole) for hole in range(holes))
            for pigeon in range(pigeons)
        ]
        + [
            (-variable(left, hole), -variable(right, hole))
            for hole in range(holes)
            for left in range(pigeons)
            for right in range(left + 1, pigeons)
        ]
    )


def pigeonhole_audit() -> dict:
    """Contrast legal symmetric histories with arbitrary prefix histories."""
    started = time.perf_counter()

    # Legal placements in PHP(9,8): 8*7*6*5 = 1680 distinct source histories.
    holes = 8
    parent = php(holes + 1, holes)
    legal_normalized = set()
    legal_unnormalized = set()
    legal_count = 0
    for placement in it.permutations(range(holes), 4):
        assignment = {}
        for pigeon, chosen_hole in enumerate(placement):
            for hole in range(holes):
                assignment[pigeon * holes + hole + 1] = hole == chosen_hole
        raw = simplify(restrict(parent, assignment))
        # simplify already normalizes; retain a renamed source-dependent view too.
        legal_normalized.add(raw)
        legal_unnormalized.add(restrict(parent, assignment))
        legal_count += 1

    # Arbitrary Boolean prefixes expose distinct UNSAT residual syntax.  Every
    # residual remains UNSAT because the parent PHP(5,4) is UNSAT.
    small_parent = php(5, 4)
    prefix_variables = list(range(1, 11))
    arbitrary_residuals = set()
    constant_false = 0
    for values in it.product((False, True), repeat=len(prefix_variables)):
        residual = simplify(
            restrict(small_parent, dict(zip(prefix_variables, values)))
        )
        arbitrary_residuals.add(residual)
        constant_false += residual == ((),)

    digest_stats = {}
    for hex_digits in (4, 6, 8):
        counts = Counter(
            digest_int(residual, hex_digits) for residual in arbitrary_residuals
        )
        digest_stats[str(hex_digits)] = {
            "unique_residuals": len(arbitrary_residuals),
            "unique_digests": len(counts),
            "collision_insertions": len(arbitrary_residuals) - len(counts),
            "max_bucket_size": max(counts.values(), default=0),
        }

    return {
        "status": "COMPUTATIONAL",
        "experiment": "pigeonhole_normalized_residuals",
        "legal_history_symmetry": {
            "formula": "PHP(9,8)",
            "fixed_pigeons": 4,
            "source_histories": legal_count,
            "distinct_raw_residuals": len(legal_unnormalized),
            "distinct_normalized_residuals": len(legal_normalized),
            "note": (
                "legal injective placements are symmetric; normalization can merge "
                "many source histories exactly in this case"
            ),
        },
        "arbitrary_prefixes": {
            "formula": "PHP(5,4)",
            "prefix_variables": len(prefix_variables),
            "histories": 1 << len(prefix_variables),
            "constant_false_histories": constant_false,
            "distinct_normalized_residuals": len(arbitrary_residuals),
            "short_digest_statistics": digest_stats,
            "note": (
                "all residuals are UNSAT, so a current-answer-only test cannot detect "
                "short-digest conflation even when normalized formulas differ"
            ),
        },
        "seconds": time.perf_counter() - started,
        "limitations": [
            "finite PHP instances only",
            "normalization is syntactic variable renaming, not semantic equivalence checking",
            "the raw-residual count is source-label-sensitive",
        ],
    }


def install_timeout(seconds: int) -> None:
    def timeout_handler(_signum, _frame):
        raise TimeoutError(f"run exceeded {seconds} seconds")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)


def write_json(path: str, value: dict) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("collision", "pigeonhole"))
    parser.add_argument("--hex-digits", type=int, choices=(4, 6, 8))
    parser.add_argument("--samples", type=int)
    parser.add_argument("--tag-bits", type=int, default=19)
    parser.add_argument("--repeats", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=24)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    install_timeout(args.timeout)
    if args.mode == "collision":
        if args.hex_digits is None or args.samples is None:
            parser.error("collision mode requires --hex-digits and --samples")
        result = run_collision(
            args.hex_digits, args.samples, args.tag_bits, args.repeats
        )
    else:
        result = pigeonhole_audit()
    signal.alarm(0)
    write_json(args.output, result)
    print(json.dumps({
        "output": args.output,
        "status": result["status"],
        "experiment": result["experiment"],
        "seconds": result.get("total_seconds", result.get("seconds")),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
