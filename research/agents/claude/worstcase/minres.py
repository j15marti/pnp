# Exact minimum resolution-DAG refutation size (number of resolution steps) for tiny 3-CNFs.
# W_Res(n) over width-exactly-3 clause sets on n variables, restricted to MINIMAL UNSAT sets
# (min size is monotone in the clause set, so the max is attained there). Level-BFS over derived-clause sets.
import itertools, random, json, sys, time
def clauses3(n):
    out=[]
    for vs in itertools.combinations(range(1,n+1),3):
        for sg in itertools.product((1,-1),repeat=3):
            out.append(frozenset(v*s for v,s in zip(vs,sg)))
    return out
def sat(cl,n):
    for m in range(1<<n):
        if all(any(((m>>(abs(l)-1))&1)==(l>0) for l in c) for c in cl): return True
    return False
def res(a,b):
    r=[]
    for l in a:
        if -l in b:
            c=(a|b)-{l,-l}
            if not any(-x in c for x in c): r.append(frozenset(c))
    return r
def minsteps(F,limit=12,tmax=8):
    t0=time.time(); F=list(F); start=frozenset()
    level={start}
    for k in range(limit+1):
        nxt=set()
        for D in level:
            if time.time()-t0>tmax: return None
            pool=F+list(D)
            if frozenset() in D: return k
            for a,b in itertools.combinations(pool,2):
                for c in res(a,b):
                    if c not in D and c not in F: nxt.add(D|{c})
        # check goal
        for D in nxt:
            if frozenset() in D: return k+1
        level=nxt
    return None
def minimal_unsat(cl,n,rng):
    S=list(cl); rng.shuffle(S)
    cur=list(S)
    for c in S:
        t=[x for x in cur if x!=c]
        if not sat(t,n): cur=t
    return cur
if __name__=="__main__":
    n=int(sys.argv[1]); N=int(sys.argv[2]); rng=random.Random(n*1000+N)
    allc=clauses3(n); res_=[]; seen=set(); t0=time.time()
    for _ in range(N):
        if time.time()-t0>20: break
        # random UNSAT set: random subset of size ~ 2^3*C(n,3)*0.8 then shrink
        sub=[c for c in allc if rng.random()<0.7]
        if sat(sub,n): continue
        m=minimal_unsat(sub,n,rng); key=frozenset(m)
        if key in seen: continue
        seen.add(key)
        s=minsteps(m); res_.append((len(m),s))
    print(json.dumps({"n":n,"samples":res_,"max_steps":max([s for _,s in res_ if s is not None],default=None),
      "timeouts":sum(1 for _,s in res_ if s is None)}))
