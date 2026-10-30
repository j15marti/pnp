#!/usr/bin/env python3
"""LSPV-2 THIRD-ORDER-CLUSTER245: exact original-clause three-flip N0..N3 spectrum.

Standalone Python 3.10+ standard-library reproducer, seed=202610300212.
PROVED/EXACT restricted algorithm for proper source 3-CNF with max occurrence
D fixed. No SAT-equity or value scores. Never treats source signed occurrences
as independent variables. External brute force labels supplied only to checker.

Usage: python 2026-10-30_0212_LSPV-2_THIRD_ORDER_CLUSTER245.py [output.json]
"""
from __future__ import annotations
import collections, itertools, json, math, os, random, sys, time, tracemalloc
from dataclasses import dataclass

SEED = 202610300212
W1 = '-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
S15= '-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14'
MUT15='1 3 14;2 -8 -9;-10 -13 -14;3 -7 -13;4 9 11;-5 -8 14;4 8 11;-1 7 13;-1 7 -10;-5 6 15;-2 6 -12;-4 9 10;2 5 12;-3 -6 -15;-6 -7 -11;-2 -9 -11;-4 8 10;-3 12 15;5 -12 -15;1 13 -14'

def parse(s):return tuple(tuple(int(v) for v in c.split()) for c in s.split(';'))
def plateau(r):
    out=[]
    def v(j,i):return 6*(j%r)+i
    for j in range(r):
        out.extend([
            (v(j-1,1),v(j,3),v(j,5)),(v(j,1),-v(j,3),v(j,6)),
            (-v(j,1),v(j,4),v(j,5)),(-v(j,1),-v(j,4),v(j,6)),
            (v(j,2),v(j,3),-v(j,5)),(v(j,2),-v(j,3),-v(j,6)),
            (-v(j,2),v(j,4),-v(j,5)),(-v(j,2),-v(j,4),-v(j,6))])
    return tuple(out)
def paired_k4():
    z=((1,2,3),(-1,4,5),(2,4,6),(3,5,6))
    return z+tuple(tuple(-x for x in c) for c in z)
def parity3(even=True):
    cs=[]
    for bs in itertools.product((0,1),repeat=3):
        if sum(bs)%2==int(even):continue
        cs.append(tuple(-(i+1) if bs[i] else i+1 for i in range(3)))
    return tuple(cs)
def litval(l,a):return a[abs(l)]==int(l>0)
def truecounts(F,a):return tuple(sum(litval(l,a) for l in c) for c in F)
def Ncounts(F,a):
    c=collections.Counter(truecounts(F,a));return tuple(c[i] for i in range(4))
def model(F,a):return all(any(litval(l,a) for l in c) for c in F)
def allvars(F):return tuple(sorted({abs(l) for c in F for l in c}))
def exact22(F):
    v=allvars(F);t=collections.Counter(l for c in F for l in c)
    return v==tuple(range(1,len(v)+1)) and all(len(c)==3 and len(set(map(abs,c)))==3 for c in F) and all(t[i]==2 and t[-i]==2 for i in v)
def connected(F):
    vs=allvars(F);g={i:set() for i in vs}
    for c in F:
        for i,j in itertools.combinations(map(abs,c),2):g[i].add(j);g[j].add(i)
    seen={vs[0]};q=[vs[0]]
    for i in q:
        for j in sorted(g[i]-seen):seen.add(j);q.append(j)
    return len(seen)==len(vs)
def add(*vv):return tuple(map(sum,zip(*vv)))
def e(k):return tuple(int(k==i) for i in range(4))
def mul(v,n):return tuple(n*x for x in v)

# User's mandatory original-clause source-level audit.
def extreme_records(F):
    rows=[]
    for j,c in enumerate(F,1):
        o=[]
        for l in c:
            S=int(l>0);U=1-S
            o.append({'x_i_j':f'x_{{{abs(l)},{j}}}', 'signed_literal':l,
                'S_local_literal_true':S, 'invert_S_gives_U':U,
                'U_local_literal_false':U, 'invert_U_gives_S':S})
        rows.append({'original_C_j':j,'literals':list(c),'source_occurrences':o,
                     'S_j_all_literals_true':{str(abs(l)):int(l>0) for l in c},
                     'invert_S_j_is_U_j':{str(abs(l)):int(l<0) for l in c},
                     'U_j_all_literals_false':{str(abs(l)):int(l<0) for l in c},
                     'invert_U_j_is_S_j':{str(abs(l)):int(l>0) for l in c}})
    return rows

def pair_extremes(F):
    rows=[];tests=0
    for j,k in itertools.combinations(range(len(F)),2):
        a={abs(l):int(l>0) for l in F[j]};b={abs(l):int(l>0) for l in F[k]}
        shared=a.keys()&b.keys()
        same=sorted(i for i in shared if a[i]==b[i]);opp=sorted(i for i in shared if a[i]!=b[i])
        pred={'SS':not bool(opp),'SU':not bool(same),'US':not bool(same),'UU':not bool(opp)}
        scope=sorted(a.keys()|b.keys());observed={q:False for q in pred}
        for z in itertools.product((0,1),repeat=len(scope)):
            ass=dict(zip(scope,z));tj=sum(litval(l,ass) for l in F[j]);tk=sum(litval(l,ass) for l in F[k]);tests+=1
            q=('S' if tj==len(F[j]) else 'U' if tj==0 else 'M')+('S' if tk==len(F[k]) else 'U' if tk==0 else 'M')
            if q in observed:observed[q]=True
        assert observed==pred,(j,k,pred,observed)
        rows.append({'source_clause_j':j+1,'source_clause_k':k+1,
            'same_polarity_shared':same,'opposite_polarity_shared':opp,
            'SS_SU_US_UU':pred, 'at_least_one_middle_for_every_assignment':not any(pred.values())})
    return rows,tests


def source_three_clause_extreme_modes(F,limit=7):
    """Original triple-clause local S/U target checks, not global SAT tests."""
    records=[];enumerations=0
    for triple in itertools.combinations(range(len(F)),3):
        sc=[set(map(abs,F[j])) for j in triple]
        if sum(bool(sc[i]&sc[j]) for i,j in itertools.combinations(range(3),2))<2:continue
        scope=sorted(set.union(*sc));observed={}
        for modes in itertools.product('SU',repeat=3):
            assignment={};pred=True
            for j,mode in zip(triple,modes):
                for z in F[j]:
                    required=int(z>0) if mode=='S' else int(z<0)
                    if abs(z) in assignment and assignment[abs(z)]!=required:pred=False
                    assignment[abs(z)]=required
            actual=False
            for bs in itertools.product((0,1),repeat=len(scope)):
                a=dict(zip(scope,bs));enumerations+=1
                counts=[sum(litval(l,a) for l in F[j]) for j in triple]
                if all(t==(len(F[j]) if mode=='S' else 0) for t,j,mode in zip(counts,triple,modes)):
                    actual=True;break
            assert pred==actual
            observed[''.join(modes)]=pred
        records.append({'three_original_clause_indices':[j+1 for j in triple],
                        'source_S_U_modes':observed,
                        'some_coherent_all_extreme_mode':any(observed.values())})
        if len(records)>=limit:break
    return records,enumerations

def endpoint_trail(F,steps):
    trails={}
    for baseval in (0,1):
        a={i:baseval for i in allvars(F)};T=[]
        for tag,flip in [('endpoint',None)]+[(f'flip_{i}',i) for i in steps]+[('global_complement',-1)]:
            if flip==-1:a={i:1-v for i,v in a.items()}
            elif flip is not None:a[flip]^=1
            counts=truecounts(F,a);n=tuple(counts.count(k) for k in range(4))
            T.append({'event':tag,'assignment':[a[i] for i in sorted(a)],
                      'original_clause_true_literal_counts':list(counts),
                      'N0_N1_N2_N3':list(n),'source_formula_SAT':n[0]==0})
        trails[f'{baseval}^n']=T
    return trails

def source_resolution_cube(F):
    for j,k in itertools.combinations(range(len(F)),2):
        for l in F[j]:
            if -l not in F[k]:continue
            w=[x for x in F[j] if x!=l]+[x for x in F[k] if x!=-l]
            if any(-x in w for x in w):continue
            res=tuple(sorted(set(w),key=lambda x:(abs(x),x<0)))
            cube={abs(z):int(z<0) for z in res}
            assert not any(litval(z,cube) for z in res)
            assert [z for z in F[j] if abs(z) not in cube]==[l]
            assert [z for z in F[k] if abs(z) not in cube]==[-l]
            return {'source_clause_parents':[j+1,k+1],'pivot':abs(l),
                    'non_tautological_resolvent':list(res),
                    'forbidden_source_variable_cube':{str(v):b for v,b in sorted(cube.items())},
                    'source_certificate':'On the forbidden cube the two original parents become opposing units.'}
    return None

# Bounded-locality 3-flip algorithm: no independent O(n^3) flip-state enumeration.
def three_flip_spectrum(F,base,verify_small=False):
    n=len(base);assert set(base)==set(range(1,n+1));assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in F)
    work=collections.Counter();N=[0]*4;d={i:[0]*4 for i in base}
    h=collections.defaultdict(lambda:[0]*4);g=collections.defaultdict(lambda:[0]*4)
    neigh={i:set() for i in base};inc=collections.defaultdict(list)
    for clauseid,c in enumerate(F,1):
        bs=[int(litval(z,base)) for z in c];t=sum(bs);N[t]+=1
        work['original_literal_reads']+=3;work['source_clause_count_updates']+=1
        ds=[1-2*x for x in bs];sing=[t+v for v in ds]
        for p,z in enumerate(c):
            i=abs(z);inc[i].append(clauseid)
            for r in range(4):d[i][r]+=(sing[p]==r)-(t==r)
            work['local_singleton_count_updates']+=4
        for p,q in itertools.combinations(range(3),2):
            i,j=sorted((abs(c[p]),abs(c[q])));neigh[i].add(j);neigh[j].add(i)
            v=t+ds[p]+ds[q]
            for r in range(4):h[(i,j)][r]+=(v==r)-(sing[p]==r)-(sing[q]==r)+(t==r)
            work['local_pair_count_updates']+=4
        ids=tuple(sorted(map(abs,c)))
        # Third finite difference of a single original clause's one-hot status.
        for r in range(4):
            triple=int(t+sum(ds)==r)
            pairs=sum(int(t+ds[p]+ds[q]==r) for p,q in itertools.combinations(range(3),2))
            single=sum(int(u==r) for u in sing)
            g[ids][r]+=triple-pairs+single-int(t==r)
        work['local_triple_count_updates']+=4
    assert sum(N)==len(F)
    D={i:tuple(v) for i,v in d.items()};H={k:tuple(v) for k,v in h.items()};G={k:tuple(v) for k,v in g.items()}
    sig=collections.defaultdict(list)
    for i,v in D.items():sig[v].append(i)
    keys=sorted(sig);freq={v:len(sig[v]) for v in keys};B=len(keys)
    work['signature_buckets']=n
    # Baseline for ALL unordered triples, as if no two of the flips co-occur in a clause.
    hist=collections.Counter();buckets=collections.Counter()
    for ai,v in enumerate(keys):
        for bi in range(ai,len(keys)):
            w=keys[bi]
            for ci in range(bi,len(keys)):
                u=keys[ci];word=(v,w,u)
                multiplicity=1
                for k,ct in collections.Counter(word).items():
                    multiplicity*=math.comb(freq[k],ct) if freq[k]>=ct else 0
                work['three_signature_multisets']+=1
                if multiplicity:
                    hist[add(N,v,w,u)]+=multiplicity
                    buckets[word]+=multiplicity
    assert sum(hist.values())==math.comb(n,3)
    # Every affected triple has either (a) one co-occurrence edge, or
    # (b) at least two such edges and hence is a connected 3-vertex set.
    multi=set()
    for center in range(1,n+1):
        for i,j in itertools.combinations(sorted(neigh[center]),2):
            multi.add(tuple(sorted((i,center,j))))
            work['connected_triple_candidate_inserts']+=1
    work['distinct_2plus_edge_triples']=len(multi)
    one_counts=collections.Counter();seen_one=0
    for (i,j),hvec in H.items():
        forbidden={i,j}|neigh[i]|neigh[j]
        fct=collections.Counter(D[v] for v in forbidden)
        for signature,count in freq.items():
            valid=count-fct.get(signature,0)
            work['edge_signature_corrections']+=1
            if valid<=0:continue
            before=add(N,D[i],D[j],signature);after=add(before,hvec)
            hist[before]-=valid;hist[after]+=valid
            one_counts[signature]+=valid;seen_one+=valid
    # A >=2-edge triple is not touched by any one-edge correction.
    for triple in sorted(multi):
        ij,ik,jk=itertools.combinations(triple,2)
        E=sum(pair in H for pair in (ij,ik,jk));assert E>=2
        pre=add(N,*(D[v] for v in triple));exact=pre
        for pair in (ij,ik,jk):
            if pair in H:exact=add(exact,H[pair])
        if triple in G:exact=add(exact,G[triple])
        hist[pre]-=1;hist[exact]+=1
        work['connected_triple_corrections']+=1
    result={k:v for k,v in hist.items() if v!=0};assert all(v>0 for v in result.values()),result
    assert sum(result.values())==math.comb(n,3)
    # Reconstruct a model within 3 flips on either endpoint without n^3
    # states: constant-size representative prefixes per signature bucket.
    witness=None;kind=None;maxdeg=max((len(x) for x in neigh.values()),default=0)
    representative_limit=3*(maxdeg+1)
    heads={d:xs[:representative_limit] for d,xs in sig.items()}
    def wanted(v):return v[0]==0 or v[3]==0
    def test_candidate(triple,vector):
        nonlocal witness,kind
        work['witness_source_clause_verifications']+=len(F)
        a=dict(base)
        for x in triple:a[x]^=1
        if vector[0]==0:result=a;kind='base'
        elif vector[3]==0:result={i:1-v for i,v in a.items()};kind='complement'
        else:return False
        assert model(F,result) and Ncounts(F,a)==vector
        witness={'flipped_original_variables':list(triple),'from_endpoint':kind,
                 'full_source_witness':[result[i] for i in range(1,n+1)],
                 'original_four_counts':list(vector)}
        return True
    if any(wanted(k) for k in result):
        for triple in sorted(multi):
            if witness:break
            vec=add(N,*(D[v] for v in triple))
            for p in itertools.combinations(triple,2):
                if p in H:vec=add(vec,H[p])
            if triple in G:vec=add(vec,G[triple])
            work['connected_witness_checks']+=1
            if wanted(vec):test_candidate(triple,vec)
        if not witness:
            for (i,j),hv in sorted(H.items()):
                if witness:break
                forbidden={i,j}|neigh[i]|neigh[j]
                for s,xs in heads.items():
                    vec=add(N,D[i],D[j],s,hv)
                    if not wanted(vec):continue
                    for k in xs:
                        work['one_edge_witness_checks']+=1
                        if k not in forbidden and test_candidate((i,j,k),vec):break
                    if witness:break
        if not witness:
            # Zero-edge classes are represented by bounded-size signature heads.
            # Replacement lemma: when a color class has >2 Delta+2 vertices,
            # any one vertex in a 3-independent set can be swapped to a head
            # vertex not adjacent to its other two vertices.
            for word,ct in buckets.items():
                if not wanted(add(N,*word)):continue
                heads3=[heads[d] for d in word]
                for triple in itertools.product(*heads3):
                    if len(set(triple))!=3:continue
                    work['independent_witness_checks']+=1
                    if all(v not in neigh[u] for u,v in itertools.combinations(triple,2)):
                        if test_candidate(triple,add(N,*word)):break
                if witness:break
        assert witness is not None,'Histogram says endpoint witness but reconstruction failed'
    else:assert witness is None
    out={'source_n':n,'source_m':len(F),'degree_bound':max(len(inc[i]) for i in inc),
         'interaction_max_degree':maxdeg,'base_N0_N1_N2_N3':N,
         'singleton_signature_count':B,'source_cooccurrence_edges':len(H),
         'source_triangles_in_clauses':len(G),'triples_with_one_interaction_edge':seen_one,
         'triples_with_2plus_interaction_edges':len(multi),
         'third_order_nonzero_clause_triples':sum(any(v) for v in G.values()),
         'three_flip_histogram':[{'N0_N1_N2_N3':list(k),'count':v} for k,v in sorted(result.items())],
         'three_flip_SAT_models_at_base':sum(v for k,v in result.items() if k[0]==0),
         'three_flip_SAT_models_at_complement':sum(v for k,v in result.items() if k[3]==0),
         'reconstructed_witness':witness, 'selected_operation_ledger':dict(work),
         'counted_selected_operations':sum(work.values())}
    if verify_small and n<=15:
        brute=collections.Counter()
        for triple in itertools.combinations(range(1,n+1),3):
            a=dict(base)
            for i in triple:a[i]^=1
            brute[Ncounts(F,a)]+=1
        assert dict(brute)==result,(n,brute,result)
        out['exhaustive_three_flip_assignments_checked']=math.comb(n,3)
    return out

# Source-preserving baseline DPLL. Same source and same input-status scan.
class Ledger:
    def __init__(self):self.events=0;self.states=0;self.clause_reads=0;self.literal_reads=0
    def read(self,c):self.events+=1+len(c);self.clause_reads+=1;self.literal_reads+=len(c)
    def stats(self):return {'selected_work':self.events,'DPLL_states':self.states,
                             'source_clause_reads':self.clause_reads,'source_literal_reads':self.literal_reads}
def up(F,known,L):
    a=dict(known)
    while True:
        changed=False
        for j,c in enumerate(F,1):
            L.read(c)
            if any(abs(l) in a and litval(l,a) for l in c):continue
            unassigned=[l for l in c if abs(l) not in a]
            if not unassigned:return None,{'falsified_original_clause':j,'pin':a}
            if len(unassigned)==1:
                l=unassigned[0];a[abs(l)]=int(l>0);L.events+=1;changed=True;break
        if not changed:return a,None

def solve(F,n,L):
    def recur(pin):
        L.states+=1;L.events+=1
        a,conf=up(F,pin,L)
        if conf:return False,{'conflict':conf}
        if len(a)==n:
            assert model(F,a)
            return True,{'witness':a}
        x=next(v for v in range(1,n+1) if v not in a)
        children=[]
        for bit in (0,1):
            sub=dict(a);sub[x]=bit
            ok,branch=recur(sub);children.append({'x':x,'value':bit,'subproof':branch})
            if ok:return True,branch
        return False,{'children':children}
    return recur({})
def profile(fn):
    tracemalloc.start();t=time.perf_counter();out=fn();seconds=time.perf_counter()-t;_,pk=tracemalloc.get_traced_memory();tracemalloc.stop()
    return out,{'wall_seconds':round(seconds,6),'peak_python_traced_bytes':pk}
def benchmark(F,use_triples):
    n=max(allvars(F));L=Ledger();L.events+=sum(len(c)+1 for c in F)
    if use_triples:
        for endpoint in (0,):
            f=three_flip_spectrum(F,{i:endpoint for i in range(1,n+1)})
            L.events+=f['counted_selected_operations']
            win=f['reconstructed_witness']
            if win:
                a={i+1:v for i,v in enumerate(win['full_source_witness'])};L.events+=sum(len(c)+1 for c in F)
                assert model(F,a)
                return {'sat':True,'witness':a,'used':'third_order_spectrum','stats':L.stats()}
    good,tree=solve(F,n,L)
    return {'sat':good,'witness':tree['witness'] if good else None,
            'used':'UP_DPLL' if not use_triples else 'third_order_fallback_UP_DPLL',
            'unsat_certificate':tree if not good else None, 'stats':L.stats()}


def benchmark_endpoint_first(F):
    """Uniform deterministic controller: endpoint scan -> 3-flip -> complete UP-DPLL.
    Endpoint scans include failed scans and original-clause verification.
    """
    n=max(allvars(F));L=Ledger();L.events+=sum(len(c)+1 for c in F)
    for bit in (0,1):
        a={i:bit for i in range(1,n+1)};good=True
        for c in F:
            L.read(c)
            if not any(litval(l,a) for l in c):good=False
        if good:
            for c in F:L.read(c)   # final original-source witness verification
            return {'sat':True,'witness':a,'used':f'endpoint_{bit}',
                    'unsat_certificate':None,'stats':L.stats()}
    f=three_flip_spectrum(F,{i:0 for i in range(1,n+1)})
    L.events+=f['counted_selected_operations']
    w=f['reconstructed_witness']
    if w:
        a={i+1:v for i,v in enumerate(w['full_source_witness'])}
        for c in F:L.read(c)
        assert model(F,a)
        return {'sat':True,'witness':a,'used':'endpoint_failed_then_three_flip',
                'unsat_certificate':None,'stats':L.stats()}
    good,tree=solve(F,n,L)
    return {'sat':good,'witness':tree['witness'] if good else None,
            'used':'endpoints_failed_three_flip_failed_UP_DPLL',
            'unsat_certificate':tree if not good else None,'stats':L.stats()}

def independent_oracle(F,cap=15):
    n=max(allvars(F))
    if n>cap:return None
    models=0
    for mask in range(1<<n):
        a={i:mask>>(i-1)&1 for i in range(1,n+1)}
        if model(F,a):models+=1
        back={i:1-a[i] for i in a}
        aa=Ncounts(F,a);bb=Ncounts(F,back)
        if all(len(c)==3 for c in F):assert aa==tuple(reversed(bb))
        elif all(len(c)==2 for c in F):assert aa[0]==bb[2] and aa[1]==bb[1] and aa[2]==bb[0] and aa[3]==bb[3]==0
    return {'full_assignments_tested':1<<n,'exact_model_count':models,'sat':models>0}

def run_case(name,F,do_solving=True):
    n=max(allvars(F));assert allvars(F)==tuple(range(1,n+1))
    for c in F:assert len(c)==3 and len(set(map(abs,c)))==3
    x22=exact22(F);base={i:0 for i in range(1,n+1)}
    spectral,prof=profile(lambda:three_flip_spectrum(F,base,verify_small=n<=15))
    ext=extreme_records(F);matrix,pair_tests=pair_extremes(F) if n<=24 else ([],0)
    trails=endpoint_trail(F,[i for i in (1,2,3,1) if i<=n])
    triple_modes,triple_tests=source_three_clause_extreme_modes(F)
    if n<=15:
        truth=independent_oracle(F)
        assert spectral['three_flip_SAT_models_at_base'] == sum(model(F,{i:(i in triple) for i in range(1,n+1)}) for triple in itertools.combinations(range(1,n+1),3))
    else:truth=None
    resolution=source_resolution_cube(F)
    outcome={'family':name,'proper_original_3cnf':True,'strict_signed_exact22':x22,
             'original_variable_graph_connected':connected(F),
             'n':n,'m':len(F),'local_S_U_targets_with_inversions':ext,
             'source_clause_SS_SU_US_UU_matrix':matrix,
             'extreme_pair_enumeration_tests':pair_tests,
             'source_triple_S_U_modes':triple_modes,'source_triple_extreme_enumeration_tests':triple_tests,
             'coherent_endpoint_and_flip_trails':trails,
             'one_source_parent_resolvent_and_forbidden_cube':resolution,
             'exact_global_truth_control_if_n_le_15':truth,
             'three_flip_spectrum':spectral,'three_flip_profile':prof}
    if do_solving:
        base_sol,p0=profile(lambda:benchmark(F,False));plus_sol,p1=profile(lambda:benchmark(F,True))
        adaptive,p2=profile(lambda:benchmark_endpoint_first(F))
        assert base_sol['sat']==plus_sol['sat']==adaptive['sat']
        if truth is not None:assert base_sol['sat']==truth['sat']
        outcome['solver_comparison']={'baseline':base_sol,'spectrum_fallback':plus_sol,
                                      'baseline_profile':p0,'spectrum_profile':p1,
                                      'endpoint_first':adaptive,'endpoint_first_profile':p2}
    return outcome

def main():
    random.seed(SEED);start=time.perf_counter();path=sys.argv[1] if len(sys.argv)>1 else 'THIRD_ORDER_CLUSTER245_raw.json'
    controls=[('strict22_W1_UNSAT',parse(W1)),('strict22_S15_SAT',parse(S15)),
              ('strict22_MUT15_SAT',parse(MUT15)),('strict22_K4_paired_SAT',paired_k4()),
              ('strict22_plateau_H1_SAT',plateau(1)),('strict22_plateau_H2_SAT',plateau(2)),
              ('strict22_plateau_H4_SAT',plateau(4)),
              ('affine_XOR3_even_SAT',parity3(True)),
              ('affine_XOR3_odd_SAT',parity3(False)),
              ('affine_XOR3_CONTRADICTORY_UNSAT',parity3(True)+parity3(False)),
              ('HORNSAT_3CNF',((-1,-2,3),(-1,-3,2),(-2,-3,1),(-1,-2,-3))),
              ('mixed_sign_3CNF',((1,2,3),(-1,-2,-3),(1,-2,3)))]
    ren=list(range(1,16));random.shuffle(ren)
    a=parse(W1);renamed=tuple(tuple((1 if l>0 else -1)*ren[abs(l)-1] for l in c) for c in a)
    controls.append(('strict22_W1_renamed_UNSAT',renamed))
    negated=tuple(tuple(-l if abs(l) in {1,3} else l for l in c) for c in a)
    controls.append(('strict22_W1_polarity_renamed_UNSAT',negated))
    rng=random.Random(SEED+1)
    dense=[]
    for j in range(25):
        vs=rng.sample(range(1,9),3)
        dense.append(tuple(v if rng.randrange(2) else -v for v in vs))
    controls.append(('dense_random_original_3CNF',tuple(dense)))
    result={'run_id':'THIRD_ORDER_CLUSTER245','seed':SEED,'algorithm_model':'indexed word RAM, logarithmic-word counts, original clause lists, input resident','cases':[], 'width2_controls':[]}
    for name,F in controls:
        rec=run_case(name,F,True);result['cases'].append(rec)
        print(name,rec['n'],rec['m'],rec['three_flip_spectrum']['three_flip_SAT_models_at_base'],
              rec.get('solver_comparison',{}).get('baseline',{}).get('stats',{}).get('DPLL_states'))
    for name,F in [('2SAT_unsat_four_clauses',((1,2),(-1,2),(1,-2),(-1,-2))),
                   ('2SAT_sat_three_clauses',((1,2),(-1,2),(1,-2)))]:
        n=max(allvars(F));assert all(len(c)==2 for c in F)
        matrix,check=pair_extremes(F);L=Ledger();L.events+=sum(len(c)+1 for c in F)
        good,tree=solve(F,n,L);oracle=independent_oracle(F)
        assert good==oracle['sat']
        result['width2_controls'].append({'family':name,'n':n,'m':len(F),
            'status':'KNOWN THEOREM 2SAT, not width3 spectrum',
            'source_extremes':extreme_records(F),'SS_SU_US_UU':matrix,
            'pair_enumeration_tests':check,'original_endpoint_flips':endpoint_trail(F,[1,2]),
            'full_assignment_truth':oracle,'SAT':good,
            'SAT_witness':tree['witness'] if good else None,
            'UNSAT_refutation_tree':tree if not good else None,'DPLL':L.stats()})
    result['elapsed_seconds']=time.perf_counter()-start
    with open(path,'w') as f:json.dump(result,f,indent=2)
    print('COMPLETE',path,os.stat(path).st_size)
if __name__=='__main__':main()