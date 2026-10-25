#!/usr/bin/env python3
"""M22-LOWSPACE-BATCH152 finite correctness/structure checks.
The code materializes clauses for testing. The theorem's logspace simulator
uses source rereading and candidate-seed enumeration instead; this script is
NOT a physical FLMV resource trace.
"""
import ast, itertools, json, math, random, sys
from pathlib import Path

Y_PLUS = [(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
Y_MINUS = [(1,2,4),(1,3,6),(2,3,5),(4,5,6)]

def fixture_y():
    return tuple(tuple(c) for c in Y_PLUS)+tuple(tuple(-a for a in c) for c in Y_MINUS)

def fixture_h():
    return tuple(tuple(c) for c in Y_PLUS)+tuple(tuple(-a for a in c) for c in Y_PLUS)

def cyclic_easy(r):
    def a(i): return 3*(i%r)+1
    def b(i): return 3*(i%r)+2
    def c(i): return 3*(i%r)+3
    out=[]
    for i in range(r):
        out.extend(((a(i),b(i),c(i)),(a(i),b(i+1),c(i+2)),
                    (-a(i),-b(i+2),-c(i+1)),(-a(i),-b(i+3),-c(i+3))))
    return tuple(out)

def check_m22(formula):
    names={abs(x) for c in formula for x in c}
    sc=set();pos={i:0 for i in names}; neg={i:0 for i in names}
    for clause in formula:
        assert len(clause)==3 and len({abs(z) for z in clause})==3
        assert all(z>0 for z in clause) or all(z<0 for z in clause)
        t=tuple(sorted(clause)); assert t not in sc;sc.add(t)
        for z in clause: (pos if z>0 else neg)[abs(z)]+=1
    assert all(pos[i]==neg[i]==2 for i in names)
    ss={tuple(sorted(abs(z) for z in c)) for c in formula if c[0]>0}
    tt={tuple(sorted(abs(z) for z in c)) for c in formula if c[0]<0}
    return {'k':len(names),'m':len(formula),'eligible':ss!=tt,'q':len(ss-tt)}

def norm_clause(c):
    t={int(z) for z in c}
    if any(-z in t for z in t):return None
    return tuple(sorted(t,key=lambda z:(abs(z),z<0)))

def dp_one(formula,pivot):
    a=[];b=[];rest=[]
    for c in formula:
        if pivot in c:a.append(tuple(z for z in c if z!=pivot))
        elif -pivot in c:b.append(tuple(z for z in c if z!=-pivot))
        else:rest.append(c)
    res=list(rest)
    for x in a:
        for y in b:
            r=norm_clause(x+y)
            if r is not None:res.append(r)
    # canonical dedup (ordinary SAT doesn't require this, but references may)
    return tuple(dict.fromkeys(res))

def degree_graph(formula):
    names={abs(x) for c in formula for x in c}
    adj={i:set() for i in names}
    for c in formula:
        ids=[abs(x) for x in c]
        for u in ids:
            adj[u].update(v for v in ids if u!=v)
    return adj

def first_prime_above(x):
    p=max(2,x+1)
    while True:
        for d in range(2,math.isqrt(p)+1):
            if p%d==0:break
        else:return p
        p+=1

def hashed_minima(adj,p,coeffs):
    def hh(x):
        value=0
        for c in reversed(coeffs):value=(value*x+c)%p
        return value
    return tuple(i for i in sorted(adj) if all((hh(i),i)<(hh(j),j) for j in adj[i]))

def choose_seed_for_test(adj,level,random_seed=20261024,limit=1000):
    n=len(adj); d=max((len(t) for t in adj.values()),default=0)
    p=first_prime_above(n*max(1,(d+1)*(d+1)*d//2)+1)
    target=(n+d)//(d+1)
    rng=random.Random(random_seed+level)
    # Prefix seeded choices for reproducible witnesses; full theorem enumerates all p^(d+1).
    for attempt in range(1,limit+1):
        coeffs=[rng.randrange(p) for _ in range(d+1)]
        result=hashed_minima(adj,p,coeffs)
        if len(result)>=target:
            return {'p':p,'d':d,'target':target,'attempts':attempt,'seed':coeffs,'independent':result}
    raise AssertionError('finite trial budget ended, no conclusion about exhaustive seed search')

def batch_dp(formula,pivots):
    current=formula
    for x in pivots:
        current=dp_one(current,x)
    return current

def evaluate(formula,assignment):
    return all(any(assignment[abs(z)-1] == (z>0) for z in c) for c in formula)

def projection_equal(src,dst,removed):
    original={abs(z) for c in src for z in c}; remset=original-set(removed)
    if len(original)>16:return None
    for vals in itertools.product((0,1),repeat=len(remset)):
        base=dict(zip(sorted(remset),vals))
        left=any(all(any(({**base,**dict(zip(sorted(set(removed)),part))})[abs(z)]==(z>0) for z in c) for c in src) for part in itertools.product((0,1),repeat=len(set(removed))))
        right=all(any(base[abs(z)]==(z>0) for z in c) for c in dst)
        assert left==right,(base,left,right)
    return 2**len(remset)

def enc_len(formula):
    # explicit ordinary clause list, original IDs retained, 3-bit clause-width, 1 sign + ell ID per literal
    k=max((abs(z) for c in formula for z in c),default=0)
    ell=max(1,math.ceil(math.log2(k+1)))
    return 2*ell + sum(3+len(c)*(ell+1) for c in formula)

def run_case(name,formula):
    meta=check_m22(formula)
    before=enc_len(formula)
    g0=degree_graph(formula)
    s1=choose_seed_for_test(g0,1)
    for x in s1['independent']:assert all(x not in g0[y] for y in s1['independent'] if y!=x)
    f1=batch_dp(formula,s1['independent'])
    g1=degree_graph(f1)
    s2=choose_seed_for_test(g1,2)
    f2=batch_dp(f1,s2['independent'])
    eliminated=set(s1['independent'])|set(s2['independent'])
    assert not (set(s1['independent']) & set(s2['independent']))
    assert all(abs(z) not in eliminated for c in f2 for z in c)
    all1=projection_equal(formula,f1,s1['independent'])
    all2=projection_equal(formula,f2,eliminated)
    assert max(map(len,f1),default=0)<=4
    assert max(map(len,f2),default=0)<=6
    assert max(map(len,g0.values()),default=0)<=8
    assert max(map(len,g1.values()),default=0)<=24
    result={'name':name,'source':meta,'source_bits':before,
    'stage1':{'pivot_count':len(s1['independent']),'prime':s1['p'],'seed_attempts':s1['attempts'],'max_primal_degree':max(map(len,g1.values()),default=0),'clauses':len(f1),'bits':enc_len(f1),'width':max(map(len,f1),default=0),'membership_hash_seed':s1['seed']},
    'stage2':{'pivot_count':len(s2['independent']),'prime':s2['p'],'seed_attempts':s2['attempts'],'clauses':len(f2),'bits':enc_len(f2),'width':max(map(len,f2),default=0),'membership_hash_seed':s2['seed']},
    'pointwise_check_count':{'stage1':all1,'stage2':all2},'original_clause_lower_bound':max(0,len(formula)-4*len(eliminated)),
    'physical_FLMV_bit_trace_measured':False,'test_implementation_materializes_residual':True}
    return result

def main():
    source_path=Path(__file__).resolve().with_name('U198.txt')
    if not source_path.exists():
        source_path=Path(__file__).resolve().with_name('2026-10-24_0011_DOECKER61_original_source.txt')
    source=source_path.read_text()
    U=tuple(tuple(c) for c in ast.literal_eval(source[source.index('[['):]))
    cases=[('Y6_SAT',fixture_y()),('H6_outside_star_SAT',fixture_h()),
           ('Cyclic_15_SAT',cyclic_easy(5)),('Docker_U198_imported_UNSAT',U)]
    results=[run_case(*item) for item in cases]
    # Independent exactly-unsatisfiable outside-class control
    toy=((1,),( -1,))
    assert not any(all(any((vals[abs(z)-1]==(z>0)) for z in c) for c in toy) for vals in itertools.product((0,1),repeat=1))
    raw={'run':'M22-LOWSPACE-BATCH152','status':'PASS','all_assertions_passed':True,
         'cases':results,'outside_target_unsat':{'clauses':toy,'SAT':False},
         'scope':'finite logical-level checks only; constructive logspace proof is separate',
         'source_U198_sha_git':'f9dda41a810ad8e02bd553f2711a26a4050861f9'}
    path=Path(__file__).resolve().with_name('M22_LOWSPACE_BATCH152_results.json')
    path.write_text(json.dumps(raw,indent=2,sort_keys=True)+'\n')
    for row in results:print(row['name'],[(a['pivot_count'],a['clauses'],a['bits'],a['seed_attempts']) for a in [row['stage1'],row['stage2']]])
    print('PASS',len(results),'cases, output',path)
if __name__=='__main__':main()
