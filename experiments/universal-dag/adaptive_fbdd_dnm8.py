from itertools import combinations
from functools import lru_cache
from math import comb, log1p
import math, random, csv, sys

# ADAPTIVE-FBDD1
# Promise classifier D(n,8): simple genuine 3-CNFs with exactly eight selected clauses.
# Positive output here means UNSAT. For n=4,8-clause UNSAT instances are the 272
# perfect matchings of Q4 in the falsifying-subcube representation.
#
# This is a heuristic FBDD constructor. It proves only an upper bound for the
# displayed construction. Exact FBDD minimization is not claimed.

WEIGHTS_D4=[
-0.0278966816915725,2.008763182738552,-0.484199628623328,
2.1618798864594315,-0.35472743217030567,0.14796949470522103,
0.045590696483015364,-2.6128203960682903]
WEIGHTS_D5=[
0.791443446086018,2.2889423302178162,1.3341324941879247,
2.468444091930575,-0.7920112233312793,0.08403898263937748,
0.47104771163657677,-2.249660938626224]

def exact_covers(n):
    triples=list(combinations(range(n),3))
    cm=[]; contains=[[] for _ in range(1<<n)]
    for T in triples:
        for pat in range(8):
            m=0
            for a in range(1<<n):
                if all(((a>>v)&1)==((pat>>j)&1) for j,v in enumerate(T)):
                    m|=1<<a
            ci=len(cm); cm.append(m)
            for a in range(1<<n):
                if (m>>a)&1: contains[a].append(ci)
    FULL=(1<<(1<<n))-1; out=set()
    def rec(cov,chosen):
        if cov==FULL:
            if len(chosen)==8:
                x=0
                for e in chosen: x|=1<<e
                out.add(x)
            return
        if len(chosen)>=8: return
        rem=(~cov)&FULL
        a=(rem&-rem).bit_length()-1
        for ci in contains[a]:
            if cm[ci]&cov: continue
            rec(cov|cm[ci],chosen+(ci,))
    rec(0,())
    return sorted(out)

def synth(n,weights):
    pms=exact_covers(n); M=8*comb(n,3)
    var1=[]
    for e in range(M):
        b=0
        for i,pm in enumerate(pms):
            if (pm>>e)&1: b|=1<<i
        var1.append(b)
    ALL=(1<<len(pms))-1
    uniq={}; nodes={}; memo={}; nextid=2

    def rec(rem,need,pos):
        nonlocal nextid
        sk=(rem,need,pos)
        if sk in memo: return memo[sk]
        r=rem.bit_count()
        if need<0 or need>r: return 0
        pc=pos.bit_count(); total=comb(r,need)
        if pc==0: return 0
        if pc==total: return 1

        best=None; bestkey=None; x=rem
        while x:
            l=x&-x; e=l.bit_length()-1; x-=l
            p1=pos&var1[e]; p0=pos^p1
            d0=comb(r-1,need) if 0<=need<=r-1 else 0
            d1=comb(r-1,need-1) if 0<=need-1<=r-1 else 0
            c0=p0.bit_count(); c1=p1.bit_count()
            mix0=1 if 0<c0<d0 else 0
            mix1=1 if 0<c1<d1 else 0
            a0=d0 if mix0 else 0; a1=d1 if mix1 else 0
            m0=min(c0,d0-c0) if d0 else 0
            m1=min(c1,d1-c1) if d1 else 0
            feats=[
                log1p(a0+a1),log1p(max(a0,a1)),
                log1p(m0+m1),log1p(max(m0,m1)),
                log1p(abs(c0-c1)),-(mix0+mix1),-min(c0,c1),c0+c1]
            score=sum(w*f for w,f in zip(weights,feats))
            key=(score,e)
            if bestkey is None or key<bestkey:
                bestkey=key; best=e

        rem2=rem&~(1<<best)
        p1=pos&var1[best]; p0=pos^p1
        lo=rec(rem2,need,p0)
        hi=rec(rem2,need-1,p1)
        if lo==hi:
            ans=lo
        else:
            nk=(best,lo,hi)
            if nk in uniq: ans=uniq[nk]
            else:
                ans=nextid; nextid+=1
                uniq[nk]=ans; nodes[ans]=nk
        memo[sk]=ans
        return ans

    root=rec((1<<M)-1,8,ALL)

    @lru_cache(None)
    def labels(v):
        if v<2: return 0
        e,lo,hi=nodes[v]
        below=labels(lo)|labels(hi)
        assert not ((below>>e)&1), ("read-once violation",v,e)
        return below|(1<<e)

    @lru_cache(None)
    def depth(v):
        if v<2: return 0
        _,lo,hi=nodes[v]
        return 1+max(depth(lo),depth(hi))

    labels(root)
    return pms,root,nodes,depth(root),len(memo)

def evalbp(root,nodes,x):
    u=root; d=0
    while u>=2:
        e,lo,hi=nodes[u]
        u=hi if (x>>e)&1 else lo
        d+=1
    return u,d

def main():
    outdir=sys.argv[1] if len(sys.argv)>1 else "."
    for n,w,expected_nodes,expected_depth in [
        (4,WEIGHTS_D4,301,17),
        (5,WEIGHTS_D5,2248,28)]:
        pms,root,nodes,depth,nstates=synth(n,w)
        assert len(nodes)==expected_nodes
        assert depth==expected_depth
        for pm in pms:
            y,_=evalbp(root,nodes,pm)
            assert y==1
        print(f"D({n},8) exact_covers={len(pms)} internal_nodes={len(nodes)} depth={depth} construction_states={nstates}")
        if n==4:
            path=outdir+"/d4_fbdd_301.csv"
            with open(path,"w",newline="") as f:
                wr=csv.writer(f); wr.writerow(["id","var","lo","hi"])
                for i in sorted(nodes):
                    e,lo,hi=nodes[i]; wr.writerow([i,e,lo,hi])
            print("D4 root",root,"node_csv",path)
        else:
            rng=random.Random(20261003); pos=set(pms); maxd=0
            for _ in range(100000):
                sel=rng.sample(range(80),8)
                x=sum(1<<e for e in sel)
                y,d=evalbp(root,nodes,x); maxd=max(maxd,d)
                assert y==(1 if x in pos else 0)
            print("D5 seeded promised sample PASS 100000 sample_max_depth",maxd)

if __name__=="__main__":
    main()
