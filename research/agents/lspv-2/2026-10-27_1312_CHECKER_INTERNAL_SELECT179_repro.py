#!/usr/bin/env python3
"""LSPV-2 CHECKER-INTERNAL-SELECT179.

Independent complete bitonic total-witness verifier emitter, independent
parameter-only checker GateAt and inverse Rank/Select. Finite oracle is only
for regression. No SAT oracle, incidence cache, stored consumer table, or
low-space claim for whole verifier evaluation.
"""
from __future__ import annotations
import argparse
import collections
import itertools
import json
from pathlib import Path

class Net:
    def __init__(self,N,q):
        self.N,self.q=N,q
        self.c0=N+q+1;self.c1=N+q+2
        self.base=N+q+3
        self.gates=[]
    def g(self,op,x,y):
        assert op in ('and','or')
        assert x and y and abs(x)<self.base+len(self.gates) and abs(y)<self.base+len(self.gates)
        g=len(self.gates);self.gates.append((op,x,y));return self.base+g
    def a(self,x,y):return self.g('and',x,y)
    def o(self,x,y):return self.g('or',x,y)
    def xor(self,x,y):return self.o(self.a(x,-y),self.a(-x,y))
    def eq(self,x,y):return -self.xor(x,y)
    def mux(self,sw,x,y):return self.o(self.a(-sw,x),self.a(sw,y))
    def tree(self,src,op):
        assert src
        while len(src)>1:
            src=[self.g(op,src[i],src[i+1]) if i+1<len(src) else src[i]
                 for i in range(0,len(src),2)]
        return src[0]
    def bits_eq(self,xx,yy):return self.tree([self.eq(x,y) for x,y in zip(xx,yy)],'and')
    def bits_lt(self,xx,yy):
        less=self.c0; eq=self.c1
        for x,y in zip(reversed(xx),reversed(yy)):
            less=self.o(less,self.a(eq,self.a(-x,y)))
            eq=self.a(eq,self.eqxor(x,y))
        return less
    def eqxor(self,x,y):return -self.xor(x,y)
    def eval(self,xx,zz):
        assert len(xx)==self.N and len(zz)==self.q
        vals=[0]*(self.base+len(self.gates))
        vals[1:self.N+1]=xx
        vals[self.N+1:self.N+self.q+1]=zz
        vals[self.c1]=1
        for h,(op,a,b) in enumerate(self.gates):
            av=vals[abs(a)] ^ (a<0)
            bv=vals[abs(b)] ^ (b<0)
            vals[self.base+h]=(av & bv) if op=='and' else (av | bv)
        return vals

class Original:
    def __init__(self,q,m):
        assert q>=3 and m>=1
        self.q,self.m=q,m;self.w=q.bit_length()
        self.N=m*(1+3*(self.w+1));self.K=1<<((q+3*m-1).bit_length())
        self.h=self.K.bit_length()-1;self.J=self.h*(self.h+1)//2
        self.net=Net(self.N,q);self.layers=[];self._build()
    def cb(self,val,w):return [self.net.c1 if val>>j&1 else self.net.c0 for j in range(w)]
    def _build(self):
        n=self.net;w=self.w;K=self.K;m=self.m;q=self.q
        self.active=[];self.requests=[]
        for c in range(m):
            b=c*(1+3*(w+1))
            self.active.append(b+1)
            for j in range(3):
                first=b+2+j*(w+1)
                self.requests.append(([first+i for i in range(w)],first+w))
        r=[]
        for v in range(1,q+1):r.append(self.cb(v,w)+self.cb(0,2)+[self.N+v])
        for ids,sign in self.requests:r.append(ids+self.cb(1,2)+[sign])
        for i in range(K-len(r)):r.append(self.cb((1<<w)-1,w)+self.cb(2,2)+[n.c0])
        for lev in range(1,self.h+1):
            size=1<<lev;stride=size//2
            while stride:
                nxt=r[:];pairs=[]
                for i in range(K):
                    j=i^stride
                    if i>=j:continue
                    a=r[i];b=r[j]
                    aa=a[w:w+2]+a[:w];bb=b[w:w+2]+b[:w]
                    sw=n.bits_lt(bb,aa) if not i&size else n.bits_lt(aa,bb)
                    nxt[i]=[n.mux(sw,x,y) for x,y in zip(a,b)]
                    nxt[j]=[n.mux(sw,y,x) for x,y in zip(a,b)]
                    pairs.append((i,j,sw))
                self.layers.append(pairs);r=nxt;stride//=2
        self.Gf=len(n.gates)
        carry=n.c0;prev=None;payload=[]
        for ids in r:
            idx=ids[:w];kind=ids[w:w+2];p=ids[w+2]
            isas=n.bits_eq(kind,self.cb(0,2)); isq=n.bits_eq(kind,self.cb(1,2))
            same=n.c0 if prev is None else n.bits_eq(idx,prev)
            keep=n.a(-isas,n.a(same,carry))
            carry=n.o(n.a(isas,p),keep)
            payload.append(n.a(isq,carry)); prev=idx
        self.scan_end=len(n.gates)
        for pairs in reversed(self.layers):
            nxt=payload[:]
            for i,j,sw in pairs:
                nxt[i]=n.mux(sw,payload[i],payload[j]);nxt[j]=n.mux(sw,payload[j],payload[i])
            payload=nxt
        self.check_start=len(n.gates)
        self.lookup=payload[q:q+3*m]
        self.row_starts=[];out=[]
        for c in range(m):
            self.row_starts.append(len(n.gates));req=self.requests[3*c:3*c+3]
            truth=[];valid=[]
            for j,(ids,sgn) in enumerate(req):
                nonzero=n.tree(ids,'or')
                leq=-n.bits_lt(self.cb(q,w),ids)
                valid.append(n.a(nonzero,leq))
                truth.append(n.eq(sgn,self.lookup[3*c+j]))
            pairwise=[-n.bits_eq(req[j][0],req[k][0]) for j,k in ((0,1),(0,2),(1,2))]
            ok=n.a(n.tree(valid+pairwise,'and'),n.tree(truth,'or'))
            out.append(n.o(-self.active[c],ok))
        self.output=n.tree(out,'and')
        self.G=len(n.gates)
        assert self.G-self.check_start==m*(36*w+15)+m-1,(q,m,self.G,self.check_start)

class Shape:
    """All register-space statements refer to these integer parameters and
    arithmetic selectors, not to the materialized Original test fixture."""
    def __init__(self,q,m):
        assert q>=3 and m>=1
        self.q,self.m=q,m;self.w=q.bit_length()
        self.N=m*(1+3*(self.w+1));self.K=1<<((q+3*m-1).bit_length())
        self.h=self.K.bit_length()-1;self.J=self.h*(self.h+1)//2
        self.F=13*self.w+32
        self.Gf=self.K*self.h*(self.h+1)//4*self.F
        self.scan_end=self.Gf+19+(self.K-1)*(4*self.w+18)
        self.check_start=self.scan_end+3*self.K*self.J
        self.B=36*self.w+15
        self.final_start=self.check_start+self.m*self.B
        self.G=self.final_start+self.m-1
        self.c0=self.N+self.q+1;self.c1=self.N+self.q+2
        self.base=self.N+self.q+3


def tree_counts(n,level):
    """Number of nodes present at output level `level` (0=input leaves)."""
    for _ in range(level):n=(n+1)//2
    return n

def tree_prefix(n,level):
    """Number of gates in levels below `level`, level 1 first gates."""
    total=0
    for j in range(1,level):
        total+=tree_counts(n,j-1)//2
    return total

def tree_val(n,base,level,i,leaf):
    """Node at level indexed after applying levels of pair reductions.
    If this is an odd unpaired tail, trace the pass-through to the first
    earlier gate or an original leaf. Only constant-many log-sized registers.
    """
    while level>0:
        prev=tree_counts(n,level-1)
        if 2*i+1<prev:
            return base+tree_prefix(n,level)+i
        assert 2*i==prev-1
        i=2*i;level-=1
    assert 0<=i<n
    return leaf(i)

def tree_record(n,base,g,leaf,op):
    assert 0<=g<max(0,n-1)
    level=1
    while True:
        ct=tree_counts(n,level-1)//2
        pref=tree_prefix(n,level)
        if pref<=g< pref+ct:break
        level+=1
        assert level<=n.bit_length()+1
    idx=g-pref
    aa=tree_val(n,base,level-1,2*idx,leaf)
    bb=tree_val(n,base,level-1,2*idx+1,leaf)
    return (op,aa,bb)

def tree_parent(n,base,child_level,child_idx):
    """First parent of node at child_level, or None at tree root.
    The argument may be a primary leaf (level0) or a gate output.
    """
    level=child_level;i=child_idx
    while tree_counts(n,level)>1:
        count=tree_counts(n,level)
        if (i^1)<count:
            parent_gate=tree_prefix(n,level+1)+i//2
            return parent_gate
        assert i==count-1 and i%2==0
        i//=2;level+=1
    return None

def tree_own_level(n,g):
    level=1
    while True:
        pref=tree_prefix(n,level)
        t=tree_counts(n,level-1)//2
        if pref<=g<pref+t:return level,g-pref
        level+=1
        assert level<=n.bit_length()+1

def layer_at(S,l):
    cur=0
    for a in range(1,S.h+1):
        for b in range(a-1,-1,-1):
            if cur==l:return 1<<a,1<<b
            cur+=1
    raise AssertionError(l)

def reverse_payload(S,pos):
    """Absolute wire from layer-zero inverse routing, including source alias."""
    assert 0<=pos<S.K
    sz,stride=layer_at(S,0)
    low=pos&~stride
    r=(low//(2*stride))*stride+low%stride
    side=int(bool(pos&stride))
    return S.base+S.scan_end+3*S.K*(S.J-1)+6*r+3*side+2

def checker_clause_input(S,c,j):
    b=c*(1+3*(S.w+1))
    first=b+2+j*(S.w+1)
    return (lambda t:first+t),first+S.w

def xor_gate(b,off,a,bb):
    if off==0:return ('and',a,-bb)
    if off==1:return ('and',-a,bb)
    return ('or',b,b+1)

def eqbits_gate(S,base,off,n,xa,ya):
    if off<3*n:
        j,k=divmod(off,3)
        return xor_gate(S.base+base+3*j,k,xa(j),ya(j))
    treestart=base+3*n
    return tree_record(n,S.base+treestart,off-3*n,
                       lambda j:-(S.base+base+3*j+2),'and')

def checker_gateat(S,g):
    """Uniform GateAt for checker and final AND tree.
    Gate lists and input-dependent tables are NEVER constructed here.
    """
    assert S.check_start<=g<S.G
    if g>=S.final_start:
        return tree_record(S.m,S.base+S.final_start,g-S.final_start,
             lambda j:S.base+S.check_start+j*S.B+S.B-1,'and')
    c,off=divmod(g-S.check_start,S.B)
    block=S.check_start+c*S.B
    w=S.w
    if off<3*(8*w+3):
        j,k=divmod(off,8*w+3)
        idbit,sgn=checker_clause_input(S,c,j)
        first=block+j*(8*w+3)
        if k<w-1:
            return tree_record(w,S.base+first,k,idbit,'or')
        k-=w-1
        if k<7*w:
            t,e=divmod(k,7)
            x=S.c1 if (S.q>>(w-1-t))&1 else S.c0
            y=idbit(w-1-t)
            prev_eq=S.c1 if t==0 else S.base+first+(w-1)+7*(t-1)+6
            prev_l=S.c0 if t==0 else S.base+first+(w-1)+7*(t-1)+2
            b=S.base+first+(w-1)+7*t
            return [('and',-x,y),('and',prev_eq,b),('or',prev_l,b+1),
                    ('and',x,-y),('and',-x,y),('or',b+3,b+4),
                    ('and',prev_eq,-(b+5))][e]
        k-=7*w
        if k==0:
            nz=S.base+first+(w-2)
            le=S.base+first+(w-1)+7*(w-1)+2
            return ('and',nz,-le)
        k-=1
        return xor_gate(S.base+first+(w-1)+7*w+1,k,sgn,reverse_payload(S,S.q+3*c+j))
    off-=3*(8*w+3)
    if off<3*(4*w-1):
        j,k=divmod(off,4*w-1)
        a,b=((0,1),(0,2),(1,2))[j]
        id_a,_=checker_clause_input(S,c,a)
        id_b,_=checker_clause_input(S,c,b)
        return eqbits_gate(S,block+3*(8*w+3)+j*(4*w-1),k,w,id_a,id_b)
    off-=3*(4*w-1)
    pair_start=block+3*(8*w+3)+3*(4*w-1)
    def valid_leaf(j):
        if j<3:return S.base+block+j*(8*w+3)+w-1+7*w
        return -(S.base+block+3*(8*w+3)+(j-3)*(4*w-1)+4*w-2)
    if off<5:
        return tree_record(6,S.base+pair_start,off,valid_leaf,'and')
    off-=5
    truth_start=pair_start+5
    def truth_leaf(j):return -(S.base+block+j*(8*w+3)+8*w+2)
    if off<2:
        return tree_record(3,S.base+truth_start,off,truth_leaf,'or')
    if off==2:
        return ('and',tree_val(6,S.base+pair_start,3,0,valid_leaf),
                tree_val(3,S.base+truth_start,2,0,truth_leaf))
    assert off==3
    active=c*(1+3*(w+1))+1
    return ('or',-active,S.base+block+S.B-2)

def checker_consumers(S,g):
    """No incidence table, at most 36w+15 GateAt requests for a checker gate,
    plus one tree-parent computation if g is a row output."""
    assert S.check_start<=g<S.G
    refs=[]
    if g<S.final_start:
        c,off=divmod(g-S.check_start,S.B)
        for d in range(S.B):
            op,aa,bb=checker_gateat(S,S.check_start+c*S.B+d)
            for k,lit in enumerate((aa,bb)):
                if abs(lit)==S.base+g:
                    refs.append((S.check_start+c*S.B+d,k,1 if lit>0 else -1))
        if off==S.B-1 and S.m>1:
            p=tree_parent(S.m,S.base+S.final_start,0,c)
            if p is not None:
                op,aa,bb=checker_gateat(S,S.final_start+p)
                for k,lit in enumerate((aa,bb)):
                    if abs(lit)==S.base+g:
                        refs.append((S.final_start+p,k,1 if lit>0 else -1))
    else:
        lev,pos=tree_own_level(S.m,g-S.final_start)
        p=tree_parent(S.m,S.base+S.final_start,lev,pos)
        if p is not None:
            op,aa,bb=checker_gateat(S,S.final_start+p)
            for k,lit in enumerate((aa,bb)):
                if abs(lit)==S.base+g:
                    refs.append((S.final_start+p,k,1 if lit>0 else -1))
    return sorted(refs)

def checker_occurrences(S,g):
    """Proper 13-clause source output-variable occurrences, signed and
    physical.  Own gate rows plus four physical clone rows per consumer."""
    op,_,_=checker_gateat(S,g)
    own=([(13*g+8,2,1)]+[(13*g+r,1,-1) for r in range(9,13)]
         if op=='and' else
         [(13*g+8,2,-1)]+[(13*g+r,1,1) for r in range(9,13)])
    for h,slot,sign in checker_consumers(S,g):
        own.extend((13*h+4*slot+r,1,sign if r<2 else -sign) for r in range(4))
    if g==S.G-1:  # Full verifier output is independently PINNED TRUE.
        own.extend((13*S.G+4*S.N+8+r,0,+1) for r in range(4))
    return sorted(own)

def independently_emitted_gate_clause(O,h,r):
    """Independent copy of the exact 13-row source compiler, with signed
    operand-clone occurrences, source-wire aliases and fixed new variables."""
    op,x,y=O.net.gates[h]
    Sbase=O.net.base
    def wire(u):
        if abs(u)<Sbase:return u
        sign=1 if u>0 else -1
        return sign*(Sbase+9*(abs(u)-Sbase)+2)
    x,y=wire(x),wire(y)
    b=Sbase+9*h;uu=b;vv=b+1;out=b+2
    if r<4:
        old=(-uu,x) if r<2 else (uu,-x)
        p=b+3 if r<2 else b+4
        return old+(p if r%2==0 else -p,)
    if r<8:
        t=r-4
        old=(-vv,y) if t<2 else (vv,-y)
        p=b+5 if t<2 else b+6
        return old+(p if t%2==0 else -p,)
    if op=='and':
        if r==8:return (-uu,-vv,out)
        if r in (9,10):return (uu,-out,(b+7)*(1 if r==9 else -1))
        return (vv,-out,(b+8)*(1 if r==11 else -1))
    if r==8:return (uu,vv,-out)
    if r in (9,10):return (-uu,out,(b+7)*(1 if r==9 else -1))
    return (-vv,out,(b+8)*(1 if r==11 else -1))

def source_oracle(O):
    """Materialized occurrence index solely for external red-team testing;
    the uniform selector never calls this function or stores this index."""
    allpos=collections.defaultdict(list)
    m0=13*O.G+4*O.N+12
    width=(9*O.G+3*O.N+O.q+8).bit_length()
    for h in range(O.G):
        for r in range(13):
            clause=independently_emitted_gate_clause(O,h,r)
            assert len(clause)==3
            assert len({abs(v) for v in clause})==3,(h,r,clause)
            for k,lit in enumerate(clause):
                allpos[abs(lit)].append((13*h+r,k,1 if lit>0 else -1))
    output_wire=O.net.base+9*(abs(O.output)-O.net.base)+2
    assert O.output>0
    for r in range(4):
        allpos[output_wire].append((13*O.G+4*O.N+8+r,0,+1))
    return allpos, width,m0

def w1_fiber_test():
    w1=((-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
        (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
        (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),
        (6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14))
    fibers={};ex=0
    for a,b in itertools.product(range(2),repeat=2):
        cs=[list(t) for t in w1]
        if a==0:
            for ci,slot in ((6,0),(11,0)):cs[ci][slot]*=-1
        if b==0:
            for ci,slot in ((17,2),(9,2)):cs[ci][slot]*=-1
        assert len({tuple(t) for t in cs})==20
        pos=collections.Counter();neg=collections.Counter()
        for row in cs:
            for lit in row:
                (pos if lit>0 else neg)[abs(lit)]+=1
        assert all(pos[v]==neg[v]==2 for v in range(1,16))
        masks=set()
        for mask in range(1<<15):
            ex+=1
            if all(any(((mask>>(abs(l)-1))&1)==(l>0) for l in row) for row in cs):
                masks.add(mask)
        fibers[a,b]=masks
    assert tuple(len(fibers[k]) for k in ((0,0),(0,1),(1,0),(1,1)))==(772,272,272,0)
    assert 616 in fibers[0,0] & fibers[0,1]
    assert 4742 in fibers[1,0]
    assert not (fibers[0,1] & fibers[1,0])
    return {'counts':{'00':772,'01':272,'10':272,'11':0},
            'Alice_0_common':len(fibers[0,0]&fibers[0,1]),
            'Bob_0_common':len(fibers[0,0]&fibers[1,0]),
            'Alice1_Bob1_common':len(fibers[0,1]&fibers[1,0]),
            'Alice_only_masks':[616,4742],
            'complete_witness_independence_from_both_inputs':False,
            'assignments_exhausted':ex}

def run():
    out={'run_id':'CHECKER-INTERNAL-SELECT179','seed':None,'source_test':w1_fiber_test(),
         'configurations':[], 'counters':collections.Counter(), 'failures':0}
    for q,m in ((3,1),(3,2),(4,2),(5,3),(7,2),(8,3),(9,4),(15,3)):
        O=Original(q,m);S=Shape(q,m)
        assert (O.Gf,O.scan_end,O.check_start,O.G)==(S.Gf,S.scan_end,S.check_start,S.G)
        actual_source,source_width,source_clause_count=source_oracle(O)
        if q==3 and m==1:
            for mask in range(1<<S.N):
                xx=[mask>>j&1 for j in range(S.N)]
                active=xx[0]
                ids=[sum(xx[1+j*(S.w+1)+i]<<i for i in range(S.w)) for j in range(3)]
                signs=[xx[1+j*(S.w+1)+S.w] for j in range(3)]
                for z in itertools.product((0,1),repeat=q):
                    good=(not active or (len(set(ids))==3 and
                        all(1<=v<=q for v in ids) and
                        any(z[ids[j]-1]==signs[j] for j in range(3))))
                    values=O.net.eval(xx,list(z))
                    actual=values[abs(O.output)] ^ (O.output<0)
                    assert actual==int(good),(mask,z,actual,good)
                    out['counters']['exhaustive_source_and_witness']+=1
        expected=collections.defaultdict(list)
        for h,(op,aa,bb) in enumerate(O.net.gates):
            for k,lit in enumerate((aa,bb)):
                if abs(lit)>=O.net.base:
                    target=abs(lit)-O.net.base
                    if target>=S.check_start:
                        expected[target].append((h,k,1 if lit>0 else -1))
        checks=0;uses=0;occ=0;max_fanout=0;gate_counts=collections.Counter()
        for g in range(S.check_start,S.G):
            got=checker_gateat(S,g)
            assert got==O.net.gates[g],(q,m,g,got,O.net.gates[g])
            ch=checker_consumers(S,g)
            want=sorted(expected[g]);assert ch==want,(q,m,g,ch,want)
            actual=[]
            op,_,_=got
            actual.extend((13*g+8,2,1 if op=='and' else -1) for _ in range(1))
            actual.extend((13*g+r,1,-1 if op=='and' else 1) for r in range(9,13))
            for h,k,sign in want:
                actual.extend((13*h+4*k+r,1,sign if r<2 else -sign) for r in range(4))
            if g==S.G-1:
                actual.extend((13*S.G+4*S.N+8+r,0,+1) for r in range(4))
            occs=checker_occurrences(S,g)
            assert occs==sorted(actual)
            true_source=sorted(actual_source[S.base+9*g+2])
            assert occs==true_source,(q,m,g,occs,true_source)
            for ri,(clause_i,position_i,pol) in enumerate(occs):
                assert occs[ri]==(clause_i,position_i,pol)
                sign_addr=32+3*source_width+(3*clause_i+position_i)*(source_width+1)
                assert sign_addr < 32+3*source_width+3*source_clause_count*(source_width+1)
                if clause_i<13*O.G:
                    assert (1 if independently_emitted_gate_clause(O,clause_i//13,clause_i%13)[position_i]>0 else -1)==pol
                else:
                    assert clause_i in range(13*O.G+4*O.N+8,13*O.G+4*O.N+12)
                    assert position_i==0 and g==S.G-1 and pol==1
            assert all(h>g for h,_,_ in ch)
            assert len(ch)<=2
            max_fanout=max(max_fanout,len(ch))
            gate_counts[op]+=1;checks+=1;uses+=len(ch);occ+=len(actual)
        out['configurations'].append({'q':q,'m':m,'N':S.N,'G':S.G,
               'checker_gate_count':checks,'checker_use_count':uses,
               'source_occurrences':occ,'max_direct_fanout':max_fanout,
               'gate_opcodes':dict(gate_counts),'status':'COMPUTATIONAL finite'})
        out['counters']['gateat_equal']+=checks
        out['counters']['inverse_equal']+=checks
        out['counters']['occurrence_equal']+=checks
        out['counters']['source_occurrences']+=occ
        out['counters']['direct_uses']+=uses
    out['counters']=dict(out['counters'])
    out['status']={'checker_parameter_inverse':'PROVED/EXACT restricted, independent peer review pending',
        'signed_exact22_4mode':'COMPUTATIONAL exhaustive finite, previously known',
        'fully_uniform_bitwise_decision_circuit':'OPEN',
        'full_source_alias_constants_and_signed_R15':'OPEN',
        'all_input_arc_contraction':'OPEN', 'P_neq_NP':'OPEN'}
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',default='2026-10-27_1312_CHECKER_INTERNAL_SELECT179_raw.json')
    z=p.parse_args()
    data=run()
    Path(z.out).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'cases':len(data['configurations']),'counters':data['counters'],
      'source':data['source_test'],'failures':data['failures']},indent=2,sort_keys=True))

if __name__=='__main__':main()
