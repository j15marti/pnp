#!/usr/bin/env python3
"""Independent verification of GATE279 original-source and cofactor assertions.
No producer module imported. SAT/UNSAT checked with independent recursive solver.
"""
from collections import Counter,deque
from pathlib import Path
import json,hashlib,itertools
ROOT=Path(__file__).resolve().parent
raw=(ROOT/'raw279.json').read_bytes();payload=json.loads(raw)
summ=json.loads((ROOT/'summary279.json').read_text())
assert hashlib.sha256(raw).hexdigest()==summ['raw_sha256']
checks=Counter()

def ck(p,name):
    checks[name]+=1
    if not p:raise AssertionError(name)

def litval(l,a):return (l>0)==a[abs(l)]

def models(F,n):
    # Independent complete DPLL with UP but left-to-right first active branch.
    def run(a):
        while True:
            change=False
            all_true=True
            for C in F:
                if any(abs(l) in a and litval(l,a) for l in C):continue
                unset=[l for l in C if abs(l) not in a]
                if not unset:return None
                all_true=False
                if len(unset)==1:
                    l=unset[0];a[abs(l)]=l>0;change=True
            if all_true:
                for v in range(1,n+1):a.setdefault(v,False)
                return a
            if not change:break
        v=next(abs(l) for C in F for l in C if abs(l) not in a and not any(abs(z) in a and litval(z,a) for z in C))
        for b in (True,False):
            aa=dict(a);aa[v]=b
            x=run(aa)
            if x is not None:return x
        return None
    return run({})

def component_groups(F,n,x):
    E={i:set() for i in range(1,n+1) if i!=x}
    for C in F:
        w=[abs(l) for l in C if abs(l)!=x]
        for v in w:
            for z in w:
                if z!=v:E[v].add(z)
    groups=[];seen=set()
    for v in E:
        if v in seen:continue
        Q=deque([v]);S={v};seen.add(v)
        while Q:
            w=Q.popleft()
            for z in E[w]:
                if z not in seen:seen.add(z);S.add(z);Q.append(z)
        groups.append(S)
    return groups

def brute_modes(C,D,mode):
    vars_=sorted({abs(l) for l in C+D})
    for vals in itertools.product((False,True),repeat=len(vars_)):
        a=dict(zip(vars_,vals));t=sum(litval(l,a) for l in C);u=sum(litval(l,a) for l in D)
        if (t==(len(C) if mode[0]=='S' else 0)) and (u==(len(D) if mode[1]=='S' else 0)):return True
    return False

for rec in payload['records']:
    F=[tuple(c) for c in rec['source']];n=rec['n'];m=len(F)
    ck(m==rec['m'],'source m')
    ck(all(0<abs(l)<=n for C in F for l in C),'source variables')
    ck(all(len(set(map(abs,C)))==len(C) for C in F),'no occurrence duplicates')
    got=models(F,n)
    ck((got is not None)==(rec['label']=='SAT'),'independent source SAT/UNSAT')
    c=rec['audit']
    for label,b in [('zero',False),('one',True)]:
        expected=[sum((l>0)==b for l in C) for C in F]
        ck(c[label]['true_counts']==expected,'coherent endpoint t')
        ck(c[label]['SAT']==all(t>0 for t in expected),'coherent endpoint label')
        ck(c[label]['histogram']==[expected.count(i) for i in range(4)],'endpoint histogram')
    ck(all(c['zero']['true_counts'][j]+c['one']['true_counts'][j]==len(F[j]) for j in range(m)),'complement exact width')
    a={i:False for i in range(1,n+1)}
    for step in c['trail']:
        old=[sum(litval(l,a) for l in C) for C in F]
        v=step['flip'];a[v]=not a[v]
        now=[sum(litval(l,a) for l in C) for C in F]
        ck(step['h']==[now.count(t) for t in range(4)],'flip counts')
        ck(step['delta']==[now[j]-old[j] for j in range(m)],'flip delta')
    for e in c['extrema']:
        j=e['j']-1;C=F[j]
        S={str(abs(l)):int(l>0) for l in C};U={str(abs(l)):int(l<0) for l in C}
        ck(e['S']==S and e['U']==U and e['invert_S']==U and e['invert_U']==S,'signed S/U')
    for e in c['pairs']:
        j=e['j']-1;k=e['k']-1
        for mode in ('SS','SU','US','UU'):
            ck(e[mode]==brute_modes(F[j],F[k],mode),'brute pair extrema')
    if rec['selector']:
        x=rec['selector']['x'];groups=component_groups(F,n,x)
        ck(len(groups)>=2,'nontrivial pivot')
        ck({frozenset(G) for G in groups}=={frozenset(G) for G in rec['selector']['components']},'exact graph partition')
        evidence=rec['selector']['branch_proofs']
        ck({e['b'] for e in evidence}=={False,True},'both labels branch')
        outcome=False
        for e in evidence:
            b=e['b'];boundary=[C for C in F if all(abs(l)==x for l in C)]
            boundary_ok=all(any((l>0)==b for l in C) for C in boundary)
            ck(boundary_ok==e['boundary_ok'],'boundary clauses')
            seen=set();allgood=boundary_ok
            ck(len(e['components'])==len(groups),'all components included')
            for q in e['components']:
                group=set(q['component_variables']);ck(group in groups,'component membership')
                ck(group.isdisjoint(seen),'disjoint components');seen|=group
                idx=[j+1 for j,C in enumerate(F) if {abs(l) for l in C if abs(l)!=x} and {abs(l) for l in C if abs(l)!=x}.issubset(group) and not any(abs(l)==x and ((l>0)==b) for l in C)]
                ck(idx==q['source_clause_indices'],'exact source indices')
                exp=[tuple(l for l in F[j-1] if abs(l)!=x) for j in idx]
                ck(exp==[tuple(C) for C in q['clauses']],'exact cofactor')
                w=models(exp,n)
                ck((w is not None)==q['SAT'],'independent cofactor SAT/UNSAT')
                if w is None:allgood=False
                if q['witness'] is not None:
                    ww={int(k):bool(v) for k,v in q['witness'].items()}
                    ck(all(any(litval(l,ww) for l in C) for C in exp),'child witness')
            ck(seen==set(range(1,n+1))-{x},'full variable coverage')
            ck(allgood==e['allgood'],'AND over components')
            outcome|=allgood
        ck(outcome==(got is not None),'OR over both pin values')
    checks['source_formulas']+=1

out={'run':'GATE279','verified':True,'total_checks':sum(checks.values()),'check_counts':dict(checks),
     'raw_sha256':summ['raw_sha256'],'independent_solver':'complete unit-propagation DPLL with first-active variable; source and every cofactor'}
(ROOT/'verified279.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))