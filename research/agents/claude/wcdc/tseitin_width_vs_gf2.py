#!/usr/bin/env python3
"""WCDC-0001 hostile control: Tseitin formulas.
Exact minimum resolution refutation WIDTH (width-bounded saturation) versus
the operation count of Gaussian elimination over GF(2) on the same formula.
One graph per invocation (chunking rule: each call < ~30 s); results appended
to tseitin_results.json.  Usage: python3 tseitin_width_vs_gf2.py <graph> [maxw]
"""
import itertools, json, sys, time, os

GRAPHS = {
    "K4": [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],
    "K33": [(a,b) for a in range(3) for b in range(3,6)],
    "Q3": [(u,u^(1<<i)) for u in range(8) for i in range(3) if u < u^(1<<i)],
    "Petersen": [(i,(i+1)%5) for i in range(5)]+[(i,i+5) for i in range(5)]
               +[(5+i,5+(i+2)%5) for i in range(5)],
}

def tseitin(edges):
    V = sorted({v for e in edges for v in e})
    charge = {v: (1 if v == V[0] else 0) for v in V}  # total charge odd -> UNSAT
    clauses = []
    for v in V:
        inc = [i for i,e in enumerate(edges) if v in e]
        for signs in itertools.product([0,1], repeat=len(inc)):
            # forbid assignments x_inc = signs with parity != charge
            if sum(signs) % 2 != charge[v]:
                pos = neg = 0
                for i,s in zip(inc,signs):
                    if s: neg |= 1<<i      # x_i=1 forbidden-> literal ~x_i
                    else: pos |= 1<<i
                clauses.append((pos,neg))
    return V, clauses

def width(c): return bin(c[0]).count("1")+bin(c[1]).count("1")

def refutes_at_width(clauses, w, budget_s=25.0):
    t0=time.time()
    S=set(c for c in clauses if width(c)<=w)
    frontier=list(S); allc=list(S)
    while frontier:
        new=[]
        for a in frontier:
            for b in allc:
                piv=(a[0]&b[1])|(a[1]&b[0])
                if bin(piv).count("1")!=1: continue
                r=((a[0]|b[0])&~piv,(a[1]|b[1])&~piv)
                if r[0]&r[1]: continue
                if width(r)>w or r in S: continue
                if r==(0,0): return True,len(S)+1
                S.add(r); new.append(r)
            if time.time()-t0>budget_s: return None,len(S)
        allc.extend(new); frontier=new
    return False,len(S)

def gf2_ops(V, edges):
    rows=[]
    for i,v in enumerate(V):
        m=0
        for j,e in enumerate(edges):
            if v in e: m|=1<<j
        rows.append([m,1 if i==0 else 0])
    ops=0; r=0
    for col in range(len(edges)):
        p=next((k for k in range(r,len(rows)) if rows[k][0]>>col&1),None)
        if p is None: continue
        rows[r],rows[p]=rows[p],rows[r]
        for k in range(len(rows)):
            if k!=r and rows[k][0]>>col&1:
                rows[k][0]^=rows[r][0]; rows[k][1]^=rows[r][1]; ops+=len(edges)+1
        r+=1
    incons=any(m==0 and b==1 for m,b in rows)
    return ops, incons

def main():
    name=sys.argv[1]; maxw=int(sys.argv[2]) if len(sys.argv)>2 else 8
    edges=GRAPHS[name]; V,cl=tseitin(edges)
    out={"graph":name,"n_vars":len(edges),"n_vertices":len(V),"n_clauses":len(cl),
         "initial_width":max(width(c) for c in cl)}
    ops,inc=gf2_ops(V,edges); out["gf2_bitops"]=ops; out["gf2_detects_unsat"]=inc
    out["width_trials"]=[]
    for w in range(out["initial_width"],maxw+1):
        t=time.time(); ok,sz=refutes_at_width(cl,w)
        out["width_trials"].append({"w":w,"refuted":ok,"closure_size":sz,"sec":round(time.time()-t,2)})
        if ok or ok is None: break
    ok=[t["w"] for t in out["width_trials"] if t["refuted"]]
    out["min_refutation_width"]=ok[0] if ok else None
    fn=os.path.join(os.path.dirname(os.path.abspath(__file__)),"tseitin_results.json")
    data=json.load(open(fn)) if os.path.exists(fn) else {}
    data[name]=out; json.dump(data,open(fn,"w"),indent=1,sort_keys=True)
    print(json.dumps(out))
main()
