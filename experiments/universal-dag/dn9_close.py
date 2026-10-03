from functools import lru_cache
from math import comb

# DN9-CLOSE1 verifier.
# This file checks the finite arithmetic and the full-binary-tree depth obstruction
# used with the classical MU(1) strict-resolution-tree characterization.

@lru_cache(None)
def depth_profiles(leaves):
    if leaves == 1:
        return {(0,)}
    out=set()
    for a in range(1, leaves):
        b=leaves-a
        for pa in depth_profiles(a):
            for pb in depth_profiles(b):
                out.add(tuple(sorted([d+1 for d in pa]+[d+1 for d in pb])))
    return out

u={3:1,4:268,5:3030,6:7800,7:5040}
v={4:9408,5:324000,6:1913280,7:3430560}

def U8(n):
    return sum(comb(n,k)*c for k,c in u.items() if n>=k)

def Min9(n):
    return sum(comb(n,k)*c for k,c in v.items() if n>=k)

def U9(n):
    M=8*comb(n,3)
    return (M-8)*U8(n)+Min9(n)

known={4:15936,5:686400,6:8561440,7:60047120}

if __name__=="__main__":
    print("8 leaves all depth 3:", (3,)*8 in depth_profiles(8))
    print("9 leaves all depth 3:", (3,)*9 in depth_profiles(9))
    assert (3,)*8 in depth_profiles(8)
    assert (3,)*9 not in depth_profiles(9)

    for n,want in known.items():
        got=U9(n)
        print("check",n,got,want)
        assert got==want

    for n in range(4,11):
        print("n",n,"U8",U8(n),"Min9",Min9(n),"U9",U9(n))

    assert U9(8)==296593920
    print("PASS")
