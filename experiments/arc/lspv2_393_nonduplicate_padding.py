#!/usr/bin/env python3
"""Independent source-deletion/sign-flip exhaustiveness for LSPV-2/393.
Pure Python, no dependencies, deterministic exhaustive finite controls.
"""
import itertools, json, hashlib

def canonical_clause(ls):
    a=frozenset(int(x) for x in ls)
    if any(-x in a for x in a): raise ValueError('tautology')
    return a

def sat(clauses, variables):
    for bits in itertools.product((False,True), repeat=variables):
        if all(any(bits[abs(l)-1] == (l>0) for l in c) for c in clauses):
            return True
    return False

def pad(F, n):
    z=n+1
    return [d for C in F for d in (C, C|{z}, C|{-z})]

def essential_count(F,n):
    if sat(F,n): return 0
    return sum(sat(F[:i]+F[i+1:],n) for i in range(len(F)))

def flip_count(F,n):
    if sat(F,n): return 0
    k=0
    for i,C in enumerate(F):
        for l in C:
            D=list(F); D[i]=(C-{l})|{-l}
            if sat(D,n): k+=1
    return k

def res(P,Q,p):
    if p in P and -p in Q: return (P-{p})|(Q-{-p})
    if -p in P and p in Q: return (P-{-p})|(Q-{p})
    raise ValueError('invalid resolution pivot')

def triangle():
    return [canonical_clause(c) for c in (
        (1,2),(-1,-2),(2,3),(-2,-3),(1,3),(-1,-3))]

def proof5(F):
    R=[]
    R.append(res(F[0],F[5],1))
    R.append(res(R[0],F[3],2))
    R.append(res(F[1],F[4],1))
    R.append(res(R[2],F[2],2))
    R.append(res(R[1],R[3],3))
    assert list(map(lambda c:tuple(sorted(c)),R))==[(-3,2),(-3,),(-2,3),(3,),()]
    return R

def run():
    universe=[canonical_clause((i,)) for i in (1,-1,2,-2)]+[canonical_clause(x) for x in itertools.product((1,-1),(2,-2))]
    counts={'input_formulas':0,'sat':0,'unsat':0,'padded_single_clause_removal_checks':0,'padded_literal_flip_checks':0,'unsat_with_essential_original':0,'all_checks_passed':True}
    for mask in range(1<<len(universe)):
        F=[universe[i] for i in range(len(universe)) if mask>>i&1]
        H=pad(F,2); orig_sat=sat(F,2)
        counts['input_formulas']+=1
        counts['sat' if orig_sat else 'unsat']+=1
        assert sat(H,3)==orig_sat
        assert len(set(map(frozenset,H)))==len(H)
        if not orig_sat and essential_count(F,2)>0: counts['unsat_with_essential_original']+=1
        for i in range(len(H)):
            assert sat(H[:i]+H[i+1:],3)==orig_sat
            counts['padded_single_clause_removal_checks']+=1
            if not orig_sat:
                for l in H[i]:
                    H1=H.copy();H1[i]=(H[i]-{l})|{-l}
                    assert not sat(H1,3)
                    counts['padded_literal_flip_checks']+=1
    F=triangle();H=pad(F,3);R=proof5(F)
    assert not sat(F,3) and not sat(H,4)
    assert essential_count(F,3)==6 and flip_count(F,3)==12
    assert essential_count(H,4)==0 and flip_count(H,4)==0
    assert len(R)==5 and not R[-1]
    assert sum(len(x) for x in H)==3*sum(len(x) for x in F)+2*len(F)
    counts['triangle']={'source_clauses':6,'padded_clauses':len(H),'original_essential':essential_count(F,3),'padded_essential':essential_count(H,4),'original_sign_sensitive':flip_count(F,3),'padded_sign_sensitive':flip_count(H,4),'resolution_upper_nodes':len(R),'orig_literal_occurrences':sum(map(len,F)),'padded_literal_occurrences':sum(map(len,H))}
    counts['sha256']=hashlib.sha256(json.dumps(counts,sort_keys=True).encode()).hexdigest()
    return counts

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
