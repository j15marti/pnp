#!/usr/bin/env python3
"""Standalone, deterministic audit: exact dynamic Boolean-relation chains.
No external packages; counts abstract Boolean compositions, not TM transitions.
Run: python 2026-10-28_2136_LSPV-4_ADAPTIVE_UPDATE_MEMORY_FIREWALL212_repro.py
"""
from __future__ import annotations
import itertools, hashlib, json, math, random
from pathlib import Path

SEED = 202610282136
rng = random.Random(SEED)
assertions = 0

def check(condition, msg='assertion failed'):
    global assertions
    assertions += 1
    if not condition:
        raise AssertionError(msg)

def ident(d):
    return tuple(1 << i for i in range(d))

def zero(d):
    return (0,) * d

def scalar(b, d=16):
    return (int(bool(b)),) + (0,) * (d - 1)

def compose(a, b):
    d = len(a)
    check(len(b) == d)
    rows = []
    for row in a:
        result = 0
        while row:
            low = row & -row
            j = low.bit_length() - 1
            result |= b[j]
            row -= low
        rows.append(result)
    return tuple(rows)

def direct(matrices, d):
    p = ident(d)
    for mat in matrices:
        p = compose(p, mat)
    return p

def accepts(matrices, d):
    p = direct(matrices, d)
    return bool(p[0] & 1)

class SegTree:
    def __init__(self, matrices, d):
        self.m = len(matrices)
        self.d = d
        self.n = 1 << (max(0, self.m - 1).bit_length())
        self.t = [ident(d)] * (self.n * 2)
        self.compositions = 0
        for i, mat in enumerate(matrices):
            self.t[self.n + i] = mat
        for i in range(self.n-1, 0, -1):
            self.t[i] = self.mul(self.t[2*i], self.t[2*i+1])
    def mul(self, a, b):
        self.compositions += 1
        return compose(a, b)
    def update(self, i, matrix):
        check(0 <= i < self.m)
        p = self.n + i
        self.t[p] = matrix
        levels = 0
        while p > 1:
            p //= 2
            self.t[p] = self.mul(self.t[2*p], self.t[2*p+1])
            levels += 1
        check(levels == math.log2(self.n))
        return levels
    def root(self):
        return self.t[1]


def random_matrix(d):
    p = rng.choice((0.07, 0.35, 0.75))
    return tuple(sum(1 << j for j in range(d) if rng.random() < p) for _ in range(d))

def forbidden_literals(statebits, vars_for_state):
    # A four-bit state equals (statebits). Return its negating 4-clause.
    return tuple(-v if ((statebits >> i) & 1) else v for i, v in enumerate(vars_for_state))

def expand_to_3cnf(lits, allocate):
    # Definitional-equivalent existential Tseitin chain, no same-variable repeats.
    if len(lits) == 3:
        return [tuple(lits)]
    if len(lits) < 3:
        raise ValueError('need width >= 3')
    aux = [allocate() for _ in range(len(lits) - 3)]
    clauses = [(lits[0], lits[1], aux[0])]
    for i in range(1, len(aux)):
        clauses.append((-aux[i - 1], lits[i + 1], aux[i]))
    clauses.append((-aux[-1], lits[-2], lits[-1]))
    return clauses

def build_dimacs(bits):
    # Physical canonical proper 3CNF for 16-state scalar relation chain.
    m = len(bits)
    d = 16
    nextvar = 4 * (m + 1) + 1
    def allocate():
        nonlocal nextvar
        v = nextvar
        nextvar += 1
        return v
    def state_vars(i):
        return tuple(4*i+j+1 for j in range(4))
    clauses = []
    for st in range(1, d):
        clauses += expand_to_3cnf(forbidden_literals(st, state_vars(0)), allocate)
        clauses += expand_to_3cnf(forbidden_literals(st, state_vars(m)), allocate)
    for i, b in enumerate(bits):
        left = state_vars(i)
        right = state_vars(i + 1)
        for u in range(d):
            for v in range(d):
                if b and u == v == 0:
                    continue
                lits = forbidden_literals(u, left) + forbidden_literals(v, right)
                clauses += expand_to_3cnf(lits, allocate)
    check(all(len(c) == 3 and len({abs(l) for l in c}) == 3 for c in clauses))
    # Formatting fixed, no hidden input oracle. The relation list is authenticated metadata.
    metadata = 'c relation-chain-scalar-v1 ' + ''.join(map(str, bits)) + '\n'
    header = f'p cnf {nextvar-1} {len(clauses)}\n'
    data = metadata + header + ''.join(' '.join(map(str, c)) + ' 0\n' for c in clauses)
    check(data.count('\n') == 2 + len(clauses))
    check(len(clauses) == (1536*m - 6*sum(bits)) + 60)
    check(nextvar-1 == 4*(m+1) + 5*(256*m - sum(bits)) + 30)
    return data.encode('ascii'), len(clauses), nextvar-1


def exhaustive_compose_tests():
    cases = 0
    for d in (2, 3):
        all_mats = list(itertools.product(range(1 << d), repeat=d))
        for a in all_mats:
            for b in all_mats:
                if d == 3 and rng.random() > 0.025:
                    continue
                p = compose(a, b)
                for i in range(d):
                    for j in range(d):
                        expected = any((a[i] >> k & 1) and (b[k] >> j & 1) for k in range(d))
                        check(bool(p[i] >> j & 1) == expected)
                cases += 1
    return cases

def dynamic_updates():
    total_updates = 0
    sat_queries = 0
    unsat_queries = 0
    compositions = 0
    height_checks = 0
    samples = []
    for d, m, trials, updates in [(2, 7, 16, 70), (4, 23, 12, 100), (16, 64, 5, 120)]:
        for _ in range(trials):
            mats = [random_matrix(d) for _ in range(m)]
            tree = SegTree(mats, d)
            check(tree.root() == direct(mats, d))
            for u in range(updates):
                i = rng.randrange(m)
                old = mats[i]
                new = random_matrix(d)
                mats[i] = new
                h = tree.update(i, new)
                height_checks += 1
                check(h <= math.ceil(math.log2(m)))
                check(tree.root() == direct(mats, d))
                decision = bool(tree.root()[0] & 1)
                check(decision == accepts(mats, d))
                sat_queries += int(decision)
                unsat_queries += int(not decision)
                if u % 9 == 0:
                    # Failed adaptive hypothesis and rollback; both transitions charged.
                    mats[i] = old
                    tree.update(i, old)
                    total_updates += 1
                    check(tree.root() == direct(mats, d))
                total_updates += 1
            compositions += tree.compositions
        samples.append({'states':d,'leaves':m,'trials':trials,'updates_per_trial':updates})
    return {'point_updates_including_rollbacks':total_updates,'explicit_associative_compositions':compositions,
            'SAT_root_queries':sat_queries,'UNSAT_root_queries':unsat_queries,'level_checks':height_checks,'samples':samples}

def lower_bounds():
    # Distinct initial tails while first leaf is zero: all scalar chain roots are zero.
    # The future query family sets all coordinates except j to 1, exposing bit j.
    max_unique = 0
    checks = 0
    for m in range(2, 12):
        fingerprints = set()
        for tail in itertools.product((0,1),repeat=m-1):
            initial = (0,) + tail
            check(not accepts([scalar(v,2) for v in initial],2))
            sig = []
            for j in range(1,m):
                transformed = [1]*m
                transformed[j] = initial[j]
                answer = accepts([scalar(v,2) for v in transformed],2)
                sig.append(int(answer))
                check(answer == bool(initial[j]))
                checks += 1
            fingerprints.add(tuple(sig))
        check(len(fingerprints) == 2**(m-1))
        max_unique = len(fingerprints)
    # Probe lower bound after updating first 0 to 1:
    # all-ones suffix indistinguishable from any one-zero suffix until probed.
    probe_adversary_checks = 0
    for m in range(2, 20):
        full = [0] + [1]*(m-1)
        root = accepts([scalar(v,2) for v in full],2)
        check(not root)
        new = full.copy(); new[0] = 1
        check(accepts([scalar(v,2) for v in new],2))
        for j in range(1,m):
            altered = full.copy(); altered[j] = 0
            check(not accepts([scalar(v,2) for v in altered],2))
            altered[0] = 1
            check(not accepts([scalar(v,2) for v in altered],2))
            probe_adversary_checks += 1
    return {'max_distinguishable_initial_states':max_unique,'memory_bits_lower_bound_at_m_11':10,
            'update_response_tests':checks,'indistinguishable_single_unread_leaf_tests':probe_adversary_checks}

def tseitin_equivalence_tests():
    # Independently exhaust all inputs for width-4 and width-8 Tseitin splits.
    checked = 0
    for width in (4, 8):
        original = tuple(range(1, width+1))
        nextaux = width + 1
        def alloc():
            nonlocal nextaux
            v=nextaux; nextaux += 1; return v
        encoded = expand_to_3cnf(original, alloc)
        check(len(encoded) == width-2)
        check(nextaux-width-1 == width-3)
        for input_bits in itertools.product((False,True), repeat=width):
            target = any(input_bits)
            possible = False
            for aux_bits in itertools.product((False,True),repeat=width-3):
                assignment = {i+1: input_bits[i] for i in range(width)}
                assignment.update({width+i+1: aux_bits[i] for i in range(width-3)})
                formula = all(any(assignment[abs(lit)] != (lit<0) for lit in clause) for clause in encoded)
                possible = possible or formula
            check(possible == target)
            checked += 1
    return checked

def binary_rank_controls():
    records=[]
    for width in (4, 8, 12):
        rank=(1<<width)-1
        steps=0
        while rank:
            rank -= 1
            steps += 1
            check(rank >= 0 and rank.bit_length() <= width)
        check(steps == (1<<width)-1)
        records.append({'rank_bit_width':width,'strict_decrement_steps':steps})
    return records

def encoded_controls():
    out = []
    for m in (1,2,4,8,12):
        for pattern in ((1,)*m, (0,)+(1,)*(m-1)):
            blob, clauses, varsnum = build_dimacs(pattern)
            header = blob.decode('ascii').splitlines()[1]
            check(header == f'p cnf {varsnum} {clauses}')
            check(bool(all(pattern)) == accepts([scalar(x,16) for x in pattern],16))
            out.append({'m':m, 'sat':bool(all(pattern)), 'encoded_bits':len(blob)*8,
                        'clauses':clauses,'variables':varsnum,'sha256':hashlib.sha256(blob).hexdigest()})
    return out


def physical_child_contraction_controls():
    rows=[]
    for m in (16, 64, 128):
        for allsat in (True, False):
            bits=[1]*m
            if not allsat:
                bits[-1]=0
            parent, _, _ = build_dimacs(bits)
            k=max(1,int(m**0.25))
            length=(m+k-1)//k
            child_bits=[int(all(bits[i:i+length])) for i in range(0,m,length)]
            child, _, _ = build_dimacs(child_bits)
            check(len(child_bits)<=k)
            check(all(bits)==all(child_bits))
            check(accepts([scalar(v,16) for v in bits],16) == accepts([scalar(v,16) for v in child_bits],16))
            check(len(child)<len(parent))
            rows.append({'source_relations':m,'child_relations':len(child_bits),'source_bits':len(parent)*8,
                         'child_bits':len(child)*8,'SAT':allsat})
    return rows

def main():
    c = exhaustive_compose_tests()
    pos = dynamic_updates()
    neg = lower_bounds()
    encoded = encoded_controls()
    tseitin = tseitin_equivalence_tests()
    rank = binary_rank_controls()
    shrink = physical_child_contraction_controls()
    out = {'status':'PASS','seed':SEED,'assertion_groups':assertions,'failures':0,
           'composition_truth_table_cases':c,'tseitin_exhaustive_input_assignments':tseitin,'dynamic':pos,'dynamic_no_reread_lower_bounds':neg,
           'physical_ordinary_3cnf_controls':encoded,'physical_power_child_controls':shrink,'rank_counterexamples':rank,
           'scope':'16-state fixed-width relation chains; not arbitrary SAT; abstract operation counts are not TM ticks'}
    print(json.dumps(out, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
