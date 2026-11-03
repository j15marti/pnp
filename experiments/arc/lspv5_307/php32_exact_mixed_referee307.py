#!/usr/bin/env python3
"""REFEREE307: exact <=9-node relaxed mixed search for PHP(3,2).

The fixed Rmix341 convention follows its original report and REFEREE303/304:
source-independent VARDEF is a charged zero-source-premise definition.  For a
9-source minimally UNSAT formula, source-cycle accounting excludes such a node
from any proof with at most 9 paid nodes.  The remaining cost-9 class is a
single-cycle all-binary DAG; this script exhausts a stronger semantic
RES/AND3/XOR relaxation of that class.
"""
from __future__ import annotations

import functools
import hashlib
import itertools
import json
import os
import resource
import time

N = 6
SOURCES = (
    (1, 2), (3, 4), (5, 6),
    (-1, -3), (-1, -5), (-3, -5),
    (-2, -4), (-2, -6), (-4, -6),
)


def canonical_clause(c):
    s = set(c)
    if 0 in s or any(-x in s for x in s):
        raise ValueError("tautological/noncanonical clause")
    return tuple(sorted(s, key=lambda z: (abs(z), z < 0)))


def clause_tt(c, n=N):
    out = 0
    for a in range(1 << n):
        if any(bool(a & (1 << (abs(l) - 1))) == (l > 0) for l in c):
            out |= 1 << a
    return out


def affine_tt(mask, rhs, n=N):
    out = 0
    for a in range(1 << n):
        if ((a & mask).bit_count() & 1) == rhs:
            out |= 1 << a
    return out


def essential_support(tt, n=N):
    support = 0
    for v in range(n):
        bit = 1 << v
        for a in range(1 << n):
            if a & bit:
                continue
            if ((tt >> a) & 1) != ((tt >> (a | bit)) & 1):
                support |= bit
                break
    return support


def aliases(n=N):
    clauses = {}
    for states in itertools.product((-1, 0, 1), repeat=n):
        if all(x == 0 for x in states):
            c = ()
        else:
            c = tuple((i + 1) if s == 1 else -(i + 1)
                      for i, s in enumerate(states) if s)
        clauses.setdefault(clause_tt(c, n), c)
    affine = {}
    for mask in range(1 << n):
        for rhs in (0, 1):
            affine.setdefault(affine_tt(mask, rhs, n), (mask, rhs))
    return clauses, affine


CLAUSE_ALIAS, AFFINE_ALIAS = aliases()


def all_local_relations():
    out = set()
    for smask in range(1 << N):
        if smask.bit_count() > 3:
            continue
        vs = [v for v in range(N) if smask >> v & 1]
        for allowed in range(1 << (1 << len(vs))):
            lifted = 0
            for a in range(1 << N):
                p = sum(((a >> v) & 1) << j for j, v in enumerate(vs))
                if allowed >> p & 1:
                    lifted |= 1 << a
            out.add(lifted)
    return tuple(sorted(out))


LOCAL_RELATIONS = all_local_relations()
ALL_ASSIGNMENTS = (1 << (1 << N)) - 1


@functools.lru_cache(None)
def free_local_converts(tt):
    """Strong relaxation of paid unary LOCAL-CONVERT.

    For a relation of essential support at most three, grant every Boolean
    relation on ANY at-most-three-variable subset logically implied by it.
    This includes weakenings that introduce an outside variable, contains all
    legal constant-support clause/circuit implications, and is strictly more
    permissive than the fixed rule.
    """
    smask = essential_support(tt)
    if smask.bit_count() > 3:
        return (tt,)
    return tuple(g for g in LOCAL_RELATIONS if tt & (ALL_ASSIGNMENTS ^ g) == 0)


@functools.lru_cache(None)
def combine(a, b):
    out = set()
    ca, cb = CLAUSE_ALIAS.get(a), CLAUSE_ALIAS.get(b)
    if ca is not None and cb is not None:
        for lit in ca:
            if -lit in cb:
                raw = (set(ca) | set(cb)) - {lit, -lit}
                if not any(-x in raw for x in raw):
                    out.add(clause_tt(canonical_clause(raw)))
        for lit in cb:
            if -lit in ca:
                raw = (set(ca) | set(cb)) - {lit, -lit}
                if not any(-x in raw for x in raw):
                    out.add(clause_tt(canonical_clause(raw)))
    aa, ab = AFFINE_ALIAS.get(a), AFFINE_ALIAS.get(b)
    if aa is not None and ab is not None:
        out.add(affine_tt(aa[0] ^ ab[0], aa[1] ^ ab[1]))
    conj = a & b
    if essential_support(conj).bit_count() <= 3:
        out.add(conj)
    return tuple(sorted(out))


def models(clauses):
    return [a for a in range(1 << N) if all((clause_tt(c) >> a) & 1 for c in clauses)]


def source_tree_states():
    m = len(SOURCES)
    bank = [set() for _ in range(1 << m)]
    for i, c in enumerate(SOURCES):
        bank[1 << i].add(clause_tt(c))
    pair_tests = outputs = 0
    for count in range(2, m + 1):
        for whole in range(1, 1 << m):
            if whole.bit_count() != count:
                continue
            least = whole & -whole
            left = (whole - 1) & whole
            while left:
                right = whole ^ left
                if right and (left & least):
                    for a in bank[left]:
                        for b in bank[right]:
                            pair_tests += 1
                            made = combine(a, b)
                            outputs += len(made)
                            bank[whole].update(made)
                left = (left - 1) & whole
    return bank, pair_tests, outputs


def one_unary_tree_search():
    """Exhaust all source-once trees with exactly zero/one strong unary convert."""
    m = len(SOURCES)
    bank0 = [set() for _ in range(1 << m)]
    bank1 = [set() for _ in range(1 << m)]
    for i, c in enumerate(SOURCES):
        t = clause_tt(c)
        bank0[1 << i].add(t)
        bank1[1 << i].update(free_local_converts(t))
    pair_tests = outputs = 0
    for count in range(2, m + 1):
        for whole in range(1, 1 << m):
            if whole.bit_count() != count:
                continue
            least = whole & -whole
            left = (whole - 1) & whole
            while left:
                right = whole ^ left
                if right and (left & least):
                    for a in bank0[left]:
                        for b in bank0[right]:
                            pair_tests += 1
                            made = combine(a, b); outputs += len(made)
                            for z in made:
                                bank0[whole].add(z)
                                bank1[whole].update(free_local_converts(z))
                    for aa, bb in ((bank1[left], bank0[right]),
                                   (bank0[left], bank1[right])):
                        for a in aa:
                            for b in bb:
                                pair_tests += 1
                                made = combine(a, b); outputs += len(made)
                                bank1[whole].update(made)
                left = (left - 1) & whole
    full = (1 << m) - 1
    return {"contradiction_found": 0 in bank1[full],
            "pair_tests": pair_tests, "outputs": outputs,
            "terminal_functions": len(bank1[full])}


def relaxed_unicycle_search():
    m = len(SOURCES)
    full = (1 << m) - 1
    trees, tree_tests, tree_outputs = source_tree_states()
    atoms = [clause_tt(c) for c in SOURCES]
    extend_calls = root_tests = root_outputs = 0

    @functools.lru_cache(None)
    def extend(shared, exclusive_mask):
        nonlocal extend_calls
        extend_calls += 1
        indices = [i for i in range(m) if exclusive_mask >> i & 1]
        tables = [shared] + [atoms[i] for i in indices]
        k = len(tables)
        bank = [set() for _ in range(1 << k)]
        for i, t in enumerate(tables):
            bank[1 << i].add(t)
        for count in range(2, k + 1):
            for whole in range(1, 1 << k):
                if whole.bit_count() != count:
                    continue
                least = whole & -whole
                left = (whole - 1) & whole
                while left:
                    right = whole ^ left
                    if right and (left & least):
                        for a in bank[left]:
                            for b in bank[right]:
                                bank[whole].update(combine(a, b))
                    left = (left - 1) & whole
        return frozenset(bank[-1])

    for shared_mask in range(1, full + 1):
        rest = full ^ shared_mask
        tail_mask = rest
        while True:
            cycle_rest = rest ^ tail_mask
            left_only = cycle_rest
            while True:
                right_only = cycle_rest ^ left_only
                if left_only <= right_only:
                    for shared in trees[shared_mask]:
                        left_outputs = extend(shared, left_only)
                        right_outputs = extend(shared, right_only)
                        for a in left_outputs:
                            for b in right_outputs:
                                root_tests += 1
                                made = combine(a, b)
                                root_outputs += len(made)
                                for cyc in made:
                                    if 0 in extend(cyc, tail_mask):
                                        return {
                                            "contradiction_found": True,
                                            "shared_mask": shared_mask,
                                            "left_only": left_only,
                                            "right_only": right_only,
                                            "tail_mask": tail_mask,
                                            "shared_table": shared,
                                            "left_table": a,
                                            "right_table": b,
                                            "cycle_table": cyc,
                                        }
                if left_only == 0:
                    break
                left_only = (left_only - 1) & cycle_rest
            if tail_mask == 0:
                break
            tail_mask = (tail_mask - 1) & rest
    unary = one_unary_tree_search()
    return {
        "contradiction_found": False,
        "tree_pair_tests": tree_tests,
        "tree_outputs": tree_outputs,
        "tree_terminal_functions": len(trees[full]),
        "tree_contains_false": 0 in trees[full],
        "one_unary_tree": unary,
        "root_pair_tests": root_tests,
        "root_outputs": root_outputs,
        "extend_calls": extend_calls,
        "extend_cache": extend.cache_info()._asdict(),
        "combine_cache": combine.cache_info()._asdict(),
        "free_local_convert_cache": free_local_converts.cache_info()._asdict(),
    }


def resolve(left, right, pivot):
    if pivot not in left or -pivot not in right:
        if -pivot in left and pivot in right:
            return resolve(right, left, pivot)
        raise ValueError("pivot absent")
    raw = (set(left) | set(right)) - {pivot, -pivot}
    if any(-x in raw for x in raw):
        raise ValueError("tautological resolvent")
    return canonical_clause(raw)


def resolution_upper():
    lines = [canonical_clause(c) for c in SOURCES]
    steps = [(1,3,3),(2,4,5),(9,8,4),(11,10,6),(1,6,4),
             (2,7,6),(13,5,3),(15,14,5),(0,12,1),(17,16,2)]
    cert = []
    for left, right, pivot in steps:
        c = resolve(lines[left], lines[right], pivot)
        lines.append(c)
        cert.append({"left": left, "right": right, "pivot": pivot, "clause": c})
    assert lines[-1] == ()
    return cert


def verify_resolution_certificate(cert):
    lines = [canonical_clause(c) for c in SOURCES]
    for step in cert:
        left, right = step["left"], step["right"]
        if not (0 <= left < len(lines) and 0 <= right < len(lines)):
            raise ValueError("forward/bad proof index")
        got = resolve(lines[left], lines[right], step["pivot"])
        if tuple(step["clause"]) != got:
            raise ValueError("wrong claimed resolvent")
        lines.append(got)
    if not cert or lines[-1] != ():
        raise ValueError("no contradiction")
    return True


def parity_cnf(incidences, charges):
    out = []
    for row, rhs in zip(incidences, charges):
        for bits in itertools.product((0, 1), repeat=len(row)):
            if (sum(bits) & 1) != rhs:
                out.append(tuple(-v if b else v for v, b in zip(row, bits)))
    return tuple(out)


def strict_dimacs(text):
    ls = text.splitlines()
    if not ls or len(ls[0].split()) != 4 or ls[0].split()[:2] != ["p", "cnf"]:
        raise ValueError("header")
    n, m = map(int, ls[0].split()[2:])
    if n < 0 or m < 0 or len(ls) != m + 1:
        raise ValueError("counts")
    out = []
    for line in ls[1:]:
        xs = list(map(int, line.split()))
        if not xs or xs[-1] != 0 or 0 in xs[:-1]:
            raise ValueError("terminator")
        c = tuple(xs[:-1])
        if any(abs(x) < 1 or abs(x) > n for x in c):
            raise ValueError("range")
        if len(set(c)) != len(c) or any(-x in c for x in c):
            raise ValueError("canonical")
        out.append(canonical_clause(c))
    return n, tuple(out)


def run():
    started = time.perf_counter()
    assert not models(SOURCES)
    deletions = [len(models(SOURCES[:i] + SOURCES[i+1:])) for i in range(9)]
    signflips = []
    for i, c in enumerate(SOURCES):
        for j in range(len(c)):
            cs = [list(z) for z in SOURCES]
            cs[i][j] *= -1
            signflips.append(len(models(tuple(tuple(z) for z in cs))))
    assert all(deletions) and all(signflips)
    search = relaxed_unicycle_search()
    assert (not search["tree_contains_false"] and not search["contradiction_found"]
            and not search["one_unary_tree"]["contradiction_found"])
    upper = resolution_upper()
    assert verify_resolution_certificate(upper)
    corrupted = []
    for kind in ("pivot", "index", "claim"):
        bad = json.loads(json.dumps(upper))
        if kind == "pivot": bad[0]["pivot"] = 4
        elif kind == "index": bad[3]["left"] = 999
        else: bad[0]["clause"] = [-1, 5]
        try:
            verify_resolution_certificate(bad)
        except (ValueError, IndexError, KeyError, TypeError):
            corrupted.append(kind)
    assert len(corrupted) == 3
    k4 = ((1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6))
    odd_k4, even_k4 = parity_cnf(k4, (1, 0, 0, 0)), parity_cnf(k4, (0, 0, 0, 0))
    parity_controls = {"odd_K4_models": len(models(odd_k4)),
                       "even_K4_models": len(models(even_k4))}
    assert parity_controls == {"odd_K4_models": 0, "even_K4_models": 8}
    malformed = ["", "p cnd 1 1\n1 0\n", "p cnf 1\n1 0\n",
                 "p cnf 1 2\n1 0\n", "p cnf 1 1\n2 0\n",
                 "p cnf 1 1\n1\n", "p cnf 1 1\n1 0 0\n",
                 "p cnf 1 1\n1 -1 0\n", "p cnf 1 1\n1 1 0\n"]
    rejected = 0
    for s in malformed:
        try: strict_dimacs(s)
        except (ValueError, TypeError): rejected += 1
    assert rejected == len(malformed)
    result = {
        "run_id": "PHP32-EXACT-MIXED-REFEREE307",
        "status": {"fixed_calculus": "Rmix341 original/REF303 zero-source-premise VARDEF convention",
                   "minimum": "PROVED/EXACT W=10 under that fixed convention",
                   "finite_search": "COMPUTATIONAL exhaustive stronger relaxation",
                   "binary_VARDEF_alternative": "DIFFERENT/UNFIXED calculus; result does not transfer",
                   "B1": "OPEN", "B2": "OPEN", "B3": "OPEN", "P_vs_NP": "OPEN"},
        "source": {"variables": N, "clauses": SOURCES, "models": 0,
                   "deletion_model_counts": deletions, "sign_flip_model_counts": signflips},
        "topology": {"m": 9, "cost_8": "full binary source-read-once tree",
                     "cost_9": "one unary tree or one unicyclic all-binary DAG; zero-premise DEF costs excess two",
                     "unary_exclusion": "free exact aliases subsume any single LOCAL-CONVERT"},
        "search": search,
        "resolution_upper": upper,
        "corrupted_certificates": {"tested": 3, "rejected": len(corrupted), "kinds": corrupted},
        "exact_cost": 10,
        "malformed": {"tested": len(malformed), "rejected": rejected},
        "parity_controls": parity_controls,
        "resources": {"elapsed_seconds": time.perf_counter()-started,
                      "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      "optimizer_charged_to_W": False},
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256"] = hashlib.sha256(payload).hexdigest()
    return result


if __name__ == "__main__":
    out = os.environ.get("REF307_OUT", "results/raw/arc/2026-11-02_2348_LSPV5_PHP32_EXACT_MIXED_REFEREE307_raw.json")
    result = run()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, sort_keys=True); f.write("\n")
    print(json.dumps({"output": out, "exact_cost": result["exact_cost"],
                      "search": result["search"], "resources": result["resources"]}, indent=2))
