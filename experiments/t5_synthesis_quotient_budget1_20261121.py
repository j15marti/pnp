#!/usr/bin/env python3
"""Finite checks of count normalization, not a hardness experiment."""
import itertools as it
import json, hashlib
from pathlib import Path
from collections import Counter
from fractions import Fraction

def div10(z,width):
    r=0;q=0
    for i in range(width-1,-1,-1):
        t=2*r+((z>>i)&1)
        b=int(t>=10);r=t-10*b;q=2*q+b
    return q,r

def mul10(q,width):
    # Ripple addition of the two shifts, with overflow retained.
    out=carry=0
    for i in range(width+4):
        a=(q>>(i-3))&1 if i>=3 else 0
        b=(q>>(i-1))&1 if i>=1 else 0
        out|=((a^b)^carry)<<i
        carry=(a&b)|(a&carry)|(b&carry)
    assert carry==0
    return out

def C(a,b,c):
    return len({a,b,c})==3 and any({a,b,c}=={i,(i+1)%5,(i+2)%5} for i in range(5))

def main():
    arithmetic=[]
    for width in range(1,13):
        for z in range(1<<width):
            q,r=div10(z,width)
            assert (q,r)==divmod(z,10)
            assert mul10(q,width)+r==z
        arithmetic.append({'width':width,'cases':1<<width})
    formulas=[]
    for n in range(3,6):
        cs=list(it.combinations(range(n),3)); masks=1<<len(cs)
        hist=[0]*masks
        for a in it.product(range(5),repeat=n):
            s=sum(int(C(*(a[i] for i in c)))<<j for j,c in enumerate(cs))
            hist[s]+=1
        # Sum over all assignment satisfaction masks containing the formula.
        z=hist[:]
        for j in range(len(cs)):
            for s in range(masks):
                if not s&(1<<j):z[s]+=z[s|(1<<j)]
        assert z[0]==5**n
        assert all(x%10==0 for x in z[1:])
        formulas.append({'n':n,'clauses':cs,'counts_by_constraint_mask':z})
    # Compare exact probability vectors under injective normalization.
    distributions=[]
    for nums in it.product(range(4),repeat=3):
        if not sum(nums):continue
        ps=[Fraction(t,sum(nums)) for t in nums]
        original={10*i:p for i,p in enumerate(ps) if p}
        quotient={i:p for i,p in enumerate(ps) if p}
        assert sorted(original.values())==sorted(quotient.values())
        assert max(original.values())==max(quotient.values())
        # Enumerate all tests on three quotient outcomes and transport them.
        for test in range(8):
            p1=sum((p for x,p in original.items() if test&(1<<(x//10))),Fraction())
            p2=sum((p for x,p in quotient.items() if test&(1<<x)),Fraction())
            assert p1==p2
        distributions.append({'weights':nums,'probabilities':[str(x) for x in ps]})
    controls={
        'one_clause':{'n':3,'m':1,'N':13,'true_count':30,'fake_counts':[30,40],
                      'fake_probabilities':['1/2','1/2'],'quotient_true':3,'quotient_fake':[3,4],
                      'conditional_entropy_bits':1,'equality_advantage':'1/2','residue_advantage':0},
        'off_lattice_collision':{'fake_counts':[30,31],'floor_quotients':[3,3],
                                'entropy_before_bits':1,'entropy_after_bits':0},
        'empty_clause_counterexample':{'encoding':'101','n':1,'m':0,'N':3,'count':5,'ten_times_floor':0}}
    assert sum(C(*a) for a in it.product(range(5),repeat=3))==30
    result={'status':'PASS','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'arithmetic_rows':arithmetic,'formula_rows':formulas,
            'distribution_rows':distributions,'controls':controls,
            'scope':'Finite checks only; entropy equality proved by bijection in report.'}
    Path('raw.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','arithmetic_cases':sum(x['cases'] for x in arithmetic),
                     'nonempty_formula_cases':sum(len(x['counts_by_constraint_mask'])-1 for x in formulas),
                     'probability_vectors':len(distributions),'transported_tests':8*len(distributions)}))

if __name__=='__main__':main()
