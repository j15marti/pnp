"""LSPV-3 PAIRED-MATCHING-CUT244 compact independent stdlib checker.
Full expanded experiment and 11-case raw JSON are local conversation artifacts.
"""
from itertools import combinations,product
import json
F=[(1,2,4),(2,3,5),(3,1,6),(-1,-2,-7),(-2,-3,-8),(-3,-1,-9),
   (-4,-6,-7),(7,-5,8),(5,9,6),(8,-9,-6),(7,-4,9),(4,-8,-5)]
N=9
def truth(c,a):
    return sum(a[abs(z)-1]==int(z>0) for z in c)
def demands(c,mode):
    return {abs(z):int(z>0) if mode=="S" else int(z<0) for z in c}
def source_extremes(c):
    s=demands(c,"S");u=demands(c,"U")
    return {"S":s,"invertS_U":{i:1-v for i,v in s.items()},
            "U":u,"invertU_S":{i:1-v for i,v in u.items()}}
def compatible(c,d,mode):
    p=demands(c,mode[0]);q=demands(d,mode[1])
    return all(p[i]==q[i] for i in p.keys()&q.keys())
def minhit(ids,free):
    if not ids:return 0
    for r in range(len(free)+1):
        for subset in combinations(free,r):
            if all(set(subset)&{abs(z) for z in F[j]} for j in ids):
                return r
    return float("inf")
occ={i:[0,0] for i in range(1,N+1)}
for c in F:
    assert len(c)==3 and len(set(map(abs,c)))==3
    for z in c:occ[abs(z)][int(z<0)]+=1
assert all(t==[2,2] for t in occ.values())
all_a=list(product((0,1),repeat=N))
models=[a for a in all_a if all(truth(c,a)>0 for c in F)]
assert len(models)==60
pairs=0
for j,k in combinations(range(len(F)),2):
    c,d=F[j],F[k]
    sign_c={abs(z):int(z<0) for z in c}
    sign_d={abs(z):int(z<0) for z in d}
    both=sign_c.keys()&sign_d.keys()
    same=any(sign_c[i]==sign_d[i] for i in both)
    opp=any(sign_c[i]!=sign_d[i] for i in both)
    for mode in ("SS","SU","US","UU"):
        want=not (opp if mode in ("SS","UU") else same)
        assert compatible(c,d,mode)==want
        support=sorted(set(map(abs,c+d)))
        brute=False
        for vals in product((0,1),repeat=len(support)):
            a=[0]*N
            for i,val in zip(support,vals):a[i-1]=val
            if (truth(c,a)==(3 if mode[0]=="S" else 0) and
                truth(d,a)==(3 if mode[1]=="S" else 0)):
                brute=True;break
        assert brute==want
        pairs+=1
for a in all_a:
    b=tuple(1-v for v in a)
    assert all(truth(c,a)+truth(c,b)==3 for c in F)
alpha={4:0,5:0,6:0,7:1,8:1,9:1}
free=(1,2,3)
refs=[]
for bit in (0,1):
    a=tuple(alpha.get(i,bit) for i in range(1,N+1))
    bad=[j for j,c in enumerate(F) if truth(c,a)==0]
    refs.append({"reference":list(a),"bad_original_clause_ids":bad,"tau":minhit(bad,free)})
assert [r["bad_original_clause_ids"] for r in refs]==[[0,1,2],[3,4,5]]
assert [r["tau"] for r in refs]==[2,2]
assert not any(all(truth(c,a)>0 for c in F) for a in all_a
               if all(a[i-1]==v for i,v in alpha.items()))
# Source-parent resolution: C0 and C6 have the unique opposite pivot x4.
r=tuple(z for z in F[0] if z!=4)+tuple(z for z in F[6] if z!=-4)
assert r==(1,2,-6,-7)
assert not any(all(truth(c,a)>0 for c in F) for a in all_a if truth(r,a)==0)
print(json.dumps({"case":"CUBE9","n":9,"m":12,"models":len(models),
                  "signed_occurrence_counts":occ,"pair_modes_checked":pairs,
                  "source_local_extremes":{str(j):source_extremes(c) for j,c in enumerate(F)},
                  "complement_repair":refs,"cube_alpha":alpha,
                  "derived_source_resolvent":list(r),
                  "scope":"finite checker, P versus NP OPEN"},sort_keys=True))
