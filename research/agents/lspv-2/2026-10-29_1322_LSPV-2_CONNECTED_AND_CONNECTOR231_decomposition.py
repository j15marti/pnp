#!/usr/bin/env python3
"""Independent certified primal tree-decomposition for connected AND joins.
For each literal clause, its three source variable names must share a bag.
No complexity claim beyond fixed 36-variable bags; source SAT not solved here.
"""
from pathlib import Path
import importlib.util,json
S=importlib.util.spec_from_file_location('C',Path(__file__).with_name('2026-10-29_1322_LSPV-2_CONNECTED_AND_CONNECTOR231_repro.py'))
C=importlib.util.module_from_spec(S);S.loader.exec_module(C)

def verify(cs,bags,edges):
    n=len(bags)
    assert len(edges)==n-1
    adj=[set() for _ in bags]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    reach={0};todo=[0]
    while todo:
        for v in adj[todo.pop()]:
            if v not in reach:reach.add(v);todo.append(v)
    assert len(reach)==n
    assert all(any({abs(x) for x in c}<=bag for bag in bags) for c in cs)
    vs={abs(x) for c in cs for x in c}
    for v in vs:
        containing={i for i,bag in enumerate(bags) if v in bag}
        start=next(iter(containing));reach={start};todo=[start]
        while todo:
            for w in adj[todo.pop()]&containing:
                if w not in reach:reach.add(w);todo.append(w)
        assert reach==containing,(v,containing-reach)
    return max(map(len,bags))-1

def build(k):
    H=list(C.G);bH=[set(range(1,16))];eH=[]
    for t in range(1,k):
        K=C.G
        out,_,info=C.join(H,K,mode=t%3)
        nh,nk=info['source_sizes']; ix,iy=info['source_clause_slots'][0][0],info['source_clause_slots'][1][0]
        sourceL={abs(l) for l in H[ix]}
        sourceR={abs(l)+nh for l in K[iy]}
        central=sourceL|sourceR|set(range(nh+nk+1,nh+nk+31))
        assert len(central)==36
        shift=len(bH)
        bags=bH+[set(range(nh+1,nh+16)),central]
        # K source has a one-bag decomposition.
        edges=eH+[(shift,shift+1)]
        anchor=next(i for i,b in enumerate(bH) if sourceL<=b)
        edges.append((anchor,shift+1))
        # Note: sourceR is covered by the shifted K leaf bag; sources are disjoint.
        w=verify(out,bags,edges)
        assert w<=35
        H=out;bH=bags;eH=edges
    return {'k':k,'n':len({abs(l) for c in H for l in c}),
            'bags':len(bH),'edges':len(eH),'max_bag_size':max(map(len,bH)),
            'width_certificate':verify(H,bH,eH),
            'checksum':sum(sum(x) for x in bH),
            'decomposition_verified':True}

if __name__=='__main__':
    print(json.dumps({'certificate_cases':[build(k) for k in (1,2,4,8,16,32)]},indent=2))