#!/usr/bin/env python3
"""Independent compact finite checks for EXTREME_HELLY_WITNESS252.
Original source clause indices and variable identities are preserved.
Python >=3.9, no third-party dependencies; exhaustive checking is external evidence.
"""
import itertools, json, collections
W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
K4=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6)]
SWAP6=W1.copy()
SWAP6[9]=(-5,6,-15)
SWAP6[13]=(-3,-6,-15)
def val(z,a):
    return (bool(a>>(abs(z)-1)&1)==(z>0))
def t(c,a):
    return sum(val(z,a) for z in c)
def ext(c,mode):
    return {abs(z):int(z>0) if mode=="S" else int(z<0) for z in c}
def checks(F):
    n=max(abs(z) for c in F for z in c)
    assert all(len(c)==3 and len({abs(z) for z in c})==3 for c in F)
    occ=collections.defaultdict(list)
    targets=[]
    for j,c in enumerate(F):
        targets.append({"j":j,"S":ext(c,"S"),"U":ext(c,"U")})
        for z in c:
            occ[abs(z)].append((j,z))
            assert ext(c,"S")[abs(z)]==1-ext(c,"U")[abs(z)]
    degrees={i:len(occ[i]) for i in range(1,n+1)}
    W=2*sum(d*(d-1)//2 for d in degrees.values())
    blocked=0; H=0; M=0; tested=0
    for j,k in itertools.combinations(range(len(F)),2):
        left={abs(z):int(z>0) for z in F[j]}
        right={abs(z):int(z>0) for z in F[k]}
        common=left.keys() & right.keys()
        same={i for i in common if left[i]==right[i]}
        opp=common-same
        H+=bool(common);M+=bool(same and opp)
        for mode in ("SS","SU","US","UU"):
            want=not (opp if mode in ("SS","UU") else same)
            pins=ext(F[j],mode[0]);other=ext(F[k],mode[1])
            consistent=all(i not in pins or pins[i]==b for i,b in other.items())
            assert consistent==bool(want)
            # Independent enumeration of coherent ORIGINAL variables on union support.
            allvars=sorted(left.keys()|right.keys())
            actual=False
            for bits in range(1<<len(allvars)):
                a=sum(1<<(i-1) for p,i in enumerate(allvars) if bits>>p&1)
                if (t(F[j],a)==(3 if mode[0]=="S" else 0) and
                    t(F[k],a)==(3 if mode[1]=="S" else 0)):
                    actual=True;break
            assert actual==bool(want)
            blocked+=not bool(want)
            tested+=1
    assert blocked==2*H+2*M
    assert W>=blocked
    if all(len(occ[i])==4 and sum(z>0 for _,z in occ[i])==2 for i in range(1,n+1)):
        assert W==12*n
    # Full coherent assignments, endpoints, inversion, and complete oracle models.
    models=0; complement_checks=0
    for a in range(1<<n):
        aa=[t(c,a) for c in F]
        bb=[t(c,a^((1<<n)-1)) for c in F]
        assert all(x+y==3 for x,y in zip(aa,bb))
        models+=all(aa)
        complement_checks+=1
    # Multi-clause prescribed extreme targets are 2-Helly.
    multi_checks=0
    for inds in itertools.islice(itertools.combinations(range(len(F)),3),12):
        for modes in itertools.product("SU",repeat=3):
            pins={};pairgood=True
            for j,m in zip(inds,modes):
                for i,b in ext(F[j],m).items():
                    if i in pins and pins[i]!=b: pairgood=False
                    pins[i]=b
            union=sorted({abs(z) for j in inds for z in F[j]})
            realizable=False
            for bits in range(1<<len(union)):
                a=sum(1<<(i-1) for q,i in enumerate(union) if bits>>q&1)
                if all(t(F[j],a)==(3 if m=="S" else 0) for j,m in zip(inds,modes)):
                    realizable=True;break
            assert realizable==pairgood
            multi_checks+=1
    return {"n":n,"m":len(F),"W_multiplicity":W,
        "distinct_blocked_modes":blocked,"shared_pairs":H,"mixed_pairs":M,
        "verified_sat_models":models,"pair_modes":tested,
        "triple_modes":multi_checks,"complement_checks":complement_checks}
def main():
    data={name:checks(F) for name,F in
       (("W1_UNSAT",W1),("SWAP6_SAT",SWAP6),("K4_SAT",K4))}
    assert data["W1_UNSAT"]["verified_sat_models"]==0
    assert data["SWAP6_SAT"]["verified_sat_models"]==54
    assert data["W1_UNSAT"]["W_multiplicity"]==data["SWAP6_SAT"]["W_multiplicity"]==180
    assert data["W1_UNSAT"]["distinct_blocked_modes"]==data["SWAP6_SAT"]["distinct_blocked_modes"]==180
    print(json.dumps({"status":"PASS","cases":data},indent=2))
if __name__=="__main__":main()
