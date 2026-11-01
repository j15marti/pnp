#!/usr/bin/env python3
"""ARC-ODD-CYCLE-BUDGET293. Standalone restricted certified cube gate.
All source clauses remain indexed; no semantic labels are assumed free.
Python 3 stdlib; output JSON. The full raw S/U, XOR and verifier are
also in ARC_ODD_CYCLE_BUDGET293_reproducibility.zip.
"""
import json
from collections import Counter,defaultdict
from itertools import product

F=(
(1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),
(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15),
(-1,-2,-11),(-2,-3,-11),(-1,-3,-12),(-4,-5,-13),(-5,-6,-14),
(-4,-6,-15),(-7,-8,-12),(-8,-9,-13),(-9,-10,-14),(-10,-7,-15))
N=15
PU=(-1,)*6+(0,)*4+(1,)*5
PS=(-1,)*6+(0,)*4+(0,)+(1,)*4
W=(0,1,1,1,0,0,0,0,0,0,0,1,1,1,1)

def grammar(F,n=N):
    if n==0 or n%3 or 3*len(F)!=4*n:return False
    counts=Counter();seen=set()
    for c in F:
        if len(c)!=3 or len({abs(x) for x in c})!=3:return False
        if not all(x>0 for x in c) and not all(x<0 for x in c):return False
        if any(abs(x)<1 or abs(x)>n for x in c):return False
        k=tuple(sorted(c))
        if k in seen:return False
        seen.add(k);counts.update(c)
    return all(counts[i]==counts[-i]==2 for i in range(1,n+1))

def truth(c,a):
    return any(a[abs(x)-1]==int(x>0) for x in c)
def models(F,p):
    free=[i for i,v in enumerate(p) if v<0]
    for bits in product((0,1),repeat=len(free)):
        a=list(p)
        for i,b in zip(free,bits):a[i]=b
        if all(truth(c,a) for c in F):yield tuple(a)

def up(p):
    p=list(p)
    while True:
        R=[]
        for j,c in enumerate(F,1):
            if any(p[abs(x)-1]==int(x>0) for x in c):continue
            R.append((j,tuple(x for x in c if p[abs(x)-1]<0)))
        if any(len(c)==0 for _,c in R):return p,R,False
        units=[c[0] for _,c in R if len(c)==1]
        if not units:return p,R,True
        x=units[0];i=abs(x)-1;v=int(x>0)
        if p[i]>=0 and p[i]!=v:return p,R,False
        p[i]=v

def odd_cycles_greedy(R,required):
    # Every edge carries the original source clause ID.
    E=[(j,abs(c[0]),abs(c[1])) for j,c in R if len(c)==2]
    out=[];work=Counter()
    while len(out)<required:
        adj=defaultdict(list)
        for j,u,v in E:
            adj[u].append((v,j));adj[v].append((u,j))
        color={};parent={};parentedge={};cycle=None
        for root in sorted(adj):
            if root in color:continue
            color[root]=0;parent[root]=None;queue=[root];head=0
            while head<len(queue) and cycle is None:
                u=queue[head];head+=1
                for v,j in adj[u]:
                    work['edge_incidence_probes']+=1
                    if v not in color:
                        color[v]=1-color[u];parent[v]=u;parentedge[v]=j;queue.append(v)
                    elif color[v]==color[u]:
                        x,y=u,v;seen=set();a=[]
                        while x is not None:
                            seen.add(x);x=parent[x]
                        while y not in seen:
                            a.append(parentedge[y]);y=parent[y]
                        meet=y;x=u
                        while x!=meet:
                            a.append(parentedge[x]);x=parent[x]
                        a.append(j);cycle=a;break
            if cycle is not None:break
        if cycle is None:break
        assert len(cycle)%2==1 and len(cycle)>=3
        out.append(sorted(cycle))
        E=[edge for edge in E if edge[0] not in set(cycle)]
    return out,dict(work)

def gate(p):
    q,R,ok=up(p)
    if not ok:return {'decision':'UNSAT_UP','cycles':[],'e':None}
    f=q.count(-1);u=len(R);e=2*f-u
    r3=sum(len(c)==3 for _,c in R)
    h=4*f-sum(len(c) for _,c in R)
    assert 2*e==r3+h and e>=0
    cycles,work=odd_cycles_greedy(R,e+1)
    return {'decision':'UNSAT_ODD' if len(cycles)>e else 'UNRESOLVED',
            'f':f,'u':u,'e':e,'r3':r3,'h':h,
            'cycles':cycles,'work':work,'residual_original_ids':[j for j,_ in R]}

def pair_modes(F):
    hist=Counter()
    for j,c in enumerate(F):
        for d in F[j+1:]:
            same=any(x==y for x in c for y in d)
            opp=any(x==-y for x in c for y in d)
            hist[''.join(map(str,(int(not opp),int(not same),int(not same),int(not opp))))]+=1
    return dict(hist)

def main():
    assert grammar(F) and not grammar(F+(F[0],))
    assert all(truth(c,W) for c in F)
    U,S=gate(PU),gate(PS)
    assert (U['f'],U['u'],U['e'],U['r3'],U['h'])==(6,11,1,1,1)
    assert U['decision']=='UNSAT_ODD' and len(U['cycles'])==2
    assert len(list(models(F,PU)))==0 and len(list(models(F,PS)))==2
    assert len(list(models(F,(-1,)*N)))==1032
    modes=pair_modes(F);assert modes=={'1111':110,'1001':29,'0110':51}
    stats=Counter()
    for x11 in (0,1):
        root=(-1,)*6+(0,)*4+(x11,)+(1,)*4
        for assignment in product((-1,0,1),repeat=6):
            p=assignment+root[6:]
            truthvalue=bool(next(models(F,p),None))
            result=gate(p)
            assert not result['decision'].startswith('UNSAT') or not truthvalue
            stats[result['decision']]+=1
    assert sum(stats.values())==1458
    assert stats['UNSAT_UP']==1338 and stats['UNSAT_ODD']==8
    out={'status':'PASS','all_valid_source_scope':True,
         'n':N,'m':len(F),'source':F,
         'source_SAT_models':1032,'sat_cube_models':2,'unsat_cube_models':0,
         'UNSAT_cube_partial':PU,'SAT_cube_partial':PS,'SAT_cube_witness':W,
         'UNSAT_cube_certificate':U,'SAT_cube_gate_result':S,
         'partial_cube_status_counts':dict(stats),'pair_modes':modes,
         'endpoints_N0_N1_N2_N3':(10,0,0,10),
         'P_versus_NP':'OPEN','native_FLMV':'NOT MEASURED'}
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
