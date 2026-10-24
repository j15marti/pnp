#!/usr/bin/env python3
"""INDEXED-MERGE-FIREWALL94 compact independently runnable stdlib auditor.
Records use zero-based word offsets, two header words, 16 words per Pin block.
This validates ordinary encoded source bits; not a physical random-access TM trace.
"""
from itertools import combinations, product
from math import ceil, log2
def enc(q,A,B):
    w=[3*q,4*q]
    for j,a in enumerate(tuple(A)+tuple(B),1):
        u,v=q+2*j-1,q+2*j
        for su,sv in product(range(2),repeat=2):
            w += [3,2*a+int(j>q//2),2*u+su,2*v+sv]
    return w
def verify(q,w):
    if len(w)!=16*q+2 or w[0]!=3*q or w[1]!=4*q:return False
    for j in range(q):
        p=2+16*j; old=None
        for i,(a,b) in enumerate(product(range(2),repeat=2)):
            h,l,u,v=w[p+4*i:p+4*i+4]; z=l//2
            if h!=3 or not 1<=z<=q or l%2!=int(j>=q//2):return False
            if old is not None and old!=z:return False
            if u!=2*(q+2*(j+1)-1)+a or v!=2*(q+2*(j+1))+b:return False
            old=z
    for offset in (0,q//2):
        names=[w[3+16*(offset+j)]//2 for j in range(q//2)]
        if names!=sorted(set(names)):return False
    return True
def indexed_merge(q,w):
    i=j=cmp=0
    while i<q//2 and j<q//2:
        a=w[3+16*i]//2
        b=w[3+16*(q//2+j)]//2
        cmp+=1
        if a==b:return False,cmp
        if a<b:i+=1
        else:j+=1
    return True,cmp
def run():
    checks=0
    for q in (2,4,6,8):
        fam=list(combinations(range(1,q+1),q//2))
        yes=no=0
        for A in fam:
            for B in fam:
                w=enc(q,A,B)
                assert verify(q,w);checks+=1
                status,c=indexed_merge(q,w)
                assert status==set(A).isdisjoint(B);checks+=1
                assert c<=q-1;checks+=1
                assert len(w)*ceil(log2(64*(7*q+1)))==(16*q+2)*ceil(log2(64*(7*q+1)));checks+=1
                if q<=4:
                    satcount=0
                    for bits in product(range(2),repeat=q):
                        if all(bits[x-1]==1 for x in A) and all(bits[y-1]==0 for y in B):
                            satcount+=1
                    assert satcount*2**(2*q)==(2**(2*q) if status else 0);checks+=1
                yes+=int(status);no+=int(not status)
        assert yes==len(fam) and no==len(fam)**2-len(fam);checks+=1
        print("q",q,"SAT",yes,"UNSAT",no)
    print("assertion-accounted checks",checks,"discrepancies",0)
if __name__=="__main__":run()
