from itertools import combinations
from collections import defaultdict, Counter
from math import log2

# PARDON_PRIMITIVE1
# Finite Pardon-style experiment on continuation relations for D(4,8), D(5,8).
#
# The actual Pardon algebra is not imported. We test an algebraic analogue:
# a semantic continuation matrix M; COPY/DEAD/tautological wrappers should not
# change rank, independent Cartesian products tensor matrices and multiply rank,
# and log2(rank) therefore becomes additive ("primitive-like").

def exact_covers(n):
    triples=list(combinations(range(n),3))
    clauses=[]; contains=[[] for _ in range(1<<n)]
    for T in triples:
        for pat in range(8):
            mask=0
            for a in range(1<<n):
                if all(((a>>v)&1)==((pat>>j)&1) for j,v in enumerate(T)):
                    mask |= 1<<a
            ci=len(clauses); clauses.append(mask)
            for a in range(1<<n):
                if (mask>>a)&1: contains[a].append(ci)
    FULL=(1<<(1<<n))-1; out=set()
    def rec(cov,chosen):
        if cov==FULL:
            if len(chosen)==8:
                x=0
                for e in chosen: x|=1<<e
                out.add(x)
            return
        if len(chosen)>=8:return
        rem=(~cov)&FULL
        a=(rem&-rem).bit_length()-1
        for ci in contains[a]:
            m=clauses[ci]
            if m&cov: continue
            rec(cov|m, chosen+(ci,))
    rec(0,())
    return sorted(out)

def gf2_rank(rows):
    piv={}
    for x in rows:
        y=x
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)

def block(pms,half,k):
    mask=(1<<half)-1
    rd=defaultdict(set); cols=set()
    for pm in pms:
        r=pm&mask; c=pm>>half
        if r.bit_count()==k:
            rd[r].add(c); cols.add(c)
    cs=sorted(cols); ci={c:i for i,c in enumerate(cs)}
    bits=[]
    for r in sorted(rd):
        b=0
        for c in rd[r]: b|=1<<ci[c]
        bits.append(b)
    return bits,len(rd),len(cs),sum(x.bit_count() for x in bits)

def components(rows,ncols):
    ra=[[] for _ in rows]; ca=[[] for _ in range(ncols)]
    for i,b in enumerate(rows):
        x=b
        while x:
            l=x&-x;j=l.bit_length()-1;x-=l
            ra[i].append(j);ca[j].append(i)
    sr=set();sc=set();out=[]
    for i in range(len(rows)):
        if i in sr or not ra[i]:continue
        q=[(0,i)];sr.add(i);rs=[];cs=[]
        while q:
            t,z=q.pop()
            if t==0:
                rs.append(z)
                for j in ra[z]:
                    if j not in sc:sc.add(j);q.append((1,j))
            else:
                cs.append(z)
                for ii in ca[z]:
                    if ii not in sr:sr.add(ii);q.append((0,ii))
        e=sum(len(ra[ii]) for ii in rs)
        out.append((len(rs),len(cs),e,e==len(rs)*len(cs)))
    return out

def kron_rows(A,nA,B,nB):
    out=[]
    for a in A:
        apos=[];x=a
        while x:
            l=x&-x;apos.append(l.bit_length()-1);x-=l
        for b in B:
            bpos=[];y=b
            while y:
                l=y&-y;bpos.append(l.bit_length()-1);y-=l
            z=0
            for i in apos:
                for j in bpos:z|=1<<(i*nB+j)
            out.append(z)
    return out

def parity_rows(t):
    out=[]
    for x in range(1<<t):
        b=0;px=x.bit_count()&1
        for y in range(1<<t):
            if px^(y.bit_count()&1):b|=1<<y
        out.append(b)
    return out

def equality_rows(t):
    return [1<<i for i in range(1<<t)]

if __name__=="__main__":
    p4=exact_covers(4);p5=exact_covers(5)
    print("covers",len(p4),len(p5))
    for n,pms,half in [(4,p4,16),(5,p5,40)]:
        print("D",n)
        for k in range(9):
            rows,nr,nc,ones=block(pms,half,k)
            if not rows:continue
            r=gf2_rank(rows);cc=components(rows,nc)
            assert all(x[3] for x in cc)
            print(k,nr,nc,ones,r,len(set(rows)),len(cc),
                  max(a+b for a,b,e,ok in cc),
                  sorted(Counter((a,b) for a,b,e,ok in cc).items()))

    A,nr,nc,ones=block(p4,16,4)
    r=gf2_rank(A)
    assert gf2_rank(A+A)==r
    assert gf2_rank(A+[0]*17)==r
    assert gf2_rank([x for x in A for _ in (0,1)])==r
    print("wrapper_D4_k4",r,r,r,r,"primitive_score",log2(r))

    B,nr,nc,ones=block(p4,16,2)
    KB=kron_rows(B,nc,B,nc)
    assert gf2_rank(KB)==gf2_rank(B)**2
    print("tensor_D4_k2",gf2_rank(B),gf2_rank(KB),
          log2(gf2_rank(B)),log2(gf2_rank(KB)))

    P=parity_rows(6);E=equality_rows(6)
    print("controls",
          "parity_rank",gf2_rank(P),"parity_score",log2(gf2_rank(P)),
          "equality_rank",gf2_rank(E),"equality_score",log2(gf2_rank(E)))

    print("STATUS COMPUTATIONAL finite experiment.")
    print("log2(rank) is a Pardon-style additive scalar analogue, not a primitive element of the actual Pardon algebra.")
