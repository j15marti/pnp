#!/usr/bin/env python3
"""Independent exhaustive checker for the connected six-vertex cubic Tseitin pair.
Rebuilds the original clauses, checks 64 right-side vectors and all assignments.
Stdlib only. It does not import the full benchmark producer.
"""
import itertools, json
def graph():
    return [(0,1),(0,2),(0,3),(1,2),(1,4),(2,5),(3,4),(3,5),(4,5)]
def source(b):
    es=graph(); F=[]
    for v in range(6):
        ids=[i+1 for i,(u,w) in enumerate(es) if v in (u,w)]
        assert len(ids)==3
        for a in itertools.product((0,1),repeat=3):
            if sum(a)%2==b[v]: continue
            F.append(tuple(-z if bit else z for z,bit in zip(ids,a)))
    return F
def litcount(c,mask):
    return sum(((mask>>(abs(z)-1))&1)==int(z>0) for z in c)
def models(F):
    return [x for x in range(512) if all(litcount(c,x)>=1 for c in F)]
def rank(rows):
    basis={}
    for r in rows:
        t=r
        while t:
            h=t.bit_length()-1
            if h in basis:t^=basis[h]
            else:basis[h]=t;break
    return len(basis)
def main():
    es=graph()
    R=[sum(1<<i for i,(u,w) in enumerate(es) if v in (u,w)) for v in range(6)]
    assert rank(R)==5
    subsets=0
    for m in range(63):
        S=[R[i] for i in range(6) if (m>>i)&1]
        assert rank(S)==len(S);subsets+=1
    sat=unsat=toggles=pairs=complements=0
    for bmask in range(64):
        b=[(bmask>>i)&1 for i in range(6)]
        F=source(b)
        assert len(F)==24 and all(len(c)==3 and len(set(map(abs,c)))==3 for c in F)
        for i in range(1,10):
            assert sum(i in c for c in F)==4
            assert sum(-i in c for c in F)==4
        witnesses=models(F)
        assert bool(witnesses)==(sum(b)%2==0)
        assert len(witnesses)==(16 if sum(b)%2==0 else 0)
        assert sum(all(z>0 for z in c) for c in F)==sum(b)
        sat+=int(bool(witnesses));unsat+=int(not witnesses)
        for i in range(6):
            other=b[:];other[i]^=1
            assert bool(models(source(other)))!=bool(witnesses);toggles+=1
        counts=[[litcount(c,x) for c in F] for x in range(512)]
        for x in range(512):
            assert all(counts[x][i]+counts[511^x][i]==3 for i in range(24))
            complements+=1
        if bmask in (0,1):
            for j in range(24):
                for k in range(j+1,24):
                    a=F[j];c=F[k]
                    shared=set(map(abs,a))&set(map(abs,c))
                    same=any(next(z for z in a if abs(z)==i)*next(z for z in c if abs(z)==i)>0 for i in shared)
                    opposite=any(next(z for z in a if abs(z)==i)*next(z for z in c if abs(z)==i)<0 for i in shared)
                    for u,v in ((3,3),(3,0),(0,3),(0,0)):
                        expect=(not opposite) if u==v else (not same)
                        actual=any(row[j]==u and row[k]==v for row in counts)
                        assert actual==expect;pairs+=1
    print(json.dumps({'status':'PASS','v':6,'e':9,'source_clauses':24,
        'SAT_rhs':sat,'UNSAT_rhs':unsat,'models_per_SAT_charge':16,
        'rank_checks_proper_subsets':subsets,'charge_bit_flip_checks':toggles,
        'assignment_complement_checks':complements,'SS_SU_US_UU_checks':pairs},indent=2))
if __name__=='__main__':main()
