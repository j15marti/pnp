#!/usr/bin/env python3
"""Minimal reproducible ADAPTIVE-COVER75 theorem check, no external packages.
For the more extensive 6361-check audit see the run's raw result and handoff.
Finite enumeration never proves unrestricted asymptotic SAT hardness.
"""
import itertools

def source(q,b):
    u,v=q+2,q+3
    a=[(1,u),(1,-u),(-(q+1),v),(-(q+1),-v)]
    a += [(-i,i+1 if bit else -(i+1)) for i,bit in enumerate(b,1)]
    return q+3,a

def lift(q,b):
    n,a=source(q,b)
    c=[]
    for j,(x,y) in enumerate(a):
        z=n+j+1
        c.extend([(x,y,z),(x,y,-z)])
    return n+len(a),c

def words(n,C):
    out=[n,len(C)]
    for c in C:
        out.extend([3]+[2*abs(x)+(x<0) for x in c])
    return out

def sat_under(C,truth):
    return all(any(truth[abs(x)]==(x>0) for x in c) for c in C)

def brute(n,C):
    return any(sat_under(C,(False,)+b)
               for b in itertools.product((False,True),repeat=n))

def check(q,b):
    n,C=lift(q,b)
    assert n==2*q+7 and len(C)==2*q+8
    assert len(words(n,C))==8*q+34
    assert len(set(C))==len(C)
    assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in C)
    label=(0 in b)
    if q<=4: assert brute(n,C)==label
    if label:
        i=b.index(0)+1
        truth=[False]*(n+1)
        for j in range(q+1):truth[j+1]=(j<i)
        assert sat_under(C,truth)
    return label

if __name__=="__main__":
    checked=0
    neighbors=0
    for q in range(1,11):
        for b in itertools.product((0,1),repeat=q):
            assert check(q,b)==(0 in b)
            checked+=1
        all1=(1,)*q
        base=words(*lift(q,all1))
        occupied=set()
        for i in range(q):
            flip=list(all1)
            flip[i]=0
            W=words(*lift(q,flip))
            D={j for j,(x,y) in enumerate(zip(base,W)) if x!=y}
            assert len(D)==2 and not D.intersection(occupied)
            assert all(base[j]^W[j]==1 for j in D)
            occupied.update(D)
            neighbors+=1
        assert len(occupied)==2*q
    controls={
      "2SAT_SAT":(2,[(1,2),(-1,2)],True),
      "2SAT_UNSAT":(2,[(1,2),(1,-2),(-1,2),(-1,-2)],False),
      "Horn_SAT":(3,[(-1,-2,3),(-3,-2)],True),
      "Horn_UNSAT":(2,[(1,),(-1,2),(-2,)],False),
      "XOR_SAT":(3,[(1,2,-3),(1,-2,3),(-1,2,3),(-1,-2,-3)],True),
      "XOR_UNSAT":(1,[(1,),(-1,)],False),
      "components_SAT":(4,[(1,2),(-1,2),(3,4)],True),
      "components_UNSAT":(4,[(1,),(-1,),(3,4)],False)
    }
    for n,C,want in controls.values():
        assert brute(n,C)==want
    print({"status":"PASS","lifted_sources":checked,
           "disjoint_flip_pairs":neighbors,
           "independent_controls":len(controls)})
