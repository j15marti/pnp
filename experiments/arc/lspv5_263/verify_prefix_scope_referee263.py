#!/usr/bin/env python3
"""No-producer-import verifier for PREFIX_SCOPE_REFEREE263."""
from collections import Counter
from itertools import combinations, product
import hashlib, json
from pathlib import Path

F9P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
F9N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F9=F9P+tuple(tuple(-v for v in c) for c in F9N)
P9={8:0,3:0,7:0,6:0,1:1,5:1}
F15P=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),
      (6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
F15N=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),
      (4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=F15P+tuple(tuple(-v for v in c) for c in F15N)
P15=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))
C9=((3,4,10),);C15=((1,10,11),(2,3,14))

def sat(F,a):
    return all(any(a[abs(l)]==(l>0) for l in c) for c in F)

def models(F,p):
    n=max(abs(l) for c in F for l in c);free=[v for v in range(1,n+1) if v not in p]
    out=[]
    for bits in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,bits))}
        if sat(F,a):out.append(a)
    return out

def rows(F,p,cycles,choices):
    n=max(abs(l) for c in F for l in c)
    free=[v for v in range(1,n+1) if v not in p]
    covered=[];uncovered=[]
    for j,c in enumerate(F):
        (covered if any(abs(l) in p and p[abs(l)]==(l>0) for l in c) else uncovered).append(j)
    counts=Counter()
    for j in covered:
        for l in F[j]:
            if abs(l) not in p:counts[abs(l),l>0]+=1
    prefs={v:(0 if counts[v,True]>counts[v,False] else 1)
           for v in free if counts[v,True]!=counts[v,False]}
    cycids={j for cyc in cycles for j in cyc};out=[]
    for j in uncovered:
        if j in cycids:continue
        lits=[l for l in F[j] if abs(l) not in p]
        out.append(({abs(l) for l in lits},1^((len(lits)&1) if F[j][0]<0 else 0)))
    out.extend(({v},b) for v,b in prefs.items())
    for i,ch in enumerate(choices):
        for j in cycles[i]:
            vs=[abs(l) for l in F[j] if abs(l) not in p]
            if j==ch:
                out.extend(({v},int(F[j][0]>0)) for v in vs)
            else:out.append((set(vs),1))
    return free,out

def affine(F,p,cycles,choices):
    free,eqs=rows(F,p,cycles,choices);ans=[]
    for bits in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,bits))}
        if all(sum(a[v] for v in vs)%2==rhs for vs,rhs in eqs):ans.append(a)
    return ans

def main():
    raw_path=Path(__file__).with_name("prefix_scope_referee263_raw.json")
    raw=json.loads(raw_path.read_text())
    checks=Counter()
    def ck(x,name):
        assert x,name;checks[name]+=1
    ck(raw["P_vs_NP"]=="OPEN","open_status")
    ck(len(models(F9,{}))==70,"f9_root_70")
    ck(len(models(F9,P9))==0,"f9_cube_unsat")
    ck(len(models(F15,P15))==2,"f15_cube_sat2")
    ck(len(affine(F9,P9,C9,()))>0,"f9_outside_parity_consistent")
    for e in C9[0]:ck(len(affine(F9,P9,C9,(e,)))==0,"f9_branch_refuted")
    a15={ch:affine(F15,P15,C15,ch) for ch in product(*C15)}
    ck(len(a15[(10,2)])==0,"f15_failed_leaf")
    ck(len(a15[(10,3)])==len(a15[(10,14)])==1,"f15_sat_siblings")
    ck(sum(map(len,a15.values()))==2,"f15_affine_count")
    enc=[{tuple(a[v] for v in range(1,16)) for a in z} for z in a15.values()]
    ck(len(set().union(*enc))==sum(map(len,enc)),"f15_no_double_count")
    certs=((1,),(11,),(10,2));all_leaves=list(product(*C15))
    uncovered=[z for z in all_leaves if not any(z[:len(c)]==c for c in certs)]
    ck(set(uncovered)=={(10,3),(10,14)},"f15_exact_uncovered_sat")
    certs2=((3,),(4,),(10,));leaves2=list(product(C9[0],C9[0]))
    ck(all(any(z[:len(c)]==c for c in certs2) for z in leaves2),"double_f9_cover")
    pair=0;feas=0
    for i,j in combinations(range(12),2):
        for mi,mj in product((0,1),repeat=2):
            req={};ok=True
            for c,m in ((F9[i],mi),(F9[j],mj)):
                for l in c:
                    v=abs(l);b=int(l>0)^m
                    if v in req and req[v]!=b:ok=False
                    req[v]=b
            pair+=1;feas+=ok
    ck((pair,feas)==(264,172),"pair_extremes")
    px=raw["physical_xor"]
    ck(px["index_steps"]==10 and px["index_adjacent_delta"]==16,"index_reset_trace")
    ck(not px["unqualified_T_ge_D"] and px["amortized_half_D_le_T"],"xor_model_firewall")
    ck(px["binary_enumeration_adjacent_delta"]==120 and
       px["gray_enumeration_adjacent_delta"]==63,"gray_binary")
    result={"run":"VERIFY_PREFIX_SCOPE_REFEREE263","status":"PASS",
            "assertions":sum(checks.values()),"checks":dict(checks),
            "raw_sha256":hashlib.sha256(raw_path.read_bytes()).hexdigest(),
            "P_vs_NP":"OPEN"}
    out=Path(__file__).with_name("verify_prefix_scope_referee263_results.json")
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":main()
