#!/usr/bin/env python3
"""REALIZABLE-TRANSFER-FRONTIER233. Deterministic stdlib reproducibility.

Two distinguishable objects:
 (A) connected strict exact-(2,2) cyclic-block 3CNF and a fixed-interface
     decomposition with EXACT private hitting number q=a-1; on this restricted
     grammar Boolean 4x4 transfer matrices decide SAT in polynomial time.
 (B) connected exact22 SAT/UNSAT conjunctions created using the authenticated
     fixed guard of CONNECTOR231, with finite gate and W1 controls.

Timing is Python wall time, traced peak allocations, not native-TM resource
bounds. Counters separately record source characters, parses, transitions,
matrix updates and table entries. No SAT/UNSAT answer bit is supplied to the
uniform transfer algorithm; source grammar is verified.

Run: python 2026-10-29_1514_LSPV-2_REALIZABLE_TRANSFER_FRONTIER233_repro.py > ...raw.json
No third-party dependencies; Python 3.10+.
"""
import collections
import hashlib
import io
import itertools
import json
import math
import statistics
import time
import tracemalloc

C = collections.Counter

# FINITE fixed control copied from source CONNECTOR231 (repository blob
# ddfea2285320d3143ac653986e708d562ecabde6) for self-contained reproduction.
W1=[
(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
V=[tuple(-lit if (j in (4,11) and abs(lit)==9) else lit
          for lit in clause) for j,clause in enumerate(W1)]
G=[tuple(-lit if (j in (6,11) and abs(lit)==4) else lit
          for lit in clause) for j,clause in enumerate(W1)]
D,E=4,6

def cyclic(n):
    if n<6 or n%3:raise ValueError('n multiple of 3, n>=6')
    clauses=[]
    for i in range(n):
        clauses.append((i+1,(i+1)%n+1,-((i+2)%n+1)))
    for i in range(0,n,3):
        clauses.append((-(i+1),-(i+2),-(i+3)))
    return clauses

def dimacs(clauses):
    n=max(abs(x) for c in clauses for x in c)
    return 'p cnf %d %d\n'%(n,len(clauses))+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)

def from_dimacs(source,stats=None):
    cs=[];n_header=m_header=None
    for row in io.StringIO(source):
        if stats is not None:stats['source_line_parses']+=1;stats['source_bytes_seen']+=len(row)
        s=row.strip()
        if not s or s.startswith('c'):continue
        if s.startswith('p '):
            x=s.split()
            if len(x)!=4 or x[1]!='cnf':raise ValueError('invalid header')
            n_header,m_header=int(x[2]),int(x[3]);continue
        a=list(map(int,s.split()))
        if not a or a[-1]!=0 or any(y==0 for y in a[:-1]):raise ValueError('bad clause')
        cs.append(tuple(a[:-1]))
    if n_header is None or len(cs)!=m_header or not cs:return None
    if n_header!=max(abs(l) for c in cs for l in c):return None
    return n_header,cs

def validate_exact22(cs,need_connect=True):
    n=max(abs(l) for cl in cs for l in cl)
    assert len(cs)*3==4*n
    assert all(len(cl)==3 and len(set(map(abs,cl)))==3 for cl in cs)
    assert len(set(tuple(sorted(c)) for c in cs))==len(cs)
    cnt=C(l for cl in cs for l in cl)
    assert all(cnt[j]==cnt[-j]==2 for j in range(1,n+1))
    if need_connect:
        adjacent={j:set() for j in range(1,n+1)}
        for cl in cs:
            a,b,c=map(abs,cl)
            adjacent[a].update((b,c));adjacent[b].update((a,c));adjacent[c].update((a,b))
        seen={1};stack=[1]
        while stack:
            for v in adjacent[stack.pop()]-seen:
                seen.add(v);stack.append(v)
        assert len(seen)==n
    return n,len(cs)

def evaluate_clause(cl,assignment):
    return any(assignment[abs(l)]==int(l>0) for l in cl)

def eval_mask_cl(cl,mask):
    return any(((mask>>(abs(l)-1))&1)==int(l>0) for l in cl)

def fixed_models(cs,n):
    count=0;first=None
    for mask in range(1<<n):
        if all(eval_mask_cl(cl,mask) for cl in cs):
            count+=1
            if first is None:first=mask
    return count,first

# Each 3-vertex block has two source clauses on one scope and one on the
# next two consecutive scopes, four clauses total. A 5-variable local graph.
def scopes_by_block(n,j):
    p=3*j
    return [frozenset(((p+u)%n)+1 for u in offsets)
            for offsets in ((0,1,2),(1,2,3),(2,3,4))]

def expected_scopes(n):
    out=C()
    for j in range(n//3):
        a,b,c=scopes_by_block(n,j)
        out[a]+=2;out[b]+=1;out[c]+=1
    return out

def validate_scopes(cs,n):
    return C(frozenset(map(abs,cl)) for cl in cs)==expected_scopes(n)

# Four endpoints, one private middle bit; relation is 4x4 Boolean matrix.
def transfer_for_block(clauses,n,j,stats=None):
    p=3*j
    names=[(p+v)%n+1 for v in range(5)]
    assert len(set(names))==5
    matrix=[0]*4
    for left in range(4):
        for right in range(4):
            feasible=False
            for mid in range(2):
                bits=(left&1,(left>>1)&1,mid,right&1,(right>>1)&1)
                assignment=dict(zip(names,bits))
                if stats is not None:stats['local_candidate_assignments']+=1
                if all(evaluate_clause(cl,assignment) for cl in clauses):
                    feasible=True;break
            if feasible:matrix[left]|=1<<right
    return matrix

def bool_mult(a,b,stats=None):
    result=[0]*4
    for i in range(4):
        row=0
        for j in range(4):
            if a[i]>>j&1:
                row|=b[j]
                if stats is not None:stats['bool_row_unions']+=1
        result[i]=row
    return result

def bool_pow(a,e):
    result=[1,2,4,8]
    for _ in range(e):result=bool_mult(result,a)
    return result

def gfrank(rows):
    basis={}
    for x in rows:
        while x:
            i=x.bit_length()-1
            if i not in basis:basis[i]=x;break
            x^=basis[i]
    return len(basis)

def trace_positive(a):
    return any(a[j] & (1<<j) for j in range(4))

def material_solver(source,stats):
    parsed=from_dimacs(source,stats)
    if parsed is None:return ('INVALID',None)
    n,cs=parsed
    if n<6 or n%3 or not validate_scopes(cs,n):return ('INVALID',None)
    if len(set(tuple(sorted(c)) for c in cs))!=len(cs):return ('INVALID',None)
    if not quotas_ok(cs,n):return ('INVALID',None)
    byscope=collections.defaultdict(list)
    for cl in cs:byscope[frozenset(map(abs,cl))].append(cl)
    acc=[1,2,4,8];local=[]
    for j in range(n//3):
        a,b,c=scopes_by_block(n,j)
        ls=byscope[a]+byscope[b]+byscope[c]
        assert len(ls)==4
        m=transfer_for_block(ls,n,j,stats)
        acc=bool_mult(acc,m,stats)
        local.append(m)
    return 'SAT' if trace_positive(acc) else 'UNSAT',local

def quotas_ok(cs,n):
    counts=C(lit for cl in cs for lit in cl)
    return all(counts[j]==counts[-j]==2 for j in range(1,n+1))

def iter_input_lines(source):
    """Read-only source cursor; allocate only current line, never a copy of N."""
    i=0
    while i<len(source):
        j=source.find('\n',i)
        if j<0:j=len(source)
        yield source[i:j+1] if j<len(source) else source[i:j]
        i=j+1

def stream_solver(source,stats):
    """Correct on any signed input matching the cyclic-block scope grammar.
    Uses source as read-only input, no length-n occurrence table; repeated scans
    validate every scope and both signed degree quotas. O(n*N) symbol scanning.
    """
    head=next(iter_input_lines(source)).strip().split()
    if len(head)!=4 or head[:2]!=['p','cnf']:return ('INVALID',None)
    try:n,ms=int(head[2]),int(head[3])
    except ValueError:return ('INVALID',None)
    if n<6 or n%3 or ms!=4*n//3:return ('INVALID',None)
    def scan():
        for line in iter_input_lines(source):
            stats['source_line_parses']+=1;stats['source_bytes_seen']+=len(line)
            if line.startswith('p '):continue
            raw=line.split()
            if len(raw)!=4 or raw[-1]!='0':raise ValueError('invalid line')
            cl=tuple(int(x) for x in raw[:3])
            if len(set(map(abs,cl)))!=3:return
            yield cl
    # One scan per variable checks signed degree, and also ensures all source
    # names are inside the expected header range.
    for v in range(1,n+1):
        cp=cn=0;total=0
        for c in scan():
            if any(abs(l)>n for l in c):return ('INVALID',None)
            for l in c:
                if l==v:cp+=1
                if l==-v:cn+=1
            total+=1
        if total!=ms or cp!=2 or cn!=2:return ('INVALID',None)
    # Duplicated clauses are forbidden in the strict source class. Use only
    # two current clauses and scans; this adds O(nN) input-head steps.
    for i,ci in enumerate(scan()):
        if any(tuple(sorted(ci))==tuple(sorted(cj)) for j,cj in enumerate(scan()) if j<i):
            return ('INVALID',None)
    acc=[1,2,4,8];total_found=0
    # Scope multiplicity check: every actual source clause belongs to exactly
    # one block (the double-scope clauses belong to the same block).
    for j in range(n//3):
        scopes=scopes_by_block(n,j)
        clauses=[];count=C()
        for cl in scan():
            scope=frozenset(map(abs,cl))
            if scope in scopes:
                clauses.append(cl);count[scope]+=1
        if any(count[s]!=c for s,c in zip(scopes,(2,1,1))):return ('INVALID',None)
        total_found+=len(clauses)
        m=transfer_for_block(clauses,n,j,stats)
        acc=bool_mult(acc,m,stats)
    if total_found!=ms:return ('INVALID',None)
    return 'SAT' if trace_positive(acc) else 'UNSAT',None

def boundary_table_solver(source,h,stats):
    res,matrices=material_solver(source,stats)
    if res=='INVALID':return ('INVALID',None)
    n=len(matrices)*3
    if n%(3*h):return ('INVALID',None)
    a=n//(3*h)
    parts=[]
    for j in range(h):
        m=[1,2,4,8]
        for k in range(a):m=bool_mult(m,matrices[j*a+k],stats)
        parts.append(m)
    table=bytearray(4**h)
    any_yes=False
    for boundary in range(4**h):
        stats['table_rows_tested']+=1
        # groups are two-bit boundary states
        states=[(boundary>>(2*j))&3 for j in range(h)]
        accepted=all(parts[j][states[j]]&(1<<states[(j+1)%h]) for j in range(h))
        if accepted:
            table[boundary]=1;any_yes=True
    stats['table_allocated_bytes']=len(table)
    stats['table_nnz']=sum(table)
    return ('SAT' if any_yes else 'UNSAT'),parts

def static_certificate(cs,a,h):
    n=3*a*h
    Y=set();mods=[]
    for j in range(h):
        p=3*a*j
        Y.update((p+1,p+2))
        mods.append(set(range(p+3,p+3*a+1)))
    assert len(Y)==2*h and all(len(z)==3*a-2 for z in mods)
    # No clause contains private names from different modules.
    touched=C()
    for cl in cs:
        S=set(map(abs,cl));indexes=[j for j,z in enumerate(mods) if z&S]
        assert len(indexes)<=1,(cl,indexes)
        for j in indexes:touched[j]+=1
    q=a-1
    Bs=[]
    for j,z in enumerate(mods):
        p=3*a*j
        B={p+3*r+1 for r in range(1,a)} # zero-based rel 3,6,... -> var names p+4,...
        assert B<=z
        Bs.append(B)
    H=Y|set().union(*Bs)
    assert all(any(abs(l) in H for l in cl) for cl in cs)
    # A separate collection of a-1 disjoint private all-negative blocks D_j
    # is within module j, therefore q>=a-1 for each j.
    for j,z in enumerate(mods):
        p=3*a*j
        for r in range(1,a):
            triple={p+3*r+1,p+3*r+2,p+3*r+3}
            assert triple<=z
            assert tuple(-v for v in sorted(triple)) in cs
    return dict(n=n,m=len(cs),a=a,h=h,k=h,b=2*h,q=q,global_hitting=len(H),
                decomposition_certified=True,full_boundary=list(sorted(Y)),
                private_sizes=list(map(len,mods)),module_B=list(map(lambda x:sorted(x),Bs)))

def min_hitting_brute(cs,private):
    scoped=[set(map(abs,cl)) for cl in cs if set(map(abs,cl))<=private]
    names=sorted(private)
    for q in range(len(names)+1):
        for combo in itertools.combinations(names,q):
            hit=set(combo)
            if all(sc&hit for sc in scoped):return q
    raise AssertionError('missing hitting set')

def signed_flip(cs,mask):
    return [tuple(-l if (mask>>(abs(l)-1))&1 else l for l in cl) for cl in cs]

def dpll(cs,n,maxnodes=1000000):
    nodes=0
    def go(assignment):
        nonlocal nodes
        nodes+=1
        if nodes>maxnodes:raise RuntimeError('node budget')
        for c in cs:
            if any(assignment.get(abs(l))==int(l>0) for l in c):continue
            if all(abs(l) in assignment for l in c):return None
        if len(assignment)==n:return assignment
        v=next(i for i in range(1,n+1) if i not in assignment)
        for val in (0,1):
            assignment[v]=val
            got=go(assignment)
            if got is not None:return got
            del assignment[v]
        return None
    sol=go({})
    return (('SAT' if sol is not None else 'UNSAT'),nodes)

def bve_pivot(cs,n,pivot):
    pos=[cl for cl in cs if pivot in cl]
    neg=[cl for cl in cs if -pivot in cl]
    others=[cl for cl in cs if pivot not in cl and -pivot not in cl]
    rs=[]
    for cp in pos:
        for cn in neg:
            rem=tuple(x for x in cp if x!=pivot)+tuple(x for x in cn if x!=-pivot)
            if any(-x in rem for x in rem):continue
            r=tuple(sorted(set(rem)))
            if r not in rs:rs.append(r)
    return dict(pivot=pivot,pos=len(pos),neg=len(neg),resolvents=len(rs),
                max_width=max(map(len,rs),default=0),
                remaining_clauses=len(others)+len(rs),
                source_bytes=len(dimacs(cs)),
                descendant_bytes=len(dimacs(others+rs)) if (others or rs) else 0,
                descendant_not_exact22=True)

# Fixed exact22 AND-connector from CONNECTOR231; the relevant 15-bit gate
# and 16 abstract truth-table checks are reproduced here.
def local_gate_table():
    table={};good=[mask for mask in range(1<<15)
                   if all(eval_mask_cl(cl,mask) for j,cl in enumerate(G) if j not in (D,E))]
    for x,A in itertools.product((0,1),repeat=2):
        options=set()
        for mask in good:
            p=(mask>>3)&1
            B=int(eval_mask_cl((-9,-11),mask))
            if (not x or B) and (A or not p):
                u=int(eval_mask_cl((-8,),mask))
                v=int(eval_mask_cl((-4,-11),mask))
                options.add((u,v))
        table[(x,A)]=options
    expect={(0,0):{(0,1)},(0,1):set(itertools.product((0,1),repeat=2)),
            (1,0):set(),(1,1):{(0,0),(1,0),(1,1)}}
    assert table==expect
    for x,A,y,B in itertools.product((0,1),repeat=4):
        linked=any((v1 or u2) and (v2 or u1)
                   for u1,v1 in table[(x,A)] for u2,v2 in table[(y,B)])
        assert linked==bool((not x or A) and (not y or B))
    return {'guard_nonpunctured_models':len(good),'abstract_gate_cases':16}

def shift(cs,delta):return [tuple((1 if l>0 else -1)*(abs(l)+delta) for l in cl) for cl in cs]

def join(H,K):
    nh,mh=validate_exact22(H);nk,mk=validate_exact22(K)
    h=H.copy();k=shift(K,nh)
    def negative_slot(cs):
        return next((j,t,abs(l)) for j,c in enumerate(cs)
                    for t,l in enumerate(c) if l<0)
    ix,sx,x=negative_slot(h);iy,sy,y=negative_slot(k)
    b1=nh+nk;b2=b1+15
    g1=shift(G,b1);g2=shift(G,b2)
    p1=b1+4;p2=b2+4
    h[ix]=tuple(-p1 if t==sx else l for t,l in enumerate(h[ix]))
    k[iy]=tuple(-p2 if t==sy else l for t,l in enumerate(k[iy]))
    g1[D]=tuple(-x if t==0 else l for t,l in enumerate(g1[D]))
    g2[D]=tuple(-y if t==0 else l for t,l in enumerate(g2[D]))
    u1=b1+8;u2=b2+8
    g1[E]=tuple(-u2 if t==1 else l for t,l in enumerate(g1[E]))
    g2[E]=tuple(-u1 if t==1 else l for t,l in enumerate(g2[E]))
    out=h+k+g1+g2
    assert validate_exact22(out)==(nh+nk+30,mh+mk+40)
    return out

def exact22_xor_triple(start,parity):
    vars=(start+1,start+2,start+3)
    clauses=[]
    for vals in itertools.product((0,1),repeat=3):
        if vals[0]^vals[1]^vals[2]!=parity:
            clauses.append(tuple(v if bit==0 else -v for v,bit in zip(vars,vals)))
    assert len(clauses)==4
    return clauses

def xor_joined(m,label='SAT'):
    if m<2:raise ValueError('need >=2 to test connectivity across gadgets')
    out=exact22_xor_triple(0,0)
    for j in range(1,m):out=join(out,exact22_xor_triple(0,j%2))
    out=join(out,V if label=='SAT' else W1)
    return out

def gaussian_affine_rank(rows,n):
    basis={};rhs={};row_ops=0
    for vars,b in rows:
        mask=0
        for v in vars:mask^=1<<(v-1)
        while mask:
            p=mask.bit_length()-1;row_ops+=1
            if p not in basis:basis[p]=mask;rhs[p]=b;break
            mask^=basis[p];b^=rhs[p]
        if not mask and b:return False,len(basis),row_ops
    return True,len(basis),row_ops

def measured(function,source,*args):
    stats=C();tracemalloc.start();t=time.perf_counter()
    answer,aux=function(source,*args,stats) if function==boundary_table_solver else function(source,stats)
    elapsed=time.perf_counter()-t
    _cur,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    return {'answer':answer,'elapsed_s':round(elapsed,6),
            'traced_peak_bytes':peak,'input_bytes':len(source),
            'total_input_plus_traced_peak_bytes':len(source)+peak,
            'stats':dict(stats)}

def uniform_material_entry(source,stats):return material_solver(source,stats)

def uniform_stream_entry(source,stats):return stream_solver(source,stats)

def main():
    raw={'report':'REALIZABLE_TRANSFER_FRONTIER233','run_utc':'2026-10-29T22:14:00Z',
         'python_model':'CPython; wall time plus tracemalloc allocation proxy; not a TM bound',
         'semiring':'Boolean matrix multiplication; GF2 matrix ranks explicitly separated',
         'tests':{},'measurements':[]}
    M=[1,15,15,11]
    M2=bool_mult(M,M);M3=bool_mult(M2,M)
    assert M2==[1,15,15,15] and M3==M2
    raw['transfer']={'one_block_rows':M,'two_block_rows':M2,
                     'three_block_rows':M3,'M1_gf2_rank':gfrank(M),
                     'M2_gf2_rank':gfrank(M2),
                     'M2_true_entries':sum(x.bit_count() for x in M2)}
    # Check transfer against direct quantified CNF for a<=5, using h=2.
    direct_checks=0
    for a in range(1,6):
        n=6*a;cs=cyclic(n)
        assert validate_exact22(cs)==(n,4*n//3)
        assert validate_scopes(cs,n)
        for j in range(n//3):
            expected=scopes_by_block(n,j)
            block=[cl for cl in cs if frozenset(map(abs,cl)) in expected]
            assert len(block)==4 and transfer_for_block(block,n,j)==M
        # for this module fix both boundary pairs and brute the private assignments
        # only up to a=5 (13 private bits), exactly 16*8192 valuations.
        private=list(range(3,3*a+1));bdry=[1,2,3*a+1,3*a+2]
        target=[cl for cl in cs if set(map(abs,cl))&set(private)]
        for u,v in itertools.product(range(4),repeat=2):
            bassign={bdry[k]:((u>>k)&1) for k in range(2)}|{
                bdry[k+2]:((v>>k)&1) for k in range(2)}
            exists=False
            for mid in range(1<<len(private)):
                ass=bassign|{p:(mid>>j)&1 for j,p in enumerate(private)}
                if all(evaluate_clause(cl,ass) for cl in target):exists=True;break
            assert exists==bool(bool_pow(M,a)[u]&(1<<v))
            direct_checks+=1
    raw['tests']['direct_local_projection_pairs']=direct_checks
    # Static certificates all exact22 and both sign-label joins.
    a_h=[(1,4),(2,4),(3,4),(4,3),(6,4),(8,4),(12,4),(24,2),(16,3)]
    static=[];exhaustive_hitting=[]
    for a,h in a_h:
        n=3*a*h;cs=cyclic(n)
        static.append({k:v for k,v in static_certificate(cs,a,h).items()
                       if k not in ('full_boundary','private_sizes','module_B')})
        if a<=4:
            z=set(range(3,3*a+1)); qtrue=min_hitting_brute(cs,z)
            assert qtrue==a-1
            exhaustive_hitting.append({'a':a,'h':h,'minimum_q':qtrue})
    raw['tests']['static']=static
    raw['tests']['exact_hitting_exhaustive']=exhaustive_hitting
    # Every source signed quota retained by complementation of arbitrary names.
    for n in (12,24,48):
        cs=cyclic(n)
        for bitmask in (0,1,3,5,12,(1<<n)-1):
            transformed=signed_flip(cs,bitmask)
            assert validate_exact22(transformed)==(n,4*n//3)
            txt=dimacs(transformed)
            r0=material_solver(txt,C())[0];r1=stream_solver(txt,C())[0]
            assert r0==r1=='SAT'
    raw['tests']['gauge_paired_comparisons']=3*6
    # A single fixed correct program on signed scope grammar: test 4 equal-n
    # cases with both algorithms and, at smaller n, generic branching.
    for a,h in ((2,4),(3,4),(4,4),(6,4),(12,4),(12,2),(6,8)):
        n=3*a*h;source=dimacs(cyclic(n))
        for method,fun in (('material',uniform_material_entry),('stream',uniform_stream_entry)):
            obs=measured(fun,source)
            raw['measurements'].append({'family':'cyclic','a':a,'h':h,'n':n,
                                        'b':2*h,'q':a-1,'method':method,**obs})
        if h<=8:
            obs=measured(boundary_table_solver,source,h)
            raw['measurements'].append({'family':'cyclic','a':a,'h':h,'n':n,
                                        'b':2*h,'q':a-1,'method':'table',**obs})
        if n<=36:
            parsed=from_dimacs(source)
            t=time.perf_counter();branch_status,nodes=dpll(parsed[1],n)
            raw['measurements'].append({'family':'cyclic','a':a,'h':h,'n':n,
                                        'b':2*h,'q':a-1,'method':'branch',
                                        'answer':branch_status,'elapsed_s':round(time.perf_counter()-t,6),
                                        'nodes':nodes,'input_bytes':len(source)})
    # Same-input, changing only partition h: n=144; actual table vs stream crossing.
    n=144;source=dimacs(cyclic(n))
    for h in (2,3,4,6,8):
        a=n//(3*h)
        obs=measured(boundary_table_solver,source,h)
        raw['measurements'].append({'family':'same_n144','a':a,'h':h,'n':n,
                                    'b':2*h,'q':a-1,'method':'table',**obs})
    raw['measurements'].append({'family':'same_n144','a':None,'h':None,'n':n,
                                'b':None,'q':None,'method':'stream',**measured(uniform_stream_entry,source)})
    raw['measurements'].append({'family':'same_n144','a':None,'h':None,'n':n,
                                'b':None,'q':None,'method':'material',**measured(uniform_material_entry,source)})
    # Three repeats on EXACT SAME physical n=144 input. Each reported (time,peak)
    # pair is from its own complete run, never the cross-input min of two runs.
    repeat_rows=[]
    for repeat in range(3):
        for method,fun,h in [('material',uniform_material_entry,None),
                             ('stream',uniform_stream_entry,None)]+[
                                 ('table',boundary_table_solver,x) for x in (2,3,4,6,8)]:
            obs=measured(fun,source,h) if method=='table' else measured(fun,source)
            repeat_rows.append({'repeat':repeat,'method':method,'h':h,
                                'b':None if h is None else 2*h,
                                'time_s':obs['elapsed_s'],
                                'peak_traced_bytes':obs['traced_peak_bytes'],
                                'input_bytes':obs['input_bytes'],
                                'answer':obs['answer']})
    raw['tests']['same_source_timing_repeats']=repeat_rows
    medians=[]
    for method,h in [('material',None),('stream',None)]+[('table',i) for i in (2,3,4,6,8)]:
        dat=[z for z in repeat_rows if z['method']==method and z['h']==h]
        medians.append({'method':method,'h':h,'b':None if h is None else 2*h,
                        'median_time_s':statistics.median(x['time_s'] for x in dat),
                        'median_peak_traced_bytes':statistics.median(x['peak_traced_bytes'] for x in dat),
                        'time_range_s':[min(x['time_s'] for x in dat),
                                        max(x['time_s'] for x in dat)]})
    raw['tests']['same_source_timing_medians']=medians
    # BVE cannot be claimed exact22; do only explicitly selected signed pivots.
    raw['tests']['bve']=[dict(n=n,**bve_pivot(cyclic(n),n,p)) for n in (24,144) for p in (1,2,3)]
    # n=1200 exact parameter grid (do not materialize exponential tables).
    n=1200;divisors=[h for h in range(2,n//3+1) if (n//3)%h==0]
    grid=[]
    for h in divisors:
        a=(n//3)//h;b=2*h;q=a-1
        grid.append(dict(h=h,a=a,b=b,q=q,t_exp=b+q,s_exp=b,
                         source_n=n,table_bits_exponent=b,
                         status='REALIZABLE STATIC, proxy only'))
    best=min(x['t_exp'] for x in grid)
    raw['proxies']={'n':n,'integer_realizable_grid':grid,
                    'best_static_proxy_t_exp':best,
                    'minimizers':[x for x in grid if x['t_exp']==best],
                    'continuous_bstar':math.sqrt(2*n/3),
                    'continuous_tstar':2*math.sqrt(2*n/3)-1,
                    'first_equal_log_proxies':{'b':2*n//3,'q':0,'a':1,'h':n//3},
                    'generic_relaxed_tstar':math.sqrt(n/3)-0.25}
    # Join fixed 15-var SAT/UNSAT controls to exact22 cyclic carriers.
    gstats=local_gate_table();wcnt,wmodel=fixed_models(W1,15);vcnt,vmodel=fixed_models(V,15)
    assert wcnt==0 and vcnt==54
    gstats.update({'W1_models':wcnt,'V_models':vcnt,'V_first_model':vmodel})
    raw['tests']['fixed_guard']=gstats
    linked=[]
    for a,h in ((2,2),(3,2),(4,3),(6,4)):
        n=3*a*h;base=cyclic(n)
        for label,core in (('SAT',V),('UNSAT',W1)):
            joint=join(base,core)
            totaln,totalm=validate_exact22(joint)
            assert totaln==n+45 and totalm==4*n//3+60
            orig=static_certificate(base,a,h)
            # Treat all 45 auxiliary-and-fixed-core names as global boundary.
            Y=set(orig['full_boundary'])|set(range(n+1,n+46))
            bs=[set(z) for z in orig['module_B']]
            zmods=[]
            for j in range(h):
                p=3*a*j
                zmods.append(set(range(p+3,p+3*a+1)))
            assert all(len({j for j,z in enumerate(zmods)
                            if set(map(abs,c))&z})<=1 for c in joint)
            assert all(set(map(abs,c))&(Y|set().union(*bs)) for c in joint)
            linked.append({'a':a,'h':h,'n':totaln,'m':totalm,
                           'label_by_exact_guard_and_fixed_core':label,
                           'b':2*h+45,'q':a-1,'k':h,'source_bits':8*len(dimacs(joint)),
                           'source_sha256':hashlib.sha256(dimacs(joint).encode()).hexdigest()})
    raw['tests']['joined_opposite_labels']=linked
    # Connected exact22 XOR carriers: true projected codimension rank grows
    # even though Gaussian elimination on this recognized affine core is P.
    xrows=[]
    for m in (2,4,8):
        cs=xor_joined(m,'SAT');nn,mm=validate_exact22(cs)
        rows=[((3*i+1,3*i+2,3*i+3),i%2) for i in range(m)]
        g_ok,rank,ops=gaussian_affine_rank(rows,3*m)
        assert g_ok and rank==m and nn==33*m+15
        # Identical known guard and XOR carrier with opposite fixed-core label.
        cu=xor_joined(m,'UNSAT');assert validate_exact22(cu)==(nn,mm)
        xrows.append({'xor_gadgets':m,'connected_variables':nn,'clauses':mm,
                      'projected_affine_codimension_e':rank,
                      'gaussian_pivot_ops':ops,'SAT_plus_core':'SAT',
                      'UNSAT_plus_core':'UNSAT',
                      'labels_certified_by_gate_truth_table_and_W1_enumeration':True})
    raw['tests']['connected_xor_controls']=xrows
    raw['tests']['all_assertions_passed']=True
    print(json.dumps(raw,indent=2,sort_keys=True))

if __name__=='__main__':main()