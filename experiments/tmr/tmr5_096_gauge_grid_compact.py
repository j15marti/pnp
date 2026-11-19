#!/usr/bin/env python3
"""TMR-5/096: standard-library gauge, witnesses, all cycle orientations audit."""
import itertools
import json

S = {1, 3}
A = [[int((j-i) % 5 in S) for j in range(5)] for i in range(5)]
AT = [[A[j][i] for j in range(5)] for i in range(5)]

def mm(U, V):
    return [[sum(U[i][k]*V[k][j] for k in range(5))
             for j in range(5)] for i in range(5)]

def mpow(U, n):
    X = [[int(i == j) for j in range(5)] for i in range(5)]
    for _ in range(n):
        X = mm(X, U)
    return X

P = [[int((j-i) % 5 == 1) for j in range(5)] for i in range(5)]
assert AT == mm(A, P)
assert mpow(A, 4)[0] == [4, 4, 1, 6, 1]

def graph(h, cyclic):
    def v(r, c, i):
        return (r*h+c)*16+i
    edges = []
    for r in range(h):
        for c in range(h):
            for i in range(16):
                u, w = v(r, c, i), v(r, c, (i+1) % 16)
                edges.append((u, w) if cyclic or i == 15 else (w, u))
            if c+1 < h:
                edges.append((v(r,c,0),v(r,c+1,5)))
            if r+1 < h:
                edges.append((v(r,c,10),v(r+1,c,15)))
    return edges

def witness(h, cyclic):
    g = [i % 5 for i in range(15)] + [2]
    return [((r+c+g[i]) + (0 if cyclic else i)) % 5
            for r in range(h) for c in range(h) for i in range(16)]

results = []
for h in (1, 2, 3, 4, 7, 12):
    left, right = graph(h, True), graph(h, False)
    rightset = set(right)
    assert len(left) == len(right) == 18*h*h-2*h
    assert {frozenset(e) for e in left} == {frozenset(e) for e in right}
    phi = [i % 5 for _ in range(h*h) for i in range(16)]
    flipped = 0
    local_truth_tests = 0
    for u,v in left:
        if (u,v) in rightset:
            assert (phi[v]-phi[u]) % 5 == 0
            a,b = u,v
        else:
            assert (v,u) in rightset
            assert (phi[v]-phi[u]) % 5 == 1
            a,b = v,u
            flipped += 1
        for x,y in itertools.product(range(5), repeat=2):
            old = (y-x) % 5 in S
            assignment = {u:x, v:y}
            new = (assignment[b]+phi[b]-assignment[a]-phi[a]) % 5 in S
            assert old == new
            local_truth_tests += 1
    assert flipped == 15*h*h
    for cyclic, edges in ((True,left),(False,right)):
        x = witness(h,cyclic)
        assert all((x[v]-x[u])%5 in S for u,v in edges)
    assert witness(h,False) == [(x+y)%5 for x,y
                               in zip(witness(h,True), phi)]
    results.append(dict(h=h, vertices=16*h*h,
                        arcs=len(left), cycle_rank=2*h*(h-1)+1,
                        reversed_arcs=flipped,
                        local_truth_tests=local_truth_tests,
                        both_satisfying_witnesses=True))

orientations = {}
for k in (3,4,5,6):
    checks = 0
    for word in itertools.product((0,1),repeat=k):
        arcs = [(i,(i+1)%k) if not b else ((i+1)%k,i)
                for i,b in enumerate(word)]
        direct = sum(all((x[v]-x[u]) % 5 in S for u,v in arcs)
                     for x in itertools.product(range(5),repeat=k))
        b = sum(word)
        transfer_count = 5*mpow(A,k)[0][(-b)%5]
        assert direct == transfer_count
        checks += 1
    orientations[k] = checks


# TMR-2/091 reproduction: four terminal paths with lengths (2,3,3,3).
# Enumerate every orientation and verify that only backward counts matter.
fourpath = {}
all_words_no = 0
for word in itertools.product((0,1),repeat=11):
    rows = []
    backward = []
    offset = 0
    for length in (2,3,3,3):
        segment = word[offset:offset+length]
        offset += length
        b = sum(segment)
        backward.append(b)
        M = mpow(A,0)
        for reverse in segment:
            M = mm(M, AT if reverse else A)
        assert M == mm(mpow(A,length), mpow(P,b))
        rows.append(M[0])
    z = 5*sum(__import__('math').prod(row[d] for row in rows) for d in range(5))
    key = tuple(backward)
    if key in fourpath:
        assert fourpath[key] == z
    else:
        fourpath[key] = z
    all_words_no += (z == 0)
assert len(fourpath) == 192
assert sum(z==0 for z in fourpath.values()) == 12
assert all_words_no == 36
tmr2_fourpath = dict(words=2048, compressed_classes=192,
                     unsat_words=all_words_no, unsat_classes=12)

print(json.dumps(dict(
    theorem="Z5 gauge cyclic/DAG grid blowup firewall",
    direct_cycle_orientation_census=orientations,
    grid_checks=results,
    tmr2_fourpath=tmr2_fourpath,
    assertion_failures=0), indent=2))
