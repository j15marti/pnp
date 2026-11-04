#!/usr/bin/env python3
"""LSPV-3/394: total lossless CNF wrapper defeating unrestricted proof-cost invariance.
Python 3, standard library only. Does NOT claim any R_mix341 inference step.
"""
import json, hashlib, math, sys
from pathlib import Path

def emit(n, clauses):
    return ('p cnf %d %d\n' % (n, len(clauses)) + ''.join(' '.join(map(str, clause)) + (' ' if clause else '') + '0\n' for clause in clauses)).encode('ascii')

def parse(src):
    try:
        s=src.decode('ascii')
    except UnicodeError:
        raise ValueError('nonascii')
    lines=s.splitlines()
    if not lines or len(lines[0].split())!=4 or lines[0].split()[:2]!=['p','cnf']:
        raise ValueError('header')
    try:
        n,m=map(int,lines[0].split()[2:])
    except (ValueError,TypeError):
        raise ValueError('numeric header')
    if n<0 or m<0 or len(lines)!=m+1:raise ValueError('length')
    clauses=[]
    for line in lines[1:]:
        try: arr=[int(z) for z in line.split()]
        except ValueError:raise ValueError('bad clause')
        if not arr or arr[-1]!=0 or any(z==0 for z in arr[:-1]) or any(abs(z)>n for z in arr[:-1]):raise ValueError('syntax')
        clauses.append(tuple(arr[:-1]))
    return n,tuple(clauses)

def php(h):
    n=h*(h+1)
    def v(i,j):return i*h+j+1
    clauses=[tuple(v(i,j) for j in range(h)) for i in range(h+1)]
    for j in range(h):
        for i in range(h+1):
            for k in range(i+1,h+1): clauses.append((-v(i,j),-v(k,j)))
    return emit(n,clauses)

def recognize_php(src):
    try:n,_=parse(src)
    except ValueError:return False
    h=(math.isqrt(4*n+1)-1)//2
    return h>=1 and h*(h+1)==n and src==php(h)

def encode(src):
    """Total on byte strings. On valid CNFs it preserves projected models.
    Every payload bit is stored TWICE in signed tautological 3-clauses.
    Original variables are mapped to even indices; payload uses odd indices.
    For recognized PHP, replaces active clauses by an empty clause.
    """
    try:n,cls=parse(src);valid=True
    except ValueError:n,cls,valid=0,(),False
    special=valid and recognize_php(src)
    body=[()] if special else [tuple(2*z for z in c) for c in cls] if valid else []
    count=len(src)*8
    for i in range(count):
        bit=(src[i//8]>>(7-(i%8)))&1
        for r in range(2):
            j=2*i+r
            z=4*j+1;a=4*j+3
            body.append((z,-z,a if bit else -a))
    return emit(max(2*n,8*count-1,0),body)

def decode(encoded):
    """Inverse on E's image. Rejects disagreement of duplicated bit signs."""
    n,cls=parse(encoded)
    tags={}
    for c in cls:
        if len(c)==3 and c[0]>0 and c[1]==-c[0] and c[0]%4==1 and abs(c[2])==c[0]+2:
            j=(c[0]-1)//4
            if j in tags:raise ValueError('duplicate tag')
            tags[j]=int(c[2]>0)
    if not tags:return b''
    if len(tags)%16 or set(tags)!=set(range(len(tags))):raise ValueError('missing tag')
    bits=[]
    for i in range(len(tags)//2):
        if tags[2*i]!=tags[2*i+1]:raise ValueError('corrupt tag pair')
        bits.append(tags[2*i])
    ans=bytearray()
    for i in range(0,len(bits),8):
        v=0
        for b in bits[i:i+8]:v=2*v+b
        ans.append(v)
    return bytes(ans)

def sat(n,cls):
    for mask in range(1<<n):
        if all(any(((mask>>(abs(z)-1))&1)==int(z>0) for z in c) for c in cls):return True
    return False

def make_cases():
    lits=[(1,),(-1,),(2,),(-2,),(1,2),(1,-2),(-1,2),(-1,-2)]
    for mask in range(256): yield '2var_%03d'%mask,emit(2,[lits[j] for j in range(8) if (mask>>j)&1])
    for h in (1,2,3):yield 'PHP_%d'%h,php(h)
    for s in (b'',b'p cnf 2 1\n1 0\n1 0\n',b'p cnf a b\n',b'bad',b'\x00\xff',b'p cnf 0 1\n0\n',b'p cnf 2 1\n3 0\n',b'p cnf 2 1\n1 2\n',b'p cnf 1 0\nextra\n'):
        yield 'malformed_'+str(len(s))+'_'+str(hashlib.sha256(s).hexdigest()[:8]),s

def verify_one(name,src):
    enc=encode(src)
    if decode(enc)!=src:raise AssertionError('roundtrip '+name)
    en,ec=parse(enc)
    try: n,cs=parse(src);valid=True
    except ValueError:n,cs,valid=0,(),False
    special=recognize_php(src)
    tags=ec[(1 if special else len(cs) if valid else 0):]
    if len(tags)!=16*len(src):raise AssertionError('count '+name)
    if any(not any(-v in t for v in t) for t in tags):raise AssertionError('non-tautology')
    if valid:
        if special:
            if ec[0]!=():raise AssertionError('missing source contradiction')
            if n<=12 and sat(n,cs):raise AssertionError('PHP SAT')
        else:
            if ec[:len(cs)]!=tuple(tuple(2*z for z in c) for c in cs):raise AssertionError('projection')
            if n<=4:
                if sat(n,cs)!=sat(n,tuple(tuple(int(z/2) for z in c) for c in ec[:len(cs)])):
                    raise AssertionError('projected SAT mismatch')
    if len(tags)>0:
        tam=list(ec)
        k=(1 if special else len(cs) if valid else 0)
        a=list(tam[k]);a[2]=-a[2];tam[k]=tuple(a)
        try:decode(emit(en,tam));raise AssertionError('accepted single-bit tag corruption')
        except ValueError:pass
    return {'case':name,'valid':valid,'php_recognized':special,'input_bytes':len(src),'output_bytes':len(enc),
            'output_clauses':len(ec),'payload_tag_clauses':len(tags),'empty_source':() in ec,
            'source_sha256':hashlib.sha256(src).hexdigest(),'encoded_sha256':hashlib.sha256(enc).hexdigest()}

def main(outpath):
    cases=[]
    for name,src in make_cases():cases.append(verify_one(name,src))
    stats={'version':'LSPV-3/394','scope':'reversible polynomial-time equisatisfiable CNF coding, not an R_mix341 step',
           'cases':len(cases),'valid':sum(c['valid'] for c in cases),'invalid':sum(not c['valid'] for c in cases),
           'recognized_php':sum(c['php_recognized'] for c in cases),'single_bit_corruptions_rejected':sum(c['payload_tag_clauses']>0 for c in cases),
           'largest_output_bytes':max(c['output_bytes'] for c in cases),
           'full_records_sha256':hashlib.sha256(json.dumps(cases,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
           'php_cases':[c for c in cases if c['php_recognized']],
           'selected_controls':[c for c in cases if c['case'] in ('2var_000','2var_003','2var_255')],
           'bad_cases':[c['case'] for c in cases if not c['valid']]}
    Path(outpath).write_text(json.dumps(stats,indent=2,sort_keys=True)+'\n')
    print(json.dumps(stats,indent=2))
if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else 'lspv3_394_raw.json')
