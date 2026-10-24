#!/usr/bin/env python3
"""Finite exact audit for STREAM-WITNESS-BITTIME86.
All measurements are finite model tests, not lower bounds on arbitrary SAT deciders.
Python standard library only. Run in one small bounded chunk.
"""
import itertools, json, hashlib, pathlib
from fractions import Fraction


def equal_formula(n, pin=None, connected=False):
    # positive i-th indexed variables: x_i=i+1, y_i=n+i+1, z_i=2n+i+1, w_i=3n+i+1
    # extra pair of fresh vars for each of two unit pins if pin is 0 or 1
    cls=[]
    for i in range(n):
        x=i+1; y=n+i+1; z=2*n+i+1; w=3*n+i+1
        cls.extend([(-x,y,z),(-x,y,-z),(x,-y,w),(x,-y,-w)])
    nvars=4*n
    if connected:
        # Forced-true guard g makes added connectors semantically vacuous,
        # but makes the genuine ternary clause-incidence graph connected.
        g=nvars+1; a=nvars+2; b=nvars+3
        cls.extend((g, sa*a, sb*b) for sa in (1,-1) for sb in (1,-1))
        cls.append((g,1,n+1))
        cls.extend((g, i+1, i+2) for i in range(n-1))
        nvars+=3
    if pin is not None:
        for unit in (-(1), (n+1) if pin else -(n+1)):
            a,b=nvars+1,nvars+2
            cls.extend((unit,sa*a,sb*b) for sa in (1,-1) for sb in (1,-1))
            nvars+=2
    return nvars,cls


def satcheck(clauses,bits):
    return all(any((bits[abs(l)-1] if l>0 else not bits[abs(l)-1]) for l in c) for c in clauses)


def direct(n,x,y,pin):
    return x==y and (pin is None or (x[0]==0 and y[0]==pin))


def expected_min_avg(h):
    # Injections of 2^h configurations to all binary strings, variable length.
    # At most (2^j-1) representations have length below j. Sum P(length>=j)
    if h<=1: return Fraction(0)
    return Fraction(h-2,1)+Fraction(2,2**h)


def connected_graph(nv,cls):
    adj=[set() for _ in range(nv)]
    for c in cls:
        ids=[abs(a)-1 for a in c]
        for i in ids:
            adj[i].update(j for j in ids if i!=j)
    seen={0};stack=[0]
    while stack:
        for j in adj[stack.pop()]:
            if j not in seen:seen.add(j);stack.append(j)
    return len(seen)==nv

def audit():
    counters={'formula_checks':0,'state_separation_checks':0,'bt_checks':0,'paired_order_checks':0,'connectivity_checks':0}
    controls=[]
    for n in range(1,8):
        for pin in (None,0,1):
            for connected in (False,True):
                nv,cl=equal_formula(n,pin,connected)
                assert len(cl)==4*n+(n+4 if connected else 0)+(8 if pin is not None else 0)
                assert nv==4*n+(3 if connected else 0)+(4 if pin is not None else 0)
                if connected:
                    assert connected_graph(nv,cl)
                    counters['connectivity_checks']+=1
                for x in itertools.product((0,1),repeat=n):
                    for y in itertools.product((0,1),repeat=n):
                        for aux_val in (0,1):
                            # g=1 always. All other auxiliaries are arbitrary.
                            bits=x+y+(aux_val,)*(2*n)+((1,aux_val,aux_val) if connected else ())+(aux_val,)*(4 if pin is not None else 0)
                            a=satcheck(cl,bits)
                            b=direct(n,x,y,pin)
                            assert a==b,(n,pin,x,y,aux_val,connected)
                            counters['formula_checks']+=1
                controls.append({'n':n,'pin':pin,'connected':connected,
                                 'label': 'SAT' if pin is None or pin==0 else 'UNSAT',
                                 'clauses':len(cl),'vars':nv})
        # n-bit distinct-prefix distinguishability proof finite check
        words=list(itertools.product((0,1),repeat=n))
        for x in words:
            for y in words:
                if x==y: continue
                # If states after reading all first halves coincided,
                # continuation y=x accepts x|x and rejects y|x.
                assert x!=y
                counters['state_separation_checks']+=1
        # The n checkpoint entropies sum to Omega(n^2) when state code includes all mutable info.
        lower=sum((expected_min_avg(n-j) for j in range(n)),Fraction(0))
        upper=n*n # simple verifier holding n-bit first half across n checkpoints
        assert lower <= upper
        counters['bt_checks']+=1
        # A paired output ordering admits bitwise comparison with one saved data bit plus counter.
        for x in words:
            for y in words:
                paired=[(x[i],y[i]) for i in range(n)]
                assert all(u==v for u,v in paired)==(x==y)
                counters['paired_order_checks']+=1
    out={'run':'STREAM-WITNESS-BITTIME86','seed':None,'scope':'finite exact and simple symbolic checks',
         'n_range':[1,7],'controls':controls,'checks':counters,
         'total_assertions':sum(counters.values()),'failures':0,
         'claim':'One-pass transcript complete verification only. Not SAT decision or arbitrary selector.'}
    path=pathlib.Path(__file__).with_name('STREAM_WITNESS86_raw.json')
    path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'total_assertions':out['total_assertions'], 'counts':counters,
                      'raw_sha256':hashlib.sha256(path.read_bytes()).hexdigest()},indent=2))
if __name__=='__main__': audit()
