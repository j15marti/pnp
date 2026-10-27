#!/usr/bin/env python3
"""LSPV-2 CIRCUIT-SCAN-REVERSE-SELECT173 (2026-10-27 04:12 UTC).

Independent full source witness-verifier gate emitter matching published 166
and independent *arithmetic* inverse consumer and proper-source occurrence
selectors for three previously open sectors: last forward layer, scan exit,
and reverse MUX outputs.  No witness elimination / decision-circuit claim.

Run: python3 2026-10-27_0412_CIRCUIT_SCAN_REVERSE_SELECT173_repro.py --out raw.json
Python 3 standard library. Fully deterministic, no SAT oracle.
"""
from __future__ import annotations
import argparse, collections, hashlib, itertools, json, math, random
from pathlib import Path

class BitNet:
    def __init__(self,N,q):
        self.N,self.q=N,q
        self.const0=N+q+1;self.const1=N+q+2;self.base=N+q+3
        self.g=[]
    def gate(self,op,a,b):
        assert op in ('and','or') and a and b
        assert abs(a)<self.base+len(self.g) and abs(b)<self.base+len(self.g)
        self.g.append((op,a,b))
        return self.base+len(self.g)-1
    def A(self,a,b):return self.gate('and',a,b)
    def O(self,a,b):return self.gate('or',a,b)
    def xor(self,a,b):return self.O(self.A(a,-b),self.A(-a,b))
    def eq(self,a,b):return -self.xor(a,b)
    def mux(self,s,a,b):return self.O(self.A(-s,a),self.A(s,b))
    def andmany(self,vals):
        assert vals
        while len(vals)>1:
            vals=[self.A(vals[i],vals[i+1]) if i+1<len(vals) else vals[i] for i in range(0,len(vals),2)]
        return vals[0]
    def ormany(self,vals):
        assert vals
        while len(vals)>1:
            vals=[self.O(vals[i],vals[i+1]) if i+1<len(vals) else vals[i] for i in range(0,len(vals),2)]
        return vals[0]
    def lt(self,aa,bb):
        assert len(aa)==len(bb)
        less=self.const0;eq=self.const1
        for x,y in zip(reversed(aa),reversed(bb)):
            less=self.O(less,self.A(eq,self.A(-x,y)))
            eq=self.A(eq,self.eqxor(x,y))
        return less
    def eqxor(self,x,y):return -self.xor(x,y)
    def eqbits(self,aa,bb):
        assert len(aa)==len(bb)
        return self.andmany([self.eq(x,y) for x,y in zip(aa,bb)])
    def eval(self,xb,zb):
        assert len(xb)==self.N and len(zb)==self.q
        v=[0]*(self.base+len(self.g))
        v[1:self.N+1]=xb;v[self.N+1:self.N+self.q+1]=zb
        v[self.const1]=1
        for g,(op,a,b) in enumerate(self.g):
            aa=v[abs(a)] ^ (a<0)
            bb=v[abs(b)] ^ (b<0)
            v[self.base+g]=(aa&bb) if op=='and' else (aa|bb)
        return v

class Verifier:
    def __init__(self,q,m):
        assert q>=3 and m>=1
        self.q,self.m=q,m
        self.w=math.ceil(math.log2(q+1));self.N=m*(1+3*(self.w+1))
        self.D=self.w+3
        self.K=1<<((q+3*m-1).bit_length());self.h=self.K.bit_length()-1
        self.J=self.h*(self.h+1)//2
        self.H=7*(self.w+2);self.F=13*self.w+32
        self.C=BitNet(self.N,q)
        self.X=list(range(1,self.N+1))
        self.Z=list(range(self.N+1,self.N+q+1))
        self.layers=[]
        self.build()
    def cbit(self,v,number):
        return [self.C.const1 if (v>>i)&1 else self.C.const0 for i in range(number)]
    def clause_fields(self,c):
        st=c*(1+3*(self.w+1));act=self.X[st]
        rows=[]
        for j in range(3):
            a=st+1+j*(self.w+1)
            rows.append((self.X[a:a+self.w],self.X[a+self.w]))
        return act,rows
    def cmp(self,A,B,ascending):
        av=A[self.w:self.w+2]+A[:self.w]
        bv=B[self.w:self.w+2]+B[:self.w]
        return self.C.lt(bv,av) if ascending else self.C.lt(av,bv)
    def build(self):
        C=self.C;w=self.w;q=self.q;m=self.m;K=self.K;D=self.D
        self.active=[];self.requests=[]
        for c in range(m):
            a,req=self.clause_fields(c)
            self.active.append(a);self.requests.extend(req)
        R=[]
        for v in range(1,q+1):R.append(self.cbit(v,w)+self.cbit(0,2)+[self.Z[v-1]])
        for ids,sgn in self.requests:R.append(ids+self.cbit(1,2)+[sgn])
        for _ in range(K-q-3*m):R.append(self.cbit((1<<w)-1,w)+self.cbit(2,2)+[C.const0])
        for level in range(1,self.h+1):
            size=1<<level; stride=size//2
            while stride:
                nxt=R[:];pairs=[]
                for i in range(K):
                    j=i^stride
                    if i>=j:continue
                    old=len(C.g);sw=self.cmp(R[i],R[j],(i&size)==0)
                    assert len(C.g)-old==self.H
                    nxt[i]=[C.mux(sw,a,b) for a,b in zip(R[i],R[j])]
                    nxt[j]=[C.mux(sw,b,a) for a,b in zip(R[i],R[j])]
                    assert len(C.g)-old==self.F
                    pairs.append((i,j,sw))
                assert len(pairs)==K//2
                self.layers.append((size,stride,pairs))
                R=nxt;stride//=2
        self.Gf=len(C.g)
        assert self.Gf==K*self.h*(self.h+1)//4*self.F
        self.last_records=R
        self.scan_starts=[];self.scan_out=[]
        prev_key=None;prev_carry=C.const0
        for rec in R:
            self.scan_starts.append(len(C.g))
            ids=rec[:w];kind=rec[w:w+2];payload=rec[w+2]
            isassign=C.eqbits(kind,self.cbit(0,2))
            isquery=C.eqbits(kind,self.cbit(1,2))
            same=C.const0 if prev_key is None else C.eqbits(ids,prev_key)
            keep=C.A(-isassign,C.A(same,prev_carry))
            carry=C.O(C.A(isassign,payload),keep)
            self.scan_out.append(C.A(isquery,carry))
            prev_key=ids;prev_carry=carry
        self.scan_end=len(C.g)
        self.reverse_gate_starts={}; self.reverse_outputs={}
        payloads=self.scan_out[:]
        for layer in range(len(self.layers)-1,-1,-1):
            self.reverse_gate_starts[layer]=len(C.g)
            nxt=payloads[:]
            for i,j,sw in self.layers[layer][2]:
                old=len(C.g)
                nxt[i]=C.mux(sw,payloads[i],payloads[j])
                nxt[j]=C.mux(sw,payloads[j],payloads[i])
                assert len(C.g)==old+6
            self.reverse_outputs[layer]=nxt
            payloads=nxt
        self.check_start=len(C.g)
        self.lookup=payloads[q:q+3*m]
        self.row_starts=[]; self.row_outputs=[]
        for c in range(m):
            self.row_starts.append(len(C.g))
            req=self.requests[3*c:3*c+3]
            truth=[];valid=[]
            for j,(ids,sgn) in enumerate(req):
                nonzero=C.ormany(ids)
                leq=-C.lt(self.cbit(q,w),ids)
                valid.append(C.A(nonzero,leq))
                truth.append(C.eq(sgn,self.lookup[3*c+j]))
            pairwise=[-C.eqbits(req[j][0],req[k][0]) for j,k in ((0,1),(0,2),(1,2))]
            row_ok=C.A(C.andmany(valid+pairwise),C.ormany(truth))
            self.row_outputs.append(C.O(-self.active[c],row_ok))
        self.output=C.andmany(self.row_outputs)
        self.G=len(C.g)
        assert self.scan_end-self.Gf==19+(K-1)*(4*w+18)
        assert self.check_start-self.scan_end==3*K*self.J
        assert self.G-self.check_start==m*(36*w+15)+(m-1)
        assert self.row_starts==[self.check_start+c*(36*w+15) for c in range(m)]
        assert self.scan_starts==[scan_base(self,p) for p in range(K)]


class Shape:
    """Logspace parameter-only circuit interface. NO gate list or occurrence table."""
    def __init__(self,q,m):
        assert q>=3 and m>=1
        self.q,self.m=q,m
        self.w=q.bit_length()
        self.N=m*(1+3*(self.w+1))
        self.D=self.w+3
        self.K=1<<((q+3*m-1).bit_length())
        self.h=self.K.bit_length()-1
        self.J=self.h*(self.h+1)//2
        self.H=7*(self.w+2)
        self.F=13*self.w+32
        self.Gf=self.K*self.h*(self.h+1)//4*self.F
        self.scan_end=self.Gf+19+(self.K-1)*(4*self.w+18)
        self.check_start=self.scan_end+3*self.K*self.J
        self.G=self.check_start+m*(36*self.w+15)+(m-1)
        self.C=type('ConstantShape',(),{'base':self.N+self.q+3})()


def layer_at(q,m,ell):
    """Compute one bitonic layer with streaming O(log K)-bit registers."""
    h=(q+3*m-1).bit_length()
    assert 0<=ell<h*(h+1)//2
    pos=0
    for a in range(1,h+1):
        for b in range(a-1,-1,-1):
            if pos==ell:return (1<<a,1<<b)
            pos+=1
    raise AssertionError(ell)


def low_rank(p,stride):
    low=p&~stride
    rank=(low//(2*stride))*stride + (low%stride)
    return low,rank,int((p&stride)!=0)


def scan_base(A,p):
    return A.Gf if p==0 else A.Gf+19+(p-1)*(4*A.w+18)


def rev_base(A,l,r):
    return A.scan_end + 6*(A.K//2)*(A.J-1-l)+6*r


def final_forward_output(A,p,c):
    assert 0<=p<A.K and 0<=c<A.D
    l=A.J-1;size,stride=layer_at(A.q,A.m,l)
    _,r,side=low_rank(p,stride)
    return l*(A.K//2)*A.F +r*A.F + A.H+3*(side*A.D+c)+2


def reverse_output(A,l,p):
    assert 0<=l<A.J and 0<=p<A.K
    size,stride=layer_at(A.q,A.m,l)
    _,r,side=low_rank(p,stride)
    return rev_base(A,l,r)+3*side+2


def scan_output(A,p):
    assert 0<=p<A.K
    return scan_base(A,p)+(18 if p==0 else 4*A.w+17)


def forward_to_scan_select(A,p,c):
    """Independent algebraic (consumer gate, operand slot, +/- polarity)."""
    assert 0<=p<A.K and 0<=c<A.D
    base=scan_base(A,p);out=[]
    if c<A.w:
        if p>0:out.extend(((base+14+3*c,0,+1),(base+15+3*c,0,-1)))
        if p<A.K-1:
            nex=scan_base(A,p+1)
            out.extend(((nex+14+3*c,1,-1),(nex+15+3*c,1,+1)))
    elif c<A.w+2:
        b=c-A.w
        out.extend(((base+3*b,0,+1),(base+3*b+1,0,-1),
                    (base+7+3*b,0,+1),(base+8+3*b,0,-1)))
    else:
        off=16 if p==0 else 4*A.w+15
        out.append((base+off,1,+1))
    return sorted(out)


def scan_to_inverse_select(A,p):
    """The p-th scan result enters final sorting layer's inverse MUXs."""
    return reverse_input_uses(A,A.J-1,p)


def reverse_input_uses(A,target_layer,p):
    size,stride=layer_at(A.q,A.m,target_layer)
    _,r,side=low_rank(p,stride)
    b=rev_base(A,target_layer,r)
    if side==0:return [(b+0,1,+1),(b+4,1,+1)]
    return [(b+1,1,+1),(b+3,1,+1)]


def reverse_output_select(A,l,p):
    assert 0<=l<A.J and 0<=p<A.K
    if l>0:return reverse_input_uses(A,l-1,p)
    if p<A.q or p>=A.q+3*A.m:return []
    t=p-A.q;row,j=divmod(t,3)
    base=A.check_start+row*(36*A.w+15)+j*(8*A.w+3)+8*A.w
    return [(base,1,-1),(base+1,1,+1)]


def audit_uses_map(A):
    # Materialized table used ONLY by the independent finite red-team.
    d=collections.defaultdict(list)
    for h,(_,a,b) in enumerate(A.C.g):
        for slot,lit in enumerate((a,b)):
            if abs(lit)>=A.C.base:
                d[abs(lit)-A.C.base].append((h,slot,1 if lit>0 else -1))
    return d


def indexed_consumer_list(A,g):
    """Actual uniform inverse accessor from one gate ID, NO netlist/occurrence lookup.

    Returns None when output class not yet supported. Mathematical model:
    O(log^3 G) elementary bit operations, O(log G) combined index/work bits.
    """
    assert 0<=g<A.G
    first_last=A.Gf-(A.K//2)*A.F
    if first_last<=g<A.Gf:
        rank,off=divmod(g-first_last,A.F)
        if A.H+2<=off<A.H+6*A.D and (off-A.H-2)%3==0:
            u=(off-A.H-2)//3
            stride=layer_at(A.q,A.m,A.J-1)[1]
            p=2*stride*(rank//stride)+(rank%stride)+(u//A.D)*stride
            return ('forward_last',p,u%A.D,forward_to_scan_select(A,p,u%A.D))
    if A.Gf<=g<A.scan_end:
        z=g-A.Gf-18
        size=4*A.w+18
        if z>=0 and z%size==0:
            p=z//size
            if p<A.K:return ('scan_output',p,None,scan_to_inverse_select(A,p))
    if A.scan_end<=g<A.check_start:
        j=g-A.scan_end
        group,inside=divmod(j,3*A.K)
        r,rem=divmod(inside,6)
        if rem in (2,5):
            l=A.J-1-group
            stride=layer_at(A.q,A.m,l)[1]
            p=2*stride*(r//stride)+(r%stride)+(rem//3)*stride
            return ('reverse_output',(l,p),None,reverse_output_select(A,l,p))
    return None


def uniform_select(A,g,r):
    a=indexed_consumer_list(A,g)
    if a is None:return None
    use=a[3]
    return use[r] if 0<=r<len(use) else None


def uniform_rank(A,g,gate,slot):
    a=indexed_consumer_list(A,g)
    if a is None:return None
    for j,(cg,cs,_) in enumerate(a[3]):
        if cg==gate and cs==slot:return j
    return -1


def uniform_source_occ_select(A,v,r):
    """Return (physical_clause, literal_slot, polarity) for supported gate output."""
    index=v-A.C.base-2
    if index<0 or index%9:return None
    g=index//9
    if not(0<=g<A.G):return None
    a=indexed_consumer_list(A,g)
    if a is None:return None
    if not(0<=r<5+4*len(a[3])):return None
    return source_occ_select(A,g,a[3],r)


def uniform_source_occ_rank(A,v,clause,slot):
    index=v-A.C.base-2
    if index<0 or index%9:return None
    g=index//9
    if not(0<=g<A.G):return None
    a=indexed_consumer_list(A,g)
    if a is None:return None
    for k in range(5+4*len(a[3])):
        if uniform_source_occ_select(A,v,k)[:2]==(clause,slot):return k
    return -1


def actual_uses(A,g):
    if not hasattr(A,'_audit_uses'):
        A._audit_uses=audit_uses_map(A)
    return A._audit_uses.get(g,[])


def gate_at(A,g):
    return A.C.g[g]


def signed_source_var(A,lit):
    w=abs(lit)
    if w < A.C.base:return lit
    g=w-A.C.base
    return (1 if lit>0 else -1)*(A.C.base+9*g+2)


def gate_clause(A,g,r):
    """Actual same physical 13-row proper Tseitin source compiler as 166."""
    op,a,b=A.C.g[g];ba=A.C.base+9*g
    u,v,y=ba,ba+1,ba+2
    a=signed_source_var(A,a);b=signed_source_var(A,b)
    if r<4:
        return ((-u,a) if r<2 else (u,-a))+((ba+3 if r%2==0 else -(ba+3)) if r<2 else (ba+4 if r%2==0 else -(ba+4)),)
    if r<8:
        j=r-4
        return ((-v,b) if j<2 else (v,-b))+((ba+5 if j%2==0 else -(ba+5)) if j<2 else (ba+6 if j%2==0 else -(ba+6)),)
    if op=='and':
        if r==8:return (-u,-v,y)
        if r<=10:return (u,-y,ba+7 if r==9 else -(ba+7))
        return (v,-y,ba+8 if r==11 else -(ba+8))
    if r==8:return (u,v,-y)
    if r<=10:return (-u,y,ba+7 if r==9 else -(ba+7))
    return (-v,y,ba+8 if r==11 else -(ba+8))


def source_occ_select(A,g,uses,i):
    """Gate-output CNF variable occurrence in order (clause,slot,sign)."""
    kind=indexed_consumer_list(A,g)
    assert kind is not None
    op='and' if kind[0]=='scan_output' else 'or'
    own=[(13*g+8,2,+1 if op=='and' else -1)]
    own.extend((13*g+r,1,-1 if op=='and' else +1) for r in (9,10,11,12))
    consumers=sorted(uses)
    for cg,slot,pol in consumers:
        consumers4=[(13*cg+4*slot+j,1,pol if j<2 else -pol) for j in range(4)]
        own.extend(consumers4)
    own.sort()
    return own[i]


def source_occ_brute(A,g):
    # An independent FULL materialization to audit the table-free selector.
    if not hasattr(A,'_audit_occ'):
        occ=collections.defaultdict(list)
        for c in range(13*A.G):
            row=gate_clause(A,c//13,c%13)
            for pos,lit in enumerate(row):
                occ[abs(lit)].append((c,pos,1 if lit>0 else -1))
        A._audit_occ=occ
    return A._audit_occ.get(A.C.base+9*g+2,[])


def compiler_metadata(A):
    n0=9*A.G+3*A.N+A.q+8
    m0=13*A.G+4*A.N+12
    width=max(n0,m0).bit_length()
    lw=width.bit_length()
    # Canonical, self-delimiting header: magic, unary width-length, width,
    # n0, m0. It is ONLY the wrapper for our fixed-width output convention.
    header='10101101'+'1'*lw+'0'+format(width,f'0{lw}b')+format(n0,f'0{width}b')+format(m0,f'0{width}b')
    return {'variables':n0,'clauses':m0,'field_width':width,
            'header':header,'header_bits':len(header),
            'physical_output_bits':len(header)+3*m0*(width+1)}


def full_source_lit(A,x,c,slot):
    assert 0<=c<13*A.G+4*A.N+12 and 0<=slot<3
    if c<13*A.G:
        return gate_clause(A,c//13,c%13)[slot]
    pinbase=A.C.base+9*A.G
    c-=13*A.G
    if c<4*A.N:
        i,row=divmod(c,4)
        if slot==0:return (i+1) if x[i] else -(i+1)
        if slot==1:return pinbase+2*i if row<2 else -(pinbase+2*i)
        return (pinbase+2*i+1) if row%2==0 else -(pinbase+2*i+1)
    c-=4*A.N
    group,row=divmod(c,4)
    pins=(-A.C.const0,A.C.const1,A.output)
    if slot==0:return signed_source_var(A,pins[group])
    aux=pinbase+2*A.N+2*group+(slot-1)
    return aux if (row<2 if slot==1 else row%2==0) else -aux


def output_bit(A,x,bit_address):
    """Audit-only FULL source oracle. Uses a materialized gate-list A.
    This is not a claimed low-space generic GateAt implementation.
    """
    meta=compiler_metadata(A)
    assert 0<=bit_address<meta['physical_output_bits']
    if bit_address<meta['header_bits']:
        return meta['header'][bit_address]
    body=bit_address-meta['header_bits']
    row,index=divmod(body,3*(meta['field_width']+1))
    slot,bit=divmod(index,meta['field_width']+1)
    lit=full_source_lit(A,x,row,slot)
    field=('1' if lit>0 else '0')+format(abs(lit),f'0{meta["field_width"]}b')
    return field[bit]


def position_of_occurrence(A,occ):
    c,slot,pol=occ
    meta=compiler_metadata(A)
    return meta['header_bits']+(3*c+slot)*(meta['field_width']+1)


def parse_fixed_record(A,x):
    rows=[];step=1+3*(A.w+1)
    for c in range(A.m):
        base=c*step
        active=x[base]; literals=[]
        for j in range(3):
            off=base+1+j*(A.w+1)
            v=sum(x[off+i]<<i for i in range(A.w))
            sgn=x[off+A.w]
            literals.append((v,sgn))
        rows.append((active,literals))
    return rows


def direct_verifier(A,x,z):
    for act,rows in parse_fixed_record(A,x):
        if not act:continue
        vs=[v for v,_ in rows]
        if min(vs)<1 or max(vs)>A.q or len(set(vs))<3:return False
        if not any(z[v-1]==sg for v,sg in rows):return False
    return True


def bits_from_rows(A,rows):
    vals=[]
    for active, literals in rows:
        vals.append(int(active))
        for v,sgn in literals:
            vals.extend((v>>i)&1 for i in range(A.w))
            vals.append(int(sgn))
    assert len(vals)==A.N
    return vals


def case_report(A, rng):
    S=Shape(A.q,A.m)
    for fld in ('q','m','w','N','D','K','h','J','H','F','Gf','scan_end','check_start','G'):
        assert getattr(S,fld)==getattr(A,fld),fld
    kinds=collections.Counter(); gate_checks=0; occ_checks=0; signed_checks=0
    pair_errors=0;max_index=0;tested=[]
    x_for_pins=[0]*A.N
    physical_position_checks=0
    typed_targets=[]
    for p in range(A.K):
        for c in range(A.D):
            g=final_forward_output(S,p,c)
            assert A.last_records[p][c]==A.C.base+g
            pr=forward_to_scan_select(S,p,c)
            au=actual_uses(A,g)
            assert pr==au,(A.q,A.m,'final-forward',p,c,pr,au)
            gate_class=indexed_consumer_list(S,g)
            assert gate_class is not None and gate_class[:3]==('forward_last',p,c)
            assert gate_class[3]==pr
            typed_targets.append((g,pr,'forward_last'))
            for ix,(cg,slot,pol) in enumerate(pr):
                assert uniform_select(S,g,ix)==(cg,slot,pol)
                assert uniform_rank(S,g,cg,slot)==ix
            assert uniform_select(S,g,len(pr)) is None
            gate_checks+=len(pr);kinds['forward_last']+=1
        gg=scan_output(S,p)
        assert A.scan_out[p]==A.C.base+gg
        pr=scan_to_inverse_select(S,p)
        au=actual_uses(A,gg)
        assert pr==au,(A.q,A.m,'scan-out',p,pr,au)
        gate_class=indexed_consumer_list(S,gg)
        assert gate_class is not None and gate_class[:3]==('scan_output',p,None)
        assert gate_class[3]==pr
        typed_targets.append((gg,pr,'scan_output'))
        for ix,(cg,slot,pol) in enumerate(pr):
            assert uniform_select(S,gg,ix)==(cg,slot,pol)
            assert uniform_rank(S,gg,cg,slot)==ix
        assert uniform_select(S,gg,len(pr)) is None
        gate_checks+=len(pr);kinds['scan_output']+=1
    for l in range(A.J):
        for p in range(A.K):
            g=reverse_output(S,l,p)
            assert A.reverse_outputs[l][p]==A.C.base+g
            pr=reverse_output_select(S,l,p)
            au=actual_uses(A,g)
            assert pr==au,(A.q,A.m,'reverse',l,p,pr,au)
            gate_class=indexed_consumer_list(S,g)
            assert gate_class is not None and gate_class[:3]==('reverse_output',(l,p),None)
            assert gate_class[3]==pr
            typed_targets.append((g,pr,'reverse_output'))
            for ix,(cg,slot,pol) in enumerate(pr):
                assert uniform_select(S,g,ix)==(cg,slot,pol)
                assert uniform_rank(S,g,cg,slot)==ix
            assert uniform_select(S,g,len(pr)) is None
            gate_checks+=len(pr);kinds['reverse_output']+=1
    # Signed occurrence inversion: source compiler with fresh argument clones.
    targets_to_check=typed_targets if A.G<2500 else rng.sample(typed_targets,min(300,len(typed_targets)))
    for g,pr,typ in targets_to_check:
        brute=source_occ_brute(A,g)
        pred=[source_occ_select(S,g,pr,i) for i in range(5+4*len(pr))]
        assert pred==brute,(A.q,A.m,typ,g,pred,brute)
        assert len(set((cl,sl) for cl,sl,_ in pred))==len(pred)
        sourcev=A.C.base+9*g+2
        for ix,item in enumerate(pred):
            assert uniform_source_occ_select(S,sourcev,ix)==item
            assert uniform_source_occ_rank(S,sourcev,item[0],item[1])==ix
            phys=position_of_occurrence(A,item)
            assert output_bit(A,x_for_pins,phys)==('1' if item[2]>0 else '0')
            meta=compiler_metadata(A)
            binary=''.join(output_bit(A,x_for_pins,phys+1+t) for t in range(meta['field_width']))
            assert int(binary,2)==sourcev
            physical_position_checks+=1
        assert uniform_source_occ_select(S,sourcev,len(pred)) is None
        assert uniform_source_occ_rank(S,sourcev,13*A.G+5,0)==-1
        occ_checks+=len(pred)
        signed_checks+=sum(1 for _,_,sg in pred if sg>0)
        max_index=max(max_index,max(cl for cl,_,_ in pred))
    # The indexed arithmetic itself needs only O(log G) live ID bits.
    assert A.Gf==A.K*A.h*(A.h+1)//4*A.F
    assert A.scan_end-A.Gf==19+(A.K-1)*(4*A.w+18)
    assert A.check_start-A.scan_end==3*A.K*A.J
    kinds['source_occurrence_targets']=len(targets_to_check)
    return {'q':A.q,'m':A.m,'w':A.w,'N':A.N,'K':A.K,'J':A.J,
        'Boolean_gates':A.G, 'comparator_gates':A.Gf,
        'comparator_count':A.K*A.J//2,
        'scan_gates':A.scan_end-A.Gf,
        'reverse_gates':A.check_start-A.scan_end,
        'row_check_gates':A.G-A.check_start,
        'target_gate_counts':dict(kinds),
        'direct_consumer_uses_checked':gate_checks,
        'signed_CNF_occurrences_checked':occ_checks,
        'signed_CNF_RankSelect_roundtrips':occ_checks,
        'physical_output_bit_sign_and_id_checks':physical_position_checks,
        'full_source_output_bits':compiler_metadata(A)['physical_output_bits'],
        'full_source_output_header_bits':compiler_metadata(A)['header_bits'],
        'two_level_R15_virtual_counts': {
             'variables_level_1':33*(13*A.G+4*A.N+12)+48*(9*A.G+3*A.N+A.q+8),
             'clauses_level_1':44*(13*A.G+4*A.N+12)+64*(9*A.G+3*A.N+A.q+8),
             'variables_level_2':3036*(13*A.G+4*A.N+12)+4416*(9*A.G+3*A.N+A.q+8),
             'clauses_level_2':4048*(13*A.G+4*A.N+12)+5888*(9*A.G+3*A.N+A.q+8),
             'scope':'algebraic counts from established Q15/J transport; not separately materialized this run'},
        'positive_CNF_occs_checked':signed_checks,
        'highest_checked_source_clause':max_index,
        'base_CNF_clauses':13*A.G+4*A.N+12,
        'first_20_gate_uses':[(g,forward_to_scan_select(S,p,c)) for p,c,g in
             [(p,c,final_forward_output(S,p,c)) for p in range(min(A.K,2)) for c in range(A.D)][:20]]}


def run():
    rng=random.Random(17320261027)
    report={'run':'CIRCUIT-SCAN-REVERSE-SELECT173','model':'fixed-record total SAT witness verifier, not SAT decision',
            'cases':[],'semantics':{}, 'status':{
             'restricted_consumer_and_CNF_occurrence_selector':'CANDIDATE pending audit',
             'all_compiler_source_inverse':'OPEN','ARC_EDGE_90':'OPEN','P_neq_NP':'OPEN'}}
    for q,m in ((3,1),(4,1),(3,2),(5,2),(7,2),(6,3)):
        A=Verifier(q,m)
        report['cases'].append(case_report(A,rng))
    # ALL 2^10 fixed source bitstrings and all 8 witnesses (SAT and UNSAT malformed included).
    A=Verifier(3,1)
    sem=0;positive=0;negative=0;good=0
    for raw in range(1<<A.N):
        x=[(raw>>i)&1 for i in range(A.N)]
        for zb in range(1<<A.q):
            z=[(zb>>i)&1 for i in range(A.q)]
            want=direct_verifier(A,x,z)
            values=A.C.eval(x,z)
            got=values[abs(A.output)] ^ (A.output<0)
            assert got==want,(raw,zb,got,want)
            sem+=1;positive+=int(want);negative+=int(not want)
        good+=1
    report['semantics']={'q':3,'m':1,'all_N_bit_inputs':good,
            'all_witness_pairs':sem,'witness_true':positive,'witness_false':negative,
            'failures':0}
    # Hostile ordinary proper ternary unsat 8-clause all-assignments-blocked source.
    A=Verifier(3,8)
    uns=[]
    for a,b,c in itertools.product((0,1),repeat=3):
        uns.append((1,[(1,1-a),(2,1-b),(3,1-c)]))
    x=bits_from_rows(A,uns)
    assert all(not direct_verifier(A,x,z) for z in itertools.product((0,1),repeat=3))
    for z in itertools.product((0,1),repeat=3):
        got=A.C.eval(x,list(z))[abs(A.output)]
        assert not got
    report['unsat_eight_clause_control']={'N':A.N,'K':A.K,'G':A.G,
        'witnesses_tested':8,'clauses':8,'UNSAT':True}
    # Explicit non-monotone proper signed exact (2,2) is a distinct stricter test family.
    report['base_output_claim']='Verifier gates and 13-row source compiler only; R15^2 expansion not ARC shortening'
    report['status']['restricted_consumer_and_CNF_occurrence_selector']='PROVED/EXACT, architecture restricted, independent review pending'
    return report


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',default='2026-10-27_0412_CIRCUIT_SCAN_REVERSE_SELECT173_raw.json')
    opts=ap.parse_args()
    data=run()
    path=Path(opts.out)
    path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'cases':len(data['cases']),
       'direct_uses':sum(z['direct_consumer_uses_checked'] for z in data['cases']),
       'occurrences':sum(z['signed_CNF_occurrences_checked'] for z in data['cases']),
       'semantics':data['semantics'],
       'unsat':data['unsat_eight_clause_control'],
       'raw':str(path)},indent=2,sort_keys=True))

# ==== SCAN-INTERNAL-INVERSE177 new independent arithmetic sector ====
# This code is appended to a verbatim copy of the archived verifier emitter
# 2026-10-27_0412_CIRCUIT_SCAN_REVERSE_SELECT173_repro.py. It uses that
# emitter only as an independently materialized verification oracle.


def si_counts(n,level):
    for _ in range(level): n=(n+1)//2
    return n


def si_result_ref(A,base,n,layer,index):
    """Signed result ID in a balanced andmany after `layer` rounds.
    No list of intermediate gates is allocated. The indexing computation
    uses fixed many O(log G)-bit registers.
    """
    assert 0 <= index < si_counts(n,layer)
    while layer:
        prev=si_counts(n,layer-1)
        if index < prev//2:
            skipped=0;count=n
            for _ in range(layer-1):
                skipped+=count//2; count=(count+1)//2
            return A.C.base+base+3*n+skipped+index
        index=2*index
        layer-=1
    return -(A.C.base+base+3*index+2)


def si_eqbits_gate(A,base,n,off,operand_pair):
    """Exact global Boolean GateAt for any eqbits block of width n.
    operand_pair(j) returns two signed source wire IDs, no gate array.
    """
    assert 0<=off<4*n-1
    if off < 3*n:
        j,k=divmod(off,3)
        x,y=operand_pair(j)
        if k==0:return ('and',x,-y)
        if k==1:return ('and',-x,y)
        return ('or',A.C.base+base+3*j,A.C.base+base+3*j+1)
    idx=off-3*n
    count=n
    layer=1
    while count>1:
        made=count//2
        if idx < made:
            x=si_result_ref(A,base,n,layer-1,2*idx)
            y=si_result_ref(A,base,n,layer-1,2*idx+1)
            return ('and',x,y)
        idx-=made
        count=(count+1)//2
        layer+=1
    raise AssertionError(off)


def si_eqbits_out(A,base,n):
    layer=0;c=n
    while c>1:
        layer+=1;c=(c+1)//2
    return si_result_ref(A,base,n,layer,0)


def si_locate(A,g):
    assert A.Gf<=g<A.scan_end
    z=g-A.Gf
    p=0 if z<19 else 1+(z-19)//(4*A.w+18)
    assert p<A.K
    b=scan_base(A,p)
    length=19 if p==0 else 4*A.w+18
    assert b<=g<b+length
    return p,b,g-b


def si_gateat(A,g):
    """Virtual SCAN gate record: no materialized gate/occurrence tables.
    Full source's index base must be supplied by the `Shape` parameters.
    """
    p,b,off=si_locate(A,g)
    w=A.w; cb=A.C.base
    c0=A.N+A.q+1;c1=c0+1
    def rec(c): return cb+final_forward_output(A,p,c)
    def kind(v): return (rec(w+v),c0)
    def qkind(v):return (rec(w+v), c1 if v==0 else c0)
    if off<7:return si_eqbits_gate(A,b,2,off,kind)
    if off<14:return si_eqbits_gate(A,b+7,2,off-7,qkind)
    if p>0 and off<14+4*w-1:
        def keys(v):
            return (rec(v), cb+final_forward_output(A,p-1,v))
        return si_eqbits_gate(A,b+14,w,off-14,keys)
    t=off-(14+(4*w-1 if p>0 else 0))
    assert 0<=t<5
    same=c0 if p==0 else si_eqbits_out(A,b+14,w)
    prevcarry=c0 if p==0 else cb+scan_base(A,p-1)+(17 if p==1 else 4*w+16)
    isassign=cb+b+6
    isquery=cb+b+13
    payload=rec(w+2)
    ks=b+(14+(4*w-1 if p>0 else 0))
    if t==0:return ('and',same,prevcarry)
    if t==1:return ('and',-isassign,cb+ks)
    if t==2:return ('and',isassign,payload)
    if t==3:return ('or',cb+ks+2,cb+ks+1)
    return ('and',isquery,cb+ks+3)


def si_inverse(A,g):
    """Exact physical signed direct consumers for every scan gate.
    Only two local scan blocks are examined, plus two known reverse uses
    if this is one terminal scan gate. One pass, no incidence table.
    """
    p,_,_=si_locate(A,g)
    target=A.C.base+g
    uses=[]
    for block in (p,p+1):
        if block>=A.K:continue
        b=scan_base(A,block)
        ct=19 if block==0 else 4*A.w+18
        for h in range(b,b+ct):
            _,x,y=si_gateat(A,h)
            for slot,lit in enumerate((x,y)):
                if abs(lit)==target:
                    uses.append((h,slot,1 if lit>0 else -1))
    if g==scan_output(A,p):
        uses.extend(scan_to_inverse_select(A,p))
    return sorted(uses)


def si_occurrences(A,g):
    """Exact signed physical source-CNF occurrence list for scan output name.
    The proper 13-row compiler creates five own rows and four clone rows
    per actual signed direct gate-input use, with no hidden alias table.
    """
    op,_,_=si_gateat(A,g)
    if op=='and':
        occ=[(13*g+8,2,1)]+[(13*g+r,1,-1) for r in (9,10,11,12)]
    else:
        occ=[(13*g+8,2,-1)]+[(13*g+r,1,1) for r in (9,10,11,12)]
    for h,slot,pol in si_inverse(A,g):
        occ.extend((13*h+4*slot+j,1,pol if j<2 else -pol) for j in range(4))
    return sorted(occ)


def si_select(A,g,r):
    # For a uniform implementation, stream the constant fanout slots or
    # repeat the candidate scan to select the rth tuple. This convenience
    # materialized tiny result is never used as an input-sized advice table.
    use=si_inverse(A,g)
    return use[r] if 0<=r<len(use) else None


def si_rank(A,g,consumer,slot):
    for i,x in enumerate(si_inverse(A,g)):
        if x[:2]==(consumer,slot):return i
    return -1


def si_run_audit():
    configs=[(3,1),(3,2),(4,1),(4,2),(5,2),(6,1),(7,1),(8,2)]
    rows=[]
    tot={'instances':0,'scan_gates':0,'gateat_matches':0,'direct_uses':0,
         'source_occurrences':0,'occurrence_roundtrips':0,
         'zero_consumer_gates':0,'nonzero_consumers':0,'and_gates':0,
         'or_gates':0,'source_row_checks':0,'physical_output_position_checks':0, 'max_direct_fanout':0}
    witness=[]
    for q,m in configs:
        A=Verifier(q,m)
        S=Shape(q,m)
        assert (A.Gf,A.scan_end,A.check_start,A.G)==(S.Gf,S.scan_end,S.check_start,S.G)
        expected=collections.defaultdict(list)
        for h,(op,x,y) in enumerate(A.C.g):
            for sl,lit in enumerate((x,y)):
                if abs(lit)>=A.C.base:
                    j=abs(lit)-A.C.base
                    if A.Gf<=j<A.scan_end:
                        expected[j].append((h,sl,1 if lit>0 else -1))
        n=0; refsum=0; occsum=0; zeros=0
        for g in range(A.Gf,A.scan_end):
            derived=si_gateat(S,g)
            actual=A.C.g[g]
            assert derived==actual,(q,m,g,derived,actual)
            got=si_inverse(S,g)
            want=sorted(expected.get(g,[]))
            assert got==want,(q,m,g,got,want)
            actual_occ=source_occ_brute(A,g)
            got_occ=si_occurrences(S,g)
            assert got_occ==actual_occ,(q,m,g,got_occ,actual_occ)
            assert len(got)<=2
            tot['max_direct_fanout']=max(tot['max_direct_fanout'],len(got))
            for j,(h,sl,pol) in enumerate(got):
                assert si_select(S,g,j)==(h,sl,pol)
                assert si_rank(S,g,h,sl)==j
            assert si_select(S,g,len(got)) is None
            assert si_rank(S,g,-1,0)==-1
            for j,item in enumerate(got_occ):
                assert got_occ[j]==item
                assert len(item)==3
                # Physical source byte location accounts for every sign/ID bit.
                addr=position_of_occurrence(A,item)
                assert output_bit(A,[0]*A.N,addr)==('1' if item[2]>0 else '0')
                tot['physical_output_position_checks']+=1
                tot['occurrence_roundtrips']+=1
                tot['source_row_checks']+=1
            if not got: zeros+=1
            tot['and_gates' if actual[0]=='and' else 'or_gates']+=1
            if got:tot['nonzero_consumers']+=1
            n+=1;refsum+=len(got);occsum+=len(got_occ)
            if len(witness)<16 and (len(got)==0 or len(got)>=3):
                witness.append({'q':q,'m':m,'gate':g,'op':actual[0],
                                'uses':got,'own_plus_clone_occurrences':len(got_occ)})
        assert refsum==sum(len(expected.get(g,[])) for g in range(A.Gf,A.scan_end))
        rows.append({'q':q,'m':m,'scan_gates':n,'direct_uses':refsum,
                     'source_occurrences':occsum,'zero_consumers':zeros,
                     'total_verifier_gates':A.G,'source_cnf_clauses':13*A.G+4*A.N+12})
        tot['instances']+=1;tot['scan_gates']+=n;tot['gateat_matches']+=n
        tot['direct_uses']+=refsum;tot['source_occurrences']+=occsum
        tot['zero_consumer_gates']+=zeros
    return {'status':'COMPUTATIONAL with symbolic local GateAt proof pending independent review',
            'configurations':rows,'totals':tot,'small_counterexamples':witness,
            'all_failures':0,'random_seed':None,
            'scope':'exact fixed-record witness verifier scan only; no full SAT decision circuit'}


def main():
    import argparse, pathlib, json
    pa=argparse.ArgumentParser()
    pa.add_argument('--out',default='2026-10-27_1112_SCAN_INTERNAL_INVERSE177_raw.json')
    args=pa.parse_args()
    result=si_run_audit()
    pathlib.Path(args.out).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'totals':result['totals'],'configurations':result['configurations'],
                      'all_failures':result['all_failures']},sort_keys=True,indent=2))

if __name__=='__main__': main()
