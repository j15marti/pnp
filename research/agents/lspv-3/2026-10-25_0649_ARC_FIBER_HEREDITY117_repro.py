#!/usr/bin/env python3
"""ARC-FIBER-HEREDITY117: exact quotient and two-level ordinary 3CNF audit.

Deterministic stdlib, no random seed. Finite tests do not certify FLMV
primitive operations, all-input exponent contraction, or P != NP.
Run: python3 2026-10-25_0649_ARC_FIBER_HEREDITY117_repro.py > ..._raw.json
"""
import json
from itertools import product

D = dict(run_id='ARC-FIBER-HEREDITY117', revision='1.0', seed=None,
         assertions=0, sat_calls=0, roundtrips=0, emitted_encoded_bits=0,
         consumed_encoded_bits=0, quotient_pairs=0, quotient_suffix_tests=0,
         failure_count=0, two_level=[], gate_controls=[], hostile=[])

def ck(condition, label):
    D['assertions'] += 1
    if not condition:
        D['failure_count'] += 1
        raise AssertionError(label)

class B:
    def __init__(self, n=0): self.n = n
    def fresh(self): self.n += 1; return self.n
    def pin(self, lit):
        p, q = self.fresh(), self.fresh()
        return [(lit,p,q),(lit,p,-q),(lit,-p,q),(lit,-p,-q)]
    def eq(self, x, u):
        p, q = self.fresh(), self.fresh()
        return [(-x,u,p),(-x,u,-p),(x,-u,q),(x,-u,-q)]
    def gate(self, z, c):
        ck(len(c)==3 and len({abs(i) for i in c})==3 and
           abs(z) not in {abs(i) for i in c}, 'proper source gating')
        h = self.fresh()
        return [(-z,c[0],h),(-h,c[1],c[2])]

def encode(C, n):
    m = len(C)
    ck(m>0 and n>0, 'nonempty ordinary formula')
    h = (2*max(n,m)+1).bit_length()
    for c in C:
        ck(len(c)==3 and len({abs(i) for i in c})==3 and
           all(1 <= abs(l) <= n for l in c), 'proper ternary clauses')
    fld = lambda j: format(j, '0%db'%h)
    bits = '1'*h+'0'+fld(n)+fld(m)+''.join(
        fld(2*(abs(l)-1)+int(l<0)) for c in C for l in c)
    ck(len(bits)==1+(3+3*m)*h, 'exact header/body bit length')
    D['emitted_encoded_bits'] += len(bits)
    return bits

def decode(bits):
    D['consumed_encoded_bits'] += len(bits)
    i = 0
    while i<len(bits) and bits[i]=='1': i += 1
    if i==0 or i>=len(bits) or bits[i]!='0' or len(bits)<3*i+1:
        raise ValueError('malformed header')
    h=i
    n=int(bits[h+1:2*h+1],2); m=int(bits[2*h+1:3*h+1],2)
    if n<1 or m<1 or h!=(2*max(n,m)+1).bit_length() or \
            len(bits)!=1+(3+3*m)*h: raise ValueError('wrong dense header')
    C=[]; k=3*h+1
    for _ in range(m):
        row=[]
        for _ in range(3):
            v=int(bits[k:k+h],2); k+=h
            a=v//2+1
            if a>n: raise ValueError('name out of header range')
            row.append(-a if v%2 else a)
        if len({abs(l) for l in row})!=3:
            raise ValueError('not proper 3CNF')
        C.append(tuple(row))
    return n,C

def sat(C):
    D['sat_calls'] += 1
    def go(ass):
        a=dict(ass)
        while True:
            rem=[]; units=[]
            for c in C:
                uns=[]; true=False
                for l in c:
                    v=abs(l)
                    if v in a:
                        if a[v]==(l>0): true=True; break
                    else: uns.append(l)
                if true: continue
                if not uns: return False
                rem.append(uns)
                if len(uns)==1: units.append(uns[0])
            if not rem: return True
            if units:
                changed=False
                for l in units:
                    v=abs(l); q=l>0
                    if v in a:
                        if a[v]!=q: return False
                    else: a[v]=q; changed=True
                if changed: continue
            v=abs(rem[0][0])
            return go({**a,v:0}) or go({**a,v:1})
    return go({})

def ordinary_decide(C,n):
    s=encode(C,n)
    n2,C2=decode(s)
    ck(n2==n and C2==list(map(tuple,C)), 'ordinary exact roundtrip')
    D['roundtrips'] += 1
    return sat(C2), len(s), len(C2)

def ren(C,src,dst):
    return [tuple(dst if l==src else -dst if l==-src else l for l in c)
            for c in C]

def pinned(C,n, pins):
    b=B(n); out=list(C)
    for v,bit in sorted(pins.items()):
        out.extend(b.pin(v if bit else -v))
    return ordinary_decide(out,b.n)

def supports(S, h):
    return {h[i] for i in range(len(h)) if S & (1<<i)}

def quotient_exhaustive():
    Bsize=4
    for s in range(1<<Bsize):
        for h in product((0,1),repeat=Bsize):
            saturated=all(((s>>i)&1)==((s>>j)&1)
                          for i in range(Bsize) for j in range(Bsize)
                          if h[i]==h[j])
            all_equal=True
            for q in range(1<<Bsize):
                exact=bool(s&q)
                merged=bool(supports(s,h)&supports(q,h))
                all_equal &= (exact==merged)
                if saturated: ck(exact==merged,'saturated universal suffix')
                D['quotient_suffix_tests']+=1
            ck(all_equal==saturated,'iff saturation universal suffix')
            D['quotient_pairs']+=1
        hstar=tuple((s>>i)&1 for i in range(Bsize))
        for q in range(1<<Bsize):
            ck(bool(s&q)==bool(supports(s,hstar)&supports(q,hstar)),
               'one-bit support map exact all suffixes')
        zero_bit_safe=s in (0,(1<<Bsize)-1)
        for const in ((0,)*4,(1,)*4):
            success=all(bool(s&q)==bool(supports(s,const)&supports(q,const))
                        for q in range(1<<Bsize))
            ck(success==zero_bit_safe,'zero-bit iff empty/full support')
    D['hostile'].append(dict(name='constant_fiber_wrong_suffix',
            support_left=[0],support_right=[1],hash=[0,0,0,0],
            exact_join=False,quotient_join=True))

def two_real_levels(suffix_positive):
    x,y,u=1,2,3
    b=B(3)
    P=b.eq(x,u)+b.pin(-y)
    M=b.pin(-x)
    Q=b.pin(x if suffix_positive else -x)
    n0=b.n
    root,N0,m0=ordinary_decide(P+M+Q,n0)
    ck(root==(not suffix_positive),'root opposite pins semantics')
    p0=[];p1=[]
    for ybit in (0,1):
        c0,_,_=pinned(P,n0,{x:0,y:ybit})
        c1,_,_=pinned(P,n0,{x:1,y:ybit})
        ck(c0==c1,'initial prefix x cylinder')
        p0.append(c0);p1.append(c1)
    ck(p0==[True,False] and p1==p0,'initial exact feasibility rows')
    xL=b.fresh(); P1=ren(P,x,xL)
    first,N1,m1=ordinary_decide(P1+M+Q,b.n)
    ck(first==root,'first ordinary label preserved')
    g0,_,_=pinned(P1+M,b.n,{x:0,y:0})
    g1,_,_=pinned(P1+M,b.n,{x:1,y:0})
    ck(g0 and not g1,'second genuine prefix no longer a cylinder')
    xM=b.fresh(); M2=ren(M,x,xM)
    second,N2,m2=ordinary_decide(P1+M2+Q,b.n)
    ck(second,'independent x_M and x suffix witness after bad renaming')
    ck((not suffix_positive) or (first==False and second==True),
       'UNSAT hostile flips label at level 2')
    ck(not any(abs(l)==x for c in P1+M2 for l in c),
       'new source names truly split from source x in suffix')
    ck(any(abs(l)==x for c in Q for l in c),
       'suffix retains original source x identity')
    D['two_level'].append(dict(case='UNSAT_opposite_suffix' if suffix_positive else 'SAT_matching_suffix',
         source_x=x,source_y=y,private_prefix_u=u,first_private_name=xL,
         second_private_name=xM, source_x_preserved_in_suffix=True,
         original_cylinder_x=True,new_prefix_cylinder_x=False,
         SAT_labels=[root,first,second],encoded_bit_lengths=[N0,N1,N2],
         clause_counts=[m0,m1,m2],first_prefix_y0=[p0[0],p1[0]],
         second_prefix_y0=[g0,g1]))

def gated_source():
    sat1=[(1,2,3)]
    unsat8=[tuple(v if bit==0 else -v for v,bit in zip((1,2,3),bits))
            for bits in product((0,1),repeat=3)]
    affine4=[tuple(v if bit==0 else -v for v,bit in zip((1,2,3),bits))
             for bits in product((0,1),repeat=3)
             if (sum(bits)%2)==1]
    horn2=[(-1,-2,3),(-1,-2,-3)]
    disconnected=[(1,2,3), (4,5,6)]
    for name,phi,nsource in [('SAT_one_clause',sat1,3),
                              ('UNSAT_all_eight',unsat8,3),
                              ('SAT_affine_four',affine4,3),
                              ('SAT_horn_two',horn2,3),
                              ('SAT_independent_product',disconnected,6)]:
        source,Nsource,_=ordinary_decide(phi,nsource)
        z=nsource+1; b=B(z)
        P=[]
        for c in phi: P+=b.gate(z,c)
        root,Nroot,mroot=ordinary_decide(P,b.n)
        r0,N0,_=pinned(P,b.n,{z:0})
        r1,N1,_=pinned(P,b.n,{z:1})
        ck(root and r0 and r1==source,'gated SAT source bit at z=1')
        D['gate_controls'].append(dict(case=name,source_sat=source,
           gated_root_sat=root,projection_z0=r0,projection_z1=r1,
           ordinary_source_N=Nsource,ordinary_gated_N=Nroot,
           pinned_N=[N0,N1],gated_clause_count=mroot,
           source_clauses=len(phi),added_helper_names=len(phi)))

def main():
    quotient_exhaustive()
    two_real_levels(True)
    two_real_levels(False)
    gated_source()
    bad=False
    try: decode('101')
    except ValueError: bad=True
    ck(bad,'malformed header rejection')
    D['malformed_reject']=bad
    D['status']='PROVED/EXACT finite-support theorem (report proof); COMPUTATIONAL tests; all-input ARC OPEN'
    D['FLMV_physical_traces_measured']=False
    print(json.dumps(D,indent=2,sort_keys=True))

if __name__=='__main__':main()
