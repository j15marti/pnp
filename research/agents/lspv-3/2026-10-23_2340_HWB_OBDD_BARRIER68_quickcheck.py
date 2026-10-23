#!/usr/bin/env python3
"""HWB-OBDD-BARRIER68 independent stdlib quickcheck.
No random inputs. This checks exact proper3CNF source construction,
independent single sign-bit supports, witness replay and all OBDD
orders through h=7. Small checks do not prove asymptotic OBDD hardness.
Full DPLL and raw audit are in the standalone LSPV-3 handoff.
"""
import itertools
import math

def hwb(b):
    t = sum(b)
    return int(t > 0 and b[t-1] == 1)

class CNF:
    def __init__(self):
        self.n = 0
        self.cl = []
        self.gates = []
    def new(self):
        self.n += 1
        return self.n
    def add(self, *l):
        assert len(l) in (2,3) and len({abs(x) for x in l}) == len(l)
        self.cl.append(tuple(l))
    def force(self, l):
        a,b=self.new(),self.new()
        for s in (a,-a):
            for t in (b,-b):
                self.add(l,s,t)
    def gate(self, typ, a, b=None):
        v=self.new()
        if typ=="NOT":
            self.add(v,a);self.add(-v,-a)
        elif typ=="AND":
            assert a!=b
            self.add(-v,a);self.add(-v,b);self.add(v,-a,-b)
        else:
            assert a!=b
            self.add(v,-a);self.add(v,-b);self.add(-v,a,b)
        self.gates.append((typ,v,a,b))
        return v
    def finish(self):
        source=list(self.cl)
        self.cl=[]
        for l in source:
            if len(l)==3:self.cl.append(l)
            else:
                z=self.new()
                self.cl.extend(((*l,z),(*l,-z)))
        assert all(len({abs(t) for t in l})==3 for l in self.cl)

def make(h, bits):
    c=CNF()
    zero=c.new();one=c.new()
    u=[c.new() for _ in range(h)]
    f=[c.new() for _ in range(h)]
    c.force(-zero);c.force(one)
    for i in range(h):
        c.force(-f[i])
        c.add(u[i] if bits[i] else -u[i],zero,f[i])
    neg=[c.gate("NOT",x) for x in u]
    prev=[one]+[zero]*h
    for i in range(h):
        nxt=[]
        for j in range(h+1):
            a=c.gate("AND",prev[j],neg[i])
            b=c.gate("AND",prev[j-1] if j else zero,u[i])
            nxt.append(c.gate("OR",a,b))
        prev=nxt
    y=zero
    for j in range(1,h+1):
        y=c.gate("OR",y,c.gate("AND",prev[j],u[j-1]))
    c.force(y);c.finish()
    m=len(c.cl)
    w=math.ceil(math.log2(64*(c.n+m+1)))
    words=[c.n,m]
    for l in c.cl:
        words.extend([3]+[2*abs(v)+int(v<0) for v in l])
    encoded=''.join(f'{x:0{w}b}' for x in words)
    assert len(encoded)==(4*m+2)*w
    return c, encoded, (zero,one,u,f),w

def witness_check(c,aux,bits):
    zero,one,u,f=aux
    val={i:0 for i in range(1,c.n+1)}
    val[zero]=0;val[one]=1
    for i,b in enumerate(bits):val[u[i]]=b
    for op,v,a,b in c.gates:
        if op=="NOT":val[v]=1-val[a]
        elif op=="AND":val[v]=val[a]&val[b]
        else:val[v]=val[a]|val[b]
    good=all(any(val[abs(x)] if x>0 else 1-val[abs(x)] for x in cl) for cl in c.cl)
    assert good==bool(hwb(bits))

def obddsize(h,order,fn):
    table=[fn(tuple((mask>>i)&1 for i in range(h))) for mask in range(1<<h)]
    unique={}
    def visit(depth,mask):
        if depth==h:return table[mask]
        j=order[depth]
        lo=visit(depth+1,mask)
        hi=visit(depth+1,mask|(1<<j))
        if lo==hi:return lo
        key=(j,lo,hi)
        if key not in unique:unique[key]=len(unique)+2
        return unique[key]
    visit(0,0)
    return len(unique)

def run():
    for h in range(1,8):
        base=tuple(0 for _ in range(h))
        _,x,_,w=make(h,base)
        seen=0
        for b in itertools.product((0,1),repeat=h):
            c,y,aux,ww=make(h,b)
            assert ww==w
            assert c.n==9*h*h+22*h+8
            assert len(c.cl)==15*h*h+34*h+12
            assert len(y)==len(x)
            assert sum(z!=t for z,t in zip(x,y))==sum(b)
            witness_check(c,aux,b)
            seen+=1
        minhw=min(obddsize(h,o,hwb) for o in itertools.permutations(range(h)))
        minpar=min(obddsize(h,o,lambda b:sum(b)%2) for o in itertools.permutations(range(h)))
        print('h',h,'sources',seen,'minimum_HWBOBDD',minhw,
              'minimum_parityOBDD',minpar)
    print('COMPUTATIONAL, no asymptotic claim')
if __name__=='__main__':run()
