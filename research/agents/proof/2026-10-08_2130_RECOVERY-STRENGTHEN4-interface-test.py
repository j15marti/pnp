"""Independent virtual-bit and restriction-fiber checks, bounded by 25s."""
import signal,time,json,itertools,collections,hashlib
from pathlib import Path
signal.alarm(25);start=time.monotonic()
def gamma(x):
    b=bin(x)[2:];return '0'*(len(b)-1)+b
def header(n,m):return gamma(n+1)+gamma(m+1)
def encode(f,n):
    w=n.bit_length()
    return header(n,len(f))+''.join(format(len(c),'02b')+''.join(('1' if v>0 else '0')+format(abs(v),f'0{w}b') for v in c) for c in f)
def parity(t):
    return tuple(tuple(-v if b else v for v,b in zip(t,bs)) for bs in itertools.product((0,1),repeat=3) if sum(bs)%2==1)
def gadget(i,n):
    h,r,a,b,c,d=range(n+1,n+7)
    if i==0:return (h,r)
    if i<=4:return parity((h,a,b))[i-1]
    if i<=8:return parity((h,c,d))[i-5]
    v=i-8;return h,v,n+6+v
def parse(s):
    pos=0;out=[]
    for _ in range(2):
        k=0
        while s[pos]=='0':k+=1;pos+=1
        out.append(int(s[pos:pos+k+1],2)-1);pos+=k+1
    return *out,pos
def outbit(s,j):
    n,m,hs=parse(s);nn=2*n+6;hh=header(nn,m+n+9)
    if j<len(hh):return hh[j]
    j-=len(hh);w=n.bit_length();ww=nn.bit_length();l3=2+3*(1+ww);l2=2+2*(1+ww)
    if j<m*l3:
        c,t=divmod(j,l3)
        if t<2:return '1'
        lit,t=divmod(t-2,1+ww);src=hs+c*(2+3*(1+w))+2+lit*(1+w)
        if t==0:return s[src]
        if t<=ww-w:return '0'
        return s[src+t-(ww-w)]
    j-=m*l3
    if j<l2:i,t=0,j
    else:i,t=divmod(j-l2,l3);i+=1
    c=gadget(i,n)
    if t<2:return format(len(c),'02b')[t]
    lit,t=divmod(t-2,1+ww);v=c[lit]
    return ('1' if v>0 else '0') if t==0 else format(abs(v),f'0{ww}b')[t-1]
bitchecks=0;cases=[]
for n in (3,4,5,7,8,15,16,31,32):
    f=tuple((i+1,-((i+1)%n+1),(i+2)%n+1) for i in range(n))
    source=encode(f,n);g=f+tuple(gadget(i,n) for i in range(n+9));out=encode(g,2*n+6)
    rebuilt=''.join(outbit(source,j) for j in range(len(out)))
    assert rebuilt==out
    bitchecks+=len(out);cases.append({'n':n,'input_bits':len(source),'output_bits':len(out)})
# F3, total degree <=2, E(t)=(t,t+1). Coefficient order 1,x,y,x²,xy,y².
fibers=collections.Counter()
for a,b,c,d,e,f in itertools.product(range(3),repeat=6):
    image=((a+c+f)%3,(b+c+e+2*f)%3,(d+e+f)%3)
    fibers[image]+=1
assert len(fibers)==27 and set(fibers.values())=={27}
signal.alarm(0)
print(json.dumps({'passed':True,'local_output_bit_checks':bitchecks,'cases':cases,
 'entropy_domain_polynomials':729,'entropy_fibers':len(fibers),'each_fiber_size':27,
 'kernel_dimension':3,'entropy_loss_bits':'3 log2(3), sharp on uniform kernel',
 'seconds':time.monotonic()-start,'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'scope':'Finite exact interfaces; formal resource bounds proved separately.'},indent=2))
