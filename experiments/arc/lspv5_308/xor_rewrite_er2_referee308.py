#!/usr/bin/env python3
"""Finite certificate producer for the ER2 XOR-rewrite templates in REFEREE308.

The certificates are ordinary binary Resolution derivations from authenticated
two-input gate-definition slots and explicitly named unit/equality assumptions.
No SAT oracle, semantic inference, or unrestricted weakening is a proof rule.
"""

from __future__ import annotations

import json
import resource
import sys
import time
from collections import defaultdict
from itertools import product
from pathlib import Path


def norm(lits):
    s = set(lits)
    if any(-x in s for x in s):
        return None
    return tuple(sorted(s, key=lambda x: (abs(x), x < 0)))


def xor_slots(q, a, b):
    # q <-> (a XOR b), one paid source-independent DEF node.
    return [
        norm((a, b, -q)),
        norm((a, -b, q)),
        norm((-a, b, q)),
        norm((-a, -b, -q)),
    ]


def and_slots(q, a, b):
    # q <-> (a AND b), one paid source-independent DEF node.
    return [norm((-q, a)), norm((-q, b)), norm((q, -a, -b))]


def parity3_clauses(a, b, c, bit):
    out = []
    for va, vb, vc in product((0, 1), repeat=3):
        if (va ^ vb ^ vc) != bit:
            # Clause uniquely excluding this wrong assignment.
            out.append(norm((a if not va else -a,
                             b if not vb else -b,
                             c if not vc else -c)))
    return out


def resolve(c1, c2, pivot):
    if pivot not in c1 or -pivot not in c2:
        return None
    return norm([x for x in c1 if x != pivot] +
                [x for x in c2 if x != -pivot])


def prove_template(name, source_groups, targets):
    """Saturate finite Resolution closure and retain only target ancestors."""
    clauses = []
    parents = []
    labels = []
    seen = {}
    pos = defaultdict(set)
    neg = defaultdict(set)

    def add_source(c, label):
        if c is None or c in seen:
            return
        i = len(clauses)
        seen[c] = i
        clauses.append(c)
        parents.append(None)
        labels.append(label)
        for lit in c:
            (pos if lit > 0 else neg)[abs(lit)].add(i)

    for label, group in source_groups:
        for c in group:
            add_source(c, label)

    frontier = list(range(len(clauses)))
    while frontier and not all(norm(t) in seen for t in targets):
        i = frontier.pop(0)
        c = clauses[i]
        generated = []
        for lit in c:
            v = abs(lit)
            others = list(neg[v] if lit > 0 else pos[v])
            for j in others:
                if i == j:
                    continue
                if lit > 0:
                    r = resolve(c, clauses[j], v)
                    par = (i, j, v)
                else:
                    r = resolve(clauses[j], c, v)
                    par = (j, i, v)
                if r is not None and r not in seen:
                    generated.append((r, par))
        for r, par in generated:
            if r in seen:
                continue
            k = len(clauses)
            seen[r] = k
            clauses.append(r)
            parents.append(par)
            labels.append("RES")
            for lit in r:
                (pos if lit > 0 else neg)[abs(lit)].add(k)
            frontier.append(k)
        if len(clauses) > 20000:
            raise RuntimeError(f"closure blowup in {name}")

    target_ids = []
    for t in targets:
        nt = norm(t)
        if nt not in seen:
            raise AssertionError(f"target {nt} not derived in {name}")
        target_ids.append(seen[nt])

    needed = set()

    def visit(i):
        if i in needed:
            return
        needed.add(i)
        if parents[i] is not None:
            visit(parents[i][0])
            visit(parents[i][1])

    for i in target_ids:
        visit(i)
    order = sorted(needed)
    remap = {old: new for new, old in enumerate(order)}
    lines = []
    for old in order:
        p = parents[old]
        line = {"clause": list(clauses[old]), "kind": labels[old]}
        if p is not None:
            line.update({"left": remap[p[0]], "right": remap[p[1]],
                         "pivot": p[2]})
        lines.append(line)
    return {
        "name": name,
        "lines": lines,
        "targets": [remap[i] for i in target_ids],
        "source_lines": sum(1 for x in lines if x["kind"] != "RES"),
        "resolution_lines": sum(1 for x in lines if x["kind"] == "RES"),
        "closure_clauses_examined": len(clauses),
    }


def eval_cnf(clauses, assignment):
    return all(any((lit > 0) == assignment[abs(lit)] for lit in c)
               for c in clauses)


def k4_tseitin(bit0):
    # Edges 1..6: 01,02,03,12,13,23.
    triples = [(1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6)]
    charges = [bit0, 0, 0, 0]
    clauses = []
    for tri, b in zip(triples, charges):
        clauses.extend(parity3_clauses(*tri, b))
    models = []
    for bits in product((0, 1), repeat=6):
        a = {i + 1: bits[i] for i in range(6)}
        if eval_cnf(clauses, a):
            models.append("".join(map(str, bits)))
    return {"charges": charges, "clauses": [list(c) for c in clauses],
            "model_count": len(models), "first_models": models[:8]}


def malformed_controls():
    def parse_dimacs(text):
        toks = text.split()
        if len(toks) < 4 or toks[0:2] != ["p", "cnf"]:
            return False
        try:
            n, m = int(toks[2]), int(toks[3])
            xs = [int(x) for x in toks[4:]]
        except ValueError:
            return False
        clauses, cur = [], []
        for x in xs:
            if x == 0:
                clauses.append(cur); cur = []
            elif abs(x) > n:
                return False
            else:
                cur.append(x)
        return not cur and len(clauses) == m

    cases = {
        "valid_sat": "p cnf 1 1 1 0",
        "valid_unsat": "p cnf 1 2 1 0 -1 0",
        "bad_header": "cnf 1 1 1 0",
        "bad_clause_count": "p cnf 1 2 1 0",
        "bad_variable": "p cnf 1 1 2 0",
        "missing_terminator": "p cnf 1 1 1",
        "nonnumeric": "p cnf 1 1 x 0",
    }
    return {k: parse_dimacs(v) for k, v in cases.items()}


def main():
    t0 = time.perf_counter()
    T, x, xp, y, a, b, c, u, v, p, q, r = range(1, 13)
    templates = []
    templates.append(prove_template(
        "xor_commutativity",
        [("DEF_XOR_q_ab", xor_slots(q, a, b)),
         ("DEF_XOR_r_ba", xor_slots(r, b, a))],
        [(-q, r), (q, -r)]))
    templates.append(prove_template(
        "xor_associativity",
        [("DEF_XOR_u_ab", xor_slots(u, a, b)),
         ("DEF_XOR_v_uc", xor_slots(v, u, c)),
         ("DEF_XOR_p_bc", xor_slots(p, b, c)),
         ("DEF_XOR_q_ap", xor_slots(q, a, p))],
        [(-v, q), (v, -q)]))
    templates.append(prove_template(
        "xor_congruence_left",
        [("ASSUME_x_iff_xp", [norm((-x, xp)), norm((x, -xp))]),
         ("DEF_XOR_q_xy", xor_slots(q, x, y)),
         ("DEF_XOR_r_xpy", xor_slots(r, xp, y))],
        [(-q, r), (q, -r)]))
    templates.append(prove_template(
        "and_copy_under_true_rail",
        [("UNIT_T", [norm((T,))]),
         ("DEF_AND_xp_Tx", and_slots(xp, T, x))],
        [(-xp, x), (xp, -x)]))
    templates.append(prove_template(
        "xor_copy_cancellation",
        [("UNIT_T", [norm((T,))]),
         ("DEF_AND_xp_Tx", and_slots(xp, T, x)),
         ("DEF_XOR_q_xxp", xor_slots(q, x, xp))],
        [(-q,)]))
    for va, vb in product((0, 1), repeat=2):
        out = va ^ vb
        templates.append(prove_template(
            f"xor_unit_{va}{vb}",
            [("UNIT_a", [norm((a if va else -a,))]),
             ("UNIT_b", [norm((b if vb else -b,))]),
             ("DEF_XOR_q_ab", xor_slots(q, a, b))],
            [(q if out else -q,)]))
    for bit in (0, 1):
        templates.append(prove_template(
            f"parity3_to_xor_output_{bit}",
            [(f"PARITY3_{bit}", parity3_clauses(a, b, c, bit)),
             ("DEF_XOR_u_ab", xor_slots(u, a, b)),
             ("DEF_XOR_q_uc", xor_slots(q, u, c))],
            [(q if bit else -q,)]))

    out = {
        "tag": "NONAFFINE-LIFT-ER2-COLLAPSE-REFEREE308",
        "fixed_fragment": "source-independent two-input AND/XOR VARDEF plus strict binary RES",
        "templates": templates,
        "template_totals": {
            "count": len(templates),
            "resolution_lines": sum(t["resolution_lines"] for t in templates),
            "retained_certificate_lines": sum(len(t["lines"]) for t in templates),
            "max_resolution_lines": max(t["resolution_lines"] for t in templates),
        },
        "both_label_k4": {
            "odd_unsat": k4_tseitin(1),
            "even_sat": k4_tseitin(0),
        },
        "malformed_controls": malformed_controls(),
        "rejected_shortcuts": {
            "false_as_axiom": "REJECT: not an authenticated original or fixed DEF slot",
            "semantic_xor_jump": "REJECT: every rewrite equality has a retained RES certificate",
            "instance_advice": "REJECT: templates and gate grammar are source-independent",
        },
        "producer": {
            "wall_seconds": time.perf_counter() - t0,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "python": sys.version.split()[0],
        },
    }
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("referee308.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out["template_totals"], sort_keys=True))
    print(json.dumps({
        "odd_models": out["both_label_k4"]["odd_unsat"]["model_count"],
        "even_models": out["both_label_k4"]["even_sat"]["model_count"],
        "malformed": out["malformed_controls"],
        "wall_seconds": out["producer"]["wall_seconds"],
        "peak_rss_kib": out["producer"]["peak_rss_kib"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
