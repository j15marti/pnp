#!/usr/bin/env python3
"""Exact, source-preserving 2-SAT backdoor flip DAG, finite research controls.
Python 3 stdlib; deterministic. For proof and raw JSON see main().
"""
import itertools, json, hashlib, time, tracemalloc
from collections import Counter

SEED=202610310938

def norm(c):
    return tuple(sorted(set(c),key=lambda x:(abs(x),x<0)))

def truth(lit,a): return bool(a[abs(lit)]) if lit>0 else not bool(a[abs(lit)])
def sat(F,a): return all(any(truth(l,a) for l in C) for C in F)
def counts(F,a): return [sum(truth(l,a) for l in C) for C in F]
def all_assign(n):
    for bits in itertools.product((0,1),repeat=n): yield {i+1:bits[i] for i in range(n)}
def sat_models(F,n): return [a for a in all_assign(n) if sat(F,a)]

def two_sat_sat(clauses,variables,ledger=None):
    vs=sorted(variables)
    if ledger is not None:
        ledger['two_sat_calls']+=1
        ledger['two_sat_literal_probes']+=sum(len(c) for c in clauses)
    if any(len(c)==0 for c in clauses):return False
    adj={l:[] for x in vs for l in (x,-x)}
    rev={l:[] for x in vs for l in (x,-x)}
    for c in clauses:
        if len(c)==1: pairs=[(-c[0],c[0])]
        elif len(c)==2: pairs=[(-c[0],c[1]),(-c[1],c[0])]
        else: raise AssertionError('not 2cnf')
        for x,y in pairs: adj[x].append(y);rev[y].append(x)
    visited=set();order=[]
    def dfs(v):
        visited.add(v)
        for w in adj[v]:
            if w not in visited:dfs(w)
        order.append(v)
    for v in adj:
        if v not in visited: dfs(v)
    comp={}
    def dfs2(v,tag):
        comp[v]=tag
        for w in rev[v]:
            if w not in comp:dfs2(w,tag)
    for v in reversed(order):
        if v not in comp:dfs2(v,len(comp)+1)
    return all(comp[x]!=comp[-x] for x in vs)

def two_sat_witness(clauses,variables,ledger):
    if not two_sat_sat(clauses,variables,ledger):return None
    vs=sorted(variables);a={}
    for v in vs:
        fixed=[(k if z else -k,) for k,z in a.items()]
        if two_sat_sat(list(clauses)+fixed+[(-v,)],vs,ledger):a[v]=0
        else:
            assert two_sat_sat(list(clauses)+fixed+[(v,)],vs,ledger)
            a[v]=1
    return a

def legal_backdoor(F,T): return all(sum(abs(l) not in T for l in c)<=2 for c in F)

def find_backdoor(F,n,max_k,ledger):
    ledger['recognition_scans']+=sum(len(c) for c in F)
    for k in range(max_k+1):
        for tup in itertools.combinations(range(1,n+1),k):
            ledger['candidate_tests']+=1
            ledger['literal_probes']+=sum(len(c) for c in F)
            if legal_backdoor(F,set(tup)):
                ledger['selected_backdoor_size']=k
                return tuple(tup)
    ledger['failed_policy_switches']+=1
    return None

def cube(F,T,b,ledger):
    ledger['cube_source_literal_probes']+=sum(len(c) for c in F)
    R=set(abs(l) for c in F for l in c)-set(T)
    active=[]
    for j,c in enumerate(F):
        if any(abs(l) in T and truth(l,b) for l in c):continue
        residual=norm(l for l in c if abs(l) in R)
        if len(residual)>2:raise AssertionError('bad certificate of backdoor')
        active.append((j,residual))
    return R,active

def derive_nogood(F,T,b,ledger):
    R,leaves=cube(F,T,b,ledger)
    reduced=[c for j,c in leaves]
    ledger['two_sat_clauses']+=len(reduced)
    sol=two_sat_witness(reduced,R,ledger)
    if sol is not None:
        w=dict(b);w.update(sol)
        assert sat(F,w)
        return {'sat':True,'witness':w,'nodes':[],'root':None,'nogood':None,'two_sat_size':len(reduced)}
    # Source-preserving resolution DAG: leaf is the full original clause.
    nodes=[{'source':j,'clause':list(c)} for j,c in enumerate(F)]
    active=[(j,c) for j,c in leaves]
    ledger['source_proof_nodes']+=len(F)
    for v in sorted(R):
        pos=[(i,c) for i,c in active if v in c]
        neg=[(i,c) for i,c in active if -v in c]
        keep=[(i,c) for i,c in active if v not in c and -v not in c]
        for i,ci in pos:
            for j,cj in neg:
                ledger['resolution_candidate_pairs']+=1
                rs=norm([l for l in ci if l!=v]+[l for l in cj if l!=-v])
                if any(-l in rs for l in rs):continue
                old=nodes[i]['clause']; other=nodes[j]['clause']
                full=norm([l for l in old if l!=v]+[l for l in other if l!=-v])
                if any(-l in full for l in full):raise AssertionError('lifted tautology')
                ix=len(nodes)
                nodes.append({'parents':[i,j],'pivot':v,'clause':list(full)})
                ledger['resolution_steps']+=1
                ledger['proof_literal_writes']+=len(full)
                keep.append((ix,rs))
        seen={}
        for i,c in keep:
            if c not in seen or len(nodes[i]['clause'])<len(nodes[seen[c]]['clause']):seen[c]=i
        active=[(i,c) for c,i in seen.items()]
    zeros=[i for i,c in active if len(c)==0]
    assert zeros,'DP resolution must produce empty residual for UNSAT 2CNF'
    root=min(zeros,key=lambda i:len(nodes[i]['clause']))
    D=tuple(nodes[root]['clause'])
    assert all(abs(l) in T and not truth(l,b) for l in D)
    ledger['learned_literal_writes']+=len(D)
    return {'sat':False,'witness':None,'nodes':nodes,'root':root,'nogood':list(D),'two_sat_size':len(reduced)}

def combine_refutations(F,T,answers,ledger):
    # Nodes from every rejected cube, plus complete resolution elimination over T.
    allnodes=[];active=[]
    for a in answers:
        if a['sat']:return None
        off=len(allnodes)
        for v in a['nodes']:
            w=dict(v)
            if 'parents' in w:w['parents']=[p+off for p in w['parents']]
            allnodes.append(w)
        i=a['root']+off
        active.append(i)
    for x in sorted(T):
        pos=[i for i in active if x in allnodes[i]['clause']]
        neg=[i for i in active if -x in allnodes[i]['clause']]
        keep=[i for i in active if x not in allnodes[i]['clause'] and -x not in allnodes[i]['clause']]
        for i in pos:
            for j in neg:
                out=norm([l for l in allnodes[i]['clause'] if l!=x]+[l for l in allnodes[j]['clause'] if l!=-x])
                if any(-l in out for l in out):continue
                u=len(allnodes);allnodes.append({'parents':[i,j],'pivot':x,'clause':list(out)})
                ledger['join_resolution_steps']+=1
                keep.append(u)
        active=list(dict.fromkeys(keep))
    roots=[i for i in active if not allnodes[i]['clause']]
    assert roots, 'complete rejected 2^k cubes imply UNSAT and resolution joins refute'
    return {'nodes':allnodes,'root':roots[0]}

def verify_dag(F,dag,require_empty=False):
    nodes=dag['nodes']
    for i,p in enumerate(nodes):
        c=norm(p['clause'])
        assert c==tuple(p['clause'])
        if 'source' in p:
            assert c==F[p['source']]
        else:
            u,v=p['parents'];x=p['pivot'];assert u<i and v<i
            a=nodes[u]['clause'];b=nodes[v]['clause']
            assert x in a and -x in b
            expect=norm([l for l in a if l!=x]+[l for l in b if l!=-x])
            assert expect==c and all(-l not in c for l in c)
    root=norm(nodes[dag['root']]['clause'])
    if require_empty: assert root==()
    return root

def dpll(F,n):
    ledger={'nodes':0,'literal_tests':0,'unit_loops':0}
    def rec(a):
        ledger['nodes']+=1
        a=dict(a)
        while True:
            reduced=[];units=[]
            for c in F:
                undec=[];fulfilled=False
                for l in c:
                    ledger['literal_tests']+=1
                    if abs(l) not in a:undec.append(l)
                    elif truth(l,a):fulfilled=True;break
                if fulfilled:continue
                if not undec:return None
                reduced.append(undec)
                if len(undec)==1:units.append(undec[0])
            if not reduced:
                for i in range(1,n+1):a.setdefault(i,0)
                return a
            if units:
                ledger['unit_loops']+=1
                l=units[0];a[abs(l)]=int(l>0)
                continue
            v=abs(reduced[0][0]);break
        for b in (0,1):
            w=rec(dict(a,**{} ) | {v:b})
            if w is not None:return w
        return None
    return rec({}),ledger

def extremes(F,n):
    local=[]
    for j,c in enumerate(F):
        S={abs(l):int(l>0) for l in c};U={x:1-v for x,v in S.items()}
        local.append({'j':j,'source_signed_occurrences':[{'variable':abs(l),'clause':j,'sign':int(l>0),'S':int(l>0),'invert_S_to_U':int(l<0),'U':int(l<0),'invert_U_to_S':int(l>0)} for l in c], 'S':S,'invert_S':U,'U':U,'invert_U':S})
    modes=[]
    for i in range(len(F)):
        for j in range(i+1,len(F)):
            row={'i':i,'j':j}
            for s in ('S','U'):
                for t in ('S','U'):
                    row[s+t]=all(k not in local[j][t] or v==local[j][t][k] for k,v in local[i][s].items())
            modes.append(row)
    zero={i:0 for i in range(1,n+1)};one={i:1 for i in range(1,n+1)}
    flips=[];curr=dict(zero)
    for i in range(1,n+1):
        before=counts(F,curr);curr[i]=1;after=counts(F,curr)
        flips.append({'variable':i,'before':before,'after':after,'clause_0_1_2_3_histogram':dict(Counter(after))})
    return {'local':local,'pair_modes':modes,'zero_counts':counts(F,zero),'one_counts':counts(F,one),'zero_sat':sat(F,zero),'one_sat':sat(F,one),'flips':flips}

def force(lit,p,q):return [norm((lit,u,v)) for u in (p,-p) for v in (q,-q)]
def rename(F,perm,flip):return [norm((1 if l>0 else -1)*perm[abs(l)]*(-1 if abs(l) in flip else 1) for l in c) for c in F]

def generate():
    satforce=force(1,2,3)
    unsatforce=satforce+force(-1,4,5)
    cases=[('pin_yes',satforce,3),('pin_no',unsatforce,5),
           ('pin_yes_negated',rename(satforce,{1:3,2:2,3:1},{1,3}),3),
           ('pin_no_renamed',rename(unsatforce,{1:5,2:4,3:3,4:2,5:1},{2,4}),5),
           ('krom_yes',[norm((1,2)),norm((1,-2))],2),
           ('krom_no',[norm((1,)),norm((-1,))],2),
           ('horn_yes',[norm((-1,2)),norm((-2,3)),norm((1,))],3),
           ('dual_horn_yes',[norm((1,-2)),norm((2,-3)),norm((-1,))],3),
           ('parity_yes',[norm((1,2,3)),norm((1,-2,-3)),norm((-1,2,-3)),norm((-1,-2,3))],3),
           ('parity_no',[norm((s1,s2,s3)) for s1 in (1,-1) for s2 in (2,-2) for s3 in (3,-3)],3),
           ('unique_middle_yes',[norm((1,2,3)),norm((-1,2,3)),norm((1,-2,3)),norm((1,2,-3)),norm((-1,-2,3)),norm((-1,2,-3)),norm((1,-2,-3))],3),
           ('highwidth_yes',[norm((1,2,3,4,5,6))],6),
           ('highwidth_no',[norm((1,)),norm((-1,)),norm((2,3,4,5,6))],6),
           ('dense_no',[norm((s1,s2,s3)) for s1 in (1,-1) for s2 in (2,-2) for s3 in (3,-3)],3)]
    return cases

def run():
    output={'run':'LSPV2_HITTING_BACKDOOR_FLIP_DAG276','date':'2026-10-31 09:38 PDT','seed':SEED,'cases':[]}
    tracemalloc.start();t0=time.perf_counter()
    for name,F,n in generate():
        ledger=Counter()
        dsol,baseline=dpll(F,n)
        T=find_backdoor(F,n,max_k=3,ledger=ledger)
        answers=[];refutation=None
        if T is not None:
            for bits in itertools.product((0,1),repeat=len(T)):
                b=dict(zip(T,bits));a=derive_nogood(F,set(T),b,ledger)
                answers.append(a)
                if a['sat']:break
            if all(not a['sat'] for a in answers):
                refutation=combine_refutations(F,T,answers,ledger)
                assert verify_dag(F,refutation,True)==()
            for a in answers:
                if not a['sat']:
                    root=verify_dag(F,{'nodes':a['nodes'],'root':a['root']})
                    assert root==tuple(a['nogood'])
        else:
            ledger['fallback_nodes']+=baseline['nodes']
        models=sat_models(F,n)
        assert bool(models)==bool(dsol)
        actual=any(a['sat'] for a in answers)
        if T is not None:assert actual==bool(models)
        if T is not None and not models:assert refutation is not None
        if T is not None and models:assert sat(F,next(a['witness'] for a in answers if a['sat']))
        learned=[tuple(a['nogood']) for a in answers if not a['sat']]
        child=F+learned
        assert bool(sat_models(child,n))==bool(models)
        child_repr=('p cnf %d %d\n'%(n,len(child)))+'\n'.join(' '.join(map(str,c))+' 0' for c in child)
        ledger['ordinary_child_output_bits']=8*len(child_repr)
        ledger['extreme_diagnostic_pair_records']=len(F)*(len(F)-1)//2
        ledger['extreme_diagnostic_flip_frames']=n+2
        rec={'selected_child_clauses':[list(c) for c in child],'selected_child_bits':8*len(child_repr),'name':name,'n':n,'source_clauses':[list(c) for c in F],'source_dimacs_bits':8*len(('p cnf %d %d\n'%(n,len(F)))+'\n'.join(' '.join(map(str,c))+' 0' for c in F)),'truth':bool(models),'models':len(models),'backdoor':T,'ledger':dict(ledger),'baseline':baseline,'cube_results':answers,'full_unsat_refutation':refutation,'extreme_controls':extremes(F,n)}
        output['cases'].append(rec)
    output['runtime_sec']=round(time.perf_counter()-t0,3)
    output['python_peak_bytes']=tracemalloc.get_traced_memory()[1]
    output['digest_source_excluding_digest']=hashlib.sha256(json.dumps(output,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return output

if __name__=='__main__':
    o=run()
    with open('/mnt/data/lspv2_276/raw276.json','w') as f:json.dump(o,f,sort_keys=True,indent=1)
    print(json.dumps({'cases':len(o['cases']),'sat':sum(x['truth'] for x in o['cases']),'unsat':sum(not x['truth'] for x in o['cases']),'backdoor_found':sum(x['backdoor'] is not None for x in o['cases']),'refutations':sum(x['full_unsat_refutation'] is not None for x in o['cases']),'proof_steps':sum(x['ledger'].get('resolution_steps',0)+x['ledger'].get('join_resolution_steps',0) for x in o['cases']),'baseline_nodes':sum(x['baseline']['nodes'] for x in o['cases']),'runtime_sec':o['runtime_sec'],'peak_bytes':o['python_peak_bytes'],'sha256':o['digest_source_excluding_digest'],'cases_detail':[(x['name'],x['truth'],x['backdoor'],x['ledger'].get('resolution_steps',0),x['ledger'].get('join_resolution_steps',0)) for x in o['cases']]},indent=2))