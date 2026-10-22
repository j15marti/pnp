"""CERT-GENERATOR-COMPRESSIBILITY77: zlib/lzma as a crude KT upper-bound proxy.
Compares explicit UNSAT certificates (DPLL refutation trees) for (a) pigeonhole
PHP_n^{n+1} under a fixed variable order and (b) random 3-CNF at ratio 5.0.
Runtime: each case is bounded by node budget; whole run well under 30s."""
import json, random, zlib, lzma, itertools, sys, time

def php(n):
    v=lambda p,h:p*n+h+1
    cl=[[v(p,h) for h in range(n)] for p in range(n+1)]
    for h in range(n):
        for p,q in itertools.combinations(range(n+1),2): cl.append([-v(p,h),-v(q,h)])
    return n*(n+1),cl

def rand3(nv,ratio,seed):
    r=random.Random(seed); cl=[]
    for _ in range(int(ratio*nv)):
        vs=r.sample(range(1,nv+1),3); cl.append([x*r.choice((-1,1)) for x in vs])
    return nv,cl

def dpll_trace(nv,cl,budget):
    """returns (status, trace bytes): trace = preorder of (var,leaf-marker) with unit propagation"""
    out=bytearray(); nodes=[0]
    def rec(assign):
        nodes[0]+=1
        if nodes[0]>budget: raise TimeoutError
        # unit propagate
        changed=True; trail=[]
        while changed:
            changed=False
            for c in cl:
                sat=False; un=[]
                for l in c:
                    a=assign.get(abs(l))
                    if a is None: un.append(l)
                    elif (a>0)==(l>0): sat=True;break
                if sat: continue
                if not un:
                    out.append(0); 
                    for t in trail: del assign[t]
                    return False
                if len(un)==1:
                    assign[abs(un[0])]=1 if un[0]>0 else -1; trail.append(abs(un[0])); changed=True
        free=[v for v in range(1,nv+1) if v not in assign]
        if not free: raise ValueError("SAT")
        v=free[0]; out.extend([1,v&255,v>>8])
        ok=True
        for s in (1,-1):
            assign[v]=s; r=rec(assign); del assign[v]
            if r: raise ValueError("SAT")
        for t in trail: del assign[t]
        return False
    try: rec({}); return "UNSAT",bytes(out),nodes[0]
    except ValueError: return "SAT",bytes(out),nodes[0]
    except TimeoutError: return "BUDGET",bytes(out),nodes[0]

rows=[]; t0=time.time()
for n in range(3,8):
    nv,cl=php(n); s,tr,k=dpll_trace(nv,cl,60000)
    rows.append(dict(fam="PHP",n=n,vars=nv,status=s,nodes=k,raw=len(tr),zlib=len(zlib.compress(tr,9)),lzma=len(lzma.compress(tr))))
for nv in (20,30,40,50):
    for seed in range(3):
        v,cl=rand3(nv,5.0,seed); s,tr,k=dpll_trace(v,cl,60000)
        rows.append(dict(fam="R3SAT5.0",n=nv,seed=seed,vars=v,status=s,nodes=k,raw=len(tr),zlib=len(zlib.compress(tr,9)),lzma=len(lzma.compress(tr))))
    if time.time()-t0>20: break
for r in rows:
    r["ratio_lzma"]=round(r["lzma"]/max(r["raw"],1),4)
    print(r)
json.dump(rows,open(sys.argv[1] if len(sys.argv)>1 else "/dev/stdout","w"),indent=1) if len(sys.argv)>1 else None
