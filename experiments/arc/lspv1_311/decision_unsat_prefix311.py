#!/usr/bin/env python3
"""LSPV-1 311: ONE all-input exact decider, finite verified UNSAT prefix.
The Python loop counts inspected source bits; asymptotic native tape costs
are proved separately and NOT measured by this Python instrumentation.
Run from any directory: python experiments/arc/lspv1_311/decision_unsat_prefix311.py
"""
import json,itertools
from pathlib import Path
from collections import Counter

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'lspv2_296'/'U198.txt'
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
def u198():
    return tuple(map(tuple,json.loads(''.join(s for s in
        SOURCE.read_text().splitlines() if not s.startswith('#')))))
def valid(F,n):
    if not n or n%3 or len(F)*3!=4*n:return False
    occ=Counter();seen=set()
    for row in F:
        if len(row)!=3 or len({abs(x) for x in row})!=3:return False
        if any(abs(x)<1 or abs(x)>n for x in row):return False
        if not(all(x>0 for x in row) or all(x<0 for x in row)):return False
        k=tuple(sorted(row))
        if k in seen:return False
        seen.add(k)
        for x in row:occ[(abs(x),x>0)]+=1
    return all(occ[(x,b)]==2 for x in range(1,n+1) for b in (False,True))
def gamma(x):
    w=format(x,'b');return '0'*(len(w)-1)+w
def encode(F,n):
    b=n.bit_length()
    return gamma(n)+gamma(len(F))+''.join(
      ('1' if row[0]>0 else '0')+''.join(format(abs(x),f'0{b}b') for x in row)
      for row in F)
def parse(s):
    p=0
    def head():
        nonlocal p
        k=0
        while p<len(s) and s[p]=='0':k+=1;p+=1
        if p+k+1>len(s) or s[p]!='1':raise ValueError('header')
        x=int(s[p:p+k+1],2);p+=k+1
        return x
    n=head();m=head();b=n.bit_length()
    if n<1 or m<0 or len(s)-p!=m*(1+3*b):raise ValueError('length')
    F=[]
    for _ in range(m):
        sg=s[p]=='1';p+=1
        row=[]
        for __ in range(3):
            bits=s[p:p+b];p+=b
            v=int(bits,2)
            row.append(v if sg else -v)
        F.append(tuple(row))
    if not valid(F,n):raise ValueError('grammar')
    return F,n
def sat(F,a):
    return all(any(a[abs(x)-1]==(x>0) for x in c) for c in F)
def exact(F,n):
    return any(sat(F,a) for a in itertools.product((False,True),repeat=n))
def decide(s,U):
    """Correct on every binary string. Only prefix reads on fast UNSAT family."""
    seen=set()
    def read(pos):
        seen.add(pos)
        return s[pos] if pos<len(s) else None
    pos=0
    def hdr():
        nonlocal pos
        k=0
        while True:
            x=read(pos);pos+=1
            if x is None:raise ValueError('short')
            if x=='1':break
            if x!='0':raise ValueError('nonbinary')
            k+=1
        v=1
        for _ in range(k):
            x=read(pos);pos+=1
            if x not in ('0','1'):raise ValueError('short')
            v=2*v+(x=='1')
        return v
    try:
        n=hdr();m=hdr()
        if n>=198 and m>=264:
            w=n.bit_length()
            for c in U:
                pattern=('1' if c[0]>0 else '0')+''.join(
                    format(abs(x),f'0{w}b') for x in c)
                for bit in pattern:
                    if read(pos)!=bit:raise ValueError('prefix mismatch')
                    pos+=1
            return False,len(seen),'certified-unsat-prefix'
    except ValueError:pass
    # Full scan and exact fallback for every unrecognized input, including malformed.
    seen.update(range(len(s)))
    try:F,n=parse(s)
    except ValueError:return False,len(seen),'malformed'
    return exact(F,n),len(seen),'exact-fallback'
def union(U,t):
    F=list(U)
    for i in range(t):
        off=198+9*i
        F.extend(tuple((abs(x)+off)*(1 if x>0 else -1) for x in c)
                 for c in F9)
    return tuple(F),198+9*t
def main():
    U=u198()
    assert len(U)==264 and valid(U,198) and valid(F9,9) and valid(Y6,6)
    assert sum(sat(F9,a) for a in itertools.product((False,True),repeat=9))==70
    assert sum(sat(Y6,a) for a in itertools.product((False,True),repeat=6))==20
    a={1:1,3:0,5:1,6:0,7:0,8:0};b=dict(a);b[1]=0
    def pinned_count(p):
        return sum(sat(F9,x) and all(x[i-1]==bool(v) for i,v in p.items())
                   for x in itertools.product((False,True),repeat=9))
    assert (pinned_count(a),pinned_count(b))==(0,2)
    records=[]
    for t in (0,1,2,4,8,16,64,256):
        F,n=union(U,t)
        assert valid(F,n)
        x=encode(F,n)
        ans,read,mode=decide(x,U)
        want=len(gamma(n))+len(gamma(len(F)))+264*(1+3*n.bit_length())
        assert (ans,read,mode)==(False,want,'certified-unsat-prefix')
        records.append({'t':t,'N':len(x),'prefix_reads':read})
    for F,n in ((F9,9),(Y6,6)):
        x=encode(F,n);ans,read,mode=decide(x,U)
        assert ans and read==len(x) and mode=='exact-fallback'
        for bad in (x[:-1],x[:-1]+'2'):
            assert decide(bad,U)[0] is False
    print(json.dumps({'status':'PASS','cases':records,
     'same_original_F9_SAT_UNSAT':(2,0),'F9_models':70,'Y6_models':20,
     'U198_UNSAT_certificate':'see independently replayed LSPV1_309 verifier'},
     indent=2))
if __name__=='__main__':main()
