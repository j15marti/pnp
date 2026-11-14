#!/usr/bin/env python3
"""TMR-2/030: exact finite audit of r-sparse oracle locality.
A deterministic global b-query preprocessor is followed by N independent
q-query local evaluators. Every response is obtained only through get(a).
Native CPython, stdlib only. Finite evidence, not a TM lower-bound proof.
"""
from __future__ import annotations
import itertools, math, random, json, hashlib, pathlib, datetime

SEED=202611141518
RNG=random.Random(SEED)
assertions=0
cases=0
sparse_runs=0
output_checks=0
sharp_cases=0
sharp_equalities=0
cnf_controls=0


def check(ok, detail):
    global assertions
    assertions += 1
    if not ok:
        raise AssertionError(detail)


def oracle_eval(mask, M, N, b, q, seed):
    # Only the oracle accessor reads source bits; branching is adaptive.
    def get(a):
        assert 0 <= a < M
        return (mask >> a) & 1
    state=(seed ^ 0x7EF561CA) & 0xFFFFFFFF
    queried=[]
    # Global queries are unique but can depend on previous answers.
    for i in range(b):
        pos=(state+17*i+seed) % M
        while pos in queried: pos=(pos+1)%M
        z=get(pos)
        queried.append(pos)
        state=(state*1664525+1013904223+ 1299709*z +i) & 0xFFFFFFFF
    out=[]
    for j in range(N):
        # Independently restart each output computation from exact global state.
        st=(state + (j+1)*2246822519) & 0xFFFFFFFF
        local_queries=[]
        zs=[]
        for i in range(q):
            pos=(st+31*i+11*j) % M
            while pos in local_queries: pos=(pos+1)%M
            z=get(pos)
            local_queries.append(pos)
            zs.append(z)
            st=(st*1103515245+12345*z+(i+1)*271) & 0xFFFFFFFF
        # Nonlinear postprocessing, allowed to depend on global state and j.
        bit=(sum(zs) + (st & 3) + (state & 7) + (j%3)) & 1
        out.append(bit)
    return tuple(out),tuple(queried)


# Explicit ground truth masks, not exposed to the transformer.
for M in range(3, 11):
    Nvals=sorted(set([1,3,7,2*M]))
    for b in sorted(set([0,1,M//2,M-1])):
        for q in sorted(set([0,1,min(2,M),min(3,M)])):
            for seed in [0,9,17]:
                N=RNG.choice(Nvals)
                y0,Q0=oracle_eval(0,M,N,b,q,seed)
                check(len(Q0)==b and len(set(Q0))==b,(M,b,Q0))
                remaining=tuple(a for a in range(M) if a not in Q0)
                B=len(remaining)
                for r in sorted(set([1, min(2,B), min(3,B), B])):
                    if r<1: continue
                    total=0
                    k=0
                    for S in itertools.combinations(remaining,r):
                        mask=sum(1<<a for a in S)
                        y,_=oracle_eval(mask,M,N,b,q,seed)
                        d=sum(u!=v for u,v in zip(y,y0))
                        total+=d
                        sparse_runs+=1
                        output_checks+=N
                        check(d<=N,(M,b,q,seed,r,S,d))
                        k+=1
                    # Exact ratio of zero-path q-set hitting a uniform r-subset.
                    # If q>B, use qeff=B, but q can include already pre-read bits.
                    qeff=min(q,B)
                    forbidden=math.comb(B-qeff,r) if B-qeff>=r else 0
                    eligible=math.comb(B,r)
                    # Integer, no roundoff: sum_S d <= N*(eligible-forbidden)
                    check(total<=N*(eligible-forbidden),(M,b,q,seed,r,total,N*(eligible-forbidden)))
                    check(k==eligible,(M,b,q,seed,r,k,eligible))
                    cases+=1

# SHARPNESS: all q-subsets of remaining source positions used once,
# each output bit ORs its Q; on zero output is zero. Each r-sparse mask
# differs at exact fraction 1 - C(B-q,r)/C(B,r).
for B in range(2,11):
    for q in range(0,min(5,B)+1):
        Qs=tuple(itertools.combinations(range(B),q))
        N=len(Qs)
        for r in range(1,B+1):
            missing = math.comb(B-r,q) if B-r>=q else 0
            for S in itertools.combinations(range(B),r):
                support=set(S)
                # OR-only output on singleton / r-sparse source.
                bits=[int(bool(support.intersection(Q))) for Q in Qs]
                d=sum(bits)
                check(d==N-missing,(B,q,r,S,d,N-missing))
                sharp_equalities+=1
            sharp_cases+=1


# Hostile syntax-aware source control: short proper 3-CNF forces c variables
# and leaves v-c variables free (including y,z). A two-sign contradiction is
# directly visible from clauses, bypassing all black-box query assumptions.
def forcing_clauses(v, c, contradictory=False):
    y,z=v-2,v-1
    clauses=[]
    for i in range(c):
        for ya,za in itertools.product([False,True],repeat=2):
            clauses.append(((i,True),(y,ya),(z,za)))
    if contradictory:
        for ya,za in itertools.product([False,True],repeat=2):
            clauses.append(((0,False),(y,ya),(z,za)))
    return clauses

def cnf_sat(clauses, assignment):
    return all(any(bool((assignment>>i)&1)==positive for i,positive in clause)
               for clause in clauses)

for v in range(3,9):
    for c in range(1,v-1):
        for contradictory in [False,True]:
            cls=forcing_clauses(v,c,contradictory)
            check(all(len(set(i for i,_ in cl))==3 for cl in cls),(v,c,cls))
            sat=sum(cnf_sat(cls,a) for a in range(1<<v))
            check(sat == (0 if contradictory else 1<<(v-c)),(v,c,contradictory,sat))
            cnf_controls+=1

# Relation to source satisfiability: zero function is UNSAT; any r-sparse
# Boolean function is satisfiable. The proof's bound is query-model only.
raw={
 'tag':'TMR2_R_SPARSE_HYPERGEOMETRIC_LOCALITY038',
 'date_pst':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-8))).isoformat(),
 'engine':'native CPython stdlib',
 'seed':SEED,
 'adaptive_configurations':cases,
 'adaptive_sparse_runs':sparse_runs,
 'adaptive_output_coordinate_checks':output_checks,
 'sharp_parameter_cases':sharp_cases,
 'sharp_full_subset_equalities':sharp_equalities,
 'proper_3cnf_syntax_shortcut_controls':cnf_controls,
 'assertions':assertions,
 'failures':0,
 'statement':'For B=M-|Q0|, r-subset sources disjoint from global zero-path, average reference output distance <= N*(1-C(B-q,r)/C(B,r)). Tight via all q-subset OR outputs.',
 'scope':'deterministic source-independent evaluation oracles, b global adaptive queries then N independently restarted at-most-q local query routines; unbounded other computation',
 'status':'COMPUTATIONAL finite evidence; separate elementary symbolic argument; no general SAT or MCSP time lower bound'
}
print(json.dumps(raw,indent=2,sort_keys=True))
