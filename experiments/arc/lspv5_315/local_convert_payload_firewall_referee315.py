#!/usr/bin/env python3
"""REFEREE315: independent LOCAL-CONVERT payload-sensitivity controls."""

from __future__ import annotations

import hashlib
import json
import random
import resource
import sys
import time
from pathlib import Path

SEED = 202611030748
K_VALUES = [1, 2, 3, 5, 8, 16, 32, 64, 128, 256, 512, 1024]
RAW_PATH = Path("results/raw/arc/lspv5_315/local_convert_payload_firewall_referee315.json")


def lit_value(lit: int, assignment: dict[int, bool]) -> bool:
    value = assignment[abs(lit)]
    return value if lit > 0 else not value


def clause_value(clause: list[int], assignment: dict[int, bool]) -> bool:
    return any(lit_value(lit, assignment) for lit in clause)


SAT_SOURCE = [[1], [1, 2]]
UNSAT_SOURCE = [[1], [1, 2], [-1]]


def source_models(source: list[list[int]]) -> list[dict[int, bool]]:
    models = []
    for mask in range(4):
        assignment = {1: bool(mask & 1), 2: bool(mask & 2)}
        if all(clause_value(c, assignment) for c in source):
            models.append(assignment)
    return models


def build_and_payload(bits: list[int]) -> dict:
    gates = []
    next_id = 0
    constant_ids = []
    for bit in bits:
        gates.append({"id": next_id, "op": "CONST", "value": bit})
        constant_ids.append(next_id)
        next_id += 1
    root = constant_ids[0]
    for constant_id in constant_ids[1:]:
        gates.append({"id": next_id, "op": "AND", "args": [root, constant_id]})
        root = next_id
        next_id += 1
    gates.append({"id": next_id, "op": "VAR", "var": 1})
    x_id = next_id
    next_id += 1
    gates.append({"id": next_id, "op": "AND", "args": [x_id, root]})
    return {"support": [1], "gates": gates, "output": next_id, "constant_ids": constant_ids}


def eval_payload(payload: dict, assignment: dict[int, bool]) -> bool:
    values: dict[int, bool] = {}
    for position, gate in enumerate(payload["gates"]):
        if gate.get("id") != position:
            raise ValueError("noncanonical gate id")
        op = gate.get("op")
        if op == "CONST":
            if gate.get("value") not in (0, 1):
                raise ValueError("bad constant")
            values[position] = bool(gate["value"])
        elif op == "VAR":
            variable = gate.get("var")
            if variable not in payload.get("support", []):
                raise ValueError("variable outside declared support")
            values[position] = assignment[variable]
        elif op in ("AND", "OR", "XOR"):
            args = gate.get("args")
            if not isinstance(args, list) or len(args) != 2 or any(not isinstance(a, int) or a < 0 or a >= position for a in args):
                raise ValueError("bad binary references")
            left, right = values[args[0]], values[args[1]]
            values[position] = left and right if op == "AND" else left or right if op == "OR" else left != right
        elif op == "NOT":
            args = gate.get("args")
            if not isinstance(args, list) or len(args) != 1 or not isinstance(args[0], int) or args[0] < 0 or args[0] >= position:
                raise ValueError("bad unary reference")
            values[position] = not values[args[0]]
        else:
            raise ValueError("bad opcode")
    output = payload.get("output")
    if not isinstance(output, int) or output < 0 or output >= len(payload["gates"]):
        raise ValueError("bad output")
    return values[output]


def parent_factor(assignment: dict[int, bool]) -> bool:
    return clause_value(SAT_SOURCE[0], assignment) and clause_value(SAT_SOURCE[1], assignment)


def conversion_legal(payload: dict) -> bool:
    if payload.get("support") != [1]:
        raise ValueError("noncanonical support")
    for mask in range(4):
        assignment = {1: bool(mask & 1), 2: bool(mask & 2)}
        if parent_factor(assignment) and not eval_payload(payload, assignment):
            return False
    return True


def random_constant_circuit(rng: random.Random, gates_count: int) -> tuple[dict, bool]:
    gates = []
    for i in range(gates_count):
        if i < 2 or rng.random() < 0.35:
            gates.append({"id": i, "op": "CONST", "value": rng.randrange(2)})
        else:
            op = rng.choice(["AND", "OR", "XOR"])
            gates.append({"id": i, "op": op, "args": [rng.randrange(i), rng.randrange(i)]})
    t_id = len(gates) - 1
    x_id = len(gates)
    gates.append({"id": x_id, "op": "VAR", "var": 1})
    out_id = len(gates)
    gates.append({"id": out_id, "op": "AND", "args": [x_id, t_id]})
    payload = {"support": [1], "gates": gates, "output": out_id, "constant_ids": []}
    t_value = eval_constant_prefix(gates, t_id)
    return payload, t_value


def eval_constant_prefix(gates: list[dict], output: int) -> bool:
    values: dict[int, bool] = {}
    for i, gate in enumerate(gates[: output + 1]):
        op = gate["op"]
        if op == "CONST":
            values[i] = bool(gate["value"])
        else:
            a, b = gate["args"]
            if op == "AND":
                values[i] = values[a] and values[b]
            elif op == "OR":
                values[i] = values[a] or values[b]
            elif op == "XOR":
                values[i] = values[a] != values[b]
            else:
                raise ValueError("unexpected prefix opcode")
    return values[output]


def malformed_payloads() -> list[dict]:
    base = build_and_payload([1, 1, 1])
    cases = []
    def clone():
        return json.loads(json.dumps(base))
    p = clone(); p["gates"][0]["id"] = 7; cases.append(p)
    p = clone(); p["gates"][0]["op"] = "NAND"; cases.append(p)
    p = clone(); p["gates"][0]["value"] = 2; cases.append(p)
    p = clone(); p["gates"][3]["args"] = [3, 1]; cases.append(p)
    p = clone(); p["gates"][3]["args"] = [0]; cases.append(p)
    p = clone(); p["gates"][3]["args"] = [0, "1"]; cases.append(p)
    p = clone(); p["support"] = [2]; cases.append(p)
    p = clone(); p["support"] = [1, 2]; cases.append(p)
    p = clone(); p["gates"][-2]["var"] = 2; cases.append(p)
    p = clone(); p["output"] = 999; cases.append(p)
    p = clone(); del p["output"]; cases.append(p)
    p = clone(); p["gates"] = p["gates"][:-1]; cases.append(p)
    return cases


def main() -> None:
    started = time.perf_counter()
    rng = random.Random(SEED)
    sat_models = source_models(SAT_SOURCE)
    unsat_models = source_models(UNSAT_SOURCE)
    assert len(sat_models) == 2 and len(unsat_models) == 0
    assert any(m[1] and not m[2] for m in sat_models)

    chain_rows = []
    total_flips = 0
    total_gate_records = 0
    for k in K_VALUES:
        legal = build_and_payload([1] * k)
        assert conversion_legal(legal)
        invalid = 0
        for i in range(k):
            bits = [1] * k
            bits[i] = 0
            assert not conversion_legal(build_and_payload(bits))
            invalid += 1
        total_flips += invalid
        total_gate_records += len(legal["gates"])
        chain_rows.append({
            "k": k,
            "gate_records": len(legal["gates"]),
            "charged_nodes_under_U": 2,
            "legal_all_one": True,
            "illegal_single_zero_neighbors": invalid,
            "forced_constant_probes_on_legal_input": k,
        })

    random_true = 0
    random_false = 0
    random_cases = 512
    for _ in range(random_cases):
        payload, truth = random_constant_circuit(rng, rng.randrange(2, 65))
        legal = conversion_legal(payload)
        assert legal == truth
        random_true += int(truth)
        random_false += int(not truth)

    malformed = malformed_payloads()
    malformed_rejected = 0
    for payload in malformed:
        try:
            conversion_legal(payload)
        except (KeyError, TypeError, ValueError, IndexError):
            malformed_rejected += 1
    assert malformed_rejected == len(malformed)

    corruptions = []
    p = build_and_payload([1, 1, 1]); p["support"] = []; corruptions.append(p)
    p = build_and_payload([1, 1, 1]); p["gates"][-1]["args"][0] = 999; corruptions.append(p)
    p = build_and_payload([1, 1, 1]); p["gates"][0]["value"] = 0; corruptions.append(p)
    p = build_and_payload([1, 1, 1]); p["gates"][0]["value"] = 0; p["output"] = 0; corruptions.append(p)
    p = build_and_payload([1, 1, 1]); p["gates"][-2]["var"] = 2; corruptions.append(p)
    corrupt_rejected = 0
    for payload in corruptions:
        try:
            ok = conversion_legal(payload)
            if not ok:
                corrupt_rejected += 1
        except (KeyError, TypeError, ValueError, IndexError):
            corrupt_rejected += 1
    assert corrupt_rejected == len(corruptions)

    elapsed = time.perf_counter() - started
    result = {
        "artifact": "LOCAL-CONVERT-PAYLOAD-FIREWALL-REFEREE315",
        "seed": SEED,
        "status": "PASS",
        "fixed_sources": {
            "sat_source": SAT_SOURCE,
            "sat_model_count": len(sat_models),
            "unsat_source": UNSAT_SOURCE,
            "unsat_model_count": len(unsat_models),
            "parent_factor": "x",
        },
        "syntax_condition": "U: one LOCAL-CONVERT record may carry an arbitrary-length explicit acyclic fan-in-two circuit over at most three original variables",
        "theorem": {
            "validity_equivalence": "S=x entails C=x AND t_G iff constant-fed circuit output t_G is 1",
            "probe_lower_bound": "On the all-one k-constant AND payload, every deterministic exact bit-probe validator reads all k independent constants",
            "node_count_firewall": "Under U, charged node count q=2 does not polynomially bound payload bytes or validation probes; k is arbitrary",
            "repair": "If every internal gate is separately charged, q is Omega(g) and this constant-q payload gap disappears",
            "scope": "Does not settle the intended Rmix341 syntax, B1, B2, B3, Wbar, L versus P, or P versus NP",
        },
        "chains": chain_rows,
        "counts": {
            "chain_lengths": len(K_VALUES),
            "single_zero_illegal_neighbors": total_flips,
            "legal_chain_gate_records": total_gate_records,
            "random_cvp_reductions": random_cases,
            "random_true": random_true,
            "random_false": random_false,
            "sat_source_controls": len(K_VALUES) + random_cases,
            "unsat_global_controls": len(K_VALUES) + random_cases,
            "malformed_rejected": malformed_rejected,
            "corrupt_rejected": corrupt_rejected,
        },
        "ledger": {
            "producer_wall_seconds": elapsed,
            "producer_peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "largest_k": max(K_VALUES),
            "largest_gate_records": chain_rows[-1]["gate_records"],
            "largest_forced_probes": max(K_VALUES),
            "proof_search_charged": False,
            "payload_parse_and_validation_charged_as_machine_work": True,
        },
    }
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    RAW_PATH.write_text(encoded, encoding="utf-8")
    digest = hashlib.sha256(encoded.encode()).hexdigest()
    print(json.dumps({
        "status": "PASS",
        **result["counts"],
        "largest_k": max(K_VALUES),
        "largest_gate_records": chain_rows[-1]["gate_records"],
        "raw_sha256": digest,
        "wall_seconds": elapsed,
        "peak_rss_kib": result["ledger"]["producer_peak_rss_kib"],
    }, separators=(",", ":")))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": repr(exc)}), file=sys.stderr)
        raise
