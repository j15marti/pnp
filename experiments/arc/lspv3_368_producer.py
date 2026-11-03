#!/usr/bin/env python3
"""ER2 conservative-gate support projection to ordinary Resolution.
Fully deterministic, explicit signed clause certificate. No SAT oracle used.
"""
from __future__ import annotations
import json
from itertools import product
from pathlib import Path

OUT=Path(__file__).with_name('lspv3_368_results.json')

def normalize(c):
    s=set(c)
    if 0 in s or any(-x in s for x in s): raise ValueError('zero or tautological clause')
    return sorted(s,key=lambda x:(abs(x),x<0))

def resolve(a,b,p):
    a=set(a);b=set(b)
    if p in a and -p in b: pass
    elif -p in a and p in b: a,b=b,a
    else: raise ValueError('invalid pivot')
    return normalize((a-{p}) | (b-{-p}))

def definition(v,a,b):
    if v<=0 or a==0 or b==0 or abs(a)==abs(b) or abs(a)>=v or abs(b)>=v:
        raise ValueError('non-conservative AND2')
    return [normalize([-v,a]),normalize([-v,b]),normalize([v,-a,-b])]

def formula(case):
    lines={}; records=[]
    for i,c in enumerate(case['source']):
        idx='s'+str(i); lines[idx]=normalize(c); records.append({'id':idx,'kind':'source','clause':lines[idx]})
    for i,g in enumerate(case['gates']):
        v,a,b=g
        for j,c in enumerate(definition(v,a,b)):
            idx=f'd{i}:{j}';lines[idx]=c;records.append({'id':idx,'kind':'definition_slot','clause':c,'gate':i})
    for i,(x,y,p) in enumerate(case['steps']):
        idx='p'+str(i)
        if x not in lines or y not in lines: raise ValueError('forward parent')
        lines[idx]=resolve(lines[x],lines[y],p)
        records.append({'id':idx,'kind':'resolve','parents':[x,y],'pivot':p,'clause':lines[idx]})
    if lines['p'+str(len(case['steps'])-1)]!=[]: raise ValueError('not refutation')
    return lines,records

def restriction(c,values):
    out=[]
    for l in c:
        if abs(l) in values:
            if values[abs(l)] == (l>0): return None
        else: out.append(l)
    return out

def compile_case(case):
    lines,original=formula(case)
    original_source={i:r['clause'] for i,r in enumerate(original) if r['kind']=='source'}
    S=set()
    for v,a,b in case['gates']:
        for lit in (a,b):
            if abs(lit) not in {g[0] for g in case['gates']}:
                S.add(abs(lit))
    S=sorted(S)
    assert len(S)<=2*len(case['gates'])
    newlines={};pr=[]; derived=0
    for i,c in enumerate(case['source']):
        k=f's{i}';newlines[k]=normalize(c);pr.append({'id':k,'kind':'source','clause':newlines[k]})
    leaf_clauses={}
    for mask in product([False,True],repeat=len(S)):
        alpha=dict(zip(S,mask));val=dict(alpha)
        for v,a,b in case['gates']:
            aval=val[abs(a)] if a>0 else not val[abs(a)]
            bval=val[abs(b)] if b>0 else not val[abs(b)]
            val[v]=aval and bval
        tag=''.join(str(int(a)) for a in mask) or 'empty'
        proxy={}
        for rec in original:
            idx=rec['id'];c=restriction(rec['clause'],val)
            if rec['kind']=='source':
                proxy[idx] = None if c is None else idx
            elif rec['kind']=='definition_slot':
                if c is not None: raise AssertionError('definition not satisfied')
                proxy[idx]=None
            else:
                if c is None:proxy[idx]=None;continue
                x,y=rec['parents'];px,py=proxy[x],proxy[y]
                if px is None and py is None: raise AssertionError('both missing nontrue derived')
                bound=set(c)
                if px is not None and set(restriction(newlines[px],val) or [])<=bound:
                    proxy[idx]=px;continue
                if py is not None and set(restriction(newlines[py],val) or [])<=bound:
                    proxy[idx]=py;continue
                if px is None or py is None: raise AssertionError('missing parent not subsumed')
                p=rec['pivot'];
                if abs(p) in val: raise AssertionError('assigned pivot needs subclause parent')
                z=resolve(newlines[px],newlines[py],p)
                if not set(restriction(z,val) or [])<=bound:raise AssertionError('invalid lifted clause')
                idn=f'a{tag}_{derived}';derived+=1
                newlines[idn]=z;pr.append({'id':idn,'kind':'resolve','parents':[px,py],'pivot':p,'clause':z})
                proxy[idx]=idn
        leaf=proxy[original[-1]['id']]
        if leaf is None:raise AssertionError('lost refutation leaf')
        block={-v if alpha[v] else v for v in S}
        if not set(newlines[leaf])<=block:raise AssertionError('leaf not blocking alpha')
        leaf_clauses[mask]=leaf
    def merge(prefix):
        nonlocal derived
        if len(prefix)==len(S):return leaf_clauses[prefix]
        c0=merge(prefix+(False,));c1=merge(prefix+(True,))
        p=S[len(prefix)]
        C0=set(newlines[c0]);C1=set(newlines[c1])
        if p not in C0:return c0
        if -p not in C1:return c1
        zz=resolve(newlines[c0],newlines[c1],p)
        idn=f'm{derived}';derived+=1;newlines[idn]=zz
        pr.append({'id':idn,'kind':'resolve','parents':[c0,c1],'pivot':p,'clause':zz})
        return idn
    last=merge(())
    if newlines[last]!=[]:raise AssertionError('compiler failed')
    paid=sum(r['kind']=='resolve' for r in pr)
    oldres=len(case['steps']);e=len(case['gates'])
    bound=2**len(S)*(oldres+1)-1
    if paid>bound:raise AssertionError('violated projection bound')
    return {'name':case['name'],'S':S,'e':e,'q_res':oldres,'q_er2':e+oldres,'source':case['source'],'gates':case['gates'],'original':original,'projection':pr,'projection_node_count':paid,'node_upper_bound':bound,'merge_output':last}

CASES=[
    {'name':'no_extension_unit_clash','source':[[1],[-1]],'gates':[],'steps':[('s0','s1',1)]},
    {'name':'one_used_and2','source':[[1,3],[-3],[2],[-1,-2]],'gates':[(4,1,2)],
     'steps':[('s0','s1',3),('d0:2','p0',1),('p1','s2',2),('s3','d0:0',1),('p3','d0:1',2),('p2','p4',4)]},
    {'name':'two_used_and2','source':[[1,3],[-3],[2],[-1,-2]],'gates':[(4,1,2),(5,4,1)],
     'steps':[('s0','s1',3),('d0:2','p0',1),('p1','s2',2),('d1:2','p2',4),('p3','p0',1),('s3','d1:1',1),('p5','s2',2),('p4','p6',5)]}
]

def sat_count(source,variables):
    return sum(all(any((val[abs(l)] if l>0 else not val[abs(l)]) for l in c) for c in source)
               for bits in product([False,True],repeat=len(variables))
               for val in [dict(zip(variables,bits))])

def main():
    results=[]
    for case in CASES:
        entry=compile_case(case)
        vs=sorted({abs(l) for c in case['source'] for l in c})
        entry['sat_models']=sat_count(case['source'],vs)
        if entry['sat_models']!=0:raise AssertionError('bad source')
        models=[]
        for k,c in enumerate(case['source']):
            alt=case['source'][:k]+case['source'][k+1:]
            models.append(sat_count(alt,vs))
        entry['deleted_clause_model_counts']=models
        if len(case['source'])==4:
            mate=case['source'][:-1]+[[1,-2]]
            entry['paired_sat_models']=sat_count(mate,vs)
            assert entry['paired_sat_models']>0
        results.append(entry)
    OUT.write_text(json.dumps({'theorem':'ER2 support projection, W_RES(F) <= 2^(2e)*(q_RES+1)-1',
                               'cases':results,'assertion_status':'passed','seed':None,'type':'deterministic exhaustive finite controls'},indent=2))
    print(json.dumps([{'case':r['name'],'source_clause_count':len(r['source']),'source_vars':len({abs(l) for c in r['source'] for l in c}),
                       'e':r['e'],'q_res':r['q_res'],'S':r['S'],'projection_res_nodes':r['projection_node_count'],
                       'bound':r['node_upper_bound'],'sat_models':r['sat_models'],'matched_sat':r.get('paired_sat_models')} for r in results],indent=2))

if __name__=='__main__':main()
