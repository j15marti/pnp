#!/usr/bin/env python3
"""LSPV-1/460: authenticated pigeon-choice Resolution proof for a Hall kernel.
Pure standard library; source IDs/clauses and every inference emitted, not R_mix341 byte grammar.
"""
import json, hashlib, math, sys, time, tracemalloc, itertools
from pathlib import Path

HERE=Path(__file__).resolve().parent

def canon(clause):
    assert all(type(l)==int and l!=0 for l in clause)
    if any(-l in clause for l in clause):
        raise ValueError('tautological clause')
    return tuple(sorted(set(clause),key=lambda l:(abs(l),l)))

def encode_dimacs(n, cs):
    return f'p cnf {n} {len(cs)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in cs)

def derive(neighbors, fixture):
    assert all(len(z)>=3 and len(set(z))==len(z) for z in neighbors)
    p=len(neighbors); h=len(set(itertools.chain.from_iterable(neighbors)))
    assert p>h, 'must be explicit Hall witness'
    edge={}; n=0
    for i,holes in enumerate(neighbors):
        for hole in holes:
            n+=1;edge[(i,hole)]=n
    source=[]; row_sources=[]; collision={}; pad_count=0; row_split_count=0
    for i,holes in enumerate(neighbors):
        literals=[edge[i,j] for j in holes]; d_i=len(holes)
        first=len(source);splitters=[]
        if d_i>3:
            splitters=list(range(n+1,n+d_i-2));n+=d_i-3
            source.append(canon([literals[0],literals[1],splitters[0]]))
            for q in range(1,len(splitters)):
                source.append(canon([-splitters[q-1],literals[q+1],splitters[q]]))
            source.append(canon([-splitters[-1],literals[-2],literals[-1]]))
            row_split_count+=d_i-3
        else:
            source.append(canon(literals))
        row_sources.append((list(range(first,len(source))),splitters))
    for i in range(p):
        for k in range(i+1,p):
            for j in sorted(set(neighbors[i]).intersection(neighbors[k])):
                n+=1;pad_count+=1
                x,y=edge[i,j],edge[k,j]
                source.append(canon([-x,-y,n]));a=len(source)-1
                source.append(canon([-x,-y,-n]));b=len(source)-1
                collision[(i,k,j)]=(a,b)
    steps=[]; clauses=list(source); memo={}; rec_calls=0
    def resolution(a,b,pivot):
        ca=set(clauses[a]);cb=set(clauses[b]);assert pivot in ca and -pivot in cb
        out=canon((ca|cb)-{pivot,-pivot})
        # A syntactically justified RES step; no weakening
        idx=len(clauses);clauses.append(out)
        steps.append({'id':idx,'a':a,'b':b,'pivot':pivot,'clause':list(out)})
        return idx
    # Restore each original long pigeon disjunction using only paid RES
    # on the private clause-chain splitters (d_i-3 steps per row).
    pigeons=[]
    for src_ids,splitters in row_sources:
        acc=src_ids[0]
        for src,z in zip(src_ids[1:],splitters):
            acc=resolution(acc,src,z)
        pigeons.append(acc)
    # derive one RES per original padded collision; exact positive padding id
    for (i,k,j),(a,b) in collision.items():
        z=next(x for x in source[a] if x>0 and abs(x) not in (edge[i,j],edge[k,j]))
        memo[(i,k,j)]=resolution(a,b,z)
    def walk(prefix):
        nonlocal rec_calls
        rec_calls+=1
        # prefix tuple pairs (pigeon_index, hole), each prefix variable positive
        seen={}
        for i,j in prefix:
            if j in seen:
                i0=seen[j]; a,b=min(i0,i),max(i0,i)
                return memo[(a,b,j)]
            seen[j]=i
        t=len(prefix)
        assert t<p, 'Hall deficit means no complete collision-free tuple'
        current=pigeons[t]
        for j in neighbors[t]:
            child=walk(prefix+((t,j),))
            lit=edge[t,j]
            if -lit not in clauses[child]:
                # A logically stronger, already derived negative clause
                # involving only earlier choices; no weakening or discharge.
                assert set(clauses[child])<=set(-edge[i,k] for i,k in prefix)
                return child
            assert lit in clauses[current]
            current=resolution(current,child,lit)
        assert set(clauses[current])<=set(-edge[i,j] for i,j in prefix)
        return current
    root=walk(())
    assert clauses[root]==(), (root,clauses[root])
    assert all(len(cl)==3 for cl in source)
    # Preserve the original source index namespace, but charge only the
    # union of actual inference nodes ancestral to the empty root.
    byid={st['id']:st for st in steps}; used=set()
    def mark(idx):
        if idx < len(source) or idx in used: return
        used.add(idx)
        st=byid[idx];mark(st['a']);mark(st['b'])
    mark(root)
    old_to_new={i:i for i in range(len(source))}
    kept=[]
    for old in sorted(used):
        st=byid[old]; idx=len(source)+len(kept)
        old_to_new[old]=idx
        kept.append({'id':idx,'a':old_to_new[st['a']],
                     'b':old_to_new[st['b']], 'pivot':st['pivot'], 'clause':st['clause']})
    root=old_to_new[root];steps=kept
    derived=len(steps)
    res_col=sum(1 for st in steps if st['a']<len(source) and st['b']<len(source) and st['pivot']>sum(len(x) for x in neighbors)+row_split_count)
    res_rows=sum(1 for st in steps if st['pivot']>sum(len(x) for x in neighbors) and st['pivot']<=sum(len(x) for x in neighbors)+row_split_count)
    topological_span=[0]*len(source)
    for st in steps:
        topological_span.append(1+max(topological_span[st['a']],topological_span[st['b']]))
    lines=encode_dimacs(n,source)
    out={'schema':'LSPV1_460_PROPER3_HALL_RES_V1','fixture':fixture,
      'pigeons':p,'holes':h,'neighbors':neighbors,'vars':n,'original_clauses':[list(z) for z in source],
      'original_dimacs_sha256':hashlib.sha256(lines.encode()).hexdigest(),
      'paid_steps':steps,'root':root,'paid_nodes':derived,
      'padding_eliminations':res_col,'pigeon_row_eliminations':res_rows,'branch_resolution':derived-res_col-res_rows,
      'source_count':len(source),'recursion_calls':rec_calls,'span':topological_span[root],
      'formula_parameters':{'edges':len(edge),'padding_variables':pad_count,'row_splitters':row_split_count},
      'theorem_upper_bound':p*(max(map(len,neighbors))-3)+max(map(len,neighbors))*math.comb(p,2)+max(map(len,neighbors))*(max(map(len,neighbors))**p-1)//(max(map(len,neighbors))-1)}
    assert derived<=out['theorem_upper_bound']
    (HERE/f'{fixture}.cnf').write_text(lines)
    (HERE/f'{fixture}.json').write_text(json.dumps(out,indent=2)+'\n')
    return out

def satisfiable(neighbors):
    choices=(dict.fromkeys(neighbors[0]),)
    return any(len(set(t))==len(t) for t in itertools.product(*neighbors))

def main():
    tracemalloc.start();t0=time.perf_counter()
    configs=[('hall5_4',[[0,1,2],[0,1,3],[0,2,3],[1,2,3],[0,1,2]]),
             ('four_on_three',[[0,1,2] for _ in range(4)]),
             ('hall6_5',[[0,1,2],[0,1,3],[0,2,4],[1,3,4],[2,3,4],[0,1,2]]),
             ('degree4_hall6_5',[[0,1,2,3],[0,1,2,4],[0,1,3,4],[0,2,3,4],[1,2,3,4],[0,1,2,3]])]
    summaries=[]
    for name,nei in configs:
        assert not satisfiable(nei)
        r=derive(nei,name)
        summaries.append({k:r[k] for k in ['fixture','pigeons','holes','vars','source_count','paid_nodes','padding_eliminations','pigeon_row_eliminations','branch_resolution','recursion_calls','span','original_dimacs_sha256','theorem_upper_bound']})
    assert satisfiable([[0,1,2],[0,1,3],[0,2,3],[1,2,3]])
    elapsed=time.perf_counter()-t0;peak=tracemalloc.get_traced_memory()[1]
    summary={'schema':'LSPV1_460_RESULTS_V1','fixtures':summaries,'sat_control':'PASS (4 pigeons inject into 4 holes)',
            'python_elapsed_seconds':elapsed,'python_peak_tracemalloc_bytes':peak,
            'status':'COMPUTATIONAL certificates for PROVED/RESTRICTED general theorem; historical checker not run'}
    (HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
