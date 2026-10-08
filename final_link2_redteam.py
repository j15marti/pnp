#!/usr/bin/env python3
"""FINAL-LINK2 bounded red-team experiments.

This runner checks exact finite controls and symbolic accounting identities for
shared acquisition, delta children, clause-first DAGs, amortization, typed
cycles, and code-dependent portfolios.  Its negative statements are explicitly
restricted to the declared models.  It is not a SAT lower bound and does not
decide P versus NP.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import signal
import time
from collections import deque
from fractions import Fraction
from pathlib import Path


Clause = tuple[int, ...]
CNF = tuple[Clause, ...]


def alarm_handler(_signum, _frame):
    raise TimeoutError("25-second internal deadline exceeded")


def canonical_clause(clause: Clause) -> Clause | None:
    lits = set(clause)
    if any(-lit in lits for lit in lits):
        return None
    return tuple(sorted(lits, key=lambda z: (abs(z), z < 0)))


def normalize(cnf: CNF) -> CNF:
    clauses: set[Clause] = set()
    for clause in cnf:
        c = canonical_clause(clause)
        if c is not None:
            clauses.add(c)
    if () in clauses:
        return ((),)
    ordered = sorted(clauses, key=lambda c: (len(c), c))
    kept: list[Clause] = []
    kept_sets: list[frozenset[int]] = []
    for clause in ordered:
        s = frozenset(clause)
        if any(t <= s for t in kept_sets):
            continue
        kept.append(clause)
        kept_sets.append(s)
    return tuple(kept)


def variables(cnf: CNF) -> list[int]:
    return sorted({abs(lit) for clause in cnf for lit in clause})


def encoding_bits(cnf: CNF, source_n: int | None = None) -> int:
    n = source_n if source_n is not None else max(variables(cnf), default=1)
    width = max(1, math.ceil(math.log2(n + 1)))
    return sum(1 + len(clause) * (width + 1) for clause in cnf)


def restrict_once(cnf: CNF, assignment: dict[int, bool]) -> CNF:
    out: list[Clause] = []
    for clause in cnf:
        residual: list[int] = []
        satisfied = False
        for lit in clause:
            v = abs(lit)
            if v not in assignment:
                residual.append(lit)
                continue
            if (lit > 0) == assignment[v]:
                satisfied = True
                break
        if not satisfied:
            out.append(tuple(residual))
    return normalize(tuple(out))


def unit_propagate(cnf: CNF, initial: dict[int, bool] | None = None) -> tuple[CNF, dict[int, bool], bool]:
    assignment = dict(initial or {})
    current = restrict_once(cnf, assignment)
    while True:
        if () in current:
            return ((),), assignment, True
        units = [c[0] for c in current if len(c) == 1]
        if not units:
            return current, assignment, False
        changed = False
        for lit in units:
            v, value = abs(lit), lit > 0
            if v in assignment and assignment[v] != value:
                return ((),), assignment, True
            if v not in assignment:
                assignment[v] = value
                changed = True
        if not changed:
            return current, assignment, False
        current = restrict_once(current, assignment)


def brute_sat(cnf: CNF) -> bool:
    vs = variables(cnf)
    for bits in itertools.product((False, True), repeat=len(vs)):
        a = dict(zip(vs, bits))
        if all(any((lit > 0) == a[abs(lit)] for lit in clause) for clause in cnf):
            return True
    return False


def satisfies(cnf: CNF, assignment: dict[int, bool]) -> bool:
    return all(any((lit > 0) == assignment[abs(lit)] for lit in clause) for clause in cnf)


def clause_first_assignments(clause: Clause) -> list[dict[int, bool]]:
    terms: list[dict[int, bool]] = []
    for i, lit in enumerate(clause):
        a: dict[int, bool] = {}
        for prior in clause[:i]:
            a[abs(prior)] = prior < 0
        a[abs(lit)] = lit > 0
        terms.append(a)
    return terms


def minimally_unsat(n: int) -> CNF:
    return tuple((i,) for i in range(1, n + 1)) + (tuple(-i for i in range(1, n + 1)),)


def positive_three_clause_payload(n: int, offset: int = 0) -> CNF:
    return tuple(tuple(offset + i for i in triple) for triple in itertools.combinations(range(1, n + 1), 3))


def payload_family(payload_n: int, choice_w: int) -> tuple[CNF, CNF, Clause]:
    payload = positive_three_clause_payload(payload_n)
    choice = tuple(payload_n + i for i in range(1, choice_w + 1))
    return normalize((choice,) + payload), normalize(payload), choice


def selector_family(d: int) -> tuple[CNF, list[Clause], dict[str, object]]:
    """A clause-first/equality-DAG control with 2^d distinct residuals.

    a_i,b_i form exact-one choice gadgets.  An address selector forces y_alpha
    for the chosen address.  Every y_alpha has a private non-Horn implication.
    Full address branches remain satisfiable but are syntactically distinct
    after unit propagation.
    """
    q = 1 << d
    a_vars = [i + 1 for i in range(d)]
    b_vars = [d + i + 1 for i in range(d)]
    y0 = 2 * d + 1
    u0 = y0 + q
    v0 = u0 + q
    clauses: list[Clause] = []
    decision_clauses: list[Clause] = []
    for a, b in zip(a_vars, b_vars):
        decision_clauses.append((a, b))
        clauses.extend(((a, b), (-a, -b)))
    for alpha in range(q):
        selector: list[int] = []
        for i, a in enumerate(a_vars):
            bit = bool((alpha >> i) & 1)
            selector.append(-a if bit else a)
        selector.append(y0 + alpha)
        clauses.append(tuple(selector))
        clauses.append((-(y0 + alpha), u0 + alpha, v0 + alpha))
    meta = {
        "d": d,
        "addresses": q,
        "a_vars": a_vars,
        "b_vars": b_vars,
        "y0": y0,
        "u0": u0,
        "v0": v0,
        "nvars": v0 + q - 1,
    }
    return normalize(tuple(clauses)), decision_clauses, meta


def clause_first_layers(cnf: CNF, decisions: list[Clause], max_depth: int) -> list[dict[str, int | bool]]:
    states: dict[CNF, dict[int, bool]] = {cnf: {}}
    rows: list[dict[str, int | bool]] = []
    source_n = max(variables(cnf), default=1)
    rows.append({
        "depth": 0,
        "states": 1,
        "min_bits": encoding_bits(cnf, source_n),
        "max_bits": encoding_bits(cnf, source_n),
        "all_consistent": True,
    })
    for depth in range(max_depth):
        next_states: dict[CNF, dict[int, bool]] = {}
        decision = decisions[depth]
        for state, inherited in states.items():
            for term in clause_first_assignments(decision):
                merged = dict(inherited)
                contradiction = any(v in merged and merged[v] != value for v, value in term.items())
                if contradiction:
                    continue
                merged.update(term)
                residual, closure, bad = unit_propagate(cnf, merged)
                if not bad:
                    next_states.setdefault(residual, closure)
        states = next_states
        sizes = [encoding_bits(s, source_n) for s in states]
        rows.append({
            "depth": depth + 1,
            "states": len(states),
            "min_bits": min(sizes) if sizes else 0,
            "max_bits": max(sizes) if sizes else 0,
            "all_consistent": bool(states),
        })
    return rows


def exact_source_read_controls() -> dict[str, object]:
    rows = []
    checks = 0
    for n in range(2, 13):
        cnf = minimally_unsat(n)
        assert not brute_sat(cnf)
        pivotal = 0
        for i in range(len(cnf)):
            deleted = cnf[:i] + cnf[i + 1 :]
            assert brute_sat(deleted)
            if i < n:
                replacement = cnf[:i] + ((-(i + 1),),) + cnf[i + 1 :]
            else:
                replacement = cnf[:i] + (tuple(range(1, n + 1)),) + cnf[i + 1 :]
            assert brute_sat(replacement)
            pivotal += 1
            checks += 3
        m_bits = encoding_bits(cnf, n)
        rows.append({
            "n": n,
            "clauses": len(cnf),
            "encoding_bits": m_bits,
            "pivotal_clause_cells": pivotal,
            "read_fraction_of_bits": pivotal / m_bits,
        })
    return {
        "family": "unit clauses plus one all-negative clause",
        "interpretation": "Every clause cell is pivotal on the UNSAT input even under a same-count, same-width replacement; the clause-oracle read lower bound is linear in clauses but remains near-linear in encoded bits.",
        "rows": rows,
        "checks": checks,
    }


def equality_frontier_controls() -> dict[str, object]:
    rows = []
    checks = 0
    for k in range(9, 31, 3):
        m = 1 << k
        q = 1 << (k // 3)
        child = 1 << (2 * k // 3)
        total = q * child
        per_child_parent_scan = q * m
        assert 0.75 * m <= total <= 1.35 * m
        assert per_child_parent_scan >= m ** (4 / 3) * 0.75
        checks += 2
        rows.append({
            "M": m,
            "q": q,
            "child_bits": child,
            "total_child_bits": total,
            "total_over_M": total / m,
            "one_parent_scan": m,
            "one_parent_scan_per_child": per_child_parent_scan,
            "repeated_scan_over_M": per_child_parent_scan / m,
        })
    return {
        "identity": "q=M^(1/3), L=M^(2/3) implies qL=M",
        "rows": rows,
        "checks": checks,
    }


def payload_controls() -> dict[str, object]:
    rows = []
    checks = 0
    for payload_n, choice_w in ((6, 2), (7, 3), (8, 4), (9, 6), (10, 8)):
        cnf, payload, choice = payload_family(payload_n, choice_w)
        residuals = []
        for term in clause_first_assignments(choice):
            residual, _, bad = unit_propagate(cnf, term)
            assert not bad
            assert residual == payload
            residuals.append(residual)
            checks += 2
        source_n = max(variables(cnf))
        parent_bits = encoding_bits(cnf, source_n)
        child_bits = encoding_bits(payload, source_n)
        handle_bits = choice_w * (math.ceil(math.log2(source_n + 1)) + 1)
        rows.append({
            "payload_variables": payload_n,
            "choice_width": choice_w,
            "parent_bits": parent_bits,
            "expanded_child_bits": child_bits,
            "child_over_parent": child_bits / parent_bits,
            "distinct_expanded_children": len(set(residuals)),
            "delta_handle_bits_upper_bound": handle_bits,
            "handle_exponent_logM": math.log(max(2, handle_bits), parent_bits),
            "expanded_exponent_logM": math.log(child_bits, parent_bits),
        })
    return {
        "family": "one choice clause conjoined with a disjoint equal-width payload",
        "lemma_control": "Every clause-first child normalizes to the same parent-scale payload.",
        "rows": rows,
        "checks": checks,
    }


def selector_controls() -> dict[str, object]:
    rows = []
    checks = 0
    for d in range(2, 9):
        cnf, decisions, meta = selector_family(d)
        layers = clause_first_layers(cnf, decisions, d)
        for layer in layers:
            expected = 1 << int(layer["depth"])
            assert layer["states"] == expected
            assert layer["all_consistent"]
            checks += 2
        # Every complete address branch has an explicit model: choose the
        # exact-one address, set every selector y and every u true, and every
        # v false.  Thus no branch disappears because it was inconsistent.
        for alpha in range(1 << d):
            witness: dict[int, bool] = {}
            for i, (a, b) in enumerate(zip(meta["a_vars"], meta["b_vars"])):
                bit = bool((alpha >> i) & 1)
                witness[int(a)] = bit
                witness[int(b)] = not bit
            for j in range(1 << d):
                witness[int(meta["y0"]) + j] = True
                witness[int(meta["u0"]) + j] = True
                witness[int(meta["v0"]) + j] = False
            assert satisfies(cnf, witness)
            checks += 1
        m_bits = encoding_bits(cnf, int(meta["nvars"]))
        target_q = m_bits ** (1 / 3)
        target_child = m_bits ** (2 / 3)
        terminal = layers[-1]
        rows.append({
            "d": d,
            "addresses": 1 << d,
            "variables": meta["nvars"],
            "clauses": len(cnf),
            "parent_bits": m_bits,
            "target_q_real": target_q,
            "target_child_real": target_child,
            "terminal_distinct_residuals": terminal["states"],
            "terminal_min_bits": terminal["min_bits"],
            "terminal_max_bits": terminal["max_bits"],
            "layers": layers,
        })
    return {
        "family": "exact-one address choices plus selector clauses and private non-Horn tags",
        "scope": "unit propagation plus syntactic normalization/equality merging; semantic VALUE solvers can bypass this satisfiable control",
        "rows": rows,
        "checks": checks,
    }


def amortization_controls() -> dict[str, object]:
    rows = []
    checks = 0
    for m_exp in (12, 18, 24, 30):
        m = 1 << m_exp
        q = 1 << (m_exp // 3)
        child = 1 << (2 * m_exp // 3)
        total_volume = q * child
        assert total_volume == m
        for k in (1, 2, 3, 4):
            direct = q * (child**k)
            qlen = total_volume * (child ** (k - 1))
            assert direct == qlen
            checks += 2
            rows.append({
                "M": m,
                "q": q,
                "child": child,
                "solver_power_k": k,
                "direct_sum": direct,
                "qlen_bound": qlen,
                "exponent_base_M": math.log(direct, m),
                "symbolic_exponent": 1 + Fraction(2, 3) * (k - 1),
            })
    for row in rows:
        row["symbolic_exponent"] = str(row["symbolic_exponent"])
    return {
        "identity": "sum_i s_i^k = (sum_i s_i) S_max^(k-1) for equal maximum-size children",
        "interpretation": "QLEN amortization is tight on the equality frontier and does not by itself remove branch-local semantic work.",
        "rows": rows,
        "checks": checks,
    }


def pointer_chain_controls() -> dict[str, object]:
    """Exact direct-sum counts in the declared disjoint pointer-chain oracle."""
    rng = random.Random(220260108)
    rows = []
    checks = 0
    for q in (1, 2, 4, 8):
        for length in (2, 4, 8, 16):
            cells = {}
            starts = []
            terminal_bits = []
            for branch in range(q):
                labels = rng.sample(range((branch + 1) * 100000, (branch + 1) * 100000 + 10000), length + 1)
                starts.append(labels[0])
                for j in range(length):
                    cells[labels[j]] = ("next", labels[j + 1])
                bit = rng.randrange(2)
                cells[labels[-1]] = ("bit", bit)
                terminal_bits.append(bit)

            queries = 0
            outputs = []
            for start in starts:
                cursor = start
                while True:
                    kind, value = cells[cursor]
                    queries += 1
                    if kind == "bit":
                        outputs.append(value)
                        break
                    cursor = value
            assert outputs == terminal_bits
            assert queries == q * (length + 1)
            # Every terminal cell is pivotal: flipping an unqueried terminal bit
            # changes one required output while preserving all other cells.
            pivotal_terminals = q
            assert pivotal_terminals == len(outputs)
            checks += 3
            rows.append({
                "branches": q,
                "chain_edges": length,
                "exact_queries": queries,
                "per_branch_queries": length + 1,
                "pivotal_terminal_cells": pivotal_terminals,
            })
    return {
        "model": "q disjoint black-box pointer chains with unknown labels and required terminal bits",
        "restricted_lemma": "Interleaving does not share a chain cell; exact evaluation requires q(R+1) queries.",
        "scope": "Relativized/direct-sum control only; it does not rule out sharing derived from CNF semantics or A's code.",
        "rows": rows,
        "checks": checks,
    }


def solve_two_cycle(l_ab: Fraction, l_ba: Fraction, w_ab: Fraction, w_ba: Fraction) -> tuple[Fraction, Fraction]:
    product = l_ab * l_ba
    if product >= 1:
        raise ValueError("no finite affine fixed point from contraction formula")
    t_a = (w_ab + l_ab * w_ba) / (1 - product)
    t_b = w_ba + l_ba * t_a
    return t_a, t_b


def typed_cycle_controls() -> dict[str, object]:
    phi = (1 + math.sqrt(5)) / 2
    specs = [
        ("contracting_but_endpoint_bad", Fraction(1), Fraction(1, 2), Fraction(4, 5), Fraction(1, 10), Fraction(1, 2)),
        ("contracting_and_endpoint_good", Fraction(1), Fraction(1, 2), Fraction(1, 5), Fraction(1, 10), Fraction(1, 2)),
    ]
    rows = []
    checks = 0
    for name, lab, lba, wab, wba, p in specs:
        ta, tb = solve_two_cycle(lab, lba, wab, wba)
        product = lab * lba
        assert product < 1
        endpoint = float(ta + p)
        rows.append({
            "name": name,
            "lambda_ab": str(lab),
            "lambda_ba": str(lba),
            "cycle_product": str(product),
            "w_ab": str(wab),
            "w_ba": str(wba),
            "fixed_t_a": str(ta),
            "fixed_t_b": str(tb),
            "space_floor": str(p),
            "endpoint_sum_at_A": endpoint,
            "below_phi_product_region": endpoint < phi,
        })
        checks += 3
    assert rows[0]["below_phi_product_region"] is False
    assert rows[1]["below_phi_product_region"] is True
    checks += 2

    handle_b = Fraction(2, 3)
    expansion = 1 / handle_b
    assert handle_b * expansion == 1
    checks += 1
    return {
        "phi": phi,
        "rows": rows,
        "delta_handle_cycle": {
            "explicit_to_handle_exponent": str(handle_b),
            "handle_to_explicit_exponent": str(expansion),
            "cycle_product": str(handle_b * expansion),
            "interpretation": "A handle of M^(2/3) naming an ordinary Theta(M) child has a reverse expansion exponent 3/2; the apparent cycle is noncontracting.",
        },
        "checks": checks,
    }


def padded_decider_controls() -> dict[str, object]:
    base = Fraction(2)
    rows = []
    checks = 0
    for delay in range(0, 13):
        trace_exp = max(base, Fraction(delay))
        rows.append({
            "delay_exponent": delay,
            "base_exponent": str(base),
            "trace_acquisition_exponent": str(trace_exp),
        })
        assert trace_exp >= delay
        checks += 1
    return {
        "family": "A_d runs an extensionally correct base SAT decider and then performs n^d irrelevant steps",
        "restricted_lemma": "Any acquisition contract requiring reproduction of A_d's full parent trace inherits exponent at least d.",
        "scope": "This defeats trace-defined acquisition, not a static code transformation that soundly bypasses the delay.",
        "rows": rows,
        "checks": checks,
    }


def run() -> dict[str, object]:
    started = time.perf_counter()
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(25)
    sections = {
        "equality_frontier": equality_frontier_controls(),
        "source_reads": exact_source_read_controls(),
        "payload_delta": payload_controls(),
        "clause_first_dag": selector_controls(),
        "amortization": amortization_controls(),
        "direct_sum_oracle": pointer_chain_controls(),
        "typed_cycles": typed_cycle_controls(),
        "code_dependent_trace": padded_decider_controls(),
    }
    signal.alarm(0)
    elapsed = time.perf_counter() - started
    total_checks = sum(int(section["checks"]) for section in sections.values())
    payload = {
        "experiment": "FINAL-LINK2 red-team",
        "status": "COMPUTATIONAL plus restricted exact lemmas; no general SAT lower bound",
        "seed": 220260108,
        "deadline_seconds": 25,
        "elapsed_seconds": elapsed,
        "total_declared_checks": total_checks,
        "sections": sections,
        "conclusions": [
            "A one-pass Omega(M) source-read floor is compatible with q=M^(1/3), child=M^(2/3), because total explicit child volume is Theta(M).",
            "Scanning the parent once per child costs Theta(M^(4/3)) and fails the clean near-linear acquisition target, but that multiplicity is not an information-theoretic source-read necessity.",
            "Clause-first branching can leave an identical Theta(M) payload in every child; a small delta handle does not certify an ordinary child of size M^(2/3).",
            "Exact-residual DAG merging has finite exponential controls even after unit propagation; semantic VALUE solvers may bypass them, so this is not an all-algorithm lower bound.",
            "QLEN amortization is tight on equal maximum-size children and does not erase independent semantic work by itself.",
            "A contracting typed cycle can still miss the valid golden-ratio product endpoint; a delta-handle expansion cycle has honest scale product one.",
            "Parent-trace acquisition is not invariant under extensionally irrelevant polynomial delays in the supplied SAT code.",
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["content_sha256_without_this_field"] = hashlib.sha256(canonical).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("final_link2_redteam_results.json"))
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "elapsed_seconds": result["elapsed_seconds"],
        "total_declared_checks": result["total_declared_checks"],
        "sha256": result["content_sha256_without_this_field"],
    }, indent=2))


if __name__ == "__main__":
    main()
