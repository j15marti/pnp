#!/usr/bin/env python3
"""SAT-encode the remaining exact-8-node binary derivations of rsmu_5_7_1.

Each derived line chooses two earlier source/derived lines and exactly one of
the relaxed Rmix341 binary rules:
  * exact clause Resolution with either pivot orientation;
  * exact affine GF(2) row addition;
  * conjunction whose output has essential support at most three.

Clause and affine aliases are therefore free, which strengthens the actual
calculus.  The last line is forced to the false 32-bit truth table.  SAT gives
a checkable <=8-node proof; UNSAT excludes every all-binary cost-eight DAG,
including the remaining bicyclic topology from REFEREE303.  REFEREE302 has
already excluded every <=7-node relaxed derivation, so every premise and every
nonfinal inference in an 8-node counterproof must occur in the final node's
ancestry.  We impose that logically forced ancestry condition as a symmetry
breaker; acyclicity then makes every selected line an ancestor of the root.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import platform
import resource
import sys
import time
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from experiments.arc.lspv5_300.peitl_mixed_floor_referee300 import (
    affine_tt,
    clause_tt,
    malformed_controls,
    mixed_combine,
    model_count,
    parity_cnf_k4,
    parse_dimacs,
    sign_flip_counts,
)
from experiments.arc.lspv5_302.peitl_seven_node_exclusion_referee302 import resolution_witness


INPUT = Path("results/raw/arc/lspv5_300_peitl/rsmu_5_7_1.cnf")
CNF_OUT = Path("results/raw/arc/2026-11-02_2148_LSPV5_PEITL_EIGHT_NODE_ENCODING_REFEREE304.cnf")
OUT = Path("results/raw/arc/2026-11-02_2148_LSPV5_PEITL_EXACT_EIGHT_REFEREE304_raw.json")


class Encoder:
    def __init__(self, sources, n=5, nodes=8):
        self.sources = sources
        self.n = n
        self.nodes = nodes
        self.width = 1 << n
        self.pool = IDPool()
        self.cnf = CNF()
        self.y = [[self.pool.id(("y", i, a)) for a in range(self.width)] for i in range(nodes)]
        self.meta = []
        self.degree_patterns = []

    def exactly_one(self, lits):
        self.cnf.extend(CardEnc.equals(lits=lits, bound=1, vpool=self.pool, encoding=EncType.seqcounter).clauses)

    def conditional_one(self, gate, lits):
        self.cnf.append([-gate] + lits)
        for lit in lits:
            self.cnf.append([-lit, gate])
        self.cnf.extend(CardEnc.atmost(lits=lits, bound=1, vpool=self.pool, encoding=EncType.seqcounter).clauses)

    def imply_const(self, selector, bit, value):
        self.cnf.append([-selector, bit if value else -bit])

    def imply_equal(self, selector, left, right):
        self.cnf.append([-selector, -left, right])
        self.cnf.append([-selector, left, -right])

    def line_bits(self, line):
        if line < len(self.sources):
            table = clause_tt(self.sources[line], self.n)
            return [(table >> a) & 1 for a in range(self.width)]
        return self.y[line - len(self.sources)]

    def mux(self, node, side, prior):
        sels = [self.pool.id(("parent", node, side, line)) for line in range(prior)]
        self.exactly_one(sels)
        bits = [self.pool.id(("mux", node, side, a)) for a in range(self.width)]
        for line, sel in enumerate(sels):
            source = self.line_bits(line)
            for a, target in enumerate(bits):
                if line < len(self.sources):
                    self.imply_const(sel, target, source[a])
                else:
                    self.imply_equal(sel, target, source[a])
        return sels, bits

    def tie_clause(self, gate, bits, pos, neg):
        for v in range(self.n):
            self.cnf.append([-gate, -pos[v], -neg[v]])
        for assignment, out in enumerate(bits):
            satisfied = []
            for v in range(self.n):
                satisfied.append(pos[v] if assignment >> v & 1 else neg[v])
            self.cnf.append([-gate, -out] + satisfied)
            for lit_state in satisfied:
                self.cnf.append([-gate, -lit_state, out])

    def encode_and(self, node, gate, left, right, out):
        for a in range(self.width):
            self.cnf.append([-gate, -left[a], -right[a], out[a]])
            self.cnf.append([-gate, left[a], -out[a]])
            self.cnf.append([-gate, right[a], -out[a]])
        pairs = list(__import__("itertools").combinations(range(self.n), 2))
        selectors = [self.pool.id(("inessential", node, u, v)) for u, v in pairs]
        self.conditional_one(gate, selectors)
        for sel, (u, v) in zip(selectors, pairs):
            for variable in (u, v):
                for assignment in range(self.width):
                    other = assignment ^ (1 << variable)
                    if assignment < other:
                        self.imply_equal(sel, out[assignment], out[other])
        return {"inessential_pairs": pairs, "selectors": selectors}

    def encode_xor(self, node, gate, left, right, out):
        left_sel = [self.pool.id(("affine_left", node, i)) for i in range(1 << (self.n + 1))]
        right_sel = [self.pool.id(("affine_right", node, i)) for i in range(1 << (self.n + 1))]
        out_sel = [self.pool.id(("affine_out", node, i)) for i in range(1 << (self.n + 1))]
        for sels in (left_sel, right_sel, out_sel):
            self.conditional_one(gate, sels)
        tables = [affine_tt(i >> 1, i & 1, self.n) for i in range(1 << (self.n + 1))]
        for sels, bits in ((left_sel, left), (right_sel, right), (out_sel, out)):
            for i, sel in enumerate(sels):
                for a, bit in enumerate(bits):
                    self.imply_const(sel, bit, (tables[i] >> a) & 1)
        for i, li in enumerate(left_sel):
            for j, rj in enumerate(right_sel):
                self.cnf.append([-li, -rj, out_sel[i ^ j]])
        return {"left": left_sel, "right": right_sel, "out": out_sel}

    def gated_or_equiv(self, gate, target, a, b):
        self.cnf.append([-gate, -a, target])
        self.cnf.append([-gate, -b, target])
        self.cnf.append([-gate, -target, a, b])

    def encode_resolution(self, node, gate, left, right, out):
        apos = [self.pool.id(("apos", node, v)) for v in range(self.n)]
        aneg = [self.pool.id(("aneg", node, v)) for v in range(self.n)]
        bpos = [self.pool.id(("bpos", node, v)) for v in range(self.n)]
        bneg = [self.pool.id(("bneg", node, v)) for v in range(self.n)]
        cpos = [self.pool.id(("cpos", node, v)) for v in range(self.n)]
        cneg = [self.pool.id(("cneg", node, v)) for v in range(self.n)]
        self.tie_clause(gate, left, apos, aneg)
        self.tie_clause(gate, right, bpos, bneg)
        self.tie_clause(gate, out, cpos, cneg)
        pivots = [self.pool.id(("pivot", node, v, orientation)) for v in range(self.n) for orientation in (0, 1)]
        self.conditional_one(gate, pivots)
        for p, sel in enumerate(pivots):
            v, orientation = divmod(p, 2)
            if orientation == 0:
                self.cnf.extend([[-sel, apos[v]], [-sel, bneg[v]]])
            else:
                self.cnf.extend([[-sel, aneg[v]], [-sel, bpos[v]]])
            for w in range(self.n):
                if w == v:
                    self.cnf.extend([[-sel, -cpos[w]], [-sel, -cneg[w]]])
                else:
                    self.gated_or_equiv(sel, cpos[w], apos[w], bpos[w])
                    self.gated_or_equiv(sel, cneg[w], aneg[w], bneg[w])
                self.cnf.append([-sel, -cpos[w], -cneg[w]])
        return {"apos": apos, "aneg": aneg, "bpos": bpos, "bneg": bneg, "cpos": cpos, "cneg": cneg, "pivots": pivots}

    def build(self):
        for node in range(self.nodes):
            prior = len(self.sources) + node
            left_sel, left = self.mux(node, "L", prior)
            right_sel, right = self.mux(node, "R", prior)
            # Every rule is symmetric in its two premises at the semantic
            # level (RES has both pivot orientations explicitly).  Canonical
            # left<right removes operand-order duplicates and same-parent
            # padding, which cannot occur in a minimum derivation.
            for i, li in enumerate(left_sel):
                for j, rj in enumerate(right_sel):
                    if i >= j:
                        self.cnf.append([-li, -rj])
            ops = {name: self.pool.id(("op", node, name)) for name in ("AND3", "XOR", "RES")}
            self.exactly_one(list(ops.values()))
            and_meta = self.encode_and(node, ops["AND3"], left, right, self.y[node])
            xor_meta = self.encode_xor(node, ops["XOR"], left, right, self.y[node])
            res_meta = self.encode_resolution(node, ops["RES"], left, right, self.y[node])
            self.meta.append({"left_sel": left_sel, "right_sel": right_sel, "ops": ops, "and": and_meta, "xor": xor_meta, "res": res_meta})

        # REFEREE302 proves there is no proof with at most seven nodes in the
        # same relaxation.  Hence an eight-node proof cannot contain padding:
        # every source and every nonfinal derived line must be selected later.
        # In a finite acyclic line order this is equivalent to root ancestry.
        last_nonfinal_line = len(self.sources) + self.nodes - 2
        line_uses = []
        for line in range(last_nonfinal_line + 1):
            uses = []
            for meta in self.meta:
                if line < len(meta["left_sel"]):
                    uses.append(meta["left_sel"][line])
                    uses.append(meta["right_sel"][line])
            self.cnf.append(uses)
            line_uses.append(uses)

        # There are 2*8=16 selected premise edges and 14 nonroot lines, all
        # used.  Therefore total outdegree excess is exactly two: either one
        # line has degree three, or two lines have degree two.  Reify all 119
        # exhaustive cases so solvers can check them independently by an
        # exhaustive cases (14+C(14,2)=105) so a solver can check them
        # independently by an assumption literal while retaining learned clauses.
        pattern_specs = [("triple", (i,)) for i in range(len(line_uses))]
        pattern_specs += [("double_pair", pair) for pair in itertools.combinations(range(len(line_uses)), 2)]
        for kind, exceptional in pattern_specs:
            selector = self.pool.id(("degree_pattern", kind, exceptional))
            expected = [1] * len(line_uses)
            if kind == "triple":
                expected[exceptional[0]] = 3
            else:
                expected[exceptional[0]] = 2
                expected[exceptional[1]] = 2
            for uses, bound in zip(line_uses, expected):
                if bound > len(uses):
                    self.cnf.append([-selector])
                    continue
                card = CardEnc.equals(lits=uses, bound=bound, vpool=self.pool, encoding=EncType.seqcounter)
                for clause in card.clauses:
                    self.cnf.append([-selector] + clause)
            self.degree_patterns.append({"kind": kind, "exceptional_lines": exceptional, "selector": selector})
        for bit in self.y[-1]:
            self.cnf.append([-bit])
        return self.cnf

    @staticmethod
    def chosen(model_set, variables):
        hits = [i for i, v in enumerate(variables) if v in model_set]
        if len(hits) != 1:
            raise AssertionError(("not one-hot", hits))
        return hits[0]

    def decode(self, model):
        m = set(x for x in model if x > 0)
        proof = []
        tables = [clause_tt(c, self.n) for c in self.sources]
        for node, meta in enumerate(self.meta):
            left_line = self.chosen(m, meta["left_sel"])
            right_line = self.chosen(m, meta["right_sel"])
            op_index = self.chosen(m, list(meta["ops"].values()))
            op = ("AND3", "XOR", "RES")[op_index]
            table = sum((self.y[node][a] in m) << a for a in range(self.width))
            detail = {}
            if op == "AND3":
                idx = self.chosen(m, meta["and"]["selectors"])
                detail["inessential_pair"] = meta["and"]["inessential_pairs"][idx]
            elif op == "XOR":
                detail["left_affine"] = self.chosen(m, meta["xor"]["left"])
                detail["right_affine"] = self.chosen(m, meta["xor"]["right"])
                detail["out_affine"] = self.chosen(m, meta["xor"]["out"])
            else:
                idx = self.chosen(m, meta["res"]["pivots"])
                detail["pivot_variable"] = idx // 2 + 1
                detail["orientation"] = idx & 1
            proof.append({"node": node, "left_line": left_line, "right_line": right_line, "op": op, "truth_table": table, **detail})
            tables.append(table)
        return proof


def validate_relaxed_proof(clauses, proof, n):
    from experiments.arc.lspv5_300.peitl_mixed_floor_referee300 import aliases
    clause_alias, affine_alias = aliases(n)
    tables = [clause_tt(c, n) for c in clauses]
    for step in proof:
        if step["left_line"] >= len(tables) or step["right_line"] >= len(tables):
            raise AssertionError("forward reference")
        made = mixed_combine(tables[step["left_line"]], tables[step["right_line"]], n, clause_alias, affine_alias)
        if step["truth_table"] not in made or made[step["truth_table"]].split("(")[0] != step["op"].replace("RES", "RES"):
            # Operation names for RES include the pivot, so check separately.
            if step["op"] == "RES" and step["truth_table"] in made and made[step["truth_table"]].startswith("RES("):
                pass
            else:
                raise AssertionError((step, made))
        tables.append(step["truth_table"])
    return tables[-1] == 0


def strict_parse_controls():
    return malformed_controls()


def main():
    started = time.perf_counter()
    raw = INPUT.read_bytes()
    n, clauses = parse_dimacs(raw.decode())
    encoder = Encoder(clauses, n=n, nodes=8)
    cnf = encoder.build()
    CNF_OUT.parent.mkdir(parents=True, exist_ok=True)
    cnf.to_file(CNF_OUT)
    solve_records = []
    model = None
    for name in ("glucose4",):
        t0 = time.perf_counter()
        with Solver(name=name, bootstrap_with=cnf.clauses) as solver:
            answer = False
            case_results = []
            for case_index, pattern in enumerate(encoder.degree_patterns):
                case_t0 = time.perf_counter()
                case_answer = solver.solve(assumptions=[pattern["selector"]])
                case_results.append({
                    "case_index": case_index,
                    "kind": pattern["kind"],
                    "exceptional_lines": pattern["exceptional_lines"],
                    "sat": case_answer,
                    "seconds": time.perf_counter() - case_t0,
                })
                if case_answer:
                    answer = True
                    candidate = solver.get_model()
                    break
                if (case_index + 1) % 20 == 0:
                    print(f"{name}: {case_index + 1}/{len(encoder.degree_patterns)} degree cases UNSAT", flush=True)
            stats = solver.accum_stats()
        solve_records.append({"solver": name, "sat": answer, "seconds": time.perf_counter() - t0, "stats": stats, "degree_cases": case_results})
        if answer and model is None:
            model = candidate
    if not solve_records:
        raise AssertionError("no solver record")
    sat = solve_records[0]["sat"]
    proof = encoder.decode(model) if sat else None
    if proof is not None and not validate_relaxed_proof(clauses, proof, n):
        raise AssertionError("decoded proof invalid")

    deletions = [model_count(clauses[:i] + clauses[i + 1 :], n) for i in range(len(clauses))]
    flips = sign_flip_counts(clauses, n)
    malformed = strict_parse_controls()
    odd_n, odd = parity_cnf_k4((1, 0, 0, 0))
    even_n, even = parity_cnf_k4((0, 0, 0, 0))
    parity = {"odd_models": model_count(odd, odd_n), "even_models": model_count(even, even_n)}
    upper = resolution_witness(clauses)
    assertions = {
        "authentic_sha256": hashlib.sha256(raw).hexdigest() == "6ca65edf800525363d4153b266cd4f4d207bd3a8977064c74996bc363ee8f6d6",
        "source_unsat": model_count(clauses, n) == 0,
        "clause_minimal": all(x > 0 for x in deletions),
        "all_occurrence_sign_flips_sat": all(x > 0 for x in flips),
        "all_degree_cases_checked": all(len(x["degree_cases"]) == len(encoder.degree_patterns) for x in solve_records),
        "encoding_result_checked": (proof is None and not sat) or validate_relaxed_proof(clauses, proof, n),
        "nine_node_resolution_upper": len(upper) == 9 and upper[-1]["clause"] == (),
        "all_malformed_rejected": all(malformed.values()),
        "parity_both_labels": parity == {"odd_models": 0, "even_models": 8},
    }
    if not all(assertions.values()):
        raise AssertionError(assertions)
    exact = "9" if not sat else "8"
    result = {
        "claim_id": "PEITL-EXACT-EIGHT-REFEREE304",
        "status": {
            "encoding": "PROVED/EXACT finite propositional encoding of every <=8-node relaxed binary derivation",
            "solver_result": "COMPUTATIONAL/EXHAUSTIVE finite with Glucose4; independent encoding audit and positive controls required",
            "mixed_minimum": f"PROVED/EXACT W_Rmix341={exact}" if not sat else "RELAXED SAT witness requires actual-rule replay",
            "B1_B2_B3": "OPEN",
        },
        "input": {"path": str(INPUT), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "variables": n, "clauses": clauses, "deletion_model_counts": deletions, "sign_flip_model_counts": flips},
        "fixed_calculus": "Rmix341 source-independent VARDEF; this encoding covers the all-binary RES/AND3/XOR class with free exact aliases; REFEREE303 separately excludes one DEF",
        "encoding": {"variables": cnf.nv, "clauses": len(cnf.clauses), "dimacs_path": str(CNF_OUT), "dimacs_sha256": hashlib.sha256(CNF_OUT.read_bytes()).hexdigest(), "nodes": 8, "truth_bits_per_line": 32},
        "solver_records": solve_records,
        "sat": sat,
        "decoded_relaxed_proof": proof,
        "resolution_upper_certificate": upper,
        "malformed_controls": malformed,
        "parity_controls": parity,
        "assertions": assertions,
        "optimizer_cost_note": "proof selection is free in W_R; CNF construction and SAT solving are external finite certification work",
        "resource_ledger": {"elapsed_seconds": time.perf_counter() - started, "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, "python": platform.python_version(), "all_phase_note": "includes source parsing, encoding, DIMACS materialization, all 105 Glucose4 assumption cases, controls and JSON"},
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(OUT), "sat": sat, "exact_candidate": exact, "encoding": result["encoding"], "solvers": solve_records, "proof": proof, "resources": result["resource_ledger"]}, indent=2))


if __name__ == "__main__":
    main()
