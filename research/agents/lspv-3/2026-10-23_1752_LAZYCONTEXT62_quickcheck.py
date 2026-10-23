#!/usr/bin/env python3
"""Small independent no-dependency audit of LAZY-CONTEXT-EXTRACT62."""
from itertools import product

def gadget(lit, a, b):
    return [(lit,u,v) for u in (a,-a) for v in (b,-b)]

def family(h, contradictory=False):
    cls=[]
    for i in range(h):
        x,y=i+1,h+i+1
        p,q=2*h+2*i+1,2*h+2*i+2
        cls += [(-x,y,p),(-x,y,-p),(x,-y,q),(x,-y,-q)]
    cls+=gadget(h+1,4*h+1,4*h+2)
    if contradictory:cls+=gadget(-1,4*h+3,4*h+4)
    return cls

def sat(clauses):
    def recurse(F,env):
        while True:
            rem=[];unit=[]
            for C in F:
                if any((abs(l) in env and env[abs(l)]==(l>0)) for l in C):continue
                u=[l for l in C if abs(l) not in env]
                if not u:return False
                if len(u)==1:unit.append(u[0])
                rem.append(u)
            if not rem:return True
            if not unit:break
            changed=False
            for l in unit:
                k=abs(l);v=l>0
                if k in env and env[k]!=v:return False
                if k not in env:env[k]=v;changed=True
            if not changed:break
            F=rem
        x=abs(min(rem,key=len)[0])
        for value in (False,True):
            d=env.copy();d[x]=value
            if recurse(rem,d):return True
        return False
    return recurse(clauses,{})

def condition(F,first_vars,values,n):
    out=list(F)
    for var,val in zip(first_vars,values):
        n+=2
        out+=gadget(var if val else -var,n-1,n)
    return out,n

def main():
    roots=0;contexts=0;proj=0
    for h in range(1,7):
        F=family(h)
        assert sat(F) and not sat(family(h,True));roots+=2
        for a in product((0,1),repeat=h):
            C,n=condition(F,range(1,h+1),a,4*h+2)
            assert sat(C)==bool(a[0]);contexts+=1
            if h<=5:
                for y in product((0,1),repeat=h):
                    Z,_=condition(C,range(h+1,2*h+1),y,n)
                    assert sat(Z)==(a[0]==1 and y==a)
                    proj+=1
    assert (roots,contexts,proj)==(12,126,1364)
    print({'root_checks':roots,'context_checks':contexts,'projected_checks':proj,'errors':0})

if __name__=='__main__':main()
