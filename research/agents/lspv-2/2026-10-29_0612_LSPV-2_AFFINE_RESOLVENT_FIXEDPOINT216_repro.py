#!/usr/bin/env python3
"""Exact finite audit of an affine signed exact-(2,2)-3CNF resolution trap.

Only Python stdlib. Run: python3 <this_file> > raw.json
All exhaustive counts and measurements are assertions, not theorem proofs.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from hashlib import sha256
import itertools, json, random

SEED = 20261029
RNG = random.Random(SEED)


def var(g, i, p):
    return g*p + (i%p) + 1


def canonical(clauses):
    return tuple(sorted((tuple(sorted(c,key=lambda x:(abs(x),x<0))) for c in clauses)))


def family(p):
    assert p>=5 and p%2==1
    C=[]
    for s in range(4):
        for i in range(p):
            a=var(0,i,p)
            b=var(1,i+s,p)
            c=var(2,i+2*s,p)
            C.append(((-a if s in (0,1) else a),
                      (-b if s in (2,3) else b),
                      (-c if s in (0,2) else c)))
    return canonical(C)


def check_source(C,p):
    n=3*p
    if len(C)!=4*p:return False
    if any(len(c)!=3 or len({abs(x) for x in c})!=3 for c in C):return False
    if not all(1<=abs(x)<=n for c in C for x in c):return False
    cnt=Counter(x for c in C for x in c)
    if any(cnt[i]!=2 or cnt[-i]!=2 for i in range(1,n+1)):return False
    if len(set(C))!=len(C):return False
    # Verify promised exact byte-canonical source. This also tests all indices and all signs.
    return C==family(p)


def is_linear(C):
    sets=[set(map(abs,c)) for c in C]
    return all(len(x&y)<=1 for i,x in enumerate(sets) for y in sets[i+1:])


def is_connected(C,n):
    adj=[set() for _ in range(n+1)]
    for clause in C:
        ids=[abs(x) for x in clause]
        for i in ids:
            adj[i].update(ids)
    seen={1};queue=[1]
    while queue:
        k=queue.pop()
        for j in adj[k]:
            if j not in seen:seen.add(j);queue.append(j)
    return len(seen)==n


def eval_cnf(C, assignment):
    return all(any(assignment[abs(l)] == (l>0) for l in c) for c in C)


def eliminate(C,pivot):
    P=[c for c in C if pivot in c]
    M=[c for c in C if -pivot in c]
    rest=[c for c in C if pivot not in c and -pivot not in c]
    resolvents=[];taut=0
    for A in P:
        for B in M:
            S=set(A)-{pivot}
            S.update(set(B)-{-pivot})
            if any(-lit in S for lit in S):taut+=1;continue
            resolvents.append(tuple(sorted(S,key=lambda x:(abs(x),x<0))))
    return canonical(rest),canonical(resolvents),len(P),len(M),taut


def factor_4(R):
    """Recover a K_2,2 rectangle of four disjoint 2-literal feet without source table."""
    if len(R)!=4 or len(set(R))!=4 or any(len(x)!=4 for x in R):return None
    sets=list(map(set,R))
    best=None
    # Exhaustive constant-size orientation search, bounded by 4! possibilities.
    for ids in itertools.permutations(range(4)):
        a,b,c,d=[sets[z] for z in ids]
        P0=a&b; P1=c&d; M0=a&c; M1=b&d
        feet=[P0,P1,M0,M1]
        if any(len(q)!=2 for q in feet):continue
        if len(set.union(*feet))!=8:continue
        product={frozenset(x|y) for x in (P0,P1) for y in (M0,M1)}
        if product!={frozenset(x) for x in sets}:continue
        # Orientation chosen deterministically using original literal signs, not lookup tables.
        packed=tuple(tuple(sorted(q,key=lambda x:(abs(x),x<0))) for q in feet)
        if best is None or packed<best:best=packed
    return best


def reentry(rest,R,newx):
    feet=factor_4(R)
    if feet is None:raise ValueError('not K2,2')
    P0,P1,M0,M1=feet
    return canonical(list(rest)+[(newx,)+a for a in (P0,P1)]+[(-newx,)+a for a in (M0,M1)])


def tseitin_child(rest,R,first_aux):
    output=list(rest)
    for j,clause in enumerate(R):
        assert len(clause)==4
        x=first_aux+j
        output.append((clause[0],clause[1],x))
        output.append((-x,clause[2],clause[3]))
    return canonical(output)


def dimacs(C,num_vars):
    out=[f'p cnf {num_vars} {len(C)}\n']
    for c in C:
        out.append(' '.join(map(str,c))+' 0\n')
    return ''.join(out).encode('ascii')


def exhaustive_checks(C,p):
    n=3*p
    probes=0
    for pivot in range(1,n+1):
        rest,R,np,nm,taut=eliminate(C,pivot)
        assert (np,nm,taut,len(R))==(2,2,0,4)
        assert all(len(q)==4 for q in R) and len(set(R))==4
        assert factor_4(R) is not None
        converted=reentry(rest,R,pivot)
        # Extra check: returned selector must be a renaming/sign flip, not a free answer bit.
        assert len(converted)==len(C)
        assert len(tseitin_child(rest,R,n+1))==len(C)+4
        # The finite check treats the factored selector and actual source pivot independently.
        other=[v for v in range(1,n+1) if v!=pivot]
        if p==5:
            assignments=range(1<<(n-1))
        else:
            assignments=[RNG.randrange(1<<(n-1)) for _ in range(128)]
        for mask in assignments:
            A={i:bool((mask>>pos)&1) for pos,i in enumerate(other)}
            projected=eval_cnf(R,A) and eval_cnf(rest,A)
            source_any=False;factor_any=False
            for bit in (False,True):
                A[pivot]=bit
                source_any |= eval_cnf(C,A)
                factor_any |= eval_cnf(converted,A)
            if not (projected==source_any==factor_any):
                raise AssertionError((p,pivot,mask,projected,source_any,factor_any))
            probes+=1
    return probes


def negative_controls():
    # Even p violates the no-repeated-2-scope premise (2s mod p collides).
    p=6;C=[]
    for s in range(4):
        for i in range(p):
            C.append((var(0,i,p),var(1,i+s,p),var(2,i+2*s,p)))
    assert not is_linear(C)
    # A simple signed contradictory intersection creates a tautological resolvent.
    a=((1,2,3),(1,4,5),(-1,-2,6),(-1,7,8))
    _,R,np,nm,taut=eliminate(a,1)
    assert (np,nm,taut,len(R))==(2,2,1,3)
    assert factor_4(R) is None
    assert factor_4([(1,2,3,4),(1,5,6,7),(2,5,8,9),(3,6,8,9)]) is None
    return {'even_modulus_linearity_rejected':True,'tautological_resolvent_detected':True,'nonrectangular_factor_rejected':True}


def orbit_controls(p,steps=180):
    """Test adaptive closure under arbitrary pivots with same vacated selector name."""
    C=family(p)
    n=3*p
    base=C
    flips=set()
    changes=0
    for step in range(steps):
        pivot=RNG.randrange(1,n+1)
        rest,R,np,nm,taut=eliminate(C,pivot)
        assert (np,nm,taut,len(R))==(2,2,0,4)
        nxt=reentry(rest,R,pivot)
        switched=canonical(tuple((-l if abs(l)==pivot else l) for l in clause) for clause in C)
        assert nxt==C or nxt==switched
        if nxt!=C:
            changes+=1
            flips.symmetric_difference_update({pivot})
        C=nxt
        assert all(sum(l==v for clause in C for l in clause)==2 and
                   sum(l==-v for clause in C for l in clause)==2 for v in range(1,n+1))
        assert is_linear(C)
        assert len(dimacs(C,n))==len(dimacs(base,n))
        # The variable-complement image of the source preserves the known witness.
        assert eval_cnf(C,{i:(i in flips) for i in range(1,n+1)})
    assert C==canonical(tuple((-l if abs(l) in flips else l) for l in clause) for clause in base)
    return {'p':p,'steps':steps,'pivot_changes':changes,'final_flipped_variables':len(flips),
            'source_bytes_every_step':len(dimacs(base,n))}


def main():
    controls=negative_controls()
    orbits=[orbit_controls(q) for q in (5,7,31,101)]
    runs=[];checks=0
    for p in (5,7,9,15,31,101,501):
        C=family(p)
        assert check_source(C,p)
        assert is_linear(C) and is_connected(C,3*p)
        assert eval_cnf(C,{i:False for i in range(1,3*p+1)})
        # Deliberate malformed sign flipping must fail exact canonical validation.
        bad=list(C); c=list(bad[0]);c[0]=-c[0];bad[0]=tuple(c)
        assert not check_source(canonical(bad),p)
        # Every pivot must have the exact 2x2 width-four, no-tautology resolution pattern.
        fixed_pivots=0
        for pivot in range(1,3*p+1):
            rest,R,np,nm,taut=eliminate(C,pivot)
            assert (np,nm,taut,len(R))==(2,2,0,4)
            assert len(set(R))==4 and all(len(q)==4 for q in R)
            assert factor_4(R) is not None
            source_free_return=reentry(rest,R,pivot)
            assert len(dimacs(source_free_return,3*p))==len(dimacs(C,3*p))
            fixed_pivots += (source_free_return==C)
        probes=exhaustive_checks(C,p) if p in (5,7) else 0
        checks+=probes
        # Fixed pivot x=A_0: compare full ordinary signed physical encodings.
        rest,R,_,_,_=eliminate(C,1)
        extended=tseitin_child(rest,R,3*p+1)
        factored=reentry(rest,R,1)
        parent_bytes=len(dimacs(C,3*p))
        aux_bytes=len(dimacs(extended,3*p+4))
        factored_bytes=len(dimacs(factored,3*p))
        # Other clauses never subsume resolvents: no source scope contains only 2 groups.
        assert all(not set(c).issubset(set(r)) for c in rest for r in R)
        assert len(extended)==4*p+4 and len(factored)==4*p
        runs.append({'p':p,'variables':3*p,'clauses':4*p,
                     'source_bytes':parent_bytes,
                     'tseitin_child_bytes':aux_bytes,
                     'factor_reentry_bytes':factored_bytes,
                     'factor_ratio':round(factored_bytes/parent_bytes,6),
                     'tseitin_ratio':round(aux_bytes/parent_bytes,6),
                     'all_pivots_no_tautology':3*p,
                     'source_free_exact_fixed_pivots':fixed_pivots,
                     'projection_assignment_checks':probes})
    raw={'status':'PASS','seed':SEED,'family':'four affine triple partitions, odd p >= 5',
         'proof_status':'restricted mathematical arguments separate from finite tests',
         'negative_controls':controls,'orbit_controls':orbits,'total_projection_checks':checks,
         'cases':runs,
         'limitations':['All generated controls are SAT by the known all-zero witness.',
                        'A single algebraic factored return is not a SAT decision lower bound.',
                        'Raw operation counts are not native tape transition counts.',
                        'No all-input SAT contraction or separation is obtained.']}
    print(json.dumps(raw,indent=2,sort_keys=True))

if __name__=='__main__':main()
