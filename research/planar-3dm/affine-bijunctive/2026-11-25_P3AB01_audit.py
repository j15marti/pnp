import itertools as it, random, json, networkx as nx
from collections import Counter

def parity(x): return x.bit_count()&1

def basis(rows):
    B={}
    for x in rows:
        for p in sorted(B,reverse=True):
            if x>>p&1: x^=B[p]
        if x:B[x.bit_length()-1]=x
    return B

def affine(rows,m):
    B={}
    for a,b in rows:
        for p in sorted(B,reverse=True):
            if a>>p&1: a^=B[p][0]; b^=B[p][1]
        if not a:
            if b:return None
        else:B[a.bit_length()-1]=(a,b)
    F=[j for j in range(m) if j not in B]; A=[None]*m
    for i,j in enumerate(F):A[j]=(1<<i,0)
    for p in sorted(B):
        a,b=B[p]; v=0
        for j in range(p):
            if a>>j&1:v^=A[j][0]; b^=A[j][1]
        A[p]=(v,b)
    return A,len(F)

def forms(T,n):return [[j for j,t in enumerate(T) if t[c]==v] for c in range(3) for v in range(n)]
def verify(T,n,w):return all(sum(w>>j&1 for j in S)==1 for S in forms(T,n))
def planar(T,n):
    G=nx.Graph();G.add_nodes_from(range(3*n+len(T)))
    G.add_edges_from((c*n+v,3*n+j) for j,t in enumerate(T) for c,v in enumerate(t))
    return nx.check_planarity(G)[0]
def match(T,n,pins,c,d):
    pos=[j for j,b in pins.items() if b]; C={T[j][c] for j in pos};D={T[j][d] for j in pos}
    if len(C)!=len(pos) or len(D)!=len(pos):return False
    L=[(0,i) for i in range(n) if i not in C]; R=[(1,i) for i in range(n) if i not in D]
    G=nx.Graph();G.add_nodes_from(L+R)
    G.add_edges_from(((0,t[c]),(1,t[d])) for j,t in enumerate(T) if j not in pins and t[c] not in C and t[d] not in D)
    return len(nx.algorithms.bipartite.maximum_matching(G,top_nodes=L))==2*len(L)

def quad(f,g,d):
    a,b=f;c,e=g; lin=(a&c)^(a if e else 0)^(c if b else 0); q=0
    for i in range(d):
        for j in range(i+1,d):
            if ((a>>i&1)*(c>>j&1))^((a>>j&1)*(c>>i&1)):q|=1<<(i*d+j)
    return q,lin,b&e

def normalize(T,n,pins):
    m=len(T);S= forms(T,n);pins=dict(pins); rows=[(sum(1<<j for j in s),1) for s in S]
    # Rows inferred in the original coordinates by lifting latent free columns.
    while True:
        old=(len(pins),len(rows)); bad=False
        for s in S:
            P=[j for j in s if pins.get(j)==1];L=[j for j in s if j not in pins]
            if len(P)>1 or not P and not L:return None
            if P:
                for j in L:pins[j]=0
            elif len(L)==1:pins[L[0]]=1
        for c,d in [(0,1),(0,2),(1,2)]:
            if not match(T,n,pins,c,d):return None
        for j in range(m):
            if j not in pins:
                if not all(match(T,n,{**pins,j:1},c,d) for c,d in [(0,1),(0,2),(1,2)]):pins[j]=0
        A=affine(rows+[(1<<j,b) for j,b in pins.items()],m)
        if A is None:return None
        A,d=A;F=[next(j for j,f in enumerate(A) if f==(1<<i,0)) for i in range(d)]
        for j,(a,b) in enumerate(A):
            if not a:
                if j in pins and pins[j]!=b:return None
                pins[j]=b
        B={};new=[]
        for s in S:
            for i,j in it.combinations(s,2):
                q,a,b=quad(A[i],A[j],d)
                for p in sorted(B,reverse=True):
                    if q>>p&1:q^=B[p][0];a^=B[p][1];b^=B[p][2]
                if q:B[q.bit_length()-1]=(q,a,b)
                elif not a:
                    if b:return None
                else:new.append((sum(1<<F[i] for i in range(d) if a>>i&1),b))
        # Each nonzero row restricts the current chart, hence progress.
        rows.extend(new)
        if old==(len(pins),len(rows)):return A,d,pins,rows

def close(T,n,pins,probe=True):
    P=dict(pins)
    while True:
        C=normalize(T,n,P)
        if C is None:return None
        A,d,P,rows=C
        if not probe:return C
        for j in range(len(T)):
            if j in P:continue
            for b in [0,1]:
                if normalize(T,n,{**P,j:b}) is None:P[j]=1-b;break
            else:continue
            break
        else:return C

def cover(planes):
    P=sorted(set(tuple(sorted(p)) for p in planes)); counts=Counter(v for p in P for v in p); F={v for v,k in counts.items() if k>1};D=set(F)
    for p in P:
        for v in p:
            if len(D.intersection(p))>=2:break
            D.add(v)
    # ownerwise coordinateization iff the constructed cover is independent
    # if all three forced in one plane, this already fails.
    if len(D)==len(basis(D)):return sorted(D),0,P
    # Additional paid greedy cover tracks; exact zero-excess recognition above.
    U=sorted(counts); G=nx.Graph();G.add_nodes_from(U)
    for p in P:G.add_edges_from(it.combinations(p,2))
    opts=[D]
    for order in (U,U[::-1],sorted(U,key=lambda v:(G.degree(v),v)),sorted(U,key=lambda v:(-G.degree(v),v))):
        I=set()
        for v in order:
            if not I.intersection(G[v]):I.add(v)
        opts.append(set(U)-I)
    D=min(opts,key=lambda x:(len(x),sorted(x)))
    assert all(len(D.intersection(p))>=2 for p in P)
    return sorted(D),len(D)-len(basis(D)),P

def evaluate(A,z):return sum((parity(a&z)^b)<<j for j,(a,b) in enumerate(A))
def compile_chart(T,n,A,d):
    units=[];polys=[];planes=[]
    for S in forms(T,n):
        for i,j in it.combinations(S,2):
            a,b=A[i];c,e=A[j]
            if not a or not c or a==c:
                # Evaluate in at most one direction and add forbidding patterns.
                v=a or c
                for t in ([0,1] if v else [0]):
                    if ((t if a else 0)^b) and ((t if c else 0)^e):units.append((v,t))
            else:
                p=tuple(sorted((a,c,a^c)));planes.append(p);polys.append((a,b,c,e,p))
    D,ex,P=cover(planes)
    D=sorted(set(D)|{v for v,t in units if v})
    # units not in chosen coordinates are retained as linear equations; instead add them to D.
    ex=len(D)-len(basis(D));idx={v:i for i,v in enumerate(D)}; clauses=[]
    for v,t in units:
        if not v:return None
        clauses.append(((idx[v],1-t),))
    for a,b,c,e,p in polys:
        u,v=[x for x in p if x in idx][:2]
        def val(r,x,y):return x if r==u else y if r==v else x^y
        for x,y in it.product([0,1],repeat=2):
            if (val(a,x,y)^b) and (val(c,x,y)^e):clauses.append(((idx[u],1-x),(idx[v],1-y)))
    # obtain exact relations among D by incremental elimination with provenance
    B={};eq=[]
    for i,v in enumerate(D):
        r=1<<i
        for p in sorted(B,reverse=True):
            if v>>p&1:v^=B[p][0];r^=B[p][1]
        if v:B[v.bit_length()-1]=(v,r)
        else:eq.append(r)
    assert len(eq)==ex
    return D,eq,clauses,P

def two_sat(k,clauses):
    G=nx.DiGraph();G.add_nodes_from(range(2*k))
    for cl in clauses:
        a=2*cl[0][0]+cl[0][1];b=2*cl[-1][0]+cl[-1][1]
        G.add_edge(a^1,b);G.add_edge(b^1,a)
    s=list(nx.strongly_connected_components(G));ids={v:i for i,S in enumerate(s) for v in S}
    if any(ids[2*j]==ids[2*j+1] for j in range(k)):return None
    return sum((ids[2*j+1]<ids[2*j])<<j for j in range(k))
def sat_clauses(w,C):return all(any(w>>j&1==b for j,b in cl) for cl in C)
def low_excess(k,eq,C,cap=2):
    if len(eq)>cap:return 'UNKNOWN',None
    a=two_sat(k,C)
    if a is None:return 'NO',None
    assert sat_clauses(a,C)
    # Translate the 2CNF around a model. Horn constraints become implications or negative pairs.
    G=nx.DiGraph();G.add_nodes_from(range(k));forbid=[]
    for cl in C:
        L=[(j,b^(a>>j&1)) for j,b in cl];assert any(b==0 for j,b in L)
        if len(L)==1:forbid.append((L[0][0],L[0][0]))
        elif L[0][1]==L[1][1]==0:forbid.append((L[0][0],L[1][0]))
        else:
            neg=next(j for j,b in L if b==0);pos=next(j for j,b in L if b==1);G.add_edge(neg,pos)
    reach=[(1<<j)|sum(1<<v for v in nx.descendants(G,j)) for j in range(k)]
    for h in range(len(eq)+1):
        for S in it.combinations(range(k),h):
            w=0
            for j in S:w|=reach[j]
            if any(w>>i&1 and w>>j&1 for i,j in forbid):continue
            x=w^a;assert sat_clauses(x,C)
            if all(not parity(x&r) for r in eq):return 'YES',x
    return 'NO',None

def solve(T,n,pins={},cap=2,probe=True):
    C=close(T,n,pins,probe)
    if C is None:return 'NO',None,None
    A,d,P,rows=C; chart=compile_chart(T,n,A,d)
    if chart is None:return 'NO',None,None
    D,eq,cl,planes=chart;label,w=low_excess(len(D),eq,cl,cap)
    if label=='YES':
        Z=affine([(v,w>>i&1) for i,v in enumerate(D)],d);assert Z is not None
        z=evaluate(Z[0],0);x=evaluate(A,z);assert verify(T,n,x) and all(x>>j&1==b for j,b in pins.items())
    else:x=None
    return label,x,(len(D),len(eq),d,len(planes))

def ref(T,n,pins={}):
    return next((sum(1<<j for j in S) for S in it.combinations(range(len(T)),n) if all(len({T[j][c] for j in S})==n for c in range(3)) and all((j in S)==b for j,b in pins.items())),None)

def run():
    rng=random.Random(20261125); stats=Counter();examples={}; accepted=0
    for n in (2,3,4):
        U=list(it.product(range(n),repeat=3));seen=set()
        for trial in range(250):
            T=tuple(sorted(rng.sample(U,rng.randint(2*n,min(3*n,len(U))))))
            if T in seen or not planar(T,n):continue
            seen.add(T);stats['planar_sources']+=1
            for P in ({},{rng.randrange(len(T)):rng.randrange(2)}):
                w=ref(T,n,P);r,x,meta=solve(T,n,P,2)
                stats['jobs']+=1;stats['reference_'+('YES' if w is not None else 'NO')]+=1;stats[r]+=1
                if r!='UNKNOWN':assert (r=='YES')==(w is not None)
                if meta:
                    stats['chart_jobs']+=1;stats['excess_'+str(meta[1])]+=1
                    if meta[1]>0 and w is not None and 'positive_excess_SAT' not in examples:examples['positive_excess_SAT']=(n,T,P,meta)
                    if meta[1]>2 and 'cap_overflow' not in examples:examples['cap_overflow']=(n,T,P,meta)
    # Peer near-consensus planar neighbors, plus exact 2x2x2 octahedron-minus-two-opposite-faces.
    fixtures=[(2,[(0,0,0),(1,1,0),(1,0,1),(0,1,1)]),(2,[(0,0,0),(1,1,0),(1,0,1),(0,1,1),(0,0,1)])]
    for n,T in fixtures:
        assert planar(T,n);r,x,meta=solve(T,n);assert r!='UNKNOWN' and (r=='YES')==(ref(T,n) is not None);examples['neighbor_'+str(len(T))]=(r,meta)
    # Independently audit low-excess theorem on arbitrary small 2CNF with <=2 parity rows.
    for _ in range(500):
        k=rng.randint(2,7);C=[tuple((j,rng.randrange(2)) for j in rng.sample(range(k),rng.randint(1,2))) for _ in range(rng.randrange(10))];E=[rng.randrange(1,1<<k) for _ in range(rng.randrange(3))];r,x=low_excess(k,E,C)
        F=[w for w in range(1<<k) if sat_clauses(w,C) and all(not parity(w&e) for e in E)];assert (r=='YES')==bool(F);stats['abstract_jobs']+=1;stats['abstract_'+r]+=1
    def oct_chain(n):
        T=set(it.product(range(2),repeat=3)); W={(0,0,0),(1,1,1)}
        for k in range(2,n):
            f=min(T-W);T.remove(f);T.update(t for t in it.product(*[(f[i],k) for i in range(3)]) if t!=f);W.add((k,k,k))
        return sorted(T),W
    chain=[]
    for n in (2,3,4,6,8):
        T,W=oct_chain(n);assert planar(T,n);assert verify(T,n,sum(1<<j for j,t in enumerate(T) if t in W))
        r,x,meta=solve(T,n);assert r in ('YES','UNKNOWN');chain.append((n,len(T),r,meta))
    T,_=oct_chain(3);rng=random.Random(193)
    for _ in range(240):
        A=tuple(sorted(rng.sample(T,rng.randint(8,14))));assert planar(A,3);r,x,meta=solve(A,3);w=ref(A,3);assert r=='UNKNOWN' or (r=='YES')==(w is not None);stats['oct_sub_'+r]+=1
        if meta:stats['oct_excess_'+str(meta[1])]+=1
    for _ in range(100):
        d=3;Q=[]
        for _ in range(rng.randrange(1,8)):
            a,b=rng.sample(range(1,1<<d),2);Q.append((a,b,a^b))
        D,e,P=cover(Q);U=sorted(set(v for p in P for v in p));r=len(basis(U))
        best=min(len(S)-r for h in range(len(U)+1) for S in it.combinations(U,h) if all(len(set(S).intersection(p))>=2 for p in P))
        assert e>=best and (e==0)==(best==0);stats['cover_oracle']+=1
    print(json.dumps({'seed':20261125,'stats':stats,'examples':examples,'chain':chain},indent=2))
if __name__=='__main__':run()
