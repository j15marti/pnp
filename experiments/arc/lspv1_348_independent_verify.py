#!/usr/bin/env python3
"""Independent checker for LSPV1 348. No import from the producer."""
import itertools,json,copy,sys
F=((-3,1,4),(-1,2),(1,3),(-4,-3),(-2,-1,3),(-2,4))
def normal(f):
    return tuple(sorted(tuple(sorted(cl,key=lambda x:(abs(x),x))) for cl in f))
def permute(f,p,s):
    return tuple(tuple((1 if v>0 else -1)*s[abs(v)-1]*p[abs(v)-1] for v in cl) for cl in f)
def models(f):
    return sum(all(any((a[abs(z)-1] == (z>0)) for z in c) for c in f)
      for a in itertools.product((False,True),repeat=4))
def res(left,right,v):
    if v in left and -v in right:l=[x for x in left if x!=v];r=[x for x in right if x!=-v]
    elif -v in left and v in right:l=[x for x in left if x!=-v];r=[x for x in right if x!=v]
    else:raise AssertionError('bad pivot')
    c=set(l+r)
    assert not any(-z in c for z in c)
    return tuple(sorted(c,key=lambda z:(abs(z),z)))
def check_proof(f,p,s):
    c=permute(f,p,s);tr=lambda i:p[i-1]*s[i-1]
    d0=res(c[0],c[3],tr(4));d1=res(c[2],d0,tr(3))
    d2=res(c[3],c[5],tr(4));d3=res(c[4],d2,tr(3))
    d4=res(c[1],d3,tr(2));d5=res(d1,d4,tr(1))
    assert tuple(map(len,(d0,d1,d2,d3,d4,d5)))==(2,1,2,2,1,0)
def verify(data):
    assert data['original']==[list(c) for c in F]
    group=list(itertools.product(itertools.permutations((1,2,3,4)), itertools.product((-1,1),repeat=4)))
    orbits={normal(permute(F,p,s)) for p,s in group}
    assert len(group)==data['group_order']==384 and len(orbits)==data['orbit_size']==192
    for p,s in group:check_proof(F,p,s)
    checks={'six_step_proof_replays':384,'source_clause_deletion':0,'sign_flip':0}
    neighbors=set()
    for f in orbits:
        assert models(f)==0
        delete=sorted(models(f[:i]+f[i+1:]) for i in range(len(f)))
        assert delete==data['deletion_model_counts']==[1,1,1,3,3,3]
        checks['source_clause_deletion']+=len(f)
        for i,c in enumerate(f):
            for j in range(len(c)):
                other=[list(row) for row in f];other[i][j]*=-1
                assert models(other)>0
                checks['sign_flip']+=1
                neighbors.add(normal(other))
    assert len(neighbors)==data['distinct_sat_neighbor_formulas']==2688
    cls={}
    for i,c in enumerate(F):
        for j in range(len(c)):
            f=[list(row) for row in F];f[i][j]*=-1
            orb={normal(permute(f,p,s)) for p,s in group}
            assert len(orb)==384
            cls.setdefault(min(orb),[]).append((i+1,j+1))
    assert len(cls)==data['distinct_sat_neighbor_orbits']==7
    assert sorted(tuple(sorted(v)) for v in cls.values())==sorted(tuple(sorted(tuple(q) for q in cl)) for cl in data['neighbor_orbit_classes'])
    assert checks['source_clause_deletion']==data['source_deletion_checks']==1152
    assert checks['sign_flip']==data['one_occurrence_sign_flips']==2688
    assert data['mixed_W_interval']==[5,6]
    return checks
def parse_clauses(data):
    if not isinstance(data,list) or len(data)!=6:raise ValueError('invalid clause list')
    for c in data:
      if not isinstance(c,list) or len(c)<1:raise ValueError('bad clause')
      if len(set(c))!=len(c) or any(type(x)!=int or x==0 or abs(x)>4 for x in c):raise ValueError('invalid literal')
      if any(-x in c for x in c):raise ValueError('tautological')
    return data
if __name__=='__main__':
    if len(sys.argv)!=2:sys.exit('usage: independent_verify.py raw.json')
    data=json.load(open(sys.argv[1],encoding='utf-8'))
    checks=verify(data)
    corrupt=0
    for field in ('orbit_size','group_order','distinct_sat_neighbor_orbits','source_deletion_checks'):
        d=copy.deepcopy(data);d[field]+=1
        try:verify(d)
        except AssertionError:corrupt+=1
        else:raise AssertionError('tampered result accepted')
    malformed=0
    for bad in ([],[[]]*6,[[0]]*6,[[5]]*6,[[1,1]]*6,[[1,-1]]*6):
        try:parse_clauses(bad)
        except ValueError:malformed+=1
        else:raise AssertionError('bad input accepted')
    print(json.dumps({'status':'PASS','independent':True,'checks':checks,'corrupted_summary_rejected':corrupt,'malformed_clause_lists_rejected':malformed},sort_keys=True))
