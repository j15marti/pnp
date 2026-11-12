"""Exact structural discovery for small-interface mixed SAT composition.

The graph is only a scope graph. Fill edges never become logical constraints.
Failed or budget-exhausted decomposition attempts retain the whole residual
graph as one bag, preserving exactness while potentially losing tractability.
All variables in bags are zero-based original variable identifiers.
"""
from itertools import combinations


def _natural(value, name, allow_none=False):
    if value is None and allow_none:
        return value
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(name + ' must be a nonnegative integer')
    return value


def primal_graph(n, clauses, equations, counters=None):
    """Build clique scopes of the supplied factors, without logical inference."""
    _natural(n, 'n')
    counts = counters if counters is not None else {}
    graph = {}

    def add_scope(scope):
        ordered = sorted(scope)
        for vertex in ordered:
            graph.setdefault(vertex, set())
        for left, right in combinations(ordered, 2):
            counts['primal_edge_insert_attempts'] = counts.get('primal_edge_insert_attempts', 0) + 1
            graph[left].add(right)
            graph[right].add(left)

    for clause in clauses:
        scope = set()
        for literal in clause:
            if not isinstance(literal, int) or isinstance(literal, bool) or literal == 0 or abs(literal) > n:
                raise ValueError('clause literal outside declared variable universe')
            counts['input_literal_visits'] = counts.get('input_literal_visits', 0) + 1
            scope.add(abs(literal) - 1)
        add_scope(scope)
    for row in equations:
        if len(row) != 2:
            raise ValueError('affine row must have mask and right-hand side')
        mask, rhs = row
        _natural(mask, 'affine mask')
        if mask.bit_length() > n or rhs not in (0, 1):
            raise ValueError('invalid affine row')
        scope = set()
        while mask:
            bit = mask & -mask
            scope.add(bit.bit_length() - 1)
            mask ^= bit
            counts['input_affine_bit_visits'] = counts.get('input_affine_bit_visits', 0) + 1
        add_scope(scope)
    counts['primal_vertices'] = len(graph)
    counts['primal_edges'] = sum(map(len, graph.values())) // 2
    return graph


def _components(graph, removed, counts):
    counts['component_scans'] += 1
    removed = set(removed)
    seen = set(removed)
    result = []
    for start in sorted(graph):
        counts['component_start_checks'] += 1
        if start in seen:
            continue
        seen.add(start)
        pending = [start]
        component = []
        while pending:
            vertex = pending.pop()
            component.append(vertex)
            counts['component_vertex_visits'] += 1
            for neighbor in graph[vertex]:
                counts['component_edge_scans'] += 1
                if neighbor not in seen:
                    seen.add(neighbor)
                    pending.append(neighbor)
        result.append(tuple(sorted(component)))
    return sorted(result, key=lambda item: (-len(item), item))


def _articulations(graph, counts):
    """Iterative Tarjan low-link computation; does not consume Python recursion."""
    counts['articulation_passes'] += 1
    discovery, low, parent, child_count = {}, {}, {}, {}
    cut_vertices = set()
    clock = 0
    for root in sorted(graph):
        if root in discovery:
            continue
        discovery[root] = low[root] = clock
        clock += 1
        parent[root] = None
        child_count[root] = 0
        stack = [(root, iter(sorted(graph[root])))]
        while stack:
            vertex, neighbors = stack[-1]
            try:
                neighbor = next(neighbors)
                counts['articulation_edge_scans'] += 1
                if neighbor not in discovery:
                    parent[neighbor] = vertex
                    child_count[vertex] += 1
                    child_count[neighbor] = 0
                    discovery[neighbor] = low[neighbor] = clock
                    clock += 1
                    stack.append((neighbor, iter(sorted(graph[neighbor]))))
                elif neighbor != parent[vertex]:
                    low[vertex] = min(low[vertex], discovery[neighbor])
            except StopIteration:
                stack.pop()
                ancestor = parent[vertex]
                if ancestor is None:
                    if child_count[vertex] > 1:
                        cut_vertices.add(vertex)
                else:
                    low[ancestor] = min(low[ancestor], low[vertex])
                    if parent[ancestor] is not None and low[vertex] >= discovery[ancestor]:
                        cut_vertices.add(ancestor)
    counts['articulation_vertex_visits'] += len(discovery)
    return cut_vertices


def _child_graph(graph, component, separator, counts):
    """Copy the interior's incident edges; avoid rescanning a large shared hub."""
    vertices = set(component) | set(separator)
    child = {vertex: set() for vertex in vertices}
    counts['subgraph_vertex_copies'] += len(vertices)
    for vertex in component:
        for neighbor in graph[vertex]:
            counts['subgraph_edge_scans'] += 1
            if neighbor in vertices:
                child[vertex].add(neighbor)
                child[neighbor].add(vertex)
    for left, right in combinations(separator, 2):
        if right not in graph[left]:
            counts['fill_edge_insertions'] += 1
        child[left].add(right)
        child[right].add(left)
    return child


def discover_decomposition(n, clauses, equations, max_separator=2,
                           candidate_cap=100000, max_splits=None):
    """Return a valid decomposition with adjacent intersections <= max_separator.

    The default split cap is the number of occurring vertices (at least one).
    A split has at most n children, so at most 1+n^2 residual calls occur. Each
    residual tests at most O(n^2) candidate pairs, with polynomial graph work.
    This gives polynomial discovery even with candidate_cap=None. A caller
    requesting a larger split cap receives a bound polynomial also in that cap.
    Both cap types trigger a one-bag fallback, never an UNSAT decision.
    """
    if max_separator not in (0, 1, 2):
        raise ValueError('max_separator must be 0, 1, or 2')
    _natural(candidate_cap, 'candidate_cap', allow_none=True)
    _natural(max_splits, 'max_splits', allow_none=True)
    clauses = [tuple(clause) for clause in clauses]
    equations = [tuple(row) for row in equations]
    counts = {name: 0 for name in (
        'input_literal_visits', 'input_affine_bit_visits', 'primal_edge_insert_attempts',
        'component_scans', 'component_start_checks', 'component_vertex_visits',
        'component_edge_scans', 'articulation_passes', 'articulation_vertex_visits',
        'articulation_edge_scans', 'separator_candidates', 'pair_candidates',
        'split_nodes', 'disconnected_splits', 'single_vertex_splits', 'pair_splits',
        'fallback_nodes', 'budget_fallbacks', 'fill_edge_insertions',
        'subgraph_vertex_copies', 'subgraph_edge_scans', 'attachment_bag_checks',
        'residual_calls', 'complete_graph_leaves')}
    graph = primal_graph(n, clauses, equations, counts)
    split_cap = max(1, len(graph)) if max_splits is None else max_splits
    counts['candidate_cap'] = candidate_cap
    counts['split_cap'] = split_cap
    counts['maximum_separator'] = max_separator
    bags, edges, nodes, completed = [], [], [], {}

    def new_node(local_graph):
        index = len(nodes)
        nodes.append({'graph': local_graph})
        return index

    def one_bag(index, budget=False, complete=False):
        bag_index = len(bags)
        bags.append(sorted(nodes[index]['graph']))
        completed[index] = [bag_index]
        nodes[index]['graph'] = None
        counts['fallback_nodes'] += 1
        counts['budget_fallbacks'] += int(budget)
        counts['complete_graph_leaves'] += int(complete)

    root = new_node(graph)
    pending = [('enter', root)]
    while pending:
        event, index = pending.pop()
        node = nodes[index]
        if event == 'finish':
            separator = set(node['separator'])
            all_bags = [node['bag']]
            for child_index in node['children']:
                child_bags = completed.pop(child_index)
                attachment = None
                for candidate in child_bags:
                    counts['attachment_bag_checks'] += 1
                    if separator.issubset(bags[candidate]):
                        attachment = candidate
                        break
                if attachment is None:
                    raise AssertionError('fill clique has no containing child bag')
                edges.append([node['bag'], attachment])
                all_bags.extend(child_bags)
            completed[index] = all_bags
            continue

        counts['residual_calls'] += 1
        local = node['graph']
        if counts['split_nodes'] >= split_cap:
            one_bag(index, budget=True)
            continue
        parts = _components(local, (), counts)
        separator = None
        if len(parts) > 1:
            separator = ()
            counts['disconnected_splits'] += 1
        elif len(local) <= 2 or sum(map(len, local.values())) == len(local) * (len(local) - 1):
            one_bag(index, complete=True)
            continue
        elif max_separator == 0 or (candidate_cap is not None and counts['separator_candidates'] >= candidate_cap):
            one_bag(index, budget=True)
            continue
        else:
            articulation = _articulations(local, counts)
            order = sorted(local, key=lambda vertex: (-len(local[vertex]), vertex))
            if articulation:
                vertex = next(vertex for vertex in order if vertex in articulation)
                counts['separator_candidates'] += 1
                separator = (vertex,)
                parts = _components(local, separator, counts)
                counts['single_vertex_splits'] += 1
            elif max_separator == 2:
                for left, right in combinations(order, 2):
                    if candidate_cap is not None and counts['separator_candidates'] >= candidate_cap:
                        break
                    counts['separator_candidates'] += 1
                    counts['pair_candidates'] += 1
                    trial = _components(local, (left, right), counts)
                    if len(trial) > 1:
                        separator = tuple(sorted((left, right)))
                        parts = trial
                        counts['pair_splits'] += 1
                        break
        if separator is None:
            exhausted = candidate_cap is not None and counts['separator_candidates'] >= candidate_cap
            one_bag(index, budget=exhausted)
            continue
        if len(parts) < 2:
            raise AssertionError('separator did not separate')
        counts['split_nodes'] += 1
        node['separator'] = separator
        node['bag'] = len(bags)
        bags.append(list(separator))
        node['children'] = []
        for component in parts:
            child = _child_graph(local, component, separator, counts)
            if len(child) >= len(local) and separator:
                raise AssertionError('nondecreasing recursive separator piece')
            node['children'].append(new_node(child))
        node['graph'] = None
        pending.append(('finish', index))
        pending.extend(('enter', child) for child in reversed(node['children']))
    counts['bags'] = len(bags)
    counts['tree_edges'] = len(edges)
    counts['largest_bag'] = max(map(len, bags), default=0)
    counts['observed_max_separator'] = max((len(set(bags[left]) & set(bags[right])) for left, right in edges), default=0)
    return {'bags': bags, 'edges': edges, 'discovery_counters': counts}
