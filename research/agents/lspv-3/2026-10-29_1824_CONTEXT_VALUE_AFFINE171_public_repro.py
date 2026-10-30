#!/usr/bin/env python3
"""Independent compact proof controls, LSPV-3 CONTEXT-VALUE-AFFINE171.
Source row equations are (integer bitmask, binary RHS). This script uses
brute-force source-row XOR certificates, NOT a unit-cost word-TM claim.
"""
import itertools,json,random,hashlib
rng=random.Random(1711029)
def p(v):return v.bit_count()%2
def sat(rows,x):return all(p(mask&x)==rhs for mask,rhs in rows)
def models(A,B,b,y,z):
    return [(x,yy,zz) for x in range(1<<b) for yy in range(1<<y)
            for zz in range(1<<z) if sat(A,x|(yy<<b)) and sat(B,x|(zz<<b))]
def projection(A,b,y):
    # Enumerate the entire left-nullspace of M_Y; redundancy is intentional.
    m=len(A);out=[];seen=set()
    for lam in range(1<<m):
        full=rhs=0
        for i,(mask,c) in enumerate(A):
            if (lam>>i)&1:full^=mask;rhs^=c
        if full>>b==0 and (full&((1<<b)-1),rhs) not in seen:
            pair=(full&((1<<b)-1),rhs)
            out.append(pair);seen.add(pair)
    return out

def source_no_cert(A,B,b,y,z):
    # Exhaust every original row-combination for small test instances.
    rows=A+[((mask&((1<<b)-1))|((mask>>b)<<(b+y)),rhs)
            for mask,rhs in B]
    for subset in range(1,1<<len(rows)):
        mm=rr=0
        for i,(mask,rhs) in enumerate(rows):
            if (subset>>i)&1:mm^=mask;rr^=rhs
        if mm==0 and rr==1:return subset
    return None

def run():
    counts={'cases':0,'SAT':0,'UNSAT':0,'projection_checks':0,
            'source_NO_proofs':0,'distinct_rank_one_functions':{}}
    for b in range(1,5):
        answers={tuple(int(p(a&x)==beta) for x in range(1<<b))
                 for a in range(1<<b) for beta in (0,1)}
        assert len(answers)==1<<(b+1)
        counts['distinct_rank_one_functions'][str(b)]=len(answers)
    for _ in range(300):
        b=rng.randint(1,3);y=rng.randint(0,2);z=rng.randint(0,2)
        A=[(rng.randrange(1<<(b+y)),rng.randrange(2))
           for _ in range(rng.randrange(5))]
        B=[(rng.randrange(1<<(b+z)),rng.randrange(2))
           for _ in range(rng.randrange(5))]
        R=projection(A,b,y)
        for x in range(1<<b):
            assert sat(R,x)==any(sat(A,x|(yy<<b)) for yy in range(1<<y))
            counts['projection_checks']+=1
        actual=models(A,B,b,y,z)
        if actual:
            counts['SAT']+=1
            assert sat(A,actual[0][0]|(actual[0][1]<<b))
        else:
            counts['UNSAT']+=1
            assert source_no_cert(A,B,b,y,z) is not None
            counts['source_NO_proofs']+=1
        counts['cases']+=1
    # XOR source shares: individual target entropy gain 0, joint gain 1.
    samples=[(a,b,a^b) for a,b in itertools.product((0,1),repeat=2)]
    assert len({t for a,b,t in samples})==2
    assert all(len({t for x,y,t in samples if x==a})==2 for a in (0,1))
    assert all(len({t for x,y,t in samples if y==b})==2 for b in (0,1))
    assert all(len({t for x,y,t in samples if x==a and y==b})==1
               for a,b in itertools.product((0,1),repeat=2))
    counts['xor_synergy']=1
    counts['direct_macro_greedy_ratios']=[(1<<n)//2 for n in (2,4,8,12,16)]
    print(json.dumps(counts,sort_keys=True,indent=2))
if __name__=='__main__':run()
