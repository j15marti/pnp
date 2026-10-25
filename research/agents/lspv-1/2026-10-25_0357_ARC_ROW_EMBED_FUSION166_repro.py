#!/usr/bin/env python3
"""ARC row-membership boundary transfer, two real ordinary CNF child levels.
Standard library only, deterministic finite semantic audit; NOT a FLMV TM trace.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
from itertools import product
import json, math, random, sys, hashlib, os

SEED=202610250357
C=Fraction(241,200)
D=Fraction(11642479,23232400)


def sat(clauses):
    clauses=tuple(tuple(c) for c in clauses)
    def rec(f, assignment):
        while True:
            changed=False
            residual=[]
            for clause in f:
                ok=False; un=[]
                for lit in clause:
                    v=abs(lit)
                    if v in assignment:
                        if assignment[v] == (lit>0): ok=True; break
                    else: un.append(lit)
                if ok:continue
                if not un:return False
                if len(un)==1:
                    lit=un[0]; v=abs(lit); val=lit>0
                    if v in assignment and assignment[v]!=val:return False
                    if v not in assignment:assignment[v]=val;changed=True
                residual.append(tuple(un))
            if not residual:return True
            if not changed:break
            f=tuple(residual)
        freq=defaultdict(int)
        for c in residual:
            for lit in c:freq[abs(lit)]+=1
        v=max(freq,key=lambda x:(freq[x],-x))
        for val in (False,True):
            a=assignment.copy();a[v]=val
            if rec(tuple(residual),a):return True
        return False
    return rec(clauses,{})


def proper_or(clause, counter):
    """E-satisfiable proper 3CNF for distinct-variable OR, fresh counter[0]."""
    L=list(clause)
    if len(set(map(abs,L)))!=len(L): raise AssertionError('input clause repeats name')
    if len(L)==0:
        a,b,c=counter[0],counter[0]+1,counter[0]+2;counter[0]+=3
        return [tuple(sign[i]*var for i,var in enumerate((a,b,c))) for sign in product((1,-1),repeat=3)]
    if len(L)==1:
        a,b=counter[0],counter[0]+1;counter[0]+=2
        return [(L[0],sa*a,sb*b) for sa,sb in product((1,-1),repeat=2)]
    if len(L)==2:
        a=counter[0];counter[0]+=1
        return [(L[0],L[1],a),(L[0],L[1],-a)]
    if len(L)==3:return [tuple(L)]
    aux=[*range(counter[0],counter[0]+len(L)-3)];counter[0]+=len(aux)
    out=[(L[0],L[1],aux[0])]
    for idx in range(2,len(L)-2):
        out.append((-aux[idx-2],L[idx],aux[idx-1]))
    out.append((-aux[-1],L[-2],L[-1]))
    assert len(out)==len(L)-2
    return out


def dimacs(clauses):
    maxvar=max((abs(lit) for c in clauses for lit in c),default=0)
    header=f'p cnf {maxvar} {len(clauses)}\n'
    body=''.join(' '.join(map(str,c))+' 0\n' for c in clauses)
    return header+body


def parse(text):
    lines=[l.strip() for l in text.splitlines() if l.strip() and not l.startswith('c')]
    if not lines:raise ValueError('missing header')
    head=lines[0].split()
    if len(head)!=4 or head[:2]!=['p','cnf']:raise ValueError('invalid header')
    n,m=int(head[2]),int(head[3]);out=[]
    if n<0 or m<0:raise ValueError('negative length')
    for line in lines[1:]:
        vals=list(map(int,line.split()))
        if not vals or vals[-1]!=0 or 0 in vals[:-1]:raise ValueError('bad terminator')
        c=tuple(vals[:-1]);
        if len(c)!=3 or len({abs(z) for z in c})!=3:raise ValueError('not proper 3CNF')
        if any(abs(z)>n for z in c):raise ValueError('var exceeds header')
        out.append(c)
    if m!=len(out):raise ValueError('clause header mismatch')
    return tuple(out)


def scope(clauses):
    first={};last={}
    for i,cl in enumerate(clauses):
        for v in map(abs,cl):
            first.setdefault(v,i);last[v]=i
    maxw=max((sum(first[v]<=i<=last[v] for v in first) for i in range(len(clauses))),default=0)
    return first,last,maxw


def interface(clauses,start,end,first,last):
    left=tuple(sorted(v for v in first if first[v]<start<=last[v]))
    right=tuple(sorted(v for v in first if first[v]<=end<last[v]))
    return left,right


def embed_reachable_and_pin(block,left,right,reachable,beta,allmax,include_row=True):
    counter=[allmax+1]
    out=[tuple(c) for c in block]
    for alpha in product((False,True),repeat=len(left)):
        if include_row and alpha not in reachable:
            # Forbid one incoming boundary assignment, so OR of differences.
            clause=[-v if bit else v for v,bit in zip(left,alpha)]
            out.extend(proper_or(clause,counter))
    for v,b in zip(right,beta):
        out.extend(proper_or((v if b else -v,),counter))
    assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in out)
    return tuple(out)


class Audit:
    def __init__(self):
        self.calls=defaultdict(int); self.labels=defaultdict(lambda:defaultdict(int));self.max_child_bits=defaultdict(int)
        self.max_width=defaultdict(int);self.assertions=0;self.total_queries=0
        self.failures=[];self.first_child_examples=[]
    def check(self,yes,explanation):
        self.assertions+=1
        if not yes:self.failures.append(explanation);raise AssertionError(explanation)


def dp(clauses,depth,audit,level=0,include_row=True):
    clauses=tuple(tuple(c) for c in clauses)
    audit.calls[level]+=1
    f,l,w=scope(clauses);audit.max_width[level]=max(audit.max_width[level],w)
    m=len(clauses)
    if m==0: return True
    block_size=math.ceil(math.sqrt(m))
    reachable={()};prev_right=()
    for start in range(0,m,block_size):
        end=min(m,start+block_size)-1
        left,right=interface(clauses,start,end,f,l)
        audit.check(left==prev_right,f'left/right mismatch level {level}')
        nextrow=set()
        for beta in product((False,True),repeat=len(right)):
            child=embed_reachable_and_pin(clauses[start:end+1],left,right,reachable,beta,
                                        max((abs(x) for c in clauses for x in c),default=0),include_row)
            encoded=dimacs(child); parsed=parse(encoded)
            audit.check(parsed==child,'ordinary DIMACS roundtrip')
            audit.max_child_bits[level]=max(audit.max_child_bits[level],len(encoded)*8)
            audit.total_queries+=1
            if level==0 and len(audit.first_child_examples)<3:audit.first_child_examples.append(dict(bits=len(encoded)*8,left=left,right=right,forbidden=2**len(left)-len(reachable)))
            ans=dp(parsed,depth-1,audit,level+1,include_row) if depth>1 else sat(parsed)
            if depth==1:audit.labels[level+1]['SAT' if ans else 'UNSAT']+=1
            if ans:nextrow.add(beta)
        prev_right=right;reachable=nextrow
    audit.check(prev_right==(),f'nonempty terminal scope level {level}')
    return () in reachable


def example_sources():
    roots=[]
    # Explicit unsat separated complementary 1-pins, and SAT twin pins.
    for opposite in (False,True):
        counter=[4]
        first=proper_or((1,),counter)
        second=proper_or((-1 if opposite else 1,),counter)
        roots.append((f'unit_pair_{"UNSAT" if opposite else "SAT"}',tuple(first+second)))
    # Full 3-variable cube is UNSAT, deletion of one clause SAT.
    cube=[tuple((v if bit else -v) for v,bit in zip((1,2,3),bits)) for bits in product((False,True),repeat=3)]
    roots.append(('cube_UNSAT',tuple(cube)))
    roots.append(('cube_minus_one_SAT',tuple(cube[:-1])))
    # Equalities forcing x==y and x!=y using 3CNF-encoded OR subclauses.
    for inequality in (False,True):
        cnt=[4]
        pairs=[(-1,2),(1,-2)]
        if inequality:pairs.extend([(1,2),(-1,-2)])
        else:pairs.extend([(-1,2),(1,-2)])
        body=[]
        for p in pairs:body+=proper_or(p,cnt)
        roots.append((f'correlated_{"UNSAT" if inequality else "SAT"}',tuple(body)))
    rng=random.Random(SEED)
    n=4
    for i in range(12):
        # Small deterministic SAT and UNSAT examples with new name/sign patterns.
        v=rng.sample(range(1,n+1),3)
        if i%2:
            # The full three-variable cube is UNSAT, independent of clause order.
            body=[tuple(vv if bit else -vv for vv,bit in zip(v,bits))
                  for bits in product((False,True),repeat=3)]
            rng.shuffle(body)
        else:
            witness={vv:bool(rng.getrandbits(1)) for vv in range(1,n+1)}
            body=[]
            for j in range(6):
                vars3=rng.sample(range(1,n+1),3)
                signs=[bool(rng.getrandbits(1)) for _ in range(3)]
                if not any(witness[z]==sgn for z,sgn in zip(vars3,signs)):
                    signs[0]=witness[vars3[0]]
                body.append(tuple(z if sign else -z for z,sign in zip(vars3,signs)))
        roots.append((f'seeded_{i}_{"UNSAT" if i%2 else "SAT"}',tuple(body)))
    return roots


def ledger():
    width=Fraction(1,128);mu=Fraction(1);t=Fraction(10);s=Fraction(10)
    d=6
    new_time=max(Fraction(0),mu+d*width,mu*(1-Fraction(1,2**d))+d*width+mu*t/Fraction(2**d))
    old_time=max(Fraction(0),mu+2*d*width,mu*(1-Fraction(1,2**d))+2*d*width+mu*t/Fraction(2**d))
    space=max(mu/Fraction(2),width,mu*s/Fraction(2**d))
    assert new_time<C and old_time>C and space<D
    return {"mu":str(mu),"delta":str(width),"t":str(t),"s":str(s),"depth":d,
            "one_boundary_time":str(new_time),"two_boundary_time":str(old_time),"space_exponent_without_normalizer_eta":str(space),"strict_c":str(C),"strict_d":str(D)}


def main():
    audit=Audit();roots=example_sources();rootresults=[]
    offset=int(os.getenv("OFFSET","0")); lim=int(os.getenv("LIMIT",str(len(roots))))
    for name,clauses in roots[offset:offset+lim]:
        print('root',name,'width',scope(clauses)[2], 'm',len(clauses),flush=True)
        e=dimacs(clauses);parse(e)
        ref=sat(clauses)
        for depth in (1,2):
            print(' depth',depth,flush=True)
            ans=dp(clauses,depth,audit)
            audit.check(ans==ref,f'mismatch name={name} depth={depth} predicted={ans} actual={ref}')
        rootresults.append({'name':name,'clauses':len(clauses),'sat':ref,'width':scope(clauses)[2],'bits':len(e)*8})
    # Guard: removing the incoming reachable table is incorrect for opposite pins.
    name,clauses=roots[1]
    bad=dp(clauses,1,audit,include_row=False)
    audit.check(bad and not sat(clauses),'missing row should give false SAT positive')
    # Guard: the separate SAT labels of conflicting proper-3CNF units cannot be naively AND-joined.
    ctr=[4];plus=proper_or((1,),ctr);minus=proper_or((-1,),ctr)
    audit.check(sat(plus) and sat(minus) and not sat(plus+minus),'shared-var naive join')
    # Guard: malformed child encoding (out of range) must reject.
    try:parse('p cnf 2 1\n1 2 3 0\n')
    except ValueError: audit.check(True,'malformed guard')
    else:audit.check(False,'missing malformed guard')
    # Independent truth-table check of the row CNF, including long-OR 3CNF chains.
    membership_checks=0
    rowrng=random.Random(SEED+17)
    for w in range(0,6):
        vars0=tuple(range(1,w+1))
        allrows=tuple(product((False,True),repeat=w))
        if w<=3:
            masks=range(1<<len(allrows))
        else:
            masks=[0,(1<<len(allrows))-1]+[rowrng.getrandbits(len(allrows)) for _ in range(10)]
        for mask in masks:
            reach={row for idx,row in enumerate(allrows) if (mask>>idx)&1}
            rowclauses=embed_reachable_and_pin((),vars0,(),reach,(),w)
            for alpha in allrows:
                counter=[max([abs(v) for c in rowclauses for v in c]+[w])+1]
                pins=[]
                for v,bit in zip(vars0,alpha):pins.extend(proper_or((v if bit else -v,),counter))
                audit.check(sat(rowclauses+tuple(pins))==(alpha in reach),f'row-clause truth table w={w} mask={mask} row={alpha}')
                membership_checks+=1
    L=ledger()
    result={"run":"ARC-ROW-EMBED-FUSION166","seed":SEED,"status":"COMPUTATIONAL semantics / CONDITIONAL asymptotic ARC resource envelope",
            "root_count":len(rootresults),"sat_roots":sum(x['sat'] for x in rootresults),"unsat_roots":sum(not x['sat'] for x in rootresults),
            "root_results":rootresults,"semantic_assertions":audit.assertions,"row_membership_truth_table_checks":membership_checks,"failures":audit.failures,"recursive_nodes_by_level":dict(audit.calls),
            "leaf_labels":{str(k):dict(v) for k,v in audit.labels.items()},"actual_ordinary_child_queries":audit.total_queries,
            "max_ordinary_child_bits_by_level":dict(audit.max_child_bits),"max_scope_width_by_level":dict(audit.max_width),
            "child_examples":audit.first_child_examples,"exact_ledger":L,
            "limitations":"No all-input normalizer. Controls are low-width/affine or small. Python steps are not FLMV bit operations, physical switching, nor actual model peak storage."}
    path='/mnt/data/arc_rowfusion_results.json'
    with open(path,'w') as out:json.dump(result,out,indent=2,sort_keys=True)
    print(json.dumps({k:v for k,v in result.items() if k!='root_results'},sort_keys=True,indent=2))

if __name__=='__main__':main()
