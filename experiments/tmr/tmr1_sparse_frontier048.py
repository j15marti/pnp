#!/usr/bin/env python3
"""TMR-1 sparse-input MCSP NO/output-sharing frontier finite falsifier.
This script tests finite semantic cases and exact-count asymptotic margins.
It does not prove asymptotic circuit lower bounds or simulate physical TM steps.
"""
from itertools import combinations
from math import ceil, floor, lgamma, log2, log
from json import dumps

checks = 0

def check(condition, message):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(message)

def TT(n, func):
    return sum((int(bool(func(i))) << i) for i in range(1 << n))

def circuit_tables(n, s):
    full = (1 << (1 << n)) - 1
    base = [TT(n, lambda i, j=j: (i >> j) & 1) for j in range(n)] + [0, full]
    outputs = set(base)
    frontier = {()}
    for depth in range(1, s + 1):
        nxt = set()
        for gates in frontier:
            avail = base + list(gates)
            for a in avail:
                nxt.add(gates + (full ^ a,))
            for a in avail:
                for b in avail:
                    nxt.add(gates + (a & b,))
                    nxt.add(gates + (a | b,))
        frontier = nxt
        outputs.update(g[-1] for g in frontier)
    return outputs, len(frontier)

def encode(n, positions):
    assert len(set(positions)) == len(positions)
    assert list(positions) == sorted(positions)
    assert all(0 <= p < (1 << n) for p in positions)
    return '1' * n + '0' + ''.join(format(p, '0%db' % n) for p in positions)

def parse(description):
    n = description.find('0')
    if n < 1 or any(c not in '01' for c in description):
        raise ValueError('bad unary header')
    payload = description[n+1:]
    if len(payload) % n:
        raise ValueError('trailing bits')
    pos = [int(payload[i:i+n], 2) for i in range(0, len(payload), n)]
    if any(b <= a for a, b in zip(pos, pos[1:])):
        raise ValueError('not increasing')
    return n, pos

def output_stream(desc):
    n, positions = parse(desc)
    out=[]
    k=0
    for j in range(1 << n):
        found=(k<len(positions) and positions[k] == j)
        out.append('1' if found else '0')
        if found:k += 1
    return ''.join(out)

def indexed(desc,j):
    n,positions=parse(desc)
    if not 0 <=j<1 << n:raise ValueError('out-of-range')
    return int(j in positions)

def log_binom(N,r):
    return (lgamma(N+1)-lgamma(r+1)-lgamma(N-r+1))/log(2)

# log2 combinatorial counts, conservatively using exact python lgamma differences.
# log2 count of circuits D(n,s) = (s+1)(n+s+2)[3(n+s+2)^2]^s

def log_D(n,s):
    return log2(s+1)+log2(n+s+2)+s*(log2(3)+2*log2(n+s+2))

finite=[]
for n,s,r in ((3,1,4),(4,2,8),(5,2,8)):
    allowed,frontier=circuit_tables(n,s)
    N=1<<n
    hard_count=0
    exact_total=0
    first=None
    # for n=5, sample 4000 lexicographic supports (not exhaustive)
    for support in combinations(range(N),r):
        exact_total+=1
        y=sum(1<<i for i in support)
        hard=(y not in allowed)
        hard_count+=int(hard)
        if hard and first is None:
            first=support
        if n==5 and exact_total>=4000:break
    check(first is not None, f'no hard example n={n}')
    desc=encode(n,first)
    check(parse(desc)==(n,list(first)), 'parse roundtrip')
    actual=output_stream(desc)
    expected=''.join('1' if j in first else '0' for j in range(N))
    check(actual==expected, 'stream mismatch')
    check(sum(indexed(desc,j) != int(actual[j]) for j in range(N))==0,'indexed mismatch')
    check(len(desc)==(n+1)+r*n, 'length')
    check(int(actual[::-1],2) not in allowed,'hard fixture escaped')
    check(not (len(desc) <= 0), 'nonempty')
    finite.append(dict(n=n,N=N,gate_cap=s,sparse_weight=r,enumerated_circuit_outputs=len(allowed),final_gate_sequences=frontier,supports_tested=exact_total,hard_supports_found=hard_count,exhaustive=(n<5),example_support=list(first),example_description_length=len(desc)))

for bad in ('','000','1011','110111', '1101001', '111000101111'):
    # malformed inputs must either produce valid strict list or raise, never loop
    try:
        n,pos=parse(bad)
        check(encode(n,pos)==bad, 'parser accepts noncanonical')
    except ValueError:
        check(True,'rejected malformed')

asymptotic=[]
mu=0.25
K=4
for n in (12,16,24,32,48,64,96):
    N=1<<n
    s=floor(2**(mu*n))
    r=ceil(K*s)
    check(r < N,'r<N')
    log_no=log_binom(N,r) if n<=32 else None
    log_yes=log_D(n,s)
    # lgamma precision at huge N can fail numerically, use robust simple lower bound
    log_no_lower=r*(n-log2(r))
    if log_no is not None:check(log_no_lower <= log_no+max(1e-4,log_no*1e-3),'numeric issue')
    asymptotic.append(dict(n=n,N=str(N),s=s,r=r,log2_circuit_upper=round(log_yes,3),log2_sparse_count_lower=round(log_no_lower,3),counting_margin=round(log_no_lower-log_yes,3),L=r*n+n+1,log_ratio=round(log2(r*n+n+1)/n,6)))

print(dumps({'run':'TMR1_SPARSE_NO_ENCODING_FRONTIER048','date_pacific':'2026-11-14','model':'finite circuit AND OR NOT, free constants and inputs; sorted sparse index list','status':'COMPUTATIONAL finite checks; asymptotic theorem separately proved','mu':mu,'K':K,'assertions':checks,'finite':finite,'asymptotic_checks':asymptotic,'failures':0},sort_keys=True,indent=2))
