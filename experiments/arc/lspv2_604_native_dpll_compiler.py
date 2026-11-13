#!/usr/bin/env python3
"""LSPV-2/604, independent source-bound DPLL-tree -> archived /386 strict RES bytes.
NOT a compiler for historical R_mix341. Python >=3.10; Node checker supplied separately.

Usage: python lspv2_604_native_dpll_compiler.py OUT_DIR CHECKER386_JS
"""
from __future__ import annotations
from pathlib import Path
import json, hashlib, sys, subprocess, copy, itertools, time

def check(p, message):
    if not p: raise AssertionError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def canon(xs):return sorted(set(xs),key=lambda v:(abs(v),v))
def lit_false(l, assn):
    v=assn.get(abs(l))
    return v is not None and (v == 0 if l>0 else v == 1)
def lit_true(l, assn):
    v=assn.get(abs(l))
    return v is not None and (v == 1 if l>0 else v == 0)
def false_clause(c, assn):return all(lit_false(l,assn) for l in c)

def graphs():
    g=[]
    g.append(('K4',4,[(i,j) for i in range(4) for j in range(i+1,4)]))
    g.append(('K33',6,[(i,j) for i in range(3) for j in range(3,6)]))
    g.append(('CUBE',8,[(i,i^(1<<b)) for i in range(8) for b in range(3) if i < (i^(1<<b))]))
    return g

def make_source(name, h, edges):
    edges=sorted([sorted(e) for e in edges])
    E=len(edges)
    check(2*E==3*h,'noncubic edge count')
    occ=[[] for _ in range(h)]
    for i,(a,b) in enumerate(edges):
        occ[a].append(i+1); occ[b].append(i+1)
    check(all(len(x)==3 for x in occ),'noncubic degree')
    guard=E+1;charge=[1]+[0]*(h-1)
    rows=[]
    for v in range(h):
        for mask in range(8):
            bits=[(mask>>j)&1 for j in range(3)]
            if sum(bits)%2==charge[v]:continue
            c=canon([(-x if b else x) for x,b in zip(occ[v],bits)]+[-guard]);rows.append({'kind':'SOURCE','source':v,'parents':[],'c':c})
    rows.append({'kind':'SOURCE','source':-1,'parents':[],'c':[guard]})
    check(len(rows)==4*h+1,'source count')
    # SOURCE external bytes independent of serialized native certificate
    text=f'p cnf {guard} {len(rows)}\n'+''.join(' '.join(map(str,r['c']))+' 0\n' for r in rows)
    # Independent row-by-row parse and signed occurrence verification
    lines=text.splitlines(); head=lines[0].split();check(head==['p','cnf',str(guard),str(len(rows))],'header mismatch')
    clauses=[]
    for line in lines[1:]:
        toks=list(map(int,line.split()));check(toks[-1]==0,'line terminator')
        clauses.append(toks[:-1]); check(all(0<abs(l)<=guard for l in toks[:-1]),'invalid literal')
    check(clauses==[r['c'] for r in rows],'different input formulas')
    return {'h':h,'edges':edges,'charge':charge,'guard':guard},rows,text.encode('ascii')

def run_dpll(spec, sources, order):
    clauses=[r['c'] for r in sources];n=len(order)
    check(set(order)==set(range(1,spec['guard']+1)),'incomplete branch order')
    # Full binary DPLL refutation extraction, no auxiliary assumptions as proof premises.
    records=copy.deepcopy(sources)
    leaves=0; internal=0; skipped=0; nodes=0; maxdepth=0; saved={}
    def walk(i,assn):
        nonlocal leaves,internal,skipped,nodes,maxdepth
        nodes+=1;maxdepth=max(maxdepth,i)
        for j,c in enumerate(clauses):
            if false_clause(c,assn):
                leaves+=1;return j
        if i==n:
            raise AssertionError('SAT assignment found; not an UNSAT tree: '+str(assn))
        x=order[i];internal+=1
        a=dict(assn);a[x]=0;lo=walk(i+1,a)
        b=dict(assn);b[x]=1;hi=walk(i+1,b)
        A=records[lo]['c'];B=records[hi]['c']; ap=x in A;bm=-x in B
        # Inductive invariant: each returned clause is falsified by branch prefix.
        check(false_clause(A,a) and false_clause(B,b),'bad child invariant')
        if not ap:
            check(-x not in A,'wrong x in 0 branch');skipped+=1
            check(false_clause(A,assn),'nonpivot not falsified at parent');return lo
        if not bm:
            check(x not in B,'wrong x in 1 branch');skipped+=1
            check(false_clause(B,assn),'nonpivot not falsified at parent');return hi
        c=canon([y for y in A if y!=x]+[y for y in B if y!=-x])
        check(not any(-y in c for y in c),'tautological resolvent')
        check(false_clause(c,assn),'parent invariant failed')
        rec={'kind':'RES','c':c,'pivot':x,'parents':[lo,hi]};idx=len(records);records.append(rec)
        return idx
    root=walk(0,{})
    check(records[root]['c']==[],'nonempty root')
    # The checker insists the final serialized row is the contradiction.
    check(root==len(records)-1,'final contradiction absent')
    rcount=len(records)-len(sources)
    packet={'spec':spec,'records':records,'gate_defs':[[0,spec['guard']+1,1,2]],'summary':{
        'source':len(sources),'def_views':0,'resolution':rcount,'paid_gates':1,
        'paid_total':rcount+1,'live_records':len(records)}}
    # Check all accepted clause records are source or exact strict RES.
    for i,rec in enumerate(records):
        check(rec['c']==canon(rec['c']) and not any(-l in rec['c'] for l in rec['c']),'unclean')
        if rec['kind']=='RES':
            p,q=rec['parents'];x=rec['pivot'];check(p<i and q<i and x in records[p]['c'] and -x in records[q]['c'],'bad RES')
            c=canon([y for y in records[p]['c'] if y!=x]+[y for y in records[q]['c'] if y!=-x]); check(c==rec['c'],'bad resolvent')
    return packet, {'search_nodes':nodes,'visited_conflict_leaves':leaves,'branch_internal':internal,
                    'skipped_pivots':skipped,'derived_resolution':rcount,'tree_max_depth':maxdepth,
                    'source':len(sources),'variables':n}

def native(checker, file):
    t0=time.perf_counter(); proc=subprocess.run(['node',str(checker),str(file)],capture_output=True,text=True,timeout=120)
    stdout=proc.stdout.strip(); stderr=proc.stderr.strip()
    if proc.returncode==0:
        obj=json.loads(stdout);obj.pop('file',None);obj.pop('sha256',None)
        return {'exit':0,'verdict':'ACCEPT','checker_metrics':obj}
    reason=(stderr.split('Error: ',1)[1].splitlines()[0] if 'Error: ' in stderr else stderr[:200])
    return {'exit':proc.returncode,'verdict':'REJECT','error':reason}

def independent(p,cnf):
    code=Path(__file__).with_name('lspv2_604_independent_source_replay.cjs')
    result=subprocess.run(['node',str(code),str(p),str(cnf)],capture_output=True,text=True,timeout=30)
    if result.returncode==0:return {'exit':0,'check':json.loads(result.stdout)}
    reason=(result.stderr.split('Error: ',1)[1].splitlines()[0] if 'Error: ' in result.stderr else result.stderr[:180])
    return {'exit':result.returncode,'error':reason}

def main():
    out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
    checker=Path(sys.argv[2]);check(checker.exists(),'checker absent')
    native_sha=sha(checker.read_bytes());
    check(native_sha=='22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113','wrong native checker')
    positives=[]; negs=[]
    for name,h,edges in graphs():
        spec,sources,raw=make_source(name,h,edges)
        srcfile=out/f'{name}_SOURCE.cnf';srcfile.write_bytes(raw)
        order_set=[('guard_first',[spec['guard']]+list(range(1,spec['guard']))),
                   ('guard_last',list(range(1,spec['guard']+1))),
                   ('reverse',[spec['guard']]+list(range(spec['guard']-1,0,-1)))]
        for ordname,order in order_set:
            packet,measure=run_dpll(spec,sources,order)
            p=out/f'{name}_{ordname}_DPLL_RES.json'; b=(json.dumps(packet,separators=(',',':'),ensure_ascii=True)+'\n').encode('utf8');p.write_bytes(b)
            response=native(checker,p);check(response['exit']==0,f'{p} original checker rejected {response}')
            positives.append({'case':name,'order':ordname,'source_sha256':sha(raw),'accepted_sha256':sha(b),
                              'packet_bytes':len(b),'statistics':measure,'native':response,'separate_source_replay': independent(p,srcfile)})
    # Native accepted K4 control versus hostile variations. Every negative based on an accepted packet, not fabricated fake grammar.
    p0=json.loads((out/'K4_guard_first_DPLL_RES.json').read_text())
    def mutate(label,fn):
        cp=copy.deepcopy(p0);fn(cp); p=out/(f'REJECT_{label}.json');b=(json.dumps(cp,separators=(',',':'))+'\n').encode();p.write_bytes(b)
        r=native(checker,p);check(r['exit']!=0,'BAD packet was ACCEPTED: '+label)
        negs.append({'case':label,'sha256':sha(b),'bytes':len(b),'native':r,'separate_source_replay':independent(p,out/'K4_SOURCE.cnf')})
    mutate('forged_source',lambda d:d['records'][0].update({'c':[-d['spec']['guard']]}))
    mutate('bad_signed_pivot',lambda d:d['records'][-1].update({'pivot':-d['records'][-1]['pivot']}))
    mutate('missing_source',lambda d:d['records'][0].update({'source':-1}))
    mutate('underpaid',lambda d:d['summary'].update({'paid_total':0}))
    mutate('unsupported_XOR',lambda d:d['records'][-1].update({'kind':'XOR'}))
    mutate('forward_dependency',lambda d:d['records'][-1].update({'parents':[len(d['records']),d['records'][-1]['parents'][1]]}))
    mutate('duplicate_gate_owner',lambda d:d['gate_defs'].append([0,d['spec']['guard']+2,1,2]))
    mutate('SAT_even_charge',lambda d:d['spec'].update({'charge':[0]*d['spec']['h']}))
    check(all(q['separate_source_replay']['exit']==0 for q in positives),'independent positive failed')
    check(all(q['separate_source_replay']['exit']!=0 for q in negs),'independent negative failed')
    manifest={'run_id':'LSPV-2/604','scope':'original archived /386 strict SOURCE+RES, not R_mix341',
            'native_checker_sha256':native_sha,'positive':positives,'negative':negs,
            'known_compiler_limit':'DPLL tree only, no generic arbitrary SAT decider transfer',
            'status':{'P2-D1':'OPEN','P2-C3':'OPEN','P2-B1':'OPEN','P2-B2/B3':'OPEN','P_vs_NP':'OPEN'}}
    b=(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode();(out/'LSPV2_604_NATIVE_DPLL_COMPILER_RAW.json').write_bytes(b)
    print(json.dumps({'cases':[(p['case'],p['order'],p['statistics']['derived_resolution'],p['statistics']['search_nodes']) for p in positives],
                      'accept':len(positives),'reject':len(negs),'manifest_sha256':sha(b),'checker_sha256':native_sha},indent=2))
if __name__=='__main__':main()
