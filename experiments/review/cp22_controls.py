#!/usr/bin/env python3
"""Small cross-family CP22LIFT1 proof controls. Python 3.10+, no dependencies."""
from __future__ import annotations
import collections, hashlib, itertools, json, time
from pathlib import Path
import cp22_audit as cp

def properize(clauses):
    n=max(abs(l) for c in clauses for l in c); out=[]
    for c in clauses:
        if len(c)==3: out.append(tuple(c))
        elif len(c)==2:
            n+=1; out.extend([(*c,n),(*c,-n)])
        elif len(c)==1:
            a,b=n+1,n+2;n+=2
            out.extend([(c[0],sa*a,sb*b) for sa in (1,-1) for sb in (1,-1)])
        else: raise ValueError('Only nonempty clauses of width <=3 are supported')
    return out

def resolution_cp(F,deadline):
    cs=[frozenset(c) for c in F]; seen={c:i for i,c in enumerate(cs)}
    deriv=[('ax',i) for i in range(len(cs))]; ix=collections.defaultdict(list)
    for i,c in enumerate(cs):
        for l in c: ix[l].append(i)
    q=0; empty=None
    while q<len(cs) and empty is None:
        if time.perf_counter()>deadline: raise TimeoutError('Split the control batch')
        A=cs[q]
        for l in sorted(A):
            for j in tuple(ix[-l]):
                R=(A-{l})|(cs[j]-{-l})
                if any(-x in R for x in R) or R in seen:continue
                k=len(cs);seen[R]=k;cs.append(R);deriv.append(('res',q,j,l))
                for x in R:ix[x].append(k)
                if not R:empty=k;break
            if empty is not None:break
        q+=1
    assert empty is not None,'Expected UNSAT control'
    need=set()
    def visit(j):
        if j in need:return
        need.add(j)
        if deriv[j][0]=='res':visit(deriv[j][1]);visit(deriv[j][2])
    visit(empty);P=cp.Proof(F);ids={}
    for i in sorted(need):
        op=deriv[i]
        if op[0]=='ax':ids[i]=P.ax(op[1]);continue
        _,j,k,l=op;z=P.sum(ids[j],ids[k])
        for t in sorted((cs[j]-{l})^(cs[k]-{-l})):z=P.sum(z,P.bound(t))
        z=P.div(z,2);assert P.rows[z]==cp.clause(cs[i]);ids[i]=z
    cp.check(P.data());return P

def tseitin_k4():
    E=list(itertools.combinations(range(4),2)); F=[]
    for u in range(4):
        inc=[i+1 for i,e in enumerate(E) if u in e];charge=int(u==0)
        for vals in itertools.product((0,1),repeat=3):
            if sum(vals)%2!=charge:F.append(tuple(v if b==0 else -v for v,b in zip(inc,vals)))
    return F

def main():
    start=time.perf_counter(); deadline=start+25; template=cp.resolution_ports()
    horn=properize([(1,),(-1,2),(-2,)])
    krom=properize([(1,2),(1,-2),(-1,2),(-1,-2)])
    cases={'properized_Horn':horn,'properized_2SAT':krom,
           'affine_K4_odd_Tseitin':tseitin_k4(),
           'all_eight_proper_three_clauses':list(itertools.product((1,-1),(2,-2),(3,-3))),
           'independent_product':krom+[(7,8,9)],
           'duplicated_source_occurrences':horn+horn,
           'clause_literal_order':list(reversed([tuple(reversed(c)) for c in horn]))}
    rows=[]
    for seed,(name,F) in enumerate(cases.items(),2026101300):
        src=resolution_cp(F,deadline);T=cp.compile22(F);P=cp.transport(T,src,template)
        a=cp.check(P.data());b=cp.check(cp.scramble(P.data(),seed))
        c=cp.check(cp.project_back(P.data(),T,F).data())
        rows.append({'name':name,'source_clauses':len(F),'target_variables':72*len(F),
                     'canonical_lines':a['lines'],'scrambled_lines':b['lines'],
                     'projected_lines':c['lines'],'source_lines':len(src.rows)})
    out={'run':'CP22LIFT1','scope':'COMPUTATIONAL proof-transport controls',
         'cases':rows,'zero_failures':True,'seconds':time.perf_counter()-start,
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'core_script_sha256':hashlib.sha256(Path(cp.__file__).read_bytes()).hexdigest(),
         'limitation':'Properization does not preserve the Horn or 2SAT syntax; the source origins are controls, not claimed target subclasses.'}
    Path('controls.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
