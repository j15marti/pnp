#!/usr/bin/env python3
"""Reproducible two-parameter EXACT-(2,2)-3CNF frontal audit.

This file relies on the reviewed prior connector231.py (bundled in ZIP; repository
version: research/agents/lspv-2/2026-10-29_1322_LSPV-2_CONNECTED_AND_CONNECTOR231_repro.py,
blob ddfea2285320d3143ac653986e708d562ecabde6). All SAT/UNSAT
labels are checked by explicit witnesses or exact finite bridge tables.
No general SAT time bound follows; CPU measures are Python-only.

Run e.g.:
 python 2026-10-29_1612_LSPV-2_PAIRED_REALIZABLE_FRONTIER233_repro.py --mode core
 python ... --mode bench --b 6 --q 4
"""
import argparse, collections, hashlib, itertools, json, math, os, sys, time, tracemalloc
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'deps'))
from connector231 import W1, G, join, local_profile, simple_models, validate, var_scope_rank, renamed


def gen_base(b,q):
    assert b>=6 and b%3==0 and q>=2
    ell=3*q
    y=lambda j:1+(j%b)
    p=lambda j,i:b+j*ell+1+(i%ell)
    clauses=[]
    for j in range(b):clauses.append((y(j),y(j+1),-p(j,0)))
    for h in range(b//3):clauses.append((-y(3*h),-y(3*h+1),-y(3*h+2)))
    for j in range(b):
        for i in range(ell):clauses.append((p(j,i),p(j,i+1),-p(j,i+2)))
        clauses.append((-y(j+2),-p(j,1),-p(j,2)))
        for h in range(1,q):clauses.append(tuple(-p(j,3*h+t) for t in range(3)))
    model={y(j):int(j%3!=2) for j in range(b)}
    for j in range(b):
        for i in range(ell):model[p(j,i)]=int(i%3!=2)
    assert len(clauses)==4*b*(3*q+1)//3
    return clauses,model


def truth(cs,model):
    return all(any(model[abs(l)]==int(l>0) for l in c) for c in cs)


def scope(cs):
    return tuple(tuple(sorted(map(abs,c))) for c in cs)


def boundary_point(b,q,s,joined):
    assert 0<=s<=q
    B=b*(1+s)+(45 if joined else 0)
    Q=q-s
    return dict(s=s,n=b*(3*q+1)+(45 if joined else 0),B=B,Q=Q,
                k=b,E_T=B+Q,E_S=B,first_equality=(Q==0))


def module_profile(q,ys,counter=None):
    """Exact cyclic private DP for one attached module. No assignment oracle."""
    ell=3*q
    # (first0,first1,prevprev,prev) with first two initialized
    st={(a,c,a,c) for a,c in itertools.product((0,1),repeat=2)}
    peak=len(st)
    for t in range(2,ell):
        ns=set()
        for f0,f1,older,old in st:
            for z in (0,1):
                if counter is not None:counter['module_candidates']+=1
                if not(older or old or not z):continue
                if t==2:
                    if not(ys[0] or ys[1] or not f0):continue
                    if not(not ys[2] or not f1 or not z):continue
                if t%3==2 and t>=5 and older and old and z:continue
                ns.add((f0,f1,old,z))
        st=ns;peak=max(peak,len(st))
        if not st:break
    if counter is not None:counter['max_module_states']=max(counter['max_module_states'],peak)
    for f0,f1,older,old in st:
        if (older or old or not f0) and (old or f0 or not f1):return True
    return False


def module_profile_brute(q,ys):
    ell=3*q
    for mask in range(1<<ell):
        p=lambda i:(mask>>(i%ell))&1
        if not(ys[0] or ys[1] or not p(0)):continue
        if not(not ys[2] or not p(1) or not p(2)):continue
        if any(not(p(i) or p(i+1) or not p(i+2)) for i in range(ell)):continue
        if any(p(3*h) and p(3*h+1) and p(3*h+2) for h in range(1,q)):continue
        return True
    return False


def decide_streamed_frontier(b,q):
    """Source H only, with independent 8-entry local profile computed on demand."""
    c=collections.Counter(module_candidates=0,boundary_candidates=0,
                          max_module_states=0,max_boundary_states=0,
                          local_profile_evaluations=0)
    # boundary cyclic DP.  Four bits, first2 plus last2.
    states={(a,d,a,d) for a,d in itertools.product((0,1),repeat=2)}
    c['max_boundary_states']=len(states)
    for t in range(2,b):
        R=tuple(module_profile(q,ys,c) for ys in itertools.product((0,1),repeat=3))
        c['local_profile_evaluations']+=8
        nxt=set()
        for y0,y1,older,old in states:
            for z in (0,1):
                c['boundary_candidates']+=1
                if not R[(older<<2)|(old<<1)|z]:continue
                if t%3==2 and older and old and z:continue
                nxt.add((y0,y1,old,z))
        states=nxt;c['max_boundary_states']=max(c['max_boundary_states'],len(states))
        if not states:break
    if states:
        r1=tuple(module_profile(q,ys,c) for ys in itertools.product((0,1),repeat=3))
        r2=tuple(module_profile(q,ys,c) for ys in itertools.product((0,1),repeat=3))
        c['local_profile_evaluations']+=16
        ok=any(r1[(older<<2)|(old<<1)|y0] and r2[(old<<2)|(y0<<1)|y1]
               for y0,y1,older,old in states)
    else:ok=False
    c['max_profile_bits']=8
    c['logical_work_bits_peak_upper']=8+4*c['max_module_states']+4*c['max_boundary_states']+4*math.ceil(math.log2(3*q+2))+4*math.ceil(math.log2(b+2))
    return ok,dict(c)


def local_clauses(q,ys):
    ell=3*q
    cs=[]
    # include fixed source bridge clauses; y values evaluated now
    if not (ys[0] or ys[1]):cs.append((-1,))
    if ys[2]:cs.append((-2,-3))
    for i in range(ell):cs.append((i+1,(i+1)%ell+1,-((i+2)%ell+1)))
    for h in range(1,q):cs.append((-3*h-1,-3*h-2,-3*h-3))
    return cs


def two_sat_remainder(cs,assigned,numvars,ct):
    """Exact implication-SCC solver after assignment. Inputs must reduce to width<=2."""
    small=[]
    for clause in cs:
        ct['clause_scans']+=1
        live=[];satisfied=False
        for lit in clause:
            ct['literal_reads']+=1
            v=abs(lit)
            if v in assigned:
                if assigned[v]==int(lit>0):satisfied=True;break
            else:live.append(lit)
        if satisfied:continue
        if not live:return False
        if len(live)>2:raise AssertionError('not a valid syntactic hitting set')
        small.append(live)
    g=[[] for _ in range(2*numvars)];rev=[[] for _ in range(2*numvars)]
    def node(l):return 2*(abs(l)-1)+int(l>0)
    def edge(u,v):g[u].append(v);rev[v].append(u);ct['implication_edges']+=1
    for clause in small:
        if len(clause)==1:edge(node(-clause[0]),node(clause[0]))
        else:
            a,z=clause;edge(node(-a),node(z));edge(node(-z),node(a))
    seen=[False]*(2*numvars);order=[]
    for v in range(2*numvars):
        if seen[v]:continue
        seen[v]=True;stack=[(v,0)]
        while stack:
            u,i=stack[-1];ct['scc_work']+=1
            if i<len(g[u]):
                z=g[u][i];stack[-1]=(u,i+1)
                if not seen[z]:seen[z]=True;stack.append((z,0))
            else:order.append(u);stack.pop()
    comp=[-1]*(2*numvars);num=0
    for v in reversed(order):
        if comp[v]>=0:continue
        comp[v]=num;st=[v]
        while st:
            u=st.pop();ct['scc_work']+=1
            for z in rev[u]:
                if comp[z]<0:comp[z]=num;st.append(z)
        num+=1
    return all(comp[2*v]!=comp[2*v+1] for v in range(numvars))


def boundary_with_cached_profiles(profiles,b):
    """Exact cycle join for 8-entry module Boolean profiles and disjoint Q_Y."""
    states={(a,d,a,d) for a,d in itertools.product((0,1),repeat=2)}
    transitions=0;peak=len(states)
    for t in range(2,b):
        R=profiles[t-2];nxt=set()
        for y0,y1,older,old in states:
            for z in (0,1):
                transitions+=1
                if not R[(older<<2)|(old<<1)|z]:continue
                if t%3==2 and older and old and z:continue
                nxt.add((y0,y1,old,z))
        states=nxt;peak=max(peak,len(states))
        if not states:break
    result=any(profiles[b-2][(older<<2)|(old<<1)|y0] and
               profiles[b-1][(old<<2)|(y0<<1)|y1]
               for y0,y1,older,old in states)
    return result,{'cached_boundary_transitions':transitions,
                   'cached_boundary_state_peak':peak,
                   'cached_profile_bits':8*b}


def hitset_profile(q,ys,reverse=False):
    cs=local_clauses(q,ys);ct=collections.Counter()
    it=range((1<<q)-1,-1,-1) if reverse else range(1<<q)
    for mask in it:
        assigned={3*h+1:(mask>>h)&1 for h in range(q)}
        ct['attempts']+=1
        if two_sat_remainder(cs,assigned,3*q,ct):return True,dict(ct)
        ct['failed_attempts']+=1
    return False,dict(ct)


def rank_binary(rows):
    piv={}
    for x in rows:
        while x:
            u=x.bit_length()-1
            if u not in piv:piv[u]=x;break
            x^=piv[u]
    return len(piv)


def algebra_control(b,contradiction=False):
    """Separate affine-only control, explicitly NOT a strict22 root instance."""
    rows=[];n=b
    for i in range(b):rows.append((1<<i)^(1<<((i+1)%b)))
    rhs=[0]*b
    if contradiction:rhs[-1]=1
    r=rank_binary(rows)
    aug=rank_binary([row|(z<<n) for row,z in zip(rows,rhs)])
    return dict(parity_cycle_constraints=b,affine_rank=r,
                linear_dependency_excess=b-r,consistent=(aug==r),
                satisfied_by_zero=not contradiction,
                domain='affine-only diagnostic, not exact22 root')


def canonical_bits(n,m):
    return (4*m+2)*math.ceil(math.log2(64*(n+m+1)))


def exhaustive_hitting_min(q,s):
    """Exhaustive for small q only; theorem for all q uses disjoint clauses."""
    ell=3*q; moved={3*h for h in range(s)}
    R={i for i in range(ell) if i not in moved}
    private_clauses=[]
    # Each private cycle touches Y when it contains moved p.
    for i in range(ell):
        z={i,(i+1)%ell,(i+2)%ell}
        if not (z&moved):private_clauses.append(z)
    for h in range(1,q):
        z={3*h,3*h+1,3*h+2}
        if not(z&moved):private_clauses.append(z)
    for sz in range(q+1):
        for tup in itertools.combinations(sorted(R),sz):
            chosen=set(tup)
            if all(z&chosen for z in private_clauses):return sz
    return None


def inspect_pair(b,q,full_bridge=True):
    source,model=gen_base(b,q)
    n,m=validate(source)
    assert truth(source,model)
    assert (n,m)==(b*(3*q+1),4*b*(3*q+1)//3)
    work={'b':b,'q':q,'base_n':n,'base_m':m,
          'base_incidence_rank':var_scope_rank(source),
          'base_dependency_excess':m-var_scope_rank(source)}
    if full_bridge:
        g_model=next(simple_models(G))
        gg_model={j:int((g_model>>(j-1))&1) for j in range(1,16)}
        sat,witness,_=join(source,G,model,gg_model,witness=local_profile()[1])
        unsat,_,_=join(source,W1)
        assert validate(sat)==validate(unsat)
        assert scope(sat)==scope(unsat)
        assert truth(sat,witness)
        diffs=sum(l1!=l2 for C,D in zip(sat,unsat) for l1,l2 in zip(C,D))
        assert diffs==2, diffs
        work.update({'pair_n':len(witness),'pair_m':len(sat),'pair_unsigned_scope_match':True,
                     'pair_signed_literal_differences':diffs,'sat_witness_verified':True,
                     'unsat_certificate':'W1 exhaustive 2^15; exact connector231 gate truth table',
                     'pair_GF2_scope_rank':var_scope_rank(sat),
                     'pair_GF2_signed_positive_rank':var_scope_rank(sat,'positive'),
                     'pair_GF2_signed_negative_rank':var_scope_rank(sat,'negative'),
                     'pair_N':canonical_bits(len(witness),len(sat))})
    work['frontier']=[boundary_point(b,q,s,full_bridge) for s in range(q+1)]
    return work


def authenticate_pair(cs):
    """Uniform promise recognizer, no given (b,q) or SAT/UNSAT label.

    It generates and compares both templates for each feasible integer factor
    pair, counting failed candidates. On an unknown formula returns UNKNOWN;
    a total general SAT decider could fall back to exhaustive assignments.
    """
    n=max(abs(l) for C in cs for l in C)
    m=len(cs);stats=collections.Counter(actual_clauses_read=m,
                                       actual_literal_fields_read=3*m)
    if n<=45 or m!=4*n//3 or (4*n)%3:return 'UNKNOWN',dict(stats)
    n0=n-45
    for b in range(6,n0+1,3):
        stats['integer_factor_candidates']+=1
        if n0%b:continue
        ell=n0//b
        if (ell-1)%3:continue
        q=(ell-1)//3
        if q<2:continue
        base,_=gen_base(b,q)
        for label,K in (('SAT',G),('UNSAT',W1)):
            expected,_,_=join(base,K)
            stats['source_clauses_generated']+=len(base)
            stats['candidate_clauses_generated']+=len(expected)
            matched=True
            for left,right in zip(cs,expected):
                stats['candidate_clauses_compared']+=1
                stats['candidate_literal_fields_compared']+=3
                if left!=right:matched=False;break
            if matched and len(cs)==len(expected):
                stats['inferred_b']=b;stats['inferred_q']=q
                return label,dict(stats)
            stats['failed_template_candidates']+=1
    return 'UNKNOWN',dict(stats)


def run_pairbench(b,q):
    result=[]
    for true_label,K in (('SAT',G),('UNSAT',W1)):
        tracemalloc.start();start=time.perf_counter()
        base,_=gen_base(b,q)
        source,_,_=join(base,K)
        validate(source)
        label,stats=authenticate_pair(source)
        elapsed=time.perf_counter()-start
        _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
        assert label==true_label,(label,true_label)
        result.append({'source_label':true_label,'reported_label':label,
                       'b':b,'q':q,'pair_n':len(base[0])*0 + b*(3*q+1)+45,
                       'pair_m':len(source),'source_bits_N':canonical_bits(b*(3*q+1)+45,len(source)),
                       'python_elapsed_sec':round(elapsed,5),
                       'python_tracemalloc_peak_bytes':peak,'charged_counts':stats})
    return {'pair_recognition':result,'caveat':'Promised canonical syntax; fallback on outside inputs not timed. Includes template discovery and failed candidates.'}


def run_core():
    start=time.perf_counter();st=[]
    for b,q in [(6,2),(6,3),(9,2),(9,3),(12,2),(12,4),(21,18),(30,13)]:
        st.append(inspect_pair(b,q,full_bridge=(q<=4 or b>=21)))
    table,_,base=local_profile()
    assert base['source_W1_models']==0 and base['source_G_models']==272
    checks=0
    for q in (2,3,4):
        for y in itertools.product((0,1),repeat=3):
            assert module_profile(q,y)==module_profile_brute(q,y)==True
            checks+=1
    hits=[]
    for q in (2,3,4):
        for s in range(q+1):
            got=exhaustive_hitting_min(q,s)
            assert got==q-s,(q,s,got)
            hits.append({'q':q,'s':s,'exact_min':got})
    # Hostile renaming, clause-order, and literal-order controls. Such inputs
    # preserve labels but leave the canonical recognizer's promise class.
    h,model=gen_base(6,2)
    permuted_controls=[]
    for label,K in (('SAT',G),('UNSAT',W1)):
        root,_,_=join(h,K)
        permuted,mp=renamed(root,240101 if label=='SAT' else 240102)
        got,metrics=authenticate_pair(permuted)
        assert got=='UNKNOWN' and validate(permuted)==validate(root)
        assert scope(permuted)!=scope(root)
        permuted_controls.append({'label_preserved_by_bijection':label,
                                   'canonical_recognizer_result':got,
                                   'n':max(abs(l) for c in permuted for l in c),
                                   'renaming_seed':240101 if label=='SAT' else 240102})
    discrete=[];n0=1200
    for b in range(6,n0+1,3):
        if n0%b:continue
        ell=n0//b
        if (ell-1)%3:continue
        q=(ell-1)//3
        if q<2:continue
        discrete.append({'b':b,'q':q,'E_T':b+q,'E_S':b})
    assert min(discrete,key=lambda z:z['E_T'])=={'b':30,'q':13,'E_T':43,'E_S':30}
    return {'title':'PAIRED-REALIZABLE-FRONTIER233','builds':st,
            'bridge_control':base,'small_profile_bruteforce_checks':checks,
            'minimum_hitting_exhaustive':hits,'renamed_controls':permuted_controls,
            'n0_1200_discrete_candidates':discrete,
            'continuous_min_n0_1200':2*math.sqrt(1200/3)-1/3,
            'separate_affine_diagnostics':[algebra_control(12,False),algebra_control(12,True)],
            'elapsed_sec':time.perf_counter()-start}


def run_bench(b,q):
    results=[]
    for mode in ('streamed_frontier','hitset_zero_first','hitset_reverse'):
        tracemalloc.start();t0=time.perf_counter()
        cs,model=gen_base(b,q)
        n,m=validate(cs)
        if mode=='streamed_frontier':ans,cnt=decide_streamed_frontier(b,q)
        else:
            cnt=collections.Counter();profiles=[]
            # Compute each Boolean local profile, then do the exact boundary
            # compatibility join. This works even when some profiles are empty.
            for j in range(b):
                R=[]
                for bits in itertools.product((0,1),repeat=3):
                    ok,detail=hitset_profile(q,bits,reverse=(mode=='hitset_reverse'))
                    R.append(ok)
                    cnt['local_profiles']+=1
                    for k,v in detail.items():cnt[k]+=v
                profiles.append(R)
            ans,bc=boundary_with_cached_profiles(profiles,b)
            for k,v in bc.items():cnt[k]+=v
        elapsed=time.perf_counter()-t0
        current,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
        assert ans and truth(cs,model)
        results.append({'mode':mode,'b':b,'q':q,'n':n,'m':m,
                        'canonical_N_bits':canonical_bits(n,m),
                        'result':ans,'source_clauses_checked':m,
                        'time_seconds':round(elapsed,5),'tracemalloc_peak_bytes':peak,
                        'counters':dict(cnt)})
    return {'benchmark':results,'caveat':'CPython tracemalloc and instrumented counters; not native TM/RAM step or space complexity'}

if __name__=='__main__':
    pa=argparse.ArgumentParser();pa.add_argument('--mode',choices=['core','bench','pairbench'],default='core')
    pa.add_argument('--b',type=int,default=6);pa.add_argument('--q',type=int,default=3)
    args=pa.parse_args()
    out=run_core() if args.mode=='core' else (run_bench(args.b,args.q) if args.mode=='bench' else run_pairbench(args.b,args.q))
    print(json.dumps(out,sort_keys=True,indent=2))