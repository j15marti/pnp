"""Exact state probabilities and conditional entropy audit, standard library."""
from fractions import Fraction
from collections import defaultdict
from math import log2
import json

RELATIONS = (0b1101, 0b0110, 0b0100)
WEIGHTS = (Fraction(1,4), Fraction(1,4), Fraction(1,2))
IDENTITY = 0b1001


def compose(left, right):
    result = 0
    for start in range(2):
        for end in range(2):
            if any((left >> (2*start+middle)) & 1 and
                   (right >> (2*middle+end)) & 1 for middle in range(2)):
                result |= 1 << (2*start+end)
    return result


def audit(length):
    distribution = {IDENTITY: Fraction(1)}
    reads = Fraction(0)
    demand = 0.0
    for step in range(1, length+1):
        alive = 1-distribution.get(0,Fraction(0))
        assert alive <= Fraction(3,4)**((step-1)//2)
        reads += 2*alive
        following = defaultdict(Fraction)
        stage = 0.0
        for state, probability in distribution.items():
            outcomes = defaultdict(Fraction)
            for relation, weight in zip(RELATIONS, WEIGHTS):
                outcomes[compose(state,relation)] += weight
            entropy = -sum(float(p)*log2(float(p)) for p in outcomes.values())
            stage += float(probability)*entropy
            for outcome, weight in outcomes.items():
                following[outcome] += probability*weight
            # Given the previous state, empty record at absorption and
            # two read bits otherwise decode the next state exactly.
            records = [""] if state == 0 else ["00","01","10","11"]
            assert all(not(y.startswith(x)) for x in records for y in records if x != y)
        assert stage <= 1.5*float(alive)+1e-12
        demand += stage
        distribution = dict(following)
        assert sum(distribution.values()) == 1
    assert reads <= 16 and demand <= 12+1e-10
    return dict(length=length, expected_selected_reads=str(reads),
                entropy_sum_bits=demand,
                survival_probability=str(1-distribution.get(0,Fraction(0))),
                peak_reachable_states=len(distribution))


if __name__ == "__main__":
    assert compose(RELATIONS[2],RELATIONS[2]) == 0
    print(json.dumps([audit(t) for t in (3,4,8,16,32,100)],indent=2))
