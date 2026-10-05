#!/usr/bin/env python3
"""DUALPRIME1 finite hostile test for literal-prime SAT semantics.

Each variable xi receives two distinct primes t_i and f_i. An assignment is
the square-free product selecting exactly one prime from each pair. Divisibility
then decodes the assignment exactly. Tests whether clause satisfaction can be
expressed by divisibility predicates and whether multiplication-only clause
aggregation preserves enough information for exact SAT semantics.

COMPUTATIONAL only; no asymptotic lower bound.
"""
import itertools,json,math

def primes(k):
    out=[]; x=2
    while len(out)<k:
        ok=all(x%d for d in range(2,int(math.isqrt(x))+1))
        if ok: out.append(x)
        x+=1
    return out

def enc_assignment(bits,tp,fp):
    z=1
    for b,t,f in zip(bits,tp,fp): z*=t if b else f
    return z

def decode(z,tp,fp):
    out=[]
    for t,f in zip(tp,fp):
        dt,df=(z%t==0),(z%f==0)
        if dt==df:return None
        out.append(1 if dt else 0)
    return tuple(out)

def litprime(lit,tp,fp):
    i=abs(lit)-1
    return tp[i] if lit>0 else fp[i]

def clause_sat_div(z,cl,tp,fp):
    return any(z%litprime(l,tp,fp)==0 for l in cl)

def formula_sat(bits,F):
    return all(any(bits[abs(l)-1] if l>0 else not bits[abs(l)-1] for l in c) for c in F)

def main():
    n=5; ps=primes(2*n); tp=ps[::2]; fp=ps[1::2]
    # Includes the user's style: x1 true/false have separate primes.
    assignments=list(itertools.product([0,1],repeat=n))
    roundtrip=all(decode(enc_assignment(a,tp,fp),tp,fp)==a for a in assignments)
    clauses=list(itertools.combinations([i for i in range(1,n+1)],3))
    F=[[1,-2,3],[-1,4,5],[2,-3,-5]]
    semantic=all(formula_sat(a,F)==all(clause_sat_div(enc_assignment(a,tp,fp),c,tp,fp) for c in F) for a in assignments)

    # Multiplying the primes occurring in a clause records occurrence, not OR truth.
    # Show two assignments with same gcd-pattern against clause product can differ
    # only if exact per-literal divisibility information is discarded.
    cl=F[0]; cp=math.prod(litprime(l,tp,fp) for l in cl)
    groups={}
    for a in assignments:
        z=enc_assignment(a,tp,fp); g=math.gcd(z,cp)
        groups.setdefault(g,set()).add(clause_sat_div(z,cl,tp,fp))
    gcd_exact=all(len(v)==1 for v in groups.values())

    print(json.dumps({
      "status":"COMPUTATIONAL finite exact-semantics control",
      "n":n,"true_primes":tp,"false_primes":fp,
      "user_example_note":"first pair is the automatically chosen analogue of distinct true/false primes",
      "assignment_roundtrip":roundtrip,
      "formula_divisibility_semantics_exact":semantic,
      "clause_product_gcd_preserves_clause_truth":gcd_exact,
      "assignment_code_max_bits":max(enc_assignment(a,tp,fp).bit_length() for a in assignments),
      "observations":[
       "Unique factorization gives an exact literal-set namespace.",
       "Clause OR is tested by divisibility by at least one satisfying-literal prime, not by multiplication alone.",
       "The encoder already knows all factors; later factoring is not a hardness charge.",
       "A SAT-semantic return theorem still needs a smaller ordinary-CNF output or a model-matched many-query combiner."
      ]},indent=2))
if __name__=="__main__":main()
