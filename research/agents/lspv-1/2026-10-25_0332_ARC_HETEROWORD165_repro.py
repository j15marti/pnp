#!/usr/bin/env python3
"""ARC route-word arithmetic and two-level SAT/UNSAT controls; stdlib only.
Finite resource certificates are conditional on a real uniform machine edge.
"""
from fractions import Fraction as Q
import json
import random

C=Q(241,200)
D=Q(11642479,23232400)
HALF=Q(1,2)

def phase(kind):
    lam=HALF; a=Q(3,5); r=Q(11,10)
    if kind=='eager':
        g=Q(1,20); u=a; L=max(r,a+lam+g)
    elif kind=='lazy':
        g=Q(1,20); u=a+g; L=r
    elif kind=='critical':
        g=Q(1,400); u=a+g; L=r
    elif kind=='good-lazy':
        g=Q(0); u=a; L=r
    else: raise ValueError(kind)
    return {'type':kind,'lam':lam,'u':u,'L':L,'nu':lam,'V':HALF}

def forward(word,K):
    t=s=Q(K)
    history=[]
    for kind in word:
        p=phase(kind)
        t=max(p['L'],p['u']+p['lam']*t)
        s=max(p['V'],p['nu']*s)
        history.append((t,s))
    return t,s,history

def closed(word,K):
    """Expands all lower-affine branches without floating point."""
    pt=Q(K); candidates=[]
    ps=Q(K); sp=[]
    for kind in word:
        p=phase(kind)
        pt=p['u']+p['lam']*pt
        candidates=[p['u']+p['lam']*v for v in candidates]+[p['L']]
        ps=p['nu']*ps
        sp=[p['nu']*v for v in sp]+[p['V']]
    return max([pt]+candidates),max([ps]+sp)

# Canonical DIMACS strings are actual ordinary SAT encodings, not pointers.
def dimacs(clauses):
    nv=max([abs(v) for c in clauses for v in c],default=0)
    return 'p cnf %d %d\n'%(nv,len(clauses)) + ''.join(' '.join(map(str,c))+' 0\n' for c in clauses)

def parse_dimacs(s):
    lines=s.splitlines()
    assert lines and lines[0].startswith('p cnf ')
    _,_,nv,nc=lines[0].split()
    nv=int(nv);nc=int(nc)
    assert nv>=0 and len(lines)==nc+1
    clauses=[]
    for line in lines[1:]:
        a=[int(i) for i in line.split()]
        assert a[-1]==0 and all(0<abs(x)<=nv for x in a[:-1])
        clauses.append(tuple(a[:-1]))
    return tuple(clauses)

def xor_cycle(q,start,odd=False):
    """q-variable 2-CNF cycle, SAT iff XOR of edge right sides is 0."""
    clauses=[]
    for i in range(q):
        x=start+i; y=start+(i+1)%q
        b=int(odd and i==q-1)
        clauses.extend(((x,y),(-x,-y)) if b else ((x,-y),(-x,y)))
    return tuple(clauses)

def sat2(clauses):
    """Deterministic graph SCC solver for clauses of size 1 or 2."""
    assert all(1<=len(c)<=2 for c in clauses)
    vs=sorted({abs(v) for c in clauses for v in c})
    pos={v:i for i,v in enumerate(vs)}
    n=len(vs)
    g=[[] for _ in range(2*n)]; gr=[[] for _ in range(2*n)]
    def node(x):return 2*pos[abs(x)]+int(x<0)
    def edge(x,y):
        u=node(x);v=node(y);g[u].append(v);gr[v].append(u)
    for c in clauses:
        if len(c)==1:
            (x,)=c;edge(-x,x)
        else:
            x,y=c;edge(-x,y);edge(-y,x)
    seen=[False]*(2*n);order=[]
    def dfs(u):
        seen[u]=True
        for v in g[u]:
            if not seen[v]:dfs(v)
        order.append(u)
    for u in range(2*n):
        if not seen[u]:dfs(u)
    label=[-1]*(2*n)
    def dfsr(u,k):
        label[u]=k
        for v in gr[u]:
            if label[v]<0:dfsr(v,k)
    for u in reversed(order):
        if label[u]<0:dfsr(u,u)
    return all(label[2*i]!=label[2*i+1] for i in range(n))

def two_level_controls():
    counts={'roots':0,'SAT_roots':0,'UNSAT_roots':0,'level1_calls':0,
            'level2_calls':0,'assertions':0,'max_root_bits':0,
            'max_level1_bits':0,'max_level2_bits':0,
            'shared_variable_counterexample':False,'malformed_rejected':False}
    for q in [3,4,5,6]:
        for k in range(4):
            is_unsat=(k%2==1)
            blocks=[];at=1
            for i in range(q*q):
                block=xor_cycle(q,at,odd=is_unsat and i==(q*q)//2)
                blocks.append(block);at+=q
            groups=[tuple(c for block in blocks[j*q:(j+1)*q] for c in block)
                    for j in range(q)]
            root=tuple(c for gr in groups for c in gr)
            root_string=dimacs(root)
            parent=sat2(parse_dimacs(root_string))
            counts['assertions']+=1; assert parent== (not is_unsat)
            counts['roots']+=1
            counts['SAT_roots' if parent else 'UNSAT_roots']+=1
            counts['max_root_bits']=max(counts['max_root_bits'],8*len(root_string))
            first=[];second=[]
            for j,group in enumerate(groups):
                group_string=dimacs(group)
                gp=sat2(parse_dimacs(group_string))
                counts['level1_calls']+=1
                counts['max_level1_bits']=max(counts['max_level1_bits'],8*len(group_string))
                ch=[]
                for block in blocks[j*q:(j+1)*q]:
                    block_string=dimacs(block)
                    bc=sat2(parse_dimacs(block_string))
                    counts['level2_calls']+=1
                    counts['max_level2_bits']=max(counts['max_level2_bits'],8*len(block_string))
                    ch.append(bc)
                counts['assertions']+=1;assert gp==all(ch)
                first.append(gp);second.extend(ch)
            counts['assertions']+=2
            assert parent==all(first)==all(second)
    # Independently SAT children do not glue if their scopes overlap.
    first=((1,),);second=((-1,),)
    assert sat2(first) and sat2(second) and not sat2(first+second)
    counts['assertions']+=3
    counts['shared_variable_counterexample']=True
    try:parse_dimacs('p cnf 1 1\n2 0\n')
    except AssertionError:counts['malformed_rejected']=True
    assert counts['malformed_rejected']
    counts['assertions']+=1
    return counts

def main():
    sample_words={
      'eleven_eager':['eager']*11,
      'initial_lazy_then_ten_eager':['lazy']+['eager']*10,
      'ten_eager_then_lazy':['eager']*10+['lazy'],
      'late_lazy_then_six_recovery':['eager']*10+['lazy']+['eager']*6,
      'critical_256':['critical']*256}
    samples={}
    for name,w in sample_words.items():
        t,s,_=forward(w,10)
        assert (t,s)==closed(w,10)
        samples[name]={'phases':len(w),'t':str(t),'s':str(s),
          't_decimal':round(float(t),12),'strict_finite_hit':t<C and s<D}
    rng=random.Random(20261025)
    checks=0
    for k in [2,3,10,50,100]:
        for depth in range(1,31):
            for repeat in range(20):
                word=[rng.choice(('eager','lazy','critical','good-lazy')) for _ in range(depth)]
                t,s,_=forward(word,k)
                assert (t,s)==closed(word,k)
                checks+=2
    t_crit,_,_=forward(['critical']*256,10)
    assert t_crit==C+(Q(10)-C)/2**256
    checks+=1
    sat=two_level_controls()
    data={'artifact':'ARC-HETEROWORD165','status':'CONDITIONAL-ARITHMETIC / COMPUTATIONAL-CONTROLS',
      'c_star':str(C),'d_star':str(D),'d_minus_half':str(D-Q(1,2)),
      'critical_lazy_g':str(Q(1,400)),
      'samples_K10':samples,'random_seed':20261025,
      'exact_rational_route_checks':checks,'sat_controls':sat,
      'not_claimed':'No all-input ARC machine, no FLMV contradiction, no SAT lower bound.'}
    print(json.dumps(data,indent=2,sort_keys=True))
if __name__=='__main__':main()
