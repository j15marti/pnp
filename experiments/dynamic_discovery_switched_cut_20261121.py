"""Exact aggregate violation-energy switch test and integer min-cut audit."""
from collections import defaultdict, deque
from itertools import combinations, product
from pathlib import Path
import json


def polynomial(rows, flips):
    terms = defaultdict(int)
    for row in rows:
        factors = [(abs(lit), (lit > 0) ^ flips.get(abs(lit), 0)) for lit in row]
        constant = {(): 1}
        for i, complemented in factors:
            after = defaultdict(int)
            for key, value in constant.items():
                if complemented:
                    after[key] += value
                after[tuple(sorted((*key, i)))] += -value if complemented else value
            constant = after
        for key, value in constant.items():
            terms[key] += value
    return {key: v for key, v in terms.items() if v}


def switches(terms):
    bounds = defaultdict(lambda: [0, 0])
    for key, v in terms.items():
        if len(key) == 2:
            for h in (0, 1):
                bounds[key][h] += v
        if len(key) == 3:
            for pair in combinations(key, 2):
                bounds[pair][int(v > 0)] += v
    graph = defaultdict(list)
    for (i,j), (lo,hi) in bounds.items():
        if lo < 0 < hi:
            return None
        if lo == hi == 0:
            continue
        parity = int(hi > 0)
        graph[i].append((j, parity))
        graph[j].append((i, parity))
    flip = {}
    for i in graph:
        if i in flip:
            continue
        flip[i] = 0
        stack = [i]
        while stack:
            u = stack.pop()
            for v, parity in graph[u]:
                value = flip[u] ^ parity
                if v in flip:
                    if flip[v] != value:
                        return None
                else:
                    flip[v] = value
                    stack.append(v)
    return flip


def energy_min(rows):
    flip = switches(polynomial(rows, {}))
    if flip is None:
        return None
    terms = polynomial(rows, flip)
    quad = defaultdict(int)
    aux = max((abs(x) for c in rows for x in c), default=0)
    for key, val in terms.items():
        if len(key) < 3:
            quad[key] += val
            continue
        aux += 1
        g = abs(val)
        quad[(aux,)] += g if val > 0 else 2*g
        for i in key:
            quad[i,aux] -= g
        if val > 0:
            for pair in combinations(key, 2):
                quad[pair] += g
    source, sink = -1, -2
    residual = defaultdict(lambda: defaultdict(int))

    def arc(i, j, cap):
        residual[i][j] += cap
        residual[j][i] += 0

    unary = defaultdict(int)
    offset = quad[()]
    for key, val in quad.items():
        if len(key) == 2:
            i,j = key
            assert val <= 0
            arc(i,j,-val)
            unary[i] += val
        elif len(key) == 1:
            unary[key[0]] += val
    for i, val in unary.items():
        if val >= 0:
            arc(i,sink,val)
        else:
            offset += val
            arc(source,i,-val)
    while True:
        queue = deque([source])
        prev = {source: None}
        while queue and sink not in prev:
            i = queue.popleft()
            for j, weight in residual[i].items():
                if weight and j not in prev:
                    prev[j] = i
                    queue.append(j)
        if sink not in prev:
            return offset
        path = []
        j = sink
        while j != source:
            i = prev[j]
            path.append((i,j))
            j = i
        flow = min(residual[i][j] for i,j in path)
        offset += flow
        for i,j in path:
            residual[i][j] -= flow
            residual[j][i] += flow


def decision_tree(rows):
    stats = {"nodes": 0, "admitted_leaves": 0, "max_depth": 0}
    def visit(current, depth):
        stats["nodes"] += 1
        stats["max_depth"] = max(stats["max_depth"], depth)
        optimum = energy_min(current)
        if optimum is not None:
            stats["admitted_leaves"] += 1
            return optimum == 0
        pivot = min(abs(l) for c in current for l in c)
        for bit in (0,1):
            true_lit = pivot if bit else -pivot
            reduced = [tuple(l for l in c if l != -true_lit)
                       for c in current if true_lit not in c]
            if visit(reduced, depth+1):
                return True
        return False
    stats["sat"] = visit(rows, 0)
    return stats


def extract(mod, bits):
    import dynamic_construction_dihedral_choice_20261121 as construction
    try:
        n, rows, _, _, _ = construction.codec.parse(bits)
        m0, rem = divmod(len(rows)-4, 2)
        if rem:
            return None
        for c in range(1, m0+1):
            r = max(3, 2*((c+1)//2)+1)
            if (20*c+4)*r >= m0:
                break
        else:
            return None
        if (20*c+4)*r != m0:
            return None
        d = n-m0-3-(10*c+1)*r-2
        clauses = []
        for j in range(c):
            clause = []
            for pos in (0,1,4):
                stage = 10*j+pos
                row = 4*r + 2*(stage*r+1)
                _, selector, image = rows[5+2*row]
                if not 1 <= selector <= d:
                    return None
                stationary = d+1+(stage+1)*r+1
                clause.append(selector if image != stationary else -selector)
            clauses.append(tuple(clause))
        return clauses if construction.build(mod, clauses)[0] == bits else None
    except (ValueError, IndexError):
        return None


def main():
    clauses = [tuple(sign*i for i,sign in enumerate(pattern,1))
               for pattern in product((1,-1), repeat=3)]
    outcomes = []
    for mask in range(256):
        rows = [row for i,row in enumerate(clauses) if mask >> i & 1]
        values = {x: sum(all(x[abs(l)-1] != (l>0) for l in c) for c in rows)
                  for x in product((0,1), repeat=3)}
        possible = False
        for f in values:
            def value(x):
                return values[tuple(a^b for a,b in zip(x,f))]
            if all(value(x)+value(y) >= value(tuple(map(min,x,y)))+value(tuple(map(max,x,y)))
                   for x in values for y in values):
                possible = True
                break
        result = energy_min(rows)
        assert (result is not None) == possible
        assert result is None or result == min(values.values())
        outcomes.append(result)
    prior = json.loads((Path(__file__).resolve().parents[1] /
        "results/raw/dynamic_construction_dihedral_choice_20261121.json").read_text())
    peer = {r["name"]: energy_min(r["clauses"]) for r in prior["records"]}
    for r in prior["records"]:
        result = peer[r["name"]]
        assert result is None or (result==0) == (r["z3"]=="sat")
    import dynamic_construction_dihedral_choice_20261121 as construction
    mod = construction.codec.load_generator()
    trees = {}
    for record in prior["records"]:
        bits = construction.build(mod, record["clauses"])[0]
        rows = extract(mod, bits)
        assert rows == list(map(tuple, record["clauses"]))
        trees[record["name"]] = decision_tree(rows)
    assert extract(mod, bits[:-1]) is None
    damaged = bits[:-1] + str(1-int(bits[-1]))
    assert extract(mod, damaged) is None
    assert all(trees[r["name"]]["sat"] == (r["z3"]=="sat") for r in prior["records"])
    return dict(branch_trees=trees, mask_order=clauses, minimum_or_null=outcomes,
                admitted=sum(r is not None for r in outcomes), peer=peer)


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
