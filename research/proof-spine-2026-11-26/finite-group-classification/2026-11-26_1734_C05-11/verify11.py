"""Independent stdlib certificate checks for C05-11, no inherited solver imports."""
from fractions import Fraction
from itertools import product, combinations
from random import Random

def par(x): return x.bit_count() & 1
def active(F,x): return all(par(v&x)==c for v,c in F)
def span(rows):
    s={0}
    for v in rows: s |= {v^w for w in s}
    return s
def restrict(x,S): return tuple(par(x&v) for v in sorted(S))
G=[[(1,1),(2,1)],[(1,1),(4,1)],[(2,1),(5,1)],[(3,0),(8,0)],[(3,1),(4,1)],[(3,1),(13,1)],[(5,0),(14,0)],[(5,1),(13,1)]]
E=[(7,5),(7,3),(7,2),(6,5),(6,1),(5,4),(3,0)]
p=[sum(active(F,x) for F in G)-sum(active(G[i],x) and active(G[j],x) for i,j in E) for x in range(16)]
alpha=max(len(S) for k in range(9) for S in combinations(range(8),k) if all(not(i in S and j in S) for i,j in E))
a=Fraction(sum(p),16);b=Fraction(sum(v*v for v in p),16)
assert alpha==4 and a==Fraction(9,8) and b==Fraction(15,8) and b-5*a+4==Fraction(1,4)
# Two distinct sets of 3 affine lines, identical two moments, opposite zero existence.
S=[[(1,1)],[(2,1)],[(3,1)]];U=[[(1,1)],[(2,1)],[(3,0)]]
s=[sum(active(F,x) for F in S) for x in range(4)];u=[sum(active(F,x) for F in U) for x in range(4)]
assert sorted(s)==[0,2,2,2] and sorted(u)==[1,1,1,3]
assert sum(s)==sum(u)==6 and sum(v*v for v in s)==sum(v*v for v in u)==12
# Exhaustive path support (not just decision), including higher-order dependencies.
r=Random(26112611);checks=0
for trial in range(300):
    d=r.randint(1,6);k=r.randint(1,5)
    blocks=[[[(r.randrange(1,1<<d),r.randrange(2)) for _ in range(r.randint(1,3))] for _ in range(r.randint(1,3))] for _ in range(k)]
    rows=[[v for F in H for v,c in F] for H in blocks]
    C=[span(v for J in rows[:j] for v in J)&span(v for J in rows[j:] for v in J) for j in range(k+1)]
    # Every transition records both full boundary restrictions simultaneously.
    table=[{(restrict(x,C[j]),restrict(x,C[j+1])) for x in range(1<<d) if not any(active(F,x) for F in H)} for j,H in enumerate(blocks)]
    paths={(restrict(0,C[0]),)}
    for T in table:paths={P+(bb,) for P in paths for aa,bb in T if aa==P[-1]}
    ref={tuple(restrict(x,W) for W in C) for x in range(1<<d) if not any(active(F,x) for H in blocks for F in H)}
    assert paths==ref;checks+=1
print({'cube_scores':p,'alpha':alpha,'mean':str(a),'second':str(b),'same_moment_SAT':s,'same_moment_UNSAT':u,'exact_path_support_checks':checks})
# Fixed-order moment obstruction: parity-conditioned Hamming weights.
for h in range(2,9):
    a=[x.bit_count()+par(x) for x in range(1<<h)]
    b=[x.bit_count()+1-par(x) for x in range(1<<h)]
    assert 0 in a and 0 not in b
    assert all(sum(v**j for v in a)==sum(v**j for v in b) for j in range(1,h+1))
print('parity moment obstruction verified for orders 2 through 8')
