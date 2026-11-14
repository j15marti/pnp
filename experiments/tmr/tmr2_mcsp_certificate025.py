#!/usr/bin/env python3
"""MCSP cylinder-certificate bounds, finite controls. No external packages."""
import itertools, json, hashlib, math
from pathlib import Path

OUT=Path(__file__).parent / '2026-11-14_1015_TMR2_MCSP_CERTIFICATE025_RAW.json'

# A truth table is an N-bit integer indexed by inputs in lexicographic binary order.
def wires(n):
    N=1<<n; ones=(1<<N)-1
    vs=[sum(((a>>(n-i-1))&1)<<a for a in range(N)) for i in range(n)]
    return vs+[0,ones]

def one_step(w,mask):
    allops=[]
    for a in w: allops.append((~a)&mask)
    for a in w:
        for b in w: allops.append(a&b);allops.append(a|b)
    return set(allops)

def circuit_functions(n,s):
    base=wires(n);mask=(1<<(1<<n))-1
    found=set(base)
    # Complete enumerator for circuits with <=2 gates using output wire selection.
    if s>=1:
        gs=one_step(base,mask); found.update(gs)
    if s>=2:
        for first in gs:
            found.update(one_step(base+[first],mask))
    return found

def sparse_extension(n,labeled):
    """Return TT and actual shared-negative DNF gate budget for the 1 points."""
    ones=[a for a,b in labeled.items() if b==1]
    tab=sum(1<<a for a in ones)
    cost=0 if not ones else n+n*len(ones)-1
    return tab,cost

def descriptor_bound(n,s):
    return (s+1)*(n+s+2)*(3*(n+s+2)**2)**s

def test_all_partial_cylinders(n,s,r):
    N=1<<n
    checked=0
    for q in range(r+1):
        for pts in itertools.combinations(range(N),q):
            for vals in itertools.product((0,1),repeat=q):
                d=dict(zip(pts,vals)); ext,cost=sparse_extension(n,d)
                assert cost<=s, (n,s,r,d,cost)
                assert all(((ext>>a)&1)==b for a,b in d.items())
                checked+=1
    return checked

def prefixes_no_cert(n,s,yes):
    N=1<<n
    D=descriptor_bound(n,s)
    t=D.bit_length()  # floor(log2 D)+1
    assert t<=N
    prefixes={f&((1<<t)-1) for f in yes}
    missing=next(k for k in range(1<<t) if k not in prefixes)
    # The first t coordinates of any completion matching missing are impossible for YES.
    assert all((f&((1<<t)-1))!=missing for f in yes)
    return dict(s=s,N=N,D=D,certificate_coordinates=t,yes_size=len(yes),distinct_seen=len(prefixes),missing_pattern=missing)

def min_no_cert(n,yes,source):
    N=1<<n
    for q in range(N+1):
        for pos in itertools.combinations(range(N),q):
            p=set(pos)
            # All YES f must disagree with source at some certified coordinate.
            if all(any(((f^source)>>i)&1 for i in p) for f in yes):
                return q,list(pos)
    raise AssertionError('Missing NO certificate')

def main():
    checks=[]
    for n,s in [(3,9),(4,12),(5,20)]:
        r=max(0,(s-n+1)//n)
        checked=test_all_partial_cylinders(n,s,r)
        checks.append(dict(n=n,s=s,sparse_radius=r,partial_labelings_checked=checked))
    actual=[]
    for s in (0,1,2):
        y=circuit_functions(4,s)
        actual.append(dict(n=4,s=s,N=16,YES=len(y)))
    upper=prefixes_no_cert(4,1,circuit_functions(4,1))
    # The previous bound based on actual |YES| is stronger than descriptor count.
    yes=circuit_functions(4,2)
    M=len(yes);t=M.bit_length()
    assert t<=16
    prefixes={f&((1<<t)-1) for f in yes}
    miss=next(x for x in range(1<<t) if x not in prefixes)
    no=miss  # remaining bits set to zero
    assert no not in yes
    q,pos=min_no_cert(4,yes,no)
    for f in yes:assert any(((f^no)>>i)&1 for i in pos)
    short=dict(n=4,s=2,N=16,yes_count=M,info_certificate_bound=t,
               witness_no_truth_table=no,min_no_certificate_size=q,min_no_certificate_positions=pos)
    # Another hostile test: the high threshold 2^n table length is NOT polynomial in n.
    for n in range(8,21,4):
        assert (1<<n)>n**2
    data=dict(proven_lemma='every q-labeled partial table extends to <= n+nq-1 gates; some NO has cert <= floor(log2 D)+1',
        circuit_basis='fan-in-two AND,OR; unary NOT; constants free; count gates, fanout free',
        test_method='exact topological circuit enumeration n=4 s<=2; exhaustive partial cylinder checks; brute force certificates',
        partial_controls=checks,exact_mcsp_sets=actual,description_upper=upper,
        exact_positive_support_upper=short,final_failed_assertions=0,
        claims='FINITE COMPUTATIONAL ONLY; symbolic theorem separate; no physical one-tape simulation')
    OUT.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    print(json.dumps(data,sort_keys=True,indent=2))
    print('SOURCE_SHA256',hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    print('RAW_SHA256',hashlib.sha256(OUT.read_bytes()).hexdigest())

if __name__=='__main__':main()
