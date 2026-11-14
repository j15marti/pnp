#!/usr/bin/env python3
"""Independent Hall-certificate extremal audit for the authenticated 8x3 mask promise.
Uses direct UNSAT permutation compatibility, NOT Hall matching or peer verifier imports.
All finite experiments are COMPUTATIONAL, not P-versus-NP claims.
"""
import itertools
import collections
import json
from math import comb

ROWS=range(8)
COLS=range(3)


def bit(a,j):
    return (a>>(2-j)) & 1


def m7_structural(a):
    result=0
    for j in COLS:
        for k in COLS:
            if j==k: continue
            for b in (0,1):
                for c in (0,1):
                    nH=sum(bit(x,j)==b for x in a)
                    nJ=sum(bit(x,k)==c for x in a)
                    m=sum(bit(x,j)==b and bit(x,k)==c for x in a)
                    for i in range(5):
                        if 0<=i<=m and 0<=4-i<=nH-m and nJ-i>=3:
                            result+=comb(m,i)*comb(nH-m,4-i)*comb(nJ-i,3)
    return result


def sweep_balanced():
    cols=[sum(1<<i for i in selected) for selected in itertools.combinations(ROWS,4)]
    hist=collections.Counter()
    maximum=-1
    max_count=0
    max_example=None
    # Every ordered row-mask tuple with 4/4 sign balance on all three columns occurs once.
    for x in cols:
        for y in cols:
            p=(x&y).bit_count()
            vxy=16 if p in (0,4) else 4 if p in (1,3) else 0
            for z in cols:
                p=(x&z).bit_count()
                vxz=16 if p in (0,4) else 4 if p in (1,3) else 0
                p=(y&z).bit_count()
                vyz=16 if p in (0,4) else 4 if p in (1,3) else 0
                val=vxy+vxz+vyz
                hist[val]+=1
                if val>maximum:
                    maximum=val
                    max_count=1
                    max_example=[4*bool(x&(1<<i))+2*bool(y&(1<<i))+bool(z&(1<<i)) for i in ROWS]
                elif val==maximum:
                    max_count+=1
    assert sum(hist.values())==70**3==343000
    assert maximum==48
    return {'total':sum(hist.values()),'max_M7':maximum,'maximizers':max_count,
            'example':max_example,'histogram':dict(sorted(hist.items()))}


def direct_test(a):
    permutations=list(itertools.permutations(ROWS))
    # For each source bit position, a bitset of actual permutations agreeing with a there.
    cm=[]
    for row in ROWS:
        for j in COLS:
            accepted=0
            expected=bit(a[row],j)
            for p,perm in enumerate(permutations):
                if bit(perm[row],j)==expected:
                    accepted|=(1<<p)
            cm.append(accepted)
    full=(1<<len(permutations))-1
    c7=0
    minimal=0
    first=[]
    examined=0
    for q in itertools.combinations(range(24),7):
        examined+=1
        prefix=[full]
        for x in q: prefix.append(prefix[-1]&cm[x])
        if prefix[-1]!=0: continue
        c7+=1
        suffix=[full]*8
        for i in range(6,-1,-1): suffix[i]=suffix[i+1]&cm[q[i]]
        if all(prefix[i]&suffix[i+1] for i in range(7)):
            minimal+=1
            if len(first)<3: first.append(q)
    assert examined==comb(24,7)==346104
    predicted=m7_structural(a)
    assert minimal==predicted,(a,minimal,predicted)
    return {'masks':list(a),'query_sets_7_checked':examined,
            'all_7_certificates':c7,'minimal_7':minimal,'predicted_m7':predicted,
            'witnesses':[list(q) for q in first]}


def main():
    bal=sweep_balanced()
    fixtures=[(0,0,0,0,7,7,7,7),(7,)*8,(0,0,1,1,6,6,7,7),(0,1,2,3,4,5,6,7)]
    tests=[direct_test(a) for a in fixtures]
    assert tests[0]['minimal_7']==48
    assert tests[1]['minimal_7']==1680
    assert tests[2]['minimal_7']==16
    assert tests[3]['minimal_7']==0
    print(json.dumps({'schema':'tmr2-m7-014','status':'COMPUTATIONAL','method':'independent direct full UNSAT permutation-bitset intersections and complete balanced-column sweep','balanced':bal,
                      'fixtures':tests,'total_query_sets_checked':sum(t['query_sets_7_checked'] for t in tests),
                      'failures':0},indent=2))

if __name__=='__main__': main()
