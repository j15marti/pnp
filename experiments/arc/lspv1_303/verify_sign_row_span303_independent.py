#!/usr/bin/env python3
"""Independent no-producer-import verifier: source signed-literal encoding, bottom-up witnesses."""
import json,itertools,sys
from collections import Counter

POS9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
NEG9=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
POS6=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
NEG6=((1,2,4),(1,3,6),(2,3,5),(4,5,6))

def make(P,N):return tuple(tuple(v for v in c) for c in P)+tuple(tuple(-v for v in c) for c in N)
def sat(C,bits):return all(any((bits[abs(l)-1] if l>0 else 1-bits[-l-1]) for l in c) for c in C)
def rank(vectors):
    basis={}
    for word in vectors:
        x=word
        while x:
            k=x.bit_length()-1
            if k in basis:x^=basis[k]
            else:basis[k]=x;break
    return len(basis)

def rows_for_partial(C,p,q):
    un=[];covered={}
    for j,c in enumerate(C):
        if any((l>0 and p[abs(l)-1]==1) or (l<0 and p[abs(l)-1]==0) for l in c):covered[j]=c;continue
        if all(p[abs(l)-1]!=-1 for l in c):return None
        free=tuple(l for l in c if p[abs(l)-1]==-1)
        mask=0
        for l in free: mask ^= 1<<(abs(l)-1)
        rhs=q[j]^(sum(l<0 for l in free)&1)
        un.append((j,mask,rhs))
    return un,covered

def check():
    raw=json.load(open('sign_row_span303_raw.json'))
    metrics={};assertions=0
    for label,P,N in (('Y6',POS6,NEG6),('F9',POS9,NEG9)):
        C=make(P,N);n=6 if label=='Y6' else 9
        assert len(C)*3==4*n;assert len(set(C))==len(C)
        quotas=Counter((abs(l),l>0) for c in C for l in c)
        assert len(quotas)==2*n and set(quotas.values())=={2}
        allbits=list(itertools.product((0,1),repeat=n))
        models=[b for b in allbits if sat(C,b)]
        assert len(models)==raw['families'][label]['global_models'];assertions+=1
        extreme_checks=0
        for a in allbits:
            a_inv=tuple(1-x for x in a)
            for c in C:
                t=sum((a[abs(l)-1] if l>0 else 1-a[abs(l)-1]) for l in c)
                ti=sum((a_inv[abs(l)-1] if l>0 else 1-a_inv[abs(l)-1]) for l in c)
                assert t+ti==3;assertions+=1
        for j,k in itertools.combinations(range(len(C)),2):
            same=bool(set(C[j])&set(C[k]));opp=bool({-l for l in C[j]}&set(C[k]))
            for sj,sk in itertools.product((0,1),repeat=2):
                feasible=any(all(((b[abs(l)-1] if l>0 else 1-b[abs(l)-1])==val) for ci,val in ((j,sj),(k,sk)) for l in C[ci]) for b in allbits)
                expected=(not opp) if sj==sk else (not same)
                assert feasible==expected;extreme_checks+=1
        assert extreme_checks==(len(C)*(len(C)-1)//2)*4
        derived=0
        for b in models:
            for keep in range(1<<n):
                p=tuple(b[i] if (keep>>i)&1 else -1 for i in range(n))
                q=[sum((b[abs(l)-1] if l>0 else 1-b[abs(l)-1]) for l in c)&1 for c in C]
                result=rows_for_partial(C,p,q); assert result is not None
                uncl,covered=result
                allv=[(m<<1)|r for _,m,r in uncl]
                for sign in (1,-1):
                    ids=[j for j,_,_ in uncl if (C[j][0]>0)==(sign==1)]
                    xored=0
                    for j,m,r in uncl:
                        if j in ids:xored ^= (m<<1)|r
                    covered_count=[0]*n
                    for j,c in covered.items():
                        if (c[0]>0)==(sign==1):
                            for l in c:covered_count[abs(l)-1]+=1
                    mask=sum((covered_count[i]&1)<<i for i in range(n) if p[i]==-1)
                    assert xored>>1==mask
                    assert rank(allv+[xored])==rank(allv)
                    derived+=1;assertions+=2
        assert derived==raw['families'][label]['checks']['row_XOR_source_id_tests']
        metrics[label]={'models':len(models),'row_span_checks':derived,'pair_extreme_modes':extreme_checks,'complete_assignment_complement_assertions':len(allbits)*len(C)}
    C=make(POS9,NEG9);arb=0
    for q in itertools.product((0,1),repeat=12):
        uncl,_=rows_for_partial(C,(-1,)*9,q)
        full=[(m<<1)|r for j,m,r in uncl]
        for s in (True,False):
            aggregate=0
            for j,m,r in uncl:
                if (C[j][0]>0)==s:aggregate^=(m<<1)|r
            assert rank(full+[aggregate])==rank(full)
            arb+=1
    assert arb==8192;assertions+=arb
    ticketq=tuple(0 if (j==0 or 6<=j<=10) else 1 for j in range(12))
    uncl,_=rows_for_partial(C,(-1,)*9,ticketq)
    for sign in (True,False):
        folded=0
        for j,m,r in uncl:
            if (C[j][0]>0)==sign:folded^=(m<<1)|r
        assert folded==1;assertions+=1
    assert raw['controls']['F9_root_odd_positive_ticket']['total_ticket_excess']==6;assertions+=1
    for key in ('F9_sat','F9_unsat','F9_sixpin_unsat'):
        p={int(k):v for k,v in raw['controls'][key]['partial'].items()}
        sols=[b for b in itertools.product((0,1),repeat=9) if all(b[i-1]==v for i,v in p.items()) and sat(C,b)]
        assert len(sols)==raw['controls'][key]['SAT_extensions'];assertions+=1
    C=make(POS6,NEG6)
    p=(0,)+(-1,)*5;witnesses=[]
    for b in itertools.product((0,1),repeat=6):
        if b[0]==0 and sat(C,b):
            exminus=sum(sum(1-b[-l-1] for l in c)-1 for c in C if c[0]<0 and not any(l<0 and p[-l-1]==0 for l in c))
            witnesses.append((b,exminus&1))
    assert len(witnesses)==10 and {v for _,v in witnesses}=={0,1};assertions+=2
    print(json.dumps({'verifier':'independent_no_producer_import','passed':True,'assertions':assertions,'arbitrary_F9_root_parity_rows':arb,'families':metrics,'same_source_F9_sat_unsat':True,'Y6_pin_parity_scope_counterexample':True,'native_FLVM_measurement':False},sort_keys=True))
if __name__=='__main__':check()
