"""Independent compact finite checks for TMR-5/086. Python 3.10+, stdlib only.
These checks corroborate, but do not replace, the symbolic bounded-width proof.
"""
from itertools import product
import json

R = lambda a,b: (b-a)%5 in (1,3)
C5 = lambda a,b: (b-a)%5 in (1,4)

# One edge in the seventh direct power links a tuple to its cyclic shift.
x = (0,3,1,4,2,3,4)
y = x[1:] + x[:1]
assert all(R(a,b) for a,b in zip(x,y))
assert tuple((b-a)%5 for a,b in zip(x,y)) == (3,3,3,3,1,1,1)

# A distinct direct verification at more prime arities.
primes = [7,11,13,17,19,23,29]
for p in primes:
    j = (2*p)%5
    steps = [3]*j + [1]*(p-j)
    seq = [0]
    for d in steps[:-1]:seq.append((seq[-1]+d)%5)
    assert all(R(a,b) for a,b in zip(seq,seq[1:]+seq[:1]))

gadget_assignments = 0
lifted = 0
for u,v in product(range(5),repeat=2):
    good=[]
    for a,b,c in product(range(5),repeat=3):
        gadget_assignments += 1
        if all(R(i,j) for i,j in [(u,a),(a,b),(b,c),(u,c),(c,v)]):
            good.append((a,b,c))
    expected = [((u+1)%5,(u+2)%5,(u+3)%5)] if C5(u,v) else []
    assert good == expected
    lifted += len(good)

# Completeness of fixed 32-Horn-rule propagation compilation.
horn_patterns = 0
for left,right in product(range(32),repeat=2):
    no_support = not any((left>>z)&(right>>z)&1 for z in range(5))
    horn_rule = any(all((not ((left if (choice>>z)&1 == 0 else right)>>z&1))
                        for z in range(5)) for choice in range(32))
    assert no_support == horn_rule,(left,right)
    horn_patterns += 1

assert (gadget_assignments,lifted,horn_patterns)==(3125,10,1024)
print(json.dumps({'gadget_assignments':gadget_assignments,'valid_gadget_lifts':lifted,
                  'Horn_truth_patterns':horn_patterns,'prime_witnesses':primes,
                  'seven_tuple':x,'all_checks_passed':True},sort_keys=True))
