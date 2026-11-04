#!/usr/bin/env python3
"""Finite audit of the REFEREE341 clause-private evaluator replay."""

import hashlib
import json
from itertools import product
from pathlib import Path


def canon(clause):
    vals = set(int(x) for x in clause)
    if 0 in vals:
        raise ValueError("zero literal")
    if any(-x in vals for x in vals):
        raise ValueError("tautological clause")
    return tuple(sorted(vals, key=lambda x: (abs(x), x < 0)))


def resolve(c1, c2, pivot):
    c1, c2 = set(c1), set(c2)
    if pivot in c1 and -pivot in c2:
        a, b = pivot, -pivot
    elif -pivot in c1 and pivot in c2:
        a, b = -pivot, pivot
    else:
        raise ValueError("missing complementary pivot")
    return canon((c1 - {a}) | (c2 - {b}))


def gate_slots(op, out, a, b):
    if op == "OR":
        return [canon((-a, out)), canon((-b, out)), canon((a, b, -out))]
    if op == "AND":
        return [canon((-out, a)), canon((-out, b)), canon((out, -a, -b))]
    raise ValueError("bad gate")


def eval_clause(clause, assignment):
    return any(assignment[abs(x)] == (x > 0) for x in clause)


def compile_replay(clauses):
    clauses = [canon(c) for c in clauses]
    if not clauses or any(len(c) == 0 for c in clauses):
        raise ValueError("expected nonempty CNF with nonempty clauses")
    next_var = max(abs(x) for c in clauses for x in c) + 1
    env, sources, defs, steps, outputs = {}, [], [], [], []

    for i, clause in enumerate(clauses):
        sid = f"S{i}"
        sources.append({"id": sid, "clause": list(clause)})
        env[sid] = clause
        cur_ref = sid
        if len(clause) == 1:
            outputs.append((clause[0], cur_ref))
            continue
        frontier = list(clause)
        for j in range(1, len(clause)):
            a, b = (frontier[0], frontier[1]) if j == 1 else (out, frontier[j])
            out, next_var = next_var, next_var + 1
            did = f"D{len(defs)}"
            slot_records = []
            for s, sc in enumerate(gate_slots("OR", out, a, b)):
                slot_id = f"{did}:s{s}"
                env[slot_id] = sc
                slot_records.append({"id": slot_id, "clause": list(sc)})
            defs.append({"id": did, "op": "OR", "out": out,
                         "inputs": [a, b], "slots": slot_records})
            for inp, slot_index in ((a, 0), (b, 1)):
                rid, right = f"R{len(steps)}", f"{did}:s{slot_index}"
                conclusion = resolve(env[cur_ref], env[right], abs(inp))
                steps.append({"id": rid, "left": cur_ref, "right": right,
                              "pivot": abs(inp), "clause": list(conclusion)})
                env[rid], cur_ref = conclusion, rid
        assert env[cur_ref] == (out,)
        outputs.append((out, cur_ref))

    cur_lit, cur_ref = outputs[0]
    for lit, lit_ref in outputs[1:]:
        out, next_var = next_var, next_var + 1
        did = f"D{len(defs)}"
        slot_records = []
        for s, sc in enumerate(gate_slots("AND", out, cur_lit, lit)):
            slot_id = f"{did}:s{s}"
            env[slot_id] = sc
            slot_records.append({"id": slot_id, "clause": list(sc)})
        defs.append({"id": did, "op": "AND", "out": out,
                     "inputs": [cur_lit, lit], "slots": slot_records})
        current = f"{did}:s2"
        for inp, unit_ref in ((cur_lit, cur_ref), (lit, lit_ref)):
            rid = f"R{len(steps)}"
            conclusion = resolve(env[current], env[unit_ref], abs(inp))
            steps.append({"id": rid, "left": current, "right": unit_ref,
                          "pivot": abs(inp), "clause": list(conclusion)})
            env[rid], current = conclusion, rid
        assert env[current] == (out,)
        cur_lit, cur_ref = out, current

    literal_count = sum(map(len, clauses))
    assert len(defs) == literal_count - 1
    assert len(steps) == 2 * (literal_count - 1)
    return {"clauses": [list(c) for c in clauses],
            "literal_count": literal_count, "sources": sources, "defs": defs,
            "res": steps, "root_literal": cur_lit, "root_ref": cur_ref,
            "paid": len(defs) + len(steps)}


def verify_record(record):
    env = {}
    for src in record["sources"]:
        env[src["id"]] = canon(src["clause"])
    max_old = max(abs(x) for c in record["clauses"] for x in c)
    seen_gate = set()
    for gate in record["defs"]:
        out, (a, b) = gate["out"], gate["inputs"]
        assert out > max_old and out not in seen_gate
        expected = gate_slots(gate["op"], out, a, b)
        assert [canon(s["clause"]) for s in gate["slots"]] == expected
        for slot, clause in zip(gate["slots"], expected):
            env[slot["id"]] = clause
        seen_gate.add(out)
    for step in record["res"]:
        assert step["left"] in env and step["right"] in env
        got = resolve(env[step["left"]], env[step["right"]], step["pivot"])
        assert got == canon(step["clause"])
        env[step["id"]] = got
    assert env[record["root_ref"]] == (record["root_literal"],)
    assert record["paid"] == 3 * (record["literal_count"] - 1)
    return env


def downstream_block2(record, env):
    """Recover four source clauses from the evaluator root and refute them."""
    steps = []

    def add(left, right, pivot):
        rid = f"Q{len(steps)}"
        clause = resolve(env[left], env[right], pivot)
        steps.append({"id": rid, "left": left, "right": right,
                      "pivot": pivot, "clause": list(clause)})
        env[rid] = clause
        return rid

    units = {record["root_literal"]: record["root_ref"]}
    for gate in reversed([d for d in record["defs"] if d["op"] == "AND"]):
        out_ref = units[gate["out"]]
        a, b = gate["inputs"]
        units[a] = add(out_ref, f"{gate['id']}:s0", gate["out"])
        units[b] = add(out_ref, f"{gate['id']}:s1", gate["out"])
    recovered = []
    for gate in [d for d in record["defs"] if d["op"] == "OR"]:
        recovered.append(add(units[gate["out"]], f"{gate['id']}:s2", gate["out"]))
    assert [env[r] for r in recovered] == [canon(c) for c in record["clauses"]]
    pos = add(recovered[0], recovered[1], 2)
    neg = add(recovered[2], recovered[3], 2)
    empty = add(pos, neg, 1)
    assert env[empty] == () and len(steps) == 13
    return steps, empty


def main():
    checks, fixtures = 0, []
    for width in range(1, 8):
        for signs in product((1, -1), repeat=width):
            rec = compile_replay([[signs[i] * (i + 1) for i in range(width)]])
            verify_record(rec)
            fixtures.append(["polarity", width, rec["paid"]])
            checks += 1
    for m in range(1, 9):
        rec = compile_replay([[i + 1] for i in range(m)])
        verify_record(rec)
        fixtures.append(["and_chain", m, rec["paid"]])
        checks += 1
    assert checks == 262

    block2 = [[1, 2], [1, -2], [-1, 2], [-1, -2]]
    rec = compile_replay(block2)
    env = verify_record(rec)
    downstream, empty = downstream_block2(rec, env)
    assert rec["paid"] == 21 and len(downstream) == 13
    assert not any(all(eval_clause(c, {1: a, 2: b}) for c in block2)
                   for a, b in product((False, True), repeat=2))
    sat = [[1, 2], [-1, 2]]
    sat_rec = compile_replay(sat)
    verify_record(sat_rec)
    assert any(all(eval_clause(c, {1: a, 2: b}) for c in sat)
               for a, b in product((False, True), repeat=2))
    malformed = [[], [[0]], [[1, -1]], [[1], []], [["x"]]]
    rejected = 0
    for bad in malformed:
        try:
            compile_replay(bad)
        except (AssertionError, TypeError, ValueError):
            rejected += 1
    assert rejected == len(malformed)

    payload = {"claim": "EVALUATOR-COST-REFLECTION-REFEREE341",
               "status": "PROVED_RESTRICTED_FINITE_CHECK",
               "polarity_and_chain_records_checked": checks,
               "block2": {"literal_count": rec["literal_count"],
                           "gate_nodes": len(rec["defs"]),
                           "replay_resolution_nodes": len(rec["res"]),
                           "source_to_root_paid": rec["paid"],
                           "downstream_resolution_nodes": len(downstream),
                           "spliced_paid": rec["paid"] + len(downstream),
                           "final_ref": empty, "record": rec,
                           "downstream": downstream},
               "sat_control_paid": sat_rec["paid"],
               "malformed_rejected": rejected,
               "fixture_digest": hashlib.sha256(json.dumps(fixtures, sort_keys=True).encode()).hexdigest()}
    out = Path("results/raw/arc/lspv5_341/evaluator_cost_reflection_referee341.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"checks": checks, "malformed_rejected": rejected,
                      "raw_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
                      "status": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
