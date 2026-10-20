"""ARC-SIGN-COLOR-GLUE4: exhaustive 3-variable control and matched 9-clause pair."""
from itertools import product
EIGHT=tuple(tuple(a*b for a,b in zip(s,(1,2,3))) for s in product((-1,1),repeat=3))
def sat(cnf,n):
    return any(all(any((bool((a>>(abs(l)-1))&1)==(l>0)) for l in clause) for clause in cnf) for a in range(1<<n))
def split(cnf):
    return (tuple(c for c in cnf if sum(l>0 for l in c)<=1),
            tuple(c for c in cnf if sum(l>0 for l in c)>=2))
ok=0
for mask in range(256):
    f=tuple(EIGHT[i] for i in range(8) if (mask>>i)&1)
    h,d=split(f)
    assert sat(h,3) and sat(d,3)
    ok+=int(sat(f,3))
assert ok==255
no=EIGHT+((-1,-3,-4),)
yes=tuple(c for c in EIGHT if c!=(-1,-2,-3))+((-1,-3,-4),(-1,-2,-4))
assert len(no)==len(yes)==9 and not sat(no,4) and sat(yes,4)
assert tuple(sum(sum(l>0 for l in c)==k for c in no) for k in range(4)) == tuple(sum(sum(l>0 for l in c)==k for c in yes) for k in range(4))
print("PASS 256 subsets; matched distinct-clause pair; P vs NP OPEN")
