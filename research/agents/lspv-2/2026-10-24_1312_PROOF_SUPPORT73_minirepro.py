#!/usr/bin/env python3
"""Standalone source-labelled proof-support demo, no external packages.
The full 127-node XOR and strict exact-(2,2) audits are in the linked archive.
This models one proof-analysis policy, not all SAT algorithms.
"""
import json
from collections import Counter

def make(k):
    x,a,b=1,2,3
    d=[]
    for i in range(k):
        y,q=4+2*i,5+2*i
        d.extend([(y,a,q),(-y,a,q)])
    core=[(x,sa*a,sb*b) for sa in (1,-1) for sb in (1,-1)]
    return d+core,{1:False,**{4+2*i:False for i in range(k)}}

def proof(F,assumptions):
    def rec(A):
        A=dict(A)
        while True:
            progress=False
            for i,c in enumerate(F):
                remaining=[];true=False
                for l in c:
                    v=abs(l)
                    if v in A:
                        if A[v]==(l>0):true=True;break
                    else:remaining.append(l)
                if true:continue
                if not remaining:return {'conflict':i}
                if len(remaining)==1:
                    l=remaining[0];A[abs(l)]=l>0;progress=True
            if not progress:break
        if all(any(v in A and A[v]==(l>0) for l in c for v in [abs(l)]) for c in F):
            return None
        v=min(abs(l) for c in F for l in c if abs(l) not in A)
        left=rec({**A,v:False});right=rec({**A,v:True})
        if left is None or right is None:return None
        return {'var':v,'order':0,'first':left,'second':right}
    return rec(assumptions)

def verify(F,P,A,stats=None):
    """Fresh source-clause checker, with all failed-check work countable."""
    if stats is None:stats=Counter()
    def rec(P,A):
        A=dict(A)
        while True:
            changed=False
            for c in F:
                stats['clause_reads']+=1
                remaining=[];sat=False
                for lit in c:
                    v=abs(lit)
                    if v in A:
                        if A[v]==(lit>0):sat=True;break
                    else:remaining.append(lit)
                if sat:continue
                if not remaining:break
                if len(remaining)==1:
                    lit=remaining[0];A[abs(lit)]=lit>0;changed=True
            if not changed:break
        if 'conflict' in P:
            C=F[P['conflict']]
            assert all(abs(l) in A and A[abs(l)]!=(l>0) for l in C)
            return
        v=P['var'];assert v not in A
        rec(P['first'],{**A,v:bool(P['order'])})
        rec(P['second'],{**A,v:not bool(P['order'])})
    rec(P,A)
    return stats['clause_reads']

def support(F,P,alpha):
    """Source assumptions have 'a' tokens; split choices have 'b' tokens."""
    serial=[0];stats=Counter()
    A={v:(b,{('a',v)}) for v,b in alpha.items()}
    def rec(P,A):
        serial[0]+=1;this=serial[0];A=dict(A)
        while True:
            changed=False
            for C in F:
                stats['clause_reads']+=1
                remaining=[];sat=False;deps=set()
                for l in C:
                    v=abs(l)
                    if v in A:
                        val,S=A[v]
                        if val==(l>0):sat=True;break
                        deps.update(S)
                    else:remaining.append(l)
                if sat:continue
                if not remaining:break
                if len(remaining)==1:
                    l=remaining[0];A[abs(l)]=(l>0,deps.copy());changed=True
            if not changed:break
        if 'conflict' in P:
            C=F[P['conflict']]
            assert all(abs(l) in A and A[abs(l)][0]!=(l>0) for l in C)
            return set().union(*(A[abs(l)][1] for l in C))
        v=P['var'];assert v not in A
        token=('b',this)
        a=rec(P['first'],{**A,v:(bool(P['order']),{token})})
        b=rec(P['second'],{**A,v:(not bool(P['order']),{token})})
        return (a|b)-{token}
    deps=rec(P,A)
    assert all(tag=='a' for tag,var in deps)
    return {v:alpha[v] for tag,v in deps},stats['clause_reads']

def run(k):
    F,A=make(k)
    assert all(len(C)==3 and len({abs(l) for l in C})==3 for C in F)
    P=proof(F,A);assert P is not None
    old=0;core=dict(A)
    for v in sorted(A):
        trial=core.copy();trial.pop(v)
        effort=Counter();accepted=True
        try:verify(F,P,trial,effort)
        except (AssertionError,KeyError):accepted=False
        old+=effort['clause_reads']
        if accepted:core=trial
    extracted,cost=support(F,P,A)
    final=verify(F,P,extracted)
    assert core==extracted=={1:False}
    return {'dummy_count':k,'input_assumptions':len(A),'retained':1,
            'replays_greedy_total_scans':old,
            'support_and_independent_check_scans':cost+final}

if __name__=='__main__':
    print(json.dumps({'id':'PROOF-SUPPORT73',
        'scope':'standalone source-labelled proof support',
        'controls':[run(k) for k in (4,16,64)]},indent=2))
