#!/usr/bin/env python3
"""Constructive meta-solver audit: XOR+2SAT compatibility and GF(3) certificate.
Run: python3 research/agents/meta-solver-theorem/2026-11-23_0935_fano_gf3.py
No dependencies beyond Python 3 standard library.
"""
import itertools, json, random, time
FANO = ((1,4,6),(2,3,6),(0,3,4),(2,4,5),(0,1,2),(1,3,5),(0,5,6))

def affine_mod_p(edges, n, p):
    """Exact consistency of incidence equations A*x=1 over GF(p)."""
    a=[]
    for edge in edges:
        row=[0]*(n+1)
        for v in edge:row[v]=(row[v]+1)%p
        row[-1]=1
        a.append(row)
    rank=0; operations=0
    for col in range(n):
        pivot=next((i for i in range(rank,len(a)) if a[i][col]),None)
        if pivot is None:continue
        a[rank],a[pivot]=a[pivot],a[rank]
        inverse=pow(a[rank][col],-1,p)
        a[rank]=[x*inverse%p for x in a[rank]]
        for r in range(len(a)):
            if r==rank or a[r][col]==0:continue
            fac=a[r][col];a[r]=[(x-fac*y)%p for x,y in zip(a[r],a[rank])]
            operations+=n+1
        rank+=1
    consistent=not any(all(x==0 for x in row[:-1]) and row[-1]!=0 for row in a)
    return dict(consistent=consistent,rank=rank,field_updates=operations)

def full_models(edges,n):
    exact=xor=at_most=0
    for bits in range(1<<n):
        weights=[sum((bits>>v)&1 for v in e) for e in edges]
        exact+=all(w==1 for w in weights)
        xor+=all(w%2==1 for w in weights)
        at_most+=all(w<=1 for w in weights)
    return dict(exact=exact,xor=xor,at_most=at_most)

def copied_system(edges):
    """Return A (disjoint local XOR rows), B (binary clauses), and copy map."""
    xor=[];two=[];by_orig={};copies={};next_v=1
    for ei,edge in enumerate(edges):
        row=[]
        for original in edge:
            v=next_v;next_v+=1;row.append(v)
            copies[(ei,original)]=v
            by_orig.setdefault(original,[]).append(v)
        xor.append((tuple(row),1))
        for a,b in itertools.combinations(row,2):two.append((-a,-b))
    for occur in by_orig.values():
        for v in occur[1:]:
            u=occur[0];two.extend(((-u,v),(u,-v)))
    return xor,two,copies

def eval_copied(xor,two,copies,original_bits):
    assignment={v:(original_bits>>orig)&1 for (_,orig),v in copies.items()}
    a=all((sum(assignment[v] for v in row)&1)==rhs for row,rhs in xor)
    b=all(any(assignment[abs(l)]==(l>0) for l in clause) for clause in two)
    return a,b

def check_family(edges,n):
    models=full_models(edges,n)
    m2=affine_mod_p(edges,n,2)
    m3=affine_mod_p(edges,n,3)
    xor,two,copies=copied_system(edges)
    assert all(len(row)==3 for row,_ in xor)
    assert len({v for row,_ in xor for v in row})==3*len(edges)
    assert all(len(c)==2 for c in two)
    # Every copied XOR subsystem is satisfiable: select one variable per row.
    # Every copied 2CNF subsystem is satisfiable: every copied variable is zero.
    sat_copy=0
    for bits in range(1<<n):
        a,b=eval_copied(xor,two,copies,bits)
        sat_copy+=a and b
    assert models['exact']==sat_copy
    assert (not m3['consistent']) <= (models['exact']==0)
    assert (not m2['consistent']) <= (models['exact']==0)
    return dict(n=n,edges=len(edges),copies=len(copies),xor_rows=len(xor),two_clauses=len(two),
                models=models,gf2=m2,gf3=m3,encoded_cnf_clauses=4*len(xor)+len(two))

def main():
    t=time.perf_counter()
    base=check_family(FANO,7)
    assert base['models']==dict(exact=0,xor=8,at_most=8),base
    assert base['gf2']['consistent'] and not base['gf3']['consistent']
    assert base['encoded_cnf_clauses']==77 and base['copies']==21
    neighbors=[check_family(FANO[:i]+FANO[i+1:],7) for i in range(7)]
    assert all(r['models']['exact']==1 and r['gf3']['consistent'] for r in neighbors)
    rng=random.Random(20261123)
    random_cases=[]
    for n in range(4,9):
        pool=list(itertools.combinations(range(n),3))
        for _ in range(20):
            es=tuple(rng.sample(pool,rng.randrange(1,min(len(pool),n+7)+1)))
            random_cases.append(check_family(es,n))
    assert len(random_cases)==100
    summary=dict(theorem='NP-complete union, with individually SAT XOR and 2SAT components',
                 fano=base,neighbors=[dict(dropped=i,models=r['models'],gf3=r['gf3']) for i,r in enumerate(neighbors)],
                 random_count=len(random_cases),
                 random_gf3_rejections=sum(not r['gf3']['consistent'] for r in random_cases),
                 random_unsat=sum(r['models']['exact']==0 for r in random_cases),
                 random_false_rejections=sum(not r['gf3']['consistent'] and r['models']['exact']>0 for r in random_cases),
                 seconds=round(time.perf_counter()-t,4))
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
