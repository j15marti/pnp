#!/usr/bin/env python3
"""LSPV-2 bounded-occurrence two-port profile compiler: deterministic, SciPy HiGHS MILP for independent full-CNF controls.
Run: python3 two_port_guarded220.py > raw220.json
The assertions independently check small finite controls. Full theorem is in report.
"""
from collections import Counter, defaultdict, deque
from itertools import product
import json, random
import numpy as np
import scipy
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix

SEED=20261029
rng=random.Random(SEED)

class Builder:
    def __init__(self):
        self.n=0
        self.C=[]
        self.long_count=0
        self.cycle_edges=0
    def var(self):
        self.n+=1
        return self.n
    def clause(self,*lits):
        assert len(lits)==3 and all(isinstance(l,int) and l!=0 for l in lits)
        assert len({abs(l) for l in lits})==3
        self.C.append(tuple(lits))
    def split_binary(self,a,b):
        assert abs(a)!=abs(b)
        t=self.var()
        self.clause(a,b,t)
        self.clause(a,b,-t)
        self.cycle_edges+=1
    def split_five(self,l):
        assert len(l)==5 and len({abs(v) for v in l})==5
        t=self.var()
        s=self.var()
        self.clause(l[0],l[1],t)
        self.clause(-t,l[2],s)
        self.clause(-s,l[3],l[4])
        self.long_count+=1
    def equality_cycle(self,vs):
        assert len(vs)>=2 and len(set(vs))==len(vs)
        for i in range(len(vs)):
            self.split_binary(-vs[i],vs[(i+1)%len(vs)])

def canonical(H,n):
    assert n>=3 and len(H)>=1
    C=[]
    for c in H:
        if len(c)!=3 or any(not isinstance(l,int) or not 1<=abs(l)<=n for l in c):
            raise ValueError('bad clause format or variable range')
        if len({abs(l) for l in c})!=3:raise ValueError('not proper')
        C.append(tuple(c))
    if set(abs(l) for c in C for l in c)!=set(range(1,n+1)):
        raise ValueError('unused or non-dense source variable')
    return C

def compile_module(H,n):
    H=canonical(H,n)
    b=Builder()
    groups=defaultdict(list)
    aports=[];bports=[]
    for c in H:
        for sign in (+1,-1):
            a=b.var();bb=b.var()
            aports.append(a);bports.append(bb)
            copied=[]
            for lit in c:
                x=b.var()
                groups[abs(lit)].append(x)
                copied.append(x if lit>0 else -x)
            b.split_five((a if sign==+1 else -a,bb if sign==+1 else -bb,*copied))
    # Cycle linking enforces equality for each variable, without high-degree fanout.
    b.equality_cycle(aports)
    b.equality_cycle(bports)
    for x in sorted(groups):b.equality_cycle(groups[x])
    m=len(H)
    assert b.n==24*m and len(b.C)==26*m
    return b.C,b.n,(aports[0],bports[0]),{'input_m':m,'variables':b.n,'clauses':len(b.C),'long_clauses_split':b.long_count,'binary_cycle_constraints':b.cycle_edges,'source_variables':n}

def connected(C,n):
    adj=[[] for _ in range(n+1)]
    for c in C:
        a,b,d=[abs(x) for x in c]
        adj[a].extend([b,d]);adj[b].extend([a,d]);adj[d].extend([a,b])
    seen={1};q=deque([1])
    while q:
        for v in adj[q.popleft()]:
            if v not in seen:seen.add(v);q.append(v)
    return len(seen)==n

def occurrence_metrics(C,n):
    total=Counter(abs(l) for c in C for l in c)
    assert len(total)==n
    return {'max':max(total.values()),'min':min(total.values()),'histogram':dict(sorted(Counter(total.values()).items()))}

def eval_cnf(C,vals):
    return all(any((vals[abs(l)-1] if l>0 else not vals[abs(l)-1]) for l in c) for c in C)

def brute_sat(C,n):
    for vals in product([False,True],repeat=n):
        if eval_cnf(C,vals):return True
    return False

def dpll(C,assumptions=()):
    """Independent exact DPLL with unit propagation. Calls are counted."""
    A={}
    for var,bit in assumptions:
        if var in A and A[var]!=bit:return False,0
        A[var]=bit
    calls=0
    def rec(A):
        nonlocal calls
        calls+=1
        while True:
            changed=False
            reduced=[]
            for clause in C:
                unknown=[]; satisfied=False
                for lit in clause:
                    v=abs(lit)
                    if v in A:
                        if A[v]==(lit>0):satisfied=True;break
                    else:unknown.append(lit)
                if satisfied:continue
                if not unknown:return False
                if len(unknown)==1:
                    z=unknown[0];v=abs(z);truth=z>0
                    if v in A and A[v]!=truth:return False
                    if v not in A:A[v]=truth;changed=True
                reduced.append(unknown)
            if not changed:break
        if not reduced:return True
        rank=Counter(abs(t) for cl in reduced for t in cl)
        v=max(rank, key=lambda z:(rank[z], -z))
        # Positive first is deterministic, and no completeness depends on the priority.
        for truth in (True,False):
            AA=A.copy();AA[v]=truth
            if rec(AA):return True
        return False
    result=rec(A)
    return result,calls

def exact_milp(C,n,assumptions=()):
    """Independent 0-1 integer-programming SAT control (HiGHS through SciPy)."""
    rows=[];cols=[];values=[];lo=[]
    for i,c in enumerate(C):
        for lit in c:
            rows.append(i);cols.append(abs(lit)-1)
            values.append(1.0 if lit>0 else -1.0)
        lo.append(1-sum(v<0 for v in c))
    A=coo_matrix((values,(rows,cols)),shape=(len(C),n)).tocsr()
    LB=np.zeros(n);UB=np.ones(n)
    for v,truth in assumptions:
        LB[v-1]=UB[v-1]=int(truth)
    r=milp(np.zeros(n),integrality=np.ones(n),bounds=Bounds(LB,UB),
           constraints=LinearConstraint(A,np.array(lo),np.inf),
           options={'time_limit':6,'disp':False})
    if r.status not in (0,2):
        raise RuntimeError('MILP did not certify feasibility or infeasibility: '+str(r.status))
    if r.status==0:
        vals=tuple(x>=0.5 for x in r.x)
        assert eval_cnf(C,vals)
        assert all(vals[v-1]==truth for v,truth in assumptions)
    return r.status==0,r.status


def dimacs_bytes(C,n):
    s=f'p cnf {n} {len(C)}\n'
    s+=''.join(' '.join(map(str,clause))+' 0\n' for clause in C)
    return len(s.encode('ascii'))

def independent_clause_split_checks():
    binary=0;five=0
    for q in product((False,True),repeat=2):
        b=Builder();a=b.var();c=b.var();b.split_binary(a,c)
        assert (q[0] or q[1])==any(eval_cnf(b.C,q+tt) for tt in product((False,True),repeat=1))
        binary+=1
    for q in product((False,True),repeat=5):
        b=Builder();vs=[b.var() for _ in range(5)];b.split_five(vs)
        assert any(q)==any(eval_cnf(b.C,q+tt) for tt in product((False,True),repeat=2))
        five+=1
    return binary,five

def sample_H():
    # Source H controls of both labels and varied connectedness.
    unsat=[tuple(1 if b[0] else -1 for _ in [])] if False else []
    unsat=[tuple(v if bit else -v for v,bit in zip((1,2,3),bits)) for bits in product((False,True),repeat=3)]
    sat7=unsat[:-1]
    examples=[('sat_single',[(1,2,3)],3),('sat7',sat7,3),('unsat8',unsat,3),
       ('sat4',[(1,2,-3),(-1,2,4),(1,-3,-4),(2,3,4)],4),
       ('unsat8plus',unsat+[(3,4,5)],5)]
    # Deterministic randomized controls with n<=4 so brute SAT is inexpensive.
    for q in range(7):
        n=3+(q%2);m=2+(q%4)
        H=[]
        for j in range(m):
            vv=rng.sample(range(1,n+1),3)
            H.append(tuple(v if rng.randrange(2) else -v for v in vv))
        # Guarantee each variable used before normalization.
        used={abs(x) for c in H for x in c}
        if used!=set(range(1,n+1)):
            continue
        examples.append((f'random{q}',H,n))
    return examples

def main():
    bin_checks,five_checks=independent_clause_split_checks()
    invalid=0
    for H,n in [([(1,1,2)],3),([(1,2,0)],3),([(1,2)],3),([(1,2,4)],3)]:
        try:compile_module(H,n)
        except ValueError:invalid+=1
        else:raise AssertionError('malformed accepted')
    result=[];total_dpll=0;exact_checks=0;milp_checks=0
    for label,H,n in sample_H():
        source_answer=brute_sat(H,n)
        C,nout,ports,stats=compile_module(H,n)
        assert connected(C,nout)
        occ=occurrence_metrics(C,nout)
        assert occ['max']==5
        # For all 4 port assignments, compare the full 3CNF with the symbolic profile theorem.
        profile={};calls=0
        for a,b in product((False,True),repeat=2):
            sat,status=exact_milp(C,nout,[(ports[0],a),(ports[1],b)])
            milp_checks+=1;exact_checks+=1
            if len(H)==1: # independent DPLL cross-check at the small end
                sat2,cnt=dpll(C,[(ports[0],a),(ports[1],b)])
                assert sat2==sat
                calls+=cnt;total_dpll+=cnt
            assert sat == ((a!=b) or source_answer),(label,a,b,sat,source_answer)
            profile[f'{int(a)}{int(b)}']=sat
        assert (profile['00'] or profile['01']) and (profile['10'] or profile['11'])
        assert (profile['00'] or profile['10']) and (profile['01'] or profile['11'])
        result.append({'case':label,'m':len(H),'source_sat':source_answer,'source_bytes':dimacs_bytes(H,n),
            'module_bytes':dimacs_bytes(C,nout),'module_bits':dimacs_bytes(C,nout)*8,
            'ports':list(ports),'exact_profile':profile,'occurrence':occ,'dpll_calls':calls,**stats})
    # Large structural-only controls; don't confuse this with an all-size DPLL check.
    sizes=[]
    for m in (1,2,8,32,128):
        H=[(1,2,3)]*m
        C,nout,ports,st=compile_module(H,3)
        o=occurrence_metrics(C,nout)
        assert connected(C,nout) and o['max']==5
        sizes.append({'m':m,'vars':nout,'clauses':len(C),'source_bits':8*dimacs_bytes(H,3),
            'output_bits':8*dimacs_bytes(C,nout),'occ_max':o['max']})
    print(json.dumps({'status':'PASS','seed':SEED,'theorem':'exact port projection is XOR if source UNSAT, full 4-pair relation if source SAT',
      'structural':{'vars_per_source_clause':24,'clauses_per_source_clause':26,'max_occurrence':5,'proper':True,'connected':True},
      'finite_controls':{'binary_split_truth_tables':bin_checks,'five_split_truth_tables':five_checks,'malformed_rejections':invalid,
       'profile_MILP_checks':milp_checks,'profile_DPLL_small_checks':4,'total_DPLL_recursive_calls':total_dpll,'cases':result,'scaling':sizes,'scipy_version':scipy.__version__},
      'limitations':['This is not strict signed exact-(2,2)-3CNF.',
        'NP-completeness of exact-profile entry membership is a conditional polynomial-algorithm barrier, not an unconditional time bound.',
        'No polynomial-time exact profile compiler for arbitrary SAT is exhibited.',
        'The finite DPLL controls are not a formal proof of the all-size projection identity.',
        'Proof of general 3SAT hardness uses the standard NP-completeness of proper 3CNF.']},indent=2,sort_keys=True))

if __name__=='__main__':main()
