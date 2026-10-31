#!/usr/bin/env python3
"""LSPV-3 ARC273: source-authenticated star-cofactor broker, full source controls.
Standard library only. Fully reproducible finite experiment; no native FLMV claim.
"""
import argparse, collections, hashlib, itertools, json, math, random, sys, time, tracemalloc
from pathlib import Path

SEED=2731031
class BudgetExhausted(Exception): pass

def xor3(vs, parity):
    out=[]
    for vals in itertools.product((0,1),repeat=3):
        if vals[0]^vals[1]^vals[2] != parity:
            out.append(tuple(v if b==0 else -v for v,b in zip(vs,vals)))
    return out

def pin(v, p, q, val):
    fixed = v if val else -v
    return [(fixed, s*p,t*q) for s in (1,-1) for t in (1,-1)]

def module(k, j, p, q, r, extras):
    base=1+j*(5+2*k)
    a,b,c,u,v=[base+i for i in range(5)]
    x=1+k*(5+2*k)
    out=xor3((x,a,b),p)+xor3((a,b,c),q)+pin(c,u,v,r)
    for t in range(k):
        d,e=base+5+2*t,base+6+2*t
        out+=xor3((x,d,e),extras[t])
    return out

def star(k, label, rng, opposite='last'):
    charges=[];clauses=[];target=rng.randrange(2)
    for j in range(k):
        p,q=rng.randrange(2),rng.randrange(2)
        t=target ^ (int(label=='UNSAT' and j==k-1))
        r=t^p^q
        extras=[rng.randrange(2) for _ in range(k)]
        charges.append({'j':j,'p':p,'q':q,'r':r,'t':t,'extras':extras})
        clauses.extend(module(k,j,p,q,r,extras))
    n=1+k*(5+2*k)
    return {'name':f'STAR_K{k}_{label}','n':n,'clauses':[list(c) for c in clauses],
            'canonical':True,'k':k,'charges':charges,'expected':label,'shared':n}

def cofactor(clauses, var, val):
    out=[]
    for c in clauses:
        if (var if val else -var) in c:continue
        nc=tuple(l for l in c if abs(l)!=var)
        out.append(nc)
    return out

def renumber(cs):
    v=sorted({abs(x) for c in cs for x in c});d={x:i+1 for i,x in enumerate(v)}
    return [tuple((1 if l>0 else -1)*d[abs(l)] for l in c) for c in cs],d

def dimacs(cs):
    n=max((abs(l) for c in cs for l in c),default=0)
    return ('p cnf %d %d\n'%(n,len(cs))+''.join(' '.join(map(str,c))+' 0\n' for c in cs))

def sat_clause(c, assign):
    return any((assign[abs(l)]==int(l>0)) for l in c)

def verify_witness(cs,assign):
    return all(sat_clause(c,assign) for c in cs)

def dpll(cs, fixed=None, metrics=None, node_limit=None):
    metrics=metrics if metrics is not None else collections.Counter()
    start={} if fixed is None else dict(fixed)
    vars_=sorted({abs(l) for c in cs for l in c})
    occ=collections.Counter(abs(l) for c in cs for l in c)
    metrics['heuristic_source_literal_reads']+=sum(len(c) for c in cs)
    def unit_propagate(a):
        while True:
            changed=False
            for c in cs:
                metrics['clause_scans']+=1
                un=[];satisfied=False
                for l in c:
                    metrics['literal_tests']+=1
                    v=abs(l)
                    if v not in a:un.append(l)
                    elif a[v]==int(l>0):satisfied=True;break
                if satisfied:continue
                if len(un)==0:
                    metrics['contradictions']+=1
                    return None
                if len(un)==1:
                    l=un[0];v=abs(l);b=int(l>0)
                    if v in a and a[v]!=b:
                        metrics['contradictions']+=1
                        return None
                    if v not in a:
                        a[v]=b;metrics['propagations']+=1;changed=True
            if not changed:return a
    def dfs(a):
        if node_limit is not None and metrics['nodes']>=node_limit:raise BudgetExhausted
        metrics['nodes']+=1
        a=unit_propagate(dict(a))
        if a is None:return None
        all_sat=True
        for c in cs:
            if not any(abs(l) in a and a[abs(l)]==int(l>0) for l in c):
                all_sat=False;break
        if all_sat:
            return {v:a.get(v,0) for v in vars_}
        v=max((v for v in vars_ if v not in a),key=lambda t:(occ[t],-t))
        metrics['heuristic_variable_comparisons']+=len(vars_)
        metrics['decisions']+=1
        for b in (0,1):
            ans=dfs({**a,v:b})
            if ans is not None:return ans
        return None
    return dfs(start)

def source_targets(cs):
    targets=[]
    for j,c in enumerate(cs,1):
        o=[]
        for l in c:
            s=int(l>0);u=1-s
            o.append({'occurrence':f'x_{abs(l)},{j}','variable':abs(l), 'literal':l,
                      'S':s,'invert_S_to_U':1-s,'U':u,'invert_U_to_S':1-u})
        targets.append({'j':j,'source':list(c),'occurrences':o})
    return targets

def extreme_matrix(cs):
    out=[]
    for i,c in enumerate(cs):
        for j in range(i+1,len(cs)):
            d=cs[j]
            shared=set(map(abs,c))&set(map(abs,d))
            ca={abs(l):int(l>0) for l in c if abs(l) in shared}
            da={abs(l):int(l>0) for l in d if abs(l) in shared}
            same=any(ca[v]==da[v] for v in shared)
            opposite=any(ca[v]!=da[v] for v in shared)
            flags={'SS':int(not opposite),'SU':int(not same),
                   'US':int(not same),'UU':int(not opposite)}
            out.append({'i':i+1,'j':j+1,'shared':sorted(shared),'flags':flags})
    return out

def Ntuple(cs,n,a):
    counts=[0,0,0,0];by=[]
    for c in cs:
        t=sum(a[abs(l)]==int(l>0) for l in c)
        if len(c)==3:counts[t]+=1
        by.append(t)
    return {'all_clauses_sat':all(x>=1 for x in by),'N3':counts,'true_literals_per_clause':by}

def trails(cs,n):
    z={v:0 for v in range(1,n+1)}
    zero=Ntuple(cs,n,z);one=Ntuple(cs,n,{v:1 for v in z})
    gray=[];maxmask=min(16,1<<min(n,4))
    for t in range(maxmask):
        mask=t^(t>>1)
        a={v:int(bool(mask&(1<<(v-1)))) for v in range(1,n+1)}
        b={v:1-a[v] for v in a}
        x=Ntuple(cs,n,a);y=Ntuple(cs,n,b)
        ok=all(len(c)!=3 or sum(a[abs(l)]==int(l>0) for l in c)==3-sum(b[abs(l)]==int(l>0) for l in c) for c in cs)
        if not ok:raise AssertionError('complement identity')
        gray.append({'t':t,'mask':mask,'count3':x['N3'],'complement_count3':y['N3'],
                     'SAT':x['all_clauses_sat'],'complement_SAT':y['all_clauses_sat']})
    return {'all_zero':zero,'all_one':one,'gray_trail':gray}

def recognize(cs,n, counter):
    m=len(cs)
    k=next((k for k in range(1,200) if m==4*k*(k+3) and n==1+k*(5+2*k)),None)
    counter['schema_candidates']+=1
    if k is None:counter['failed_recognitions']+=1;return None
    x=n;charges=[]
    for j in range(k):
        lo=j*(12+4*k)
        c1=[tuple(c) for c in cs[lo:lo+4]]
        c2=[tuple(c) for c in cs[lo+4:lo+8]]
        pc=[tuple(c) for c in cs[lo+8:lo+12]]
        p=next((v for v in (0,1) if c1==xor3((x,1+j*(5+2*k),2+j*(5+2*k)),v)),None)
        q=next((v for v in (0,1) if c2==xor3((1+j*(5+2*k),2+j*(5+2*k),3+j*(5+2*k)),v)),None)
        r=next((v for v in (0,1) if pc==pin(3+j*(5+2*k),4+j*(5+2*k),5+j*(5+2*k),v)),None)
        counter['source_literal_compares']+=sum(map(len,c1+c2+pc))
        if None in (p,q,r):counter['failed_recognitions']+=1;return None
        extras=[]
        for t in range(k):
            current=[tuple(c) for c in cs[lo+12+4*t:lo+16+4*t]]
            a=6+j*(5+2*k)+2*t
            b=a+1
            bit=next((v for v in (0,1) if current==xor3((x,a,b),v)),None)
            counter['source_literal_compares']+=sum(map(len,current))
            if bit is None:counter['failed_recognitions']+=1;return None
            extras.append(bit)
        charges.append({'j':j,'p':p,'q':q,'r':r,'t':p^q^r,'extras':extras})
    return {'k':k,'charges':charges,'shared':x}

def construct_child(cs,k,j,x,b):
    block=cs[j*(12+4*k):(j+1)*(12+4*k)]
    cc=cofactor(block,x,b)
    ren,d=renumber(cc)
    return {'xval':b,'block':j,'clauses':[list(c) for c in ren],
            'bytes':len(dimacs(ren).encode()),'literal_occurrences':sum(len(c) for c in ren)}

def selector(cs,n,counter,record):
    desc=recognize(cs,n,counter)
    if desc is None:
        counter['policy_switches']+=1
        t=collections.Counter();w=dpll(cs,metrics=t)
        counter.update({f'fallback_{key}':v for key,v in t.items()})
        record['policy']='fallback_UP_DPLL';record['child_summary']=[]
        return w,desc
    record['policy']='authenticated_canonical_star_two_sided_DP'
    k=desc['k'];x=desc['shared']; children=[];selected=[];boundary=[]
    witness=None
    for b in (0,1):
        good=True;localw=[]
        for j in range(k):
            child=construct_child(cs,k,j,x,b)
            counter['original_clause_reads']+=12+4*k
            counter['child_emission_bytes']+=child['bytes']
            counter['guest_input_literal_reads']+=child['literal_occurrences']
            counter['guest_calls']+=1
            metrics=collections.Counter()
            ww=dpll(child['clauses'],metrics=metrics)
            counter.update({f'guest_{key}':v for key,v in metrics.items()})
            child['guest_answer']='SAT' if ww is not None else 'UNSAT'
            child['guest_nodes']=metrics['nodes'];child['guest_literal_tests']=metrics['literal_tests']
            children.append(child)
            if ww is None:
                good=False
                selected.append({'boundary':b,'bad_module':j,'source_ids':list(range(j*(12+4*k)+1,j*(12+4*k)+13)),
                                 'derived_unit':desc['charges'][j]['t'],
                                 'parity_rows':[[x,1+j*(5+2*k),2+j*(5+2*k)],
                                                [1+j*(5+2*k),2+j*(5+2*k),3+j*(5+2*k)]],
                                 'pin_var':3+j*(5+2*k)})
                break
            inv={val:key for key,val in renumber(cofactor(cs[j*(12+4*k):(j+1)*(12+4*k)],x,b))[1].items()}
            localw.append({inv[key]:value for key,value in ww.items()})
        boundary.append({'b':b,'all_feasible':good,'blocks_tested':len(localw)+int(not good)})
        if good:
            witness={x:b}
            for tmp in localw:witness.update(tmp)
            for v in range(1,n+1):witness.setdefault(v,0)
            break
    record['child_summary']=[{k:v for k,v in child.items() if k!='clauses'} for child in children]
    record['children'] = children
    record['boundary']=boundary
    record['forbidden_cubes']=selected
    record['sources']=desc
    return witness,desc

def deterministic_witness(desc):
    k=desc['k'];x=desc['shared'];ts={r['t'] for r in desc['charges']}
    if len(ts)!=1:return None
    b=next(iter(ts));assign={x:b}
    for ch in desc['charges']:
        j=ch['j'];a=1+j*(5+2*k);bb=a+1;c=a+2;u=a+3;v=a+4
        assign[a]=0;assign[bb]=b^ch['p'];assign[c]=ch['r'];assign[u]=0;assign[v]=0
        # a xor b xor c = q -> b must be q xor r, consistent only if b= p xor q xor r
        assert assign[bb]==ch['q']^ch['r']
        for t,h in enumerate(ch['extras']):
            d=a+5+2*t;e=d+1;assign[d]=0;assign[e]=b^h
    return assign

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',default='raw273.json');args=parser.parse_args()
    rng=random.Random(SEED)
    fixtures=json.loads((Path(__file__).parent/'fixtures271.json').read_text())
    sources=[]
    for k in (1,2,3,4,5,6):
        sources += [star(k,'SAT',rng)]
        if k>=2:sources += [star(k,'UNSAT',rng)]
    for name in ('HORN_CHAIN_SAT','HORN_CHAIN_UNSAT','KROM_SAT','KROM_UNSAT','SWAP6_SAT','W1_UNSAT','SWAP6_RENAMED_SAT','W1_RENAMED_UNSAT'):
        f=fixtures[name]
        sources.append({'name':name,'n':f['n'],'clauses':f['original_clauses'],
                        'canonical':False,'expected':'SAT' if 'UNSAT' not in name else 'UNSAT'})
    rows=[];start=time.time()
    for i,s in enumerate(sources):
        cs=[tuple(c) for c in s['clauses']];n=s['n']
        baseline=collections.Counter();complete=True
        try:w=dpll(cs,metrics=baseline,node_limit=(2000 if s['canonical'] and s['expected']=='UNSAT' and s['k']>=3 else None))
        except BudgetExhausted:w=None;complete=False
        truth=('SAT' if w is not None else 'UNSAT') if complete else s['expected']
        if complete:assert truth==s['expected'],(s['name'],truth)
        counter=collections.Counter()
        endpoint=trails(cs,n)
        counter['endpoint_literal_reads']=2*sum(len(c) for c in cs)
        counter['flip_literal_reads']=2*len(endpoint['gray_trail'])*sum(len(c) for c in cs)
        record={}
        p,desc=selector(cs,n,counter,record)
        if complete:assert (p is not None)==(w is not None)
        else:assert p is None and desc is not None and len(set(v['t'] for v in desc['charges']))==2
        if p is not None:assert verify_witness(cs,p)
        if desc is not None:
            deterministic=deterministic_witness(desc)
            assert (deterministic is None)==(truth=='UNSAT')
            if deterministic is not None:assert verify_witness(cs,deterministic)
        targets=source_targets(cs)
        matrix=extreme_matrix(cs)
        cost_baseline=baseline['literal_tests']+baseline['nodes']+sum(len(c) for c in cs)
        cost_controller=(sum(counter.values())+counter['guest_literal_tests']*0)
        row={'id':i+1,'name':s['name'],'expected':truth,'n':n,'m':len(cs),
             'source_dimacs_bytes':len(dimacs(cs).encode()),'original_clauses':[list(c) for c in cs],
             'metadata':{k:v for k,v in s.items() if k not in ('clauses',)},
             'source_occurrences':targets,'extreme_pair_matrix':matrix,
             'endpoints_and_flips':endpoint,'baseline':dict(baseline),'baseline_complete':complete,
             'baseline_selected_events':cost_baseline,'controller':dict(counter),
             'controller_selected_events':cost_controller,
             'policy':record,'answer':truth,'witness':{str(k):v for k,v in p.items()} if p is not None else None}
        rows.append(row)
        print(f"{s['name']:<25} {truth:<5} baseline nodes={baseline['nodes']:>6} child guest nodes={counter['guest_nodes']:>6} source bytes={row['source_dimacs_bytes']:>6} output bytes={counter['child_emission_bytes']:>6}",flush=True)
    raw={'run':'CANONICAL-STAR-BROKER273','seed':SEED,'model':'Python instrumented steps; not native FLMV',
         'proof_status':'restricted exact star-join lemma; independently reviewed mathematical proof pending',
         'elapsed_s':round(time.time()-start,3),'rows':rows}
    path=Path(args.out);path.write_text(json.dumps(raw,sort_keys=True,separators=(',',':'))+'\n')
    summaries=[]
    for z in rows:
        p=z['policy'];c=z['controller'];n=z['name'];
        summaries.append({'name':n,'label':z['answer'],'n':z['n'],'m':z['m'],
                          'source_dimacs_bytes':z['source_dimacs_bytes'],
                          'baseline_nodes':z['baseline']['nodes'],'baseline_complete':z['baseline_complete'],
                          'baseline_literal_tests':z['baseline']['literal_tests'],
                          'controller_guest_nodes':c.get('guest_nodes',0),
                          'controller_guest_literal_tests':c.get('guest_literal_tests',0),
                          'guest_calls':c.get('guest_calls',0),
                          'output_bytes':c.get('child_emission_bytes',0),
                          'max_child_bytes':max((x['bytes'] for x in p.get('children',[])),default=0),
                          'fallback':p['policy']=='fallback_UP_DPLL',
                          'selected_baseline_events':z['baseline_selected_events'],
                          'selected_controller_events':z['controller_selected_events'],
                          'extreme_pairs':len(z['extreme_pair_matrix'])})
    summary={'run':raw['run'],'seed':SEED,'cases':len(rows),'SAT':sum(z['answer']=='SAT' for z in rows),
             'UNSAT':sum(z['answer']=='UNSAT' for z in rows),
             'source_occurrences':sum(3*len(z['original_clauses']) for z in rows if all(len(c)==3 for c in z['original_clauses'])),
             'pair_matrices':sum(len(z['extreme_pair_matrix']) for z in rows),
             'total_baseline_nodes':sum(z['baseline']['nodes'] for z in rows),
             'total_controller_guest_nodes':sum(z['controller'].get('guest_nodes',0)+z['controller'].get('fallback_nodes',0) for z in rows),
             'total_guest_calls':sum(z['controller'].get('guest_calls',0) for z in rows),
             'rows':summaries}
    Path(path.parent/'summary273.json').write_text(json.dumps(summary,indent=2)+'\n')
    print('RAW_SHA256',hashlib.sha256(path.read_bytes()).hexdigest());print('ELAPSED',raw['elapsed_s'])
if __name__=='__main__':main()