#!/usr/bin/env python3
"""LSPV-1/477: exact ring-polynomial split-clause transfer controls.
Standalone stdlib executable. This is not a historical R_mix341 checker.
"""
from itertools import product, combinations
from collections import Counter
import hashlib, json, time, resource
from pathlib import Path

PSET = (2, 3, 5, 7)
POLY_TESTS = 0
BOOL_TESTS = 0
BAD_REJECTIONS = 0

# Sparse ordinary polynomial representation, monomial is a sorted tuple of variables.
# Repeated variables are retained: x^2-x is not the zero polynomial.
def clean(d, p):
    return {m: (c % p) for m, c in d.items() if c % p}
def add(a, b, p):
    o = dict(a)
    for m,c in b.items(): o[m] = o.get(m,0)+c
    return clean(o,p)
def scale(a,c,p):
    return clean({m:c*v for m,v in a.items()},p)
def mul(a,b,p):
    d={}
    for m,c in a.items():
        for n,v in b.items():
            key=tuple(sorted(m+n));d[key]=d.get(key,0)+c*v
    return clean(d,p)
def const(c,p): return clean({():c},p)
def var(i,p):return {(i,):1}
def lit(i,positive,p): return var(i,p) if positive else add(const(1,p),scale(var(i,p),-1,p),p)
def falsity(i,positive,p):return lit(i,not positive,p)
def clausepoly(clause,p):
    r=const(1,p)
    for i,positive in clause:r=mul(r,falsity(i,positive,p),p)
    return r
def sigma(poly, a_idx, image, p):
    z={}
    for mon,c in poly.items():
        s=const(c,p)
        for index in mon:s=mul(s,image if index==a_idx else var(index,p),p)
        z=add(z,s,p)
    return z
def deg(poly):return max((len(m) for m in poly),default=0)
def assert_same(x,y,tag):
    global POLY_TESTS
    POLY_TESTS+=1
    assert x==y, tag

def verify_local(lits):
    global BOOL_TESTS,BAD_REJECTIONS
    (i1,b1),(i2,b2),(i3,b3)=lits
    a=3
    P=[(i1,b1),(i2,b2),(a,True)]
    Q=[(i1,b1),(i3,b3),(a,False)]
    C=lits
    badQ=[(i1,b1),(i3,b3),(a,True)]
    for p in PSET:
        cp,pp,qp=clausepoly(C,p),clausepoly(P,p),clausepoly(Q,p)
        l3=lit(i3,b3,p)
        assert_same(sigma(pp,a,l3,p),cp,(p,lits,'Pprojection'))
        assert_same(sigma(qp,a,l3,p),scale(mul(falsity(i1,b1,p),add(mul(var(i3,p),var(i3,p),p),scale(var(i3,p),-1,p),p),p),-1,p),(p,lits,'QprojectionBoolean'))
        # Boolean axiom of auxiliary under sigma maps to original Boolean axiom.
        abool=add(mul(var(a,p),var(a,p),p),scale(var(a,p),-1,p),p)
        xbool=add(mul(var(i3,p),var(i3,p),p),scale(var(i3,p),-1,p),p)
        assert_same(sigma(abool,a,l3,p),xbool,(p,lits,'Boolprojection'))
        # The original falsity polynomial is derived by a degree-four PC combination.
        lifted=add(mul(pp,falsity(i3,b3,p),p),mul(qp,falsity(i2,b2,p),p),p)
        assert_same(lifted,cp,(p,lits,'forward_PC'))
        assert max(deg(pp),deg(qp),deg(lifted),deg(mul(pp,falsity(i3,b3,p),p)),deg(mul(qp,falsity(i2,b2,p),p)))<=4
        # All field identities are ordinary polynomial ring identities, not just Boolean functions.
    for mask in range(8):
        val={i:bool((mask>>i)&1) for i in range(3)}
        def ev(c, a_value=None):
            return any((val.get(j,a_value) if b else not val.get(j,a_value)) for j,b in c)
        cval=ev(C)
        solvable=any(ev(P, v) and ev(Q, v) for v in (False,True))
        section=ev(P,ev([(i3,b3)])) and ev(Q,ev([(i3,b3)]))
        assert cval==solvable==section
        BOOL_TESTS+=1
    # Mutated polarity has a counterexample on the source clause's falsifying row.
    falsifying={i: not b for i,b in lits}
    assert not any((any(falsifying.get(j,a_) if b else not falsifying.get(j,a_) for j,b in P)
                    and any(falsifying.get(j,a_) if b else not falsifying.get(j,a_) for j,b in Q))
                   for a_ in (False,True))
    assert any((any(falsifying.get(j,a_) if b else not falsifying.get(j,a_) for j,b in P)
                and any(falsifying.get(j,a_) if b else not falsifying.get(j,a_) for j,b in badQ))
               for a_ in (False,True))
    BAD_REJECTIONS+=1

def k4_tseitin(charges):
    edges=list(combinations(range(4),2))
    clauses=[]
    for v in range(4):
        incident=[i for i,e in enumerate(edges) if v in e]
        for bits in product((0,1),repeat=3):
            if sum(bits)%2 !=charges[v]:
                clauses.append(tuple((ei,not bool(bit)) for ei,bit in zip(incident,bits)))
    return edges,clauses

def cnf_bytes(variables, clauses):
    lines=[f'p cnf {variables} {len(clauses)}']
    for c in clauses: lines.append(' '.join(str((i+1)*(1 if pos else -1)) for i,pos in c)+' 0')
    return ('\n'.join(lines)+'\n').encode()
def is_sat_clause(c,bits):return any(bool((bits>>i)&1)==b for i,b in c)
def test_graph():
    global BOOL_TESTS,BAD_REJECTIONS
    out={}
    for tag,charges in [('odd',(1,0,0,0)),('even',(0,0,0,0))]:
        e,F=k4_tseitin(charges)
        assert len(e)==6 and len(F)==16
        S=[]
        for idx,c in enumerate(F):
            a=len(e)+idx
            S.extend([tuple([c[0],c[1],(a,True)]),tuple([c[0],c[2],(a,False)])])
        models=[]
        for mask in range(1<<len(e)):
            f=all(is_sat_clause(c,mask) for c in F)
            # Uniform section sigma(a_i)=literal 3 value, no search or oracle.
            avalues={len(e)+j:int(bool((mask>>c[2][0])&1)==c[2][1]) for j,c in enumerate(F)}
            def satisfies_clause(c):
                return any((bool((mask>>i)&1) if i<len(e) else bool(avalues[i]))==pos for i,pos in c)
            s=all(satisfies_clause(c) for c in S)
            assert s==f
            # Equisatisfiability verified directly using each independent auxiliary pair.
            existential=True
            for j,c in enumerate(F):
                pair=S[2*j:2*j+2]
                def pairvalue(a_):
                    def value(cl):
                        return any((bool((mask>>i)&1) if i<len(e) else a_)==pos for i,pos in cl)
                    return all(map(value,pair))
                existential &= any(pairvalue(a_) for a_ in (False,True))
            assert existential==f
            if f:models.append(mask)
            BOOL_TESTS+=2
        assert len(models)==(0 if tag=='odd' else 8)
        if tag=='odd':
            for removed in range(len(F)):
                assert any(all(is_sat_clause(c,bits) for j,c in enumerate(F) if j!=removed) for bits in range(1<<len(e)))
                BOOL_TESTS+=1
        out[tag]={'vars':len(e),'clauses':len(F),'models':len(models),'sha256':hashlib.sha256(cnf_bytes(len(e),F)).hexdigest(),'split_vars':len(e)+len(F),'split_clauses':len(S),'split_sha256':hashlib.sha256(cnf_bytes(len(e)+len(F),S)).hexdigest()}
    return out

def main():
    t=time.perf_counter()
    for signs in product((False,True),repeat=3):
        verify_local(tuple((i,signs[i]) for i in range(3)))
    graphs=test_graph()
    # Plain PC string projection has at most two instructions for x->1-x multiplication.
    # Deliberate invalid candidate: replacing Q_i's -a with +a always corrupts model projection.
    out={'status':'PASS','model':'ordinary PC over fields; 3CNF gadget, no R_mix341 accepted-byte claims','fields':list(PSET),'polynomial_identities':POLY_TESTS,'truth_table_assignments':BOOL_TESTS,'wrong_polarity_rejections':BAD_REJECTIONS,'graphs':graphs,'wall_s':round(time.perf_counter()-t,6),'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
