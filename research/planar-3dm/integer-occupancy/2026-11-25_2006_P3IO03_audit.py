import itertools as it, random, json, collections, time
import networkx as nx

def incidence(n,T):
    G=nx.Graph(); G.add_nodes_from((c,i) for c in range(3) for i in range(n))
    for j,t in enumerate(T):
        G.add_edges_from(((3,j),(c,v)) for c,v in enumerate(t))
    return G

def match(n,T,a,b,p):
    fixed=[j for j in p if p[j]==1]
    A={T[j][a] for j in fixed}; B={T[j][b] for j in fixed}
    if len(A)!=len(fixed) or len(B)!=len(fixed): return None
    G=nx.Graph(); X=[(a,i) for i in range(n) if i not in A]; Y=[(b,i) for i in range(n) if i not in B]; G.add_nodes_from(X+Y); ids={}
    for j,t in enumerate(T):
        if j in p or t[a] in A or t[b] in B: continue
        u=(a,t[a]);v=(b,t[b]);G.add_edge(u,v);ids[u,v]=j
    M=nx.algorithms.bipartite.maximum_matching(G,top_nodes=X)
    if any(u not in M for u in X): return None
    return set(fixed+[ids[u,M[u]] for u in X])

def closure(n,T,p,stats):
    p=dict(p); rows=[[j for j,t in enumerate(T) if t[c]==i] for c in range(3) for i in range(n)]
    while True:
        old=len(p)
        for R in rows:
            ones=[j for j in R if p.get(j)==1]; free=[j for j in R if j not in p]
            if len(ones)>1 or not ones and not free: return None
            if ones:
                for j in free:p[j]=0
            elif len(free)==1:p[free[0]]=1
        for a,b in [(0,1),(0,2),(1,2)]:
            stats['match_calls']+=1
            if match(n,T,a,b,p) is None:return None
            for j in range(len(T)):
                if j in p:continue
                for v in (0,1):
                    stats['match_calls']+=1
                    if match(n,T,a,b,{**p,j:v}) is None:p[j]=1-v;break
        if len(p)==old:return p

def chart(n,T,a,b,p):
    M=match(n,T,a,b,p); assert M is not None
    G=nx.Graph();G.add_nodes_from((c,i) for c in (a,b) for i in range(n))
    for j,t in enumerate(T):G.add_edges_from([((a,t[a]),(3,j)),((3,j),(b,t[b]))])
    ok,E=nx.check_planarity(G);assert ok
    faces={}; roots=set();f=0
    for comp in nx.connected_components(G):
        root=f
        for u in sorted(comp):
            for v in E.neighbors_cw_order(u):
                if (u,v) in faces:continue
                walk=E.traverse_face(u,v)
                for x,y in zip(walk,walk[1:]+walk[:1]):faces[x,y]=f
                f+=1
        if f>root:roots.add(root)
    def row(items):
        d=collections.Counter()
        for k,v in items:d[k]+=v
        return {k:v for k,v in d.items() if v and k not in roots}
    edges=[]
    for j,t in enumerate(T):edges.append(row([(faces[(a,t[a]),(3,j)],1),(faces[(3,j),(a,t[a])],-1)]))
    c=3-a-b; labels=[]
    for z in range(n):
        J=[j for j,t in enumerate(T) if t[c]==z]
        labels.append((row((k,v) for j in J for k,v in edges[j].items()),1-sum(j in M for j in J)))
    constraints=[]
    for j,D in enumerate(edges):
        lo=hi=p[j] if j in p else None
        if lo is None:lo,hi=0,1
        constraints.extend([(D,lo-int(j in M)),({k:-v for k,v in D.items()},int(j in M)-hi)])
    return M,edges,labels,constraints,f,roots

def blocks(labels):
    G=nx.Graph();G.add_nodes_from(range(len(labels))); seen={}
    for i,(D,b) in enumerate(labels):
        for k in D:
            if k in seen:G.add_edge(i,seen[k])
            else:seen[k]=i
    return list(nx.connected_components(G))

def monotone(rows,f,roots,B,stats):
    h=[0 if k in roots else -B for k in range(f)]
    for D,b in rows:assert sum(v>0 for v in D.values())<=1
    while True:
        changed=False
        for D,b in rows:
            stats['row_scans']+=1
            if sum(v*h[k] for k,v in D.items())>=b:continue
            pos=[k for k,v in D.items() if v>0]
            if not pos:return None
            k=pos[0];rhs=b-sum(v*h[j] for j,v in D.items() if j!=k);val=-(-rhs//D[k]);assert val>h[k]
            if val>B:return None
            h[k]=val;changed=True;stats['raises']+=1
        if not changed:return h

def gauge(rows,f,roots):
    G=nx.DiGraph();G.add_nodes_from((k,v) for k in range(f) if k not in roots for v in (0,1))
    for D,b in rows:
        for (i,a),(j,c) in it.combinations(D.items(),2):
            u=(i,int(a<0));v=(j,int(c<0)) # these values make coefficients positive
            G.add_edge(u,(v[0],1-v[1]));G.add_edge(v,(u[0],1-u[1]))
    C=list(nx.strongly_connected_components(G));idx={u:i for i,S in enumerate(C) for u in S}
    if any(idx[k,0]==idx[k,1] for k in range(f) if k not in roots):return None
    order={i:t for t,i in enumerate(nx.topological_sort(nx.condensation(G,C)))}
    signs={k:(-1 if order[idx[k,1]]>order[idx[k,0]] else 1) for k in range(f) if k not in roots}
    assert all(sum(signs[k]*v>0 for k,v in D.items())<=1 for D,b in rows)
    return signs

def lane(n,T,a,b,p,stats):
    M,edges,labels,base,f,roots=chart(n,T,a,b,p)
    groups=blocks(labels);rows=list(base);directions=[];admitted=True
    for C in groups:
        assert all(sum(labels[i][0].get(k,0) for i in C)==0 for k in range(f))
        if sum(labels[i][1] for i in C)!=0:return 'NO',None,False
        opts=[s for s in (1,-1) if all(sum(s*v>0 for v in labels[i][0].values())<=1 for i in C)]
        if not opts:admitted=False;break
        s=opts[0];directions.append(s)
        rows.extend([({k:s*v for k,v in labels[i][0].items()},s*labels[i][1]) for i in C])
    mode='BLOCK'
    if admitted:signs={k:1 for k in range(f) if k not in roots}
    else:
        rows=base+labels;signs=gauge(rows,f,roots);mode='GAUGE'
        if signs is None:
            for sg in (1,-1):
                signs={k:sg for k in range(f) if k not in roots}
                rows=[({k:sg*v for k,v in D.items()},b) for D,b in base]
                for D,b in labels:
                    for d in (1,-1):
                        R={k:d*sg*v for k,v in D.items()}
                        if sum(v>0 for v in R.values())<=1:rows.append((R,d*b))
                stats['relax_attempts']+=1
                h=monotone(rows,f,roots,len(T),stats)
                if h is None:stats['relax_NO']+=1;return 'NO',None,False
                W=[j for j,D in enumerate(edges) if int(j in M)+sum(v*signs[k]*h[k] for k,v in D.items())==1]
                if valid(n,T,W) and all((j in W)==bool(v) for j,v in p.items()):stats['relax_YES']+=1;return 'YES',W,False
            return 'UNKNOWN',None,False
        rows=[({k:signs[k]*v for k,v in D.items()},b) for D,b in rows]
    stats['admitted_'+mode]+=1
    if any(len(D)>=3 for D,b in labels):stats['one_sided_strict']+=1
    if len(p)<len(T):stats['admitted_nontrivial']+=1
    h=monotone(rows,f,roots,len(T),stats)
    if h is None:return 'NO',None,mode=='GAUGE'
    W=[j for j,D in enumerate(edges) if int(j in M)+sum(v*signs[k]*h[k] for k,v in D.items())==1]
    assert valid(n,T,W) and all((j in W)==bool(v) for j,v in p.items())
    return 'YES',W,mode=='GAUGE'

def valid(n,T,W):
    return len(W)==n and all(len({T[j][c] for j in W})==n for c in range(3))

def ref(n,T,p={}):
    for W in it.product(*[[j for j,t in enumerate(T) if t[0]==x] for x in range(n)]):
        if valid(n,T,W) and all((j in W)==bool(v) for j,v in p.items()):return W
    return None

def run(n,T,stats,p={}):
    assert len(set(T))==len(T) and nx.check_planarity(incidence(n,T))[0]
    P=closure(n,T,p,stats)
    if P is None:return 'CLOSURE_NO',[]
    ans=[]
    for a,b in [(0,1),(0,2),(1,2)]:
        status,W,mixed=lane(n,T,a,b,P,stats);ans.append((status,mixed));stats['lanes_'+status]+=1
    # Paid closure again at stagnation, on identical guarded state.
    if all(x[0]=='UNKNOWN' for x in ans):assert closure(n,T,P,stats)==P
    return ('YES' if any(x[0]=='YES' for x in ans) else 'NO' if any(x[0]=='NO' for x in ans) else 'UNKNOWN'),ans

def prism(k):
    V=list(it.product(range(2),range(2*k))); inc={v:[None]*3 for v in V}; counts=[0]*3
    for r in range(2):
        for i in range(2*k):
            c=i%2; j=counts[c];counts[c]+=1;inc[r,i][c]=inc[r,(i+1)%(2*k)][c]=j
    for i in range(2*k):inc[0,i][2]=inc[1,i][2]=counts[2];counts[2]+=1
    assert len(set(counts))==1
    return counts[0],[tuple(inc[v]) for v in V]

def main():
    stats=collections.Counter();out={};rng=random.Random(20261125);cases=[]
    cube=list(it.product(range(2),repeat=3))
    for mask in range(256):cases.append((2,[t for i,t in enumerate(cube) if mask>>i&1],{}))
    for _ in range(350):
        n=3;T=sorted(rng.sample(list(it.product(range(n),repeat=3)),rng.randrange(7,15)))
        if nx.check_planarity(incidence(n,T))[0]:cases.append((n,T,{}))
    U=[tuple(map(int,s)) for s in '000 002 010 011 021 022 100 101 111 201 202 221'.split()]; V=U+[(1,1,0)]
    for T in (U,V):
        cases.append((3,T,{}));cases.extend((3,T,{j:v}) for j in range(len(T)) for v in (0,1))
    for n,T,p in cases:
        if not nx.check_planarity(incidence(n,T))[0]:continue
        exp=ref(n,T,p); got,lanes=run(n,T,stats,p);stats['cases']+=1;stats['reference_'+('SAT' if exp is not None else 'UNSAT')]+=1;stats['result_'+got]+=1
        assert got=='UNKNOWN' or (got=='YES')==(exp is not None)
        if got=='UNKNOWN' and exp is not None and 'unknown_sat' not in out:out['unknown_sat']={'n':n,'T':T,'pins':p,'witness':exp,'lanes':lanes}
        if got=='UNKNOWN' and exp is None and 'unknown_unsat' not in out:out['unknown_unsat']={'n':n,'T':T,'pins':p,'lanes':lanes}
        if any(m for _,m in lanes) and 'gauge_example' not in out:out['gauge_example']={'n':n,'T':T,'pins':p,'lanes':lanes}
    out['small']=dict(stats);out['named']={}
    for name,T in [('U',U),('V',V)]:out['named'][name]=run(3,T,stats)
    out['prism']=[]
    for k in (3,6,12,24):
        n,T=prism(k)
        for label,Q in [('SAT',T),('UNSAT',[t for j,t in enumerate(T) if j not in (0,3)])]:
            # Delete two nonadjacent opposite-parity vertices, killing both bipartition covers.
            if label=='SAT':assert valid(n,Q,list(range(0,2*k,2))+list(range(2*k+1,4*k,2)))
            else:assert all(any(t[c]==i for t in Q) for c in range(3) for i in range(n))
            got,lanes=run(n,Q,stats);assert got in ('UNKNOWN','YES') if label=='SAT' else got in ('CLOSURE_NO','NO','UNKNOWN')
            out['prism'].append({'k':k,'n':n,'m':len(Q),'truth':label,'result':got,'lanes':lanes})
    out['total']=dict(stats);print(json.dumps(out,indent=2))
if __name__=='__main__':main()
