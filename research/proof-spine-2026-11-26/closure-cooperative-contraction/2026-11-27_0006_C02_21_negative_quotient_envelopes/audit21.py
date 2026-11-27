"""Independent sequential profile DP; checks negative soundness and nested projections."""
from itertools import product
from random import Random
from hashlib import sha256
import json

def solve(groups,mask,target):
    states={0:(0,0)}
    for group in groups:
        projected={}
        for x in group:
            k=x&mask
            a,b=projected.get(k,(target,0))
            projected[k]=(a&x,b|x)
        nxt={}
        for x,(a,b) in states.items():
            for y,(c,d) in projected.items():
                if a&c:continue
                key=x^y
                l,h=nxt.get(key,(target,0))
                nxt[key]=(l&(a|c),h|(b|d))
        states=nxt
    return target&mask in states and states[target&mask][1]==target

def direct(groups,target):
    for xs in product(*groups):
        seen=0
        for x in xs:
            if seen&x:break
            seen|=x
        else:
            if seen==target:return True
    return False

def main():
    rng=Random(2611272102);cases=600;checks=positive=loose=0
    for _ in range(cases):
        n=rng.randrange(2,5);target=(1<<(2*n))-1
        groups=[sorted({(1<<rng.randrange(n))|(1<<(n+rng.randrange(n))) for _ in range(rng.randrange(1,5))}) for _ in range(n)]
        yes=direct(groups,target);positive+=yes;prior=True
        order=list(range(2*n));rng.shuffle(order);mask=0
        for k in range(2*n+1):
            ok=solve(groups,mask,target)
            assert not yes or ok
            assert prior or not ok
            if k==2*n:assert ok==yes
            loose+=ok and not yes;checks+=1;prior=ok
            if k<2*n:mask|=1<<order[k]
    # All three pairwise projections admit a matching, but no cover.
    groups=[[0b0101,0b1010],[0b1001,0b0110]]
    assert not direct(groups,15) and solve(groups,0,15) and not solve(groups,15,15)
    # Union is not a safe substitute for the mandatory intersection.
    assert direct([[1,2],[2]],3) and solve([[1,2],[2]],0,3)
    print(json.dumps(dict(cases=cases,checks=checks,positive_controls=positive,loose_negative_checks=loose,q2='PASS',wrong_must='PASS'),sort_keys=True))
if __name__=='__main__':main()
