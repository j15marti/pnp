#!/usr/bin/env python3
"""TMR-4/054: exact min signal-hyperedge cut and #Circuit-SAT factorization.
stdlib only; fixed deterministic seed; no external reads; PYTHONHASHSEED independent.
"""
import json, random, itertools
from collections import deque

REVISION='tmr4-signalcut054.v1'
SEED=202611151452
PRIME=65521

class Circuit:
    def __init__(self,n,gates,name):
        self.n,self.gates,self.name=n,gates,name
        for j,(op,src) in enumerate(gates):
            assert op in ('AND','OR','XOR','NOT')
            assert len(src)==(1 if op=='NOT' else 2)
            assert all(0<=v<n+j for v in src)
    @property
    def V(self): return self.n+len(self.gates)
    def eval(self,bits):
        v=list(bits)
        for op,src in self.gates:
            a=v[src[0]]
            v.append(int(not a) if op=='NOT' else
                     (a & v[src[1]]) if op=='AND' else
                     (a | v[src[1]]) if op=='OR' else
                     (a ^ v[src[1]]))
        return v[-1]

def append(g,op,*src):
    g.append((op,tuple(src)));return CUR_N[0]+len(g)-1
CUR_N=[0]
def example(k,kind):
    n=2*k; CUR_N[0]=n; g=[]
    if kind=='DISJ':
        terms=[append(g,'NOT',append(g,'AND',i,k+i)) for i in range(k)]
        res=terms[0]
        for v in terms[1:]:res=append(g,'AND',res,v)
    elif kind=='EQ':
        terms=[append(g,'NOT',append(g,'XOR',i,k+i)) for i in range(k)]
        res=terms[0]
        for v in terms[1:]:res=append(g,'AND',res,v)
    elif kind=='IP':
        terms=[append(g,'AND',i,k+i) for i in range(k)]
        res=terms[0]
        for v in terms[1:]:res=append(g,'XOR',res,v)
    elif kind=='SEPARABLE':
        ax=0; by=k
        for i in range(1,k):ax=append(g,'XOR',ax,i)
        for i in range(1,k):by=append(g,'XOR',by,k+i)
        res=append(g,'AND',ax,by)
    else: raise ValueError(kind)
    return Circuit(n,g,kind+str(k))

class Flow:
    def __init__(self,n): self.ad=[[] for _ in range(n)]
    def add(self,u,v,c):
        a=[v,c,len(self.ad[v])];b=[u,0,len(self.ad[u])]
        self.ad[u].append(a);self.ad[v].append(b)
    def mincut(self,s,t):
        n=len(self.ad);total=0
        while True:
            dist=[-1]*n;dist[s]=0;dq=deque([s])
            while dq:
                u=dq.popleft()
                for v,c,_ in self.ad[u]:
                    if c and dist[v]<0:dist[v]=dist[u]+1;dq.append(v)
            if dist[t]<0:break
            pos=[0]*n
            def dfs(u,f):
                if u==t:return f
                while pos[u]<len(self.ad[u]):
                    e=self.ad[u][pos[u]];v,c,back=e
                    if c and dist[v]==dist[u]+1:
                        z=dfs(v,min(f,c))
                        if z:e[1]-=z;self.ad[v][back][1]+=z;return z
                    pos[u]+=1
                return 0
            while True:
                z=dfs(s,10**9)
                if not z:break
                total+=z
        seen={s};dq=deque([s])
        while dq:
            u=dq.popleft()
            for v,c,_ in self.ad[u]:
                if c and v not in seen:seen.add(v);dq.append(v)
        return total,seen

def min_signal_cut(C,a):
    assert 0<a<C.n
    fans=[{i} for i in range(C.V)]
    for j,(op,src) in enumerate(C.gates):
        for v in src:fans[v].add(C.n+j)
    n=C.V; S=3*n; T=S+1; f=Flow(3*n+2); INF=n+2
    for v,hyper in enumerate(fans):
        aa=n+2*v;bb=aa+1
        f.add(aa,bb,1)
        for u in sorted(hyper): f.add(u,aa,INF); f.add(bb,u,INF)
    for i in range(a):f.add(S,i,INF)
    for i in range(a,C.n):f.add(i,T,INF)
    r,reach=f.mincut(S,T)
    side=[int(i in reach) for i in range(n)]
    cross=[v for v,h in enumerate(fans) if len({side[u] for u in h})>1]
    assert len(cross)==r,(r,cross)
    return r,side,cross

def brute_cut(C,a):
    n=C.V; g=n-C.n;best=n+1
    fans=[{i} for i in range(n)]
    for j,(_,src) in enumerate(C.gates):
        for v in src:fans[v].add(C.n+j)
    for m in range(1<<g):
        side=[1]*a+[0]*(C.n-a)+[(m>>j)&1 for j in range(g)]
        val=sum(len({side[u] for u in h})>1 for h in fans)
        best=min(val,best)
    return best

def ok_side(C,a,side,cross,z,bits,which):
    # bits is the assignment on this side only; input parity and gates are local.
    zz=dict(zip(cross,z));v={}
    for i in range(C.n):
        if side[i]==which:
            v[i]=bits[i if i<a else i-a]
            if i in zz and zz[i]!=v[i]:return 0
    def get(q):return v[q] if side[q]==which else zz[q]
    for j,(op,src) in enumerate(C.gates):
        idx=C.n+j
        if side[idx]!=which:continue
        aa=get(src[0]);vv=(1-aa) if op=='NOT' else (
             (aa & get(src[1])) if op=='AND' else
             (aa | get(src[1])) if op=='OR' else
             (aa ^ get(src[1])))
        v[idx]=vv
        if idx in zz and zz[idx]!=vv:return 0
    return int(v[C.V-1]==1) if side[C.V-1]==which else 1

def enumerate_count(C,a,side,cross,check_matrix=True):
    n=C.n; rank_bound=1<<len(cross);Cmat=[[0]*(1<<(n-a)) for _ in range(1<<a)]
    count=0;sum_products=0;rankfactor=0
    for mask in range(1<<n):
        x=[(mask>>i)&1 for i in range(a)]
        y=[(mask>>(a+j))&1 for j in range(n-a)]
        Cmat[mask&((1<<a)-1)][mask>>a]=C.eval(x+y)
        count+=C.eval(x+y)
    for z in itertools.product([0,1],repeat=len(cross)):
        left=[ok_side(C,a,side,cross,z,[(x>>i)&1 for i in range(a)],1) for x in range(1<<a)]
        right=[ok_side(C,a,side,cross,z,[(y>>i)&1 for i in range(n-a)],0) for y in range(1<<(n-a))]
        sum_products+=sum(left)*sum(right)
        if check_matrix:
            for i in range(len(left)):
                for j in range(len(right)):
                    Cmat[i][j]-=left[i]*right[j]
        rankfactor+=1
    assert count==sum_products,(C.name,count,sum_products)
    if check_matrix:assert all(all(v==0 for v in row) for row in Cmat),C.name
    return count,rankfactor

def rank_mod(A,p):
    A=[row[:] for row in A];m=len(A);n=len(A[0]);r=0
    for j in range(n):
        h=next((i for i in range(r,m) if A[i][j]%p),None)
        if h is None:continue
        A[h],A[r]=A[r],A[h];inv=pow(A[r][j],-1,p)
        A[r]=[(v*inv)%p for v in A[r]]
        for i in range(m):
            if i!=r and A[i][j]%p:
                c=A[i][j];A[i]=[(v-c*w)%p for v,w in zip(A[i],A[r])]
        r+=1
        if r==m:break
    return r

def matrix(C,a):
    return [[C.eval([(x>>i)&1 for i in range(a)]+[(y>>j)&1 for j in range(C.n-a)]) for y in range(1<<(C.n-a))] for x in range(1<<a)]

def run():
    rng=random.Random(SEED); rec=[];assertions=0
    examples=[example(k,p) for k in range(1,5) for p in ('DISJ','EQ','IP','SEPARABLE')]
    for idx in range(80):
        n=4;g=[];CUR_N[0]=n;size=1+idx%7
        for j in range(size):
            op=rng.choice(['AND','OR','XOR','NOT']);src=(rng.randrange(n+j),) if op=='NOT' else (rng.randrange(n+j),rng.randrange(n+j))
            append(g,op,*src)
        examples.append(Circuit(n,g,'RND'+str(idx)))
    for C in examples:
        a=C.n//2;r,side,cross=min_signal_cut(C,a)
        assertions+=1;assert r<=C.n
        if len(C.gates)<=10:
            assert r==brute_cut(C,a),(C.name,r,brute_cut(C,a));assertions+=1
        mat=matrix(C,a);R2=rank_mod(mat,2);Rp=rank_mod(mat,PRIME)
        assert R2<=2**r and Rp<=2**r,(C.name,R2,Rp,r);assertions+=2
        count,rankfactor=enumerate_count(C,a,side,cross)
        assert count==sum(map(sum,mat)) and rankfactor==2**r;assertions+=2
        rec.append(dict(name=C.name,n=C.n,gates=len(C.gates),wire_occurrences=sum(len(src) for _,src in C.gates),signals=C.V,r=r,cross=cross,side=''.join(map(str,side)),rank_GF2=R2,rank_F65521=Rp,count=count,terms=rankfactor))
    # Explicit duplicate fanout: driver x0 used by five gates on the other side; hyperedge cost once.
    C=Circuit(4,[('AND',(0,2)),('AND',(0,3)),('OR',(4,5)),('XOR',(0,6)),('AND',(7,1))],'REUSE')
    r,side,cross=min_signal_cut(C,2)
    assert r==brute_cut(C,2);assertions+=1
    assert enumerate_count(C,2,side,cross)[0]==sum(map(sum,matrix(C,2)));assertions+=1
    rec.append(dict(name='REUSE',r=r,cross=cross,side=''.join(map(str,side))))
    return dict(revision=REVISION,seed=SEED,prime=PRIME,cases=len(examples)+1,assertions=assertions,failures=0,records=rec)

if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
