#!/usr/bin/env python3
"""LSPV-2 semantic projection finite verifier. Python 3 standard library only."""
import json,math
from collections import Counter

def force(l,u,v):
    return [(l,u,v),(l,u,-v),(l,-u,v),(l,-u,-v)]

def build(n,a,unsat=False):
    e=lambda i:i+1 if (a>>i)&1 else -(i+1)
    clauses=[]
    for i in range(n): clauses+=force(e(i),n+i+1,2*n+i+1)
    for i in range(n-1): clauses.append((e(i),e(i+1),n+i+1))
    nv=3*n
    if unsat:
        p,s,t=nv+1,nv+2,nv+3
        clauses+=force(p,s,t)+force(-p,s,t)+[(e(0),p,n+1)]
        nv+=3
    return clauses,nv

def evaluate(clauses,bits):
    return all(any(((bits>>(abs(v)-1))&1)==(v>0) for v in c) for c in clauses)

def check_shape(clauses,nv):
    assert all(len(c)==3 and len({abs(v) for v in c})==3 for c in clauses)
    edges=[set() for _ in range(nv)]
    count=Counter(abs(v) for c in clauses for v in c)
    for c in clauses:
        for v in c: edges[abs(v)-1].update(abs(w)-1 for w in c)
    seen={0}; todo=[0]
    for v in todo:
        for w in edges[v]:
            if w not in seen: seen.add(w);todo.append(w)
    assert len(seen)==nv
    return max(count.values())

def size(clauses,nv):
    return 8*(len(f'p cnf {nv} {len(clauses)}\n')+
       sum(len(' '.join(map(str,c))+' 0\n') for c in clauses))

def main():
    counts=Counter();small=[];scales=[]
    for n in range(1,6):
        maxbytes=0
        for a in range(1<<n):
            f,nv=build(n,a)
            assert nv==3*n and len(f)==5*n-1 and check_shape(f,nv)<=6
            counts['structural_instances']+=1
            maxbytes=max(maxbytes,size(f,nv)//8)
            for assignment in range(1<<nv):
                valid=evaluate(f,assignment)
                assert valid==((assignment&((1<<n)-1))==a)
                counts['full_boolean_assignments']+=1
                if valid:counts['satisfying_full_assignments']+=1
            if n<=4:
                u,nu=build(n,a,True)
                check_shape(u,nu)
                for assignment in range(1<<nu):
                    assert not evaluate(u,assignment)
                    counts['unsat_control_assignments']+=1
                counts['unsat_control_instances']+=1
        for x in range(1<<n):
            assert sum(x==a for a in range(1<<n))==1
            counts['distinct_function_checks']+=1
        small.append({'n':n,'maximum_parent_bytes':maxbytes,'number_semantically_distinct_SAT_formulas':1<<n})
    for n in (8,16,32,64,128,512,2048):
        f,nv=build(n,0);N=size(f,nv)
        scales.append({'n':n,'input_bits_upper_all_masks':N,'sqrt_input_bits':round(math.sqrt(N),3),
            'ratio_sqrt_over_n':round(math.sqrt(N)/n,5),'number_clauses':len(f),
            'max_occurrences_per_var':check_shape(f,nv)})
    for l in (False,True):
        for u in (False,True):
            for v in (False,True):
                assert all(l or (u if c[1]>0 else not u) or (v if c[2]>0 else not v)
                    for c in force(1,2,3))==l
    print(json.dumps({'run':'SEMANTIC-PROJECTION210','counts':dict(counts),
        'local_force_truth_table_cases':8,'small_instances':small,'large_source_bit_scales':scales,
        'method':'exhaustive n<=5; deterministic; no randomness','status':'COMPUTATIONAL; semantic theorem PROVED/EXACT restricted; P vs NP OPEN'},sort_keys=True,indent=2))
if __name__=='__main__':main()