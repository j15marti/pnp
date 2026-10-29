#!/usr/bin/env python3
"""AFFINE-LIFT-BVE229: independent exact-(2,2) bounded-variable-elimination controls.

Dependency-free deterministic reproducer.  It never invokes a SAT oracle.
Exact finite tests validate the proof's local construction, not P vs NP.
"""
import itertools, json, math, hashlib, random
from collections import Counter, deque


def base_design():
    points = tuple((x, y) for x in range(3) for y in range(3))
    clauses = []
    for typ in range(4):
        for const in range(3):
            line = []
            for x, y in points:
                lhs = (x, y, y-x, y-2*x)[typ] % 3
                if lhs == const: line.append(3*x+y)
            assert len(line) == 3
            clauses.append((typ, const, tuple(line)))
    assert len(clauses) == 12
    assert len({tuple(sorted(p)) for _, _, p in clauses}) == 12
    pcount = Counter(p for _,_,line in clauses for p in line)
    pairs = Counter(tuple(sorted(ab)) for _,_,line in clauses for ab in itertools.combinations(line,2))
    assert set(pcount.values()) == {4} and len(pcount)==9
    assert len(pairs)==36 and set(pairs.values())=={1}
    assert all(set(typ for typ,_,line in clauses if p in line)=={0,1,2,3} for p in range(9))
    return clauses

BASE = base_design()


def lifted_formula(r):
    """Twist one incidence edge of a cyclic r-fold connected graph cover."""
    assert r>=1
    lines=[]
    for t in range(r):
        for j,(typ,const,ps) in enumerate(BASE):
            pts = tuple(p*r + ((t+1)%r if (j==0 and p==0) else t) for p in ps)
            sign = 1 if typ in (0,1) else -1
            lines.append(tuple(sign*(p+1) for p in pts))
    return 9*r, tuple(lines)


def check_structure(n, clauses):
    assert n%9==0 and len(clauses)==4*n//3
    degree=Counter()
    signed=Counter()
    paircounts=Counter()
    adjacency={v:set() for v in range(1,n+1)}
    scopes=[]
    for i,c in enumerate(clauses):
        assert len(c)==3 and all(1<=abs(v)<=n for v in c)
        names=[abs(v) for v in c]
        assert len(set(names))==3
        assert tuple(sorted(names)) not in scopes
        scopes.append(tuple(sorted(names)))
        for v in c: degree[abs(v)]+=1; signed[(abs(v),1 if v>0 else -1)]+=1
        for a,b in itertools.combinations(names,2):
            paircounts[tuple(sorted((a,b)))]+=1
            adjacency[a].add(b); adjacency[b].add(a)
    assert set(degree)==set(range(1,n+1))
    assert set(degree.values())=={4}
    assert all(signed[(v,1)]==2 and signed[(v,-1)]==2 for v in range(1,n+1))
    assert max(paircounts.values())==1
    seen={1}; stack=[1]
    while stack:
        for w in adjacency[stack.pop()]:
            if w not in seen: seen.add(w);stack.append(w)
    assert len(seen)==n
    return {'variables':n,'clauses':len(clauses),'unique_variable_pairs':len(paircounts),'pair_multiplicity_max':max(paircounts.values()),'connected':True, 'balanced':True}


def canon_clause(cl):
    return tuple(sorted(cl,key=lambda z:(abs(z),z)))


def resolution_data(clauses, pivot):
    pos=[c for c in clauses if pivot in c]
    neg=[c for c in clauses if -pivot in c]
    rest=[c for c in clauses if pivot not in c and -pivot not in c]
    out=[]
    for c in pos:
        for d in neg:
            lits=[z for z in c if abs(z)!=pivot]+[z for z in d if abs(z)!=pivot]
            if any(-z in lits for z in lits): continue
            z=canon_clause(set(lits))
            if z not in out:out.append(z)
    return pos,neg,rest,out


def split_clause(cl, next_free):
    """One OR clause, exactly Tseitin-equivalent after existentially forgetting fresh u."""
    c = tuple(cl)
    assert len(c) >= 3
    if len(c) == 3:
        return [c], next_free, []
    first = next_free
    next_free += 1
    aux = [first]
    out = [(c[0], c[1], first)]
    prev = first
    for j in range(2, len(c)-2):
        new = next_free
        next_free += 1
        aux.append(new)
        out.append((-prev, c[j], new))
        prev = new
    out.append((-prev, c[-2], c[-1]))
    assert len(out) == len(c)-2 and len(aux) == len(c)-3
    assert all(len(row) == 3 for row in out)
    return out, next_free, aux


def renumber_dense(cnf, original_aux):
    """Charge source-ID normalization explicitly; return old-to-new correspondence."""
    ids = sorted(set(abs(z) for c in cnf for z in c))
    old_original = [x for x in ids if x not in original_aux]
    surviving_aux = [x for x in ids if x in original_aux]
    ids = old_original + surviving_aux
    mp = {old: j+1 for j, old in enumerate(ids)}
    new_cnf = tuple(tuple(mp[abs(z)]*(1 if z>0 else -1) for z in c) for c in cnf)
    return new_cnf, tuple(mp[a] for a in surviving_aux), mp

def split_all(cnf,n):
    next_free=n+1
    new=[];aux=[]
    for cl in cnf:
        repl,next_free,created=split_clause(cl,next_free)
        new.extend(repl);aux.extend(created)
    return tuple(new),next_free-1,tuple(aux)


def eliminate_and_reenter(formula, n, pivot):
    pos, neg, rest, res = resolution_data(formula, pivot)
    # First produce exact projection, then convert each long OR back to 3CNF.
    new, last_id, aux = split_all(rest+res, n)
    # Dense source names are essential to the claimed exact physical bit count.
    new, dense_aux, mp = renumber_dense(new, set(aux))
    new_n = len(mp)
    assert max(abs(z) for c in new for z in c) == new_n
    return {'p':len(pos),'q':len(neg),'resolvent_count':len(res),
            'resolvent_widths':list(map(len,res)), 'resolvents':res,
            'clauses':new,'variables':new_n,'aux':dense_aux,
            'source_to_child':{old:mp[old] for old in range(1,n+1) if old in mp}}

def sat(cnf,bits):
    return all(any(((bits[abs(z)-1]) if z>0 else (not bits[abs(z)-1])) for z in c) for c in cnf)


def compact_bits(n,m):
    w=math.ceil(math.log2(64*(n+m+1)))
    return {'word_bits':w,'physical_bits':(4*m+2)*w}


def local_projection_check(cnf,pivot):
    pos,neg,rest,res=resolution_data(cnf,pivot)
    assert len(pos)==len(neg)==2 and len(res)==4
    assert set(len(x) for x in res)=={4}
    vars8=sorted(set(abs(y) for c in pos+neg for y in c if abs(y)!=pivot))
    assert len(vars8)==8
    split,_,aux=split_all(res,max(vars8))
    assert len(aux)==4 and len(split)==8
    tests=0
    for a in itertools.product([False,True],repeat=8):
        assign={v:a[i] for i,v in enumerate(vars8)}
        def check_some(clauses,free):
            for fs in itertools.product([False,True],repeat=len(free)):
                env={**assign,**dict(zip(free,fs))}
                if all(any((env[abs(z)] if z>0 else not env[abs(z)]) for z in c) for c in clauses):return True
            return False
        lhs=check_some(pos+neg,[pivot])
        rhs=check_some(split,list(aux))
        mid=check_some(res,[])
        assert lhs==mid==rhs
        tests+=1
    return tests


def random_balanced_signing(n, clauses, rng):
    """Keep support, signed degree, and all 3-clause scopes fixed."""
    places = {v: [] for v in range(1,n+1)}
    new = [list(c) for c in clauses]
    for i,c in enumerate(new):
        for j,z in enumerate(c): places[abs(z)].append((i,j))
    for v,occ in places.items():
        assert len(occ)==4
        rng.shuffle(occ)
        for t,(i,j) in enumerate(occ): new[i][j]=v if t<2 else -v
    return tuple(tuple(c) for c in new)


def main():
    allrows=[];local_tests=0;first_elim_checks=0;second_rows=[];second_tests=0
    for r in (1,2,3,5,8,12,20):
        n,clauses=lifted_formula(r)
        row=check_structure(n,clauses)
        base_size=compact_bits(n,len(clauses))
        variants=[]
        for pivot in range(1,n+1):
            e=eliminate_and_reenter(clauses,n,pivot)
            assert (e['p'],e['q'],e['resolvent_count'])==(2,2,4)
            assert e['resolvent_widths']==[4]*4
            assert len(e['aux'])==4
            assert len(e['clauses'])==len(clauses)+4
            # n source variables minus pivot plus four auxiliaries.
            assert e['variables']==n+3
            after=compact_bits(n+3,len(e['clauses']))
            assert after['physical_bits']>base_size['physical_bits']
            assert all(len(cl)==3 for cl in e['clauses'])
            # Check invariants: all eight former neighbors gain one occurrence;
            # each new auxiliary appears twice; exact22 has ceased to hold.
            old_counts=Counter(abs(z) for cl in clauses for z in cl)
            new_counts=Counter(abs(z) for cl in e['clauses'] for z in cl)
            assert pivot not in e['source_to_child']
            assert sorted([new_counts[new]-old_counts[old] for old,new in e['source_to_child'].items()]).count(1)==8
            assert all(new_counts[v]==2 for v in e['aux'])
            variants.append(after['physical_bits'])
            first_elim_checks+=1
            if r<=2 and pivot in (1,2,n):local_tests+=local_projection_check(clauses,pivot)
        row.update({'base_encoding_bits':base_size['physical_bits'],'base_word_bits':base_size['word_bits'],
                    'all_pivots_checked':n,'all_pivot_reentry_bits_min':min(variants),
                    'all_pivot_reentry_bits_max':max(variants),'after_variables':n+3,
                    'after_clauses':len(clauses)+4,
                    'literal_token_count_before':3*len(clauses),
                    'literal_token_count_after':3*(len(clauses)+4)})
        allrows.append(row)
        if r==1:
            for pivot in range(1,n+1):
                e1=eliminate_and_reenter(clauses,n,pivot)
                # Test repeated local elimination with exact native re-entry.
                first=compact_bits(n+3,len(e1['clauses']))['physical_bits']
                counts={'orig':[],'aux':[]}
                for other in range(1,e1['variables']+1):
                    try:
                        e2=eliminate_and_reenter(e1['clauses'],e1['variables'],other)
                    except AssertionError:
                        continue
                    size=compact_bits(e2['variables'],len(e2['clauses']))['physical_bits']
                    cats='aux' if other in e1['aux'] else 'orig'
                    counts[cats].append({'other':other,'bits':size,'versus_first':size-first,'vs_parent':size-compact_bits(n,len(clauses))['physical_bits'],'resolvents':e2['resolvent_count'],'widths':sorted(e2['resolvent_widths'])})
                    second_tests+=1
                second_rows.append({'pivot':pivot,'second':counts})
    # Independent sign changes preserve the local non-shrink invariant.
    rng=random.Random(22920261029)
    random_signs={'cases':0,'all_pivots':0,'sat_samples_n9':0,'unsat_samples_n9':0}
    for r,reps in [(1,64),(2,32),(3,16)]:
        n,base=lifted_formula(r)
        for _ in range(reps):
            cl=random_balanced_signing(n,base,rng)
            check_structure(n,cl)
            for v in range(1,n+1):
                z=eliminate_and_reenter(cl,n,v)
                assert z['resolvent_widths']==[4]*4 and z['variables']==n+3
                assert len(z['clauses'])==len(cl)+4
                random_signs['all_pivots']+=1
            random_signs['cases']+=1
            if r==1:
                answer=any(sat(cl,bits) for bits in itertools.product([False,True],repeat=n))
                random_signs['sat_samples_n9' if answer else 'unsat_samples_n9']+=1
    result={'name':'AFFINE_LIFT_BVE229','status':'COMPUTATIONAL finite; PROVED restricted by separate math',
            'design':'Affine plane F_3^2, 12 lines, r-fold twisted incidence lift; signs by two positive and two negative parallel classes',
            'rows':allrows,'randomized_signs':random_signs,'first_pivot_checks':first_elim_checks,'exact_local_equisat_8bit_assignments':local_tests,
            'second_step_cases':second_tests,'second_level':second_rows,
            'no_general_algorithm_claim':True}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
