#!/usr/bin/env python3
"""Independent control for JOINT-FRONTIER-SUPPORT-REFEREE189.

Builds a connected strict signed exact-(2,2)-3CNF family with BOTH:
  * an H x H grid minor (hence every-order syntactic frontier Omega(H)); and
  * on the UNSAT side, source-premise support in at least H^2 modules.

The family is nevertheless decided by one fixed polynomial recognizer.  This
is a restricted-family countercontrol, not a SAT runtime lower bound.
"""
from __future__ import annotations

import collections
import hashlib
import json

W1 = tuple(tuple(map(int, row.split())) for row in (
    "-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;"
    "4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;"
    "-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;"
    "-5 -12 15;-1 13 14"
).split(";"))

S = tuple(tuple(map(int, row.split())) for row in (
    "-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;"
    "4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;"
    "-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;"
    "5 12 -15;-1 13 -14"
).split(";"))

PORTS = {"N": (1, 2), "S": (2, 0), "E": (3, 1), "W": (4, 0)}
CHECKS = collections.Counter()


def ck(condition, tag):
    CHECKS["assertions"] += 1
    if not condition:
        raise AssertionError(tag)


def swap_signs(formula, a, b):
    out = [list(c) for c in formula]
    ck(out[a[0]][a[1]] == -out[b[0]][b[1]], "swap needs opposite signs")
    out[a[0]][a[1]] *= -1
    out[b[0]][b[1]] *= -1
    return tuple(map(tuple, out))


# Long-chain templates from SOURCE-SUPPORT150.
TEMPLATES = {
    "U": W1,
    "C": swap_signs(W1, (3, 1), (14, 1)),
    "D": swap_signs(W1, (3, 0), (13, 0)),
}

# Universal x3-port tail template.  Starting from the W1-ring S template,
# exchange the signs of its first-clause -x3 and a later +x3.  This preserves
# exact-(2,2), makes the first-clause x3 port positive, and direct enumeration
# proves all four (own x3, predecessor x3) pairs.
TEMPLATES["E"] = swap_signs(S, (0, 1), (3, 0))


def clause_true(clause, mask, prev=None):
    for lit in clause:
        if abs(lit) == 16:
            value = prev
        else:
            value = (mask >> (abs(lit) - 1)) & 1
        if value == int(lit > 0):
            return True
    return False


def exact22(formula, n):
    occ = collections.Counter(lit for c in formula for lit in c)
    return (
        len(formula) * 3 == 4 * n
        and all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in formula)
        and len({tuple(sorted(c)) for c in formula}) == len(formula)
        and all(occ[v] == occ[-v] == 2 for v in range(1, n + 1))
    )


def local_relation(template):
    relation = {}
    trials = 0
    for own in (0, 1):
        for prev in (0, 1):
            witness = None
            for mask in range(1 << 15):
                trials += 1
                if ((mask >> 2) & 1) != own:
                    continue
                ok = True
                for ci, c in enumerate(template):
                    row = list(c)
                    if ci == 0:
                        ck(row[1] == 3, "positive x3 port")
                        row[1] = 16
                    if not clause_true(row, mask, prev):
                        ok = False
                        break
                if ok:
                    witness = mask
                    break
            relation[(own, prev)] = witness
    return relation, trials


REL = {}
TRIALS = {}
for name, template in TEMPLATES.items():
    ck(exact22(template, 15), "local exact22 " + name)
    REL[name], TRIALS[name] = local_relation(template)

EXPECTED = {
    "C": {(0, 0), (0, 1)},
    "D": {(0, 0), (0, 1), (1, 1)},
    "U": {(0, 1)},
    "E": {(0, 0), (0, 1), (1, 0), (1, 1)},
}
for name in EXPECTED:
    got = {pair for pair, witness in REL[name].items() if witness is not None}
    ck(got == EXPECTED[name], "relation " + name)

# Every grid port is a negative literal whose variable is zero in every chosen
# E witness.  Therefore occurrence swaps among E modules preserve each witness.
for pair, witness in REL["E"].items():
    ck(witness is not None, "E total")
    for ci, pos in PORTS.values():
        lit = TEMPLATES["E"][ci][pos]
        ck(lit < 0 and not ((witness >> (abs(lit) - 1)) & 1), "E port false")


def remap(lit, block):
    return (1 if lit > 0 else -1) * (abs(lit) + 15 * block)


def typeword(H, unsat):
    chain = H * H
    return ["C"] + ["D"] * (chain - 2) + (["U"] if unsat else ["E"]) + ["E"] * (H * H)


def build(H, unsat):
    types = typeword(H, unsat)
    clauses = []
    for block, name in enumerate(types):
        for ci, source in enumerate(TEMPLATES[name]):
            row = [remap(lit, block) for lit in source]
            if ci == 0:
                ck(row[1] > 0 and abs(row[1]) == 15 * block + 3, "ring port")
                row[1] = 15 * ((block - 1) % len(types)) + 3
            clauses.append(row)

    start = H * H

    def patch(b1, d1, b2, d2):
        c1, p1 = PORTS[d1]
        c2, p2 = PORTS[d2]
        z1, z2 = 20 * b1 + c1, 20 * b2 + c2
        ck(clauses[z1][p1] < 0 and clauses[z2][p2] < 0, "negative grid ports")
        clauses[z1][p1], clauses[z2][p2] = clauses[z2][p2], clauses[z1][p1]

    idx = lambda r, c: start + r * H + c
    for r in range(H):
        for c in range(H):
            if c + 1 < H:
                patch(idx(r, c), "E", idx(r, c + 1), "W")
            if r + 1 < H:
                patch(idx(r, c), "S", idx(r + 1, c), "N")
    return tuple(map(tuple, clauses)), types


def connected(formula, n):
    graph = {v: set() for v in range(1, n + 1)}
    for clause in formula:
        names = list(map(abs, clause))
        for a in names:
            for b in names:
                if a != b:
                    graph[a].add(b)
    seen, queue = {1}, [1]
    for v in queue:
        for u in graph[v]:
            if u not in seen:
                seen.add(u)
                queue.append(u)
    return len(seen) == n, graph


def grid_minor_check(formula, H):
    start = H * H
    _, graph = connected(formula, 30 * H * H)
    branch = [set(range(15 * b + 1, 15 * b + 16)) for b in range(start, 2 * H * H)]
    for bi, vertices in enumerate(branch):
        root = next(iter(vertices))
        seen, queue = {root}, [root]
        for v in queue:
            for u in graph[v] & vertices:
                if u not in seen:
                    seen.add(u)
                    queue.append(u)
        ck(seen == vertices, "tail branch connected")
    def adjacent(a, b):
        return any(graph[v] & b for v in a)
    for r in range(H):
        for c in range(H):
            here = branch[r * H + c]
            if c + 1 < H:
                ck(adjacent(here, branch[r * H + c + 1]), "horizontal minor edge")
            if r + 1 < H:
                ck(adjacent(here, branch[(r + 1) * H + c]), "vertical minor edge")


def cycle_bits(types, skip=None):
    K = len(types)
    for u0 in (0, 1):
        states = {u0: [u0]}
        for i in range(1, K):
            nxt = {}
            for prev, path in states.items():
                for own in (0, 1):
                    if i == skip or REL[types[i]][(own, prev)] is not None:
                        nxt.setdefault(own, path + [own])
            states = nxt
        for last, path in states.items():
            if skip == 0 or REL[types[0]][(u0, last)] is not None:
                return path
    return None


def assignment(types, bits, skip=None):
    values = {}
    K = len(types)
    for i, name in enumerate(types):
        own, prev = bits[i], bits[(i - 1) % K]
        witness = 0 if i == skip else REL[name][(own, prev)]
        ck(witness is not None, "missing local witness")
        for v in range(1, 16):
            values[15 * i + v] = (witness >> (v - 1)) & 1
        values[15 * i + 3] = own
    return values


def formula_true(formula, values, skip=None):
    for ci, clause in enumerate(formula):
        if skip is not None and ci // 20 == skip:
            continue
        if not any(values[abs(lit)] == int(lit > 0) for lit in clause):
            return False
    return True


def render(formula, n):
    return ("p cnf %d %d\n" % (n, len(formula)) + "".join(
        " ".join(map(str, c)) + " 0\n" for c in formula
    )).encode("ascii")


rows = []
deletion_models = 0
for H in range(2, 8):
    for unsat in (False, True):
        formula, types = build(H, unsat)
        K, n = 2 * H * H, 30 * H * H
        ck(len(types) == K and len(formula) == 20 * K, "sizes")
        ck(exact22(formula, n), "global exact22")
        ok, _ = connected(formula, n)
        ck(ok, "connected")
        grid_minor_check(formula, H)
        bits = cycle_bits(types)
        ck((bits is None) == unsat, "answer polarity")
        if bits is not None:
            ck(formula_true(formula, assignment(types, bits)), "SAT witness")
        else:
            for skip in range(H * H):
                repaired = cycle_bits(types, skip)
                ck(repaired is not None, "deleted chain module should be SAT")
                ck(formula_true(formula, assignment(types, repaired, skip), skip), "deletion witness")
                deletion_models += 1
        raw = render(formula, n)
        rows.append({
            "H": H,
            "label": "UNSAT" if unsat else "SAT",
            "modules": K,
            "chain_modules": H * H,
            "variables": n,
            "clauses": len(formula),
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "grid_frontier_symbolic_floor": H / 16,
            "unsat_source_module_support_floor": H * H if unsat else None,
        })

out = {
    "research_id": "JOINT-FRONTIER-SUPPORT-REFEREE189",
    "status": "PASS",
    "template_relations": {
        name: [list(pair) for pair, witness in REL[name].items() if witness is not None]
        for name in ("C", "D", "U", "E")
    },
    "local_assignment_trials": TRIALS,
    "sizes": rows,
    "chain_module_deletion_models_checked": deletion_models,
    "assertions": CHECKS["assertions"],
    "symbolic_result": {
        "proper_strict_signed_exact22": True,
        "connected": True,
        "both_answer_classes": True,
        "every_order_syntactic_frontier": "at least H/16",
        "UNSAT_source_premise_module_support": "at least H^2 of 2H^2 modules",
        "uniform_decision": "polynomial-time fixed-template parser and transfer",
    },
    "limitations": [
        "Restricted syntactically recognizable fixed-template family.",
        "Source-premise support is not proof bit length, width, space, or arbitrary-algorithm time.",
        "Grid frontier is syntactic and need not survive semantic projection.",
        "Finite Python counts are not native single-tape, two-tape, or universal-machine transitions.",
        "No arbitrary-SAT interface acquisition or N^lambda all-input child constructor is proved.",
    ],
}
print(json.dumps(out, indent=2, sort_keys=True))
