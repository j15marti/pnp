"""Triangle bundles on authenticated graph-star inputs. Run from experiments/."""
from itertools import permutations, combinations, product
import json
from dynamic_construction_join_palette_20261122 import encode, recover

PERMS = tuple(permutations(range(3)))


def parity(p):
    return sum(a > b for a, b in combinations(p, 2)) % 2


def expand(q, matching):
    edges = {(3*u+a, 3*u+b) for u in range(q) for a, b in combinations(range(3), 2)}
    for (u, v), perm in matching.items():
        edges.update((3*u+a, 3*v+perm[a]) for a in range(3))
    return 3*q, edges


def guard(h, edges):
    if h % 3:
        return None
    q = h//3
    internal = {(3*u+a, 3*u+b) for u in range(q) for a,b in combinations(range(3), 2)}
    if not internal <= edges:
        return None
    groups = {}
    for x,y in edges-internal:
        u,a = divmod(x,3)
        v,b = divmod(y,3)
        groups.setdefault((u,v), []).append((a,b))
    adjacency = [dict() for _ in range(q)]
    for (u,v), pairs in groups.items():
        pairs.sort()
        perm = tuple(b for a,b in pairs)
        if [a for a,b in pairs] != [0,1,2] or perm not in PERMS:
            return None
        adjacency[u][v] = adjacency[v][u] = parity(perm)
    sign = {}
    for root in range(q):
        if root in sign:
            continue
        sign[root] = 0
        todo = [root]
        while todo:
            u = todo.pop()
            for v,flip in adjacency[u].items():
                target = sign[u] ^ flip
                if v not in sign:
                    sign[v] = target
                    todo.append(v)
                elif sign[v] != target:
                    return False
    live = set(range(q))
    while live:
        vertex = next((v for v in sorted(live) if len(live.intersection(adjacency[v]))<=2), None)
        if vertex is None:
            return None
        live.remove(vertex)
    return True


def oracle(q, matching):
    # Enumerate proper color permutations in each triangle with first fiber fixed by symmetry.
    for choices in product(PERMS, repeat=q-1):
        colors = (PERMS[0],)+choices
        if all(all(colors[u][a] != colors[v][p[a]] for a in range(3))
               for (u,v),p in matching.items()):
            return True
    return False


def main():
    counts = [0,0]
    # K4 minus an edge has intersecting quotient cycles and is 2-degenerate.
    skeleton = [(0,1),(0,2),(1,2),(0,3),(1,3)]
    for perms in product(PERMS, repeat=3):
        match = dict(zip(skeleton, (PERMS[0],PERMS[0])+perms))
        h,edges = expand(4,match)
        n, rows = encode(h,edges)
        recovered = recover(n,[r[::-1] for r in rows[::-1]])
        assert recovered == (h,edges)
        value = guard(*recovered)
        assert value == oracle(4,match)
        counts[int(value)]+=1
    for q in range(5,25):
        for perm in PERMS:
            match = {(i,i+1):PERMS[0] for i in range(q-1)}
            match[0,q-1] = perm
            h,edges = expand(q,match)
            assert guard(h,edges) == (parity(perm)==0)
            assert guard(h,edges-{(0,1)}) is None
            assert guard(h,edges-{(0,3)}) is None
    complete = {edge:PERMS[0] for edge in combinations(range(4),2)}
    assert guard(*expand(4,complete)) is None and not oracle(4,complete)
    print(json.dumps(dict(unsat=counts[0],sat=counts[1],cycle_cases=120,
                          broken_guard_cases=240,balanced_K4_unsat=True),sort_keys=True))


if __name__ == "__main__":
    main()
