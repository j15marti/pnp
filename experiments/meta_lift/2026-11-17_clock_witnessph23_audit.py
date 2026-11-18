#!/usr/bin/env python3
"""CLOCKWITNESSPH23: finite tests only. Standard library, <30 seconds."""
import itertools, json
from pathlib import Path
from collections import defaultdict

checks = 0
counters = defaultdict(int)
def check(condition, label):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(f'{label} at assertion {checks}')

def ordered_label(f):
    return (f[0], int(any(f)), int(any(f[i] and f[i+1] for i in range(len(f)-1))))

def source_from_slots(slots, N):
    g = [0]*N
    for j in slots:
        if j != N:
            g[j] = 1
    return tuple(g)

def descriptions(n):
    N=1<<n
    # descriptions are two (n+1)-bit integers, allowing sentinel N
    L=2*(n+1)
    for d in range(1<<L):
        a=d>>(n+1); b=d&((1<<(n+1))-1)
        if a<=N and b<=N and a<=b and (a!=b or a==N):
            yield d, (a,b)

def prefix_extractor(n, label):
    N=1<<n; L=2*(n+1)
    desc=dict(descriptions(n))
    def feasible(prefix):
        return any(bin(d)[2:].zfill(L).startswith(prefix) and ordered_label(source_from_slots(s,N))==label for d,s in desc.items())
    check(feasible(''), 'target must have easy witness')
    prefix=''
    for _ in range(L):
        prefix += '0' if feasible(prefix+'0') else '1'
        check(feasible(prefix), 'prefix extends to witness')
        counters['prefix_decision_calls'] += 1
    d=int(prefix,2)
    check(d in desc, 'decoded candidate syntactically legal')
    g=source_from_slots(desc[d],N)
    check(ordered_label(g)==label, 'extracted candidate correct')
    check(sum(g)<=2, 'small sparse witness')
    counters['extracted_labels'] += 1

for n in (2,3):
    N=1<<n
    by_label=defaultdict(int)
    for num in range(1<<N):
        f=tuple((num>>i)&1 for i in range(N))
        y=ordered_label(f)
        by_label[y]+=1
        counters['source_words_checked']+=1
        # explicit classification and easy representative for *every* source
        cand={
            (0,0,0):(), (0,1,0):(1,), (0,1,1):(1,2),
            (1,1,0):(0,), (1,1,1):(0,1)
        }
        check(y in cand, 'exact five-label classification')
        g=source_from_slots(cand[y],N)
        check(ordered_label(g)==y, 'canonical label preserved')
        check(sum(g)<=2, 'canonical support bound')
    check(len(by_label)==5, 'all five target labels attained')
    for label in sorted(by_label):
        prefix_extractor(n,label)

# A finite 2-variable quantified formula codec, not a PSPACE-hard finite test.
# D is a four-bit matrix, V(D)=forall x exists y D[x,y].
def v_qbf(D):
    return int(all(any((D >> (2*x+y))&1 for y in (0,1)) for x in (0,1)))

def adj(h):
    return int(any(h[i] and h[i+1] for i in range(len(h)-1)))

def masked_label(D,a,h):
    return (D,a^v_qbf(D),adj(h))

for D,b,q in itertools.product(range(16),range(2),range(2)):
    a=b^v_qbf(D)
    h=(0,)*11 if q==0 else (1,1)+(0,)*9
    check(masked_label(D,a,h)==(D,b,q),'surjective witness')
    counters['masked_targets']+=1
    for toggle in range(32):
        # preserve adjacent 11 for q=1; use nonadjacent sparse positions for q=0
        if q==0:
            h2=list((0,)*11)
            if toggle&1: h2[1]=1
            if toggle&2: h2[3]=1
            if toggle&4: h2[5]=1
            if toggle&8: h2[7]=1
            if toggle&16: h2[9]=1
        else:
            h2=list((1,1)+(0,)*9)
            for shift,bit in enumerate((4,6,8)):
                if toggle>>shift &1: h2[bit]=1
        if adj(h2)!=q: continue
        check(masked_label(D,a,h2)==(D,b,q),'forced-source-bit case')
        check(a==(b^v_qbf(D)),'forced source bit')
        counters['forced_bit_cases']+=1
    other_a=a^1
    check(masked_label(D,other_a,h)!=(D,b,q),'opposite forced bit excluded')

out={
  'artifact':'CLOCKWITNESSPH23',
  'date_pacific':'2026-11-17',
  'status':'COMPUTATIONAL; finite support only, no complexity separation',
  'assertions':checks,
  'failures':0,
  'counters':dict(sorted(counters.items())),
  'theorem_scope':'PH supplied-witness verifier plus uniform polynomial-size circuit sections implies FP^PH inverse-bit selector; under P=NP becomes FP. Symbolic theorem independent of test.',
  'finite_caveat':'Two-variable quantified matrix codec is not PSPACE-hard. Prefix search is exhaustive toy oracle, not a PH algorithm performance test.',
}
with Path(__file__).with_name('2026-11-17_CLOCKWITNESSPH23_raw.json').open('w') as f: json.dump(out,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps(out,indent=2))
