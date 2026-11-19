#!/usr/bin/env python3
"""Source-bound critical T5 thread-identity replay. No external dependencies.

Run from j15marti/pnp checkout: python experiments/t5/lspv3_critical_thread_identity_20261118.py
This checks original-source SAT deletion models, not a SAT-time lower bound.
"""
import pathlib, hashlib, collections, json

ROOT=pathlib.Path(__file__).resolve().parents[2]
SOURCES={
 "H9":("research/agents/lspv-3/certificates/2026-11-18_LSPV3_H9_BLOCK_COVER.t5",
       "15625c3bec0f5281a6a943f42b611995d9607cceec71c52e544bcd48f099d1d2"),
 "H33":("research/agents/tmr-2/certificates/2026-11-18_0112_TMR2_T5_GIRTH8_33_NO079.t5",
       "0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac")
}
R=lambda a,b:(b-a)%5 in (1,3)

def source(p,expected):
    data=(ROOT/p).read_bytes()
    assert hashlib.sha256(data).hexdigest()==expected,(p,"source hash changed")
    lines=data.decode("ascii").splitlines()
    h=lines[0].split();assert h[:2]==["p","t5"]
    n,m=map(int,h[2:])
    assert lines[1:1+n]==[f"v {i}" for i in range(n)]
    e=[]
    for s in lines[1+n:]:
        t=s.split();assert t[0]=="a" and len(t)==3
        u,v=map(int,t[1:]);assert 0<=u<n and 0<=v<n and u!=v
        e.append((u,v))
    assert len(e)==m and len({frozenset(t) for t in e})==m
    return n,e

def threads(n,e):
    a=[set() for _ in range(n)]
    for u,v in e:a[u].add(v);a[v].add(u)
    B={i for i in range(n) if len(a[i])>=3}
    assert B
    edgeid={frozenset(t):j for j,t in enumerate(e)}
    done=set();out=[]
    for u in sorted(B):
        for v in sorted(a[u]):
            if frozenset((u,v)) in done:continue
            seq=[u,v];done.add(frozenset((u,v)));prev,cur=u,v
            while cur not in B:
                assert len(a[cur])==2
                nxt=next(i for i in a[cur] if i!=prev)
                assert frozenset((cur,nxt)) not in done
                done.add(frozenset((cur,nxt)))
                seq.append(nxt);prev,cur=cur,nxt
            out.append((seq,[edgeid[frozenset(t)] for t in zip(seq,seq[1:])]))
    assert len(done)==len(e)
    return sorted(B),out

def relation(path,e):
    arcs=set(e);q={(x,x) for x in range(5)}
    for u,v in zip(path,path[1:]):
        forward=(u,v) in arcs
        assert forward or (v,u) in arcs
        q={(a,c) for a,b in q for c in range(5) if R(b,c) if forward} if forward else {
           (a,c) for a,b in q for c in range(5) if R(c,b)}
    return q

def solve(n,e,drop=-1):
    edges=[v for i,v in enumerate(e) if i!=drop]
    dom=[31]*n;dom[0]=1
    count=[0]
    def dfs(d):
        count[0]+=1
        changed=True
        while changed:
            changed=False
            for u,v in edges:
                A=sum(1<<a for a in range(5) if d[u]>>a&1 and
                      any((d[v]>>b&1) and R(a,b) for b in range(5)))
                if A==0:return None
                B=sum(1<<b for b in range(5) if d[v]>>b&1 and
                      any((A>>a&1) and R(a,b) for a in range(5)))
                if B==0:return None
                if A!=d[u]:d[u]=A;changed=True
                if B!=d[v]:d[v]=B;changed=True
        un=[i for i in range(n) if d[i].bit_count()>1]
        if not un:
            colors=[v.bit_length()-1 for v in d]
            assert all(R(colors[u],colors[v]) for u,v in edges)
            return colors
        u=min(un,key=lambda i:(d[i].bit_count(),i))
        for a in range(5):
            if d[u]>>a&1:
                d2=d[:];d2[u]=1<<a
                ans=dfs(d2)
                if ans is not None:return ans
        return None
    return dfs(dom),count[0]

def replay(label,p,sha):
    n,e=source(p,sha);B,T=threads(n,e)
    s=[relation(seq,e) for seq,ids in T]
    assert all(len(seq)<=4 for seq,ids in T)
    full,_=solve(n,e)
    assert full is None
    used=set()
    for i,(seq,ids) in enumerate(T):
        model,_=solve(n,e,ids[0])
        assert model is not None
        row=tuple(model[v] for v in B)
        assert row not in used
        used.add(row)
        bad=[j for j,(path,_) in enumerate(T)
             if (model[path[0]],model[path[-1]]) not in s[j]]
        assert bad==[i],(i,bad)
    for eid in range(len(e)):
        model,_=solve(n,e,eid)
        assert model is not None
        assert all(R(model[u],model[v]) for j,(u,v) in enumerate(e) if j!=eid)
    return {"source":label,"n":n,"arcs":len(e),"branches":len(B),
            "threads":len(T),"unique_bad_rows":len(used),
            "deleted_edges_verified":len(e),"rank":len(T),
            "sha256":sha}

if __name__=="__main__":
    print(json.dumps([replay(name,*info) for name,info in SOURCES.items()],indent=2))
