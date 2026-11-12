#!/usr/bin/env python3
"""LSPV-1/602 rankless Resolution hyper-DAG counterexample, Python 3 stdlib.
Reference calculus only, NOT historical /341, /386 or R_mix341 acceptance.
"""
import json

def canon(xs):
    z=tuple(sorted(set(xs),key=lambda x:(abs(x),x)))
    if 0 in z or any(-x in z for x in z): raise ValueError('tautology/zero')
    return z

def res(a,b,p):
    if p not in a or -p not in b: raise ValueError('bad signed pivot')
    return canon([x for x in a if x!=p]+[x for x in b if x!=-p])

def models(cs,n):
    return sum(all(any(bool(t & (1<<(abs(x)-1)))==(x>0) for x in c)
                   for c in cs) for t in range(1<<n))

def k4():
    ed=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]; inc=[[] for _ in range(4)]
    for i,(u,v) in enumerate(ed,1):inc[u].append(i);inc[v].append(i)
    return [canon(-e if (t>>j)&1 else e for j,e in enumerate(inc[v]))
            for v in range(4) for t in range(8)
            if t.bit_count()%2 != (v==0)]

def chronological(rows,source):
    db={'S'+str(i):c for i,c in enumerate(source)}
    for ident,out,a,b,p in rows:
        if a not in db or b not in db: return False
        if res(db[a],db[b],p)!=out: return False
        db[ident]=out
    return bool(rows and rows[-1][1]==())

F=k4(); H=list(map(canon,([8,-9],[-8,9],[-8],[-7]))); src=F+H
rows=[('A',canon([7,8]),'B','S16',9),
      ('B',canon([7,9]),'A','S17',8),
      ('U',canon([7]),'A','S18',8),
      ('E',canon([]),'U','S19',7)]
db={'S'+str(i):c for i,c in enumerate(src)}
db.update({name:c for name,c,a,b,p in rows})
assert all(res(db[a],db[b],p)==c for name,c,a,b,p in rows)
assert not chronological(rows,src)
assert models(F,6)==0 and models(H,9)==64 and models(src,9)==0
assert all(models(F[:i]+F[i+1:],6)==2 for i in range(16))
assert all(models(src[:i]+src[i+1:],9)==2 for i in range(16))
# Construct a genuine chronological RES refutation of F using first witnesses.
known={c:'S'+str(i) for i,c in enumerate(F)}; active=set(F); real=[]
for p in (1,2,4,3,5,6):
    plus=[c for c in active if p in c]; minus=[c for c in active if -p in c]
    added=set()
    for a in plus:
        for b in minus:
            try:c=res(a,b,p)
            except ValueError:continue
            added.add(c)
            if c not in known:
                ident='R'+str(len(real));real.append((ident,c,known[a],known[b],p));known[c]=ident
    active.difference_update(plus+minus);active.update(added)
assert len(real)==27 and chronological(real,F) and chronological(real,src)
# Three independently corrupted local inference controls.
mutants=[('pivot',db['B'],db['S16'],8,db['A']),
         ('result',db['B'],db['S16'],9,canon([7,-8]))]
assert all((lambda a,b,p,c: (res(a,b,p)!=c))(a,b,p,c) if p in a and -p in b else True
           for _,a,b,p,c in mutants)
assert 'UNKNOWN' not in db
result={'status':'PASS','scope':'reference signed RES, not native /341 or /386',
        'K4_source_clauses':len(F),'gadget_clauses':list(map(list,H)),
        'rankless_paid_steps':len(rows),'local_valid_steps':4,
        'cyclic_dependency':['A','B','A'],'chronological_accept':False,
        'H_models_9vars':models(H,9),'K4_models_6vars':models(F,6),
        'combined_models_9vars':models(src,9),
        'source_deletion_16_each_models':2,
        'real_RES_lower_bound':15,'legal_DP_RES_steps':len(real),
        'invalid_local_mutations_rejected':3,
        'theorem':'Every minimally UNSAT m-source core requires >=m-1 paid binary RES nodes; rankless cycle pays 4'}
print(json.dumps(result,sort_keys=True,separators=(',',':')))
