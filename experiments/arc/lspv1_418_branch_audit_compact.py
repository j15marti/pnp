#!/usr/bin/env python3
"""LSPV-1/418 compact source-only branching-audit to Resolution reproducer.
Run: python3 compact_reproduce418.py. Standard library only.
Full independent source and raw proof archive: audit_cut418.py, raw418.json.
"""
from itertools import product


def source(n, cs):
    assert type(n) is int and n >= 0
    assert all(c == sorted(set(c), key=lambda z: (abs(z), z < 0))
               and all(type(z) is int and 0 < abs(z) <= n for z in c) for c in cs)


def solve(n, cs):
    """Return SAT witness or (strict RES trace, final empty-clause ID, branches)."""
    source(n, cs)
    lines = [set(c) for c in cs]
    steps, memo = [], {}
    branches = 0

    def visit(a):
        nonlocal branches
        if a in memo:
            return memo[a]
        for j, c in enumerate(cs):
            if all(abs(z) <= len(a) and a[abs(z)-1] != int(z > 0) for z in c):
                memo[a] = (j, None)
                return memo[a]
        if len(a) == n:
            memo[a] = (None, a)
            return memo[a]
        v = len(a) + 1
        left = visit(a + (0,))
        if left[1] is not None:
            return left
        right = visit(a + (1,))
        if right[1] is not None:
            return right
        branches += 1
        l, r = lines[left[0]], lines[right[0]]
        if v not in l:
            final = left[0]
        elif -v not in r:
            final = right[0]
        else:
            final = len(lines)
            new = (l - {v}) | (r - {-v})
            assert new <= {-(j+1) if b else j+1 for j, b in enumerate(a)}
            lines.append(new)
            steps.append((left[0], right[0], v, new))
        memo[a] = (final, None)
        return memo[a]

    root, witness = visit(())
    if witness is not None:
        assert all(any(witness[abs(z)-1] == int(z > 0) for z in c) for c in cs)
        return witness, (len(steps), None), branches
    assert not lines[root]
    ledger = [set(c) for c in cs]
    for l, r, p, out in steps:
        assert l < len(ledger) and r < len(ledger)
        assert p in ledger[l] and -p in ledger[r]
        assert (ledger[l] - {p}) | (ledger[r] - {-p}) == out
        ledger.append(out)
    assert not ledger[root]
    return None, (len(steps), root), branches


def php(h):
    var = lambda p, hole: p*h + hole + 1
    cs = [[var(p, j) for j in range(h)] for p in range(h+1)]
    for j in range(h):
        for p in range(h+1):
            for q in range(p+1, h+1):
                cs.append(sorted([-var(p,j), -var(q,j)], key=lambda z:(abs(z), z<0)))
    return h*(h+1), cs


def main():
    opts = [[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]]
    sat_count, unsat_count, steps, branches = 0, 0, 0, 0
    for mask in range(256):
        cs = [opts[i] for i in range(8) if mask >> i & 1]
        witness, trace, b = solve(2, cs)
        actual_sat = any(all(any(bits[abs(z)-1] == int(z > 0) for z in c) for c in cs)
                         for bits in product((0,1), repeat=2))
        assert (witness is not None) == actual_sat
        sat_count += actual_sat
        unsat_count += not actual_sat
        branches += b
        if trace: steps += trace[0]
    assert (sat_count,unsat_count,steps,branches) == (95,161,246,294)
    print(f'two-variable: SAT={sat_count}, UNSAT={unsat_count}, RES={steps}, branches={branches}')
    for h, expected_res, expected_branch in ((1,2,2),(2,12,14),(3,78,98),(4,600,782)):
        n, cs = php(h)
        wit, tr, b = solve(n, cs)
        assert wit is None and tr[0] == expected_res and b == expected_branch
        print(f'PHP_{h}: source={len(cs)}, RES={tr[0]}, branches={b}')
    print('PASS; minimum and asymptotic hardness are NOT inferred from finite counts')


if __name__ == '__main__':
    main()
