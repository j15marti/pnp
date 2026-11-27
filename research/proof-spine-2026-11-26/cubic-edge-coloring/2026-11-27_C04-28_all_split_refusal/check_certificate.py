#!/usr/bin/env python3
"""Check a C04-28 all-splits refusal certificate on exact native bytes.
Usage: python check_certificate.py network.eb.json certificate.json
The all-splits theorem is proved in the accompanying report. This checker
verifies its affine-witness premise, not original integer-B4 feasibility.
"""
import sys, json, hashlib
from pathlib import Path


def check(network_bytes, certificate_bytes):
    G = json.loads(network_bytes)
    C = json.loads(certificate_bytes)
    assert G['format'] == C['problem_id'] == 'STRICT-EB4-v1'
    assert C['guard_id'] == 'EMPTY' and C['residual_id'] == 'ROOT'
    assert C['original_N_bits'] == 8 * len(network_bytes)
    assert C['instance_id'] == 'STRICT-EB4-v1:sha256:' + hashlib.sha256(network_bytes).hexdigest()
    T, edges = G['types'], G['edges']
    n = len(T)
    assert all(t in ('E', 'B') for t in T)
    adj = [[] for _ in range(4*n)]
    seen_ports, seen_edges = set(), set()
    def link(a, b, s):
        adj[a].append((b, s)); adj[b].append((a, s))
    for a, b, s in edges:
        assert 0 <= a < 4*n and 0 <= b < 4*n and s in (0, 1)
        key = tuple(sorted((a//4, b//4)))
        assert key[0] != key[1] and key not in seen_edges
        assert a not in seen_ports and b not in seen_ports
        seen_edges.add(key); seen_ports.update((a, b)); link(a, b, s)
    assert len(seen_ports) == 4*n
    for v, t in enumerate(T):
        if t == 'E':
            for j in (1, 2, 3): link(4*v, 4*v+j, 0)
    true_roots = set(C['true_roots'])
    assert len(true_roots) == len(C['true_roots'])
    word = [-1]*(4*n)
    actual_roots = set()
    for p in range(4*n):
        if word[p] != -1: continue
        actual_roots.add(p)
        word[p] = int(p in true_roots)
        queue = [p]
        for a in queue:
            for b, s in adj[a]:
                z = word[a] ^ s
                if word[b] == -1:
                    word[b] = z; queue.append(b)
                else: assert word[b] == z
    assert true_roots <= actual_roots
    for a, b, s in edges: assert word[a] ^ word[b] == s
    for v, t in enumerate(T):
        w = word[4*v:4*v+4]
        if t == 'E': assert len(set(w)) == 1
        else: assert sum(w) % 2 == 0
    return {'status': 'AFFINE-WITNESS-VERIFIED', 'source_feasibility': 'NOT ESTABLISHED',
            'certificate_id': 'CERT-v1:sha256:' + hashlib.sha256(certificate_bytes).hexdigest(),
            'ports': len(word), 'edges': len(edges)}

if __name__ == '__main__':
    assert len(sys.argv) == 3, 'supply native network JSON and certificate JSON'
    print(json.dumps(check(Path(sys.argv[1]).read_bytes(), Path(sys.argv[2]).read_bytes()), indent=2))
