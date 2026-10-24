#!/usr/bin/env python3
"""LSPV-1 SIGNED-DEGREE2-MATCH133. Python 3, NetworkX 3.x.
Signed +/- literals, one-based variable ids, EXACTLY ONE true per clause.
CLI: python SIGNED_DEGREE2_MATCH133_repro.py --out results.json
"""
import argparse
import collections
import itertools
import json
import random
import time
import networkx as nx


def validate(clauses):
    for C in clauses:
        if not 1 <= len(C) <= 3 or 0 in C:
            raise ValueError("bad source clause")
        if len(set(map(abs,C))) != len(C):
            raise ValueError("repeated variable within source clause")


def occs(clauses):
    d=collections.defaultdict(list)
    for i,C in enumerate(clauses):
        for lit in C:d[abs(lit)].append((i,lit>0))
    return d


def brute(clauses):
    validate(clauses)
    keys=sorted(occs(clauses))
    for bits in itertools.product((False,True),repeat=len(keys)):
        w=dict(zip(keys,bits))
        if all(sum(w[abs(l)] if l>0 else not w[abs(l)] for l in C)==1 for C in clauses):
            return w
    return None


def deg2_matching(clauses,log=None):
    """Return exact signed source witness or None if UNSAT. Require occurrence<=2."""
    validate(clauses)
    O=occs(clauses)
    if any(len(v)>2 for v in O.values()):
        raise ValueError("source has occurrence > 2")
    G=nx.Graph()
    required=set()
    label={}
    for i in range(len(clauses)):
        c=("C",i)
        G.add_node(c)
        required.add(c)
    for x,obs in O.items():
        if len(obs)==1:
            i,s=obs[0]
            a,b=("C",i),("L",x)
            G.add_edge(a,b,weight=1)
            label[frozenset((a,b))]=("one",x,i,s)
        else:
            (i,s),(j,t)=obs
            if i==j:raise ValueError("same named variable twice in one clause")
            if s==t:
                a,b=("C",i),("C",j)
                # Parallel same-sign edges are equivalent; one representative suffices.
                if not G.has_edge(a,b):
                    G.add_edge(a,b,weight=2)
                    label[frozenset((a,b))]=("same",x,i,s)
            else:
                h=("H",x)
                required.add(h)
                for ix,sign in obs:
                    c=("C",ix)
                    G.add_edge(h,c,weight=2)
                    label[frozenset((h,c))]=("opposite",x,ix,sign)
    M=nx.max_weight_matching(G,weight="weight",maxcardinality=False)
    found={frozenset(pair) for pair in M}
    score=sum(G[a][b]["weight"] for a,b in M)
    if log is not None:
        log["matching_calls"]+=1
        log["matching_nodes"]+=len(G.nodes)
        log["matching_edges"]+=len(G.edges)
    if score!=len(required):return None
    W={}
    for x,obs in O.items():
        if len(obs)==1:
            i,s=obs[0]
            W[x]=s if frozenset((("C",i),("L",x))) in found else not s
        else:
            (i,s),(j,t)=obs
            if s==t:
                k=frozenset((("C",i),("C",j)))
                W[x]=s if k in found and label[k][1]==x else not s
            else:
                picked=[label[e] for e in found
                        if e in label and label[e][0]=="opposite" and label[e][1]==x]
                if len(picked)!=1:raise AssertionError("choice node not saturated")
                W[x]=picked[0][3]
    if not all(sum(W[abs(l)] if l>0 else not W[abs(l)] for l in C)==1 for C in clauses):
        raise AssertionError("matching witness invalid")
    return W


def branch_on_high(clauses,log=None):
    validate(clauses)
    H=sorted(x for x,ob in occs(clauses).items() if len(ob)>=3)
    for bits in itertools.product((False,True),repeat=len(H)):
        if log is not None:log["branch_attempts"]+=1
        fixed=dict(zip(H,bits))
        residual=[]
        reject=False
        for C in clauses:
            a=[l for l in C if abs(l) in fixed]
            b=[l for l in C if abs(l) not in fixed]
            trues=sum(fixed[abs(l)] if l>0 else not fixed[abs(l)] for l in a)
            if trues>=2:
                reject=True
                break
            if trues==1:
                residual.extend([(-l,) for l in b])
            elif b:
                residual.append(tuple(b))
            else:
                reject=True
                break
        if reject:continue
        rem=deg2_matching(residual,log)
        if rem is None:continue
        ans={**rem,**fixed}
        if not all(sum(ans[abs(l)] if l>0 else not ans[abs(l)] for l in C)==1 for C in clauses):
            raise AssertionError("branch witness invalid")
        return ans
    return None


def k4(mask):
    triples=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
    return [tuple(-x if mask & (1<<(3*i+j)) else x
                  for j,x in enumerate(C)) for i,C in enumerate(triples)]


def random_source(rng,n,m,cap):
    remaining={i:cap for i in range(1,n+1)}
    clauses=[]
    for _ in range(m):
        avail=[x for x,c in remaining.items() if c>0]
        if not avail:break
        size=min(rng.randint(1,3),len(avail))
        V=rng.sample(avail,size)
        clauses.append(tuple(x if rng.getrandbits(1) else -x for x in V))
        for x in V:remaining[x]-=1
    return clauses


def audit(seed=202610240826,k4_start=0,k4_stop=4096,random_count=1200,high_count=240):
    rng=random.Random(seed)
    counts=collections.Counter()
    work=collections.Counter()
    start=time.monotonic()
    for mask in range(k4_start,k4_stop):
        C=k4(mask)
        ans=deg2_matching(C,work)
        gold=brute(C)
        assert (ans is None)==(gold is None)
        counts["k4"]+=1
        counts["sat_k4"]+=gold is not None
        counts["unsat_k4"]+=gold is None
        counts["checks"]+=2
    for _ in range(random_count):
        C=random_source(rng,rng.randint(3,11),rng.randint(1,9),2)
        ans=deg2_matching(C,work)
        gold=brute(C)
        assert (ans is None)==(gold is None)
        counts["random_deg2"]+=1
        counts["sat_deg2"]+=gold is not None
        counts["unsat_deg2"]+=gold is None
        counts["checks"]+=2
    for _ in range(high_count):
        C=random_source(rng,rng.randint(4,10),rng.randint(2,9),3)
        ans=branch_on_high(C,work)
        gold=brute(C)
        assert (ans is None)==(gold is None)
        counts["random_high"]+=1
        counts["sat_high"]+=gold is not None
        counts["unsat_high"]+=gold is None
        counts["checks"]+=2
    P=k4(0)
    seen=set()
    N=[]
    for C in P:
        row=[]
        for x in C:
            row.append(-x if x in seen else x)
            seen.add(x)
        N.append(tuple(row))
    assert brute(P) is not None and brute(N) is None
    assert deg2_matching(P,work) is not None and deg2_matching(N,work) is None
    assert len(occs(P))==6 and len(occs(N))==6
    counts["matched_pairs"]+=1
    counts["checks"]+=6
    out={"run_id":"SIGNED-DEGREE2-MATCH133","seed":seed,
         "range":{"k4_start":k4_start,"k4_stop":k4_stop,
                  "random_count":random_count,"high_count":high_count},
         "counts":dict(counts),"abstract_work":dict(work),
         "K4":{"SAT":P,"UNSAT":N},
         "physical_FLMV_machine_steps_measured":False,
         "elapsed_seconds":round(time.monotonic()-start,3)}
    return out


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--seed",type=int,default=202610240826)
    parser.add_argument("--k4-start",type=int,default=0)
    parser.add_argument("--k4-stop",type=int,default=4096)
    parser.add_argument("--random-count",type=int,default=1200)
    parser.add_argument("--high-count",type=int,default=240)
    parser.add_argument("--out",default="SIGNED_DEGREE2_MATCH133_results.json")
    opts=parser.parse_args()
    ans=audit(opts.seed,opts.k4_start,opts.k4_stop,opts.random_count,opts.high_count)
    with open(opts.out,"w") as f:json.dump(ans,f,sort_keys=True,indent=2)
    print(json.dumps(ans,sort_keys=True))
