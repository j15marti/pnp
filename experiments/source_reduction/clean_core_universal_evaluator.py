#!/usr/bin/env python3
"""
CLEANCORE-EVAL1 reproducible finite experiment.

Models k bare type-1 chains, each with its seven satisfying local states.
Every outside mediator y occurs in d clauses, 2 <= d <= max_deg, with at
least one positive and one negative occurrence.  Every mediator clause has
the form (a OR b OR +/-y), where a,b are literals from two distinct chains.

For a complete chain-state challenge, the exact response is whether the
assignment extends to all outside mediators.  Mediators are eliminated exactly
by pairwise resolution.  The script compares:
  * explicit 7^k response-table size;
  * simplified eliminated-CNF clause count;
  * reduced ordered 7-ary MDD node count for sampled chain orders.

The MDD experiment is only a representation diagnostic.  The eliminated CNF
and the direct per-mediator evaluator are already polynomial-size evaluators.
"""

import itertools, random, math, statistics, collections, csv, argparse

STATES = [b for b in itertools.product([0,1], repeat=3) if any(b)]
FALSE = ("FALSE",)

def lit_value(chain_state, coord, neg=False):
    v = chain_state[coord]
    return 1-v if neg else v

def pair_term_value(assignment, term):
    ci, li, ni, cj, lj, nj = term
    return bool(lit_value(assignment[ci], li, ni) or
                lit_value(assignment[cj], lj, nj))

def full_compatibility(assignment, mediators):
    for P,N in mediators:
        all_pos = all(pair_term_value(assignment,t) for t in P)
        all_neg = all(pair_term_value(assignment,t) for t in N)
        if not (all_pos or all_neg):
            return False
    return True

def term_literals(term):
    ci,li,ni,cj,lj,nj = term
    return [(ci,li,ni),(cj,lj,nj)]

def normalize_clause(lits):
    s=set(lits)
    for c,l,n in tuple(s):
        if (c,l,not n) in s:
            return None
    return tuple(sorted(s))

def simplify_cnf(clauses):
    uniq=sorted(set(clauses), key=lambda x:(len(x),x))
    kept=[]
    kept_sets=[]
    for cl in uniq:
        sc=set(cl)
        if any(k.issubset(sc) for k in kept_sets):
            continue
        kept.append(cl)
        kept_sets.append(sc)
    return tuple(kept)

def eliminated_cnf(mediators):
    clauses=[]
    raw=0
    for P,N in mediators:
        for a in P:
            for b in N:
                raw += 1
                cl=normalize_clause(term_literals(a)+term_literals(b))
                if cl is not None:
                    clauses.append(cl)
    return raw, simplify_cnf(clauses)

def eval_cnf(assignment, cnf):
    for cl in cnf:
        if not any(lit_value(assignment[c],l,n) for c,l,n in cl):
            return False
    return True

def random_pair_term(k, rng):
    i,j=rng.sample(range(k),2)
    return (i,rng.randrange(3),bool(rng.randrange(2)),
            j,rng.randrange(3),bool(rng.randrange(2)))

def random_clean_core(k,m,max_deg,seed):
    rng=random.Random(seed)
    meds=[]
    for _ in range(m):
        d=rng.randint(2,max_deg)
        p=rng.randint(1,d-1)
        q=d-p
        P=[random_pair_term(k,rng) for _ in range(p)]
        N=[random_pair_term(k,rng) for _ in range(q)]
        meds.append((P,N))
    return meds

def restrict_cnf(cnf, chain, state):
    if cnf==FALSE:
        return FALSE
    out=[]
    for cl in cnf:
        sat=False
        rem=[]
        for c,l,n in cl:
            if c==chain:
                if lit_value(state,l,n):
                    sat=True
                    break
            else:
                rem.append((c,l,n))
        if sat:
            continue
        if not rem:
            return FALSE
        out.append(tuple(rem))
    return simplify_cnf(out)

def mdd_size(cnf, order):
    unique={}
    memo={}
    next_id=[2]  # 0=false, 1=true
    def rec(depth, f):
        if f==FALSE:
            return 0
        if not f:
            return 1
        key=(depth,f)
        if key in memo:
            return memo[key]
        ch=order[depth]
        children=tuple(rec(depth+1, restrict_cnf(f,ch,s)) for s in STATES)
        if len(set(children))==1:
            memo[key]=children[0]
            return children[0]
        ukey=(depth,children)
        if ukey not in unique:
            unique[ukey]=next_id[0]
            next_id[0]+=1
        memo[key]=unique[ukey]
        return memo[key]
    rec(0,cnf)
    return next_id[0]-2

def best_sampled_mdd(cnf,k,seed,samples):
    rng=random.Random(seed)
    deg=[0]*k
    for cl in cnf:
        for c,_,_ in cl:
            deg[c]+=1
    orders=[
        tuple(range(k)),
        tuple(sorted(range(k), key=lambda c:deg[c])),
        tuple(sorted(range(k), key=lambda c:-deg[c]))
    ]
    seen=set(orders)
    target=min(samples, math.factorial(k))
    while len(orders)<target:
        o=list(range(k)); rng.shuffle(o); o=tuple(o)
        if o not in seen:
            seen.add(o); orders.append(o)
    vals=[mdd_size(cnf,o) for o in orders]
    return min(vals), statistics.median(vals)

def exhaustive_check(k,mediators,cnf):
    for a in itertools.product(STATES, repeat=k):
        if full_compatibility(a,mediators)!=eval_cnf(a,cnf):
            return False
    return True

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out", default="clean_core_eval_results.csv")
    args=ap.parse_args()
    rows=[]
    for k in range(3,9):
        for seed in range(5):
            s=2026100500+k*100+seed
            meds=random_clean_core(k,2*k,4,s)
            raw,cnf=eliminated_cnf(meds)
            if k<=4 and not exhaustive_check(k,meds,cnf):
                raise AssertionError("elimination mismatch")
            best,med=best_sampled_mdd(cnf,k,seed,40)
            rows.append({
                "k":k,"seed":seed,"mediators":len(meds),
                "raw_resolvents":raw,
                "simplified_cnf_clauses":len(cnf),
                "truth_table_entries":7**k,
                "best_sampled_mdd_nodes":best,
                "median_sampled_mdd_nodes":med
            })
    with open(args.out,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)

if __name__=="__main__":
    main()
