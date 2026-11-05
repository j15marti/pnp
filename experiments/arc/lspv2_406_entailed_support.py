#!/usr/bin/env python3
"""LSPV-2/406 finite tests. Conditional unbounded-input grammar, NOT native R_mix341.
Each source is (u) AND (u OR v) for every other original variable v;
equivalent to u, SAT, and explicitly mentions all original inputs.
"""
from itertools import product
import json
V=('u','a','b','z','p','q')
CLAUSES=((('p',1),),(('p',0),),(('q',1),),(('q',0),),
         (('p',1),('q',1)),(('p',1),('q',0)),
         (('p',0),('q',1)),(('p',0),('q',0)))
def cnf(mask,env):
    return all(any(bool(env[var])==bool(pos) for var,pos in clause)
               for j,clause in enumerate(CLAUSES) if mask&(1<<j))
def root(mask,env):
    return bool(env['u'] or (env['a']^env['b']^(env['z'] and cnf(mask,env))))
def support(mask):
    essential=[]; probes=0
    for var in V:
        for x in product((0,1),repeat=len(V)):
            env=dict(zip(V,x)); alt=env.copy(); alt[var]^=1
            probes+=1
            if root(mask,env)!=root(mask,alt):
                essential.append(var);break
    return essential,probes
def well_formed_paid_gates(records):
    used=set(V)
    for rec in records:
        if not isinstance(rec,dict) or set(rec)!={'id','op','in'}:
            return False
        rid=rec['id']
        if not isinstance(rid,str) or rid in used:return False
        ins=rec['in']
        if rec['op'] not in ('AND','OR','XOR') or not isinstance(ins,list) or len(ins)!=2:
            return False
        if not all(isinstance(t,str) and t in used for t in ins):return False
        used.add(rid)
    return True
r={'id':'LSPV2_406_PROMISED_ENTAILED_SUPPORT','scope':'conditional unbounded-input signed circuit syntax, NOT native Rmix341',
   'cnf_subsets':0,'sat_C':0,'unsat_C':0,'support_size_histogram':{},
   'source_entailed_tests':0,'support_checks':0,'malformed_rejected':0,'seed':None}
for mask in range(256):
    count=sum(cnf(mask,dict(p=p,q=q)) for p,q in product((0,1),repeat=2))
    supp,probes=support(mask)
    assert (len(supp)<=3)==(count==0),(mask,supp,count)
    assert all(v in supp for v in ('u','a','b'))
    assert ('z' in supp)==(count>0)
    r['support_checks']+=probes
    for bits in product((0,1),repeat=6):
        env=dict(zip(V,bits))
        if env['u']==1:
            assert root(mask,env)
            r['source_entailed_tests']+=1
    r['cnf_subsets']+=1
    r['sat_C']+=bool(count);r['unsat_C']+=not bool(count)
    k=str(len(supp));r['support_size_histogram'][k]=r['support_size_histogram'].get(k,0)+1
assert well_formed_paid_gates([{'id':'g1','op':'XOR','in':['a','b']},
                               {'id':'g2','op':'AND','in':['z','p']}])
bad=[
 [{'id':'g1','op':'XOR','in':['a','g2']}],
 [{'id':'a','op':'AND','in':['a','b']}],
 [{'id':'g1','op':'XOR','in':['a','b']},{'id':'g1','op':'OR','in':['a','b']}],
 [{'id':'g1','op':'AND','in':['a']}],
 [{'id':'g1','op':'NAND','in':['a','b']}],
 [{'id':'g1','op':'AND','in':['a','b'],'proof':'oracle'}]]
for pair in bad:
    assert not well_formed_paid_gates(pair);r['malformed_rejected']+=1
for x,y in product((0,1),repeat=2):
    a=x^y;b=a^y
    assert b==x and (a^x^y)==0 and (b^a^y)==0
r['typed_nested_countertest']={
 'source':'(x) AND (x OR y): SAT; x=1, y arbitrary',
 'paid_records':['AND3 sources -> x=1','DEF a := XOR(x,y)','DEF b := XOR(a,y)'],
 'desired_GF2_rows':['a XOR x XOR y = 0','b XOR a XOR y = 0'],
 'semantic_identity':'b=x for all original assignments',
 'native_GF2_export_legality':'OPEN: paid DEF-to-AFFINE exported port not specified in /341',
 'forbidden_shortcut':'a or b as a globally asserted true literal',
 'verified_b_equals_x':True}
r['finite_checks_completed']=r['source_entailed_tests']+r['support_checks']+r['malformed_rejected']+8
print(json.dumps(r,indent=2,sort_keys=True))
