"""Independent finite check: direct evaluations, no elimination-library import."""
import itertools as it
import json, random

def bitdot(a,b): return (a&b).bit_count()%2
def evalmask(rows,x): return sum(bitdot(row,x)<<j for j,row in enumerate(rows))

def audit():
    # Six-bit control: direct existential projection, independent of pair formula.
    bad=set()
    for y in range(32):
        a,b,c,u,v=[y>>i&1 for i in range(5)]
        if not any(not ((a and t==0) or (b and t==u) or (c and t==v)) for t in (0,1)):
            bad.add(y)
    assert len(bad)==9
    for flat in it.combinations(bad,8):
        x=flat[0]; D={z^x for z in flat}
        assert any(p^q not in D for p in D for q in D)
    # Directly compute attainable masks and row-dependency masks, and compare
    # the zero-signature rule with every possible evaluation mask.
    rng=random.Random(2611261102); checks=0; sparse=0
    for trial in range(180):
        n=rng.randrange(1,6); r=rng.randrange(1,10)
        rows=[rng.randrange(1<<n) for j in range(r)]
        attainable={evalmask(rows,x) for x in range(1<<n)}
        kernel=[]
        for k in range(1<<r):
            a=0
            for j,row in enumerate(rows):
                if k>>j&1: a^=row
            if a==0: kernel.append(k)
        for m in range(1<<r):
            assert (m in attainable)==all(bitdot(k,m)==0 for k in kernel)
            checks+=1
        # Random contiguous event partition, with exact all-mask search.
        cut=[0]+[j for j in range(1,r) if rng.randrange(2)]+[r]
        entries=[]
        for i,(a,b) in enumerate(zip(cut,cut[1:])):
            for u in range(1,1<<(b-a)):
                m=u<<a
                sig=evalmask(kernel,m)
                entries.append((i,m,sig))
        found=set()
        for q in (1,2,3):
            for tup in it.combinations(entries,q):
                if len({e[0] for e in tup})!=q: continue
                s=m=0
                for _,u,z in tup: s^=z; m^=u
                if s==0: found.add(m)
        ref={m for m in attainable if m and sum(bool(m & (((1<<(b-a))-1)<<a)) for a,b in zip(cut,cut[1:]))<=3}
        assert found==ref
        sparse+=len(ref)
    return {'systems':180,'mask_checks':checks,'exact_sparse_masks':sparse,'bad_words':len(bad),'nonaffine_8sets':9}
if __name__=='__main__':
    print(json.dumps(audit(),sort_keys=True))
