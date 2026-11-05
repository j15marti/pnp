"""Exact ternary shift-CSP to ordinary (binary) Resolution. Python 3.10+.

An oriented edge (u, v, D) requires x[v]-x[u] mod 3 in D. Run this file
to reproduce the experiments, or pass --replay FILE to check a saved example.
All certificate IDs are zero-based; a step (i,j,p) resolves source/derived
clauses i,j on +p in i and -p in j. JSON carries a graph and the steps.
"""
import argparse
import itertools
import json
import random
from collections import defaultdict, deque
from pathlib import Path

Q = range(3)


def var(v, a):
    return 3 * v + a + 1


def source(n, edges):
    """Source clauses plus index lookups for fixed implications and no-goods."""
    clauses, index = [], {}

    def emit(key, *lits):
        index[key] = len(clauses)
        clauses.append(frozenset(lits))

    for v in range(n):
        emit(('alo', v), *(var(v, a) for a in Q))
        for a, b in itertools.combinations(Q, 2):
            emit(('amo', v, a, b), -var(v, a), -var(v, b))
    for i, (u, v, allowed) in enumerate(edges):
        if not (0 <= u < n and 0 <= v < n and set(allowed) <= set(Q)
                and len(allowed) == len(set(allowed))):
            raise ValueError('invalid edge')
        if len(allowed) == 1:
            d = allowed[0]
            for a in Q:
                b = (a + d) % 3
                emit(('imp', i, 1, a), -var(u, a), var(v, b))
                emit(('imp', i, -1, b), -var(v, b), var(u, a))
        else:
            for a, b in itertools.product(Q, repeat=2):
                if (b - a) % 3 not in allowed:
                    emit(('ban', i, a, b), -var(u, a), -var(v, b))
    return clauses, index


def replay(n, edges, steps):
    """Independent checker: rebuild axioms and verify each pivot and exact resolvent."""
    cs, _ = source(n, edges)
    orig = len(cs)
    width = max(map(len, cs), default=0)
    for k, (i, j, p) in enumerate(steps, start=orig):
        if not (0 <= i < k and 0 <= j < k and p > 0 and p in cs[i] and -p in cs[j]):
            raise ValueError(f'invalid resolution at clause {k}')
        result = frozenset([x for x in cs[i] if x != p] + [x for x in cs[j] if x != -p])
        cs.append(result)
        width = max(width, len(result))
    if not steps or cs[-1]:
        raise ValueError('missing final empty clause')
    return {'axioms': orig, 'resolution_steps': len(steps), 'maximum_width': width}


class Derivation:
    def __init__(self, n, edges):
        self.clauses, self.index = source(n, edges)
        self.steps = []

    def resolve(self, left, right, pivot):
        a, b = self.clauses[left], self.clauses[right]
        assert pivot in a and -pivot in b
        self.steps.append((left, right, pivot))
        self.clauses.append((a - {pivot}) | (b - {-pivot}))
        return len(self.clauses) - 1


def normalize(proof, factors):
    """Intersect masks; contract newly forced pairs using original-variable proofs.

    factors map forbidden color tuples to exact negative clauses. After an
    intersection, one witness suffices for each forbidden tuple. Shifts
    of both endpoints by the same color preserve every factor.
    """
    merged = {}
    for scope, rows in factors:
        merged.setdefault(scope, {}).update(rows)
    eliminated = set()
    while True:
        # An entirely forbidden unary or binary relation is already UNSAT.
        for scope, rows in merged.items():
            if len(rows) == 3 ** len(scope):
                u = scope[0]
                units = []
                for a in Q:
                    if len(scope) == 1:
                        units.append(rows[a,])
                        continue
                    v = scope[1]
                    cid = proof.index['alo', v]
                    for b in Q:
                        cid = proof.resolve(cid, rows[a, b], var(v, b))
                    units.append(cid)
                cid = proof.index['alo', u]
                for a in Q:
                    cid = proof.resolve(cid, units[a], var(u, a))
                return [], eliminated, True
        forced = next((f for f, rows in merged.items() if len(f) == 2 and len(rows) == 6), None)
        if forced is None:
            return list(merged.items()), eliminated, False
        u, v = forced
        rows = merged.pop(forced)
        delta = next(b for b in Q if (0, b) not in rows)
        transport = {}
        for a in Q:
            cid = proof.index['alo', v]
            for b in Q:
                if b != (a + delta) % 3:
                    cid = proof.resolve(cid, rows[a, b], var(v, b))
            transport[a] = cid
        # Keep factors away from v verbatim; translate the others under
        # the sourced implication x_u=a -> x_v=a+delta.
        eliminated.add(v)
        changing = [f for f in merged if v in f]
        for old in changing:
            rows = merged.pop(old)
            new = tuple(sorted({u if x == v else x for x in old}))
            lifted = {}
            for colors in itertools.product(Q, repeat=len(new)):
                assign = dict(zip(new, colors))
                a = assign[u]
                assign[v] = (a + delta) % 3
                old_colors = tuple(assign[x] for x in old)
                if old_colors in rows:
                    cid = proof.resolve(transport[a], rows[old_colors], var(v, assign[v]))
                    assert proof.clauses[cid] == {-var(x, assign[x]) for x in new}
                    lifted[colors] = cid
            if lifted:
                merged.setdefault(new, {}).update(lifted)


def refute(n, edges, active_ambiguous=None, order=None, active_pairs=None, degree_prune=False):
    """Refute with all fixed edges and the selected non-singleton edge indices.

    None means SAT for the selected subsystem. Every returned proof resolves
    the *full original* source clauses. An optional order lists component
    representatives, which are the least numbered vertices in their components.
    degree_prune=True computes the structural reduction and its width-bound order
    using the companion degree_reduction module, preserving satisfiability.
    active_pairs optionally filters fully normalized quotient edges *after*
    certified contraction. A proof always certifies the full instance;
    with pruning, None only means the selected subsystem passed elimination.
    All representatives in active factors must appear exactly once in the order.
    """
    if degree_prune and (active_pairs is not None or order is not None):
        raise ValueError('automatic degree pruning supplies its own retained pairs and order')
    if active_ambiguous is not None:
        active_ambiguous = set(active_ambiguous)
        if any(i not in range(len(edges)) or len(edges[i][2]) == 1 for i in active_ambiguous):
            raise ValueError('invalid non-singleton edge index')
    proof = Derivation(n, edges)
    idx = proof.index
    adj = [[] for _ in range(n)]
    for i, (u, v, allowed) in enumerate(edges):
        if len(allowed) == 1:
            d = allowed[0]
            adj[u].append((v, d, i, 1))
            adj[v].append((u, -d, i, -1))
    root, shift = [-1] * n, [0] * n
    path = {}
    for r in range(n):
        if root[r] != -1:
            continue
        root[r] = r
        queue = deque([r])
        while queue:
            u = queue.popleft()
            for v, d, i, direction in adj[u]:
                if root[v] != -1:
                    continue
                root[v], shift[v] = r, (shift[u] + d) % 3
                for c in Q:
                    a = (c + shift[u]) % 3
                    edge = idx['imp', i, direction, a]
                    path[v, c] = edge if u == r else proof.resolve(path[u, c], edge, var(u, a))
                queue.append(v)

    scopes = []
    for i, (u, v, allowed) in enumerate(edges):
        if active_ambiguous is not None and len(allowed) != 1 and i not in active_ambiguous:
            continue
        scope = tuple(sorted({root[u], root[v]}))
        blocked = {}
        for row in itertools.product(Q, repeat=len(scope)):
            assign = dict(zip(scope, row))
            c, e = assign[root[u]], assign[root[v]]
            a, b = (c + shift[u]) % 3, (e + shift[v]) % 3
            if (b - a) % 3 in allowed:
                continue
            if len(allowed) == 1:
                actual = (a + allowed[0]) % 3
                lo, hi = sorted((actual, b))
                cid = proof.resolve(idx['imp', i, 1, a], idx['amo', v, lo, hi], var(v, actual))
            else:
                cid = idx['ban', i, a, b]
            for vertex, base, color in ((u, c, a), (v, e, b)):
                if vertex != root[vertex] and -var(vertex, color) in proof.clauses[cid]:
                    cid = proof.resolve(path[vertex, base], cid, var(vertex, color))
            assert proof.clauses[cid] == {-var(r, assign[r]) for r in scope}
            blocked[row] = cid
        if blocked:
            scopes.append((scope, blocked))

    scopes, eliminated, conflict = normalize(proof, scopes)
    initial_roots = set(root)
    survivors = initial_roots - eliminated
    plan = {}
    if degree_prune and not conflict:
        from degree_reduction import structure

        reps = sorted(survivors)
        position = {r: i for i, r in enumerate(reps)}
        simple = []
        for (u, v), rows in scopes:
            assert len(rows) == 3
            d = next(b for b in Q if (0, b) in rows)
            simple.append((position[u], position[v], d))
        high, kept, dense_order, width, reasons = structure(len(reps), simple)
        kept_ids = {reps[i] for i in kept}
        active_pairs = [f for f, _ in scopes if set(f) <= kept_ids]
        order = [reps[i] for i in dense_order]
        plan = {'degree_plan': dict(high=sorted(reps[i] for i in high), retained=sorted(kept_ids),
                                    order=order, structural_width=width, dropped=reasons)}
    if active_pairs is not None and not conflict:
        active_pairs = set(map(tuple, active_pairs))
        if not active_pairs <= {f for f, _ in scopes}:
            raise ValueError('unknown normalized pair')
        scopes = [(f, rows) for f, rows in scopes if f in active_pairs]
    stats = dict(components=len(initial_roots), normalized_components=len(survivors),
                 additional_contractions=len(eliminated), lifted_factors=len(scopes),
                 preprocess_steps=len(proof.steps), max_bucket_neighbors=0, **plan)
    if conflict:
        return proof.steps, stats
    rank = None
    if order is not None:
        rank = {r: i for i, r in enumerate(order)}
        needed = {r for f, _ in scopes for r in f}
        if len(rank) != len(order) or not needed <= set(rank) <= survivors:
            raise ValueError('order must contain each active representative and only representatives')
    while scopes:
        # Minimum current number of neighbors; any variable order is sound.
        neighbors = defaultdict(set)
        for scope, _ in scopes:
            for v in scope:
                neighbors[v].update(x for x in scope if x != v)
        if rank is None:
            v = min(neighbors, key=lambda x: (len(neighbors[x]), x))
        else:
            v = min(neighbors, key=rank.__getitem__)
        scope = tuple(sorted(neighbors[v]))
        bucket = [(f, rows) for f, rows in scopes if v in f]
        scopes = [(f, rows) for f, rows in scopes if v not in f]
        stats['max_bucket_neighbors'] = max(stats['max_bucket_neighbors'], len(scope))
        blocked = {}
        for row in itertools.product(Q, repeat=len(scope)):
            assign = dict(zip(scope, row))
            parents = []
            for color in Q:
                assign[v] = color
                witness = None
                for f, rows in bucket:
                    key = tuple(assign[x] for x in f)
                    if key in rows:
                        witness = rows[key]
                        break
                if witness is None:
                    break
                parents.append(witness)
            if len(parents) < 3:
                continue
            for c, parent in enumerate(parents):
                if -var(v, c) not in proof.clauses[parent]:
                    cid = parent
                    break
            else:
                cid = idx['alo', v]
                for c, parent in enumerate(parents):
                    cid = proof.resolve(cid, parent, var(v, c))
            assert proof.clauses[cid] <= {-var(x, assign[x]) for x in scope}
            blocked[row] = cid
            if not proof.clauses[cid]:
                assert cid == len(proof.clauses) - 1
                return proof.steps, stats
        if blocked:
            scopes.append((scope, blocked))
    return None, stats


def clique_family(length, leaves, clique=4):
    edges = []
    n = clique
    for i, j in itertools.combinations(range(clique), 2):
        u, total = i, 0
        for k in range(length):
            delta = 1 + ((i + j + k) % 2)
            edges.append((u, n, [delta]))
            u, n = n, n + 1
            total += delta
        edges.append((u, j, [d for d in Q if d != -total % 3]))
    for k in range(leaves):
        edges.append((k % clique, n, [0, 1] if k % 2 else [2]))
        n += 1
    return n, edges


def brute(n, edges):
    return any(all((s[v] - s[u]) % 3 in ds for u, v, ds in edges)
               for s in itertools.product(Q, repeat=n))


def run():
    checks = defaultdict(int)

    def test(n, edges, expected):
        steps, stats = refute(n, edges)
        sat = steps is None
        if sat != expected:
            raise RuntimeError((n, edges, sat, expected))
        auto, _ = refute(n, edges, degree_prune=True)
        if (auto is None) != expected:
            raise RuntimeError(('automatic degree pruning', n, edges, expected))
        if auto is not None:
            replay(n, edges, auto)
        checks['auto_degree_sat' if sat else 'auto_degree_unsat_replayed'] += 1
        checks['sat' if sat else 'unsat_replayed'] += 1
        if not sat:
            stats.update(replay(n, edges, steps))
        return steps, stats

    masks = [list(x) for k in range(4) for x in itertools.combinations(Q, k)]
    # All 32 individual oriented edges and all 1024 ordered pairs on two vertices.
    choices = list(itertools.product(range(2), range(2), masks))
    for size in (1, 2):
        for edges in itertools.product(choices, repeat=size):
            test(2, edges, brute(2, edges))
    rng = random.Random(4371)
    for _ in range(250):
        n = rng.randrange(1, 7)
        edges = [(rng.randrange(n), rng.randrange(n), rng.choice(masks))
                 for _ in range(rng.randrange(16))]
        test(n, edges, brute(n, edges))
    explicit = {
        'inconsistent_fixed_triangle': (3, [(0, 1, [1]), (1, 2, [1]), (2, 0, [0])]),
        'incompatible_parallel_shifted_edges': (3, [(0, 1, [1]), (0, 2, [0, 1]), (1, 2, [1])]),
        'loop_on_shifted_component': (2, [(0, 1, [1]), (1, 1, [1, 2])]),
    }
    special = {}
    for name, (n, edges) in explicit.items():
        assert not brute(n, edges)
        _, special[name] = test(n, edges, False)
    # With no fixed input edges, two parallel exclusions force 0=1.
    # Their transport exposes pairs forcing 0=2 then 0=3; the last
    # contraction makes all 3 differences impossible on pair (0,4).
    cascade = [(0, 1, [0, 1]), (0, 1, [0, 2])]
    for i in (2, 3):
        cascade += [(0, i, [0, 1]), (i - 1, i, [0, 2])]
    cascade += [(0, 4, [0, 1]), (2, 4, [0, 2]), (3, 4, [1, 2])]
    assert not brute(5, cascade)
    _, special['cascading_parallel_exclusions'] = test(5, cascade, False)
    assert special['cascading_parallel_exclusions']['additional_contractions'] == 3
    family, certificate = [], None
    for length in (0, 1, 2, 4, 8, 16, 32):
        leaves = 2 * length
        n, edges = clique_family(length, leaves)
        steps, stats = test(n, edges, False)
        family.append(dict(length=length, leaves=leaves, vertices=n, edges=len(edges), **stats))
        if length == 2:
            certificate = dict(n=n, edges=edges, steps=steps)
        n, edges = clique_family(length, leaves, clique=3)
        test(n, edges, True)
    # H={0}. After deleting H, K4 leaves a triangle; the attached K2,3
    # has a single non-clique, non-cycle block. Its three degree-two
    # vertices all attach to H. Reuse the unexpanded source IDs without
    # recalculating a subformula or renumbering its variables.
    core = [(i, j, [1, 2]) for i, j in itertools.combinations(range(4), 2)]
    periphery = [(i, j, [1, 2]) for i in (4, 5) for j in (6, 7, 8)]
    periphery.extend((0, j, [1, 2]) for j in (6, 7, 8))
    edges = core + periphery
    assert not brute(9, edges)
    active, order = list(range(6)), [1, 2, 3, 0]
    active_pairs = [(u, v) for u, v, _ in core]
    reduced_steps, reduced_stats = refute(9, edges, active_pairs=active_pairs, order=order)
    reduced_stats.update(replay(9, edges, reduced_steps))
    # All three boundary states admit an extension on the removed component.
    extend = []
    for h in Q:
        for colors in itertools.product(Q, repeat=5):
            s = dict(zip((0, 4, 5, 6, 7, 8), (h,) + colors))
            if all((s[v] - s[u]) % 3 in ds for u, v, ds in periphery):
                extend.append(list(colors))
                break
    assert len(extend) == 3
    pruned = dict(n=9, edges=edges, hub=0, degree_of_hub=6, retained_non_singleton_edges=active, retained_normalized_pairs=active_pairs,
                  elimination_order=order, extension_vertices=[4, 5, 6, 7, 8],
                  peripheral_witnesses_in_hub_color_order=extend,
                  stats=reduced_stats, steps=reduced_steps)
    checks['pruned_unsat_replayed'] += 1
    # One fixed shift (0 -> 1) and a parallel-edge-derived shift (3 -> 10)
    # mediate paths to the original K4. The normalized IDs have a gap at 1.
    mapping = [0, 2, 3, 4, 5, 6, 7, 8, 9]
    auto_mixed = []
    for twist in (False, True):
        mixed = [(0, 1, [1]), (3, 10, [0, 2]), (3, 10, [1, 2])]
        for u, v, _ in edges:
            i, j = mapping[u], mapping[v]
            d = int(twist and (u, v) == (1, 2))
            if i == 0:
                i, d = 1, d - 1
            if i == 3:
                i, d = 10, d - 2
            if j == 3:
                j, d = 10, d + 2
            mixed.append((i, j, [b for b in Q if b != d % 3]))
        model = next((list(s) for s in itertools.product(Q, repeat=11)
                      if all((s[v] - s[u]) % 3 in ds for u, v, ds in mixed)), None)
        assert bool(model) == twist
        seq, st = refute(11, mixed, degree_prune=True)
        assert (seq is None) == twist
        assert st['degree_plan']['high'] == [0] and st['degree_plan']['retained'] == [0, 2, 3, 4]
        assert st['degree_plan']['dropped'] == {'degree_coloring_theorem': 5}
        assert st['additional_contractions'] == 1
        if seq is not None:
            st.update(replay(11, mixed, seq))
        auto_mixed.append(dict(n=11, edges=mixed, satisfiable=twist, witness=model, steps=seq, stats=st))
    corrupted = list(certificate['steps'])
    corrupted[-1] = (0, 0, 0)
    try:
        replay(certificate['n'], certificate['edges'], corrupted)
    except ValueError:
        checks['corrupted_certificate_rejected'] += 1
    else:
        raise RuntimeError('checker accepted a corrupted certificate')
    return dict(seed=4371, exhaustive_two_vertex_cases=1056,
                random_bruteforce_cases=250, checks=dict(checks),
                special_cases=special, expanded_K4=family, pruned_example=pruned, automatic_mixed=auto_mixed, certificate=certificate)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', type=Path)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('proof_results.json'))
    parser.add_argument('--example', choices=('certificate', 'pruned_example', 'automatic_mixed'), default='certificate')
    args = parser.parse_args()
    if args.replay:
        case = json.loads(args.replay.read_text())[args.example]
        if args.example == 'automatic_mixed':
            case = case[0]
        print(json.dumps(replay(case['n'], case['edges'], case['steps']), indent=2))
    else:
        result = run()
        args.output.write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps({k: v for k, v in result.items() if k not in {'certificate', 'pruned_example', 'automatic_mixed'}}, indent=2))
