# Run beside AGE08 audit.py (renamed age08.py), exact dependency in report.
import itertools as I, math, json, networkx as nx
from age08 import graph, close, chart, hull, clauses, model, U, V, ring, solve_ref

def saturate(T,n,c,d):
    k,B,P,L,edge,lo,ids=chart(T,n,c,d);R=hull(B,k);assert R is not None
    while True:
        old=R
        for Lz in L:
            A=None;B=clauses(R)
            for j in Lz:
                Q=hull(B+sum((P[e][int(e==j)] for e in Lz),[]),k)
                if Q is not None:A=Q if A is None else tuple(a&b for a,b in zip(A,Q))
            if A is None:return None
            R=A
        if R==old:break
    return k,clauses(R),P,L,edge,lo,ids

def solve(T,n,c,d,cap=100000,saturated=True):
    ch=saturate(T,n,c,d) if saturated else chart(T,n,c,d)
    if ch is None:return {'status':'NO','reason':'hull'}
    k,B,P,L,edge,lo,ids=ch;R=hull(B,k);assert R is not None
    hi=dict(lo)
    for f,t in ids:hi[f]=max(hi[f],t)
    def pins(f,h):
        out=[]
        if (f,h) in ids:out.append(2*ids[f,h])
        if (f,h+1) in ids:out.append(2*ids[f,h+1]+1)
        return frozenset(out)
    def compatible(A,C=frozenset()):
        S=A|C
        return all(not (R[a]>>(b^1)&1) for a in S for b in S)
    D=[z for z,Lz in enumerate(L) if hull(B+sum((P[e][0] for e in Lz),[]),k) is not None]
    E=[z for z,Lz in enumerate(L) if any(hull(B+P[e][1]+P[f][1],k) is not None for e,f in I.combinations(Lz,2))]
    opts={}
    for z in D:
        A=set()
        for e in L[z]:
            l,r,m=edge[e]
            for hr in range(lo[r],hi[r]+1):
                hl=hr+1-m
                if lo[l]<=hl<=hi[l]:
                    p=pins(l,hl)|pins(r,hr)
                    if compatible(p):A.add((e,tuple(sorted(p))))
        opts[z]=sorted(A)
        if not A:return {'status':'NO','reason':'empty option'}
    H=nx.Graph();H.add_nodes_from(D);bad={}
    for z,w in I.combinations(D,2):
        F={(i,j) for i,(_,p) in enumerate(opts[z]) for j,(_,q) in enumerate(opts[w]) if not compatible(frozenset(p),frozenset(q))}
        if F:H.add_edge(z,w);bad[z,w]=F
    def ok(z,i,w,j):return (i,j) not in bad.get((z,w),set()) if z<w else (j,i) not in bad.get((w,z),set())
    assignment={};work=0;blocks=[];unknown=False
    for C in nx.connected_components(H):
        C=sorted(C);prod=math.prod(len(opts[z]) for z in C);tree=nx.is_tree(H.subgraph(C));blocks.append([len(C),prod,tree]);sol=None
        if tree:
            parent={C[0]:None};order=[C[0]]
            for z in order:
                for w in H[z]:
                    if w not in parent:parent[w]=z;order.append(w)
            valid={};pick={}
            for z in reversed(order):
                valid[z]=[]
                for i in range(len(opts[z])):
                    choices={};good=True
                    for w in H[z]:
                        if parent.get(w)!=z:continue
                        j=next((j for j in valid[w] if ok(z,i,w,j)),None);work+=len(valid[w])
                        if j is None:good=False;break
                        choices[w]=j
                    if good:valid[z].append(i);pick[z,i]=choices
            if valid[C[0]]:
                sol={C[0]:valid[C[0]][0]}
                for z in order:sol.update(pick[z,sol[z]])
        else:
            width,TD=nx.approximation.treewidth_min_fill_in(H.subgraph(C))
            bags=list(TD);assert nx.is_tree(TD)
            assert set.union(*(set(b) for b in bags))==set(C)
            assert all(any(z in b and w in b for b in bags) for z,w in H.subgraph(C).edges)
            assert all(nx.is_connected(TD.subgraph([b for b in bags if z in b])) for z in C)
            bp=max(math.prod(len(opts[z]) for z in b) for b in bags);blocks[-1]+=[width,bp]
            if bp>cap:unknown=True;continue
            parent={bags[0]:None};order=[bags[0]]
            for b in order:
                for a in TD[b]:
                    if a not in parent:parent[a]=b;order.append(a)
            msg={};records={};sep={b:sorted(b & parent[b]) if parent[b] is not None else [] for b in order}
            for b in reversed(order):
                msg[b]={};vs=sorted(b)
                for values in I.product(*(range(len(opts[z])) for z in vs)):
                    work+=1;S=dict(zip(vs,values))
                    if any(not ok(z,S[z],w,S[w]) for z,w in H.subgraph(b).edges):continue
                    if any(tuple(S[z] for z in sep[a]) not in msg[a] for a in TD[b] if parent.get(a)==b):continue
                    key=tuple(S[z] for z in sep[b]);msg[b].setdefault(key,S)
            if () in msg[order[0]]:
                sol={}
                for b in order:sol.update(msg[b][tuple(sol[z] for z in sep[b])])
        if sol is None:return {'status':'NO','reason':'factor','D':len(D),'E':len(E),'blocks':blocks}
        assignment.update(sol)
    result={'status':'UNKNOWN' if unknown else 'YES','D':len(D),'E':len(E),'old_product':math.prod(len(L[z]) for z in E),'options':sum(map(len,opts.values())),'raw_product':math.prod(map(len,opts.values())),'blocks':blocks,'work':work}
    if unknown:return result
    PINS=frozenset(a for z,i in assignment.items() for a in opts[z][i][1]);assert compatible(PINS)
    vals=model(B+[(a,a) for a in PINS],k);h=dict(lo)
    for (f,t),i in ids.items():h[f]+=vals[i]
    W=[j for j,(l,r,m) in enumerate(edge) if m+h[l]-h[r]==1]
    assert len(W)==n and all(len({T[j][q] for j in W})==n for q in range(3))
    result['witness']=W;return result

def chain(k):
    base=[(0,0,0),(1,1,1),(0,0,1),(1,1,0),(0,1,0),(1,0,1)]
    T=[tuple(2*i+v for v in t) for i in range(k) for t in base]
    for i in range(k-1):
        a=6*i+2*(i%2)+1;b=6*(i+1)+2*(i%2);x=list(T[a]);y=list(T[b]);x[1],y[1]=y[1],x[1];T[a]=tuple(x);T[b]=tuple(y)
    return T

def test(T,n):
    G=graph(T,n);assert nx.check_planarity(G)[0] and len(set(T))==len(T)
    S=close(T,n)
    if S is None:return {'status':'NO','closure':'NO'}
    R=[T[j] for j in S];out=[solve(R,n,c,d) for c,d in I.combinations(range(3),2)]
    for a in out:
        if 'witness' in a:a['witness']=[S[j] for j in a['witness']]
    return {'closure':'stagnant' if len(S)==len(T) else 'reduced','connected':nx.is_connected(G),'jobs':out}

def octsplice(k):
    base=list(I.product(range(2),repeat=3));T=[tuple(2*i+v for v in t) for i in range(k) for t in base]
    for i in range(k-1):
        p=8*i+7;q=8*(i+1);u=list(T[p]);v=list(T[q]);u[1],v[1]=v[1],u[1];T[p]=tuple(u);T[q]=tuple(v)
    return T

if __name__=='__main__':
    O={}
    for name,T,n in [('U',U,3),('V',V,3),('oct',list(I.product(range(2),repeat=3)),2)]:O[name]=test(T,n)
    for k in (2,4,8):O['chain'+str(k)]=test(chain(k),2*k)
    for k in (2,4):O['ring'+str(k)]=test(ring(k),3*k)
    for k in (2,4):
        T=chain(k);O['delete'+str(k)]=test(T[1:],2*k);O['zero'+str(k)]=test([t for t in T if t[0]!=0],2*k)
    for k in (2,4,8):O['octsplice'+str(k)]=test(octsplice(k),2*k)
    for k in (16,32):
        T=octsplice(k);G=graph(T,2*k);assert nx.check_planarity(G)[0] and nx.is_connected(G) and len(set(T))==len(T)
        assert close(T,2*k)==list(range(len(T)))
        O['octsplice_xz'+str(k)]=solve(T,2*k,0,2)
    print(json.dumps(O,indent=2))
