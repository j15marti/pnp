#!/usr/bin/env python3
"""No-import verifier for REFEREE281."""
import argparse,collections,itertools,json
F={
"Y6":((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)),
"F9":((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))}
P=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15));N=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15));F["F15"]=P+tuple(tuple(-x for x in c) for c in N)
def sat(C,z):return all(any(((z>>(abs(x)-1))&1)==int(x>0) for x in c) for c in C)
def circuit(meta,z):
    vals=[]
    def val(t):return (z>>(int(t[1:])-1))&1 if t[0]=="x" else vals[int(t[1:])]
    for g in meta["gates"]:
        a,b=val(g["a"]),val(g["b"]);vals.append(int((a and b) if g["op"]=="AND" else ((a or b) if g["op"]=="OR" else not(a and b))))
    return val(meta["output"])
def matching(C,ids):
    E={(i,j):len(set(map(abs,C[i]))&set(map(abs,C[j]))) for i,j in itertools.combinations(ids,2)}
    def go(rem):
        if not rem:return 0
        i=min(rem);best=go(rem-{i})
        for j in rem-{i}:best=max(best,E.get((min(i,j),max(i,j)),0)+go(rem-{i,j}))
        return best
    return go(set(ids))
def main():
    ap=argparse.ArgumentParser();ap.add_argument("raw");a=ap.parse_args();r=json.load(open(a.raw));checks=0
    expected={"Y6":6,"F9":9,"F15":15}
    for name,n in expected.items():
        C=F[name];entry=r["fixtures"][name]
        for meta in entry["projections"]:
            v=meta["variable"];remaining=[i for i,c in enumerate(C) if v not in map(abs,c)]
            W=matching(C,[i for i in remaining if C[i][0]>0])+matching(C,[i for i in remaining if C[i][0]<0])
            incp=[c for c in C if v in c];incn=[c for c in C if -v in c]
            d=int(len(set(map(abs,incp[0]))&set(map(abs,incp[1])))==2)+int(len(set(map(abs,incn[0]))&set(map(abs,incn[1])))==2)
            assert len(meta["gates"])==meta["gate_count"]==3*len(C)-5-W-d;checks+=1
            models=0
            for y in range(1<<(n-1)):
                lo=y&((1<<(v-1))-1);hi=y>>(v-1);z=lo|(hi<<v);want=int(sat(C,z) or sat(C,z|1<<(v-1)))
                assert circuit(meta,z)==want;models+=want;checks+=1
            assert models==meta["projected_models"];checks+=1
    common={3:0,5:1,6:0,7:0,8:0};free=(2,4,9);counts=[]
    for x1 in (0,1):
        q=0
        for bits in itertools.product((0,1),repeat=3):
            z=(x1<<0)+sum(b<<(v-1) for v,b in common.items())+sum(b<<(v-1) for v,b in zip(free,bits));q+=sat(F["F9"],z);checks+=1
        counts.append(q)
    assert counts==[2,0];checks+=1
    assert r["controls"]["F9_OBDD_nodes"]=={"best":52,"natural":66,"worst":80};checks+=1
    assert r["controls"]["malformed_rejected"]==6 and r["P_vs_NP"]=="OPEN";checks+=2
    print(json.dumps({"status":"PASS","independent_assertion_groups":checks,"projection_truth_rows":r["controls"]["projection_truth_rows"],"F9_projection_gates":[p["gate_count"] for p in r["fixtures"]["F9"]["projections"]],"same_original_models":counts,"P_vs_NP":"OPEN"},indent=2))
if __name__=="__main__":main()
