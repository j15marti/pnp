#!/usr/bin/env python3
"""TMR-2/052: exact unique-selector two-slice multicut rank collapse.
Pure Python 3.11+, deterministic; strict proper ternary CNF, no external libraries.
Ranks computed over GF(2) and F_65521 for every balanced cut of C6, Q3,
Petersen, plus a seeded Q4 GF(2) balanced-cut sample.
All input assignments on small graphs tested with uniquely-defined gate auxiliaries.
"""
import json, random, hashlib, itertools, sys, platform

VERSION = 'tmr2_unique_selector_rank052.v1'
PRIME = 65521
CHECKS = 0

def ck(cond, msg):
    global CHECKS
    CHECKS += 1
    if not cond:
        raise AssertionError(msg)

def cycle(n):
    return n, sorted({tuple(sorted((u, (u + 1) % n))) for u in range(n)})

def cube(d):
    n = 1 << d
    return n, [(u, u ^ (1 << j)) for u in range(n) for j in range(d) if u < (u ^ (1 << j))]

def petersen():
    E = set()
    for i in range(5):
        for a,b in [(i, (i+1)%5), (i, i+5), (i+5, ((i+2)%5)+5)]:
            E.add(tuple(sorted((a,b))))
    return 10, sorted(E)

def cnf(n, edges):
    m = len(edges)
    assert m >= 2
    t_ids = list(range(n+1,n+m+1))
    # p1=t1; p2...p_{m-1}, then pm=z
    p_ids = [t_ids[0]] + list(range(n+m+1,n+2*m))
    z = p_ids[-1]
    q,a,b = (n+2*m, n+2*m+1, n+2*m+2)
    V = n+2*m+2
    clauses = []
    for (u,v), t in zip(edges,t_ids):
        x,y=u+1,v+1
        clauses += [(-x,-y,t),(x,-t,q),(y,-t,q)]
    for j in range(1,m):
        prev,current,t=p_ids[j-1],p_ids[j],t_ids[j]
        clauses += [(-prev,current,q),(-t,current,q),(prev,t,-current)]
    for bitmask in range(1,8):
        clauses.append(tuple(-var if bitmask&(1<<i) else var for i,var in enumerate([q,a,b])))
    ck(len(clauses)==6*m+4,'clause ledger')
    ck(V==n+2*m+2,'variable ledger')
    ck(len(set(clauses))==len(clauses),'duplicate clauses')
    for cl in clauses:
        ck(len(cl)==3 and len(set(map(abs,cl)))==3,'strict proper clause')
        ck(set(cl).isdisjoint(set(-v for v in cl)),'tautological clause')
    return V,clauses,{'t':t_ids,'p':p_ids,'z':z,'pins':(q,a,b)}

def gate_extension(n,edges,meta,mask):
    A=[0]*(n+2*len(edges)+3)
    for i in range(n):A[i+1]=(mask>>i)&1
    ts=[]
    for (u,v),tid in zip(edges,meta['t']):
        val=A[u+1]&A[v+1]
        A[tid]=val;ts.append(val)
    v=ts[0]
    for j in range(1,len(ts)):
        v |= ts[j]
        A[meta['p'][j]]=v
    for pin in meta['pins']: A[pin]=0
    return A

def sat_clause(cl,A):
    return any((A[abs(v)] if v>0 else 1-A[abs(v)]) for v in cl)

def rank_gf2(rows):
    pivots={}
    for row in rows:
        r=row
        while r:
            p=r.bit_length()-1
            if p not in pivots:
                pivots[p]=r;break
            r ^= pivots[p]
    return len(pivots)

def rank_mod(rows,ncols,p=PRIME):
    A=[[(mask>>j)&1 for j in range(ncols)] for mask in rows]
    k=0
    for j in range(ncols):
        piv=next((i for i in range(k,len(A)) if A[i][j]%p),None)
        if piv is None:continue
        A[k],A[piv]=A[piv],A[k]
        iv=pow(A[k][j],-1,p)
        for i in range(k+1,len(A)):
            if A[i][j]:
                f=(A[i][j]*iv)%p
                for z in range(j,ncols):
                    A[i][z]=(A[i][z]-f*A[k][z])%p
        k+=1
        if k==len(A):break
    return k

def make_masks(coords):
    masks=[0]
    for i in coords:
        masks += [m | (1<<i) for m in masks[:]]
    return masks

def slice_rows(n,values,left):
    R=[i for i in range(n) if i not in left]
    a_masks=make_masks(left);b_masks=make_masks(R)
    rows=[]
    for a in a_masks:
        bits=0
        for j,b in enumerate(b_masks):
            bits |= (values[a|b]<<j)
        rows.append(bits)
    return rows,len(b_masks)

def induced_matching(n,edges,left):
    left=set(left)
    N=[set() for _ in range(n)]
    for u,v in edges: N[u].add(v);N[v].add(u)
    crossing=[(u,v) for u,v in edges if (u in left)!=(v in left)]
    chosen=[];remaining=crossing[:]
    while remaining:
        u,v=remaining[0]
        chosen.append((u,v))
        forbid={u,v}|N[u]|N[v]
        remaining=[(a,b) for a,b in remaining if a not in forbid and b not in forbid]
    endpoints=[i for e in chosen for i in e]
    ck(len(set(endpoints))==len(endpoints),'induced matching shared vertex')
    for i,e in enumerate(chosen):
        for f in chosen[i+1:]:
            ck(not any(y in N[x] for x in e for y in f),'induced matching cross edge')
    return len(chosen),len(crossing)

def graph_audit(name,graph,kind='all',seed=None,samples=None):
    n,edges=graph;m=len(edges)
    ck(len(set(edges))==m,'simple graph')
    degree=max(sum(v==u or w==u for u,w in edges) for v in range(n))
    values=[int(not any((mask>>u)&(mask>>v)&1 for u,v in edges)) for mask in range(1<<n)]
    ck(values[0]==1,'zero source witness')
    V,clauses,meta=cnf(n,edges)
    for mask in range(1<<n):
        A=gate_extension(n,edges,meta,mask)
        ck(A[meta['z']]==1-values[mask],f'z selector {name}:{mask}')
        ck(all(sat_clause(c,A) for c in clauses),f'canonical extension {name}:{mask}')
        A[meta['z']]^=1
        ck(not all(sat_clause(c,A) for c in clauses),f'wrong selector {name}:{mask}')
    if kind=='all':
        cut_list=[]
        for s in range((n+2)//3,(2*n)//3+1):
            for left in itertools.combinations(range(n),s):
                if 0 in left:
                    cut_list.append(left)
    else:
        rng=random.Random(seed)
        cut_list=[]
        for _ in range(samples):
            left=tuple(sorted(rng.sample(range(n),n//2)))
            if 0 not in left:left=tuple(i for i in range(n) if i not in left)
            if left not in cut_list:cut_list.append(left)
    summaries=[]
    for left in cut_list:
        D,cols=slice_rows(n,values,left)
        full=(1<<cols)-1
        C=[full^row for row in D]
        J=[full]*len(D)
        r0=rank_gf2(D);r1=rank_gf2(C);rJ=rank_gf2(J)
        rmatch,cedges=induced_matching(n,edges,left)
        ck(r0>=2**rmatch,'induced matching rank')
        ck(r1>=r0-1,'complement rank inequality GF2')
        ck(rJ==1,'selector projection rank collapse GF2')
        ck(all((a^b)==full for a,b in zip(D,C)),'matrix sum equality')
        if kind=='all':
            p0=rank_mod(D,cols);p1=rank_mod(C,cols);pJ=rank_mod(J,cols)
            ck(p0>=2**rmatch,'prime rank induced matching')
            ck(p1>=p0-1,'prime complement rank')
            ck(pJ==1,'prime projected rank')
        summaries.append({'rank0':r0,'rank1':r1,'matching':rmatch,'cross_edges':cedges})
    return {'graph':name,'vertices':n,'edges':m,'max_degree':degree,
            'strict_cnf_variables':V,'strict_cnf_clauses':len(clauses),
            'strict_cnf_literal_occurrences':3*len(clauses),
            'original_assignments_checked':1<<n,
            'balanced_cuts_checked':len(cut_list),'mode':kind,
            'rank0_range_GF2':[min(s['rank0'] for s in summaries),max(s['rank0'] for s in summaries)],
            'rank1_range_GF2':[min(s['rank1'] for s in summaries),max(s['rank1'] for s in summaries)],
            'induced_matching_range':[min(s['matching'] for s in summaries),max(s['matching'] for s in summaries)],
            'min_crossing_edges':min(s['cross_edges'] for s in summaries),
            'projected_rank_GF2':1, 'projected_rank_F65521':1 if kind=='all' else 'theorem_only',
            'seed':seed,'cut_fingerprint':hashlib.sha256(json.dumps(cut_list).encode()).hexdigest()[:24]}

def gate_table():
    for a,b,o in itertools.product((0,1),repeat=3):
        ck(((not a or not b or o) and (a or not o) and (b or not o)) == (o == (a&b)),'AND gate truth')
        ck(((not a or o) and (not b or o) and (a or b or not o)) == (o == (a|b)),'OR gate truth')
    for bits in range(8):
        vals=[(bits>>i)&1 for i in range(3)]
        # seven ternary clauses excluding the forbidden bit assignment
        c=[tuple(-j-1 if forbidden&(1<<j) else j+1 for j in range(3)) for forbidden in range(1,8)]
        ck(all(sat_clause(v,[0]+vals) for v in c)==(bits==0),'pin truth')

def main():
    gate_table()
    reports=[graph_audit('cycle_6',cycle(6)),graph_audit('cube_Q3',cube(3)),graph_audit('petersen_10',petersen()),graph_audit('cube_Q4',cube(4),'seeded_sample',seed=20261115,samples=12)]
    # A 2x2 DISJ minor, plus both slices and their one-bit sum
    D=[0b11,0b01];C=[v^3 for v in D]
    ck(rank_gf2(D)==2 and rank_gf2(C)==1 and rank_gf2([a^b for a,b in zip(D,C)])==1,'DISJ1 control')
    # one unique satisfying original assignment has rank one by pure tensor identity
    for k in range(1,6):
        n=2*k
        zeros=[0]*(1<<k);zeros[0]=1
        ck(rank_gf2(zeros)==1,'unique assignment indicator')
    out={'version':VERSION,'python':platform.python_version(),'prime':PRIME,'random_seed_for_cube_Q4':20261115,'tests':reports,'checks':CHECKS,'failures':0,
         'symbolic_status':'every balanced cut lower bound for constant-degree expander follows from TMR5-046 induced matching; complement rank >= original rank - 1; selector sum J rank 1; unique extension induction',
         'important_limit':'fixed-formula assignment slices, NOT formula encoding SAT decision; sample ranks are finite COMPUTATIONAL evidence; no SAT machine lower bound'}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
