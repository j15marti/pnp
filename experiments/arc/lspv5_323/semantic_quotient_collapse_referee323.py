#!/usr/bin/env python3
"""Finite controls for SEMANTIC-QUOTIENT-COLLAPSE-REFEREE323.

The controls test only the exact semantic quotient and quantifier lemmas. They
do not search for a new asymptotic hard family or certify a proof optimum.
"""

import itertools
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "results/raw/arc/lspv5_323/semantic_quotient_collapse_referee323.json"


def models(clauses, variables):
    answer = []
    for bits in itertools.product((0, 1), repeat=variables):
        if all(
            any(bits[abs(lit) - 1] == (1 if lit > 0 else 0) for lit in clause)
            for clause in clauses
        ):
            answer.append(bits)
    return answer


def projected_relation(clauses, variables, boundary):
    relation = set()
    for assignment in models(clauses, variables):
        relation.add(tuple(assignment[i - 1] for i in boundary))
    return [list(item) for item in sorted(relation)]


def tseitin_k4(charge):
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    incident = [[i for i, edge in enumerate(edges) if v in edge] for v in range(4)]
    clauses = []
    for vertex, edge_ids in enumerate(incident):
        for local in itertools.product((0, 1), repeat=3):
            if (sum(local) & 1) != charge[vertex]:
                clauses.append(
                    tuple(
                        (edge_id + 1) if bit == 0 else -(edge_id + 1)
                        for edge_id, bit in zip(edge_ids, local)
                    )
                )
    return clauses


def php(pigeons, holes):
    def var(pigeon, hole):
        return pigeon * holes + hole + 1

    clauses = [tuple(var(p, h) for h in range(holes)) for p in range(pigeons)]
    for hole in range(holes):
        for first in range(pigeons):
            for second in range(first + 1, pigeons):
                clauses.append((-var(first, hole), -var(second, hole)))
    return clauses


def parse_dimacs(text):
    lines = [line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith("c")]
    if not lines or not lines[0].startswith("p cnf "):
        raise ValueError("missing header")
    header = lines[0].split()
    if len(header) != 4:
        raise ValueError("bad header")
    variables, expected = int(header[2]), int(header[3])
    if variables < 0 or expected < 0:
        raise ValueError("negative count")
    clauses = []
    for line in lines[1:]:
        tokens = [int(token) for token in line.split()]
        if not tokens or tokens[-1] != 0 or 0 in tokens[:-1]:
            raise ValueError("bad terminator")
        clause = tuple(tokens[:-1])
        if any(abs(lit) < 1 or abs(lit) > variables for lit in clause):
            raise ValueError("literal out of range")
        clauses.append(clause)
    if len(clauses) != expected:
        raise ValueError("clause count")
    return clauses, variables


def canonical_dimacs(clauses, variables):
    body = [" ".join(str(lit) for lit in clause) + " 0" for clause in clauses]
    return "\n".join([f"p cnf {variables} {len(clauses)}", *body, ""])


def brute_force_label_dimacs(text):
    clauses, variables = parse_dimacs(text)
    return bool(models(clauses, variables))


def specialized_total_decider(target_text, target_label, candidate_text):
    """A_x: fast on one target, complete brute-force fallback elsewhere."""
    try:
        parse_dimacs(candidate_text)
    except (ValueError, TypeError):
        return "MALFORMED"
    if candidate_text == target_text:
        return target_label
    return brute_force_label_dimacs(candidate_text)


fixtures = {
    "odd_k4_tseitin": (tseitin_k4((1, 0, 0, 0)), 6, []),
    "even_k4_tseitin": (tseitin_k4((0, 0, 0, 0)), 6, []),
    "php_3_2": (php(3, 2), 6, []),
    "horn_unsat": ([(1,), (-1, 2), (-2,)], 2, []),
    "horn_sat_neighbor": ([(1,), (-1, 2)], 2, []),
    "two_sat_unsat": ([(1, 2), (1, -2), (-1, 2), (-1, -2)], 2, []),
    "two_sat_sat_neighbor": ([(1, 2), (1, -2), (-1, 2)], 2, []),
    "equality_boundary": ([(-1, 2), (1, -2)], 2, [1, 2]),
    "equality_aux_boundary": ([(-1, 3), (1, -3), (-3, 2), (3, -2)], 3, [1, 2]),
    "guarded_unsat_internal": ([(-1, 2), (-1, -2)], 2, [1]),
    "guarded_sat_sibling": ([(-1, 2)], 2, [1]),
}

fixture_results = {}
for name, (clauses, variables, boundary) in fixtures.items():
    relation = projected_relation(clauses, variables, boundary)
    fixture_results[name] = {
        "clauses": clauses,
        "variables": variables,
        "boundary": boundary,
        "model_count": len(models(clauses, variables)),
        "relation": relation,
    }

assert fixture_results["odd_k4_tseitin"]["model_count"] == 0
assert fixture_results["even_k4_tseitin"]["model_count"] == 8
assert fixture_results["php_3_2"]["model_count"] == 0
assert fixture_results["horn_unsat"]["relation"] == []
assert fixture_results["two_sat_unsat"]["relation"] == []
assert fixture_results["equality_boundary"]["relation"] == [[0, 0], [1, 1]]
assert fixture_results["equality_aux_boundary"]["relation"] == [[0, 0], [1, 1]]
assert fixture_results["guarded_unsat_internal"]["relation"] == [[0]]
assert fixture_results["guarded_sat_sibling"]["relation"] == [[0], [1]]

closed_unsat = ["odd_k4_tseitin", "php_3_2", "horn_unsat", "two_sat_unsat"]
closed_sat = ["even_k4_tseitin", "horn_sat_neighbor", "two_sat_sat_neighbor"]
assert all(fixture_results[name]["relation"] == [] for name in closed_unsat)
assert all(fixture_results[name]["relation"] == [[]] for name in closed_sat)

malformed = [
    "",
    "1 0\n",
    "p sat 1 1\n1 0\n",
    "p cnf 1\n1 0\n",
    "p cnf -1 0\n",
    "p cnf 1 2\n1 0\n",
    "p cnf 1 1\n2 0\n",
    "p cnf 1 1\n1\n",
]
malformed_rejected = 0
for specimen in malformed:
    try:
        parse_dimacs(specimen)
    except (ValueError, TypeError):
        malformed_rejected += 1
assert malformed_rejected == len(malformed)

dimacs = {
    name: canonical_dimacs(data["clauses"], data["variables"])
    for name, data in fixture_results.items()
}
labels = {
    name: bool(data["model_count"])
    for name, data in fixture_results.items()
}
hardcode_checks = []
for target in closed_unsat + closed_sat:
    target_text = dimacs[target]
    target_label = labels[target]
    for candidate in closed_unsat + closed_sat:
        observed = specialized_total_decider(
            target_text, target_label, dimacs[candidate]
        )
        assert observed == labels[candidate]
        hardcode_checks.append(
            {
                "target": target,
                "candidate": candidate,
                "same_input": target == candidate,
                "correct": observed == labels[candidate],
            }
        )
    assert specialized_total_decider(target_text, target_label, malformed[0]) == "MALFORMED"

quotient_counts = {str(boundary): 2 ** (2 ** boundary) for boundary in range(4)}
assert quotient_counts == {"0": 2, "1": 4, "2": 16, "3": 256}

raw = {
    "artifact": "SEMANTIC-QUOTIENT-ALGORITHM-MINIMUM-COLLAPSE-REFEREE323",
    "status": "PROVED no-go lemmas; finite controls; B1/B2/B3 OPEN",
    "fixed_target": "Rmix341 unchanged; source-authenticated unit-weight mixed inference DAG",
    "theorems": {
        "semantic_quotient": {
            "definition": "Rel_B(F)={b in {0,1}^B : exists y F(b,y)=1}",
            "class_bound": "at most 2^(2^|B|) exact projected relations",
            "closed_consequence": "B=empty gives exactly SAT and UNSAT classes; all closed UNSAT sources are extensionally identical",
            "cost_consequence": "Any extensional invariant lower-bounding native cost on every exact representation is bounded by the cheapest representative; at most 1 on UNSAT under the opposite-unit Rmix341 control.",
        },
        "pointwise_algorithm_minimum": {
            "construction": "For fixed x, A_x compares input y with x, returns x's stored correct label on equality, and uses complete brute force otherwise.",
            "consequence": "min over total correct algorithms chosen after x of code acquisition plus target runtime is O(|x|)",
            "non_consequence": "Does not refute family-wide worst-case quantifiers that fix A before choosing an unbounded hard family.",
        },
        "uniformity_trilemma": [
            "Free exact representative choice collapses SAT/UNSAT to TOP/BOTTOM.",
            "Per-input or per-size selection is forbidden nonuniform hardcoding.",
            "One charged all-input exact canonicalizer is itself a SAT decision procedure.",
        ],
    },
    "controls": {
        "fixtures": fixture_results,
        "closed_unsat_names": closed_unsat,
        "closed_sat_names": closed_sat,
        "quotient_class_counts": quotient_counts,
        "malformed_rejected": malformed_rejected,
        "hardcoded_total_decider_checks": hardcode_checks,
    },
    "accounting": {
        "explicit_B_bit_intermediate": "at least ceil(B/w) word writes; B live bits if retained",
        "streamed_intermediate": "output time remains; peak space may fall",
        "implicit_intermediate": "charge descriptor and actual evaluations/accesses, not a virtual dense table",
        "producer_work": "complete enumeration of at most 64 assignments per finite fixture",
        "optimizer_discovery": "not charged to W_R, but uniform representation construction is charged to an implemented solver",
        "host_runtime_and_rss": "experimental metadata only, not FLMV resources",
    },
    "classification": {
        "semantic_representation_independent_growing_invariant": "FALSIFIED for closed SAT/UNSAT by quotient collapse",
        "source_query_sensitivity": "PROVED but source/model relative and at most linear in source bits",
        "Rmix341_superpolynomial_lower_bound": "OPEN",
        "B1": "OPEN",
        "B2": "OPEN",
        "B3": "OPEN",
        "P_vs_NP": "OPEN",
    },
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n")
print(
    json.dumps(
        {
            "out": str(OUT),
            "fixtures": len(fixture_results),
            "hardcode_checks": len(hardcode_checks),
            "malformed_rejected": malformed_rejected,
            "quotient_counts": quotient_counts,
        },
        sort_keys=True,
    )
)
