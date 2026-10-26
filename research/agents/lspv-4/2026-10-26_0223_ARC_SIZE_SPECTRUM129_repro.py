#!/usr/bin/env python3
"""ARC size-spectrum/time-space audit: exact rational arithmetic and exhaustive restricted ordinary 3CNF controls.
No third-party dependencies, no randomness. Run: python3 arc_size_spectrum129_repro.py
"""
import itertools, json
from fractions import Fraction as F

checks=0
def check(ok,msg):
    global checks
    checks+=1
    if not ok: raise AssertionError(msg)

def fstr(x):
    x=F(x); return f"{x.numerator}/{x.denominator}" if x.denominator!=1 else str(x.numerator)

def maxf(*xs):return max(map(F,xs))

def beta(c):return ((c+2)/c**2-c)/2

# Original full-input sample bound and nonuniform alternate-seed parameters
cstar=F(241,200); sstar=F(11642479,23232400)
d=F(901,500); s=F(1)
check(beta(cstar)==sstar,'FLMV rational beta')
check(sstar-F(1,2)==F(26279,23232400),'space margin')
check(cstar-F(11,10)==F(21,200),'time margin')
check((2*d-1)/(d*(d-1))==F(651000,361301),'coNTIME branch')
check(d*d/(d*d-1)==F(811801,561801),'full decision circuit conditional value')

# First level, two size spectra: count N^(4/5) at length N^(1/10), one N^(1/2)
groups=[{'name':'many-tiny','count':F(4,5),'length':F(1,10)},
        {'name':'one-medium','count':F(0),'length':F(1,2)}]
b=F(9,10); lam=F(1,2); r=F(11,10); access=F(21,20)
coarse=b+lam*(d-1)
spectrum=max(g['count']+d*g['length'] for g in groups)
t1=maxf(r,access,spectrum)
check(coarse==F(1301,1000),'coarse exponent')
check(spectrum==F(4901,5000),'spectrum exponent')
check(t1==F(11,10),'first time')
check(coarse>cstar and t1<cstar,'numerical contrast')
check(maxf(lam,lam*s,F(2,5),F(0))==F(1,2),'eager workspace peak')

# The child solver at depth 1 has exponent t1. Its own source scanning, serializing,
# generator bookkeeping and lookup costs are premises represented by r/access,
# not proved by the numeric experiment. The second level is a genuine separate recursion.
t2=maxf(r,access,max(g['count']+g['length']*t1 for g in groups))
check(t2==F(11,10),'two levels time')
check(t2<cstar,'strict time')
check(F(1,2)<sstar,'strict space')

# Source formulas contain only clauses with exactly three distinct literal variables.
sat_leaf=[[1,2,3]]
unsat_leaf=[list(signs) for signs in itertools.product([1,-1],repeat=3)]
unsat_leaf=[[signs[i]*(i+1) for i in range(3)] for signs in itertools.product([1,-1],repeat=3)]
horn_leaf=[[-1,-2,3]]

def sat(clauses,n):
    for vals in itertools.product((False,True),repeat=n):
        if all(any(vals[abs(v)-1] if v>0 else not vals[abs(v)-1] for v in c) for c in clauses):return True
    return False

def union(parts):
    clauses=[]; off=0
    for a,n in parts:
        clauses.extend([[int(v>0)*(abs(v)+off) - int(v<0)*(abs(v)+off) for v in c] for c in a]);off+=n
    return clauses,off

def text3(clauses,n):
    for c in clauses:check(len(c)==3 and len(set(map(abs,c)))==3 and all(1<=abs(x)<=n for x in c),'proper ternary')
    return ('p cnf %d %d\n'%(n,len(clauses))+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode('ascii')

runs=0; sat_roots=0; unsat_roots=0; bits_written=0; records=0
# two disjoint level-1 CNFs, each composed of two actual level-2 ordinary CNFs
for states in itertools.product((0,1),repeat=4):
    leaves=[(sat_leaf if b else unsat_leaf,3) for b in states]
    first=[union(leaves[i:i+2]) for i in (0,2)]
    parent=union(first)
    expected=all(states)
    truth=sat(*parent)
    check(truth==expected,'two-level exact semantic AND')
    for j,x in enumerate(first):check(sat(*x)==all(states[2*j:2*j+2]),'first level child label')
    for j,x in enumerate(leaves):check(sat(*x)==bool(states[j]),'second level child label')
    # These encodings really represent ordinary CNF problems, rather than truth-bit stubs.
    for cs,n in [parent]+first+leaves:
        dat=text3(cs,n);bits_written+=len(dat)*8;records+=1
        check(dat.startswith(b'p cnf '),'physical CNF header')
    runs+=1;sat_roots+=truth;unsat_roots+=not truth
check(sat(horn_leaf,3),'Horn easy control')
check(not sat(unsat_leaf,3),'UNSAT control')
check(sat(sat_leaf,3),'SAT control')

# Adversarial implementation: answer retention as independent writable cells.
# Histograms and one-bit folding agree on all restricted conjunction instances,
# but retention has exponent 4/5, violating the simultaneous space rectangle.
check(F(4,5)>sstar,'retained answer exponent exceeds region')
check(maxf(F(4,5),lam*s,F(2,5))==F(4,5),'adversarial peak exponent')

data={
 'audit':'ARC-SIZE-SPECTRUM129','status':'CONDITIONAL+COMPUTATIONAL; P-versus-NP OPEN',
 'assumptions':{'seed_time':fstr(d),'seed_space':fstr(s),'aggregate_access_exponent':fstr(access),
                'local_work_exponent':fstr(r),'aggregate_volume_exponent':fstr(b),'max_child_exponent':fstr(lam)},
 'thresholds':{'FLMV_time':fstr(cstar),'FLMV_space':fstr(sstar),'beta_identity':fstr(beta(cstar)),
              'coNTIME_curved_threshold_extra_seed':fstr((2*d-1)/(d*(d-1))),
              'full_circuit_threshold_extra_seed':fstr(d*d/(d*d-1))},
 'exponents':{'coarse_volume':fstr(coarse),'spectrum_guest':fstr(spectrum),
               'one_level_time':fstr(t1),'two_level_time':fstr(t2),
               'ideal_streamed_eager_space':fstr(F(1,2)),'retained_answer_space':fstr(F(4,5)),
               'time_margin':fstr(cstar-t2),'space_margin':fstr(sstar-F(1,2))},
 'sample':{'actual_two_level_proper_CNF_roots':runs,'SAT_roots':sat_roots,'UNSAT_roots':unsat_roots,
           'actual_CNF_serializations':records,'emitted_bits_including_headers':bits_written,
           'assertions':checks,'seed':None},
 'caveat':'Numerical premises do not assert an all-input adaptive SAT contractor. Retained answer storage violates joint memory. Proper-CNF controls are disjoint/easy.'
}
print(json.dumps(data,indent=2,sort_keys=True))
