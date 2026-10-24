#!/usr/bin/env python3
"""Compact peer-checkable exact pinned-child byte oracle and two-level semantics.
Restricted pinned proper-3CNF model. Not a lower bound on SAT decision time.
"""
from itertools import product
import json

def wd(n,m): return (64*(n+m+1)-1).bit_length()
def code(lit): return 2*abs(lit)+(lit<0)
def enc(n,cls):
    h=wd(n,len(cls)); vals=[n,len(cls)]
    for c in cls:
        assert len(c)==3 and len(set(map(abs,c)))==3
        vals += [code(z) for z in c]+[0]
    return ''.join(f'{int(v):0{h}b}' for v in vals)
def gadget(x,v,u,z):
    return [(v if x else -v,a*u,b*z) for a,b in ((1,1),(1,-1),(-1,1),(-1,-1))]
def child(n,cls,pins):
    out=list(cls)
    for i,(v,b) in enumerate(pins):out+=gadget(b,v,n+2*i+1,n+2*i+2)
    return enc(n+2*len(pins),out),out

def lazy_bit(original,n,cls,pins,i):
    m=len(cls);p=len(pins);h0=wd(n,m);h=wd(n+2*p,m+4*p)
    ix=i//h;off=i%h
    if ix<2:word=(n+2*p,m+4*p)[ix]
    else:
        ci=(ix-2)//4;slot=(ix-2)%4
        if ci<m:
            src=(2+4*ci+slot)*h0
            word=int(original[src:src+h0],2)
        else:
            k=(ci-m)//4;g=(ci-m)%4;v,b=pins[k]
            u=n+2*k+1;z=u+1
            c=gadget(b,v,u,z)[g]
            word=0 if slot==3 else code(c[slot])
    return (word>>(h-1-off))&1

def satisfies(cls,assignment):
    return all(any(assignment[abs(x)-1]==(x>0) for x in c) for c in cls)
def can(n,cls,pins=()):
    return any(satisfies(cls,a) and all(a[v-1]==b for v,b in pins)
               for a in product((0,1),repeat=n))

def run():
    all8=[tuple((j+1 if (bits[j]==0) else -(j+1)) for j in range(3))
          for bits in product((0,1),repeat=3)]
    controls=[('seven_SAT',3,all8[:-1]),('eight_UNSAT',3,all8),
              ('Horn',3,[(-1,-2,3)]),('two_components',6,[(1,2,3),(4,5,6)]),
              ('padded_2SAT',3,[(1,-2,3),(1,-2,-3)])]
    tested=0;passes=0;yes=0;no=0;conflicts=0
    for name,n,cls in controls:
        original=enc(n,cls)
        for v in range(1,min(n,3)+1):
            for b in (0,1):
                P=[(v,b)];full,fullcls=child(n,cls,P)
                assert len(full)>len(original)
                for i,bit in enumerate(full):
                    assert lazy_bit(original,n,cls,P,i)==int(bit)
                    passes+=1
                answer=can(n,cls,P)
                assert answer==can(n+2,len(fullcls) and fullcls)
                yes+=answer;no+=not answer;tested+=1
                for z in (0,1):
                    # Actual second-level pin on the SAME source variable.
                    _,lvl2=child(n+2,fullcls,[(v,z)])
                    result=can(n+4,lvl2)
                    assert result==(answer if z==b else False)
                    conflicts+=(z!=b)
    print(json.dumps({'controls':len(controls),'pinned_children':tested,
                      'SAT':yes,'UNSAT':no,'child_bits_checked':passes,
                      'two_level_checks':2*tested,'conflicting_second_pins':conflicts,
                      'unexpected_discrepancies':0},sort_keys=True,indent=2))
if __name__=='__main__':run()
