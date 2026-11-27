#!/usr/bin/env python3
"""Grok 4.7 work 2026-11-28 04:xx KST.
(A) Structural audit of the PINNED compiler (j15marti/pnp compile.js @21b9d53, blob 7cb0303):
    signed-BFS carriers == source-map groups; every B factor is local to one ternary clause (+ anchor f);
    canonical completion sigma satisfies exactly the gadgets of satisfied clauses (exhaustive over 2^n).
(B) Small-n illustration: exact resolution width w(F) by width-bounded saturation, versus the least k at
    which a T4-02/T1-Q style width-k exact bucket queue (+unit support pins, gauge f=0) refutes the
    normalized native factor system.  Theorem (in the .tex) predicts k_native >= floor(w(F)/3) - 1.
"""
import json, random, subprocess, itertools, sys, os
from collections import defaultdict
HERE=os.path.dirname(os.path.abspath(__file__))
SEED=20261128
rng=random.Random(SEED)

def rand3cnf(n,m):
    cl=[]
    for _ in range(m):
        vs=rng.sample(range(1,n+1),3)
        cl.append([v if rng.random()<0.5 else -v for v in vs])
    return cl

def dimacs(n,cl): return "p cnf %d %d\n"%(n,len(cl))+"".join(" ".join(map(str,c))+" 0\n" for c in cl)

def compile_batch(insts):
    p=subprocess.run(["node",os.path.join(HERE,"compile_batch.js")],input=json.dumps(insts),capture_output=True,text=True,check=True)
    return json.loads(p.stdout)

# ---------- normalization: signed union-find over ports ----------
def normalize(net):
    types=net["types"]; P=4*len(types)
    par=list(range(P)); off=[0]*P
    def find(x):
        if par[x]==x: return x,0
        r,o=find(par[x]); par[x]=r; off[x]^=o; return r,off[x]
    def union(a,b,s):
        ra,oa=find(a); rb,ob=find(b)
        if ra==rb:
            if oa^ob!=s: raise Exception("signed cycle inconsistency")
            return
        par[rb]=ra; off[rb]=oa^ob^s
    sys.setrecursionlimit(1000000)
    for a,b,s in net["edges"]: union(a,b,s)
    for v,t in enumerate(types):
        if t=="E":
            for j in range(1,4): union(4*v,4*v+j,0)
    return [find(p) for p in range(P)]

def analyse(inst, comp):
    net=comp["network"]; sm=comp["source_map"]; n=inst["nvars"]
    pr=normalize(net)
    roots=sorted(set(r for r,_ in pr))
    reps=sm["representative_ports"]          # group id -> [port, sign]
    root2grp={}
    for gid,(p,s) in reps.items():
        r,o=pr[p]
        assert r not in root2grp, "two groups share a carrier"
        root2grp[r]=(gid,o^s)                # port bit = group value XOR (o^s) relative ... see below
    assert len(root2grp)==len(roots), "carrier/group count mismatch"
    # port bit = carrier(root) value XOR off; group value g defined by bit(rep port) = g XOR s_rep
    # so carrier value = g XOR s_rep XOR off(rep); port bit = g XOR s_rep XOR off(rep) XOR off(p)
    def port_expr(p):
        r,o=pr[p]; gid,c=root2grp[r]; return gid,c^o
    F=sm["ternary_clauses"]; prov=sm["vertex_provenance"]
    Bfac=[]; local_ok=True
    for v,t in enumerate(net["types"]):
        if t!="B": continue
        tag,parent,i,j,k=prov[v]; assert tag=="clause"
        lits=[port_expr(4*v+q) for q in range(4)]
        allowed={"x%d"%abs(l) for l in F[i]}|{"z%d"%i,"w%d_0"%i,"w%d_1"%i,"f"}
        if not all(g in allowed for g,_ in lits): local_ok=False
        Bfac.append((i,lits))
    return F,Bfac,local_ok,len(roots)

def canon(F,i,xv):
    """canonical (z,w0,w1) for ternary clause i, f=0; returns None if clause false."""
    a,b,c=F[i]
    L=lambda l: xv[abs(l)] ^ (1 if l<0 else 0)
    for z,w0,w1 in itertools.product((0,1),repeat=3):
        if L(a)+L(b)+z+w0==2 and (1-z)+L(c)+0+w1==2: return z,w0,w1
    return None

def sigma_check(n,F,Bfac):
    checks=0
    for x in range(2**n):
        xv=[0]+[(x>>(v-1))&1 for v in range(1,n+1)]
        val={"f":0}
        for v in range(1,n+1): val["x%d"%v]=xv[v]
        sat_cl=[]
        for i in range(len(F)):
            c=canon(F,i,xv); sat=c is not None; sat_cl.append(sat)
            z,w0,w1=c if sat else (0,0,0)
            val["z%d"%i]=z; val["w%d_0"%i]=w0; val["w%d_1"%i]=w1
        gad_ok=defaultdict(lambda:True)
        for i,lits in Bfac:
            s=sum(val[g]^c for g,c in lits); checks+=1
            if s!=2: gad_ok[i]=False
        for i in range(len(F)):
            if sat_cl[i]!=gad_ok[i]: return False,checks
    return True,checks

# ---------- exact resolution width of a CNF by width-bounded saturation ----------
def res_width(n,cl,wmax):
    base=set()
    for c in cl:
        pos=0;neg=0
        for l in c:
            if l>0: pos|=1<<l
            else: neg|=1<<(-l)
        if pos&neg: continue
        base.add((pos,neg))
    W0=max(bin(p|q).count("1") for p,q in base)
    for w in range(W0,wmax+1):
        S=set(c for c in base if bin(c[0]|c[1]).count("1")<=w)
        frontier=list(S)
        while frontier:
            new=[]
            Sl=list(S)
            for (p1,n1) in frontier:
                for (p2,n2) in Sl:
                    piv=(p1&n2)|(n1&p2)
                    if piv==0 or piv&(piv-1): continue
                    p=(p1|p2)&~piv; q=(n1|n2)&~piv
                    if p&q: continue
                    if bin(p|q).count("1")>w: continue
                    if (p,q) not in S: S.add((p,q)); new.append((p,q))
            if (0,0) in S: return w
            frontier=new
        if (0,0) in S: return w
    return None

# ---------- width-k exact bucket queue (T1-Q / T4-02 style) ----------
def bucket_queue(factors,k):
    """factors: list of (scope tuple, set of allowed rows as dicts->tuple). Returns 'UNSAT','SAT','STUCK'."""
    fs={}; fid=0
    for sc,rows in factors:
        fs[fid]=(tuple(sc),set(rows)); fid+=1
    def restrict(var,val):
        nonlocal fid
        for i,(sc,rows) in list(fs.items()):
            if var in sc:
                j=sc.index(var); nsc=sc[:j]+sc[j+1:]
                nr={r[:j]+r[j+1:] for r in rows if r[j]==val}
                fs[i]=(nsc,nr)
    changed=True
    while True:
        # contradiction / unit support closure
        progress=True
        while progress:
            progress=False
            for i,(sc,rows) in list(fs.items()):
                if not rows: return "UNSAT"
                if not sc: del fs[i]; continue
                for j,v in enumerate(sc):
                    vals={r[j] for r in rows}
                    if len(vals)==1:
                        restrict(v,vals.pop()); progress=True; break
                if progress: break
        live=set(v for sc,_ in fs.values() for v in sc)
        if not live: return "SAT"
        best=None
        for v in sorted(live):
            inc=[i for i,(sc,_) in fs.items() if v in sc]
            U=sorted(set(u for i in inc for u in fs[i][0]))
            if len(U)<=k and (best is None or len(U)<len(best[1])): best=(v,U,inc)
        if best is None: return "STUCK"
        v,U,inc=best
        out=sorted(u for u in U if u!=v); rows=set()
        pos={u:t for t,u in enumerate(U)}
        for word in itertools.product((0,1),repeat=len(U)):
            if all(tuple(word[pos[u]] for u in fs[i][0]) in fs[i][1] for i in inc):
                rows.add(tuple(word[pos[u]] for u in out))
        for i in inc: del fs[i]
        fs[fid]=(tuple(out),rows); fid+=1

def native_factors(Bfac,gauge_f=True):
    out=[]
    for i,lits in Bfac:
        sc=sorted(set(g for g,_ in lits))
        rows=set()
        for word in itertools.product((0,1),repeat=len(sc)):
            a=dict(zip(sc,word))
            if sum(a[g]^c for g,c in lits)==2: rows.add(word)
        out.append((sc,rows))
    if gauge_f: out.append((["f"],{(0,)}))
    return out

def cnf_factors(cl):
    out=[]
    for c in cl:
        sc=sorted(set(abs(l) for l in c))
        rows={w for w in itertools.product((0,1),repeat=len(sc))
              if any(w[sc.index(abs(l))]==(1 if l>0 else 0) for l in c)}
        out.append((sc,rows))
    return out

def min_k(factors,kmax):
    for k in range(2,kmax+1):
        r=bucket_queue(factors,k)
        if r!="STUCK": return k,r
    return None,"STUCK"

def main():
    res={"seed":SEED,"compiler":"compile.js@21b9d53 blob 7cb030354b765aa003cd295bd538165ef83507b3","A":[],"B":[]}
    # (A) structural + exhaustive sigma audit
    insts=[]
    for n in (5,6,7,8,9,10):
        for r in range(6):
            m=rng.choice([2*n,3*n,4*n,5*n,6*n])
            insts.append({"id":"A-%d-%d"%(n,r),"nvars":n,"dimacs":dimacs(n,rand3cnf(n,m)),"m":m})
    comps=compile_batch([{k:x[k] for k in ("id","nvars","dimacs")} for x in insts])
    allA=True; totchecks=0
    for x,c in zip(insts,comps):
        F,Bfac,loc,ncar=analyse(x,c)
        ok,ch=sigma_check(x["nvars"],F,Bfac); totchecks+=ch
        exp_car=x["nvars"]+3*len(F)+1
        row={"id":x["id"],"n":x["nvars"],"m":x["m"],"B_vertices":len(Bfac),"carriers":ncar,
             "carriers_expected_n_plus_3m_plus_1":exp_car,"local":loc,"sigma_exact":ok}
        allA&= loc and ok and ncar==exp_car
        res["A"].append(row)
    res["A_summary"]={"instances":len(insts),"all_pass":allA,"B_gadget_evaluations":totchecks}
    print("A:",res["A_summary"])
    # (B) widths on small UNSAT instances
    insts=[]
    for n in (6,7,8,9,10):
        cnt=0; tries=0
        while cnt<4 and tries<200:
            tries+=1
            m=int(round(rng.choice([7,8,9])*n))
            cl=rand3cnf(n,m)
            if any(all(any(((x>>(abs(l)-1))&1)==(l>0) for l in c) for c in cl) for x in range(2**n)): continue
            insts.append({"id":"B-%d-%d"%(n,cnt),"nvars":n,"dimacs":dimacs(n,cl),"cl":cl,"m":m}); cnt+=1
    comps=compile_batch([{k:x[k] for k in ("id","nvars","dimacs")} for x in insts])
    viol=0
    for x,c in zip(insts,comps):
        F,Bfac,loc,ncar=analyse(x,c)
        wF=res_width(x["nvars"],x["cl"],x["nvars"])
        kF,rF=min_k(cnf_factors(x["cl"]),x["nvars"]+1)
        kN,rN=min_k(native_factors(Bfac),14)
        pred=wF//3-1
        if kN is not None and kN<pred: viol+=1
        row={"id":x["id"],"n":x["nvars"],"m":x["m"],"w_res_F":wF,"k_bucket_F":kF,"k_bucket_native_gauged":kN,
             "native_result":rN,"theorem_lower_bound_floor_w/3_minus_1":pred}
        res["B"].append(row); print(row)
    res["B_summary"]={"instances":len(insts),"theorem_violations":viol}
    print("B:",res["B_summary"])
    json.dump(res,open(os.path.join(HERE,"locality_width.out.json"),"w"),indent=1)
main()
