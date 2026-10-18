#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, math, random
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

SEED=20261018
random.seed(SEED)


def canon3(bits):
    b=tuple(bits); c=tuple(1-x for x in b)
    return min(b,c)

CLASSES=sorted({canon3(b) for b in itertools.product([0,1], repeat=3)})


def nae(vals): return len(set(vals))>1


def satisfying_assignments(edges,base,n):
    out=[]
    for a in itertools.product([0,1], repeat=n):
        ok=True
        for e,s in zip(edges,base):
            if not nae(tuple(a[v]^s[i] for i,v in enumerate(e))):
                ok=False; break
        if ok: out.append(a)
    return out


def gauge_orbit(edges,base,n):
    forms=[]
    for x in itertools.product([0,1], repeat=n):
        f=[]
        for ei,e in enumerate(edges):
            label=canon3(tuple(base[ei][i]^x[v] for i,v in enumerate(e)))
            f.append((ei,label))
        forms.append(frozenset(f))
    return forms


def inclusion_probability(forms,A):
    A=frozenset(A)
    return Fraction(sum(A.issubset(F) for F in forms),len(forms))


def candidate_subsets(family):
    out={frozenset()}
    for T in family:
        T=tuple(T)
        for r in range(1,len(T)+1):
            out.update(frozenset(c) for c in itertools.combinations(T,r))
    return out


def spread_ok(family,rho):
    family=[frozenset(T) for T in family]
    if not family: return True
    w=len(family[0])
    assert all(len(T)==w for T in family)
    L=len(family)
    for A in candidate_subsets(family):
        d=sum(A.issubset(T) for T in family)
        if d > L*rho**(-len(A))+1e-12:
            return False
    return True


def locate_core(H,rho):
    H=list(dict.fromkeys(map(frozenset,H)))
    core=frozenset(); current=H
    while True:
        residual=[T-core for T in current]
        if spread_ok(residual,rho):
            return core,current,residual
        L=len(residual); witness=None
        for A in sorted(candidate_subsets(residual),key=lambda s:(len(s),tuple(sorted(map(str,s))))):
            if not A: continue
            d=sum(A.issubset(R) for R in residual)
            if d > L*rho**(-len(A))+1e-12:
                witness=A; break
        assert witness is not None
        core=core|witness
        current=[T for T in current if core.issubset(T)]
        assert current


def peel_uniform(F,rho):
    rem=list(dict.fromkeys(map(frozenset,F))); out=[]
    while rem:
        C,selected,G=locate_core(rem,rho)
        out.append((C,G))
        selected=set(selected)
        rem=[T for T in rem if T not in selected]
    return out


def peel_mixed(F,rho):
    by=defaultdict(list)
    for T in F: by[len(T)].append(T)
    out=[]
    for w,H in by.items():
        out.extend((C,w,G) for C,G in peel_uniform(H,rho))
    return out


def dnf_probability(forms,F):
    return sum(any(T.issubset(X) for T in F) for X in forms)/len(forms)


def main():
    assertions=0; failures=[]; records={}

    fano=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
    plus=[(0,0,0)]*7
    minus=[(0,0,1)]*7
    sp=satisfying_assignments(fano,plus,7)
    sm=satisfying_assignments(fano,minus,7)
    assertions+=2
    if sp: failures.append(['fano_plus_not_unsat',len(sp)])
    if not sm: failures.append(['fano_minus_not_sat'])
    op=gauge_orbit(fano,plus,7); om=gauge_orbit(fano,minus,7)
    coords=[(e,c) for e in range(7) for c in CLASSES]
    checked={}
    for j in (1,2):
        mism=0; total=0
        for A in itertools.combinations(coords,j):
            total+=1; assertions+=1
            if inclusion_probability(op,A)!=inclusion_probability(om,A):
                mism+=1
        checked[j]={'patterns':total,'mismatches':mism}
        if mism: failures.append(['fano_low_order_mismatch',j,mism])
    first_cycle_mismatch=None
    for A in itertools.combinations(coords,3):
        p=inclusion_probability(op,A); m=inclusion_probability(om,A)
        if p!=m:
            first_cycle_mismatch={'pattern':repr(A),'plus':str(p),'minus':str(m)}
            break
    assertions+=1
    if first_cycle_mismatch is None: failures.append(['no_order3_mismatch'])
    records['fano']={'plus_solutions':len(sp),'minus_solutions':len(sm),'unique_plus_orbit':len(set(op)),'unique_minus_orbit':len(set(om)),'orbit_intersection':len(set(op)&set(om)),'low_order':checked,'first_order3_mismatch':first_cycle_mismatch}

    cyc=[(i,5+i,(i+1)%5) for i in range(5)]
    b0=[(0,0,0)]*5
    b1=[(0,0,0)]*5; b1[0]=(0,0,1)
    o0=gauge_orbit(cyc,b0,10); o1=gauge_orbit(cyc,b1,10)
    allcoords=[(e,c) for e in range(5) for c in CLASSES]
    terms=[]
    for w in (1,2):
        for T in itertools.combinations(allcoords,w):
            if len({x[0] for x in T})==w:
                terms.append(frozenset(T))
    rho=4.0; trials=[]
    for rep in range(200):
        F=set(random.sample(terms,random.randint(1,80)))
        clusters=peel_mixed(F,rho)
        reconstructed=[]
        for C,w,G in clusters:
            assertions+=1
            if not spread_ok(G,rho): failures.append(['nonspread',rep,repr(C),w])
            reconstructed.extend(C|R for R in G)
        assertions+=1
        if set(reconstructed)!=F or len(reconstructed)!=len(F): failures.append(['reconstruction',rep])
        for w in (1,2):
            L=sum(len(T)==w for T in F)
            if L:
                J=sum(cw==w for _,cw,_ in clusters)
                bound=rho**w*(1+math.log(L))
                assertions+=1
                if J>bound+1e-12: failures.append(['cluster_count',rep,w,J,bound])
        p0=dnf_probability(o0,F); p1=dnf_probability(o1,F)
        W=max(map(len,F)); J=len(clusters)
        factor=2*J*math.exp(4*W/rho)
        assertions+=2
        if p0>factor*p1+1e-12: failures.append(['transfer_01',rep,p0,p1,factor])
        if p1>factor*p0+1e-12: failures.append(['transfer_10',rep,p0,p1,factor])
        trials.append({'terms':len(F),'clusters':J,'p0':p0,'p1':p1,'ratio':max(p0/p1 if p1 else 1,p1/p0 if p0 else 1),'factor':factor})
    records['cycle_transfer']={'trials':len(trials),'max_terms':max(x['terms'] for x in trials),'max_clusters':max(x['clusters'] for x in trials),'max_observed_ratio':max(x['ratio'] for x in trials),'min_certified_factor':min(x['factor'] for x in trials),'max_certified_factor':max(x['factor'] for x in trials)}

    arithmetic=[]
    for v in (3,6,9,30,300):
        q=3*v; t=4*v; core_edges=3*v; leaf_edges=v
        assertions+=3
        if t!=4*q//3 or t!=core_edges+leaf_edges or 3*t!=4*q:
            failures.append(['density_arithmetic',v])
        arithmetic.append({'core_vertices':v,'slice_variables_q':q,'clauses_t':t,'core_clauses':core_edges,'transparent_leaf_clauses':leaf_edges})
    records['density_arithmetic']=arithmetic

    result={'status':'PASS' if not failures else 'FAIL','seed':SEED,'assertions':assertions,'failure_count':len(failures),'failures':failures,'records':records}
    out=Path(__file__).resolve().parents[1]/'results'/'nae_companion_audit.json'
    out.write_text(json.dumps(result,indent=2,sort_keys=True),encoding='utf-8')
    print(json.dumps({'status':result['status'],'assertions':assertions,'failures':len(failures),'fano_order3_mismatch':first_cycle_mismatch,'max_transfer_ratio':records['cycle_transfer']['max_observed_ratio'],'max_clusters':records['cycle_transfer']['max_clusters']},indent=2))
    if failures: raise SystemExit(1)

if __name__=='__main__': main()
