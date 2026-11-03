#!/usr/bin/env python3
"""Canonical bit-pigeonhole -> private-chain 3-CNF, with constructive deletion witnesses.
Never assert Braun's Res(oplus) lower bound for this transformed 3-CNF.
"""
import argparse, json, math, hashlib, time
from pathlib import Path

def bphp3(n):
    assert n >= 4 and n & (n-1) == 0
    ell=n.bit_length()-1; m=n+1
    original=[]; chains=[]; clauses=[]; next_v=m*ell+1
    def var(p,b): return 1+p*ell+b
    for i in range(m):
      for j in range(i+1,m):
        for z in range(n):
          lits=[]
          for p in (i,j):
            for b in range(ell):
              lits.append(var(p,b) if ((z>>b)&1)==0 else -var(p,b))
          assert len(lits)==2*ell
          cid=len(original)
          original.append({'pair':(i,j),'label':z,'literals':lits})
          internal=list(range(next_v,next_v+len(lits)-3))
          next_v+=len(internal)
          part=[[lits[0],lits[1],internal[0]]]
          for k in range(1,len(internal)):
            part.append([-internal[k-1],lits[k+1],internal[k]])
          part.append([-internal[-1],lits[-2],lits[-1]])
          assert len(part)==len(lits)-2
          start=len(clauses); clauses.extend(part)
          chains.append({'parent':cid,'start':start,'length':len(part),'aux':internal})
    return {'n_holes':n,'bits_per_pigeon':ell,'pigeons':m,
       'original_variable_count':m*ell,'variable_count':next_v-1,
       'original':original,'chains':chains,'clauses':clauses}

def eval_lit(lit, value):
    return (value[abs(lit)] == (lit>0))

def is_true_clause(clause,assignment):
    return any(eval_lit(lit,assignment) for lit in clause)

def witness_for_deleted(data, clause_index):
    n=data['n_holes']; ell=data['bits_per_pigeon']; m=n+1
    q=2*ell-2; parent=clause_index//q; part=clause_index%q
    src=data['original'][parent]; i,j=src['pair']; z=src['label']
    labels=[None]*m; labels[i]=z; labels[j]=z
    others=[x for x in range(n) if x!=z]
    for pigeon,k in zip([k for k in range(m) if k not in (i,j)],others):
        labels[pigeon]=k
    assert len(others)==m-2
    a=[False]*(data['variable_count']+1)
    for pigeon,x in enumerate(labels):
        for b in range(ell): a[1+pigeon*ell+b]=bool(x>>b&1)
    for idx,ch in enumerate(data['chains']):
        src_i=data['original'][idx]
        vals=[eval_lit(lit,a) for lit in src_i['literals']]
        if idx==parent:
            assert not any(vals)
            for t,aux in enumerate(ch['aux']): a[aux]=t<part
        else:
            assert any(vals)
            for t,aux in enumerate(ch['aux']): a[aux]=not any(vals[:t+2])
    return a

def dimacs(data):
    return 'c bit pigeonhole chain 3-CNF, all clauses width 3, UNSAT by pigeonhole\n'+f'p cnf {data["variable_count"]} {len(data["clauses"])}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in data['clauses'])

def audit(n, save, full):
    start=time.time(); d=bphp3(n); c=d['clauses']; m=len(c)
    q=2*d['bits_per_pigeon']-2
    assert len(d['original'])==n*math.comb(n+1,2)
    assert m==len(d['original'])*q
    assert all(len(x)==3 and len(set(map(abs,x)))==3 for x in c)
    txt=dimacs(d)
    if save: Path(save).write_text(txt)
    if full:
      for idx in range(m):
        a=witness_for_deleted(d,idx)
        falses=[j for j,cl in enumerate(c) if not is_true_clause(cl,a)]
        if falses!=[idx]: raise AssertionError((n,idx,falses[:5],len(falses)))
        for x in c[idx]: assert not eval_lit(x,a)
    return {'n_holes':n,'pigeons':n+1,'bits_per_pigeon':d['bits_per_pigeon'],
      'original_variables':d['original_variable_count'],'original_clauses':len(d['original']),
      'original_clause_width':2*d['bits_per_pigeon'],
      'converted_variables':d['variable_count'],'converted_clauses':m,'converted_width':3,
      'minimal_unsat':'SYMBOLIC_PROOF_FOR_ALL_n_POW2_ge4',
      'full_deletion_witnesses_checked':m if full else 0,
      'single_sign_flips_certified_sat':3*m,
      'mixed_Rmix341_source_arity_lower_bound':m-1,
      'ordinary_resoplus_lower_bound_transfers_to_3cnf':False,
      'sha256_dimacs':hashlib.sha256(txt.encode()).hexdigest(),
      'dimacs_bytes':len(txt.encode()),'elapsed_host_sec':round(time.time()-start,3)}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--sizes',nargs='+',type=int,default=[4,8,16])
    ap.add_argument('--out',default='.')
    ap.add_argument('--full-to',type=int,default=8)
    a=ap.parse_args()
    path=Path(a.out); path.mkdir(parents=True,exist_ok=True)
    results=[]
    for n in a.sizes:
        r=audit(n,str(path/f'bphp3_n{n}.cnf') if n<=a.full_to else None,n<=a.full_to)
        print('n=',n,'vars=',r['converted_variables'],'clauses=',r['converted_clauses'])
        results.append(r)
    (path/'results.json').write_text(json.dumps({
      'experiment':'BPHP-3CNF exact signed-instance and source-criticality atlas',
      'seed':None,'mode':'deterministic exhaustive deletion witnesses through n=8',
      'results':results},indent=2)+'\n')
