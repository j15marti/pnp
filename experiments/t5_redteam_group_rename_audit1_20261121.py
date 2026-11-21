"""Standalone semantic reconstruction. Python 3; no peer imports, no randomness.
Run: python experiments/t5_redteam_group_rename_audit1_20261121.py > results/raw/t5_redteam_group_rename_audit1_20261121.json
"""
import itertools as it
import json
import hashlib
from pathlib import Path


def compose(p, h):
    return tuple(p[h[i]] for i in range(len(p)))


def group(v, generators):
    seen = {tuple(range(v))}
    todo = list(seen)
    for p in todo:
        for h in generators:
            q = compose(p, h)
            if q not in seen:
                seen.add(q)
                todo.append(q)
    return sorted(seen)


class DAG:
    def __init__(self, v):
        self.v, self.nodes = v, []

    def add(self, op, args=(), data=None, scope=None):
        assert all(0 <= u < len(self.nodes) for u in args)
        sets = [self.nodes[u][3] for u in args]
        if op == 'view':
            assert sorted(data) == list(range(self.v))
            expected = frozenset(data[i] for i in sets[0])
        elif op == 'lit':
            expected = frozenset([data])
        elif op == 'const':
            expected = frozenset(scope or ())
        elif op == 'not':
            expected = sets[0]
        elif op == 'decision':
            assert all(data not in s for s in sets)
            expected = sets[0] | sets[1] | {data}
        else:
            assert len(sets) == 2 and not (sets[0] & sets[1])
            assert op == 'binary' and 0 <= data < 16
            expected = sets[0] | sets[1]
        if scope is not None:
            assert frozenset(scope) == expected
        self.nodes.append((op, tuple(args), data, expected))
        return len(self.nodes)-1

    def eval(self, u, assignment):
        # Direct semantic recursion transforms assignments at views, never composes maps.
        op, args, data, _ = self.nodes[u]
        if op == 'const': return bool(data)
        if op == 'lit': return bool(assignment[data])
        if op == 'view':
            return self.eval(args[0], tuple(assignment[data[i]] for i in range(self.v)))
        if op == 'not': return not self.eval(args[0], assignment)
        if op == 'decision': return self.eval(args[assignment[data]], assignment)
        a, b = (self.eval(x, assignment) for x in args)
        return bool((data >> (2*int(a)+int(b))) & 1)

    def shannon(self, predicate, variables=None, partial=()):
        variables = tuple(range(self.v)) if variables is None else variables
        if not variables:
            return self.add('const', data=int(predicate(partial)))
        low = self.shannon(predicate, variables[1:], partial+(0,))
        high = self.shannon(predicate, variables[1:], partial+(1,))
        return self.add('decision', (low, high), variables[0])


def expand(dag, root, p, cache=None, out=None):
    cache = {} if cache is None else cache
    out = DAG(dag.v) if out is None else out
    def rec(u, q):
        key = (u, q)
        if key in cache: return cache[key]
        op, args, data, scope = dag.nodes[u]
        if op == 'view':
            r = rec(args[0], compose(q, data))
        else:
            children = tuple(rec(x, q) for x in args)
            label = q[data] if op in ('lit', 'decision') else data
            r = out.add(op, children, label, {q[i] for i in scope})
        cache[key] = r
        return r
    return rec(root, p), cache, out


def audit(v, generators, label):
    perms = group(v, generators)
    d = DAG(v)
    roots = []
    # Both full and empty free scopes, all literals, native complements.
    for scope in ((), tuple(range(v))):
        for bit in (0, 1): roots.append(d.add('const', data=bit, scope=scope))
    lits = [d.add('lit', data=i) for i in range(v)]
    roots += lits
    roots += [d.add('not', (u,)) for u in lits]
    # Every two-input Boolean operator, with disjoint children.
    if v >= 2:
        roots += [d.add('binary', (lits[0], lits[1]), t) for t in range(16)]
    # Native decomposable parity plus full Shannon controls including UNSAT.
    parity = lits[0]
    for u in lits[1:]: parity = d.add('binary', (parity, u), 6)
    roots.append(parity)
    edges = [(i, i+1) for i in range(v-1)]
    tests = {
        'path_independent_sets': lambda a: all(not (a[i] and a[j]) for i,j in edges),
        'private_leaf_star': lambda a: all(not (a[0] and a[i]) for i in range(1,v)),
        'forced_zero': lambda a: not any(a),
        'odd_parity': lambda a: sum(a) % 2 == 1,
        'inconsistent_affine': lambda a: (sum(a) % 2 == 1) and (sum(a) % 2 == 0),
    }
    control_counts = {}
    assignments = list(it.product((0,1), repeat=v))
    for name, pred in tests.items():
        u = d.shannon(pred)
        roots.extend([u, d.add('not', (u,))])
        control_counts[name] = sum(d.eval(u, a) for a in assignments)
    # Shared bases, recomputed identities, nested chains much deeper than v.
    initial = list(roots)
    for u in initial:
        r = u
        for depth in range(24):
            h = generators[depth % len(generators)]
            r = d.add('view', (r,), h)
            if depth in (0,1,7,23): roots.append(r)
        roots.append(d.add('view', (u,), generators[0]))
    # Cross-context sharing below a decomposable native operator.
    if v >= 2:
        swap = tuple([1,0]+list(range(2,v)))
        if swap in perms:
            renamed = d.add('view', (lits[0],), swap)
            roots.append(d.add('binary', (lits[0],renamed), 8))
    M = len(d.nodes)
    cache, out, checks = {}, DAG(v), 0
    rows = []
    for u in roots:
        for p in perms:
            r, cache, out = expand(d, u, p, cache, out)
            count = 0
            for a in assignments:
                transformed = tuple(a[p[i]] for i in range(v))
                expected = d.eval(u, transformed)
                actual = out.eval(r, a)
                assert actual == expected
                count += actual
                checks += 1
            free = v-len(out.nodes[r][3])
            assert count % (1 << free) == 0
            rows.append([u, list(p), count >> free, r])
    assert len(cache) <= len(perms)*M and len(out.nodes) <= len(cache)
    # Reconstruction after cache deletion is legal and uses fresh output records.
    r, rebuilt, rebuilt_out = expand(d, roots[-1], perms[-1])
    assert all(rebuilt_out.eval(r,a) == d.eval(roots[-1],tuple(a[perms[-1][i]] for i in range(v))) for a in assignments)
    counts_by_root = {}
    for u, _, count, _ in rows:
        counts_by_root.setdefault(u, set()).add(count)
    assert all(len(s) == 1 for s in counts_by_root.values())
    row_digest = hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest()
    return {'label':label,'v':v,'generators':generators,'group_order':len(perms),
            'M':M,'roots':len(roots),'memo_keys':len(cache),'native_nodes':len(out.nodes),
            'gM_ceiling':len(perms)*M,'assignment_checks':checks,
            'rebuild_keys':len(rebuilt),'control_counts':control_counts,
            'context_rows_sha256':row_digest,'context_rows_checked':len(rows),
            'root_scoped_counts':[[u,next(iter(s))] for u,s in counts_by_root.items()]}


def main():
    rows = []
    for v in (2,3,4):
        cycle = tuple((i+1)%v for i in range(v))
        swap = tuple([1,0]+list(range(2,v)))
        rows.append(audit(v,[cycle,swap],'symmetric'))
    v=5
    rows.append(audit(v,[tuple((i+1)%v for i in range(v)),tuple((-i)%v for i in range(v))],'dihedral'))
    # Minimal failure of record-only caching: one shared literal under id and swap.
    d=DAG(2); u=d.add('lit',data=0); w=d.add('view',(u,),(1,0)); root=d.add('binary',(u,w),8)
    good,cache,out=expand(d,root,(0,1))
    a=(1,0)
    assert not out.eval(good,a) and bool(a[0] and a[0])
    # Noncommuting composition requires at least three variable names.
    p,h=(1,0,2),(0,2,1)
    assert compose(p,h)[0]==1 and compose(h,p)[0]==2
    a3=(0,1,0)
    assert a3[compose(p,h)[0]] != a3[compose(h,p)[0]]
    # One declared free variable suffices to make support-only counting wrong.
    f=DAG(1); t=f.add('const',data=1,scope=(0,))
    assert sum(f.eval(t,a) for a in it.product((0,1),repeat=1))==2
    # Actual strict-C NAND source, v=2 with its one bipartite edge.
    allowed = {p for i in range(5) for p in it.permutations((i,(i+1)%5,(i+2)%5))}
    clauses = [(i,(i+1)%5,(i+2)%5) for i in range(5)] + [(0,1,5),(0,4,6),(0,5,6)]
    n,m=7,len(clauses); width=n.bit_length()
    gamma=bin(m+1)[2:]
    encoded='1'*n+'0'+'0'*(len(gamma)-1)+gamma+''.join(format(i+1,'0%db'%width) for c in clauses for i in c)
    source_count=sum(all(tuple(a[i] for i in c) in allowed for c in clauses) for a in it.product(range(5),repeat=n))
    assert source_count==30 and len(encoded)==n+2+2*((m+1).bit_length()-1)+3*m*width
    # Its Boolean NAND expansion shares one literal across identity and swap.
    nand=d.add('not',(root,)); nr,_,no=expand(d,nand,(0,1))
    assert sum(no.eval(nr,a) for a in it.product((0,1),repeat=2))==3
    result={'target':'T5-SMALL-GROUP-RENAME1','peer_commit':'3168128105d8f040f41f8a49da8d6f0deffb9112',
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'mode':'exhaustive assignments for declared finite DAGs; no random seed',
            'runs':rows,'total_assignment_checks':sum(r['assignment_checks'] for r in rows),
            'strict_C_source':{'n':n,'m':m,'N':len(encoded),'one_based_clauses':[[i+1 for i in c] for c in clauses],
                               'encoded_bits':encoded,'count':source_count,'assignments_enumerated':5**n,'Boolean_NAND_count':3},
            'negative_controls':{
                'record_only':{'v':2,'assignment':a,'correct':False,'wrong':True},
                'composition_order':{'v':3,'p':p,'h':h,'assignment':a3,'correct_variable':1,'wrong_variable':2},
                'free_scope':{'v':1,'true_count':2,'wrong_support_only_count':1}},
            'status':'PASS; no counterexample to the published scoped lemma'}
    print(json.dumps(result,separators=(',',':')))


if __name__ == '__main__': main()
