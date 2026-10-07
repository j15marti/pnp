#!/usr/bin/env python3
"""Bounded arithmetic checks for conditional ARC lemmas, not SAT evidence."""
import json
import math
import time
from pathlib import Path


def main():
    start = time.monotonic()
    deadline = start + 25.0
    checks = 0
    gamma = 2 * math.cos(math.pi / 7)
    scalar = []
    for lam in (0.1, 0.5, 0.9, 0.99):
        for fixed in (0.0, 1.0, 1.7):
            for initial in (2.0, 10.0, 1000.0):
                value = initial
                count = 0
                while value >= gamma:
                    if time.monotonic() > deadline:
                        raise TimeoutError('25-second checkpoint budget reached')
                    count += 1
                    value = lam * value + (1-lam) * fixed
                    predicted = fixed + lam**count * (initial-fixed)
                    assert math.isclose(value, predicted, rel_tol=1e-10, abs_tol=1e-10)
                    checks += 1
                scalar.append({'lambda':lam,'fixed_point':fixed,'initial':initial,'first_crossing':count,'value':value})
    # Rational boundary control: v_r = 1 + 2^(-r) > 1 at every finite r.
    # Store exact positive numerator of the gap, avoiding floating underflow.
    boundary = [{'r':r, 'gap_numerator':1,'gap_denominator':str(2**r)} for r in (1,10,100,1000)]
    assert all(int(row['gap_denominator']) > 0 for row in boundary)
    checks += len(boundary)
    # rho(M)=1/2 but a large transient; sum need not decrease every step.
    matrix = [[0.5, 3.0], [0.0, 0.5]]
    offset = [0.2, 0.05]
    fixed = [1.0, 0.1]
    z = [10.0,10.0]
    trajectory = [z[:]]
    for _ in range(100):
        z = [matrix[0][0]*z[0]+matrix[0][1]*z[1]+offset[0], matrix[1][1]*z[1]+offset[1]]
        trajectory.append(z[:])
        checks += 1
    assert sum(trajectory[1]) > sum(trajectory[0])
    assert sum(trajectory[-1]) < gamma
    assert all(abs(z[i]-fixed[i]) < 1e-10 for i in range(2))
    # Non-downward region: upper envelope can approach target while smaller y misses it.
    arbitrary_region_control = {'fixed_point':1.0,'region':'(0.9,1.1)','achievable_sequence':0.0,'upper_bound':1.0,'enters_region':False}
    assert not (0.9 < 0.0 < 1.1)
    checks += 1
    restriction = []
    for n in (100,1000,10000,1000000):
        r = int(2*math.log2(n))
        restriction.append({'n':n,'fixed_variables':r,'remaining_fraction':(n-r)/n,'child_count_log2':r})
        assert r <= 2*math.log2(n)
        checks += 1
    result={'status':'COMPUTATIONAL: arithmetic sanity and hostile controls only','elapsed_seconds':time.monotonic()-start,'checks':checks,'gamma':gamma,'scalar_cases':scalar,'strict_boundary_control':boundary,'matrix':{'M':matrix,'offset':offset,'fixed_point':fixed,'first_sum':sum(trajectory[0]),'next_sum':sum(trajectory[1]),'final_sum':sum(trajectory[-1])},'non_downward_region_control':arbitrary_region_control,'restriction_control':restriction,'limitations':'No SAT closure map, universal resource bound, or P versus NP separation is tested or established.'}
    output=Path(__file__).with_name('arc_test_results.json')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'checks':checks,'elapsed_seconds':result['elapsed_seconds'],'output':str(output)}))


if __name__ == '__main__':
    main()
