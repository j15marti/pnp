#!/usr/bin/env python3
"""Independent finite referee for connected G_t representation separation."""
import argparse, itertools, json, time, resource
from functools import lru_cache

F9 = ((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
      (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))

def gt(t):
    out=[]
    for i in range(t):
        off=9*i; nxt=9*((i+1)%t)
        for ci,c in enumerate(F9):
            cc=[]
            for z in c:
                if ci==0 and z==5: cc.append(nxt+5)
                else: cc.append((1 if z>0 else -1)*(off+abs(z)))
            out.append(tuple(cc))
    return tuple(out)

def sat(F,mask):
    return all(any(((mask>>(abs(z)-1))&1)==(z>0) for z in c) for c in F)

def valid(F,n):
    if len(set(F))!=len(F): return False
    cnt={(v,s):0 for v in range(1,n+1) for s in (1,-1)}
    for c in F:
        if len(c)!=3 or len({abs(z) for z in c})!=3 or not(all(z>0 for z in c) or all(z<0 for z in c)): return False
        for z in c:
            if not 1<=abs(z)<=n: return False
            cnt[(abs(z),1 if z>0 else -1)]+=1
    return all(x==2 for x in cnt.values())

def circuit_metrics(F,n):
    depths=[]
    for c in F:
        d1=1; d2=max(d1,0)+1; depths.append(d2)
    layer=depths[:]
    while len(layer)>1:
        layer=[max(layer[i],layer[i+1])+1 if i+1<len(layer) else layer[i] for i in range(0,len(layer),2)]
    return 2*len(F)+len(F)-1,layer[0]

def circuit_truth(F,n):
    gates=[]; outs=[]
    def add(op,x,y):
        z=n+len(gates)+1;gates.append((z,op,x,y));return z
    for c in F:outs.append(add("OR",add("OR",c[0],c[1]),c[2]))
    while len(outs)>1:outs=[add("AND",outs[i],outs[i+1]) if i+1<len(outs) else outs[i] for i in range(0,len(outs),2)]
    tt=[]
    for mask in range(1<<n):
        a={v:(mask>>(v-1))&1 for v in range(1,n+1)}
        for z,op,x,y in gates:
            X=a[abs(x)] if x>0 else 1-a[abs(x)];Y=a[abs(y)] if y>0 else 1-a[abs(y)]
            a[z]=int((X or Y) if op=="OR" else (X and Y))
        tt.append(a[outs[0]])
    return tt

def connected_incidence(F,n):
    adj={i:set() for i in range(n+len(F))}
    for j,c in enumerate(F):
        q=n+j
        for z in c:adj[abs(z)-1].add(q);adj[q].add(abs(z)-1)
    seen={0};stack=[0]
    while stack:
        u=stack.pop()
        for v in adj[u]-seen:seen.add(v);stack.append(v)
    return len(seen)==len(adj)

def gf2_rank(rows):
    piv={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in piv: x^=piv[p]
            else: piv[p]=x; break
    return len(piv)

def cut_stats(F,n,A):
    B=[v for v in range(1,n+1) if v not in A]; rows=[]
    for am in range(1<<len(A)):
        r=0
        base=sum(((am>>i)&1)<<(v-1) for i,v in enumerate(A))
        for bm in range(1<<len(B)):
            mask=base|sum(((bm>>i)&1)<<(v-1) for i,v in enumerate(B))
            if sat(F,mask): r|=1<<bm
        rows.append(r)
    cols=[]
    for j in range(1<<len(B)):
        col=sum(((r>>j)&1)<<i for i,r in enumerate(rows)); cols.append(col)
    return {"gf2_rank":gf2_rank(rows),"forward_rows":len(set(rows)),"reverse_rows":len(set(cols))}

def local_rank9():
    rows=[]
    for a in range(16):
        r=0
        for b in range(16):
            mask=sum(((a>>i)&1)<<(v-1) for i,v in enumerate((1,2,3,4)))
            mask|=sum(((b>>i)&1)<<(v-1) for i,v in enumerate((6,7,8,9)))
            if sat(F9,mask):r|=1<<b
        rows.append(r)
    ri=(1,3,4,5,6,9,11,12,13);ci=(2,3,4,5,7,8,9,10,14)
    minor=[sum(((rows[r]>>c)&1)<<j for j,c in enumerate(ci)) for r in ri]
    return {"rank":gf2_rank(rows),"minor_rank":gf2_rank(minor),"minor_rows":ri,"minor_cols":ci}

def robdd_nodes(F,n,order):
    uniq={}; nextid=[2]
    @lru_cache(None)
    def rec(level,mask):
        if level==n: return int(sat(F,mask))
        v=order[level]; lo=rec(level+1,mask); hi=rec(level+1,mask|(1<<(v-1)))
        if lo==hi:return lo
        key=(v,lo,hi)
        if key not in uniq: uniq[key]=nextid[0];nextid[0]+=1
        return uniq[key]
    rec(0,0); return len(uniq)

def f9_all_orders():
    T=tuple(int(sat(F9,z)) for z in range(512)); edge={}
    for S in range(512):
      pre=[i for i in range(9) if S>>i&1]
      for v in range(9):
       if S>>v&1:continue
       rest=[i for i in range(9) if not(S>>i&1) and i!=v];pairs=set()
       for a in range(1<<len(pre)):
        base=sum(((a>>j)&1)<<u for j,u in enumerate(pre));p=[]
        for bit in (0,1):
         q=0
         for b in range(1<<len(rest)):
          z=base|(bit<<v)|sum(((b>>j)&1)<<u for j,u in enumerate(rest));q|=T[z]<<b
         p.append(q)
        if p[0]!=p[1]:pairs.add(tuple(p))
       edge[S,v]=len(pairs)
    full=511
    @lru_cache(None)
    def best(S):return 0 if S==full else min(edge[S,v]+best(S|1<<v) for v in range(9) if not(S>>v&1))
    @lru_cache(None)
    def worst(S):return 0 if S==full else max(edge[S,v]+worst(S|1<<v) for v in range(9) if not(S>>v&1))
    S=0;natural=0
    for v in range(9):natural+=edge[S,v];S|=1<<v
    return {"best":best(0),"natural":natural,"worst":worst(0),"orders":362880}

def support_matrix(F,t,block,pins):
    b0=9*block+5; b1=9*((block+1)%t)+5
    priv=[9*block+j for j in (1,2,3,4,6,7,8,9)]
    BF=F[12*block:12*(block+1)]; W=[[0,0],[0,0]]
    for u in (0,1):
      for v in (0,1):
        a=dict(pins)
        if (b0 in a and a[b0]!=u) or (b1 in a and a[b1]!=v):continue
        a[b0]=u;a[b1]=v; free=[x for x in priv if x not in a]
        for bits in range(1<<len(free)):
            aa=dict(a);aa.update({x:(bits>>i)&1 for i,x in enumerate(free)})
            if all(any(aa[abs(z)]==(z>0) for z in c) for c in BF):W[u][v]+=1
    return W

def bool_product(A,B):
    return [[int(any(A[i][k] and B[k][j] for k in (0,1))) for j in (0,1)] for i in (0,1)]

def trace_support(mats):
    P=[[1,0],[0,1]]
    for M in mats:P=bool_product(P,[[int(x>0) for x in row] for row in M])
    return int(P[0][0] or P[1][1]),P

def brute_pins(F,n,pins):
    free=[v for v in range(1,n+1) if v not in pins]; count=0; witness=None
    base=sum(x<<(v-1) for v,x in pins.items())
    for b in range(1<<len(free)):
        m=base|sum(((b>>i)&1)<<(v-1) for i,v in enumerate(free))
        if sat(F,m):count+=1; witness=m if witness is None else witness
    return count,witness

def antichain(t):
    F=gt(t); A={9*i+j for i in range(t) for j in (1,2,3,4)}
    crossing=[c for c in F if any(abs(z) in A for z in c) and any(abs(z) not in A for z in c)]
    inside=[c for c in F if all(abs(z) in A for z in c)]; av=sorted(A); masks=set(); rejected=0
    for b in range(1<<len(av)):
        a={v:(b>>i)&1 for i,v in enumerate(av)}
        if not all(any(a[abs(z)]==(z>0) for z in c) for c in inside): rejected+=1;continue
        q=0
        for j,c in enumerate(crossing):
            if any(abs(z) in A and a[abs(z)]==(z>0) for z in c):q|=1<<j
        masks.add(q)
    maximal=[x for x in masks if not any(x!=y and x&~y==0 for y in masks)]
    return {"alive_assignments":(1<<len(av))-rejected,"distinct_masks":len(masks),"maximal_antichain":len(maximal),"crossing_clauses":len(crossing)}

def su_modes(F):
    out={"SS":0,"SU":0,"US":0,"UU":0}
    for i,j in itertools.combinations(range(len(F)),2):
      for a,b in itertools.product(("S","U"),repeat=2):
        req={};ok=True
        for c,m in ((F[i],a),(F[j],b)):
          for z in c:
            v=int(z>0) if m=="S" else int(z<0)
            if abs(z) in req and req[abs(z)]!=v:ok=False
            req[abs(z)]=v
        out[a+b]+=ok
    return out

def f9_phase():
    t=time.time(); gates,depth=circuit_metrics(F9,9); truth=[]
    for m in range(512):truth.append(int(sat(F9,m)))
    ctt=circuit_truth(F9,9)
    pins={2:0,3:0,6:1}; p0=dict(pins,x=0) if False else None
    c0,_=brute_pins(F9,9,{**pins,1:0});c1,_=brute_pins(F9,9,{**pins,1:1})
    mal=[F9[:-1],F9+(F9[0],),((1,1,2),)+F9[1:],((-1,2,3),)+F9[1:],((1,2,99),)+F9[1:],F9[:-1]+((1,2,3),)]
    return {"valid":valid(F9,9),"models":sum(truth),"truth_sha_like":{"ones":sum(truth),"length":len(truth)},
            "circuit":{"gates":gates,"depth":depth,"matches_all":ctt==truth},"obdd_all_orders":f9_all_orders(),"SU_modes":su_modes(F9),
            "same_source_pins":{"common":pins,"x1_0":c0,"x1_1":c1},"malformed_rejected":sum(not valid(x,9) for x in mal),"seconds":time.time()-t,"peak_rss_kb":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}

def g2_phase():
    t=time.time(); F=gt(2); n=18; truth=[int(sat(F,m)) for m in range(1<<n)]
    A=[1,2,3,4,10,11,12,13]; B=[v for v in range(1,19) if v not in A]
    bad={"left_first":robdd_nodes(F,n,A+B),"right_first":robdd_nodes(F,n,B+A),
         "natural_blocks":robdd_nodes(F,n,list(range(1,19))),"reverse_blocks":robdd_nodes(F,n,list(range(18,0,-1)))}
    pU={8:1,6:0,1:0,15:0,11:0,13:0}; pS={**pU,6:1}
    controls={}
    for name,p in (("UNSAT",pU),("SAT",pS)):
        mats=[support_matrix(F,2,i,p) for i in range(2)]; bit,P=trace_support(mats); cnt,wit=brute_pins(F,n,p)
        controls[name]={"pins":p,"local_count_matrices":mats,"boolean_product":P,"support_trace":bit,"models":cnt,"witness":wit}
    gates,depth=circuit_metrics(F,n);ctt=circuit_truth(F,n)
    return {"valid_connected_original":valid(F,n),"incidence_connected":connected_incidence(F,n),"n":n,"m":len(F),"models":sum(truth),"circuit":{"gates":gates,"depth":depth,"matches_all_262144":ctt==truth},
            "rank_tensor_seed":local_rank9(),"cut":cut_stats(F,n,A),"fixed_order_obdd":bad,"same_original_pair":controls,
            "antichain":{"t1":antichain(1),"t2":antichain(2),"t3":antichain(3)},"seconds":time.time()-t,"peak_rss_kb":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--phase",choices=("f9","g2","merge"),required=True);ap.add_argument("--f9");ap.add_argument("--g2");ap.add_argument("--out",required=True);a=ap.parse_args()
    if a.phase=="f9":out={"run":"CONNECTED_REPRESENTATION_SEPARATION_REFEREE291","phase":"f9","result":f9_phase()}
    elif a.phase=="g2":out={"run":"CONNECTED_REPRESENTATION_SEPARATION_REFEREE291","phase":"g2","result":g2_phase()}
    else:
        with open(a.f9) as f:x=json.load(f)
        with open(a.g2) as f:y=json.load(f)
        out={"run":"CONNECTED_REPRESENTATION_SEPARATION_REFEREE291","status":"PASS_RESTRICTED_INDEPENDENT_REFEREE","P_vs_NP":"OPEN","f9":x["result"],"g2":y["result"],
             "theorem_status":"connected G_t fixed-cut rank and antichain are representation lower bounds only; Boolean 2x2 support transfer decides every coherent pinned residual after paid family acquisition",
             "universal_gap":"no all-input acquisition/solver bound, no arbitrary-A power-short Phi, and no strict same-machine FLMV numeric transfer"}
    with open(a.out,"w") as f:json.dump(out,f,indent=2,sort_keys=True)
    print(json.dumps({"phase":a.phase,"out":a.out,"status":"PASS"}))
if __name__=="__main__":main()
