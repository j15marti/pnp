#!/usr/bin/env python3
"""REFEREE283: source-disjoint batch tightness and recognition escape."""
from __future__ import annotations
import argparse,collections,itertools,json
from functools import lru_cache
from pathlib import Path

F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),
     (7,11,13),(8,12,14),(9,13,15),(10,14,15))
N15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),
     (7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-x for x in c) for c in N15)

PARALLEL=(((1,2,3),(4,5,6),(7,8,9)),
          ((1,4,7),(2,5,8),(3,6,9)),
          ((1,5,9),(2,6,7),(3,4,8)),
          ((1,6,8),(2,4,9),(3,5,7)))
A9=tuple(c if d<2 else tuple(-x for x in c) for d,pc in enumerate(PARALLEL) for c in pc)

def canonical(F,n):
    if not F or n%3 or 3*len(F)!=4*n:return False
    if len({tuple(sorted(c)) for c in F})!=len(F):return False
    q=collections.Counter()
    for c in F:
        if len(c)!=3 or len({abs(x) for x in c})!=3:return False
        if any(abs(x)<1 or abs(x)>n for x in c):return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        q.update(c)
    return all(q[v]==q[-v]==2 for v in range(1,n+1))

def sat(F,z):return all(any(((z>>(abs(x)-1))&1)==int(x>0) for x in c) for c in F)

def normalize(cs):
    raw=[]
    for c in cs:
        s=frozenset(c)
        if any(-x in s for x in s):continue
        raw.append(s)
    u=set(raw);keep=[c for c in u if not any(d<c for d in u)]
    return tuple(sorted((tuple(sorted(c,key=lambda x:(abs(x),x<0))) for c in keep),key=lambda c:(len(c),c)))

def eliminate(F,v):
    F=normalize(F);p=[c for c in F if v in c];n=[c for c in F if -v in c]
    rest=[c for c in F if v not in c and -v not in c];rs=[]
    for a in p:
      for b in n:rs.append(tuple((set(a)-{v})|(set(b)-{-v})))
    return normalize(rest+rs)

def primal(F,n):
    adj=[set() for _ in range(n+1)]
    for c in F:
      for a,b in itertools.combinations(map(abs,c),2):adj[a].add(b);adj[b].add(a)
    return adj

def greedy(F,n):
    adj=primal(F,n);chosen=[];blocked=set()
    for v in range(1,n+1):
        if v not in blocked:chosen.append(v);blocked.add(v);blocked.update(adj[v])
    return tuple(chosen)

def alpha_exact(F,n):
    adj=primal(F,n);best=()
    def go(cands,cur):
        nonlocal best
        if len(cur)+len(cands)<=len(best):return
        if not cands:
            if len(cur)>len(best):best=tuple(cur)
            return
        v=cands[-1];go(cands[:-1],cur)
        go([u for u in cands[:-1] if u not in adj[v]],cur+[v])
    go(list(range(1,n+1)),[]);return best

def lift(r):
    """Connected affine incidence lift from prior BVE229."""
    out=[]
    for d,pc in enumerate(PARALLEL):
      for li,c in enumerate(pc):
       for t in range(r):
        q=[]
        for x in c:
            layer=(t-1)%r if d==0 and li==0 and x==1 else t
            v=9*layer+x;q.append(v if d<2 else -v)
        out.append(tuple(q))
    return tuple(out)

def components(F,n):
    a=primal(F,n);seen=set();out=[]
    for s in range(1,n+1):
      if s in seen:continue
      stack=[s];seen.add(s);q=[]
      while stack:
        v=stack.pop();q.append(v)
        for w in a[v]:
          if w not in seen:seen.add(w);stack.append(w)
      out.append(tuple(sorted(q)))
    return out

def product_A9(t):
    return tuple(tuple((1 if x>0 else -1)*(abs(x)+9*j) for x in c) for j in range(t) for c in A9)

def scramble_product(t):
    F=product_A9(t);perms=((3,1,8,5,2,9,4,7,6),(9,8,7,6,5,4,3,2,1),(2,5,1,9,7,3,8,6,4))
    maps={}
    for j in range(t):
        p=perms[j%len(perms)]
        for i in range(1,10):maps[9*j+i]=9*((j+1)%t)+p[i-1] if t>1 else p[i-1]
    G=[tuple((1 if x>0 else -1)*maps[abs(x)] for x in reversed(c)) for c in reversed(F)]
    return tuple(G)

def recognize_k9_product(F,n):
    """Paid component recognizer plus constant 512-row local exact solver."""
    if not canonical(F,n):return None
    comps=components(F,n);z=0;trials=0
    for V in comps:
        if len(V)!=9:return None
        a=primal(F,n)
        if any(len(a[v]&set(V))!=8 for v in V):return None
        local=[c for c in F if abs(c[0]) in V]
        if len(local)!=12 or any(any(abs(x) not in V for x in c) for c in local):return None
        found=None
        for bits in range(512):
            trials+=1;assignment={v:(bits>>i)&1 for i,v in enumerate(V)}
            if all(any(assignment[abs(x)]==int(x>0) for x in c) for c in local):found=assignment;break
        if found is None:return None
        for v,b in found.items():z|=b<<(v-1)
    assert sat(F,z)
    return {"components":len(comps),"local_trials":trials,"witness":z}

def lift_alpha_formula(r):return 1 if r==1 else r+r//2

def lift_alpha_dp(F,r):
    """Independent local-subset cycle DP, deliberately separate from the closed form."""
    adj=primal(F,9*r);opts=[]
    for j in range(r):
      V=tuple(range(9*j+1,9*j+10));local=[]
      for mask in range(1<<9):
        S=tuple(V[i] for i in range(9) if (mask>>i)&1)
        if all(v not in adj[u] for u,v in itertools.combinations(S,2)):local.append(S)
      opts.append(local)
    best=0
    for first in opts[0]:
      dp={first:len(first)}
      for j in range(1,r):
        nd={}
        for cur in opts[j]:
          val=max((q for prev,q in dp.items() if all(v not in adj[u] for u in prev for v in cur)),default=-10**9)+len(cur)
          nd[cur]=val
        dp=nd
      for last,q in dp.items():
        if all(v not in adj[u] for u in last for v in first):best=max(best,q)
    return best

def matching_weight(F):
    total=0
    for sign in (1,-1):
      ids=[i for i,c in enumerate(F) if (1 if c[0]>0 else -1)==sign]
      @lru_cache(None)
      def go(mask):
        if not mask:return 0
        i=(mask&-mask).bit_length()-1;best=go(mask&~(1<<i))
        for j in range(i+1,len(ids)):
          if (mask>>j)&1:
            w=len(set(map(abs,F[ids[i]]))&set(map(abs,F[ids[j]])))
            best=max(best,w+go(mask&~(1<<i)&~(1<<j)))
        return best
      total+=go((1<<len(ids))-1)
    return total

def obdd_counts(F,n):
    costs={};full=(1<<n)-1
    for mask in range(1<<n):
      A=[i for i in range(n) if (mask>>i)&1];R=[i for i in range(n) if not(mask>>i)&1];S=set()
      for aa in range(1<<len(A)):
        sig=0
        for rr in range(1<<len(R)):
          z=sum(((aa>>k)&1)<<i for k,i in enumerate(A))+sum(((rr>>k)&1)<<i for k,i in enumerate(R));sig|=sat(F,z)<<rr
        S.add(sig)
      for p,v in enumerate(R):
        q=0
        for sig in S:
          lo=hi=0
          for y in range(1<<(len(R)-1)):
            i=(y&((1<<p)-1))|((y>>p)<<(p+1));lo|=((sig>>i)&1)<<y;hi|=((sig>>(i|1<<p))&1)<<y
          q+=lo!=hi
        costs[mask,v]=q
    @lru_cache(None)
    def dp(mask,worst=False):
      if mask==full:return 0
      vals=[costs[mask,v]+dp(mask|1<<v,worst) for v in range(n) if not(mask>>v)&1]
      return max(vals) if worst else min(vals)
    mask=natural=0
    for v in range(n):natural+=costs[mask,v];mask|=1<<v
    return {"best":dp(0),"natural":natural,"worst":dp(0,True)}

def su_modes(F):
    n=max(abs(x) for c in F for x in c);checks=0
    for A,B in itertools.combinations(F,2):
      same=any(abs(x)==abs(y) and (x>0)==(y>0) for x in A for y in B);opp=any(abs(x)==abs(y) and (x>0)!=(y>0) for x in A for y in B)
      pred=(not opp,not same,not same,not opp);act=[False]*4
      for z in range(1<<n):
        AS=all(((z>>(abs(x)-1))&1)==int(x>0) for x in A);AU=all(((z>>(abs(x)-1))&1)!=int(x>0) for x in A)
        BS=all(((z>>(abs(x)-1))&1)==int(x>0) for x in B);BU=all(((z>>(abs(x)-1))&1)!=int(x>0) for x in B)
        act=[a or b for a,b in zip(act,(AS and BS,AS and BU,AU and BS,AU and BU))]
      assert tuple(act)==pred;checks+=4
    return checks

def batch_project(F,I):
    G=F
    for v in I:G=eliminate(G,v)
    return G

def projection_rows(F,n,I,G):
    R=[v for v in range(1,n+1) if v not in I];rows=0
    for bits in itertools.product((0,1),repeat=len(R)):
      a=dict(zip(R,bits));got=all(any(a[abs(x)]==int(x>0) for x in c) for c in G);want=False
      for eb in itertools.product((0,1),repeat=len(I)):
        z=sum(b<<(v-1) for v,b in list(zip(R,bits))+list(zip(I,eb)));want|=sat(F,z)
      assert got==want;rows+=1
    return rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",required=True);a=ap.parse_args()
    fixtures={"Y6":(Y6,6),"F9":(F9,9),"F15":(F15,15),"A9":(A9,9)};forward={};truth=0
    for name,(F,n) in fixtures.items():
      assert canonical(F,n);models=sum(sat(F,z) for z in range(1<<n));truth+=1<<n
      forward[name]={"n":n,"m":len(F),"models":models,"private_gates":3*len(F)-1,"depth":2+(len(F)-1).bit_length()}
    assert [forward[x]["models"] for x in ("Y6","F9","F15","A9")]==[20,70,1032,18]
    E=primal(A9,9);assert sum(len(x) for x in E)//2==36 and all(len(E[v])==8 for v in range(1,10))
    alphaA=alpha_exact(A9,9);assert len(alphaA)==1
    products=[]
    for t in range(1,6):
      F=product_A9(t);assert canonical(F,9*t);g=greedy(F,9*t)
      S=scramble_product(t);rec=recognize_k9_product(S,9*t)
      assert len(g)==t and rec is not None and sat(S,rec["witness"])
      products.append({"t":t,"n":9*t,"m":12*t,"components":len(components(F,9*t)),"greedy_batch":g,"alpha":t,"scrambled_recognition":rec,"witness_check":sat(F,sum(((78>>i)&1)<<(9*j+i) for j in range(t) for i in range(9)))})
    lifts=[]
    for r in range(1,13):
      F=lift(r);assert canonical(F,9*r);assert len(components(F,9*r))==1
      dp=lift_alpha_dp(F,r);want=lift_alpha_formula(r);assert dp==want
      lifts.append({"r":r,"n":9*r,"m":12*r,"connected":True,"alpha":dp,"formula":want,"lex_greedy":len(greedy(F,9*r))})
    # Exact simultaneous projections on two independent source sets.
    IF9=greedy(F9,9);GF9=batch_project(F9,IF9);IA=(1,);GA=batch_project(A9,IA)
    projrows=projection_rows(F9,9,IF9,GF9)+projection_rows(A9,9,IA,GA)
    assert IF9==(1,4) and projrows==384
    # Same-original opposite-label A9 control.
    common={2:0,3:0,4:0,5:1,6:1,7:1,8:0,9:0};siblings=[]
    for x1 in (0,1):
      q=0
      for z in range(1<<9):q+=sat(A9,z) and ((z&1)==x1) and all(((z>>(v-1))&1)==b for v,b in common.items())
      siblings.append(q)
    assert siblings==[0,1]
    obdd={"F9":obdd_counts(F9,9),"A9":obdd_counts(A9,9)}
    assert obdd=={"F9":{"best":52,"natural":66,"worst":80},"A9":{"best":42,"natural":43,"worst":50}}
    W=matching_weight(A9);assert W==6
    malformed=[(),((1,1,2),),((1,-2,3),),((1,2,3),),A9+(A9[0],),((1,2,3),(1,2,4))]
    assert all(not canonical(x,max([abs(v) for c in x for v in c],default=3)) for x in malformed)
    result={"run":"AFFINE-BATCH-TIGHTNESS-REFEREE283","timestamp_pst":"2026-11-01 23:48","status":"PROVED_EXACT_RESTRICTED_PLUS_COMPUTATIONAL","P_vs_NP":"OPEN",
      "obstruction":"A guaranteed source-disjoint projection batch is a strong independent set in the source-clause hypergraph. The all-input n/9 guarantee is tight, yet tightness does not imply decision hardness because the extremal family has a paid direct recognizer and explicit witness.",
      "theorem":["The signed affine-plane A9 original is valid canonical, connected, SAT with 18 models, and has primal graph K9; hence its maximum source-disjoint pivot batch is one.","For t disjoint renamed A9 copies, alpha=t=n/9, so no all-input theorem can guarantee more than n/9 source-disjoint pivots.","For the prior connected affine incidence lift F_r, alpha=1 for r=1 and alpha=r+floor(r/2) for r>=2. Thus this connected family admits asymptotically n/6, but still only a linear one-phase batch."],
      "proof":"A9 is the resolvable STS(9): every pair of variables occurs in exactly one source clause, so the primal graph is K9. In the cyclic lift, each layer is K9 except the two nonedges {p0,p1},{p0,p2}; a doubled layer must select p0 and one of p1,p2, and adjacent doubled layers conflict through the shifted clause. Hence doubled layers form an independent set of a cycle, giving at most floor(r/2), attained by alternating doubled layers and a safe singleton elsewhere.",
      "fixtures":forward,"truth_rows":truth,"A9":{"clauses":A9,"primal_edges":36,"alpha_witness":alphaA,"matching_weight":W,"matched_architecture_gates":35-W,"OBDD":obdd["A9"],"same_original_common_pins":common,"x1_sibling_models":siblings},
      "F9_controls":{"models":70,"private_gates":35,"depth":6,"OBDD":obdd["F9"],"greedy_batch":IF9,"projected_clauses":len(GF9),"projected_literals":sum(map(len,GF9)),"SU_modes":su_modes(F9)},
      "product_tightness":products,"connected_lifts":lifts,"projection_truth_rows":projrows,"malformed_rejected":6,
      "falsified":["every canonical original has a source-disjoint pivot batch strictly larger than n/9","tightness of the n/9 batch bound implies exponential decision work","a 35-gate evaluator or 42/52-node best OBDD is necessary for recognizing the affine extremal family"],
      "recognition_escape":{"algorithm":"authenticate canonical primal components; if every component is K9, solve each constant nine-variable component by at most 512 source evaluations and verify the joined source witness. Scrambled names, blocks, clauses and literal orders are allowed.","time":"O(N log N) under sorting-based component acquisition plus at most 512 evaluations per nine-variable component, or polynomial repeated scans","peak":"O(N) cached source/component map, or logarithmic live indices with paid repeated scans","decision":"SAT without constructing any projection batch or using a SAT-label oracle"},
      "charged_work":{"recurrence":"W_D=grammar+source/index/head+incidence/primal acquisition+independent-set policy and failures+projection/resolvent+semantic/proof/GE+cache/replay+child/output/bit+guest DELAY/COPY/RECOMP+sum over evaluated successors","peak":"maximum co-live source, incidence/primal graph or repeated-scan indices, selected pivots, resolvent/provenance buffers, semantic cache/proof, ancestors, children, index/head and guest state","offline":"OBDD all-order DP, alpha DP and XOR traces are experimental unless explicitly acquired and charged by the SAT machine"},
      "exact_gap":"The n/9 one-phase guarantee is optimal for source-disjoint batches but is only an upper-bound technique. Overlapping pivots, factoring, treewidth/affine/Horn/2SAT recognition and arbitrary correct deciders remain available. No polynomial aggregate-work controller, arbitrary-A power-short Phi(A), or strict same-machine FLMV numerical transfer is proved.",
      "literature_queries":["Steiner triple system affine plane order 3 resolvable STS(9)","rank-three hypergraph strong independent set maximum degree bound","3-uniform 4-regular hypergraph matching n/9 tight affine plane","GitHub j15marti/pnp Steiner triple system; affine plane order 3; source-disjoint projection","GitHub org:openai Steiner triple system; hypergraph independent set"],
      "literature_findings":{"design":"STS(9) is the unique affine plane of order three with four parallel classes","hypergraph":"rank-three strong independent-set bounds identify complete hypergraphs on 2Delta+1 vertices as the exceptional extremal obstruction; A9 realizes Delta=4 and K9","project":"AFFINE-LIFT-BVE229 already constructed the connected cyclic lift; SOURCE-DISJOINT-BATCH-PROJECTION321 supplied the n/9 compiler. REFEREE283 adds exact batch tightness and recognition escape.","openai":"one unrelated mathematical Steiner-system preprint hit and zero hypergraph-independent-set code hits; absence is not novelty evidence"}}
    Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","truth_rows":truth,"A9_models":18,"A9_alpha":1,"product_alpha":[x["alpha"] for x in products],"lift_alpha":[x["alpha"] for x in lifts],"OBDD":obdd,"same_original_models":siblings,"projection_rows":projrows,"P_vs_NP":"OPEN"},indent=2))
if __name__=="__main__":main()
