#!/usr/bin/env python3
"""Standalone compact fixed-T5 pinning verifier; Python standard library."""
import hashlib,json,sys
S={1,3}
def sat(n,E,pin={}):
    d=[31]*n
    for v,c in pin.items():d[v]=1<<c
    def vals(m):return [i for i in range(5) if m>>i&1]
    def dfs(x):
        while True:
            changed=False
            for u,v in E:
                a,b=x[u],x[v]
                aa=sum(1<<i for i in vals(a) if any((j-i)%5 in S for j in vals(b)))
                bb=sum(1<<j for j in vals(b) if any((j-i)%5 in S for i in vals(a)))
                if not aa or not bb:return None
                if aa!=a or bb!=b:x[u],x[v]=aa,bb;changed=True
            if not changed:break
        multi=[i for i in range(n) if x[i].bit_count()>1]
        if not multi:return [vals(z)[0] for z in x]
        v=min(multi,key=lambda i:x[i].bit_count())
        for c in vals(x[v]):
            y=x.copy();y[v]=1<<c
            sol=dfs(y)
            if sol is not None:return sol
        return None
    z=dfs(d)
    assert z is None or (all((z[v]-z[u])%5 in S for u,v in E) and all(z[v]==c for v,c in pin.items()))
    return z

def h9():
    E=[]; paths=[];v=2
    for word in ('BBB','FBB','FFF','BB'):
        vs=[0]
        for _ in word[:-1]:vs.append(v);v+=1
        vs.append(1);idx=[]
        for (u,w),direction in zip(zip(vs,vs[1:]),word):
            idx.append(len(E));E.append((u,w) if direction=='F' else (w,u))
        paths.append((word,vs,idx))
    return v,E,paths

def threads(n,E):
    adj=[set() for _ in range(n)]; ix={frozenset(a):i for i,a in enumerate(E)}
    for u,v in E:adj[u].add(v);adj[v].add(u)
    B={v for v in range(n) if len(adj[v])>2}; seen=set();out=[]
    for u in sorted(B):
        for a in sorted(adj[u]):
            if ix[frozenset((u,a))] in seen:continue
            seq=[u,a];prev=u;cur=a
            while cur not in B:
                nxt=next(x for x in adj[cur] if x!=prev)
                seq.append(nxt);prev,cur=cur,nxt
            idx=[ix[frozenset((x,y))] for x,y in zip(seq,seq[1:])]
            seen.update(idx)
            word=''.join('F' if E[i]==(x,y) else 'B' for i,(x,y) in zip(idx,zip(seq,seq[1:])))
            out.append((word,seq,idx))
    assert len(seen)==len(E)
    return out

def check(path):
    n,E,p=h9()
    assert n==9 and len(E)==11 and sat(n,E,{0:0}) is None
    for j in range(len(E)):
        assert sat(n,E[:j]+E[j+1:],{0:0}) is not None
    raw=open(path,'rb').read()
    assert hashlib.sha256(raw).hexdigest()=='0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac'
    rows=[s.split() for s in raw.decode().splitlines()]
    n,m=map(int,rows[0][2:])
    E=[(int(r[1]),int(r[2])) for r in rows[1:] if r[0]=='a']
    assert n==33 and m==44 and sat(n,E,{0:0}) is None
    found=[];tests=0
    for word,vs,ix in threads(n,E):
        if len(word)!=3:continue
        u,v=vs[0],vs[-1];wanted=(word.count('B')+1)%5
        for j in ix:
            rem=E[:j]+E[j+1:]
            feasible=[d for d in range(5) if sat(n,rem,{u:0,v:d}) is not None]
            a,b=E[j]
            missing=[d for d in range(5) if sat(n,rem,{a:0,b:d}) is not None]
            assert feasible==[wanted] and missing==[0,2,4],(j,feasible,missing)
            tests+=10
        found.append(dict(word=word,u=u,v=v,forced_delta=wanted))
    assert len(found)==4 and tests==120
    return dict(H9_edge_deletions=11,H33_SHA256=hashlib.sha256(raw).hexdigest(),
                H33_long_threads=found,independent_fixed_endpoint_queries=tests)
if __name__=='__main__':
    print(json.dumps(check(sys.argv[1]),indent=2))
