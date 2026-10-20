"""Finite controls for MINIMAL-UNSAT-PROJECTION20.

The family is proved symbolically in the accompanying report.  Exhaustive SAT
checks here test small members, their every one-clause deletion, and a matched
same-size SAT partner.  They do not prove an unrestricted SAT lower bound.
"""
from itertools import product


def unit(lit, a, b):
    return tuple((lit, sa * a, sb * b)
                 for sa, sb in product((-1, 1), repeat=2))


def implication(left, right, pad):
    return ((-left, right, pad), (-left, right, -pad))


def pair(m):
    assert m >= 2
    a0, b0, am, bm = m + 1, m + 2, m + 3, m + 4
    clauses = list(unit(1, a0, b0))
    for i in range(1, m):
        clauses.extend(implication(i, i + 1, m + 4 + i))
    end = list(unit(-m, am, bm))
    clauses.extend(end)
    unsat = tuple(clauses)
    removed = (-m, am, bm)
    replacement = (-m, am, 1)
    satmate = tuple(replacement if c == removed else c for c in unsat)
    return unsat, satmate, 2 * m + 3


def satisfies(cnf, assignment):
    return all(any(((assignment >> (abs(lit) - 1)) & 1) == (lit > 0)
                   for lit in clause) for clause in cnf)


def find_witness(cnf, variables):
    for assignment in range(1 << variables):
        if satisfies(cnf, assignment):
            return assignment
    return None


proper_checks = 0
pair_checks = 0
minimality_checks = 0
transcript_checks = 0
large_shape_checks = 0

for m in range(2, 8):
    no, yes, variables = pair(m)
    assert len(no) == len(yes) == 2 * m + 6
    assert variables == 2 * m + 3
    assert find_witness(no, variables) is None
    assert find_witness(yes, variables) is not None
    pair_checks += 4

    for cnf in (no, yes):
        for clause in cnf:
            assert len(clause) == 3
            assert len({abs(x) for x in clause}) == 3
            assert all(-variables <= x <= variables and x != 0 for x in clause)
            proper_checks += 3

    # Every strict subset of a minimally UNSAT formula is SAT once every
    # one-clause deletion is SAT.  The SAT mate is monotone under deletion.
    no_transcript = []
    yes_transcript = []
    for i in range(len(no)):
        no_child = no[:i] + no[i + 1:]
        yes_child = yes[:i] + yes[i + 1:]
        no_ans = find_witness(no_child, variables) is not None
        yes_ans = find_witness(yes_child, variables) is not None
        assert no_ans and yes_ans
        no_transcript.append(no_ans)
        yes_transcript.append(yes_ans)
        minimality_checks += 2
    assert no_transcript == yes_transcript == [True] * len(no)
    transcript_checks += len(no) + 1

# Shape/properness controls at scales where exhaustive truth tables are not run.
for m in range(8, 1001):
    no, yes, variables = pair(m)
    assert len(no) == len(yes) == 2 * m + 6
    assert variables == 2 * m + 3
    assert no != yes
    large_shape_checks += 4

total = (proper_checks + pair_checks + minimality_checks +
         transcript_checks + large_shape_checks)
print({
    "proper_checks": proper_checks,
    "pair_checks": pair_checks,
    "minimality_checks": minimality_checks,
    "transcript_checks": transcript_checks,
    "large_shape_checks": large_shape_checks,
    "assertions_total": total,
    "failures": 0,
})
