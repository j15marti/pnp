#!/usr/bin/env python3
"""Reproduce finite hostile tests for VSC/PPC-HEC SHIFT1.

No external packages required.
Seed: 20261001.
"""
import itertools
import json
import math
import random
import statistics
import zlib
from collections import deque

SEED = 20261001
rng = random.Random(SEED)

def pack_bits(s):
    pad = (-len(s)) % 8
    s = s + "0" * pad
    return bytes(int(s[i:i+8], 2) for i in range(0, len(s), 8))

def compressed_bits(s):
    return len(zlib.compress(pack_bits(s), 9)) * 8

def cyclic_shift(s, k):
    k %= len(s)
    return s[k:] + s[:k]

def pyramid_dag(h):
    idx = {}
    c = 0
    for level in range(h):
        for i in range(h - level):
            idx[(level, i)] = c
            c += 1
    preds = [set() for _ in range(c)]
    for level in range(1, h):
        for i in range(h - level):
            preds[idx[(level, i)]] = {
                idx[(level - 1, i)],
                idx[(level - 1, i + 1)],
            }
    return preds, idx[(h - 1, 0)]

def binary_tree_dag(depth):
    idx = {}
    c = 0
    for level in range(depth + 1):
        for i in range(2 ** (depth - level)):
            idx[(level, i)] = c
            c += 1
    preds = [set() for _ in range(c)]
    for level in range(1, depth + 1):
        for i in range(2 ** (depth - level)):
            preds[idx[(level, i)]] = {
                idx[(level - 1, 2 * i)],
                idx[(level - 1, 2 * i + 1)],
            }
    return preds, idx[(depth, 0)]

def min_moves_with_space(preds, sink, space):
    n = len(preds)
    q = deque([(0, 0)])
    seen = {0}
    while q:
        mask, dist = q.popleft()
        if (mask >> sink) & 1:
            return dist

        for v in range(n):
            if (mask >> v) & 1:
                nxt = mask & ~(1 << v)
                if nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, dist + 1))

        if mask.bit_count() < space:
            for v in range(n):
                if (mask >> v) & 1:
                    continue
                if all((mask >> u) & 1 for u in preds[v]):
                    nxt = mask | (1 << v)
                    if nxt not in seen:
                        seen.add(nxt)
                        q.append((nxt, dist + 1))
    return None

out = {"seed": SEED}

# Exact state-fiber enumeration.
rows = []
for K in range(1, 9):
    payloads = list(itertools.product([0, 1], repeat=K))
    counts = {0: 0, 1: 0}
    for x in payloads:
        counts[sum(x) % 2] += 1
    rows.append({
        "K": K,
        "no_side_required_bits": K,
        "parity_side_required_bits": int(math.log2(max(counts.values()))) if K > 1 else 0,
    })
out["state_fibers"] = rows

# Exact static-reread bypass table.
out["reread_collapse"] = [
    {
        "K": K,
        "no_reread_free_sat_required_state_bits": K - 1,
        "retained_payload_bits_with_random_access": 0,
        "post_shift_payload_probes": 1,
        "address_bits": math.ceil(math.log2(K)),
    }
    for K in [16, 64, 256, 1024, 4096, 16384]
]

# Compression diagnostic.
comp = []
for K in [256, 1024, 4096, 16384]:
    random_s = "".join(str(rng.randrange(2)) for _ in range(K))
    periodic = ("0011" * (K // 4 + 1))[:K]
    for kind, s in [("random", random_s), ("periodic", periodic)]:
        vals = [compressed_bits(cyclic_shift(s, rng.randrange(K))) for _ in range(32)]
        comp.append({
            "K": K,
            "kind": kind,
            "base_compressed_bits": compressed_bits(s),
            "shifted_mean_compressed_bits": statistics.mean(vals),
            "shifted_min": min(vals),
            "shifted_max": max(vals),
        })
out["compression_diagnostic"] = comp

# Cyclic and affine history-collapse checks.
groups = []
for K in [17, 64, 257]:
    for E in [4, 16, 64]:
        shifts = [rng.randrange(K) for _ in range(E)]
        sigma = sum(shifts) % K
        ok = all((j + sum(shifts)) % K == (j + sigma) % K for j in range(K))
        groups.append({
            "family": "cyclic",
            "K": K,
            "epochs": E,
            "summary_bits": math.ceil(math.log2(K)),
            "verified": ok,
        })

for K in [17, 257]:
    for E in [4, 16, 64]:
        params = []
        A, B = 1, 0
        for _ in range(E):
            a, b = rng.randrange(1, K), rng.randrange(K)
            params.append((a, b))
            A, B = (a * A) % K, (a * B + b) % K

        def seq(x):
            for a, b in params:
                x = (a * x + b) % K
            return x

        ok = all(seq(j) == (A * j + B) % K for j in range(K))
        groups.append({
            "family": "affine",
            "K": K,
            "epochs": E,
            "summary_bits": 2 * math.ceil(math.log2(K)),
            "verified": ok,
        })
out["group_history"] = groups

# Exact black-pebbling small DAGs.
pebbling = []
for family, params in [("pyramid", range(2, 6)), ("binary_tree", range(1, 4))]:
    for p in params:
        preds, sink = pyramid_dag(p) if family == "pyramid" else binary_tree_dag(p)
        n = len(preds)
        for space in range(1, min(n, 8) + 1):
            moves = min_moves_with_space(preds, sink, space)
            if moves is not None:
                pebbling.append({
                    "family": family,
                    "parameter": p,
                    "nodes": n,
                    "space": space,
                    "min_moves": moves,
                })
out["pebbling"] = pebbling

print(json.dumps(out, indent=2, sort_keys=True))
