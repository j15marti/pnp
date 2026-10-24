#!/usr/bin/env python3
"""TWOHEAD86 compact independent-head reproduction, Python 3 standard library."""
import itertools

def source(u,v):
    F=[]; k=len(u)
    for h,bits in enumerate((u,v)):
        for i,b in enumerate(bits):
            x=5*i+1; a=x+1+2*h; c=x+2+2*h
            F.extend((x if b else -x,sa*a,sc*c)
                     for sa in (1,-1) for sc in (1,-1))
    return tuple(F)

def encoding(F,n):
    return [n,len(F)]+[x for C in F for x in (3,*C)]

class Head:
    def __init__(self,tape):
        self.tape=tape; self.pos=0; self.moves=0; self.reads=0
    def move(self,to):
        self.moves+=abs(self.pos-to); self.pos=to
    def read(self,to):
        self.move(to); self.reads+=1; return self.tape[to]
    def work(self): return self.moves+self.reads

def signed_site(k,h,i):
    return 3+16*(h*k+i)

def validate(tape,n,k,head):
    if head.read(0)!=n or head.read(1)!=8*k:return False
    for h in (0,1):
        for i in range(k):
            x=5*i+1; a=x+1+2*h; b=x+2+2*h; saved=None
            for j in range(4):
                off=2+16*(h*k+i)+4*j
                w,lit,y,z=[head.read(off+t) for t in range(4)]
                if (w!=3 or abs(lit)!=x
                    or y!=(a if j<2 else -a)
                    or z!=(b if j%2==0 else -b)
                    or (saved is not None and lit!=saved)):
                    return False
                saved=lit
    return True

def two_head(F,n):
    if n%5 or len(F)!=(8*(n//5)):return None,0
    k=n//5; tape=encoding(F,n)
    left=Head(tape); right=Head(tape)
    if not validate(tape,n,k,left):return None,left.work()
    left.move(signed_site(k,0,0))
    right.move(signed_site(k,1,0))
    for i in range(k):
        u=left.read(signed_site(k,0,i))
        v=right.read(signed_site(k,1,i))
        if (u>0)!=(v>0):
            return False,left.work()+right.work()
    return True,left.work()+right.work()

def one_head(F,n,batch):
    if n%5 or len(F)!=(8*(n//5)):return None,0
    k=n//5; tape=encoding(F,n); head=Head(tape)
    if not validate(tape,n,k,head):return None,head.work()
    for lo in range(0,k,batch):
        hi=min(k,lo+batch)
        memo=[head.read(signed_site(k,0,i))>0 for i in range(lo,hi)]
        for j,i in enumerate(range(lo,hi)):
            if memo[j]!=(head.read(signed_site(k,1,i))>0):
                return False,head.work()
    return True,head.work()

def brute(F,n):
    for mask in range(1<<n):
        if all(any(bool(mask&(1<<(abs(l)-1)))==(l>0) for l in C)
               for C in F):return True
    return False

def run():
    checks=0
    for k in (1,2):
        for u in itertools.product((0,1),repeat=k):
            for v in itertools.product((0,1),repeat=k):
                F=source(u,v); expected=u==v
                assert brute(F,5*k)==expected; checks+=1
                assert two_head(F,5*k)[0]==expected; checks+=1
                assert one_head(F,5*k,1)[0]==expected; checks+=1
    for k in (4,8,16,32,64,128,256):
        u=tuple((7*i+i//3)%2 for i in range(k))
        for loc in (None,0,k//2,k-1):
            v=list(u)
            if loc is not None:v[loc]^=1
            F=source(u,tuple(v))
            assert two_head(F,5*k)[0]==(loc is None);checks+=1
            assert one_head(F,5*k,1)[0]==(loc is None);checks+=1
            assert one_head(F,5*k,k.bit_length())[0]==(loc is None);checks+=1
        x=source(u,u)
        print(k,*(f"{v[1]:,}" for v in
              (two_head(x,5*k),one_head(x,5*k,1),
               one_head(x,5*k,k.bit_length()))))
    print("TWOHEAD86 compact assertions:",checks, "failures: 0")

if __name__=="__main__":run()
