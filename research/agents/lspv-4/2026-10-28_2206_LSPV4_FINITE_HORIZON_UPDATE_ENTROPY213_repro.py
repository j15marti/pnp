#!/usr/bin/env python3
"""Independent finite-horizon dynamic-scalar-CNF audit. Python 3, stdlib only.

Tests a fixed-width signed-literal, byte-canonical proper 3CNF embedding of
AND_m and a no-reread h-overwrite dynamic data-structure theorem. The program
checks its own source parsing and DPLL decisions; the asymptotic claims come
from explicit combinatorial proofs, not from these finite checks.
"""
from __future__ import annotations
import json, hashlib, random, math, itertools, sys
from pathlib import Path
from collections import Counter

VERSION = "LSPV4_FINITE_HORIZON_UPDATE_ENTROPY213_v1"
CHECKS = Counter()

def verify(cond, label):
    CHECKS[label] += 1
    if not cond:
        raise AssertionError(f'{label}: assertion #{CHECKS[label]}')

def vint(v: int) -> bytes:
    assert v >= 0
    res=bytearray()
    while True:
        k=v&127
        v >>=7
        res.append(k | (128 if v else 0))
        if not v: return bytes(res)

def read_vint(raw: bytes, pos: int):
    x=0; s=0
    while True:
        if pos>=len(raw): raise ValueError('truncated header')
        q=raw[pos];pos+=1
        x |= (q&127)<<s
        if not (q&128): return x,pos
        s+=7
        if s>128: raise ValueError('excessive header')

def variable_map(m):
    return {
        'x': [i+1 for i in range(m)],
        'y': [m+i+1 for i in range(m+1)],
        'u': [2*m+i+2 for i in range(m)],
        'v': [3*m+i+2 for i in range(m)],
        't': [4*m+i+2 for i in range(m)],
        'w': [5*m+i+2 for i in range(m)],
        'end': [6*m+i+2 for i in range(4)],
    }

def unit3(lit, a, b):
    return [(lit,a,b),(lit,a,-b),(lit,-a,b),(lit,-a,-b)]

def ordinary_3cnf(bits):
    m=len(bits)
    v=variable_map(m)
    clauses=[]
    clauses.extend(unit3(v['y'][0],v['end'][0],v['end'][1]))
    for i,bit in enumerate(bits):
        x=v['x'][i]
        clauses.extend(unit3(x if bit else -x,v['u'][i],v['v'][i]))
        p=v['y'][i]; q=v['y'][i+1]; a=v['t'][i]; b=v['w'][i]
        clauses.extend([(-q,p,a),(-q,p,-a),(-q,x,b),(-q,x,-b),(q,-p,-x)])
    clauses.extend(unit3(v['y'][-1],v['end'][2],v['end'][3]))
    return 6*m+5, clauses

def pack_canonical(bits):
    m=len(bits)
    if m<1: raise ValueError('m>=1')
    varnum,clauses=ordinary_3cnf(bits)
    assert len(clauses)==9*m+8
    width=max(1,((2*varnum+1).bit_length()+7)//8)
    prefix=b'SCALAR3F'+vint(m)+vint(width)
    body=bytearray()
    for cls in clauses:
        for l in cls:
            val=2*abs(l)+int(l<0)
            body.extend(val.to_bytes(width,'big'))
    return prefix+body

def unpack_canonical(raw):
    prefix=b'SCALAR3F'
    if not raw.startswith(prefix): raise ValueError('magic')
    m,pos=read_vint(raw,len(prefix))
    width,pos=read_vint(raw,pos)
    if m<1 or m>len(raw) or not 1<=width<=len(raw): raise ValueError('header range')
    nv=6*m+5
    expwidth=max(1,((2*nv+1).bit_length()+7)//8)
    if width!=expwidth: raise ValueError('noncanonical width')
    need=(9*m+8)*3*width
    if len(raw)-pos != need: raise ValueError('body length')
    values=[]
    for i in range((9*m+8)*3):
        val=int.from_bytes(raw[pos:pos+width],'big');pos+=width
        idx=val>>1
        if not 1<=idx<=nv: raise ValueError('literal index')
        values.append(-idx if val&1 else idx)
    clauses=[tuple(values[i:i+3]) for i in range(0,len(values),3)]
    v=variable_map(m)
    bits=[]
    for i in range(m):
        forced=clauses[4+9*i][0]
        if abs(forced)!=v['x'][i]:raise ValueError('control index')
        bits.append(int(forced>0))
    if ordinary_3cnf(bits)!=(nv,clauses):raise ValueError('source-auth mismatch')
    if pack_canonical(bits)!=raw:raise ValueError('noncanonical encoding')
    return bits

def dpll(clauses):
    """Independent recursive SAT solver, unit propagation and arbitrary branching."""
    def recurse(todo):
        while True:
            if any(len(c)==0 for c in todo): return False
            units=[c[0] for c in todo if len(c)==1]
            if not units:break
            a=units[0]
            todo=[tuple(x for x in c if x != -a) for c in todo if a not in c]
        if not todo:return True
        lit=todo[0][0]
        for a in [lit,-lit]:
            sub=[tuple(x for x in c if x != -a) for c in todo if a not in c]
            if recurse(sub):return True
        return False
    return recurse(tuple(clauses))

class HorizonZeroCache:
    """Stores the complete zero-set only while it remains reachable as SAT within h updates."""
    def __init__(self,bits,h):
        self.m=len(bits)
        self.h=h
        zeros={i for i,b in enumerate(bits) if not b}
        self.overfull=len(zeros)>h
        self.zeros=set() if self.overfull else zeros
        self.edits=0
    def replace(self,i,val):
        if self.edits>=self.h:raise ValueError('edit budget')
        assert 0<=i<self.m and val in (0,1)
        self.edits +=1
        if not self.overfull:
            self.zeros.discard(i)
            if val==0:self.zeros.add(i)
            assert len(self.zeros)<=2*self.h
    def sat(self):
        return not self.overfull and not self.zeros
    def memory_bits_cap(self):
        # Conservative worst-case: up to 2h indices, one control, one edit counter.
        return 2*self.h * math.ceil(math.log2(self.m+1)) + 2*math.ceil(math.log2(self.h+2)) + 4

def signature_of_source(m,h,zero_set):
    # All possible future streams setting a subset (of size <=h) of coordinates to 1.
    # These streams are common to both source states, independent of source identity.
    zero_set=frozenset(zero_set)
    return tuple(int(zero_set.issubset(frozenset(J))) for k in range(h+1) for J in itertools.combinations(range(m),k))

def log2_ceil_int(k):
    return 0 if k<=1 else (k-1).bit_length()

def main():
    rng=random.Random(202610282206)
    enc_stats=[]
    dpll_cases=0
    for m in range(1,9):
        lengths=set()
        bit_patterns=[tuple(p) for p in itertools.product((0,1),repeat=m)] if m<=6 else [tuple(rng.randrange(2) for _ in range(m)) for _ in range(40)]
        for bits in bit_patterns:
            raw=pack_canonical(bits)
            parsed=unpack_canonical(raw)
            verify(parsed==list(bits),'source_roundtrip')
            lengths.add(len(raw))
            nv,cls=ordinary_3cnf(bits)
            verify(len(cls)==9*m+8 and nv==6*m+5,'fixed_scope_count')
            verify(all(len(c)==3 and len(set(abs(z) for z in c))==3 for c in cls),'proper_3cnf')
            if m<=6:
                ans=dpll(cls);dpll_cases+=1
                verify(ans==all(bits),'independent_DPLL_SAT_UNSAT')
            # Hostile sign flip in a single force-control occurrence must be rejected.
            mutation=bytearray(raw)
            mutpos=len(raw)-((9*m+8)*3*max(1,((2*nv+1).bit_length()+7)//8))
            # first control literal is in the first clause following four endpoint clauses
            pos=mutpos+4*3*max(1,((2*nv+1).bit_length()+7)//8)
            mutation[pos+max(1,((2*nv+1).bit_length()+7)//8)-1]^=1
            try:
                unpack_canonical(bytes(mutation))
                valid=True
            except ValueError:valid=False
            verify(not valid,'reject_single_control_corruption')
        verify(len(lengths)==1,'all_control_signings_same_physical_length')
        enc_stats.append({'m':m,'length_bytes':next(iter(lengths)),'patterns':len(bit_patterns)})
    inject=[]
    for m in range(2,10):
        for h in range(1,min(4,m)+1):
            sources=[frozenset(S) for k in range(h+1) for S in itertools.combinations(range(m),k)]
            sigs=set()
            for S in sources:
                sig=signature_of_source(m,h,S)
                verify(len(sig)==len(sources),'signature_length')
                sigs.add(sig)
            lower=log2_ceil_int(len(sources))
            verify(len(sigs)==len(sources),'all_horizon_sources_distinguishable')
            # Exact semantic equivalence includes a single indistinguishable overflow
            # class containing every source with more than h original zeroes.
            all_sigs={signature_of_source(m,h,frozenset(S)) for k in range(m+1) for S in itertools.combinations(range(m),k)}
            expected=len(sources)+(1 if h<m else 0)
            verify(len(all_sigs)==expected,'exact_finite_horizon_equivalence_classes')
            inject.append({'m':m,'h':h,'small_zero_sources':len(sources),'all_equivalence_classes':expected,'minimum_information_bits':log2_ceil_int(expected)})
    edit_stats=[]
    for m,h,trials in [(8,1,300),(8,3,400),(32,4,500),(32,16,500),(128,2,600),(128,16,600),(256,32,200)]:
        sat=unsat=0
        for _ in range(trials):
            bits=[rng.randrange(2) for _ in range(m)]
            # Inject cases with few zeros to ensure the live-cache branch and SAT outcomes.
            if rng.randrange(3)==0:
                bits=[1]*m
                for x in rng.sample(range(m),rng.randrange(min(h,m)+1)):
                    bits[x]=0
            cache=HorizonZeroCache(bits,h)
            verify(cache.sat()==all(bits),'initial_decision')
            for _ in range(h):
                j=rng.randrange(m);new=rng.randrange(2)
                bits[j]=new
                cache.replace(j,new)
                ans=cache.sat()
                verify(ans==all(bits),'adaptive_update_decision')
                sat+=int(ans);unsat+=int(not ans)
        edit_stats.append({'m':m,'h':h,'trials':trials,'sat_queries':sat,'unsat_queries':unsat,'cache_bit_cap':HorizonZeroCache([1]*m,h).memory_bits_cap()})
    # Source-encoding controls: no hidden sign-length shortening across SAT/UNSAT.
    for m in [10,64,128,256]:
        a=pack_canonical([1]*m)
        b=pack_canonical([0]*m)
        verify(len(a)==len(b),'large_uniform_source_length')
    # Compare exact entropy lower bound to the proposed simple sparse cache bound.
    compare=[]
    for m in (16,32,64,128):
        for h in (1,2,4,8,min(m,16)):
            if h>m:continue
            state_count=sum(math.comb(m,j) for j in range(h+1))+(1 if h<m else 0)
            lo=log2_ceil_int(state_count)
            up=HorizonZeroCache([1]*m,h).memory_bits_cap()
            verify(lo<=up,'finite_entropy_vs_sparse_cap')
            compare.append({'m':m,'h':h,'min_info_bits':lo,'sparse_upper_cap_bits':up,'state_count':state_count})
    raw={
        'version':VERSION,
        'model':'fixed-width signed-literal canonical proper ordinary-3CNF; updates to authenticated source-control bits',
        'assertions':dict(sorted(CHECKS.items())),
        'total_assertions':sum(CHECKS.values()),
        'independent_DPLL_cases':dpll_cases,
        'encoding':enc_stats,
        'horizon_injectivity':inject,
        'update_simulations':edit_stats,
        'entropy_upper_bounds':compare,
        'connected_interface_original_sha256':'05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca',
        'limitations':['Finite checks are not proofs.','This is an ordinary proper-3CNF restricted scalar promise, not exact 2P2N.', 'No general SAT algorithm or lower bound follows.', 'Tape and RAM costs are analytic ceilings, not measured machine transitions.']
    }
    s=json.dumps(raw,indent=2,sort_keys=True)+'\n'
    out=Path(__file__).with_name('2026-10-28_2206_LSPV4_FINITE_HORIZON_UPDATE_ENTROPY213_raw.json')
    out.write_text(s)
    print(json.dumps({'passed':True,'assertions':raw['total_assertions'],'independent_DPLL_cases':dpll_cases,'raw_path':str(out),'sha256':hashlib.sha256(s.encode()).hexdigest(),'sample':compare[:6]},indent=2))

if __name__=='__main__':main()
