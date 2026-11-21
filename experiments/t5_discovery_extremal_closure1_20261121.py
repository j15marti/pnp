"""Exact finite audit for T5-EXTREMAL-COUNT-CLOSURE1; Python 3, no packages.
Truth tables are audit inputs, not a proposed succinct-source counting algorithm.
"""
import hashlib
import itertools
import json
import math
from pathlib import Path


def authenticate(scope, table, claimed_count):
    if len(set(scope)) != len(scope):
        raise ValueError("duplicate scope name")
    if len(table) != 1 << len(scope) or any(type(b) is not bool for b in table):
        raise ValueError("wrong Boolean universe")
    if type(claimed_count) is not int or sum(table) != claimed_count:
        raise ValueError("incorrect exact count")
    # Actual semantic authentication by full enumeration, deliberately paid.
    return (tuple(scope), claimed_count)


def close_verified(verified):
    scope, count = verified
    # Internal API: only authenticate() outputs are used in this runner.
    if count == 0:
        return (scope, False)
    if count == 1 << len(scope):
        return (scope, True)
    return None


def run():
    rows = []
    rejected = 0
    for s in range(5):
        scope = tuple(range(s))
        universe = 1 << s
        histogram = [0] * (universe + 1)
        witnesses = [[] for _ in histogram]
        accepted = 0
        for mask in range(1 << universe):
            table = tuple(bool(mask >> i & 1) for i in range(universe))
            count = sum(table)
            histogram[count] += 1
            if len(witnesses[count]) < 2:
                witnesses[count].append(mask)
            output = close_verified(authenticate(scope, table, count))
            if output is not None:
                accepted += 1
                assert all(value == output[1] for value in table)
                assert output[0] == scope
                assert count == (universe if output[1] else 0)
            else:
                assert 0 < count < universe
        assert histogram == [math.comb(universe, z) for z in range(universe + 1)]
        assert accepted == 2
        for z in range(1, universe):
            assert len(witnesses[z]) == 2 and witnesses[z][0] != witnesses[z][1]
        # Both kinds of fabricated extremal answer are rejected on each scope.
        for table, fake in [(tuple([False] * universe), universe),
                            (tuple([True] * universe), 0)]:
            try:
                authenticate(scope, table, fake)
            except ValueError:
                rejected += 1
            else:
                raise AssertionError("fabricated count accepted")
        rows.append(dict(scope_size=s, tables=1 << universe, accepted=accepted,
                         cardinality_histogram=histogram,
                         ambiguous_nonextreme_counts=universe - 1))
    # Truth-table transport under all permutations for scopes up to three.
    transported = 0
    for s in range(4):
        assignments = list(itertools.product((False, True), repeat=s))
        for perm in itertools.permutations(range(s)):
            for mask in range(1 << (1 << s)):
                table = tuple(bool(mask >> i & 1) for i in range(1 << s))
                indexed = dict(zip(assignments, table))
                renamed = tuple(indexed[tuple(a[perm[i]] for i in range(s))]
                                for a in assignments)
                assert sum(renamed) == sum(table)
                before = close_verified(authenticate(tuple(range(s)), table, sum(table)))
                after = close_verified(authenticate(tuple(range(s)), renamed, sum(renamed)))
                assert before == after
                transported += 1
    # Five allowed T5 values in a 3-bit code are not Boolean TRUE.
    domain = tuple(i < 5 for i in range(8))
    assert close_verified(authenticate((0, 1, 2), domain, 5)) is None
    # A full projected count does not mean the unprojected relation is full.
    equality = (True, False, False, True)
    assert sum(equality) == 2
    assert close_verified(authenticate(("x", "y"), equality, 2)) is None
    # A forced bit is not a free variable. Dropping it changes the scope.
    forced = (False, False, True, True)
    assert close_verified(authenticate(("x", "y"), forced, 2)) is None
    # Nonnegative weights with zeros do not justify the unweighted zero rule.
    weights = (1, 0)
    relation = (False, True)
    assert sum(w * b for w, b in zip(weights, relation)) == 0 and any(relation)
    # Modular zero is not exact integer zero.
    assert sum((True, True)) % 2 == 0
    return dict(
        lemma="T5-EXTREMAL-COUNT-CLOSURE1",
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        rows=rows, truth_tables=sum(r["tables"] for r in rows),
        renamed_tables=transported, fabricated_counts_rejected=rejected,
        controls=dict(five_value_binary_domain="PASS", projection="PASS",
                      forced_scope="PASS", zero_weight="PASS", modular_count="PASS",
                      smallest_ambiguous_pair={"scope": ["x"], "tables": [[False, True], [True, False]], "count": 1}),
        status="PASS; finite Boolean audit, not a T5 lower-bound test",
        randomness="none", external_dependencies="none")


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
