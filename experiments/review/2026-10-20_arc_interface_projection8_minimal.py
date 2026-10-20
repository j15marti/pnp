"""Standalone exact semantic-join checker for scoped-CNF. No packages required.
This miniature checks one proof lemma, not the full resource experiment.
"""
from itertools import product

def sat(clauses, pins=None):
    pins = {} if pins is None else pins
    names = sorted({abs(x) for c in clauses for x in c} | set(pins))
    for bits in product((False, True), repeat=len(names)):
        a = dict(zip(names, bits))
        if all(a[v] == val for v, val in pins.items()) and all(
            any(a[abs(l)] == (l > 0) for l in c) for c in clauses
        ):
            return True
    return False

def events(clauses):
    # Tiny verification only: O(n) preprocessing, not full ARC.
    vars_ = sorted({abs(x) for c in clauses for x in c})
    E = [('O', v) for v in vars_]
    E += [('C', c) for c in clauses]
    E += [('X', v) for v in vars_]
    return E

def solve_join(E, chunk):
    active = set()
    reachable = {()}
    for lo in range(0, len(E), chunk):
        incoming = tuple(sorted(active))
        cs = []
        for typ, x in E[lo:lo+chunk]:
            if typ == 'O':
                assert x not in active
                active.add(x)
            elif typ == 'X':
                assert x in active
                active.remove(x)
            else:
                assert all(abs(l) in active for l in x)
                cs.append(x)
        outgoing = tuple(sorted(active))
        nxt = set()
        for abits in reachable:
            aa = dict(zip(incoming, abits))
            fresh = [v for v in outgoing if v not in aa]
            for bb in product((False, True), repeat=len(fresh)):
                pins = dict(aa)
                pins.update(dict(zip(fresh, bb)))
                if sat(cs, pins):
                    nxt.add(tuple(pins[v] for v in outgoing))
        reachable = nxt
    assert not active
    return () in reachable

def main():
    allc = [tuple((v if bit else -v) for v, bit in zip((1, 2, 3), signs))
            for signs in product((False, True), repeat=3)]
    checks = 0
    for mask in range(256):
        f = [allc[k] for k in range(8) if mask & (1 << k)]
        expected = sat(f)
        if mask == 255:
            assert not expected
        for chunk in range(1, 9):
            assert solve_join(events(f), chunk) == expected
            checks += 1
    print({'semantic_join_tests': checks, 'failures': 0,
           'scope': 'finite correctness only, not full ARC contraction'})

if __name__ == '__main__':
    main()
