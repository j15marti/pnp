"""ARC224 supplementary independent exhaustive GF(2)-core tester.

Does NOT implement the full source parser or proof checker. The full verifier
is in ARC224_cyclic_affine_core.py in the reproducibility ZIP.
"""
import itertools
import json
import random


def rank(vectors):
    pivots = {}
    for value in vectors:
        x = value
        while x:
            p = x.bit_length() - 1
            if p in pivots:
                x ^= pivots[p]
            else:
                pivots[p] = x
                break
    return len(pivots)


def basis_of(vectors):
    result = []
    for value in vectors:
        if rank(result + [value]) > len(result):
            result.append(value)
    return result


def coordinates(value, basis):
    # Exhaustive small-case evaluator, not used by the claimed poly-time solver.
    for mask in range(1 << len(basis)):
        y = 0
        for i, vector in enumerate(basis):
            if mask & (1 << i):
                y ^= vector
        if y == value:
            return mask
    raise AssertionError('form outside span')


def check_instance(r, observed, clauses):
    forms = sorted(set(observed) - {0})
    rho = rank(forms)
    coloops = [v for v in forms if rank([w for w in forms if w != v]) < rho]
    h = rho - len(coloops)
    b = basis_of(forms)
    assert len(b) == rho and set(coloops).issubset(b)
    core_indices = [i for i, v in enumerate(b) if v not in coloops]
    coloop_indices = [i for i, v in enumerate(b) if v in coloops]
    assert len(core_indices) == h
    decomposed = {v: coordinates(v, b) for v in forms}
    for v in forms:
        if v not in coloops:
            assert all(not (decomposed[v] & (1 << j)) for j in coloop_indices)
    def truth(form, polarity, t):
        return ((form & t).bit_count() & 1) ^ polarity
    def satisfies(t):
        return all(any(truth(v, sign, t) for v, sign in clause)
                   for clause in clauses)
    expected = any(satisfies(t) for t in range(1 << r))
    actual = False
    for u in itertools.product((0, 1), repeat=h):
        for w in itertools.product((0, 1), repeat=len(coloop_indices)):
            coordinates_value = [0] * len(b)
            for i, bit in zip(core_indices, u):
                coordinates_value[i] = bit
            for i, bit in zip(coloop_indices, w):
                coordinates_value[i] = bit
            def evaluate(v, sign):
                mask = decomposed.get(v, 0)
                return (sum(coordinates_value[i] for i in range(len(b))
                            if mask & (1 << i)) & 1) ^ sign
            if all(any(evaluate(v, sign) for v, sign in clause)
                   for clause in clauses):
                actual = True
                break
        if actual:
            break
    assert actual == expected
    return rho, len(coloops), h


def main():
    rng = random.Random(224)
    trials = 500
    max_h = 0
    for _ in range(trials):
        r = rng.randrange(1, 7)
        observed = rng.sample(range(1, 1 << r), rng.randrange(1, min(9, 1 << r)))
        clauses = [tuple((rng.choice(observed), rng.randrange(2))
                         for _ in range(rng.randint(1, 2)))
                   for _ in range(rng.randrange(0, 12))]
        rho, c, h = check_instance(r, observed, clauses)
        assert 0 <= h <= rho <= r and c + h == rho
        max_h = max(max_h, h)
    full = list(range(1, 8))
    rho, c, h = check_instance(3, full,
                             [((1, 0),), ((2, 0),), ((3, 1),)])
    assert (rho, c, h) == (3, 0, 3)
    print(json.dumps({'seed': 224, 'random_cases': trials,
                      'max_cyclic_rank': max_h,
                      'all_nonzero_F2_3': {'rank': rho, 'coloops': c, 'h': h},
                      'all_assertions_passed': True}, sort_keys=True))


if __name__ == '__main__':
    main()
