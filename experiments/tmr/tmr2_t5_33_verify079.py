#!/usr/bin/env python3
"""Independent stdlib T5 refutation checker for TMR-2/079.
Usage: python tmr2_t5_33_verify079.py example.t5 evidence.json.gz.b64
The evidence includes the entire refutation tree and 44 edge-deletion witnesses.
"""
import base64,gzip,hashlib,json,sys
from collections import Counter,deque

K=5
R=lambda a,b:(b-a)%5 in (1,3)

def read_source(path):
    raw=open(path,'rb').read()
    assert raw.isascii() and raw.endswith(b'\n') and b'\r' not in raw
    lines=raw.decode().splitlines();hdr=lines[0].split(' ')
    assert len(hdr)==4 and hdr[:2]==['p','t5']
    n,m=map(int,hdr[2:]);assert n==33 and m==44 and len(lines)==1+n+m
    assert lines[1:1+n]==[f'v {i}' for i in range(n)]
    E=[]
    for line in lines[n+1:]:
        tag,u,v=line.split(' ');assert tag=='a'
        u,v=int(u),int(v);assert 0<=u<n and 0<=v<n and u!=v
        E.append((u,v))
    assert E==sorted(set(E)) and all((v,u) not in E for u,v in E)
    assert raw.decode()==f'p t5 {n} {m}\n'+''.join(f'v {i}\n' for i in range(n))+''.join(f'a {u} {v}\n' for u,v in E)
    return n,E,hashlib.sha256(raw).hexdigest()

def domains(n,E,assignments):
    D=[set(range(5)) for _ in range(n)]
    for v,c in assignments:D[v].intersection_update({c})
    if any(not d for d in D):return None
    while True:
        changed=False
        for u,v in E:
            A={a for a in D[u] if any(R(a,b) for b in D[v])}
            B={b for b in D[v] if any(R(a,b) for a in A)}
            if not A or not B:return None
            if A!=D[u]:D[u]=A;changed=True
            if B!=D[v]:D[v]=B;changed=True
        if not changed:return D

def proof_check(n,E,tree):
    ct=Counter()
    def visit(node,pins):
        ct['nodes']+=1;D=domains(n,E,pins)
        if node=='X':
            assert D is None,('false conflict',pins)
            ct['conflicts']+=1;return
        assert D is not None and set(node)=={'v','branches'}
        v=node['v'];assert isinstance(v,int) and 0<=v<n and len(D[v])>=2
        children=node['branches'];assert set(children)=={str(c) for c in D[v]},('incomplete branch',v,pins)
        ct['splits']+=1
        for c in sorted(D[v]):visit(children[str(c)],pins+[(v,c)])
    # Every T5 solution can be rotated so that x_0=0.
    assert all(R(a,b)==R((a+t)%5,(b+t)%5) for a in range(5) for b in range(5) for t in range(5))
    visit(tree,[(0,0)])
    return dict(ct)

def graph(n,E):
    A=[set() for _ in range(n)]
    for u,v in E:A[u].add(v);A[v].add(u)
    def bfs(s,excluded=None):
        q=deque([s]);d={s:0}
        while q:
            u=q.popleft()
            for v in A[u]:
                if excluded and frozenset((u,v))==excluded:continue
                if v not in d:d[v]=d[u]+1;q.append(v)
        return d
    side={0:0};q=deque([0])
    while q:
        u=q.popleft()
        for v in A[u]:
            if v in side:assert side[v]!=side[u]
            else:side[v]=1-side[u];q.append(v)
    assert len(side)==n
    girth=min(bfs(u,frozenset((u,v)))[v]+1 for u,v in E)
    assert girth==8
    return A,side,[bfs(u) for u in range(n)]

def pc(n,E):
    ALL=(1<<25)-1
    EQ=sum(1<<(6*a) for a in range(5))
    POS=sum(1<<(5*a+b) for a in range(5) for b in range(5) if R(a,b))
    NEG=sum(1<<(5*b+a) for a in range(5) for b in range(5) if R(a,b))
    P=[[EQ if i==j else ALL for j in range(n)] for i in range(n)]
    for u,v in E:P[u][v]&=POS;P[v][u]&=NEG
    removed=0;sweeps=0
    while True:
        changed=False;sweeps+=1
        for i in range(n):
            for h in range(n):
                for j in range(n):
                    X=P[i][h];Y=P[h][j];support=0
                    for a in range(5):
                        for c in range(5):
                            if any((X>>(5*a+b))&1 and (Y>>(5*b+c))&1 for b in range(5)):
                                support|=1<<(5*a+c)
                    Z=P[i][j]&support
                    if Z!=P[i][j]:removed+=(P[i][j]^Z).bit_count();P[i][j]=Z;changed=True
        if not changed:break
        assert sweeps<=10
    return P,removed,sweeps

def main(source,packed):
    n,E,src_sha=read_source(source)
    evidence=json.loads(gzip.decompress(base64.b64decode(open(packed,'rb').read())))
    assert evidence['source_sha256']==src_sha
    proof_stats=proof_check(n,E,evidence['proof_tree'])
    assert proof_stats==evidence['NO_proof_nodes']
    assert proof_stats=={'nodes':73,'conflicts':37,'splits':36}
    W=evidence['edge_deletion_witnesses'];assert len(W)==len(E)
    for idx,labels in enumerate(W):
        assert len(labels)==n and all(type(c)==int and 0<=c<5 for c in labels)
        assert all(R(labels[u],labels[v]) for j,(u,v) in enumerate(E) if j!=idx)
        u,v=E[idx];assert not R(labels[u],labels[v])
    A,side,dist=graph(n,E)
    YES=sorted((u,v) if side[u]==0 else (v,u) for u,v in (tuple(sorted(edge)) for edge in E))
    labels=evidence['YES_original_witness']
    assert len(labels)==n and all(R(labels[u],labels[v]) for u,v in YES)
    for arcs in (E,YES):
        for v in range(n):
            for c in range(5):assert domains(n,arcs,[(v,c)]) is not None
        P,deleted,sweeps=pc(n,arcs)
        assert deleted==3040 and sweeps==3
        assert sum(mask.bit_count() for row in P for mask in row)==22205
        for u in range(n):
            for v in range(n):
                assert P[u][v].bit_count()==(5 if u==v else 5*min(dist[u][v]+1,5))
    print(json.dumps({'status':'VERIFIED','n':n,'m':len(E),'girth':8,'source_sha256':src_sha,'UNSAT_proof_nodes':proof_stats,'edge_deletion_SAT_witnesses':len(W),'SAC_trials':330,'PC_retained_entries_per_orientation':22205,'P_vs_NP':'OPEN'},sort_keys=True))
if __name__=='__main__':
    assert len(sys.argv)==3,'usage: verify.py source.t5 evidence.json.gz.b64'
    main(*sys.argv[1:])
