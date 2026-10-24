#!/usr/bin/env python3
"""GUARD-BOUNDARY90: finite exact controls, not SAT time lower bounds."""
import itertools, json, hashlib, random

def signed_ternaries():
    return [tuple((i+1)*(1 if b==0 else -1) for i,b in enumerate(bits))
            for bits in itertools.product((0,1),repeat=3)]

def shield(H,n):
    x=n+1
    clauses=[]
    for i,(l1,l2,l3) in enumerate(H):
        a=n+2+i
        clauses.extend([(-x,l1,a),(-a,l2,l3)])
    return clauses,x,n+1+len(H)

def pin(x,p,n):
    u,v=n+1,n+2
    lit=x if p else -x
    return [(lit,e*u,d*v) for e in (1,-1) for d in (1,-1)],n+2

def dpll(formula,initial=None):
    assignment={} if initial is None else dict(initial)
    def run(A):
        while True:
            changed=False
            residual=[]
            for clause in formula:
                sat=False
                free=[]
                for lit in clause:
                    val=A.get(abs(lit))
                    if val is None: free.append(lit)
                    elif val==(lit>0):
                        sat=True;break
                if sat:continue
                if not free:return False
                if len(free)==1:
                    l=free[0];v=abs(l);b=l>0
                    if v in A and A[v]!=b:return False
                    if v not in A:A[v]=b;changed=True
                else:residual.append(free)
            if not changed:break
        if not residual:return True
        var=abs(residual[0][0])
        for b in (False,True):
            B=dict(A);B[var]=b
            if run(B):return True
        return False
    return run(assignment)

def connected(H):
    if not H:return False
    clauses=[set(abs(l) for l in c) for c in H]
    visited={0};pending=[0]
    while pending:
        j=pending.pop()
        for i in range(len(clauses)):
            if i not in visited and clauses[j]&clauses[i]:
                visited.add(i);pending.append(i)
    return len(visited)==len(clauses)

def encoded_bits(n,m):
    w=(64*(n+m+1)-1).bit_length()
    return (4*m+2)*w

def run():
    checks=0
    classes={'sat_H':0,'unsat_H':0,'sat_guard':0,'unsat_guard':0}
    templates=signed_ternaries()
    for mask in range(1,1<<len(templates)):
        H=[cl for i,cl in enumerate(templates) if mask&(1<<i)]
        satH=dpll(H)
        classes['sat_H' if satH else 'unsat_H']+=1
        G,x,nG=shield(H,3)
        assert connected(G);checks+=1
        assert len(G)==2*len(H) and nG==4+len(H);checks+=1
        assert all(len(set(map(abs,c)))==3 for c in G);checks+=1
        assert all(any(l<0 for l in c) for c in G);checks+=1
        q0,q1=dpll(G,{x:0}),dpll(G,{x:1})
        assert q0 and q1==satH;checks+=1
        b0,n0=pin(x,0,nG)
        b1,n1=pin(x,1,nG)
        assert n0==n1;checks+=1
        assert dpll(G+b0) and dpll(G+b1)==satH;checks+=1
        classes['sat_guard']+=1
        if not satH: classes['unsat_guard']+=1
        assert len(G+b0)==len(G+b1)==2*len(H)+4;checks+=1
        assert encoded_bits(n0,len(G+b0))==encoded_bits(n1,len(G+b1));checks+=1
        masks=[0,1,(1<<len(G))-1]+[((1<<j)-1) for j in range(min(3,len(G)))]
        for bits in masks:
            C=[c for j,c in enumerate(G) if bits&(1<<j)]
            assert all(any(l<0 for l in c) for c in C);checks+=1
    sat_h=templates[:7];unsat_h=templates
    assert dpll(sat_h) and not dpll(unsat_h);checks+=1
    for H in [sat_h,unsat_h]:
        G,x,nG=shield(H,3)
        assert dpll(G) and dpll(G,{x:1})==dpll(H);checks+=1
    rng=random.Random(20261024)
    for trial in range(64):
        n=3+rng.randrange(1,6)
        m=1+rng.randrange(1,16)
        H=[]
        for i in range(m):
            vs=rng.sample(range(1,n+1),3)
            H.append(tuple(v if rng.randrange(2) else -v for v in vs))
        G,x,nG=shield(H,n)
        expected=dpll(H)
        assert connected(G);checks+=1
        assert dpll(G,{x:0});checks+=1
        assert dpll(G,{x:1})==expected;checks+=1
        if rng.randrange(2):
            B,nP=pin(x,1,nG)
            assert dpll(G+B)==expected
        else:
            B,nP=pin(x,0,nG)
            assert dpll(G+B)
        checks+=1
    res=dict(run='GUARD-BOUNDARY90',status='COMPUTATIONAL',assertions=checks,
        discrepancies=0,exhaustive_nonempty_three_variable_clause_subsets=255,
        controls=64,labels=classes,
        theorem='Q_H(0)=true, Q_H(1)=SAT(H), SAT(G_H)=true; exact boundary bit NP-complete',
        caveat='source validation, SAT controls and oracle calls are actually charged in implementations; no all-decider LB')
    payload=json.dumps(res,sort_keys=True,indent=2)+'\n'
    print(payload)
    print('SHA256',hashlib.sha256(payload.encode()).hexdigest())

if __name__=='__main__':
    run()
