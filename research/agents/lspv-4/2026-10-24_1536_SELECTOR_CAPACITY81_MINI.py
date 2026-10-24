#!/usr/bin/env python3
"""Independent compact checks for SELECTOR-CAPACITY-BIT-LEDGER81.
All results finite, no claim of unrestricted SAT complexity lower bound.
"""
import itertools
import json
import math

def parent(m):
    assert m >= 8
    core = [tuple(-v if ((mask >> (v-1)) & 1) else v for v in (1,2,3))
            for mask in range(8)]
    fillers = [(4+3*j,5+3*j,6+3*j) for j in range(m-8)]
    return core+fillers, 3+3*(m-8)

def width(n,k):
    return (64*(n+k+1)-1).bit_length()

def serial(p,n,sel):
    k=len(sel);w=width(n,k)
    words=[n,k]
    for j in sel:
        c=p[j]
        words += [3]+[2*abs(x)+(x<0) for x in c]
    assert max(words) < 2**w
    return ''.join(format(a,'0%db'%w) for a in words)

def virt(p,n,sel,i):
    k=len(sel);w=width(n,k);j,offset=divmod(i,w)
    if j<2: val=(n,k)[j]
    else:
        b,r=divmod(j-2,4);c=p[sel[b]]
        val=3 if r==0 else 2*abs(c[r-1])+(c[r-1]<0)
    return (val >> (w-1-offset))&1

def rank(sel):
    return sum(math.comb(x,i+1) for i,x in enumerate(sel))

def unrank(r,m,k):
    out=[None]*k;upper=m-1
    for j in range(k,0,-1):
        v=upper
        while math.comb(v,j)>r: v-=1
        out[j-1]=v;r-=math.comb(v,j);upper=v-1
    assert r==0
    return tuple(out)

def formula_count(m,k,sel):
    r=sum(i<8 for i in sel)
    return (8-r)*7**(k-r)*8**(m-8-k+r)

def brute(p,n,sel):
    total=0
    for bits in range(1<<n):
        total+=all(any(((bits>>(abs(l)-1))&1)==(l>0) for l in p[i]) for i in sel)
    return total

def run():
    out=[];checks=0
    for m,k in ((10,7),(10,8),(16,7),(16,8),(16,9)):
        p,n=parent(m);sat=unsat=0;seen=set()
        for cnt,s in enumerate(itertools.combinations(range(m),k),1):
            r=rank(s)
            assert r not in seen and unrank(r,m,k)==s
            seen.add(r);checks+=2
            want=formula_count(m,k,s)
            if want: sat+=1
            else: unsat+=1
            if m==10:
                assert brute(p,n,s)==want
                checks+=1
            if m==10 or cnt%257==0 or want==0:
                bits=serial(p,n,s)
                assert all((c=='1')==bool(virt(p,n,s,i)) for i,c in enumerate(bits))
                checks+=len(bits)
        assert len(seen)==math.comb(m,k)
        assert unsat==(math.comb(m-8,k-8) if k>=8 else 0)
        checks+=2
        out.append(dict(m=m,k=k,selectors=len(seen),SAT=sat,UNSAT=unsat,
                        descriptor_lower_bits=(len(seen)-1).bit_length(),
                        array_bits=k*(m-1).bit_length()))
    return dict(run="SELECTOR_CAPACITY81_MINI",checks=checks,failures=0,cases=out)

if __name__=="__main__":
    print(json.dumps(run(),indent=2))
