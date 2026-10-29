#!/usr/bin/env python3
"""LSPV-2 TWO-SWAP-EXACT-PORT-TRANSPORT223 (stdlib, deterministic).

Build an arbitrary-source strict signed exact-(2,2)-3CNF 2-swap port equality
transport. Verify the 15-variable guard by full 2^15 enumeration and test
actual connected joined formulas independently by DPLL. The script does NOT
solve arbitrary SAT efficiently and makes no P-vs-NP claim.
"""
from __future__ import annotations
import collections, hashlib, itertools, json

W1 = ((-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14))


def canon(C):
    return tuple(sorted(tuple(sorted(clause, key=lambda l:(abs(l),l<0))) for clause in C))


def guard():
    C=[list(c) for c in W1]
    for j in (6,11): C[j][0] *= -1
    return canon(C)


def affine(p):
    assert p>=5 and p%2
    def v(g,i): return g*p+(i%p)+1
    C=[]
    for s in range(4):
        for i in range(p):
            a,b,c=v(0,i),v(1,i+s),v(2,i+2*s)
            C.append((-a if s in (0,1) else a,
                      -b if s in (2,3) else b,
                      -c if s in (0,2) else c))
    return canon(C)


def is_strict_connected(C,n):
    if len(C)*3!=4*n or len(C)!=len(set(C)): return False
    counts=collections.Counter(l for c in C for l in c)
    if any(counts[v]!=2 or counts[-v]!=2 for v in range(1,n+1)): return False
    graph=[set() for _ in range(n+len(C)+1)]
    for j,c in enumerate(C):
        if len(c)!=3 or any(not 1<=abs(l)<=n for l in c): return False
        if len({abs(l) for l in c})!=3:return False
        for l in c:
            graph[abs(l)].add(n+j+1);graph[n+j+1].add(abs(l))
    seen={1};todo=[1]
    while todo:
        for nxt in graph[todo.pop()]:
            if nxt not in seen: seen.add(nxt);todo.append(nxt)
    return len(seen)==n+len(C)


def dimacs(C,n):
    return ('p cnf %d %d\n'%(n,len(C))+''.join(' '.join(map(str,c))+' 0\n' for c in C)).encode('ascii')


def parse_canonical(data):
    try: s=data.decode('ascii')
    except (UnicodeError,AttributeError) as exc: raise ValueError('nonascii') from exc
    lines=s.splitlines(keepends=True)
    if not lines or any(not z.endswith('\n') for z in lines): raise ValueError('bad lines')
    head=lines[0].split()
    if len(head)!=4 or head[:2]!=['p','cnf']: raise ValueError('header')
    try: n,m=int(head[2]),int(head[3])
    except ValueError as exc:raise ValueError('header ints') from exc
    if n<1 or m<1 or len(lines)!=m+1:raise ValueError('header mismatch')
    C=[]
    for row in lines[1:]:
        tok=row.split()
        if len(tok)!=4 or tok[-1]!='0': raise ValueError('not proper ternary')
        try:C.append(tuple(int(q) for q in tok[:3]))
        except ValueError as exc:raise ValueError('literal token') from exc
    C=canon(C)
    if not is_strict_connected(C,n) or dimacs(C,n)!=data:raise ValueError('noncanonical or invalid')
    return C,n


def guard_without_edges_connected(G,port=4,slots=(15,2)):
    graph={}
    for j,c in enumerate(G):
        key=('clause',j);graph.setdefault(key,set())
        for l in c:
            if j in slots and abs(l)==port:continue
            v=('variable',abs(l));graph.setdefault(v,set());graph[key].add(v);graph[v].add(key)
    seen={('variable',port)};todo=list(seen)
    while todo:
        for v in graph[todo.pop()]:
            if v not in seen:seen.add(v);todo.append(v)
    return len(seen)==len(graph),len(seen),len(graph)


def guard_puncture():
    G=guard(); assert is_strict_connected(G,15)
    assert G[15]==(4,8,-10) and G[2]==(-4,-9,-11)
    mask_count=collections.Counter();witness={}
    remaining=[c for j,c in enumerate(G) if j not in (15,2)]
    for mask in range(1<<15):
        if all(any(bool(mask>>(abs(l)-1)&1)==(l>0) for l in clause) for clause in remaining):
            p=(mask>>3)&1
            a=int(bool(mask>>(8-1)&1) or not bool(mask>>(10-1)&1))
            b=int(not bool(mask>>(9-1)&1) or not bool(mask>>(11-1)&1))
            mask_count[(p,a,b)]+=1
            witness.setdefault((p,a,b),mask)
    expected={(0,0,0):85,(0,1,0):153,(1,0,0):85,(1,0,1):119}
    assert dict(mask_count)==expected,mask_count
    assert all(not(p==0 and b==1) and not(p==1 and a==1) for p,a,b in mask_count)
    # G original has models at p=0 and p=1, both necessary for exact cofactor preservation.
    assert any(p==0 and a==1 for p,a,b in mask_count)
    assert any(p==1 and b==1 for p,a,b in mask_count)
    # Independent DPLL refutations for the two disallowed fibers, split at the
    # two foot literals. These calls are on the fixed 15-variable gadget only.
    bad_pins=({4:True,8:True},{4:True,10:False},
              {4:False,9:False},{4:False,11:False})
    independent=[]
    for pins in bad_pins:
        sol,calls=dpll(remaining,pins)
        assert sol is None
        independent.append({'pins':{str(i):int(v) for i,v in sorted(pins.items())},
                            'dpll_calls':calls,'unsat':True})
    ok,seen,size=guard_without_edges_connected(G)
    assert ok and seen==size==35
    return {'checked_assignments':32768,'independent_guard_refutations':independent,'puncture_counts':{''.join(map(str,k)):v for k,v in sorted(mask_count.items())},
            'first_witnesses':{''.join(map(str,k)):witness[k] for k in sorted(witness)},
            'guard_connected_after_deleting_two_selected_p_edges':ok,
            'source_pivot':4,'selected_g_positive':15,'selected_g_negative':2}


def splice2(H,n,x,pos_slot=None,neg_slot=None):
    """One positive and one negative cross swap, no SAT/cofactor oracle."""
    assert is_strict_connected(H,n) and 1<=x<=n
    if pos_slot is None: pos_slot=next(j for j,c in enumerate(H) if x in c)
    if neg_slot is None: neg_slot=next(j for j,c in enumerate(H) if -x in c)
    assert pos_slot!=neg_slot and x in H[pos_slot] and -x in H[neg_slot]
    p=n+4
    new_H=[list(c) for c in H]
    new_H[pos_slot][new_H[pos_slot].index(x)]=p
    new_H[neg_slot][new_H[neg_slot].index(-x)]=-p
    new_G=[[l+n if l>0 else l-n for l in c] for c in guard()]
    assert p in new_G[15] and -p in new_G[2]
    new_G[15][new_G[15].index(p)]=x
    new_G[2][new_G[2].index(-p)]=-x
    F=canon(new_H+new_G)
    assert is_strict_connected(F,n+15)
    return F,p,(pos_slot,neg_slot)


def dpll(C,pins=None):
    pins={} if pins is None else dict(pins)
    calls=[0]
    def recur(A,cls):
        calls[0]+=1
        while True:
            rem=[];units=[]
            for c in cls:
                if any(abs(l) in A and A[abs(l)]==(l>0) for l in c):continue
                live=[l for l in c if abs(l) not in A]
                if not live:return None
                rem.append(tuple(live))
                if len(live)==1:units.append(live[0])
            if not rem:return A
            if not units:break
            for l in units:
                v=abs(l);b=l>0
                if v in A and A[v]!=b:return None
                A[v]=b
        freq=collections.Counter(abs(l) for c in rem for l in c)
        v=max(freq,key=lambda x:(freq[x],-x))
        for b in (False,True):
            V=dict(A);V[v]=b
            ret=recur(V,rem)
            if ret is not None:return ret
        return None
    ret=recur(pins,C)
    if ret is not None:
        for c in C:
            for l in c: ret.setdefault(abs(l),False)
        assert all(any(ret[abs(l)]==(l>0) for l in c) for c in C)
    return ret,calls[0]


def n3_sources():
    L=[]
    for bits in itertools.product((False,True),repeat=3):
        L.append(tuple(i+1 if b else -(i+1) for i,b in enumerate(bits)))
    for quartet in itertools.combinations(L,4):
        C=canon(quartet)
        if is_strict_connected(C,3):yield C


def cofactor_test(H,n,x,name):
    assert parse_canonical(dimacs(H,n))==(H,n)
    F,p,slots=splice2(H,n,x)
    source=[];joined=[];calls=0
    for xv in (0,1):
        A,c=dpll(H,{x:bool(xv)});calls+=c
        source.append(A is not None)
        for pv in (0,1):
            B,c=dpll(F,{x:bool(xv),p:bool(pv)});calls+=c
            joined.append(int(B is not None))
            assert bool(B) == ((xv==pv) and (A is not None)),(name,xv,pv)
    parent=8*len(dimacs(H,n));child=8*len(dimacs(F,n+15))
    assert child>parent
    return {'case':name,'variables':n,'clauses':len(H),'x':x,'source_cofactors':list(map(int,source)),
            'joined_cofactors_00_01_10_11':joined,'parent_bits':parent,'child_bits':child,
            'additional_bits':child-parent,'DPLL_calls':calls,'slots':slots,
            'source_sha256':hashlib.sha256(dimacs(H,n)).hexdigest(),
            'child_sha256':hashlib.sha256(dimacs(F,n+15)).hexdigest()}


def adverse_pair():
    # Same H, but wrong G feet (positive at 15, negative at 3) leaves false off diagonal fiber.
    H=affine(5);n=15;x=1;G=guard();p=n+4
    h_pos=next(j for j,c in enumerate(H) if x in c)
    h_neg=next(j for j,c in enumerate(H) if -x in c)
    A=[list(c) for c in H];B=[[l+n if l>0 else l-n for l in c] for c in G]
    for i,j,lit in ((h_pos,15,x),(h_neg,3,-x)):
        incoming=p if lit>0 else -p
        A[i][A[i].index(lit)]=incoming
        B[j][B[j].index(incoming)]=lit
    F=canon(A+B);assert is_strict_connected(F,n+15)
    relation={}
    for xv,pv in itertools.product((0,1),repeat=2):
        A,_=dpll(F,{x:bool(xv),p:bool(pv)})
        relation[f'{xv}{pv}']=A is not None
    assert relation=={'00':True,'01':True,'10':True,'11':True}
    return {'wrong_negative_slot':3,'wrong_pair_relation':relation,'interpretation':'paired signed quota alone does not imply equality'}


def main():
    out={'run':'TWO-SWAP-EXACT-PORT-TRANSPORT223','status':'PASS','seed':None,
         'source_code':'Python stdlib explicit finite enumeration and DPLL',
         'guard':guard_puncture(),'negative_control':adverse_pair(),
         'cases':[],'parser_bad_controls':0}
    src3=list(n3_sources())
    assert len(src3)==8, len(src3)
    for i,H in enumerate(src3):out['cases'].append(cofactor_test(H,3,1,f'n3-exact22-{i}'))
    out['cases'].append(cofactor_test(canon(W1),15,4,'W1-UNSAT'))
    out['cases'].append(cofactor_test(guard(),15,4,'G-SAT'))
    for p in (5,7):
        H=affine(p)
        out['cases'].append(cofactor_test(H,3*p,1,f'R_{p}-SAT'))
        if p==5:
            # Verify all four choices of source pos/neg slots on same source.
            for a in [j for j,c in enumerate(H) if 1 in c]:
                for b in [j for j,c in enumerate(H) if -1 in c]:
                    F,port,_=splice2(H,15,1,a,b)
                    for xv,pv in itertools.product((0,1),repeat=2):
                        sol,_=dpll(F,{1:bool(xv),port:bool(pv)})
                        assert bool(sol)==(xv==pv)
    # Larger physical controls only; arbitrary SAT oracle calls are NOT charged free.
    out['physical_only']=[]
    for p in (31,101,501):
        H=affine(p);F,pvar,slots=splice2(H,3*p,1)
        out['physical_only'].append({'p':p,'source_bits':8*len(dimacs(H,3*p)),
            'spliced_bits':8*len(dimacs(F,3*p+15)),'slots':slots})
    # Actual two-step closure on tiny n=3. Two recursive children each validated.
    H=src3[0];F,p,_=splice2(H,3,1)
    F2,p2,_=splice2(F,18,p)
    for x,p1,pnew in itertools.product((0,1),repeat=3):
        w,_=dpll(F2,{1:bool(x),p:bool(p1),p2:bool(pnew)})
        assert bool(w)==(x==p1==pnew)
    out['two_step_closure']={'source_n':3,'middle_n':18,'last_n':33,
                              'source_bits':8*len(dimacs(H,3)),
                              'middle_bits':8*len(dimacs(F,18)),
                              'last_bits':8*len(dimacs(F2,33)),
                              'joint_three_port_tests':8}
    good=dimacs(guard(),15)
    for wrong in (b'q'+good[1:], good[:-1],good+b'0\n',good.replace(b'p cnf',b'p abc',1),good.replace(b' 0\n',b' 0 0\n',1)):
        try:parse_canonical(wrong)
        except ValueError:out['parser_bad_controls']+=1
        else:raise AssertionError('malformed accepted')
    out['case_count']=len(out['cases'])
    out['independently_solved_cofactors']=4*len(out['cases'])
    out['all_source_unsigned_degree_controls']=True
    out['limitations']=[
        'The transport grows physical CNF size by Theta(log N), not a SAT shrink.',
        'The exact G puncture table is an exhaustive finite verified computation, not a kernel-certified theorem.',
        'All-source correctness is conditional on proper strict signed exact-(2,2) source validation.',
        'There is no arbitrary ordinary-SAT-to-exact22 port compiler, no uniform SAT contraction, no SAT runtime lower bound.',
        'The two-step test is a correctness control, not a polynomial-value descending rank.']
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()