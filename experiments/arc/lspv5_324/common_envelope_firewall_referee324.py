#!/usr/bin/env python3
"""Finite controls for COMMON-ENVELOPE-QUANTIFIER-FIREWALL-REFEREE324.

The symbolic results concern quantifier order and cost reflection. These
controls exercise only small exact SAT/UNSAT, reversible-encoder, parity-basis,
schema, and malformed-input cases. They do not regenerate an asymptotic hard
family or search for a shortest proof.
"""

import itertools
import json
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "results/raw/arc/lspv5_324/common_envelope_firewall_referee324.json"


def models(clauses, variables):
    result = []
    for bits in itertools.product((0, 1), repeat=variables):
        if all(any(bits[abs(lit) - 1] == (1 if lit > 0 else 0) for lit in clause) for clause in clauses):
            result.append(bits)
    return result


def php(pigeons, holes):
    def var(pigeon, hole):
        return pigeon * holes + hole + 1
    clauses = [tuple(var(p, h) for h in range(holes)) for p in range(pigeons)]
    for hole in range(holes):
        for first in range(pigeons):
            for second in range(first + 1, pigeons):
                clauses.append((-var(first, hole), -var(second, hole)))
    return clauses, pigeons * holes


def canonical_php_h(clauses, variables):
    for holes in range(1, int(math.sqrt(variables)) + 2):
        expected, count = php(holes + 1, holes)
        if variables == count and list(clauses) == expected:
            return holes
    return None


def encode_prefix_trap(clauses, variables, cutoff):
    source = [tuple(clause) for clause in clauses]
    recognized_h = canonical_php_h(source, variables)
    exceptional = recognized_h is not None and recognized_h <= cutoff
    fresh = variables + 1
    trailer = [(fresh,), (-fresh,)] if exceptional else [(fresh,)]
    return {"source_variables": variables, "source_clause_count": len(source),
            "encoded_variables": fresh, "fresh": fresh, "cutoff": cutoff,
            "recognized_h": recognized_h, "exceptional": exceptional,
            "clauses": source + trailer}


def decode_prefix_trap(record):
    required = {"source_variables", "source_clause_count", "encoded_variables", "fresh",
                "cutoff", "recognized_h", "exceptional", "clauses"}
    if set(record) != required:
        raise ValueError("record fields")
    n, m, fresh, cutoff = (record["source_variables"], record["source_clause_count"],
                            record["fresh"], record["cutoff"])
    clauses = [tuple(clause) for clause in record["clauses"]]
    if not all(isinstance(value, int) for value in (n, m, fresh, cutoff)):
        raise ValueError("integer metadata")
    if n < 0 or m < 0 or cutoff < 0 or fresh != n + 1:
        raise ValueError("metadata range")
    if record["encoded_variables"] != fresh or m > len(clauses):
        raise ValueError("encoded counts")
    source = clauses[:m]
    if any(abs(lit) == fresh for clause in source for lit in clause):
        raise ValueError("fresh collision")
    recognized_h = canonical_php_h(source, n)
    exceptional = recognized_h is not None and recognized_h <= cutoff
    expected = [(fresh,), (-fresh,)] if exceptional else [(fresh,)]
    if clauses[m:] != expected:
        raise ValueError("trailer")
    if record["recognized_h"] != recognized_h or record["exceptional"] != exceptional:
        raise ValueError("family tag")
    return source, n


def restrict_fresh_true(record):
    fresh, restricted = record["fresh"], []
    for clause in record["clauses"]:
        clause = tuple(clause)
        if fresh in clause:
            continue
        restricted.append(tuple(lit for lit in clause if lit != -fresh))
    return restricted


def tseitin_k4(charge):
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    incident = [[i for i, edge in enumerate(edges) if v in edge] for v in range(4)]
    clauses = []
    for vertex, edge_ids in enumerate(incident):
        for local in itertools.product((0, 1), repeat=3):
            if (sum(local) & 1) != charge[vertex]:
                clauses.append(tuple(edge_id + 1 if bit == 0 else -(edge_id + 1)
                                     for edge_id, bit in zip(edge_ids, local)))
    return clauses


def recode_charge(bits):
    return (sum(bits) & 1,) + tuple(bits[1:])


def decode_charge(encoded):
    if not encoded:
        raise ValueError("empty charge")
    return (sum(encoded) & 1,) + tuple(encoded[1:])


def parse_dimacs(text):
    lines = [line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith("c")]
    if not lines or not lines[0].startswith("p cnf "):
        raise ValueError("header")
    header = lines[0].split()
    if len(header) != 4:
        raise ValueError("header arity")
    variables, count = int(header[2]), int(header[3])
    if variables < 0 or count < 0:
        raise ValueError("negative count")
    clauses = []
    for line in lines[1:]:
        tokens = [int(token) for token in line.split()]
        if not tokens or tokens[-1] != 0 or 0 in tokens[:-1]:
            raise ValueError("terminator")
        clause = tuple(tokens[:-1])
        if any(abs(lit) < 1 or abs(lit) > variables for lit in clause):
            raise ValueError("literal range")
        clauses.append(clause)
    if len(clauses) != count:
        raise ValueError("clause count")
    return clauses, variables


def common_envelope_schema(spec):
    required = {"fixed_source_system", "fixed_target_system", "source_authenticated",
                "compiler_uniform", "construction_charged", "access_output_space_charged",
                "direction", "overhead", "quantifiers"}
    if set(spec) != required:
        return False
    return (spec["fixed_source_system"] and spec["fixed_target_system"]
            and spec["source_authenticated"] and spec["compiler_uniform"]
            and spec["construction_charged"] and spec["access_output_space_charged"]
            and spec["direction"] == "W_source<=p(N+code+construct+W_target)"
            and spec["overhead"] == "one_common_polynomial"
            and spec["quantifiers"] == "exists_p_forall_E_forall_F")


fixtures = {}
for holes in range(1, 4):
    unsat_clauses, unsat_variables = php(holes + 1, holes)
    sat_clauses, sat_variables = php(holes, holes)
    unsat_models, sat_models = models(unsat_clauses, unsat_variables), models(sat_clauses, sat_variables)
    assert not unsat_models and len(sat_models) == math.factorial(holes)
    fixtures[f"php_{holes+1}_{holes}"] = {"clauses": unsat_clauses, "variables": unsat_variables,
        "models": 0, "canonical_h": holes}
    fixtures[f"php_{holes}_{holes}"] = {"clauses": sat_clauses, "variables": sat_variables,
        "models": len(sat_models), "canonical_h": None}

fixtures.update({
    "horn_unsat": {"clauses": [(1,), (-1, 2), (-2,)], "variables": 2},
    "horn_sat": {"clauses": [(1,), (-1, 2)], "variables": 2},
    "two_sat_unsat": {"clauses": [(1, 2), (1, -2), (-1, 2), (-1, -2)], "variables": 2},
    "two_sat_sat": {"clauses": [(1, 2), (1, -2), (-1, 2)], "variables": 2},
    "k4_tseitin_odd": {"clauses": tseitin_k4((1, 0, 0, 0)), "variables": 6},
    "k4_tseitin_even": {"clauses": tseitin_k4((0, 0, 0, 0)), "variables": 6}})
for data in fixtures.values():
    data.setdefault("models", len(models(data["clauses"], data["variables"])))
    data.setdefault("canonical_h", canonical_php_h(data["clauses"], data["variables"]))
assert fixtures["horn_unsat"]["models"] == 0 and fixtures["horn_sat"]["models"] == 1
assert fixtures["two_sat_unsat"]["models"] == 0 and fixtures["two_sat_sat"]["models"] == 1
assert fixtures["k4_tseitin_odd"]["models"] == 0 and fixtures["k4_tseitin_even"]["models"] == 8

encoder_controls = []
for cutoff in range(0, 4):
    for name, data in fixtures.items():
        record = encode_prefix_trap(data["clauses"], data["variables"], cutoff)
        decoded, decoded_variables = decode_prefix_trap(record)
        assert decoded == [tuple(clause) for clause in data["clauses"]] and decoded_variables == data["variables"]
        encoded_models = models(record["clauses"], record["encoded_variables"])
        assert bool(encoded_models) == bool(data["models"])
        if record["exceptional"]:
            assert record["recognized_h"] <= cutoff and len(record["clauses"]) == len(data["clauses"]) + 2
            target_resolution_upper = 1
        else:
            assert restrict_fresh_true(record) == [tuple(clause) for clause in data["clauses"]]
            target_resolution_upper = None
        encoder_controls.append({"cutoff": cutoff, "fixture": name, "source_models": data["models"],
            "encoded_models": len(encoded_models), "exceptional": record["exceptional"],
            "recognized_h": record["recognized_h"], "source_prefix_exact": True,
            "target_resolution_upper": target_resolution_upper, "record": record})

corrupt_records = []
base = encode_prefix_trap(fixtures["php_3_2"]["clauses"], fixtures["php_3_2"]["variables"], 2)
for mutation in range(7):
    bad = json.loads(json.dumps(base))
    if mutation == 0: bad["fresh"] += 1
    elif mutation == 1: bad["encoded_variables"] += 1
    elif mutation == 2: bad["source_clause_count"] -= 1
    elif mutation == 3: bad["clauses"] = bad["clauses"][:-1]
    elif mutation == 4: bad["exceptional"] = False
    elif mutation == 5: bad["recognized_h"] = 3
    else: bad["clauses"][0][0] = bad["fresh"]
    try:
        decode_prefix_trap(bad)
        accepted = True
    except (ValueError, TypeError, IndexError):
        accepted = False
    assert not accepted
    corrupt_records.append({"mutation": mutation, "rejected": True})

parity_controls = []
for width in range(1, 13):
    for bits in itertools.product((0, 1), repeat=width):
        encoded = recode_charge(bits)
        assert decode_charge(encoded) == bits and encoded[0] == (sum(bits) & 1)
        label = sum(bits) & 1
        for index in range(width):
            flipped = list(bits); flipped[index] ^= 1
            assert (sum(flipped) & 1) != label
        parity_controls.append({"width": width, "bits": bits, "encoded": encoded, "label": label,
            "raw_query_depth": width, "supplied_recoded_query_depth": 1,
            "compiler_source_reads": width, "full_materialized_output_writes": width,
            "lazy_parity_xors": max(0, width - 1)})

valid_schema = {"fixed_source_system": True, "fixed_target_system": True,
    "source_authenticated": True, "compiler_uniform": True, "construction_charged": True,
    "access_output_space_charged": True,
    "direction": "W_source<=p(N+code+construct+W_target)",
    "overhead": "one_common_polynomial", "quantifiers": "exists_p_forall_E_forall_F"}
invalid_schemas = []
for key, value in [("fixed_source_system", False), ("fixed_target_system", False),
        ("source_authenticated", False), ("compiler_uniform", False), ("construction_charged", False),
        ("access_output_space_charged", False), ("direction", "W_target<=p(N+W_source)"),
        ("overhead", "exponential"), ("quantifiers", "forall_E_exists_p_E_forall_F"),
        ("quantifiers", "forall_N_exists_E_N_exists_p_N")]:
    candidate = dict(valid_schema); candidate[key] = value; invalid_schemas.append(candidate)
assert common_envelope_schema(valid_schema) and all(not common_envelope_schema(x) for x in invalid_schemas)

malformed = ["", "1 0\n", "p sat 1 1\n1 0\n", "p cnf 1\n1 0\n", "p cnf -1 0\n",
             "p cnf 1 2\n1 0\n", "p cnf 1 1\n2 0\n", "p cnf 1 1\n1\n"]
malformed_rejected = 0
for specimen in malformed:
    try: parse_dimacs(specimen)
    except (ValueError, TypeError): malformed_rejected += 1
assert malformed_rejected == len(malformed)

raw = {"artifact": "COMMON-ENVELOPE-QUANTIFIER-FIREWALL-REFEREE324",
 "status": "PROVED quantifier counterexample and common-envelope repair; finite controls; B1/B2/B3 OPEN",
 "fixed_target": "Rmix341 unchanged; theorem instantiated with ordinary Resolution for Haken PHP",
 "theorems": {
  "encoderwise_polynomial_failure": {"bad_quantifiers": "forall_E exists_p_E forall_F",
   "family": "canonical unary PHP_(h+1)^h",
   "encoders": "E_k appends opposite fresh units exactly on recognized PHP_h with h<=k and one positive fresh unit otherwise",
   "individual_property": "Each fixed E_k has some polynomial p_k; finite exceptional proofs enter p_k constants.",
   "collapse": "Choosing k=h after P_h gives O(N_h) construction/code plus one target Resolution node despite exponential source Resolution cost."},
  "common_envelope_repair": {"good_quantifiers": "exists_p forall_E forall_F",
   "premise": "W_R(F)<=p(N+code(E)+construct_E(F)+W_R(E(F)))",
   "consequence": "For J_R(F)=inf_E(code+construct+W_R(E(F))), W_R(F)<=p(N+J_R(F)+1).",
   "identity_control": "Identity representation gives J_R(F)<=O(N+W_R(F))."},
  "per_cutoff_algorithm_firewall": {"bad_quantifiers": "forall_N exists_A_N",
   "construction": "A_N stores the complete correctly labelled prefix through N and uses a fixed complete fallback beyond N.",
   "consequence": "T_A_N^wc(N)=O(N) with exponential program/table size; this does not imply one polynomial-time A for all N."},
  "charged_pipeline_equivalence": {"statement": "Every fixed fully charged compiler-consumer pipeline composes to one fixed SAT decider; every SAT decider is a degenerate identity pipeline.",
   "consequence": "An unrestricted fully charged representation-independent superpolynomial lower bound is an unrestricted SAT lower bound, not a consequence of proof-system hardness."}},
 "controls": {"fixtures": fixtures, "encoder_controls": encoder_controls,
  "corrupt_records": corrupt_records, "parity_controls": parity_controls,
  "schemas": {"valid": valid_schema, "invalid": invalid_schemas},
  "malformed_rejected": malformed_rejected},
 "accounting": {"E_k_parse_recognize": "O(N) for fixed k", "E_k_output": "N+O(log N) bits; source exact prefix",
  "E_k_peak": "O(N) if materialized; streaming still charges source reads and trailer",
  "recoded_parity": "query depth 1 only when recoded coordinates supplied; raw construction reads all h bits",
  "exponential_intermediate": "permitted and charged if materialized; unnecessary for compact parity basis",
  "producer": "small exact enumeration only; no asymptotic hard-family regeneration or proof optimizer"},
 "classification": {"common_envelope_theorem": "PROVED",
  "encoderwise_polynomials_suffice_for_representation_minimum": "FALSIFIED",
  "source_authentication_plus_reversibility_suffices": "FALSIFIED by established PHP trap synthesis",
  "pure_resolution_source_splicing": "PROVED/RESTRICTED by LSPV-1 Result 374",
  "full_Rmix341_common_envelope": "OPEN", "B1": "OPEN", "B2": "OPEN", "B3": "OPEN", "P_vs_NP": "OPEN"}}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n")
print(json.dumps({"out": str(OUT), "fixtures": len(fixtures), "encoder_controls": len(encoder_controls),
                  "parity_vectors": len(parity_controls), "corrupt_rejected": len(corrupt_records),
                  "schema_rejections": len(invalid_schemas), "malformed_rejected": malformed_rejected}, sort_keys=True))
