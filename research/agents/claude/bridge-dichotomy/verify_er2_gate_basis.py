"""Exhaustive check: every 2-input Boolean function f(a,b) is realizable as a
signed literal of the output of a circuit of <=3 fresh signed two-input AND
gates with DISTINCT input IDs (the ER2 extension convention, P2-L5-448).
Also verifies each gate's three defining facets are exactly its CNF.
Runs in well under 1 second."""
import itertools, json
A=(0,0,1,1); B=(0,1,0,1)
def neg(t): return tuple(1-x for x in t)
def AND(s,t): return tuple(x&y for x,y in zip(s,t))
best={}
# state: list of (id, truthtable); gates take two distinct ids, each signed
def search(nodes, depth):
    for (i,t) in nodes:
        for tt in (t,neg(t)):
            if tt not in best or best[tt]>depth: best[tt]=depth
    if depth==3: return
    for (i,s),(j,t) in itertools.combinations(nodes,2):
        for s2 in (s,neg(s)):
            for t2 in (t,neg(t)):
                search(nodes+[(len(nodes),AND(s2,t2))],depth+1)
search([(0,A),(1,B)],0)
# facets of q<->(x AND y): (-q|x),(-q|y),(q|-x|-y)
facet_ok=all(bool(((not q) or x) and ((not q) or y) and (q or (not x) or (not y))) == (q==(x and y))
             for q,x,y in itertools.product((0,1),repeat=3))
res={"functions_realized":len(best),"all_16":len(best)==16,
     "max_gates_needed":max(best.values()),"gate_counts":{"".join(map(str,k)):v for k,v in sorted(best.items())},
     "facets_exact":facet_ok}
print(json.dumps(res,indent=1))
assert res["all_16"] and res["max_gates_needed"]<=3 and facet_ok
