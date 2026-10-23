#!/usr/bin/env python3
"""Independent adaptive-state audit for ADAPTIVE-TRAJECTORY-FIREWALL107.

The tested solver is a total deterministic policy:
  acquire -> certified binary resolution/unit propagation ->
  (conflict | SCC 2-SAT | Horn least model | exact DPLL fallback).
All recognizer failures and switches are recorded.  Standard library only.
"""
from itertools import combinations, product
import hashlib
import json
import sys

sys.setrecursionlimit(200000)
checks = 0


def ck(condition, label):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(f"check {checks}: {label}")


def sat_clause(clause, assignment):
    return any(assignment.get(abs(lit), False) == (lit > 0) for lit in clause)


def verify(cnf, assignment):
    return all(sat_clause(clause, assignment) for clause in cnf)


def simplify(cnf, assignment, counter):
    residual = []
    for clause in cnf:
        counter["clause_touches"] += 1
        out = []
        satisfied = False
        for lit in clause:
            counter["literal_reads"] += 1
            var = abs(lit)
            if var in assignment:
                if assignment[var] == (lit > 0):
                    satisfied = True
                    break
            else:
                out.append(lit)
        if not satisfied:
            residual.append(tuple(out))
    return residual


def certified_binary_seeds(cnf, counter):
    # Index (common literal -> other literals).  If both x and -x occur as
    # the other literal, ordinary binary resolution certifies the common unit.
    companions = {}
    for clause in cnf:
        if len(clause) != 2:
            continue
        a, b = clause
        companions.setdefault(a, set()).add(b)
        companions.setdefault(b, set()).add(a)
        counter["binary_index_writes"] += 2
    seeds = set()
    for common, others in companions.items():
        counter["pair_probes"] += len(others)
        if any(-other in others for other in others):
            seeds.add(common)
    return seeds


def unit_propagate(cnf, initial, counter):
    assignment = {}
    queue = []
    occurrences = {}
    for ci, clause in enumerate(cnf):
        for lit in clause:
            occurrences.setdefault(lit, []).append(ci)
            counter["literal_reads"] += 1
    live = [len(clause) for clause in cnf]
    satisfied = [False] * len(cnf)

    def enqueue(lit):
        counter["unit_events"] += 1
        v, value = abs(lit), lit > 0
        if v in assignment:
            return assignment[v] == value
        assignment[v] = value
        queue.append(lit)
        return True

    for v, value in initial.items():
        if not enqueue(v if value else -v):
            return assignment, [()], False
    for clause in cnf:
        if len(clause) == 1 and not enqueue(clause[0]):
            return assignment, [()], False

    head = 0
    while head < len(queue):
        true_lit = queue[head]
        head += 1
        for ci in occurrences.get(true_lit, []):
            counter["clause_touches"] += 1
            satisfied[ci] = True
        for ci in occurrences.get(-true_lit, []):
            counter["clause_touches"] += 1
            if satisfied[ci]:
                continue
            if any(abs(lit) in assignment and
                   assignment[abs(lit)] == (lit > 0) for lit in cnf[ci]):
                satisfied[ci] = True
                continue
            live[ci] -= 1
            if live[ci] == 0:
                return assignment, [()], False
            if live[ci] == 1:
                remaining = next((lit for lit in cnf[ci]
                                  if abs(lit) not in assignment), None)
                if remaining is None or not enqueue(remaining):
                    return assignment, [()], False

    residual = simplify(cnf, assignment, counter)
    if any(len(c) == 0 for c in residual):
        return assignment, residual, False
    return assignment, residual, True


def literal_index(lit):
    return 2 * (abs(lit) - 1) + (0 if lit > 0 else 1)


def index_literal(index):
    var = index // 2 + 1
    return var if index % 2 == 0 else -var


def solve_2sat(cnf, nvars, counter):
    graph = [[] for _ in range(2 * nvars)]
    reverse = [[] for _ in range(2 * nvars)]
    for clause in cnf:
        if len(clause) == 1:
            pairs = [(-clause[0], clause[0])]
        elif len(clause) == 2:
            a, b = clause
            pairs = [(-a, b), (-b, a)]
        else:
            raise ValueError("not 2-CNF")
        for a, b in pairs:
            u, v = literal_index(a), literal_index(b)
            graph[u].append(v)
            reverse[v].append(u)
            counter["graph_edges"] += 1
    seen, order = [False] * (2 * nvars), []
    def dfs1(v):
        seen[v] = True
        for u in graph[v]:
            if not seen[u]:
                dfs1(u)
        order.append(v)
    for v in range(2 * nvars):
        if not seen[v]:
            dfs1(v)
    comp = [-1] * (2 * nvars)
    def dfs2(v, label):
        comp[v] = label
        for u in reverse[v]:
            if comp[u] < 0:
                dfs2(u, label)
    label = 0
    for v in reversed(order):
        if comp[v] < 0:
            dfs2(v, label)
            label += 1
    for var in range(1, nvars + 1):
        if comp[literal_index(var)] == comp[literal_index(-var)]:
            return False, {}
    # Components are numbered in topological order by this Kosaraju variant.
    assignment = {
        var: comp[literal_index(var)] > comp[literal_index(-var)]
        for var in range(1, nvars + 1)
    }
    if cnf and not verify(cnf, assignment):
        assignment = {var: not val for var, val in assignment.items()}
    ck(verify(cnf, assignment), "SCC witness")
    return True, assignment


def solve_horn(cnf, nvars, counter):
    if any(sum(lit > 0 for lit in clause) > 1 for clause in cnf):
        return None, {}
    assignment = {v: False for v in range(1, nvars + 1)}
    changed = True
    while changed:
        changed = False
        for clause in cnf:
            counter["horn_clause_touches"] += 1
            positives = [lit for lit in clause if lit > 0]
            antecedents = [-lit for lit in clause if lit < 0]
            if all(assignment[v] for v in antecedents):
                if not positives:
                    return False, {}
                head = positives[0]
                if not assignment[head]:
                    assignment[head] = True
                    changed = True
    ck(verify(cnf, assignment), "Horn witness")
    return True, assignment


def dpll(cnf, nvars, counter, partial=None):
    partial = {} if partial is None else dict(partial)
    residual = simplify(cnf, partial, counter)
    if any(not clause for clause in residual):
        return False, {}
    if not residual:
        return True, {v: partial.get(v, False) for v in range(1, nvars + 1)}
    units = [c[0] for c in residual if len(c) == 1]
    if units:
        lit = units[0]
        v, value = abs(lit), lit > 0
        if v in partial and partial[v] != value:
            return False, {}
        partial[v] = value
        return dpll(cnf, nvars, counter, partial)
    var = abs(residual[0][0])
    for value in (False, True):
        counter["fallback_branches"] += 1
        child = dict(partial)
        child[var] = value
        ok, witness = dpll(cnf, nvars, counter, child)
        if ok:
            return True, witness
    return False, {}


def adaptive_policy(cnf, nvars):
    counter = {k: 0 for k in [
        "source_words", "literal_reads", "clause_touches",
        "binary_index_writes", "pair_probes", "unit_events",
        "graph_edges", "horn_clause_touches", "policy_checks",
        "switches", "fallback_branches", "witness_replay"
    ]}
    counter["source_words"] = 4 * len(cnf) + 2
    trajectory = [{"stage": "raw", "m": len(cnf),
                   "k": sum(len(c) == 3 for c in cnf),
                   "available": ["n", "m", "clause_widths"]}]
    seeds = certified_binary_seeds(cnf, counter)
    seed_assignment = {}
    for lit in seeds:
        v, value = abs(lit), lit > 0
        if v in seed_assignment and seed_assignment[v] != value:
            return False, {}, trajectory, counter, "seed_conflict"
        seed_assignment[v] = value
    counter["policy_checks"] += 1
    assignment, residual, consistent = unit_propagate(cnf, seed_assignment, counter)
    trajectory.append({"stage": "binary_closure", "certified_seeds": len(seeds),
                       "assigned": len(assignment), "residual_m": len(residual),
                       "residual_k": sum(len(c) >= 3 for c in residual)})
    if not consistent:
        counter["switches"] += 1
        trajectory.append({"stage": "conflict", "label": "UNSAT"})
        return False, {}, trajectory, counter, "propagation_conflict"
    counter["policy_checks"] += 1
    if all(len(c) <= 2 for c in residual):
        counter["switches"] += 1
        ok, tail = solve_2sat(residual, nvars, counter)
        if ok:
            tail.update(assignment)
            counter["witness_replay"] += sum(len(c) for c in cnf)
            ck(verify(cnf, tail), "original-source SCC replay")
        trajectory.append({"stage": "SCC", "label": "SAT" if ok else "UNSAT"})
        return ok, tail, trajectory, counter, "SCC"
    counter["policy_checks"] += 1
    horn_ok, horn_witness = solve_horn(residual, nvars, counter)
    if horn_ok is not None:
        counter["switches"] += 1
        if horn_ok:
            horn_witness.update(assignment)
            counter["witness_replay"] += sum(len(c) for c in cnf)
            ck(verify(cnf, horn_witness), "original-source Horn replay")
        trajectory.append({"stage": "Horn", "label": "SAT" if horn_ok else "UNSAT"})
        return horn_ok, horn_witness, trajectory, counter, "Horn"
    counter["switches"] += 1
    ok, witness = dpll(cnf, nvars, counter, assignment)
    if ok:
        counter["witness_replay"] += sum(len(c) for c in cnf)
        ck(verify(cnf, witness), "original-source fallback replay")
    trajectory.append({"stage": "fallback", "label": "SAT" if ok else "UNSAT"})
    return ok, witness, trajectory, counter, "fallback"


def make_h(q, bits):
    next_var = 1
    z = list(range(next_var, next_var + q + 1)); next_var += q + 1
    p = list(range(next_var, next_var + q + 1)); next_var += q + 1
    y = list(range(next_var, next_var + q + 1)); next_var += q + 1
    u, v = next_var, next_var + 1; next_var += 2
    cnf = [(z[0], u), (z[0], -u), (y[q], v), (y[q], -v), (-z[0], p[0])]
    cnf += [(-p[i - 1], p[i]) for i in range(1, q + 1)]
    cnf += [(-z[i - 1], z[i] if bits[i - 1] else -z[i])
            for i in range(1, q + 1)]
    for i in range(q + 1):
        cnf += [
            (z[i], y[i], -p[i]), (z[i], -y[i], p[i]),
            (-z[i], y[i], p[i]), (-z[i], -y[i], -p[i]),
        ]
    return cnf, next_var - 1, {"z": z, "p": p, "y": y, "u": u, "v": v}


def backdoor_hitting_number(cnf):
    supports = {frozenset(abs(lit) for lit in c) for c in cnf if len(c) == 3}
    universe = sorted(set().union(*supports)) if supports else []
    for size in range(len(universe) + 1):
        for subset in combinations(universe, size):
            if all(set(subset) & support for support in supports):
                return size
    raise AssertionError("no hitting set")


records = []

# Exhaustive all-orientation audit for small q, including exact backdoor minima.
for q in range(1, 6):
    for bits in product((0, 1), repeat=q):
        cnf, nvars, _ = make_h(q, bits)
        got, witness, trace, counter, mode = adaptive_policy(cnf, nvars)
        expected = bits != (1,) * q
        ck(got == expected, "H label")
        ck(mode == ("SCC" if expected else "propagation_conflict"), "H policy mode")
        if got:
            ck(verify(cnf, witness), "H witness")
        if q <= 4:
            ck(backdoor_hitting_number(cnf) == q + 1, "raw backdoor minimum")
        records.append({"family": "H", "q": q, "label": "SAT" if got else "UNSAT",
                        "mode": mode, "initial_k": 4 * (q + 1),
                        "initial_h": q + 1, "final_k": trace[-2].get("residual_k", 0),
                        "charged_events": sum(counter.values())})

# Scaling pairs: no exhaustive search, but exact source replay on SAT members.
scaling = []
for q in (8, 32, 128, 512, 1024):
    for bits, label in [((1,) * q, "UNSAT"), ((0,) + (1,) * (q - 1), "SAT")]:
        cnf, nvars, _ = make_h(q, bits)
        got, witness, trace, counter, mode = adaptive_policy(cnf, nvars)
        ck(got == (label == "SAT"), "scaling label")
        if got:
            ck(verify(cnf, witness), "scaling witness")
        scaling.append({"q": q, "label": label, "mode": mode,
                        "n": nvars, "m": len(cnf), "k0": 4 * (q + 1),
                        "h0": q + 1, "k_after_binary": trace[-2].get("residual_k", 0),
                        "assigned_after_binary": trace[-2].get("assigned", 0),
                        "events": counter})

# Hybrid controls exercise distinct evidence-selected continuations.
controls = [
    ("2SAT_SAT", [(1, 2), (-1, 2)], 2, True, "SCC"),
    ("2SAT_UNSAT", [(1,), (-1,)], 1, False, "propagation_conflict"),
    ("HORN_SAT", [(-1, -2, 3), (-2, -3, 4)], 4, True, "Horn"),
    ("HORN_UNSAT", [(1,), (-1, 2), (-2,)], 2, False, "propagation_conflict"),
    ("FALLBACK_SAT", [(1, 2, 3), (-1, -2, 3)], 3, True, "fallback"),
    ("FALLBACK_UNSAT", [tuple((v if ((mask >> (v - 1)) & 1) == 0 else -v)
                              for v in (1, 2, 3)) for mask in range(8)],
     3, False, "fallback"),
]
control_rows = []
for name, cnf, nvars, expected, expected_mode in controls:
    got, witness, trace, counter, mode = adaptive_policy(cnf, nvars)
    ck(got == expected, name + " label")
    ck(mode == expected_mode, name + " mode")
    if got:
        ck(verify(cnf, witness), name + " witness")
    control_rows.append({"name": name, "label": "SAT" if got else "UNSAT",
                         "selected_mode": mode, "trajectory": trace,
                         "events": counter})

# Failed shortcut: break the p-chain so binary closure leaves ternaries and
# the policy must pay for recognition failure and switch to exact fallback.
cnf, nvars, names = make_h(4, (0, 1, 1, 1))
broken = [c for c in cnf if c != (-names["p"][1], names["p"][2])]
got, witness, trace, counter, mode = adaptive_policy(broken, nvars)
ck(got and mode == "fallback" and verify(broken, witness), "broken-chain fallback")
control_rows.append({"name": "BROKEN_CHAIN_SAT", "label": "SAT",
                     "selected_mode": mode, "trajectory": trace, "events": counter})

payload = {
    "run": "ADAPTIVE_TRAJECTORY_FIREWALL107",
    "checks": checks,
    "failures": 0,
    "small_H_instances": len(records),
    "scaling_runs": scaling,
    "hybrid_controls": control_rows,
    "proved_scope": "restricted trajectory counterexample and total exact hybrid upper bound",
    "all_decider_lower_bound": "OPEN",
    "P_vs_NP": "OPEN",
}
canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
payload["content_sha256_without_hash_field"] = hashlib.sha256(canonical).hexdigest()
print(json.dumps(payload, indent=2, sort_keys=True))
