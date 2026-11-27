#!/usr/bin/env python3
"""Grok 4.7 work 2026-11-28 ~06 KST.  Computational audit for the Sherali-Adams / SOS degree transfer
through the PINNED compiler j15marti/pnp compile.js @21b9d53 (blob 7cb0303, verbatim copy already in
comments/grok-4.7/2026-11-28/code/).
 (A) Substitution identity  ml(rho(delta_a)) = c * P_C  (re-run of the 04:55 check on fresh seeds).
 (J) Junta expansion: every substituted carrier p_y and 1-p_y is a {0,1}-valued function of <=3 source
     variables, hence equals (mod the Boolean ideal) a nonnegative 0/1 sum of x-juntas of degree <=3;
     checked exactly via Moebius coefficients.  This is the only fact the SA transfer needs beyond (A).
 (T) Complement (tau) closure of every B factor's forbidden set (needed for the gauge step).
 (L) Local LP illustration: for compiled UNSAT random 3-CNFs, the 'factor-scope Sherali-Adams' LP
     (a probability distribution on the allowed words of every B factor, with marginals agreeing on
     every nonempty intersection of factor scopes) with a gauge carrier pinned to 0 -- feasibility by
     HiGHS, then the returned point is re-checked in exact rational arithmetic after rounding to the
     explicit symmetric witness when available.  Illustration only (not a degree bound).
"""
import json, random, subprocess, itertools, os, sys, time
from fractions import Fraction
from collections import defaultdict
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix, csr_matrix
HERE=os.path.dirname(os.path.abspath(__file__))
rng=random.Random(2026112806)
def rand3cnf(n,m):
    return [[v if rng.random()<0.5 else -v for v in rng.sample(range(1,n+1),3)] for _ in range(m)]
def dimacs(n,cl): return "p cnf %d %d\n"%(n,len(cl))+"".join(" ".join(map(str,c))+" 0\n" for c in cl)
def compile_batch(insts):
    p=subprocess.run(["node",os.path.join(HERE,"compile_batch.js")],input=json.dumps(insts),capture_output=True,text=True,check=True)
    return json.loads(p.stdout)

def normalize(net):
    types=net["types"]; P=4*len(types); par=list(range(P)); off=[0]*P
    def find(x):
        path=[]
        while par[x]!=x: path.append(x); x=par[x]
        r=x; acc=0
        for y in reversed(path):
            acc^=off[y]; off[y]=acc; par[y]=r
        return r
    def get(x): r=find(x); return r,(off[x] if x!=r else 0)
    def union(a,b,s):
        ra,oa=get(a); rb,ob=get(b)
        if ra==rb:
            assert oa^ob==s; return
        par[rb]=ra; off[rb]=oa^ob^s
    for a,b,s in net["edges"]: union(a,b,s)
    for v,t in enumerate(types):
        if t=="E":
            for j in range(1,4): union(4*v,4*v+j,0)
    return [get(p) for p in range(P)]

def analyse(comp):
    net=comp["network"]; sm=comp["source_map"]; pr=normalize(net)
    root2grp={}
    for gid,(p,s) in sm["representative_ports"].items():
        r,o=pr[p]; assert r not in root2grp; root2grp[r]=(gid,o^s)
    assert len(root2grp)==len(set(r for r,_ in pr))
    def port_expr(p):
        r,o=pr[p]; gid,c=root2grp[r]; return gid,c^o
    F=sm["ternary_clauses"]; prov=sm["vertex_provenance"]; Bfac=[]
    for v,t in enumerate(net["types"]):
        if t!="B": continue
        i=prov[v][2]; Bfac.append((i,[port_expr(4*v+q) for q in range(4)]))
    return F,Bfac

def canon(c,xv):
    a,b,cc=c; L=lambda l: xv[abs(l)]^(1 if l<0 else 0)
    for z,w0,w1 in itertools.product((0,1),repeat=3):
        if L(a)+L(b)+z+w0==2 and (1-z)+L(cc)+w1==2: return (z,w0,w1)
    return (0,0,0)

def mobius(vals,k):
    """vals: dict tuple(bits)->int over {0,1}^k ; returns multilinear integer coefficients dict mask->coef"""
    co={}
    for S in range(1<<k):
        s=0
        for T in range(1<<k):
            if T & ~S: continue
            pt=tuple((T>>j)&1 for j in range(k))
            s+=(-1)**(bin(S).count("1")-bin(T).count("1"))*vals[pt]
        if s: co[S]=s
    return co

def audit_AB(F,Bfac):
    stats=dict(factors=0,forbidden_words=0,identity_ok=0,nonzero_c=0,max_sigma_deg=0,max_unreduced=0,compl_ok=0)
    for i,lits in Bfac:
        c=F[i]; vs=sorted({abs(l) for l in c}); k=len(vs)
        carriers=sorted({g for g,_ in lits}); stats["factors"]+=1
        # sigma polynomial of each carrier as function of vs
        def sig_val(g,pt):
            xv=defaultdict(int)
            for v,b in zip(vs,pt): xv[v]=b
            if g=="f": return 0
            if g.startswith("x"): return xv[int(g[1:])]
            zw=canon(c,xv)
            assert g in ("z%d"%i,"w%d_0"%i,"w%d_1"%i), g
            return zw[{"z":0,"w":1+int(g.split("_")[1]) if "_" in g else 0}[g[0]] if g[0]=="w" else 0]
        pts=list(itertools.product((0,1),repeat=k))
        for g in carriers:
            co=mobius({pt:sig_val(g,pt) for pt in pts},k)
            d=max([bin(S).count("1") for S in co] or [0]); stats["max_sigma_deg"]=max(stats["max_sigma_deg"],d)
        # forbidden carrier words
        forb=[]
        for word in itertools.product((0,1),repeat=len(carriers)):
            val=dict(zip(carriers,word))
            if sum(val[g]^s for g,s in lits)!=2: forb.append(word)
        fs=set(forb)
        if all(tuple(1-b for b in w) in fs for w in forb): stats["compl_ok"]+=1
        nontriv=[g for g in carriers if g!="f"]
        stats["max_unreduced"]=max(stats["max_unreduced"],3*len(nontriv))
        # clause polynomial P_C over vs: indicator that c is false
        def clause_false(pt):
            xv=dict(zip(vs,pt)); return int(all((xv[abs(l)]^(1 if l<0 else 0))==0 for l in c))
        PC=mobius({pt:clause_false(pt) for pt in pts},k)
        for w in forb:
            stats["forbidden_words"]+=1
            vals={pt:int(all(sig_val(g,pt)==b for g,b in zip(carriers,w))) for pt in pts}
            Q=mobius(vals,k)
            cst=[vals[pt] for pt in pts if clause_false(pt)]
            cc=cst[0] if cst else 0
            target={S:cc*v for S,v in PC.items() if cc*v}
            if Q==target: stats["identity_ok"]+=1
            if cc: stats["nonzero_c"]+=1
    return stats

def factor_tables(F,Bfac):
    """per B factor: (clause idx, carriers, allowed words, forbidden words, sigma tables)"""
    out=[]
    for i,lits in Bfac:
        carriers=sorted({g for g,_ in lits})
        allowed=[];forb=[]
        for word in itertools.product((0,1),repeat=len(carriers)):
            val=dict(zip(carriers,word))
            (allowed if sum(val[g]^s for g,s in lits)==2 else forb).append(word)
        out.append((i,carriers,allowed,forb))
    return out

def sigma_table(c,i,g,vs,pt):
    xv=defaultdict(int)
    for v,b in zip(vs,pt): xv[v]=b
    if g=="f": return 0
    if g.startswith("x"): return xv[int(g[1:])]
    zw=canon(c,xv)
    if g=="z%d"%i: return zw[0]
    if g=="w%d_0"%i: return zw[1]
    if g=="w%d_1"%i: return zw[2]
    raise AssertionError(g)

def audit_J_T(F,Bfac):
    st=dict(carrier_tables=0,zero_one_valued=0,junta_expansion_ok=0,max_deg=0,factors_JT=0,tau_closed=0)
    for i,carriers,allowed,forb in factor_tables(F,Bfac):
        st["factors_JT"]+=1
        fs=set(forb)
        if all(tuple(1-b for b in w) in fs for w in forb): st["tau_closed"]+=1
        c=F[i]; vs=sorted({abs(l) for l in c}); k=len(vs); pts=list(itertools.product((0,1),repeat=k))
        for g in carriers:
            vals={pt:sigma_table(c,i,g,vs,pt) for pt in pts}
            st["carrier_tables"]+=1
            if set(vals.values())<={0,1}: st["zero_one_valued"]+=1
            co=mobius(vals,k); st["max_deg"]=max([st["max_deg"]]+[bin(S).count("1") for S in co])
            # sum of point-juntas delta_b over b with value 1, expanded exactly
            for neg in (0,1):
                tgt=defaultdict(int)
                for pt in pts:
                    if (vals[pt]^neg)!=1: continue
                    dco=mobius({q:int(q==pt) for q in pts},k)
                    for S,v in dco.items(): tgt[S]+=v
                tgt={S:v for S,v in tgt.items() if v}
                want=mobius({pt:vals[pt]^neg for pt in pts},k)
                if tgt==want and all(vals[pt]^neg in (0,1) for pt in pts): st["junta_expansion_ok"]+=1
    return st

def local_lp(F,Bfac,pin=None):
    tabs=factor_tables(F,Bfac)
    scopes=[frozenset(c) for _,c,_,_ in tabs]
    Ts=set()
    for s in scopes:
        for g in s: Ts.add(frozenset([g]))
    by=defaultdict(list)
    for fi,s in enumerate(scopes):
        for g in s: by[g].append(fi)
    for g,fl in by.items():
        for a,b in itertools.combinations(fl,2):
            t=scopes[a]&scopes[b]
            if len(t)>=2: Ts.add(t)
    Ts=[tuple(sorted(t)) for t in Ts]
    var={}; 
    for fi,(_,c,al,_) in enumerate(tabs):
        for w in al: var[("m",fi,w)]=len(var)
    for t in Ts:
        for u in itertools.product((0,1),repeat=len(t)): var[("n",t,u)]=len(var)
    rows=[]; rhs=[]
    for fi,(_,c,al,_) in enumerate(tabs):
        rows.append({var[("m",fi,w)]:1 for w in al}); rhs.append(1)
        sc=set(c)
        for t in Ts:
            if not set(t)<=sc: continue
            idx=[c.index(g) for g in t]
            for u in itertools.product((0,1),repeat=len(t)):
                r={var[("n",t,u)]:-1}
                for w in al:
                    if tuple(w[j] for j in idx)==u: r[var[("m",fi,w)]]=r.get(var[("m",fi,w)],0)+1
                rows.append(r); rhs.append(0)
    if pin is not None:
        rows.append({var[("n",(pin,),(1,))]:1}); rhs.append(0)
    A=lil_matrix((len(rows),len(var)))
    for ri,r in enumerate(rows):
        for j,v in r.items(): A[ri,j]=v
    A=csr_matrix(A); b=np.array(rhs,float)
    t0=time.time()
    res=linprog(np.zeros(len(var)),A_eq=A,b_eq=b,bounds=(0,1),method="highs")
    info=dict(factors=len(tabs),intersection_sets=len(Ts),vars=len(var),rows=len(rows),status=int(res.status),
              feasible=bool(res.status==0),secs=round(time.time()-t0,2))
    if res.status==0:
        x=res.x; info["max_abs_residual"]=float(np.max(np.abs(A@x-b))); info["min_x"]=float(x.min())
    return info

def uniform_blp_exact(F,Bfac):
    """exact: uniform distribution on each factor's allowed words gives every carrier marginal 1/2 (no pin)"""
    for i,c,al,_ in factor_tables(F,Bfac):
        for j in range(len(c)):
            if Fraction(sum(w[j] for w in al),len(al))!=Fraction(1,2): return False
    return True

def sat(n,cl):
    for x in range(1<<n):
        if all(any(((x>>(abs(l)-1))&1)==(l>0) for l in c) for c in cl): return True
    return False

if __name__=="__main__":
    out={"seed":2026112806,"compiler_blob":"7cb030354b765aa003cd295bd538165ef83507b3"}
    insts=[]
    for t in range(30):
        n=rng.randint(4,9); m=rng.randint(2*n,6*n); insts.append({"id":"A%d"%t,"nvars":n,"dimacs":dimacs(n,rand3cnf(n,m))})
    comps=compile_batch(insts)
    tot=defaultdict(int)
    for cpl in comps:
        F,B=analyse(cpl)
        for k,v in list(audit_AB(F,B).items())+list(audit_J_T(F,B).items()):
            tot[k]=max(tot[k],v) if k.startswith("max") else tot[k]+v
    out["A_J_T"]=dict(instances=len(insts),**tot)
    uns=[]
    while len(uns)<12:
        n=rng.randint(8,12); m=6*n; cl=rand3cnf(n,m)
        if not sat(n,cl): uns.append({"id":"L%d"%len(uns),"nvars":n,"dimacs":dimacs(n,cl)})
    comps=compile_batch(uns); L=[]
    for x,cpl in zip(uns,comps):
        F,B=analyse(cpl)
        row=dict(id=x["id"],n=x["nvars"],m=len(F),uniform_blp_exact=uniform_blp_exact(F,B))
        carriers=sorted({g for _,c,_,_ in factor_tables(F,B) for g in c})
        pins=["f","x1",carriers[11]] if len(carriers)>11 else ["f","x1"]
        row["nopin"]=local_lp(F,B,None)
        row["pins"]={p:local_lp(F,B,p) for p in pins}
        L.append(row)
    out["L_local_lp_unsat"]=L
    out["L_summary"]=dict(unsat=len(L),uniform_blp_exact=sum(r["uniform_blp_exact"] for r in L),
        nopin_feasible=sum(r["nopin"]["feasible"] for r in L),
        pinned_runs=sum(len(r["pins"]) for r in L),
        pinned_feasible=sum(v["feasible"] for r in L for v in r["pins"].values()))
    print(json.dumps(out,indent=1))
