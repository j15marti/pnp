#!/usr/bin/env python3
"""TMR-2/095 compact independent finite verifier for source-embedded signs.
Status: computational checks; not a physical low-space RAM measurement.
"""
from itertools import product

checks = 0

def ck(a, where):
    global checks
    checks += 1
    if not a:
        raise AssertionError(where)

def guard(q, u):
    return tuple(-(i + 1) if (u >> i) & 1 else i + 1 for i in range(q))

def original_cnf(q, m, flags):
    r = 1 << q
    result = []
    for u in range(r):
        g = guard(q, u)
        for j in range(m):
            y = q + u * m + j + 1
            result += [g + (y,), g + ((-y if flags[u * m + j] else y),)]
    return q + r * m, tuple(result)

def eval_cnf(clauses, a):
    return all(any(bool((a >> (abs(l)-1)) & 1) == (l > 0)
                   for l in clause) for clause in clauses)

def claim_unsat(clauses, q, m, choice):
    r = 1 << q
    if len(choice) != r:
        return False
    for u in range(r):
        j = choice[u]
        if j not in range(m):
            return False
        y = q + u*m + j + 1
        if clauses[2*(u*m+j)] != guard(q,u)+(y,):
            return False
        if clauses[2*(u*m+j)+1] != guard(q,u)+(-y,):
            return False
    return True

def claim_sat(clauses, q, m, u):
    if u not in range(1 << q):
        return False
    return all(clauses[2*(u*m+j)+1] ==
               guard(q,u)+(q+u*m+j+1,)
               for j in range(m))

table = []
for q,m in ((1,1),(1,2),(1,3),(2,1),(2,2)):
    r=1 << q
    pos=neg=0
    for h in product((0,1), repeat=r*m):
        nv, c = original_cnf(q,m,h)
        cnt = sum(eval_cnf(c,x) for x in range(1 << nv))
        zero_rows = [u for u in range(r) if not any(h[u*m:(u+1)*m])]
        ck(cnt == len(zero_rows) * (1 << ((r-1)*m)), ('count',q,m,h))
        is_unsat = not zero_rows
        ck((cnt == 0) == is_unsat, ('decision',q,m,h))
        if is_unsat:
            neg += 1
        else:
            pos += 1
        for path in product(range(m),repeat=r):
            ck(claim_unsat(c,q,m,path) <= is_unsat, ('wrong UNSAT path',q,m,h,path))
        ck(any(claim_unsat(c,q,m,path) for path in product(range(m),repeat=r))
           == is_unsat, ('complete UNSAT advice',q,m,h))
        for u in range(r):
            ck(claim_sat(c,q,m,u) == (u in zero_rows),
               ('SAT row validation',q,m,h,u))
    table.append((q,m,r*m,pos,neg))
    # A row-interleaving adversary returning a 1 on each row's last
    # queried cell forces every adaptive solver to inspect all r*m cells.
    for order in (list(range(r*m)),
                  list(range(r*m-1,-1,-1)),
                  [i for j in range(m) for i in range(j,r*m,m)]):
        seen=[0]*r
        out=[None]*(r*m)
        for pos,idx in enumerate(order):
            row=idx//m
            seen[row]+=1
            out[idx]=int(seen[row]==m)
            ck(pos==r*m-1 or any(out[k*m:(k+1)*m].count(None)
                                   for k in range(r)), 'unresolved row')
        ck(all(any(out[k*m:(k+1)*m]) for k in range(r)),
           'adversary final UNSAT')

# Duplicate-free encoding, with three distinct clauses and two private
# variables per cell. Active h=0 has unique (y,t)=(1,0).
robust_tables = 0
for q,m in ((1,1),(1,2),(1,3),(2,1)):
    r = 1 << q
    for h in product((0,1), repeat=r*m):
        clauses = []
        for u in range(r):
            g = guard(q,u)
            for j in range(m):
                y = q + 2*(u*m+j) + 1
                t = y+1
                clauses.extend((g+(y,),
                                g+((-y if h[u*m+j] else y),t),
                                g+(-t,)))
        ck(len(set(clauses)) == len(clauses), 'pairwise distinct clauses')
        good = sum(not any(h[u*m:(u+1)*m]) for u in range(r))
        expected = good * (1 << (2*(r-1)*m))
        actual = sum(eval_cnf(clauses,a) for a in range(1 << (q+2*r*m)))
        ck(actual == expected, ('distinct-clauses exact count',q,m,h))
        robust_tables += 1

print('TMR-2/095 PASS; duplicate_free_tables=',robust_tables,'assertions=',checks,'table=',table)
