#!/usr/bin/env python3
"""NONAFFINE-WINDOW131: reproducible canonical proper-3CNF window audit.
Restricted grammar, NOT a polynomial algorithm for unrestricted SAT.
stdlib only. Run: python 2026-10-24_2300_NONAFFINE_WINDOW131_minirepro.py
"""
import itertools
import json
import random

SEED = 202610242300

def forbidden_clause(i, word):
    return tuple((-(i+j+1) if bit else i+j+1) for j, bit in enumerate(word))

def unit_gadget(v, positive, a, b):
    return [(v if positive else -v, sa*a, sb*b)
            for sa, sb in itertools.product((1, -1), repeat=2)]

def build(forbidden, final):
    r = len(forbidden)
    assert r >= 1 and final in (0, 1)
    n = r + 8
    clauses = [forbidden_clause(i, triple)
               for i, words in enumerate(forbidden)
               for triple in sorted(words)]
    q = r + 2
    clauses += unit_gadget(1, True, q+1, q+2)
    clauses += unit_gadget(2, True, q+3, q+4)
    clauses += unit_gadget(q, bool(final), q+5, q+6)
    return n, clauses

def parse(n, clauses):
    r = n - 8
    if r < 1 or len(clauses) < 12:
        return None
    q = r+2
    suffix = clauses[-12:]
    for j,(v,a,b) in enumerate(((1,q+1,q+2),(2,q+3,q+4),(q,q+5,q+6))):
        group = suffix[4*j:4*j+4]
        if any(len(c)!=3 or tuple(map(abs,c))!=(v,a,b) for c in group):
            return None
        signs = {int(c[0]>0) for c in group}
        if len(signs)!=1 or (j<2 and signs!={1}):
            return None
        if {(int(c[1]>0),int(c[2]>0)) for c in group} != set(itertools.product((0,1), repeat=2)):
            return None
    final = int(suffix[-1][0] > 0)
    groups = [set() for _ in range(r)]
    previous = -1
    for clause in clauses[:-12]:
        if len(clause)!=3:
            return None
        ids = tuple(map(abs,clause))
        i = ids[0]-1
        if not 0<=i<r or ids!=(i+1,i+2,i+3) or i<previous:
            return None
        previous = i
        word = tuple(int(v<0) for v in clause)
        if word in groups[i]:
            return None
        groups[i].add(word)
    return groups,final

def window_decide(groups,final):
    states={(1,1)}
    for bad in groups:
        states={(b,c) for a,b in states for c in (0,1) if (a,b,c) not in bad}
        if not states: break
    return any(b==final for a,b in states)

def independent_truth(groups,final):
    r=len(groups)
    for x in itertools.product((0,1),repeat=r+2):
        if x[0]==x[1]==1 and x[-1]==final and all(tuple(x[i:i+3]) not in bad for i,bad in enumerate(groups)):
            return True
    return False

def cycles(n,clauses):
    edges={tuple(sorted(pair)) for cl in clauses for pair in
           itertools.combinations(map(abs,cl),2)}
    return len(edges)-n+1

def main():
    rng=random.Random(SEED)
    stats=dict(matched=0,random=0,checks=0,sat=0,unsat=0,failures=0)
    AND={(0,0,1),(0,1,1),(1,0,1),(1,1,0)}
    for r in (1,2,3,4,5,6,8,12,20,48,96,192):
        for final in (0,1):
            source=[AND.copy() for _ in range(r)]
            n,clauses=build(source,final)
            parsed=parse(n,clauses)
            assert parsed==(source,final)
            assert n==r+8 and len(clauses)==4*r+12
            assert cycles(n,clauses)==r+3
            actual=window_decide(source,final)
            assert actual==(final==1)
            if r<=8: assert independent_truth(source,final)==actual
            if not final:
                for j in range(r):
                    shorter=[x.copy() for x in source]
                    shorter[j].clear()
                    assert window_decide(shorter,0)
            stats['checks']+=6
            stats['matched']+=1
            stats['sat' if actual else 'unsat']+=1
    for r in range(1,9):
        for k in range(70):
            groups=[{word for word in itertools.product((0,1),repeat=3)
                     if rng.randrange(5)==0} for _ in range(r)]
            final=rng.randrange(2)
            n,cls=build(groups,final)
            assert parse(n,cls)==(groups,final)
            actual=window_decide(groups,final)
            assert actual==independent_truth(groups,final)
            stats['checks']+=2
            stats['random']+=1
            stats['sat' if actual else 'unsat']+=1
    for r in (3,7,19):
        n,clauses=build([{(1,1,0)} for _ in range(r)],1)
        assert parse(n,list(reversed(clauses))) is None
        assert parse(n,clauses+[(1,2,3)]) is None
        assert parse(n,clauses[:-1]) is None
        stats['checks']+=3
    print(json.dumps(dict(seed=SEED,**stats,scope='restricted canonical grammar; not general SAT or FLMV time')))
if __name__=='__main__': main()
