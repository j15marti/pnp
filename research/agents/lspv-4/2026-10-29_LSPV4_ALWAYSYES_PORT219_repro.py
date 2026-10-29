#!/usr/bin/env python3
"""LSPV-4 ALWAYSYES-PORT-ACQUISITION219 independent finite reproducer.

No external dependencies. Builds a proper connected 3CNF G_F that is always
SAT, but the exact feasibility of its single Boolean port y=1 is SAT(F).
Checks all nonempty 3-variable clause subsets and randomized instances.
All counts are computational controls, not proof of polynomial hardness.
"""
import itertools
import json
import random
from collections import Counter

SEED = 20261029
checks = 0

def require(condition, description="assertion"):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(description)


def clause_value(clause, mask):
    return any((((mask >> (abs(lit)-1)) & 1) == 1) if lit > 0 else
               (((mask >> (abs(lit)-1)) & 1) == 0) for lit in clause)


def brute_sat(clauses, nvars, fixed=None):
    fixed = fixed or {}
    for mask in range(1 << nvars):
        if any(((mask >> (v-1)) & 1) != bit for v,bit in fixed.items()):
            continue
        if all(clause_value(clause, mask) for clause in clauses):
            return True
    return False


def sat_dpll(clauses, fixed=None):
    """Independent recursive unit-propagation SAT checker."""
    clauses = tuple(tuple(c) for c in clauses)
    init = dict(fixed or {})
    def rec(assignment):
        while True:
            unresolved = []
            singles = []
            for clause in clauses:
                if any((assignment.get(abs(lit)) == (lit > 0)) for lit in clause
                       if abs(lit) in assignment):
                    continue
                rest = [lit for lit in clause if abs(lit) not in assignment]
                if not rest:
                    return False
                unresolved.append(rest)
                if len(rest) == 1:
                    singles.append(rest[0])
            if not unresolved:
                return True
            changed = False
            for lit in singles:
                var, val = abs(lit), (lit > 0)
                if var in assignment:
                    if assignment[var] != val:
                        return False
                else:
                    assignment[var] = val
                    changed = True
            if not changed:
                break
        # Find a current variable, then try both values (one fixed program).
        var = abs(min(unresolved, key=len)[0])
        for value in (False, True):
            next_assign = dict(assignment)
            next_assign[var] = value
            if rec(next_assign):
                return True
        return False
    return rec(init)


def is_proper_three(clauses):
    return all(len(c)==3 and len(set(map(abs,c)))==3 for c in clauses)


def is_connected(clauses):
    if not clauses:
        return False
    used = {abs(l) for c in clauses for l in c}
    adj = {v:set() for v in used}
    for c in clauses:
        v = [abs(l) for l in c]
        for a,b in itertools.combinations(v,2):
            adj[a].add(b); adj[b].add(a)
    seen = {next(iter(used))}
    front = list(seen)
    while front:
        for v in adj[front.pop()]:
            if v not in seen:
                seen.add(v); front.append(v)
    return seen == used


def gate_formula(F, n):
    """Each 4-CNF guard (~y OR l1 OR l2 OR l3) becomes two proper 3CNF.
       The source port is y=n+1, and fresh local split names u_i=n+2+i.
    """
    y = n+1
    out = []
    for i,c in enumerate(F):
        require(len(c)==3 and len(set(map(abs,c)))==3, "source clause improper")
        u = n+2+i
        out.extend([(-y,c[0],u),(-u,c[1],c[2])])
    return out,y,n+len(F)+1


def force_port(y, value, start_var):
    """Four proper 3-clauses enforce y=value, two fresh auxiliary names."""
    a,b = start_var,start_var+1
    lit = y if value else -y
    return [(lit,a,b),(lit,a,-b),(lit,-a,b),(lit,-a,-b)]


def encoded_bits(cnf, n):
    # Fully physically printed standard DIMACS, no succinct oracle names.
    lines=[f"p cnf {n} {len(cnf)}"]
    lines.extend(' '.join(str(l) for l in c)+" 0" for c in cnf)
    return ('\n'.join(lines)+'\n').encode('ascii')


def exercise(F,n,do_brute_g=False):
    require(is_proper_three(F), 'proper source')
    G,y,nG=gate_formula(F,n)
    require(is_proper_three(G), 'proper target')
    require(is_connected(G), 'connected target')
    require(len(G)==2*len(F),'output clause count')
    require(nG==n+len(F)+1,'output variable count')
    original = brute_sat(F,n)
    require(sat_dpll(F)==original,'source DPLL versus brute')
    require(sat_dpll(G)==True,'constructed source must always be SAT')
    require(sat_dpll(G,{y:0})==True,'port 0 always feasible')
    require(sat_dpll(G,{y:1})==original,'port 1 iff original SAT')
    for val in (0,1):
        ctx = force_port(y,val,nG+1)
        require(is_proper_three(ctx),'proper forced-port context')
        require(is_connected(G+ctx),'context remains connected')
        want = True if val==0 else original
        require(sat_dpll(G+ctx)==want,'contextual SAT equivalence')
    if do_brute_g:
        for val in (0,1):
            require(brute_sat(G,nG,{y:val})==(True if val==0 else original),
                    'independent full extension enumeration')
    source_bytes=len(encoded_bits(F,n))
    child_bytes=len(encoded_bits(G,nG))
    return original,source_bytes,child_bytes


def main():
    rng = random.Random(SEED)
    # All eight proper clause sign patterns on three names.
    all3 = [tuple((i+1) if (bits>>i)&1 else -(i+1) for i in range(3))
            for bits in range(8)]
    totals=Counter()
    for clause_mask in range(1,1<<8):
        F=[all3[i] for i in range(8) if (clause_mask>>i)&1]
        answer,_,_=exercise(F,3,do_brute_g=(len(F)<=4))
        totals['exhaustive_formulas']+=1
        totals['exhaustive_SAT' if answer else 'exhaustive_UNSAT']+=1
        if len(F)<=4:
            totals['independent_extension_cases']+=1
    for n in range(4,9):
        for i in range(120):
            m=rng.randrange(2, min(3*n+1,22))
            F=[]
            for _ in range(m):
                vs=rng.sample(range(1,n+1),3)
                F.append(tuple(v if rng.randrange(2) else -v for v in vs))
            answer,_,_=exercise(F,n,do_brute_g=(n<=4 and m<=4))
            totals['random_formulas']+=1
            totals['random_SAT' if answer else 'random_UNSAT']+=1
    # Controlled UNSAT controls on every larger variable count: the eight
    # sign patterns over one triple forbid all eight local assignments.
    for n in range(4,9):
        for _ in range(50):
            vs=rng.sample(range(1,n+1),3)
            F=[tuple(v if (bits>>i)&1 else -v for i,v in enumerate(vs))
               for bits in range(8)]
            for _ in range(rng.randrange(0,9)):
                tri=rng.sample(range(1,n+1),3)
                F.append(tuple(v if rng.randrange(2) else -v for v in tri))
            answer,_,_=exercise(F,n)
            require(answer is False,'unsat control')
            totals['controlled_UNSAT']+=1
    F_yes=[(1,2,3)]*4 + [(-1,-2,-3)]*4
    F_no=all3
    _,b_y,g_y=exercise(F_yes,3)
    _,b_n,g_n=exercise(F_no,3)
    require(b_y==b_n and g_y==g_n,'matched physical source and target lengths')
    Gy,y,ny=gate_formula(F_yes,3)
    Gn,_,nn=gate_formula(F_no,3)
    require(sat_dpll(Gy) and sat_dpll(Gn),'both matched sources YES')
    require(sat_dpll(Gy,{y:1}) and not sat_dpll(Gn,{y:1}), 'port polarity')
    require(sat_dpll(Gy,{y:0}) and sat_dpll(Gn,{y:0}), 'same trivial 0 witness')
    result={
       'status':'PASS',
       'seed':SEED,
       'checks':checks,
       'counts':dict(sorted(totals.items())),
       'matched_pair':{
           'n_input':3,'m_input':8,
           'source_bytes_each':b_y,'gated_bytes_each':g_y,
           'source_SAT':[True,False],
           'gated_SAT':[True,True],
           'port0_feasible':[True,True],
           'port1_feasible':[True,False],
           'gated_clause_count':len(Gy),
           'gated_variable_count':ny
       },
       'proof_status':'Formal reduction, not a proof that P != NP.',
       'caveats':[
           'Connected and proper 3CNF, not signed exact-(2,2).',
           'All gated source inputs are satisfiable.',
           'Computing the one-port relation is NP-hard, not an unconditional superpolynomial bound.',
           'No universal SAT shrinking algorithm is constructed.',
           'Finite tests are not a kernel-verified proof.'
       ]
    }
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
