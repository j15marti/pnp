#!/usr/bin/env python3
"""LSPV-1/402 exact finite support controls, Python 3 stdlib only.
Usage: python3 lspv1_402_monotone_port_producer.py > raw.json
"""
import json
from itertools import product, combinations

checks=0
def check(v,msg):
    global checks
    assert v, msg
    checks += 1

def valid(F,n):
    if not isinstance(n,int) or n<1 or not isinstance(F,list): return False
    for C in F:
        if not isinstance(C,(list,tuple)) or not C or len(C)>3: return False
        if any(type(l)!=int or not l or abs(l)>n for l in C): return False
        if len({abs(l) for l in C})!=len(C): return False
    return True

def sat_count(F,n):
    return sum(all(any((bits[abs(l)-1] if l>0 else not bits[abs(l)-1]) for l in C) for C in F) for bits in product((0,1),repeat=n))

def build(F,n):
    assert valid(F,n)
    names=[f'a{i}' for i in range(1,n+1)]+[f'b{i}' for i in range(1,n+1)]+['t']
    gates=[]
    def gate(op,u,v):
        ix=len(names)+len(gates); gates.append((op,u,v));return ix
    def fold(op,arr):
        assert arr
        z=arr[0]
        for a in arr[1:]:z=gate(op,z,a)
        return z
    g=fold('AND',[gate('OR',i,n+i) for i in range(n)])
    bad=[gate('AND',i,n+i) for i in range(n)]
    for C in F:
        wrong=[n+abs(l)-1 if l>0 else abs(l)-1 for l in C]
        bad.append(fold('AND',wrong))
    h=fold('OR',bad)
    root=gate('OR',h,gate('AND',2*n,g))
    return names,gates,root

def evaluate(names,gates,root,bits):
    vals=list(bits)
    for op,u,v in gates:
        vals.append((vals[u] and vals[v]) if op=='AND' else (vals[u] or vals[v]))
    return int(vals[root])

def relevance(F,n):
    names,gates,root=build(F,n)
    has=False; witness=None; evals=0
    for flags in product((0,1),repeat=2*n):
        p=evaluate(names,gates,root,flags+(0,));q=evaluate(names,gates,root,flags+(1,));evals+=2
        check(p<=q,'monotone t')
        if q>p:has=True;witness=''.join(map(str,flags));break
    return has,witness,evals,len(gates)

# Full set of n=2 non-tautological proper clauses, all 2^8 CNFs.
clauses=[]
for s in product((-1,0,1),repeat=2):
    C=[s[i]*(i+1) for i in range(2) if s[i]]
    if C:clauses.append(C)
check(len(clauses)==8,'eight clauses')
rows=[];sat_total=unsat_total=0;total_evals=0
for mask in range(256):
    F=[clauses[i] for i in range(8) if (mask>>i)&1]
    cnt=sat_count(F,2)
    rel,wit,n_eval,ng=relevance(F,2)
    check(rel==(cnt>0),'SAT iff essential')
    if wit is not None:
        v=[int(x) for x in wit]
        check(all(v[i]+v[2+i]==1 for i in range(2)),'exact assignment')
        check(all(any((v[abs(l)-1] if l>0 else v[2+abs(l)-1]) for l in C) for C in F),'witness clauses')
    check(ng>=1,'nonempty gates')
    rows.append({'mask':mask,'models':cnt,'essential':rel,'witness':wit,'gates':ng})
    total_evals+=n_eval
    sat_total+=(cnt>0);unsat_total+=(cnt==0)
check((sat_total,unsat_total)==(95,161),'2-var count')

# Odd/even K4 charge-parity Tseitin 3CNF on six edges.
edges=list(combinations(range(4),2))
def tseitin(charges):
    F=[]
    for v in range(4):
        inc=[i+1 for i,e in enumerate(edges) if v in e]
        for bits in product((0,1),repeat=3):
            if (sum(bits)%2)!=charges[v]:
                F.append([(-ix if bit else ix) for ix,bit in zip(inc,bits)])
    return F
parity=[]
for charges in [(0,0,0,0),(1,0,0,0)]:
    F=tseitin(charges);cnt=sat_count(F,6);rel,wit,ne,ng=relevance(F,6)
    check(len(F)==16 and rel==(cnt>0),'K4 truth')
    parity.append({'charge':''.join(map(str,charges)),'models':cnt,'essential':rel,'gates':ng})
check((parity[0]['models'],parity[1]['models'])==(8,0),'K4 8/0')

malformed=[([[]],2), ([[0]],2), ([[3]],2), ([[1,-1]],2), ([[1,2,1]],2), ([[True]],2), ([[1]],0), ('x',2), ([[1,2,3,4]],4)]
for F,n in malformed:check(not valid(F,n),'reject malformed')
for F,n in [([[1]],1),([[-1]],1),([[1],[-1]],1),([],2)]:
    check(valid(F,n),'good source')
    rel,wit,ne,ng=relevance(F,n)
    check(rel==(sat_count(F,n)>0),'control label')

out={'id':'LSPV1-402-MONOTONE-RECONVERGENT-ESSENTIALITY','encoding':'signed explicit original clauses; monotone AND/OR fanin2 DAG; distinguished t','clauses':clauses,'rows':rows,'sat_count':sat_total,'unsat_count':unsat_total,'parity':parity,'malformed_rejections':len(malformed),'assertions':checks,'total_pair_evaluations':total_evals,'scope':'finite test only; asymptotic NP-completeness is separately proved by SAT reduction'}
print(json.dumps(out,separators=(',',':'),sort_keys=True))
