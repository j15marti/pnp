#!/usr/bin/env python3
"""ARC-DISCONTINUITY175: exact return-cycle and declared XOR/2CNF typed controls.
The experiment is not an all-SAT contraction or calibrated FLMV TM audit.
"""
from fractions import Fraction as Q
from itertools import product
from functools import lru_cache
import json, hashlib, sys

T0,S0=Q(6,5),Q(1,2)
CT,CS=Q(241,200),Q(11642479,23232400)

def phase_A(t,s): return (T0+2*(t-T0), S0+(s-S0)/5)
def phase_B(t,s): return (T0+(t-T0)/5, S0+2*(s-S0))

def resolve(clauses):
    @lru_cache(None)
    def dfs(q):
        if not q: return True
        if any(not c for c in q): return False
        unit=next((c[0] for c in q if len(c)==1),None)
        def assign(lit):
            nxt=tuple(sorted(tuple(v for v in clause if v!=-lit) for clause in q if lit not in clause))
            return dfs(nxt)
        if unit is not None: return assign(unit)
        v=min(q,key=len)[0]
        return assign(v) or assign(-v)
    return dfs(tuple(sorted(tuple(x) for x in clauses)))

def xor3_odd(i):
    a,b,c=3*i+1,3*i+2,3*i+3
    return [tuple(v if bit==0 else -v for v,bit in zip((a,b,c),bits))
            for bits in product((0,1),repeat=3) if sum(bits)%2==0]

def assemble(lo,hi,pins):
    cs=[]
    for j in range(lo,hi): cs+=xor3_odd(j)
    for j in range(lo,hi-1): cs.append((-(3*j+1),-(3*(j+1)+1)))
    for v,b in pins:
        if lo<=((v-1)//3)<hi: cs.append((v if b else -v,))
    return cs

def serialize(clauses,nvars):
    s=f'p cnf {nvars} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)
    return s.encode('ascii')

def parse(data):
    lines=data.decode('ascii').splitlines()
    a=lines[0].split(); assert a[:2]==['p','cnf']; n=int(a[2]); k=int(a[3])
    cs=[]
    for line in lines[1:]:
        vals=list(map(int,line.split())); assert vals[-1]==0
        c=tuple(vals[:-1]); assert all(0<abs(v)<=n for v in c)
        cs.append(c)
    assert len(cs)==k
    return cs

counts=dict(assertions=0,first_level=0,second_level=0,root_sat=0,root_unsat=0,total_encoded_bytes=0,max_child_bytes=0)

def check(ok):
    assert ok
    counts['assertions']+=1

def recurse(lo,hi,pins,depth,level,nvars):
    cs=assemble(lo,hi,pins)
    buf=serialize(cs,nvars)
    check(parse(buf)==cs)
    counts['total_encoded_bytes']+=len(buf)
    if level==1:
        counts['first_level']+=1
        counts['max_child_bytes']=max(counts['max_child_bytes'],len(buf))
    if level==2: counts['second_level']+=1
    exact=resolve(cs)
    if depth==0 or hi-lo<2:
        return exact
    mid=(lo+hi)//2
    ans=False
    for b1,b2 in product((0,1),repeat=2):
        if b1 and b2: continue   # the actual crossing binary clause
        left=recurse(lo,mid,(*pins,(3*(mid-1)+1,b1)),depth-1,level+1,nvars)
        right=recurse(mid,hi,(*pins,(3*mid+1,b2)),depth-1,level+1,nvars)
        ans |= left and right
    check(exact==ans)
    return ans

def run():
    cycles=[]
    for k in (2,5,10,100,10000):
        t=s=Q(k)
        for d in range(1,80):
            t,s=phase_B(*phase_A(t,s))
            predicted_t=T0+Q(2,5)**d*(Q(k)-T0)
            predicted_s=S0+Q(2,5)**d*(Q(k)-S0)
            check((t,s)==(predicted_t,predicted_s))
            if t<CT and s<CS:
                cycles.append(dict(K=k,cycles=d,stages=2*d,t=str(t),s=str(s),
                    margin_t=str(CT-t),margin_s=str(CS-s)))
                break
        else: raise AssertionError('no finite hit')
    for k in range(2,12):
        t,s=Q(k),Q(k)
        ta,sa=phase_A(t,s)
        check(ta>t and sa<s if k>=2 else True)
        tb,sb=phase_B(ta,sa)
        check(tb<t and sb<s)
    # q=1 affine component plus binary clauses; q=2 counterpart both labels
    q1eq=[(-1,2),(1,-2)] # XOR x1 = x2, 2CNF
    check(resolve(q1eq+[(1,)]))
    check(not resolve(q1eq+[(1,),(-2,)]))
    odd=xor3_odd(0)
    check(resolve(odd+[(1,)]))
    check(not resolve(odd+[(-1,),(-2,),(-3,)]))
    samples=[]
    for n in (4,8):
        for kind in ('SAT','UNSAT_CROSS','UNSAT_LOCAL','SAT_PIN'):
            pins=()
            if kind=='UNSAT_CROSS': pins=((3*(n//2-1)+1,1),(3*(n//2)+1,1))
            if kind=='UNSAT_LOCAL': pins=((1,0),(2,0),(3,0))
            if kind=='SAT_PIN': pins=((1,1),)
            root=assemble(0,n,pins)
            expected=resolve(root)
            label=recurse(0,n,pins,2,0,3*n)
            check(label==expected)
            if expected: counts['root_sat']+=1
            else: counts['root_unsat']+=1
            samples.append(dict(blocks=n,kind=kind,satisfiable=expected,
                parent_bytes=len(serialize(root,3*n))))
    result={
        'id':'ARC-DISCONTINUITY175','status':'COMPUTATIONAL exact rationals and finite SAT controls, conditional SAT transition',
        'flmv_bounds':{'c':str(CT),'d':str(CS),'margin_time':str(CT-T0),'margin_space':str(CS-S0)},
        'phase_A':'excess_t*2; excess_s/5', 'phase_B':'excess_t/5; excess_s*2',
        'composite_factor':'2/5', 'cycle_examples':cycles,'controls':counts,
        'samples':samples,'randomness':'none',
        'limitations':['Phase edges are hypothetical machines, not constructed SAT transformations.',
        'The XOR/2CNF family is restricted and recognizable, not general SAT.',
        'Two levels have source-length proportional children, not lambda<1.',
        'Encoded byte counts are not FLMV random-access machine steps or peak space.']}
    return result

if __name__=='__main__':
    r=run()
    json.dump(r,sys.stdout,sort_keys=True,indent=2)
    print()
