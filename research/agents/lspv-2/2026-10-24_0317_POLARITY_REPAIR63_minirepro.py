#!/usr/bin/env python3
"""POLARITY-REPAIR63 standard-library source audit. Run from repo root.
UNSAT(U) is imported from DOECKER-CORE-CERT61, not proved by this script.
"""
import ast,collections,hashlib,json
from pathlib import Path
SOURCE=Path("research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt")
HEX="39a2b53c16ab15bc16ab15ca4b9715c4faa7143d31b0f26598"
EXPECTED="4ed9031a7a1b1fa9fcb752f9feece1ea7201df6b610059b90793517ecd874001"
def load():
    s="\n".join(l for l in SOURCE.read_text().splitlines() if l.strip() and not l.startswith("#"))
    return [tuple(c) for c in ast.literal_eval(s)]
def verify(F):
    assert len(F)==264
    assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in F)
    assert len({tuple(sorted(map(abs,c))) for c in F})==264
    t=collections.Counter(l for c in F for l in c)
    assert all(t[v]==t[-v]==2 for v in range(1,199))
def sat(c,a): return any(bool(a[abs(x)])==(x>0) for x in c)
def hk(F):
    n=198;m=len(F)
    adj=[[(abs(x)-1)*2+j for x in c for j in (0,1)] for c in F]
    left=[-1]*m;right=[-1]*(2*n);dist=[0]*m;inf=m+1
    def bfs():
        from collections import deque
        q=deque();found=False
        for v in range(m):
            if left[v]<0:dist[v]=0;q.append(v)
            else:dist[v]=inf
        while q:
            v=q.popleft()
            for r in adj[v]:
                z=right[r]
                if z<0:found=True
                elif dist[z]==inf:dist[z]=dist[v]+1;q.append(z)
        return found
    def dfs(v):
        for r in adj[v]:
            z=right[r]
            if z<0 or (dist[z]==dist[v]+1 and dfs(z)):
                left[v]=r;right[r]=v;return True
        dist[v]=inf;return False
    while bfs():
        for v in range(m):
            if left[v]<0:dfs(v)
    assert all(v>=0 for v in left)
    return [next(j for j,x in enumerate(F[i]) if abs(x)==r//2+1) for i,r in enumerate(left)]
def conflicts(F,s):
    use=collections.defaultdict(list)
    for i,j in enumerate(s):use[abs(F[i][j])].append((i,j,F[i][j]))
    assert all(len(a)<=2 for a in use.values())
    return {v:a for v,a in use.items() if len({x>0 for _,_,x in a})==2},use
def repair(F,s):
    bad,use=conflicts(F,s);G=[list(c) for c in F];sw=[]
    for v,a in sorted(bad.items()):
        q=next((i,j) for i,j,x in a if x<0)
        used={(i,j) for i,j,_ in a}
        p=next((i,j) for i,c in enumerate(F) for j,x in enumerate(c)
               if x==v and (i,j) not in used)
        G[q[0]][q[1]]=v;G[p[0]][p[1]]=-v
        sw.append((v,q,p))
    G=[tuple(c) for c in G];verify(G)
    no_bad,use2=conflicts(G,s);assert not no_bad
    assignment=[0]*199
    for v,a in use2.items():assignment[v]=int(a[0][2]>0)
    assert all(sat(c,assignment) for c in G)
    return G,sw
def main():
    U=load();verify(U)
    digest=hashlib.sha256(json.dumps(U,separators=(",",":")).encode()).hexdigest()
    assert digest==EXPECTED
    V=[list(c) for c in U];V[3][1]=3;V[13][0]=-3
    V=[tuple(c) for c in V];verify(V)
    b=format(int(HEX,16),"0198b");a=[0]+[int(x) for x in b]
    assert [i for i,c in enumerate(U) if not sat(c,a)]==[3]
    assert all(sat(c,a) for c in V)
    s=[next(j for j,x in enumerate(c) if (a[abs(x)]==1)==(x>0)) for c in V]
    assert not conflicts(V,s)[0]
    old_bad,_=conflicts(U,s);assert set(old_bad)=={3}
    repaired,swaps=repair(U,s)
    assert repaired==V and len(swaps)==1
    arbitrary=hk(U)
    edited,changes=repair(U,arbitrary)
    assert len(changes)==42 and all(sat(c,[0]+[int(any(x>0 for i,j,x in conflicts(edited,arbitrary)[1].get(v,[]))) for v in range(1,199)]) for c in edited)
    print(json.dumps({"n":198,"m":264,"N_bits":15870,"source_digest":digest,
      "source_unsat":"imported DOECKER-CORE-CERT61","repaired_sat_witness":True,
      "nearest_neighbor_conflicts":len(swaps),"arbitrary_matching_conflicts":len(changes),
      "failure_count":0},indent=2))
if __name__=="__main__":main()
