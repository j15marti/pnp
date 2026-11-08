#!/usr/bin/env python3
"""Independent strict semantic replay and mutation audit for LSPV-3/512.

This is not the unavailable historical R_mix341 byte checker.  It reconstructs
the exact declared SOURCE/AND3/XOR/LOCAL/RES semantics used by peer /512.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import resource
import time
from collections import Counter


CALCULUS = "Rmix341-DECLARED-SEMANTIC-SUBLANGUAGE; NOT HISTORICAL BYTE CHECKER"
TOP_KEYS = {
    "name", "calculus", "source_dimacs", "source_sha256", "graph",
    "nodes", "root", "expected",
}


class Reject(ValueError):
    pass


def fail(message):
    raise Reject(message)


def parse_dimacs(raw):
    lines = raw.splitlines()
    if not lines or lines[0] != "p cnf 24 64":
        fail("noncanonical DIMACS header")
    clauses = []
    for line in lines[1:]:
        toks = line.split()
        if not toks or toks[-1] != "0":
            fail("bad DIMACS line")
        lits = [int(x) for x in toks[:-1]]
        if len(lits) != 3 or any(x == 0 or abs(x) > 24 for x in lits):
            fail("source must be strict width-three CNF")
        if len({abs(x) for x in lits}) != 3:
            fail("source clause has repeated variable")
        clauses.append(lits)
    if len(clauses) != 64:
        fail("wrong clause count")
    canonical = "p cnf 24 64\n" + "".join(
        " ".join(map(str, clause)) + " 0\n" for clause in clauses
    )
    if raw != canonical:
        fail("noncanonical source bytes")
    return clauses


def clause_factor(clause):
    support = tuple(sorted(abs(x) for x in clause))
    allowed = set()
    for bits in itertools.product((0, 1), repeat=len(support)):
        env = dict(zip(support, bits))
        if any((env[abs(lit)] == 1) if lit > 0 else (env[abs(lit)] == 0)
               for lit in clause):
            allowed.add(bits)
    return {"support": support, "allowed": allowed, "clause": tuple(clause)}


def row_factor(mask, rhs):
    support = tuple(sorted(mask))
    allowed = {
        bits for bits in itertools.product((0, 1), repeat=len(support))
        if sum(bits) % 2 == rhs
    }
    return {"support": support, "allowed": allowed, "row": (frozenset(mask), rhs)}


def as_factor(obj):
    if "support" in obj:
        return obj
    mask, rhs = obj["row"]
    return row_factor(mask, rhs)


def conjunction(a, b):
    a, b = as_factor(a), as_factor(b)
    support = tuple(sorted(set(a["support"]) | set(b["support"])))
    if len(support) > 3:
        fail("AND3 combined original support exceeds three")
    allowed = set()
    for bits in itertools.product((0, 1), repeat=len(support)):
        env = dict(zip(support, bits))
        aa = tuple(env[x] for x in a["support"]) in a["allowed"]
        bb = tuple(env[x] for x in b["support"]) in b["allowed"]
        if aa and bb:
            allowed.add(bits)
    return {"support": support, "allowed": allowed}


def implies_clause(factor, clause):
    factor = as_factor(factor)
    cvars = {abs(x) for x in clause}
    if not cvars <= set(factor["support"]):
        return False
    for bits in factor["allowed"]:
        env = dict(zip(factor["support"], bits))
        if not any((env[abs(lit)] == 1) if lit > 0 else (env[abs(lit)] == 0)
                   for lit in clause):
            return False
    return True


def gf2_solve(num_vars, equations):
    basis = {}
    for mask, rhs in equations:
        while mask:
            pivot = (mask & -mask).bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (mask, rhs & 1)
                break
            row, bit = basis[pivot]
            mask ^= row
            rhs ^= bit
        else:
            if rhs & 1:
                return False
    return True


def validate_graph_and_source(packet, clauses):
    graph = packet["graph"]
    if set(graph) != {"vertices", "edges", "charges"}:
        fail("graph schema")
    if graph["vertices"] != 16 or len(graph["edges"]) != 24:
        fail("graph size")
    edges = []
    for edge in graph["edges"]:
        if not (isinstance(edge, list) and len(edge) == 2):
            fail("edge syntax")
        u, v = edge
        if not (0 <= u < v < 16 or 0 <= v < u < 16) or u == v:
            fail("edge endpoint")
        edges.append((u, v))
    if len({tuple(sorted(e)) for e in edges}) != 24:
        fail("duplicate graph edge")
    charges = graph["charges"]
    if len(charges) != 16 or any(x not in (0, 1) for x in charges):
        fail("charge vector")
    if sum(charges) % 2 != 1:
        fail("charge must be odd")
    inc = {v: [] for v in range(16)}
    for eid, (u, v) in enumerate(edges, 1):
        inc[u].append(eid)
        inc[v].append(eid)
    if any(len(inc[v]) != 3 for v in range(16)):
        fail("graph not cubic")
    expected = []
    owners = []
    wrong_bits = []
    for v in range(16):
        for bits in itertools.product((0, 1), repeat=3):
            if sum(bits) % 2 == charges[v]:
                continue
            expected.append([-e if b else e for e, b in zip(inc[v], bits)])
            owners.append(v)
            wrong_bits.append(bits)
    if clauses != expected:
        fail("source bytes disagree with graph/charge encoding")
    return edges, charges, inc, owners, wrong_bits


def resolution(c1, c2, pivot):
    if pivot <= 0:
        fail("pivot must be positive variable id")
    if pivot in c1 and -pivot in c2:
        left, right = c1, c2
    elif -pivot in c1 and pivot in c2:
        left, right = c2, c1
    else:
        fail("RES parents lack complementary named pivot")
    out = [x for x in left if x != pivot] + [x for x in right if x != -pivot]
    if len(set(out)) != len(out):
        fail("duplicate literal in resolvent")
    if any(-x in out for x in out):
        fail("tautological resolvent")
    return out


def verify(packet):
    if set(packet) != TOP_KEYS:
        fail("top-level schema")
    if packet["name"] != "LSPV3-512-bridge-star" or packet["calculus"] != CALCULUS:
        fail("identity/calculus tag")
    raw = packet["source_dimacs"]
    if hashlib.sha256(raw.encode()).hexdigest() != packet["source_sha256"]:
        fail("source hash")
    clauses = parse_dimacs(raw)
    edges, charges, inc, owners, wrong_bits = validate_graph_and_source(packet, clauses)
    source = {f"S{i}": clause_factor(c) for i, c in enumerate(clauses)}
    objs, depths, parents_by_id = {}, {}, {}
    rule_counts = Counter()
    for i, node in enumerate(packet["nodes"]):
        if not isinstance(node, dict):
            fail("node not object")
        if node.get("id") != f"N{i}":
            fail("node id/ordering")
        rule = node.get("rule")
        schemas = {
            "AND3": ({"id", "rule", "parents"}, {"row"}),
            "XOR": ({"id", "rule", "parents"}, set()),
            "LOCAL": ({"id", "rule", "parents", "clause"}, set()),
            "RES": ({"id", "rule", "parents", "pivot", "clause"}, set()),
        }
        if rule not in schemas:
            fail("unknown rule")
        required, optional = schemas[rule]
        if not required <= set(node) or not set(node) <= required | optional:
            fail("node schema")
        parents = node["parents"]
        arity = 1 if rule == "LOCAL" else 2
        if not isinstance(parents, list) or len(parents) != arity:
            fail("rule arity")
        pobj = []
        for parent in parents:
            if parent in source:
                pobj.append(source[parent])
            elif parent in objs:
                pobj.append(objs[parent])
            else:
                fail("missing or forward parent")
        if len(set(parents)) != len(parents):
            fail("repeated parent")
        if rule == "AND3":
            obj = conjunction(pobj[0], pobj[1])
            if "row" in node:
                row = node["row"]
                if set(row) != {"mask", "rhs"}:
                    fail("row schema")
                mask, rhs = row["mask"], row["rhs"]
                if (not isinstance(mask, list) or len(mask) != len(set(mask))
                        or any(not isinstance(x, int) or not 1 <= x <= 24 for x in mask)
                        or rhs not in (0, 1)):
                    fail("row payload")
                rf = row_factor(mask, rhs)
                if obj["support"] != rf["support"] or obj["allowed"] != rf["allowed"]:
                    fail("AND3 row annotation not exactly equivalent")
                obj["row"] = (frozenset(mask), rhs)
        elif rule == "XOR":
            if "row" not in pobj[0] or "row" not in pobj[1]:
                fail("XOR parent is not an authenticated row")
            m1, r1 = pobj[0]["row"]
            m2, r2 = pobj[1]["row"]
            obj = {"row": (m1 ^ m2, r1 ^ r2)}
        elif rule == "LOCAL":
            clause = node["clause"]
            if (not isinstance(clause, list) or any(not isinstance(x, int) or x == 0 for x in clause)
                    or len({abs(x) for x in clause}) != len(clause)):
                fail("LOCAL clause syntax")
            if not implies_clause(pobj[0], clause):
                fail("LOCAL implication false")
            obj = clause_factor(clause)
        else:
            clause = node["clause"]
            if not isinstance(clause, list):
                fail("RES clause syntax")
            derived = resolution(list(pobj[0]["clause"]), list(pobj[1]["clause"]), node["pivot"])
            if derived != clause:
                fail("RES explicit clause differs from oriented resolvent")
            obj = clause_factor(clause)
        nid = node["id"]
        objs[nid] = obj
        parents_by_id[nid] = parents
        depths[nid] = 1 + max((depths.get(p, 0) for p in parents), default=0)
        rule_counts[rule] += 1
    root = packet["root"]
    if root not in objs or objs[root].get("clause") != ():
        fail("root is not authenticated empty clause")
    expected = packet["expected"]
    if set(expected) != {"paid", "and3", "xor", "local", "res", "used_sources", "all_sources"}:
        fail("expected schema")
    actual_counts = {
        "paid": len(packet["nodes"]), "and3": rule_counts["AND3"],
        "xor": rule_counts["XOR"], "local": rule_counts["LOCAL"],
        "res": rule_counts["RES"], "all_sources": len(clauses),
    }
    used, todo = set(), [root]
    while todo:
        cur = todo.pop()
        for p in parents_by_id.get(cur, []):
            if p.startswith("S"):
                used.add(int(p[1:]))
            else:
                todo.append(p)
    actual_counts["used_sources"] = len(used)
    if expected != actual_counts:
        fail(f"expected ledger mismatch: {actual_counts}")
    essential = []
    for ci, (owner, bits) in enumerate(zip(owners, wrong_bits)):
        equations = []
        for eid, bit in zip(inc[owner], bits):
            equations.append((1 << (eid - 1), bit))
        for v in range(16):
            if v != owner:
                equations.append((sum(1 << (eid - 1) for eid in inc[v]), charges[v]))
        if gf2_solve(24, equations):
            essential.append(ci)
    if used != set(essential) or len(essential) != 55:
        fail("trace sources differ from independently recomputed essential core")
    return {
        "paid": len(packet["nodes"]),
        "depth": depths[root],
        "rule_counts": dict(sorted(rule_counts.items())),
        "used_sources": len(used),
        "essential_sources": len(essential),
        "source_sha256": packet["source_sha256"],
    }


def mutations(packet):
    def case(name, edit):
        q = copy.deepcopy(packet)
        edit(q)
        return name, q

    first_row = next(i for i, n in enumerate(packet["nodes"]) if "row" in n)
    first_xor = next(i for i, n in enumerate(packet["nodes"]) if n["rule"] == "XOR")
    first_local = next(i for i, n in enumerate(packet["nodes"]) if n["rule"] == "LOCAL")
    first_res = next(i for i, n in enumerate(packet["nodes"]) if n["rule"] == "RES")
    return [
        case("source_byte_same_hash", lambda q: q.__setitem__("source_dimacs", q["source_dimacs"].replace("1 9 17 0", "1  9 17 0", 1))),
        case("source_reencoded_rehashed", lambda q: (q.__setitem__("source_dimacs", q["source_dimacs"].replace("1 9 17 0", "1  9 17 0", 1)), q.__setitem__("source_sha256", hashlib.sha256(q["source_dimacs"].encode()).hexdigest()))),
        case("false_source_hash", lambda q: q.__setitem__("source_sha256", "0" * 64)),
        case("false_calculus_tag", lambda q: q.__setitem__("calculus", "R_mix341-HISTORICAL")),
        case("unknown_top_member", lambda q: q.__setitem__("proof", True)),
        case("duplicate_node_id", lambda q: q["nodes"][1].__setitem__("id", "N0")),
        case("forward_parent", lambda q: q["nodes"][0].__setitem__("parents", ["N56", "S1"])),
        case("missing_source", lambda q: q["nodes"][0].__setitem__("parents", ["S64", "S1"])),
        case("row_rhs_flip", lambda q: q["nodes"][first_row]["row"].__setitem__("rhs", 1 - q["nodes"][first_row]["row"]["rhs"])),
        case("xor_nonrow_parent", lambda q: q["nodes"][first_xor].__setitem__("parents", ["S0", q["nodes"][first_xor]["parents"][1]])),
        case("local_sign_flip", lambda q: q["nodes"][first_local].__setitem__("clause", [-q["nodes"][first_local]["clause"][0]])),
        case("res_pivot_wrong", lambda q: q["nodes"][first_res].__setitem__("pivot", 24)),
        case("res_clause_wrong", lambda q: q["nodes"][first_res].__setitem__("clause", q["nodes"][first_res]["clause"] + [24])),
        case("wrong_root", lambda q: q.__setitem__("root", "N55")),
        case("false_paid_ledger", lambda q: q["expected"].__setitem__("paid", 56)),
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("packet")
    args = ap.parse_args()
    started = time.perf_counter()
    with open(args.packet, encoding="utf-8") as f:
        packet = json.load(f, object_pairs_hook=lambda pairs: (
            (_ for _ in ()).throw(Reject("duplicate JSON member"))
            if len({k for k, _ in pairs}) != len(pairs) else dict(pairs)
        ), parse_constant=lambda x: (_ for _ in ()).throw(Reject(f"nonfinite JSON {x}")))
    baseline = verify(packet)
    rejected = {}
    for name, mutant in mutations(packet):
        try:
            verify(mutant)
        except Reject as exc:
            rejected[name] = str(exc)
        else:
            fail(f"mutation accepted: {name}")
    out = {
        "experiment": "LSPV5_445_PEER512_STRICT_REPLAY",
        "status": "COMPUTATIONAL_INDEPENDENT_DECLARED_SEMANTIC_REPLAY_NOT_HISTORICAL_CHECKER",
        "baseline": baseline,
        "mutations_rejected": rejected,
        "mutation_count": len(rejected),
        "publication_gap": (
            "Peer repository publishes compact producer, report and raw summary, "
            "but not the claimed full independent checkers or complete certificate."
        ),
        "b3": "OPEN",
        "historical_R_mix341": "OPEN",
        "elapsed_seconds": time.perf_counter() - started,
        "maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
