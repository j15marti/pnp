#!/usr/bin/env python3
"""Compact independent reproducer for HORN-SELECTOR-DEGREE60.
The 10,378-check full audit is horn_selector60_audit.py, not this mini.
Python stdlib only. Independent source and lifted brute-force SAT counts.
"""
from itertools import product
from random import Random

R = Random(202610231217)
checks = 0

def ok(test):
    global checks
    checks += 1
    if not test:
        raise AssertionError('check ' + str(checks))

def satisfied(cnf, bits):
    return all(any(((bits >> (abs(l)-1)) & 1) == (l > 0)
                   for l in c) for c in cnf)

def lift(n, source):
    b, t = [], []
    for j, c in enumerate(source):
        s = [n+3*j+a+1 for a in range(3)]
        t.append(tuple(s))
        b.extend([(-s[a],c[a]) for a in range(3)])
    return n+3*len(source), b+t, b, t

def match(n,source):
    mate = [-1]*(n+1)
    def aug(j,seen):
        for l in source[j]:
            v = abs(l)
            if v not in seen:
                seen.add(v)
                if mate[v]<0 or aug(mate[v],seen):
                    mate[v]=j
                    return True
        return False
    for j in range(len(source)):
        if not aug(j,set()):
            return None
    selected = {}
    for v,j in enumerate(mate):
        if j>=0:
            selected[j] = next(l>0 for l in source[j] if abs(l)==v)
    bits = 0
    for v,j in enumerate(mate):
        if j>=0 and selected[j]:bits |= 1<<(v-1)
    return bits

def randclause(n):
    idx=R.sample(range(1,n+1),3)
    return tuple(v if R.randrange(2) else -v for v in idx)

def tests():
    for n in (3,4,5,8,12,20):
        for trial in range(60):
            deg=[0]*(n+1); src=[]
            for j in range(3*n):
                c=randclause(n)
                if all(deg[abs(l)]<3 for l in c):
                    src.append(c)
                    for l in c:deg[abs(l)]+=1
            witness=match(n,src)
            ok(witness is not None)
            ok(satisfied(src,witness))
            nn,H,B,D=lift(n,src)
            ok(len(B)==3*len(src) and len(D)==len(src) and nn==n+3*len(src))
            ok(all(sum(l>0 for l in c)<=1 for c in B))
    for n in (3,4):
        for trial in range(35):
            source=[randclause(n) for _ in range(R.randint(1,3))]
            nn,H,B,D=lift(n,source)
            actual=sum(satisfied(H,z) for z in range(1<<nn))
            expected=0
            for x in range(1<<n):
                count=1
                for c in source:
                    t=sum(((x>>(abs(l)-1))&1)==(l>0) for l in c)
                    count*=2**t-1
                expected+=count
            ok(actual==expected)
            ok((actual>0)==any(satisfied(source,x) for x in range(1<<n)))
    cube=[tuple(signs[a]*(a+1) for a in range(3))
          for signs in product((-1,1), repeat=3)]
    ok(not any(satisfied(cube,x) for x in range(8)))
    ok(any(satisfied(cube[:-1],x) for x in range(8)))
    for q in range(1,7):
        for bits in range(1<<q):
            z=list(range(1,q+2)); u=q+2;v=q+3
            source=[(z[0],u),(z[0],-u),(-z[-1],v),(-z[-1],-v)]
            source += [(-z[i], z[i+1] if (bits>>i)&1 else -z[i+1])
                       for i in range(q)]
            ok(any(satisfied(source,x) for x in range(1<<(q+3)))
               == (bits!=(1<<q)-1))
    print({'mini_checks':checks,'failures':0,'seed':202610231217,
           'scope':'finite reproducer only; universal lower bound OPEN'})

if __name__=='__main__':tests()
