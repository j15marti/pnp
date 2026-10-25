#!/usr/bin/env python3
"""ARC-PIN-BUDGET171: two true Shannon levels, restriction-only full cubes.
Deterministic ordinary-CNF SAT/UNSAT and encoding controls; no FLMV timing claim.
"""
import json
import math
from pathlib import Path

SEED_ID = 202610250700

def source(q, sat):
    # q disjoint proper positive ternary clauses; separate guard literal.
    n=3*q+1
    clauses=[tuple((3*j+1,3*j+2,3*j+3)) for j in range(q)]
    clauses.append((n,))
    if not sat:
        clauses.append((-n,))
    return n,tuple(clauses)

def restrict(cs,v,b):
    yes = v if b else -v
    no = -yes
    return tuple(tuple(x for x in c if x!=no) for c in cs if yes not in c)

def encode(n,cs):
    return ('p cnf %d %d\n'%(n,len(cs)) + ''.join(' '.join(map(str,c))+' 0\n' for c in cs)).encode('ascii')

def parse(bb):
    lines=bb.decode('ascii').splitlines()
    assert lines and lines[0].startswith('p cnf ')
    h=lines[0].split();assert len(h)==4 and h[:2]==['p','cnf']
    n,m=int(h[2]),int(h[3]); assert n>=1 and m>=0
    assert len(lines)==m+1
    out=[]
    for line in lines[1:]:
        ff=list(map(int,line.split()))
        assert ff and ff[-1]==0 and 0 not in ff[:-1]
        assert all(1<=abs(x)<=n for x in ff[:-1])
        out.append(tuple(ff[:-1]))
    return n,tuple(out)

def dpll(cs):
    # Fixed deterministic total DPLL with unit, pure-literal and split rules.
    cs=tuple(cs)
    while True:
        if not cs:return True
        if any(not c for c in cs):return False
        units=[c[0] for c in cs if len(c)==1]
        if units:
            lit=units[0];cs=restrict(cs,abs(lit),lit>0);continue
        all_lits={x for c in cs for x in c}
        pures=[x for x in all_lits if -x not in all_lits]
        if pures:
            lit=min(pures,key=lambda x:(abs(x),x<0))
            cs=restrict(cs,abs(lit),lit>0);continue
        break
    lit=cs[0][0];return dpll(restrict(cs,abs(lit),lit>0)) or dpll(restrict(cs,abs(lit),lit<0))

def run():
    reports=[];checks=0;total_source_bytes=0;total_child_bytes=0
    for q in [8,16,32,64,128,256]:
        k=int(math.log2(q));k1=k//2;k2=k-k1
        # Different clauses per level: one variable from each disjoint triple.
        level1=[3*i+1 for i in range(k1)]
        level2=[3*i+1 for i in range(k1,k1+k2)]
        for sat in [True,False]:
            n,root=source(q,sat);base=encode(n,root)
            assert parse(base)==(n,root);checks+=1
            expected=dpll(root);assert expected==sat;checks+=1
            parent_results=[];leaf_ratios=[];leaf_bytes=[];leaf_count=0
            first_bytes=[]
            for mask1 in range(1<<k1):
                c1=root
                for i,v in enumerate(level1): c1=restrict(c1,v,bool(mask1&(1<<i)))
                b1=encode(n,c1); assert parse(b1)==(n,c1);checks+=1
                first_bytes.append(len(b1));total_child_bytes+=len(b1)
                truth1=dpll(c1);results2=[]
                for mask2 in range(1<<k2):
                    c2=c1
                    for i,v in enumerate(level2):c2=restrict(c2,v,bool(mask2&(1<<i)))
                    b2=encode(n,c2);assert parse(b2)==(n,c2);checks+=1
                    total_child_bytes+=len(b2);leaf_count+=1
                    truth2=dpll(c2);results2.append(truth2)
                    leaf_bytes.append(len(b2));leaf_ratios.append(len(b2)/len(base))
                    unaffected=sum(1 for j in range(q) if (3*j+1,3*j+2,3*j+3) in c2)
                    assert unaffected>=q-k;checks+=1
                assert truth1==any(results2);checks+=1
                parent_results.append(truth1)
            assert expected==any(parent_results);checks+=1
            assert leaf_count==2**k;checks+=1
            total_source_bytes+=len(base)
            reports.append(dict(q=q,label='SAT' if sat else 'UNSAT',root_bytes=len(base),first_level_count=2**k1,second_level_total=leaf_count,k=k,k1=k1,k2=k2,first_level_min_bytes=min(first_bytes),first_level_max_bytes=max(first_bytes),leaf_min_bytes=min(leaf_bytes),leaf_max_bytes=max(leaf_bytes),leaf_min_ratio=round(min(leaf_ratios),6),leaf_max_ratio=round(max(leaf_ratios),6),leaf_min_exp=round(math.log(min(leaf_bytes))/math.log(len(base)),6),unaffected_floor=q-k))
    # Hostile controls: independent SAT children do not imply conjunction SAT.
    assert dpll(((1,),)) and dpll(((-1,),)) and not dpll(((1,),(-1,)));checks+=1
    # Invalid variable name, missing clause, malformed suffix all rejected.
    for bad in (b'p cnf 1 1\n2 0\n',b'p cnf 1 2\n1 0\n',b'p cnf 1 1\n1 0 0\n'):
        rejected=False
        try:parse(bad)
        except AssertionError:rejected=True
        assert rejected;checks+=1
    output={"run":"ARC-PIN-BUDGET171","seed_id":SEED_ID,"model":"standard DIMACS ordinary-CNF representation, two genuine eager full Shannon levels","method":"deterministic exhaustive complete cubes, independent DPLL SAT labels","all_checks":checks,"failures":0,"root_cases":len(reports),"sat_cases":sum(r['label']=='SAT' for r in reports),"unsat_cases":sum(r['label']=='UNSAT' for r in reports),"grandchild_calls":sum(r['second_level_total'] for r in reports),"first_child_calls":sum(r['first_level_count'] for r in reports),"source_bytes":total_source_bytes,"serialized_child_bytes":total_child_bytes,"rows":reports,"limitations":"Python bytes and DPLL nodes are not FLMV bit-time, hardware flips, or same-machine peak indexed/workspace"}
    return output

if __name__=='__main__':
    out=run()
    dest=Path(__file__).with_name('arc_pin_budget171_results.json')
    dest.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
    for r in out['rows']:
        print(r['q'],r['label'],r['root_bytes'],r['leaf_min_bytes'],r['leaf_min_ratio'],r['leaf_min_exp'])
