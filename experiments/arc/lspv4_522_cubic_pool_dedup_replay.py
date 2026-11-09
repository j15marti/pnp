"""LSPV-4/522 independent finite verification of canonical mod-2 cubic Magnus pools.
Requires Python 3 standard library only. Not an R_mix341/FLMV checker.
"""
import itertools, json

def graphs():
    k4=list(itertools.combinations(range(4),2))
    prism=[(i,(i+1)%3) for i in range(3)]+[(i+3,(i+1)%3+3) for i in range(3)]+[(i,i+3) for i in range(3)]
    cube=[(x,x^(1<<j)) for x in range(8) for j in range(3) if x<(x^(1<<j))]
    pet=[(i,(i+1)%5) for i in range(5)]+[(i,5+i) for i in range(5)]+[(5+i,5+(i+2)%5) for i in range(5)]
    return [('K4',4,k4),('prism',6,prism),('cube',8,cube),('petersen',10,pet)]

def formula(h,edges,odd):
    inc=[[] for _ in range(h)]
    for j,(u,v) in enumerate(edges,1):
        inc[u].append(j); inc[v].append(j)
    assert all(len(a)==3 for a in inc)
    out=[]
    for v,ids in enumerate(inc):
        ids=sorted(ids)
        for signs in itertools.product([0,1],repeat=3):
            if (sum(signs)%2)!=(1 if odd and v==0 else 0):
                out.append(tuple(zip(ids,signs)))
    return out

def jet(clause):
    a,b,c=[2*id+sign for id,sign in clause]
    return {(a,b,c),(a,c,b),(b,c,a),(c,b,a)}

def pool(rows):
    p=set()
    for r in rows:
        p.symmetric_difference_update(jet(r))
    return p

def recover(p):
    return {tuple((g//2,g%2) for g in w) for w in p
            if w[0]//2 < w[1]//2 < w[2]//2}

def count_sat(n,rows):
    return sum(all(any(((x>>(k-1))&1)!=s for k,s in r) for r in rows)
               for x in range(1<<n))

out=[]
for name,h,edges in graphs():
    for odd in (False,True):
        rows=formula(h,edges,odd)
        assert len(rows)==4*h
        assert len(pool(rows))==16*h
        assert recover(pool(rows))==set(rows)
        assert pool(rows*2)==set()
        assert pool(rows*2+[rows[0]])==jet(rows[0])
        dedup=list(dict.fromkeys(rows*2))
        assert dedup==rows
        models=count_sat(len(edges),rows)
        assert models==(0 if odd else 2**(len(edges)-h+1))
        assert count_sat(len(edges),dedup)==models
        out.append(dict(graph=name,odd=odd,variables=len(edges),
                        clauses=len(rows),models=models,pool_size=len(pool(rows))))
n=5
universe=[tuple(zip(ids,sg)) for ids in itertools.combinations(range(1,n+1),3)
          for sg in itertools.product((0,1),repeat=3)]
assert len(universe)==80
assert len({tuple(sorted(jet(r))) for r in universe})==80
for i,a in enumerate(universe):
    assert recover(pool([a]))=={a}
    assert recover(pool([a,a]))==set()
    for b in universe[i+1:]:
        assert recover(pool([a,b]))=={a,b}
result=dict(status='PASS',graph_controls=out,canonical_clause_universe=len(universe),
            distinct_clause_pair_checks=len(universe)*(len(universe)-1)//2,
            duplicate_annihilation_checks=len(universe),
            scope='Formal clause-word coefficients only; not link invariants or SAT-machine bounds')
print(json.dumps(result,indent=2))
