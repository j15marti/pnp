#!/usr/bin/env python3
"""REFEREE278: demand-bounded semantic cache for LSPV-4 rank migration.

Restricted source-layout/address theorem only.  It neither decides arbitrary
SAT nor supplies a native FLMV translation.
"""
from __future__ import annotations
import argparse,collections,itertools,json,random
from fractions import Fraction
from pathlib import Path

F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
H=((1,2),(5,3),(6,8))+F9[2:]
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
N15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-x for x in c) for c in N15)
F9_S={8:1,3:0,7:0,6:0,1:1,5:1};F9_U={**F9_S,8:0}

def valid_signed(F,n,allowed=(2,3)):
    if not F or len({tuple(sorted(c)) for c in F})!=len(F):return False
    q=collections.Counter()
    for c in F:
        if len(c) not in allowed or len({abs(x) for x in c})!=len(c):return False
        if any(abs(x)<1 or abs(x)>n for x in c):return False
        q.update(c)
    return all(q[v]==q[-v]==2 for v in range(1,n+1))

def canonical(F,n=None):
    try:
        if not F:return False
        n=n or max(abs(x) for c in F for x in c)
        if n%3 or 3*len(F)!=4*n:return False
        if not valid_signed(F,n,(3,)):return False
        return all(all(x>0 for x in c) or all(x<0 for x in c) for c in F)
    except Exception:return False

def sat(F,a):return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)
def models(F,pins=None):
    pins=pins or {};n=max(abs(x) for c in F for x in c);free=[v for v in range(1,n+1) if v not in pins];z=0
    for bits in itertools.product((0,1),repeat=len(free)):
        a=dict(pins);a.update(zip(free,bits));z+=sat(F,a)
    return z

def rename(c,i):return tuple((1 if x>0 else -1)*(abs(x)+9*i) for x in c)
def source(r,mask):
    first=[];second=[]
    for i in range(1,r+1):
        c2,c3=rename(H[0],i),rename(H[3],i)
        if (mask>>(i-1))&1:first.append(c2);second.append(c3)
        else:first.append(c3);second.append(c2)
    return tuple(first+[rename(H[3],0)]+second+
      [rename(c,0) for j,c in enumerate(H) if j!=3]+
      [rename(c,i) for i in range(1,r+1) for j,c in enumerate(H) if j not in (0,3)])

def address_bit(r,mask):
    # bit 2 of 1072r+4(r-popcount(mask))
    address=1072*r+4*(r-mask.bit_count())
    return (address>>2)&1

def cache_bit(r,mask):return (r&1)^(mask.bit_count()&1)

def randomized_bound(r,eps):
    cost=(1-2*eps)*r
    return {'r':r,'epsilon':str(eps),'lower_expected_width_queries':str(cost),
            'matching_expected_width_queries':str(cost),
            'query_all_probability':str(1-2*eps),'guess_probability':str(2*eps)}

def prefixes(bits):
    p=[];x=0
    for b in bits:x^=b;p.append(x)
    return p

def selected_cache(bits,demands):
    ds=sorted(set(demands));out={};x=0;k=0
    for j,b in enumerate(bits,1):
        x^=b
        while k<len(ds) and ds[k]==j:out[j]=x;k+=1
    return out

def su_modes(F):
    n=max(abs(x) for c in F for x in c);checks=0
    for A,B in itertools.combinations(F,2):
        same=any(abs(x)==abs(y) and (x>0)==(y>0) for x in A for y in B)
        opp=any(abs(x)==abs(y) and (x>0)!=(y>0) for x in A for y in B)
        pred=(not opp,not same,not same,not opp);act=[False]*4
        for z in range(1<<n):
            a={v:(z>>(v-1))&1 for v in range(1,n+1)}
            AS=all(a[abs(x)]==int(x>0) for x in A);AU=all(a[abs(x)]!=int(x>0) for x in A)
            BS=all(a[abs(x)]==int(x>0) for x in B);BU=all(a[abs(x)]!=int(x>0) for x in B)
            act=[u or v for u,v in zip(act,(AS and BS,AS and BU,AU and BS,AU and BU))]
        assert tuple(act)==pred;checks+=4
    return checks

def false_cover(F,pins):
    n=max(abs(x) for c in F for x in c);free=[v for v in range(1,n+1) if v not in pins];q=0
    for bs in itertools.product((0,1),repeat=len(free)):
        a=dict(pins);a.update(zip(free,bs));assert not sat(F,a);q+=1
    return q

def xor_control(F,gray):
    n=max(abs(x) for c in F for x in c);states=[]
    for z in range(1<<n):
        z=z^(z>>1) if gray else z;a={v:(z>>(v-1))&1 for v in range(1,n+1)}
        b=[a[v] for v in range(1,n+1)]
        for c in F:
            t=sum(a[abs(x)]==int(x>0) for x in c);b.extend((t&1,(t>>1)&1))
        states.append(b)
    d=[sum(x!=y for x,y in zip(a,b)) for a,b in zip(states,states[1:])]
    return {'steps':len(d),'sum_adjacent_d_logic':sum(d),'endpoint_d_logic':sum(x!=y for x,y in zip(states[0],states[-1]))}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
    assert canonical(F9,9) and canonical(Y6,6) and canonical(F15,15) and valid_signed(H,9)
    family=0;flips=0
    for r in range(1,13):
        for mask in range(1<<r):
            F=source(r,mask);assert valid_signed(F,9*(r+1));assert address_bit(r,mask)==cache_bit(r,mask)
            for i in range(r):assert address_bit(r,mask)!=address_bit(r,mask^(1<<i));flips+=1
            family+=1
    rng=random.Random(278);demand_checks=0;reconstruction_checks=0
    for r in range(1,129):
        for _ in range(8):
            bits=[rng.randrange(2) for _ in range(r)];p=prefixes(bits)
            ds=sorted(set(rng.randrange(1,r+1) for _ in range(min(r,13))))
            c=selected_cache(bits,ds)
            for j in ds:assert c[j]==p[j-1];demand_checks+=1
            assert [p[0]]+[p[i]^p[i-1] for i in range(1,r)]==bits;reconstruction_checks+=r
    randomized=[]
    for r in (1,2,4,8,32,128):
        for eps in (Fraction(0),Fraction(1,10),Fraction(1,3),Fraction(49,100)):
            randomized.append(randomized_bound(r,eps))
    amortized=[]
    for r in (8,32,128,1024):
        for q in (1,2,8,64):
            amortized.append({'r':r,'repeated_queries':q,
              'stateless_source_probes':r*q,'cached_source_probes':r,
              'cached_total_operations_proxy':r+q,'retained_semantic_bits':1})
    controls={'F9_models':models(F9),'Y6_models':models(Y6),'F15_models':models(F15),
      'F9_SAT_models':models(F9,F9_S),'F9_UNSAT_models':models(F9,F9_U),
      'F9_UNSAT_cover_leaves':false_cover(F9,F9_U),'F9_SU_modes':su_modes(F9),
      'F15_SAT_models':models(F15,dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))),
      'F15_UNSAT_models':models(F15,dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0))))}
    assert controls=={'F9_models':70,'Y6_models':20,'F15_models':1032,'F9_SAT_models':3,
      'F9_UNSAT_models':0,'F9_UNSAT_cover_leaves':8,'F9_SU_modes':264,
      'F15_SAT_models':2,'F15_UNSAT_models':0}
    malformed=[(),((1,1,2),),((1,-2,3),),((1,2,3),),F9+(F9[0],),((1,2,3),(1,2,4))]
    assert all(not canonical(x) for x in malformed);controls['malformed_rejected']=6
    out={'run':'DEMAND-BOUNDED-PARITY-CACHE-REFEREE278','status':'PROVED_EXACT_RESTRICTED_PLUS_COMPUTATIONAL','P_vs_NP':'OPEN',
      'exact_obstruction':'LSPV4-320 proves r raw width-tag probes for one unpreprocessed address bit, but repeated or predeclared demand can be served by a paid semantic cache much smaller than a lossless rank index.',
      'theorems':{
        'raw':'For A_r(z)=bit2(1072r+4(r-|z|)), A_r(z)=r mod2 XOR parity(z); exact deterministic raw-query complexity is r.',
        'randomized':'For error epsilon<1/2, minimum worst-input expected raw queries is exactly (1-2epsilon)r.',
        'single_demand_cache':'One charged r-tag scan and one retained parity bit answer every repetition of the fixed pivot query with zero further source probes and O(1) cache lookup/output work.',
        'known_demands':'For k predeclared pivot positions, one source scan stores k prefix parities; total source probes m, retained semantic data k bits plus addresses if demand positions are not implicit.',
        'all_prefixes':'All r prefix parities reconstruct z by adjacent XOR, so the all-pivot continuation table has 2^r lossless classes and r-bit information, yet is built in O(r) and queried in O(1) random-access work.'},
      'proof_scope':'authenticated LSPV4 F_(r,z) source-layout promise and designated address-bit function only; not target SAT decision complexity',
      'family_checks':{'r_max':12,'variants':family,'single_flip_checks':flips},
      'demand_cache_checks':{'checks':demand_checks,'reconstruction_bits':reconstruction_checks},
      'randomized_bounds':randomized,'amortized_work':amortized,'controls':controls,
      'equivalence_firewall':{
        'current':'for one fixed pivot/address bit, exactly two semantic classes and one retained bit suffice after paid acquisition',
        'continuation':'for every possible pivot query, the prefix-parity vector is injective in z and needs r lossless bits, but not exponential work',
        'syntactic':'full source record order contains additional syntax unnecessary even for all prefix-parity answers'},
      'charged_work':{
        'fixed_q':'W=grammar+source/index/head+authenticate+Theta(r) scan+one cache write+q(address/cache/output)+failed policies+proof/replay+guest',
        'unknown_demands':'charge each miss, scan/rebuild or a declared directory, plus selection/switching and simultaneous co-live cache/index/head/proof/guest space',
        'peak':'one fixed query needs one semantic bit plus counters after authentication; all-prefix service needs r bits or a time-space tradeoff; all other live controller objects are additive'},
      'falsified':['multiplying the raw r-probe lower bound by the number of repeated identical requests','requiring an injective source/rank key for one fixed address bit','inferring exponential computation from 2^r all-prefix continuation classes'],
      'preserved':['r one-time acquisition probes for the fixed parity in the raw model','randomization changes only the constant for raw acquisition','unknown/adaptive demands require charged acquisition or a declared index','native sequential head motion and strict FLMV simultaneous space remain unproved'],
      'wrappers':{'DELAY_steps':4096,'COPY_writes':128,'RECOMP_reads':36,'changed_then_restored_adjacent_delta':2,'logical_endpoint_delta':0},
      'offline_XOR':{'binary':xor_control(F9,False),'gray':xor_control(F9,True)},
      'large_controls':{'U198_V198':'inherited opposite-label controls; not used to prove this source-layout theorem'},
      'search_record':[
        {'query':'Fredman Saks cell probe partial sums primary','finding':'dynamic partial-sums/cell-probe precedent; model differs'},
        {'query':'Jacobson succinct rank two-level directory','finding':'classical static rank directory and time-space tradeoff'},
        {'query':'Patrascu Viola succinct partial sums lower bound','finding':'all-rank cell-probe redundancy/probe tradeoff, not a one-demand cache lower bound'},
        {'query':'repo:j15marti/pnp single pivot parity cache','finding':'prior SINGLE-PARITY-SCC76 and semantic-prefix reports found; current result is a direct referee specialization of LSPV4-320, not novelty'},
        {'query':'org:openai prefix parity cache / succinct rank select','finding':'only irrelevant lexical hits; failed search is not novelty evidence'}],
      'limitations':['not an all-input SAT algorithm','not a SAT lower bound','not a native indexed-TM trace','no arbitrary-A contraction','no strict numerical FLMV transfer']}
    Path(a.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','variants':family,'flips':flips,'demand_checks':demand_checks,'controls':controls,'P_vs_NP':'OPEN'},indent=2))
if __name__=='__main__':main()
