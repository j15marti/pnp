#!/usr/bin/env python3
"""Reproduce LSPV-3 M22-TWO-HALL-CUBE107 finite controls (not FLMV bit traces)."""
from itertools import product
from pathlib import Path
import sys, json, math, random

def family(q):
    assert q >= 2
    t=3*q
    D=list(range(t))
    Z=list(range(t,2*t))
    P={tuple(range(3*j,3*j+3)) for j in range(q)}
    Q={tuple(sorted((3*j,3*j+1,3*((j+1)%q)+2))) for j in range(q)}
    H={tuple(sorted((i,Z[i],Z[(i+1)%t]))) for i in D}
    assert len(P)==len(Q)==q and P.isdisjoint(Q) and H.isdisjoint(P|Q)
    return P|H,Q|H

def grammar(P,Q):
    assert P and Q and len(P)==len(set(P)) and len(Q)==len(set(Q))
    names=set().union(*P,*Q)
    for s in P|Q:
        assert len(s)==3 and len(set(s))==3
    for v in names:
        assert sum(v in s for s in P)==2
        assert sum(v in s for s in Q)==2
    assert 3*(len(P)+len(Q))==4*len(names)
    return len(names)

def matching(items):
    owner={}
    calls=0
    def aug(i,seen):
        nonlocal calls
        calls+=1
        for v in items[i]:
            if v in seen: continue
            seen.add(v)
            if v not in owner or aug(owner[v],seen):
                owner[v]=i
                return True
        return False
    for i in range(len(items)):
        assert aug(i,set()), ('Hall matching failed',i)
    return {i:v for v,i in owner.items()},calls

def hall_witness(P,Q):
    k=grammar(P,Q)
    H=P&Q; pp=P-H; qq=Q-H
    D=set().union(*pp,*qq)
    assert set().union(*pp)==set().union(*qq)
    Z=set(range(k))-D
    assert H and pp and qq and P!=Q
    assert all(len(set(h)&D)==1 for h in H)
    assert all(sum(v in h for h in H)==1 for v in D)
    assert all(sum(v in h for h in H)==2 for v in Z)
    unmatched=[('+',s) for s in sorted(pp)]+[('-',s) for s in sorted(qq)]
    a={v:0 for v in range(k)}
    ma,ca=matching([tuple(sorted(s)) for _,s in unmatched])
    for i,v in ma.items():a[v]=int(unmatched[i][0]=='+')
    paired=sorted(H)
    mb,cb=matching([tuple(sorted(set(h)&Z)) for h in paired])
    for i,v in mb.items():
        d=next(iter(set(paired[i])&D))
        a[v]=1-a[d]
    assert all(any(a[v] for v in s) for s in P)
    assert all(any(not a[v] for v in s) for s in Q)
    return a,dict(k=k,m=len(P)+len(Q),q=len(pp),H=len(H),D=len(D),Z=len(Z),matchingA_calls=ca,matchingB_calls=cb)

def check(clauses,assignment):
    return all(any(assignment[v] if sign=='+' else not assignment[v] for v in s) for sign,s in clauses)

def cube_check(P,Q):
    H=sorted(P&Q)
    D=sorted(set().union(*(P-(P&Q))))
    Z=sorted(set().union(*H)-set(D))
    assert len(D)<=6
    for dbits in product((0,1),repeat=len(D)):
        d=dict(zip(D,dbits))
        assert any(all(len({val.get(v,d.get(v)) for v in h})>1 for h in H)
                   for zb in product((0,1),repeat=len(Z))
                   for val in [dict(zip(Z,zb))])
    return True

def bits(clauses,k):
    m=len(clauses)
    w=math.ceil(math.log2(k+m+2))
    return 2*w+sum(3+len(s)*w for _,s in clauses)

def pin(clauses,v,b):
    out=[]
    for sign,s in clauses:
        if v not in s:
            out.append((sign,s))
        elif (b==1 if sign=='+' else b==0):
            continue
        else:
            out.append((sign,tuple(x for x in s if x!=v)))
    return out

def main():
    rng=random.Random(202610241952)
    rows=[]
    for q in (2,3,4,6,10,32):
        P,Q=family(q)
        k=grammar(P,Q)
        a,row=hall_witness(P,Q)
        assert k==6*q and row['H']==3*q and row['q']==q
        for _ in range(12):
            perm=list(range(k));rng.shuffle(perm)
            p={tuple(sorted(perm[v] for v in s)) for s in P}
            n={tuple(sorted(perm[v] for v in s)) for s in Q}
            grammar(p,n)
            b,_=hall_witness(p,n)
            assert check([('+',s) for s in p]+[('-',s) for s in n],b)
        if q==2:
            assert cube_check(P,Q)
            clauses=sorted([('+',s) for s in P]+[('-',s) for s in Q])
            one=pin(clauses,0,a[0])
            two=pin(one,1,a[1])
            assert all(check(cs,a) for cs in (clauses,one,two))
            assert set(len(s) for _,s in one)!={3}
            assert set(len(s) for _,s in two)!={3}
            row['two_level_pins']=[[0,a[0]],[1,a[1]]]
            row['encoded_bits_two_levels']=[bits(cs,k) for cs in (clauses,one,two)]
            row['child_clause_widths']=[sorted(set(len(s) for _,s in cs)) for cs in (clauses,one,two)]
            assert row['encoded_bits_two_levels']==[298,252,216]
            for cs in (clauses,one,two):
                assert any(check(cs,dict(enumerate(b))) for b in product((0,1),repeat=k))
        rows.append(row)
    generalized=[]
    for q in (2,3,4,6):
        t=3*q;valid=0;attempts=0
        while valid<40 and attempts<2000:
            attempts+=1
            u=list(range(t));a=u[:];b=u[:]
            rng.shuffle(a);rng.shuffle(b)
            pp={tuple(sorted(a[3*j:3*j+3])) for j in range(q)}
            qq={tuple(sorted(b[3*j:3*j+3])) for j in range(q)}
            if pp&qq:continue
            perm=list(range(t));rng.shuffle(perm)
            if any(i==perm[i] for i in range(t)):continue
            H={tuple(sorted((i,t+i,t+perm[i]))) for i in range(t)}
            if len(H)!=t:continue
            P=pp|H;Q=qq|H
            if len(P)!=q+t or len(Q)!=q+t:continue
            cert,stats=hall_witness(P,Q)
            assert stats['q']==q
            assert check([('+',s) for s in P]+[('-',s) for s in Q],cert)
            valid+=1
        assert valid==40
        generalized.append(dict(q=q,verified_distinct_guarded_sources=valid,attempts=attempts))
    PY={(0,1,2),(0,3,4),(1,3,5),(2,4,5)}
    QY={(0,1,3),(0,2,5),(1,2,4),(3,4,5)}
    assert grammar(PY,QY)==6 and PY!=QY
    Y=sum(check([('+',s) for s in PY]+[('-',s) for s in QY],dict(enumerate(a)))
          for a in product((0,1),repeat=6))
    assert Y==20
    out={'run_id':'M22-HALL-DOUBLE-MATCH107','seed':202610241952,
         'q_values':[2,3,4,6,10,32],'relabelings_each':12,
         'general_guard_random_tests':generalized,'family_rows':rows,'Y_models':Y,
         'full_cube_q2':True,'two_level_pin_selection':'follow computed SAT certificate',
         'assertion_failures':0,'claim_scope':'finite audit and exact algebraic proof; no FLMV measurement'}
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path('M22_HALL_DOUBLE_MATCH107_results.json')
    path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
