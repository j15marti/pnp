#!/usr/bin/env python3
"""ARC-PROVENANCE-RECONVERGENCE135: standard-library finite audit.

This script tests a narrowly scoped source-offset provenance obstruction.
It does NOT measure FLMV Turing-machine resources or prove SAT runtime LBs.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

SEED = 'none; exhaustive deterministic'


def build(k, force_unsat=False):
    assert k >= 1
    n = 3*k + (3 if force_unsat else 0)
    clauses = []
    for i in range(1, k+1):
        a,b=k+i,2*k+i
        clauses.append((i,a,b))
        clauses.append((-i,a,b))
    if force_unsat:
        y,z,w=3*k+1,3*k+2,3*k+3
        for signs in itertools.product((-1,1),repeat=3):
            clauses.append((signs[0]*y,signs[1]*z,signs[2]*w))
    assert len(set(clauses))==len(clauses)
    assert all(len({abs(x) for x in c})==3 for c in clauses)
    txt=f'p cnf {n} {len(clauses)}\n'
    offsets=[]
    for c in clauses:
        offsets.append(len(txt.encode('ascii')))
        txt+=' '.join(map(str,c))+' 0\n'
    return n,clauses,offsets,txt


def parse_source(txt):
    raw=txt.encode('ascii')
    lines=raw.splitlines(keepends=True)
    assert lines and lines[0].startswith(b'p cnf ')
    head=lines[0].decode().split()
    assert len(head)==4 and head[:2]==['p','cnf']
    n,m=map(int,head[2:]); assert m==len(lines)-1
    pos=len(lines[0]); offsets=[]; clauses=[]
    for line in lines[1:]:
        assert line.endswith(b'\n')
        cells=list(map(int,line.decode().strip().split()))
        assert cells[-1]==0 and len(cells)==4
        c=tuple(cells[:-1]); assert all(0<abs(l)<=n for l in c)
        assert len(set(map(abs,c)))==3
        offsets.append(pos);clauses.append(c);pos+=len(line)
    assert pos==len(raw)
    return n,clauses,offsets


def residual_and_origins(clauses, offsets, assignment, k):
    residual=[]; origins=[]; payload={}
    for c,off in zip(clauses,offsets):
        satisfied=False; keep=[]
        for lit in c:
            if abs(lit) in assignment:
                value=assignment[abs(lit)]
                if (lit>0 and value) or (lit<0 and not value):
                    satisfied=True; break
            else: keep.append(lit)
        if not satisfied:
            residual.append(tuple(keep));origins.append(off)
            for i in range(1,k+1):
                if tuple(keep)==(k+i,2*k+i):
                    assert i not in payload
                    payload[i]=off
    assert len(payload)==k
    # Canonical normalized residual disregards physical source provenance.
    return tuple(sorted(residual)),tuple(payload[i] for i in range(1,k+1))


def interleaved_verifier(source, selector_bits, claimed_offsets, k):
    """Reference one-pass ordered source/proof reader with no origin table.

    Maintains only a current physical source offset, a single selector bit,
    one expected source offset, and counters.  A TM implementation can read
    the two adjacent source clause lines directly as it advances.
    """
    lines=source.encode('ascii').splitlines(keepends=True)
    if not lines or not lines[0].startswith(b'p cnf '):return False
    if len(selector_bits)!=k or len(claimed_offsets)!=k:return False
    current_offset=len(lines[0])
    if len(lines)<1+2*k:return False
    for i in range(k):
        positive=lines[1+2*i]
        negative=lines[2+2*i]
        plus_offset=current_offset
        minus_offset=current_offset+len(positive)
        # Canonical syntax is authenticated against the two physical lines.
        expected_plus=(i+1,k+i+1,2*k+i+1)
        expected_minus=(-(i+1),k+i+1,2*k+i+1)
        try:
            parsed_plus=tuple(map(int,positive.decode().split()))
            parsed_minus=tuple(map(int,negative.decode().split()))
        except ValueError:return False
        if parsed_plus!=(*expected_plus,0) or parsed_minus!=(*expected_minus,0):return False
        bit=selector_bits[i]
        if bit not in (0,1):return False
        expected=plus_offset if bit==0 else minus_offset
        if claimed_offsets[i]!=expected:return False
        current_offset+=len(positive)+len(negative)
    return True

def dpll(clauses, assignment=None):
    if assignment is None: assignment={}
    simplified=[]
    for c in clauses:
        rest=[];sat=False
        for lit in c:
            v=abs(lit)
            if v in assignment:
                if assignment[v]==(lit>0):sat=True;break
            else:rest.append(lit)
        if sat:continue
        if not rest:return False
        simplified.append(tuple(rest))
    if not simplified:return True
    unit=next((c[0] for c in simplified if len(c)==1),None)
    if unit is not None:
        nxt=dict(assignment);nxt[abs(unit)]=(unit>0)
        return dpll(simplified,nxt)
    lit=min(simplified,key=len)[0];v=abs(lit)
    for value in (lit>0,lit<0):
        nxt=dict(assignment);nxt[v]=value
        if dpll(simplified,nxt):return True
    return False


def verify_src_offset(clauses, offsets,assignment,offset,expected_payload):
    if offset not in offsets:return False
    ix=offsets.index(offset)
    c=clauses[ix]
    kept=[]
    for lit in c:
        v=abs(lit)
        if v in assignment:
            if assignment[v]==(lit>0):return False
        else: kept.append(lit)
    return tuple(kept)==expected_payload


def unique_exact_alpha_paths(depth):
    # An adaptive complete tree, with branch variable chosen as a function of
    # the current assignment.  Every encountered exact assignment is unique.
    states=set();nodes=0;edges=0
    def visit(alpha):
        nonlocal nodes,edges
        assert alpha not in states
        states.add(alpha);nodes+=1
        if len(alpha)==depth:return
        free=[x for x in range(1,depth+1) if x not in dict(alpha)]
        variable=free[(sum((x*3+v)*11 for x,v in alpha)+len(alpha))%len(free)]
        for value in (0,1):
            edges+=1
            visit(tuple(sorted((*alpha,(variable,value)))))
    visit(tuple())
    return nodes,edges,len(states)


def main():
    assertions=0
    def check(cond,msg):
        nonlocal assertions
        assertions+=1
        if not cond:raise AssertionError(msg)

    table=[]
    for force_unsat in (False,True):
        for k in range(1,9):
            n,clauses,offs,text=build(k,force_unsat)
            n2,cls2,of2=parse_source(text)
            check((n,clauses,offs)==(n2,cls2,of2),f'parse k={k}')
            check(len(set(clauses))==len(clauses),'no duplicate source clauses')
            check(all(len(set(map(abs,c)))==3 for c in clauses),'proper 3CNF')
            if k<=5:
                check(dpll(clauses)==(not force_unsat),'root SAT/UNSAT')
            keys=set();normalized=set();wrong=0
            for bits in itertools.product((0,1), repeat=k):
                alpha={i+1:b for i,b in enumerate(bits)}
                r,origins=residual_and_origins(clauses,offs,alpha,k)
                normalized.add(r);keys.add(origins)
                check(len(origins)==k,'provenance vector arity')
                check(interleaved_verifier(text,bits,origins,k),'interleaved positive verifier')
                for i in range(k):
                    expected=(k+i+1,2*k+i+1)
                    check(verify_src_offset(clauses,offs,alpha,origins[i],expected),'authentic correct origin')
                    wrong_origin=offs[2*i+(0 if bits[i]==1 else 1)]
                    check(not verify_src_offset(clauses,offs,alpha,wrong_origin,expected),'wrong branch origin MUST fail')
                    wrong+=1
                if k<=4:
                    switched=list(origins);switched[0]=offs[0 if bits[0]==1 else 1]
                    check(not interleaved_verifier(text,bits,switched,k),'interleaved bad first origin rejects')
                if k<=4:
                    check(dpll(clauses,alpha)==(not force_unsat),'restricted SAT/UNSAT')
            check(len(normalized)==1,'all residual CNFs identical')
            check(len(keys)==2**k,'2^k different origin maps')
            check(len(text.encode()) <= 256*k*math.ceil(math.log2(k+4))+512,'encoding coarse bound')
            table.append(dict(k=k,force_unsat=force_unsat,n_vars=n,n_clauses=len(clauses),input_bits=8*len(text.encode()),assignments=2**k,distinct_canonical_residuals=len(normalized),distinct_provenance_vectors=len(keys),cross_branch_wrong_offsets_rejected=wrong,root_sat=not force_unsat))
    tree=[]
    for h in range(1,11):
        nodes,edges,states=unique_exact_alpha_paths(h)
        check(nodes==2**(h+1)-1,'tree size')
        check(edges==nodes-1,'edge size')
        check(states==nodes,'unique exact alpha')
        tree.append(dict(depth=h,nodes=nodes,edges=edges,unique_contexts=states))
    c=Fraction(241,200)
    beta=Fraction(1,2)*( (c+2)/(c*c)-c )
    check(beta==Fraction(11642479,23232400),'published exact beta endpoint')
    check(Fraction(1)-beta==Fraction(11589921,23232400),'provenance space exponent gap')
    d=Fraction(901,500)
    C=(2*d-1)/(d*(d-1))
    check(C==Fraction(651000,361301),'conditional two-algorithm fraction')
    # Distinct source-provenance vectors imply >=2^k states only for the
    # separated proof protocol where the complete selector prelude is read
    # once and no arbitrary re-reading/rewind or independent witness tape exists.
    payload={"run":"ARC-PROVENANCE-RECONVERGENCE135","seed":SEED,"checks":assertions,"failures":0,
    "scope":"fixed canonical proper 3CNF; separated source-authenticated provenance replay; not an arbitrary SAT algorithm lower bound",
    "family":table,"exact_alpha_trees":tree,
    "exact_fractions":{"FLMV_c":"241/200","FLMV_beta":str(beta),"one_pass_provenance_space_exponent":1,"space_exponent_gap":str(Fraction(1)-beta),"extra_seed_d":str(d),"conditional_coNTIME_C":str(C)},
    "additional_positive_control":"interleaved selector/source-offset check admits an O(log N)-workspace streaming implementation with a source-order scan; the lower bound applies only to separated prelude/replay ordering",
    "symbolic_theorems":["unique-path: rooted binary decisions with monotonically retained original assignments admit no exact-context reconvergence","2^k distinct authenticated physical-origin maps despite identical residual CNF for all selector assignments","separated one-pass exact provenance replay has >=2^k midpoint configurations by splicing"]}
    output=Path(__file__).with_name('2026-10-26_1544_ARC_PROVENANCE_RECONVERGENCE135_raw.json')
    output.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print(json.dumps({"checks":assertions,"failures":0,"rows":len(table),"largest_k":8,"largest_provenance_maps":256,"tree_depth_max":10,"beta":str(beta),"raw_sha256":hashlib.sha256(output.read_bytes()).hexdigest()},sort_keys=True))

if __name__=='__main__':main()