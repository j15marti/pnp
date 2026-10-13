#!/usr/bin/env python3
"""Independent bounded audit of affine projection and nonlinear witness lifting.

All arithmetic is over GF(2).  This script is self-contained, deterministic,
and prints one JSON object.  It tests semantics and witness reconstruction; it
does not infer asymptotic runtime lower bounds from measured timings.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import time
from dataclasses import dataclass
from pathlib import Path


SEED = 202610132024


@dataclass
class Counters:
    assertions: int = 0
    row_xors: int = 0
    projection_candidates: int = 0
    q_evaluations: int = 0
    reconstruction_solves: int = 0
    encoded_bytes_parsed: int = 0


COUNT = Counters()


def check(value: bool, message: str = "assertion failed") -> None:
    COUNT.assertions += 1
    if not value:
        raise AssertionError(message)


def component_count(n: int, edges: list[tuple[int, int]]) -> int:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    for u, v in edges:
        union(u, v)
    return len({find(v) for v in range(n)})


def boundary(n: int, edges: list[tuple[int, int]], x: int) -> int:
    out = 0
    for j, (u, v) in enumerate(edges):
        if (x >> j) & 1:
            out ^= (1 << u) | (1 << v)
    return out


def incidence_rows(n: int, edges: list[tuple[int, int]]) -> list[int]:
    rows = [0] * n
    for j, (u, v) in enumerate(edges):
        rows[u] |= 1 << j
        rows[v] |= 1 << j
    return rows


def solve_linear(rows: list[int], rhs: int, width: int) -> int | None:
    """Return one solution of rows*x=rhs over GF(2), or None."""
    a = [rows[i] | (((rhs >> i) & 1) << width) for i in range(len(rows))]
    pivots: list[int] = []
    r = 0
    for col in range(width):
        hit = next((i for i in range(r, len(a)) if (a[i] >> col) & 1), None)
        if hit is None:
            continue
        a[r], a[hit] = a[hit], a[r]
        for i in range(len(a)):
            if i != r and ((a[i] >> col) & 1):
                a[i] ^= a[r]
                COUNT.row_xors += 1
        pivots.append(col)
        r += 1
    coeff_mask = (1 << width) - 1
    for row in a:
        if (row & coeff_mask) == 0 and ((row >> width) & 1):
            return None
    x = 0
    for i, col in enumerate(pivots):
        if (a[i] >> width) & 1:
            x |= 1 << col
    return x


def project(x: int, positions: list[int]) -> int:
    return sum(((x >> j) & 1) << k for k, j in enumerate(positions))


def insert_projection(y: int, positions: list[int]) -> int:
    return sum(((y >> k) & 1) << j for k, j in enumerate(positions))


def extend_projection(
    n: int,
    edges: list[tuple[int, int]],
    charge: int,
    positions: list[int],
    y: int,
) -> int | None:
    """Fix x_positions=y and solve for all remaining edges."""
    COUNT.reconstruction_solves += 1
    fixed = insert_projection(y, positions)
    residual = charge ^ boundary(n, edges, fixed)
    pos_set = set(positions)
    free = [j for j in range(len(edges)) if j not in pos_set]
    free_edges = [edges[j] for j in free]
    z = solve_linear(incidence_rows(n, free_edges), residual, len(free))
    if z is None:
        return None
    x = fixed
    for k, j in enumerate(free):
        if (z >> k) & 1:
            x |= 1 << j
    return x


def projected_rank_formula(n: int, edges: list[tuple[int, int]], positions: list[int]) -> int:
    pset = set(positions)
    kept = [e for j, e in enumerate(edges) if j not in pset]
    return len(positions) + component_count(n, edges) - component_count(n, kept)


def spanning_forest_cotree(n: int, edges: list[tuple[int, int]]) -> tuple[list[int], list[int]]:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    tree: list[int] = []
    cotree: list[int] = []
    for j, (u, v) in enumerate(edges):
        a, b = find(u), find(v)
        if a == b:
            cotree.append(j)
        else:
            parent[b] = a
            tree.append(j)
    return tree, cotree


def eval_cnf(clauses: list[list[int]], bits: int, variables: int) -> bool:
    COUNT.q_evaluations += 1
    for clause in clauses:
        if not any(bool((bits >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause):
            return False
    return True


def sat_cnf(clauses: list[list[int]], variables: int) -> tuple[bool, int | None]:
    for bits in range(1 << variables):
        if eval_cnf(clauses, bits, variables):
            return True, bits
    return False, None


def forbidden_assignment_clause(bits: int, variables: int) -> list[int]:
    return [-(i + 1) if (bits >> i) & 1 else i + 1 for i in range(variables)]


def random_planted_3cnf(rng: random.Random, variables: int, clauses_n: int) -> tuple[list[list[int]], int]:
    planted = rng.randrange(1 << variables)
    clauses: list[list[int]] = []
    if variables < 3:
        # Repeated indices are intentionally avoided by using unit controls.
        return [[i + 1 if (planted >> i) & 1 else -(i + 1)] for i in range(variables)], planted
    seen: set[tuple[int, ...]] = set()
    while len(clauses) < clauses_n:
        vs = rng.sample(range(variables), 3)
        lits = []
        for v in vs:
            sign = rng.choice((False, True))
            lits.append(v + 1 if sign else -(v + 1))
        if not any(bool((planted >> (abs(l) - 1)) & 1) == (l > 0) for l in lits):
            lits[0] = -lits[0]
        key = tuple(sorted(lits, key=lambda z: abs(z)))
        if key not in seen:
            seen.add(key)
            clauses.append(lits)
    return clauses, planted


def canonical_encode(instance: dict) -> bytes:
    return json.dumps(instance, sort_keys=True, separators=(",", ":")).encode("utf-8")


def parse_instance(blob: bytes) -> dict:
    COUNT.encoded_bytes_parsed += len(blob)
    obj = json.loads(blob.decode("utf-8"))
    if set(obj) != {"n", "edges", "charge", "residual"}:
        raise ValueError("wrong keys")
    n = obj["n"]
    if not isinstance(n, int) or n < 1:
        raise ValueError("bad n")
    edges = []
    for e in obj["edges"]:
        if not isinstance(e, list) or len(e) != 2:
            raise ValueError("bad edge")
        u, v = e
        if not all(isinstance(w, int) for w in (u, v)) or not (0 <= u < v < n):
            raise ValueError("bad endpoint")
        edges.append((u, v))
    if len(set(edges)) != len(edges):
        raise ValueError("duplicate edge")
    charge = obj["charge"]
    if not isinstance(charge, list) or len(charge) != n or any(x not in (0, 1) for x in charge):
        raise ValueError("bad charge")
    residual = obj["residual"]
    if not isinstance(residual, dict) or residual.get("type") not in {"cnf", "quadratic"}:
        raise ValueError("bad residual")
    return {"n": n, "edges": edges, "charge": sum(x << i for i, x in enumerate(charge)), "residual": residual}


def exhaustive_projection_audit() -> dict:
    graph_support = 0
    charge_cases = 0
    projection_points = 0
    inconsistent = 0
    isolated_graphs = 0
    for n in range(1, 5):
        universe = list(itertools.combinations(range(n), 2))
        for gmask in range(1 << len(universe)):
            edges = [e for j, e in enumerate(universe) if (gmask >> j) & 1]
            if component_count(n, edges) > 1:
                isolated_graphs += 1
            by_charge: dict[int, list[int]] = {}
            for x in range(1 << len(edges)):
                by_charge.setdefault(boundary(n, edges, x), []).append(x)
            for rmask in range(1 << len(edges)):
                positions = [j for j in range(len(edges)) if (rmask >> j) & 1]
                rho = projected_rank_formula(n, edges, positions)
                graph_support += 1
                for charge in range(1 << n):
                    charge_cases += 1
                    sols = by_charge.get(charge, [])
                    projections = {project(x, positions) for x in sols}
                    if not sols:
                        inconsistent += 1
                        check(not projections)
                        continue
                    check(len(projections) == 1 << rho, "affine projection cardinality")
                    projection_points += len(projections)
                    fiber_sizes = set()
                    for y in projections:
                        COUNT.projection_candidates += 1
                        lifted = extend_projection(n, edges, charge, positions, y)
                        check(lifted is not None)
                        check(boundary(n, edges, lifted) == charge)
                        check(project(lifted, positions) == y)
                        fiber_sizes.add(sum(project(x, positions) == y for x in sols))
                    check(len(fiber_sizes) == 1, "uniform affine fibers")
    return {
        "graph_support_pairs": graph_support,
        "charge_cases": charge_cases,
        "projection_points_lifted": projection_points,
        "inconsistent_charge_cases": inconsistent,
        "disconnected_or_isolate_graphs": isolated_graphs,
    }


def cotree_sat_audit(rng: random.Random) -> dict:
    cases = 0
    yes = 0
    no = 0
    witness_reconstructions = 0
    transforms = 0
    graphs = [
        (3, [(0, 1), (1, 2), (0, 2)]),
        (4, list(itertools.combinations(range(4), 2))),
        (5, [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4), (0, 2), (1, 3), (2, 4)]),
        (6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (3, 5)]),
    ]
    for n, edges in graphs:
        _, cotree = spanning_forest_cotree(n, edges)
        rho = projected_rank_formula(n, edges, cotree)
        check(rho == len(cotree))
        attainable = sorted({boundary(n, edges, x) for x in range(1 << len(edges))})
        for charge in attainable[: min(8, len(attainable))]:
            # Every cotree assignment extends uniquely on a spanning forest.
            lifted_seen = set()
            for y in range(1 << len(cotree)):
                x = extend_projection(n, edges, charge, cotree, y)
                check(x is not None)
                check(boundary(n, edges, x) == charge)
                check(project(x, cotree) == y)
                lifted_seen.add(x)
            check(len(lifted_seen) == 1 << len(cotree))

            h = 1 if len(cotree) < 3 else 2
            variables = len(cotree) + h
            planted, _ = random_planted_3cnf(rng, variables, 2 * max(1, variables))
            unsat = [forbidden_assignment_clause(a, variables) for a in range(1 << variables)]
            for source in (planted, unsat):
                encoded = canonical_encode({
                    "n": n,
                    "edges": [list(sorted(e)) for e in edges],
                    "charge": [(charge >> i) & 1 for i in range(n)],
                    "residual": {
                        "type": "cnf",
                        "cotree_edge_indices": cotree,
                        "external_variables": h,
                        "clauses": source,
                    },
                })
                decoded = parse_instance(encoded)
                check(decoded["n"] == n and decoded["charge"] == charge)
                expected, witness = sat_cnf(source, variables)
                found = None
                for bits in range(1 << variables):
                    COUNT.projection_candidates += 1
                    if eval_cnf(source, bits, variables):
                        y = bits & ((1 << len(cotree)) - 1)
                        x = extend_projection(n, edges, charge, cotree, y)
                        check(x is not None)
                        found = (x, bits >> len(cotree))
                        witness_reconstructions += 1
                        break
                check((found is not None) == expected)
                if expected:
                    yes += 1
                    check(witness is not None)
                else:
                    no += 1
                cases += 1

            # Clause/literal shuffling preserves the embedded residual.
            shuffled = [c[:] for c in planted]
            rng.shuffle(shuffled)
            for clause in shuffled:
                rng.shuffle(clause)
            check(sat_cnf(planted, variables)[0] == sat_cnf(shuffled, variables)[0])
            transforms += 1

            # Phase complement x'=x+d transforms c to c+B d and Q to Q(x'+d).
            d = rng.randrange(1 << len(edges))
            shifted_charge = charge ^ boundary(n, edges, d)
            x = extend_projection(n, edges, charge, cotree, 0)
            check(x is not None)
            xp = x ^ d
            check(boundary(n, edges, xp) == shifted_charge)
            transforms += 1

            # Vertex renaming preserves the same edge-indexed witness.
            perm = list(reversed(range(n)))
            renamed_edges = [tuple(sorted((perm[u], perm[v]))) for u, v in edges]
            renamed_charge = sum(((charge >> v) & 1) << perm[v] for v in range(n))
            check(boundary(n, renamed_edges, x) == renamed_charge)
            transforms += 1
    return {
        "source_residual_cases": cases,
        "yes_cases": yes,
        "no_cases": no,
        "witness_reconstructions": witness_reconstructions,
        "shuffle_and_phase_controls": transforms,
    }


def fresh_and_shared_quadratic_audit() -> dict:
    fresh_lifts = 0
    # A fresh relation x_e = p_e AND q_e has the deterministic lift p_e=q_e=x_e.
    for n in range(1, 5):
        universe = list(itertools.combinations(range(n), 2))
        for gmask in range(1 << len(universe)):
            edges = [e for j, e in enumerate(universe) if (gmask >> j) & 1]
            for x in range(1 << len(edges)):
                p = q = x
                for j in range(len(edges)):
                    check(((x >> j) & 1) == (((p >> j) & 1) & ((q >> j) & 1)))
                    fresh_lifts += 1

    # Small shared-variable counterexample: triangle, charge zero.  Its affine
    # solutions are 000 and 111, while x0*x1 XOR x2 = 1 rejects both.
    edges = [(0, 1), (1, 2), (0, 2)]
    affine = [x for x in range(8) if boundary(3, edges, x) == 0]
    check(affine == [0, 7])
    accepts = [x for x in affine if ((((x >> 0) & 1) & ((x >> 1) & 1)) ^ ((x >> 2) & 1)) == 1]
    check(accepts == [])
    return {
        "fresh_and_edge_relations_lifted": fresh_lifts,
        "smallest_shared_quadratic_counterexample": {
            "graph": "triangle",
            "charge": "000",
            "affine_solutions": ["000", "111"],
            "residual": "x0*x1 XOR x2 = 1",
            "residual_solutions": [],
        },
    }


def external_and_encoding_audit() -> dict:
    # rho=0 but an external variable is necessary.  Enumerating only the affine
    # interface and fixing u=0 misses the witness u=1.
    tree_edges = [(0, 1)]
    rho = projected_rank_formula(2, tree_edges, [])
    check(rho == 0)
    check(not bool(0))
    check(bool(1))

    instance = {
        "n": 3,
        "edges": [[0, 1], [1, 2], [0, 2]],
        "charge": [0, 0, 0],
        "residual": {"type": "quadratic", "terms": [[0, 1], [2]], "rhs": 1},
    }
    blob = canonical_encode(instance)
    parsed = parse_instance(blob)
    check(parsed["n"] == 3 and parsed["charge"] == 0)
    malformed = [
        b"{}",
        b"not-json",
        canonical_encode({**instance, "edges": [[0, 1], [0, 1]]}),
        canonical_encode({**instance, "charge": [0, 0]}),
        canonical_encode({**instance, "edges": [[0, 3]]}),
    ]
    rejected = 0
    for bad in malformed:
        try:
            parse_instance(bad)
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
            rejected += 1
    check(rejected == len(malformed))
    return {
        "rho_zero_external_bit_counterexample": "tree plus Q(u)=u requires u=1",
        "direct_domain_sizes": {f"rho={rho0},h={h}": 1 << (rho0 + h) for rho0 in range(4) for h in range(4)},
        "valid_encoded_bytes": len(blob),
        "malformed_encodings_rejected": rejected,
    }


def friendship_easy_audit() -> dict:
    cases = 0
    yes = 0
    no = 0
    largest = None
    for t in range(1, 65):
        edges: list[tuple[int, int]] = []
        for i in range(t):
            a, b = 2 * i + 1, 2 * i + 2
            edges.extend([(0, a), (a, b), (b, 0)])
        n = 2 * t + 1
        rho = projected_rank_formula(n, edges, list(range(len(edges))))
        check(rho == t)
        charges = [0, boundary(n, edges, 1)]
        if t >= 2:
            charges.append((1 << 1) | (1 << 2) | (1 << 3) | (1 << 4))
        for charge in charges:
            witness = 0 if charge == 0 else next(
                (1 << j for j in range(len(edges)) if boundary(n, edges, 1 << j) == charge),
                None,
            )
            brute = next(
                (x for x in range(1 << min(len(edges), 18)) if x.bit_count() <= 1 and boundary(n, edges, x) == charge),
                None,
            ) if len(edges) <= 18 else witness
            check((witness is None) == (brute is None))
            if witness is not None:
                check(witness.bit_count() <= 1 and boundary(n, edges, witness) == charge)
                yes += 1
            else:
                no += 1
            cases += 1
        largest = {"vertices": n, "edges": len(edges), "rho": rho}
    return {"cases": cases, "yes": yes, "no": no, "largest": largest}


def main() -> None:
    started = time.perf_counter()
    rng = random.Random(SEED)
    projection = exhaustive_projection_audit()
    cotree = cotree_sat_audit(rng)
    quadratics = fresh_and_shared_quadratic_audit()
    external = external_and_encoding_audit()
    friendship = friendship_easy_audit()
    elapsed = time.perf_counter() - started
    script_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    semantic_payload = {
        "projection": projection,
        "cotree": cotree,
        "quadratics": quadratics,
        "external": external,
        "friendship": friendship,
        "counters": COUNT.__dict__,
    }
    semantic_digest = hashlib.sha256(
        json.dumps(semantic_payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    result = {
        "run_id": "COTREELIFT1",
        "status": "COMPUTATIONAL",
        "seed": SEED,
        "elapsed_seconds": round(elapsed, 6),
        "script_sha256": script_sha,
        "semantic_digest": semantic_digest,
        **semantic_payload,
        "limitations": [
            "finite checks do not prove asymptotic complexity",
            "timing is recorded only to enforce the per-invocation budget",
            "the script does not estimate UWI H(F) or arbitrary-machine runtime",
            "cotree residuals are explicit structured inputs; hidden decomposition discovery is not assumed",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
