#!/usr/bin/env python3
"""Exact fixed-depth Davis-Putnam source patch audit. Standard library, deterministic.

CNF representation: tuple of signed integer tuples. Literals are nonzero
original source-variable IDs. No use of a SAT solver or hidden label oracle.
DP has exact pointwise existential semantics, preserving empty clauses.
"""
from __future__ import annotations
import argparse, ast, collections, hashlib, itertools, json, math, pathlib


def normalize(clauses):
    ans = []
    seen = set()
    for clause in clauses:
        c = tuple(sorted(set(clause), key=lambda v:(abs(v), v<0)))
        if any(-v in c for v in c):
            continue  # Tautology, always true.
        if c not in seen:
            ans.append(c); seen.add(c)
    return tuple(ans)


def dp_step(formula, x, log):
    pos, neg, keep = [], [], []
    for c in formula:
        log['clause_records_scanned'] += 1
        log['literal_fields_read'] += len(c)
        if x in c: pos.append(c)
        elif -x in c: neg.append(c)
        else: keep.append(c)
    out = list(keep)
    log['resolution_pairs_tried'] += len(pos) * len(neg)
    for a in pos:
        for b in neg:
            aa = [q for q in a if q != x]
            bb = [q for q in b if q != -x]
            log['literal_comparisons_budget'] += len(aa)*len(bb)
            out.append(tuple(aa+bb))
    result = normalize(out)
    log['records_generated_nonunique'] += len(pos)*len(neg)
    log['records_before'] = len(formula)
    log['records_after'] = len(result)
    log['p'] = len(pos); log['q'] = len(neg)
    return result


def sat(formula, assign):
    return all(any((assign[abs(l)] if l>0 else not assign[abs(l)]) for l in c) for c in formula)


def active(formula):
    return set(abs(l) for c in formula for l in c)


def dense_bits(formula):
    """Exact bit length for explicit self-delimiting clause-list encoding.
    Unary n and m headers; each clause has unary width and each signed literal
    consists of one sign bit plus log2(n+1) fixed-width dense index bits.
    Source original identifiers are densely relabeled only for this count.
    """
    n=len(active(formula)); m=len(formula)
    ell=max(1,math.ceil(math.log2(n+1)))
    return (n+1)+(m+1)+sum((len(c)+1)+len(c)*(1+ell) for c in formula)


def grammar(formula):
    if len(set(formula)) != len(formula): return False
    count=collections.Counter()
    for c in formula:
        if len(c)!=3 or len(set(map(abs,c)))!=3: return False
        if not (all(x>0 for x in c) or all(x<0 for x in c)): return False
        for l in c: count[(abs(l),l>0)]+=1
    return bool(count) and all(count[(v,True)]==count[(v,False)]==2 for v in active(formula))


def paired(formula):
    s=set(formula)
    return all(tuple(-x for x in c) in s for c in formula)


def anchor_Y():
    pos=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
    neg=[(1,2,4),(1,3,6),(2,3,5),(4,5,6)]
    return normalize(pos+[tuple(-i for i in c) for c in neg])


def anchor_H():
    pos=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
    return normalize(pos+[tuple(-i for i in c) for c in pos])


def cyclic_Z(h):
    def a(i,t): return 6*(i%h)+t
    clauses=[]
    for i in range(h):
        plus=[(a(i+1,1),a(i,2),a(i,3)),(a(i,1),a(i,4),a(i,5)),
              (a(i,2),a(i,4),a(i,6)),(a(i,3),a(i,5),a(i,6))]
        minus=[(a(i,1),a(i,2),a(i,4)),(a(i,1),a(i,3),a(i,6)),
               (a(i,2),a(i,3),a(i,5)),(a(i,4),a(i,5),a(i,6))]
        clauses.extend(plus);clauses.extend(tuple(-j for j in c) for c in minus)
    return normalize(clauses)


def all_signs3():
    return normalize(tuple(v if bit else -v for v,bit in zip((1,2,3),bits)) for bits in itertools.product((0,1),repeat=3))


def affine_xor3():
    # parity=1; each parity=0 assignment yields one falsifying clause.
    return normalize(tuple((-v if b else v) for v,b in zip((1,2,3),bits))
       for bits in itertools.product((0,1),repeat=3) if sum(bits)%2==0)


def exhaustive_projection_check(source, descendant, pivots):
    remain=sorted(active(source)-set(pivots))
    tests=0
    for bits in itertools.product((False,True),repeat=len(remain)):
        z=dict(zip(remain,bits))
        expected=False
        for pb in itertools.product((False,True),repeat=len(pivots)):
            assignment={**z,**dict(zip(pivots,pb))}
            expected |= sat(source,assignment)
        actual=sat(descendant,z)
        assert actual==expected, (source,descendant,pivots,z,expected,actual)
        tests+=1
    return tests


def audit(name,F,pivots,exhaust=False):
    source=F
    origN=dense_bits(source)
    rows=[]
    for d,x in enumerate(pivots,1):
        log=collections.defaultdict(int)
        F=dp_step(F,x,log)
        # Bound m-4d applies for exact M22 only; independent of SAT label.
        if grammar(source):
            assert len(F)>=len(source)-4*d
            assert all(c in F for c in source if not any(abs(l) in pivots[:d] for l in c))
        width=max([len(c) for c in F]+[0]);assert width<=2**d+2
        h_bound=0
        for _ in range(d):h_bound+= (h_bound+2)**2
        affected_original=sum(any(abs(l) in pivots[:d] for l in c) for c in source)
        new_extra=[c for c in F if c not in source]
        assert len(new_extra)<=h_bound
        row=dict(depth=d,pivot=x,clauses=len(F),active=len(active(F)),
                 max_width=width, explicit_bits=dense_bits(F),source_bits=origN,
                 source_clause_touched=affected_original, generated_unique=len(new_extra),
                 within_M22=grammar(F),
                 within_Cstar=grammar(F) and not paired(F),
                 **dict(log))
        if exhaust: row['projection_assignments_verified']=exhaustive_projection_check(source,F,pivots[:d])
        rows.append(row)
    return dict(source=name,k=len(active(source)),m=len(source),N=origN,
                original_grammar=grammar(source),Cstar=grammar(source) and not paired(source),
                source_models=(sum(sat(source,dict(zip(sorted(active(source)),bits)))
                  for bits in itertools.product((False,True),repeat=len(active(source))))
                  if len(active(source))<=12 else None),steps=rows)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--u-source',default='U_source.txt')
    parser.add_argument('--out',default='M22_FIXED_DP_LOCALITY151_raw.json')
    args=parser.parse_args()
    txt=pathlib.Path(args.u_source).read_text()
    U=normalize(ast.literal_eval(txt[txt.index('[['):]))
    suite=[('Y-SAT',anchor_Y(),[1,2,3,4],True),
           ('H-PAIRED-SAT',anchor_H(),[1,2,3,4],True),
           ('Z2-CONNECTED-SAT',cyclic_Z(2),[1,2,3,4],True),
           ('U198-PUBLISHED-UNSAT',U,[1,2,3,4],False),
           ('U198-ALTERNATE-PIVOT',U,[193,194,195,196],False),
           ('OUT-UNSAT-ALLSIGNS',all_signs3(),[1,2,3],True),
           ('OUT-AFFINE-XOR',affine_xor3(),[1,2,3],True),
           ('OUT-HORN',normalize([(-1,2),(-2,3),(1,),(-3,)]),[1,2,3],True),
           ('OUT-2SAT',normalize([(1,2),(-1,2),(1,-2)]),[1,2],True)]
    results=[audit(*x) for x in suite]
    assert all(len(r['steps'])>=2 for r in results)
    assert sum(r['steps'][-1].get('projection_assignments_verified',0) for r in results)>0
    hashes=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    out=dict(tag='M22-FIXED-DP-LOCALITY151',method='deterministic exact projection checks',
             labels_imported=['U198-PUBLISHED-UNSAT (Doeker original)'],
             code_sha256=hashes,results=results,
             total_projection_checks=sum(st.get('projection_assignments_verified',0)
                        for r in results for st in r['steps']))
    pathlib.Path(args.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(sources=len(results),total_projection_checks=out['total_projection_checks'],
         per_source=[(r['source'],r['N'],[(s['clauses'],s['explicit_bits']) for s in r['steps']])
                     for r in results]),sort_keys=True))

if __name__=='__main__': main()