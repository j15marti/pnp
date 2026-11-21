"""Finite checks of T5-FLAT-RENAME1; no runtime lower-bound measurements."""
import itertools, json, hashlib
from pathlib import Path

def norm(src):
    scope, cs = src
    out = []
    for c in cs:
        if c[0] == 'N': out.append(('N', *sorted(c[1:])))
        elif c[0] == 'P': out.append(tuple(c))
        elif c[0] == 'X': out.append(('X', c[1], tuple(sorted(c[2]))))
        else: raise ValueError('unknown source opcode')
    return tuple(sorted(scope)), tuple(sorted(out))

def rename_source(src, mp):
    scope, cs = src
    out = []
    for c in cs:
        if c[0] == 'N': out.append(('N', mp[c[1]], mp[c[2]]))
        elif c[0] == 'P': out.append(('P', mp[c[1]], c[2]))
        else: out.append(('X', c[1], tuple(mp[x] for x in c[2])))
    return norm((tuple(mp[x] for x in scope), out))

def authenticate(src, target, mp):
    # Exact data equality after validating the supplied bijection, never hash equality.
    s, t = src[0], target[0]
    if set(mp) != set(s) or len(set(mp.values())) != len(s): return False
    if set(mp.values()) != set(t): return False
    return rename_source(src, mp) == norm(target)

def source_value(src, a):
    for c in src[1]:
        if c[0] == 'N' and a[c[1]] and a[c[2]]: return False
        if c[0] == 'P' and a[c[1]] != c[2]: return False
        if c[0] == 'X' and sum(a[x] for x in c[2]) % 2 != c[1]: return False
    return True

class DAG:
    def __init__(self):
        self.nodes = [('C', 0), ('C', 1)]
        self.scopes = [frozenset(), frozenset()]
        self.unique = {self.nodes[0]: 0, self.nodes[1]: 1}
    def add(self, op, *args):
        if op == 'D':
            x, lo, hi = args
            assert x not in self.scopes[lo] | self.scopes[hi]
            if lo == hi: return lo
            scope = self.scopes[lo] | self.scopes[hi] | {x}
        elif op == 'NOT': scope = self.scopes[args[0]]
        else:
            l, r = args
            assert not self.scopes[l] & self.scopes[r], 'overlapping binary scopes'
            scope = self.scopes[l] | self.scopes[r]
        key = (op, *args)
        if key in self.unique: return self.unique[key]
        i = len(self.nodes); self.nodes.append(key); self.scopes.append(frozenset(scope))
        self.unique[key] = i
        return i
    def evaluate(self, root, a):
        memo = {}
        def rec(i):
            if i in memo: return memo[i]
            op, *z = self.nodes[i]
            if op == 'C': v = z[0]
            elif op == 'D': v = rec(z[2] if a[z[0]] else z[1])
            elif op == 'NOT': v = 1-rec(z[0])
            else:
                l, r = rec(z[0]), rec(z[1])
                v = {'AND': l & r, 'OR': l | r, 'XOR': l ^ r, 'EQ': int(l == r)}[op]
            memo[i] = v; return v
        return rec(root)
    def reachable(self, root):
        seen = set()
        def visit(i):
            if i in seen: return
            seen.add(i); op, *z = self.nodes[i]
            if op == 'D':
                visit(z[1]); visit(z[2])
            elif op != 'C':
                for j in z: visit(j)
        visit(root); return seen

def compile_explicit(src, order):
    # Exponential discovery is deliberately not assumed free.
    d = DAG(); a = {}; leaves = 0
    def rec(k):
        nonlocal leaves
        if k == len(order):
            leaves += 1; return int(source_value(src, a))
        x = order[k]
        a[x] = 0; lo = rec(k+1)
        a[x] = 1; hi = rec(k+1)
        del a[x]
        return d.add('D', x, lo, hi)
    root = rec(0)
    return d, root, leaves

class FlatCopier:
    def __init__(self, base, root):
        self.base, self.root, self.out = base, root, DAG()
        self.views = {}; self.visits = 0
    def copy(self, mp):
        key = tuple(sorted(mp.items()))
        if key in self.views: return self.views[key]
        memo = {0: 0, 1: 1}
        def rec(i):
            if i in memo: return memo[i]
            self.visits += 1
            op, *z = self.base.nodes[i]
            if op == 'D': ans = self.out.add('D', mp[z[0]], rec(z[1]), rec(z[2]))
            else: ans = self.out.add(op, *(rec(j) for j in z))
            memo[i] = ans; return ans
        ans = rec(self.root); self.views[key] = ans; return ans

def assignments(scope):
    for bits in itertools.product((0,1), repeat=len(scope)):
        yield dict(zip(scope, bits))

def main():
    cases = [
        ('matching', 4, [('N',0,2),('N',1,3)]),
        ('cycle4', 4, [('N',0,2),('N',0,3),('N',1,2),('N',1,3)]),
        ('private_leaf_tree', 5, [('N',0,2),('N',1,3),('N',0,4),('N',1,4)]),
        ('K23', 5, [('N',i,j) for i in (0,1) for j in (2,3,4)]),
        ('forced_K23', 5, [('N',i,j) for i in (0,1) for j in (2,3,4)]+[('P',i,0) for i in range(5)]),
        ('parity_even', 5, [('X',0,tuple(range(5)))]),
        ('parity_inconsistent', 5, [('X',0,tuple(range(5))),('X',1,tuple(range(5)))]),
        ('free_scope', 4, []),
    ]
    rows = []; permutation_checks = evaluations = 0; invalid_rejected = 0
    for name, n, clauses in cases:
        src = norm((tuple(range(n)), clauses))
        for order in (tuple(range(n)), tuple(reversed(range(n)))):
            d, root, leaves = compile_explicit(src, order)
            # Include a real internal complement node in the template.
            for complement in (False, True):
                rt = d.add('NOT',root) if complement else root
                size = len(d.reachable(rt)-{0,1})
                for perm in itertools.permutations(range(n)):
                    mp = {i: n+perm[i] for i in range(n)}
                    target = rename_source(src, mp)
                    assert authenticate(src,target,mp)
                    cp = FlatCopier(d,rt); mapped = cp.copy(mp)
                    first_nodes, first_visits = len(cp.out.nodes), cp.visits
                    for _ in range(7): assert cp.copy(mp) == mapped
                    assert len(cp.out.nodes) == first_nodes and cp.visits == first_visits
                    assert cp.visits == size
                    for a in assignments(target[0]):
                        expected = int(source_value(target,a)) ^ int(complement)
                        assert cp.out.evaluate(mapped,a) == expected
                        evaluations += 1
                    permutation_checks += 1
                # Two disjoint views, actual native operators, and no expansion per pointer.
                cp = FlatCopier(d,rt)
                m1 = {i:i for i in range(n)}; m2 = {i:n+i for i in range(n)}
                r1, r2 = cp.copy(m1), cp.copy(m2)
                for op in ('AND','OR','XOR','EQ'):
                    r = cp.out.add(op,r1,r2)
                    for a in assignments(tuple(range(2*n))):
                        l = d.evaluate(rt,a); b = {i:a[n+i] for i in range(n)}
                        z = d.evaluate(rt,b)
                        expected = {'AND':l & z,'OR':l | z,'XOR':l ^ z,'EQ':int(l==z)}[op]
                        assert cp.out.evaluate(r,a) == expected
                        evaluations += 1
                assert cp.visits == 2*size
                assert len(cp.out.nodes)-2 <= 2*size+4
                # Overlap forbidden except when both actual supports are empty.
                if d.scopes[rt]:
                    try: cp.out.add('AND',r1,r1)
                    except AssertionError: invalid_rejected += 1
                    else: raise AssertionError('overlap accepted')
                count = sum(d.evaluate(rt,a) for a in assignments(tuple(range(n))))
                rows.append(dict(name=name,order=order,complement=complement,
                                 declared_scope=n,base_nodes=size,base_count=count,
                                 discovery_leaf_evaluations=leaves,views=2,
                                 copy_node_visits=cp.visits,materialized_nonconstants=len(cp.out.nodes)-2))
        good = {i:n+i for i in range(n)}; target = rename_source(src,good)
        bad = dict(good); bad[1] = bad[0]
        assert not authenticate(src,target,bad); invalid_rejected += 1
        changed = norm((target[0], target[1]+(('P',n,0),)))
        assert not authenticate(src,changed,good); invalid_rejected += 1
    return dict(lemma='T5-FLAT-RENAME1',status='COMPUTATIONAL',mode='exhaustive finite controls',
                code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                permutation_checks=permutation_checks,semantic_evaluations=evaluations,
                invalid_cases_rejected=invalid_rejected,rows=rows,
                limitations=['No one-tape timing or peak-memory measurement.',
                             'Finite normalized Boolean controls, not an unrestricted T5 compiler.',
                             'Discovery uses explicit exponential enumeration and is charged in the theorem.',
                             'No lazy view is permitted inside a base template.'])

if __name__ == '__main__':
    result = main()
    target = Path('results/raw/t5_discovery_flat_rename1_20261121.json')
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
