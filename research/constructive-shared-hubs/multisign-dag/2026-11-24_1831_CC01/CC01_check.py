#!/usr/bin/env python3
"""CC01: exact, automatically discovered diamond-chain matching quotient.

Standard library only. Python 3.10+.
  python CC01_check.py --stage controls --out CC01_controls.json
  python CC01_check.py --stage scaling --out CC01_scaling.json
  python CC01_check.py --stage replay --prior /path/constructive_repair_series.py \
      --out CC01_replay.json

No unrestricted polynomial solver is claimed. Exhaustive enumeration is an
explicit small-kernel terminal and an independent small-source reference.
Edge-local guards are kept joint in four-state domains. Cross-edge guards on
eliminated internal variables are OUTSIDE this compiler's contract.
"""
from __future__ import annotations
import argparse
from collections import Counter, deque
import hashlib
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import random
import resource
import sys
import time
import tracemalloc

COUNTS = Counter()
ASSERTIONS = 0

def check(ok, message="verification failed"):
    global ASSERTIONS
    ASSERTIONS += 1
    if not ok:
        raise AssertionError(message)

def edge(u, v):
    return (u, v) if u <= v else (v, u)

class Graph:
    """Explicit edge IDs preserve parallel edges. A loop has two incidences."""
    def __init__(self, edges, vertices=None):
        self.edges = tuple(edge(*e) for e in edges)
        self.vertices = tuple(sorted(set(vertices or ()) |
                                     {v for e in self.edges for v in e}))
        self.adj = {v: [] for v in self.vertices}
        for i, (u, v) in enumerate(self.edges):
            self.adj[u].append(i)
            self.adj[v].append(i)

    def other(self, e, v):
        a, b = self.edges[e]
        return b if a == v else a

    def simple_cubic(self):
        return (len(set(self.edges)) == len(self.edges) and
                all(u != v for u, v in self.edges) and
                all(len(self.adj[v]) == 3 for v in self.vertices))

    def perfect(self, matching):
        deg = {v: 0 for v in self.vertices}
        for e in matching:
            if e < 0 or e >= len(self.edges):
                return False
            u, v = self.edges[e]
            if u == v:
                return False
            deg[u] += 1
            deg[v] += 1
        return all(x == 1 for x in deg.values())

    def digest(self):
        raw = json.dumps({"vertices": self.vertices, "edges": self.edges},
                         separators=(",", ":")).encode()
        return hashlib.sha256(raw).hexdigest()

def enumerate_matchings(g):
    """Exponential vertex-recursive reference, explicitly capped by callers."""
    def rec(left):
        COUNTS["matching_recursion_nodes"] += 1
        if not left:
            yield frozenset()
            return
        v = min(left)
        for e in g.adj[v]:
            w = g.other(e, v)
            if w != v and w in left:
                for tail in rec(left - {v, w}):
                    yield tail | {e}
    return list(rec(set(g.vertices)))

def source_clauses(g, costs):
    m = len(g.edges)
    clauses = []
    for c in range(2):
        for v in g.vertices:
            vs = sorted({1 + c*m + e for e in g.adj[v]
                         if g.edges[e][0] != g.edges[e][1]})
            clauses.append(tuple(vs))
            clauses.extend((-a, -b) for a, b in combinations(vs, 2))
    for e, (u, v) in enumerate(g.edges):
        if u == v:
            clauses.extend([(-(e+1),), (-(m+e+1),)])
        for q, cost in enumerate(costs[e]):
            if cost is None:
                # Forbid precisely the joint word q.
                clauses.append((-(e+1) if q & 1 else e+1,
                                -(m+e+1) if q & 2 else m+e+1))
    return clauses

def binary_closure(nvars, clauses):
    """Unit propagation + all forced literals in the current binary relaxation.

    Longer source clauses remain in the formula, are simplified after pins,
    and are never assumed solved by the binary relaxation. No branching.
    """
    COUNTS["closure_calls"] += 1
    assignment = {}
    equations = set()
    while True:
        COUNTS["closure_rounds"] += 1
        reduced = []
        units = []
        for clause in clauses:
            COUNTS["closure_clause_scans"] += 1
            if any(abs(l) in assignment and assignment[abs(l)] == (l > 0)
                   for l in clause):
                continue
            row = tuple(sorted(set(l for l in clause if abs(l) not in assignment)))
            if any(-l in row for l in row):
                continue
            if not row:
                return None, {"pins": len(assignment), "equations": len(equations)}
            reduced.append(row)
            if len(row) == 1:
                units.append(row[0])
        if units:
            for l in units:
                if abs(l) in assignment and assignment[abs(l)] != (l > 0):
                    return None, {"pins": len(assignment), "equations": len(equations)}
                assignment[abs(l)] = l > 0
            continue
        binary = [c for c in reduced if len(c) == 2]
        if all(all(l < 0 for l in c) for c in binary):
            # All-zero and each single-positive word certify no forced
            # literals/equivalences in this negative binary relaxation.
            COUNTS["negative_binary_fixed_points"] += 1
            break
        active = sorted({abs(l) for c in binary for l in c})
        adj = {l: set() for v in active for l in (v, -v)}
        for a, b in binary:
            adj[-a].add(b)
            adj[-b].add(a)
        reaches = {}
        for start in adj:
            seen = {start}
            todo = [start]
            while todo:
                a = todo.pop()
                for b in adj[a]:
                    COUNTS["closure_implication_scans"] += 1
                    if b not in seen:
                        seen.add(b)
                        todo.append(b)
            reaches[start] = seen
        newpins = []
        for v in active:
            pos_bad = -v in reaches[v]
            neg_bad = v in reaches[-v]
            if pos_bad and neg_bad:
                return None, {"pins": len(assignment), "equations": len(equations)}
            if pos_bad:
                newpins.append(-v)
            if neg_bad:
                newpins.append(v)
        # Register SCC equivalences without dropping the original clauses.
        for a in adj:
            for b in reaches[a]:
                if a < b and a in reaches[b]:
                    equations.add((a, b))
        if not newpins:
            break
        for l in newpins:
            assignment[abs(l)] = l > 0
    COUNTS["closure_pins"] += len(assignment)
    return assignment, {"pins": len(assignment), "equations": len(equations)}

def pin_costs(g, costs, assignments):
    out = [list(row) for row in costs]
    m = len(g.edges)
    for var, val in assignments.items():
        c, e = divmod(var-1, m)
        for q in range(4):
            if bool(q & (1 << c)) != val:
                out[e][q] = None
    return out

def discover(g):
    """Find every induced K4-minus-edge and partition maximal strings/rings.

    Source graph must be simple cubic. Private diamond interiors have no
    external observations other than their two actual incident boundary links.
    """
    check(g.simple_cubic(), "source is not simple cubic")
    nbs = {v: {g.other(e, v) for e in g.adj[v]} for v in g.vertices}
    eid = {e: i for i, e in enumerate(g.edges)}
    diamonds = []
    owner = {}
    for c, d in g.edges:
        COUNTS["discovery_edge_tests"] += 1
        common = sorted(nbs[c] & nbs[d])
        if len(common) != 2:
            continue
        a, b = common
        if b in nbs[a]:  # a whole K4 is retained as a constant-size core.
            continue
        vertices = (a, b, c, d)
        check(not any(v in owner for v in vertices), "diamonds overlap")
        k = len(diamonds)
        owner.update({v: k for v in vertices})
        internals = tuple(eid[edge(u, v)] for u, v in
                          ((a,c), (a,d), (b,c), (b,d), (c,d)))
        ext = {}
        for tip in (a, b):
            candidates = [e for e in g.adj[tip] if e not in internals]
            check(len(candidates) == 1)
            ext[tip] = candidates[0]
        # Options listed in the fixed five-edge ordering above.
        diamonds.append({"vertices": vertices, "edges": internals,
                         "external": ext,
                         "patterns": {0: ((1,0,0,1,0), (0,1,1,0,0)),
                                      1: ((0,0,0,0,1),)}})
    core_vertices = tuple(v for v in g.vertices if v not in owner)
    core_set = set(core_vertices)
    used_links = set()
    used_diamonds = set()
    chains = []
    for u in core_vertices:
        for first in g.adj[u]:
            if first in used_links:
                continue
            links, ds = [], []
            here, link = u, first
            while True:
                check(link not in used_links)
                used_links.add(link)
                links.append(link)
                there = g.other(link, here)
                if there in core_set:
                    chains.append({"endpoints": (u, there),
                                   "links": links, "diamonds": ds})
                    break
                k = owner[there]
                check(k not in used_diamonds)
                used_diamonds.add(k)
                ds.append(k)
                a, b, _, _ = diamonds[k]["vertices"]
                check(there in (a, b))
                here = b if there == a else a
                link = diamonds[k]["external"][here]
    rings = []
    for k in range(len(diamonds)):
        if k in used_diamonds:
            continue
        start = diamonds[k]["vertices"][0]
        here = start
        ds, links = [], []
        while True:
            k2 = owner[here]
            check(k2 not in used_diamonds)
            used_diamonds.add(k2)
            ds.append(k2)
            a, b, _, _ = diamonds[k2]["vertices"]
            check(here in (a, b))
            leave = b if here == a else a
            link = diamonds[k2]["external"][leave]
            check(link not in used_links)
            used_links.add(link)
            links.append(link)
            here = g.other(link, leave)
            if here == start:
                break
        rings.append({"endpoints": None, "links": links, "diamonds": ds})
    ownership = Counter(used_links)
    for d in diamonds:
        ownership.update(d["edges"])
    check(set(ownership) == set(range(len(g.edges))))
    check(all(v == 1 for v in ownership.values()))
    check(len(used_diamonds) == len(diamonds))
    core = Graph([c["endpoints"] for c in chains], core_vertices)
    check(all(len(core.adj[v]) == 3 for v in core.vertices))
    return {"core": core, "diamonds": diamonds, "chains": chains, "rings": rings}

def local_entries(diamond, costs):
    entries = []
    for q in range(4):
        best = None
        best_pattern = None
        all_count = 0
        opt_count = 0
        for p, r in product(diamond["patterns"][int(bool(q & 1))],
                            diamond["patterns"][int(bool(q & 2))]):
            COUNTS["diamond_option_evaluations"] += 1
            mask = tuple(a+2*b for a, b in zip(p, r))
            values = [costs[e][s] for e, s in zip(diamond["edges"], mask)]
            if any(v is None for v in values):
                continue
            cost = sum(values)
            all_count += 1
            if best is None or cost < best:
                best, best_pattern, opt_count = cost, mask, 1
            elif cost == best:
                opt_count += 1
        entries.append(None if best is None else
                       {"cost": best, "all": all_count, "optimal": opt_count,
                        "pattern": best_pattern})
    return entries

def project(discovery, costs):
    local = [local_entries(d, costs) for d in discovery["diamonds"]]
    def table(block):
        entries = []
        for q in range(4):
            COUNTS["block_boundary_entries"] += 1
            link_cost = [costs[e][q] for e in block["links"]]
            ds = [local[k][q] for k in block["diamonds"]]
            if any(c is None for c in link_cost) or any(d is None for d in ds):
                entries.append(None)
                continue
            c = sum(link_cost) + sum(d["cost"] for d in ds)
            total, optimal = 1, 1
            for d in ds:
                total *= d["all"]
                optimal *= d["optimal"]
            entries.append({"cost": c, "all": total, "optimal": optimal})
        return entries
    return {"chain_tables": [table(c) for c in discovery["chains"]],
            "ring_tables": [table(c) for c in discovery["rings"]],
            "local": local}

def lift(g, discovery, projected, chain_states, ring_states):
    masks = {}
    for block, q in zip(discovery["chains"] + discovery["rings"],
                        list(chain_states) + list(ring_states)):
        for e in block["links"]:
            check(e not in masks)
            masks[e] = q
        for k in block["diamonds"]:
            row = projected["local"][k][q]
            check(row is not None)
            for e, s in zip(discovery["diamonds"][k]["edges"], row["pattern"]):
                check(e not in masks)
                masks[e] = s
    check(len(masks) == len(g.edges))
    a = frozenset(e for e, q in masks.items() if q & 1)
    b = frozenset(e for e, q in masks.items() if q & 2)
    check(g.perfect(a) and g.perfect(b), "lift is not a pair of matchings")
    return a, b

def pair_cost(costs, a, b):
    total = 0
    for e, row in enumerate(costs):
        value = row[int(e in a)+2*int(e in b)]
        if value is None:
            return None
        total += value
    return total

def exhaustive_kernel(core, tables):
    """Small-kernel exact backend, not a universal polynomial algorithm."""
    matchings = enumerate_matchings(core)
    best, total, optimal, best_states = None, 0, 0, None
    for a in matchings:
        for b in matchings:
            COUNTS["kernel_matching_pair_checks"] += 1
            states = [int(e in a)+2*int(e in b) for e in range(len(core.edges))]
            entries = [t[q] for t, q in zip(tables, states)]
            if any(x is None for x in entries):
                continue
            c = sum(x["cost"] for x in entries)
            ca, co = 1, 1
            for x in entries:
                ca *= x["all"]
                co *= x["optimal"]
            total += ca
            if best is None or c < best:
                best, optimal, best_states = c, co, states
            elif c == best:
                optimal += co
    return {"best": best, "total": total, "optimal": optimal,
            "states": best_states, "matching_count": len(matchings)}

def bipartite_pair(core):
    """Deterministic augmenting paths, then alternate the even complement cycles."""
    parts = {}
    for root in core.vertices:
        if root in parts:
            continue
        parts[root] = 0
        todo = deque([root])
        while todo:
            v = todo.popleft()
            for e in core.adj[v]:
                w = core.other(e, v)
                if w in parts:
                    if parts[w] == parts[v]:
                        return None
                else:
                    parts[w] = 1-parts[v]
                    todo.append(w)
    mate = {}
    mate_edge = {}
    for root in [v for v in core.vertices if parts[v] == 0]:
        todo = deque([root])
        seen_left, seen_right, parent = {root}, set(), {}
        endpoint = None
        while todo and endpoint is None:
            u = todo.popleft()
            for e in core.adj[u]:
                COUNTS["augmenting_edge_scans"] += 1
                v = core.other(e, u)
                if v in seen_right:
                    continue
                seen_right.add(v)
                parent[v] = (u, e)
                if v not in mate:
                    endpoint = v
                    break
                w = mate[v]
                if w not in seen_left:
                    seen_left.add(w)
                    todo.append(w)
        if endpoint is None:
            return None
        v = endpoint
        while True:
            u, e = parent[v]
            old = mate.get(u)
            mate[u], mate[v] = v, u
            mate_edge[u] = mate_edge[v] = e
            if old is None:
                break
            v = old
    first = frozenset(mate_edge.values())
    if not core.perfect(first):
        return None
    remaining = set(range(len(core.edges))) - set(first)
    second = set()
    while remaining:
        initial = min(remaining)
        start, here = core.edges[initial][0], core.edges[initial][0]
        e, step = initial, 0
        while True:
            check(e in remaining)
            remaining.remove(e)
            if step % 2 == 0:
                second.add(e)
            step += 1
            here = core.other(e, here)
            if here == start:
                check(step % 2 == 0)
                break
            choices = [f for f in core.adj[here] if f in remaining]
            check(len(choices) == 1)
            e = choices[0]
    check(core.perfect(second) and not first & second)
    return first, frozenset(second)

def solve_projected(g, costs, small_limit=18, force_backend=None):
    pins, before = binary_closure(2*len(g.edges), source_clauses(g, costs))
    if pins is None:
        return {"status": "UNSAT", "best": None, "total": 0, "optimal": 0,
                "backend": "source_closure", "closure": before}
    costs = pin_costs(g, costs, pins)
    d = discover(g)
    p = project(d, costs)
    core = d["core"]
    kernel_costs = [[None if x is None else x["cost"] for x in t]
                    for t in p["chain_tables"]]
    kpins, after = binary_closure(2*len(core.edges), source_clauses(core, kernel_costs))
    info = {"source_vertices": len(g.vertices), "source_edges": len(g.edges),
            "core_vertices": len(core.vertices), "core_edges": len(core.edges),
            "diamonds": len(d["diamonds"]), "rings": len(d["rings"]),
            "source_digest": g.digest(), "closure_before": before,
            "closure_after": after}
    if kpins is None:
        return dict(info, status="UNSAT", best=None, total=0, optimal=0,
                    backend="kernel_closure")
    if kpins:
        restricted = pin_costs(core, kernel_costs, kpins)
        for t, allowed in zip(p["chain_tables"], restricted):
            for q in range(4):
                if allowed[q] is None:
                    t[q] = None
        # Certified fixed-point recheck after the deductions and at stagnation.
        check(binary_closure(2*len(core.edges),
                             source_clauses(core, restricted))[0] is not None)
    else:
        # Same immutable clauses, same fixed point archive. No free stronger closure.
        COUNTS["closure_archives_reused_at_stagnation"] += 1
    ring_states, ring_best, ring_all, ring_opt = [], 0, 1, 1
    for t in p["ring_tables"]:
        finite = [(q, x) for q, x in enumerate(t) if x is not None]
        if not finite:
            return dict(info, status="UNSAT", best=None, total=0, optimal=0,
                        backend="ring_table")
        q, x = min(finite, key=lambda qx: (qx[1]["cost"], qx[0]))
        ring_states.append(q)
        ring_best += x["cost"]
        ring_all *= sum(y["all"] for _, y in finite)
        ring_opt *= sum(y["optimal"] for _, y in finite if y["cost"] == x["cost"])
    if len(core.vertices) <= small_limit and force_backend != "bipartite":
        ans = exhaustive_kernel(core, p["chain_tables"])
        if ans["best"] is None:
            return dict(info, status="UNSAT", best=None, total=0, optimal=0,
                        backend="small_kernel", matching_count=ans["matching_count"])
        chain_states = ans["states"]
        best = ans["best"] + ring_best
        total = ans["total"] * ring_all
        optimal = ans["optimal"] * ring_opt
        backend = "small_kernel"
    else:
        # This is an unpinned disjoint-matching support terminal.
        # It does NOT solve arbitrary weighted or pinned bipartite instances.
        if not all(all(t[q] is not None for q in (0,1,2))
                   for t in p["chain_tables"]):
            return dict(info, status="UNKNOWN", backend="unsupported_guarded_core")
        pair = bipartite_pair(core)
        if pair is None:
            return dict(info, status="UNKNOWN", backend="nonbipartite_large_core")
        chain_states = [int(e in pair[0])+2*int(e in pair[1])
                        for e in range(len(core.edges))]
        best = sum(t[q]["cost"] for t, q in zip(p["chain_tables"], chain_states)) + ring_best
        total = optimal = None
        backend = "bipartite_constructive"
    a, b = lift(g, d, p, chain_states, ring_states)
    check(pair_cost(costs, a, b) == best)
    return dict(info, status="SAT", best=best, total=total, optimal=optimal,
                backend=backend, a=a, b=b, overlap=len(a & b),
                optimality_claimed=backend == "small_kernel")

def costs_for(g, reference=None, overlap_allowed=None, random_cost=None, pins=None):
    a, b = reference if reference is not None else (frozenset(), frozenset())
    rows = []
    for e in range(len(g.edges)):
        row = []
        for q in range(4):
            if overlap_allowed is not None and q == 3 and e not in overlap_allowed:
                row.append(None)
            elif pins and any(bool(q & (1 << c)) != value
                              for c, value in pins.get(e, [])):
                row.append(None)
            elif random_cost is not None:
                row.append(random_cost[e][q])
            elif reference is not None:
                row.append((int(e in a) ^ int(bool(q & 1))) +
                           (int(e in b) ^ int(bool(q & 2))))
            else:
                row.append(int(q == 3))
        rows.append(row)
    return rows

def dominance_certificate(g):
    """Direct witnesses in the actual duplicated literal conflict graph."""
    m = len(g.edges)
    adj = [set() for _ in range(2*m)]
    for c in range(2):
        for v in g.vertices:
            for e, f in combinations(g.adj[v], 2):
                if e != f:
                    adj[c*m+e].add(c*m+f)
                    adj[c*m+f].add(c*m+e)
    for e in range(m):
        adj[e].add(m+e)
        adj[m+e].add(e)
    attempts = 0
    for c in range(2):
        for v in g.vertices:
            for e in g.adj[v]:
                for f in g.adj[v]:
                    if e == f:
                        continue
                    # f's opposite-copy occurrence is outside this clause group.
                    witness = (1-c)*m+f
                    check(witness in adj[c*m+f] and witness not in adj[c*m+e])
                    check(not adj[c*m+f] <= adj[c*m+e])
                    attempts += 1
    e = 0
    v = g.edges[e][0]
    f = next(f for f in g.adj[v] if f != e)
    p3 = (m+e, e, f)
    check(p3[1] in adj[p3[0]] and p3[2] in adj[p3[1]]
          and p3[2] not in adj[p3[0]])
    return {"ordered_dominance_failures": attempts, "induced_path": p3,
            "conflict_vertices": 2*m}

def brute_source(g, costs):
    ms = enumerate_matchings(g)
    best, total, optimal, best_pair = None, 0, 0, None
    for a in ms:
        for b in ms:
            COUNTS["reference_pair_checks"] += 1
            c = pair_cost(costs, a, b)
            if c is None:
                continue
            total += 1
            if best is None or c < best:
                best, optimal, best_pair = c, 1, (a, b)
            elif c == best:
                optimal += 1
    return {"best": best, "total": total, "optimal": optimal,
            "pair": best_pair, "matching_count": len(ms)}

def inflate(base, lengths, ref=None):
    edges, manifest, nextv = [], [], max(base.vertices, default=-1)+1
    old_a, old_b = ref or (frozenset(), frozenset())
    aout, bout = set(), set()
    for eid, (u, v) in enumerate(base.edges):
        prev, links, ds = u, [], []
        for _ in range(lengths[eid]):
            a,b,c,d = range(nextv, nextv+4)
            nextv += 4
            links.append(len(edges)); edges.append(edge(prev,a))
            local = []
            for x,y in ((a,c),(a,d),(b,c),(b,d),(c,d)):
                local.append(len(edges)); edges.append(edge(x,y))
            ds.append(local)
            if eid in old_a:
                aout.add(local[4])
            else:
                aout.update((local[0], local[3]))
            if eid in old_b:
                bout.add(local[4])
            else:
                bout.update((local[1], local[2]))
            prev = b
        links.append(len(edges)); edges.append(edge(prev,v))
        if eid in old_a:
            aout.update(links)
        if eid in old_b:
            bout.update(links)
        manifest.append({"links": links, "diamonds": ds})
    result = Graph(edges)
    check(result.simple_cubic())
    if ref is not None:
        check(result.perfect(aout) and result.perfect(bout))
    return result, manifest, (frozenset(aout),frozenset(bout))

def relabel(g, rng):
    vertices = list(g.vertices)
    shuffled = vertices.copy()
    rng.shuffle(shuffled)
    p = dict(zip(vertices, shuffled))
    # Preserve edge indices so pins/costs continue to mean the actual edge.
    return Graph([edge(p[u],p[v]) for u,v in g.edges])

def k4():
    return Graph(list(combinations(range(4),2)))

def k33():
    return Graph([(i,3+j) for i in range(3) for j in range(3)])

def cube():
    return Graph(sorted({edge(i,i^(1<<b)) for i in range(8) for b in range(3)}))

def petersen():
    return Graph(sorted({edge(i,(i+1)%5) for i in range(5)} |
                        {edge(i,i+5) for i in range(5)} |
                        {edge(5+i,5+(i+2)%5) for i in range(5)}))

def trap():
    return Graph([(0,1),(0,4),(0,5),(1,2),(1,7),(2,3),
                  (2,6),(3,6),(3,7),(4,5),(4,7),(5,6)])

def trap_pair(g):
    es = {e:i for i,e in enumerate(g.edges)}
    return (frozenset(es[e] for e in [(0,4),(1,2),(3,7),(5,6)]),
            frozenset(es[e] for e in [(0,1),(2,3),(4,7),(5,6)]))

def random_cubic(n, rng):
    for _ in range(20000):
        stubs = [v for v in range(n) for _ in range(3)]
        rng.shuffle(stubs)
        es = [edge(stubs[i],stubs[i+1]) for i in range(0,3*n,2)]
        if all(a != b for a,b in es) and len(set(es)) == len(es):
            return Graph(sorted(es))
    raise RuntimeError("configuration generator exhausted cap")

def bipartite_family(p, rng):
    # Three permutations with no repeated edge. Identity and a shift ensure
    # connectivity; the third is a seeded perfect-matching permutation.
    perm = list(range(p))
    for _ in range(10000):
        rng.shuffle(perm)
        if all(perm[i] not in (i,(i+1)%p) for i in range(p)):
            break
    else:
        raise RuntimeError("bipartite generator exhausted cap")
    es = [(i,p+i) for i in range(p)]
    es += [(i,p+(i+1)%p) for i in range(p)]
    es += [(i,p+perm[i]) for i in range(p)]
    return Graph(es), frozenset(range(p))

def strip_witness(row):
    return {k:v for k,v in row.items() if k not in ("a","b")}

def control_stage():
    rng = random.Random(2082401)
    graph_cases = [k4(),k33(),cube(),petersen(),trap()]
    graph_cases += [random_cubic(n,rng) for n in (6,8,10,12,14) for _ in range(4)]
    dominance = []
    for g in graph_cases:
        d = dominance_certificate(g)
        closure, info = binary_closure(2*len(g.edges),
                                      source_clauses(g,costs_for(g,overlap_allowed=set())))
        check(closure == {} and info["equations"] == 0)
        dominance.append(dict(n=len(g.vertices), edges=g.edges, **d))

    # Independently enumerate 2^10 private words for random diamond tables.
    dg, _, _ = inflate(k33(), [1]+[0]*8)
    dec = discover(dg)
    diamond = dec["diamonds"][0]
    local_checks = []
    for case in range(80):
        costs = [[None if rng.randrange(7)==0 else rng.randrange(10) for _ in range(4)]
                 for e in dg.edges]
        got = local_entries(diamond,costs)
        expected = []
        for q in range(4):
            best, total, optimal = None,0,0
            for word in range(1<<10):
                bits = [(word>>i)&1 for i in range(10)]
                ok = True
                for c in range(2):
                    b = bits[5*c:5*c+5]
                    external = int(bool(q & (1<<c)))
                    degrees = [b[0]+b[1]+external, b[2]+b[3]+external,
                               b[0]+b[2]+b[4], b[1]+b[3]+b[4]]
                    if degrees != [1,1,1,1]:
                        ok=False;break
                if not ok:
                    continue
                masks=[bits[i]+2*bits[i+5] for i in range(5)]
                values=[costs[e][s] for e,s in zip(diamond["edges"],masks)]
                if any(x is None for x in values):
                    continue
                value=sum(values); total+=1
                if best is None or value<best:
                    best,optimal=value,1
                elif value==best:
                    optimal+=1
            expected.append(None if best is None else
                            {"cost":best,"all":total,"optimal":optimal})
        check([{k:v for k,v in x.items() if k!="pattern"} if x else None
               for x in got] == expected, "local table reference disagreement")
        local_checks.append(expected)

    global_cases = []
    for case in range(70):
        base = graph_cases[case % len(graph_cases)]
        # At most one new diamond keeps independent full-source enumeration bounded.
        lengths = [0]*len(base.edges)
        if case % 3:
            lengths[rng.randrange(len(lengths))]=1
        g, _, _ = inflate(base,lengths)
        g = relabel(g,rng)
        ms = enumerate_matchings(g)
        if not ms:
            continue
        mode = case % 5
        reference = (rng.choice(ms),rng.choice(ms))
        if mode == 0:
            costs=costs_for(g,overlap_allowed=set())
        elif mode == 1:
            costs=costs_for(g,reference=reference,overlap_allowed=set())
        elif mode == 2:
            allowed=set(reference[0]&reference[1])
            if allowed:
                allowed.remove(min(allowed))
            costs=costs_for(g,reference=reference,overlap_allowed=allowed)
        elif mode == 3:
            rc=[[rng.randrange(8) for _ in range(4)] for e in g.edges]
            pins={}
            for _ in range(3):
                pins.setdefault(rng.randrange(len(g.edges)),[]).append(
                    (rng.randrange(2),bool(rng.randrange(2))))
            costs=costs_for(g,random_cost=rc,pins=pins)
        else:
            costs=costs_for(g)
            # Preserve a genuine joint correlation, not just marginal pins.
            chosen=rng.randrange(len(g.edges))
            keep=(0,3) if case % 2 else (1,2)
            for q in range(4):
                if q not in keep:
                    costs[chosen][q]=None
        expected=brute_source(g,costs)
        got=solve_projected(g,costs,small_limit=18)
        check(got["status"] != "UNKNOWN")
        check((got["best"],got["total"],got["optimal"]) ==
              (expected["best"],expected["total"],expected["optimal"]),
              "full-source projection disagreement")
        global_cases.append({"case":case,"edges":g.edges,"costs":costs,
                             "expected":{k:v for k,v in expected.items() if k!="pair"},
                             "actual":strip_witness(got)})

    # One source overlap clause separates UNSAT from SAT on every Petersen edge.
    neighbors=[]
    base=petersen()
    ms=enumerate_matchings(base)
    check(len(ms)==6)
    pair_intersections=Counter(tuple(sorted(a&b)) for a,b in combinations(ms,2))
    check(pair_intersections == Counter({(e,):1 for e in range(15)}))
    for distinguished in range(15):
        lengths=[0]*15
        lengths[(distinguished+1)%15]=1
        g,manifest,_=inflate(base,lengths)
        distinguished_source=manifest[distinguished]["links"][0]
        pair=[]
        for allowed in (set(),{distinguished_source}):
            costs=costs_for(g,overlap_allowed=allowed)
            got=solve_projected(g,costs)
            ref=brute_source(g,costs)
            check((got["best"],got["total"],got["optimal"]) ==
                  (ref["best"],ref["total"],ref["optimal"]))
            pair.append(strip_witness(got))
        check(pair[0]["status"]=="UNSAT" and pair[1]["total"]==4)
        neighbors.append({"deleted_overlap_clause_edge":g.edges[distinguished_source],
                          "rows":pair})

    # Ring and parallel/loop quotient controls: necklace, K4 expansion, loop stem.
    special=[]
    # Three parallel kernel edges are three different resources, not one edge.
    g,_,_=inflate(Graph([(0,1),(0,1),(0,1)]),[1,1,1])
    costs=costs_for(g,overlap_allowed=set())
    got=solve_projected(g,costs)
    ref=brute_source(g,costs)
    check(got['core_vertices']==2 and got['core_edges']==3)
    check(got['total']==ref['total']==48)
    special.append(strip_witness(got))
    for m in (1,2,3):
        # Inflated K4 on one edge becomes a closed necklace of m+1 diamonds.
        lengths=[m]+[0]*5
        g,_,_=inflate(k4(),lengths)
        costs=costs_for(g,overlap_allowed=set())
        got=solve_projected(g,costs)
        ref=brute_source(g,costs)
        check(got["rings"]==1 and got["core_vertices"]==0)
        check(got["total"]==ref["total"] and got["best"]==ref["best"])
        special.append(strip_witness(got))
    # Two diamond loops connected by a bridge, simple and cubic at the source.
    es=[]
    for off in (0,5):
        a,b,c,d,u=[off+i for i in range(5)]
        es.extend([(a,c),(a,d),(b,c),(b,d),(c,d),(u,a),(u,b)])
    es.append((4,9))
    g=Graph(es)
    got=solve_projected(g,costs_for(g,overlap_allowed=set()))
    check(got["status"]=="UNSAT")
    check(brute_source(g,costs_for(g,overlap_allowed=set()))["total"]==0)
    special.append(strip_witness(got))

    return {"seed":2082401,"dominance":dominance,"local_tables":local_checks,
            "global_cases":global_cases,"petersen_single_clause_neighbors":neighbors,
            "special_controls":special}

def scaling_stage():
    out={"petersen_weighted_overlap":[],"petersen_single_clause_neighbors":[],
         "trap_repairs":[],"growing_bipartite_cores":[]}
    p=petersen()
    for m in (0,1,2,4,16,64,128):
        lengths=[m]*15
        g,_,_=inflate(p,lengths)
        got=solve_projected(g,costs_for(g))
        check(got["best"]==2*m+1)
        check(got["overlap"]==2*m+1)
        out["petersen_weighted_overlap"].append(dict(diamonds_per_edge=m,**strip_witness(got)))
        lengths[0]=0
        g,manifest,_=inflate(p,lengths)
        e0=manifest[0]["links"][0]
        root=solve_projected(g,costs_for(g,overlap_allowed=set()))
        neighbor=solve_projected(g,costs_for(g,overlap_allowed={e0}))
        check(root["status"]=="UNSAT")
        check(neighbor["status"]=="SAT" and neighbor["overlap"]==1)
        check(neighbor["total"]==2**(14*m+1))
        out["petersen_single_clause_neighbors"].append(
            {"diamonds_per_other_edge":m,"root":strip_witness(root),
             "neighbor":strip_witness(neighbor)})

    t=trap(); ab=trap_pair(t); ms=enumerate_matchings(t)
    check(min(len(a&ab[1]) for a in ms)==1)
    check(min(len(ab[0]&b) for b in ms)==1)
    check(min(len(ab[0]^a)+len(ab[1]^b) for a in ms for b in ms if not a&b)==10)
    for m in (0,1,2,4,16,64,128):
        g,_,ref=inflate(t,[m]*12,ab)
        got=solve_projected(g,costs_for(g,reference=ref,overlap_allowed=set()))
        check(got["best"]==10*(4*m+1) and got["overlap"]==0)
        out["trap_repairs"].append(dict(diamonds_per_edge=m,
                                       initial_overlap=len(ref[0]&ref[1]),
                                       **strip_witness(got)))
    rng=random.Random(2082402)
    for psize in (8,32,128,512):
        base,ma=bipartite_family(psize,rng)
        lengths=[rng.randrange(4) for _ in base.edges]
        g,_,ref=inflate(base,lengths,(ma,ma))
        g=relabel(g,rng)
        got=solve_projected(g,costs_for(g,reference=ref,overlap_allowed=set()),
                            small_limit=0,force_backend="bipartite")
        check(got["status"]=="SAT" and got["overlap"]==0)
        check(got["core_vertices"]==2*psize)
        check(got["diamonds"]==sum(lengths))
        out["growing_bipartite_cores"].append(
            dict(part_size=psize,initial_overlap=len(ref[0]&ref[1]),
                 **strip_witness(got)))
    return out

def replay_stage(prior):
    if prior is None:
        raise ValueError("--prior is required for replay")
    spec=importlib.util.spec_from_file_location("prior_repair_series",prior)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    records=[]
    for m in (0,1,2,4,8):
        E,A,B,order,seed=mod.inflate(mod.TRAP_E,mod.TRAP_A,mod.TRAP_B,m)
        original_result,stats=mod.solve(E,A,B,order,zero=True,minimum_movement=True)
        g=Graph(sorted(E));ids={e:i for i,e in enumerate(g.edges)}
        ab=(frozenset(ids[e] for e in A),frozenset(ids[e] for e in B))
        got=solve_projected(g,costs_for(g,reference=ab,overlap_allowed=set()))
        check(original_result is not None)
        check(got["best"]==stats["movement"])
        records.append({"m":m,"prior":stats,"quotient":strip_witness(got)})
    return {"prior_path_basename":Path(prior).name,
            "prior_sha256":hashlib.sha256(Path(prior).read_bytes()).hexdigest(),
            "records":records}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stage",choices=["controls","scaling","replay"],required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--prior")
    args=ap.parse_args()
    tracemalloc.start()
    start=time.perf_counter()
    if args.stage=="controls":
        data=control_stage()
    elif args.stage=="scaling":
        data=scaling_stage()
    else:
        data=replay_stage(args.prior)
    elapsed=time.perf_counter()-start
    live,peak=tracemalloc.get_traced_memory()
    tracemalloc.stop()
    envelope={"stage":args.stage,"status":"PASS","assertions":ASSERTIONS,
              "code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "python":sys.version,"elapsed_seconds":elapsed,
              "tracemalloc_peak_bytes":peak,"tracemalloc_final_bytes":live,
              "max_rss_kib_linux":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              "cumulative_memory_bit_steps":"not measured; theoretical bound in report",
              "operation_counters":dict(sorted(COUNTS.items())),"data":data}
    Path(args.out).write_text(json.dumps(envelope,indent=2)+"\n")
    print(json.dumps({k:v for k,v in envelope.items() if k!="data"},indent=2))

if __name__=="__main__":
    main()

