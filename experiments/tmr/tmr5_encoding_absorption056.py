#!/usr/bin/env python3
"""TMR-5/056, independent exact-source length and exponent audit.

This is a finite checker. The symbolic all-input argument is in the accompanying report.
No formula, SAT solver, or theorem is assumed as an oracle.
"""
import json
import math
import sys

REV = 'tmr5-encoding-absorption056.v1'
PIN = '16a5ce41304fcdaea4e0be7c132e1c361dc26da5'
assertions = 0
cases = 0
worst_ratio = -1.0
worst_case = None
min_margin = float('inf')


def check(cond, tag):
    global assertions
    assertions += 1
    if not cond:
        raise AssertionError(tag)


def bound(n, k, m):
    global cases, worst_ratio, worst_case, min_margin
    assert n >= 4 and k >= 1 and m >= max(2, (n + k - 1)//k)
    x = k*m
    w = (2*n).bit_length()
    B = k+n+2+x*w  # exactly encInput length for m clauses with k slots
    y = math.log2(n)
    E_m = x / math.sqrt(math.log2(m))
    E_n = k*k*n*math.log2(y)/math.sqrt(y)
    E = min(E_m, E_n)
    lb = math.log2(B)
    check(B == k+1+n+1 + m*k*w, 'real formal input length')
    check(n <= x, 'AllOccur capacity')
    check(lb <= 3*math.log2(x)+1e-11, 'input logarithm cubic bound')
    check(lb <= 4*E_m+1e-11, 'clause bound')
    check(lb <= 8*E_n+1e-11, 'variable bound')
    check(lb <= 8*E+1e-11, 'combined input absorption')
    ratio = lb/E
    margin = 8*E-lb
    if ratio>worst_ratio:
        worst_ratio=ratio
        worst_case=(n,k,str(m),B,round(E,6),round(lb,6))
    min_margin=min(min_margin,margin)
    cases += 1


for n in range(4,129):
    for k in range(1,33):
        lower=max(2,(n+k-1)//k)
        upper=(2*n+1)**k
        ms={lower,upper, max(lower,min(upper,4)), max(lower,min(upper,16))}
        for z in range(0,36):
            u=2**z
            if lower<=u<=upper:
                ms.add(u)
            if lower<=u+1<=upper:
                ms.add(u+1)
        for m in sorted(ms):
            bound(n,k,m)

# The formula encoding uses a unary k, unary n, and precisely m*k fixed-length slots.
# Verify actual low-first slot encoder for small valid, all-variable-occurring formula instances.
bit_cases=0
for n in range(4,9):
    for k in range(1,6):
        m=max(2,(n+k-1)//k)
        clauses=[]
        for j in range(m):
            cl=[]
            for z in range(k):
                i=j*k+z
                if i<n:
                    cl.append((i,(i%2)==0))
            clauses.append(cl)
        check(len(set(tuple(z) for z in clauses)) == m, 'NoDup')
        check(set(range(n))=={i for C in clauses for i,_ in C}, 'AllOccur')
        w=(2*n).bit_length()
        bits=[1]*k+[0]+[1]*n+[0]
        for C in clauses:
            for j in range(k):
                slot=0 if j>=len(C) else 2*C[j][0]+1+int(C[j][1])
                bits += [(slot>>p)&1 for p in range(w)]
        check(len(bits)==k+n+2+m*k*w, 'exact constructed bits')
        off=k+n+2
        decoded=[]
        for z in range(m):
            reconstructed=[]
            for j in range(k):
                s=sum(bits[off+p]<<p for p in range(w))
                off+=w
                if s:
                    v=(s-1)//2
                    positive=(s%2==0)
                    reconstructed.append((v,positive))
            decoded.append(reconstructed)
        check(decoded==clauses, 'source word exact decode')
        bit_cases += 1

print(json.dumps({'revision':REV,'upstream_pin':PIN,'scientific_scope':'finite checker for a separate all-input symbolic inequality', 'n_range':[4,128], 'k_range':[1,32], 'formula_parameter_cases':cases,'explicit_clause_encoding_cases':bit_cases,'assertions':assertions,'failures':0,'max_logB_over_E':round(worst_ratio,9),'worst_case':[str(z) for z in worst_case], 'min_8E_minus_logB':round(min_margin,9), 'python':sys.version.split()[0]}, indent=2))
