#!/usr/bin/env python3
"""Original-clause indexed S/U/inversion, exact US & UU moments, brute controls.
Independent compact checker. Full charged 16-family Python/JSON in local ZIP.
"""
from itertools import product
from fractions import Fraction

H_ONLY = ((1,2,4),(1,2,-3),(-1,2,3),(-1,-3,-4),(2,3,-4),
          (1,-3,4),(1,3,-4),(-2,3,4),(-1,3,-4))
CORE = ((1,2,3),(1,2,-3),(-1,-2,-3))
CUBE = ((1,2,3),(1,2,-3),(1,-2,3),(1,-2,-3))
ALL8 = tuple(tuple((i+1)*s[i] for i in range(3))
             for s in product((-1,1), repeat=3))
OVERLAP = ALL8 + tuple(tuple((1,2,4)[i]*s[i] for i in range(3))
                       for s in product((-1,1), repeat=3))

def target(c, mode):
    return {abs(l): int(l>0) if mode=='S' else int(l<0) for l in c}

def merged(j, jm, k, km):
    a,b=target(j,jm),target(k,km)
    return all(a[x]==b[x] for x in a.keys() & b.keys())

def modes(j,k):
    a,b=target(j,'S'),target(k,'S')
    same=any(a[x]==b[x] for x in a.keys() & b.keys())
    opp=any(a[x]!=b[x] for x in a.keys() & b.keys())
    return {'SS':not opp,'SU':not same,'US':not same,'UU':not opp}

def hit(c,a):
    return sum(int(a[abs(z)]==int(z>0)) for z in c)

def moments(F):
    mu=sum((Fraction(1,1<<len(c)) for c in F),Fraction())
    def w(j,jm,k,km):
        a,b=target(F[j],jm),target(F[k],km)
        if any(a[x]!=b[x] for x in a.keys() & b.keys()):
            return Fraction()
        return Fraction(1,1<<len(a.keys() | b.keys()))
    gamma=sum((w(j,'U',k,'S') for j in range(len(F))
               for k in range(len(F)) if j!=k),Fraction())
    b2=mu-sum((w(j,'U',k,'U') for j in range(len(F))
                for k in range(j+1,len(F))),Fraction())
    return mu,gamma,b2,gamma-2*mu+2

def run(F,pin=None):
    pin=pin or {}
    assert all(len(c)==len(set(map(abs,c))) for c in F)
    for j,c in enumerate(F):
        s,u=target(c,'S'),target(c,'U')
        for x in s:
            assert s[x]+u[x]==1
        for k in range(j):
            mode=modes(F[k],c)
            for key,val in mode.items():
                assert val==merged(F[k],key[0],c,key[1])
    R=[]
    for c in F:
        if any(abs(z) in pin and pin[abs(z)]==int(z>0) for z in c):
            continue
        d=tuple(z for z in c if abs(z) not in pin)
        if not d:
            raise ValueError('pin already falsifies source clause')
        R.append(d)
    mu,gamma,b2,H=moments(R)
    free=sorted({abs(z) for c in R for z in c})
    oracle=[0,0,0,0]
    dist=[0,0,0,0]
    endpoints=[]
    for vec in product((0,1),repeat=len(free)):
        a=dict(zip(free,vec))
        z0=sum(hit(c,a)==0 for c in R)
        z3=sum(hit(c,a)==len(c) for c in R)
        oracle[0]+=z0;oracle[1]+=z0*z3
        oracle[2]+=z0-z0*(z0-1)//2
        oracle[3]+=z0*z3-z0-z3+2
        dist[min(3,z0)]+=1
        if all(v==0 for v in vec) or all(v==1 for v in vec):
            endpoints.append((vec,z0,z3))
    denom=1<<len(free)
    assert (mu,gamma,b2,H)==tuple(Fraction(k,denom) for k in oracle)
    sat=dist[0]>0
    assert (gamma<1 or H<1) <= sat
    assert (b2==1)==(dist[0]==0 and dist[3]==0)
    return {'clauses':len(R),'free':len(free),
            'mu64':str(64*mu),'gamma64':str(64*gamma),
            'H64':str(64*H),'B2_64':str(64*b2),
            'SAT':sat,'global_endpoints':endpoints}

def main():
    for label,F,pin in (
        ('both_endpoints_fail_SAT',CORE,{}),
        ('H_only_SAT',H_ONLY,{}),
        ('post_UP_forbidden_cube',CUBE,{1:0}),
        ('all8_UNSAT',ALL8,{}),
        ('overlap16_UNSAT',OVERLAP,{})):
        print(label,run(F,pin))
    assert run(H_ONLY)['gamma64']=='72'
    assert run(H_ONLY)['H64']=='56'
    assert run(CUBE,{1:0})['B2_64']=='64'
    for mask in range(256):
        F=tuple(c for j,c in enumerate(ALL8) if mask&(1<<j))
        if F:run(F)
    print('PASS: 256 exhaustive signed subfamilies + five named source-indexed controls')
if __name__=='__main__':
    main()
