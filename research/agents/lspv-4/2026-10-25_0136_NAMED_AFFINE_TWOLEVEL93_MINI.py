#!/usr/bin/env python3
"""Independent compact reproducer for the scoped XOR-cycle profile identities."""
from itertools import product
import json

checks = 0

def must(condition):
    global checks
    checks += 1
    assert condition, checks

def relation(bit):
    return ((1,0),(0,1)) if bit == 0 else ((0,1),(1,0))

def mul(a,b):
    return tuple(tuple(sum(a[i][t]*b[t][j] for t in (0,1))
                       for j in (0,1)) for i in (0,1))

def parity(bits):
    return sum(bits)%2

def child_matrix(bits):
    k = len(bits)
    p = relation(parity(bits))
    return tuple(tuple((16*4**k)*p[i][j] for j in (0,1))
                 for i in (0,1))

def half_clauses(k, bits):
    clauses=[]
    for j,b in enumerate(bits):
        x,y=j+1,j+2
        pairs=((-x,y),(x,-y)) if b==0 else ((x,y),(-x,-y))
        for h,pair in enumerate(pairs):
            u=k+2+2*j+h
            clauses.extend([(*pair,u),(*pair,-u)])
    return clauses

def pinned(bits, start, end):
    k=len(bits)
    clauses=half_clauses(k,bits)
    for var,val,a,b in ((1,start,3*k+2,3*k+3),
                        (k+1,end,3*k+4,3*k+5)):
        literal=var if val else -var
        for sa,sb in product((1,-1),repeat=2):
            clauses.append((literal,sa*a,sb*b))
    must(len(clauses)==4*k+8)
    must(all(len({abs(v) for v in c})==3 for c in clauses))
    return clauses,3*k+5

def brute_count(cnf,n):
    return sum(all(any(((z>>(abs(l)-1))&1)==(l>0) for l in c)
                   for c in cnf) for z in range(1<<n))

orientations=0
for q in range(3,10):
    for bits in product((0,1),repeat=q):
        orientations+=1
        B=relation(0)
        W=relation(0)
        blocks=0
        for lo in range(0,q,3):
            group=bits[lo:lo+3]
            B=mul(B,relation(parity(group)))
            W=mul(W,child_matrix(group))
            blocks+=1
        truth=(B[0][0]+B[1][1])>0
        must(truth==(parity(bits)==0))
        must((W[0][0]+W[1][1])//(16**blocks) ==
             ((2*4**q) if truth else 0))
        must((W[0][0]+W[1][1])%(16**blocks)==0)
        for cut in range(1,q):
            L=child_matrix(bits[:cut])
            R=child_matrix(bits[cut:])
            D=child_matrix(bits)
            A=mul(L,R)
            must(all(A[i][j]==16*D[i][j]
                     for i,j in product((0,1),repeat=2)))

child_counts=0
for k in (1,2,3):
    for bits in product((0,1),repeat=k):
        for entry,exit in product((0,1),repeat=2):
            cnf,n=pinned(bits,entry,exit)
            actual=brute_count(cnf,n)
            expected=child_matrix(bits)[entry][exit]
            must(actual==expected)
            child_counts+=1

triples=((0,1,2),(0,1,3),(0,2,3),(1,2,3))
for selected in range(1<<4):
    counts=[]
    for signed in (False,True):
        valid=0
        for bits in product((0,1),repeat=4):
            ok=True
            for i in range(4):
                if not ((selected>>i)&1):
                    continue
                row=[bits[j] for j in triples[i]]
                if signed and i==3:
                    row[0]=1-row[0]
                if sum(row)!=1:
                    ok=False
                    break
            valid+=ok
        counts.append(valid)
    must((counts[0]>0 and counts[1]>0) if selected!=15
         else (counts[0]==0 and counts[1]==1))

print(json.dumps({'run':'NAMED_AFFINE_TWOLEVEL93_MINI', 'status':'PASS',
                  'checks':checks,'orientations':orientations,
                  'ordinary_pinned_3CNF_brute_counts':child_counts,
                  'seed':None,'scope':'finite restricted controls'},sort_keys=True))
