#!/usr/bin/env python3
"""Restricted exact source indexed child-bit compiler, stdlib, no dependencies.
An independent full physical event verifier is supplied in the conversation ZIP.
P vs NP and all-input ARC/FLMV remain OPEN.
"""
from itertools import product
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),
   (-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
def gamma(k):
    assert k>=1
    b=format(k,"b")
    return "0"*(len(b)-1)+b
def enc(clauses):
    n=max(abs(x)for c in clauses for x in c)
    w=n.bit_length()
    return gamma(n)+gamma(len(clauses))+"".join(
        ("1" if c[0]<0 else "0")+"".join(format(abs(x),f"0{w}b") for x in c)
        for c in clauses)
def decode_gamma(s,p):
    z=0
    while p+z<len(s) and s[p+z]=="0":
        z+=1
        if z>=len(s).bit_length():
            raise ValueError("huge malformed header")
    if p+2*z+1>len(s):raise ValueError("truncated gamma")
    return int(s[p+z:p+2*z+1],2),p+2*z+1
def clause(s,h,w,j):
    i=h+j*(1+3*w)
    sg=-1 if s[i]=="1" else 1
    return tuple(sg*int(s[i+1+k*w:i+1+(k+1)*w],2)for k in range(3))
def validate_and_map(s):
    if not s or any(b not in "01"for b in s):raise ValueError("not binary")
    n,p=decode_gamma(s,0);m,h=decode_gamma(s,p)
    if n<12 or m<16 or 4*n!=3*m or h+m*(1+3*n.bit_length())!=len(s):
        raise ValueError("bad source shape")
    w=n.bit_length()
    suffix=tuple(tuple((1 if v>0 else -1)*(abs(v)+n-6)for v in c)for c in Y)
    for j in range(m):
        c=clause(s,h,w,j)
        if len({abs(x)for x in c})!=3 or any(abs(x)<1 or abs(x)>n for x in c):
            raise ValueError("bad clause")
        if j<m-8 and any(abs(v)>n-6 for v in c):raise ValueError("suffix overlaps")
        if j>=m-8 and c!=suffix[j-m+8]:raise ValueError("NO_RULE")
        for k in range(j):
            if tuple(sorted(clause(s,h,w,k)))==tuple(sorted(c)):
                raise ValueError("duplicate clause")
    for x in range(1,n+1):
        positive=negative=0
        for j in range(m):
            c=clause(s,h,w,j)
            positive+=sum(z==x for z in c)
            negative+=sum(z==-x for z in c)
        if positive!=2 or negative!=2:raise ValueError("bad quota")
    hc=gamma(n-6)+gamma(m-8)
    wp=n.bit_length();wc=(n-6).bit_length();rp=1+3*wp;rc=1+3*wc
    def bit(q):
        M=len(hc)+(m-8)*rc
        if not 0<=q<M:raise IndexError(q)
        if q<len(hc):return hc[q]
        j,t=divmod(q-len(hc),rc)
        source=h+j*rp
        if t==0:return s[source]
        k,u=divmod(t-1,wc)
        return s[source+1+k*wp+(wp-wc)+u]
    return bit,len(hc)+(m-8)*rc
def shift(F,k):
    return tuple(tuple((1 if x>0 else -1)*(abs(x)+k)for x in c)for c in F)
def valid_model(F,A):
    return all(any(A[abs(z)-1]==int(z>0)for z in c)for c in F)
def run():
    six=next(a for a in product((0,1),repeat=6)if valid_model(Y,a))
    assert six==(0,0,1,0,1,1)
    for blocks in (1,2,42):
        H=tuple(c for i in range(blocks)for c in shift(Y,i*6))
        F=H+shift(Y,blocks*6)
        s=enc(F);expected=enc(H);bit,L=validate_and_map(s)
        assert L==len(expected) and "".join(bit(i)for i in range(L))==expected
        print("PASS",blocks,"N",len(s),"M",L)
    bad=enc(Y+shift(Y,6))+"0"
    try:validate_and_map(bad)
    except ValueError:pass
    else:raise AssertionError("malformed encoding accepted")
    print("OPEN: no all-input connected-child contraction or FLMV lower bound")
if __name__=="__main__":run()
