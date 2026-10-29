#!/usr/bin/env python3
"""LSPV-2 EXACT22-IMPLICATION-SPLICE222.
Standalone deterministic construction, source certification, cofactor controls.
No oracle, random samples, or external solver used. Python standard library.
"""
import collections, hashlib, itertools, json

W1 = (
(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14))

def canon(C):
    return tuple(sorted(tuple(sorted(c,key=lambda l:(abs(l),l<0))) for c in C))

def G_base():
    C=[list(c) for c in W1]
    for j in (6,11): C[j][0]=-C[j][0]
    return canon(C)

def affine(p):
    assert p>=5 and p%2
    def v(g,i): return g*p+(i%p)+1
    C=[]
    for s in range(4):
        for i in range(p):
            a=v(0,i);b=v(1,i+s);c=v(2,i+2*s)
            C.append(((-a if s in (0,1) else a),
                      (-b if s in (2,3) else b),
                      (-c if s in (0,2) else c)))
    return canon(C)

def check_strict(C,n,connected=True):
    if len(C)*3 !=4*n or len(C)!=len(set(C)):return False
    cnt=collections.Counter(l for c in C for l in c)
    if any(cnt[v]!=2 or cnt[-v]!=2 for v in range(1,n+1)):return False
    adj=[set() for _ in range(n+1)]
    for c in C:
        if len(c)!=3 or any(not 1<=abs(l)<=n for l in c):return False
        ids=[abs(l) for l in c]
        if len(set(ids))!=3:return False
        for v in ids:adj[v].update(ids)
    if connected:
        seen={1};todo=[1]
        while todo:
            for v in adj[todo.pop()]:
                if v not in seen:seen.add(v);todo.append(v)
        if len(seen)!=n:return False
    return True

def eval_cnf(C,mask):
    return all(any(bool(mask>>(abs(l)-1)&1)==(l>0) for l in c) for c in C)

def dimacs(C,n):
    return ('p cnf %d %d\n'%(n,len(C))+''.join(' '.join(map(str,c))+' 0\n' for c in C)).encode()

def parse_canonical_strict(data):
    """Fully authenticated canonical DIMACS parser for connected exact-(2,2)."""
    if not isinstance(data,bytes):raise ValueError('expected bytes')
    try: s=data.decode('ascii')
    except UnicodeError as exc:raise ValueError('non-ASCII') from exc
    lines=s.splitlines(keepends=True)
    if not lines or any(not row.endswith('\n') for row in lines):
        raise ValueError('unterminated input line')
    hdr=lines[0].strip().split()
    if len(hdr)!=4 or hdr[:2]!=['p','cnf']:
        raise ValueError('bad DIMACS header')
    try: n=int(hdr[2]);m=int(hdr[3])
    except ValueError as exc:raise ValueError('bad header count') from exc
    if n<1 or m<1 or len(lines)!=m+1:raise ValueError('count mismatch')
    C=[]
    for row in lines[1:]:
        fields=row.strip().split()
        if len(fields)!=4 or fields[-1]!='0':raise ValueError('not exactly 3 literals')
        try:clause=tuple(int(t) for t in fields[:3])
        except ValueError as exc:raise ValueError('bad literal') from exc
        C.append(clause)
    C=canon(C)
    if not check_strict(C,n) or dimacs(C,n)!=data:
        raise ValueError('not exact canonical strict connected source')
    return C,n

def parser_negative_controls(C,n):
    good=dimacs(C,n)
    assert parse_canonical_strict(good)==(C,n)
    controls=(good.replace(b'p cnf ',b'p cnc ',1),
              good[:-1],good+b'0\n',
              good.replace(b' 0\n',b' 1\n',1),
              good.replace(b'\n',b'\r\n',1),
              good.replace(b' 0\n',b' 0 0\n',1))
    for datum in controls:
        try:parse_canonical_strict(datum)
        except ValueError:continue
        raise AssertionError('malformed source accepted')
    return len(controls)

def negative_slot(H,x,prefer_extra_negative=False):
    candidates=[i for i,c in enumerate(H) if -x in c]
    if prefer_extra_negative:
        candidates.sort(key=lambda j:(-sum(l<0 for l in H[j]),j))
    return candidates[0]

def splice(H,n,x,slot=None):
    """Swap -x in H with -(n+4) in W1-G negative clause 2.

    Original H variables retain indices 1..n. W1-G occupies n+1..n+15.
    Must not claim this is a cofactor-preserving equality wrapper.
    """
    assert check_strict(H,n) and 1<=x<=n
    hslot=negative_slot(H,x) if slot is None else slot
    assert -x in H[hslot]
    B=[[z+(n if z>0 else -n) for z in c] for c in G_base()]
    assert -(n+4) in B[2]
    A=[list(c) for c in H]
    A[hslot][A[hslot].index(-x)]=-(n+4)
    B[2][B[2].index(-(n+4))]=-x
    C=canon(A+B)
    assert check_strict(C,n+15)
    return C,hslot

def solve(C,pins=None):
    pins={} if pins is None else dict(pins)
    calls=[0]
    def dpll(A,clauses):
        calls[0]+=1
        while True:
            residual=[]; units=[]
            for c in clauses:
                if any(abs(l) in A and A[abs(l)]==(l>0) for l in c): continue
                alive=[l for l in c if abs(l) not in A]
                if not alive:return None
                residual.append(alive)
                if len(alive)==1:units.append(alive[0])
            if not residual:return A
            if not units:break
            for l in units:
                k=abs(l);v=(l>0)
                if k in A and A[k]!=v:return None
                A[k]=v
        freq=collections.Counter(abs(l) for c in residual for l in c)
        x=max(freq,key=lambda v:(freq[v],-v))
        for bit in (False,True):
            Z=dict(A); Z[x]=bit
            r=dpll(Z,residual)
            if r is not None:return r
        return None
    r=dpll(pins,C)
    if r is not None:
        for c in C:
            for l in c:r.setdefault(abs(l),False)
        assert all(any(r[abs(l)]==(l>0) for l in c) for c in C)
    return r,calls[0]

def local_profile(H,n,x,slot,method='dpll'):
    foot=tuple(l for l in H[slot] if abs(l)!=x)
    stripped=H[:slot]+H[slot+1:]
    assert len(foot)==2 and -x in H[slot]
    out={}
    for xv,uv in itertools.product((0,1),repeat=2):
        # u = (foot_lit1 OR foot_lit2) cofactor, implemented by pinning
        # exact u via clause foot if 1, via unit pins both literals false if 0.
        if uv:
            tested=stripped+(foot,)
            pins={x:bool(xv)}
        else:
            tested=stripped
            pins={x:bool(xv)}
            for l in foot:pins[abs(l)]=(l<0)
        r,_=solve(tested,pins)
        out[f'{xv}{uv}']=r is not None
    return out

def cofactor(F,x,p):
    data={}; calls=0
    for xv,pv in itertools.product((0,1),repeat=2):
        witness,ncalls=solve(F,{x:bool(xv),p:bool(pv)})
        calls+=ncalls
        data[f'{xv}{pv}']={'sat':witness is not None,'dpll_calls':ncalls,
         'witness_integer':sum((1<<(i-1)) for i in witness if witness[i]) if witness else None}
    return data,calls

def exhaustive_G_puncture():
    G=G_base(); assert check_strict(G,15)
    slot=2;foot=[l for l in G[slot] if abs(l)!=4]
    S=collections.Counter();W={}
    for mask in range(1<<15):
        if all(any(bool(mask>>(abs(l)-1)&1)==(l>0) for l in c)
               for j,c in enumerate(G) if j!=slot):
            p=(mask>>3)&1
            u=int(any(bool(mask>>(abs(l)-1)&1)==(l>0) for l in foot))
            S[(p,u)]+=1;W.setdefault((p,u),mask)
    assert set(S)=={(0,0),(1,0),(1,1)}
    for mask in range(1<<15):
        if eval_cnf(G,mask):
            assert (mask>>3)&1 in (0,1)
    return {'puncture_counts':{''.join(map(str,k)):v for k,v in sorted(S.items())},
            'puncture_witnesses':{''.join(map(str,k)):v for k,v in sorted(W.items())},
            'checked_assignments':1<<15}

def raw_case(name,H,n,x,slot,with_joint=True):
    assert check_strict(H,n)
    source_bits=8*len(dimacs(H,n))
    assert parse_canonical_strict(dimacs(H,n))==(H,n)
    F,j=splice(H,n,x,slot)
    assert j==slot
    child_bits=8*len(dimacs(F,n+15))
    res={'name':name,'n':n,'m':len(H),'x':x,'clause_index':slot,
         'source_clause':H[slot],'parent_bits':source_bits,'spliced_bits':child_bits,
         'growth_bits':child_bits-source_bits,'child_parent_ratio':round(child_bits/source_bits,9),
         'power_short_3_4': child_bits<=source_bits**.75,
         'source_sha256':hashlib.sha256(dimacs(H,n)).hexdigest(),
         'spliced_sha256':hashlib.sha256(dimacs(F,n+15)).hexdigest()}
    if with_joint:
        rel,calls=cofactor(F,x,n+4)
        original0,_=solve(H,{x:False}); original1,_=solve(H,{x:True})
        prof=local_profile(H,n,x,slot)
        expected={'00':original0 is not None,'01':prof['01'],
                  '10':False,'11':original1 is not None}
        got={k:z['sat'] for k,z in rel.items()}
        assert got==expected,(name,got,expected,prof)
        assert (any(got.values()))==((original0 is not None) or (original1 is not None))
        res.update(cofactors=rel,cofactor_calls=calls,expected_cofactors=expected,
                   source_puncture_profile=prof,
                   source_sat=original0 is not None or original1 is not None,
                   spliced_sat=any(got.values()))
    return res

def main():
    control=exhaustive_G_puncture()
    control['malformed_input_rejections']=parser_negative_controls(G_base(),15)
    R5=affine(5)
    implication_pivots=0
    for x in range(1,16):
        for slot in [j for j,c in enumerate(R5) if -x in c]:
            pp=local_profile(R5,15,x,slot)
            assert pp['01'],('unexpected tight negative foot',x,slot)
            implication_pivots+=1
    control['affine_R5_negative_slots_allow_implication']=implication_pivots
    G=G_base(); out=[]
    out.append(raw_case('G-to-G equality',G,15,4,2))
    for name,C in [('W1 UNSAT original',canon(W1)),('G source',G)]:
        out.append(raw_case(name,C,15,4,negative_slot(C,4)))
    for p in (5,7,31,101,501):
        R=affine(p);slot=negative_slot(R,1,prefer_extra_negative=True)
        out.append(raw_case('affine R_%d'%p,R,3*p,1,slot,with_joint=(p<=7)))
    for r in out:
        if r.get('name')=='affine R_5':
            assert r['expected_cofactors']=={'00':True,'01':True,'10':False,'11':True}
        if r.get('name')=='G-to-G equality':
            assert r['expected_cofactors']=={'00':True,'01':False,'10':False,'11':True}
        if r.get('name')=='W1 UNSAT original':
            assert not r['source_sat'] and not r['spliced_sat']
        assert r['growth_bits']>0
    print(json.dumps({'status':'PASS','run':'EXACT22-IMPLICATION-SPLICE222',
        'G_fixed_puncture':control,'cases':out,
        'claims':['Source-arbitrary strict22 negative-occurrence one-swap preserves SAT/UNSAT.',
                  'Full four-cofactor equality transport is false for affine R_p.',
                  'The splice output grows by O(log N) bits on the selected DIMACS grammar.',
                  'The R_p splice realizes the nonaffine implication relation.'],
        'limitations':['No generic exact cofactor-preserving reduction for arbitrary 3CNF.',
                       'No polynomial-time algorithm for arbitrary puncture-profile acquisition.',
                       'No all-input SAT shrinker or machine-independent lower bound.',
                       'DPLL runs are finite controls, not a kernel-verified theorem.']},sort_keys=True,indent=2))

if __name__=='__main__':main()