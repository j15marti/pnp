"""Exact convex-reference containment for polynomially capped projected modes."""
from hall_context import *

def enumerate_modes(D,cap):
    Y=sorted({y for y,z in D});Z={z for y,z in D};out=[];calls=0
    def rec(j,used,M):
        nonlocal calls
        if len(out)>cap:return
        if j==len(Y):out.append(tuple(M));return
        for z in sorted({z for y,z in D if y==Y[j]}-used):
            remY=set(Y[j+1:]);remZ=Z-used-{z};E={e:v for e,v in D.items() if e[0] in remY and e[1] in remZ}
            calls+=1
            if not remY or ({y for y,z in E}==remY and {z for y,z in E}==remZ and pm(E) is not None):rec(j+1,used|{z},M+[(Y[j],z)])
            if len(out)>cap:return
    rec(0,set(),[]);return (None if len(out)>cap else out),calls

def max_demand(D,M,F):
    r=len(M);H=nx.DiGraph();H.add_node('s',demand=-r);H.add_node('t',demand=r)
    for j,e in enumerate(M):
        H.add_edge('s',('p',j),capacity=1,weight=0)
        for x in D[e]:H.add_edge(('p',j),('x',x),capacity=1,weight=-int(x in F));H.add_edge(('x',x),'t',capacity=1,weight=0)
    try:v=nx.min_cost_flow_cost(H);return -v
    except nx.NetworkXUnfeasible:return None

def exact_chart(D,cap=256):
    modes,calls=enumerate_modes(D,cap);st=Counter(enumeration_probes=calls)
    if modes is None:return None,{'overflow':1,**st}
    st['modes']=len(modes);X=set().union(*(set(v) for v in D.values()))
    for ref in modes:
        # Explicit empty-support Hall quota; remove unsupported labels from the ordering test.
        support=set().union(*(set(D[e]) for e in ref));missing=X-support
        Q,typ=interval_quotas({e:{x:i for x,i in v.items() if x in support} for e,v in D.items()},ref)
        if Q is None:continue
        if missing:Q[frozenset(missing)]=0
        st['order_candidates']+=1
        for F,k in Q.items():
            vals=[max_demand(D,M,F) for M in modes];st['quota_queries']+=len(vals)
            if any(v is not None and v>k for v in vals):break
        else:return ref,dict(st)
    return None,dict(st)

def abstract_fixture():
    # Theta projection: exactly two of e0,e1,e2 diagonal, remaining paired with slot3.
    D={(i,i):{x:0 for x in (range(3) if i<2 else [2])} for i in range(3)}
    for i in range(3):D[i,3]={3:0};D[3,i]={4:0}
    ref=[(0,0),(1,1),(2,3),(3,2)];M,c=enumerate_modes(D,10);assert len(M)==3
    assert all(max_demand(D,m,{0,1,2})<=2 for m in M)
    assert set().union(*(footprints(D,m) for m in M))==footprints(D,ref)
    # Occurrences (diag0, owner0),(diag1,owner1),(diag2,owner2) form a triangle of conflicts.
    for a,b in it.combinations(range(3),2):assert any((a,a) in m and (b,b) in m for m in M)
    assert all(not all((i,i) in m for i in range(3)) for m in M)
    Q,typ=interval_quotas(D,ref);assert Q is not None and Q[frozenset(range(3))]==2
    assert transport(D,ref)[0] is None
    triples=dict(enumerate((x,y,z) for (y,z),v in D.items() for x in v))
    return {'modes':len(M),'ref':ref,'exact_footprints':[list(v) for v in sorted(footprints(D,ref))],'planar_incidence':nx.check_planarity(graph(triples,set().union(*(rows(t) for t in triples.values()))))[0],'static_transport_impossible':True}

def main():
    rng=random.Random(26112621);st=Counter();gain=None
    for _ in range(400):
        k=rng.randint(2,4);g=rng.randint(k,k+3);D={(y,z):{x:0 for x in range(g) if rng.random()<.42} for y in range(k) for z in range(k) if y==z or rng.random()<.5};D={e:v for e,v in D.items() if v};ms=phases(D)
        if not ms or len(ms[0])!=k:continue
        ref,stat=exact_chart(D);st['tests']+=1
        F=set().union(*(footprints(D,M) for M in ms))
        if ref is not None:
            assert footprints(D,ref)==F;st['admitted']+=1
            if F and all(certify(D,M)[0]==False for M in ms):
                st['beyond_all_local_relax']+=1
                if gain is None:gain={'D':[[e,sorted(v)] for e,v in D.items()],'ref':ref,'stats':stat}
    scale=[]
    for name,fun,ks in [('FCG17',family,[4,8,16,32,64]),('CC15',cc15,[1,2,4,8])]:
        for k in ks:
            T,R=fun(k);A,B,F,_=close(T,R);assert A;K=set();s=Counter();ok=True
            for D in components(A):
                ref,stat=exact_chart(D);s.update(stat)
                if ref is None:ok=False;break
                K|={i for e in ref for i in D[e].values()}
            if ok:
                V={i:A[i] for i in K};X=[('x',x) for c,x in B if c==0];H=nx.Graph();H.add_nodes_from(X);D=pairs(V);H.add_edges_from((('x',x),('p',e)) for e,v in D.items() for x in v);M=nx.bipartite.maximum_matching(H,top_nodes=X);assert all(x in M for x in X);W=F+[D[M[x][1]][x[1]] for x in X];assert verify(T,R,W)
            scale.append({'family':name,'k':k,'triples':len(T),'admitted':ok,'retained':len(K) if ok else None,'stats':dict(s)})
    print(json.dumps({'abstract':dict(st),'gain':gain,'theta_fixture':abstract_fixture(),'scale':scale},indent=2))
if __name__=='__main__':main()
