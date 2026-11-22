"""Independent compiler-layout audit. No native TM or target SAT benchmark."""
from itertools import product
import json
import hashlib
from pathlib import Path

def word(c):
    p=[(c[0],1)]
    for x in c[1:]:
        p=p+[(x,0)]+[(a,-s) for a,s in reversed(p)]+[(x,0)]
    return p

def sizes(d,c):
    g=max(3,2*((c+1)//2)+1)
    n0=d+(10*c+1)*g+2
    m0=(20*c+4)*g
    n=n0+m0+3
    m=2*m0+4
    w=n.bit_length()
    h=n+2+2*((m+1).bit_length()-1)
    return g,n0,m0,n,m,w,h,h+3*m*(w+1)+2*n+w

def gamma(x):
    b=bin(x)[2:]
    return '0'*(len(b)-1)+b

def literal(x,w):
    return str(int(x<0))+format(abs(x),f'0{w}b')

def encode(cs):
    d=max(abs(x) for c in cs for x in c)
    g,n0,m0,n,m,w,h,N=sizes(d,len(cs))
    p=[x for c in cs for x in word(c)]
    state=lambda j,v:d+1+j*g+v
    pad=n0-1
    base=[]
    for pin in [state(0,0)]+[-state(len(p),v) for v in range(1,g)]:
        base.extend((pin,a*pad,b*n0) for a,b in product((1,-1),repeat=2))
    for j,(x,action) in enumerate(p):
        for v in range(g):
            for bit in (0,1):
                dest=v if bit==int(x>0) else ((-v if action==0 else v+action)%g)
                base.append((-state(j,v),abs(x) if bit==0 else -abs(x),state(j+1,dest)))
    y,u,v=n0+1,n0+2,n0+3
    target=[(y,u,v),(y,u,-v),(y,-u,v),(y,-u,-v)]
    for k,(a,b,c) in enumerate(base):
        z=n0+4+k
        target.extend([(-y,a,z),(-z,b,c)])
    alpha=''.join(str(int(i==u)) for i in range(1,n+1))
    beta=''.join(str(int(i in (u,v))) for i in range(1,n+1))
    bits='1'*n+'0'+gamma(m+1)+''.join(literal(x,w) for c in target for x in c)+alpha+beta+format(y,f'0{w}b')
    assert len(bits)==N and len(target)==m
    return bits

def support(d,c,changes):
    # Changes (source-clause index, literal slot, old positive ID,new ID).
    g,n0,m0,n,m,w,h,N=sizes(d,c)
    offsets=[]
    slots=word((1,2,3))
    for k,slot,old,new in changes:
        bitdiff=[i for i,(a,b) in enumerate(zip(format(old,f'0{w}b'),format(new,f'0{w}b'))) if a!=b]
        for u,(x,_) in enumerate(slots):
            if x!=slot+1:
                continue
            layer=10*k+u
            for vertex in range(g):
                for bit in (0,1):
                    base_index=4*g+2*g*layer+2*vertex+bit
                    target_index=5+2*base_index
                    start=h+3*target_index*(w+1)+(w+1)+1
                    offsets.extend(start+i for i in bitdiff)
    return set(offsets)

def main():
    base=[(1,3,4),(2,3,4),(1,2,3)]
    strings=[]
    full=[]
    for b in product((0,1),repeat=2):
        cs=list(base)
        if b[0]:cs[0]=(2,3,4)
        if b[1]:cs[1]=(1,3,4)
        s=encode(cs)
        strings.append(s)
    for j in range(2):
        expected=support(4,3,[(j,0,1 if j==0 else 2,2 if j==0 else 1)])
        for i,b in enumerate(product((0,1),repeat=2)):
            other=i^(2 if j==0 else 1)
            actual={k for k,(a,z) in enumerate(zip(strings[i],strings[other])) if a!=z}
            assert actual==expected
        full.append(len(expected))
    assert support(4,3,[(0,0,1,2)]).isdisjoint(support(4,3,[(1,0,2,1)]))
    controls=[]
    for q in range(1,9):
        t=22*q+33;d=8*t;c=596*q+894
        used=set(); entries=[]
        for j in range(1,q+1):
            # appended parity row index 6j+7; preceding CNF has 26t clauses.
            k0=26*t+4*(6*j+7)
            old=3*(5*(q+2+j)+1)+3
            new=3*(5*(j+1)+1)+3
            ss=support(d,c,[(k0+e,0,old,new) for e in range(4)])
            g,*_=sizes(d,c)
            assert len(ss)==32*g*(old^new).bit_count()
            assert ss and used.isdisjoint(ss)
            used.update(ss)
            entries.append(dict(j=j,count=len(ss),first=min(ss),last=max(ss),
                sha256=hashlib.sha256(','.join(map(str,sorted(ss))).encode()).hexdigest()))
        controls.append(dict(q=q,N=sizes(d,c)[-1],regions=entries))
    print(json.dumps(dict(status='COMPUTATIONAL',full_small_images=4,
        full_small_N=len(strings[0]),full_diff_counts=full,cycle_sparse_controls=controls,
        scope='full small compiler strings plus exact sparse cycle offsets; no full cycle image allocation or native TM',
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2))

if __name__=='__main__':main()
