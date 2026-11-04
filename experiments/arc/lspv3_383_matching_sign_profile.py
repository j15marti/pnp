#!/usr/bin/env python3
"""LSPV-3/383 signed hypergraph matching-mask controls. No packages needed."""
import itertools, json, random, hashlib, sys

SEED=3832026

def clause_list(n, disabled_mask):
    x=lambda i,j: 1+i*n+j
    p=lambda i,j: 1+n*n+i*n+j
    clauses=[]
    for i in range(n): clauses.append([x(i,j) for j in range(n)])
    for j in range(n): clauses.append([x(i,j) for i in range(n)])
    for i in range(n):
        for j in range(n):
            for k in range(j+1,n): clauses.append([-x(i,j),-x(i,k)])
    for j in range(n):
        for i in range(n):
            for k in range(i+1,n): clauses.append([-x(i,j),-x(k,j)])
    for i in range(n):
        for j in range(n): clauses.append([p(i,j),-x(i,j)])
    for i in range(n):
        for j in range(n):
            e=i*n+j
            clauses.append([-p(i,j)] if (disabled_mask>>e)&1 else [p(i,j)])
    return clauses

def eval_cnf(clauses, n, disabled_mask, choice):
    n2=n*n
    def litval(lit):
        ix=abs(lit)-1
        val=((choice>>ix)&1) if ix<n2 else (not ((disabled_mask>>(ix-n2))&1))
        return bool(val) if lit>0 else not bool(val)
    return all(any(litval(lit) for lit in c) for c in clauses)

def match_perm(n, disabled):
    for pi in itertools.permutations(range(n)):
        if all(not ((disabled>>(i*n+pi[i]))&1) for i in range(n)):
            return list(pi)
    return None

def poly_dp(n, disabled):
    # Diagnostic DP; production algorithm uses polynomial-time bipartite matching.
    state={0}
    for i in range(n):
        new=set()
        for used in state:
            for j in range(n):
                if not (used>>j)&1 and not (disabled>>(i*n+j))&1:
                    new.add(used|(1<<j))
        state=new
    return bool(state)

def brute_x(n, disabled, clauses):
    hits=0
    for x in range(1<<(n*n)):
        if eval_cnf(clauses,n,disabled,x):hits+=1
    return hits

def check(n, masks, brute=True):
    stats={'n':n,'masks':len(masks),'sat':0,'unsat':0,'clauses':None,'occurrences':None,'variables':2*n*n,
           'checks':0,'mask_digest':None, 'canonical_zero_hits':None}
    digest=hashlib.sha256()
    base=None
    for a in masks:
        cl=clause_list(n,a)
        if base is None:
            stats['clauses']=len(cl); stats['occurrences']=sum(map(len,cl))
            base=[tuple(map(abs,c)) for c in cl]
            assert len(cl)==n**3+n*n+2*n
            assert sum(map(len,cl))==2*n**3+3*n*n
        assert [tuple(map(abs,c)) for c in cl]==base
        assert all(0<abs(x)<=2*n*n for c in cl for x in c)
        pi=match_perm(n,a)
        dp=poly_dp(n,a)
        assert (pi is not None)==dp
        if brute:
            exact=brute_x(n,a,cl)
            assert (exact>0)==dp
            num_perm=sum(all(not ((a>>(i*n+p[i]))&1) for i in range(n)) for p in itertools.permutations(range(n)))
            assert exact==num_perm
            stats['checks']+=1<<(n*n)
            if a==0:stats['canonical_zero_hits']=exact
        stats['checks']+=5
        stats['sat' if dp else 'unsat']+=1
        digest.update(f'{a}:{int(dp)};'.encode())
    stats['mask_digest']=digest.hexdigest()
    return stats

def monotone(n):
    B=1<<(n*n)
    labels=[match_perm(n,a) is None for a in range(B)]
    checks=0
    for a in range(B):
        for b in range(B):
            if (a&b)==a:
                assert not labels[a] or labels[b]
                checks+=1
    return checks

def corruptions():
    n=2;cl=clause_list(n,0)
    def structural(c):
        base=clause_list(n,0)
        return len(c)==len(base) and all(len(c[i])==len(base[i]) and
          tuple(map(abs,c[i]))==tuple(map(abs,base[i])) for i in range(len(c))) and \
          c[:len(c)-n*n]==base[:len(base)-n*n] and \
          all(c[-n*n+i] in ([n*n+i+1],[-(n*n+i+1)]) for i in range(n*n))
    assert structural(cl)
    mutations=[]
    mutations.append(cl[:-1])
    a=[z[:] for z in cl];a[0][0]=0;mutations.append(a)
    a=[z[:] for z in cl];a[-1]=[999];mutations.append(a)
    a=[z[:] for z in cl];a[0][0]=-a[0][0];mutations.append(a)
    a=[z[:] for z in cl];a[-1]=[a[-1][0],-a[-1][0]];mutations.append(a)
    a=[z[:] for z in cl];a[len(cl)-n*n-1]=[-abs(a[len(cl)-n*n-1][0]),a[len(cl)-n*n-1][1]];mutations.append(a)
    assert all(not structural(m) for m in mutations)
    return len(mutations)

if __name__=='__main__':
    assert len(sys.argv)==2
    n4={0,(1<<16)-1}
    for i in range(16):n4.add(1<<i);n4.add(((1<<16)-1)^(1<<i))
    rng=random.Random(SEED)
    while len(n4)<90:n4.add(rng.randrange(1<<16))
    result={'run_id':'LSPV3-383','seed':SEED,'status':'COMPUTATIONAL',
            'cases':[check(2,list(range(1<<4))),check(3,list(range(1<<9))),check(4,sorted(n4),False)],
            'monotonicity_checks':{str(n):monotone(n) for n in [2,3]},
            'malformed_rejections':corruptions(),
            'model':'same signed incidence; polarity of n^2 unit p literals encodes removed edges',
            'unproved':'no global R_mix341 proof-size or SAT machine lower bound follows'}
    with open(sys.argv[1],'w') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(result,sort_keys=True))
