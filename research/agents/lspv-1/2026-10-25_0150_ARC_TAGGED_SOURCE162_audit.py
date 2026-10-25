#!/usr/bin/env python3
"""ARC-TAGGED-SOURCE162: finite ordinary-CNF source-tag and two-level audit.

This audit does not implement the FLMV hard language or its Cook reduction.
The theorem about a fixed tagged FLMV-hard image is symbolic and uses FLMV.
The tests check exact encodings, readbacks, SAT/UNSAT equivalence, eligible
two-level recursion on an EASY restricted product image, and hostile joins.
Only standard-library Python is needed.
"""
from itertools import product
from pathlib import Path
import json
import hashlib
import math

def cnf_dumps(clauses, nvars):
    lines = [f"p cnf {nvars} {len(clauses)}"]
    lines.extend(" ".join(map(str,clause)) + " 0" for clause in clauses)
    return ("\n".join(lines) + "\n").encode("ascii")

def cnf_loads(data):
    lines = data.decode("ascii").splitlines()
    header = lines[0].split()
    assert len(header) == 4 and header[:2] == ["p","cnf"]
    nvars, m = map(int,header[2:])
    clauses=[]
    for line in lines[1:]:
        ints=[int(v) for v in line.split()]
        assert ints and ints[-1]==0 and all(v != 0 for v in ints[:-1])
        clause=tuple(ints[:-1])
        assert all(1<=abs(v)<=nvars for v in clause)
        clauses.append(clause)
    assert m == len(clauses)
    return clauses,nvars

def sat_dpll(clauses):
    """Independent small-instance complete DPLL decision procedure."""
    def recurse(cs):
        cs=[tuple(c) for c in cs]
        while True:
            if any(len(c)==0 for c in cs): return False
            if not cs: return True
            unit=next((c[0] for c in cs if len(c)==1),None)
            if unit is None: break
            cs=apply(cs,unit)
        if not cs: return True
        lit=min(cs,key=len)[0]
        return recurse(apply(cs,lit)) or recurse(apply(cs,-lit))
    def apply(cs,lit):
        return [tuple(v for v in c if v != -lit) for c in cs if lit not in c]
    return recurse(clauses)

def tag(clauses,source_bits,nvars):
    """Marker has literal variable 4*n+7; prefix tag clauses encode each bit.
    Fresh core variables all shifted above the marker, so SAT is preserved.
    """
    x=tuple(int(i) for i in source_bits)
    assert x and all(b in (0,1) for b in x)
    n=len(x)
    marker=4*n+7
    tagged=[(marker,1,2)]
    for i,b in enumerate(x):
        v=3*i+3
        tagged.append((v if b else -v,v+1,v+2))
    core_shift=4*n+8
    for clause in clauses:
        tagged.append(tuple((1 if l>0 else -1)*(abs(l)+core_shift)
                            for l in clause))
    assert all(len(set(map(abs,c)))==len(c) for c in tagged[:n+1])
    return cnf_dumps(tagged,nvars+core_shift)

def untag(data):
    """Recover source solely from the tagged CNF bits, no side metadata."""
    tagged,nvars=cnf_loads(data)
    marker=tagged[0][0]
    assert marker>7 and (marker-7)%4==0
    n=(marker-7)//4
    assert len(tagged)>=n+1
    bits=[]
    for i in range(n):
        clause=tagged[1+i]
        v=3*i+3
        assert tuple(map(abs,clause))==(v,v+1,v+2)
        bits.append(int(clause[0]>0))
    core_shift=4*n+8
    rest=[]
    for clause in tagged[n+1:]:
        assert all(abs(l)>core_shift for l in clause)
        rest.append(tuple((1 if l>0 else -1)*(abs(l)-core_shift)
                          for l in clause))
    return tuple(bits),rest,nvars-core_shift

def parity_core(bits):
    n=len(bits)
    clauses=[(-1,),(-(n+1),)]
    for i,b in enumerate(bits):
        a=i+1; c=i+2
        if b==0: clauses += [(-a,c),(a,-c)]
        else: clauses += [(a,c),(-a,-c)]
    return clauses,n+1

def signed_cube(block_id,unsat):
    """Seven signed 3-clauses are SAT; all eight are UNSAT."""
    names=(3*block_id+1,3*block_id+2,3*block_id+3)
    result=[]
    for j,sgn in enumerate(product((1,-1),repeat=3)):
        if j==7 and not unsat: continue
        result.append(tuple(v*s for v,s in zip(names,sgn)))
    return result

def independent_core(bits):
    cs=[]
    for i,b in enumerate(bits): cs+=signed_cube(i,b)
    return cs,3*len(bits)

def join_control():
    """A shared variable makes two individually SAT blocks jointly UNSAT."""
    left=[(1,)]; right=[(-1,)]
    assert sat_dpll(left) and sat_dpll(right)
    assert not sat_dpll(left+right)
    tagged=tag(left+right,(0,1),1)
    recovered,core,k=untag(tagged)
    assert recovered==(0,1) and core==left+right and k==1
    assert not sat_dpll(cnf_loads(tagged)[0])
    return True

def main():
    assertions=0
    lengths=[]
    parity_yes=parity_no=0
    for n in range(1,9):
        for bits in product((0,1),repeat=n):
            core,nvars=parity_core(bits)
            data=tag(core,bits,nvars)
            loaded,loaded_n=cnf_loads(data)
            back,decoded,decoded_n=untag(data)
            assert back==bits and decoded==core and decoded_n==nvars
            assertions+=3
            original=sat_dpll(core)
            guest=sat_dpll(loaded)
            expected=(sum(bits)%2==0)
            assert original==guest==expected
            assertions+=2
            parity_yes+=expected; parity_no+=not expected
            lengths.append(len(data))
    two_yes=two_no=0
    first_calls=grand_calls=0
    for bits in product((0,1),repeat=4):
        root_core,k=independent_core(bits)
        root=tag(root_core,bits,k)
        root_value=sat_dpll(cnf_loads(root)[0])
        first_vals=[]
        for i in range(0,4,2):
            sub=bits[i:i+2]
            source,_=independent_core(sub)
            child=tag(source,sub,6)
            y,child_source,child_k=untag(child)
            assert y==sub and child_source==source and child_k==6
            assertions+=3
            child_value=sat_dpll(cnf_loads(child)[0])
            first_vals.append(child_value)
            first_calls+=1
            leaf_vals=[]
            for j in range(2):
                leaf_bits=(sub[j],)
                leaf_core,_=independent_core(leaf_bits)
                leaf=tag(leaf_core,leaf_bits,3)
                recover,core2,vars2=untag(leaf)
                assert recover==leaf_bits and core2==leaf_core and vars2==3
                assertions+=3
                leaf_vals.append(sat_dpll(cnf_loads(leaf)[0]))
                grand_calls+=1
            assert child_value==all(leaf_vals)
            assertions+=1
        assert root_value==all(first_vals)==(sum(bits)==0)
        assertions+=1
        two_yes+=root_value; two_no+=not root_value
    assert join_control()
    assertions+=4

    scaling=[]
    for p in (4,8,16,32,64,128):
        x=(0,)*p
        core,nv=independent_core(x)
        parent=tag(core,x,nv)
        smaller=x[:p//2]
        child_core,child_nv=independent_core(smaller)
        child=tag(child_core,smaller,child_nv)
        scaling.append({
            "blocks":p,"parent_bytes":len(parent),
            "half_child_bytes":len(child),
            "child_parent_ratio":round(len(child)/len(parent),6),
            "effective_lambda":round(math.log(len(child))/math.log(len(parent)),6)
        })
    out={
        "id":"ARC-TAGGED-SOURCE162",
        "status":"COMPUTATIONAL finite only; symbolic theorem separate",
        "python_standard_library":True,"randomness":"none; exhaustive",
        "parity_image_instances":sum(2**n for n in range(1,9)),
        "parity_yes":parity_yes,"parity_no":parity_no,
        "two_level_parent_inputs":16,"two_level_sat":two_yes,
        "two_level_unsat":two_no,"first_level_calls":first_calls,
        "grandchild_calls":grand_calls,"assertions":assertions,
        "cross_block_unsat_join_control":"PASS",
        "scaling":scaling,
        "limitations":[
            "Toy parity image and independent-cube family are easy, not FLMV-hard",
            "DIMACS bytes are logical encodings, not calibrated FLMV TM bit-time",
            "The two-level independent-product family shrinks by a constant ratio, lambda=1",
            "No solver-dependent favorable cofinal ARC edge is constructed"
        ],
        "failures":0
    }
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__": main()
