#!/usr/bin/env python3
"""Deterministic finite test of stage-one Cook PHP conservative extensions.
This does not emit the full Cook Extended Resolution proof or certify proof minima.
"""
import itertools, json

def php(h):
    p=lambda i,j:(i-1)*h+j
    out=[tuple(p(i,j) for j in range(1,h+1)) for i in range(1,h+2)]
    for j in range(1,h+1):
        for i in range(1,h+2):
            for k in range(i+1,h+2):
                out.append((-p(i,j),-p(k,j)))
    return out

def defs(h):
    n=h*(h+1); gates=[]; cnf=[]; p=lambda i,j:(i-1)*h+j
    for i in range(1,h+1):
        for j in range(1,h):
            z=n+len(gates)+1; a=p(i,j); b=p(i,h); c=p(h+1,j)
            gates.append((z,a,b,c))
            cnf.extend([(z,-a),(z,-b,-c),(-z,a,b),(-z,a,c)])
    return gates,cnf

def sat(cnf, v):
    return all(any((v[abs(l)] if l>0 else 1-v[abs(l)]) for l in cl) for cl in cnf)

def ext(bits,gates):
    v={i+1:bits[i] for i in range(len(bits))}
    for z,a,b,c in gates:v[z]=int(bool(v[a] or (v[b] and v[c])))
    return v

def strict_dimacs(txt):
    lines=txt.splitlines()
    if not lines or not lines[0].startswith('p cnf '): raise ValueError('header')
    parts=lines[0].split()
    if len(parts)!=4:raise ValueError('header fields')
    nv,nc=map(int,parts[2:]); out=[]
    for line in lines[1:]:
        cl=[int(s) for s in line.split()]
        if not cl or cl[-1]!=0:raise ValueError('unterminated')
        if any(x==0 or abs(x)>nv for x in cl[:-1]):raise ValueError('var')
        out.append(tuple(cl[:-1]))
    if len(out)!=nc:raise ValueError('count')
    return out

def run():
    checks=0;rows=[]
    for h in [1,2,3]:
        F=php(h);gs,D=defs(h);n=h*(h+1);model_count=0;projections=0;subsets=0
        for bits in itertools.product((0,1),repeat=n):
            v=ext(bits,gs);assert sat(D,v);checks+=1
            assert not sat(F,v);checks+=1
            for z,a,b,c in gs:
                w=dict(v);w[z]=1-w[z]
                assert not sat(D,w);checks+=1
            if h<=2:
                # all old source subsets, all old assignments, all auxiliary witnesses
                for mask in range(1<<len(F)):
                    S=[F[k] for k in range(len(F)) if mask>>k&1]
                    old=sat(S,v);exists=False
                    for qb in itertools.product((0,1),repeat=len(gs)):
                        w={i+1:bits[i] for i in range(n)}
                        w.update({g[0]:b for g,b in zip(gs,qb)})
                        if sat(D,w) and sat(S,w):exists=True
                    assert old==exists;checks+=1;projections+=1
            model_count+=1
        if h<=2:subsets=1<<len(F)
        rows.append(dict(holes=h,pigeons=h+1,original_variables=n,original_clauses=len(F),gates=len(gs),definition_clauses=len(D),old_assignments=model_count,source_subsets_checked=subsets,projection_comparisons=projections))
    for txt in ('p cnf 2 1\n1 -2','p cnf 2 1\n3 0','p cnf 2 2\n1 0'):
        try:strict_dimacs(txt)
        except ValueError:checks+=1
        else:raise AssertionError('malformed DIMACS accepted')
    assert strict_dimacs('p cnf 2 2\n1 0\n-1 2 0')==[(1,),(-1,2)];checks+=1
    gs,D=defs(2);v=ext([0]*6,gs)
    assert sat(D,v);checks+=1
    w=dict(v);w[gs[0][0]]=1-w[gs[0][0]]
    assert not sat(D,w);checks+=1
    data=dict(status='COMPUTATIONAL',scope='only first-stage Cook gates, no full proof emitter',rows=rows,checks=checks,seed=None,malformed_rejected=3,corrupted_gate_rejected=True)
    print(json.dumps(data,indent=2))

if __name__=='__main__':run()