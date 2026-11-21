"""T5-CONTEXT-ORBIT1: restricted-map compiler audit; Python 3, no randomness.
Run from repository root:
 python experiments/t5_discovery_scope_context1_20261121.py > results/raw/t5_discovery_scope_context1_20261121.json
The pinned peer generator/evaluator is a dependency, not new independent evidence.
"""
import hashlib
import importlib.util
import itertools as it
import json
import math
from pathlib import Path

DEPENDENCY = Path(__file__).with_name('t5_redteam_group_rename_audit1_20261121.py')
PIN = '0166c3f184725e8929acea8f938874b4ac781b78ba4d746450663f8a74a61630'
assert hashlib.sha256(DEPENDENCY.read_bytes()).hexdigest() == PIN
spec = importlib.util.spec_from_file_location('peer', DEPENDENCY)
peer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(peer)
full_expand = peer.expand


def restricted_expand(dag, root, p, cache=None, out=None):
    cache = {} if cache is None else cache
    out = peer.DAG(dag.v) if out is None else out
    def rec(u, r):
        op, args, data, scope = dag.nodes[u]
        assert set(r) == set(scope) and len(set(r.values())) == len(scope)
        key = (u, tuple(r[i] for i in sorted(scope)))
        if key in cache:
            return cache[key]
        if op == 'view':
            base = args[0]
            mapped = {i: r[data[i]] for i in dag.nodes[base][3]}
            result = rec(base, mapped)
        else:
            children = tuple(rec(c, {i: r[i] for i in dag.nodes[c][3]}) for c in args)
            label = r[data] if op in ('lit', 'decision') else data
            result = out.add(op, children, label, set(r.values()))
        cache[key] = result
        return result
    result = rec(root, {i: p[i] for i in dag.nodes[root][3]})
    return result, cache, out


def footprint_example(v):
    d = peer.DAG(v)
    lits = [d.add('lit', data=i) for i in range(v)]
    leaves, generators = [lits[0]], []
    for i in range(1, v):
        h = list(range(v)); h[i-1], h[i] = h[i], h[i-1]
        generators.append(tuple(h))
        leaves.append(d.add('view', (lits[i-1],), tuple(h)))
    root = leaves[0]
    for u in leaves[1:]:
        root = d.add('binary', (root, u), 8)
    cache, out, full_cache, full_out = {}, peer.DAG(v), {}, peer.DAG(v)
    identity = tuple(range(v))
    for u in range(len(d.nodes)):
        r, cache, out = restricted_expand(d, u, identity, cache, out)
        _, full_cache, full_out = full_expand(d, u, identity, full_cache, full_out)
    assert out.nodes[r][3] == frozenset(range(v))
    assignments = list(it.product((0, 1), repeat=v))
    assert all(out.eval(r, a) == all(a) for a in assignments)
    assert len(cache) <= len(d.nodes)*(1+v)
    enumerated = len(peer.group(v, generators)) if v <= 6 else None
    assert enumerated is None or enumerated == math.factorial(v)
    return dict(v=v, M=len(d.nodes), Q=len(cache), native_nodes=len(out.nodes),
                full_context_keys=len(full_cache), footprint_k=1,
                Q_bound=len(d.nodes)*(1+v), global_group_order=math.factorial(v),
                group_order_enumerated=enumerated, assignment_checks=len(assignments))


def main():
    peer.expand = restricted_expand
    runs = []
    for v in (2,3,4):
        runs.append(peer.audit(v,[tuple((i+1)%v for i in range(v)),
                                 tuple([1,0]+list(range(2,v)))], 'symmetric'))
    v=5
    runs.append(peer.audit(v,[tuple((i+1)%v for i in range(v)),
                             tuple((-i)%v for i in range(v))], 'dihedral'))
    # Same image SET is not the same ordered restriction: implication distinguishes.
    d=peer.DAG(2); x=d.add('lit',data=0); y=d.add('lit',data=1)
    u=d.add('binary',(x,y),11)  # implication x -> y
    r,c,o=restricted_expand(d,u,(0,1))
    s,c,o=restricted_expand(d,u,(1,0),c,o)
    assert o.eval(r,(1,0)) != o.eval(s,(1,0)) and r != s
    # Empty universe and declared free scope are retained.
    z=peer.DAG(0); t=z.add('const',data=1)
    zr,zc,zo=restricted_expand(z,t,())
    assert zo.eval(zr,()) and len(zc)==1
    f=peer.DAG(1); t=f.add('const',data=1,scope=(0,))
    fr,fc,fo=restricted_expand(f,t,(0,))
    assert sum(fo.eval(fr,a) for a in it.product((0,1),repeat=1)) == 2
    result=dict(target='T5-CONTEXT-ORBIT1',
                dependency_commit='55805b5b8f8d6a453ddebb029a74b71de5252d07',
                dependency_sha256=PIN,code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                mode='exhaustive assignment checks for finite declared DAGs; deterministic; no random seed',
                runs=runs,total_assignment_checks=sum(row['assignment_checks'] for row in runs),
                small_footprint_examples=[footprint_example(v) for v in range(3,9)],
                negative_controls={'image_set_only':'rejected: implication and its swap differ',
                                   'free_scope':'true over one declared variable counts 2',
                                   'empty_universe':'one constant context'},
                status='COMPUTATIONAL PASS; symbolic theorem and scope in accompanying report')
    print(json.dumps(result,separators=(',',':')))


if __name__ == '__main__':
    main()
