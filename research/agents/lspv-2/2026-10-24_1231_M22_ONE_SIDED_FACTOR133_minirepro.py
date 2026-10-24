#!/usr/bin/env python3
"""M22-ONE-SIDED-FACTOR133 compact exact solver.
Requires networkx (maximum-weight matching); bit-machine resources are NOT
measured. Full extended randomized audits are separate run artifacts.
"""
from collections import Counter, defaultdict
from itertools import product
import networkx as nx

P=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
Q=((1,2,4),(1,3,6),(2,3,5),(4,5,6))

def analyse(F):
    F=[tuple(c) for c in F]
    if not F or len(set(F))!=len(F):
        raise ValueError("empty or duplicate signed clauses")
    vars_=sorted({abs(x) for c in F for x in c})
    plus=Counter();minus=Counter(); p=set();n=set()
    for c in F:
        if len(c)!=3 or len({abs(x) for x in c})!=3 or not (
                all(x>0 for x in c) or all(x<0 for x in c)):
            raise ValueError("not monotone proper 3CNF")
        for z in c:
            (plus if z>0 else minus)[abs(z)]+=1
        (p if c[0]>0 else n).add(tuple(sorted(abs(z) for z in c)))
    if any(plus[x]!=2 or minus[x]!=2 for x in vars_):
        raise ValueError("not exact signed (2,2)")
    if len(p)+len(n)!=len(F):
        raise ValueError("repeated signed supports")
    h=sorted(p&n);up=sorted(p-n);un=sorted(n-p)
    if len(up)!=len(un):
        raise AssertionError("source occurrence-count mismatch")
    return vars_,h,up,un

def check(F,x):
    return all(any(x[abs(z)] == int(z>0) for z in c) for c in F)

def factor(intervals,pins,names):
    """One matching call for signed degree<=2 [lower,upper] constraints."""
    g=nx.Graph();required=set();slots=[];occ=defaultdict(list)
    for i,(lits,lo,hi) in enumerate(intervals):
        fixed=sum(pins[abs(z)]==int(z>0) for z in lits if abs(z) in pins)
        free=[z for z in lits if abs(z) not in pins]
        lo=max(0,lo-fixed);hi=min(hi-fixed,len(free))
        if lo>hi:return None
        ss=[("slot",i,j) for j in range(hi)]
        g.add_nodes_from(ss);required.update(ss[:lo]);slots.append(ss)
        for z in free:occ[abs(z)].append((i,z>0))
    if any(len(entries)>2 for entries in occ.values()):
        raise AssertionError("one-sided degree-two invariant violated")
    for x,sites in occ.items():
        if len(sites)==1:
            (i,sg)=sites[0];a=("a",x);b=("b",x);leaf=("leaf",x)
            required.update((a,b))
            g.add_edge(a,b,weight=2);g.add_edge(b,leaf,weight=1)
            for t in slots[i]:g.add_edge(a,t,weight=1+int(t in required))
        elif sites[0][1]==sites[1][1]:
            (i,_),(j,_)=sites;a=("a",x);b=("b",x)
            required.update((a,b));g.add_edge(a,b,weight=2)
            for t in slots[i]:g.add_edge(a,t,weight=1+int(t in required))
            for t in slots[j]:g.add_edge(b,t,weight=1+int(t in required))
        else:
            v=("choice",x);required.add(v);g.add_node(v)
            for i,_ in sites:
                for t in slots[i]:
                    g.add_edge(v,t,weight=1+int(t in required))
    m=nx.max_weight_matching(g,weight="weight")
    if sum(g[a][b]["weight"] for a,b in m)!=len(required):
        return None
    mate={v:u for a,b in m for v,u in ((a,b),(b,a))}
    out=dict(pins)
    for x,sites in occ.items():
        if len(sites)==1 or sites[0][1]==sites[-1][1]:
            literal_true=mate[("a",x)][0]=="slot"
            out[x]=int(literal_true==sites[0][1])
        else:
            selected=mate[("choice",x)][1]
            out[x]=int(next(sign for i,sign in sites if i==selected))
    for x in names:out.setdefault(x,0)
    assert all(lo<=sum(out[abs(z)]==int(z>0) for z in lits)<=hi
               for lits,lo,hi in intervals)
    return out

def solve(F):
    vars_,h,up,un=analyse(F)
    if not up:
        # Paired source has exact factor continuation too, but C_star
        # recognition must REJECT it.
        raise ValueError("fully paired; outside canonical C_star")
    intervals=[(tuple(s),1,2) for s in h]+[
        (tuple(-x for x in s),1,3) for s in un]
    deg=Counter(abs(z) for literals,_,_ in intervals for z in literals)
    assert all(deg[x]==2 for x in vars_)
    attempts=0
    for indices in product(range(3),repeat=len(up)):
        pins={s[j]:1 for s,j in zip(up,indices)}
        attempts+=1
        result=factor(intervals,pins,vars_)
        if result is not None:
            assert check(F,result)
            return result,attempts
    return None,attempts

def demo():
    y=list(P)+[tuple(-x for x in t) for t in Q]
    model,attempts=solve(y)
    models=sum(check(y,dict(zip(range(1,7),bits)))
               for bits in product((0,1),repeat=6))
    assert model is not None and models==20
    remap={1:1,2:4,3:2,4:5,5:6,6:3}
    yy=[tuple((1 if z>0 else -1)*remap[abs(z)] for z in c) for c in y]
    model2,attempts2=solve(yy)
    assert model2 is not None and attempts2>=2
    # Independent degree-two SIGNED negative control:
    # x must simultaneously be 1 and 0
    assert factor([((1,),1,1),((-1,),1,1)],{},[1]) is None
    assert factor([((1,),1,1)],{},[1])=={1:1}
    print({"Y_models":models,"Y_calls":attempts,
           "relabelled_Y_calls":attempts2,
           "signed_degree_two_UNSAT_control":"PASS",
           "correctness":"PASS",
           "warning":"does not measure FLMV bit-machine resources"})

if __name__=="__main__":
    demo()
