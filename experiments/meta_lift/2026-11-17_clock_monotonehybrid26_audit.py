#!/usr/bin/env python3
"""Exhaustive/seeded adversarial audit for CLOCKMONOCHAIN26.
All operations evaluate original source bits; no oracle or hidden input.
The theorem itself is symbolic and does not depend on this program.
"""
import itertools, json, random, hashlib, sys, time
from collections import Counter
SEED = 202611171927
R = random.Random(SEED)
checks = 0
stats = Counter()
examples = []

def check(pred, label):
    global checks
    checks += 1
    if not pred:
        raise AssertionError(f'{label}; assertion {checks}')

def monotone_table(N):
    """For N<=4 source coordinates, all monotone Boolean funcs on N-bit sources."""
    parents = [sum(1 << (v ^ (1 << j)) for j in range(N) if v & (1 << j)) for v in range(1 << N)]
    for bits in range(1 << (1 << N)):
        if all(not ((bits >> v)&1) or (parents[v]&~bits)==0 for v in range(1 << N)):
            yield bits

def monoval(T, x, sign):
    return ((T >> x) & 1) ^ sign

def pv(poly, x):
    # polynomial represented as a list of masks (ANF monomials)
    return sum((x & mon) == mon for mon in poly) % 2

def degree(poly):
    return max((z.bit_count() for z in poly),default=0)

def prefix(N,t):
    return (1 << t)-1

def plateau(N, monos):
    labels=[tuple(monoval(T, prefix(N,t), sign) for T,sign in monos) for t in range(N+1)]
    a=b=best_a=best_b=0
    for t in range(1,N+1):
        if labels[t]!=labels[t-1]:
            if b-a>best_b-best_a: best_a,best_b=a,b
            a=t
        b=t
    if b-a>best_b-best_a: best_a,best_b=a,b
    return best_a,best_b,labels

def verify(N, monos, polys, tag):
    global stats
    a,b,labels=plateau(N,monos)
    L=b-a; K=len(monos)
    check(L>= (N-K)//(K+1),tag+' plateau bound')
    for j in range(K):
        changes=sum(labels[t][j]!=labels[t-1][j] for t in range(1,N+1))
        check(changes<=1,tag+' coordinate monotonicity')
    val=tuple(pv(p,prefix(N,a)) for p in polys)
    pin=prefix(N,a)
    found=0
    for mid in range(1<<L):
        x=pin | (mid<<a)
        check(tuple(monoval(T,x,sgn) for T,sgn in monos)==labels[a],tag+' subcube monotone constancy')
        if tuple(pv(p,x) for p in polys)==val: found+=1
    D=sum(degree(p) for p in polys)
    lower=1<<max(0,L-D)
    check(found>=lower,tag+f' RM mass found={found} lower={lower}')
    stats['systems']+=1;stats['cube_points']+=1<<L;stats['fiber_points']+=found
    stats['min_slack']=min(stats.get('min_slack',99999),found-lower)
    stats['max_L']=max(stats.get('max_L',0),L)
    if found==lower:stats['tight']+=1
    if len(examples)<8 and (L>=3 or found==lower):
        examples.append({'tag':tag,'N':N,'k':K,'r':len(polys),'a':a,'b':b,'L':L,'D':D,'fiber_in_cube':found,'RM_lower':lower})

# Exhaustive all 168 monotone Boolean functions on four raw source coordinates,
# all ordered pairs and both signs, with adversarial linear polynomial outputs.
N=4
mono=list(monotone_table(N))
check(len(mono)==168,'Dedekind number M(4)')
P=[[],[0],[1],[2],[4],[8],[1,2,4,8],[3,12],[0,15]]
# Check all pairs, using a suite of degrees 0,1,2 and 4.
for i,A in enumerate(mono):
    for j,B in enumerate(mono):
        if (i+j)%2:
            monos=((A,1),(B,0))
        else:
            monos=((A,0),(B,1))
        # Two different output-polynomial regimes per input pair
        verify(N,monos,(P[(i+2*j)%len(P)],),f'exhaustive4[{i},{j}]')
        verify(N,monos,(P[(3*i+j+4)%len(P)],P[(i+j+2)%len(P)]),f'exhaustive4-double[{i},{j}]')
stats['exhaustive_monotone_functions_4']=len(mono)
stats['exhaustive_ordered_pairs_4']=len(mono)**2

# Generate N=8 unate source maps from random monotone DNFs.
def random_mono(N):
    terms=[R.randrange(1<<N) for _ in range(R.randint(0,10))]
    table=0
    for x in range(1<<N):
        if any((x&t)==t for t in terms):table |= 1<<x
    return table

def random_poly(N, maxdeg):
    return [x for x in range(1<<N) if x.bit_count()<=maxdeg and R.random()<0.012]

for trial in range(1200):
    k=R.randint(1,4); rr=R.randint(0,3)
    monos=tuple((random_mono(8),R.randrange(2)) for _ in range(k))
    polys=tuple(random_poly(8,R.randint(0,3)) for _ in range(rr))
    verify(8,monos,polys,'sample8-'+str(trial))
stats['seeded_N8_cases']=1200

# Adversarial special functions at N=8: OR8 has ANF degree 8,
# AND8 has degree 8, and strict majority has high global support.
def table_predicate(N,pred):
    return sum((1<<x) for x in range(1<<N) if pred(x))
N=8
OR=table_predicate(N,lambda x:x!=0)
AND=table_predicate(N,lambda x:x==(1<<N)-1)
MAJ=table_predicate(N,lambda x:x.bit_count()>N//2)
THR3=table_predicate(N,lambda x:x.bit_count()>=3)
for tag,T in [('OR',OR),('AND',AND),('MAJ',MAJ),('THR3',THR3)]:
    for sgn in (0,1):
        verify(N,((T,sgn),),tuple(),f'global-{tag}-{sgn}')
        verify(N,((T,sgn),),([1,2,4,8,16,32,64,128],),f'global-{tag}-parity-{sgn}')
        verify(N,((T,sgn),),([3,12,48,192],),f'global-{tag}-quadratic-{sgn}')
stats['global_special_cases']=24

# Hostile control: parity is not unate. Its output changes at every prefix
# and interval constancy fails unless one adds the polynomial-degree term.
PAR=table_predicate(8,lambda x:x.bit_count()%2==1)
parpath=[(PAR>>prefix(8,t))&1 for t in range(9)]
check(all(parpath[t]!=parpath[t+1] for t in range(8)),'parity nonmonotone chain control')
for t in range(8):
    check(((PAR>>prefix(8,t))&1)!=((PAR>>prefix(8,t+1))&1),'parity break counterexample')

# Exact small n=3 circuit-library control; no identification with asymptotic MCSP.
def truth_col(i):
    return sum(((x>>i)&1)<<x for x in range(8)

def gate(a,b,t):
    z=0
    for i in range(8):z|=((t>>(((a>>i)&1)*2+((b>>i)&1)))&1)<<i
    return z
base={0,255,truth_col(0),truth_col(1),truth_col(2)}
lib0=base.copy()
lib1=base.copy()
for a in base:
    for b in base:
        for t in range(16):lib1.add(gate(a,b,t))
lib2=lib1.copy()
for v in lib1:
    for b in base:
        for t in range(16):lib2.add(gate(v,b,t))
check(0<len(lib2)<256,'small-circuit library control')
for tag,T in [('OR',OR),('AND',AND),('MAJ',MAJ),('THR3',THR3)]:
    cells={0:[],1:[]}
    for f in range(256):cells[(T>>f)&1].append(f)
    joint=[v for v in range(2) if any(x in lib2 for x in cells[v]) and any(x not in lib2 for x in cells[v])]
    check(bool(joint),f'{tag} must have a mixed finite fiber at <=2-gate proxy')
    stats['mixed_small_circuit_controls']+=1

out={'title':'CLOCKMONOCHAIN26 hybrid monotone-chain + Reed-Muller obstruction',
     'status':'COMPUTATIONAL finite only; symbolic proof separate',
     'timestamp':'2026-11-17 America/Los_Angeles','seed':SEED,
     'python':sys.version.split()[0], 'assertions':checks,'failures':0,
     'statistics':dict(stats),'finite_examples':examples,
     'caveat':'N4/N8 tests do not prove asymptotic MCSP bound; circuit library controls only <=2 gates'}
with open('/mnt/data/2026-11-17_CLOCKMONOCHAIN26_raw.json','w') as f:json.dump(out,f,indent=2,sort_keys=True)
print(json.dumps(out,indent=2))
