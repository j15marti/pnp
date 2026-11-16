#!/usr/bin/env python3
"""TMR-4/062: source-authenticated shared-component liveness compiler.
Standard-library reference, not a physical TM microstep implementation.
Run: python tmr4_live_core062.py --audit [--output evidence.json]
      python tmr4_live_core062.py --source circuit.json --output compiled.json
Canonical source grammar is identical to TMR-4/061. Invalid input is not UNSAT.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys
from typing import Any

REVISION = 'tmr4-live-core062.v1'
SEED = 202611152112
BASE_COMMIT = '82dcb3fb232297f9eaed04b29dbd5a365de9cdcb'

def encode(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')

def validate(source: bytes) -> dict[str, Any]:
    """Iterative source authentication, with arity guard before indexed allocation."""
    if not isinstance(source, bytes) or not source.isascii():
        raise ValueError('source must be ASCII bytes')
    try:
        obj = json.loads(source)
    except (ValueError, RecursionError) as exc:
        raise ValueError('invalid JSON') from exc
    if encode(obj) != source or not isinstance(obj, dict):
        raise ValueError('noncanonical source')
    if set(obj) != {'version', 'n', 'gates', 'root'} or type(obj['version']) is not int or obj['version'] != 1:
        raise ValueError('source shape/version')
    n, records, root = obj['n'], obj['gates'], obj['root']
    if type(n) is not int or n < 1 or not isinstance(records, list) or not records or n > 2*len(records):
        raise ValueError('arity/preallocation guard')
    gates = {}
    def canonical_id(v: Any, prefix: str) -> bool:
        return isinstance(v, str) and v.startswith(prefix) and v[1:].isdigit() and v[1:].isascii() and str(int(v[1:])) == v[1:]
    for e in records:
        if not isinstance(e, dict) or set(e) != {'id', 'a', 'b', 'op'}:
            raise ValueError('gate shape')
        v = e['id']
        if not canonical_id(v, 'g') or v in gates or type(e['op']) is not int or not 0 <= e['op'] < 16:
            raise ValueError('gate identity/opcode')
        gates[v] = e
    if not isinstance(root, str) or root not in gates:
        raise ValueError('root')
    inputs = {f'x{i}' for i in range(n)}
    for e in records:
        for key in ('a', 'b'):
            v = e[key]
            if not isinstance(v, str) or v not in inputs and v not in gates:
                raise ValueError('operand')
    colors, topo = {}, []
    work = [(root, False)]
    while work:
        v, exiting = work.pop()
        if exiting:
            colors[v] = 2
            topo.append(v)
        elif colors.get(v) == 1:
            raise ValueError('cycle')
        elif colors.get(v) != 2:
            colors[v] = 1
            work.append((v, True))
            if v in gates:
                work.append((gates[v]['b'], False))
                work.append((gates[v]['a'], False))
    if set(topo) != inputs | set(gates):
        raise ValueError('dead gate or unused input')
    uses = Counter(v for e in records for v in (e['a'], e['b']))
    shared = {v for v, count in uses.items() if count >= 2}
    return dict(obj=obj, n=n, gates=gates, root=root, topo=topo, shared=shared)

def compile_source(source: bytes) -> dict[str, Any]:
    c = validate(source)
    gs, shared, root, topo = c['gates'], c['shared'], c['root'], c['topo']
    targets = [v for v in topo if v in shared or v == root]
    deps, blocks, owned, reference_count, ranks = {}, {}, set(), 0, {}
    for v in topo:
        if v not in gs:
            ranks[v] = 1
        else:
            e = gs[v]
            a = 1 if e['a'] in shared else ranks[e['a']]
            b = 1 if e['b'] in shared else ranks[e['b']]
            ranks[v] = max(a, b) + int(a == b)
    for target in targets:
        dependencies, instructions = set(), []
        todo = [('visit', target, True)]
        while todo:
            kind, v, flag = todo.pop()
            if kind == 'gate':
                instructions.append(('GATE_REV' if flag else 'GATE', gs[v]['op'], v))
                continue
            if v in shared and not flag:
                dependencies.add(v)
                instructions.append(('REF', 0, v))
                reference_count += 1
                continue
            if v in owned:
                raise AssertionError('duplicated original computation')
            owned.add(v)
            if v not in gs:
                instructions.append(('READ', int(v[1:]), v))
            else:
                e = gs[v]
                a, b = e['a'], e['b']
                ra = 1 if a in shared else ranks[a]
                rb = 1 if b in shared else ranks[b]
                reverse = rb > ra
                first, second = (b, a) if reverse else (a, b)
                todo.extend([('gate', v, reverse), ('visit', second, False), ('visit', first, False)])
        deps[target], blocks[target] = dependencies, instructions
    assert owned == set(topo)
    successors = {t: set() for t in targets}
    for t in targets:
        for s in deps[t]:
            successors[s].add(t)
    tree_core = all(len(deps[t]) <= 2 for t in targets) and all(len(successors[t]) == (0 if t == root else 1) for t in targets)
    core_labels = {}
    if tree_core:
        for t in targets:
            rs = sorted((core_labels[v] for v in deps[t]), reverse=True)
            core_labels[t] = 1 if not rs else (rs[0] if len(rs) == 1 else max(rs[0], rs[1]+1))
        order, todo = [], [(root, False)]
        while todo:
            t, exiting = todo.pop()
            if exiting:
                order.append(t)
            else:
                children = sorted(deps[t], key=lambda x: (-core_labels[x], x))
                todo.append((t, True))
                todo.extend((v, False) for v in reversed(children))
    else:
        # Total, deterministic fallback. No assertion of optimal layout.
        order = targets
    assert len(order) == len(targets) and len(set(order)) == len(order)
    remaining = {t: len(successors[t]) for t in targets}
    live, instructions, frontier = set(), [], []
    for t in order:
        assert deps[t] <= live
        instructions.extend(blocks[t])
        for s in sorted(deps[t]):
            remaining[s] -= 1
            if remaining[s] == 0:
                instructions.append(('DROP', 0, s))
                live.remove(s)
        instructions.append(('STORE', 0, t))
        live.add(t)
        frontier.append(sorted(live))
    assert live == {root}
    instructions.append(('OUTPUT', 0, root))
    q = max(map(len, frontier))
    r = max(ranks[t] for t in targets)
    # Static shape is public. Data-state tuples contain values, not stale keys.
    active, height, shapes, reads, peak, peakstack = set(), 0, [], [], 0, 0
    for pc, (op, arg, v) in enumerate(instructions):
        shapes.append((tuple(sorted(active)), height))
        if op == 'READ':
            reads.append(pc)
            height += 1
        elif op == 'REF':
            assert v in active
            height += 1
        elif op.startswith('GATE'):
            assert height >= 2
            height -= 1
        elif op == 'DROP':
            assert v in active
            active.remove(v)
        elif op == 'STORE':
            assert height == 1 and v not in active
            height = 0
            active.add(v)
        else:
            assert op == 'OUTPUT' and active == {root} and height == 0
            active.clear()
        peak = max(peak, len(active)+height)
        peakstack = max(peakstack, height)
    assert peakstack <= r and peak <= q+r+1
    assert sorted(instructions[p][1] for p in reads) == list(range(c['n']))
    assert len(instructions) == c['n']+len(gs)+reference_count+2*len(shared)+2
    if tree_core:
        assert q == core_labels[root]
        assert q <= (len(shared)+1).bit_length()
    c.update(instructions=instructions, shapes=shapes, reads=reads, order=order,
             deps=deps, frontier=frontier, q=q, r=r, w=peak, bound=q+r+1,
             tree_core=tree_core, reference_count=reference_count,
             source_sha256=hashlib.sha256(source).hexdigest())
    return c

def apply(op: str, arg: int, v: str, cache: dict[str, int], stack: list[int], bit: int | None = None) -> int | None:
    if op == 'READ':
        assert bit in (0, 1)
        stack.append(bit)
    elif op == 'REF':
        stack.append(cache[v])
    elif op == 'DROP':
        del cache[v]
    elif op == 'STORE':
        cache[v] = stack.pop()
    elif op.startswith('GATE'):
        b, a = stack.pop(), stack.pop()
        if op == 'GATE_REV':
            a, b = b, a
        stack.append((arg >> (2*a+b)) & 1)
    else:
        assert op == 'OUTPUT'
        return cache.pop(v)
    return None

def transition(c: dict[str, Any], layer: int, state: tuple[int, ...], bit: int) -> tuple[int, ...] | int:
    start = c['reads'][layer]
    stop = c['reads'][layer+1] if layer+1 < c['n'] else len(c['instructions'])
    keys, h = c['shapes'][start]
    assert len(state) == len(keys)+h
    cache, stack = dict(zip(keys, state)), list(state[len(keys):])
    result = None
    for pc in range(start, stop):
        op, arg, v = c['instructions'][pc]
        result = apply(op, arg, v, cache, stack, bit if pc == start else None)
    if stop == len(c['instructions']):
        assert result in (0, 1) and not cache and not stack
        return result
    next_keys, next_h = c['shapes'][stop]
    assert set(cache) == set(next_keys) and len(stack) == next_h
    return tuple(cache[k] for k in next_keys)+tuple(stack)

def build_obdd(c: dict[str, Any], node_limit: int = 1000000) -> dict[str, Any]:
    assert c['reads'][0] == 0
    layers, edges, paths = [{(): 0}], [], {(): 1}
    nodes = 0
    for layer in range(c['n']):
        current = sorted(layers[-1])
        nodes += len(current)
        if nodes > node_limit:
            raise ValueError('explicit prototype node budget exceeded; not a semantic rejection')
        emap, nxt_paths = {}, defaultdict(int)
        for state in current:
            for bit in (0, 1):
                dest = transition(c, layer, state, bit)
                emap[(state, bit)] = dest
                nxt_paths[dest] += paths[state]
        edges.append(emap)
        paths = dict(nxt_paths)
        if layer+1 < c['n']:
            layers.append({s: i for i, s in enumerate(sorted(paths))})
    assert sum(paths.values()) == 1 << c['n']
    return dict(layers=layers, edges=edges, nodes=nodes, count=paths.get(1, 0), arcs=2*nodes)

def direct(c: dict[str, Any], bits: tuple[int, ...]) -> tuple[int, dict[str, int]]:
    vals = {f'x{i}': z for i, z in enumerate(bits)}
    for v in c['topo']:
        if v in c['gates']:
            e = c['gates'][v]
            vals[v] = (e['op'] >> (2*vals[e['a']]+vals[e['b']])) & 1
    return vals[c['root']], vals

def matrix_rank(rows: list[list[int]], p: int) -> int:
    a = [row[:] for row in rows]
    rank = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][j] % p), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][j] % p, -1, p)
        a[rank] = [(v*inv) % p for v in a[rank]]
        for i in range(rank+1, len(a)):
            z = a[i][j] % p
            if z:
                a[i] = [(v-z*w) % p for v, w in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank

def source_from(n: int, gates: list[dict[str, Any]], root: str) -> bytes:
    return encode(dict(version=1, n=n, gates=gates[::-1], root=root))

def module_tree(n: int, balanced: bool, rng: random.Random | None = None) -> bytes:
    gates: list[dict[str, Any]] = []
    def add(a: str, b: str, op: int) -> str:
        v = f'g{len(gates)}'
        gates.append(dict(id=v, a=a, b=b, op=op))
        return v
    nodes = [f'x{i}' for i in range(n)]
    while len(nodes) > 1:
        nxt = []
        if not balanced:
            a, b = nodes[:2]
            rest = nodes[2:]
            p, q = add(a,b,rng.randrange(16) if rng else 8), add(a,b,rng.randrange(16) if rng else 6)
            nodes = [add(p,q,rng.randrange(16) if rng else 14)] + rest
        else:
            for i in range(0, len(nodes)-1, 2):
                a,b = nodes[i:i+2]
                p,q = add(a,b,rng.randrange(16) if rng else 8), add(a,b,rng.randrange(16) if rng else 6)
                nxt.append(add(p,q,rng.randrange(16) if rng else 14))
            if len(nodes) % 2:
                nxt.append(nodes[-1])
            nodes = nxt
    return source_from(n, gates, nodes[0])

def random_source(rng: random.Random, n: int, extra: int) -> bytes:
    gates, available = [], [f'x{i}' for i in range(n)]
    a = available[0]
    for i in range(n-1+extra+1):
        b = f'x{i+1}' if i < n-1 else rng.choice(available)
        v = f'g{len(gates)}'
        gates.append(dict(id=v, a=a, b=b, op=rng.randrange(16)))
        a = v
        available.append(v)
    return source_from(n, gates, a)

def control_source(name: str, n: int = 6) -> bytes:
    gates = []
    def add(a: str, b: str, op: int) -> str:
        v=f'g{len(gates)}'; gates.append(dict(id=v,a=a,b=b,op=op)); return v
    xs=[f'x{i}' for i in range(n)]
    if name in ('DISJ','equality','product'):
        op={'DISJ':7,'equality':9,'product':8}[name]
        parts=[add(xs[i],xs[i+1],op) for i in range(0,n,2)]
        root=parts[0]
        for v in parts[1:]:root=add(root,v,8)
    elif name=='Horn_cycle':
        parts=[add(xs[i],xs[(i+1)%n],7) for i in range(n)]
        root=parts[0]
        for v in parts[1:]:root=add(root,v,8)
    elif name in ('affine','unique_solution'):
        root=xs[0]
        for v in xs[1:]:root=add(root,v,6 if name=='affine' else 8)
    elif name=='selector':
        # An actual conditional with structurally used, semantically canceled padding.
        n=4
        a=add('x0','x1',8); b=add('x0','x2',2)
        root=add(a,b,14); pad=add('x3','x3',6); root=add(root,pad,6)
    else:raise ValueError(name)
    return source_from(n,gates,root)

def audit() -> dict[str, Any]:
    rng = random.Random(SEED)
    counts = Counter()
    samples = []
    named_controls = []
    def check(ok: bool, label: str) -> None:
        counts['assertions'] += 1
        if not ok:
            raise AssertionError(label)
    def inspect(source: bytes, exhaustive: bool = True, family: str = '') -> dict[str, Any]:
        c = compile_source(source)
        b = build_obdd(c)
        counts['sources'] += 1
        counts['certified_tree_cores'] += c['tree_core']
        counts['bfs_arcs'] += b['arcs']
        counts['instructions'] += len(c['instructions'])
        check(c['w'] <= c['q']+c['r']+1, 'width')
        check(b['nodes'] <= c['n']*(1 << c['bound']), 'node bound')
        if exhaustive:
            yes = 0
            outs = {}
            for bits in itertools.product((0,1), repeat=c['n']):
                result, vals = direct(c, bits)
                cache, stack, visited = {}, [], []
                for op,arg,v in c['instructions']:
                    z = apply(op,arg,v,cache,stack,bits[arg] if op == 'READ' else None)
                    if op == 'READ' or op.startswith('GATE'):
                        check(stack[-1] == vals[v], 'original vertex value')
                        visited.append(v)
                    if op == 'REF':
                        check(stack[-1] == vals[v], 'reference value')
                    check(len(cache)+len(stack) <= c['bound'], 'every instruction width')
                check(z == result and len(visited) == c['n']+len(c['gates']), 'terminal/count')
                state: tuple[int,...] | int = ()
                for i, pc in enumerate(c['reads']):
                    state = b['edges'][i][(state,bits[c['instructions'][pc][1]])]
                check(state == result, 'pointwise OBDD')
                yes += result
                outs[bits] = result
                counts['assignments'] += 1
            check(yes == b['count'], 'exact path multiplicity')
            rho = [c['instructions'][p][1] for p in c['reads']]
            for j in range(1,c['n']):
                matrix=[]
                for left in itertools.product((0,1),repeat=j):
                    row=[]
                    for right in itertools.product((0,1),repeat=c['n']-j):
                        bits=[0]*c['n']
                        for k,z in zip(rho,left+right):bits[k]=z
                        row.append(outs[tuple(bits)])
                    matrix.append(row)
                for p in (2,101):
                    rank=matrix_rank(matrix,p)
                    check(rank <= len(b['layers'][j]), 'prefix rank')
                    counts['rank_checks'] += 1
        return dict(family=family,n=c['n'],g=len(c['gates']),k=len(c['shared']),q=c['q'],r=c['r'],actual_width=c['w'],bound=c['bound'],tree_core=c['tree_core'],nodes=b['nodes'],count=str(b['count']),source_sha256=c['source_sha256'])
    for n in (1,2):
        for op in range(16):
            inspect(source_from(n,[dict(id='g0',a='x0',b=f'x{n-1}',op=op)],'g0'), family='all_opcodes')
    for n in range(2,8):
        for balanced in (False,True):
            for _ in range(8):
                inspect(module_tree(n,balanced,rng), family='random_module_tree')
    for name in ('DISJ','equality','product','Horn_cycle','affine','unique_solution','selector'):
        named_controls.append(inspect(control_source(name), family=name))
    for _ in range(100):
        n=rng.randrange(1,7)
        inspect(random_source(rng,n,rng.randrange(8)), family='general_DAG')
    for n in (2,4,8,16,32,64,128):
        for balanced in (False,True):
            entry=inspect(module_tree(n,balanced), exhaustive=n<=8, family='balanced' if balanced else 'comb')
            check(int(entry['count']) == (1<<n)-1, 'OR module family closed count')
            check(entry['k'] == 2*n-2 and entry['tree_core'], 'linear many shares')
            samples.append(entry)
    # Small independently enumerated core orders check every cache boundary.
    for n in range(2,6):
        c=compile_source(module_tree(n,True))
        targets=c['order']; best=[len(targets)]; orders=[0]
        def enumerate_orders(done: set[str], peak: int) -> None:
            if len(done)==len(targets):
                orders[0]+=1; best[0]=min(best[0],peak); return
            for t in targets:
                if t not in done and c['deps'][t] <= done:
                    new=done|{t}
                    live={v for v in new if v==c['root'] or any(v in c['deps'][u] for u in targets if u not in new)}
                    enumerate_orders(new,max(peak,len(live)))
        enumerate_orders(set(),0)
        check(best[0] == c['q'], 'independent core order optimum')
        counts['independent_topological_orders'] += orders[0]
    # Exact malformed cases, including numeric preallocation attacks and cycles.
    good=json.loads(module_tree(2,True))
    bad=[]
    for mutate in ('huge_n','bool_n','opcode','bad_ref','duplicate','cycle','dead','unused','version'):
        obj=json.loads(encode(good))
        if mutate=='huge_n':obj['n']=10**80
        elif mutate=='bool_n':obj['n']=True
        elif mutate=='opcode':obj['gates'][0]['op']=16
        elif mutate=='bad_ref':obj['gates'][0]['a']='x9999'
        elif mutate=='duplicate':obj['gates'].append(obj['gates'][0].copy())
        elif mutate=='cycle':obj['gates'][0]['a']=obj['root']
        elif mutate=='dead':obj['gates'].append(dict(id='g999',a='x0',b='x1',op=8))
        elif mutate=='unused':obj['n']=3
        else:obj['version']=False
        bad.append(encode(obj))
    bad += [encode(good)+b' ', b'{"n":2,"n":2}', b'[]', b'\xff']
    for source in bad:
        try: validate(source)
        except ValueError: counts['malformed_rejections']+=1
        else: raise AssertionError('malformed accepted')
    # A real non-tree core defeats immediate-parent eviction, not correctness of fallback.
    cross=source_from(3,[dict(id='g0',a='x0',b='x1',op=8),dict(id='g1',a='g0',b='x2',op=6),dict(id='g2',a='g1',b='g1',op=8),dict(id='g3',a='g0',b='g2',op=14)],'g3')
    c=compile_source(cross)
    check(not c['tree_core'], 'cross-core fanout must not be certified')
    examine=inspect(cross,family='cross_core')
    # Compile mutant: discard g0 as soon as first consumer-component g1 completes.
    mutant=[]
    for ins in c['instructions']:
        mutant.append(ins)
        if ins[0]=='STORE' and ins[2]=='g1':mutant.append(('DROP',0,'g0'))
    cache,stack={},[]; caught=False; missing_operation=None
    try:
        for op,arg,v in mutant:apply(op,arg,v,cache,stack,1 if op=='READ' else None)
    except KeyError:
        caught=True; missing_operation=[op,v]
    check(caught and missing_operation==['REF','g0'],'premature eviction falsifier')
    # Missing arc multiplicity: constant gate on one original input has count 2, not 1.
    constant=inspect(source_from(1,[dict(id='g0',a='x0',b='x0',op=15)],'g0'),family='constant')
    check(constant['count']=='2','duplicate arc counterexample')
    return dict(revision=REVISION,seed=SEED,base_commit=BASE_COMMIT,python=sys.version.split()[0],status='COMPUTATIONAL',failures=0,counts=dict(sorted(counts.items())),samples=samples,named_controls=named_controls,cross_core=examine,controls=dict(premature_eviction_detected=caught,missing_operation=missing_operation,constant_one_input_count=constant['count']),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audit',action='store_true')
    parser.add_argument('--source',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.audit:
        result=audit()
    elif args.source:
        c=compile_source(args.source.read_bytes());b=build_obdd(c)
        layers=[]
        for i, states in enumerate(b['layers']):
            keys=sorted(states); index={v:j for j,v in enumerate(keys)}
            nxt={v:j for j,v in enumerate(sorted(b['layers'][i+1]))} if i+1<c['n'] else None
            rows=[]
            for st in keys:
                dest=[b['edges'][i][(st,z)] for z in (0,1)]
                rows.append(dict(id=index[st],state=list(st),next=[nxt[d] if nxt is not None else d for d in dest]))
            layers.append(dict(input=c['instructions'][c['reads'][i]][1],nodes=rows))
        result=dict(revision=REVISION,n=c['n'],k=len(c['shared']),q=c['q'],r=c['r'],width=c['w'],tree_core=c['tree_core'],source_sha256=c['source_sha256'],count=str(b['count']),layers=layers,instructions=c['instructions'])
    else:
        parser.error('specify --audit or --source')
    text=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')

if __name__=='__main__':
    main()
