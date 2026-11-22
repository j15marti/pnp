"""Exact finite checks for the checkpoint observation-certificate accounting.

This audits LP duality, tape-route arithmetic, and disjoint phase accounting.
The hypergraphs are abstract: this is not a SAT-machine simulation or a test
that every solver reaches a checkpoint with the required opposite-label rivals.
Run: python residual_certificate_audit.py > residual_certificate_results.json
"""

from collections import deque
from fractions import Fraction as Q
from heapq import heappop, heappush
from itertools import combinations, product
import hashlib
import json
from pathlib import Path
import platform
import time


def solve(matrix, rhs):
    n = len(rhs)
    a = [[Q(v) for v in row] + [Q(b)] for row, b in zip(matrix, rhs)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            return None
        a[j], a[pivot] = a[pivot], a[j]
        scale = a[j][j]
        a[j] = [v / scale for v in a[j]]
        for i in range(n):
            if i != j:
                scale = a[i][j]
                a[i] = [x - scale * y for x, y in zip(a[i], a[j])]
    return tuple(a[i][-1] for i in range(n))


def cover_optimum(edges, costs):
    n = len(costs)
    constraints = [([int(i == j) for j in range(n)], 0) for i in range(n)]
    constraints += [([int(i in e) for i in range(n)], 1) for e in edges]
    best = None
    for active in combinations(constraints, n):
        x = solve([row for row, _ in active], [b for _, b in active])
        if x is None or any(v < 0 for v in x):
            continue
        if any(sum(x[i] for i in e) < 1 for e in edges):
            continue
        value = sum(c * v for c, v in zip(costs, x))
        if best is None or value < best:
            best = value
    assert best is not None
    return best


def packing_optimum(edges, capacities):
    n = len(capacities)
    best, witness = Q(0), tuple(Q(0) for _ in edges)
    for k in range(1, min(n, len(edges)) + 1):
        for selected in combinations(range(len(edges)), k):
            for active_cells in combinations(range(n), k):
                x = solve(
                    [[int(i in edges[j]) for j in selected] for i in active_cells],
                    [capacities[i] for i in active_cells],
                )
                if x is None or any(v < 0 for v in x):
                    continue
                if any(sum(x[t] for t, j in enumerate(selected) if i in edges[j]) > capacities[i]
                       for i in range(n)):
                    continue
                value = sum(x)
                if value > best:
                    best = value
                    w = [Q(0) for _ in edges]
                    for j, v in zip(selected, x):
                        w[j] = v
                    witness = tuple(w)
    return best, witness


def minimum_integral_cover(edges, costs):
    return min(sum(costs[i] for i in range(len(costs)) if mask >> i & 1)
               for mask in range(1 << len(costs))
               if all(any(mask >> i & 1 for i in e) for e in edges))


COORDINATES = (-2, 0, 3)
LEFT, RIGHT = min(COORDINATES), max(COORDINATES)


def add_scan(mask, position):
    if position in COORDINATES:
        mask |= 1 << COORDINATES.index(position)
    return mask


def covers(mask, edges):
    return all(any(mask >> i & 1 for i in e) for e in edges)


def shortest_scan_route(edges, head, weighted=False):
    def price(i):
        return max(1, abs(i)) if weighted else 1
    start = (head, add_scan(0, head))
    distance = {start: price(head)}
    queue = [(price(head), start)]
    while queue:
        cost, state = heappop(queue)
        if cost != distance[state]:
            continue
        h, mask = state
        if covers(mask, edges):
            return cost
        for hh in (h - 1, h + 1):
            if not LEFT <= hh <= RIGHT:
                continue
            nxt = (hh, add_scan(mask, hh))
            value = cost + price(hh)
            if value < distance.get(nxt, 10**9):
                distance[nxt] = value
                heappush(queue, (value, nxt))
    raise AssertionError("No route")


def interval_floors(edges, head):
    time_floor, storage_floor = 10**9, 10**9
    for left in range(LEFT, head + 1):
        for right in range(head, RIGHT + 1):
            if all(any(left <= COORDINATES[i] <= right for i in e) for e in edges):
                time_floor = min(time_floor, 1 + right - left + min(head - left, right - head))
                storage_floor = min(storage_floor, sum(max(1, abs(i)) for i in range(left, right + 1)))
    return time_floor, storage_floor


def first_clear(edges, scans, begin):
    mask = 0
    for end in range(begin, len(scans)):
        mask = add_scan(mask, scans[end])
        if covers(mask, edges):
            return end + 1
    return None


def main():
    started = time.monotonic()
    all_edges = [frozenset(i for i in range(3) if mask >> i & 1) for mask in range(1, 8)]
    families = [tuple(e for j, e in enumerate(all_edges) if mask >> j & 1) for mask in range(1, 128)]
    counts = {"hypergraphs": len(families), "exact_lp_pairs": 0, "route_checks": 0,
              "potential_step_checks": 0, "complete_walk_checks": 0, "two_phase_checks": 0}
    optima = []
    for edges in families:
        answers = []
        for capacities in ((1, 1, 1), (2, 1, 3)):
            pack, weights = packing_optimum(edges, capacities)
            cover = cover_optimum(edges, capacities)
            integral = minimum_integral_cover(edges, capacities)
            assert pack == cover <= integral <= sum(capacities)
            assert all(sum(w for e, w in zip(edges, weights) if i in e) <= capacities[i] for i in range(3))
            counts["exact_lp_pairs"] += 1
            answers.append((pack, weights))
        optima.append(answers)
        for head in range(LEFT, RIGHT + 1):
            time_floor, storage_floor = interval_floors(edges, head)
            assert shortest_scan_route(edges, head) == time_floor
            assert shortest_scan_route(edges, head, weighted=True) >= storage_floor
            counts["route_checks"] += 1

    for moves in product((-1, 0, 1), repeat=5):
        scans = [0]
        for move in moves:
            scans.append(scans[-1] + move)
        if any(not LEFT <= p <= RIGHT for p in scans):
            continue
        for edges, answers in zip(families, optima):
            for weighted, (value, weights) in enumerate(answers):
                unhit = set(range(len(edges)))
                potential = value
                cost = 0
                for position in scans:
                    capacity = max(1, abs(position)) if weighted else 1
                    newly_hit = {j for j in unhit if any(COORDINATES[i] == position for i in edges[j])}
                    decrease = sum(weights[j] for j in newly_hit)
                    assert 0 <= decrease <= capacity
                    unhit -= newly_hit
                    potential -= decrease
                    cost += capacity
                    assert potential == sum(weights[j] for j in unhit)
                    counts["potential_step_checks"] += 1
                if not unhit:
                    assert value <= cost
                    counts["complete_walk_checks"] += 1

    scans = tuple(range(LEFT, RIGHT + 1)) + tuple(range(RIGHT - 1, LEFT - 1, -1))
    for i, first in enumerate(families):
        middle = first_clear(first, scans, 0)
        assert middle is not None
        for j, second in enumerate(families):
            end = first_clear(second, scans, middle)
            if end is not None:
                assert optima[i][0][0] <= middle
                assert optima[j][0][0] <= end - middle
                assert optima[i][0][0] + optima[j][0][0] <= end
                counts["two_phase_checks"] += 1

    # Exact examples: triangle overlap, independent edges, and a common cache cell.
    triangle = (frozenset((0, 1)), frozenset((1, 2)), frozenset((0, 2)))
    assert packing_optimum(triangle, (1, 1, 1))[0] == Q(3, 2)
    assert minimum_integral_cover(triangle, (1, 1, 1)) == 2
    cached = (frozenset((0, 2)), frozenset((1, 2)))
    assert packing_optimum(cached, (1, 1, 1))[0] == 1
    independent = (frozenset((0,)), frozenset((1,)), frozenset((2,)))
    assert packing_optimum(independent, (1, 1, 1))[0] == 3

    return {"status": "PASS", "python": platform.python_version(), "counts": counts,
            "exact_examples": {"triangle_fractional": "3/2", "triangle_integral": 2,
                               "independent": 3, "common_cache": 1},
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "elapsed_seconds": time.monotonic() - started,
            "scope": "Exact rational LP, geometric observation relaxation, and abstract disjoint-phase accounting only. No SAT-machine reachability, arbitrary-solver recurrence, Kolmogorov complexity, or asymptotic empirical certification."}


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
