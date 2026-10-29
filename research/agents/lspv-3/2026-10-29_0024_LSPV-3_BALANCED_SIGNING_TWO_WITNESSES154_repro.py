#!/usr/bin/env python3
"""LSPV-3 BALANCED-SIGNING-TWO-WITNESSES154.

Dependency-free reproducibility checks for a constructive perfect-matching
lemma on 4-regular, 3-uniform incidence systems. Nothing in this script
establishes a general SAT algorithm or a resource lower bound.
"""
import collections
import hashlib
import itertools
import json
import random
import sys
from pathlib import Path

SEED = 202610290024
HERE = Path(__file__).resolve().parent
C = 0

def check(cond, msg):
    global C
    C += 1
    if not cond:
        raise AssertionError(msg)

def w1_controls():
    u = '-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
    s = '-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14'
    parse = lambda v: tuple(tuple(map(int, e.split())) for e in v.split(';'))
    return parse(u),parse(s)

def support(source):
    return tuple(tuple(abs(x) for x in clause) for clause in source)

def check_support(scopes, n):
    counts = collections.Counter(x for triple in scopes for x in triple)
    if set(counts) != set(range(1,n+1)):
        return False
    return len(scopes)*3 == n*4 and all(len(c)==3 and len(set(c))==3 for c in scopes) and all(counts[i]==4 for i in range(1,n+1))

def check_exact22(formula,n):
    if not check_support(support(formula),n): return False
    counts = collections.Counter()
    for clause in formula:
        for lit in clause:
            counts[(abs(lit),lit>0)] += 1
    return all(counts[(v,True)] == counts[(v,False)] == 2 for v in range(1,n+1))

def connected(scopes,n):
    v_to_c = [[] for _ in range(n)]
    for j,c in enumerate(scopes):
        for v in c:
            v_to_c[v-1].append(j)
    sv,sc={0},set()
    todo=[('v',0)]
    while todo:
        t,i=todo.pop()
        if t=='v':
            for j in v_to_c[i]:
                if j not in sc:sc.add(j);todo.append(('c',j))
        else:
            for v in scopes[i]:
                if v-1 not in sv:sv.add(v-1);todo.append(('v',v-1))
    return len(sv)==n and len(sc)==len(scopes)

def four_matchings(scopes,n):
    """Four edge-disjoint perfect matchings after dummy left-node completion.
    n must be divisible by 3, m=4n/3, and scopes must be proper 3-uniform,
    each source variable degree exactly four. Code uses a simple augmenting
    path routine; not a specialized bit-time-optimized implementation.
    """
    assert check_support(scopes,n)
    m = len(scopes)
    assert n % 3 == 0 and m%4 == 0 and n+n//3==m
    adj=[set() for _ in range(m)]
    for j,c in enumerate(scopes):
        for v in c: adj[v-1].add(j)
        adj[n+j//4].add(j)
    assert all(len(a)==4 for a in adj)
    original_edge_count=4*m
    colors={}
    visits=0
    for color in range(4):
        mt=[-1]*m
        def dfs(left,seen):
            nonlocal visits
            # sorted ensures deterministic, reproducible output
            for right in sorted(adj[left]):
                visits += 1
                if right in seen:continue
                seen.add(right)
                if mt[right]==-1 or dfs(mt[right],seen):
                    mt[right]=left
                    return True
            return False
        for left in range(m):
            if not dfs(left,set()):
                raise AssertionError('perfect matching failed in a regular bipartite graph')
        check(sorted(mt)==list(range(m)),f'matching {color} is perfect')
        for right,left in enumerate(mt):
            check(right in adj[left],'matching edge must exist')
            colors[(left,right)]=color
            adj[left].remove(right)
        check(all(len(v)==3-color for v in adj),f'remaining graph {3-color}-regular')
    check(len(colors)==original_edge_count,'colored every incidence, dummy included')
    return colors,visits

def balanced_signing(scopes,n):
    colors,visits=four_matchings(scopes,n)
    result=[]
    counts=collections.Counter()
    for j,c in enumerate(scopes):
        lits=[]
        for v in c:
            col=colors[(v-1,j)]
            lit = -v if col < 2 else v
            lits.append(lit)
            counts[(v,col<2)]+=1
        result.append(tuple(lits))
    F=tuple(result)
    check(check_exact22(F,n),'two positive and two negative per variable')
    check(all(1<=sum(x<0 for x in clause)<=2 for clause in F),
          'every clause is mixed polarity')
    return F,visits

def satisfies(F,mask,n):
    return all(any(((mask>>(abs(l)-1))&1)==(l>0) for l in c) for c in F)

def fiber(F,n,y):
    bits=0
    for mask in range(1<<n):
        if satisfies(F,mask,n):
            bits |= 1<<((mask>>(y-1))&1)
            if bits==3:break
    return bits

def random_support(n,rng):
    assert n%3==0 and n>=6
    for attempt in range(100000):
        stubs=[v for v in range(1,n+1) for _ in range(4)]
        rng.shuffle(stubs)
        clauses=tuple(tuple(stubs[j:j+3]) for j in range(0,len(stubs),3))
        if any(len(set(c))!=3 for c in clauses):continue
        scopes=tuple(tuple(sorted(c)) for c in clauses)
        if len(set(scopes))!=len(scopes):continue
        if not connected(scopes,n):continue
        assert check_support(scopes,n)
        return scopes,attempt
    raise AssertionError('failed to sample a regular, connected proper support')

def cross_product_test():
    checked=0
    for t in range(1,5):
        for mask in range(1<<(4*t)):
            As=[((mask>>(2*i))&1) or ((mask>>(2*i+1))&1) for i in range(t)]
            Bs=[((mask>>(2*t+2*j))&1) or ((mask>>(2*t+2*j+1))&1) for j in range(t)]
            original= any(all(z or a for a in As) and all((not z) or b for b in Bs)
                          for z in (0,1))
            direct=all(a or b for a in As for b in Bs)
            compact=all(As) or all(Bs)
            check(original==direct==compact,'cross product existential equivalence')
            checked+=1
    check(checked==69904,'exact number of quantified assignments')
    return checked

def main():
    rng=random.Random(SEED)
    U,S=w1_controls();n=15;scopes=support(U)
    check(support(S)==scopes,'matched exact-2,2 controls have identical support')
    check(check_exact22(U,n) and check_exact22(S,n),'both source controls balanced')
    check(connected(scopes,n),'matched support connected')
    easy,checks=balanced_signing(scopes,n)
    check(satisfies(easy,0,n),'zero witness SAT')
    check(satisfies(easy,(1<<n)-1,n),'one witness SAT')
    check(not any(satisfies(U,x,n) for x in range(1<<n)),'W1 U UNSAT by exhaustive 2^15')
    check(any(satisfies(S,x,n) for x in range(1<<n)),'W1 S SAT by exhaustive 2^15')
    f = {'U':fiber(U,n,1),'S':fiber(S,n,1),'two_witness_signing':fiber(easy,n,1)}
    check(f['U']==0 and f['two_witness_signing']==3,'contrasting 1-bit exact tables')
    cases=[]
    for n in (6,9,12,15,30,60,120):
        reps=10 if n<=30 else 4
        for j in range(reps):
            scopes,attempts=random_support(n,rng)
            E,visits=balanced_signing(scopes,n)
            check(satisfies(E,0,n) and satisfies(E,(1<<n)-1,n), 'both witnesses')
            cases.append({'n':n,'m':len(scopes),'rejection_attempts':attempts,
                          'matching_edge_visits':visits,'witnesses':2})
    checked=cross_product_test()
    # Strictly account native simulated transitions separately from algorithmic
    # edge-visit counts; no crossing-sequence or UTM numerical assertion.
    output={
      'status':'PASS','seed':SEED,'assertion_groups':C,
      'proof_strategy':'regular bipartite four-edge-colouring via four perfect matchings',
      'controls':{
          'variables':15,'clauses':20,'unsigned_scopes_identical':True,
          'W1_U_label':'UNSAT','W1_S_label':'SAT',
          'two_witness_balanced_signing':'SAT',
          'single_boundary_y1_projection_bitmask':f,
          'two_witness_matching_edge_visits':checks,
          'two_witness_signed_clauses':[list(c) for c in easy],
      },
      'random_regular_supports':len(cases),
      'examples':cases,
      'cross_product_assignments':checked,
      'limitations':['Unrestricted exact22 SAT remains NP-complete.',
                     'Every unsigned support has at least one easy signing, not every signing is easy.',
                     'Matching edge visits are not single-tape TM steps.',
                     'Finite tests are not a proof of the all-size combinatorial result.',
                     'No universal SAT shrinker or SAT decision-time lower bound is established.']
    }
    print(json.dumps(output,indent=2,sort_keys=True))

if __name__=='__main__':main()
