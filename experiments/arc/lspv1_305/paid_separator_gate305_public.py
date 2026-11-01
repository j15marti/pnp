#!/usr/bin/env python3
"""ARC-PAID-SEPARATOR-GATE305: standalone, full source-typed three-valued gate.
Restricted exact gate; may return UNRESOLVED. Not a P=NP solver or FLMV model.
Full independently executed producer/verifier and JSONL are in the run archive.
"""
from collections import Counter
from itertools import combinations, product
import json, math

F9_POS = [(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
F9_NEG = [(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
Y6_POS = [(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
Y6_NEG = [(1,2,4),(1,3,6),(2,3,5),(4,5,6)]

def source(pos,neg):
    return [tuple(c) for c in pos] + [tuple(-v for v in c) for c in neg]

def valid(F,n):
    if not isinstance(n,int) or n < 3 or n % 3 or len(F)*3 != 4*n:
        return False
    seen=set()
    degree=Counter()
    for c in F:
        if len(c)!=3 or any(not isinstance(x,int) or x==0 or abs(x)>n for x in c):
            return False
        if len({abs(x) for x in c})!=3 or not(all(x>0 for x in c) or all(x<0 for x in c)):
            return False
        key=(c[0]>0,tuple(sorted(abs(x) for x in c)))
        if key in seen:return False
        seen.add(key)
        for x in c: degree[(abs(x),x>0)]+=1
    return all(degree[(v,sgn)]==2 for v in range(1,n+1) for sgn in (False,True))

def true(l,p):
    return abs(l) in p and p[abs(l)] == int(l>0)

def comps(scope,clauses):
    edges={x:set() for x in scope}
    for _,sup in clauses:
        for x in sup:
            for y in sup:
                if x!=y:edges[x].add(y)
    remaining=set(scope);out=[]
    while remaining:
        root=min(remaining);stack=[root];part={root};remaining.remove(root)
        while stack:
            for y in edges[stack.pop()]:
                if y in remaining: remaining.remove(y);part.add(y);stack.append(y)
        out.append(part)
    return out

def partitions(F,ids,p,scope,cost):
    live=[]
    for j in ids:
        cost["source_clause_scans"]+=1
        cost["source_literal_reads"]+=len(F[j])
        if any(true(l,p) for l in F[j]):continue
        free=tuple(abs(l) for l in F[j] if abs(l) not in p)
        if not free: return None,j
        if not set(free).issubset(scope):raise ValueError("source/environment mismatch")
        live.append((j,free))
    return live,None

def gate(F,n,p=None,s=1,rho=2/3,b=1):
    """Status SAT/UNSAT/UNRESOLVED/MALFORMED; count only if exact.
    UNSAT proof is a typed exhaustive original-source clause-ID DAG.
    Variable names and clause IDs are never renamed or forged.
    """
    if not valid(F,n):return {"status":"MALFORMED"}
    p=dict(p or {})
    if any(x<1 or x>n or v not in (0,1) for x,v in p.items()):
        return {"status":"MALFORMED"}
    N=max(2,3*len(F)*math.ceil(math.log2(2*n+2))+64)
    cutoff=max(1,int(b*math.log2(N)))
    work=Counter(grammar_literals=3*len(F))
    def recurse(ids,scope,env):
        work["states"]+=1
        live,bad=partitions(F,ids,env,scope,work)
        node={"ids":list(ids),"scope":sorted(scope),"pins":dict(env)}
        if bad is not None:
            return {"status":"UNSAT","count":0,"proof":{**node,"op":"FALSE_SOURCE_ID","clause":bad}}
        if not scope:
            return {"status":"SAT","count":1,"witness":{}}
        cc=comps(scope,live)
        if len(cc)>1:
            bags=[]
            for part in cc:
                bag=[j for j,sup in live if sup[0] in part]
                assert all(set(sup).issubset(part) for j,sup in live if j in bag)
                bags.append(bag)
            children=[recurse(bag,part,env) for bag,part in zip(bags,cc)]
            work["AND"]+=1
            if any(z["status"]=="UNSAT" for z in children):
                return {"status":"UNSAT","count":0,"proof":{**node,"op":"AND_ONE_FALSE","children":children}}
            if any(z["status"]=="UNRESOLVED" for z in children):
                return {"status":"UNRESOLVED"}
            witness={}
            for child in children:witness.update(child["witness"])
            return {"status":"SAT","count":math.prod(z["count"] for z in children),"witness":witness}
        if len(scope)<=cutoff:
            work["terminal_calls"]+=1
            models=0;witness=None;fail=[]
            variables=sorted(scope)
            for bits in product((0,1),repeat=len(variables)):
                work["complete_assignments"]+=1
                a=dict(zip(variables,bits))
                chk=dict(env);chk.update(a)
                bad_ids=[]
                for j in ids:
                    work["source_clause_scans"]+=1
                    work["source_literal_reads"]+=len(F[j])
                    if not any(true(l,chk) for l in F[j]):bad_ids.append(j)
                if bad_ids:fail.append(min(bad_ids))
                else:
                    models+=1
                    if witness is None:witness=a
            if models:
                return {"status":"SAT","count":models,"witness":witness}
            return {"status":"UNSAT","count":0,
                    "proof":{**node,"op":"ALL_COMPLETIONS_REFUTED",
                             "variable_order":variables,"falsified_clause_ids":fail}}
        B=None
        for k in range(1,min(s,len(scope))+1):
            for test in combinations(sorted(scope),k):
                work["selector_candidate_tests"]+=1
                rem=set(scope)-set(test)
                projected=[(j,tuple(x for x in sup if x not in test))
                           for j,sup in live if any(x not in test for x in sup)]
                groups=comps(rem,projected)
                if len(groups)>1 and max(map(len,groups)) <= rho*len(scope):
                    B=test;break
            if B is not None:break
        if B is None:
            work["failed_policy_nodes"]+=1
            return {"status":"UNRESOLVED"}
        work["OR"]+=1
        children=[]
        for bits in product((0,1),repeat=len(B)):
            extension=dict(zip(B,bits))
            newenv={**env,**extension}
            child=recurse(ids,scope-set(B),newenv)
            if child.get("witness") is not None:
                child["witness"]={**extension,**child["witness"]}
            children.append(child)
        if all(c["status"]!="UNRESOLVED" for c in children):
            count=sum(c["count"] for c in children)
            if count:
                return {"status":"SAT","count":count,
                        "witness":next(c["witness"] for c in children if c["status"]=="SAT")}
            return {"status":"UNSAT","count":0,
                    "proof":{**node,"op":"ALL_BOUNDARY_ALTERNATIVES_REFUTED",
                             "boundary":list(B),"children":children}}
        if any(c["status"]=="SAT" for c in children):
            return {"status":"SAT","count":None,
                    "witness":next(c["witness"] for c in children if c["status"]=="SAT")}
        return {"status":"UNRESOLVED"}
    ans=recurse(list(range(len(F))),set(range(1,n+1))-set(p),p)
    if ans["status"]=="SAT":
        witness={**p,**ans["witness"]}
        assert len(witness)==n
        assert all(any(true(l,witness) for l in c) for c in F)
        ans["witness"]={str(x):v for x,v in witness.items()}
        work["original_witness_clause_checks"]+=len(F)
    ans["source_length_proxy_bits"]=N
    ans["cost_selected_proxies"]=dict(work)
    ans["scope_note"]="Full native FLMV machine accounting NOT claimed."
    return ans

def ring(n):
    assert n>=12 and n%6==0
    F=[]
    for sign,offset in ((1,0),(1,1),(-1,0),(-1,2)):
        for k in range(n//3):
            F.append(tuple(sign*(1+(offset+3*k+i)%n) for i in range(3)))
    assert valid(F,n)
    return F

def demo():
    f9=source(F9_POS,F9_NEG)
    y6=source(Y6_POS,Y6_NEG)
    tests=[
       ("F9-root",f9,9,{},1),
       ("F9-SAT",f9,9,{5:0,6:1,7:0,8:0,9:1},1),
       ("F9-UNSAT",f9,9,{1:1,3:0,5:1,6:0,7:0,8:0},1),
       ("Y6-root",y6,6,{},1),
       ("Y6-UNSAT",y6,6,{3:1,4:0,5:0,6:1},1),
       ("RING12-s1",ring(12),12,{},1),
       ("RING12-s4",ring(12),12,{},4),
    ]
    for label,F,n,p,s in tests:
        a=gate(F,n,p,s=s)
        print(json.dumps({"case":label,"status":a["status"],
                          "count":a.get("count"),"work":a.get("cost_selected_proxies")},sort_keys=True))

if __name__=="__main__":demo()
