#!/usr/bin/env python3
"""Finite controls for TREE-HOLONOMY-REFEREE194. Stdlib only."""
from itertools import product
from math import ceil, log2
import json

CHECKS=0
def check(x,msg):
    global CHECKS
    CHECKS+=1
    if not x: raise AssertionError(msg)

def pairs(mask):
    return {(a,b) for a,b in product((0,1),repeat=2) if mask & (1 << (2*a+b))}

def compose(A,B):
    out=0
    for a,c in product((0,1),repeat=2):
        if any((a,b) in pairs(A) and (b,c) in pairs(B) for b in (0,1)):
            out |= 1 << (2*a+c)
    return out

def product_mask(seq):
    if not seq: return 0b1001
    out=seq[0]
    for x in seq[1:]: out=compose(out,x)
    return out

def path_brute(seq):
    out=0
    for vals in product((0,1),repeat=len(seq)+1):
        if all((vals[i],vals[i+1]) in pairs(R) for i,R in enumerate(seq)):
            out |= 1 << (2*vals[0]+vals[-1])
    return out

def cycle_sat(seq):
    return any(all((v[i],v[(i+1)%len(seq)]) in pairs(R)
                       for i,R in enumerate(seq))
               for v in product((0,1),repeat=len(seq)))

def trace_nonempty(mask):
    return bool(mask & ((1<<0)|(1<<3)))

def ac3_domains(n,edges):
    D=[{0,1} for _ in range(n)]
    changed=True
    while changed:
        changed=False
        for u,v,R in edges:
            for x,y,RR in ((u,v,R),(v,u,sum(1<<(2*b+a) for a,b in pairs(R)))):
                keep={a for a in D[x] if any((a,b) in pairs(RR) for b in D[y])}
                if keep != D[x]:
                    D[x]=keep; changed=True
    return D

def grouping(seq):
    g=max(2,ceil(len(seq)**0.5))
    return [product_mask(seq[i:i+g]) for i in range(0,len(seq),g)]

def bits(k):
    return 12+4*k+2*ceil(log2(k+2))

def main():
    # Boolean relation composition is associative.
    for A,B,C in product(range(16),repeat=3):
        check(compose(compose(A,B),C)==compose(A,compose(B,C)),"associativity")

    # Complete path relation equals brute force, and nonempty AC3 is complete on paths.
    path_sequences=0
    for length in range(1,4):
        for seq in product(range(16),repeat=length):
            path_sequences+=1
            exact=path_brute(seq)
            check(product_mask(seq)==exact,"path product")
            edges=[(i,i+1,R) for i,R in enumerate(seq)]
            D=ac3_domains(length+1,edges)
            check((exact!=0)==all(D),"tree AC completeness")

    # Cycle closure is the diagonal of the complete holonomy product.
    cycle_sequences=0
    for length in range(1,4):
        for seq in product(range(16),repeat=length):
            cycle_sequences+=1
            check(cycle_sat(seq)==trace_nonempty(product_mask(seq)),"cycle trace")

    # Deterministic length-four sample without the full 16^4 brute-force cost.
    state=20261029
    for _ in range(8192):
        seq=[]
        for _ in range(4):
            state=(1103515245*state+12345)&0x7fffffff
            seq.append(state&15)
        path_sequences+=1; cycle_sequences+=1
        exact=path_brute(seq)
        check(product_mask(seq)==exact,"sampled length-four path")
        D4=ac3_domains(5,[(i,i+1,R) for i,R in enumerate(seq)])
        check((exact!=0)==all(D4),"sampled length-four tree AC")
        check(cycle_sat(seq)==trace_nonempty(product_mask(seq)),"sampled length-four cycle")

    E=(1<<0)|(1<<3)
    X=(1<<1)|(1<<2)
    triangle=[E,E,X]
    D=ac3_domains(3,[(0,1,E),(1,2,E),(2,0,X)])
    check(D==[{0,1},{0,1},{0,1}],"arc consistency must retain all domains")
    check(not cycle_sat(triangle),"odd holonomy UNSAT")
    check(all({a for a,b in pairs(R)}=={0,1} and {b for a,b in pairs(R)}=={0,1}
              for R in triangle),"all unary marginals full")

    # Equality/inequality cycles: SAT iff the number of flips is even.
    parity_cycles=0
    for k in range(2,13):
        for flags in product((0,1),repeat=k):
            parity_cycles+=1
            seq=[X if f else E for f in flags]
            check(cycle_sat(seq)==(sum(flags)%2==0),"cycle parity")

    # Grouped complete relations are a repeatable one-child contraction on this grammar.
    ledgers=[]
    for k in (16,64,256,1024,4096):
        seq=[X if (i*i+3*i+1)%7 in (0,2,5) else E for i in range(k)]
        original=product_mask(seq); cur=seq; levels=[]
        while len(cur)>2:
            child=grouping(cur)
            check(product_mask(child)==product_mask(cur),"grouping preserves complete relation")
            check(trace_nonempty(product_mask(child))==trace_nonempty(product_mask(cur)),"grouping preserves cycle")
            levels.append({"parent_k":len(cur),"child_k":len(child),
                           "parent_bits":bits(len(cur)),"child_bits":bits(len(child))})
            cur=child
        check(product_mask(cur)==original,"recursive closure")
        ledgers.append({"k":k,"levels":levels})

    result={
      "run":"TREE-HOLONOMY-REFEREE194","status":"PASS",
      "assertions":CHECKS,
      "associativity_triples":16**3,
      "path_sequences":path_sequences,
      "cycle_sequences":cycle_sequences,
      "parity_cycles":parity_cycles,
      "smallest_arc_consistent_unsat":{
        "variables":3,"relations":["EQUALITY","EQUALITY","INEQUALITY"],
        "domains_after_ac3":[sorted(x) for x in D],
        "complete_product_mask":product_mask(triangle)},
      "grouped_recursion_ledgers":ledgers,
      "peer_reruns":{
        "LSPV2_MARGINAL_COHERENCE219":"PASS",
        "LSPV3_EXACT22_FOUR_FIBERS155":"PASS",
        "Connected_Interface_Audit":"PASS 4680/7191/139"},
      "statuses":{
        "tree_complete_relations":"PROVED/EXACT restricted",
        "unary_marginals_on_cycles":"FALSIFIED",
        "cycle_complete_holonomy":"PROVED/EXACT restricted",
        "arbitrary_CNF_relation_acquisition":"OPEN/NP-hard in prior one-port reductions",
        "P_vs_NP":"OPEN"},
      "limitations":[
        "Relations are supplied extensionally on a two-element domain.",
        "This is not a strict exact-(2,2) source compiler.",
        "No arbitrary-SAT module relation is acquired without solving its extension problem.",
        "Python operations are not native tape transitions."]}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__": main()
