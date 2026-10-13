#!/usr/bin/env python3
"""Independent truth-table audit of explicit iterated residual lifting.

This checker intentionally does not import HIERLIFT1/PERMEXT1 code.  It uses
small complete edge truth tables to validate satisfiability, uniqueness,
decoding, and reconstruction for source-dependent Gold-cube Tseitin layers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import time
from dataclasses import dataclass
from pathlib import Path


SEED = 23242026
MAGIC = b"HL2\x00"
MODULI = {1: 0b11, 3: 0b1011}


def gf_mul(a: int, b: int, d: int, modulus: int) -> int:
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & (1 << d):
            a ^= modulus
    return out & ((1 << d) - 1)


def gf_pow(a: int, e: int, d: int, modulus: int) -> int:
    out = 1
    while e:
        if e & 1:
            out = gf_mul(out, a, d, modulus)
        a = gf_mul(a, a, d, modulus)
        e >>= 1
    return out


def bit_list(x: int, n: int) -> list[int]:
    return [(x >> i) & 1 for i in range(n)]


def bit_value(xs: list[int]) -> int:
    return sum((b & 1) << i for i, b in enumerate(xs))


@dataclass(frozen=True)
class Graph:
    vertices: int
    edges: tuple[tuple[int, int], ...]
    tree: tuple[int, ...]
    cotree: tuple[int, ...]


def graph(d: int) -> Graph:
    # K_{2,d+1}; cycle rank d.
    edges = tuple([(0, r) for r in range(2, d + 3)] +
                  [(1, r) for r in range(2, d + 3)])
    return Graph(d + 3, edges, tuple(range(d + 2)),
                 tuple(range(d + 2, 2 * d + 2)))


def inc(g: Graph, assignment: int) -> list[int]:
    out = [0] * g.vertices
    for i, (u, v) in enumerate(g.edges):
        if (assignment >> i) & 1:
            out[u] ^= 1
            out[v] ^= 1
    return out


def cotree(g: Graph, assignment: int) -> int:
    return sum(((assignment >> e) & 1) << i for i, e in enumerate(g.cotree))


def lift(g: Graph, charge: list[int], z: int) -> int:
    if len(charge) != g.vertices or sum(charge) & 1:
        raise ValueError("inconsistent charge")
    edge_bits = [0] * len(g.edges)
    residual = charge[:]
    for i, edge_index in enumerate(g.cotree):
        b = (z >> i) & 1
        edge_bits[edge_index] = b
        if b:
            u, v = g.edges[edge_index]
            residual[u] ^= 1
            residual[v] ^= 1
    adjacency = [[] for _ in range(g.vertices)]
    for edge_index in g.tree:
        u, v = g.edges[edge_index]
        adjacency[u].append((v, edge_index))
        adjacency[v].append((u, edge_index))
    parent = [-1] * g.vertices
    parent_edge = [-1] * g.vertices
    order = [0]
    for u in order:
        for v, edge_index in adjacency[u]:
            if parent[u] == v:
                continue
            parent[v] = u
            parent_edge[v] = edge_index
            order.append(v)
    if len(order) != g.vertices:
        raise ValueError("disconnected tree")
    for v in reversed(order[1:]):
        b = residual[v]
        edge_bits[parent_edge[v]] = b
        if b:
            residual[parent[v]] ^= 1
        residual[v] = 0
    if residual[0]:
        raise ValueError("root inconsistency")
    return bit_value(edge_bits)


def transformed_source(source: list[int], phase: int) -> list[int]:
    n = len(source)
    out = [source[(i + phase) % n] for i in range(n)]
    return [b ^ ((phase >> (i % 2)) & 1) for i, b in enumerate(out)]


def target(prefix: list[int], d: int, layer: int, phase: int) -> int:
    n = len(prefix)
    out = []
    for i in range(d):
        out.append(prefix[(i + layer) % n]
                   ^ (prefix[(2 * i + phase + 1) % n]
                      & prefix[(3 * i + layer + 1) % n])
                   ^ ((i + phase + layer) & 1))
    return bit_value(out)


def charge(prefix: list[int], vertices: int, layer: int) -> list[int]:
    n = len(prefix)
    out = [prefix[(i + layer) % n]
           ^ (prefix[(2 * i + 1) % n] & prefix[(3 * i + layer + 2) % n])
           for i in range(vertices - 1)]
    out.append(sum(out) & 1)
    return out


def holds(g: Graph, assignment: int, c: list[int], b: int, d: int,
          modulus: int, order: tuple[str, str] = ("charge", "cube")) -> bool:
    for constraint in order:
        if constraint == "charge" and inc(g, assignment) != c:
            return False
        if constraint == "cube":
            z = cotree(g, assignment)
            if gf_pow(z, 3, d, modulus) != b:
                return False
    return True


def enumerate_layer(prefix: list[int], d: int, layer: int, phase: int,
                    constraint_order: tuple[str, str]) -> tuple[list[int], int, list[int], int]:
    g = graph(d)
    b = target(prefix, d, layer, phase)
    c = charge(prefix, g.vertices, layer)
    matches = [a for a in range(1 << len(g.edges))
               if holds(g, a, c, b, d, MODULI[d], constraint_order)]
    inverse = (2 ** (d + 1) - 1) // 3
    z = gf_pow(b, inverse, d, MODULI[d])
    reconstructed = lift(g, c, z)
    return matches, reconstructed, c, b


def encode_record(source_width: int, dimensions: list[int], phase: int,
                  max_dependencies: list[int] | None = None) -> bytes:
    if max_dependencies is None:
        max_dependencies = [-1] + list(range(len(dimensions) - 1))
    out = bytearray(MAGIC + bytes([source_width, len(dimensions), phase]))
    for d, dep in zip(dimensions, max_dependencies):
        modulus = MODULI.get(d, 0)
        out.extend(bytes([d, (modulus >> 8) & 0xFF, modulus & 0xFF,
                          255 if dep < 0 else dep]))
    return bytes(out)


def decode_record(data: bytes) -> tuple[int, list[int], int]:
    if len(data) < 7 or data[:4] != MAGIC:
        raise ValueError("bad magic or truncated header")
    source_width, depth, phase = data[4], data[5], data[6]
    if source_width == 0 or phase > 3 or len(data) != 7 + 4 * depth:
        raise ValueError("bad header length/value")
    dims = []
    for j in range(depth):
        pos = 7 + 4 * j
        d = data[pos]
        modulus = (data[pos + 1] << 8) | data[pos + 2]
        dep = -1 if data[pos + 3] == 255 else data[pos + 3]
        if d not in MODULI or d % 2 == 0 or modulus != MODULI[d]:
            raise ValueError("unsupported field record")
        if dep >= j:
            raise ValueError("cyclic/future dependency")
        dims.append(d)
    return source_width, dims, phase


def source_predicates(u: list[int]) -> dict[str, bool]:
    return {
        "yes": True,
        "no": False,
        "horn": (not u[0]) or (u[1] and u[2]),
        "krom": (u[0] or u[1]) and ((not u[1]) or u[2]),
        "affine": (u[0] ^ u[1] ^ u[2] ^ u[3]) == 0,
        "path": all(not (u[i] and u[i + 1]) for i in range(3)),
        "product": (u[0] == u[1]) and (u[2] or u[3]),
        "planted3": (u[0] or u[1] or u[2]) and ((not u[1]) or u[2] or u[3]),
    }


def disconnected_controls() -> dict:
    # One triangle plus an isolate.  cc(X)=2; deleting all R edges gives 4
    # components, so rho=3+2-4=1.
    edges = ((0, 1), (1, 2), (2, 0))
    def incidence(a: int) -> list[int]:
        out = [0, 0, 0, 0]
        for i, (u, v) in enumerate(edges):
            if (a >> i) & 1:
                out[u] ^= 1
                out[v] ^= 1
        return out
    even = [a for a in range(8) if incidence(a) == [0, 0, 0, 0]]
    odd_isolate = [a for a in range(8) if incidence(a) == [0, 0, 0, 1]]
    return {"rho_formula": 3 + 2 - 4, "even_witnesses": len(even),
            "odd_isolate_witnesses": len(odd_isolate)}


def run() -> dict:
    start = time.perf_counter()
    rng = random.Random(SEED)
    assertions = 0
    candidate_edges = 0
    layer_witnesses = 0
    full_hierarchies = 0
    accepted_models = {name: 0 for name in source_predicates([0, 0, 0, 0])}
    depth_rows = []

    # Independent full cube tables.
    for d, modulus in MODULI.items():
        table = {b: [] for b in range(1 << d)}
        for z in range(1 << d):
            table[gf_pow(z, 3, d, modulus)].append(z)
        assert all(len(xs) == 1 for xs in table.values())
        assertions += 1 << d

    for depth in [1, 2, 4, 8]:
        dims = [1 if j % 2 == 0 else 3 for j in range(depth)]
        row_layers = 0
        record_lengths = []
        for phase in range(4):
            record = encode_record(4, dims, phase)
            sw, decoded_dims, decoded_phase = decode_record(record)
            assert (sw, decoded_dims, decoded_phase) == (4, dims, phase)
            assertions += 1
            record_lengths.append(len(record))
            order = ("cube", "charge") if phase & 1 else ("charge", "cube")
            for source_value in range(16):
                source = transformed_source(bit_list(source_value, 4), phase)
                prefix = source[:]
                for layer, d in enumerate(dims):
                    matches, reconstructed, c, b = enumerate_layer(
                        prefix, d, layer, phase, order)
                    candidate_edges += 1 << len(graph(d).edges)
                    assert matches == [reconstructed]
                    assert sum(c) % 2 == 0
                    assert gf_pow(cotree(graph(d), reconstructed), 3, d, MODULI[d]) == b
                    assertions += 3
                    layer_witnesses += 1
                    row_layers += 1
                    prefix += bit_list(reconstructed, len(graph(d).edges))
                full_hierarchies += 1
                if depth == 2:
                    for name, truth in source_predicates(source).items():
                        accepted_models[name] += int(truth)
                        assertions += 1
        depth_rows.append({"depth": depth, "dimensions": dims,
                           "record_bytes": sorted(set(record_lengths)),
                           "layer_witnesses": row_layers})

    # A literal global truth table for depth [1,3], not just layerwise counts.
    global_candidates = 0
    global_unique = 0
    for phase in range(4):
        for source_value in range(16):
            source = transformed_source(bit_list(source_value, 4), phase)
            m1, _, _, _ = enumerate_layer(source, 1, 0, phase, ("charge", "cube"))
            count = 0
            for a1 in range(1 << len(graph(1).edges)):
                for a2 in range(1 << len(graph(3).edges)):
                    global_candidates += 1
                    if a1 not in m1:
                        continue
                    prefix = source + bit_list(a1, len(graph(1).edges))
                    b2 = target(prefix, 3, 1, phase)
                    c2 = charge(prefix, graph(3).vertices, 1)
                    if holds(graph(3), a2, c2, b2, 3, MODULI[3]):
                        count += 1
            assert count == 1
            assertions += 1
            global_unique += 1

    disc = disconnected_controls()
    assert disc == {"rho_formula": 1, "even_witnesses": 2,
                    "odd_isolate_witnesses": 0}
    assertions += 3

    malformed = [
        b"bad!" + bytes([4, 0, 0]),
        encode_record(4, [1, 3], 0) + b"\x00",
        encode_record(4, [1, 3], 0, [-1, 1]),
        bytes(MAGIC + bytes([4, 1, 0, 2, 0, 0, 255])),
        bytes(MAGIC + bytes([4, 1, 0, 3, 0, 0, 255])),
        bytes(MAGIC + bytes([0, 0, 0])),
    ]
    rejected = 0
    for record in malformed:
        try:
            decode_record(record)
        except ValueError:
            rejected += 1
    assert rejected == len(malformed)
    assertions += rejected

    # Constraint shuffling must preserve the unique solution.
    shuffled_checks = 0
    for _ in range(128):
        source = bit_list(rng.randrange(16), 4)
        phase = rng.randrange(4)
        d = rng.choice([1, 3])
        order = ["charge", "cube"]
        rng.shuffle(order)
        matches, reconstructed, _, _ = enumerate_layer(source, d, 0, phase, tuple(order))
        assert matches == [reconstructed]
        shuffled_checks += 1
        assertions += 1

    elapsed = time.perf_counter() - start
    return {
        "run_id": "HIERLIFT-TEST1",
        "status": "PASS",
        "seed": SEED,
        "assertions": assertions,
        "candidate_edge_assignments_checked": candidate_edges,
        "global_depth_two_candidates_checked": global_candidates,
        "global_unique_hierarchies": global_unique,
        "full_hierarchies_reconstructed": full_hierarchies,
        "layer_witnesses_reconstructed": layer_witnesses,
        "accepted_models_depth_two": accepted_models,
        "depth_rows": depth_rows,
        "disconnected_isolate_control": disc,
        "malformed_records_rejected": rejected,
        "shuffled_constraint_checks": shuffled_checks,
        "elapsed_seconds": elapsed,
        "method": "independent exhaustive edge truth tables plus explicit record round trips",
        "limitations": [
            "Finite checks do not prove asymptotic runtime bounds.",
            "The abstract composition theorem needs a polynomial decoder and per-layer extension algorithm.",
            "Hidden arbitrary renaming of an untagged CNF is not covered by the declared record decoder.",
            "The audit does not solve arbitrary nonlinear residuals, SAT, or MQ."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = run()
    result["code_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
