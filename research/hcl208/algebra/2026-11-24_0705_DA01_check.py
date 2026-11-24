import itertools as it, random, json, collections
import networkx as nx
R=random.Random(20801)
S=collections.Counter()
# rows (l,u,[(variable,negation)])
def valid(rows,x):
    return all(l<=sum(x[v]^s for v,s in a)<=u for l,u,a in rows)
def close(rows,p):
    p=dict(p)
    while True:
        out=[]; changed=False
        for l,u,a in rows:
            z=sum(p[v]^s for v,s in a if v in p); b=[(v,s) for v,s in a if v not in p]
            l,u=max(0,l-z),min(len(b),u-z)
            if l>u:return None,p
            if l==0 and u==len(b):continue
            if b and (u==0 or l==len(b)):
                v,s=b[0];p[v]=(int(l==len(b))^s);changed=True;S['pins']+=1;break
            out.append((l,u,b))
        if not changed:return out,p
def factor(rows):
    S['factor_calls']+=1
    bounds={i:(l,u) for i,(l,u,a) in enumerate(rows)};occ=collections.defaultdict(list)
    for i,(_,_,a) in enumerate(rows):
        for v,s in a:occ[v].append((i,s))
    edges=[]; decode={}
    for v,o in occ.items():
        i,s=o[0];decode[v]=(len(edges),s)
        if len(o)==1:
            j=len(bounds);bounds[j]=(0,1);edges.append((i,j))
        else:
            assert len(o)==2
            j,t=o[1]
            if s==t:edges.append((i,j))
            else:
                w=len(bounds);bounds[w]=(1,1);edges.extend([(i,w),(w,j)])
    g=nx.Graph();optional=[];slots={}
    for i,(l,u) in bounds.items():
        slots[i]=[('s',i,k) for k in range(u)];g.add_nodes_from(slots[i]);optional+=slots[i][l:]
    if sum(u for l,u in bounds.values())%2:optional.append(('dummy',));g.add_node(('dummy',))
    g.add_edges_from(it.combinations(optional,2))
    for j,(v,w) in enumerate(edges):
        a,b=('e',j,0),('e',j,1);g.add_edge(a,b);g.add_edges_from((a,t) for t in slots[v]);g.add_edges_from((b,t) for t in slots[w])
    S['max_matching_vertices']=max(S['max_matching_vertices'],len(g));S['max_matching_edges']=max(S['max_matching_edges'],g.number_of_edges())
    m=nx.max_weight_matching(g,maxcardinality=True)
    if 2*len(m)!=len(g):return None
    mate={a:b for e in m for a,b in [e,e[::-1]]}
    return {v:int(mate[('e',j,0)]!=('e',j,1))^s for v,(j,s) in decode.items()}

def terminal(rows,p=None):
    reduced,p=close(rows,p or {})
    if reduced is None:return None
    occ=collections.Counter(v for _,_,a in reduced for v,s in a);high={v for v,d in occ.items() if d>2}
    # Remove high-variable nodes from incidence graph. Factor components are rows.
    G=nx.Graph();G.add_nodes_from(range(len(reduced))); seen={}
    for i,(_,_,a) in enumerate(reduced):
        for v,s in a:
            if v not in high:
                if v in seen:G.add_edge(i,seen[v])
                seen[v]=i
    tables=[]
    for ids in nx.connected_components(G):
        rr=[reduced[i] for i in sorted(ids)];scope=tuple(sorted({v for _,_,a in rr for v,s in a if v in high}));table={}
        for b in it.product(range(2),repeat=len(scope)):
            pp=dict(zip(scope,b));r,pp=close(rr,pp)
            S['boundary_rows']+=1
            if r is None:continue
            x=factor(r)
            if x is not None:
                x={**pp,**x};assert valid(rr,collections.defaultdict(int,x));table[b]=x
        if not table:return None
        tables.append((scope,table))
    # Arity-two boundary terminal: each forbidden tuple becomes one 2-CNF clause.
    if all(len(s)<=2 for s,t in tables):
        S['binary_terminals']+=1
        g=nx.DiGraph();g.add_nodes_from((v,b) for v in high for b in range(2))
        for s,t in tables:
            for b in it.product(range(2),repeat=len(s)):
                if b in t:continue
                assert s
                a=(s[0],b[0]);d=(s[-1],b[-1]);g.add_edge(a,(d[0],1-d[1]));g.add_edge(d,(a[0],1-a[1]))
        cc=list(nx.strongly_connected_components(g));idx={z:i for i,c in enumerate(cc) for z in c}
        if any(idx[v,0]==idx[v,1] for v in high):return None
        rank={u:i for i,u in enumerate(nx.topological_sort(nx.condensation(g,cc)))}
        x={**p,**{v:int(rank[idx[v,1]]>rank[idx[v,0]]) for v in high}}
        for s,t in tables:
            y=t[tuple(x[v] for v in s)];assert all(k not in x or x[k]==z for k,z in y.items());x.update(y)
        return x
    # Exact Boolean variable elimination; min current union size, keep actual witnesses.
    H=set(high)
    while H:
        v=min(H,key=lambda v:(len(set().union(*(set(s) for s,t in tables if v in s))),v));H.remove(v)
        active=[(s,t) for s,t in tables if v in s];tables=[(s,t) for s,t in tables if v not in s]
        scope=tuple(sorted(set().union(*(set(s) for s,t in active))));out=tuple(u for u in scope if u!=v);table={}
        S['max_bag']=max(S['max_bag'],len(scope))
        for b in it.product(range(2),repeat=len(scope)):
            S['join_rows']+=1;d=dict(zip(scope,b));x={};ok=True
            for s,t in active:
                y=t.get(tuple(d[u] for u in s))
                if y is None:ok=False;break
                assert all(k not in x or x[k]==z for k,z in y.items());x.update(y)
            if ok:table[tuple(d[u] for u in out)]=x
        if not table:return None
        tables.append((out,table))
    x=dict(p)
    for s,t in tables:
        assert not s
        assert all(k not in x or x[k]==z for k,z in t[()].items());x.update(t[()])
    return x

def check(n,rows,p=None):
    p=p or {};a=terminal(rows,p);b=None
    for bits in it.product(range(2),repeat=n):
        S['reference_assignments']+=1
        if all(bits[v]==z for v,z in p.items()) and valid(rows,bits):b=bits
    assert (a is None)==(b is None),(rows,p,a,b)
    if a is not None:
        a=collections.defaultdict(int,a);assert valid(rows,a) and all(a[v]==z for v,z in p.items())
    S['checks']+=1;S['sat' if a is not None else 'unsat']+=1

def nae(es):return [(1,2,[(v,0) for v in e]) for e in es]
if __name__=='__main__':
    for z in range(150):
        n=R.randrange(3,9);rows=[]
        for j in range(R.randrange(1,8)):
            a=[(v,R.randrange(2)) for v in R.sample(range(n),R.randrange(1,min(4,n)+1))];l=R.randrange(len(a)+1);u=R.randrange(l,len(a)+1);rows.append((l,u,a))
        check(n,rows)
        v=R.randrange(n)
        for b in range(2):check(n,rows,{v:b})
    f=nae([(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)])
    check(7,f)
    for i,(_,_,a) in enumerate(f):
        for l,u in [(0,2),(1,3)]:check(7,f[:i]+[(l,u,a)]+f[i+1:])
    # Cubic dual of prism graphs: one variable per edge, each occurs twice.
    scaling=[]
    for h in [3,5,10,20,40]:
        G=nx.circular_ladder_graph(h);E=list(G.edges());rr=nae([tuple(i for i,e in enumerate(E) if v in e) for v in G]);before=S['factor_calls'];x=terminal(rr);assert x is not None and valid(rr,collections.defaultdict(int,x));scaling.append({'variables':len(E),'constraints':len(rr),'high':0,'factor_calls':S['factor_calls']-before})
    # Odd cycle exact-one, LP x=1/2 feasible but integral impossible; neighbor SAT.
    for h in [3,5,7,9]:
        rr=[(1,1,[(i,0),((i+1)%h,0)]) for i in range(h)];check(h,rr);check(h,rr[:-1]+[(0,1,rr[-1][2])])
    # All high variables, dense binary torso, no bounded-width promise.
    for h in [8,16,32]:
        for hostile in [False,True]:
            rr=[(1,1,[(i,0),(j,1)]) for i in range(h) for j in range(i+1,h)]
            if hostile:rr[0]=(1,1,[(0,0),(1,0)])
            before=S['factor_calls'];x=terminal(rr);assert (x is None)==hostile
            if x is not None:assert valid(rr,collections.defaultdict(int,x))
            scaling.append({'variables':h,'constraints':len(rr),'high':h,'sat':not hostile,'factor_calls':S['factor_calls']-before,'torso':'complete'})
    print(json.dumps({'seed':20801,'networkx':nx.__version__,'counts':dict(S),'scaling':scaling},indent=2))
