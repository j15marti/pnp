"""Exact protected Rado / quotient direct-sum summaries. Python 3.
Run PYTHONPATH=prior PYTHONHASHSEED=0 python protected08.py > results08.json.
Dependencies: C05_07 archive, networkx/scipy (native closure).
"""
from hostile07 import cubes,seam
from direct07 import *
from collections import defaultdict,deque

def span(V):
    B={}
    for v in V: insert(v,0,B)
    return B

def vecs(B):return [v for v,c in B.values()]
def basis(V):
    B={};out=[]
    for v in V:
        if reduce_vec(v,B)[0]:insert(v,0,B);out.append(v)
    return out

def intersection(A,B):
    # Relations between basis of A and independent basis of B, tracking A part.
    D={};out=[]
    for v in basis(A):insert(v,v,D)
    for v in basis(B):
        w,t=reduce_vec(v,D)
        if w:insert(w,t,D)
        elif t:out.append(t)
    return basis(out)

def relative(G,W):
    WB=span(W);P=list(G);V=[(u,v,u^v) for u,v in P];I={};probes=0
    while True:
        B={}
        for j,v in I.items():assert insert(reduce_vec(v,WB)[0],1<<j,B)
        parents={j:None for j in range(len(P)) if j not in I};Q=deque(parents);end=None
        while Q and end is None:
            j=Q.popleft()
            for v in V[j]:
                probes+=1;w,c=reduce_vec(reduce_vec(v,WB)[0],B)
                if w:end=j,v;break
                while c:
                    t=c&-c;c^=t;k=t.bit_length()-1
                    if k not in parents:parents[k]=(j,v);Q.append(k)
        if end is None:break
        j,v=end
        while True:
            I[j]=v
            if parents[j] is None:break
            j,v=parents[j]
    C={P[j]:G[P[j]] for j in parents};ext={P[j]:v for j,v in I.items() if j not in parents}
    CB=span([*W,*(v for p in C for v in p)])
    # Certificate for all exterior extensions, independent of maximality.
    for p,v in ext.items():assert reduce_vec(v,CB)[0];insert(v,0,CB)
    assert len(C)+len(ext)==len(G)
    return C,ext,probes

def components(C,W):
    # Every factor is tied to ALL coordinates of its quotient span in one
    # common independent basis. This handles higher-order dependencies.
    B=span(W);Q=basis(reduce_vec(v,B)[0] for p in C for v in p);D={}
    for i,v in enumerate(Q):insert(v,1<<i,D)
    H=nx.Graph();P=list(C)
    for j,p in enumerate(P):
        H.add_node(('p',j))
        for v in p:
            z,c=reduce_vec(reduce_vec(v,B)[0],D);assert not z
            while c:
                a=c&-c;c^=a;H.add_edge(('p',j),('q',a.bit_length()-1))
    out=[{P[j]:C[P[j]] for kind,j in S if kind=='p'} for S in nx.connected_components(H)]
    # Independent certificate: rank sum in quotient equals rank of union.
    assert sum(len(span(reduce_vec(v,B)[0] for p in J for v in p)) for J in out)==len(Q)
    return out

def summarize(G,W,cap=8,peel=True):
    C,E,probes=relative(G,W) if peel else (G,{},0);records=[];checks=0
    J=components(C,W)
    ranks=[len(span(v for p in K for v in p)) for K in J]
    st={'protected_rank':len(span(W)),'core_factors':len(C),'exterior':len(E),'components':len(J),'max_local_rank':max(ranks,default=0),'probes':probes,'words':0}
    for K,r in zip(J,ranks):
        if r>cap:return None,st
        A=basis(v for p in K for v in p);S=intersection(A,W);Q=basis(S+A);assert len(Q)==r
        D={}
        for i,v in enumerate(Q):insert(v,1<<i,D)
        kp={p:tuple(reduce_vec(v,D)[1] for v in p) for p in K};R={}
        for y in range(1<<r):
            st['words']+=1
            if all(tuple(parity(y&v) for v in a)!=K[p] for p,a in kp.items()):R.setdefault(y&((1<<len(S))-1),y)
        records.append((S,Q,R))
    st['max_effective_rank']=max((len(s) for s,q,r in records),default=0)
    return (records,E),st

def table_eq(S,R):
    if not R:return None
    eq=[]
    for a in range(1,1<<len(S)):
        z={parity(a&y) for y in R}
        if len(z)==1:
            v=0
            for i,u in enumerate(S):
                if a>>i&1:v^=u
            eq.append((v,next(iter(z))))
    return eq

def join(summaries,W,n,b,cap=8,peel=False):
    records=[r for rec,E in summaries for r in rec];eq=[];non=[];bad=[];admitted=True
    for j,(S,Q,R) in enumerate(records):
        a=table_eq(S,R)
        if a is None:return 'NO',None,{'reason':'empty local response'}
        eq+=a
        if len(R)!=(1<<(len(S)-len(span(v for v,c in a)))):
            non.append((S,R))
            # exact hull-minus-one on a plane, NOT hull substitution
            D={}
            for i,v in enumerate(S):insert(v,1<<i,D)
            aa=[(reduce_vec(v,D)[1],c) for v,c in a]
            missing=[y for y in range(1<<len(S)) if y not in R and all(parity(v&y)==c for v,c in aa)]
            if len(S)-len(span(v for v,c in a))==2 and len(missing)==1:
                bad.append((j,[(v,missing[0]>>i&1) for i,v in enumerate(S)]))
            else:admitted=False
    B={}
    for v,c in list(b.values())+eq:
        if not insert(v,c,B):return 'NO',None,{'reason':'inconsistent affine responses'}
    V=basis(reduce_vec(v,B)[0] for S,R in non for v in S);nr=len(V);ext=[];st={}
    if len(V)>cap and peel and admitted:
        B,G,_,_=normal(list(B.values()),bad)
        if B is None:return 'NO',None,{'reason':'exact summary normalization'}
        I,C,st=rado(G);V=basis(v for p in C for v in p)
        ext=[(v,rep_value(p,G[p],v)) for p,v in I.items() if p not in C]
    if len(V)>cap:return 'UNKNOWN',None,{'nonaffine_rank':nr,'remaining_rank':len(V),'second_rado':st}
    tests=0
    for y in range(1<<len(V)):
        tests+=1
        x=solve_eq(list(B.values())+[(v,y>>i&1) for i,v in enumerate(V)]+ext,n);assert x is not None
        if all(sum(parity(x&v)<<i for i,v in enumerate(S)) in R for S,R in non):break
    else:return 'NO',None,{'nonaffine_rank':nr,'remaining_rank':len(V),'join_words':tests,'second_rado':st}
    # Choose coherent evaluations of all W; lift each component using its
    # actual table witness, and satisfy every exterior factor via its rep.
    L=list(b.values())+[(v,parity(x&v)) for v in W]
    for rec,E in summaries:
        for S,Q,R in rec:
            z=sum(parity(x&v)<<i for i,v in enumerate(S));assert z in R;y=R[z]
            L.extend((v,y>>i&1) for i,v in enumerate(Q))
        # G bad values injected below by caller in E pairs
        L.extend(E)
    z=solve_eq(L,n);assert z is not None
    return 'YES',z,{'nonaffine_rank':nr,'remaining_rank':len(V),'response_equations':len(eq),'join_words':tests,'second_rado':st}

def side(G,W,cap,peel):
    H,s=summarize(G,W,cap,peel)
    if H is None:return None,s
    rec,E=H
    return (rec,[(v,rep_value(p,G[p],v)) for p,v in E.items()]),s

def partition(F,n,ids,T,G,b):
    H=nx.Graph();H.add_edges_from(((1,y),(2,z)) for x,y,z in T.values());blocks=sorted(nx.connected_components(H),key=min)
    loc={r:j for j,S in enumerate(blocks) for r in S};group={}
    eq,bad=aff_comp(F)
    for j,raw in bad:
        D={}
        for v,c in raw:
            u,a=reduce_vec(v,b)
            if not insert(u,c^a,D):break
        else:
            if len(D)!=2:continue
            (u,a),(v,c)=D.values();p=tuple(sorted((u,v,u^v))[:2]);d={u:a,v:c,u^v:a^c}
            if p in G and tuple(d[t] for t in p)==G[p]:
                actual=[ids[i] for i in F[j][0] if i<len(ids)];assert actual
                k=loc[1,T[actual[0]][1]] if len(blocks)>1 else j
                group.setdefault(p,k%2)
    assert set(group)==set(G)
    return [{p:G[p] for p in G if group[p]==k} for k in range(2)]

def native(T,R,delete,tag,cap=8):
    enc=json.dumps([sorted(T.items()),sorted(R),sorted(delete)],separators=(',',':'));o={'tag':tag,'m':len(T),'N':8*len(enc),'sha256':hashlib.sha256(enc.encode()).hexdigest(),'delete':sorted(delete)}
    assert nx.check_planarity(graph(T,R))[0] and len(T)==len(set(T.values()))
    live,own,fixed,_=close({i:t for i,t in T.items() if i not in delete},R)
    if live is None:return {**o,'A':'NO','B':'NO','C':'NO','I':'NO','closure':'NO'}
    if not own:assert verify({i:t for i,t in T.items() if i not in delete},R,fixed);return {**o,'A':'YES','B':'YES','C':'YES','I':'YES','closure':'YES','witness':fixed}
    F,n,ids=chain(live,own);eq,bad=aff_comp(F);b,G,_,_=normal(eq,bad)
    a,x,sa,_=rado_solve(F,n,cap);c,z,sc=elim(F,n,4)
    o.update(A=a,C=c,astats=sa,cstats=sc,closure='OPEN')
    if b is None:return {**o,'B':'NO','I':'NO'}
    P=partition(F,n,ids,live,G,b);W=intersection([v for p in P[0] for v in p],[v for p in P[1] for v in p]);o['cut_rank']=len(W)
    # B = direct-sum summary without peeling; integrated adds relative Rado.
    for key,peel in [('B',False),('I',True)]:
        ss=[];stats=[]
        for H in P:
            q,s=side(H,W,cap,peel);ss.append(q);stats.append(s)
        if any(q is None for q in ss):lab,w,t='UNKNOWN',None,{}
        else:lab,w,t=join(ss,W,n,b,cap,peel)
        o[key]=lab;o[key+'stats']={'sides':stats,'join':t}
        if lab=='YES':
            assert all(tuple(w>>i&1 for i in S) in U for S,U in F)
            wit=fixed+[i for j,i in enumerate(ids) if w>>j&1];assert verify({i:t for i,t in T.items() if i not in delete},R,wit);o[key+'witness']=wit
        l2,r2,w2,_=close({i:t for i,t in T.items() if i not in delete},R);assert l2==live and r2==own and set(w2)==set(fixed)
    assert len({o[k] for k in ('A','B','C','I') if o[k]!='UNKNOWN'})<=1
    return o

def abstract():
    rng=random.Random(26112608);stats=Counter()
    for _ in range(400):
        n=rng.randrange(2,8);G={}
        for j in range(rng.randrange(1,10)):
            u,v=rng.sample(range(1,1<<n),2);p=tuple(sorted((u,v,u^v))[:2]);G[p]=tuple(rng.randrange(2) for _ in range(2))
        W=basis(rng.randrange(1,1<<n) for _ in range(rng.randrange(n+1)));H,s=summarize(G,W);assert H is not None
        rec,E=H
        for x in range(1<<n):
            # compare exact protected projection by independently enumerating all full assignments
            if x==0:truth={tuple(parity(z&v) for v in W) for z in range(1<<n) if support(G,z)}
            pred=all(sum(parity(x&v)<<i for i,v in enumerate(S)) in R for S,Q,R in rec)
            assert pred==(tuple(parity(x&v) for v in W) in truth);stats['word_checks']+=1
        stats['cases']+=1;stats['peeled']+=s['exterior'];stats['components']+=s['components']
    # Pairwise intersection zero is NOT joint directness: 3 lines a,b,a+b.
    assert not intersection([1],[2]) and not intersection([1],[3]) and not intersection([2],[3]);assert len(span([1,2,3]))==2
    A,B,C=[1,2],[4,8],[5,10]
    assert not intersection(A,B) and not intersection(A,C) and not intersection(B,C)
    assert len(span(A+B+C))==4 and solve_eq([(1,0),(2,0),(4,0),(8,0),(5,1),(10,0)],4) is None
    stats['higher_order_counterexample']=1
    return dict(stats)

def main():
    out=[]
    for k in [1,2,4,8,16,32,64]:
        T,R=cubes(k);o=native(T,R,[],f'cube_chain_{k}');assert o['I']!='NO';out.append(o)
        if k in [2,4,8,16,32]:
            D={8*(k-1)+i for i in (1,2,3)}
            for q,ds in [('yes',D),('no',D|{0})]:
                a,w,s=seam(T,R,ds);assert a.upper()==q.upper();j=native(T,R,ds,f'cube_{k}_{q}');assert j['I'] in (a,'UNKNOWN');out.append(j)
    for k in [2,4,8,16,32]:
        T,R,P=family(k,True,True);out.append(native(T,R,[],f'mixed_{k}'))
    for k in [8,16,32]:
        T,R=cubes(k);U,S,P=family(k,True,True);off=max(T)+1;shift=max(v for c,v in R)+1
        T.update({i+off:tuple(v+shift for v in t) for i,t in U.items()});R|={(c,v+shift) for c,v in S}
        x,y,z=T[0];u,v,w=T[off];T[0]=(u,y,z);T[off]=(x,v,w)
        assert nx.is_connected(graph(T,R)) and nx.check_planarity(graph(T,R))[0]
        o=native(T,R,[],f'hybrid_{k}');assert o['I']=='YES'
        L,B,W,_=close(T,R);F,n,ids=chain(L,B);a,b,c=elim(F,n,8);o['C8']=a;o['C8stats']=c
        if a=='YES':assert verify(T,R,W+[i for j,i in enumerate(ids) if b[j]])
        out.append(o)
    R=owners(2);T0=dict(enumerate(it.product(range(2),repeat=3)))
    for mask in range(256):
        T={i:t for i,t in T0.items() if mask>>i&1};o=native(T,R,[],f'cube_{mask}');truth=any(len(set().union(*(rows(T[i]) for i in W)))==6 for W in it.combinations(T,2));assert all(o[k]=='UNKNOWN' or (o[k]=='YES')==truth for k in ['A','B','C','I']);out.append(o)
    print(json.dumps({'abstract':abstract(),'native':out},indent=2))
if __name__=='__main__':main()
