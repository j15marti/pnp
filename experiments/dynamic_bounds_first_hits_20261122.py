"""Check exact packed differences and all prefix first-hit counts on coloring stars."""
import json
from itertools import product

def graph(bits):
    q = len(bits)
    apex = 6*q
    common, chords = [], []
    for j, bit in enumerate(bits):
        base = 6*j
        common.extend((base+i, apex) for i in range(6))
        common.extend(tuple(sorted((base+i, base+(i+1)%6))) for i in range(6))
        chords.append((base, base+(2 if bit else 3)))
    return apex+1, common+chords

def encode(bits):
    h, edges = graph(bits)
    rows = []
    for i in range(2*h):
        rows.extend(((3*i,3*i+1,3*i+2),(3*i+2,3*((i+1)%(2*h)),6*h+i)))
    for j,(u,v) in enumerate(edges):
        rows.extend((6*u+c,6*v+c,8*h+3*j+c) for c in range(3))
    n, m = 8*h+3*len(edges), len(rows)
    w, gamma = n.bit_length(), format(m+1,'b')
    header = '1'*n+'0'+'0'*(len(gamma)-1)+gamma
    payload = ''.join(format(x+1,'0%db'%w) for row in rows for x in row)
    assert n == 87*len(bits)+8 and m == 63*len(bits)+4
    assert len(header+payload) == n+2+2*(m+1).bit_length()-2+3*m*w
    return header+payload

def rim_bipartite(bits):
    h, edges = graph(bits)
    neighbors = [set() for _ in range(h-1)]
    for u,v in edges:
        if v != h-1:
            neighbors[u].add(v)
            neighbors[v].add(u)
    colors = {}
    for start in range(h-1):
        if start in colors:
            continue
        colors[start] = 0
        todo = [start]
        while todo:
            x = todo.pop()
            for y in neighbors[x]:
                if y not in colors:
                    colors[y] = 1-colors[x]
                    todo.append(y)
                elif colors[x] == colors[y]:
                    return False
    return True

def main():
    pairs = checkpoints = labels = 0
    for q in range(1,17):
        base = encode([0]*q)
        union, starts = set(), []
        for i in range(q):
            bits = [int(j==i) for j in range(q)]
            other = encode(bits)
            assert len(base) == len(other)
            delta = {p for p,(a,b) in enumerate(zip(base,other)) if a!=b}
            assert delta and not delta & union
            union.update(delta)
            starts.append(min(delta))
            pairs += 1
        remaining = q
        for position in range(len(base)+1):
            if position and position-1 in starts:
                remaining -= 1
            assert remaining == sum(start>=position for start in starts)
            checkpoints += 1
        if q<=8:
            for bits in product(range(2), repeat=q):
                assert rim_bipartite(bits) == (not any(bits))
                labels += 1
    print(json.dumps(dict(single_edits=pairs, scan_prefixes=checkpoints,
                          graph_labels=labels, status="PASS"),sort_keys=True))

if __name__ == '__main__':
    main()
