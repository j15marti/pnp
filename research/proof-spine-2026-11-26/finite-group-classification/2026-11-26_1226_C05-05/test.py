import itertools as it,random,json
from collections import Counter
import networkx as nx
from prefix import *
from prior import cover
from prev17 import close
Lcap=[(1,0,1),(2,1,0),(2,1,1),(0,1,1),(2,0,0)]
Ucap=[(1,1,2),(2,0,0),(2,2,1),(2,1,2),(0,2,1)]
def family(k,nested=True,mixed=False):
    order=[(j,0) for j in range(k)]+[(j,p) for j in reversed(range(k)) for p in (1,2,3)] if nested else [(j,p) for j in range(k) for p in range(4)]
    pos={v:i for i,v in enumerate(order)};m=len(order);T={};parts=[];R=set()
    for i,(j,p) in enumerate(order):
        ty=(p%2)^int(mixed and j%2==1);V=Ucap if ty else Lcap
        # A edges with previous and next; B pairs p0/1, p2/3; C pairs p1/2, p3/0.
        A=[(i-1)%m,i,m+i];B=[2*j+p//2,m+2*i,m+2*i+1];C=[2*j+((p+1)%4)//2,m+2*i,m+2*i+1]
        if mixed and j%2==1:A[0],A[1]=A[1],A[0]
        maps=[A,B,C];ids=[]
        for tup in V:
            t=tuple(maps[c][v] for c,v in enumerate(tup));q=len(T);T[q]=t;ids.append(q);R|=rows(t)
        parts.append(ids)
    assert len(set(T.values()))==len(T);assert len({sum(c==i for c,v in R) for i in range(3)})==1
    assert nx.check_planarity(graph(T,R))[0],(k,nested,mixed)
    assert nx.is_connected(graph(T,R));return T,R,parts

def run(T,R,P,delete=()):
    A={i:t for i,t in T.items() if i not in delete};C,B,F,st=close(A,R)
    if C is None:return 'NO',None,{'native_closure':'NO'}
    z=tables(T,R,P,C,F);assert z is not None
    tab,inc=z;lab,W,s=exact_join(tab,inc)
    if W is not None:assert verify(A,R,W)
    if len(tab)<=32:
        truth=phase_flow(tab,inc)
        if lab!='UNKNOWN':assert (lab=='YES')==truth,(lab,truth,s)
    return lab,W,{**s,'native_live':len(C),'fixed':len(F)}

def main():
    rng=random.Random(26112605);ctr=Counter();examples=[]
    for _ in range(1200):
        n=rng.randrange(0,9);c={i:rng.randrange(-7,8) for i in range(n)};b=rng.randrange(-12,20);cl,e,ok=threshold(c,b)
        actual=set();hull=set()
        for x in it.product(range(2),repeat=n):
            if sum(c[i]*x[i] for i in c)<=b:actual.add(x)
            if ok and all(any(x[l//2]==l%2 for l in q) for q in cl):hull.add(x)
        assert actual<=hull and e==(actual==hull);ctr['threshold_checks']+=1;ctr['exact']+=e
    scale=[]
    for k in [2,4,8,16,32,64]:
        for nested in [False,True]:
            T,R,P=family(k,nested);lab,W,s=run(T,R,P);assert lab=='YES';scale.append({'k':k,'nested':nested,'m':len(T),'status':lab,'witness':W,**s})
    guarded=[]
    for k in [2,3,4]:
        for mixed in [False,True]:
            T,R,P=family(k,True,mixed)
            for _ in range(30):
                D=sorted(rng.sample(list(T),rng.randrange(0,7)));lab,W,s=run(T,R,P,D);guarded.append({'k':k,'mixed':mixed,'delete':D,'status':lab,**s});ctr['guard_'+lab]+=1
    # Native neighbors: restrict to a verified complete witness plus one extra, then delete one selected tuple not in extra. All guards actual IDs.
    neighbors=[]
    for k in [2,4,8,16,32]:
        T,R,P=family(k);lab,W,s=run(T,R,P);extra=next(i for i in T if i not in W);drop=next(i for i in W if not rows(T[i])&rows(T[extra]));D=set(T)-set(W)-{extra}
        a,Wa,sa=run(T,R,P,D);b,Wb,sb=run(T,R,P,D|{drop});assert a=='YES' and b=='NO';neighbors.append({'k':k,'m':len(T),'sat_deleted':sorted(D),'no_extra_deletion':drop,'yes':sa,'no':sb,'witness':Wa})
    # Mixed nested family demonstrates nonbijunctive *individual inequalities* even on actual planar charts.
    T,R,P=family(3,True,True);tab,inc=tables(T,R,P);cons,w=constraints(tab,cycle_data(tab,inc));ob=[(c,b) for c,b in cons if not threshold(c,b)[1]];assert ob
    print(json.dumps({'counts':ctr,'scale':scale,'guards':guarded,'neighbors':neighbors,'native_nonbijunctive_inequality':ob[0]},indent=2))
if __name__=='__main__':main()
