#!/usr/bin/env python3
"""SELECTOR-LOCALITY59 minimal stdlib reproduction, independently runnable.
Full arbitrary-factor bucket eliminator and raw experiment are in the local
LSPV2_SELECTOR_LOCALITY59_2026-10-23.zip package.
"""
from itertools import product
import random

def shifted_prism(q):
    assert q >= 4
    a=lambda j: 1+(j%q)
    b=lambda j: 1+q+(j%q)
    c=lambda j: 1+2*q+(j%q)
    clauses=[]
    for j in range(q):
        clauses.extend(((a(j-1),a(j),c(j)),
                        (b(j-1),b(j),c(j)),
                        (-a(j-1),-a(j),-c(j+1)),
                        (-b(j-1),-b(j),-c(j+1))))
    return clauses,3*q

def labels_ok(clauses,values):
    return all(any(values[abs(x)]==(x>0) for x in cl) for cl in clauses)

def strict22(clauses,n):
    return (len(clauses)*3 == 4*n and
            all(len(cl)==3 and len(set(map(abs,cl)))==3 for cl in clauses) and
            all(sum(x==v for cl in clauses for x in cl)==2 and
                sum(x==-v for cl in clauses for x in cl)==2
                for v in range(1,n+1)))

def conflicts(clauses):
    # one selected witness index per clause, conflicts iff source complements
    return {(i,a,j,b) for i,C in enumerate(clauses)
            for j,D in enumerate(clauses) if i<j
            for a,x in enumerate(C) for b,y in enumerate(D) if x==-y}

def strong3(clauses):
    bad=conflicts(clauses)
    def ok(i,a,j,b):
        if i>j:i,j,a,b=j,i,b,a
        return (i,a,j,b) not in bad
    for i in range(len(clauses)):
        for j in range(i+1,len(clauses)):
            for a,b in product(range(3),repeat=2):
                if not ok(i,a,j,b):continue
                for k in range(len(clauses)):
                    if k==i or k==j:continue
                    if not any(ok(i,a,k,c) and ok(j,b,k,c)
                               for c in range(3)):return False
    return True

def brute_count(clauses,n):
    return sum(labels_ok(clauses,{i+1:bool(v)
                 for i,v in enumerate(bits)})
                 for bits in product((0,1),repeat=n))

def six_source_audit(trials=100):
    rng=random.Random(2026102359)
    occurrences=[x for i in range(1,7) for x in (i,i,-i,-i)]
    successful=0
    for _ in range(trials):
        while True:
            rng.shuffle(occurrences)
            F=[tuple(occurrences[i:i+3]) for i in range(0,24,3)]
            if all(len(set(map(abs,cl)))==3 for cl in F):break
        assert strict22(F,6)
        assert len(conflicts(F))==24
        assert brute_count(F,6)>0
        successful+=1
    return successful

def prove_path_width_bags(q):
    # Four clause nodes per cyclic column. Each conflict edge must
    # be contained in one of the certified 12-node bags below.
    F,n=shifted_prism(q)
    assert strict22(F,n)
    C=[set(range(4*j,4*j+4)) for j in range(q)]
    bags=[C[0]|C[j]|C[j+1] for j in range(1,q-1)]
    assert max(map(len,bags))<=12
    bad=conflicts(F)
    assert len(bad)==4*n
    assert all(any({i,j}<=bag for bag in bags) for i,_,j,_ in bad)
    # Running intersection: every node's bags form contiguous indices.
    for v in range(4*q):
        idx=[j for j,B in enumerate(bags) if v in B]
        assert idx==list(range(min(idx),max(idx)+1))
    val={i:False for i in range(1,2*q+1)}
    val.update({i:True for i in range(2*q+1,3*q+1)})
    assert labels_ok(F,val)
    return (n,len(F),len(bags),max(map(len,bags)))

def xor3(a,b,c,rhs):
    out=[]
    for bits in product((0,1),repeat=3):
        if (bits[0]^bits[1]^bits[2])==rhs:continue
        out.append(tuple(-v if bit else v for v,bit
                         in zip((a,b,c),bits)))
    return out

def xor_cycle_control(q,flip):
    assert q%2==0
    F=[]
    for j in range(q):
        F+=xor3(j+1,(j+1)%q+1,q+1,int(j==0 and flip))
    n=q+1
    # Linear symbolic check: XOR of every equation equals flip.
    expected=(flip==0)
    observed=(brute_count(F,n)>0)
    assert expected==observed
    return expected

def run():
    assert six_source_audit(100)==100
    for q in (4,6,8,12,20):
        print("strict22_prism",q,prove_path_width_bags(q))
    F=[(1,2,3),(-1,4,5),(-2,6,7),(-3,8,9)]
    assert strong3(F)
    eight=[tuple((-i if bit else i) for i,bit
            in zip((1,2,3),bits)) for bits
           in product((0,1),repeat=3)]
    assert strong3(eight) and brute_count(eight,3)==0
    for q in (4,6,8):
        assert xor_cycle_control(q,0)
        assert not xor_cycle_control(q,1)
    print("PASS: exact22 six-source, path bags, strong3, both-label XOR")

if __name__=="__main__":
    run()
