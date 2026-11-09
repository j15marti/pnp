#!/usr/bin/env python3
"""Independent finite control for the q-ary charge-fiber Fourier-degree theorem.
Only one-hot group indicators; no auxiliary variables or proof claims.
"""
from itertools import product, combinations
from math import comb, ceil
import json, sys, time

def rank(columns):
    piv = {}
    for v in columns:
        while v:
            p = v.bit_length()-1
            if p in piv: v ^= piv[p]
            else:
                piv[p] = v
                break
    return len(piv)

def tests(q,b,eps,c,maxd):
    tuples=list(product(range(q),repeat=b))
    fiber=[x for x in tuples if sum(e*a for e,a in zip(eps,x))%q==c]
    assert len(fiber)==q**(b-1)
    # Derive the coordinate basis of degree <=d on each evaluation domain.
    res=[]
    for d in range(maxd+1):
        mon=[]
        for r in range(d+1):
            for ids in combinations(range(b),r):
                for vals in product(range(q),repeat=r):
                    mon.append((ids,vals))
        def eval_vec(domain,ids,vals):
            out=0
            for i,x in enumerate(domain):
                if all(x[j]==v for j,v in zip(ids,vals)):out |= 1<<i
            return out
        full=rank([eval_vec(tuples,*z) for z in mon])
        on=rank([eval_vec(fiber,*z) for z in mon])
        # expected full rank: unique ANOVA basis (q-1)^r for each degree r
        expect=sum(comb(b,r)*(q-1)**r for r in range(d+1))
        assert full==expect,(q,b,d,full,expect)
        if d<ceil(b/2):assert on==full,(q,b,eps,c,d,full,on)
        res.append({'d':d,'full_rank':full,'charge_fiber_rank':on,'separation_possible':on<full})
    # Explicit degree ceil(b/2) XOR witness.
    split=b//2
    wrong=[]
    for x in tuples:
        lhs=sum(e*a for e,a in zip(eps[:split],x[:split]))%q
        rhs=sum(e*a for e,a in zip(eps[split:],x[split:]))%q
        f=int(lhs==0)^int(rhs==c)
        if sum(e*a for e,a in zip(eps,x))%q==c:assert f==0
        elif f:wrong.append(x)
    assert wrong and ceil(b/2)<=maxd
    # At q odd even char, this is an exactly testable, nonzero witness.
    return {'q':q,'b':b,'eps':eps,'charge':c,'fiber_size':len(fiber),'rank_by_degree':res,'explicit_witness_degree':ceil(b/2),'wrong_tuples_detected':len(wrong),'wrong_total':len(tuples)-len(fiber),'witness_example':wrong[0]}

if __name__=='__main__':
    start=time.perf_counter(); data=[]
    configs=[(3,b,(1,)*b,0,ceil(b/2)) for b in range(2,8)]
    configs += [(3,4,(1,-1,1,-1),1,2),(3,5,(1,-1,1,-1,1),2,3),
                (5,3,(1,-1,1),2,2),(5,4,(1,1,-1,-1),0,2),
                (7,3,(1,-1,-1),3,2)]
    for q,b,eps,c,d in configs:data.append(tests(q,b,eps,c,d))
    result={'theorem':'for odd q, min one-hot algebraic degree separating any off-fiber point is ceil(b/2)',
            'status':'finite validation of separately proved theorem',
            'cases':data,'seconds':round(time.perf_counter()-start,5)}
    with open('/mnt/data/lspv1_532_fourier_degree_results.json','w') as f:json.dump(result,f,indent=2)
    print('PASS',len(data),'configurations','total rank stages',sum(len(r['rank_by_degree']) for r in data),'seconds',result['seconds'])
    for r in data:print(r['q'],r['b'],[(d['d'],d['full_rank'],d['charge_fiber_rank']) for d in r['rank_by_degree']])
