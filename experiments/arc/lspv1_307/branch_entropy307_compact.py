#!/usr/bin/env python3
"""Compact GitHub mirror of ALLINPUT-PAID-BRANCH-ENTROPY307.
Full GF(2) enumerator plus no-import verifier and 146810 tests: local archive.
Python operation counts are NOT native FLMV TM bounds.
"""
import itertools, json, math
POS=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
NEG=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
P={1:1,2:0,3:1,4:0,8:0}
Q={1:1,2:1,3:0,4:0,8:0}
def source(t):
    z=[]
    for i in range(t):
        for j,cl in enumerate(POS):
            z.append((1,tuple(((i+1)%t)*9+5 if (j==0 and x==5) else i*9+x for x in cl)))
        for cl in NEG:z.append((0,tuple(i*9+x for x in cl)))
    return z
def pins(t,label):
    return {9*i+x:(Q if i==0 and label=="UNSAT" else P)[x]
            for i in range(t) for x in P}
def validate(F,n):
    if len(F)*3!=4*n:return False
    quotas={i:[0,0] for i in range(1,n+1)}
    seen=set()
    for s,vs in F:
        if s not in (0,1) or len(vs)!=3 or len(set(vs))!=3:return False
        if any(x not in quotas for x in vs):return False
        k=(s,tuple(sorted(vs)))
        if k in seen:return False
        seen.add(k)
        for x in vs:quotas[x][s]+=1
    return all(a==[2,2] for a in quotas.values())
def eval_clause(c,a):
    s,vs=c
    return sum(a[x]==s for x in vs)
def stats(F,p):
    covered=[];uncovered=[]
    for j,(s,vs) in enumerate(F):
        if any(x in p and p[x]==s for x in vs):covered.append((j,s,vs))
        else:uncovered.append((j,s,tuple(x for x in vs if x not in p)))
    free=set(range(1,3*len(F)//4+1))-set(p)
    eta=sum(min(sum(s==1 and x in vs for _,s,vs in covered),
                sum(s==0 and x in vs for _,s,vs in covered)) for x in free)
    binary={j:tuple(sorted(vs)) for j,s,vs in uncovered if len(vs)==2}
    triangles=[];used=set()
    for triple in itertools.combinations(sorted(binary),3):
        if any(j in used for j in triple):continue
        if len({binary[j] for j in triple})==3 and len(set().union(*(binary[j] for j in triple)))==3:
            triangles.append(triple);used.update(triple)
    f=len(free);u=len(uncovered);nu=len(triangles)
    return {"f":f,"u":u,"eta":eta,"nu":nu,"delta":2*f-u-eta-nu,
            "triangles":[list(x) for x in triangles]}
def exact_count(F,p):
    free=sorted(set(x for _,vs in F for x in vs)-p.keys())
    count=0
    for bits in itertools.product((0,1),repeat=len(free)):
        a=dict(p);a.update(zip(free,bits))
        count+=all(eval_clause(cl,a)>0 for cl in F)
    return count
def main():
    out=[]
    for t in range(1,5):
        F=source(t)
        assert validate(F,9*t)
        for label in ("SAT","UNSAT"):
            p=pins(t,label);r=stats(F,p)
            assert (r["f"],r["u"],r["eta"],r["nu"],r["delta"])==(4*t,5*t,2*t,t,0)
            assert all(len(c)==3 for c in r["triangles"])
            x=exact_count(F,p)
            assert x==(label=="SAT")
            out.append({"blocks":t,"label":label,"models":x,
                        "fully_enumerated_GF2_ticket_count":3**t,
                        "source_variable_OR_depth_of_one_terminal":0,
                        "paid_ticket_entropy_bits":t*math.log2(3),
                        "f":r["f"],"delta":r["delta"],
                        "source_cycle_ids":r["triangles"]})
    assert exact_count(source(1),{})==70
    print(json.dumps({"status":"PASS","cases":out,
                      "note":"Ticket counts are exact declared enumeration workload, not a lower bound for SAT."},indent=2))
if __name__=="__main__":main()
