#!/usr/bin/env python3
"""Independent no-import verifier for REFEREE280."""
import argparse,itertools,json
from functools import lru_cache
F={
"Y6":((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)),
"F9":((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))}
P=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15));N=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15));F["F15"]=P+tuple(tuple(-x for x in c) for c in N)
def sat(C,z):return all(any(((z>>(abs(x)-1))&1)==int(x>0) for x in c) for c in C)
def matching(C,ids):
    E={(i,j):len(set(map(abs,C[i]))&set(map(abs,C[j]))) for i,j in itertools.combinations(ids,2)}
    def go(rem):
        if not rem:return 0
        i=min(rem);best=go(rem-{i})
        for j in rem-{i}:
            best=max(best,E.get((min(i,j),max(i,j)),0)+go(rem-{i,j}))
        return best
    return go(set(ids))
def circuit(meta,z):
    vals=[]
    def val(t):return (z>>(int(t[1:])-1))&1 if t[0]=="x" else vals[int(t[1:])]
    for g in meta["gates"]:
        a,b=val(g["a"]),val(g["b"]);vals.append(int((a and b) if g["op"]=="AND" else ((a or b) if g["op"]=="OR" else not(a and b))))
    return val(meta["output"])
def obdd(C,n):
    costs={};full=(1<<n)-1
    for mask in range(1<<n):
        A=[i for i in range(n) if (mask>>i)&1];R=[i for i in range(n) if not(mask>>i)&1];S=set()
        for aa in range(1<<len(A)):
            sig=0
            for rr in range(1<<len(R)):
                z=sum(((aa>>k)&1)<<i for k,i in enumerate(A))+sum(((rr>>k)&1)<<i for k,i in enumerate(R))
                sig|=sat(C,z)<<rr
            S.add(sig)
        for p,v in enumerate(R):
            q=0
            for sig in S:
                lo=hi=0
                for y in range(1<<(len(R)-1)):
                    i=(y&((1<<p)-1))|((y>>p)<<(p+1))
                    lo|=((sig>>i)&1)<<y;hi|=((sig>>(i|(1<<p)))&1)<<y
                q+=lo!=hi
            costs[mask,v]=q
    @lru_cache(None)
    def dp(mask,worst=False):
        if mask==full:return (0,0,())
        z=[(costs[mask,v]+dp(mask|1<<v,worst)[0],
            max(costs[mask,v],dp(mask|1<<v,worst)[1]),
            (v+1,)+dp(mask|1<<v,worst)[2]) for v in range(n) if not(mask>>v)&1]
        return max(z) if worst else min(z)
    def score(order):
        mask=s=peak=0
        for vv in order:
            q=costs[mask,vv-1];s+=q;peak=max(peak,q);mask|=1<<(vv-1)
        return s,peak
    b,bw,bo=dp(0);w,ww,wo=dp(0,True);natural=tuple(range(1,n+1))
    return {"best_nodes":b,"best_order":list(bo),"best_width":bw,
            "natural_nodes":score(natural)[0],"natural_width":score(natural)[1],
            "worst_nodes":w,"worst_order":list(wo),"worst_width":ww}
def main():
    ap=argparse.ArgumentParser();ap.add_argument("raw");a=ap.parse_args();r=json.load(open(a.raw));checks=0
    expected={"Y6":(6,19,4,20),"F9":(9,28,7,70),"F15":(15,48,11,1032)}
    for name,C in F.items():
        n,g,w,models=expected[name];pos=[i for i,c in enumerate(C) if c[0]>0];neg=[i for i,c in enumerate(C) if c[0]<0]
        W=matching(C,pos)+matching(C,neg);assert W==w;checks+=1
        meta=r["circuits"][name];assert meta["gate_count"]==g==3*len(C)-1-W==len(meta["gates"]);checks+=1
        count=0
        for z in range(1<<n):
            q=sat(C,z);assert circuit(meta,z)==q;count+=q;checks+=1
        assert count==models;checks+=1
    # Four local Boolean identities, all rows.
    for bits in itertools.product((0,1),repeat=5):
        a,b,c,d,e=bits
        assert ((a or b or c) and (a or d or e))==(a or ((b or c) and (d or e)))
        assert (((not a)or(not b)or(not c))and((not a)or(not d)or(not e)))==(not(a and ((b and c)or(d and e))))
        checks+=2
    for bits in itertools.product((0,1),repeat=4):
        a,b,c,d=bits
        assert ((a or b or c)and(a or b or d))==((a or b)or(c and d))
        assert (((not a)or(not b)or(not c))and((not a)or(not b)or(not d)))==(not((a and b)and(c or d)))
        checks+=2
    # Same-original F9 pin pair.
    for x1,expect in ((0,2),(1,0)):
        count=0
        for x2,x4,x9 in itertools.product((0,1),repeat=3):
            z=(x1<<0)|(x2<<1)|(0<<2)|(x4<<3)|(1<<4)|(0<<5)|(0<<6)|(0<<7)|(x9<<8);count+=sat(F["F9"],z);checks+=1
        assert count==expect
    got=obdd(F["F9"],9);assert got==r["F9_OBDD"];checks+=1
    assert (got["best_nodes"],got["best_width"],got["natural_nodes"],got["worst_nodes"])==(52,11,66,80);checks+=1
    assert r["P_vs_NP"]=="OPEN" and "not an unrestricted circuit minimum" in r["scope"];checks+=2
    print(json.dumps({"status":"PASS","independent_assertion_groups":checks,"gates":{k:r["circuits"][k]["gate_count"] for k in expected},"F9_OBDD":got,"P_vs_NP":"OPEN"},indent=2))
if __name__=="__main__":main()
