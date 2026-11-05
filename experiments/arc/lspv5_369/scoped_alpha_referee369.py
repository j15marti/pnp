#!/usr/bin/env python3
"""REFEREE369: owner-qualified branch-local DEF names and alpha compilation.

This is a declared comparison grammar, not the authoritative historical
R_mix341 checker.  It tests a narrow repair to REFEREE368: a cosmetic DEF
alias may repeat in incompatible branches, but the semantic output is the
owner node and every use is owner-qualified.  Local outputs may only be used
in contexts extending their owner's context.
"""

from __future__ import annotations

import copy
import hashlib
import itertools
import json
import resource
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
RAW = ROOT / "results/raw/arc/2026-11-05_1248_LSPV5_REFEREE369_raw.json"


def lit_key(lit: str):
    neg = lit.startswith("~")
    atom = lit[1:] if neg else lit
    if len(atom) < 2 or atom[0] not in "xd" or not atom[1:].isdigit():
        raise ValueError("unqualified or malformed literal")
    ident = int(atom[1:])
    if ident <= 0:
        raise ValueError("nonpositive identifier")
    return (atom[0], ident, neg)


def negate(lit: str):
    lit_key(lit)
    return lit[1:] if lit.startswith("~") else "~" + lit


def canon_clause(xs):
    xs = [str(x) for x in xs]
    keys = [lit_key(x) for x in xs]
    if len(set(keys)) != len(keys):
        raise ValueError("duplicate literal")
    if any(negate(x) in xs for x in xs):
        raise ValueError("tautological clause")
    return sorted(xs, key=lit_key)


def canon_ctx(xs):
    xs = [int(x) for x in xs]
    if 0 in xs or len(set(xs)) != len(xs) or any(-x in xs for x in xs):
        raise ValueError("malformed context")
    return sorted(xs, key=lambda x: (abs(x), x < 0))


def parse_dimacs(text):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.startswith("c")]
    if not lines:
        raise ValueError("missing strict header")
    h = lines[0].split()
    if len(h) != 4 or h[:2] != ["p", "cnf"]:
        raise ValueError("bad strict header")
    nvars, nclauses = int(h[2]), int(h[3])
    clauses = []
    for ln in lines[1:]:
        vals = [int(x) for x in ln.split()]
        if not vals or vals[-1] != 0 or 0 in vals[:-1]:
            raise ValueError("bad clause terminator")
        if any(abs(x) > nvars for x in vals[:-1]):
            raise ValueError("source literal out of range")
        clauses.append(canon_clause([("" if x > 0 else "~") + f"x{abs(x)}" for x in vals[:-1]]))
    if len(clauses) != nclauses:
        raise ValueError("clause count mismatch")
    return nvars, clauses


def atom_value(atom: str, assignment):
    kind, ident, _ = lit_key(atom)
    return assignment[(kind, ident)]


def clause_true(clause, assignment):
    for lit in clause:
        kind, ident, neg = lit_key(lit)
        if assignment[(kind, ident)] != neg:
            return True
    return False


def model_count(nvars, clauses):
    count = 0
    for bits in itertools.product((False, True), repeat=nvars):
        a = {("x", i + 1): bits[i] for i in range(nvars)}
        count += all(clause_true(c, a) for c in clauses)
    return count


def context_subset(parent, child):
    return set(parent).issubset(child)


def visible_defs(clause, consumer_ctx, records, consumer_idx, allow_self=False):
    for lit in clause:
        kind, owner, _ = lit_key(lit)
        if kind != "d":
            continue
        if owner > consumer_idx or (owner == consumer_idx and not allow_self):
            raise ValueError("forward/self definition reference")
        if owner == consumer_idx:
            continue
        if records[owner]["rule"] != "DEF":
            raise ValueError("definition owner is not DEF")
        if not context_subset(records[owner]["ctx"], consumer_ctx):
            raise ValueError("branch-local definition not visible in consumer context")


def definition_exact(owner, inputs, table, facets):
    if len(inputs) != 2 or len(table) != 4 or any(ch not in "01" for ch in table):
        return False
    atoms = sorted({lit_key(x)[:2] for x in inputs} | {("d", owner)})
    for bits in itertools.product((False, True), repeat=len(atoms)):
        a = dict(zip(atoms, bits))
        in_values = []
        for x in inputs:
            kind, ident, neg = lit_key(x)
            in_values.append(a[(kind, ident)] != neg)
        intended = table[2 * int(in_values[0]) + int(in_values[1])] == "1"
        relation = a[("d", owner)] == intended
        cnf = all(clause_true(f, a) for f in facets)
        if relation != cnf:
            return False
    return True


def resolve(c1, c2, pivot):
    lit_key(pivot)
    if pivot not in c1 or negate(pivot) not in c2:
        raise ValueError("oriented pivot absent")
    return canon_clause([x for x in c1 if x != pivot] + [x for x in c2 if x != negate(pivot)])


def get_parent(ref, idx, records, ops):
    if isinstance(ref, int):
        node, facet = ref, None
    elif isinstance(ref, dict) and set(ref) == {"node", "facet"}:
        node, facet = int(ref["node"]), int(ref["facet"])
    else:
        raise ValueError("malformed parent reference")
    if not 0 <= node < idx:
        raise ValueError("bad/cyclic parent")
    rec = records[node]
    if facet is None:
        if rec["rule"] == "DEF":
            raise ValueError("DEF parent requires positional facet")
        clause = rec["clause"]
    else:
        if rec["rule"] != "DEF" or not 0 <= facet < len(rec["facets"]):
            raise ValueError("bad DEF facet reference")
        clause = rec["facets"][facet]
    ops["parent_reads"] += 1
    return rec["ctx"], clause, node


def trace_fixture():
    return {
        "format": "REFEREE369-scoped-owner-v1",
        "source_dimacs": "p cnf 2 3\n1 2 0\n-1 2 0\n-2 0\n",
        "nodes": [
            {"rule": "SRC", "ctx": [], "source": 0, "clause": ["x1", "x2"]},
            {"rule": "SRC", "ctx": [], "source": 1, "clause": ["~x1", "x2"]},
            {"rule": "SRC", "ctx": [], "source": 2, "clause": ["~x2"]},
            {"rule": "ASSUME", "ctx": [1], "clause": ["x1"]},
            {"rule": "RES", "ctx": [1], "parents": [3, 1], "pivot": "x1", "clause": ["x2"]},
            {"rule": "DEF", "ctx": [1], "alias": "z", "inputs": ["x2", "x2"], "table": "0001",
             "facets": [["~d5", "x2"], ["d5", "~x2"]]},
            {"rule": "RES", "ctx": [1], "parents": [4, {"node": 5, "facet": 1}], "pivot": "x2", "clause": ["d5"]},
            {"rule": "RES", "ctx": [1], "parents": [6, {"node": 5, "facet": 0}], "pivot": "d5", "clause": ["x2"]},
            {"rule": "ASSUME", "ctx": [-1], "clause": ["~x1"]},
            {"rule": "RES", "ctx": [-1], "parents": [0, 8], "pivot": "x1", "clause": ["x2"]},
            {"rule": "DEF", "ctx": [-1], "alias": "z", "inputs": ["x2", "x2"], "table": "0001",
             "facets": [["~d10", "x2"], ["d10", "~x2"]]},
            {"rule": "RES", "ctx": [-1], "parents": [9, {"node": 10, "facet": 1}], "pivot": "x2", "clause": ["d10"]},
            {"rule": "RES", "ctx": [-1], "parents": [11, {"node": 10, "facet": 0}], "pivot": "d10", "clause": ["x2"]},
            {"rule": "MERGE", "ctx": [], "parents": [7, 12], "pivot": 1, "clause": ["x2"]},
            {"rule": "RES", "ctx": [], "parents": [13, 2], "pivot": "x2", "clause": []},
        ],
    }


def verify(trace, require_final=True):
    if trace.get("format") != "REFEREE369-scoped-owner-v1":
        raise ValueError("wrong format")
    nvars, sources = parse_dimacs(trace["source_dimacs"])
    records, aliases = [], {}
    spans = []
    ops = {"source_reads": 0, "parent_reads": 0, "literal_scans": 0,
           "context_tests": 0, "definition_truth_rows": 0}
    for idx, node in enumerate(trace["nodes"]):
        rule = node.get("rule")
        ctx = canon_ctx(node.get("ctx", []))
        rec = {"rule": rule, "ctx": ctx}
        if rule == "SRC":
            clause = canon_clause(node["clause"])
            visible_defs(clause, ctx, records, idx)
            s = int(node["source"])
            if ctx or not 0 <= s < len(sources) or clause != sources[s]:
                raise ValueError("source authentication failure")
            rec["clause"] = clause
            ops["source_reads"] += 1
            span = 0
        elif rule == "ASSUME":
            clause = canon_clause(node["clause"])
            if len(clause) != 1 or lit_key(clause[0])[0] != "x":
                raise ValueError("assumption must be original literal")
            _, ident, neg = lit_key(clause[0])
            signed = -ident if neg else ident
            if signed not in ctx or ident > nvars:
                raise ValueError("bad assumption")
            rec["clause"] = clause
            span = 1
        elif rule == "DEF":
            alias = node.get("alias")
            if not isinstance(alias, str) or not alias or alias.startswith("x") or alias.startswith("d"):
                raise ValueError("alias must be cosmetic and outside semantic namespaces")
            aliases.setdefault(alias, []).append(idx)
            inputs = [str(x) for x in node["inputs"]]
            for x in inputs:
                lit_key(x)
            visible_defs(inputs, ctx, records, idx)
            facets = [canon_clause(f) for f in node["facets"]]
            for f in facets:
                visible_defs(f, ctx, records, idx, allow_self=True)
                if any(lit_key(x)[0] == "d" and lit_key(x)[1] == idx for x in f):
                    pass
                else:
                    raise ValueError("facet omits owned output")
            if not definition_exact(idx, inputs, node["table"], facets):
                raise ValueError("facets do not exactly define relation")
            rec.update({"facets": facets, "inputs": inputs, "alias": alias})
            ops["definition_truth_rows"] += 2 ** len({lit_key(x)[:2] for x in inputs} | {("d", idx)})
            owner_deps = [lit_key(x)[1] for x in inputs if lit_key(x)[0] == "d"]
            span = 1 + max([spans[d] for d in owner_deps], default=0)
        elif rule == "RES":
            clause = canon_clause(node["clause"])
            visible_defs(clause, ctx, records, idx)
            p1, p2 = node["parents"]
            c1_ctx, c1, a = get_parent(p1, idx, records, ops)
            c2_ctx, c2, b = get_parent(p2, idx, records, ops)
            ops["context_tests"] += 2
            if not context_subset(c1_ctx, ctx) or not context_subset(c2_ctx, ctx):
                raise ValueError("parent context not available")
            if resolve(c1, c2, str(node["pivot"])) != clause:
                raise ValueError("wrong resolvent")
            rec["clause"] = clause
            span = 1 + max(spans[a], spans[b])
        elif rule == "MERGE":
            clause = canon_clause(node["clause"])
            visible_defs(clause, ctx, records, idx)
            if len(node["parents"]) != 2:
                raise ValueError("MERGE is a two-premise AND obligation")
            (ca, a_clause, a), (cb, b_clause, b) = [get_parent(r, idx, records, ops) for r in node["parents"]]
            if a_clause != clause or b_clause != clause:
                raise ValueError("merge conclusions differ")
            p = int(node["pivot"])
            expected = {tuple(canon_ctx(ctx + [p])), tuple(canon_ctx(ctx + [-p]))}
            if {tuple(ca), tuple(cb)} != expected:
                raise ValueError("omitted/wrong AND branch")
            rec["clause"] = clause
            span = 1 + max(spans[a], spans[b])
        else:
            raise ValueError("unknown rule")
        records.append(rec)
        spans.append(span)
        ops["literal_scans"] += len(ctx) + sum(len(rec.get(k, [])) for k in ("clause", "inputs"))
        ops["literal_scans"] += sum(len(f) for f in rec.get("facets", []))
    if require_final and (not records or records[-1].get("clause") != [] or records[-1]["ctx"] != []):
        raise ValueError("final node is not unconditional contradiction")
    paid = sum(r["rule"] != "SRC" for r in records)
    return {"nvars": nvars, "source_clauses": len(sources), "records": records,
            "aliases": aliases, "paid_nodes": paid, "span": spans[-1], "ops": ops}


def alpha_compile(trace):
    checked = verify(trace)
    nvars = checked["nvars"]
    owners = [i for i, r in enumerate(checked["records"]) if r["rule"] == "DEF"]
    mapping = {owner: nvars + rank + 1 for rank, owner in enumerate(owners)}

    def tr_lit(lit):
        kind, ident, neg = lit_key(lit)
        out = ident if kind == "x" else mapping[ident]
        return ("~" if neg else "") + f"x{out}"

    compiled = copy.deepcopy(trace)
    compiled["format"] = "REFEREE369-global-alpha-v1"
    compiled["alpha_map"] = {f"d{k}": f"x{v}" for k, v in mapping.items()}
    for idx, node in enumerate(compiled["nodes"]):
        if "clause" in node:
            node["clause"] = canon_clause([tr_lit(x) for x in node["clause"]])
        if "inputs" in node:
            node["inputs"] = [tr_lit(x) for x in node["inputs"]]
        if "facets" in node:
            node["facets"] = [canon_clause([tr_lit(x) for x in f]) for f in node["facets"]]
        if node["rule"] == "RES":
            node["pivot"] = tr_lit(str(node["pivot"]))
        if node["rule"] == "DEF":
            node["global_output"] = mapping[idx]
            node["alias"] = f"g{mapping[idx]}"
    return compiled, mapping


def verify_alpha(source_trace, compiled):
    checked = verify(source_trace)
    nvars = checked["nvars"]
    owners = [i for i, r in enumerate(checked["records"]) if r["rule"] == "DEF"]
    amap = compiled.get("alpha_map", {})
    if set(amap) != {f"d{i}" for i in owners}:
        raise ValueError("alpha map domain mismatch")
    targets = []
    for owner in owners:
        target = amap[f"d{owner}"]
        kind, ident, neg = lit_key(target)
        if kind != "x" or neg or ident <= nvars:
            raise ValueError("alpha target not globally fresh")
        targets.append(ident)
    if len(set(targets)) != len(targets):
        raise ValueError("alpha target collision")
    expected, mapping = alpha_compile(source_trace)
    if compiled != expected:
        raise ValueError("compiled bytes are not the canonical alpha translation")
    if len(compiled["nodes"]) != len(source_trace["nodes"]):
        raise ValueError("alpha compilation changed node count")
    return {"definition_owners": owners, "global_targets": targets,
            "same_records": True, "same_paid_nodes": checked["paid_nodes"],
            "same_span": checked["span"], "mapping": mapping}


def expect_reject(trace, label):
    try:
        verify(trace)
    except (KeyError, TypeError, ValueError) as exc:
        return {"label": label, "rejected": True, "reason": str(exc)}
    raise AssertionError(f"control unexpectedly accepted: {label}")


def canonical_bytes(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode()


def main():
    start = time.perf_counter_ns()
    trace = trace_fixture()
    checked = verify(trace)
    compiled, _ = alpha_compile(trace)
    alpha = verify_alpha(trace, compiled)
    HERE.mkdir(parents=True, exist_ok=True)
    trace_path = HERE / "scoped_alias_trace_referee369.json"
    compiled_path = HERE / "global_alpha_trace_referee369.json"
    trace_path.write_bytes(canonical_bytes(trace))
    compiled_path.write_bytes(canonical_bytes(compiled))

    controls = []
    bad = copy.deepcopy(trace)
    bad["nodes"][11]["parents"][1] = {"node": 5, "facet": 1}
    controls.append(expect_reject(bad, "sibling definition capture"))
    bad = copy.deepcopy(trace)
    bad["nodes"][6]["clause"] = ["z"]
    controls.append(expect_reject(bad, "unqualified cosmetic alias use"))
    bad = copy.deepcopy(trace)
    bad["nodes"].insert(14, {"rule": "MERGE", "ctx": [], "parents": [6, 11], "pivot": 1, "clause": ["d5"]})
    controls.append(expect_reject(bad, "local output escape through MERGE"))
    bad = copy.deepcopy(trace)
    bad["nodes"][13]["parents"] = [7, 7]
    controls.append(expect_reject(bad, "omitted complementary AND branch"))
    bad = copy.deepcopy(trace)
    bad["nodes"][5]["facets"][0] = ["d5", "x2"]
    controls.append(expect_reject(bad, "corrupt defining facet"))
    bad = copy.deepcopy(trace)
    bad["nodes"][10]["alias"] = "x1"
    controls.append(expect_reject(bad, "semantic namespace used as alias"))
    bad = copy.deepcopy(trace)
    bad["source_dimacs"] = bad["source_dimacs"].replace("p cnf 2 3", "p cnf 2 4")
    controls.append(expect_reject(bad, "malformed source clause count"))

    nvars, sources = parse_dimacs(trace["source_dimacs"])
    elapsed = time.perf_counter_ns() - start
    trace_bytes = canonical_bytes(trace)
    compiled_bytes = canonical_bytes(compiled)
    payload = {
        "artifact": "REFEREE369",
        "status": {
            "scoped_alias_lemma": "PROVED/EXACT for declared owner-qualified comparison grammar",
            "historical_rmix341": "not executed or changed; branch rules remain absent/unspecified",
            "global_mixed_normalization": "OPEN",
            "b3": "OPEN",
            "p_vs_np": "OPEN",
        },
        "positive": {
            "source_models": model_count(nvars, sources),
            "same_cosmetic_alias_owners": checked["aliases"]["z"],
            "paid_nodes": checked["paid_nodes"],
            "span": checked["span"],
            "ops": checked["ops"],
            "bytes": len(trace_bytes),
            "sha256": hashlib.sha256(trace_bytes).hexdigest(),
        },
        "alpha": {
            **alpha,
            "bytes": len(compiled_bytes),
            "sha256": hashlib.sha256(compiled_bytes).hexdigest(),
            "byte_overhead": len(compiled_bytes) - len(trace_bytes),
        },
        "controls": controls,
        "runtime": {
            "elapsed_ns": elapsed,
            "ru_maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
    }
    RAW.parent.mkdir(parents=True, exist_ok=True)
    RAW.write_bytes((json.dumps(payload, indent=2, sort_keys=True) + "\n").encode())
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
