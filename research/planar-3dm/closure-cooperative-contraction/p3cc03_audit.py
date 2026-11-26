import json, random, itertools
from collections import Counter
import networkx as nx
from sympy import Matrix


def chi(a,s): return 1-2*((a&s).bit_count()%2)
def det(a):
    a=[r[:] for r in a]; n=len(a); prev=sgn=1
    for k in range(n-1):
        i=next((i for i in range(k,n) if a[i][k]),None)
        if i is None: return 0
        if i!=k: a[k],a[i]=a[i],a[k]; sgn=-sgn
        p=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n): a[i][j]=(a[i][j]*p-a[i][k]*a[k][j])//prev
            a[i][k]=0
        prev=p
    return sgn*a[-1][-1] if n else 1


def source_graph(n,T):
    g=nx.Graph(); g.add_nodes_from((c,i) for c in range(3) for i in range(n))
    for j,t in enumerate(T):
        for c,v in enumerate(t): g.add_edge((3,j),(c,v))
    return g


def closure(n,T):
    # Keep original IDs (tuples). Forced choices recorded and removed.
    live=set(T); active=[set(range(n)) for _ in range(3)]; forced=[]
    while True:
        changed=False
        for c in range(3):
            for v in sorted(active[c]):
                inc=[t for t in live if t[c]==v]
                if not inc:return None,forced
                if len(inc)==1:
                    t=inc[0]; forced.append(t)
                    live={u for u in live if all(u[d]!=t[d] for d in range(3))}
                    for d in range(3): active[d].remove(t[d])
                    changed=True; break
            if changed:break
        if changed:continue
        for a,b in [(0,1),(0,2),(1,2)]:
            g=nx.Graph(); left=[(a,v) for v in sorted(active[a])]; g.add_nodes_from(left); g.add_nodes_from((b,v) for v in active[b]);g.add_edges_from(((a,t[a]),(b,t[b])) for t in sorted(live))
            m=nx.algorithms.bipartite.maximum_matching(g,top_nodes=left)
            if len(m)!=2*len(left):return None,forced
            d=nx.DiGraph();d.add_nodes_from(g)
            for u,v in g.edges():
                if u[0]!=a:u,v=v,u
                d.add_edge(v,u) if m[u]==v else d.add_edge(u,v)
            cid={v:i for i,C in enumerate(nx.strongly_connected_components(d)) for v in C}
            kept={t for t in live if m[(a,t[a])]==(b,t[b]) or cid[(a,t[a])]==cid[(b,t[b])]}
            if kept!=live:live=kept;changed=True;break
        if not changed:return sorted(live),forced


class Oracle:
    # Subdivision is for embedding only: original indexed edge = one triple.
    def __init__(self,n,T,labels=None):
        self.n=n; self.T=T; self.L=labels if labels is not None else [1<<z for x,y,z in T]; self.calls=0; self.cache={}
        g=nx.Graph();g.add_nodes_from((c,i) for c in (0,1) for i in range(n))
        for i,(x,y,z) in enumerate(T):g.add_edges_from([((0,x),(3,i)),((3,i),(1,y))])
        ok,emb=nx.check_planarity(g);assert ok
        # Face walks on each connected component; omit one face per component.
        rows=[]
        for C in nx.connected_components(g):
            seen=set(); faces=[]
            for u in sorted(C):
                for v in emb.neighbors_cw_order(u):
                    if (u,v) in seen:continue
                    f=emb.traverse_face(u,v,seen);ids=[i for c,i in f if c==3];assert len(ids)%2==0
                    mask=0
                    for i in ids:mask^=1<<i
                    faces.append((mask,(len(ids)//2+1)%2))
            rows.extend(faces[1:])
        piv={}
        for a,b in rows:
            while a and a.bit_length()-1 in piv:
                u,v=piv[a.bit_length()-1];a^=u;b^=v
            if a:piv[a.bit_length()-1]=(a,b)
            else:assert b==0
        s=0
        for k,(a,b) in sorted(piv.items()):
            if ((a&s).bit_count()%2)!=b:s|=1<<k
        self.sign=[chi(s,1<<i) for i in range(len(T))]; self.orientation=1
        v=self.raw(0,(1<<len(T))-1);self.orientation=1 if v>=0 else -1
        self.cache[(0,(1<<len(T))-1)]=abs(v)
    def raw(self,a,live):
        self.calls+=1;M=[[0]*self.n for _ in range(self.n)]
        for i,(x,y,z) in enumerate(self.T):
            if live>>i&1:M[x][y]+=self.sign[i]*chi(a,self.L[i])
        return det(M)
    def F(self,a,live=None):
        if live is None:live=(1<<len(self.T))-1
        key=(a,live)
        if key not in self.cache:self.cache[key]=self.orientation*self.raw(a,live)
        return self.cache[key]


def extend_basis(old,S,bit):
    # Walsh rows span over GF(3) as well as Q; GF(3) independence certifies Q independence.
    piv={};out=[]
    for a in old+[a|bit for a in old]:
        r=[chi(a,s)%3 for s in S]
        for j,v in piv.items():
            c=r[j]
            if c:r=[(x-c*y)%3 for x,y in zip(r,v)]
        j=next((j for j,x in enumerate(r) if x),None)
        if j is not None:
            piv[j]=[(x*r[j])%3 for x in r];out.append(a)
    assert len(out)==len(S)
    return out


def acquire(O,d,K):
    total=O.F(0)
    if total==0:return {},[],None
    S={0:total};B=[0]
    for j in range(d):
        bit=1<<j;words=list(S);E=Matrix([[chi(a,s) for s in words] for a in B]);rhs=Matrix([O.F(a|bit) for a in B]);diff=E.inv()*rhs
        new={}
        for s,h in zip(words,diff):
            plus=(S[s]+h)/2;minus=(S[s]-h)/2
            assert plus.q==minus.q==1 and plus>=0 and minus>=0
            if plus:new[s]=int(plus)
            if minus:new[s|bit]=int(minus)
        if len(new)>K:return None,[],None
        B=extend_basis(B,list(new),bit);S=new
    E=Matrix([[chi(a,s) for s in S] for a in B]);return S,B,E.inv()


def lift(O,S,B,Einv,s):
    row=list(Einv.row(list(S).index(s)));live=(1<<len(O.T))-1
    for i in range(len(O.T)):
        child=live&~(1<<i)
        v=sum(c*O.F(a,child) for c,a in zip(row,B))
        assert v>=0 and v.q==1
        if v:live=child
    ids=[i for i in range(len(O.T)) if live>>i&1];assert len(ids)==O.n
    word=0
    for i in ids:word^=O.L[i]
    assert word==s and all(len({O.T[i][c] for i in ids})==O.n for c in (0,1));return ids


def reference(n,T,labels=None):
    L=labels if labels is not None else [1<<t[2] for t in T];by=[[] for _ in range(n)]
    for i,t in enumerate(T):by[t[0]].append((t[1],L[i]))
    out=Counter()
    def rec(i,used,s):
        if i==n:out[s]+=1;return
        for y,l in by[i]:
            if not used>>y&1:rec(i+1,used|1<<y,s^l)
    rec(0,0,0);return dict(out)


def fan(n,yes):
    k=n-1
    return sorted([(0,0,k)]+([(0,0,0)] if yes else [])+[(i,i,i) for i in range(1,n)]+[(0,i,i-1) for i in range(1,n)]+[(i,0,i-1) for i in range(1,n)])


def octa(n):
    T=set(itertools.product(range(2),repeat=3));f=(0,1,0)
    for k in range(2,n):
        T.remove(f);T.update(t for t in itertools.product(*[(v,k) for v in f]) if t!=f);f=(k,f[1],f[2])
    return sorted(T)


def rank(words):
    p={};base=words[0]
    for w in words:
        w^=base
        while w and w.bit_length()-1 in p:w^=p[w.bit_length()-1]
        if w:p[w.bit_length()-1]=w
    return len(p)


def main():
    rng=random.Random(20261125);R={'seed':20261125,'small':0,'small_yes':0,'small_no':0,'guarded':0,'lifts':0,'fan':[],'dense':[],'count_calls':0}
    U=[tuple(map(int,s)) for s in ['000','002','010','011','021','022','100','101','111','201','202','221']]
    cases=[(3,U),(3,U+[(1,1,0)])]
    for n in (2,3,4,5):
        for _ in range(30):cases.append((n,[t for t in octa(n) if rng.random()<.83]))
    for n,T in cases:
        assert nx.check_planarity(source_graph(n,T))[0]
        C=closure(n,T);ref=reference(n,T);target=(1<<n)-1;yes=target in ref
        assert C[0] is not None or not yes
        if C[0] is not None:
            live,forced=C;allowed=set(live)|set(forced);assert (target in reference(n,[t for t in T if t in allowed]))==yes
        O=Oracle(n,T);S,B,I=acquire(O,n,2**n);assert S==ref
        R['small']+=1;R['small_yes' if yes else 'small_no']+=1
        if S:
            for s in S:lift(O,S,B,I,s);R['lifts']+=1
        L=[(1<<t[2])|(rng.randrange(4)<<n) for t in T];O2=Oracle(n,T,L);S2,B2,I2=acquire(O2,n+2,2**(n+2));assert S2==reference(n,T,L)
        if S2:lift(O2,S2,B2,I2,next(iter(S2)));R['lifts']+=1
        R['guarded']+=1;R['count_calls']+=O.calls+O2.calls
    for n in (4,8,16,32):
        for yes in (True,False):
            T=fan(n,yes);assert nx.check_planarity(source_graph(n,T))[0] and nx.is_connected(source_graph(n,T));assert closure(n,T)==(T,[])
            O=Oracle(n,T);S,B,I=acquire(O,n,n);target=(1<<n)-1;assert (target in S)==yes and len(S)==(n if yes else n-1)
            assert rank(list(S))==(n-1 if yes else n-2);assert S==reference(n,T)
            calls=O.calls;lift(O,S,B,I,target if yes else next(iter(S)));R['lifts']+=1
            R['fan'].append({'n':n,'yes':yes,'triples':len(T),'support':len(S),'affine_rank':rank(list(S)),'acquisition_calls':calls,'lift_calls':O.calls-calls})
            R['count_calls']+=O.calls
    for n in (4,8,16,32,64):
        T=octa(n);assert nx.check_planarity(source_graph(n,T))[0] and nx.is_connected(source_graph(n,T));assert closure(n,T)==(T,[])
        assert all((i,i,i) in T and (i,i,0) in T for i in range(n))
        O=Oracle(n,T);S,B,I=acquire(O,n,32)
        assert (S is None)==(2**(n-1)>32)
        if S is not None:assert len(S)==2**(n-1)
        R['dense'].append({'n':n,'triples':len(T),'support_proved':2**(n-1),'cap':32,'cap_exceeded':S is None,'calls':O.calls});R['count_calls']+=O.calls
    print(json.dumps(R,indent=2))
if __name__=='__main__':main()
