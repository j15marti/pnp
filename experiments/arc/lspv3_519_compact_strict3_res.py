"""LSPV-3/519: strict 3-CNF Q_n perfect-matching split and Resolution proof.
Original-source byte/grammar and historical full R_mix341 acceptance remain distinct.
"""
from itertools import product
from collections import Counter
import json


def q4():
    def rec(left,edges):
        if not left: yield edges;return
        a=min(left)
        for k in range(4):
            b=a^(1<<k)
            if b in left:yield from rec(left-{a,b},edges+[(a,b)])
    yield from rec(set(range(16)),[])


def norm(v):
    s=set(v)
    assert 0 not in s and all(-x not in s for x in s)
    return tuple(sorted(s,key=lambda x:(abs(x),x<0)))


def build(n,matching):
    m=1<<(n-1); assert len(matching)==m
    assert sorted(a for e in matching for a in e)==list(range(1<<n))
    src=[];wires=n+1; leaves={};bydir=[0]*n;gadgets=[]
    for a,b in sorted(tuple(sorted(e)) for e in matching):
        diff=a^b; assert diff and diff&(diff-1)==0
        j=diff.bit_length()-1;bydir[j]+=1
        C=norm((i+1)*(1 if (a>>i&1)==0 else -1) for i in range(n) if i!=j)
        if n==4: seq=[C]; aux=[]
        else:
            aux=list(range(wires,wires+n-4));wires+=n-4
            seq=[norm((C[0],C[1],aux[0]))]
            for t in range(1,len(aux)):
                seq.append(norm((-aux[t-1],C[t+1],aux[t])))
            seq.append(norm((-aux[-1],C[-2],C[-1])))
        ids=list(range(len(src),len(src)+len(seq)));src+=seq
        gadgets.append((a,b,C,aux,ids))
    cs=src[:]; steps=[]
    def res(a,b,p):
        assert a<len(cs) and b<len(cs) and p in cs[a] and -p in cs[b]
        result=norm((set(cs[a])-{p})|(set(cs[b])-{-p}))
        steps.append((a,b,p,result));cs.append(result);return len(cs)-1
    for a,b,C,aux,ids in gadgets:
        cur=ids[0]
        for t,p in enumerate(aux): cur=res(cur,ids[t+1],p)
        assert cs[cur]==C
        leaves[a]=leaves[b]=cur
    last=max(range(n),key=lambda j:bydir[j]);order=[i for i in range(n) if i!=last]+[last]
    def tree(depth,assignment):
        if depth==n:return leaves[assignment]
        p=tree(depth+1,assignment);q=tree(depth+1,assignment|(1<<order[depth]))
        v=order[depth]+1
        if v not in cs[p] and -v not in cs[p]:return p
        if v not in cs[q] and -v not in cs[q]:return q
        return res(p,q,v)
    root=tree(0,0);assert cs[root]==()
    used=set();todo=[root]
    while todo:
        u=todo.pop()
        if u in used:continue
        used.add(u)
        if u>=len(src):todo.extend(steps[u-len(src)][:2])
    assert set(range(len(src)))<=used
    charged=sum(u>=len(src) for u in used)
    assert len(src)-1<=charged<=(n-2)*m-1-max(bydir)
    return {'n':n,'clauses':len(src),'inferences':charged,'direction_max':max(bydir),'source':src,'steps':steps,'root':root}


def run():
    counts=Counter(); mats=list(q4()); assert len(mats)==272
    for M in mats:
        r=build(4,M);counts['q4_models']+=1
        counts['q4_q_%s'%r['inferences']]+=1
    for n in range(4,9):
        parallel=[(a,a^1) for a in range(1<<n) if a%2==0]
        r=build(n,parallel)
        assert r['inferences']==r['clauses']-1
        counts['parallel_exact_n_%s'%n]=r['inferences']
    return dict(counts)


if __name__=='__main__': print(json.dumps(run(),sort_keys=True,indent=2))
