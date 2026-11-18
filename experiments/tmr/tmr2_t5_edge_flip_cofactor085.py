#!/usr/bin/env python3
"""TMR-2/085. Exact single-edge T5 decision flip and cofactor support audit.
Python standard library; imports sibling tmr2_t5_girth_cycle_cert084.py.
"""
from hashlib import sha256
from tmr2_t5_girth_cycle_cert084 import graph,orientation,beat,ac

M1=(0,5,9,13,17,22,6,7,8,37,41,45,49,53,58,61,65,69,74,79,81,25,1,57,73,2,38,54,82,3,39,55,71,4,40,56,72,42,10,11,12,83,26,30,34,23,27,31,35,24,28,32,36,51,33,19,20,52,63,48,44,80,76,84,66,50,75,46,18,21,29,15,62,47,16,43,14,68,60,77,64,67,59,78,70)
M2=(1,0,10,14,18,5,25,29,34,38,6,7,8,54,57,62,66,71,73,78,82,21,37,53,77,22,2,58,74,23,3,59,75,24,4,60,76,9,67,50,72,41,68,12,11,44,40,52,48,43,39,51,47,17,64,56,70,20,19,26,30,49,35,27,31,79,36,28,65,13,83,33,16,15,84,80,61,46,81,42,69,45,32,55,63)
def sources():
    E=set(graph())
    m1={(u,85+v) for u,v in enumerate(M1)}
    m2={(u,85+v) for u,v in enumerate(M2)}
    assert len(E)==425 and len(m1)==len(m2)==85 and m1.isdisjoint(m2)
    assert m1<=E and m2<=E
    F=sorted(E-m1)
    D=dict(zip(F,orientation(F,202611180906)))
    kept=sorted(set(F)-{(u,85+M2[u]) for u in range(74)})
    assert len(kept)==266 and D[(74,169)]==(169,74)
    no=[D[e] for e in kept]
    yes=[(74,169) if e==(169,74) else e for e in no]
    def sha(arcs):
        src='p t5 170 266\n'+''.join(f'v {i}\n' for i in range(170))+''.join(f'a {a} {b}\n' for a,b in sorted(arcs))
        return sha256(src.encode()).hexdigest()
    assert sha(no)=='c2f751ad23c53d6612a5156178288b24097b26d5866306d700cca4bcad6496cb'
    assert sha(yes)=='56279caf9886d068b82f8e5873f79b7142260aabf1ebe28bd02c42f022734edb'
    return no,yes,[e for e in no if e!=(169,74)]

def solve(arcs,pins):
    degree=[0]*170
    for a,b in arcs:degree[a]+=1;degree[b]+=1
    nodes=0;leaves=0
    def dfs(branch):
        nonlocal nodes,leaves
        nodes+=1
        D=ac(arcs,pins+branch)
        if D is None:leaves+=1;return None
        choice=min((i for i in range(170) if len(D[i])>1),
                   key=lambda i:(len(D[i]),-degree[i],i),default=None)
        if choice is None:
            w=[next(iter(d)) for d in D]
            assert all(beat(w[a],w[b]) for a,b in arcs)
            return w
        for c in sorted(D[choice]):
            w=dfs(branch+[(choice,c)])
            if w is not None:return w
        return None
    witness=dfs([])
    return witness,nodes,leaves

def run():
    no,yes,missing=sources()
    w,n,l=solve(no,[(29,0)])
    assert w is None and n==259 and l==130
    w,n,l=solve(yes,[(0,0)])
    assert w is not None and all(beat(w[a],w[b]) for a,b in yes)
    print('NO 170/266: 259 nodes / 130 contradictory leaves')
    print('YES 170/266: valid original-label witness; search nodes',n)
    support=[]
    for d in range(5):
        w,n,l=solve(missing,[(74,0),(169,d)])
        support.append(int(w is not None))
        print('missing-edge cofactor d=',d,'sat',bool(w),'nodes',n,'leaves',l)
    assert support==[0,1,0,0,0]
    print('PASS cofactor support 0,1,0,0,0; all checks complete')
if __name__=='__main__':run()
