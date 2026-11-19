#!/usr/bin/env python3
"""TMR-5/075 fixed T5 polymorphism independent exhaustive small-domain audit.
Exact symbolic theorem is in the companion report; these checks are finite.
No external libraries and no randomness. Run: python3 tmr5_t5_polymorphism075.py
"""
import hashlib
import itertools
import json
import math
from pathlib import Path

P = 5
R = {(a, (a+d) % P) for a in range(P) for d in (1,3)}
NAME = ('A','B','C','D','E')
DECLARED = {
    'A':('B','D'), 'B':('C','E'), 'C':('A','D'),
    'D':('B','E'), 'E':('A','C')
}
checks = 0
def check(expr, description):
    global checks
    checks += 1
    if not expr:
        raise AssertionError(description)

def preserves_unary(p):
    return all((p[a],p[b]) in R for a,b in R)

def preserves_binary(f):
    return all((f(a,b),f(c,d)) in R for (a,c) in R for (b,d) in R)

def affine_preserves(coeff):
    return all((sum(coeff[i]*d[i] for i in range(len(coeff))) % P in (1,3))
               for d in itertools.product((1,3), repeat=len(coeff)))

# Authenticate exact user's named fixed template; graph has 10 directed arcs.
for a, name in enumerate(NAME):
    check(tuple(NAME[b] for b in range(P) if (a,b) in R) == DECLARED[name],
          'named relation mismatch at '+name)
for a in range(P):
    check((a,a) not in R, 'a loop')
    for b in range(a+1,P):
        check(((a,b) in R) != ((b,a) in R), 'not a tournament')

cycles = []
for i,j,k in itertools.combinations(range(P),3):
    if (i,j) in R and (j,k) in R and (k,i) in R:
        cycles.append((i,j,k))
    elif (i,k) in R and (k,j) in R and (j,i) in R:
        cycles.append((i,k,j))
check(len(cycles) >= 2, 'no two directed cycles')

# All 5! unary permutations and 5^5 unary maps (non-injective maps cannot preserve loopless tournament).
auto = [p for p in itertools.permutations(range(P)) if preserves_unary(p)]
check(len(auto)==5, 'unary automorphism count')
check(set(auto) == {tuple((a+t)%P for a in range(P)) for t in range(P)},
      'nonrotational automorphism')
unary_map_count = 0
for p in itertools.product(range(P),repeat=P):
    if preserves_unary(p):
        unary_map_count += 1
        check(p in auto, 'unexpected endomorphism')
check(unary_map_count == 5, 'endomorphism mismatch')

# Every D_delta={(a,a+delta)} is an induced T5 in T5^2.
product_arcs = [((a,b),(c,d)) for a,c in R for b,d in R]
check(len(product_arcs)==100,'direct product arc count')
for delta in range(P):
    for a,c in itertools.product(range(P),repeat=2):
        check((((a,(a+delta)%P),(c,(c+delta)%P)) in product_arcs) == ((a,c) in R),
              'shifted diagonal subgraph not T5')

# Every normalized binary polymorphism f(a,b)=a+c[b-a], with c[0]=0.
# Enumerate all 625 candidate c profiles, independently testing all 100 product arcs.
profiles = []
for vals in itertools.product(range(P),repeat=4):
    c = (0,) + vals
    f = lambda a,b: (a + c[(b-a)%P]) % P
    good = preserves_binary(f)
    increments = tuple((c[(d+2)%P]-c[d])%P for d in range(P))
    increment_rule = all(x in (0,2) for x in increments)
    check(good==increment_rule,'profile vs 5-cycle increment rule')
    if good:
        profiles.append(c)
check(profiles == [(0,0,0,0,0),(0,1,2,3,4)], 'normalized binary classification')

all_binary = []
for off in range(P):
    for c in profiles:
        f = lambda a,b,off=off,c=c: (a + off + c[(b-a)%P]) % P
        check(preserves_binary(f), 'rotated projection fails')
        all_binary.append(tuple(f(a,b) for a in range(P) for b in range(P)))
check(len(set(all_binary)) == 10,'binary clone count')

# All affine Z5 polymorphisms on any arity are shifted coordinate projections:
# For k=1..6 exhaustive coefficient tests, with all 2^k true coordinatewise arcs.
affine_counts = {}
affine_tested = 0
increment_patterns = 0
for k in range(1,7):
    passing=[]
    for coeff in itertools.product(range(P),repeat=k):
        yes = affine_preserves(coeff)
        affine_tested += 1
        increment_patterns += 2**k
        target = (sum(x != 0 for x in coeff)==1 and sum(coeff)%P==1)
        check(yes == target,'affine classification k='+str(k)+' coefficients='+str(coeff))
        if yes:
            passing.append(coeff)
    check(len(passing)==k,'affine count k='+str(k))
    affine_counts[str(k)] = {'tested_coefficients':5**k,'passing_coefficients':k}

# Witnesses of invalid candidate algebraic shortcuts.
check(((1+1)%P) not in (1,3),'sum of two coordinates wrongly accepted')
check(((1+3)*3%P) not in (1,3),'mean of two coordinates wrongly accepted')

src = Path(__file__).read_bytes()
result = {
    'id':'TMR5_T5_POLYMORPHISM075',
    'model':'Sigma=Z5, R(a,b) iff (b-a)%5 in (1,3)',
    'script_sha256':hashlib.sha256(src).hexdigest(),
    'deterministic':True,'seed':None,
    'template':{'arcs':len(R),'directed_triangles':cycles,
                'automorphism_count':len(auto),'endomorphism_count':unary_map_count},
    'binary':{'normalized_profiles_tested':5**4,'normalized_survivors':profiles,
              'all_binary_polymorphisms':len(all_binary),
              'product_arcs_per_candidate':len(product_arcs)},
    'affine':{'tested_arities':[1,2,3,4,5,6], 'per_arity':affine_counts,
              'coefficient_vectors_tested':affine_tested,
              'increment_pattern_checks':increment_patterns},
    'assertions':checks,'failures':0,
    'scope':'finite exhaustive audit only; all-arity affine and all-binary theorems separately proved symbolically',
    'no_claims':['no general arity clone classification','no arbitrary SAT machine lower bound','P versus NP remains OPEN']
}
print(json.dumps(result,indent=2,sort_keys=True))
