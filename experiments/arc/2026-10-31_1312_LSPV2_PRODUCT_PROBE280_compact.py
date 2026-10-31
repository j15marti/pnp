#!/usr/bin/env python3
"""PRODUCT-PROBE280 compact restricted lemma reproducer, standard library only.

The full original-source U198 proof, independent verifier, exhaustive 309764
child-bit tests, materialized producer and raw data are in the downloadable
LSPV2_PRODUCT_PROBE280_2026-10-31.zip run archive.
Usage:
 python experiments/arc/2026-10-31_1312_LSPV2_PRODUCT_PROBE280_compact.py \
   research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt
"""
import ast, collections, hashlib, itertools, json, math, pathlib, sys

def get_sources(path):
    text=pathlib.Path(path).read_text()
    U=ast.literal_eval(text[text.index('[['):])
    V=[c[:] for c in U]
    assert U[2]==[1,2,197] and U[44]==[33,34,196]
    V[2][2]=196;V[44][2]=197
    return U,V

def valid(F):
    if not F or any(len(c)!=3 or len(set(map(abs,c)))!=3 or
                    len(set(z>0 for z in c))!=1 for c in F):return False
    if len({tuple(sorted(c)) for c in F})!=len(F):return False
    n=max(abs(z) for c in F for z in c)
    degree=collections.Counter((abs(z),z>0) for c in F for z in c)
    return 3*len(F)==4*n and all(degree[v,p]==2
                               for v in range(1,n+1) for p in (False,True))

def product(k,bad,U,V):
    return [[(1 if z>0 else -1)*(abs(z)+198*i) for z in c]
            for i in range(k) for c in (U if i in bad else V)]

def gamma(n):
    b=bin(n)[2:];return '0'*(len(b)-1)+b

def tape(F):
    n=max(abs(z) for c in F for z in c);w=n.bit_length()
    return gamma(n)+gamma(len(F))+''.join(
        ('1' if c[0]>0 else '0')+
        ''.join(format(abs(z),f'0{w}b') for z in c)
        for c in F)

def length(k):
    n=198*k;m=264*k
    return len(gamma(n))+len(gamma(m))+m*(1+3*n.bit_length())

def gate(k):
    N=length(k);a,b=0,k
    while a<b:
        mid=(a+b+1)//2
        if length(mid)**2<=N:a=mid
        else:b=mid-1
    q=a
    return {'k':k,'parent_bits':N,'max_chunk':q,
            'child_bits':length(q) if q else None,
            'child_count':(k+q-1)//q if q else None,
            'multiplicity_ok':bool(q and ((k+q-1)//q)**5<=N**3)}

def main(path):
    U,V=get_sources(path)
    assert valid(U) and valid(V)
    W='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'
    assert len(W)==198 and all(any((W[abs(z)-1]=='1')==(z>0) for z in c) for c in V)
    counts=collections.Counter()
    for k in (1,2,4):
        baseline=tape(product(k,set(),U,V))
        assert len(baseline)==length(k)
        differences=[]
        for i in range(k):
            altered=product(k,{i},U,V)
            assert valid(altered)
            trial=tape(altered)
            diff={j for j,(a,b) in enumerate(zip(baseline,trial)) if a!=b}
            assert len(diff)==2 and all(not(diff & d) for d in differences)
            differences.append(diff)
            counts['changed_positions']+=len(diff)
            counts['query_lower_bound_components']+=1
        for z in (U,V):
            for a,b in itertools.combinations(z,2):
                shared=set(map(abs,a))&set(map(abs,b))
                same=any((next(v>0 for v in a if abs(v)==j))==
                         (next(v>0 for v in b if abs(v)==j)) for j in shared)
                opp=any((next(v>0 for v in a if abs(v)==j))!=
                         (next(v>0 for v in b if abs(v)==j)) for j in shared)
                assert not(same and opp)
                counts['pair_checks']+=4
    lo,hi=1,10000
    while lo<hi:
        m=(lo+hi)//2
        if length(m)>=length(1)**2:hi=m
        else:lo=m+1
    assert lo==2732
    result={'status':'PASS','first_nonempty_power_short_k':lo,
            'U_unsat_source_certificate':'existing original-source proof in TARGET-SCOPE278',
            'V_sat_witness_verified':True,
            'probe_counts':dict(counts),
            'physical_gates':[gate(k) for k in (1,4,256,1024,2732,5000,10000,100000,1000000)],
            'status_of_universal_ARC':'OPEN','P_vs_NP':'OPEN'}
    print(json.dumps(result,indent=2))

if __name__=='__main__':main(sys.argv[1])
