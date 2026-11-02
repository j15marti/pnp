#!/usr/bin/env python3
"""Independent no-import verifier for REFEREE282."""
import argparse,collections,itertools,json
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
P=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15));N=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15));F15=P+tuple(tuple(-x for x in c) for c in N)
def sat(F,z):return all(any(((z>>(abs(x)-1))&1)==int(x>0) for x in c) for c in F)
def norm(cs):
    a=[]
    for c in cs:
        s=frozenset(c)
        if not any(-x in s for x in s):a.append(s)
    u=set(a);k=[c for c in u if not any(d<c for d in u)]
    return tuple(sorted((tuple(sorted(c,key=lambda x:(abs(x),x<0))) for c in k),key=lambda c:(len(c),c)))
def elim(F,v):
    F=norm(F);p=[c for c in F if v in c];n=[c for c in F if -v in c];rest=[c for c in F if v not in c and -v not in c];rs=[];taut=0
    for a in p:
      for b in n:
        q=(set(a)-{v})|(set(b)-{-v})
        if any(-x in q for x in q):taut+=1
        else:rs.append(q)
    D=norm(rest+rs);return D,len(p)*len(n),taut,sum(map(len,D)),max(map(len,D),default=0)
def value(F,a):return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)
def main():
    ap=argparse.ArgumentParser();ap.add_argument("raw");a=ap.parse_args();r=json.load(open(a.raw));checks=0
    for name,F,n in (("Y6",Y6,6),("F9",F9,9),("F15",F15,15)):
      for v,meta in enumerate(r["first_eliminations"][name],1):
        D,pairs,taut,lits,width=elim(F,v)
        assert pairs==meta["candidate_pairs"]==4 and len(D)==meta["clauses"]<=len(F);checks+=1
        assert lits==meta["literal_records"]<=3*len(F)+4 and width==meta["max_width"]<=4;checks+=1
        for y in range(1<<(n-1)):
          ass={u:(y>>(u-1 if u<v else u-2))&1 for u in range(1,n+1) if u!=v}
          lo=y&((1<<(v-1))-1);hi=y>>(v-1);z=lo|(hi<<v)
          assert value(D,ass)==(sat(F,z) or sat(F,z|1<<(v-1)));checks+=1
    D,p,_,_,_=elim(F9,9);_,p2,_,_,_=elim(D,6);assert p==4 and p2==6;checks+=1
    common={3:0,5:1,6:0,7:0,8:0};counts=[]
    for x1 in (0,1):
      q=0
      for bits in itertools.product((0,1),repeat=3):
        z=(x1<<0)+sum(b<<(v-1) for v,b in common.items())+sum(b<<(v-1) for v,b in zip((2,4,9),bits));q+=sat(F9,z);checks+=1
      counts.append(q)
    assert counts==[2,0];checks+=1
    ex=r["F9_order_extremes"];assert ex["best"]["total_candidate_pairs"]==9 and ex["best"]["max_step_pairs"]==4;checks+=1
    assert ex["worst"]["total_candidate_pairs"]==35 and ex["worst"]["max_step_pairs"]==12;checks+=1
    assert r["controls"]["F9_OBDD_nodes"]=={"best":52,"natural":66,"worst":80};checks+=1
    assert r["forward_evaluators"]=={"F15":{"depth":7,"fan_in_two_gates":59,"models":1032,"truth_rows":32768},"F9":{"depth":6,"fan_in_two_gates":35,"models":70,"truth_rows":512},"Y6":{"depth":5,"fan_in_two_gates":23,"models":20,"truth_rows":64}};checks+=1
    assert r["controls"]["malformed_rejected"]==6 and r["P_vs_NP"]=="OPEN";checks+=2
    print(json.dumps({"status":"PASS","assertions":checks,"semantic_rows":r["semantic_projection_rows"],"F9_order_costs":[ex["best"]["total_candidate_pairs"],ex["worst"]["total_candidate_pairs"]],"same_original_models":counts,"P_vs_NP":"OPEN"},indent=2))
if __name__=="__main__":main()
