#!/usr/bin/env python3
"""RP-MKTP-FORK22: exact hash-kernel/portfolio information tradeoff.

No claim of generic SAT-to-MKTP reduction, lower bound for KT, or P!=NP.
All finite checks use standard Python; random tests use fixed seed solely for tests.
"""
from __future__ import annotations

import itertools
import json
import random
from pathlib import Path

RNG = random.Random(20261021)
CHECKS = 0


def check(ok, msg):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise AssertionError(msg)


def parity(z):
    return z.bit_count() & 1


def apply(A, x):
    return tuple(parity(a & x) for a in A)


def rank(rows, n):
    pivots = {}
    for v in rows:
        while v:
            j = v.bit_length()-1
            if j in pivots:
                v ^= pivots[j]
            else:
                pivots[j] = v
                break
    return len(pivots)


def kernel_nonzero(rows, n):
    for v in range(1, 1<<n):
        if all(parity(a & v) == 0 for a in rows):
            return v
    return None


def unit_as_proper3(lit, fresh):
    a,b = fresh, fresh+1
    return [(lit, a,b), (lit,a,-b), (lit,-a,b), (lit,-a,-b)], fresh+2


def minimal_unsat_chain(r):
    # x0 and implications x_(i-1)=>x_i and NOT x_r, each proper-3CNF.
    n=r+1
    clauses=[]
    c,fresh=unit_as_proper3(1,n+1)
    clauses.extend(c)
    for j in range(1,r+1):
        v=fresh;fresh+=1
        clauses.extend([(-j,j+1,v),(-j,j+1,-v)])
    c,fresh=unit_as_proper3(-(r+1),fresh)
    clauses.extend(c)
    return clauses,fresh-1


def forced_index_formula(x, n, j):
    """Conjunction of y_i=x_i; then demand y_j=1.

    Proper 3CNF; all sources at a fixed n have identical fixed-width encoding.
    """
    clauses=[]
    fresh=n+1
    for i in range(n):
        lit=(i+1) if (x>>i)&1 else -(i+1)
        c,fresh=unit_as_proper3(lit,fresh)
        clauses += c
    c,fresh=unit_as_proper3(j+1,fresh)
    clauses += c
    return clauses,fresh-1


def all_sat(clauses,n):
    # Simple exact DPLL with unit propagation; not used to assert complexity bound.
    def recurse(assign):
        while True:
            changed=False
            residual=[]
            for clause in clauses:
                if any(assign.get(abs(t)) == (t>0) for t in clause):
                    continue
                rem=[t for t in clause if abs(t) not in assign]
                if not rem: return False
                if len(rem)==1:
                    t=rem[0]; k=abs(t); val=(t>0)
                    if k in assign:
                        if assign[k]!=val: return False
                    else:
                        assign[k]=val; changed=True
                else:
                    residual.append(rem)
            if not changed: break
        if not residual: return True
        t=residual[0][0]
        v=abs(t)
        for b in (True, False):
            nxt=assign.copy(); nxt[v]=b
            if recurse(nxt): return True
        return False
    return recurse({})


def canonical(C,n):
    w=max(1,n.bit_length())
    hdr=f"CNF3|{n}|{len(C)}|{w}|"
    return hdr + ''.join(('1' if v<0 else '0') + format(abs(v),'0'+str(w)+'b') for c in C for v in c)


def params(N,k=241):
    N=max(2,N)
    a=(N-1).bit_length()
    L=(6*a+4)//5
    M=1<<L
    lo,hi=0,M
    while lo+1<hi:
        mid=(lo+hi)//2
        if mid**k>=M: hi=mid
        else: lo=mid
    p=max(L,hi)
    return {'source_bits':N,'L':L,'M':M,'p':p,'k':k}


def ctr_target_bits(x,n,r,M):
    # Explicit G(F,i) for this restricted family: A is first r identity rows;
    # G(F,i)=bit x_i when 0<=i<r, else 0. Fully deterministic.
    return [((x>>i)&1) if i<r else 0 for i in range(M)]


def main():
    out={'run':'RP-MKTP-FORK22','status':'ESTABLISHED_RESTRICTED_P_VS_NP_OPEN_P_VS_RP_OPEN',
         'exact_collision':[],'pair_controls':[],'rank_tests':[],
         'portfolio_controllability':[],'resource_examples':[],'minimal_unsat_controls':[],'checks':0}

    # Every fixed q x n linear fingerprint must collide on some SAT/UNSAT
    # INDEX pair, because q<n forces a nonzero null-space vector.
    for n in range(2,10):
        for q in range(1,min(n,4)):
            for trial in range(30):
                A=[RNG.getrandbits(n) for _ in range(q)]
                v=kernel_nonzero(A,n)
                check(v is not None,'no kernel vector q<n')
                j=(v & -v).bit_length()-1
                check(apply(A,0)==apply(A,v),'fingerprint collision failed')
                c0,n0=forced_index_formula(0,n,j)
                c1,n1=forced_index_formula(v,n,j)
                check(n0==n1 and len(c0)==len(c1),'formula sizes unequal')
                check(canonical(c0,n0) != canonical(c1,n1),'pair formulas not distinct')
                check(not all_sat(c0,n0),'zero prefix with selected one should be UNSAT')
                check(all_sat(c1,n1),'v prefix with selected one should be SAT')
                check(len(canonical(c0,n0))==len(canonical(c1,n1)),'pair encoded lengths differ')
                out['pair_controls'].append({'n':n,'q':q,'trial':trial,'j':j,
                                             'rank':rank(A,n),'kernel_vector':v})

    # Hostile connected minimally UNSAT proper-3CNF chains.
    for r in range(1,6):
        C,nvars=minimal_unsat_chain(r)
        check(not all_sat(C,nvars), f'chain r={r} not UNSAT')
        for k in range(len(C)):
            check(all_sat(C[:k]+C[k+1:],nvars),f'chain r={r} deleting clause {k} still UNSAT')
        check(len(C)==2*r+8 and nvars==2*r+5, 'bad chain resources')
        out['minimal_unsat_controls'].append({'r':r,'variables':nvars,'clauses':len(C),'all_deletions_sat':len(C),
                                              'source_bits':len(canonical(C,nvars))})

    # Exact probability over ALL qxn matrices: for a fixed v != 0, each row
    # annihilates v with probability exactly one half.
    for n,q in ((3,1),(4,2),(5,2)):
        limit=1<<n
        mats=itertools.product(range(limit),repeat=q)
        tested=0
        collisions=[0]*(limit)
        for mat in mats:
            tested+=1
            for v in range(1,limit):
                if apply(mat,v)==(0,)*q: collisions[v]+=1
        expected=tested//(1<<q)
        for v in range(1,limit):
            check(collisions[v]==expected,f'bad collision frequency n={n} q={q} v={v}')
        out['exact_collision'].append({'n':n,'q':q,'number_matrices':tested,
                                       'nonzero_differences':limit-1,
                                       'collisions_per_difference':expected,
                                       'probability':f'1/{1<<q}'})

    # Stacking hashed outputs is lossless iff the concatenated rows have full
    # GF2 rank. When rank deficient, collisions persist for a common selector.
    for n in (3,4,6,8):
        for q in (1,2,3):
            h=(n+q-1)//q
            for trial in range(48):
                blocks=[[RNG.getrandbits(n) for _ in range(q)] for _ in range(h)]
                rows=[v for block in blocks for v in block]
                r=rank(rows,n)
                images={apply(rows,x) for x in range(1<<n)}
                check(len(images)==(1<<r),'rank/image cardinality identity failed')
                if r<n:
                    v=kernel_nonzero(rows,n)
                    check(v is not None and apply(rows,v)==apply(rows,0), 'portfolio kernel wrong')
                else:
                    check(len(images)==(1<<n),'full rank not injective')
                out['rank_tests'].append({'n':n,'q':q,'h':h,'rank':r,'distinct_images':len(images)})

    # Explicit full-rank online portfolio A=I_n, outputs x verbatim, then zero.
    # This has correct physical resources but not the SAT->LOW KT condition.
    # Finite tests audit only injectivity and the encoded-size/threshold arithmetic;
    # unbounded ordinary KT conclusion is proved by Kolmogorov incompressibility.
    for n in (2,3,4,5,6,7,8):
        pairs=[]
        for x in range(1<<n):
            C,vars_=forced_index_formula(x,n,0)
            encoded=canonical(C,vars_)
            bounds=params(len(encoded))
            check(all_sat(C,vars_) == bool(x&1),'INDEX label mismatch')
            bits=ctr_target_bits(x,n,n,bounds['M'])
            check(bits[:n] == [(x>>i)&1 for i in range(n)],'explicit child bits wrong')
            check(not any(bits[n:]),'padded tail not zero')
            pairs.append(tuple(bits[:n]))
        check(len(set(pairs))==1<<n,'full portfolio not injective')
        out['portfolio_controllability'].append({'n':n,'distinct_recoverable_prefixes':len(set(pairs)),
                                                  'satisfiable_prefixes':1<<(n-1),
                                                  'N':len(encoded),'M':bounds['M'],'p':bounds['p']})
    for n in (8,16,32,64,128,256,512,1024,4096):
        # Exact source-length upper bound for n forced gadgets + selector:
        # 4(n+1) proper clauses * 3 literals * (1+ceil(log2(3n+3))) plus header.
        # An n-bit source can be emitted online with O(log N) workspace.
        vars_=3*n+2
        w=vars_.bit_length()
        N=50+12*(n+1)*(1+w)
        b=params(N)
        out['resource_examples'].append({'n':n,'N_upper':N,'target_M':b['M'],
                                        'threshold_p':b['p'],'p_lt_n_minus_2':b['p']<n-2,
                                        'time_target_ratio_exponent':'1.2 < 1.205',
                                        'workspace':'O(log N) for identity-row streaming'})
    out['checks']=CHECKS
    out['aggregates']={'INDEX_pairs_tested':len(out['pair_controls']),
                       'exhaustive_matrix_memberships':sum(a['number_matrices']*a['nonzero_differences'] for a in out['exact_collision']),
                       'portfolio_samples':len(out['rank_tests']),
                       'padded_formulas_tested':sum(1<<n for n in (2,3,4,5,6,7,8))}
    dst=Path(__file__).with_name('RP_MKTP_FORK22_raw.json')
    dst.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'checks':CHECKS,'aggregates':out['aggregates'],
                      'exact_collision':out['exact_collision'],
                      'last_resource':out['resource_examples'][-1]},indent=2))

if __name__=='__main__':main()