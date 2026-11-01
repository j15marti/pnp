#!/usr/bin/env python3
"""LSPV-2 311 compact reproducible dynamic G_t decision-only segment DAG."""
from itertools import product
from collections import Counter
POS=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
NEG=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
A={1:1,2:0,3:1,4:0,8:0}
B={1:1,2:1,3:0,4:0,8:0}
def source(t):
    rows=[]
    for i in range(t):
        rows += [tuple(9*((i+1)%t)+5 if j==0 and x==5 else 9*i+x for x in C)
                 for j,C in enumerate(POS)]
        rows += [tuple(-9*i-x for x in C) for C in NEG]
    return rows
def valid(F,n):
    if n<1 or 3*len(F)!=4*n:return False
    c=Counter();seen=set()
    for C in F:
        if len(C)!=3 or len(set(map(abs,C)))!=3:return False
        if not(all(x>0 for x in C) or all(x<0 for x in C)):return False
        if any(abs(x)>n or x==0 for x in C):return False
        key=tuple(sorted(C))
        if key in seen:return False
        seen.add(key)
        c.update((abs(x),x>0) for x in C)
    return all(c[i,True]==2 and c[i,False]==2 for i in range(1,n+1))
def local(p):
    M=0
    for v in product((0,1),repeat=9):
        if any(v[x-1]!=a for x,a in p.items()):continue
        for b in (0,1):
            ok=all(any(b if j==0 and x==5 else v[x-1] for x in C)
                   for j,C in enumerate(POS))
            if ok:ok=all(any(not v[x-1] for x in C) for C in NEG)
            if ok:M|=1<<(2*v[4]+b)
    return M
def mul(a,b):
    return sum(1<<(2*i+k) for i in (0,1) for k in (0,1)
               if any((a&(1<<(2*i+j))) and (b&(1<<(2*j+k))) for j in (0,1)))
class Tree:
    def __init__(self,P):
        self.t=len(P);self.cap=1<<(self.t-1).bit_length()
        self.pin=[dict(p) for p in P];self.a=[9]*(2*self.cap);self.compositions=0
        for i,p in enumerate(self.pin):self.a[self.cap+i]=local(p)
        for i in range(self.cap-1,0,-1):self.a[i]=mul(self.a[2*i],self.a[2*i+1])
    def update(self,i,x,v):
        self.pin[i][x]=v;j=self.cap+i
        self.a[j]=local(self.pin[i])
        while j>1:
            j//=2;self.a[j]=mul(self.a[2*j],self.a[2*j+1]);self.compositions+=1
    def label(self):return bool(self.a[1]&9)
def exactG2(p,q):
    F=source(2);fix=dict(p);fix.update({9+k:v for k,v in q.items()})
    free=[i for i in range(1,19) if i not in fix];count=0
    for b in product((0,1),repeat=len(free)):
        v=dict(fix);v.update(zip(free,b))
        if all(any((v[abs(x)]==1)==(x>0) for x in C) for C in F):count+=1
    return count
assert valid(source(1),9) and valid(source(2),18)
assert local(A)==3 and local(B)==0
p8={1:0,3:0,6:0};p12={5:1};k2={1:0,5:0,6:0}
assert [local(x) for x in (p8,p12,k2)]==[8,12,2]
assert exactG2(p8,k2)==0 and exactG2(p12,k2)==299
assert exactG2(A,A)==1 and exactG2(B,A)==0
for t in (1,2,4,8,16,32,128):
    f=source(t);assert valid(f,9*t)
    tree=Tree([A]*t);assert tree.label()
    for i in range(t):
        for x,v in ((2,1),(3,0),(2,0),(3,1)):
            tree.update(i,x,v)
            assert tree.label()==(x==3 and v==1)
            if t<=8:
                root=9
                for p in tree.pin:root=mul(root,local(p))
                assert (tree.a[1]&9)==(root&9)
    assert tree.compositions==4*t*(tree.cap.bit_length()-1)
for t in (1,2,3):
    f=source(t);bad=f.copy();bad[0]=(-bad[0][0],)+bad[0][1:]
    assert not valid(bad,9*t) and not valid(f+[f[0]],9*t)
print("PASS restricted dynamic decision: both labels, canonical grammar, G2=0/299, t<=128")



# 312 addition: complete both-label semantic target child, after paid decision.
import ast,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
U_PATH=ROOT/'experiments/arc/lspv3_283/DOECKER61_original_source.txt'
U=[tuple(c) for c in ast.literal_eval(' '.join(s for s in U_PATH.read_text().splitlines() if not s.startswith('#')))]
Y=[tuple(c) for c in ((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))]
def ga(k):
    s=bin(k)[2:];return '0'*(len(s)-1)+s
def encoded(F,n):
    w=n.bit_length()
    return ga(n)+ga(len(F))+''.join(('1' if c[0]>0 else '0')+''.join(format(abs(x),f'0{w}b') for x in c) for c in F)
def Nbits(t):
    n=9*t;m=12*t;w=n.bit_length()
    return len(ga(n))+len(ga(m))+m*(1+3*w)
def child(t,pins):
    F=source(t);assert valid(F,9*t)
    decision=9
    masks=[]
    for pin in pins:
        mask=local(pin)    # 1024 fixed-block candidate trials, fully paid
        masks.append(mask)
        decision=mul(decision,mask)
    yes=bool(decision&9)
    C,n=(Y,6) if yes else (U,198)
    assert valid(C,n)
    return yes,masks,encoded(C,n)
assert len(encoded(Y,6))==92 and len(encoded(U,198))==6632
for t in (1,2,4,8,16,128):
    pa=[dict(A) for _ in range(t)]
    pb=[dict(A) for _ in range(t)];pb[t//2]=dict(B)
    sa,ma,ca=child(t,pa);sb,mb,cb=child(t,pb)
    assert sa and not sb and len(ca)==92 and len(cb)==6632
    assert Nbits(t)==len(encoded(source(t),9*t))
assert Nbits(60086)==43983030 and Nbits(60087)==43983762
assert 43983030<6632**2<43983762 and Nbits(28)<92**2<Nbits(29)
assert len(set(tuple(sorted(c)) for c in U))==len(U)
print("PASS 312: same-original both labels, valid canonical Y6/U198 emitted, exact power-short threshold t=60087")
