#!/usr/bin/env python3
"""ARC228 verified full-shared-interface tree composition.
Requires the sibling 2026-10-29_1200_ARC228_fixed_codimension_solver.py.
No uncharged decomposition discovery; supplied tree and sources are validated.
"""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import product
from random import Random
import importlib.util,json,sys

helper=Path(__file__).with_name('2026-10-29_1200_ARC228_fixed_codimension_solver.py')
spec=importlib.util.spec_from_file_location('arc228fixed',helper)
H=importlib.util.module_from_spec(spec);sys.modules[spec.name]=H;spec.loader.exec_module(H)

def tree_solver(modules,edges,root=0,stats=None):
    """Each module has id, vars, clauses (length<=2) and eqs (variable support,rhs).
    The supplied tree must satisfy exact source ownership, scope and running
    intersection. Each source occurrence belongs to exactly one input module.
    """
    if stats is None:stats=Counter()
    byid={m['id']:m for m in modules}
    if len(byid)!=len(modules) or root not in byid:raise ValueError('duplicate/missing module')
    ids=set(byid)
    if len(edges)!=len(ids)-1:raise ValueError('not a tree')
    adj={t:set() for t in ids}
    for u,v in edges:
        if u not in ids or v not in ids or u==v:raise ValueError('invalid edge')
        adj[u].add(v);adj[v].add(u)
    seen={root};queue=[root]
    for u in queue:
        for v in adj[u]:
            if v not in seen:seen.add(v);queue.append(v)
    if seen!=ids:raise ValueError('disconnected tree')
    scopes={};occ=defaultdict(set)
    for m in modules:
        t=m['id'];w=set(m['vars'])
        if len(w)!=len(m['vars']):raise ValueError('duplicate declared var')
        for c in m['clauses']:
            if not c or len(c)>2 or any(abs(l) not in w or l==0 for l in c):
                raise ValueError('bad source 2CNF')
        for support,rhs in m['eqs']:
            if rhs not in (0,1) or any(v not in w for v in support):
                raise ValueError('bad source affine support')
        scopes[t]=w
        for x in w:occ[x].add(t)
    for x,nodes in occ.items():
        start=next(iter(nodes));seen={start};queue=[start]
        for u in queue:
            for v in adj[u]&nodes:
                if v not in seen:seen.add(v);queue.append(v)
        if seen!=nodes:raise ValueError('broken running intersection')
    B={t:tuple(sorted(v for v in scopes[t] if len(occ[v])>1)) for t in ids}
    stats['module_count']=len(ids)
    stats['max_full_boundary']=max((len(x) for x in B.values()),default=0)
    parent={root:None};order=[root]
    for u in order:
        for v in sorted(adj[u]):
            if v not in parent:parent[v]=u;order.append(v)
    child={t:[v for v in adj[t] if parent.get(v)==t] for t in ids}
    table={};proj={};witness={}
    for t in reversed(order):
        m=byid[t];fullB=B[t]
        sep=tuple(sorted(scopes[t]&scopes[parent[t]])) if parent[t] is not None else ()
        table[t]={};proj[t]={};witness[t]={}
        for bits in product((0,1),repeat=len(fullB)):
            stats['full_rows']+=1
            a=dict(zip(fullB,bits))
            if any(tuple(a[v] for v in sorted(scopes[t]&scopes[c]))
                   not in proj[c] for c in child[t]):
                stats['child_failures']+=1
                table[t][bits]=False
                continue
            # Physical restriction before the fixed-e local solver avoids e+b.
            rest=tuple(v for v in sorted(scopes[t]) if v not in a)
            inv={v:i for i,v in enumerate(rest)}
            C=[];E=[];bad=False
            for clause in m['clauses']:
                if any(abs(l) in a and a[abs(l)]==int(l>0) for l in clause):
                    continue
                row=tuple((inv[abs(l)]+1)*(1 if l>0 else -1)
                          for l in clause if abs(l) not in a)
                if not row:bad=True;break
                C.append(row)
            if not bad:
                for support,rhs in m['eqs']:
                    bb=rhs
                    for v in support:
                        if v in a:bb^=a[v]
                    mm=sum(1<<inv[v] for v in support if v not in a)
                    if not mm:
                        if bb:bad=True;break
                    else:E.append((mm,bb))
            if bad:
                stats['pin_failures']+=1;table[t][bits]=False;continue
            localstats=Counter()
            w=H.fixed_codim_solver(len(rest),C,E,localstats)
            stats['local_calls']+=1;stats['local_nodes']+=localstats['nodes']
            stats['failed_plucks']+=localstats['plucks_tried']
            if w is None:
                stats['local_failures']+=1;table[t][bits]=False;continue
            local={**a,**{v:w[inv[v]] for v in rest}}
            assert all(any(local[abs(l)]==int(l>0) for l in cl)
                       for cl in m['clauses'])
            assert all(sum(local[v] for v in support)%2==rhs
                       for support,rhs in m['eqs'])
            table[t][bits]=True;witness[t][bits]=local
            key=tuple(a[v] for v in sep)
            if key not in proj[t]:proj[t][key]=bits
        stats['table_entries']+=len(table[t])
        stats['projected_entries']+=len(proj[t])
    if () not in proj[root]:return 'UNSAT',None,dict(stats)
    out={}
    def glue(t,bits):
        for x,v in witness[t][bits].items():
            if x in out and out[x]!=v:raise AssertionError('gluing disagreement')
            out[x]=v
        for c in child[t]:
            sep=tuple(sorted(scopes[c]&scopes[t]))
            glue(c,proj[c][tuple(out[v] for v in sep)])
    glue(root,proj[root][()])
    assert all(all(any(out[abs(l)]==int(l>0) for l in cl)
                   for cl in m['clauses']) and
               all(sum(out[v] for v in support)%2==rhs
                   for support,rhs in m['eqs']) for m in modules)
    stats['verified_output_variables']=len(out)
    return 'SAT',out,dict(stats)

def chain(k,target,charge):
    modules=[]
    for i in range(k):
        x,y,z=i+1,i+2,k+2+i
        C=[(-z,)]
        if i==0:C.append((-x,))
        if i==k-1:C.append((y if target else -y,))
        modules.append({'id':i,'vars':[x,y,z],
                        'clauses':C,'eqs':[((x,y,z),charge[i])]})
    return modules,[(i,i+1) for i in range(k-1)]

def main():
    rng=Random(91128);count=Counter();mx=0
    for k in (1,2,3,4,5,6,8,10,20,50,100):
        for target_mismatch in (0,1):
            charges=[rng.randrange(2) for j in range(k)]
            target=(sum(charges)%2)^target_mismatch
            M,E=chain(k,target,charges)
            ans,model,stats=tree_solver(M,E)
            expected='SAT' if not target_mismatch else 'UNSAT'
            assert ans==expected,(k,target_mismatch,ans)
            count[ans]+=1;mx=max(mx,stats['max_full_boundary'])
    # This source looks connected as a tree, but variable 999 appears at
    # both endpoints and not the middle; it must be rejected.
    M,E=chain(3,0,[0]*3)
    for i in (0,2):M[i]['vars'].append(999)
    try:tree_solver(M,E)
    except ValueError:count['running_intersection_rejected']+=1
    # Empty separator has valid empty tuple, not false.
    singleton=[
      {'id':0,'vars':[1],'clauses':[(1,)],'eqs':[]},
      {'id':1,'vars':[2],'clauses':[(2,)],'eqs':[]}]
    ans,model,stats=tree_solver(singleton,[(0,1)])
    assert ans=='SAT' and model[1]==1 and model[2]==1
    count['empty_separator_accepted']+=1
    print(json.dumps({'counts':dict(count),'max_full_boundary':mx,
                      'max_global_rank':100,'scientific_status':'RESTRICTED',
                      'P_versus_NP':'OPEN'},indent=2))
if __name__=='__main__':main()
