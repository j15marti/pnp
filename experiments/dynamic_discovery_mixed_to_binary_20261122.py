"""Semantic checker, Python 3. Run from the repository root."""
from collections import Counter
from itertools import combinations, product
import json
import random

from dynamic_construction_synchronized_cycles_20261122 import generate, transfer


def binary_sat(clauses, variables):
    literals = [signed for v in variables for signed in (v + 1, -v - 1)]
    reach = {lit: {lit} for lit in literals}
    for a, b in clauses:
        reach[-a].add(b)
        reach[-b].add(a)
    for pivot in literals:
        for lit in literals:
            if pivot in reach[lit]:
                reach[lit].update(reach[pivot])
    return all(-lit not in reach[lit] or lit not in reach[-lit] for lit in literals)


def reduce_source(factors, checks):
    """Inputs are authenticated, disjoint exact-one factors and even XOR rows."""
    factors = [set(row) for row in factors]
    checks = [set(row) for row in checks]
    ports = set().union(*factors)
    uses = Counter(x for row in checks for x in row)
    binary = []
    removed = set()
    for i, j in combinations(range(len(checks)), 2):
        if i in removed or j in removed:
            continue
        shared = checks[i] & checks[j]
        if len(shared) != 2 or shared & ports or any(uses[x] != 2 for x in shared):
            continue
        x, = checks[i] - shared
        y, = checks[j] - shared
        binary.extend([(-(x+1), y+1), (x+1, -(y+1))])
        removed.update([i, j])
    for i, row in enumerate(checks):
        if i in removed:
            continue
        factor = next((f for f in factors if len(f & row) >= 2), None)
        if factor is None:
            return "UNKNOWN"
        if factor == row:
            return "UNSAT"
        w, = factor - row
        x, = row - factor
        binary.extend([(w+1, x+1), (-(w+1), -(x+1))])
    touched = {abs(lit)-1 for clause in binary for lit in clause}
    for f in factors:
        private = f - touched
        if not private:
            return "UNKNOWN"
        a, z = f - {min(private)}
        binary.append((-(a+1), -(z+1)))
    variables = sorted({abs(lit)-1 for clause in binary for lit in clause})
    return "SAT" if binary_sat(binary, variables) else "UNSAT"


def brute(factors, checks, n):
    for bits in product(range(2), repeat=n):
        if all(sum(bits[x] for x in f) == 1 for f in factors) and all(
                sum(bits[x] for x in row) % 2 == 0 for row in checks):
            return "SAT"
    return "UNSAT"


def main():
    small = Counter()
    factors = [(0, 1, 2), (3, 4, 5)]
    pool = [(2, 6, 7), (5, 6, 7), (0, 1, 3), (3, 4, 0),
            (0, 3, 6), (0, 1, 2), (4, 6, 7)]
    for mask in range(1 << len(pool)):
        checks = [row for i, row in enumerate(pool) if mask >> i & 1]
        label = brute(factors, checks, 8)
        answer = reduce_source(factors, checks)
        assert answer in ("UNKNOWN", label)
        small[f"{answer} / oracle {label}"] += 1
    rng = random.Random(324)
    ladders = {}
    for t in (3, 4):
        counts = Counter()
        for top, bottom in product(product("AC", repeat=t), repeat=2):
            f, q, _ = generate("".join(top), "".join(bottom))
            ids = list(range(8*t))
            rng.shuffle(ids)

            def scramble(rows):
                mixed = [rng.sample([ids[x] for x in row], 3) for row in rows]
                rng.shuffle(mixed)
                return mixed

            answer = reduce_source(scramble(f), scramble(q))
            assert answer == ("SAT" if transfer(top, bottom) else "UNSAT")
            counts[answer] += 1
        ladders[t] = dict(counts)
    print(json.dumps({"seed": 324, "small": dict(small), "renamed_ladders": ladders},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
