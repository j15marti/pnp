#!/usr/bin/env python3
"""Grok 4.7 work 2026-11-28 ~05 KST.  Computational audit for the PC-degree transfer through the
PINNED compiler j15marti/pnp compile.js @21b9d53 (blob 7cb0303, copied verbatim).
 (A) Substitution identity: for every B factor of gadget i and every forbidden carrier word a of that
     factor, the substituted axiom delta_a o sigma, as an exact integer multilinear polynomial in vars(C_i),
     equals c * P_{C_i}, where P_{C_i} is the clause (falsity-indicator) polynomial and c in {0,1}.
     Exact over Z, hence over every field.  Also checks deg(sigma_y) <= 3 and unreduced degree <= 12.
 (B) Complement invariance of CNF(N): each B factor's forbidden set is closed under complementing all carriers.
 (C) Q-affine relaxation: the all-1/2 port point satisfies every signed edge, E and B linear equation.
 (D) GF(2) affine relaxation (edge XOR, E equality, B even parity) on compiled UNSAT random 3-CNFs:
     consistency by exact Gaussian elimination (illustration only).
 (E) Spot-check of T1/L02 NAE sewing identity (21d3f8c) exhaustively for |A|,|B|<=3.
"""
import json, random, subprocess, itertools, os, sys
from fractions import Fraction
from collections import defaultdict
HERE=os.path.dirname(os.path.abspath(__file__))
rng=random.Random(20261128_05)

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

def gf2_consistent(net):
    """edge XOR, E equalities, B even parity over port bits; exact GE with python ints as bitsets"""
    types=net["types"]; P=4*len(types); rows=[]
    for a,b,s in net["edges"]: rows.append(((1<<a)|(1<<b),s))
    for v,t in enumerate(types):
        if t=="E":
            for j in range(1,4): rows.append(((1<<(4*v))|(1<<(4*v+j)),0))
        else: rows.append((sum(1<<(4*v+j) for j in range(4)),0))
    piv={}
    for m,r in rows:
        while m:
            h=m.bit_length()-1
            if h in piv: pm,pr_=piv[h]; m^=pm; r^=pr_
            else: piv[h]=(m,r); break
        if m==0 and r==1: return False,len(rows),len(piv)
    return True,len(rows),len(piv)

def half_point_ok(net):
    types=net["types"]; y=[Fraction(1,2)]*(4*len(types))
    ok=all((y[b]==(y[a] if s==0 else 1-y[a])) for a,b,s in net["edges"])
    for v,t in enumerate(types):
        q=y[4*v:4*v+4]
        ok&= (len(set(q))==1) if t=="E" else (sum(q)==2)
    return ok

def sat(n,cl):
    for x in range(1<<n):
        if all(any(((x>>(abs(l)-1))&1)==(l>0) for l in c) for c in cl): return True
    return False

def nae(xs): return len(set(xs))>1
def nae_check():
    cnt=0
    for la in range(1,4):
        for lb in range(1,4):
            for A in itertools.product((0,1),repeat=la):
                for B in itertools.product((0,1),repeat=lb):
                    lhs=any(nae(A+(p,)) and nae(B+(1-p,)) for p in (0,1))
                    assert lhs==nae(A+B); cnt+=1
    return cnt

out={"seed":"20261128_05","compiler_blob":"7cb030354b765aa003cd295bd538165ef83507b3"}
# (A),(B),(C) on random small instances
insts=[]
for t in range(30):
    n=rng.randint(4,9); m=rng.randint(2*n,6*n); insts.append({"id":"A%d"%t,"nvars":n,"dimacs":dimacs(n,rand3cnf(n,m)),"m":m})
comps=compile_batch([{k:v for k,v in x.items() if k!="m"} for x in insts])
tot=defaultdict(int); half_all=True
for x,cpl in zip(insts,comps):
    F,B=analyse(cpl); s=audit_AB(F,B)
    for k,v in s.items():
        tot[k]=max(tot[k],v) if k.startswith("max") else tot[k]+v
    half_all&=half_point_ok(cpl["network"])
out["A_B_C"]=dict(instances=len(insts),**tot,half_point_all=half_all)
# (D) GF(2) relaxation on compiled UNSAT random 3-CNF
D=[]; tries=0; uns=[]
while len(uns)<20:
    n=rng.randint(8,14); m=int(6*n); cl=rand3cnf(n,m); tries+=1
    if not sat(n,cl): uns.append({"id":"D%d"%len(uns),"nvars":n,"dimacs":dimacs(n,cl)})
comps=compile_batch(uns)
for x,cpl in zip(uns,comps):
    ok,r,rk=gf2_consistent(cpl["network"]); D.append(dict(id=x["id"],n=x["nvars"],ports=4*len(cpl["network"]["types"]),rows=r,rank=rk,gf2_consistent=ok,half_point=half_point_ok(cpl["network"])))
out["D_gf2_relaxation_unsat_instances"]=D
out["D_summary"]=dict(unsat=len(D),gf2_consistent=sum(d["gf2_consistent"] for d in D),half_point=sum(d["half_point"] for d in D))
out["E_nae_sewing_cases"]=nae_check()
print(json.dumps(out,indent=1))
