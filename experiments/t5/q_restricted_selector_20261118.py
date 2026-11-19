#!/usr/bin/env python3
"""T5 Q: fixed-head signature compilation, sound budgeted backdoor solver.
Standard library only. Run to write reproducible raw evidence to stdout.
"""
import hashlib
import itertools as it
import json
import random
import time
import tracemalloc
from collections import Counter
from pathlib import Path

WINS = ({1,3},{2,4},{0,3},{1,4},{0,2})
def r(a,b): return int(b in WINS[a])
def q(a,b,c): return r(a,b) != r(a,c)
def p(a,b,c): return r(a,b) and r(a,c)

def signatures(colors, domain=range(5)):
    return {tuple(r(h,c) for h in colors) for c in domain}

def majority_obstruction(S, count=None):
    for a,b,c in it.product(sorted(S), repeat=3):
        if count is not None: count['majority_triples_tested']+=1
        z=tuple(int(x+y+w>=2) for x,y,w in zip(a,b,c))
        if z not in S: return [list(a),list(b),list(c),list(z)]
    return None

def twosat(n, clauses, count):
    """Literal (variable, desired truth value); iterative Kosaraju."""
    g=[[] for _ in range(2*n)]; rev=[[] for _ in range(2*n)]
    for C in clauses:
        if not C: return None
        a,b=C if len(C)==2 else (C[0],C[0])
        a=2*a[0]+a[1]; b=2*b[0]+b[1]
        for x,y in ((a^1,b),(b^1,a)):
            g[x].append(y); rev[y].append(x); count['implication_edges']+=1
    seen=set(); order=[]
    for root in range(2*n):
        if root in seen: continue
        seen.add(root); stack=[(root,0)]
        while stack:
            x,i=stack[-1]
            if i<len(g[x]):
                y=g[x][i]; stack[-1]=(x,i+1); count['scc_edge_visits']+=1
                if y not in seen: seen.add(y); stack.append((y,0))
            else: order.append(x); stack.pop()
    comp=[-1]*(2*n); idx=0
    for root in reversed(order):
        if comp[root]>=0: continue
        comp[root]=idx; stack=[root]
        while stack:
            x=stack.pop()
            for y in rev[x]:
                count['scc_edge_visits']+=1
                if comp[y]<0: comp[y]=idx; stack.append(y)
        idx+=1
    if any(comp[2*v]==comp[2*v+1] for v in range(n)): return None
    ans=[int(comp[2*v+1]>comp[2*v]) for v in range(n)]
    assert all(any(ans[v]==b for v,b in C) for C in clauses)
    return ans

def terminal(n, F, fixed, count):
    """All head colors fixed. Return SAT/UNSAT/UNKNOWN, full witness.
    UNKNOWN means a non-bijunctive follower relation was encountered.
    This is never promoted to UNSAT. All-color domains plus absolute pins.
    """
    inc=[set() for _ in range(n)]
    for h,u,v in F:
        count['terminal_source_clause_scans']+=1
        inc[u].add(fixed[h]); inc[v].add(fixed[h])
    ids={}; spaces={}; clauses=[]
    for v in range(n):
        colors=sorted(inc[v]); domain=[fixed[v]] if v in fixed else range(5)
        S=signatures(colors,domain); count['signature_color_tests']+=len(colors)*len(domain)
        if majority_obstruction(S,count): return 'UNKNOWN',None
        spaces[v]=(colors,S)
        for h in colors: ids[v,h]=len(ids)
        # All absent unary and binary projections give the exact 2-CNF
        # iff S is majority closed. Width is at most five, a fixed constant.
        for width in (1,2):
            for J in it.combinations(range(len(colors)),width):
                projection={tuple(s[j] for j in J) for s in S}
                for bits in it.product(range(2),repeat=width):
                    count['projection_tests']+=1
                    if bits not in projection:
                        clauses.append([(ids[v,colors[j]],1-b) for j,b in zip(J,bits)])
    for h,u,v in F:
        a=ids[u,fixed[h]]; b=ids[v,fixed[h]]
        clauses.extend([[(a,1),(b,1)],[(a,0),(b,0)]])
    count['twosat_calls']+=1; count['twosat_clauses']+=len(clauses)
    count['max_boolean_variables']=max(count['max_boolean_variables'],len(ids))
    bits=twosat(len(ids),clauses,count)
    if bits is None: return 'UNSAT',None
    witness=[]
    for v in range(n):
        colors,S=spaces[v]; wanted=tuple(bits[ids[v,h]] for h in colors)
        choices=[fixed[v]] if v in fixed else range(5)
        chosen=None
        for c in choices:
            count['witness_color_attempts']+=1
            if tuple(r(h,c) for h in colors)==wanted: chosen=c; break
        assert chosen is not None
        witness.append(chosen)
    for h,u,v in F:
        count['original_clause_verifications']+=1
        assert q(witness[h],witness[u],witness[v])
    assert all(witness[v]==c for v,c in fixed.items())
    return 'SAT',witness

def solve(n, F, pins=None, budget=7):
    """Strong syntactic backdoor: heads + nonheads under >=3 head names.
    Budget bounds the number of unpinned backdoor variables. No oracle advice.
    """
    pins={} if pins is None else dict(pins); count=Counter()
    assert all(len(set(C))==3 and all(0<=v<n for v in C) for C in F)
    assert all(0<=v<n and 0<=c<5 for v,c in pins.items())
    Hset={h for h,u,v in F}; H=[v for v in range(n) if v in Hset]; inc=[set() for _ in range(n)]
    for h,u,v in F:
        inc[u].add(h); inc[v].add(h); count['preprocess_clauses']+=1
    D=[v for v in range(n) if v not in Hset and len(inc[v])>=3]
    Dset=set(D); K=[v for v in range(n) if v in Hset or v in Dset]; free=[v for v in K if v not in pins]
    meta={'heads':H,'exception_followers':D,'free_backdoor':free}
    if len(free)>budget: return {'status':'UNKNOWN','witness':None,'counters':dict(count),**meta}
    for values in it.product(range(5),repeat=len(free)):
        fixed={**pins,**dict(zip(free,values))}; count['color_routes']+=1
        status,w=terminal(n,F,fixed,count)
        assert status!='UNKNOWN' # theorem: every residual follower has <=2 heads
        if status=='SAT': return {'status':status,'witness':w,'counters':dict(count),**meta}
    return {'status':'UNSAT','witness':None,'counters':dict(count),**meta}

def brute(n,F,pins=None,relation=q):
    pins=pins or {}; total=0; checks=0; first=None
    for a in it.product(range(5),repeat=n):
        if any(a[v]!=c for v,c in pins.items()): continue
        ok=True
        for h,u,v in F:
            checks+=1
            if not relation(a[h],a[u],a[v]): ok=False; break
        if ok:
            total+=1
            if first is None: first=list(a)
    return {'count':total,'first':first,'relation_checks':checks}

def run():
    out={'seed':202611180629,'relation':'A:BD B:CE C:AD D:BE E:AC; ties are non-wins',
         'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out['truth_table']={'Q':sum(q(*t) for t in it.product(range(5),repeat=3)),
                        'P':sum(p(*t) for t in it.product(range(5),repeat=3)),
                        'intersection':sum(q(*t) and p(*t) for t in it.product(range(5),repeat=3))}
    # New complete finite signature classification, not the old formula grid.
    classification=[]
    for width in range(6):
        for colors in it.combinations(range(5),width):
            S=signatures(colors); bad=majority_obstruction(S)
            assert (bad is None)==(width<=2)
            classification.append({'head_colors':colors,'signatures':sorted(S),'majority_obstruction':bad})
    out['signature_classification']=classification
    # Independently check 2-projection reconstruction on every majority-closed
    # signature table for each subset of head colors AND each nonempty domain.
    projection_audits=0
    for width in range(6):
        for colors in it.combinations(range(5),width):
            for mask in range(1,32):
                S=signatures(colors,[c for c in range(5) if mask>>c&1])
                if majority_obstruction(S): continue
                for bits in it.product(range(2),repeat=width):
                    local=all(tuple(bits[j] for j in J) in {tuple(s[j] for j in J) for s in S}
                              for w in (1,2) for J in it.combinations(range(width),w))
                    assert local==(bits in S)
                projection_audits+=1
    out['majority_closed_domain_projection_audits']=projection_audits
    core=[(0,1,2),(0,1,3),(1,0,2),(1,2,3),(2,0,3)]
    controls=[('odd_head_triangle',4,[(0,1,2),(0,2,3),(0,3,1)],{}),('five_core',4,core,{})]
    controls += [('five_core_delete_'+str(i+1),4,core[:i]+core[i+1:],{}) for i in range(5)]
    # Three distinct head colors; all three signatures of x are forced to 0.
    # Each pair is possible; their conjunction is impossible. Tail variables
    # a,b,c are pinned to a beaten color of the respective head.
    controls += [('three_signature_boundary',7,[(0,3,4),(1,3,5),(2,3,6)],{0:0,1:1,2:2,4:1,5:2,6:0})]
    raw=[]
    for name,n,F,pins in controls:
        oracle=brute(n,F,pins); got=solve(n,F,pins)
        assert (got['status']=='SAT')==(oracle['count']>0)
        raw.append({'name':name,'n':n,'clauses':F,'pins':pins,'Q_oracle':oracle,
                    'P_oracle':brute(n,F,pins,p),'solver':got})
    out['controls']=raw
    rng=random.Random(out['seed']); raw=[]
    for i in range(80):
        n=5 if i<60 else 6
        scopes=[(h,u,v) for h in range(n) for u,v in it.combinations([x for x in range(n) if x!=h],2)]
        F=rng.sample(scopes,rng.randrange(0,min(13,len(scopes))+1))
        pins={v:rng.randrange(5) for v in range(n) if rng.random()<.35}
        # Keep this targeted audit bounded; it is not another random grid.
        while n-len(pins)>3:
            v=rng.choice([v for v in range(n) if v not in pins]); pins[v]=rng.randrange(5)
        oracle=brute(n,F,pins); got=solve(n,F,pins)
        assert (got['status']=='SAT')==(oracle['count']>0)
        raw.append({'id':i,'n':n,'clauses':F,'pins':pins,'Q_oracle':oracle,
                    'P_oracle':brute(n,F,pins,p),'solver':got})
    out['targeted_random']=raw
    # Arbitrarily many heads, source pins; each follower occurs under two heads.
    F=[]; pins={h:h%5 for h in range(20)}
    for h in range(20):
        F.append((h,20+h,40+h))
        F.append(((h+1)%20,20+h,40+h))
    got=solve(60,F,pins,budget=0); assert got['status']=='SAT'
    out['many_pinned_heads']={'n':60,'clauses':F,'pins':pins,'solver':got}
    # Exact semantic terminal boundary at fixed heads, independent brute oracle.
    F=[(0,3,4),(1,3,5),(2,3,6)]; fixed={0:0,1:1,2:2,4:1,5:2,6:0}
    out['boundary_terminal']={'status':terminal(7,F,fixed,Counter())[0],
        'exact_backdoor_status':solve(7,F,fixed)['status'],
        'oracle':brute(7,F,fixed)}
    assert out['boundary_terminal']['status']=='UNKNOWN'
    assert out['boundary_terminal']['oracle']['count']==0
    # Private heads on K6: deliberately outside this small-backdoor promise.
    F=[(6+i,u,v) for i,(u,v) in enumerate(it.combinations(range(6),2))]
    out['K6_budget_control']={'n':21,'clauses':F,'solver':solve(21,F,budget=7)}
    assert out['K6_budget_control']['solver']['status']=='UNKNOWN'
    # Independent audits of SCC on all 2-variable 2-CNF clause subsets.
    Cs=[[(v,b)] for v in range(2) for b in range(2)]
    Cs += [[(0,a),(1,b)] for a,b in it.product(range(2),repeat=2)]
    for mask in range(1<<len(Cs)):
        C=[c for i,c in enumerate(Cs) if mask>>i&1]
        possible=any(all(any(a[v]==b for v,b in c) for c in C) for a in it.product(range(2),repeat=2))
        assert (twosat(2,C,Counter()) is not None)==possible
    out['SCC_exhaustive_clause_subsets']=256
    # Row/block wrapper with one genuinely shared five-valued variable 0.
    # Each block has three disjoint private names. Source clauses retained.
    wrapper=[]
    for case in range(6):
        scopes=[(h,u,v) for h in range(4) for u,v in it.combinations([x for x in range(4) if x!=h],2)]
        blocks=[rng.sample(scopes,rng.randrange(1,6)) for _ in range(2)]
        if case==0: blocks[1]=core
        calls=[]; witnesses=None; selected=[]
        for z in range(5):
            bad=None
            for j,B in enumerate(blocks):
                result=solve(4,B,{0:z}); calls.append({'row':z,'block':j,'phase':'scan',**result})
                if result['status']=='UNSAT': bad=j; selected.append([z,j]); break
                assert result['status']=='SAT'
            if bad is None:
                witnesses=[z]+[None]*6
                for j,B in enumerate(blocks):
                    result=solve(4,B,{0:z}); calls.append({'row':z,'block':j,'phase':'replay',**result})
                    for v in range(1,4): witnesses[3*j+v]=result['witness'][v]
                break
        full=[tuple(0 if v==0 else 3*j+v for v in C) for j,B in enumerate(blocks) for C in B]
        oracle=brute(7,full)
        assert (witnesses is not None)==(oracle['count']>0)
        if witnesses: assert all(q(*(witnesses[v] for v in C)) for C in full)
        wrapper.append({'case':case,'blocks':blocks,'global_clauses':full,'oracle':oracle,
                        'witness':witnesses,'rejected_rows':selected,'all_child_calls':calls})
    out['wrapper']=wrapper
    return out

if __name__=='__main__':
    start=time.perf_counter(); data=run(); elapsed=time.perf_counter()-start
    tracemalloc.start()
    measured=solve(4,[(0,1,2),(0,1,3),(1,0,2),(1,2,3),(2,0,3)])
    peak=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    data['measurement']={'wall_seconds_tests_before_serialization':elapsed,
        'python_tracemalloc_peak_bytes_one_core_solve':peak,
        'measured_solver':measured,
        'scope':'Peak is a separate complete five-clause-core solve, including preprocessing, routes, SCC, counters and output. Input literal exists before tracing. Excludes imports, earlier tests and JSON serialization. Not a machine-independent bit-space bound.'}
    print(json.dumps(data,indent=2,sort_keys=True))
