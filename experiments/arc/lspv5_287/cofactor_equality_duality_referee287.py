#!/usr/bin/env python3
"""REFEREE287: cofactor equality is not an extra necessary decision on F_G=G and Z6.

The theorem is an exact promise-family duality and paid component escape, not an
all-input SAT algorithm.  Residual circuits remain noncanonical.
"""
from __future__ import annotations
import argparse, collections, functools, itertools, json
from pathlib import Path

F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
Z6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),
     (7,11,13),(8,12,14),(9,13,15),(10,14,15))
N15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),
     (7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-x for x in c) for c in N15)

def canonical(F,n):
    if not F or n%3 or 3*len(F)!=4*n:return False
    if len({tuple(sorted(c)) for c in F})!=len(F):return False
    q=collections.Counter()
    for c in F:
        if len(c)!=3 or len({abs(x) for x in c})!=3:return False
        if any(type(x) is not int or not x or abs(x)>n for x in c):return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        q.update(c)
    return all(q[v]==q[-v]==2 for v in range(1,n+1))

def shift(F,k):return tuple(tuple((1 if x>0 else -1)*(abs(x)+k) for x in c) for c in F)
def sat(F,a):return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)
def ass(n,z):return {i:(z>>(i-1))&1 for i in range(1,n+1)}
def model_count(F,n,p):
    free=[v for v in range(1,n+1) if v not in p];q=0
    for z in range(1<<len(free)):
        a=dict(p);a.update((v,(z>>i)&1) for i,v in enumerate(free));q+=sat(F,a)
    return q

def sibling_audit(G,ng,gpins=()):
    """Exhaustive h0/h1 comparison in G disjoint Z6, pivot first Z name."""
    F=G+shift(Z6,ng);p0=dict(gpins);p1=dict(gpins);p0[ng+1]=0;p1[ng+1]=1
    fixed=set(p0);free=[v for v in range(1,ng+7) if v not in fixed]
    c0=c1=both=o0=o1=0;rows=0
    for z in range(1<<len(free)):
        a0=dict(p0);a0.update((v,(z>>i)&1) for i,v in enumerate(free));a1=dict(a0);a1[ng+1]=1
        f0=sat(F,a0);f1=sat(F,a1);c0+=f0;c1+=f1;both+=f0 and f1;o0+=f0 and not f1;o1+=f1 and not f0;rows+=1
    gm=model_count(G,ng,dict(gpins))
    assert (c0,c1,both,o0,o1)==(9*gm,9*gm,4*gm,5*gm,5*gm)
    return {"G_models":gm,"cofactor0_models":c0,"cofactor1_models":c1,
            "shared_models":both,"only0":o0,"only1":o1,"equal":o0+o1==0,
            "both_current_SAT":bool(c0) and bool(c1),"future_rows":rows}

def components(F):
    adj=collections.defaultdict(set);vs={abs(x) for c in F for x in c}
    for c in F:
        u=[abs(x) for x in c]
        for x in u:adj[x].update(set(u)-{x})
    seen=set();out=[]
    for s in sorted(vs):
        if s in seen:continue
        st=[s];seen.add(s);C=[]
        while st:
            x=st.pop();C.append(x)
            for y in adj[x]:
                if y not in seen:seen.add(y);st.append(y)
        W=set(C);out.append((tuple(sorted(C)),tuple(c for c in F if all(abs(x) in W for x in c))))
    return out

def is_z6_component(C,F):
    if len(C)!=6 or len(F)!=8:return False
    target={tuple(sorted(c)) for c in Z6}
    for perm in itertools.permutations(C):
        mp={perm[i]:i+1 for i in range(6)}
        got={tuple(sorted((1 if x>0 else -1)*mp[abs(x)] for x in c)) for c in F}
        if got==target:return True
    return False

def recognize_product(F,n,pivot):
    if not canonical(F,n):return None
    cs=components(F)
    hits=[i for i,(C,H) in enumerate(cs) if pivot in C and is_z6_component(C,H)]
    if len(hits)!=1:return None
    z=hits[0];G=tuple(c for i,(_,H) in enumerate(cs) if i!=z for c in H)
    gv=sorted({abs(x) for c in G for x in c});mp={v:i+1 for i,v in enumerate(gv)}
    Gn=tuple(tuple((1 if x>0 else -1)*mp[abs(x)] for x in c) for c in G)
    return {"components":len(cs),"G_n":len(gv),"G":Gn,"recognized_Z_names":list(cs[z][0]),
            "source_clause_reads":len(F),"literal_reads":3*len(F),"constant_isomorphism_trials_max":720}

def compile_private(F,n):
    gates=[];outs=[];depth={v:0 for v in range(1,n+1)}
    def add(op,x,y):
        z=n+len(gates)+1;gates.append((z,op,x,y));depth[z]=1+max(depth[abs(x)],depth[abs(y)]);return z
    for c in F:outs.append(add("OR",add("OR",c[0],c[1]),c[2]))
    while len(outs)>1:outs=[add("AND",outs[i],outs[i+1]) if i+1<len(outs) else outs[i] for i in range(0,len(outs),2)]
    return gates,outs[0],depth[outs[0]]

def eval_circuit(gates,root,a):
    b=dict(a)
    for z,op,x,y in gates:
        X=b[abs(x)] if x>0 else 1-b[abs(x)];Y=b[abs(y)] if y>0 else 1-b[abs(y)]
        b[z]=int((X or Y) if op=="OR" else (X and Y))
    return bool(b[root])

def obdd_extrema(F,n):
    tab=tuple(int(sat(F,ass(n,z))) for z in range(1<<n));cost={}
    for S in range(1<<n):
        pre=[i for i in range(n) if S>>i&1]
        for v in range(n):
            if S>>v&1:continue
            rest=[i for i in range(n) if not(S>>i&1) and i!=v];pairs=set()
            for pa in range(1<<len(pre)):
                base=sum(((pa>>k)&1)<<i for k,i in enumerate(pre));lo=hi=0
                for rb in range(1<<len(rest)):
                    z=base+sum(((rb>>k)&1)<<i for k,i in enumerate(rest));lo|=tab[z]<<rb;hi|=tab[z|1<<v]<<rb
                if lo!=hi:pairs.add((lo,hi))
            cost[S,v]=len(pairs)
    full=(1<<n)-1
    @functools.lru_cache(None)
    def dp(S,worst=False):
        if S==full:return 0
        q=[cost[S,v]+dp(S|1<<v,worst) for v in range(n) if not(S>>v&1)]
        return max(q) if worst else min(q)
    S=natural=0
    for v in range(n):natural+=cost[S,v];S|=1<<v
    return {"best":dp(0),"natural":natural,"worst":dp(0,True)}

def restrict(F,p):
    R=[]
    for c in F:
        if any(abs(x) in p and p[abs(x)]==int(x>0) for x in c):continue
        q=tuple(x for x in c if abs(x) not in p)
        if not q:return None
        R.append(q)
    return R

def dpll(F,p):
    R=restrict(F,p);stats={"nodes":0,"literal_inspections":0,"forced":0,"branches":0}
    def rec(C,a):
        stats["nodes"]+=1
        while True:
            unit=None;new=[]
            for c in C:
                satc=False;q=[]
                for x in c:
                    stats["literal_inspections"]+=1
                    if abs(x) in a:
                        if a[abs(x)]==int(x>0):satc=True;break
                    else:q.append(x)
                if satc:continue
                if not q:return False
                if len(q)==1 and unit is None:unit=q[0]
                new.append(tuple(q))
            C=new
            if unit is None:break
            v=abs(unit);val=int(unit>0)
            if v in a and a[v]!=val:return False
            if v not in a:a=dict(a);a[v]=val;stats["forced"]+=1
        if not C:return True
        v=abs(C[0][0]);stats["branches"]+=1
        for val in (1,0):
            b=dict(a);b[v]=val
            if rec(C,b):return True
        return False
    ans=False if R is None else rec(R,dict(p))
    return {"SAT":ans,**stats}

def su_modes(F,n):
    q=0
    for i,j in itertools.combinations(range(len(F)),2):
        for a,b in itertools.product((0,1),repeat=2):
            def mode(x,c,m):
                z=[x[abs(l)]==int(l>0) for l in c];return all(z) if m else not any(z)
            brute=any(mode(ass(n,z),F[i],a) and mode(ass(n,z),F[j],b) for z in range(1<<n))
            req={};good=True
            for c,m in ((F[i],a),(F[j],b)):
                for x in c:
                    v=int(x>0) if m else int(x<0)
                    if abs(x) in req and req[abs(x)]!=v:good=False
                    req[abs(x)]=v
            assert brute==good;q+=1
    return q

def malformed():
    bad=[(),((1,1,2),),((1,-2,3),),((1,2,3),),F9+(F9[0],),((1,2,3),(1,2,4))]
    return sum(not canonical(F,max([abs(x) for c in F for x in c],default=3)) for F in bad)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",required=True);a=ap.parse_args()
    assert all((canonical(F,n) for F,n in ((F9,9),(Y6,6),(Z6,6),(F15,15))))
    F=F9+shift(Z6,9);assert canonical(F,15)
    root=sibling_audit(F9,9);satpins={1:0,4:0,5:1,8:0};unspins={1:1,4:0,5:1,8:0}
    satpair=sibling_audit(F9,9,satpins.items());unspair=sibling_audit(F9,9,unspins.items())
    assert root=={"G_models":70,"cofactor0_models":630,"cofactor1_models":630,"shared_models":280,"only0":350,"only1":350,"equal":False,"both_current_SAT":True,"future_rows":16384}
    assert satpair["G_models"]==7 and not satpair["equal"] and unspair["G_models"]==0 and unspair["equal"]
    y6=sibling_audit(Y6,6)
    f15pins=[]
    for q in ((1,0,0,0,1,1,1,1,0),(0,0,0,0,1,1,1,1,0)):
        f15pins.append(sibling_audit(F15,15,dict(zip(range(7,16),q)).items()))
    assert [x["G_models"] for x in f15pins]==[2,0]
    rec=recognize_product(F,15,10);assert rec and rec["G_n"]==9 and rec["G"]==F9
    gates,rt,dep=compile_private(F,15);ones=0
    for z in range(1<<15):
        x=ass(15,z);v=eval_circuit(gates,rt,x);assert v==sat(F,x);ones+=v
    assert (len(gates),dep,ones)==(59,7,1260)
    f9g,r9,d9=compile_private(F9,9);assert (len(f9g),d9)==(35,6)
    for z in range(512):assert eval_circuit(f9g,r9,ass(9,z))==sat(F9,ass(9,z))
    obdd=obdd_extrema(F9,9);assert obdd=={"best":52,"natural":66,"worst":80}
    dpll_full={"SAT_z0":dpll(F,{**satpins,10:0}),"SAT_z1":dpll(F,{**satpins,10:1}),
               "UNSAT_z0":dpll(F,{**unspins,10:0}),"UNSAT_z1":dpll(F,{**unspins,10:1})}
    dpll_G={"SAT":dpll(F9,satpins),"UNSAT":dpll(F9,unspins)}
    assert all(dpll_full[k]["SAT"]==(not k.startswith("UNSAT")) for k in dpll_full)
    bad=malformed();assert bad==6
    out={"run":"COFACTOR-EQUALITY-DUALITY-REFEREE287","timestamp_pacific":"2026-11-02T03:48:00-08:00",
      "status":"PROVED_EXACT_PROMISE_DUALITY_AND_PAID_RECOGNITION_ESCAPE_PLUS_COMPUTATIONAL","P_vs_NP":"OPEN",
      "theorem":"For any valid canonical G and F_G=G disjoint-union Z6, with h0,h1 the unequal nonempty equal-9 Z6 cofactors: SAT(F_G|z1=b) iff SAT(G) for both b; equality and either directional dominance of the two sibling continuation functions iff UNSAT(G). Hence on this promise semantic equality is exactly the complement of either current SAT label, not an additional mandatory computation. Paid component/template recognition routes one direct decision to G and reuses the label for both siblings; it does not make deciding arbitrary G easy.",
      "falsifiers":["coNP-hard cofactor equality adds independent mandatory work beyond deciding one sibling on the reduction family",
        "equal model counts and anonymous profiles justify semantic merging","every solver of both sibling decisions must acquire exact continuation equality",
        "the disconnected product promise yields a connected or all-input SAT lower bound"],
      "charged_escape":{"recognition":"grammar plus incidence components plus constant-size Z6 isomorphism; O(N) source work with at most 720 constant gadget permutations",
        "decision":"one paid arbitrary fallback A(G), then reuse its one-bit current label for both z1 siblings; no equality/dominance query",
        "constructive_caveat":"a SAT witness or complete UNSAT proof for the original remains separately charged; decision reuse alone does not output either",
        "recurrence":"T_product <= T_grammar+T_components+T_Z6_recognize+T_A(G)+O(1); S_peak <= S_A(G)+O(N) explicit indices, or streamed recognition with its declared head costs",
        "global_ledger":"all failed policies/switches, source/index/head, circuit/OBDD/equality/proof/GE, cache/replay, child/output, DELAY/COPY/RECOMP and simultaneous ancestors remain charged"},
      "F9_Z6":{"root":root,"same_original_G_SAT_pins":satpair,"same_original_G_UNSAT_pins":unspair,"recognition":rec,
        "forward":{"gates":len(gates),"depth":dep,"truth_rows":1<<15,"models":ones},"direct_source_DPLL":dpll_full,"component_G_DPLL":dpll_G},
      "F9":{"models":model_count(F9,9,{}),"forward":{"gates":35,"depth":6,"truth_rows":512},"obdd":obdd,"su_modes":su_modes(F9,9)},
      "Y6_Z6":y6,"F15_Z6_same_original_pins":f15pins,"malformed_rejected":bad,
      "exact_gap":"The escape invokes an arbitrary exact decision method on G and proves no polynomial bound for it. It does not cover connected products, all canonical originals, arbitrary-A power shortening, or a strict same-machine FLMV transfer.",
      "inherited_not_replayed":["U198/V198","saturated-cycle affine terminal"]}
    Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"run":out["run"],"root":root,"satpair":satpair,"unspair":unspair,"forward":out["F9_Z6"]["forward"],"dpll":dpll_full,"ok":True},sort_keys=True))
if __name__=="__main__":main()
