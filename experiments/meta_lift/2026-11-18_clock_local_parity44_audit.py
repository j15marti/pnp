#!/usr/bin/env python3
"""CLOCKLOCALPARITY44: deterministic, independently enumerated finite checks.
Source bits f[i] are genuine truth-table entries for n-variable Boolean functions.
No external packages. 2026-11-18. Python 3.11+.
"""
import json, random, hashlib, sys, time, itertools
from pathlib import Path
SEED=20261118134444
R=random.Random(SEED)
RESULTS={'name':'CLOCKLOCALPARITY44','seed':SEED,'python':sys.version,'checks':0,'failures':0,'by_n':[], 'method':'exhaustive where specified; seeded samples otherwise'}

def ck(expr, message):
    RESULTS['checks']+=1
    if not expr:
        RESULTS['failures']+=1
        raise AssertionError(message)

def parity(x):return x.bit_count()&1

def delta_direct(i):return parity(i)^parity(i+1)

def delta_ac0(n,i):
    # DNF: OR_{t even} (AND_{j<t} i_j) AND NOT i_t
    return int(any((i & ((1<<t)-1))==((1<<t)-1) and not ((i>>t)&1)
                   for t in range(0,n,2)))

def delta_current_ac0(n,i):
    # At CURRENT address i>0, parity(i-1) XOR parity(i) is 1
    # iff the number t of trailing zero bits of i is even.
    return int(any((i & ((1<<t)-1))==0 and ((i>>t)&1)
                   for t in range(0,n,2)))

def truth_table_parity(n):
    return sum(parity(i)<<i for i in range(1<<n))

def scan(n,f):
    N=1<<n
    prev=f&1
    dead=(prev!=0)
    for i in range(1,N):
        bit=(f>>i)&1
        dead |= ((bit^prev)!=delta_current_ac0(n,i))
        prev=bit
    return int(dead)

def implicant_matches(bits, pattern):
    return all((bits>>k)&1 == p for k,p in enumerate(pattern) if p != -1)

def exact_dnf_implicants(n):
    # All 3^n terms (literal positive, negative, missing) and the parity-1 set.
    valid=[]
    for term in itertools.product((-1,0,1),repeat=n):
        covered=[x for x in range(1<<n) if implicant_matches(x,term)]
        if covered and all(parity(x)==1 for x in covered):
            valid.append((term,covered))
    return valid

def restricted_complexity_control(n):
    valid=exact_dnf_implicants(n)
    ck(len(valid)==1<<(n-1),f'DNF number {n}')
    ck(all(len(cov)==1 and all(v!=-1 for v in term) for term,cov in valid),f'DNF singleton {n}')
    ck(set(cov[0] for _,cov in valid)==set(x for x in range(1<<n) if parity(x)), f'DNF cover {n}')
    return len(valid)

start=time.time()
for n in range(1,11):
    N=1<<n; h=truth_table_parity(n)
    stats={'n':n,'N':N,'delta_addresses':0,'sources_tested':0,'full_source_exhaustive':n<=4,'flips_checked':0,'dnf_min_terms':None}
    for i in range(N-1):
        ck(delta_ac0(n,i)==delta_direct(i),f'derivative {n} {i}')
        ck(delta_current_ac0(n,i+1)==delta_direct(i),f'current address derivative {n} {i+1}')
        stats['delta_addresses']+=1
    # Exhaustive genuine 2^N-bit source space through n=4.
    if n<=4:
        source_iterator=range(1<<N)
    else:
        examples={0,(1<<N)-1,h,h^1,h^(1<<(N-1)),h^((1<<(N//2))-1)}
        examples.update(R.getrandbits(N) for _ in range(1000))
        source_iterator=sorted(examples)
    for f in source_iterator:
        val=scan(n,f)
        ck(val==int(f!=h),f'source scan n{n} f{f}')
        stats['sources_tested']+=1
    for i in range(N):
        ck(scan(n,h^(1<<i))==1,f'essential source bit {n} {i}')
        stats['flips_checked']+=1
    ck(scan(n,h)==0,f'parity accepted {n}')
    ck(scan(n,0)==int(h!=0),f'zero rejected when nonzero {n}')
    if n<=6:
        stats['dnf_min_terms']=restricted_complexity_control(n)
    # For the exact collapsed-output indicator, its full ANF monomial has coefficient 1.
    # A full source-variable ANF computation is done for N<=16 separately.
    RESULTS['by_n'].append(stats)

for n in (1,2,3,4):
    N=1<<n
    h=truth_table_parity(n)
    # Mobius transform on a sparse truth table for F(f)=1 iff f != h.
    vals=bytearray(1 if f!=h else 0 for f in range(1<<N))
    for i in range(N):
        step=1<<i
        for k in range(0,len(vals),step*2):
            for j in range(step):
                vals[k+step+j]^=vals[k+j]
    top=vals[(1<<N)-1]
    degree=max((mask.bit_count() for mask,v in enumerate(vals) if v),default=-1)
    ck(top==1 and degree==N,f'ANF exact degree {n}')
    RESULTS.setdefault('exact_anf',[]).append({'n':n,'source_variables':N,'degree':degree,'top_coefficient':int(top)})

RESULTS['elapsed_seconds']=round(time.time()-start,4)
RESULTS['status']='PASS' if RESULTS['failures']==0 else 'FAIL'
out=Path(__file__).with_name('2026-11-18_CLOCKLOCALPARITY44_raw.json')
out.write_text(json.dumps(RESULTS,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':RESULTS['status'],'checks':RESULTS['checks'],'elapsed_seconds':RESULTS['elapsed_seconds'],'tested_sources':sum(v['sources_tested'] for v in RESULTS['by_n']),'flip_checks':sum(v['flips_checked'] for v in RESULTS['by_n']),'delta_addresses':sum(v['delta_addresses'] for v in RESULTS['by_n']),'raw':str(out)},indent=2))
