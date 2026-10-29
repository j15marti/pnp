#!/usr/bin/env python3
"""LSPV-4 RANK-INTERFACE-GRID229: independent finite controls.

Exact mathematical result is in accompanying report. This file tests syntax,
grid-subdivision paths, running-intersection path bags, and numerical bounds.
Standard-library only, deterministic. No SAT solver or hardness assertion.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path


def formula(q: int):
    assert q >= 2
    Q = q*q
    def name(k, r, c):
        return k*Q + (r%q)*q + (c%q)+1
    cls=[]
    for r in range(q):
        for c in range(q):
            a=name(0,r,c); b=name(1,r,c); c0=name(2,r,c)
            b1=name(1,r+1,c); c1=name(2,r,c+1)
            cls.extend([(a,b,c0), (a,b1,c0), (-a,-b,-c1),(-a,-b1,-c1)])
    return cls, name


def graph(clauses):
    adj=defaultdict(set)
    for cl in clauses:
        for x in cl:
            adj[abs(x)]
        for a,b in itertools.combinations([abs(x) for x in cl],2):
            adj[a].add(b); adj[b].add(a)
    return adj


def certify_instance(q:int):
    clauses,name=formula(q)
    n=3*q*q; m=4*q*q
    assert len(clauses)==m
    occurrences=Counter()
    for cl in clauses:
        assert len(cl)==3 and len({abs(x) for x in cl})==3
        for lit in cl:occurrences[(abs(lit),lit>0)]+=1
    assert len({abs(x) for cl in clauses for x in cl})==n
    for x in range(1,n+1):
        assert occurrences[(x,True)]==2 and occurrences[(x,False)]==2
    # A=1, B=C=0 is the same explicit easy control as prior GRID209.
    valuation={x:(x<=q*q) for x in range(1,n+1)}
    assert all(any(valuation[abs(l)] if l>0 else not valuation[abs(l)] for l in cl) for cl in clauses)
    adj=graph(clauses)
    seen={1};todo=[1]
    for v in todo:
        for w in adj[v]:
            if w not in seen:seen.add(w);todo.append(w)
    assert len(seen)==n
    # Extract the nonwrapping subdivided q x q grid on A vertices.
    horizontal=[]; vertical=[]
    for r in range(q):
        for c in range(q):
            a=name(0,r,c)
            if r+1<q:
                v=name(1,r+1,c); end=name(0,r+1,c)
                assert v in adj[a] and end in adj[v]
                horizontal.append((a,v,end))
            if c+1<q:
                v=name(2,r,c+1); end=name(0,r,c+1)
                assert v in adj[a] and end in adj[v]
                vertical.append((a,v,end))
    internal=[x[1] for x in horizontal+vertical]
    assert len(internal)==len(set(internal))==2*q*(q-1)
    # Cross-bramble: a hitting set of <q A-grid positions misses a row+column.
    bramble_checks=0
    if q<=4:
        positions=list(range(q*q))
        for size in range(q):
            for subset in itertools.combinations(positions,size):
                occupied=set(subset)
                row=next(r for r in range(q) if not any((r*q+c) in occupied for c in range(q)))
                col=next(c for c in range(q) if not any((r*q+c) in occupied for r in range(q)))
                assert all((row*q+c) not in occupied for c in range(q))
                assert all((r*q+col) not in occupied for r in range(q))
                bramble_checks+=1
    # Normalized ASCII DIMACS is an explicit physical encoding.
    dimacs=f'p cnf {n} {m}\n'+''.join(' '.join(map(str,cl))+' 0\n' for cl in clauses)
    return clauses,{'q':q,'n':n,'m':m,'encoded_bytes':len(dimacs.encode()),
                    'subdivided_edges':len(horizontal)+len(vertical),
                    'bramble_subsets_tested':bramble_checks,
                    'sha256_dimacs':hashlib.sha256(dimacs.encode()).hexdigest()}


def path_decomposition(clauses,chunk:int,q:int):
    # Clause-owned path: each node receives <=chunk consecutive clauses.
    groups=[clauses[i:i+chunk] for i in range(0,len(clauses),chunk)]
    first={};last={}
    for i,grp in enumerate(groups):
        for cl in grp:
            for lit in cl:
                v=abs(lit);first[v]=min(i,first.get(v,i));last[v]=max(i,last.get(v,i))
    # Bags contain all original names active in this interval; each variable's
    # bags form a contiguous path and every local clause lies in its owner bag.
    bags=[]
    for i,grp in enumerate(groups):
        local={abs(lit) for cl in grp for lit in cl}
        bag={v for v in first if first[v]<=i<=last[v]}
        assert local<=bag
        bags.append(bag)
    for v in first:
        hits=[i for i,b in enumerate(bags) if v in b]
        assert hits==list(range(min(hits),max(hits)+1))
    # b_t counts all original source names appearing in >=2 module bags,
    # not only the parent-facing separator.
    count=Counter(v for b in bags for v in b)
    interfaces=[{v for v in b if count[v]>1} for b in bags]
    local_ranks=[len(g) for g in groups] # each owned selector XOR row has fresh disjoint s_{j,*}
    assert all(len(b)<=3*e+len(shared) for b,e,shared in zip(bags,local_ranks,interfaces))
    assert max(len(b) for b in bags)>=q # mathematically guaranteed by the grid bramble
    assert max(3*e+len(shared) for e,shared in zip(local_ranks,interfaces))>=q
    return {'modules':len(groups),'max_clauses_per_module':max(local_ranks),
            'max_interface_original_names':max(map(len,interfaces)),
            'max_bag_original_names':max(map(len,bags)),
            'max_3e_plus_b':max(3*e+len(s) for e,s in zip(local_ranks,interfaces)),
            'sum_full_interface_table_rows':sum(1<<len(s) for s in interfaces),
            'min_required_global_lower_bound_q':q}


def renaming_controls(clauses,q,seed):
    n=3*q*q;rng=random.Random(seed)
    perm=list(range(1,n+1));rng.shuffle(perm)
    signs=[rng.choice([-1,1]) for _ in range(n)]
    renamed=[]
    for cl in clauses:
        renamed.append(tuple((1 if x>0 else -1)*signs[abs(x)-1]*perm[abs(x)-1] for x in cl))
    occ=Counter()
    for cl in renamed:
        assert len({abs(x) for x in cl})==3
        for l in cl:occ[(abs(l),l>0)]+=1
    assert all(occ[(v,True)]==2 and occ[(v,False)]==2 for v in range(1,n+1))
    return hashlib.sha256(str(renamed).encode()).hexdigest()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',default=None)
    args=parser.parse_args()
    results=[];checks=0
    for q in [2,3,4,5,6,8,12,16,24,32]:
        cls,data=certify_instance(q)
        audits=[]
        for chunk in [1,2,4,8,16,4*q]:
            audit=path_decomposition(cls,chunk,q)
            audits.append({'group_size':chunk,**audit});checks+=3*len(cls)
        data['decompositions']=audits
        data['renamed_control_sha256']=renaming_controls(cls,q,1000+q)
        assert audits[0]['max_clauses_per_module']==1
        assert audits[0]['max_interface_original_names']>=q-3
        results.append(data)
    out={'run_id':'LSPV4_RANK_INTERFACE_TRADEOFF229',
         'status':'COMPUTATIONAL tests; symbolic theorem in report',
         'cases':results,'tested_path_groups':60,'assertion_proxy':checks,
         'qualifications':['Already known GRID209 grid-width lemma reused.',
          'New rank-interface tradeoff only for clause-atomic selector-gadget module trees.',
          'Full-interface table enumeration lower bound is architectural, not unrestricted SAT time.',
          'All source instances carry explicit A=1,B=C=0 witness.']}
    out_path=Path(args.out or Path(__file__).with_name('raw_grid_rank.json'))
    out_path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'run_id':out['run_id'],'cases':len(results),
                      'modules_tested':60,'assertion_proxy':checks,
                      'q32':results[-1]['decompositions'][0],
                      'raw_sha256':hashlib.sha256(out_path.read_bytes()).hexdigest()},indent=2))
if __name__=='__main__': main()
