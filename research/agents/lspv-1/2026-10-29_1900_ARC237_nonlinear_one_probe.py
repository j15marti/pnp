#!/usr/bin/env python3
"""ARC237: stdlib-only finite reproducer of the nonlinear one-probe theorem.
No claim to decide general SAT. Usage: python 2026-10-29_1900_ARC237_nonlinear_one_probe.py
"""
import json

def bit(x): return x.bit_count() & 1

def model(b):
    r=(b+1).bit_length()-1
    cols=list(range(1,1<<r))+[1]*(b-((1<<r)-1))
    rows=[sum(((c>>j)&1)<<i for i,c in enumerate(cols)) for j in range(r)]
    a=rows[:]; p=[]; k=0
    for i in range(b):
        t=next((j for j in range(k,len(a)) if (a[j]>>i)&1),None)
        if t is None: continue
        a[k],a[t]=a[t],a[k]
        for j in range(len(a)):
            if j!=k and ((a[j]>>i)&1): a[j]^=a[k]
        p.append(i);k+=1
        if k==len(a):break
    K=[]
    for j in range(b):
        if j in p:continue
        x=1<<j
        for row,i in zip(a,p):
            if bit(row&x):x^=1<<i
        assert all(not bit(row&x) for row in rows)
        K.append(x)
    piv={}
    for j,v in enumerate(K):
        coeff=1<<j
        while v:
            t=v.bit_length()-1
            if t not in piv:piv[t]=(v,coeff);break
            u,c=piv[t];v^=u;coeff^=c
        assert v
    return cols,K,piv

def online(a,w,s,cols,piv):
    syn=0
    for i in range(len(cols)):
        if (w>>i)&1:syn^=cols[i]
    probe=cols.index(syn) if syn else None
    residual=w^(1<<probe if probe is not None else 0)
    coeff=0
    while residual:
        t=residual.bit_length()-1
        row,c=piv[t];residual^=row;coeff^=c
    value=bit(coeff&s)
    if probe is not None:value^=(a>>probe)&1
    return value,probe

def oneprobe_ok(fiber,b,w):
    vals={a:bit(a&w) for a in fiber}
    if len(set(vals.values()))<=1:return True
    return any(any(all(vals[a]==(((a>>i)&1)^q) for a in fiber)
                   for q in (0,1)) for i in range(b))

def nonlinear(b,L):
    ns=1<<L;n=1<<b;total=ns**n;good=0
    assert total<=256
    for code in range(total):
        fs=[[] for _ in range(ns)];z=code
        for a in range(n):fs[z%ns].append(a);z//=ns
        if all(oneprobe_ok(f,b,w) for f in fs if f for w in range(n)):
            good+=1
    return {'b':b,'L':L,'preprocessors':total,'oneprobe_valid':good}

def main():
    cases=[];total=0
    for b in range(1,9):
        cols,K,piv=model(b);count=0
        for a in range(1<<b):
            s=sum(bit(row&a)<<j for j,row in enumerate(K))
            for w in range(1<<b):
                v,probe=online(a,w,s,cols,piv)
                assert v==bit(a&w) and (probe is None or 0<=probe<b)
                count+=1
        assert count==4**b
        total+=count
        cases.append({'b':b,'L':len(K),'exact_pairs':count})
    non=[nonlinear(b,L) for b,L in ((2,0),(2,1),(3,0),(3,1))]
    assert [x['oneprobe_valid'] for x in non]==[0,6,0,2]
    assert total==87380
    # Two XOR shares: each leaves both target bits; together target fixed.
    U=[(t,r) for t in (0,1) for r in (0,1)]
    f1=lambda t,r:(t^r)==1
    f2=lambda t,r:r==0
    def distinct(fs):return {t for t,r in U if all(f(t,r) for f in fs)}
    assert list(map(len,[distinct(()),distinct((f1,)),distinct((f2,)),distinct((f1,f2))]))==[2,2,2,1]
    # One realized source bit can shrink candidate log-cardinality from 2 to 0.
    F=(0,4,2,1)
    assert len([a for a in F if a&4])==1
    print(json.dumps({'project':'ARC237','tested_pairs':total,
                      'case_table':cases,'nonlinear_enumeration':non,
                      'synergy_and_pointwise_drop_passed':True,
                      'all_assertions_passed':True},indent=2,sort_keys=True))
if __name__=='__main__':main()
