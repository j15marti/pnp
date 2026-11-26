"""P3FCG06, deterministic source/common-scaffold tests, Python+NetworkX."""
import itertools as it, json, networkx as nx, random

def incidence(T,n):
    G=nx.Graph(); G.add_nodes_from((c,v) for c in range(3) for v in range(n)); G.add_edges_from((('t',j),(c,v)) for j,t in enumerate(T) for c,v in enumerate(t)); return G

def matching(L,R,E):
    L=list(L); R=list(R); G=nx.Graph(); A=[(0,x) for x in L]; B=[(1,y) for y in R]; G.add_nodes_from(A+B); G.add_edges_from(((0,x),(1,y)) for x,y in E)
    M=nx.algorithms.bipartite.maximum_matching(G,top_nodes=A)
    return {x:M[(0,x)][1] for x in L} if all((0,x) in M for x in L) else None

def verify(T,n,W):
    return len(W)==n and all(sorted(t[c] for t in W)==list(range(n)) for c in range(3)) and set(W)<=set(T)

def brute(T,n):
    def go(rem, W):
        if not rem[0]: return W
        a=min(rem[0]);
        for t in T:
            if t[0]==a and all(t[c] in rem[c] for c in range(3)):
                r=go([rem[c]-{t[c]} for c in range(3)],W+[t])
                if r is not None:return r
        return None
    return go([set(range(n)) for _ in range(3)],[])

def closure(T,n):
    live=set(T); used=[set() for _ in range(3)]; W=[]; calls=0
    while True:
        changed=False
        for c in range(3):
            for v in set(range(n))-used[c]:
                S=[t for t in live if t[c]==v]
                if not S:return None,None,calls
                if len(S)==1:
                    t=S[0]; W.append(t)
                    for d in range(3):used[d].add(t[d])
                    live={u for u in live if all(u[d]!=t[d] for d in range(3))};changed=True;break
            if changed:break
        if changed:continue
        for a,b in ((0,1),(0,2),(1,2)):
            L=set(range(n))-used[a];R=set(range(n))-used[b]; E={(t[a],t[b]) for t in live};calls+=1
            if matching(L,R,E) is None:return None,None,calls
            bad=set()
            for x,y in sorted(E):
                calls+=1
                if matching(L-{x},R-{y},[(u,v) for u,v in E if u!=x and v!=y]) is None:bad.add((x,y))
            if bad:live={t for t in live if (t[a],t[b]) not in bad};changed=True
        if not changed:return sorted(live),W,calls

def components(T):
    G=nx.Graph();G.add_edges_from(((0,x),(1,y)) for x,y,z in T)
    return [sorted(t for t in T if (0,t[0]) in C) for C in nx.connected_components(G)]

def cert(C,a):
    b=1-a; L=sorted({t[a] for t in C});R=sorted({t[b] for t in C}); E=set()
    D={u:{t[2] for t in C if t[a]==u} for u in L}; V={(t[a],t[b],t[2]) for t in C}
    for u in L:
        for v in R:
            if all((u,v,z) in V for z in D[u]):E.add((u,v))
    M=matching(L,R,E)
    return (D,M) if M is not None else None

def solve(T,n,order=(0,1,2)):
    assert len(T)==len(set(T)) and all(len(t)==3 and all(0<=v<n for v in t) for t in T)
    assert nx.check_planarity(incidence(T,n))[0]
    live,W,calls=closure(T,n)
    if live is None:return 'NO',None,{'calls':calls,'closure':True}
    if not live:return 'YES',W,{'calls':calls,'closure':True}
    D=[]; lift={};types=[]
    # all three choices of omitted color, each with locally adaptive orientation
    for z in order:
        a,b=[i for i in range(3) if i!=z]; C=[(t[a],t[b],t[z]) for t in live]; comps=components(C); D=[]; lift={};types=[]; fail=False
        for i,K in enumerate(comps):
            P=[cert(K,c) for c in (0,1)];calls+=2; types.append('both' if all(P) else 'left' if P[0] else 'right' if P[1] else 'none')
            if not any(P):fail=True;break
            side=0 if P[0] else 1; labels,M=P[side]
            for u,S in labels.items():
                D.append(((i,u),S))
                for v in S:
                    q=[0]*3;q[a],q[b]=(u,M[u]) if side==0 else (M[u],u);q[z]=v;lift[((i,u),v)]=tuple(q)
        if fail:continue
        calls+=1; R=set(range(n))-{t[z] for t in W};A=matching([u for u,S in D],R,[(u,v) for u,S in D for v in S])
        if A is None:return 'NO',None,{'calls':calls,'lane':z,'types':types,'closure':False}
        ans=W+[lift[(u,v)] for u,v in A.items()];assert verify(T,n,ans)
        return 'YES',ans,{'calls':calls,'lane':z,'types':types,'closure':False}
    return 'UNKNOWN',None,{'calls':calls,'closure':False}

def ring(k,off=0,rev=False):
    T=[]
    for i in range(k):T += [(i,i,i),(i,i,k+i),(i,(i+1)%k,i+(i%2)*k)]
    j=k
    for side in (0,1):
        for i in range(0,k,2):
            T += [(j,j,side*k+i),(j,j,side*k+i+1)];j+=1
    return [(off+(y if rev else x),off+(x if rev else y),off+z) for x,y,z in T]

def mixed(k):
    A=ring(k);B=ring(k,2*k,True); A[3*k+1]=(k,k,2*k+1); B[3*k+1]=(3*k,3*k,1); return A+B

def main():
    U=[tuple(map(int,x)) for x in '000 002 010 011 021 022 100 101 111 201 202 221'.split()];V=U+[(1,1,0)]
    result={'peer':[], 'scale':[], 'random':{}}
    for T in (U,V):
        d,W,info=solve(T,3); truth=brute(T,3) is not None;assert d=='UNKNOWN' or (d=='YES')==truth
        result['peer'].append({'m':len(T),'decision':d,'truth':truth,**info})
    for k in (2,4,8,16,32,64):
        T=mixed(k);n=4*k;assert nx.is_connected(incidence(T,n)); d,W,info=solve(T,n,order=(2,0,1));assert d=='YES' and verify(T,n,W);assert 'left' in info['types'] and 'right' in info['types'];assert not info['closure']
        result['scale'].append({'k':k,'n':n,'m':len(T),'decision':d,'central_local_masks_each':str(2**k), 'left':info['types'].count('left'),'right':info['types'].count('right'),'both':info['types'].count('both'),'calls':info['calls']})
    rng=random.Random(20261125); counts={}; examples={}
    for i in range(500):
        n=rng.choice((2,3,4)); allT=list(it.product(range(n),repeat=3));T=[];rng.shuffle(allT)
        for t in allT[:rng.randint(n,min(3*n+2,len(allT)))]:
            if nx.check_planarity(incidence(T+[t],n))[0]:T.append(t)
        d,W,info=solve(T,n); truth=brute(T,n) is not None;assert d=='UNKNOWN' or (d=='YES')==truth
        if d=='YES':assert verify(T,n,W)
        key=f'{d}/truth={truth}/closure={info["closure"]}';counts[key]=counts.get(key,0)+1
        if key not in examples:examples[key]=T
    result['random']={'counts':counts,'examples':examples};print(json.dumps(result,indent=2))
if __name__=='__main__':main()
