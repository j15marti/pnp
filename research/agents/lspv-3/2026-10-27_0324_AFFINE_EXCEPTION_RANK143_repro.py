#!/usr/bin/env python3
"""Affine-exception boundary core theorem independent finite controls; pure Python.
Seed fixed 20261027. Restriction: explicit Boolean boundary projections, NOT derived SAT projections.
"""
import json, random, hashlib, itertools, math
from collections import Counter
R = random.Random(20261027)
checks=Counter()

def check(x, label):
    checks[label]+=1
    if not x: raise AssertionError(label)

def bitset_affine(b, equations):
    return {x for x in range(1<<b) if all((x & mask).bit_count()%2==rhs for mask,rhs in equations)}

def select_core(b, affines, exceptions):
    """Returns selected authenticated module IDs and rank r. No source-projection inference."""
    full=set(range(1<<b))
    cur=full.copy(); sel=[]
    for mid,eqns in affines:
        nxt=cur & bitset_affine(b,eqns)
        if nxt != cur:
            sel.append(mid)
            cur=nxt
            if not cur: return sel, None, 'AFFINE_CONFLICT'
    # Source affine restriction is now cur, rank r if nonempty.
    r=b-(len(cur).bit_length()-1)
    if not exceptions or all(x in set.intersection(*(set(t) for _,t in exceptions)) for x in cur):
        return None,r,'SAT'
    selected=list(sel)
    for x in sorted(cur):
        found=next((mid for mid,support in exceptions if x not in support),None)
        if found is None: return None,r,'SAT'
        if found not in selected:selected.append(found)
    return selected,r,'EXCEPTIONS'

def intersection_of_selected(b, affines, exceptions, sel):
    mp={i: bitset_affine(b,e) for i,e in affines}
    mp.update({i:s for i,s in exceptions})
    return set.intersection(set(range(1<<b)), *(mp[i] for i in sel))

# Random explicit affine modules and arbitrary nonaffine supports.
for b in range(1,7):
    universe=set(range(1<<b))
    for rep in range(450):
        nA=R.randrange(1,8);nQ=R.randrange(0,9)
        aff=[];exc=[]
        for j in range(nA):
            eqn=[(R.randrange(1<<b),R.randrange(2)) for _ in range(R.randrange(0,4))]
            aff.append((f'a{j}',eqn))
        for j in range(nQ):
            supp={x for x in universe if R.randrange(2)}
            exc.append((f'e{j}',supp))
        core,r,typ=select_core(b,aff,exc)
        truth=bool(set.intersection(universe,*[bitset_affine(b,e) for _,e in aff],*[s for _,s in exc]))
        check((core is None)==truth,'random_truth')
        if core is not None:
            check(not intersection_of_selected(b,aff,exc,core),'source_identified_core_sound')
            if typ=='AFFINE_CONFLICT':
                check(len(core)<=b+1,'affine_helly')
            else:
                check(r is not None and len(core)<=r+min(nQ,1<<(b-r)),'mixed_rank_defect_bound')
        else:
            check(typ=='SAT','positive_status')

# Sharp family: r affine coordinate pins, and 2^t complements of points on A.
# Every selected constraint necessary and all exceptions truly nonaffine for b>=3.
sharp=[]
for r in range(0,4):
    for t in range(2,5):
        b=r+t;universe=set(range(1<<b));A={x for x in universe if (x & ((1<<r)-1))==0}
        aff=[(f'pin{i}',[(1<<i,0)]) for i in range(r)]
        exc=[(f'forbid{w}',universe-{w<<r}) for w in range(1<<t)]
        core,rr,typ=select_core(b,aff,exc)
        check(rr==r and typ=='EXCEPTIONS','sharp_rank')
        check(len(core)==r+(1<<t),'sharp_bound_attained')
        for missing in core:
            rem=[x for x in core if x!=missing]
            check(bool(intersection_of_selected(b,aff,exc,rem)),'sharp_every_module_essential')
        sharp.append({'b':b,'r':r,'t':t,'modules':len(core)})

# A fully ordinary proper 3CNF sharp example for b=3,r=1,t=2.
# Unit pin ~y1 is source-authenticated by a 4-clause proper ternary gadget.
# Vars 1=y1,2=y2,3=y3,4=u,5=v.
pin=[(-1,s4*4,s5*5) for s4 in (1,-1) for s5 in (1,-1)]
exclude=[(1,s2*2,s3*3) for s2 in (1,-1) for s3 in (1,-1)]
F=pin+exclude

def sat(F,n):
    for a in range(1<<n):
        if all(any(((a>>(abs(x)-1))&1)==int(x>0) for x in cl) for cl in F):return a
    return None
check(all(len(c)==3 and len(set(map(abs,c)))==3 for c in F),'proper_three')
check(len(set(tuple(c) for c in F))==8,'distinct_clauses')
check(sat(F,5) is None,'proper_3cnf_unsat')
for idx in range(len(F)):
    check(sat(F[:idx]+F[idx+1:],5) is not None,'eight_clause_minimal_unsat')
# Signed-degree controls. y1 is 4+4-, all others are 2+2-.
deg={v: (sum(v in c for c in F),sum(-v in c for c in F)) for v in range(1,6)}
check(deg=={1:(4,4),2:(2,2),3:(2,2),4:(2,2),5:(2,2)},'honest_not_exact22')
# Source-identified unit derivation by three resolutions; no Boolean oracle.
def resolve(a,b,pivot):
    check(pivot in a and -pivot in b,'resolution_inputs')
    c=tuple(sorted((set(a)-{pivot}) | (set(b)-{-pivot})))
    check(not any(-i in c for i in c),'no_tautological_resolvent')
    return c
c0=resolve(pin[0],pin[1],5)
c1=resolve(pin[2],pin[3],5)
c2=resolve(c0,c1,4)
check(c2==(-1,), 'authenticated_unit_resolution')
# Every point in y1=0 violates exactly one of four original exception clauses.
for w2,w3 in itertools.product((0,1),repeat=2):
    val={1:0,2:w2,3:w3}
    bad=[j for j,cl in enumerate(exclude) if not any(val[abs(z)] == (1 if z>0 else 0) for z in cl)]
    check(len(bad)==1,'point_exclusion_exactly_one')
# Two genuine ordinary SAT descendants, preserve source IDs and truth.
# After conditioning y2 then y3, UNSAT source stays UNSAT in every branch.
def restrict(F,branch):
    out=[]
    for cid,cl in enumerate(F):
        if any(branch.get(abs(x),-1)==int(x>0) for x in cl):continue
        row=tuple(x for x in cl if abs(x) not in branch)
        out.append((cid,row))
    return out
for y2,y3 in itertools.product((0,1),repeat=2):
    c1=restrict(F,{2:y2});c2=restrict(F,{2:y2,3:y3})
    check(len(c2)<len(c1)<len(F),'two_genuine_child_levels')
    check(sat([cl for _,cl in c1],5) is None and sat([cl for _,cl in c2],5) is None,'unsat_descendants')
    # Delete the one exception clause for this boundary word => SAT control.
    miss=[j for j,cl in enumerate(exclude) if not any(({1:0,2:y2,3:y3}[abs(x)]==int(x>0)) for x in cl)][0]
    Fsat=F[:4]+exclude[:miss]+exclude[miss+1:]
    check(sat(Fsat,5) is not None,'sat_one_exception_missing')
    check(sat([cl for _,cl in restrict(Fsat,{2:y2,3:y3})],5) is not None,'sat_child_path')
# Copy Y versus shared Y hostile control: (y),(~y) UNSAT only if same original identifier.
check(sat([(1,),(-1,)],2) is None and sat([(1,),(-2,)],2) is not None,'shared_boundary_identifier')

# Authentication adversaries: source-indexed resolution lines must match original signed rows.
def checked_resolution(source_rows, sequence):
    known={i:tuple(sorted(c)) for i,c in enumerate(source_rows)}
    for nextid,p1,p2,pivot,expected in sequence:
        if p1 not in known or p2 not in known or pivot not in known[p1] or -pivot not in known[p2]:return False
        row=tuple(sorted((set(known[p1])-{pivot}) | (set(known[p2])-{-pivot})))
        if row!=tuple(sorted(expected)) or any(-i in row for i in row):return False
        known[nextid]=row
    return True
lines=[(8,0,1,5,(-1,4)), (9,2,3,5,(-1,-4)), (10,8,9,4,(-1,))]
check(checked_resolution(F,lines),'source_resolution_valid')
spoof=[list(c) for c in F];spoof[0][0]=1
check(not checked_resolution(spoof,lines),'source_spoof_rejected')
check(not checked_resolution(F,lines[:-1]+[(10,8,9,4,(1,))]),'false_terminal_rejected')
# Small Horn and 2CNF hostility: do not label a SAT source as UNSAT.
check(sat([(1,),(-1,2),(-2,)],2) is None,'horn_unsat')
check(sat([(-1,2),(-2,1)],2) is not None,'krom_sat')
check(sat([(1,2),(-1,-2)],2) is not None,'binary_xor_sat')

# Strict signed exact22 controls sourced from W1 (4 model counts, no false UWI acceptance).
W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
 (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
 (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
 (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
for a,b in itertools.product((0,1),repeat=2):
    cls=[list(c) for c in W1]
    for row,j in ((6,0),(11,0)):
        if a==0:cls[row][j]*=-1
    for row,j in ((17,2),(9,2)):
        if b==0:cls[row][j]*=-1
    signed={v:(sum(v in c for c in cls),sum(-v in c for c in cls)) for v in range(1,16)}
    check(all(x==(2,2) for x in signed.values()),'W1_strict_exact22')
    count=0
    for mask in range(1<<15):
        count+=all(any(((mask>>(abs(x)-1))&1)==int(x>0) for x in c) for c in cls)
    check(count=={(0,0):772,(0,1):272,(1,0):272,(1,1):0}[(a,b)],'W1_models')

# XOR/affine and Horn/2SAT controls: parsed semantic truth, not false-UNSAT guesses.
for b in range(2,6):
    # Odd XOR cycle: x0 XOR x1 =0, ..., last x_last XOR x0=1, has no solution.
    eq=[((1<<i)|(1<<((i+1)%b)),int(i==b-1)) for i in range(b)]
    # b=2 creates two opposite equations on same mask: also UNSAT.
    aff=[(str(i),[e]) for i,e in enumerate(eq)]
    core,_,typ=select_core(b,aff,[])
    check(typ=='AFFINE_CONFLICT' and core is not None,'odd_affine_cycle')
# Tseitin K4 even/odd edges parity rows (each edge touches two vertices).
verts=range(4);edges=list(itertools.combinations(verts,2));maskrow=[]
for v in verts:maskrow.append(sum(1<<i for i,(a,b) in enumerate(edges) if a==v or b==v))
for parity in (0,1):
    eq=list(zip(maskrow,[parity,0,0,0]))
    status=bool(bitset_affine(6,eq))
    check(status==(parity==0),'K4_even_odd_tseitin')

out={'run':'LSPV3_AFFINE_EXCEPTION_RANK143','random_seed':20261027,'controls':dict(sorted(checks.items())), 'total_assertions':sum(checks.values()),'failures':0,'sharp':sharp,'proper_three_clause_model':'5 vars, 8 clauses, connected, minimal unsat; 4/4 on y1, 2/2 others','structural': 'affine consistent rank r, q arbitrary supports: <=r+min(q,2^(b-r)); affine inconsistent <=b+1','statuses':{'theorem':'RESTRICTED_PROVED_PENDING_REVIEW','general_coverage':'OPEN','p_vs_np':'OPEN'}}
print(json.dumps(out,sort_keys=True,indent=2))
