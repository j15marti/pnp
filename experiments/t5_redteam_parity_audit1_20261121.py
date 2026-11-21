#!/usr/bin/env python3
"""Independent strict-C parity audit. Standard library; no peer imports."""
import itertools as it
import json, hashlib
from pathlib import Path

def C(a,b,c):
    # Independent tournament directed-cycle definition.
    beats=lambda x,y: (y-x)%5 in (1,3)
    return (beats(a,b) and beats(b,c) and beats(c,a)) or (beats(a,c) and beats(c,b) and beats(b,a))

def count(n, clauses):
    used=sorted(set(sum((list(c) for c in clauses),[])))
    total=0
    for vals in it.product(range(5),repeat=len(used)):
        d=dict(zip(used,vals))
        total+=all(C(*(d[i] for i in c)) for c in clauses)
    return total*5**(n-len(used))

def encode(n,cs):
    w=n.bit_length(); g=bin(len(cs)+1)[2:]
    return '1'*n+'0'+'0'*(len(g)-1)+g+''.join(format(i,f'0{w}b') for c in cs for i in c)

def decode(s):
    n=s.index('0'); p=n+1; q=p
    while s[q]=='0': q+=1
    width=q-p+1; m=int(s[q:q+width],2)-1; p=q+width; w=n.bit_length()
    assert len(s)-p==3*m*w
    ids=[int(s[j:j+w],2) for j in range(p,len(s),w)]
    cs=[tuple(ids[j:j+3]) for j in range(0,len(ids),3)]
    assert all(len(set(c))==3 and all(1<=i<=n for i in c) for c in cs)
    return n,cs

def clauses(bits):
    return [c for j,b in enumerate(bits) for c in [(8*j+1,8*j+2,8*j+3),(8*j+1,8*j+2,8*j+3+4*b)]]

def support(f,n):
    return sum(any(((f>>x)^(f>>(x^(1<<j))))&1 for x in range(1<<n)) for j in range(n))

def main():
    local=[]
    for a,b in it.combinations_with_replacement(list(it.combinations(range(1,6),3)),2):
        local.append({'clauses':[a,b],'overlap':len(set(a)&set(b)),'count':count(5,[a,b])})
    observed={t:sorted({r['count'] for r in local if r['overlap']==t}) for t in (1,2,3)}
    assert observed=={1:[180],2:[250],3:[750]}
    z0=count(8,clauses([0])); z1=count(8,clauses([1]))
    assert (z0,z1)==(93750,31250)
    full=[]
    for bs in it.product((0,1),repeat=2):
        z=count(16,clauses(bs)); assert z==z0**(2-sum(bs))*z1**sum(bs)
        full.append({'bits':bs,'count':z})
    encoded=[]
    for k in [1,2,3,7,8,15,16,31,32,63,64,127,128]:
        base=encode(8*k,clauses([0]*k)); coords=[]
        for j in range(k):
            bs=[0]*k;bs[j]=1;s=encode(8*k,clauses(bs))
            diff=[i for i,(a,b) in enumerate(zip(base,s)) if a!=b]
            assert len(diff)==1;coords+=diff
        assert len(set(coords))==k
        rows=[]
        for r in range(k+1):
            bs=[1]*r+[0]*(k-r); s=encode(8*k,clauses(bs));n,cs=decode(s)
            assert (n,cs)==(8*k,clauses(bs))
            assert len(s)==8*k+2+2*((2*k+1).bit_length()-1)+6*k*(8*k).bit_length()
            z=z0**(k-r)*z1**r
            assert (z>>k)&3==1+2*((k-r)%2)
            assert all(s[p]==str(b) for p,b in zip(coords,bs))
            rows.append({'r':r,'low_shifted_two_bits':(z>>k)&3,'count_sha256':hashlib.sha256(str(z).encode()).hexdigest()})
        encoded.append({'k':k,'N':len(base),'coordinates':coords,'weights':rows})
    # Rename a legal k=2 pair: 3 -> 4, 4 -> 3. Counts unchanged;
    # the varying ID changes 4 -> 7, now TWO bits, not one.
    rename=lambda v: {3:4,4:3}.get(v,v)
    renamed=[]
    for bs in [(0,0),(1,0)]:
        cs=[tuple(map(rename,c)) for c in clauses(bs)]
        s=encode(16,cs);decode(s);renamed.append(s)
    diff=[i for i,(a,b) in enumerate(zip(*renamed)) if a!=b]
    assert len(diff)==2
    # Every 3-input AND/OR/NOT straight-line circuit with <=2 gates,
    # allowing constants, fanout, repeated operands and disconnected gates.
    n=3;mask=(1<<(1<<n))-1
    inputs=tuple(sum(((x>>j)&1)<<x for x in range(1<<n)) for j in range(n))+(0,mask)
    states={inputs}; stats=[]
    for g in range(3):
        assert all(support(f,n)<=g+1 for st in states for f in st)
        stats.append({'gates':g,'distinct_semantic_sequences':len(states),'max_support':max(support(f,n) for st in states for f in st)})
        if g<2:
            states={st+(f,) for st in states for f in ({mask^x for x in st}|{x&y for x in st for y in st}|{x|y for x in st for y in st})}
    result={'status':'PASS','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'local_pair_rows':local,'overlap_counts':observed,'local_8_counts':[z0,z1],'independent_two_block_counts':full,'encoding_boundary_rows':encoded,'renamed_two_bit_positions':diff,'shared_circuit_rows':stats,'scope':'Finite tests; symbolic proof in report. No machine simulation.'}
    Path('raw.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','pair_cases':len(local),'encoded_weight_cases':sum(len(x['weights']) for x in encoded),'two_block_cases':len(full),'circuit_rows':stats,'renaming_distance':len(diff)}))

if __name__=='__main__':main()
