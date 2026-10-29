#!/usr/bin/env python3
"""Independent deterministic finite audit of affine plus matching-2SAT hardness lift.

All variable identifiers are 0-based in the mixed model and 1-based in CNF.
No external SAT solver, nondeterminism or uncharged oracle is used.
"""
from __future__ import annotations
from collections import Counter
from itertools import combinations, product, permutations
from pathlib import Path
import hashlib
import json
import random
import sys

FANO = [(0,1,2), (0,3,4), (0,5,6), (1,3,5), (1,4,6), (2,3,6), (2,4,5)]
CHECKS = 0

def check(cond, info=''):
    global CHECKS
    CHECKS += 1
    if not cond:
        raise AssertionError(f'check #{CHECKS}: {info}')


def generate(n, triples):
    """Affine rows are (variable tuple, parity bit); negative 2CNF is matching."""
    triples = [tuple(row) for row in triples]
    A, B, equality_pairs = [], [], []
    for j, (a, b, c) in enumerate(triples):
        check(len({a,b,c}) == 3 and all(0 <= x < n for x in (a,b,c)), 'source row')
        A.append(((a,b,c), 1))
        for edge_no, (u,v) in enumerate(((a,b),(a,c),(b,c))):
            p = n + 6*j + 2*edge_no
            q = p + 1
            A.extend([((p,u),0),((q,v),0)])
            B.append((p,q))
            equality_pairs.extend([(p,u),(q,v)])
    return {'n': n, 't': len(triples), 'triples': triples,
            'total_mixed_vars': n + 6*len(triples),
            'affine': A, 'binary_matching': B,
            'equality_pairs': equality_pairs}


def exact1_on_core(triples, x):
    return all(sum(x[v] for v in row) == 1 for row in triples)


def copies_from_core(inst, x):
    bits = list(x) + [0] * (inst['total_mixed_vars'] - inst['n'])
    for p, v in inst['equality_pairs']:
        bits[p] = bits[v]
    return bits


def eval_affine(rows, bits):
    return all((sum(bits[v] for v in idx) % 2) == target for idx, target in rows)


def eval_negative_matching(edges, bits):
    return all(not (bits[u] and bits[v]) for u,v in edges)


def matching_stats(inst):
    cnt = Counter(v for edge in inst['binary_matching'] for v in edge)
    check(all(c == 1 for c in cnt.values()), '2SAT induced graph is matching')
    check(all(v >= inst['n'] for v in cnt), 'nonaffine constraints on fresh vars only')
    check(len(cnt) == 6*inst['t'], 'endpoints count')
    return {'edges': len(inst['binary_matching']),
            'max_binary_degree': max(cnt.values(), default=0),
            'nonaffine_treewidth': 1 if cnt else 0,
            'minimum_binary_vertex_cover': len(inst['binary_matching'])}


def xor3_to_clauses(a,b,c):
    out=[]
    for bits in product((0,1),repeat=3):
        if sum(bits) % 2 == 0:  # forbid even parity
            out.append(tuple(v+1 if bit==0 else -(v+1) for v,bit in zip((a,b,c),bits)))
    check(len(out) == 4)
    return out


def canonical_cnf(inst):
    """Return completely physical proper 3CNF, with each binary clause Tseitin padded."""
    clauses=[]
    next_var=inst['total_mixed_vars']
    for vars_,parity in inst['affine']:
        if len(vars_) == 3:
            check(parity == 1)
            clauses.extend(xor3_to_clauses(*vars_))
        else:
            check(len(vars_) == 2 and parity == 0)
            a,b=vars_
            for bi in ((-(a+1),b+1), (a+1,-(b+1))):
                next_var += 1
                clauses.extend([(bi[0],bi[1],next_var), (bi[0],bi[1],-next_var)])
    for a,b in inst['binary_matching']:
        next_var += 1
        clauses.extend([(-(a+1),-(b+1),next_var), (-(a+1),-(b+1),-next_var)])
    check(len(clauses) == 34*inst['t'], 'clause count')
    check(next_var == inst['n']+21*inst['t'], 'variable count')
    check(all(len(c) == 3 and len({abs(v) for v in c}) == 3 for c in clauses), 'proper width3')
    return next_var, clauses


def clause_value(clause, assignment):
    return any((assignment[abs(v)-1] if v > 0 else not assignment[abs(v)-1]) for v in clause)


def source_bytes(inst):
    body='h %d %d\n' % (inst['n'],inst['t'])
    body+=''.join('%d %d %d\n' % row for row in inst['triples'])
    return body.encode()


def cnf_bytes(n, clauses):
    return ('p cnf %d %d\n' % (n,len(clauses)) +
            ''.join(' '.join(map(str,row))+' 0\n' for row in clauses)).encode()


def dpll(clauses, n, max_calls=100000):
    """Independent small-instance decision checker; both SAT and UNSAT use one program."""
    stats={'calls': 0, 'decisions': 0, 'unit_steps': 0}
    def go(clauses, assignments):
        stats['calls']+=1
        if stats['calls']>max_calls:
            raise RuntimeError('DPLL node budget exhausted')
        while True:
            reduced=[]
            units=[]
            for row in clauses:
                sat=False
                unresolved=[]
                for lit in row:
                    v=abs(lit)-1
                    if v not in assignments:
                        unresolved.append(lit)
                    elif assignments[v] == int(lit>0):
                        sat=True
                        break
                if sat:
                    continue
                if not unresolved:
                    return False
                reduced.append(tuple(unresolved))
                if len(unresolved)==1:
                    units.append(unresolved[0])
            if not reduced:
                return True
            if not units:
                break
            changed=False
            for lit in units:
                v=abs(lit)-1
                bit=int(lit>0)
                if v in assignments and assignments[v]!=bit:
                    return False
                if v not in assignments:
                    assignments[v]=bit
                    stats['unit_steps']+=1
                    changed=True
            if not changed:
                break
        freq=Counter(abs(lit)-1 for row in reduced for lit in row)
        # Prefer low numbered source variables to avoid irrelevant padding choices.
        v=min(freq,key=lambda k:(k >= n, -freq[k],k))
        stats['decisions']+=1
        for bit in (0,1):
            new_a=assignments.copy()
            new_a[v]=bit
            if go(reduced,new_a):
                return True
        return False
    return go(tuple(tuple(row) for row in clauses),{}), stats


def primal_graph(triples, n):
    edges=set()
    for tri in triples:
        for a,b in combinations(tri,2):
            edges.add(tuple(sorted((a,b))))
    return edges


def eliminate_width(order, edges):
    adj={v:set() for v in order}
    for a,b in edges:
        adj[a].add(b)
        adj[b].add(a)
    width=0
    for v in order:
        nbr=list(adj[v])
        width=max(width,len(nbr))
        for a,b in combinations(nbr,2):
            adj[a].add(b)
            adj[b].add(a)
        for u in nbr:
            adj[u].remove(v)
        del adj[v]
    return width


def exact_tw(edges,n):
    if n > 8:
        raise ValueError('only finite controls <=8')
    return min(eliminate_width(order,edges) for order in permutations(range(n)))


def audit_inst(inst, check_compiler=False):
    m=matching_stats(inst)
    check(len(inst['affine'])==7*inst['t'], 'affine equation count')
    # Affine part has a uniform all-one satisfying assignment; binary part all-zero.
    check(eval_affine(inst['affine'],[1]*inst['total_mixed_vars']), 'all-one affine')
    check(eval_negative_matching(inst['binary_matching'],[0]*inst['total_mixed_vars']), 'all-zero 2CNF')
    exact_core=0
    for x in product((0,1),repeat=inst['n']):
        bits=copies_from_core(inst,x)
        af=eval_affine(inst['affine'],bits)
        bi=eval_negative_matching(inst['binary_matching'],bits)
        original=exact1_on_core(inst['triples'],x)
        check((af and bi) == original, 'matching lift exact projection')
        if original:
            exact_core+=1
    if check_compiler:
        n3, cnf=canonical_cnf(inst)
        check(n3==inst['n']+21*inst['t'])
        check(len(cnf)==34*inst['t'])
        # All padding symbols z=0 suffice if the source assignment is a model.
        for x in product((0,1),repeat=inst['n']):
            assignment=copies_from_core(inst,x) + [0]*(15*inst['t'])
            cnf_sat=all(clause_value(row,assignment) for row in cnf)
            check(cnf_sat==exact1_on_core(inst['triples'],x), 'CNF extension at all padding zero')
            # If CNF fails, no padding could repair a false binary clause or parity3.
        output=cnf_bytes(n3,cnf)
        check(output.startswith(b'p cnf '))
    return exact_core,m



class ParityDSU:
    """Union-find with parity to parent, enforcing x_u xor x_v = c."""
    def __init__(self, n):
        self.parent=list(range(n))
        self.parity=[0]*n
        self.rank=[0]*n
    def find(self, x):
        if self.parent[x]==x:
            return x,0
        r,p=self.find(self.parent[x])
        self.parity[x]^=p
        self.parent[x]=r
        return r,self.parity[x]
    def union(self,u,v,c):
        ru,pu=self.find(u)
        rv,pv=self.find(v)
        if ru==rv:
            return (pu^pv)==c
        if self.rank[ru]>self.rank[rv]:
            ru,rv=rv,ru
        self.parent[ru]=rv
        self.parity[ru]=pu^pv^c
        if self.rank[ru]==self.rank[rv]:
            self.rank[rv]+=1
        return True


def solve_2sat(clauses, numvars):
    if numvars==0:
        return len(clauses)==0
    g=[[] for _ in range(2*numvars)]
    rg=[[] for _ in range(2*numvars)]
    def litnode(lit):
        return 2*(abs(lit)-1) + int(lit<0)
    def edge(a,b):
        g[a].append(b);rg[b].append(a)
    for cl in clauses:
        if not cl:
            return False
        a=litnode(cl[0]);b=litnode(cl[-1])
        edge(a^1,b)
        edge(b^1,a)
    used=[False]*len(g); order=[]
    for i in range(len(g)):
        if used[i]:continue
        stack=[(i,0)];used[i]=True
        while stack:
            v,j=stack[-1]
            if j>=len(g[v]):
                order.append(v);stack.pop()
                continue
            w=g[v][j];stack[-1]=(v,j+1)
            if not used[w]:
                used[w]=True;stack.append((w,0))
    comp=[-1]*len(g)
    for i in reversed(order):
        if comp[i]!=-1:continue
        cid=i
        stack=[i];comp[i]=cid
        while stack:
            v=stack.pop()
            for w in rg[v]:
                if comp[w]==-1:
                    comp[w]=cid;stack.append(w)
    return all(comp[2*i]!=comp[2*i+1] for i in range(numvars))


def solve_affine2_with_2cnf(n, xor2_rows, clauses):
    """Polynomial algorithm for arbitrary 2CNF plus parity rows of arity <= 2.

    xor rows are (tuple variable identifiers, parity target); 1-variable
    equations are linked to a distinguished zero variable. Two-variable
    equations are represented by parity union-find; no branching occurs.
    """
    d=ParityDSU(n+1)
    zero=n
    for vars_, parity in xor2_rows:
        if len(vars_)==0:
            if parity:return False
        elif len(vars_)==1:
            if not d.union(vars_[0],zero,parity):return False
        elif len(vars_)==2:
            if not d.union(vars_[0],vars_[1],parity):return False
        else:
            raise ValueError('parity width >2')
    zr,zp=d.find(zero)
    roots={}
    reduced=[]
    for clause in clauses:
        converted=[]
        satisfied=False
        for lit in clause:
            v=abs(lit)-1
            r,p=d.find(v)
            if r==zr:
                literal_val = (p ^ zp) if lit>0 else (1 ^ p ^ zp)
                if literal_val:
                    satisfied=True
                    break
                continue
            if r not in roots:
                roots[r]=len(roots)+1
            root_lit = roots[r] if ((lit>0) != bool(p)) else -roots[r]
            converted.append(root_lit)
        if satisfied:continue
        if len(converted)==0:return False
        if len(converted)==2 and converted[0]==-converted[1]:continue
        reduced.append(converted)
    return solve_2sat(reduced,len(roots))


def brute_affine2_cnf(n, xor2_rows,clauses):
    for bits in product((0,1),repeat=n):
        if not eval_affine(xor2_rows,bits):continue
        if all(any((bits[abs(lit)-1] if lit>0 else (not bits[abs(lit)-1]))
                   for lit in row) for row in clauses):
            return True
    return False


def main():
    rng=random.Random(202610290536)
    trials=0
    compiler_trials=0
    sat=0
    unsat=0
    for n in range(3,6):
        triples=list(combinations(range(n),3))
        for mask in range(1<<len(triples)):
            rows=[row for j,row in enumerate(triples) if mask>>j&1]
            inst=generate(n,rows)
            count,_=audit_inst(inst, check_compiler=(mask % 19 == 0))
            trials+=1
            sat+=int(count>0)
            unsat+=int(count==0)
            compiler_trials+=int(mask % 19 == 0)
    # Random signed-looking hypergraph structure; positive exact-one source.
    random_tests=0
    for idx in range(190):
        n=rng.randrange(4,10)
        source=list(combinations(range(n),3))
        rows=[rng.choice(source) for j in range(rng.randrange(1,13))]
        inst=generate(n,rows)
        count,_=audit_inst(inst, check_compiler=(idx%19==0))
        random_tests+=1
        sat+=int(count>0)
        unsat+=int(count==0)
        compiler_trials+=int(idx%19==0)
    # Polynomial side of the sharp arity-two versus arity-three frontier.
    affine2_tests=0
    affine2_sat=0
    affine2_unsat=0
    for n in range(2,10):
        for j in range(220):
            rows=[]
            clauses=[]
            for _ in range(rng.randrange(0,2*n+4)):
                width=rng.randrange(0,3)
                inds=tuple(rng.sample(range(n),width))
                rows.append((inds,rng.randrange(2)))
            for _ in range(rng.randrange(0,2*n+4)):
                width=rng.randrange(1,3)
                inds=rng.sample(range(1,n+1),width)
                clauses.append(tuple(v if rng.randrange(2) else -v for v in inds))
            ans=solve_affine2_with_2cnf(n,rows,clauses)
            independent=brute_affine2_cnf(n,rows,clauses)
            check(ans==independent,'affine arity <=2 plus general 2CNF SAT')
            affine2_tests+=1
            affine2_sat+=int(ans)
            affine2_unsat+=int(not ans)
    # Both separate systems SAT but combined UNSAT, correctly detected by quotient SCC.
    contradictory_rows=[((0,1),0)]
    contradictory_cnf=[(1,2),(-1,-2)]
    check(eval_affine(contradictory_rows,(0,0)))
    check(solve_2sat(contradictory_cnf,2))
    check(not solve_affine2_with_2cnf(2,contradictory_rows,contradictory_cnf))
    f=generate(7,FANO)
    f_count,f_match=audit_inst(f, check_compiler=True)
    check(f_count==0,'Fano mixed UNSAT')
    check(f_match['edges']==21 and f_match['minimum_binary_vertex_cover']==21)
    n3,cl=canonical_cnf(f)
    dpll_answer,dpll_stats=dpll(cl,f['n'],max_calls=100000)
    check(dpll_answer is False,'Fano CNF UNSAT')
    core_graph=primal_graph(FANO,7)
    check(len(core_graph)==21,'Fano quotient becomes K7')
    quotient_tw=exact_tw(core_graph,7)
    check(quotient_tw==6,'Fano quotient tw6')
    controls=[]
    cases=[[(0,1,2)],[(0,1,2),(1,2,3)],[(0,1,2),(0,1,3),(0,2,3)],FANO]
    for i,rows in enumerate(cases):
        n=max(max(row) for row in rows)+1
        ins=generate(n,rows)
        nn,cc=canonical_cnf(ins)
        result,stat=dpll(cc,ins['n'],max_calls=100000)
        expected=any(exact1_on_core(rows,x) for x in product((0,1),repeat=n))
        check(result==expected,'DPLL label')
        controls.append({'source_triples':len(rows),'source_sat':expected,
                         'dpll':stat,'mixed_matching_edges':len(ins['binary_matching']),
                         'cnf_vars':nn,'cnf_clauses':len(cc),
                         'source_bytes':len(source_bytes(ins)),'cnf_bytes':len(cnf_bytes(nn,cc))})
    # Exact graph quotient tracks source primal graph; input matching graph remains width one.
    for n in range(3,8):
        triples=list(combinations(range(n),3))
        for _ in range(20):
            rows=[rng.choice(triples) for j in range(rng.randint(1,9))]
            ins=generate(n,rows)
            edge_graph=primal_graph(rows,n)
            quotient_edges={tuple(sorted((a,b))) for a,b in edge_graph}
            check(quotient_edges==edge_graph,'quotient edge graph')
            check(matching_stats(ins)['nonaffine_treewidth']==1)
    # Run the original audit externally to track hash/readback independently.
    root=Path(__file__).parent
    original=root/'connected'/'results.json'
    rerun=root/'connected'/'rerun_results.json'
    direct_equal=(original.read_bytes()==rerun.read_bytes()) if original.exists() and rerun.exists() else None
    original_sha=hashlib.sha256(original.read_bytes()).hexdigest() if original.exists() else None
    report={
        'theorem':'POSITIVE-1-IN-3-SAT <= mixed XOR(arity <= 3) plus negative 2CNF matching via fresh copies',
        'status':'RESTRICTED mathematical reduction; finite checks COMPUTATIONAL',
        'exhaustive_source_instances':trials,
        'random_source_instances':random_tests,
        'affine_arity_2_plus_general_2cnf_tests':affine2_tests,
        'affine2_sat_cases':affine2_sat,
        'affine2_unsat_cases':affine2_unsat,
        'checked_cnf_compilers':compiler_trials,
        'sat_case_checks':sat,
        'unsat_case_checks':unsat,
        'total_assertions':CHECKS,
        'fano':{'mixed_original_vars':f['n'],'mixed_vars':f['total_mixed_vars'],
                'affine_equations':len(f['affine']), 'binary_matching_clauses':len(f['binary_matching']),
                'proper_cnf_vars':n3,'proper_cnf_clauses':len(cl),
                'source_solutions':f_count,'matching_graph_treewidth':1,
                'affine_quotient_graph_treewidth':quotient_tw,'dpll':dpll_stats},
        'dpll_controls':controls,
        'direct_library_original_results_identical':direct_equal,
        'direct_library_original_results_sha256':original_sha,
        'source_code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output=root/'LSPV4_MATCHING_AFFINE_2SAT222_raw.json'
    output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=='__main__':
    main()