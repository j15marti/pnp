#!/usr/bin/env python3
"""LSPV-4: independent XOR(3) + 2-SAT interaction audit.

The script uses Python stdlib only. It verifies Fano plane structure, checks
separate affine and bijunctive closures, compiles monotone exact-one clauses
to proper signed 3CNF, and cross-checks a DPLL implementation.
No tests claim SAT lower bounds or native-TM transition counts.
"""
from __future__ import annotations

import itertools
import json
import math
import random
from collections import Counter
from pathlib import Path

SEED = 202610290436
RNG = random.Random(SEED)
FANO = [(0,1,2), (0,3,4), (0,5,6), (1,3,5), (1,4,6), (2,3,6), (2,4,5)]
CHECKS = Counter()


def verify(flag: bool, kind: str) -> None:
    CHECKS[kind] += 1
    if not flag:
        raise AssertionError(f"FAILED {kind}, check={CHECKS[kind]}")


def parity_sat(triples: list[tuple[int,int,int]], n: int, fixed: dict[int,int]|None=None):
    """Exact GF(2) RREF solver with optional fixed variables."""
    rows = []
    for triple in triples:
        mask = sum(1 << i for i in triple)
        rows.append((mask,1))
    if fixed:
        rows += [(1 << i, v) for i,v in fixed.items()]
    pivots: dict[int,tuple[int,int]] = {}
    for mask,rhs in rows:
        while mask:
            bit = mask.bit_length()-1
            if bit in pivots:
                p,q=pivots[bit]
                mask ^= p
                rhs ^= q
            else:
                pivots[bit]=(mask,rhs)
                break
        if mask==0 and rhs:
            return False
    return True


def neg_2sat_sat(triples: list[tuple[int,int,int]], n:int, fixed: dict[int,int]|None=None):
    """SCC implementation for negative pairwise clauses and unit assumptions."""
    adj=[[] for _ in range(2*n)]
    rev=[[] for _ in range(2*n)]
    def edge(u,v):
        adj[u].append(v); rev[v].append(u)
    for a,b,c in triples:
        for x,y in ((a,b),(a,c),(b,c)):
            # (not x OR not y)  => x->not y, y->not x
            edge(2*x,2*y+1); edge(2*y,2*x+1)
    for k,v in (fixed or {}).items():
        # force x=True: not-x -> x; x=False: x -> not-x
        if v: edge(2*k+1,2*k)
        else: edge(2*k,2*k+1)
    seen=[False]*len(adj)
    order=[]
    def dfs(u):
        seen[u]=True
        for v in adj[u]:
            if not seen[v]: dfs(v)
        order.append(u)
    for u in range(2*n):
        if not seen[u]: dfs(u)
    comp=[-1]*len(adj)
    def dfs2(u,k):
        comp[u]=k
        for v in rev[u]:
            if comp[v]<0: dfs2(v,k)
    for u in reversed(order):
        if comp[u]<0: dfs2(u,u)
    return all(comp[2*i]!=comp[2*i+1] for i in range(n))



def find_cover(edges, k):
    """Discover a vertex cover with branching including failed branches."""
    total=[0]
    edges=tuple(sorted({tuple(sorted(e)) for e in edges}))
    def go(rem,budget):
        total[0]+=1
        if not rem:return ()
        if budget==0:return None
        a,b=rem[0]
        for v in (a,b):
            z=go(tuple(e for e in rem if v not in e),budget-1)
            if z is not None:return (v,)+z
        return None
    return go(edges,k),total[0]


def mixed_sat_via_cover(triples,n):
    """Uniform deterministic exact solver with charged cover discovery."""
    edges=[(a,b) for a,b,c in triples for (a,b) in ((a,b),(a,c),(b,c))]
    explored=0
    for budget in range(n+1):
        cover,nodes=find_cover(edges,budget)
        explored+=nodes
        if cover is not None:break
    cover=tuple(sorted(set(cover)))
    verify(all(u in cover or v in cover for u,v in edges),"cover_verified")
    trials=0
    for values in itertools.product((0,1),repeat=len(cover)):
        trials+=1
        fixed=dict(zip(cover,values)); valid=True
        for u,v in edges:
            if fixed.get(u)==1 and fixed.get(v)==1:
                valid=False;break
            if fixed.get(u)==1:
                fixed[v]=0
            if fixed.get(v)==1:
                fixed[u]=0
        if valid and parity_sat(triples,n,fixed):
            return True,len(cover),explored,trials
    return False,len(cover),explored,trials

def exact_one(triples: list[tuple[int,int,int]], bits:tuple[int,...]):
    return all(sum(bits[i] for i in t)==1 for t in triples)


def all_marginals_both(triples,n):
    return all(parity_sat(triples,n,{i:0}) and parity_sat(triples,n,{i:1})
       and neg_2sat_sat(triples,n,{i:0}) and neg_2sat_sat(triples,n,{i:1}) for i in range(n))


def literal_exchange(triples,n):
    """Complete per-side consistency queries, exchange ONLY unit facts."""
    forced={}
    steps=0
    while True:
        steps+=1
        verify(parity_sat(triples,n,forced),"closure_affine_consistent")
        verify(neg_2sat_sat(triples,n,forced),"closure_2sat_consistent")
        additions={}
        for i in range(n):
            if i in forced: continue
            for oracle in (parity_sat,neg_2sat_sat):
                possible0=oracle(triples,n,{**forced,i:0})
                possible1=oracle(triples,n,{**forced,i:1})
                verify(possible0 or possible1,"closure_consistency_each_side")
                if possible0 != possible1:
                    v=int(possible1)
                    if i in additions:
                        verify(additions[i]==v,"closure_no_conflict")
                    additions[i]=v
        if not additions:
            return forced,steps
        forced.update(additions)


def compile_proper_3cnf(triples: list[tuple[int,int,int]], n:int):
    """Fresh z for each negative pair. 4 parity + 6 AMO = 10 clauses per triple."""
    out=[]
    z=n
    for a0,b0,c0 in triples:
        a,b,c=a0+1,b0+1,c0+1
        out.extend([(a,b,c),(a,-b,-c),(-a,b,-c),(-a,-b,c)])
        for u,v in ((a,b),(a,c),(b,c)):
            z+=1
            out.append((-u,-v,z))
            out.append((-u,-v,-z))
    return z,out


def cnf_eval(clauses,assignment):
    return all(any(assignment[abs(l)-1] == (l>0) for l in cl) for cl in clauses)


def dpll(clauses,assumptions=(),return_nodes=False):
    """Independent elementary recursive DPLL, with unit propagation."""
    assignment={abs(l):l>0 for l in assumptions}
    if len(assignment)!=len(assumptions): return (False,0) if return_nodes else False
    cls=tuple(tuple(cl) for cl in clauses)
    nodes=0
    def recurse(assign):
        nonlocal nodes
        nodes += 1
        while True:
            changed=False; shortest=None
            for cl in cls:
                undec=[]
                for lit in cl:
                    v=abs(lit)
                    if v in assign:
                        if assign[v] == (lit>0):break
                    else:undec.append(lit)
                else:
                    if not undec:return False
                    if len(undec)==1:
                        lit=undec[0]; v=abs(lit); val=lit>0
                        if v in assign and assign[v]!=val:return False
                        if v not in assign:
                            assign[v]=val; changed=True
                    if shortest is None or len(undec)<len(shortest):shortest=undec
            if not changed:break
        if shortest is None: return True
        v=abs(shortest[0])
        for val in (True,False):
            nxt=assign.copy();nxt[v]=val
            if recurse(nxt):return True
        return False
    result=recurse(assignment)
    return (result,nodes) if return_nodes else result


def dimacs(n,clauses):
    return f"p cnf {n} {len(clauses)}\n"+"".join(" ".join(str(v) for v in cl)+" 0\n" for cl in clauses)


def exercise():
    pair_counts=Counter(tuple(sorted(pair)) for l in FANO for pair in itertools.combinations(l,2))
    point_counts=Counter(i for l in FANO for i in l)
    verify(len(pair_counts)==21 and set(pair_counts.values())=={1},"fano_steiner_pairs")
    verify(sorted(point_counts.values())==[3]*7,"fano_regular_degree")
    verify(all(len(set(t))==3 for t in FANO),"fano_proper_triples")
    A=[bits for bits in itertools.product((0,1),repeat=7) if all(sum(bits[i] for i in l)%2==1 for l in FANO)]
    B=[bits for bits in itertools.product((0,1),repeat=7) if all(sum(bits[i] for i in l)<=1 for l in FANO)]
    C=[bits for bits in itertools.product((0,1),repeat=7) if exact_one(FANO,bits)]
    verify(len(A)==8,"fano_affine_solution_count")
    verify(len(B)==8,"fano_2sat_solution_count")
    verify(len(C)==0,"fano_mixed_unsat")
    verify(sorted({sum(x) for x in A})==[3,7],"fano_affine_weights")
    verify(sorted({sum(x) for x in B})==[0,1],"fano_2sat_weights")
    verify(parity_sat(FANO,7),"fano_affine_consistent")
    verify(neg_2sat_sat(FANO,7),"fano_2sat_consistent")
    verify(all_marginals_both(FANO,7),"fano_both_full_marginals")
    fpt_answer,fpt_cover,fpt_search,fpt_trials=mixed_sat_via_cover(FANO,7)
    verify(not fpt_answer and fpt_cover==6,"fano_cover_solver")
    force,steps=literal_exchange(FANO,7)
    verify(force=={} and steps==1,"fano_unit_exchange_stuck")
    # Verify each 3CNF gadget projects exactly onto the original triple.
    n3,c3=compile_proper_3cnf([(0,1,2)],3)
    verify(n3==6 and len(c3)==10,"gadget_exact_size")
    for x in itertools.product((False,True),repeat=3):
        sat=any(cnf_eval(c3,x+zs) for zs in itertools.product((False,True),repeat=3))
        verify(sat == (sum(x)==1),"gadget_full_projection")
    nf,cf=compile_proper_3cnf(FANO,7)
    verify(nf==28 and len(cf)==70,"fano_compiled_size")
    verify(all(len(c)==3 and len({abs(l) for l in c})==3 for c in cf),"fano_compiled_proper")
    verify(not dpll(cf),"fano_compiled_unsat")
    # Parity and AMO 2-SAT sublanguages each SAT, their intersection may not.
    satcounts=Counter(); examples=[]; node_sums=Counter(); node_max=Counter(); node_min={}
    cover_sums=Counter();cover_max=Counter();search_sums=Counter();trial_sums=Counter()
    for n in range(3,9):
        triples_all=list(itertools.combinations(range(n),3))
        for _ in range(90):
            t=RNG.randrange(1,min(13,len(triples_all))+1)
            src=RNG.sample(triples_all,t)
            truth=any(exact_one(src,bits) for bits in itertools.product((0,1),repeat=n))
            verify((not truth) or (parity_sat(src,n) and neg_2sat_sat(src,n)),"separate_necessary_conditions")
            nn,cl=compile_proper_3cnf(src,n)
            verify(nn==n+3*t and len(cl)==10*t,"random_encoded_size")
            verify(all(len(set(abs(v) for v in c))==3 for c in cl),"random_proper")
            actual,nodes=dpll(cl,return_nodes=True)
            verify(actual==truth,"random_dpll_equivalence")
            c_actual,c_size,c_search,c_trials=mixed_sat_via_cover(src,n)
            verify(c_actual==truth,"random_cover_equivalence")
            side="SAT" if truth else "UNSAT"
            node_sums[side]+=nodes; node_max[side]=max(node_max[side],nodes)
            cover_sums[side]+=c_size;cover_max[side]=max(cover_max[side],c_size)
            search_sums[side]+=c_search;trial_sums[side]+=c_trials
            node_min[side]=min(node_min.get(side,nodes),nodes)
            # For each random original assignment fix x and existentially check z using DPLL.
            for _ in range(3):
                bits=tuple(RNG.randrange(2) for _ in range(n))
                assumptions=[(i+1 if val else -(i+1)) for i,val in enumerate(bits)]
                verify(dpll(cl,assumptions)==exact_one(src,bits),"random_full_projection")
            satcounts['SAT' if truth else 'UNSAT']+=1
            if len(examples)<4:examples.append({'n':n,'triples':t,'sat':truth})
    # Source model: all symbols and index bytes are materialized.
    orig_size=len("".join(" ".join(str(i+1) for i in t)+"\n" for t in FANO).encode())
    compiled_size=len(dimacs(nf,cf).encode())
    return {
      'status':'PASS','seed':SEED,'assertions':sum(CHECKS.values()),'counts':dict(sorted(CHECKS.items())),
      'fano':{'variables':7,'lines':7,'parity_solutions':len(A),'two_sat_solutions':len(B),'mixed_solutions':len(C),
              'parity_solution_weights':sorted(Counter(map(sum,A)).items()),
              'two_sat_solution_weights':sorted(Counter(map(sum,B)).items()),
              'unary_exchange_rounds':steps,'forced_literals':force,
              'proper_3cnf_variables':nf,'proper_3cnf_clauses':len(cf),
              'vertex_cover_size':fpt_cover,'cover_search_nodes':fpt_search,'cover_assignments_checked':fpt_trials,
              'source_triple_text_bytes':orig_size,'compiled_DIMACS_bytes':compiled_size},
      'random_instances':dict(satcounts),'cover_solver_by_side':{side:{'max_vertex_cover':cover_max[side],'mean_vertex_cover':round(cover_sums[side]/satcounts[side],3),'mean_discovery_nodes':round(search_sums[side]/satcounts[side],3),'mean_assignments':round(trial_sums[side]/satcounts[side],3)} for side in ('SAT','UNSAT')},'dpll_same_program_nodes':{side:{'min':node_min[side],'max':node_max[side],'mean':round(node_sums[side]/satcounts[side],3)} for side in ('SAT','UNSAT')},'examples':examples,
      'limitations':'Finite DPLL tests and unit-exchange barrier only; no all-algorithm lower bound. Not strict exact22 occurrence class.'
    }

if __name__=='__main__':
    print(json.dumps(exercise(),sort_keys=True,indent=2))