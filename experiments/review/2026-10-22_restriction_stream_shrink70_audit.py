"""RESTRICTION-STREAM-SHRINK70 audit (stdlib only, <30s).
Tests: can restriction-type child streams (fix variables, simplify) meet the
ARC target child length n^beta with Q=n^alpha children?  Counting + random 3-CNF."""
import json, math, random, itertools
random.seed(70)
def cnf(n, ratio=4.2):
    return [tuple(random.choice((1,-1))*v for v in random.sample(range(1,n+1),3)) for _ in range(int(ratio*n))]
def restrict(F, asg):
    out=[]
    for c in F:
        keep=[]; sat=False
        for l in c:
            v=abs(l)
            if v in asg:
                if (l>0)==asg[v]: sat=True; break
            else: keep.append(l)
        if not sat: out.append(tuple(keep))
    return out
rows=[]; fails=0
for n in (64,128,256,512,1024):
    F=cnf(n); m=len(F)
    q=max(1,round(n**0.6)); target=n**0.5
    # a depth-d restriction tree has 2^d leaves; Q=n^0.6 leaves => d=log2 Q
    d=int(math.log2(q)); sizes=[]
    for _ in range(20):
        vs=random.sample(range(1,n+1),d)
        asg={v:random.random()<.5 for v in vs}
        sizes.append(sum(len(c) for c in restrict(F,asg)))
    full=sum(len(c) for c in F)
    # vars needed fixed to reach size n^0.5 (expected untouched-literal mass ~ full*(1-k/n)^3-ish)
    k_needed=n-n**0.5/ (3*4.2)
    rows.append(dict(n=n,Q=q,depth=d,full_size=full,mean_child_size=sum(sizes)/len(sizes),
      target_child=target,beta_eff=math.log(sum(sizes)/len(sizes))/math.log(n),
      vars_to_fix_for_target=round(k_needed),leaves_needed_log2=round(k_needed)))
    if sum(sizes)/len(sizes) < target: fails+=1
for r in rows: assert r['leaves_needed_log2']>r['depth']
print(json.dumps(rows,indent=1)); print("restriction trees reaching target size:",fails)
json.dump(dict(rows=rows,reached_target=fails),open('research/raw/RESTRICTION_STREAM_SHRINK70_raw.json','w'),indent=1)
