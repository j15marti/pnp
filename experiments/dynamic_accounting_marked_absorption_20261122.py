"""Exact marked-syndrome event ledger. Python 3 standard library."""
from collections import defaultdict
from fractions import Fraction
from math import log2
import json

RELATIONS = (0b1101, 0b0110, 0b0100)
WEIGHTS = (Fraction(1,4), Fraction(1,4), Fraction(1,2))


def project(state):
    return sum(1 << (2*s+x) for s in range(2) for x in range(2)
               if any(state & (1 << (4*s+2*x+p)) for p in range(2)))


def update(state, relation, marked):
    result = 0
    for start in range(2):
        for x in range(2):
            for parity in range(2):
                if state & (1 << (4*start+2*x+parity)):
                    for y in range(2):
                        if relation & (1 << (2*x+y)):
                            result |= 1 << (4*start+2*y+(parity ^ (x if marked else 0)))
    return result


def compose(left, right):
    return sum(1 << (2*s+y) for s in range(2) for y in range(2)
               if any(left & (1 << (2*s+x)) and right & (1 << (2*x+y))
                      for x in range(2)))


def audit(t, marks):
    distribution = {65: Fraction(1)}
    reads = Fraction(0)
    demand = 0.0
    peak = 1
    for j in range(t):
        alive = 1-distribution.get(0,Fraction(0))
        assert alive <= Fraction(3,4)**(j//2)
        reads += 2*alive
        following = defaultdict(Fraction)
        stage = 0.0
        for state, mass in distribution.items():
            outcomes = defaultdict(Fraction)
            for relation, weight in zip(RELATIONS,WEIGHTS):
                outcomes[update(state,relation,j in marks)] += weight
            entropy = -sum(float(p)*log2(float(p)) for p in outcomes.values())
            stage += float(mass)*entropy
            for result, probability in outcomes.items():
                following[result] += mass*probability
            records = [""] if state==0 else ["00","01","10","11"]
            assert all(not b.startswith(a) for a in records for b in records if a != b)
        assert stage <= 1.5*float(alive)+1e-12
        demand += stage
        distribution = dict(following)
        peak = max(peak,len(distribution))
        assert sum(distribution.values()) == 1
    assert reads <= 16 and demand <= 12+1e-10
    sat = sum(mass for state,mass in distribution.items() if state & 65)
    return dict(t=t, marks=list(marks), expected_selected_reads=str(reads),
                entropy_sum_bits=demand, survival=str(1-distribution.get(0,Fraction(0))),
                sat_probability=str(sat), peak_distribution_support=peak)


if __name__ == "__main__":
    count = 0
    for state in range(256):
        for marked in (False,True):
            for relation in RELATIONS:
                assert project(update(state,relation,marked)) == compose(project(state),relation)
                count += 1
    rows=[]
    for t in (3,4,8,16,100):
        schedules = sorted({(0,1,2),(0,t//2,t-1),(t-3,t-2,t-1)})
        results = [audit(t,m) for m in schedules]
        assert len({x["expected_selected_reads"] for x in results})==1
        rows.extend(results)
    print(json.dumps(dict(projection_identity_cases=count, results=rows),indent=2))
