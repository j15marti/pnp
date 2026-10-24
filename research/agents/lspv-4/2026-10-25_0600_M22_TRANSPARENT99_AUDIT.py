#!/usr/bin/env python3
"""M22-TRANSPARENT-ANCHOR99: exhaustive small-instance and malformed-interface test.
Self-contained Python 3, no external dependency. Source-only bit representation.
"""
from collections import Counter
from itertools import combinations
import json, random, math, hashlib, sys

P=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
Q=((1,2,4),(1,3,6),(2,3,5),(4,5,6))
Y=tuple((0,tuple(s)) for s in P)+tuple((1,tuple(s)) for s in Q)
H=tuple((0,tuple(s)) for s in P)+tuple((1,tuple(s)) for s in P)
BAD='0' # length-one string cannot be a valid self-delimiting header

def width(k):
    return k.bit_length() if k>=0 else -1

def encode(k,clauses):
    w=width(k)
    assert 0<=k<2**w if w else k==0
    m=len(clauses)
    assert m<2**(w+1)
    header='1'*w+'0'+(format(k,f'0{w}b') if w else '')+format(m,f'0{w+1}b')
    body=''.join(str(sign)+format(v,f'0{w}b') for sign,triple in clauses for v in triple)
    return header+body

def parse_candidate(src):
    N=len(src)
    # Input domain is binary strings; scan at most O(log N) header bits.
    # An unterminated long unary header can be rejected without reading it all.
    maxw=(N+1).bit_length()+1
    i=src.find('0',0,min(N,maxw+1))
    if i<0 or i>maxw:return None
    w=i
    if w+1+w+w+1>N:return None
    a=w+1
    k=int(src[a:a+w],2) if w else 0
    a+=w
    m=int(src[a:a+w+1],2)
    a+=w+1
    if w!=width(k) or k>N or a+3*m*(w+1)!=N:return None
    return (w,k,m,a)

def decode(src):
    hdr=parse_candidate(src)
    if hdr is None:return None
    w,k,m,a=hdr
    clauses=[]
    for i in range(m):
        row=[]
        for j in range(3):
            start=a+(i*3+j)*(w+1)
            row.append((int(src[start]),int(src[start+1:start+w+1],2) if w else 0))
        clauses.append((row[0][0],tuple(x for _,x in row),tuple(s for s,_ in row)))
    return k,clauses

def grammar(src,strict_star=False):
    d=decode(src)
    if d is None:return False
    k,cl=d
    if not cl and k!=0:return False
    if len(cl)*3!=4*k:return False
    if not strict_star and k==0:return True
    pos=Counter();neg=Counter(); seen=set()
    for sign,tri,sgn in cl:
        if len(set(tri))!=3 or tuple(sorted(tri))!=tri or not all(1<=a<=k for a in tri):return False
        if len(set(sgn))!=1:return False
        row=(sign,tri)
        if row in seen:return False
        seen.add(row)
        for a in tri:(pos if sign==0 else neg)[a]+=1
    if any(pos[i]!=2 or neg[i]!=2 for i in range(1,k+1)):return False
    if strict_star and all((1-s,tri) in seen for s,tri in seen):return False
    return True

def anchor_meta(src):
    hdr=parse_candidate(src)
    if hdr is None:return None
    w,k,m,a=hdr
    kp=k+6;wp=width(kp);mp=m+8
    if mp>=2**(wp+1):return None
    H=('1'*wp+'0'+format(kp,f'0{wp}b')+format(mp,f'0{wp+1}b'))
    return (w,k,m,a,wp,kp,mp,H,3*wp+2+3*mp*(wp+1))

def virtual_length(src):
    z=anchor_meta(src)
    return z[-1] if z else len(BAD)

def virtual_bit(src,j):
    z=anchor_meta(src)
    if z is None:return BAD[j]
    w,k,m,a,wp,kp,mp,head,Np=z
    assert 0<=j<Np
    if j<len(head):return head[j]
    b=j-len(head)
    row,slot=divmod(b,3*(wp+1))
    lit,bit=divmod(slot,wp+1)
    if row<m:
        off=a+(row*3+lit)*(w+1)
        if bit==0:return src[off]
        srcid=int(src[off+1:off+w+1],2) if w else 0
        # Explicitly invalidate any original ID beyond the old k.
        if srcid>k:srcid=0
        return format(srcid,f'0{wp}b')[bit-1]
    sign,tri=Y[row-m]
    v=k+tri[lit]
    return str(sign) if bit==0 else format(v,f'0{wp}b')[bit-1]

def virtual_materialize(src):
    return ''.join(virtual_bit(src,j) for j in range(virtual_length(src)))

def anchor_fast(src):
    z=anchor_meta(src)
    if z is None:return BAD
    w,k,m,a,wp,kp,mp,head,Np=z
    out=[head]
    for i in range(m):
        for j in range(3):
            at=a+(i*3+j)*(w+1)
            ident=int(src[at+1:at+w+1],2) if w else 0
            if ident>k:ident=0
            out.append(src[at]+format(ident,f'0{wp}b'))
    for sign,tri in Y:
        for v in tri:out.append(str(sign)+format(k+v,f'0{wp}b'))
    o=''.join(out)
    assert len(o)==Np
    return o

def num_models(k,clauses):
    total=0
    for a in range(1<<k):
        ok=all(any(((a>>(v-1))&1)!=sign for v in triple) for sign,triple in clauses)
        total+=ok
    return total

def supports_regular(k):
    triples=list(combinations(range(1,k+1),3))
    return [z for z in combinations(triples,4) if all(sum(v in c for c in z)==2 for v in range(1,k+1))]

def check():
    rng=random.Random(20261024)
    checks=0
    assert len(BAD)==1 and parse_candidate(BAD) is None
    results={"seed":20261024,"status":"COMPUTATIONAL", "model":"indexed read-only bit-access; Python counters not FLMV machine steps"}
    reg=supports_regular(6)
    assert len(reg)==75
    dist=Counter();mismatch=0
    for a in reg:
        for b in reg:
            f=tuple((0,c) for c in a)+tuple((1,c) for c in b)
            src=encode(6,f)
            assert grammar(src)
            target=anchor_fast(src)
            assert grammar(target,True)
            cm=num_models(6,f)
            dist["paired" if a==b else "nonpaired"]+=1
            if a==b:assert cm>0
            checks+=2
    results['complete_6v']={'formulas':len(reg)**2,'regular_support_sets':len(reg),'paired':dist['paired'],'nonpaired':dist['nonpaired'],'tests':2*len(reg)**2}
    for n,f in [('Y',Y),('H',H)]:
        s=encode(6,f)
        assert grammar(s)
        o=anchor_fast(s)
        assert grammar(o,True)
        assert virtual_materialize(s)==o
        assert num_models(12,tuple(f)+tuple((sg,tuple(v+6 for v in tri)) for sg,tri in Y))==20*num_models(6,f)
        results[n]={'source_models':num_models(6,f), 'output_models':num_models(12,tuple(f)+tuple((sg,tuple(v+6 for v in tri)) for sg,tri in Y)), 'bits':len(s),'anchored_bits':len(o)}
        checks+=5+len(o)
    # Each source-invalid cause must survive without parsing and validating its clauses.
    f=list(Y)
    invalid={
        'duplicate_clause':encode(6,[f[0], f[0]]+f[2:]),
        'quota_break':encode(6,[f[1]]+f[1:]),
        'mixed_clause':encode(6,[f[0],f[1]]+f[2:]),
        'repeated_variable':encode(6,[(0,(1,1,3))]+f[1:]),
        'zero_id':encode(6,[(0,(0,2,3))]+f[1:]),
        'out_of_range_id':encode(6,[(0,(1,2,7))]+f[1:]),
        'unsorted_clause':encode(6,[(0,(2,1,3))]+f[1:]),
        'incorrect_k_header':encode(7,Y),
        'incorrect_m_length':encode(6,Y)+'0',
        'bad_unary_prefix':'1111111111'+encode(6,Y),
        'all_ones':'1'*300,
        'empty':'',
        'literal_sentinel':BAD,
    }
    # mixed literal signs cannot be represented by encode() and is inserted directly.
    s=encode(6,Y)
    hh=parse_candidate(s)
    w,k,m,hstart=hh
    mixed=list(s)
    mixed[hstart+w+1]='1' # negative sign of 2nd literal in first positive clause
    invalid['mixed_clause']=''.join(mixed)
    for tag,src in invalid.items():
        assert not grammar(src),tag
        o=anchor_fast(src)
        assert not grammar(o,True),tag
        assert virtual_materialize(src)==o,tag
        checks+=3+len(o)
    results['invalid_kinds']=sorted(invalid)
    for q in range(200):
        k=rng.choice([0,1,2,3,6,7,12])
        w=width(k)
        mm=min((1<<(w+1))-1,rng.randint(0,30))
        clauses=[]
        for ci in range(mm):
            sign=rng.randint(0,1)
            triple=tuple(rng.randint(0,(1<<w)-1) if w else 0 for _ in range(3))
            clauses.append((sign,triple))
        src=encode(k,clauses)
        if grammar(src):continue
        out=anchor_fast(src)
        assert not grammar(out,True)
        if q<50:assert virtual_materialize(src)==out
        checks+=1+(len(out) if q<50 else 0)
    results['random_invalid_candidate_tests']=200
    results['assertion_accounted_checks']=checks
    results['all_passed']=True
    print(json.dumps(results,sort_keys=True,indent=2))
    return results
if __name__=='__main__': check()