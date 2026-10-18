#!/usr/bin/env python3
"""Small independent control for PROMISE-BOUNDARY-CAPACITY12.
The full 13,312-case and adaptive test suite is distributed separately.
"""
from itertools import product,combinations

def ham(a,b): return (a^b).bit_count()

def audit(s,funcs,C):
    q=len(funcs)
    d=min(ham(x,y) for x,y in combinations(C,2))
    outputs=[sum(f(z)<<i for i,f in enumerate(funcs)) for z in range(1<<s)]
    heavy=set()
    for bit in range(s):
        touched=sum(any(f(z)!=f(z^(1<<bit)) for z in range(1<<s))
                    for f in funcs)
        if touched>=d: heavy.add(bit)
    good=[z for z,out in enumerate(outputs) if out in C]
    if not good:return 0
    bad=(1<<s)-len(good)
    labels={outputs[z] for z in good}
    assert len(labels)<=(1<<len(heavy))+bad
    for z in good:
        for bit in range(s):
            if bit not in heavy and (z^(1<<bit)) in good:
                assert outputs[z]==outputs[z^(1<<bit)]
    return 1

def main():
    s,q=3,3
    fs=[lambda z:0,lambda z:1]
    for i in range(s):
        fs.extend([lambda z,i=i:(z>>i)&1,
                   lambda z,i=i:1^((z>>i)&1)])
    codes=[]
    for mask in range(1<<(1<<q)):
        C=[u for u in range(1<<q) if (mask>>u)&1]
        if len(C)>1 and min(ham(x,y) for x,y in combinations(C,2))>=2:
            codes.append(C)
    checked=0
    nonempty=0
    for f in product(fs,repeat=q):
        for C in codes:
            checked+=1
            nonempty+=audit(s,f,C)
    assert checked==13312 and nonempty==10312
    print("PASS",checked,"pairs;",nonempty,"nonempty promises")
if __name__=="__main__": main()
