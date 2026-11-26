"""Mixed orientations: exact global DD-cover size obstruction in all lanes.
Same series-cycle solver, no target-supplied orientation or solution in solver.
"""
from cycle import *
from strengthen import strengthen

def mixed(r):
    k=3*r;e=BASE[0]
    def move(t,i):
        p=[None]*3
        for j in range(3):
            c=(j+i%3)%3
            p[c]=3*((i+1)%k)+e[(1-(i+1)%3)%3] if t==e and c==1 else 3*i+t[j]
        return tuple(p)
    return tuple(sorted(move(t,i) for i in range(k) for t in BASE)),3*k,lambda w:tuple(move(t,i) for i in range(k) for t in w)
def mixed_test(r,guard=False):
    T,n,move=mixed(r);k=3*r; E=a.old.Engine();R,_=E.closure(T,n);assert R==T
    assert a.old.check(T,n) and nx.is_connected(a.old.incidence(T,n));covers=[move(w) for w in W];assert all(a.old.verify(T,n,w) for w in covers);assert set(T)==set().union(*map(set,covers))
    obs=[]
    for c in range(3):
        J=a.prev.Join(T,n,c,E,'reference');P=J.ports;words=[]
        for w in covers:
            p={}
            for t in w:p.update(J.tuplepins(t))
            words.append(p)
        hard=[]
        for i in range(k):
            if i%3!=c:continue
            Q=[p for p in P if p[1]//3==i];ww=[tuple(w[p] for p in Q) for w in words];assert len(set(ww))==4
            bad=tuple(a.dd(*v) for v in zip(*ww[1:]));assert bad not in ww
            hard.append(dict(block=i,words=ww,false=bad))
        row=dict(center=c,hard=len(hard),first=hard[0])
        if guard:
            A=a.Join(J);stats=strengthen(A);q={p:a.dd(*(words[i][p] for i in (1,2,3))) for p in P}
            assert A.C.valid and A.C.solve(list(q.items())) is not None and J.lift(q) is None
            row['guard']=dict(stats)
        obs.append(row)
    res=solve(T,n);assert res['decision']=='YES' and sum(res['counts'])==1+3**k
    res.pop('witness');return dict(r=r,m=len(T),obstructions=obs,solver=res,cover_lower_bound=(3**r+2**r-1)//2**r)
if __name__=='__main__':print(json.dumps([mixed_test(r,guard=(r<=2)) for r in (1,2,4,8,16,32)]))
