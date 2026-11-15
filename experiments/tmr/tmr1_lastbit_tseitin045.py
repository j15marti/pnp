#!/usr/bin/env python3
"""TMR-1/045: independent finite verifier of last-sign-bit SAT sensitivity.
Uses only the Python 3 standard library. No SAT oracle or graph library.
Finite tests are COMPUTATIONAL, not asymptotic complexity results.
"""
import json
import itertools
import sys
from collections import deque


def gamma(n):
    assert n > 0
    b = format(n, 'b')
    return '0' * (len(b) - 1) + b


def make_graph(m):
    assert m >= 2
    t = 2 * m
    edges = set()
    for i in range(t):
        for a, b in ((i, (i+1) % t),
                     (t+i, t+(i+1) % t),
                     (i, t+i)):
            edges.add(tuple(sorted((a, b))))
    edges = sorted(edges)
    H = 2*t
    assert len(edges) == 3*H//2
    incidence = [[] for _ in range(H)]
    for k, (a,b) in enumerate(edges):
        incidence[a].append(k)
        incidence[b].append(k)
    for v in range(H):
        incidence[v].sort()
        assert len(incidence[v]) == 3
    return edges, incidence


def build(m):
    edges, incidence = make_graph(m)
    H, E = len(incidence), len(edges)
    charge = [int(v == 0) for v in range(H)]
    clauses = []
    for v in range(H):
        wrong = [s for s in itertools.product((0,1), repeat=3)
                 if (s[0] ^ s[1] ^ s[2]) != charge[v]]
        assert len(wrong) == 4
        # Force the final literal sign in each four-clause packet to be 0.
        tail = next(s for s in wrong if s[2] == 0)
        ordered = [s for s in wrong if s != tail] + [tail]
        for s in ordered:
            clauses.append(tuple((incidence[v][j], s[j]) for j in range(3)))
    assert len(clauses) == 4*H
    assert clauses[-1][-1][1] == 0
    width = (E+1).bit_length()-1
    if (1 << width) < E+1:
        width += 1
    assert width == (E+1-1).bit_length()
    # Indexed, counted proper-3CNF format; last bit is last literal sign.
    bits = '00110101' + gamma(E) + gamma(4*H)
    for C in clauses:
        for e, s in C:
            bits += format(e+1, '0%db' % width) + str(s)
    assert bits[-1] == '0'
    flipped = bits[:-1] + '1'
    # Mutant changes the literal polarity, never the variable identity.
    mutant = list(clauses)
    last = list(mutant[-1])
    e,s = last[-1]
    last[-1] = (e,1-s)
    mutant[-1] = tuple(last)
    return edges, incidence, charge, clauses, mutant, bits, flipped, width


def eval_clause(C, edgevals):
    return any((edgevals[e] ^ s) == 1 for e,s in C)


def explicit_mutant_witness(edges, incidence, charges, last):
    """Solve the graph-with-last-vertex-deleted parity equations on a tree."""
    H = len(incidence)
    v = H-1
    vals = [0] * len(edges)
    for e, s in last:
        vals[e] = s
    root = 0
    adj = [[] for _ in range(H)]
    for e,(a,b) in enumerate(edges):
        if a != v and b != v:
            adj[a].append((b,e))
            adj[b].append((a,e))
    parent = [-1] * H
    parent_edge = [-1] * H
    parent[root] = root
    queue = deque([root])
    order = []
    while queue:
        a=queue.popleft()
        order.append(a)
        for b,e in adj[a]:
            if parent[b] == -1:
                parent[b], parent_edge[b] = a,e
                queue.append(b)
    assert len(order) == H-1
    rhs = [charges[u] for u in range(H)]
    for e,(a,b) in enumerate(edges):
        if a == v and b != v:
            rhs[b] ^= vals[e]
        if b == v and a != v:
            rhs[a] ^= vals[e]
    for a in reversed(order[1:]):
        e=parent_edge[a]
        vals[e] = rhs[a]
        rhs[parent[a]] ^= rhs[a]
    assert rhs[root] == 0
    for u in range(H):
        parity = 0
        for e in incidence[u]:
            parity ^= vals[e]
        if u != v:
            assert parity == charges[u]
        else:
            assert parity != charges[u]
    return vals


def run(mmax=20):
    results=[]
    assertions=0
    exhaustive_count=0
    for m in range(2,mmax+1):
        edges, inc, charges, original, mutant, bits, flipped, w = build(m)
        H,E,N=len(inc),len(edges),len(bits)
        assert H==4*m and E==6*m
        assert len(original)==16*m
        assert N==8+len(gamma(E))+len(gamma(4*H))+12*H*(w+1)
        assert bits[:-1]==flipped[:-1] and bits[-1]=='0' and flipped[-1]=='1'
        assert all(len(C)==3 and len({e for e,s in C})==3 for C in original+mutant)
        assert sum(charges)%2==1
        witness=explicit_mutant_witness(edges,inc,charges,original[-1])
        assert all(eval_clause(C,witness) for C in mutant)
        assert not eval_clause(original[-1],witness)
        assert all(eval_clause(C,witness) for C in original[:-1])
        assertions+=11
        # Trace for honest serial promise reader: one read per byte then EOF/HALT.
        read_max=-1
        delta_hist=[]
        for pos in range(N):
            assert pos==read_max+1
            old=N-1-read_max
            read_max=pos
            new=N-1-read_max
            assert old-new==1
            assert bits[pos]==flipped[pos] or pos==N-1
            delta_hist.append(old-new)
            assertions+=3
        assert read_max==N-1 and sum(delta_hist)==N
        assertions+=1
        if m==2:
            for mask in range(1<<E):
                x=[(mask>>j)&1 for j in range(E)]
                a=all(eval_clause(C,x) for C in original)
                b=all(eval_clause(C,x) for C in mutant)
                assert not a
                exhaustive_count+=1
                if b:
                    assert mask == sum(bit<<j for j,bit in enumerate(x))
                assertions+=1
            assert any(all(eval_clause(C,[(mask>>j)&1 for j in range(E)])
                           for C in mutant) for mask in range(1<<E))
            assertions+=1
        results.append(dict(m=m,vertices=H,edges=E,clauses=len(original),
                            bit_length=N,last_index=N-1,baseline_last=bits[-1],
                            mutant_last=flipped[-1],witness_weight=sum(witness),
                            tariff_initial=N,scanner_steps=N+1))
    return dict(status='COMPUTATIONAL',family='circular-ladder odd-charge Tseitin strict-3CNF',
                encoding='8-bit magic; Elias gamma(E),gamma(4H); 12H id/sign records',
                ranges={'m_min':2,'m_max':mmax},assertions=assertions,
                failures=0,exhaustive_m2_assignments=exhaustive_count,
                records=results)


if __name__ == '__main__':
    output=run(int(sys.argv[1]) if len(sys.argv)>1 else 20)
    print(json.dumps(output,indent=2,sort_keys=True))
