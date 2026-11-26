"""Exact extracted C05-07 executed Rado augmentation core."""
from collections import deque,Counter

def reduce_vec(v,b):
    a=0
    for p,(w,c) in sorted(b.items(),reverse=True):
        if (v>>p)&1:v^=w;a^=c
    return v,a

def insert(v,c,b):
    v,a=reduce_vec(v,b);c^=a
    if not v:return not c
    b[v.bit_length()-1]=(v,c);return True

def rado(G):
    """Rado augmentations, using all 3 nonzero forms of each forbidden plane.
    Returns maximal independent representatives, reachable deficient core, and counters.
    G keyed by plane (u,v), forbidden bit pair (a,b).
    """
    keys=list(G);V=[(u,v,u^v) for u,v in keys];I={};st=Counter()
    while True:
        basis={}
        for j,v in I.items():assert insert(v,1<<j,basis)
        parent={j:None for j in range(len(keys)) if j not in I};Q=deque(parent);end=None
        while Q and end is None:
            j=Q.popleft()
            for v in V[j]:
                st['vector_probes']+=1;w,c=reduce_vec(v,basis)
                if w:end=(j,v);break
                while c:
                    bit=c&-c;c^=bit;k=bit.bit_length()-1
                    if k not in parent:parent[k]=(j,v);Q.append(k)
        if end is None:
            core=set(parent);bs={}
            for j in core & I.keys():assert insert(I[j],0,bs)
            assert all(not reduce_vec(v,bs)[0] for j in core for v in V[j])
            assert len(bs)==len(core & I.keys());st.update(core_factors=len(core),core_rank=len(bs),represented=len(I),factors=len(keys))
            return {keys[j]:v for j,v in I.items()},{keys[j] for j in core},dict(st)
        j,v=end
        while True:
            I[j]=v
            if parent[j] is None:break
            j,v=parent[j]
        st['augmentations']+=1

