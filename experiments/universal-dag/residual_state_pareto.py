from itertools import combinations
from collections import defaultdict
from math import comb, log2

# Heuristic query schedules found with deterministic local search, then verified exhaustively.
D4_OPT=[2,25,11,10,3,24,29,17,16,27,20,31,0,8,22,18,1,28,21,6,15,14,12,26,9,4,19,23,13,7,30,5]
D5_OPT=[77,45,78,62,68,39,21,23,47,37,60,70,17,20,79,66,46,38,58,63,71,76,61,69,67,44,64,22,36,57,59,56,19,73,74,72,35,33,43,41,65,75,32,6,16,42,34,55,40,51,18,7,3,2,50,54,49,4,53,5,48,1,12,13,0,15,14,52,9,11,27,30,28,31,25,10,24,29,26,8]
D4_SIGN=[ti*8+pat for pat in range(8) for ti in range(4)]
D4_TRIPLE=list(range(32))

def exact_covers(n):
    triples=list(combinations(range(n),3)); clauses=[]; contains=[[] for _ in range(1<<n)]
    for T in triples:
        for pat in range(8):
            mask=0
            for a in range(1<<n):
                if all(((a>>v)&1)==((pat>>j)&1) for j,v in enumerate(T)): mask|=1<<a
            ci=len(clauses); clauses.append(mask)
            for a in range(1<<n):
                if (mask>>a)&1: contains[a].append(ci)
    FULL=(1<<(1<<n))-1; out=set()
    def rec(cov,chosen):
        if cov==FULL:
            if len(chosen)==8: out.add(tuple(sorted(chosen)))
            return
        if len(chosen)>=8: return
        rem=(~cov)&FULL; a=(rem&-rem).bit_length()-1
        for ci in contains[a]:
            m=clauses[ci]
            if m&cov: continue
            rec(cov|m,chosen+(ci,))
    rec(0,())
    masks=[]
    for F in sorted(out):
        x=0
        for e in F: x|=1<<e
        masks.append(x)
    return len(clauses),masks

def gf2_rank(rows):
    piv={}; r=0
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in piv: x^=piv[p]
            else: piv[p]=x; r+=1; break
    return r

def cut_stats(pm_masks,M,Q):
    Q=set(Q); t=len(Q); pref=0
    for e in Q: pref|=1<<e
    suff=((1<<M)-1)^pref
    groups=defaultdict(lambda:defaultdict(set))
    for fm in pm_masks:
        p=fm&pref; z=fm&suff; groups[p.bit_count()][p].add(z)
    max_total=max_active=max_rank=0; argk=None
    for k in range(9):
        if k>t or 8-k>M-t: continue
        gs=groups.get(k,{})
        residuals={frozenset(v) for v in gs.values()}
        active=len(residuals)
        terminal_sat=(comb(t,k)>len(gs))
        total=active+(1 if terminal_sat else 0)
        col={}; rows=[]
        for vals in gs.values():
            b=0
            for z in vals:
                if z not in col: col[z]=len(col)
                b|=1<<col[z]
            rows.append(b)
        rank=gf2_rank(rows)
        if total>max_total: max_total=total; argk=k
        max_active=max(max_active,active); max_rank=max(max_rank,rank)
    return max_total,max_active,max_rank,argk

def profile(pm_masks,M,order):
    Q=set(); rows=[]
    for t in range(M+1):
        rows.append((t,*cut_stats(pm_masks,M,Q)))
        if t<M: Q.add(order[t])
    return rows

def summarize(name,rows):
    peak_total=max(x[1] for x in rows); peak_active=max(x[2] for x in rows); peak_rank=max(x[3] for x in rows)
    levels=[x[0] for x in rows if x[2]==peak_active]
    cm=sum(log2(max(1,x[2])) for x in rows); area=sum(x[2] for x in rows)
    print(f"{name}: peak_active={peak_active} peak_active_bits={log2(max(1,peak_active)):.9f} peak_total_including_terminal={peak_total} peak_GF2_rank={peak_rank} active_peak_levels={levels} cumulative_log2_active={cm:.9f} active_state_area={area}")

for n in (4,5):
    M,pms=exact_covers(n); print(f"D({n},8): clause_bits={M} unsat_exact_covers={len(pms)}")
    if n==4:
        for name,order in [("D4_sign_round",D4_SIGN),("D4_triple_group",D4_TRIPLE),("D4_optimized_nested",D4_OPT)]: summarize(name,profile(pms,M,order))
        rows=profile(pms,M,D4_OPT); print("D4_OPT_ACTIVE_PROFILE="+",".join(str(x[2]) for x in rows))
    else:
        rows=profile(pms,M,D5_OPT); summarize("D5_optimized_nested",rows)
        t,w,a,r,k=rows[40]; print(f"D5_midcut_t40 active={a} total_including_terminal={w} GF2_rank={r} dominant_k={k}")
        print("D5_OPT_ACTIVE_PROFILE="+",".join(str(x[2]) for x in rows))

print("PARITY_CONTROL: total parity on N bits has exactly 2 nonterminal residual functions at every proper cut, so continuation-state width=2 (one live bit) despite decision depth N.")
print("STATUS: COMPUTATIONAL finite experiment. The candidate schedules are heuristic, not proven globally optimal over all read-once schedules. The cut counts themselves are exact for the displayed schedules. These are read-once/nonadaptive cut-state bounds, not general branching-program or RAM lower bounds.")
