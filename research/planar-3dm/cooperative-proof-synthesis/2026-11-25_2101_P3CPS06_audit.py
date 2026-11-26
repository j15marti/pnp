import itertools as it, json, random, networkx as nx
from collections import defaultdict
P=lambda x:x.bit_count()%2

def span(vs):
    b={}
    for v in vs:
        while v:
            i=v.bit_length()-1
            if i in b:v^=b[i]
            else:b[i]=v;break
    return list(b.values())

def delta(R):
    if not R:return False
    if len({P(x) for x in R})!=1:return False
    return all(any((a^(1<<i)^(1<<j)) in R for j in range((a^b).bit_length()) if i!=j and (a^b)>>j&1) for a in R for b in R for i in range((a^b).bit_length()) if (a^b)>>i&1)

def repair(R,p):
    if delta(R):return None
    if len({P(x) for x in R})==2:return (1<<p)-1
    return 1

def normslots(R,p,flip):
    S={x^flip for x in R};weights={x.bit_count() for x in S};assert len(weights)==1
    w=weights.pop();full=(1<<p)-1
    if w>p//2:S={x^full for x in S};flip^=full;w=p-w
    if w==0:return flip,[]
    if w==1:return flip,[sum(S)]
    assert w==2
    for a in range(1,1<<p):
        for b in range(a,1<<p):
            Q={(1<<i)|(1<<j) for i in range(p) for j in range(p) if i!=j and a>>i&1 and b>>j&1}
            if Q==S:return flip,[a,b]
    raise AssertionError((R,p,flip))

def all_masks():
    out=defaultdict(int)
    for p in range(1,5):
        for colors in it.product(range(3),repeat=p):
            by=defaultdict(list)
            for x in range(1<<p):
                a=[sum((x>>i)&1 for i,c in enumerate(colors) if c==j) for j in range(3)]
                by[(a[0]-a[1],a[0]-a[2])].append(x)
            for E in by.values():
                for s in range(1,1<<len(E)):
                    R={x for i,x in enumerate(E) if s>>i&1};g=repair(R,p)
                    out['masks']+=1;out['direct' if g is None else 'parity_repair' if len({P(x) for x in R})==2 else 'wire_repair']+=1
                    for bit in range(1 if g is None else 2):
                        Q=R if g is None else {x for x in R if P(x&g)==bit}
                        if Q:assert delta(Q);normslots(Q,p,0);out['slot_checks']+=1
                    # conservation + binary hull; check every absent point in E has missing unary/pair projection
                    for x in set(E)-R:
                        assert any(not any((a&f)==(x&f) for a in R) for f in range(1,1<<p) if f.bit_count()<=2)
                        out['binary_exclusions']+=1
    return dict(out)

def lin_solve(eq,n):
    B={}
    for a,b in eq:
        while a:
            i=a.bit_length()-1
            if i in B:c,d=B[i];a^=c;b^=d
            else:B[i]=(a,b);break
        else:
            if b:return None
    def extend(v,hom):
        for i,(a,b) in sorted(B.items()):
            if P(a&v) != (0 if hom else b):v^=1<<i
        return v
    return extend(0,False),[extend(1<<i,True) for i in range(n) if i not in B]

def restrict_blocks(blocks,guards,syndrome):
    Q=[]
    for i,(ports,R,flip) in enumerate(blocks):
        if i in guards:
            j,g=guards[i];R={x for x in R if P(x&g)==(syndrome>>j&1)}
        if not R:return None
        Q.append((ports,R,flip))
    return Q

def matching_terminal(blocks):
    G=nx.Graph(); ends=defaultdict(list); ps={}
    for i,(ports,R,flip) in enumerate(blocks):
        p=len(ports);flip,slots=normslots(R,p,flip)
        for j,e in enumerate(ports):
            v=('p',i,j);G.add_node(v);ends[e].append((v,flip>>j&1));ps[v]=(e,flip>>j&1)
        for s,A in enumerate(slots):
            v=('s',i,s);G.add_node(v)
            for j in range(p):
                if A>>j&1:G.add_edge(v,('p',i,j))
    for e,ab in ends.items():
        assert len(ab)==2
        (v,f),(w,h)=ab
        if f==h:G.add_edge(v,w)
        else:G.add_edges_from([(v,('inv',e)),(w,('inv',e))])
    M=nx.max_weight_matching(G,maxcardinality=True)
    if 2*len(M)!=len(G):return None
    mate={x:y for a,b in M for x,y in [(a,b),(b,a)]};bits={}
    for v,(e,f) in ps.items():
        val=int(mate[v][0]=='s')^f;assert e not in bits or bits[e]==val;bits[e]=val
    for ports,R,_ in blocks:assert sum(bits[e]<<j for j,e in enumerate(ports)) in R
    return bits

def solve_blocks(blocks,n,cap=8):
    eq=[];guards={};gf=[]
    for i,(ports,R,flip) in enumerate(blocks):
        if not R:return 'NO',0,0,None
        def globalmask(x):return sum(1<<e for j,e in enumerate(ports) if x>>j&1)
        for g in range(1,1<<len(ports)):
            vals={P(x&g) for x in R}
            if len(vals)==1:eq.append((globalmask(g),vals.pop()))
        g=repair(R,len(ports))
        if g is not None:guards[i]=(len(gf),g);gf.append(globalmask(g))
    sol=lin_solve(eq,n)
    if sol is None:return 'NO',len(gf),0,None
    x,V=sol
    proj=lambda v:sum(P(v&g)<<j for j,g in enumerate(gf))
    B=span(proj(v) for v in V);rank=len(B)
    if rank>cap:return 'OPEN',len(gf),rank,None
    base=proj(x)
    for mask in range(1<<rank):
        q=base
        for j,v in enumerate(B):
            if mask>>j&1:q^=v
        Q=restrict_blocks(blocks,guards,q)
        if Q is not None:
            w=matching_terminal(Q)
            if w is not None:return 'YES',len(gf),rank,w
    return 'NO',len(gf),rank,None

def graph(T,n):
    G=nx.Graph();G.add_nodes_from(range(3*n+len(T)))
    for i,t in enumerate(T):
        for c,x in enumerate(t):G.add_edge(3*n+i,c*n+x)
    return G

def verify(T,n,ids):
    return len(ids)==n and all({T[i][c] for i in ids}==set(range(n)) for c in range(3))

def brute(T,n):
    by=[[i for i,t in enumerate(T) if t[0]==x] for x in range(n)]
    for ids in it.product(*by):
        if verify(T,n,ids):return True
    return False

def closure(T,n):
    live=set(range(len(T)));forced=set();rem=[set(range(n)) for _ in range(3)]
    while True:
        old=set(live)
        for c in range(3):
            for v in sorted(rem[c]):
                opts=[i for i in live if T[i][c]==v]
                if not opts:return None,forced
                if len(opts)==1:
                    i=opts[0];t=T[i];forced.add(i)
                    for d in range(3):rem[d].remove(t[d])
                    live={j for j in live if all(T[j][d]!=t[d] for d in range(3))}
                    break
            else:continue
            break
        if live!=old:continue
        for c,d in [(0,1),(0,2),(1,2)]:
            A=nx.Graph();L=[(c,v) for v in sorted(rem[c])];R=[(d,v) for v in sorted(rem[d])];A.add_nodes_from(L+R)
            A.add_edges_from(((c,T[i][c]),(d,T[i][d])) for i in sorted(live))
            M=nx.bipartite.maximum_matching(A,top_nodes=L)
            if any(x not in M for x in L):return None,forced
            D=nx.DiGraph();D.add_nodes_from(A)
            for a,b in A.edges:
                if a[0]!=c:a,b=b,a
                D.add_edge(b,a) if M[a]==b else D.add_edge(a,b)
            labels={v:j for j,C in enumerate(nx.strongly_connected_components(D)) for v in C}
            live={i for i in live if M[(c,T[i][c])]==(d,T[i][d]) or labels[(c,T[i][c])]==labels[(d,T[i][d])]}
        if live==old:return (live,rem),forced

def paired(T,n):
    G=graph(T,n);assert nx.check_planarity(G)[0] and len(T)==len(set(T))
    cl,F=closure(T,n)
    if cl is None:return 'NO',0,0,'closure'
    live,rem=cl
    if not live:assert verify(T,n,F);return 'YES',0,0,'closure'
    E={c*n+x for c in range(3) for x in rem[c]};Q={3*n+i for i in live};H=G.subgraph(E|Q).copy()
    if max(H.degree(v) for v in E)>3:return 'OPEN',0,0,'degree'
    M=nx.bipartite.maximum_matching(H,top_nodes=Q);assert all(v in M for v in Q)
    groups=[{v,M[v]} for v in sorted(Q)]+[{v} for v in sorted(E-set(M))]
    owner={v:i for i,C in enumerate(groups) for v in C};wires=[]
    for a,b in H.edges:
        if owner[a]!=owner[b]:wires.append((a,b))
    blocks=[]
    for C in groups:
        pp=[j for j,(a,b) in enumerate(wires) if (a in C)!=(b in C)]
        inner=[a if a in C else b for j in pp for a,b in [wires[j]]];p=len(pp)
        flip=sum(1<<j for j,v in enumerate(inner) if v>=3*n)
        R=set()
        for x in range(1<<p):
            for z in range(2 if len(C)==2 else 1):
                if all(((sum((x>>j)&1 for j,u in enumerate(inner) if u==v)+z==1) if v<3*n else all((x>>j)&1==z for j,u in enumerate(inner) if u==v)) for v in C):R.add(x)
        blocks.append((pp,R,flip))
    result,g,r,bits=solve_blocks(blocks,len(wires))
    if bits is not None:
        ids=F|{(a if a>=3*n else b)-3*n for j,(a,b) in enumerate(wires) if bits[j]}
        assert verify(T,n,ids)
    return result,g,r,'paired'

def prism(m):
    return [tuple(next(j%m//3 for j in [i-1,i,i+1] if j%3==c) for c in range(3)) for i in range(m)]

def splice(k):
    base=[(0,0,0),(1,1,1),(0,0,1),(1,1,0),(0,1,0),(1,0,1)]
    T=[[2*i+x for x in t] for i in range(2*k) for t in base]
    for i in range(k-1):a,b=6*i+1,6*(i+1);T[a][1],T[b][1]=T[b][1],T[a][1]
    for i in range(k):a,b=6*i+2,6*(k+i)+2;T[a][2],T[b][2]=T[b][2],T[a][2]
    return list(map(tuple,T))

if __name__=='__main__':
    out={'finite':all_masks(),'small':defaultdict(int),'prisms':[],'splices':[],'peer':[]}
    rng=random.Random(5506)
    samples=[(2,[t for j,t in enumerate(it.product(range(2),repeat=3)) if mask>>j&1]) for mask in range(256)]
    all3=list(it.product(range(3),repeat=3));samples += [(3,rng.sample(all3,rng.randint(5,12))) for _ in range(400)]
    for n,T in samples:
        if not nx.check_planarity(graph(T,n))[0] or max(dict(graph(T,n).degree()).values(),default=0)>3:continue
        ans=brute(T,n);res,g,r,stage=paired(T,n)
        assert res=='OPEN' or (res=='YES')==ans
        out['small'][res+'_'+stage]+=1;out['small']['SAT' if ans else 'UNSAT']+=1
    for m in [6,12,24,48,96,192]:
        T=prism(m);n=m//3;assert verify(T,n,range(0,m,3))
        a=paired(T,n);assert a[0]=='YES' and a[2]==2
        U=[t for i,t in enumerate(T) if i not in {0,1,2}];b=paired(U,n);assert b[0]=='NO'
        out['prisms'].append([m,a,b])
    for k in [1,2,4,8,16,32]:
        T=splice(k);n=4*k
        for j in range(k):
            ids=[6*i+h for i in range(2*k) for h in ([2,3] if i%k==j else [4,5])];assert verify(T,n,ids)
        assert verify(T,n,[6*i+h for i in range(2*k) for h in [4,5]])
        a=paired(T,n);assert a[2]>=k
        out['splices'].append([k,len(T),a])
    U=[tuple(map(int,t)) for t in '000 012 010 110 111 121 123 221 232 333 332 302'.split()]
    for T in [U,U+[(0,0,2)]]:
        a=paired(T,4);out['peer'].append([len(T),brute(T,4),a]);assert a[0]=='OPEN' or (a[0]=='YES')==brute(T,4)
    print(json.dumps(out,indent=2))
