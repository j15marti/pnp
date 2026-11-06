#!/usr/bin/env python3
"""REFEREE374: actual CANON2R LOCAL restoration and global-normalizer audit.

This proves/checks statements only for the frozen proposed CANON2/CANON2R
completion.  It does not authenticate the underspecified historical /341 byte
grammar and it does not prove B3.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import resource
import time
import argparse
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/raw/arc/2026-11-05_1748_LSPV5_REFEREE374_raw.json"
CERTS = ROOT / "results/raw/arc/2026-11-05_1748_LSPV5_REFEREE374_certificates.json"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


C2 = load("ref374_canon2", ROOT / "experiments/arc/lspv5_361/rmix341_canon2_repair_referee361.py")
R2 = load("ref374_canon2r", ROOT / "experiments/arc/lspv5_362/rmix341_raw_affine_firewall_referee362.py")
D372 = load("ref374_def372", ROOT / "experiments/arc/lspv5_372/canon2r_binary_def_normalizer_referee372.py")
R371 = load("ref374_def371", ROOT / "experiments/arc/lspv5_371/boolean_def_to_signed_and_referee371.py")


PADDED = [
    [1, 3, 4], [1, 3, -4], [1, -3, 4], [1, -3, -4],
    [-1, 2, 5], [-1, 2, -5], [-1, -2, 6], [-1, -2, -6],
]
RAW_PADDED = (
    b"c REFEREE374 exact LSPV3-435 padded source\n"
    b"p cnf 6 8\n"
    + b"".join((" ".join(map(str, c)) + " 0\n").encode("ascii") for c in PADDED)
)


def srci(i: int) -> dict:
    return {"src": i, "view": "clause"}


def nodei(i: int, view: str = "clause") -> dict:
    return {"node": i, "view": view}


def res(i: int, left: dict, right: dict, pivot: int, clause: list[int]) -> dict:
    return {"id": i, "rule": "RES", "left": left, "right": right,
            "pivot": pivot, "clause": clause}


def lspv3_435_doc() -> dict:
    """The exact eleven-node shared-port trace printed in LSPV-3/435."""
    source = {"nvars": 6, "clauses": copy.deepcopy(PADDED)}
    nodes = [
        res(0, srci(0), srci(1), 4, [1, 3]),
        res(1, srci(2), srci(3), 4, [1, -3]),
        res(2, srci(4), srci(5), 5, [-1, 2]),
        res(3, srci(6), srci(7), 6, [-1, -2]),
        res(4, nodei(0), nodei(1), 3, [1]),
        {"id": 5, "rule": "AND3", "left": nodei(4), "right": nodei(2),
         "factor": {"support": [1, 2], "truth": [0, 0, 0, 1]}},
        {"id": 6, "rule": "LOCAL", "parent": nodei(5, "factor"),
         "out": {"kind": "clause", "clause": [1, 2]}},
        {"id": 7, "rule": "AND3", "left": nodei(6), "right": nodei(3),
         "factor": {"support": [1, 2], "truth": [0, 1, 1, 0]},
         "affine": {"mask": [1, 2], "rhs": 1}},
        {"id": 8, "rule": "LOCAL", "parent": nodei(5, "factor"),
         "out": {"kind": "clause", "clause": [1, -2]}},
        {"id": 9, "rule": "AND3", "left": nodei(2), "right": nodei(8),
         "factor": {"support": [1, 2], "truth": [1, 0, 0, 1]},
         "affine": {"mask": [1, 2], "rhs": 0}},
        {"id": 10, "rule": "GF2", "left": nodei(7, "affine"),
         "right": nodei(9, "affine"), "affine": {"mask": [], "rhs": 1}},
    ]
    return C2.doc(source, nodes, nodei(10, "affine"))


def raw_for(source: dict, label: str) -> bytes:
    lines = [f"c REFEREE374 {label}", f"p cnf {source['nvars']} {len(source['clauses'])}"]
    lines += [" ".join(map(str, c)) + " 0" for c in source["clauses"]]
    return ("\n".join(lines) + "\n").encode("ascii")


def contradiction_core(start: int = 1) -> dict:
    return {"id": start, "rule": "RES", "left": srci(1), "right": srci(2),
            "pivot": 1, "clause": []}


def clause_restore_doc(d: list[int], c: list[int]) -> tuple[dict, bytes]:
    source = {"nvars": 3, "clauses": [d, [1], [-1]]}
    nodes = [
        {"id": 0, "rule": "LOCAL", "parent": srci(0),
         "out": {"kind": "clause", "clause": c}},
        contradiction_core(1),
    ]
    return C2.doc(source, nodes, nodei(1)), raw_for(source, "clause restoration")


def factor_restore_doc(support: list[int], sub: list[int], full: list[int],
                       mask: list[int], rhs: int) -> tuple[dict, bytes]:
    source = {"nvars": 3, "clauses": [[], [1], [-1]]}
    fsub = {"support": support, "truth": sub}
    ffull = {"support": support, "truth": full}
    nodes = [
        {"id": 0, "rule": "LOCAL", "parent": srci(0),
         "out": {"kind": "factor", "factor": fsub}},
        {"id": 1, "rule": "LOCAL", "parent": nodei(0, "factor"),
         "out": {"kind": "factor", "factor": ffull}},
        {"id": 2, "rule": "AND3", "left": nodei(1, "factor"),
         "right": nodei(1, "factor"), "factor": ffull,
         "affine": {"mask": mask, "rhs": rhs}},
        contradiction_core(3),
    ]
    return C2.doc(source, nodes, nodei(3)), raw_for(source, "factor restoration")


def powerset(xs):
    xs = list(xs)
    for k in range(len(xs) + 1):
        yield from combinations(xs, k)


def check_clause_restoration() -> tuple[int, dict]:
    """All D subset C over three variables, including tautological clauses."""
    universe = [1, -1, 2, -2, 3, -3]
    checked = 0
    sample = None
    # Each literal is absent, in C only, or in D (hence also C): 3^6 cases.
    for code in range(3 ** len(universe)):
        z = code
        c, d = [], []
        for lit in universe:
            state, z = z % 3, z // 3
            if state >= 1:
                c.append(lit)
            if state == 2:
                d.append(lit)
        c = list(C2.simplify_clause(c)); d = list(C2.simplify_clause(d))
        proof, raw = clause_restore_doc(d, c)
        assert R2.check_wrapper(R2.wrap(raw, proof))["accepted"]
        checked += 1
        if sample is None and d == [1] and c == [1, -2]:
            sample = R2.wrap(raw, proof)
    assert checked == 729 and sample is not None
    return checked, sample


def affine_truth(support: list[int], mask: list[int], rhs: int) -> list[int]:
    return [int(sum((bits >> support.index(v)) & 1 for v in mask) % 2 == rhs)
            for bits in range(1 << len(support))]


def check_factor_restoration() -> tuple[int, dict]:
    """All subrelations of every affine relation on every support subset."""
    checked = 0
    sample = None
    for support_tuple in powerset([1, 2, 3]):
        support = list(support_tuple)
        for mask_tuple in powerset(support):
            mask = list(mask_tuple)
            for rhs in (0, 1):
                full = affine_truth(support, mask, rhs)
                true_rows = [i for i, bit in enumerate(full) if bit]
                for keep_bits in range(1 << len(true_rows)):
                    sub = [0] * len(full)
                    for j, row in enumerate(true_rows):
                        sub[row] = (keep_bits >> j) & 1
                    proof, raw = factor_restore_doc(support, sub, full, mask, rhs)
                    assert R2.check_wrapper(R2.wrap(raw, proof))["accepted"]
                    checked += 1
                    if (support == [1, 2] and mask == [1, 2] and rhs == 1
                            and sub == [0, 1, 0, 0]):
                        sample = R2.wrap(raw, proof)
    assert checked == 634 and sample is not None
    return checked, sample


def check_resolution_strengthening() -> int:
    """Exhaustively audit the set-theoretic strengthening simulation on 3 vars."""
    universe = [1, -1, 2, -2, 3, -3]
    checked = 0
    for a_tail in powerset([x for x in universe if x != 1]):
        a = {1, *a_tail}
        for b_tail in powerset([x for x in universe if x != -1]):
            b = {-1, *b_tail}
            old = (a - {1}) | (b - {-1})
            for da in powerset(a):
                da = set(da)
                for db in powerset(b):
                    db = set(db)
                    if 1 in da and -1 in db:
                        got = (da - {1}) | (db - {-1})
                    elif 1 not in da:
                        got = da
                    else:
                        assert -1 not in db
                        got = db
                    assert got <= old
                    checked += 1
    return checked


def check_def_alias_normalization(input_pairs) -> dict:
    """Extend REFEREE372's distinct-input test to all repeated/input orders."""
    templates, _ = R371.bfs_templates()
    source = {"nvars": 2, "clauses": [[1], [-1]]}
    raw = raw_for(source, "DEF repeated-input normalization")
    gates = facets = exact = proper = 0
    max_local_nodes = 0
    for input_a, input_b in input_pairs:
        for table in range(16):
                old_truth = tuple(int(R371.expected(table, bool(a), bool(b)))
                                  for b in (0, 1) for a in (0, 1))
                # First authenticate the old accepted DEF bytes for this alias pattern.
                old = C2.doc(source, [
                    {"id": 0, "rule": "DEF", "var": 3,
                     "inputs": [input_a, input_b], "truth": list(old_truth)},
                    res(1, srci(0), srci(1), 1, []),
                ], nodei(1))
                assert R2.check_wrapper(R2.wrap(raw, old))["accepted"]

                nodes = []
                reps = {R371.A: input_a, R371.B: input_b}
                seed = {}
                next_var = 3
                template = templates[table]
                for p, np, r, nr, h in template:
                    truth = D372.and_truth(np, nr)
                    nid = len(nodes)
                    nodes.append({"id": nid, "rule": "DEF", "var": next_var,
                                  "inputs": [reps[p], reps[r]], "truth": truth})
                    for j, clause in enumerate(C2.def_facets(reps[p], reps[r], next_var,
                                                            tuple(truth))):
                        seed.setdefault(tuple(clause), {"node": nid, "view": "clause", "facet": j})
                    reps[h] = next_var
                    next_var += 1
                output = reps[template[-1][-1]]
                closure, parents = D372.resolution_closure(seed, nodes)
                roots = []
                for target in C2.def_facets(input_a, input_b, output, old_truth):
                    candidates = [c for c in closure if set(c).issubset(target)]
                    assert candidates, (input_a, input_b, table, target)
                    representative = min(candidates,
                                         key=lambda c: (len(c), D372.ancestry_nodes(c, parents)))
                    roots.append(closure[representative])
                    exact += int(tuple(target) in closure)
                    proper += int(tuple(target) not in closure)
                    facets += 1
                final_id = len(nodes)
                nodes.append(res(final_id, srci(0), srci(1), 1, []))
                trimmed, root_refs = D372.trim_and_renumber(nodes, roots + [nodei(final_id)])
                proof = C2.doc(source, trimmed, root_refs[-1])
                stats = R2.check_wrapper(R2.wrap(raw, proof))
                assert stats["accepted"]
                local_nodes = stats["paid_nodes"] - 1
                max_local_nodes = max(max_local_nodes, local_nodes)
                assert local_nodes <= 11
                gates += 1
    assert gates == 16 * len(input_pairs) and facets == 64 * len(input_pairs)
    assert exact + proper == facets
    return {"accepted_old_and_normalized_gates": gates, "facets": facets,
            "exact_representatives": exact, "proper_subclause_representatives": proper,
            "maximum_local_nodes_excluding_validation_core": max_local_nodes}


def span(nodes: list[dict]) -> int:
    depths = []
    for n in nodes:
        ps = []
        for key in ("left", "right", "parent"):
            r = n.get(key)
            if isinstance(r, dict) and "node" in r:
                ps.append(r["node"])
        depths.append(1 + max((depths[p] for p in ps), default=0))
    return max(depths, default=0)


def expect_reject(fn, needle: str) -> str:
    try:
        fn()
    except (C2.Reject, R2.RawReject) as exc:
        assert needle in str(exc), (needle, str(exc))
        return "REJECTED: " + str(exc)
    raise AssertionError("hostile control accepted")


def hostile_controls(base: dict, wrapped: dict, factor_sample: dict) -> dict:
    bad_imp = copy.deepcopy(factor_sample["proof"])
    # Reverse the valid inclusion: XOR=1 does not imply the strict singleton row.
    bad_imp["nodes"][0]["out"]["factor"]["truth"] = [0, 1, 1, 0]
    bad_imp["nodes"][1]["out"]["factor"]["truth"] = [0, 1, 0, 0]
    false_local = expect_reject(lambda: C2.Checker(bad_imp, bad_imp["source"]).run(),
                                "false LOCAL implication")

    bad_aff = copy.deepcopy(base)
    bad_aff["nodes"][7]["affine"]["rhs"] = 0
    false_affine = expect_reject(lambda: C2.Checker(bad_aff, bad_aff["source"]).run(),
                                 "false affine annotation")

    scoped = copy.deepcopy(base)
    scoped["nodes"][6]["context"] = [1]
    scope_payload = expect_reject(lambda: C2.Checker(scoped, scoped["source"]).run(),
                                  "wrong keys")

    aux_source = {"nvars": 1, "clauses": [[1], [-1]]}
    aux = C2.doc(aux_source, [
        {"id": 0, "rule": "DEF", "var": 2, "inputs": [1, 1], "truth": [0, 0, 0, 1]},
        {"id": 1, "rule": "LOCAL", "parent": {"node": 0, "view": "clause", "facet": 0},
         "out": {"kind": "clause", "clause": [1]}},
    ], nodei(1))
    aux_reject = expect_reject(lambda: C2.Checker(aux, aux_source).run(), "LOCAL support")

    bad_hash = copy.deepcopy(wrapped); bad_hash["source_raw_sha256"] = "0" * 64
    hash_reject = expect_reject(lambda: R2.check_wrapper(bad_hash), "raw hash mismatch")

    malformed = RAW_PADDED.replace(b"p cnf 6 8", b"p cnf 6 9")
    malformed_reject = expect_reject(lambda: R2.parse_strict_dimacs(malformed),
                                     "clause count mismatch")

    sat = {"nvars": 1, "clauses": [[1], [1]]}
    sat_doc = C2.doc(sat, [res(0, srci(0), srci(1), 1, [])], nodei(0))
    sat_reject = expect_reject(lambda: C2.Checker(sat_doc, sat).run(),
                               "not an oriented resolvent")
    return {"false_LOCAL_direction": false_local, "false_affine": false_affine,
            "branch_context_payload": scope_payload, "auxiliary_LOCAL_boundary": aux_reject,
            "raw_hash": hash_reject, "malformed_source": malformed_reject,
            "SAT_source_fake_refutation": sat_reject}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--alias-pair", choices=["11", "12", "21", "22"])
    args = ap.parse_args()
    if args.alias_pair:
        pair = (int(args.alias_pair[0]), int(args.alias_pair[1]))
        started_chunk = time.perf_counter()
        chunk = check_def_alias_normalization([pair])
        chunk["input_pair"] = list(pair)
        chunk["producer_seconds"] = time.perf_counter() - started_chunk
        path = OUT.with_name(OUT.stem + f"_def_alias_{args.alias_pair}.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(chunk, indent=2, sort_keys=True) + "\n")
        print(json.dumps(chunk, indent=2, sort_keys=True))
        return
    started = time.perf_counter()
    parsed = R2.parse_strict_dimacs(RAW_PADDED)
    assert parsed == {"nvars": 6, "clauses": PADDED}

    peer = lspv3_435_doc()
    peer_stats = C2.Checker(peer, parsed).run()
    peer_wrap = R2.wrap(RAW_PADDED, peer)
    peer_wrap_stats = R2.check_wrapper(peer_wrap)
    assert peer_stats["paid_nodes"] == 11 and span(peer["nodes"]) == 6

    clause_count, clause_sample = check_clause_restoration()
    factor_count, factor_sample = check_factor_restoration()
    res_count = check_resolution_strengthening()
    chunks = []
    for pair in ("11", "12", "21", "22"):
        path = OUT.with_name(OUT.stem + f"_def_alias_{pair}.json")
        chunks.append(json.loads(path.read_text()))
    def_aliases = {
        "accepted_old_and_normalized_gates": sum(x["accepted_old_and_normalized_gates"] for x in chunks),
        "facets": sum(x["facets"] for x in chunks),
        "exact_representatives": sum(x["exact_representatives"] for x in chunks),
        "proper_subclause_representatives": sum(x["proper_subclause_representatives"] for x in chunks),
        "maximum_local_nodes_excluding_validation_core": max(x["maximum_local_nodes_excluding_validation_core"] for x in chunks),
        "chunk_seconds": {"".join(map(str, x["input_pair"])): x["producer_seconds"] for x in chunks},
    }
    assert def_aliases["accepted_old_and_normalized_gates"] == 64
    assert def_aliases["facets"] == 256
    hostile = hostile_controls(peer, peer_wrap, factor_sample)

    # REFEREE372 gives <=3 replacement DEF owners and <=2 RES ancestors per
    # each of four facets, hence <=11 distinct nodes per old DEF owner.
    bound = {
        "old_counts": "d DEF, r RES, a AND3, l LOCAL, g GF2; q=d+r+a+l+g",
        "translated_nodes": "<=11d+r+3a+2l+g",
        "linear_bound": "<=11q",
        "why": "DEF <=3+4*2; RES <=1; AND3 <=2 clause restores+1 replay; LOCAL <=1 restore+1 replay; GF2 <=1",
    }
    elapsed = time.perf_counter() - started
    payload = {
        "artifact": "REFEREE374", "status": "PASS",
        "scope": "frozen proposed CANON2/CANON2R; historical /341 serialization remains unauthenticated",
        "peer_435_actual_bytes": {"checker": peer_stats, "wrapper": peer_wrap_stats,
                                  "distinct_nodes": 11, "span": 6},
        "exhaustive_actual_checker": {
            "clause_subclause_LOCAL_pairs": clause_count,
            "affine_factor_subrelation_LOCAL_AND3_pairs": factor_count,
            "total_wrapped_certificates": clause_count + factor_count,
        },
        "resolution_strengthening_control": {"finite_set_cases": res_count,
                                               "symbolic_statement": "one RES or a pivot-free parent yields a subclause of the old resolvent"},
        "DEF_alias_normalization": def_aliases,
        "global_normalization_bound": bound,
        "hostile_controls": hostile,
        "status_ledger": {
            "LSPV3_435_actual_CANON2R_bytes": "COMPUTATIONAL_ACCEPTED",
            "frozen_CANON2R_whole_proof_normalizer": "PROVED_EXACT_FROM_REFEREE372_PLUS_RULE_INDUCTION",
            "historical_Rmix341_byte_grammar": "OPEN_UNDERSPECIFIED",
            "superpolynomial_full_mixed_Wbar": "OPEN",
            "same_R_B3": "OPEN",
            "P_vs_NP": "OPEN",
        },
        "resource_ledger": {
            "producer_seconds": elapsed,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "logical_nodes_are_not_physical_time": True,
            "construction_search_parsing_hashing_serialization_verification_charged_here": True,
            "logical_xor_trace": "not used",
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    CERTS.write_text(json.dumps({
        "artifact": "REFEREE374-CERTIFICATES",
        "lspv3_435_actual_canon2r": peer_wrap,
        "clause_restore_sample": clause_sample,
        "affine_restore_sample": factor_sample,
    }, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
