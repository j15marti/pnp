#!/usr/bin/env python3
"""LSPV-3 EXACT22-PARITY-RING160, deterministic reproducer.

Builds a connected proper strict signed (2,2) 3CNF ring of 15-variable
W1-derived modules from LSPV-2 EXACT22-PORT-WIRES221. The two-sided
SAT/UNSAT outcome is exactly XOR of the encoded edge modes.

Checks the local 2^15 source cofactor tables, four-state transfer algebra,
physical source authentication, both-polarity DP certificates, adversarial
mutations, and optional independent scipy HiGHS MILP controls.

No assumptions of polynomial arbitrary-SAT acquisition or oracle access.
"""
from __future__ import annotations
import collections, hashlib, itertools, json, sys, copy

W1 = (
(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14))


def key(c):return tuple(sorted(c,key=lambda z:(abs(z),z<0)))
def canon(C):return tuple(sorted(map(key,C)))
def base():
    D=[list(c) for c in W1]
    for i in (6,11):D[i][0]=-D[i][0]
    C=canon(D)
    assert C[2]==(-4,-9,-11) and C[3]==(-4,-8,-11) and C[15]==(4,8,-10)
    return C

C=base()
STATES=list(itertools.product((0,1),repeat=2))
INDEX={x:i for i,x in enumerate(STATES)}


def lit_true(l,mask):return bool(mask>>(abs(l)-1)&1)==(l>0)
def cnf_true(D,mask):return all(any(lit_true(l,mask) for l in c) for c in D)

def profile(slots):
    slots=tuple(slots)
    counts=collections.Counter();examples={}
    for mask in range(1<<15):
        if not all(any(lit_true(l,mask) for l in C[j]) for j in range(20) if j not in slots):continue
        sig=((mask>>3)&1,)+tuple(int(any(lit_true(l,mask) for l in C[j] if abs(l)!=4)) for j in slots)
        counts[sig]+=1
        examples.setdefault(sig,mask)
    return counts,examples


def signed22(D,n):
    if len(D)*3!=4*n or len(set(map(key,D)))!=len(D):return False
    ctr=collections.Counter(l for c in D for l in c)
    if any(ctr[v]!=2 or ctr[-v]!=2 for v in range(1,n+1)):return False
    if any(len(c)!=3 or len({abs(l) for l in c})!=3 or any(abs(l)>n for l in c) for c in D):return False
    adj=[set() for _ in range(n+1)]
    for clause in D:
        for l in clause:adj[abs(l)].update(abs(z) for z in clause)
    seen={1};todo=[1]
    while todo:
        v=todo.pop()
        for u in adj[v]:
            if u not in seen:seen.add(u);todo.append(u)
    return len(seen)==n


def offset(c,amount):return tuple((1 if l>0 else -1)*(abs(l)+amount) for l in c)

def ring(modes):
    """modes[j] is the equality (0) or XOR (1) between modules 2j,2j+1.

    Remaining module-neighbor edges are equality with C3 slots. This
    alternating slot assignment saturates all signal occurrences without
    reusing a slot. k=2r, n=15k, m=20k.
    """
    modes=tuple(int(x) for x in modes)
    assert modes and all(x in (0,1) for x in modes)
    k=2*len(modes)
    B=[[list(offset(cl,15*j)) for cl in C] for j in range(k)]
    for j,mode in enumerate(modes):
        a,b=2*j,2*j+1
        if mode:
            B[a][2][0]=15*b+4
            B[b][15][0]=-(15*a+4)
            B[a][15][0]=-(15*b+4)
            B[b][2][0]=15*a+4
        else:
            B[a][2][0]=-(15*b+4)
            B[b][2][0]=-(15*a+4)
        # Negative C3 slots at odd-to-next-even boundaries.
        v=b;u=(b+1)%k
        B[v][3][0]=-(15*u+4)
        B[u][3][0]=-(15*v+4)
    D=canon(cl for block in B for cl in block)
    assert signed22(D,15*k)
    return D


def dimacs(D,n):
    return (f'p cnf {n} {len(D)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in D)).encode('ascii')

def parse_source(payload):
    """Authenticate ALL source clauses and decode every edge mode without search.

    Raises ValueError when formula is not in this explicit two-polarity family.
    Not a universal SAT decider for rejected out-of-class inputs.
    """
    try:
        lines=payload.decode('ascii').splitlines()
        header=lines[0].split()
        if len(header)!=4 or header[:2]!=['p','cnf']:raise ValueError('DIMACS header')
        n,m=int(header[2]),int(header[3])
        if n<30 or n%30 or m*3!=4*n:raise ValueError('shape')
        k=n//15
        clauses=[]
        for line in lines[1:]:
            z=[int(v) for v in line.split()]
            if len(z)!=4 or z[-1]!=0:raise ValueError('clause width')
            clauses.append(tuple(z[:3]))
        if len(clauses)!=m:raise ValueError('clause count')
        D=canon(clauses)
        if len(set(D))!=m:raise ValueError('duplicate clauses')
        modes=[]
        for j in range(k//2):
            a,b=2*j,2*j+1
            feet={-(15*a+9),-(15*a+11)}
            hits=[cl for cl in D if feet.issubset(set(cl))]
            expected_base={15*b+4,-(15*b+4)}
            candidates=[next((l for l in cl if l in expected_base),None) for cl in hits]
            candidates=[z for z in candidates if z is not None]
            if len(candidates)!=1:raise ValueError('noncanonical mode signature')
            modes.append(int(candidates[0]>0))
        expected=ring(modes)
        if D!=expected:raise ValueError('source clauses do not match signed ring grammar')
        return tuple(modes),D
    except (UnicodeError,ValueError,IndexError,TypeError) as e:
        raise ValueError('not an authenticated ring instance: '+str(e)) from e


def product(A,B):
    return tuple(tuple(int(any(A[i][j] and B[j][t] for j in range(len(B)))) for t in range(len(B[0]))) for i in range(len(A)))

def identity(n=4):return tuple(tuple(int(i==j) for j in range(n)) for i in range(n))


def matrices():
    profiles={}
    for mode in (0,1):
        slots=(2,3,15) if mode else (2,3)
        counts,examples=profile(slots)
        profiles[mode]=(slots,counts,examples)
    B=tuple(tuple(int((f3 or q==0) and (g3 or p==0)) for q,g3 in STATES) for p,f3 in STATES)
    T={};witness={}
    for mode in (0,1):
        slots,counts,examples=profiles[mode]
        mat=[[0]*4 for _ in range(4)];wit={}
        for a,b in itertools.product(counts,repeat=2):
            p,f3=a[0],a[1+slots.index(3)];q,g3=b[0],b[1+slots.index(3)]
            def foot(sig,s):return sig[1+slots.index(s)]
            if mode:
                ok=(foot(a,2) or q==1) and (foot(a,15) or q==0) and (foot(b,2) or p==1) and (foot(b,15) or p==0)
            else:
                ok=(foot(a,2) or q==0) and (foot(b,2) or p==0)
            if ok:
                i,j=INDEX[p,f3],INDEX[q,g3]
                mat[i][j]=1
                wit.setdefault((i,j),(examples[a],examples[b]))
        T[mode]=tuple(map(tuple,mat));witness[mode]=wit
    A={x:product(T[x],B) for x in (0,1)}
    # Exact transfer tables are independently reproduced by complete source assignments.
    assert T[0]==((1,0,0,0),(0,0,0,0),(0,0,1,1),(0,0,1,1))
    assert T[1]==((0,0,1,1),(0,0,0,0),(1,0,1,0),(1,0,0,0))
    assert B==((1,1,0,0),(1,1,1,1),(0,1,0,0),(0,1,0,1))
    assert A[0]==((1,1,0,0),(0,0,0,0),(0,1,0,1),(0,1,0,1))
    assert A[1]==((0,1,0,1),(0,0,0,0),(1,1,0,0),(1,1,0,0))
    assert product(A[0],A[0])==A[0]
    assert product(A[0],A[1])==A[1]
    assert product(A[1],A[0])==A[1]
    assert product(A[1],A[1])==A[0]
    assert any(A[0][i][i] for i in range(4))
    assert not any(A[1][i][i] for i in range(4))
    return profiles,B,T,A,witness


def solve(payload, data):
    """One deterministic algorithm both SAT and UNSAT; no answer label supplied."""
    modes,D=parse_source(payload)
    profiles,B,T,A,pair_witness=data
    seq=[identity()]
    for mode in modes:seq.append(product(seq[-1],A[mode]))
    expected=(sum(modes)%2==0)
    assert any(seq[-1][i][i] for i in range(4))==expected
    if not expected:
        proof={'type':'UNSAT','modes':list(modes),
               'matrix_chain':[[list(row) for row in M] for M in seq],
               'source_sha256':hashlib.sha256(payload).hexdigest()}
        return proof
    r=len(modes)
    # Recover a closed 4-state path through the r macro-cells.
    path=None
    for begin in range(4):
        reachable={begin:[]}
        for mode in modes:
            nxt={}
            for s,history in sorted(reachable.items()):
                for t in range(4):
                    if A[mode][s][t]:nxt.setdefault(t,history+[t])
            reachable=nxt
        if begin in reachable:
            path=[begin]+reachable[begin];break
    assert path is not None and len(path)==r+1 and path[0]==path[-1]
    masks=[]
    for j,mode in enumerate(modes):
        start,end=path[j],path[j+1]
        odd_options=[u for u in range(4) if T[mode][start][u] and B[u][end]]
        assert odd_options
        odd=min(odd_options)
        pair=pair_witness[mode][(start,odd)]
        masks.extend(pair)
    fullmask=sum(mask<<(15*i) for i,mask in enumerate(masks))
    assert cnf_true(D,fullmask)
    return {'type':'SAT','modes':list(modes),'witness_hex':hex(fullmask),
            'source_sha256':hashlib.sha256(payload).hexdigest()}


def verify(payload,certificate,data):
    """Source authenticated, exact local tables recomputed; no trusted result bit."""
    try:
        modes,D=parse_source(payload)
        if certificate.get('source_sha256')!=hashlib.sha256(payload).hexdigest():return False
        if certificate.get('modes')!=list(modes):return False
        if certificate.get('type')=='SAT':
            mask=int(certificate['witness_hex'],16)
            return mask>=0 and mask.bit_length()<=15*len(modes)*2 and cnf_true(D,mask)
        if certificate.get('type')!='UNSAT':return False
        chain=certificate.get('matrix_chain')
        if not isinstance(chain,list) or len(chain)!=len(modes)+1:return False
        _,B,T,A,_=data
        mat=identity()
        if chain[0]!=[list(row) for row in mat]:return False
        for j,m in enumerate(modes):
            mat=product(mat,A[m])
            if chain[j+1]!=[list(row) for row in mat]:return False
        return not any(mat[i][i] for i in range(4))
    except (KeyError,ValueError,TypeError,IndexError):return False


def independent_milp(D,n):
    """Optional separate SciPy optimization backend, no source-profile reuse."""
    import numpy as np
    from scipy.optimize import Bounds,LinearConstraint,milp
    from scipy.sparse import coo_matrix
    rows=[];cols=[];vals=[];lower=[]
    for idx,clause in enumerate(D):
        neg=sum(l<0 for l in clause)
        lower.append(1-neg)
        for l in clause:
            rows.append(idx);cols.append(abs(l)-1);vals.append(1 if l>0 else -1)
    A=coo_matrix((np.array(vals,dtype=float),(rows,cols)),shape=(len(D),n)).tocsr()
    res=milp(np.zeros(n),integrality=np.ones(n),bounds=Bounds(np.zeros(n),np.ones(n)),
             constraints=LinearConstraint(A,np.array(lower),np.full(len(D),np.inf)),
             options={'time_limit':30.0,'mip_rel_gap':0.0})
    if res.status==0:
        mask=sum((1<<i) for i,x in enumerate(res.x) if x>=0.5)
        assert cnf_true(D,mask)
        return 'SAT'
    if res.status==2:return 'UNSAT'
    return 'UNKNOWN(status=%s)'%res.status


def main():
    data=matrices()
    controls=[];checked=0;milp_results=[]
    for r in (1,2,3,4,5,8,16,32,64):
        masks=list(range(1<<r)) if r<=4 else [0,1,(1<<r)-1,(1<<(r-1)),sum(1<<i for i in range(0,r,2))]
        for mask in sorted(set(masks)):
            modes=tuple((mask>>j)&1 for j in range(r))
            D=ring(modes);payload=dimacs(D,30*r)
            detected,parsed=parse_source(payload)
            assert modes==detected and parsed==D
            certificate=solve(payload,data)
            assert verify(payload,certificate,data)
            assert (certificate['type']=='SAT')==(sum(modes)%2==0)
            bad=copy.deepcopy(certificate)
            if bad['type']=='UNSAT':bad['matrix_chain'][-1][0][0]^=1
            else:bad['witness_hex']='not-a-hex'
            assert not verify(payload,bad,data)
            bad2=bytearray(payload)
            idx=payload.find(b' -')
            if idx<0:idx=payload.find(b' 0')
            if idx>=0:
                bad2[idx+1]=ord('9')
                assert not verify(bytes(bad2),certificate,data)
            if r<=3 and mask in (0,1,(1<<r)-1):
                actual=independent_milp(D,30*r)
                expected='SAT' if sum(modes)%2==0 else 'UNSAT'
                assert actual==expected,(r,modes,actual)
                milp_results.append({'r':r,'mask':mask,'result':actual})
            checked+=1
            if r in (1,2,4,16,64) and mask in (0,1):
                controls.append({'r':r,'k':2*r,'variables':30*r,'clauses':40*r,
                                 'mode_mask':mask,'parity':sum(modes)%2,
                                 'answer':certificate['type'],'input_bits':8*len(payload),
                                 'certificate_bits':8*len(json.dumps(certificate,sort_keys=True).encode('utf8')),
                                 'digest':hashlib.sha256(payload).hexdigest()})
    profiles,B,T,A,witness=data
    summary={'run':'EXACT22_PARITY_RING160','status':'PASS',
             'provenance':'W1 source/mode from LSPV-2 218/221, new closed ring and exact transfer semigroup',
             'full_source_assignments_per_profile':32768,
             'profile_counts':{str(m):{','.join(map(str,s)):v for s,v in sorted(profiles[m][1].items())} for m in (0,1)},
             'T':{str(m):T[m] for m in (0,1)},'B':B,'A':{str(m):A[m] for m in (0,1)},
             'tested_instances':checked,'controls':controls,'independent_milp':milp_results,
             'semigroup':'A_0*A_0=A_0;A_0*A_1=A_1*A_0=A_1;A_1*A_1=A_0;trace(A_0)>0, trace(A_1)=0',
             'scope':'explicit connected two-polarity exact22 ring family, not arbitrary SAT'}
    print(json.dumps(summary,sort_keys=True,indent=2))

if __name__=='__main__':main()