#!/usr/bin/env python3
"""LSPV-4 mixed affine/3CNF full-port research reproducibility.
All result fields and assertion counters are deterministic. No third-party imports.
"""
import itertools
import json
import math
import random
from pathlib import Path

SEED = 20261029
rng = random.Random(SEED)
checks = 0

def check(cond, note="assertion failed"):
    global checks
    checks += 1
    if not cond:
        raise AssertionError(note)


def linear_project(n, eqs, keep):
    """Canonical GF(2) projected row-echelon relation. None means contradiction.
    Equations: (global variable bitmask, right-hand parity)."""
    keep = tuple(keep)
    hidden = [i for i in range(n) if i not in keep]
    rows = [[mask, parity] for mask, parity in eqs]
    rank = 0
    for col in hidden:
        pivot = next((j for j in range(rank, len(rows)) if (rows[j][0] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for j in range(len(rows)):
            if j != rank and ((rows[j][0] >> col) & 1):
                rows[j][0] ^= rows[rank][0]
                rows[j][1] ^= rows[rank][1]
        rank += 1
    rem = []
    for full, parity in rows[rank:]:
        assert full & ~sum(1 << c for c in keep) == 0
        mapped = sum(((full >> original) & 1) << j for j, original in enumerate(keep))
        rem.append([mapped, parity])
    rank = 0
    for col in range(len(keep)):
        pivot = next((j for j in range(rank, len(rem)) if (rem[j][0] >> col) & 1), None)
        if pivot is None:
            continue
        rem[rank], rem[pivot] = rem[pivot], rem[rank]
        for j in range(len(rem)):
            if j != rank and ((rem[j][0] >> col) & 1):
                rem[j][0] ^= rem[rank][0]
                rem[j][1] ^= rem[rank][1]
        rank += 1
    if any(mask == 0 and parity for mask, parity in rem):
        return None
    return tuple(sorted((mask, parity) for mask, parity in rem if mask))


def piece_accepts(piece, y):
    return piece is not None and all(((mask & y).bit_count() % 2) == parity for mask, parity in piece)


def first_true_parts(n, xor_eqs, clauses, keep):
    """Exact projection as a deduplicated OR of affine pieces.
    Clause literal (var, target_value) is true when var == target_value.
    """
    pieces = set()
    raw_sat_branches = 0
    for choices in itertools.product(range(3), repeat=len(clauses)):
        eqs = list(xor_eqs)
        for clause, j in zip(clauses, choices):
            for k in range(j):
                v, target = clause[k]
                eqs.append((1 << v, 1 - target))
            v, target = clause[j]
            eqs.append((1 << v, target))
        projection = linear_project(n, eqs, keep)
        if projection is not None:
            raw_sat_branches += 1
            pieces.add(projection)
    return tuple(sorted(pieces)), raw_sat_branches


def eval_source(n, xor_eqs, clauses, assignment):
    return (all(((mask & assignment).bit_count() % 2) == parity for mask, parity in xor_eqs)
            and all(any(((assignment >> v) & 1) == target for v, target in clause) for clause in clauses))


def direct_projection(n, xor_eqs, clauses, keep):
    hidden = [i for i in range(n) if i not in keep]
    satisfying = set()
    for x in range(1 << len(hidden)):
        for y in range(1 << len(keep)):
            mask = sum(((x >> j) & 1) << var for j, var in enumerate(hidden))
            mask |= sum(((y >> j) & 1) << var for j, var in enumerate(keep))
            if eval_source(n, xor_eqs, clauses, mask):
                satisfying.add(y)
    return satisfying


class Proper3Compiler:
    def __init__(self, port_vars):
        self.vars = port_vars
        self.clauses = []
        self.port_vars = port_vars

    def new(self):
        self.vars += 1
        return self.vars

    def add3(self, a, b, c):
        assert len({abs(a), abs(b), abs(c)}) == 3
        self.clauses.append((a,b,c))

    def add2(self, a, b):
        assert abs(a) != abs(b)
        t = self.new()
        self.add3(a,b,t)
        self.add3(a,b,-t)

    def force1(self, lit):
        t, u = self.new(), self.new()
        for sa, sb in itertools.product((1,-1), repeat=2):
            self.add3(lit,sa*t,sb*u)

    def xor2(self, a, b):
        c = self.new()
        for aa, bb, cc in itertools.product((0,1), repeat=3):
            if cc != (aa ^ bb):
                self.add3(a if aa == 0 else -a, b if bb == 0 else -b, c if cc == 0 else -c)
        return c

    def or2(self, a, b):
        c = self.new()
        self.add3(a,b,-c)
        self.add2(-a,c)
        self.add2(-b,c)
        return c

    def guard_row(self, sel, mask, parity):
        vars_ = [v + 1 for v in range(self.port_vars) if (mask >> v) & 1]
        if not vars_:
            if parity:
                self.force1(-sel)
            return
        node = vars_[0]
        for v in vars_[1:]:
            node = self.xor2(node,v)
        self.add2(-sel, node if parity else -node)

    def compile(self, pieces):
        if not pieces:
            x,y,z = self.new(),self.new(),self.new()
            for v in itertools.product((1,-1),repeat=3):
                self.add3(v[0]*x,v[1]*y,v[2]*z)
            return self
        selectors = [self.new() for _ in pieces]
        for selector, piece in zip(selectors, pieces):
            for mask, parity in piece:
                self.guard_row(selector, mask, parity)
        root = selectors[0]
        for s in selectors[1:]:
            root = self.or2(root,s)
        self.force1(root)
        return self

    def physical_dimacs(self):
        header = f"p cnf {self.vars} {len(self.clauses)}\n"
        return header + ''.join(' '.join(str(x) for x in cl)+' 0\n' for cl in self.clauses)


def cnf_exists_given_port(clauses, port_assignment):
    """Independent DPLL decision for already fixed core port variables."""
    def solve(cur_clauses, known):
        while True:
            residual = []
            units = []
            for cl in cur_clauses:
                if any(abs(l) in known and known[abs(l)] == (l > 0) for l in cl):
                    continue
                todo = [l for l in cl if abs(l) not in known]
                if not todo:
                    return False
                if len(todo) == 1:
                    units.append(todo[0])
                residual.append(tuple(todo))
            if not residual:
                return True
            if not units:
                break
            progressed = False
            for unit in units:
                var, value = abs(unit), unit > 0
                if var in known:
                    if known[var] != value:
                        return False
                else:
                    known[var] = value
                    progressed = True
            if not progressed:
                break
            cur_clauses = residual
        counts = {}
        for cl in residual:
            for lit in cl:
                counts[abs(lit)] = counts.get(abs(lit),0)+1
        variable = max(counts, key=counts.get)
        for truth in (True,False):
            modified = known.copy()
            modified[variable] = truth
            if solve(residual,modified):
                return True
        return False
    return solve(tuple(clauses), port_assignment.copy())


def affine_max_piece(r):
    """Concrete affine subspace satisfying r disjoint OR3 clauses: x_(3i)=1."""
    return {x for x in range(1 << (3*r)) if all((x >> (3*i)) & 1 for i in range(r))}


def exact_span_size(vectors, shift=0):
    vals = {shift}
    for v in vectors:
        vals |= {x ^ v for x in list(vals)}
    return vals


def run():
    source_cases, projection_assignments, dpll_assignments = 0,0,0
    compiled_max_bits, raw_branches_max = 0,0
    sat_cases, unsat_cases = 0,0
    for t in range(235):
        n = rng.randint(3,8)
        r = rng.randint(0,3)
        eqs = []
        for _ in range(rng.randint(0, n+1)):
            eqs.append((rng.randrange(1<<n),rng.randrange(2)))
        clauses = []
        for _ in range(r):
            vars_ = rng.sample(range(n),3)
            clauses.append(tuple((v,rng.randrange(2)) for v in vars_))
        keep = sorted(rng.sample(range(n),rng.randint(0,min(4,n))))
        pieces, raw = first_true_parts(n,eqs,clauses,keep)
        truth = direct_projection(n,eqs,clauses,keep)
        sat_cases += bool(truth)
        unsat_cases += not bool(truth)
        raw_branches_max = max(raw_branches_max,raw)
        check(len(pieces) <= 3**r)
        for y in range(1 << len(keep)):
            prediction = any(piece_accepts(piece,y) for piece in pieces)
            check(prediction == (y in truth),f"Projection mismatch case {t}, y={y}")
            projection_assignments += 1
        source_cases += 1
        if t < 70 and len(keep) <= 3 and r <= 2:
            compiled = Proper3Compiler(len(keep)).compile(pieces)
            dimacs = compiled.physical_dimacs()
            compiled_max_bits=max(compiled_max_bits,len(dimacs.encode())*8)
            check(dimacs.count('\n') == len(compiled.clauses)+1)
            for cl in compiled.clauses:
                check(len(cl)==3 and len({abs(l) for l in cl})==3 and max(abs(l) for l in cl)<=compiled.vars)
            for y in range(1<<len(keep)):
                assignment = {j+1:bool((y>>j)&1) for j in range(len(keep))}
                dpll_answer = cnf_exists_given_port(compiled.clauses,assignment)
                check(dpll_answer==(y in truth),f"Tseitin mismatch case={t}, y={y}")
                dpll_assignments += 1

    # Compact disjoint clause family and tight per-component max dimension.
    for r in range(1,7):
        full = {x for x in range(1<<(3*r)) if all(any((x>>(3*i+j))&1 for j in range(3)) for i in range(r))}
        check(len(full)==7**r)
        witness = affine_max_piece(r)
        check(len(witness)==4**r and witness <= full)
        required = math.ceil((7/4)**r - 1e-13)
        check(required*(4**r)>=7**r)
        if r>=2:
            check((required-1)*4**r < 7**r)
        # Sample random affine subspaces and test the projection/dimension inequality.
        for k in range(120):
            nbits=3*r
            dim=rng.randrange(nbits+1)
            origin=rng.randrange(1<<nbits)
            vectors=[rng.randrange(1<<nbits) for _ in range(dim)]
            space=exact_span_size(vectors,origin)
            if space<=full:
                check(len(space) <= 4**r)
        # Witness r disjoint OR-clauses has a trivial fixed all-one satisfying assignment.
        check(((1<<(3*r))-1) in full)

    # Physical affine-union Tseitin output on simple disjoint OR3 sources.
    expansion_examples=[]
    for r in range(1,6):
        n=3*r
        clauses=[tuple((3*i+j,1) for j in range(3)) for i in range(r)]
        pieces,raw=first_true_parts(n, [], clauses, tuple(range(n)))
        check(len(pieces)==3**r and raw==3**r)
        cnf=Proper3Compiler(n).compile(pieces)
        source=f"p cnf {n} {r}\n"+''.join(' '.join(str(3*i+j+1) for j in range(3))+' 0\n' for i in range(r))
        expansion_examples.append({"r":r,"source_bytes":len(source.encode()),
         "piece_count":len(pieces),"compiled_bytes":len(cnf.physical_dimacs().encode()),
         "compiled_clause_count":len(cnf.clauses),"compiled_variable_count":cnf.vars})
        check(all(len({abs(lit) for lit in cl})==3 for cl in cnf.clauses))

    # Projected first-true branches can overlap (counting them overcounts).
    pieces, raw = first_true_parts(3,[],[((0,1),(1,1),(2,1))],[1,2])
    y=1  # retained y_1=1, y_2=0
    signatures=[]
    for j in range(3):
        eqs=[(1<<i,0) for i in range(j)]
        eqs.append((1<<j,1))
        pj=linear_project(3,eqs,[1,2])
        if piece_accepts(pj,y):
            signatures.append(j)
    check(len(signatures)==2 and signatures==[0,1],"Projected branches overlap")

    result={"status":"PASS","seed":SEED,"assertions":checks,
        "source_cases":source_cases,"SAT_cases":sat_cases,"UNSAT_cases":unsat_cases,"exact_projected_port_assignments":projection_assignments,
        "compiled_cnf_port_dpll_comparisons":dpll_assignments,
        "max_compiled_physical_bits":compiled_max_bits, "disjoint_or3_compilation_growth":expansion_examples,
        "max_satisfiable_raw_first_true_branches":raw_branches_max,
        "affine_cover_architecture":[{"r":r,"model_count":7**r,"max_one_affine_piece":4**r,"pieces_needed_at_least":(7**r+4**r-1)//(4**r),"known_achievable_single_piece":4**r} for r in range(1,7)],
        "projected_first_true_overlap_example":{"clause":"x0 OR x1 OR x2","eliminated":"x0","retained":"x1=1,x2=0","feasible_first_true_branch_indices":signatures},
        "theorem_status":{"mixed_affine_union":"PROVED_RESTRICTED","affine_cover_exponential":"PROVED_RESTRICTED","sat_time_lower_bound":"NOT_CLAIMED","unrestricted_sat_shrinker":"OPEN"}}
    return result

if __name__=='__main__':
    result=run()
    output=Path(__file__).with_name('LSPV4_MIXED_AFFINE_PORT218_raw.json')
    output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True,indent=2))
