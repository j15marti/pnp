#!/usr/bin/env python3
"""RETURNMAP2 finite controls: restriction preservation, cover bound, recurrence sweep."""
import argparse,itertools,json,math,random

def sat_clause(cl,a):
    return any((a[abs(l)-1] if l>0 else 1-a[abs(l)-1]) for l in cl)
def sat_formula(F,a): return all(sat_clause(c,a) for c in F)

def unique_formula(n,target):
    # CNF of unit clauses, unique satisfying assignment target.
    return [[i+1 if target[i] else -(i+1)] for i in range(n)]

def restriction_preserves(F,n,fixed):
    # fixed dict var-index -> bit
    live=[i for i in range(n) if i not in fixed]
    for bits in itertools.product([0,1],repeat=len(live)):
        a=[0]*n
        for i,b in fixed.items():a[i]=b
        for i,b in zip(live,bits):a[i]=b
        if sat_formula(F,a):return True
    return False

def fixed_restrictions(n,m):
    for live in itertools.combinations(range(n),m):
        L=set(live); fixedvars=[i for i in range(n) if i not in L]
        for vals in itertools.product([0,1],repeat=len(fixedvars)):
            yield {i:b for i,b in zip(fixedvars,vals)}

def recurrence(eta,theta,r):
    if theta>=1:return None
    return max(r,eta/(1-theta))

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--seed",type=int,default=1618033);args=ap.parse_args()
    rng=random.Random(args.seed)
    restriction=[]
    for n,m in [(4,1),(4,2),(6,2),(6,3),(8,4)]:
        target=[rng.randrange(2) for _ in range(n)]
        F=unique_formula(n,target)
        rs=list(fixed_restrictions(n,m))
        good=sum(restriction_preserves(F,n,r) for r in rs)
        restriction.append({"n":n,"m":m,"restrictions":len(rs),"preserve":good,
          "fraction":good/len(rs),"expected_fraction_per_live_set":2**(-(n-m))})
    cover=[]
    for n in [16,32,64,128]:
        for qexp in [0,1,2,3]:
            q=max(1,n**qexp)
            m_needed=math.ceil(n-math.log2(q))
            cover.append({"n":n,"q":q,"m_min_from_q2m_ge2n":m_needed,"variables_fixed_max":n-m_needed})
    sweep=[]
    vals=[0,.125,.25,.5,.75,.875]
    for eta,theta,r in itertools.product(vals,vals,vals):
        c=recurrence(eta,theta,r)
        if c is not None and c<1:
            sweep.append({"eta":eta,"theta":theta,"r":r,"fixed_point":c})
    print(json.dumps({"status":"COMPUTATIONAL finite controls only","seed":args.seed,
      "restriction_unique_sat_controls":restriction,
      "cover_controls":cover,
      "recurrence_subunit_examples":sweep[:40],"recurrence_subunit_count":len(sweep),
      "guards":["Finite tests do not prove asymptotic SAT lower bounds.",
       "Unique-unit CNFs are deliberately easy hostile controls.",
       "A favorable recurrence point is meaningless until a source-certified SAT return instantiates its parameters."]},indent=2))
if __name__=="__main__":main()
