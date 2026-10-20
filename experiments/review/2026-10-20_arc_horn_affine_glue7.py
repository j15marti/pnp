#!/usr/bin/env python3
"""ARC-HORN-AFFINE-SHARED-GLUE7: exhaustive plus fixed-seed controls. P vs NP OPEN."""
import itertools, random, json

def sat(F,n):
    return any(all(any(x[abs(l)-1] == (l>0) for l in c) for c in F)
               for x in itertools.product((False,True),repeat=n))

def audit(F,n,stats):
    H=[]; X=[]
    for j,c in enumerate(F):
        assert len(c)==3 and len(set(map(abs,c)))==3
        zs=[n+3*j+r+1 for r in range(3)]
        H.append(tuple(-z for z in zs))
        for z,l in zip(zs,c): X.append((z,abs(l),int(l>0)))
    target=sat(F,n)
    joint=False
    for x in itertools.product((False,True),repeat=n):
        z={p: x[v-1]^bool(b) for p,v,b in X}
        if all(any(not z[abs(l)] for l in c) for c in H):
            joint=True;break
    assert target==joint
    # Standalone Horn witness z=0, standalone XOR witness x=0,z=b.
    assert all(all(l<0 for l in c) for c in H)
    assert len(X)==3*len(F) and len(H)==len(F)
    assert all((int(bool(b))^0)==b for _,_,b in X)
    stats['instances']+=1;stats['yes']+=int(target);stats['no']+=int(not target)
    stats['checks']+=6+len(H)+len(X)

def main():
    r={'instances':0,'yes':0,'no':0,'checks':0}
    signs=list(itertools.product((-1,1),repeat=3))
    base=[tuple((i+1)*a[i] for i in range(3)) for a in signs]
    for mask in range(256):audit([c for j,c in enumerate(base) if mask&(1<<j)],3,r)
    assert r['yes']==255 and r['no']==1
    assert not sat(base,3) and sat(base[1:],3)
    r['checks']+=3
    rng=random.Random(20261020)
    for n in (4,5,6):
        for m in (1,4,8,12,20):
            for _ in range(32):
                F=[]
                for _ in range(m):
                    vs=rng.sample(range(1,n+1),3)
                    F.append(tuple(v if rng.getrandbits(1) else -v for v in vs))
                audit(F,n,r)
    assert r=={'instances':736,'yes':720,'no':16,'checks':25795}
    print(json.dumps(dict(r,result='PASS',model='restricted factor SAT no-go'),indent=2))
if __name__=='__main__':main()
