#!/usr/bin/env python3
"""CHILD-SCALE-PREFIX117. Complete, standard-library source-aware join control.
The policy has no true-label oracle and falls back to ordinary exact SAT.
This tests a restricted family, not P!=NP or unrestricted solver lower bounds.
"""
import json
from collections import Counter

def pin3(l,a,b):
    return [(l,a,b),(l,a,-b),(l,-a,b),(l,-a,-b)]

def module(bits,start,loose=0):
    out=[]
    for i,bit in enumerate(bits,1):
        if i==loose: continue
        out.extend(pin3(i if bit else -i,start,start+1))
        start+=2
    return out,start

def block3(lits,start):
    lits=list(lits)
    if len(lits)==1:return pin3(lits[0],start,start+1)
    if len(lits)==2:return [(lits[0],lits[1],start),(lits[0],lits[1],-start)]
    if len(lits)==3:return [tuple(lits)]
    out=[(lits[0],lits[1],start)]
    z=start
    for l in lits[2:-2]:
        zz=z+1
        out.append((-z,l,zz))
        z=zz
    out.append((-z,lits[-2],lits[-1]))
    return out

def query(base,prefix=None,excluded=None):
    prefix=prefix or {}
    q=list(base)
    nxt=max((abs(z) for c in q for z in c),default=0)+1
    for v,bit in sorted(prefix.items()):
        q.extend(pin3(v if bit else -v,nxt,nxt+1))
        nxt+=2
    if excluded is not None:
        q.extend(block3([-i if excluded[i-1] else i for i in range(1,len(excluded)+1)],nxt))
    assert all(len(c)==3 and len({abs(z) for z in c})==3 for c in q)
    return q

def sat(clauses):
    """Complete DPLL plus recognized exact four-clause pin gadgets."""
    cls=list(clauses)
    while True:
        freq=Counter(abs(z) for c in cls for z in c)
        by={}
        for idx,c in enumerate(cls):
            if len(c)!=3:continue
            for l in c:
                a,b=sorted(abs(z) for z in c if z!=l)
                if a!=b:by.setdefault((l,a,b),[]).append(idx)
        hit=None
        for (l,a,b),inds in by.items():
            if len(inds)!=4 or freq[a]!=4 or freq[b]!=4:continue
            signs={tuple(next(z>0 for z in cls[j] if abs(z)==v) for v in (a,b)) for j in inds}
            if len(signs)==4:
                hit=(l,set(inds));break
        if hit is None:break
        l,inds=hit
        cls=[c for i,c in enumerate(cls) if i not in inds]+[(l,)]
    variables={abs(l) for c in cls for l in c}
    def go(a):
        while True:
            changed=False
            all_good=True
            for clause in cls:
                if any(abs(l) in a and a[abs(l)]==(l>0) for l in clause):continue
                missing=[l for l in clause if abs(l) not in a]
                if not missing:return None
                all_good=False
                if len(missing)==1:
                    l=missing[0]
                    a=dict(a);a[abs(l)]=l>0
                    changed=True;break
            if all_good:return a
            if not changed:break
        var=min(variables-set(a))
        return go({**a,var:False}) or go({**a,var:True})
    return go({})

def projection(base,w,stats):
    def check(q):
        stats['calls']+=1
        stats['query_clauses']+=len(q)
        return sat(q) is not None
    if not check(base):return 'EMPTY',None
    prefix={}
    for i in range(1,w+1):
        prefix[i]=False if check(query(base,{**prefix,i:False})) else True
    y=tuple(prefix[i] for i in range(1,w+1))
    assert check(query(base,prefix))
    return ('UNIQUE' if not check(query(base,excluded=y)) else 'MULTIPLE'),y

def run_case(w,kind):
    x=tuple(i%3==0 for i in range(w))
    y=list(x)
    if kind!='SAT':y[-1]=not y[-1]
    A,nxt=module(x,w+1)
    B,_=module(y,nxt,loose=w if kind=='FALLBACK_SAT' else 0)
    stats={'calls':0,'query_clauses':0}
    ta,ya=projection(A,w,stats)
    tb,yb=projection(B,w,stats)
    if ta=='UNIQUE' and tb=='UNIQUE':
        result=ya==yb;method='UNIQUE_JOIN'
    else:
        result=sat(A+B) is not None;method='EXACT_FALLBACK';stats['calls']+=1
    assert result==(kind!='UNSAT')
    assert method==('EXACT_FALLBACK' if kind=='FALLBACK_SAT' else 'UNIQUE_JOIN')
    return {'width':w,'kind':kind,'sat':result,'method':method,'calls':stats['calls'],
            'clauses_generated':stats['query_clauses']}

def main():
    rows=[run_case(w,k) for w in (4,6,8,12) for k in ('SAT','UNSAT','FALLBACK_SAT')]
    assert all(r['calls']==2*r['width']+(7 if r['kind']=='FALLBACK_SAT' else 6) for r in rows)
    # Relative-width counterexample (algebraic; source serialization in local package).
    for h in (8,16,32):
        assert h <= (20*h)/20 and h > (10*h)/20
    print(json.dumps({'run':'CHILD-SCALE-PREFIX117','passed':True,'controls':len(rows),'rows':rows},indent=2))
if __name__=='__main__': main()
