#!/usr/bin/env python3
"""ADAPTIVE_BIDIR65 minimal exact graph-parity continuation, standard library.
The recognized family is NOT signed exact-(2,2) SAT. The general fallback
used in the full audit is intentionally not part of this minimal reproduction.
"""
from collections import defaultdict

def generate(q, flip):
    assert q >= 4
    shifts = (0, 1, q//2)
    assert len(set(shifts)) == 3
    incidence = [[] for _ in range(2*q)]
    for i in range(q):
        for s in shifts:
            edge = 1 + sum(len(x) for x in [])  # explicit source counter below
    eid = 0
    for i in range(q):
        for s in shifts:
            eid += 1
            j = (i+s) % q
            incidence[i].append(eid)
            incidence[q+j].append(eid)
    assert eid == 3*q and all(len(z) == 3 for z in incidence)
    clauses = []
    for i, support in enumerate(incidence):
        rhs = int(bool(flip and i == 0))
        for mask in range(8):
            bits = tuple((mask >> j) & 1 for j in range(3))
            if sum(bits) % 2 != rhs:
                clauses.append(tuple(v if bit == 0 else -v
                                     for v,bit in zip(support,bits)))
    g = 3*q+1
    clauses += [(g,1), (g,-1)]
    h1,h2,h3 = g+1,g+2,g+3
    clauses += [(-h1,-h2,h3),(-h3,-h1),(-h3,-h2)]
    u,v = g+4,g+5
    clauses += [(u,v),(-u,-v)]
    assert len(clauses) == 8*q+7
    return v, tuple(clauses)

def certify_quartets(clauses):
    """Accept only exactly four source clauses encoding each 3-XOR."""
    assert len(clauses) % 4 == 0
    equations = []
    for i in range(0, len(clauses),4):
        quartet = clauses[i:i+4]
        support = tuple(sorted(map(abs, quartet[0])))
        if len(set(support)) != 3:
            return None
        forbidden = set()
        for clause in quartet:
            if tuple(sorted(map(abs, clause))) != support:
                return None
            lit = {abs(z):z for z in clause}
            mask = sum(1 << j for j,v in enumerate(support) if lit[v] < 0)
            forbidden.add(mask)
        if len(forbidden) != 4:
            return None
        parity = {m.bit_count() % 2 for m in forbidden}
        if len(parity) != 1:
            return None
        equations.append((support, 1 - parity.pop()))
    return equations

def forest_parity(equations):
    """Returns None if UNSAT, dictionary of coherent source bits otherwise."""
    incidence = defaultdict(list)
    for i,(support,rhs) in enumerate(equations):
        if len(support) != 3 or len(set(support)) != 3:
            raise ValueError("not a certified graph-parity system")
        for e in support:
            incidence[e].append(i)
    if any(len(v) != 2 or v[0] == v[1] for v in incidence.values()):
        raise ValueError("not a certified graph-parity system")
    adj = [[] for _ in equations]
    for edge,(a,b) in incidence.items():
        adj[a].append((b,edge))
        adj[b].append((a,edge))
    charges = [rhs for support,rhs in equations]
    assignment = {edge:False for edge in incidence}
    visited = set()
    for root in range(len(equations)):
        if root in visited:
            continue
        visited.add(root)
        order = [root]
        parent = {root:(None,None)}
        for node in order:
            for nxt,edge in adj[node]:
                if nxt not in visited:
                    visited.add(nxt)
                    parent[nxt] = node,edge
                    order.append(nxt)
        for node in reversed(order[1:]):
            prev,edge = parent[node]
            if charges[node]:
                assignment[edge] = True
                charges[prev] ^= 1
        if charges[root]:
            return None
    assert all(sum(assignment[e] for e in support) % 2 == rhs
               for support,rhs in equations)
    return assignment

def recognized_source_solver(q, n, clauses):
    """Exact within canonical mixed-family grammar; unsupported raises."""
    if n != 3*q+6 or len(clauses) != 8*q+7:
        raise ValueError("UNSUPPORTED input")
    g = 3*q+1
    h1,h2,h3 = g+1,g+2,g+3
    u,v = g+4,g+5
    if clauses[-7:] != ((g,1),(g,-1),(-h1,-h2,h3),
                        (-h3,-h1),(-h3,-h2),(u,v),(-u,-v)):
        raise ValueError("UNSUPPORTED input")
    equations = certify_quartets(clauses[:-7])
    if equations is None:
        raise ValueError("UNSUPPORTED quartet grammar")
    edge_values = forest_parity(equations)
    if edge_values is None:
        return "UNSAT",None
    model = dict(edge_values)
    model.update({g:True,h1:False,h2:False,h3:False,u:True,v:False})
    assert all(any(model[abs(lit)] == (lit>0) for lit in clause)
               for clause in clauses)
    return "SAT",model

def main():
    tests = 0
    for q in (4,5,6,8,10,12,16,24,32):
        for flip in (False,True):
            n,clauses = generate(q,flip)
            label,model = recognized_source_solver(q,n,clauses)
            assert label == ("UNSAT" if flip else "SAT")
            print("q",q,"label",label,"sources",n,"clauses",len(clauses),
                  "witness",bool(model))
            tests += 1
    print("PASS",tests,"both-label canonical instances.")
if __name__ == "__main__":
    main()
