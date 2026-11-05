#!/usr/bin/env python3
"""Source-independent DEF/Resolution alias experiment for signed-CNF port equality.
Only tests the explicitly hypothesized readable-CNF-DEF convention, not a completed native grammar.
"""
from __future__ import annotations
import json, itertools
from collections import defaultdict
from pathlib import Path

assertions = 0

def check(test, message=''):
    global assertions
    assertions += 1
    if not test: raise AssertionError(message)

class Circuit:
    def __init__(self,n): self.n=n; self.next=n+1; self.gates=[]
    def gate(self,op,a,b):
        if not (isinstance(a,int) and isinstance(b,int) and 1<=abs(a)<self.next and 1<=abs(b)<self.next): raise ValueError('invalid wire')
        z=self.next; self.next+=1; self.gates.append((z,op,a,b)); return z
    def value(self,lit,vals): return (not vals[abs(lit)]) if lit<0 else vals[lit]
    def eval(self,assignment):
        vals={i+1:bool(b) for i,b in enumerate(assignment)}
        for z,op,a,b in self.gates:
            u,v=self.value(a,vals),self.value(b,vals)
            vals[z]={'AND':u and v,'OR':u or v,'XOR':u!=v,'NAND':not(u and v),'XNOR':u==v}[op]
        return vals
    def defs(self):
        # Exact 4-row forbidden-pattern CNF. Each line attributed to a paid gate.
        out=[]
        for z,op,a,b in self.gates:
            for ua,ub in itertools.product((False,True),repeat=2):
                uz={'AND':ua and ub,'OR':ua or ub,'XOR':ua!=ub,'NAND':not(ua and ub),'XNOR':ua==ub}[op]
                for wz in (not uz,):
                    # formula disjunction to exclude inconsistent (a=ua,b=ub,z=wz)
                    lits=[]
                    for wire,value in ((a,ua),(b,ub),(z,wz)):
                        original_positive_value=value if wire>0 else not value
                        lits.append(-abs(wire) if original_positive_value else abs(wire))
                    clause=frozenset(lits)
                    if any(-x in clause for x in clause): continue
                    out.append((clause,z))
        return out

def normalize_clause(c):
    cc=frozenset(c)
    if any(-x in cc for x in cc): return None
    return cc

def resolve(a,b,pivot):
    if pivot in a and -pivot in b:
        return normalize_clause((a-{pivot}) | (b-{-pivot}))
    if -pivot in a and pivot in b:
        return normalize_clause((a-{-pivot}) | (b-{pivot}))
    return None

def saturate(clauses, targets, cap=20000):
    """Davis-Putnam variable elimination retaining target ports, valid RES trace."""
    known=[];parent=[];index={}
    for c,z in clauses:
        if c not in index:
            index[c]=len(known); known.append(c);parent.append(('DEF',z))
    active=set(range(len(known)))
    keep={abs(k) for c in targets for k in c}
    vars_all={abs(x) for c in known for x in c}
    for v in sorted(vars_all-keep,reverse=True):
        plus=[i for i in active if v in known[i]]
        minus=[i for i in active if -v in known[i]]
        nxt=active-set(plus)-set(minus)
        for i in plus:
            for j in minus:
                r=resolve(known[i],known[j],v)
                if r is None:continue
                if r not in index:
                    index[r]=len(known);known.append(r);parent.append(('RES',i,j,v))
                    if len(known)>cap:raise RuntimeError(f'closure cap {cap} exceeded')
                nxt.add(index[r])
        active=nxt
    # needed clauses can be subsumed by shorter derived clauses (rare on nonconstant outputs)
    return known,parent,index

def verify(known,parent,initial_defs):
    allowed={c for c,_ in initial_defs}
    for i,(cl,step) in enumerate(zip(known,parent)):
        if step[0]=='DEF':
            check(cl in allowed,'unjustified gate antecedent')
        else:
            _,j,k,p=step
            check(j<i and k<i,'forward parent')
            check(resolve(known[j],known[k],p)==cl,'invalid resolution')
    return True

def proof_case(case,build,out_a,out_b):
    C=Circuit(case['n']); p,q=build(C); a,b=out_a(C,p,q),out_b(C,p,q)
    check(len({z for z,_,_,_ in C.gates})==len(C.gates),'not fresh')
    defs=C.defs(); goals={frozenset((-a,b)),frozenset((a,-b))}
    mismatches=0
    for bits in itertools.product((False,True),repeat=C.n):
        v=C.eval(bits);eq=(C.value(a,v)==C.value(b,v))
        if not eq:mismatches+=1
        if case['expected_equal']:check(eq,f'semantics {case["name"]} {bits}')
        for c,z in defs:
            check(any((lit>0)==v[abs(lit)] for lit in c),'bad gate definition')
    check((mismatches==0)==case['expected_equal'],'bad control')
    known,parents,idx=saturate(defs,goals)
    verify(known,parents,defs)
    if case['expected_equal']:
        check(goals.issubset(idx),'missing equality certificate')
    else:
        check(not goals.issubset(idx),'false alias accepted')
    # The checker must reject corrupt pivots
    at=next((i for i,p in enumerate(parents) if p[0]=='RES'),None)
    if at is not None:
        wrong=parents.copy();j,k,p=wrong[at][1:];wrong[at]=('RES',j,k,100000)
        try:verify(known[:at+1],wrong[:at+1],defs)
        except AssertionError:pass
        else:raise AssertionError('corrupted proof accepted')
    return dict(name=case['name'],n_inputs=C.n,paid_def_gates=len(C.gates),def_clauses=len(defs),res_nodes=len(known)-len({x for x,_ in defs}),goal_indices=sorted(idx[g] for g in goals) if goals.issubset(idx) else None,closure_clauses=len(known),expected_equal=case['expected_equal'],passed=True,ports=[a,b],gates=[list(g) for g in C.gates],proof=[{'clause':sorted(c),'step':list(v)} for c,v in zip(known,parents)])

cases=[]
cases.append((dict(name='xor_cancel',n=2,expected_equal=True),lambda C: (C.gate('XOR',C.gate('XOR',1,2),2),1),lambda C,p,q:p,lambda C,p,q:q))
cases.append((dict(name='distributive',n=3,expected_equal=True),lambda C:(C.gate('OR',C.gate('AND',1,2),C.gate('AND',1,3)),C.gate('AND',1,C.gate('OR',2,3))),lambda C,p,q:p,lambda C,p,q:q))
cases.append((dict(name='nonalias',n=2,expected_equal=False),lambda C:(C.gate('XOR',1,2),C.gate('AND',1,2)),lambda C,p,q:p,lambda C,p,q:q))
cases.append((dict(name='reconvergent',n=2,expected_equal=True),lambda C:(C.gate('OR',C.gate('AND',1,2),C.gate('AND',1,-2)),1),lambda C,p,q:p,lambda C,p,q:q))

results=[]
for c,build,p,q in cases:
    r=proof_case(c,build,p,q);results.append(r);print({k:v for k,v in r.items() if k not in ('proof','gates')},flush=True)

# Corruption/malformed gate proofs
c=Circuit(2)
for malformed in [(1,0),(1,4),(0,1),('bad',1)]:
    try:c.gate('AND',*malformed)
    except (ValueError,TypeError):check(True)
    else:raise AssertionError('invalid reference allowed')

payload=dict(status='COMPUTATIONAL: conditional readable DEF clause interface, not native all-rule proof',assertions=assertions,cases=results,quantifiers='exhaustive original input valuations per case; strict resolution closure checked per inference',time_utc='2026-11-05',source=Path(__file__).name)
out=Path(__file__).with_name('raw_408.json');out.write_text(json.dumps(payload,indent=2)+'\n');print('RESULT', {k:v for k,v in payload.items() if k!='cases'},flush=True)
