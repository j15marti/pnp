"""BOUNDARY-TW81 compact executable: cyclic 2-state interfaces, both labels."""
from itertools import product


def matches(q, eta):
    # Independent full source-state enumeration of cycle equations.
    return any(all((x[i] ^ x[(i+1) % q]) == eta[i] for i in range(q))
               for x in product((0, 1), repeat=q))


def eliminate_cycle(q, eta):
    # Exact Boolean-table variable elimination, with fully charged table rows.
    domains = (0, 1)
    factors = []
    for i in range(q):
        j = (i + 1) % q
        scope = tuple(sorted((i, j)))
        tab = {}
        for row in product(domains, repeat=2):
            d = dict(zip(scope, row))
            tab[row] = (d[i] ^ d[j]) == eta[i]
        factors.append((scope, tab))
    factors.append(((0,), {(0,): False, (1,): True}))
    table_rows = 0
    for i in range(q):
        selected = [(s, t) for s, t in factors if i in s]
        factors = [(s, t) for s, t in factors if i not in s]
        scope = sorted(set().union(*(set(s) for s, _ in selected)))
        rest = tuple(x for x in scope if x != i)
        reduced = {}
        for row in product(domains, repeat=len(scope)):
            table_rows += 1
            d = dict(zip(scope, row))
            if all(t[tuple(d[x] for x in s)] for s, t in selected):
                reduced[tuple(d[x] for x in rest)] = True
        factors.append((rest, {row: row in reduced
                              for row in product(domains, repeat=len(rest))}))
    decision = all(t[()] for s, t in factors)
    return decision, table_rows


def main():
    tests = 0
    for q in range(3, 10):
        for eta in product((0, 1), repeat=q):
            got, rows = eliminate_cycle(q, eta)
            assert got == matches(q, eta) == (sum(eta) % 2 == 0)
            assert rows <= 8 * q
            tests += 1
    print({"paired_cycles_checked": tests, "unexpected_discrepancies": 0})


if __name__ == '__main__':
    main()
