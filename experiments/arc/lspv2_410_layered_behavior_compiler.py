#!/usr/bin/env python3
"""LSPV-2/410: conditional 88t+r two-stage public DEF-facet compiler.
Only strict Resolution and explicitly assumed readable DEF clause facets.
"""
from itertools import product
import json

S=(1,2,3)
# function truth code f(a,b) with bits indexed 2*a+b
OLD=[(4,1,2,6),(5,4,3,6),(6,4,5,9)] # 6 XOR, 9 XNOR
NEW=[(4,1,2,6),(7,1,2,6),(5,7,3,6),(6,3,3,3)] # 3 NOT first input

def gate_val(op,a,b):return (op>>(2*a+b))&1

def canonical(c):
    v=sorted(set(c),key=lambda x:(abs(x),x<0))
    if any(-x in v for x in v):return None
    return tuple(v)

def cnf(gates):
    clauses=[]
    for out,aa,bb,op in gates:
        for a,b in product((0,1),repeat=2):
            y=1-gate_val(op,a,b)
            lits=(-aa if a else aa,-bb if b else bb,-out if y else out)
            c=canonical(lits)
            if c is not None and c not in clauses:clauses.append(c)
    return clauses

def assignment(gates,original):
    v={i:original[j] for j,i in enumerate(S)}
    for out,a,b,op in gates:v[out]=gate_val(op,v[a],v[b])
    return v

def clause_val(c,v):return any(v[abs(t)]==(t>0) for t in c)

OLD_C=cnf(OLD);NEW_C=cnf(NEW)
assert len(OLD_C)==12 and len(NEW_C)==14,(len(OLD_C),len(NEW_C))
for v in product((0,1),repeat=3):
    ov=assignment(OLD,v);nv=assignment(NEW,v)
    assert all(ov[k]==nv[k] for k in (4,5,6))
    assert all(clause_val(c,ov) for c in OLD_C)
    assert all(clause_val(c,nv) for c in NEW_C)

class DB:
    def __init__(self,axioms):
        self.axioms=list(axioms);self.nodes=[]
        self.clause_to_ref={c:('axiom',i) for i,c in enumerate(axioms)}
    def derive(self,c1,c2,pivot):
        a=set(c1);b=set(c2)
        assert pivot in a and -pivot in b,('pivot',pivot,c1,c2)
        r=canonical((a-{pivot})|(b-{-pivot}))
        assert r is not None,('taut-res',c1,c2,pivot)
        if r not in self.clause_to_ref:
            ref=('res',len(self.nodes))
            self.nodes.append((self.clause_to_ref[c1],self.clause_to_ref[c2],pivot,r))
            self.clause_to_ref[r]=ref
        return r
    def implicate(self,clauses,target):
        """Derive a subclause using only k-c outside variables and strict RES."""
        variables=sorted({abs(x) for c in clauses for x in c}|{abs(x) for x in target})
        tvars={abs(x) for x in target}
        outside=[x for x in variables if x not in tvars]
        fixed={abs(x):int(x<0) for x in target}
        start=len(self.nodes)
        def recurse(i,val):
            if i==len(outside):
                c=next((c for c in clauses if not clause_val(c,val)),None)
                assert c is not None,('not entailed',target,val)
                assert c in self.clause_to_ref
                return c
            x=outside[i]
            val[x]=0;z=recurse(i+1,val)
            val[x]=1;o=recurse(i+1,val)
            del val[x]
            if x in z and -x in o:return self.derive(z,o,x)
            if x not in z:return z
            if -x not in o:return o
            raise AssertionError(('bad converge',x,z,o))
        result=recurse(0,dict(fixed))
        assert set(result)<=set(target),('not subclause',result,target)
        added=len(self.nodes)-start
        assert added<=2**len(outside)-1
        return result,added,len(outside)

behavior=[];reports=[];allnodes=[];proofs=[]
for out in (4,5,6):
    new_in_cone=[];seen=set()
    gates={g[0]:g for g in NEW}
    def rec(y):
        if y in S:return
        g=gates[y]
        if y in seen:return
        for z in (g[1],g[2]):rec(z)
        seen.add(y);new_in_cone.append(g)
    rec(out)
    axi=cnf(new_in_cone)
    for values in product((0,1),repeat=3):
        w=assignment(NEW,values)[out]
        c=canonical(tuple(-s if v else s for s,v in zip(S,values))+((out if w else -out),))
        assert len(c)==4
        db=DB(axi)
        r,cost,deficit=db.implicate(axi,c)
        # IMPORTANT: downstream consumes actual derived subclause, NOT target.
        behavior.append((out,r))
        reports.append({'step':'behavior','output':out,'target':list(c),'derived':list(r),
                        'cost':cost,'deficit':deficit,'cone':[g[0] for g in new_in_cone]})
        proofs.append({'stage':'behavior','gate':out,'target':list(c),
                       'axioms':[list(x) for x in axi],
                       'nodes':[{'left':list(node[0]),'right':list(node[1]),
                                 'pivot':node[2],'clause':list(node[3])} for node in db.nodes],
                       'root':list(r)})
        for node in db.nodes:allnodes.append(('behavior',out,c,node))

assert len(behavior)==24
for facet in OLD_C:
    names=set(abs(t) for t in facet)
    axi=list(dict.fromkeys(c for output,c in behavior if output in names))
    assert axi
    db=DB(axi)
    r,cost,deficit=db.implicate(axi,facet)
    reports.append({'step':'facet','target':list(facet),'derived':list(r),'cost':cost,'deficit':deficit})
    proofs.append({'stage':'facet','target':list(facet),
                   'axioms':[list(x) for x in axi],
                   'nodes':[{'left':list(node[0]),'right':list(node[1]),
                             'pivot':node[2],'clause':list(node[3])} for node in db.nodes],
                   'root':list(r)})
    for node in db.nodes:allnodes.append(('facet',facet,node))
counts={'old_defs':len(OLD),'new_defs':len(NEW),'original_facets':len(OLD_C),
        'replacement_facets':len(NEW_C),'behavioral_clauses':len(behavior),
        'behavior_res':sum(z['cost'] for z in reports if z['step']=='behavior'),
        'facet_res':sum(z['cost'] for z in reports if z['step']=='facet'),
        'total_res':len(allnodes)}
counts['q_new']=counts['new_defs']+counts['total_res']
counts['coefficient_old']=2**14;counts['coefficient_new']=88
assert all(z['deficit']<=3 and z['cost']<=7 for z in reports)
assert counts['total_res']==counts['behavior_res']+counts['facet_res']
raw={'label':'LSPV2_410_two_stage_public_def_facets',
     'scope':'explicit readable DEF facets; pure RES consumers; original support <=3; NOT certified native Rmix341',
     'old_gates':OLD,'new_gates':NEW,'old_facets':[list(c) for c in OLD_C],
     'new_facets':[list(c) for c in NEW_C],
     'reports':reports,'proofs':proofs,'counts':counts,
     'proof_status':'restricted symbolic theorem; computational finite positive control; full grammar and B3 open'}
print(json.dumps(counts,indent=2))
with open('LSPV2_410_two_stage_raw.json','w') as f:json.dump(raw,f,indent=2)
