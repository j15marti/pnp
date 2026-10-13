#!/usr/bin/env python3
"""EQSPECTRAL1: bounded audit of a connected balanced-support repair.

This is a hostile-control experiment, not a lower-bound experiment.  Each
invocation enforces a cooperative 25-second deadline.  Run the source batch
and the two target batches separately.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
import hashlib
import json
import random
import time
from pathlib import Path

import universal22 as u
import image22_decoder_audit as d

RUN_ID = "EQSPECTRAL1"
START = time.monotonic()
DEADLINE = START + 25.0
COUNTS: Counter[str] = Counter()


def check(ok: bool, group: str) -> None:
    if time.monotonic() > DEADLINE:
        raise TimeoutError("cooperative 25-second budget exceeded")
    COUNTS[group] += 1
    if not ok:
        raise AssertionError((group, COUNTS[group]))


def planted(r: int) -> tuple[int, set[tuple[int, int]], list[int]]:
    """Connected 6-regular equitable 3-partite graph on 21r vertices."""
    t = 7 * r
    edges: set[tuple[int, int]] = set()
    for a, b in ((0, 1), (0, 2), (1, 2)):
        for shift in (0, 1, 2):
            for i in range(t):
                x, y = a * t + i, b * t + (i + shift) % t
                edges.add((min(x, y), max(x, y)))
    colors = [v // t for v in range(3 * t)]
    return 3 * t, edges, colors


def k7_ring(r: int) -> tuple[int, set[tuple[int, int]]]:
    """Connected 6-regular graph made from 3r K7 blocks by degree-preserving switches."""
    k = 3 * r
    edges: set[tuple[int, int]] = set()
    for block in range(k):
        base = 7 * block
        for a in range(7):
            for b in range(a + 1, 7):
                edges.add((base + a, base + b))
        edges.remove((base + 4, base + 5))
    for block in range(k):
        x = 7 * block + 4
        y = 7 * ((block + 1) % k) + 5
        edges.add((min(x, y), max(x, y)))
    return 7 * k, edges


def degrees(n: int, edges: set[tuple[int, int]]) -> list[int]:
    deg = [0] * n
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    return deg


def connected(n: int, edges: set[tuple[int, int]]) -> bool:
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    seen = {0}
    q = deque([0])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                q.append(y)
    return len(seen) == n


def matrix_plus_three(n: int, edges: set[tuple[int, int]]) -> list[list[int]]:
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        A[i][i] = 3
    for a, b in edges:
        A[a][b] = A[b][a] = 1
    return A


def rank_mod(A: list[list[int]], p: int) -> int:
    M = [[x % p for x in row] for row in A]
    m, n = len(M), len(M[0]) if M else 0
    rank = 0
    for col in range(n):
        pivot = next((i for i in range(rank, m) if M[i][col]), None)
        if pivot is None:
            continue
        M[rank], M[pivot] = M[pivot], M[rank]
        inv = pow(M[rank][col], p - 2, p)
        M[rank] = [(x * inv) % p for x in M[rank]]
        for i in range(m):
            if i != rank and M[i][col]:
                f = M[i][col]
                M[i] = [(x - f * y) % p for x, y in zip(M[i], M[rank])]
        rank += 1
        if rank == m:
            break
    return rank


def matvec(A: list[list[int]], x: list[int]) -> list[int]:
    return [sum(a * b for a, b in zip(row, x)) for row in A]


def permute_graph(n: int, edges: set[tuple[int, int]], rng: random.Random):
    pi = list(range(n))
    rng.shuffle(pi)
    out = {(min(pi[a], pi[b]), max(pi[a], pi[b])) for a, b in edges}
    return out


def proper_colouring(n: int, edges: set[tuple[int, int]]) -> u.CNF:
    return u.properize23(u.colouring_cnf(n, edges))[0]


def recover_six_regular_colouring_prefix(B: u.CNF):
    """Recognize F=properize23(colouring_cnf(G)) as a prefix of B.

    The support under test is 6-regular, hence F has exactly 25n clauses.
    Full balancing equality prevents acceptance of an accidental prefix.
    """
    n = 0
    while n < len(B) and B[n] == (3*n + 1, 3*n + 2, 3*n + 3):
        n += 1
    if n == 0 or len(B) < 25 * n:
        return None
    F = B[:25 * n]
    if u.balance(F)[0] != B:
        return None
    pairs = []
    rest = F[n:]
    if len(rest) % 2:
        return None
    for i in range(0, len(rest), 2):
        a, b = rest[i], rest[i + 1]
        if len(a) != 3 or a[:2] != b[:2] or a[2] != -b[2] or a[0] >= 0 or a[1] >= 0:
            return None
        pairs.append(a[:2])
    expected_vertex = []
    for v in range(n):
        ids = [3*v + k + 1 for k in range(3)]
        expected_vertex.extend([(-ids[0], -ids[1]), (-ids[0], -ids[2]), (-ids[1], -ids[2])])
    if pairs[:3*n] != expected_vertex:
        return None
    epairs = pairs[3*n:]
    if len(epairs) != 9*n or len(epairs) % 3:
        return None
    edges: list[tuple[int, int]] = []
    for i in range(0, len(epairs), 3):
        triple = epairs[i:i+3]
        uv = []
        for color, (a, b) in enumerate(triple):
            aa, bb = -a - 1, -b - 1
            if aa % 3 != color or bb % 3 != color:
                return None
            uv.append((aa // 3, bb // 3))
        if not (uv[0] == uv[1] == uv[2]):
            return None
        x, y = uv[0]
        if not (0 <= x < y < n):
            return None
        edges.append((x, y))
    E = set(edges)
    if len(E) != 3*n or degrees(n, E) != [6] * n:
        return None
    if proper_colouring(n, E) != F:
        return None
    return n, E


def separator_graph(n: int, edges: set[tuple[int, int]]) -> int | None:
    if not connected(n, edges) or degrees(n, edges) != [6] * n:
        return None
    A = matrix_plus_three(n, edges)
    nullity = n - rank_mod(A, 1_000_003)
    if nullity >= 2:
        return 1
    if nullity == 0:
        return 0
    return None


def separator_target(payload: bytes) -> int | None:
    decoded = d.decode_image(payload)
    if decoded is None:
        return None
    recovered = recover_six_regular_colouring_prefix(decoded.balanced)
    if recovered is None:
        return None
    return separator_graph(*recovered)


def source_batch() -> dict:
    rows = []
    rng = random.Random(20261013)
    for r in range(1, 9):
        ny, Ey, colors = planted(r)
        nn, En = k7_ring(r)
        check(ny == nn == 21*r, "matched_vertices")
        check(len(Ey) == len(En) == 63*r, "matched_edges")
        check(degrees(ny, Ey) == degrees(nn, En) == [6] * ny, "matched_degrees")
        check(connected(ny, Ey) and connected(nn, En), "connected")
        check(all(colors[a] != colors[b] for a, b in Ey), "yes_colouring")
        for block in range(3*r):
            core = [7*block + x for x in (0, 1, 2, 3)]
            check(all((min(a,b),max(a,b)) in En for i,a in enumerate(core) for b in core[i+1:]), "no_k4")
        Ay = matrix_plus_three(ny, Ey)
        t = 7*r
        v1 = [1]*t + [-1]*t + [0]*t
        v2 = [1]*t + [0]*t + [-1]*t
        check(matvec(Ay, v1) == [0]*ny and matvec(Ay, v2) == [0]*ny, "yes_minus3_kernel")
        An = matrix_plus_three(nn, En)
        check(rank_mod(An, 1_000_003) == nn, "no_minus3_kernel")
        check(separator_graph(ny, Ey) == 1 and separator_graph(nn, En) == 0, "separator")
        if r <= 4:
            for _ in range(4):
                check(separator_graph(ny, permute_graph(ny, Ey, rng)) == 1, "yes_relabel")
                check(separator_graph(nn, permute_graph(nn, En, rng)) == 0, "no_relabel")
        rows.append({"r": r, "vertices": ny, "edges": len(Ey), "yes_nullity_lower_bound": 2,
                     "no_rank_mod_1000003": nn, "compiler_variables": 4572*ny,
                     "compiler_clauses": 6096*ny})
    # Off-support connected 6-regular circulant: the separator may say either label,
    # so the support recognizer must be kept distinct from an L22 decider.
    n = 22
    Ec = {(min(i,(i+s)%n), max(i,(i+s)%n)) for i in range(n) for s in (1,2,3)}
    check(connected(n, Ec) and degrees(n, Ec) == [6]*n, "off_support_graph")
    return {"rows": rows, "off_support_label": separator_graph(n, Ec)}


def target_batch(kind: str) -> dict:
    n, edges = planted(1)[:2] if kind == "yes" else k7_ring(1)
    F = proper_colouring(n, edges)
    comp = u.compile22(F)
    payload = d.encode(comp.clauses)
    check(separator_target(payload) == (1 if kind == "yes" else 0), "target_separator")
    decoded = d.decode_image(payload)
    check(decoded is not None and recover_six_regular_colouring_prefix(decoded.balanced) == (n, edges), "target_recovery")
    swapped = list(comp.clauses)
    swapped[0], swapped[1] = swapped[1], swapped[0]
    check(separator_target(d.encode(swapped)) is None, "clause_permutation_off_image")
    check(separator_target(payload + b" ") is None, "malformed_encoding")
    return {"kind": kind, "graph_vertices": n, "graph_edges": len(edges),
            "source_clauses": len(F), "balanced_clauses": len(decoded.balanced),
            "target_variables": comp.n, "target_clauses": len(comp.clauses),
            "encoded_bytes": len(payload), "label": separator_target(payload)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", choices=("source", "target_yes", "target_no"), required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    detail = source_batch() if args.batch == "source" else target_batch(args.batch.split("_")[1])
    result = {"run_id": RUN_ID, "batch": args.batch, "status": "COMPUTATIONAL",
              "assertions": sum(COUNTS.values()), "checks": dict(COUNTS),
              "elapsed_seconds": time.monotonic() - START, "failures": 0,
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "detail": detail,
              "limits": ["Finite checks do not prove asymptotic hardness.",
                         "The separator decides only the declared two-support promise.",
                         "The exact symbolic nullity argument is proved separately in the report."]}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
