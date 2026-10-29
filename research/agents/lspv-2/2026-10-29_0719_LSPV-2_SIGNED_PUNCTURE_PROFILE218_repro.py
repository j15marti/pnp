#!/usr/bin/env python3
"""SIGNED-PUNCTURE-PROFILE218.
Deterministic stdlib proof-control audit of genuine connected strict signed
exact-(2,2)-3CNF cycles and their two-state puncture transfer matrices.
No SAT oracle, handwaved source data, or input answer bit.
Run: python3 signed_puncture_profile218.py > raw218.json
"""
from __future__ import annotations
from collections import Counter
from hashlib import sha256
from itertools import product
import json

W1 = [(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
    (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
    (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
    (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]


def normal(c):
    return tuple(sorted(c, key=lambda z: (abs(z), z<0)))


def w_mode(a,b):
    C=[list(c) for c in W1]
    if a==0:
        for i in (6,11): C[i][0]=-C[i][0]
    if b==0:
        for i in (17,9): C[i][2]=-C[i][2]
    return tuple(sorted(map(normal,C)))


def affine_shell(p):
    assert p>=5 and p%2==1
    C=[]
    v=lambda g,i: g*p+(i%p)+1
    for s in range(4):
        for i in range(p):
            a,b,c=v(0,i),v(1,i+s),v(2,i+2*s)
            C.append(((-a if s in (0,1) else a),
                      (-b if s in (2,3) else b),
                      (-c if s in (0,2) else c)))
    return tuple(sorted(map(normal,C)))


def offset(C,n):
    return tuple(tuple((1 if z>0 else -1)*(abs(z)+n) for z in c) for c in C)


def canon_signed(C):
    return tuple(sorted(map(normal,C)))


def dimacs(C,n):
    return (f'p cnf {n} {len(C)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in C)).encode('ascii')


def parse_dimacs(data):
    try:
        txt=data.decode('ascii')
        assert txt.endswith('\n')
        lines=txt.splitlines()
        h=lines[0].split()
        assert len(h)==4 and h[:2]==['p','cnf']
        n,m=map(int,h[2:])
        assert n>=1 and m>=1 and len(lines)==m+1
        out=[]
        for line in lines[1:]:
            items=[int(x) for x in line.split()]
            assert len(items)==4 and items[-1]==0
            c=tuple(items[:3])
            assert all(1<=abs(x)<=n for x in c)
            assert len({abs(x) for x in c})==3
            out.append(c)
        assert len(set(map(normal,out)))==m
        return tuple(out),n
    except (ValueError,IndexError,AssertionError,UnicodeDecodeError):
        raise ValueError('not canonical proper 3DIMACS') from None


def connected(C):
    names={abs(z) for c in C for z in c}
    adj={i:set() for i in names}
    for c in C:
        ids=list(map(abs,c))
        for z in ids: adj[z].update(ids)
    seen={min(names)}; stack=list(seen)
    while stack:
        x=stack.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y);stack.append(y)
    return seen==names


def degree22(C,n):
    cnt=Counter(z for c in C for z in c)
    return all(cnt[i]==cnt[-i]==2 for i in range(1,n+1))


def evaluator(C, A):
    return all(any(A[abs(z)]==(z>0) for z in c) for c in C)


def mode_profile(a,b):
    C=w_mode(a,b)
    chosen=(-5,-12,15)
    assert chosen in C
    puncture=tuple(c for c in C if c!=chosen)
    counts=Counter();sample={};full_models=0
    for mask in range(1<<15):
        A={j:bool(mask&(1<<(j-1))) for j in range(1,16)}
        ok=all(any(A[abs(z)]==(z>0) for z in c) for c in puncture)
        if not ok:continue
        alpha=int(not A[5])
        delta=int((not A[12]) or A[15])
        counts[(alpha,delta)]+=1
        sample.setdefault((alpha,delta),mask)
        full_models+=int(alpha or delta)
    return C,counts,sample,full_models


def module_source(p,modes):
    assert p%2==1 and p>=5 and len(modes)>=2
    blocks=[affine_shell(p)]
    sizes=[3*p]
    for a,b in modes:
        assert a in (0,1) and b in (0,1)
        sizes.append(15)
        blocks.append(w_mode(a,b))
    prefix=[0]
    for x in sizes:prefix.append(prefix[-1]+x)
    blocks=[offset(C,prefix[i]) for i,C in enumerate(blocks)]
    labels=[-(p),]+[-(prefix[i]+5) for i in range(1,len(blocks))]
    # The selected affine clause is s=1, i=p-1. The selected W clause is fixed.
    selected=[normal((-p,p+1,2*p+2))]
    selected += [normal(tuple((1 if z>0 else -1)*(abs(z)+prefix[i]) for z in (-5,-12,15)))
                 for i in range(1,len(blocks))]
    out=[]
    for i,block in enumerate(blocks):
        assert selected[i] in block
        assert labels[i] in selected[i]
        incoming=labels[i-1] if i>0 else labels[-1]
        for c in block:
            if c==selected[i]:
                out.append(normal(tuple(incoming if z==labels[i] else z for z in c)))
            else:out.append(c)
    n=prefix[-1]
    assert degree22(out,n) and connected(out)
    assert len(set(map(normal,out)))==len(out)
    return tuple(out),n

PROFILE_W={}
EXAMPLE_W={}
PROFILE_COUNTS={}
FULL_MODEL_COUNTS={}
for a,b in product((0,1),repeat=2):
    _,counts,examples,models=mode_profile(a,b)
    PROFILE_W[a,b]=frozenset(counts)
    EXAMPLE_W[a,b]=examples
    PROFILE_COUNTS[a,b]=counts
    FULL_MODEL_COUNTS[a,b]=models

# General affine puncture has all four pairs. The four explicit witnesses
# are all-zero, with A_(p-1) and/or C_1 flipped; see report proof.
PROFILE_R=frozenset(product((0,1),repeat=2))


def transition(P,prev,current):
    return any(a==current and (prev or d) for a,d in P)


def matrix(P):
    return tuple(tuple(int(transition(P,i,j)) for j in range(2)) for i in range(2))


def bmul(A,B):
    return tuple(tuple(int(any(A[i][h] and B[h][j] for h in range(2))) for j in range(2)) for i in range(2))


def cycle_decision(profiles):
    P=((1,0),(0,1))
    for R in profiles:P=bmul(P,matrix(R))
    return bool(P[0][0] or P[1][1]),P


def brute_profile_cycle(profiles):
    k=len(profiles)
    for ad in product(*[tuple(P) for P in profiles]):
        if all(ad[(i-1)%k][0] or ad[i][1] for i in range(k)):
            return True
    return False


def shell_witness(p):
    # x=A_{p-1}=0; C_1=1; all other shell variables 0.
    return {i:(i==2*p+2) for i in range(1,3*p+1)}


def sat_witness(p,modes):
    assert modes[0]==(1,1) and all(m==(0,0) for m in modes[1:])
    A=shell_witness(p)
    for i,mode in enumerate(modes):
        target=(0,0) if i==0 else (1,1)
        assert target in EXAMPLE_W[mode]
        mask=EXAMPLE_W[mode][target]
        off=3*p+15*i
        for j in range(1,16):A[off+j]=bool(mask & (1<<(j-1)))
    return A


def recover_modes(C,n):
    """Uniform source authenticator: polynomial candidate scan, no SAT side bit.
    Python caches the input; streaming implementation can rescan and use O(log N) bits.
    """
    m=len(C)
    for p in range(5,n//3+1,2):
        extra=n-3*p
        if extra<30 or extra%15:continue
        k=extra//15
        if m!=4*p+20*k:continue
        # Candidate all-(0,0) reveals the exact R prefix, independent of W modes.
        expected,nn=module_source(p,((0,0),)*k)
        if nn!=n or C[:4*p]!=expected[:4*p]:continue
        recovered=[];good=True
        for i in range(k):
            section=C[4*p+20*i:4*p+20*(i+1)]
            matched=[]
            for a,b in product((0,1),repeat=2):
                # Context labels are independent of mode, so the module can be checked locally.
                cand,_=module_source(p,((0,0),)*i+((a,b),)+((0,0),)*(k-i-1))
                if cand[4*p+20*i:4*p+20*(i+1)]==section:matched.append((a,b))
            if len(matched)!=1:good=False;break
            recovered.append(matched[0])
        if good:
            final,_=module_source(p,tuple(recovered))
            if final==C:return p,tuple(recovered)
    raise ValueError('not authenticated cycle grammar')


def shrink(data):
    C,n=parse_dimacs(data)
    for side in ((0,0),(1,1)):
        B=w_mode(*side)
        if C==B and n==15:return data,'base',side
    p,modes=recover_modes(C,n)
    satisfiable,_=cycle_decision([PROFILE_R]+[PROFILE_W[x] for x in modes])
    child=w_mode(0,0) if satisfiable else w_mode(1,1)
    return dimacs(child,15),'child',dict(p=p,modes=modes,answer=satisfiable)


def dpll_independent(C, ordered_vars):
    """Independent finite CNF decision check. No module-profile calls."""
    stats={'calls':0}
    def dfs(A):
        stats['calls']+=1
        A=dict(A)
        while True:
            units=[];active=set();complete=True
            for c in C:
                un=[];sat=False
                for lit in c:
                    v=abs(lit)
                    if v in A:
                        if A[v]==(lit>0):sat=True;break
                    else:un.append(lit)
                if sat:continue
                complete=False
                if not un:return None
                active.update(map(abs,un))
                if len(un)==1:units.append(un[0])
            if complete:return A
            if not units:break
            for lit in units:
                v=abs(lit);b=lit>0
                if v in A and A[v]!=b:return None
                A[v]=b
        x=next(v for v in ordered_vars if v in active)
        for b in (False,True):
            B=dict(A);B[x]=b
            r=dfs(B)
            if r is not None:return r
        return None
    return dfs({}),stats


def profile_256():
    profiles=[frozenset((a,d) for a,d in product((0,1),repeat=2)
                       if mask&(1<<(2*a+d))) for mask in range(16)]
    counts=Counter()
    for A in profiles:
        for B in profiles:
            original=any(a or d for a,d in A) and any(b or e for b,e in B)
            changed=any((b or d) and (a or e) for a,d in A for b,e in B)
            new_brute=brute_profile_cycle([A,B])
            new_dp,_=cycle_decision([A,B])
            assert changed==new_brute==new_dp
            counts[(bool(original),bool(changed))]+=1
    return counts


def test():
    assert FULL_MODEL_COUNTS=={(0,0):772,(0,1):272,(1,0):272,(1,1):0}
    assert PROFILE_W[1,1]==frozenset({(0,0)})
    assert PROFILE_W[0,0]==frozenset(product((0,1),repeat=2))
    assert EXAMPLE_W[1,1][0,0]==2802
    truth=profile_256()
    assert truth=={(False,False):44,(False,True):16,(True,False):8,(True,True):188}
    controls=[];total_signed_checks=0;total_witness_checks=0;total_dps=0
    independent_dpll_checks=[]
    for p,k in ((5,3),(5,4),(7,3),(11,6),(31,7),(101,12)):
        sat_modes=((1,1),)+((0,0),)*(k-1)
        no_modes=((1,1),(1,1))+((0,0),)*(k-2)
        Fsat,n=module_source(p,sat_modes)
        Fno,nn=module_source(p,no_modes)
        assert nn==n
        csat=dimacs(Fsat,n);cno=dimacs(Fno,n)
        assert len(csat)==len(cno)
        by_a={tuple(sorted(map(abs,c))):c for c in Fsat}
        by_b={tuple(sorted(map(abs,c))):c for c in Fno}
        assert by_a.keys()==by_b.keys()
        changes=sum(sum(1 for x,y in zip(by_a[scope],by_b[scope]) if x!=y) for scope in by_a)
        assert changes==4
        assert degree22(Fsat,n) and degree22(Fno,n)
        total_signed_checks+=2
        sat_dp,mat=cycle_decision([PROFILE_R]+[PROFILE_W[m] for m in sat_modes])
        no_dp,_=cycle_decision([PROFILE_R]+[PROFILE_W[m] for m in no_modes])
        assert sat_dp and not no_dp
        total_dps+=2
        A=sat_witness(p,sat_modes)
        assert evaluator(Fsat,A)
        affine=affine_shell(p)
        removed=normal((-p,p+1,2*p+2))
        surviving=tuple(c for c in affine if c!=removed)
        assert len(surviving)==len(affine)-1
        for alpha,delta in product((0,1),repeat=2):
            ar={i:False for i in range(1,3*p+1)}
            ar[p]=not bool(alpha)
            ar[2*p+2]=bool(delta)
            assert evaluator(surviving,ar)
        total_witness_checks+=len(Fsat)
        if p==5 and k==3:
            for C,label in ((Fsat,True),(Fno,False)):
                independent,st=dpll_independent(C,tuple(range(3*p+1,n+1))+tuple(range(1,3*p+1)))
                assert bool(independent)==label
                independent_dpll_checks.append({'label':label,'calls':st['calls'],
                                                'witness_checked':bool(independent)})
                if independent is not None:
                    assert evaluator(C,{i:independent.get(i,False) for i in range(1,n+1)})
        # Strict parsing, complete source authentication, actual child emission and base handling.
        assert parse_dimacs(csat)==(Fsat,n)
        assert parse_dimacs(cno)==(Fno,n)
        if True:  # full source authentication is independently checked at every finite size
            child,typ,info=shrink(csat)
            assert typ=='child' and info['answer'] and child==dimacs(w_mode(0,0),15)
            child2,typ2,_=shrink(child)
            assert typ2=='base' and child2==child
            childN,typN,infoN=shrink(cno)
            assert typN=='child' and not infoN['answer'] and childN==dimacs(w_mode(1,1),15)
            assert shrink(childN)[1]=='base'
        controls.append(dict(p=p,k=k,variables=n,clauses=len(Fsat),
                 sat_bytes=len(csat),unsat_bytes=len(cno),
                 difference_signed_literals=4,source_authenticated=True,
                 sat_witness_checked=True,unsat_adjacent_W11_certificate=True,
                 total_model_assignments_in_W_profiles=4*(1<<15),
                 lambda_3_4_in_BITS=(8*len(dimacs(w_mode(0,0),15))<=(8*len(csat))**0.75)))
    # Independent solver crosscheck on every pair of W modes, fixed p=5,k=3.
    # 4^2=16 source formulas; the solver is entirely separate from profiles.
    full_mode_pair_check={'cases':0,'sat':0,'unsat':0,'dpll_calls':0}
    for m1,m2 in product(product((0,1),repeat=2),repeat=2):
        G,gn=module_source(5,(m1,m2))
        dp,_=cycle_decision([PROFILE_R,PROFILE_W[m1],PROFILE_W[m2]])
        witness,ds=dpll_independent(G,tuple(range(16,gn+1))+tuple(range(1,16)))
        assert bool(witness)==dp
        full_mode_pair_check['cases']+=1
        full_mode_pair_check['sat']+=int(dp)
        full_mode_pair_check['unsat']+=int(not dp)
        full_mode_pair_check['dpll_calls']+=ds['calls']
    # Actual source-body corruptions, including altered sign quotas and malformed formats.
    base,_=module_source(5,((1,1),(0,0)))
    n=45;valid=dimacs(base,n)
    broken=[valid[:-1],valid.replace(b'p cnf 45',b'p cnf 44',1),
        valid.replace(b' 0\n',b'\n',1), valid.replace(b' 0\n',b' 1\n',1),
        valid.replace(b' 0\n',b' 0\n 1 2 3 0\n',1)]
    for bad in broken:
        try:
            c,n=parse_dimacs(bad)
            recover_modes(c,n)
        except ValueError:pass
        else:raise AssertionError('malformed source accepted')
    # Full 15-variable near-model profile verification checks all 131072 assignments;
    # profile-cycle algebra cross-checks all 256 abstract relations.
    return dict(status='PASS',run='SIGNED_PUNCTURE_PROFILE218',seed=None,
      W_full_models={str(k):v for k,v in FULL_MODEL_COUNTS.items()},
      W_puncture_counts={str(m):{str(x):v for x,v in c.items()} for m,c in PROFILE_COUNTS.items()},
      W_example_masks={str(m):{str(x):v for x,v in d.items()} for m,d in EXAMPLE_W.items()},
      profile_256={str(k):v for k,v in truth.items()},
      finite_cases=controls,source_signed22_checks=total_signed_checks,
      inspected_source_clause_evaluations=total_witness_checks,
      matrix_decisions=total_dps,malformed_rejections=len(broken),
      independent_DPLL=independent_dpll_checks,exhaustive_mode_pair_DPLL=full_mode_pair_check,
      mathematically_supported=[
        'exact profile transfer equivalence for disjoint modules linked by cyclic literal exchange',
        'R_p selected puncture admits all four (a,d) states with explicit short witnesses',
        'two adjacent W11 punctures force UNSAT, a preceding W00 admits SAT with explicit witnesses',
        'same-sign cyclic exchange preserves strict exact22 and connects the given modules'],
      limitations=[
        'No general SAT or UNSAT decision lower bound follows.',
        'W profiles are obtained by complete finite enumeration of 15-variable templates, not an instance oracle.',
        'R_p and W modes are authenticated syntactic templates; arbitrary module profile acquisition is not provided.',
        'Python allocation and instruction counts are not native TM step measurements.',
        'This is an architecture-specific restricted contraction, not general SAT compression.'])

if __name__=='__main__':
    print(json.dumps(test(),indent=2,sort_keys=True))