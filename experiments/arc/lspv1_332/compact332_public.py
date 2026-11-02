#!/usr/bin/env python3
"""LSPV-1 332: exact finite canonical-source cofactor tests, stdlib only."""
import itertools, json, hashlib, collections
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
Q=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
B=P+tuple(tuple(-v for v in c) for c in Q)
def valid(n,cs):
    if type(n)!=int or n<3 or type(cs) not in (list,tuple) or 3*len(cs)!=4*n:return False
    seen=set();cnt=collections.Counter()
    for c in cs:
        if type(c) not in (list,tuple) or len(c)!=3 or any(type(v)!=int or not v or abs(v)>n for v in c):return False
        if len({abs(v) for v in c})!=3 or not (all(v>0 for v in c) or all(v<0 for v in c)):return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key)
        for v in c:cnt[(abs(v),v>0)]+=1
    return all(cnt[(i,s)]==2 for i in range(1,n+1) for s in (True,False))
def sat(cs,a):
    return all(any(((a>>(abs(l)-1))&1)==(l>0) for l in c) for c in cs)
def blocks(t):
    return [tuple((1 if v>0 else -1)*(abs(v)+9*j) for v in c) for j in range(t) for c in B]
def main():
    assert valid(9,B) and all(valid(9*t,blocks(t)) for t in (1,2,3))
    f=[bytes(sat(B,x if k<0 else ((x&~1)|k)) for x in range(512)) for k in (-1,0,1)]
    assert tuple(sum(z) for z in f)==(70,80,60)
    rows={};shas={}
    for t in (1,2):
        signatures=[];supports=[]
        for choice in itertools.product(range(3),repeat=t):
            if t==1:by=f[choice[0]]
            else:by=b''.join(f[choice[0]] if bit else bytes(512) for bit in f[choice[1]])
            signatures.append(hashlib.sha256(by).hexdigest());supports.append(sum(by))
        assert len(set(signatures))==3**t
        rows[t]=sorted(supports);shas[t]=signatures
    pins={3:0,5:1,6:0,7:0,8:0};labels={};cover=[]
    for b in (0,1):
        count=0
        for bits in itertools.product((0,1),repeat=3):
            a={**pins,1:b,**dict(zip((2,4,9),bits))}
            mask=sum(v<<(i-1) for i,v in a.items())
            if sat(B,mask):count+=1
            elif b==1:
                cover.append(next(j for j,c in enumerate(B,1) if not any(((mask>>(abs(l)-1))&1)==(l>0) for l in c)))
        labels[b]=count
    assert labels=={0:2,1:0} and len(cover)==8
    pairmodes=0
    for j,k in itertools.combinations(range(12),2):
        for typj,typk in itertools.product((0,1),repeat=2):
            req={};consistent=True
            for c,typ in ((B[j],typj),(B[k],typk)):
                for l in c:
                    val=(l>0) if typ else (l<0)
                    if abs(l) in req and req[abs(l)]!=val:consistent=False
                    req[abs(l)]=val
            same=any(abs(v)==abs(w) and (v>0)==(w>0) for v in B[j] for w in B[k])
            opp=any(abs(v)==abs(w) and (v>0)!=(w>0) for v in B[j] for w in B[k])
            assert consistent==((not opp) if typj==typk else (not same))
            pairmodes+=1
    bad=[list(B)+[B[0]],list(B[:-1]),[(1,1,6)]+list(B[1:]),[(1,-5,6)]+list(B[1:]),[(1,5,10)]+list(B[1:])]
    assert all(not valid(9,cs) for cs in bad)
    print(json.dumps({'canonical_F9_models':70,'forward_architecture_binary_gates':35,
       'embedded_support':{'unfixed':70,'zero':80,'one':60},
       'exact_classes':{'t1':len(set(shas[1])),'t2':len(set(shas[2]))},
       'support_multisets':rows,'sha256':shas,'same_original_pins':labels,
       'UNSAT_original_clause_cover_ids':cover,'SU_modes_verified':pairmodes,
       'malformed_rejected':len(bad),'all_input_polynomial_result':False,
       'arbitrary_decider_FLMV_transfer':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
