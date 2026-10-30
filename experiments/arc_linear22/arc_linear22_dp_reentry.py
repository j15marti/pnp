#!/usr/bin/env python3
"""Exact DP elimination + proper3CNF reentry on connected 4-regular linear 3hypergraph.
Restricted constructive proof and exhaustively validated local interface.
"""
from pathlib import Path
import sys,math,collections,itertools,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from arc_linear22_projection_firewall import formula
from arc_mixed_projection_test import source_sat,bitcnf

def dp(clauses,x):
    pos=[];neg=[];common=[]
    for clause in clauses:
        if x in clause:pos.append(tuple(a for a in clause if a!=x))
        elif -x in clause:neg.append(tuple(a for a in clause if a!=-x))
        else:common.append(clause)
    assert len(pos)==2 and len(neg)==2
    all_res=[]
    for a in pos:
        for b in neg:
            z=tuple(sorted(set(a+b),key=lambda v:(abs(v),v)))
            if any(-v in z for v in z):continue
            all_res.append(z)
    assert len(all_res)==4 and len(set(all_res))==4
    assert all(len(c)==4 for c in all_res)
    return common,all_res

def convert_resolvents(common,resolvents,n,x):
    # Syntax must name exactly n+3 active variables; original pivot is removed.
    remaining=[i for i in range(1,n+1) if i!=x]
    to={old:i+1 for i,old in enumerate(remaining)}
    clauses=[]
    for c in common:
        clauses.append(tuple((1 if v>0 else -1)*to[abs(v)] for v in c))
    for j,c in enumerate(resolvents):
        a=[(1 if v>0 else -1)*to[abs(v)] for v in c]
        y=n+j # n-1 old vars => first new label n
        clauses.extend([(a[0],a[1],y),(-y,a[2],a[3])])
    return clauses,to

def local_equiv_for_pivot(clauses,x):
    common,rs=dp(clauses,x)
    neighbors=sorted(set(abs(z) for c in clauses if x in c or -x in c for z in c if abs(z)!=x))
    assert len(neighbors)==8
    affected=[c for c in clauses if x in c or -x in c]
    checks=0
    for vals in itertools.product((0,1),repeat=len(neighbors)):
        assign=dict(zip(neighbors,vals))
        old=any(all(any((assign.get(abs(z),b) if abs(z)!=x else b)==int(z>0) for z in c) for c in affected)
                for b in (0,1))
        new=all(any(assign[abs(z)]==int(z>0) for z in c) for c in rs)
        if old!=new:raise AssertionError((x,vals,old,new))
        checks+=1
    return checks

def gamma_bits(z):
    assert z>=1
    return 2*(z.bit_length()-1)+1

def cnf_gamma_bits(clauses,n):
    w=max(1,n.bit_length())  # ceil(log2(n+1))
    return gamma_bits(n+1)+gamma_bits(len(clauses)+1)+sum(gamma_bits(4)+3*(1+w) for _ in clauses)

def audit(k):
    n,clauses=formula(k)
    N=bitcnf(clauses,n)
    Ngamma=cnf_gamma_bits(clauses,n)
    counts=[]
    gamma=[]
    for x in range(1,n+1):
        common,rs=dp(clauses,x)
        to=convert_resolvents(common,rs,n,x)[0]
        assert len(to)==len(clauses)+4
        assert all(len(set(abs(z) for z in c))==3 for c in to)
        assert len(set(to))==len(to)
        assert max(abs(z) for c in to for z in c)==n+3
        length=bitcnf(to,n+3)
        targetgamma=cnf_gamma_bits(to,n+3)
        assert length>N and targetgamma>Ngamma
        gamma.append(targetgamma)
        count=local_equiv_for_pivot(clauses,x)
        counts.append((len(to),length,count))
    assert len(set(counts))==1
    return dict(k=k,old_n=n,old_m=len(clauses),old_bits=N,
       child_n=n+3,child_m=len(clauses)+4,child_bits=counts[0][1],
       delta_bits=counts[0][1]-N,source_gamma_bits=Ngamma,child_gamma_bits=gamma[0],delta_gamma_bits=gamma[0]-Ngamma,verified_local_assignments=sum(z[2] for z in counts),
       unsat_preserving=True,source_witness='A_i=1,B_i=C_i=0')

if __name__=='__main__':
    out=[audit(k) for k in (7,9,11,15,21,31)]
    print(json.dumps(out,indent=2))
    with open(str(Path(__file__).resolve().parent / 'arc_linear22_dp_reentry_results.json'),'w') as f:json.dump(out,f,indent=2)
