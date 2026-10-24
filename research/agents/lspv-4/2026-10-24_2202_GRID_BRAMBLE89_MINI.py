#!/usr/bin/env python3
"""GRID-BRAMBLE89: reproducible standard-library finite audit.
No random seeds or uncharged timing assertions are used. All source encodings
are fixed-width signed-literal words. Mathematical lower bounds are separate.
"""
import json
import itertools
import random
from collections import Counter
from math import ceil,log2

SEED = 202610242202
rng = random.Random(SEED)
checks = 0

def require(test, why):
    global checks
    checks += 1
    if not test: raise AssertionError(why)

def spec(r, label):
    assert r>=2 and label in ('SAT','UNSAT')
    grid=r*r
    edges=[]
    for i in range(r):
        for j in range(r):
            v=i*r+j+1
            if j+1<r: edges.append((v,v+1))
            if i+1<r: edges.append((v,v+r))
    es=len(edges)
    a=grid+es+1; b=a+1; c=a+2; y=a+3
    n=y
    clauses=[]
    eidx={}
    for idx,(u,v) in enumerate(edges):
        z=grid+idx+1
        eidx[tuple(sorted((u,v)))]=idx
        clauses.extend(((u,v,z),(u,v,-z)))
    clauses.extend(((a,1,y),(a,1,-y)))
    for mask in range(8):
        effective=1 if label=='SAT' and mask==0 else mask
        core=tuple((-v if (effective>>i)&1 else v) for i,v in enumerate((a,b,c)))
        clauses.append(core)
    h=(64*(n+len(clauses)+1)-1).bit_length()
    N=(4*len(clauses)+2)*h
    return dict(r=r,n=n,m=len(clauses),edges=edges,clauses=clauses,a=a,b=b,c=c,y=y,
                eidx=eidx,grid=grid,es=es,h=h,N=N,label=label)

def value_literal(lit, assign):
    bit=(assign>>(abs(lit)-1))&1
    return bit if lit>0 else 1-bit

def sat_clauses(clauses, assign):
    return all(any(value_literal(lit,assign) for lit in cl) for cl in clauses)

def row_dp_indsets(r):
    masks=[v for v in range(1<<r) if not (v & (v<<1))]
    old={v:1 for v in masks if not (v&1)}
    for row in range(1,r):
        old={v:sum(c for u,c in old.items() if not(u&v)) for v in masks}
    return sum(old.values())

def brute_indsets(r):
    es=spec(r,'SAT')['edges']; count=0
    for mask in range(1<<(r*r)):
        if mask&1: continue
        if all(not ((mask>>(u-1)&1) and (mask>>(v-1)&1)) for u,v in es):
            count+=1
    return count

def primal_stats(clauses,n):
    neigh=[set() for _ in range(n+1)];occ=Counter()
    for cl in clauses:
        vs=list(map(abs,cl))
        for v in vs:occ[v]+=1
        for u,v in itertools.combinations(vs,2):neigh[u].add(v);neigh[v].add(u)
    four=[]
    for u in range(1,n+1):
        for v in neigh[u]:
            if v<=u: continue
            common=neigh[u]&neigh[v]
            for w in common:
                for z in common:
                    if w<z and z in neigh[w]:four.append((u,v,w,z))
    return max(map(len,neigh)), max(occ.values()), four

def scoped_stream(F):
    r=F['r']; es=F['es']; clauses=F['clauses']; a,b,c,y=F['a'],F['b'],F['c'],F['y']
    events=[]
    def O(v):events.append(('OPEN',v))
    def C(v):events.append(('CLOSE',v))
    def K(idx):events.append(('CLAUSE',idx))
    for v in (a,b,c):O(v)
    for i in range(2*es+2,2*es+10):K(i)
    C(b);C(c)
    O(1);O(y);K(2*es);K(2*es+1);C(y);C(a)
    for i in range(r):
        if i==0:
            for j in range(1,r):O(j+1)
        for j in range(r-1):
            u=i*r+j+1;v=u+1
            z=F['grid']+F['eidx'][tuple(sorted((u,v)))]+1
            O(z);idx=F['eidx'][(u,v)];K(2*idx);K(2*idx+1);C(z)
        if i<r-1:
            for j in range(r):O((i+1)*r+j+1)
            for j in range(r):
                u=i*r+j+1;v=u+r
                z=F['grid']+F['eidx'][(u,v)]+1
                O(z);idx=F['eidx'][(u,v)];K(2*idx);K(2*idx+1);C(z)
            for j in range(r):C(i*r+j+1)
    for j in range(r):C((r-1)*r+j+1)
    return events

def check_scoped(F, events):
    opened=set();closed=set();live=set();seen=[];peak=0
    for ev,v in events:
        if ev=='OPEN':
            require(v not in opened,'duplicate opening');opened.add(v);live.add(v)
        elif ev=='CLOSE':
            require(v in live,'premature close');live.remove(v);closed.add(v)
        else:
            require(all(abs(l) in live for l in F['clauses'][v]),'clause outside scope')
            seen.append(v)
        peak=max(peak,len(live))
    require(len(opened)==F['n'] and opened==closed and not live,'not closed')
    require(sorted(seen)==list(range(F['m'])),'not exact same clause multiset')
    return peak

def scope_for_clause_order(F,order):
    first=[len(order)]*(F['n']+1)
    last=[-1]*(F['n']+1)
    for p,idx in enumerate(order):
        for l in F['clauses'][idx]:
            v=abs(l);first[v]=min(first[v],p);last[v]=max(last[v],p)
    return max(sum(first[v]<=p<=last[v] for v in range(1,F['n']+1)) for p in range(len(order)))

def explicit_witness(F):
    return (1<<F['grid'])-1

def serialize(F):
    h=F['h']
    records=[F['n'],F['m']]
    for cl in F['clauses']:
        records.extend((2*abs(l)+(l<0) for l in cl))
        records.append(0)
    require(len(records)==4*F['m']+2,'record count')
    return ''.join(format(int(v),f'0{h}b') for v in records)

def main():
    rows=[]
    for r in range(2,8):
        u=spec(r,'UNSAT');s=spec(r,'SAT')
        require((u['n'],u['m'],u['h'],u['N'])==(s['n'],s['m'],s['h'],s['N']),'same size')
        require(u['n']==3*r*r-2*r+4 and u['m']==4*r*(r-1)+10,'dimensions')
        require(all(len(set(map(abs,c)))==3 for c in u['clauses']),'proper 3CNF')
        require(serialize(u)!=serialize(s),'labels source fields differ')
        require(len(serialize(s))==s['N'],'encoded length')
        require(sat_clauses(s['clauses'],explicit_witness(s)),'valid SAT witness')
        for F in (u,s):
            deg,occ,four=primal_stats(F['clauses'],F['n'])
            require(deg<=8 and occ<=10 and not four,'degree/occurrence/clique max')
            ev=scoped_stream(F)
            peak=check_scoped(F,ev)
            require(r<=peak<=2*r+1,'width construction and lower bound')
            for _ in range(20):
                perm=list(range(F['m']));rng.shuffle(perm)
                require(scope_for_clause_order(F,perm)>=r,'grid cross width')
        ind=row_dp_indsets(r)
        if r<=4: require(ind==brute_indsets(r),'ind-set DP compared with brute force')
        predicted=ind*(1<<(u['es']+1))
        if r==2:
            brute=sum(sat_clauses(s['clauses'],ass) for ass in range(1<<s['n']))
            ub=sum(sat_clauses(u['clauses'],ass) for ass in range(1<<u['n']))
            require(brute==predicted and ub==0,'independent complete CNF model count')
        rows.append(dict(r=r,n=u['n'],m=u['m'],N=u['N'],grid_edges=u['es'],
                         width_constructed=check_scoped(u,scoped_stream(u)),
                         grid_width_lower=r,clique_max=3,occurrence_max=10,
                         independent_sets_not_containing_corner=ind,
                         SAT_models=predicted,UNSAT_models=0))
    result={'run':'GRID-BRAMBLE89','seed':SEED,'assertion_count':checks,'failures':0,
            'exact_basis':'proper 3CNF and fixed-width signed-literal words',
            'tests':'canonical witnesses, full brute count r=2, independent-set DP, exhaustive grid count r<=4, random clause orders, valid source-preserving scopes, primal clique/degree bound',
            'rows':rows,'limitations':'No physical FLMV time or bit-flip counts; asymptotic theorem is separate from these finite experiments.'}
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
