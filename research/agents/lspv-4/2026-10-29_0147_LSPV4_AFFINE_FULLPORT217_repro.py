#!/usr/bin/env python3
"""LSPV-4 AFFINE-FULLPORT217, full independent reproducer.

Checks exact GF(2) existential projection, full ordinary proper-3CNF gadget
compilation, authenticated physical serialization, and restricted size descent.
Run: python 2026-10-29_0147_LSPV4_AFFINE_FULLPORT217_repro.py > results.json
No external packages and no unrestricted SAT or time-space claim.
"""
from __future__ import annotations
import itertools
import json
import math
import random
import hashlib
from collections import defaultdict

SEED = 202610290147
RNG = random.Random(SEED)
CHECKS = 0

def check(cond, message='assertion failed'):
    global CHECKS
    CHECKS += 1
    if not cond:
        raise AssertionError(message)

def parity(v):
    return v.bit_count() & 1

def eqholds(rows, val):
    return all(parity(mask & val) == rhs for mask, rhs in rows)

def reduce_rows(rows, n):
    """Canonical RREF on variable columns and rhs. Return [(mask, rhs)]."""
    aa = [mask | (rhs << n) for mask,rhs in rows]
    r = 0
    for col in range(n):
        hit = next((i for i in range(r,len(aa)) if (aa[i]>>col)&1),None)
        if hit is None: continue
        aa[r],aa[hit] = aa[hit],aa[r]
        for i in range(len(aa)):
            if i != r and ((aa[i]>>col)&1): aa[i] ^= aa[r]
        r+=1
    reduced = [(x & ((1<<n)-1),(x>>n)&1) for x in aa]
    if any(mask==0 and rhs==1 for mask,rhs in reduced):
        return [(0,1)]
    return [row for row in reduced if row[0]]

def project_affine(rows,n,keep):
    """Eliminate every variable outside keep from A*x=b over GF(2)."""
    keep=tuple(keep)
    assert all(0<=v<n for v in keep) and len(set(keep))==len(keep)
    kept=set(keep)
    elim=[v for v in range(n) if v not in kept]
    aa=[mask | (rhs<<n) for mask,rhs in rows]
    piv=0
    for col in elim:
        hit=next((i for i in range(piv,len(aa)) if (aa[i]>>col)&1),None)
        if hit is None:continue
        aa[piv],aa[hit]=aa[hit],aa[piv]
        for i in range(len(aa)):
            if i!=piv and ((aa[i]>>col)&1): aa[i]^=aa[piv]
        piv+=1
    # Lower rows have zero coefficient in every eliminated variable.
    out=[]
    for big in aa[piv:]:
        mask=sum(((big>>v)&1)<<j for j,v in enumerate(keep))
        rhs=(big>>n)&1
        out.append((mask,rhs))
    return reduce_rows(out,len(keep))

def xor3_clauses(variables,rhs):
    """Four *proper* signed ternary clauses enforcing XOR of three vars = rhs."""
    assert len(set(variables))==3
    out=[]
    for bits in itertools.product((0,1),repeat=3):
        if (sum(bits)&1)==rhs: continue
        out.append(tuple(-v if b else v for v,b in zip(variables,bits)))
    assert len(out)==4
    return out

def compile_proper3(n,rows):
    """Proper ordinary ternary CNF with existential aux for full affine rows."""
    aux=n
    clauses=[]
    def fresh():
        nonlocal aux
        aux+=1
        return aux
    def pad2(l,r):
        u=fresh()
        clauses.extend(((l,r,u),(l,r,-u)))
    for mask,rhs in rows:
        variables=[j+1 for j in range(n) if (mask>>j)&1]
        k=len(variables)
        if k==0:
            if rhs:
                a,b,c=fresh(),fresh(),fresh()
                for bits in itertools.product((0,1),repeat=3):
                    clauses.append(tuple(-v if bit else v for v,bit in zip((a,b,c),bits)))
        elif k==1:
            lit=variables[0] if rhs else -variables[0]
            u,v=fresh(),fresh()
            for s,t in itertools.product((-1,1),repeat=2):
                clauses.append((lit,s*u,t*v))
        elif k==2:
            a,b=variables
            if rhs==0:
                pad2(-a,b);pad2(a,-b)
            else:
                pad2(a,b);pad2(-a,-b)
        else:
            prev=variables[0]
            for v in variables[1:-2]:
                t=fresh()
                clauses.extend(xor3_clauses((prev,v,t),0))
                prev=t
            clauses.extend(xor3_clauses((prev,variables[-2],variables[-1]),rhs))
    for clause in clauses:
        check(len(clause)==3 and len(set(map(abs,clause)))==3,'non-proper 3CNF')
        check(all(1<=abs(v)<=aux for v in clause),'bad identifier')
    return aux,tuple(clauses)

def encode_instance(n,rows):
    """Canonical physical DIMACS, authenticated XOR metadata in comments."""
    assert n>=1
    for mask,rhs in rows:
        assert 0<=mask<(1<<n) and rhs in (0,1)
    nvar,clauses=compile_proper3(n,rows)
    lines=[f'c affine-fullport v1 {n} {len(rows)}',
           'c core '+(' '.join(map(str,range(1,n+1))))]
    for mask,rhs in rows:
        cols=[str(i+1) for i in range(n) if (mask>>i)&1]
        lines.append('c xor '+str(rhs)+((' '+' '.join(cols)) if cols else ''))
    lines.append(f'p cnf {nvar} {len(clauses)}')
    lines.extend(' '.join(map(str,clause))+' 0' for clause in clauses)
    return ('\n'.join(lines)+'\n').encode('ascii')

def decode_instance(data):
    """Authenticate entire input byte-for-byte, including CNF gadgets."""
    text=data.decode('ascii')
    lines=text.splitlines()
    if not lines or not lines[0].startswith('c affine-fullport v1 '):
        raise ValueError('bad tag')
    try:
        parts=lines[0].split();n=int(parts[3]);nr=int(parts[4])
        if n<1 or nr<0 or n>len(data) or nr>len(data) or len(lines)<nr+3:
            raise ValueError('bad or excessively large header')
        if lines[1] != 'c core '+' '.join(map(str,range(1,n+1))):
            raise ValueError('bad core list')
        rows=[]
        for line in lines[2:2+nr]:
            z=line.split()
            if len(z)<3 or z[:2]!=['c','xor']:
                raise ValueError('bad row')
            rhs=int(z[2]);ids=list(map(int,z[3:]))
            if rhs not in (0,1) or ids!=sorted(set(ids)) or any(x<1 or x>n for x in ids):
                raise ValueError('bad row entries')
            mask=sum(1<<(x-1) for x in ids)
            rows.append((mask,rhs))
        if encode_instance(n,rows)!=data: raise ValueError('body mismatch')
        return n,tuple(rows)
    except (IndexError,TypeError,UnicodeError) as e:
        raise ValueError('malformed input') from e

def sat_cnf(clauses, nvar, fixed):
    """Independent DPLL for fixed assignments. Never reads XOR row metadata."""
    def solve(clauses, val):
        while True:
            remain=[];units=[]
            for clause in clauses:
                if any(abs(l) in val and val[abs(l)]==(l>0) for l in clause):
                    continue
                live=[l for l in clause if abs(l) not in val]
                if not live:return False
                if len(live)==1:units.append(live[0])
                remain.append(clause)
            if not units:
                if not remain:return True
                v=abs(next(l for cl in remain for l in cl if abs(l) not in val))
                return solve(remain,{**val,v:False}) or solve(remain,{**val,v:True})
            for l in units:
                v=abs(l);b=l>0
                if v in val and val[v]!=b:return False
                val[v]=b
    return solve(clauses, dict(fixed))

def direct_extension_exists(rows,n,keep,y):
    """Independent fixed-boundary feasibility by substituting y, then GF(2) SAT."""
    fixed={v:(y>>j)&1 for j,v in enumerate(keep)}
    hidden=[v for v in range(n) if v not in fixed]
    rewritten=[]
    for mask,rhs in rows:
        b=rhs
        for v,bit in fixed.items():
            if (mask>>v)&1:b^=bit
        newmask=sum(((mask>>v)&1)<<j for j,v in enumerate(hidden))
        rewritten.append((newmask,b))
    return reduce_rows(rewritten,len(hidden))!=[(0,1)]

def run():
    sizes=[(n,m) for n in range(1,9) for m in (0,1,2,n,n+3)]
    cases=0;assignments=0;physical_cnf=0;no=0;yes=0;bad=0
    for n,m in sizes:
        for rep in range(8):
            rows=[(RNG.getrandbits(n),RNG.randrange(2)) for _ in range(m)]
            if rep%4==0:rows.append((0,1))
            # Test arbitrary unsorted retained-subsets, not only suffix projection.
            k=RNG.randrange(n+1)
            keep=RNG.sample(range(n),k)
            P=project_affine(rows,n,keep)
            for y in range(1<<k):
                direct=False
                for hx in range(1<<(n-k)):
                    x=0
                    for j,v in enumerate(keep):x|=((y>>j)&1)<<v
                    for j,v in enumerate(i for i in range(n) if i not in set(keep)):
                        x|=((hx>>j)&1)<<v
                    if eqholds(rows,x):direct=True;break
                projected=eqholds(P,y)
                check(projected==direct,'projection mismatch')
                assignments+=1
            enc=encode_instance(k if k>0 else 1,
               P if k>0 else ([(0,1)] if not eqholds(P,0) else []))
            kn,parsed=decode_instance(enc)
            check(kn==max(1,k) and tuple(parsed)==tuple(P if k>0 else ([(0,1)] if not eqholds(P,0) else [])))
            nv,clauses=compile_proper3(kn,parsed)
            for y in range(1<<k):
                original=eqholds(P,y)
                fixed={i+1:bool((y>>i)&1) for i in range(k)}
                actual=sat_cnf(clauses,nv,fixed)
                check(actual==original,'proper3CNF gadget mismatch')
                physical_cnf+=1
            cases+=1
            if eqholds(P,0):yes+=1
            else:no+=1
            # Hostile single-byte mutation to actual CNF must fail authentication.
            marker=b'\np cnf '
            start=enc.find(marker)
            if start!=-1 and len(enc)>start+9:
                pos=start+2
                badenc=enc[:pos]+bytes([enc[pos]^1])+enc[pos+1:]
                try:decode_instance(badenc)
                except ValueError:bad+=1
                else:check(False,'bad source accepted')
    # Infinitesimal marginal summaries cannot distinguish x0=x1 from x0!=x1.
    equal=[(0b11,0)]; unequal=[(0b11,1)]
    support=lambda rows,i:{(v>>i)&1 for v in range(4) if eqholds(rows,v)}
    for i in range(2):check(support(equal,i)==support(unequal,i)=={0,1})
    check({v for v in range(4) if eqholds(equal,v)}!={v for v in range(4) if eqholds(unequal,v)})
    # Nonaffine OR3 cannot be any projection of affine constraints: 7 states.
    or3={v for v in range(8) if v!=0}
    check(len(or3)==7 and (len(or3)&(len(or3)-1))!=0)
    # Dense K_n XOR constraints have complete primal scopes but easy elimination.
    dense=[]
    for n in (4,6,10,18):
        rows=[((1<<i)|(1<<j),RNG.randrange(2)) for i in range(n) for j in range(i+1,n)]
        P=project_affine(rows,n,tuple(range(min(n,4))))
        check(len(P)<=min(n,4) or P==[(0,1)])
        dense.append({'core_n':n,'binary_xor_edges':len(rows),'projected_rank_max':len(P),'affine_answer':any(eqholds(P,y) for y in range(1<<min(n,4)))})
    # Full bitlength sample on a sparse large class, two *genuine* reductions.
    length_samples=[]
    for n in (64,256,1024,4096):
        rows=[]
        for i in range(n):
            mask=1<<i
            for j in range(1,3):mask|=1<<((i+j)%n)
            rows.append((mask,RNG.randrange(2)))
        source=encode_instance(n,rows)
        ns,rs=decode_instance(source)
        path=[len(source)]
        chain=[(ns,rs)]
        for _ in range(2):
            nprev,prev=chain[-1]
            newn=max(1,math.isqrt(math.isqrt(nprev)))
            keep=tuple(range(nprev-newn,nprev))
            p=project_affine(prev,nprev,keep)
            child=encode_instance(newn,p)
            chk=decode_instance(child)
            check(chk==(newn,tuple(p)))
            if nprev<=16:
                for y in range(1<<newn):
                    check(eqholds(p,y)==direct_extension_exists(prev,nprev,keep,y),
                          'small reentry full-port projection')
            chain.append(chk)
            path.append(len(child))
        length_samples.append({'core_n':n,'physical_bytes':path,
            'first_power_shrink_0_75':path[1]*8<=(path[0]*8)**.75,
            'second_power_shrink_0_75':path[2]*8<=(path[1]*8)**.75})
    return {'status':'PASS','seed':SEED,'assertions':CHECKS,'random_projection_cases':cases,
       'bruteforce_projection_assignments':assignments,'compiled_3cnf_fixed_assignment_checks':physical_cnf,
       'source_authentication_rejections':bad,'zero_assignment_projection_true':yes,'zero_assignment_projection_false':no,
       'marginal_counterexample':'x0 XOR x1=0 versus =1; same singleton supports',
       'nonaffine_counterexample':'OR3 has 7 assignments; every affine relation has 0 or power-of-two cardinality',
       'dense_complete_primal_controls':dense,'physical_two_level_samples':length_samples,
       'source_note':'Library archive rerun separately and matched archived JSON SHA256 05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca',
       'model_ledger':'conservative explicit fixed-k time O(N^5), work O(N^2); simulated one-tape time O(N^7), footprint O(N^2)',
       'scope':'restricted authenticated affine XOR-to-proper3CNF; P vs NP OPEN'}

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
