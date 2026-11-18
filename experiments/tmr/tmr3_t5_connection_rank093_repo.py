#!/usr/bin/env python3
"""TMR-3/093: source-derived affine-gadget recognition and sharp connection-rank witnesses.
Finite checks are COMPUTATIONAL; no unrestricted SAT time/space lower bound.
"""
from collections import deque
from itertools import product

def t5(a,b):
    return (b-a)%5 in (1,3)

def construct(q, patterns):
    """Gluing of labeled q-terminal sources B_alpha; terminals are 0..q-1."""
    edges=set()
    next_v=q
    for alpha in patterns:
        assert len(alpha)==q-1
        for terminal,d in enumerate(alpha,1):
            prev=0
            length=d if d else 5
            for j in range(length):
                v=terminal if j+1==length else next_v
                if j+1!=length:
                    next_v+=1
                w=next_v
                next_v+=1
                edges.update(((prev,v),(prev,w),(w,v)))
                prev=v
    return next_v,edges

def exact_count(n,source):
    """Recognize each genuine 3-edge triangle, then solve source-derived +1 constraints.
    None means not a member of this authenticated family. General fallback required.
    """
    E=set(source)
    if any(u<0 or v<0 or u>=n or v>=n or u==v for u,v in E):
        return None
    ins=[set() for _ in range(n)]
    outs=[set() for _ in range(n)]
    for u,v in E:
        ins[v].add(u)
        outs[u].add(v)
    private={}
    for w in range(n):
        if len(ins[w])==len(outs[w])==1:
            u=next(iter(ins[w]))
            v=next(iter(outs[w]))
            if (u,v) in E:
                private[w]=(u,v)
    if any(u in private or v in private for u,v in private.values()):
        return None
    direct=set(private.values())
    covered=set(direct)
    for w,(u,v) in private.items():
        covered.add((u,w))
        covered.add((w,v))
    if covered != E:
        return None
    active=set(range(n))-set(private)
    adj={u:[] for u in active}
    for u,v in direct:
        adj[u].append((v,1))
        adj[v].append((u,-1))
    color={}
    components=0
    for root in sorted(active):
        if root in color:
            continue
        components+=1
        color[root]=0
        todo=deque((root,))
        while todo:
            u=todo.popleft()
            for v,delta in adj[u]:
                val=(color[u]+delta)%5
                if v in color:
                    if color[v]!=val:
                        return 0
                else:
                    color[v]=val
                    todo.append(v)
    witness=dict(color)
    for w,(u,v) in private.items():
        witness[w]=(color[u]+3)%5
    assert all(t5(witness[u],witness[v]) for u,v in E)
    return 5**components

def audit():
    checks=0
    for a in range(5):
        n,E=construct(2,[(a,)])
        assert exact_count(n,E)==5
        checks+=1
        for b in range(5):
            n,E=construct(2,[(a,),(b,)])
            assert exact_count(n,E)==(5 if a==b else 0)
            checks+=1
    for a in product(range(5),repeat=2):
        n,E=construct(3,[a,a])
        assert exact_count(n,E)==5
        checks+=1
    for q in (4,10,40):
        alpha=tuple((i*3+1)%5 for i in range(q-1))
        n,E=construct(q,[alpha,alpha])
        assert exact_count(n,E)==5
        checks+=1
        beta=list(alpha)
        beta[0]=(beta[0]+1)%5
        n,E=construct(q,[alpha,tuple(beta)])
        assert exact_count(n,E)==0
        checks+=1
    for n,E in ((2,{(0,1)}),(2,{(0,1),(1,0)}),
                (1,{(0,0)}),(3,{(0,1),(1,2),(2,0)})):
        assert exact_count(n,E) is None
        checks+=1
    q=40
    a=tuple((i*3+1)%5 for i in range(q-1))
    n,E=construct(q,[a,a])
    print({"checks":checks,"failures":0,"q40_vertices":n,"q40_arcs":len(E),
           "q40_count":exact_count(n,E),"full_connection_rank":5**(q-1)})
if __name__=="__main__":
    audit()
