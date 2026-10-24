#!/usr/bin/env python3
"""Independent AFFINE-BIJUNCTIVE-GATE75 small-case reproducer, standard library only."""
from itertools import product
import json

def cnf(q,bits):
    assert q>=4 and q%2==0 and len(bits)==q
    binary=[]
    for i in range(q-1):
        a=i+1;b=i+2
        binary.extend([(-a,b),(a,-b)])
    ternary=[]
    for i in range(q):
        a=q+((i-1)%q)+1;b=q+i+1;c=i+1
        for left,right in product((0,1),repeat=2):
            fail=1^bits[i]^left^right
            ternary.append((a if left==0 else -a,
                            b if right==0 else -b,
                            c if fail==0 else -c))
    return tuple(binary),tuple(ternary)

def models(n,clauses):
    count=0
    for vals in product((False,True),repeat=n):
        if all(any(vals[abs(a)-1]==(a>0) for a in c) for c in clauses):
            count+=1
    return count

def gf2rank(vectors):
    piv={}
    for v in vectors:
        while v:
            j=v.bit_length()-1
            if j not in piv:
                piv[j]=v
                break
            v^=piv[j]
    return len(piv)

def parity_projection(q):
    rows=[1<<i for i in range(q-1)]+[(1<<(q-1))-1]
    return {'s':len(set(rows)),'d':gf2rank(rows),
            'excess':len(set(rows))-gf2rank(rows)}

def main():
    checks=0;examples=[]
    for q in (4,6):
        for word in range(1<<q):
            bits=[(word>>i)&1 for i in range(q)]
            binary,ternary=cnf(q,bits)
            exact=models(2*q,binary+ternary)
            expected=4 if word.bit_count()%2==0 else 0
            assert exact==expected
            assert models(2*q,binary)>0
            assert models(2*q,ternary)>0
            checks+=3
        assert parity_projection(q)=={'s':q,'d':q-1,'excess':1}
        checks+=1
        examples.append({'q':q,'even_charge_models':4,'odd_charge_models':0,
                         'raw_backdoor':q//2,'semantic_backdoor':q-2})
    for q in (4,6,8,16,32,128,1024):
        for syndrome in (0,1):
            beta=[syndrome]+[0]*(q-1)
            _,t0=cnf(q,beta)
            for i in range(q):
                other=beta.copy();other[i]^=1
                _,t1=cnf(q,other)
                assert all(t0[j]==t1[j] for j in range(4*q) if j//4!=i)
                assert all(t0[4*i+j][:2]==t1[4*i+j][:2]
                           and t0[4*i+j][2]==-t1[4*i+j][2]
                           for j in range(4))
                checks+=1
    return {'study':'AFFINE_BIJUNCTIVE_GATE75_MINI','checks':checks,
            'failures':0,'examples':examples,'scope':
            'Finite verification only; universal SAT lower bound OPEN'}

if __name__=='__main__':
    print(json.dumps(main(),indent=2))
