#!/usr/bin/env python3
"""REFEREE355: LOCAL internal-port soundness firewall for R_mix341.

The original rule derives one root condition.  This audit distinguishes:
  * root assertion: the LOCAL conclusion, checked by implication;
  * internal term: a subexpression value, not asserted true;
  * internal assertion: an unsound permissive interpretation in general.

The concrete witness has a satisfiable source, an exact AND3 factor x, and a
LOCAL root x OR (NOT x).  Exporting the internal NOT x as an asserted clause
allows a false Resolution refutation of the SAT source.
"""

from __future__ import annotations

import itertools
import json
from dataclasses import dataclass
from typing import Iterable


class Reject(ValueError):
    pass


Val = tuple[int, ...]
Table = tuple[int, ...]


def parse_dimacs(text: str) -> tuple[int, list[tuple[int, ...]]]:
    lines = [line.strip() for line in text.splitlines()
             if line.strip() and not line.lstrip().startswith("c")]
    if not lines or lines[0].split()[:2] != ["p", "cnf"] or len(lines[0].split()) != 4:
        raise Reject("bad-header")
    try:
        n, m = map(int, lines[0].split()[2:])
    except ValueError as exc:
        raise Reject("bad-header-int") from exc
    if n < 0 or m < 0:
        raise Reject("negative-header")
    clauses: list[tuple[int, ...]] = []
    for line in lines[1:]:
        try:
            row = tuple(map(int, line.split()))
        except ValueError as exc:
            raise Reject("bad-literal") from exc
        if not row or row[-1] != 0 or 0 in row[:-1]:
            raise Reject("bad-terminator")
        clause = row[:-1]
        if any(abs(lit) < 1 or abs(lit) > n for lit in clause):
            raise Reject("literal-out-of-range")
        clauses.append(clause)
    if len(clauses) != m:
        raise Reject("clause-count")
    return n, clauses


def valuations(n: int) -> list[Val]:
    return list(itertools.product((0, 1), repeat=n))


def clause_value(clause: Iterable[int], val: Val) -> int:
    return int(any(val[abs(lit) - 1] == int(lit > 0) for lit in clause))


def clause_table(clause: tuple[int, ...], n: int) -> Table:
    return tuple(clause_value(clause, val) for val in valuations(n))


def models(n: int, clauses: list[tuple[int, ...]]) -> list[Val]:
    return [val for val in valuations(n)
            if all(clause_value(clause, val) for clause in clauses)]


def t_and(a: Table, b: Table) -> Table:
    if len(a) != len(b):
        raise Reject("table-length")
    return tuple(x & y for x, y in zip(a, b))


def t_not(a: Table) -> Table:
    return tuple(1 ^ x for x in a)


def t_or(a: Table, b: Table) -> Table:
    if len(a) != len(b):
        raise Reject("table-length")
    return tuple(x | y for x, y in zip(a, b))


def entails(a: Table, b: Table) -> bool:
    return all(not x or y for x, y in zip(a, b))


@dataclass(frozen=True)
class Port:
    name: str
    table: Table
    kind: str  # root_assertion | internal_term | internal_assertion


def res_unit(left: tuple[int, ...], right: tuple[int, ...], pivot: int) -> tuple[int, ...]:
    if left != (pivot,) or right != (-pivot,):
        raise Reject("not-complementary-units")
    return ()


SOURCE_SAT = "p cnf 2 2\n1 0\n1 2 0\n"
SOURCE_UNSAT = "p cnf 1 2\n1 0\n-1 0\n"


def witness() -> dict[str, object]:
    n, clauses = parse_dimacs(SOURCE_SAT)
    source_models = models(n, clauses)
    source_tables = [clause_table(c, n) for c in clauses]

    # Paid node 1: exact AND3 factor x.
    factor = t_and(source_tables[0], source_tables[1])
    x_table = clause_table((1,), n)
    if factor != x_table:
        raise AssertionError("AND3 is not exact x")

    # Paid node 2: LOCAL root x OR NOT x, with internal gate g=NOT x.
    internal_g = t_not(x_table)
    root = t_or(x_table, internal_g)
    if not entails(factor, root):
        raise AssertionError("LOCAL root not entailed")
    if entails(factor, internal_g):
        raise AssertionError("internal NOT x unexpectedly entailed")

    root_port = Port("root", root, "root_assertion")
    term_port = Port("g", internal_g, "internal_term")
    bad_port = Port("g", internal_g, "internal_assertion")

    # Native/root-only: an internal term is not a RES premise.
    native_rejection = ""
    try:
        if term_port.kind != "root_assertion":
            raise Reject("internal-term-is-not-an-asserted-clause")
        res_unit((1,), (-1,), 1)
    except Reject as exc:
        native_rejection = str(exc)

    # Permissive asserted-port completion accepts the forged contradiction.
    permissive_empty = res_unit((1,), (-1,), 1) if bad_port.kind == "internal_assertion" else None

    return {
        "source_models": source_models,
        "node1_and3_factor": factor,
        "node2_local_root": root_port.table,
        "node2_internal_not_x": term_port.table,
        "factor_entails_root": entails(factor, root_port.table),
        "factor_entails_internal": entails(factor, term_port.table),
        "native_rejection": native_rejection,
        "permissive_exported_assertion_resolvent": list(permissive_empty) if permissive_empty is not None else None,
        "permissive_completion_sound": not (source_models and permissive_empty == ()),
    }


def run() -> dict[str, object]:
    checks = 0

    # Both-label source controls.
    ns, cs = parse_dimacs(SOURCE_SAT)
    sat_models = models(ns, cs)
    checks += 2  # parse + exact model list
    assert sat_models == [(1, 0), (1, 1)]
    nu, cu = parse_dimacs(SOURCE_UNSAT)
    unsat_models = models(nu, cu)
    checks += 2
    assert unsat_models == []

    w = witness()
    checks += 9
    assert w["source_models"] == [(1, 0), (1, 1)]
    assert w["node1_and3_factor"] == (0, 0, 1, 1)
    assert w["node2_local_root"] == (1, 1, 1, 1)
    assert w["node2_internal_not_x"] == (1, 1, 0, 0)
    assert w["factor_entails_root"] is True
    assert w["factor_entails_internal"] is False
    assert w["native_rejection"] == "internal-term-is-not-an-asserted-clause"
    assert w["permissive_exported_assertion_resolvent"] == []
    assert w["permissive_completion_sound"] is False

    # Exhaustive two-variable firewall.  For every nonempty factor A and every
    # internal function g, the circuit root g OR NOT g is entailed.  Exporting
    # g as an assertion is unsound exactly when A does not entail g.
    nonempty_factors = 0
    factor_gate_pairs = 0
    unsound_exports = 0
    entailed_exports = 0
    for factor_bits in itertools.product((0, 1), repeat=4):
        if not any(factor_bits):
            continue
        nonempty_factors += 1
        for gate_bits in itertools.product((0, 1), repeat=4):
            factor_gate_pairs += 1
            root = t_or(gate_bits, t_not(gate_bits))
            checks += 2
            assert root == (1, 1, 1, 1)
            assert entails(factor_bits, root)
            if entails(factor_bits, gate_bits):
                entailed_exports += 1
            else:
                unsound_exports += 1
                checks += 1
                assert any(a and not g for a, g in zip(factor_bits, gate_bits))
    checks += 4
    assert nonempty_factors == 15
    assert factor_gate_pairs == 240
    assert unsound_exports == 175
    assert entailed_exports == 65

    # Port-kind and mutation controls.
    x = (0, 0, 1, 1)
    not_x = (1, 1, 0, 0)
    modes = {
        "private": False,
        "internal_term": False,
        "internal_assertion": True,
        "root_assertion": True,
    }
    for mode, admissible_as_assertion in modes.items():
        checks += 1
        if mode in {"private", "internal_term"}:
            assert not admissible_as_assertion
        else:
            assert admissible_as_assertion
    checks += 4
    assert entails(x, (1, 1, 1, 1))
    assert not entails(x, not_x)
    assert res_unit((1,), (-1,), 1) == ()
    try:
        res_unit((1,), (1,), 1)
    except Reject:
        pass
    else:
        raise AssertionError("same-sign units resolved")

    malformed = [
        "", "p cnd 2 0\n", "p cnf 2 1\n3 0\n",
        "p cnf 2 1\n1\n", "p cnf 2 2\n1 0\n",
    ]
    for text in malformed:
        try:
            parse_dimacs(text)
        except Reject:
            pass
        else:
            raise AssertionError(("malformed accepted", text))
        checks += 1

    # Offline state-XOR diagnostic: root semantics are identical between the
    # native and permissive views; one port-kind bit changes proof validity.
    native_root_bits = tuple(w["node2_local_root"])
    permissive_root_bits = tuple(w["node2_local_root"])
    d_logic_root = sum(a ^ b for a, b in zip(native_root_bits, permissive_root_bits))
    native_port_tag = 0
    permissive_port_tag = 1
    d_phys_declared_tag = native_port_tag ^ permissive_port_tag
    checks += 2
    assert d_logic_root == 0
    assert d_phys_declared_tag == 1

    return {
        "schema": "Rmix341-local-port-soundness-v1",
        "status": "PASS",
        "checks": checks,
        "witness": w,
        "exhaustive_two_variable_catalog": {
            "nonempty_factors": nonempty_factors,
            "internal_functions": 16,
            "factor_gate_pairs": factor_gate_pairs,
            "unsound_asserted_exports": unsound_exports,
            "entailed_exports": entailed_exports,
        },
        "controls": {
            "sat_models": sat_models,
            "unsat_models": unsat_models,
            "malformed_rejected": len(malformed),
            "port_modes": modes,
        },
        "offline_state_xor": {
            "d_logic_root": d_logic_root,
            "d_phys_declared_port_tag": d_phys_declared_tag,
            "warning": "offline diagnostic, not a machine lower bound",
        },
        "proved_scope": (
            "LOCAL internal gates cannot automatically be exported as asserted "
            "conditions; only the checked root is asserted."
        ),
        "not_claimed": [
            "internal terms can never be serialized",
            "full byte grammar is complete",
            "B3 is refuted for R_mix341",
            "unrestricted SAT machine lower bound",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
