#!/usr/bin/env python3
"""Finite controls for REFEREE325.

The asymptotic lower bound is Haken's published theorem and is not
recomputed here.  These controls check only the exact compiler semantics,
uniform recognizable-island behavior, both labels, malformed records, and
the mandatory affine/Tseitin countercontrol.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


def canonical(cnf):
    return tuple(tuple(c) for c in cnf)


def max_var(cnf):
    return max((abs(x) for c in cnf for x in c), default=0)


def models(cnf):
    n = max_var(cnf)
    out = []
    for bits in itertools.product((False, True), repeat=n):
        if all(any(bits[abs(l)-1] if l > 0 else not bits[abs(l)-1] for l in c) for c in cnf):
            out.append(bits)
    return out


def php(holes, pigeons):
    def v(i, j):
        return i * holes + j + 1
    clauses = []
    for i in range(pigeons):
        clauses.append([v(i, j) for j in range(holes)])
    for j in range(holes):
        for i in range(pigeons):
            for k in range(i + 1, pigeons):
                clauses.append([-v(i, j), -v(k, j)])
    return clauses


def recognize_canonical_php(cnf):
    """Return h iff cnf is exactly the ordered unary PHP_(h+1)^h."""
    n = max_var(cnf)
    for h in range(1, int(n ** 0.5) + 2):
        target = php(h, h + 1)
        if canonical(cnf) == canonical(target):
            return h
    return None


def encode_island(cnf):
    """One fixed source-prefix exact encoder E_PHP."""
    z = max_var(cnf) + 1
    out = [list(c) for c in cnf]
    if recognize_canonical_php(cnf) is not None:
        out.extend([[z], [-z]])
        branch = "hard_island"
    else:
        out.append([z])
        branch = "benign"
    return out, branch, z


def k4_tseitin(charge):
    vertices = range(4)
    edges = [(i, j) for i in vertices for j in vertices if i < j]
    eid = {e: k + 1 for k, e in enumerate(edges)}
    clauses = []
    for v in vertices:
        inc = [eid[tuple(sorted((v, u)))] for u in vertices if u != v]
        for bits in itertools.product((0, 1), repeat=3):
            if (sum(bits) & 1) != charge[v]:
                clauses.append([(-x if bit else x) for x, bit in zip(inc, bits)])
    return clauses


def validate_cnf_record(rec):
    if not isinstance(rec, dict) or set(rec) != {"nvars", "clauses"}:
        return False
    if not isinstance(rec["nvars"], int) or rec["nvars"] < 0:
        return False
    if not isinstance(rec["clauses"], list):
        return False
    for c in rec["clauses"]:
        if not isinstance(c, list) or not c:
            return False
        if any(not isinstance(x, int) or x == 0 or abs(x) > rec["nvars"] for x in c):
            return False
    return True


def main():
    fixtures = []
    compiler_checks = 0
    for h in (1, 2, 3):
        hard = php(h, h + 1)
        assert recognize_canonical_php(hard) == h
        assert len(models(hard)) == 0
        encoded, branch, z = encode_island(hard)
        assert branch == "hard_island"
        assert encoded[:len(hard)] == hard
        assert encoded[-2:] == [[z], [-z]]
        assert len(models(encoded)) == 0
        compiler_checks += 6
        fixtures.append({"name": f"PHP_{h+1}^{h}", "label": "UNSAT", "models": 0,
                         "branch": branch, "source_clauses": len(hard),
                         "encoded_clauses": len(encoded), "resolution_output_cost": 1})

        sat = php(h, h)
        assert recognize_canonical_php(sat) is None
        sm = models(sat)
        assert len(sm) == (1 if h == 1 else 2 if h == 2 else 6)
        encoded_sat, branch_sat, zsat = encode_island(sat)
        em = models(encoded_sat)
        assert branch_sat == "benign"
        assert encoded_sat[:len(sat)] == sat
        assert all(m[zsat-1] for m in em)
        assert len(em) == len(sm)
        compiler_checks += 7
        fixtures.append({"name": f"PHP_{h}^{h}", "label": "SAT", "models": len(sm),
                         "branch": branch_sat, "source_clauses": len(sat),
                         "encoded_clauses": len(encoded_sat)})

    # Ordinary non-island controls: contradictory units, Horn SAT, and 2-SAT SAT.
    extra = [
        ("unit_core", [[1], [-1]], 0),
        ("horn_sat", [[1], [-1, 2]], 1),
        ("two_sat", [[1, 2], [-1, 2], [1, -2]], 1),
    ]
    for name, cnf, expected in extra:
        before = len(models(cnf))
        enc, branch, z = encode_island(cnf)
        after = len(models(enc))
        assert branch == "benign" and before == expected and after == expected
        assert enc[:len(cnf)] == cnf and enc[-1] == [z]
        compiler_checks += 5
        fixtures.append({"name": name, "label": "SAT" if expected else "UNSAT",
                         "models": expected, "branch": branch})

    odd = k4_tseitin([1, 0, 0, 0])
    even = k4_tseitin([0, 0, 0, 0])
    odd_count, even_count = len(models(odd)), len(models(even))
    assert odd_count == 0 and even_count == 8

    malformed = [
        {}, {"nvars": 1}, {"clauses": [[1]]},
        {"nvars": -1, "clauses": [[1]]},
        {"nvars": 1.0, "clauses": [[1]]},
        {"nvars": 1, "clauses": "1 0"},
        {"nvars": 1, "clauses": [[]]},
        {"nvars": 1, "clauses": [[0]]},
        {"nvars": 1, "clauses": [[2]]},
        {"nvars": 1, "clauses": [["1"]]},
    ]
    rejected = sum(not validate_cnf_record(x) for x in malformed)
    assert rejected == len(malformed)

    result = {
        "id": "REFEREE325",
        "theorem_anchor": {
            "family": "canonical unary PHP_(h+1)^h",
            "encoding": "explicit signed CNF; N_h=Theta(h^3 log h) bits under DIMACS-style indices",
            "system": "ordinary unrestricted shared-DAG Resolution",
            "quantifiers": "exists c>0,h0 forall h>=h0 forall Resolution refutations pi",
            "strength": "|pi| >= 2^(c h); no ER, Rmix341, or arbitrary-machine consequence",
        },
        "counterexample": {
            "encoder": "one fixed E_PHP, source-prefix and reversible",
            "hard_branch": "append fresh (z),(-z)",
            "other_branch": "append fresh (z)",
            "construction": "uniform polynomial time; linear output and source scan",
            "consequence": "W_Res(E_PHP(PHP_(h+1)^h))=1, so no common polynomial cost-reflection envelope over this encoder class",
        },
        "algorithm_corollary": {
            "decider": "one fixed A_PHP recognizes the whole canonical family, else complete fallback",
            "classification": "B1 fails for ordinary Resolution; B2/B3 unaffected",
        },
        "fixtures": fixtures,
        "compiler_checks": compiler_checks,
        "tseitin_control": {"odd_models": odd_count, "even_models": even_count},
        "malformed_rejected": rejected,
        "malformed_total": len(malformed),
        "statuses": {
            "broad_common_envelope": "FALSIFIED",
            "proof_carrying_model_relative_envelope": "OPEN",
            "Rmix341_superpolynomial_hardness": "OPEN",
            "B1_Rmix341": "OPEN", "B2_Rmix341": "OPEN", "B3_Rmix341": "OPEN",
            "P_vs_NP": "OPEN",
        },
    }
    payload = json.dumps(result, sort_keys=True, indent=2) + "\n"
    result["prehash_sha256"] = hashlib.sha256(payload.encode()).hexdigest()
    out = Path("results/raw/arc/lspv5_325/recognizable_island_firewall_referee325.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"fixtures": len(fixtures), "compiler_checks": compiler_checks,
                      "malformed_rejected": rejected, "odd_models": odd_count,
                      "even_models": even_count}, sort_keys=True))


if __name__ == "__main__":
    main()
