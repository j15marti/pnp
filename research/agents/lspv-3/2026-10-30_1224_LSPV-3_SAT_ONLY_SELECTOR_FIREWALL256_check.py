#!/usr/bin/env python3
"""Independent truth-table and safe-selector test. Does not import producer."""
import itertools
from fractions import Fraction

def models(F,n):
    return [a for a in itertools.product((False,True),repeat=n)
            if all(any(a[abs(l)-1] == (l>0) for l in c) for c in F)]

def safe_chain(F,n):
    allmodels=models(F,n)
    partial={}
    for x in range(1,n+1):
        probe=partial | {x:False}
        choose_zero=any(all(a[i-1]==v for i,v in probe.items()) for a in allmodels)
        partial[x]=False if choose_zero else True
    candidate=tuple(partial[x] for x in range(1,n+1))
    is_sat=all(any(candidate[abs(l)-1]==(l>0) for l in c) for c in F)
    assert is_sat == bool(allmodels)
    return is_sat

def triples():
    clauses=[tuple((i+1)*sign[i] for i in range(3))
             for sign in itertools.product((-1,1),repeat=3)]
    totals={'formulas':0,'SAT':0,'UNSAT':0,'validated_selector':0,
            'bad_first_zero_on_SAT':0,'pairs':0,'complements':0}
    for mask in range(256):
        F=[clauses[j] for j in range(8) if (mask>>j)&1]
        M=models(F,3)
        got=safe_chain(F,3)
        assert got==bool(M)
        totals['formulas']+=1
        totals['validated_selector']+=1
        totals['SAT' if M else 'UNSAT']+=1
        if M and not any(a[0]==False for a in M):
            totals['bad_first_zero_on_SAT']+=1
        for j in range(len(F)):
            for k in range(j+1,len(F)):
                s={abs(l):l>0 for l in F[j]}
                t={abs(l):l>0 for l in F[k]}
                equal=all(s[i]==t[i] for i in s)
                opposite=all(s[i]!=t[i] for i in s)
                for ext1,ext2,expected in [('S','S',equal),('U','U',equal),
                                           ('S','U',opposite),('U','S',opposite)]:
                    jmap={i:(s[i] if ext1=='S' else not s[i]) for i in s}
                    kmap={i:(t[i] if ext2=='S' else not t[i]) for i in t}
                    feasible=any(all(a[i-1]==v for i,v in jmap.items()) and
                                 all(a[i-1]==v for i,v in kmap.items())
                                 for a in itertools.product((False,True),repeat=3))
                    assert feasible==expected
                    totals['pairs']+=1
        for a in itertools.product((False,True),repeat=3):
            b=tuple(not x for x in a)
            for c in F:
                u=sum(a[abs(l)-1]==(l>0) for l in c)
                v=sum(b[abs(l)-1]==(l>0) for l in c)
                assert u+v==3
            totals['complements']+=1
    assert totals=={'formulas':256,'SAT':255,'UNSAT':1,'validated_selector':256,
                     'bad_first_zero_on_SAT':15,'pairs':7168,'complements':2048}
    return totals

W=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
   (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
   (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),
   (6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),
   (-5,-12,15),(-1,13,14)]
S=W.copy();S[9]=(-5,6,-15);S[13]=(-3,-6,-15)

def strict():
    r={}
    for label,F in [('W1',W),('SWAP6',S)]:
        for x in range(1,16):
            assert sum(l==x for c in F for l in c)==2
            assert sum(l==-x for c in F for l in c)==2
        count=len(models(F,15))
        assert count==({'W1':0,'SWAP6':54}[label])
        r[label]=count
    return r

def flmv():
    c=Fraction(241,200);f=Fraction(1);best=Fraction(0);bestidx=None
    for k in range(1,50):
        f=c*f/(1+f)
        dk=min((1/f-c)/k,c**(-k))
        if dk>best:best,bestidx=dk,k
        if best>0 and c**(-(k+1))<best:
            assert (best,bestidx,k)==(Fraction(11642479,23232400),2,3)
            return {'d':str(best),'best_index':bestidx,'tail_at':k}
    raise AssertionError('tail not certified')

if __name__=='__main__':
    import json
    print(json.dumps({'n3':triples(),'strict22':strict(),'flmv':flmv()},sort_keys=True,indent=2))
