#!/usr/bin/env python3
"""Independent stdlib reproduction: strict (2,2) cyclic pivot cancellation.
Reports actual original-source witness replay and a negative-socket hostile case.
No general SAT lower bound and no independently checked UNSAT certificate.
"""
import collections,itertools,json
def family(q):
    F=[]
    for i in range(q):
        a,b,c,x,y,z=[6*i+j for j in range(1,7)]
        nexta=6*((i+1)%q)+1
        F.extend([(nexta,b,x),(nexta,b,-x),(-a,c,y),(-a,c,-y),
                  (-b,x,z),(-b,-x,-z),(-c,y,z),(-c,-y,-z)])
    return F
def validate(F):
    n=max(abs(l) for c in F for l in c);m=len(F)
    assert 3*m==4*n
    assert len({tuple(sorted(c)) for c in F})==m
    assert all(len(c)==3 and len({abs(v) for v in c})==3 for c in F)
    cnt=collections.Counter(l for c in F for l in c)
    assert all(cnt[v]==cnt[-v]==2 for v in range(1,n+1))
    graph=collections.defaultdict(set)
    for c in F:
        for l in c:
            graph[abs(l)].update(abs(v) for v in c if abs(v)!=abs(l))
    seen={1};q=[1]
    while q:
        for v in graph[q.pop()]-seen:
            seen.add(v);q.append(v)
    assert len(seen)==n
    return n,m
def reduce_source(F):
    idx=collections.defaultdict(lambda:{1:[], -1:[]})
    for i,c in enumerate(F):
        for k,l in enumerate(c):
            other=tuple(sorted(v for j,v in enumerate(c) if j!=k))
            idx[(other,abs(l))][1 if l>0 else -1].append(i)
    paired=set();B=[]
    for (other,x),rows in sorted(idx.items()):
        for i in rows[1]:
            for j in rows[-1]:
                assert i not in paired and j not in paired
                paired.update((i,j));B.append(other)
    T={i:F[i] for i in range(len(F)) if i not in paired}
    delta=len(T)
    boundary={abs(v) for c in B for v in c}
    occ=collections.defaultdict(list)
    for i,c in T.items():
        for v in c:occ[abs(v)].append((i,v))
    trace=[]
    for x in sorted(occ):
        rows=occ[x]
        if x in boundary or len(rows)!=2:continue
        (i,a),(j,b)=rows
        if a*b>=0 or i not in T or j not in T:continue
        pos,neg=(T[i],T[j]) if a>0 else (T[j],T[i])
        mates=[v for v in pos if v!=x and -v in neg]
        if not mates:continue
        trace.append((x,mates[0]));del T[i];del T[j]
    return B,list(T.values()),trace,delta
def sat(F,assignment):
    return all(any(assignment[abs(l)]==(l>0) for l in c) for c in F)
def run():
    rows=[]
    for q in [1,2,3,4,8,16,32,128,256,512]:
        F=family(q);n,m=validate(F)
        B,T,tr,delta=reduce_source(F)
        assert len(B)==2*q and delta==4*q and not T and len(tr)==2*q
        a={v:False for v in range(1,n+1)}
        for i in range(q):
            a[6*i+2]=True;a[6*i+3]=True
        for x,mate in reversed(tr):
            ell_true=a[abs(mate)]==(mate>0);a[x]=not ell_true
        assert sat(F,a)
        if q<=2:
            assert any(sat(F,{v:bool((bits>>(v-1))&1) for v in range(1,n+1)}) for bits in range(1<<n))
        w=(64*(n+m+1)-1).bit_length()
        rows.append(dict(q=q,n=n,m=m,N_bits=(4*m+2)*w,original_unmatched=delta,
                         removed_unmatched=2*len(tr),binary_remainder=len(B),witness_verified=True))
    H=[list(c) for c in family(2)]
    H[5][-1],H[15][-1]=H[15][-1],H[5][-1]
    H=list(map(tuple,H))
    validate(H)
    B,T,tr,delta=reduce_source(H)
    assert delta==8 and len(tr)==2 and len(T)==4
    print(json.dumps(dict(family=rows,hostile=dict(n=12,m=16,unmatched=delta,
                         removed_unmatched=2*len(tr),residual_ternaries=len(T))),indent=2))
if __name__=='__main__':run()
