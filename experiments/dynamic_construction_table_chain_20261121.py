#!/usr/bin/env python3
"""Explicit Boolean table-chain compiler and authenticated polynomial control.
Finite exhaustive semantics, not a full single-tape timing experiment.
"""
from itertools import product, combinations
from pathlib import Path
from hashlib import sha256
import json
import dynamic_synthesis_reachable_splice_20261121 as transport


def source(tables, s, t):
    L, r = len(tables), len(tables[0])
    assert L >= 1 and r >= 3 and 1 <= s <= r and 1 <= t <= r
    assert all(len(f) == r and all(1 <= v <= r for v in f) for f in tables)
    z = lambda j, v: j*r+v
    p, q = (L+1)*(2*r-3)+1, (L+1)*(2*r-3)+2
    cs = []
    for v in (z(0,s), z(L,t)):
        cs.extend((v, a*p, b*q) for a,b in product((1,-1), repeat=2))
    for j in range(L+1):
        xs = [z(j,v) for v in range(1,r+1)]
        ts = [(L+1)*r+j*(r-3)+h+1 for h in range(r-3)]
        if r == 3:
            cs.append(tuple(xs))
        else:
            cs.append((xs[0],xs[1],ts[0]))
            cs.extend((-ts[h],xs[h+2],ts[h+1]) for h in range(r-4))
            cs.append((-ts[-1],xs[-2],xs[-1]))
        for a,b in combinations(xs,2):
            cs.extend(((-a,-b,p),(-a,-b,-p)))
    for j,f in enumerate(tables,1):
        for v,image in enumerate(f,1):
            cs.extend(((-z(j-1,v),z(j,image),p),(-z(j-1,v),z(j,image),-p)))
    assert q == (L+1)*(2*r-3)+2
    assert len(cs) == (L+1)*(r*r-2)+2*L*r+8
    return tuple(cs), q


def image(mod, tables, s, t):
    cs, n0 = source(tables,s,t)
    target, n, y, u, v, alpha, beta = mod.compile_compatibility(cs,n0)
    bits = mod.encode(target,n,y,alpha,beta,len(tables[0]))[0]
    return bits, target, n, y, u, v, alpha, beta


def endpoint(tables,s):
    path=[s]
    for f in tables:
        path.append(f[path[-1]-1])
    return path


def admit(mod,bits):
    try:
        n,cs,_,_,_=transport.parse(bits)
        if len(cs)<4 or (len(cs)-4)%2:
            return None
        m0=(len(cs)-4)//2; n0=n-m0-3
        if n0<1:return None
        rows=[(cs[4+2*j][1],*cs[5+2*j][1:]) for j in range(m0)]
        for r in range(3,n0+1):
            if (n0-2)%(2*r-3):continue
            L=(n0-2)//(2*r-3)-1
            if L<1 or m0!=(L+1)*(r*r-2)+2*L*r+8:continue
            s=rows[0][0]; t=rows[4][0]-L*r
            if not (1<=s<=r and 1<=t<=r):continue
            start=8+(L+1)*(r*r-2)
            fs=tuple(tuple(rows[start+2*((j-1)*r+v)][1]-j*r for v in range(r))
                     for j in range(1,L+1))
            if any(not 1<=v<=r for f in fs for v in f):continue
            if image(mod,fs,s,t)[0]==bits:
                return endpoint(fs,s)[-1]==t
        return None
    except (ValueError,IndexError,AssertionError):
        return None


def source_witness(tables,s):
    path=endpoint(tables,s); L=len(tables);r=len(tables[0])
    value=sum(1<<(j*r+v-1) for j,v in enumerate(path))
    for j,v in enumerate(path):
        for h in range(r-3):
            if v>h+2:
                name=(L+1)*r+j*(r-3)+h+1
                value |= 1<<(name-1)
    return value


def check(mod,tables,s,t):
    bits,cs,n,y,u,v,alpha,beta=image(mod,tables,s,t)
    L=len(tables);r=len(tables[0]);m=len(cs);w=n.bit_length()
    assert n==(L+1)*(r*r+2*r-5)+2*L*r+13
    assert len(bits)==3*n+2+2*((m+1).bit_length()-1)+3*m*(w+1)+w
    assert all(len(set(map(abs,c)))==3 for c in cs)
    sat=endpoint(tables,s)[-1]==t
    assert admit(mod,bits) is sat
    # Exhaust all one-hot layer choices. Gadget identities justify projection.
    paths=[p for p in product(range(1,r+1),repeat=L+1)
           if p[0]==s and p[-1]==t and all(p[j]==tables[j-1][p[j-1]-1] for j in range(1,L+1))]
    assert len(paths)==int(sat)
    assert (alpha^beta).bit_count()==1
    assert all(any(mod.literal_value(a,alpha) for a in c) for c in cs if sum(a>0 for a in c)<=1)
    assert all(any(mod.literal_value(a,beta) for a in c) for c in cs if sum(a>0 for a in c)>=2)
    if sat:
        src,n0=source(tables,s,t); ass=source_witness(tables,s)
        assert all(any(mod.literal_value(a,ass) for a in c) for c in src)
        target=ass|(1<<(y-1))
        for j,c in enumerate(src):
            if not mod.literal_value(c[0],ass):target |= 1<<(n0+3+j)
        assert all(any(mod.literal_value(a,target) for a in c) for c in cs)
    return dict(L=L,r=r,s=s,t=t,tables=tables,n=n,m=m,N=len(bits),sat=sat,
                satisfying_layer_paths=len(paths),input_sha256=sha256(bits.encode()).hexdigest())


def main():
    mod=transport.load_generator(); groups=[]
    fs=list(product(range(1,4),repeat=3))
    for L in (1,2):
        records=[]
        for tables in product(fs,repeat=L):
            for s,t in product(range(1,4),repeat=2):records.append(check(mod,tables,s,t))
        first=records[0]
        groups.append(dict(L=L,r=3,cases=len(records),SAT=sum(x['sat'] for x in records),
                           n=first['n'],m=first['m'],N=first['N'],
                           record_columns=['tables','s','t','sat','input_sha256'],
                           records=[[x[k] for k in ('tables','s','t','sat','input_sha256')] for x in records]))
    controls=[check(mod,((2,3,4,1),(4,4,4,4),(2,1,4,3)),s,t)
              for s,t in ((1,3),(1,4),(4,3),(4,4))]
    b=image(mod,((1,2,3),),1,1)[0]
    assert admit(mod,b[:-1]) is None and admit(mod,b+'0') is None
    return dict(lemma='DYNAMIC-TABLE-COMPOSITION1',status='COMPUTATIONAL',seed=None,
                scope='All r=3 tables and endpoints at L=1,2; local witnesses and exact byte admission; no TM benchmark',
                groups=groups,controls=controls,malformed_rejections=2,
                script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                generator_sha256=transport.EXPECTED)


if __name__=='__main__':
    print(json.dumps(main(),separators=(',',':')))
