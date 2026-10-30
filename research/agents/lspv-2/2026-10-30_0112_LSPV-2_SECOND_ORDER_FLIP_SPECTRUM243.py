#!/usr/bin/env python3
"""Source-indexed clause-extreme controls and exact second-order Hamming spectra.

No SAT-equity/valuation scores. All returned counts refer to coherent ORIGINAL variable
assignments. O(n + sum_j |C_j|^2) second-order counting in indexed word RAM;
for bounded width=3 this is O(n+m), with no expansion of n-choose-2 pairs.

Usage: python 2026-10-30_0112_LSPV-2_SECOND_ORDER_FLIP_SPECTRUM243.py [output.json]
Python 3.11+ standard library. Seed 202610300112. No stochastic solver decisions.
"""
from __future__ import annotations
import collections, hashlib, itertools, json, math, random, sys, time, tracemalloc
from dataclasses import dataclass
SEED=202610300112
W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
S15='-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14'
MUT15='1 3 14;2 -8 -9;-10 -13 -14;3 -7 -13;4 9 11;-5 -8 14;4 8 11;-1 7 13;-1 7 -10;-5 6 15;-2 6 -12;-4 9 10;2 5 12;-3 -6 -15;-6 -7 -11;-2 -9 -11;-4 8 10;-3 12 15;5 -12 -15;1 13 -14'

def parse(s):return tuple(tuple(int(x) for x in c.split()) for c in s.split(';'))

def plateau(r):
    out=[]
    def v(j,i): return 6*(j%r)+i
    for j in range(r):
        out.extend([
            (v(j-1,1), v(j,3), v(j,5)),
            (v(j,1), -v(j,3),v(j,6)),
            (-v(j,1),v(j,4),v(j,5)),
            (-v(j,1),-v(j,4),v(j,6)),
            (v(j,2),v(j,3),-v(j,5)),
            (v(j,2),-v(j,3),-v(j,6)),
            (-v(j,2),v(j,4),-v(j,5)),
            (-v(j,2),-v(j,4),-v(j,6))])
    return tuple(out)

def paired_k4():
    c=((1,2,3),(-1,4,5),(2,4,6),(3,5,6))
    return tuple(c)+tuple(tuple(-x for x in d) for d in c)

def parity3(even=True):
    ans=[]
    for bits in itertools.product((0,1),repeat=3):
        if sum(bits)%2==int(even):continue
        ans.append(tuple(-(i+1) if bits[i] else i+1 for i in range(3)))
    return tuple(ans)

def litval(l,a):return a[abs(l)]==int(l>0)

def truth(F,a):return [tuple(int(litval(l,a)) for l in c) for c in F]

def histogram(F,a):
    t=list(map(sum,truth(F,a)));return [t.count(i) for i in range(4)]

def ismodel(F,a):return all(any(litval(l,a) for l in c) for c in F)

def variables(F):return tuple(sorted({abs(l) for c in F for l in c}))

def exact22(F):
    v=variables(F);c=collections.Counter(l for cl in F for l in cl)
    return (v==tuple(range(1,len(v)+1)) and all(len(cl)==3 and len({abs(l) for l in cl})==3 for cl in F)
            and all(c[i]==2 and c[-i]==2 for i in v))

def connected(F):
    v=variables(F)
    if not v:return True
    adj={i:set() for i in v}
    for c in F:
        for x,y in itertools.combinations([abs(z) for z in c],2):adj[x].add(y);adj[y].add(x)
    reach={v[0]};q=[v[0]]
    for x in q:
        for y in sorted(adj[x]-reach):reach.add(y);q.append(y)
    return len(reach)==len(v)

def source_extremes(F):
    rows=[]
    for j,c in enumerate(F,1):
        occ=[]
        for l in c:
            u=int(l<0);s=1-u
            occ.append({'x_i_j':f'x_{{{abs(l)},{j}}}','source_clause':j,
                        'source_literal':l,'variable':abs(l),'polarity':'+' if l>0 else '-',
                        'S_local_target':s,'inverse_of_S_is_U':u,
                        'U_local_target':u,'inverse_of_U_is_S':s})
        rows.append({'j':j,'signed_original_clause':list(c),'occurrences':occ,
                     'S_j':{str(abs(l)):int(l>0) for l in c},
                     'inverted_S_j_is_U_j':{str(abs(l)):int(l<0) for l in c},
                     'U_j':{str(abs(l)):int(l<0) for l in c},
                     'inverted_U_j_is_S_j':{str(abs(l)):int(l>0) for l in c}})
    return rows

def pair_compat(F):
    records=[];checked=0
    for j,k in itertools.combinations(range(len(F)),2):
        a={abs(l):l>0 for l in F[j]};b={abs(l):l>0 for l in F[k]}
        shared=set(a)&set(b)
        same=sorted(x for x in shared if a[x]==b[x]);opp=sorted(x for x in shared if a[x]!=b[x])
        modes={'SS':not bool(opp),'SU':not bool(same),'US':not bool(same),'UU':not bool(opp)}
        allvars=sorted(set(a)|set(b));actual={q:False for q in modes}
        for bits in itertools.product((0,1),repeat=len(allvars)):
            z=dict(zip(allvars,bits)); tj=sum(litval(l,z) for l in F[j]);tk=sum(litval(l,z) for l in F[k]);checked+=1
            q=('S' if tj==len(F[j]) else 'U' if tj==0 else 'M')+('S' if tk==len(F[k]) else 'U' if tk==0 else 'M')
            if q in actual:actual[q]=True
        assert actual==modes,(j,k,actual,modes)
        records.append({'source_j':j+1,'source_k':k+1,'same_sign_shared':same,
                        'opposite_sign_shared':opp,'SS_SU_US_UU':modes,'all_extremes_impossible':not any(modes.values())})
    return records,checked

def fliptrail(F,base,steps):
    a=dict(base);out=[]
    def snap(name):
        tv=truth(F,a); h=[sum(t)==0 for t in tv]
        return {'action':name,'assignment':[a[i] for i in sorted(a)],
                'per_original_clause_literal_bits':[''.join(map(str,t)) for t in tv],
                'per_original_clause_true_counts':list(map(sum,tv)),
                'N0_N1_N2_N3':[sum(sum(t)==q for t in tv) for q in range(4)],'satisfies_all':not any(h)}
    out.append(snap('base'))
    for x in steps:
        a[x]^=1;out.append(snap('flip_original_variable_'+str(x)))
    return out

def independent_pair_check(F,lim=18):
    n=max(variables(F),default=0)
    if n>lim:return {'checked':0,'skipped':'n exceeds exact enumeration cap'}
    ops=0
    for j,k in itertools.combinations(range(len(F)),2):
        if abs(j-k)>5 and (j+k)%4!=0:continue
        scopes=sorted(set(map(abs,F[j]))|set(map(abs,F[k])))
        for modes in ('SS','SU','US','UU'):
            expected=all(not any((int(l>0) if modes[0]=='S' else int(l<0)) !=
                          (int(v>0) if modes[1]=='S' else int(v<0))
                          for l in F[j] for v in F[k] if abs(l)==abs(v)) for _ in [0])
            got=False
            for bits in itertools.product((0,1),repeat=len(scopes)):
                a=dict(zip(scopes,bits));t1=sum(litval(l,a) for l in F[j]);t2=sum(litval(l,a) for l in F[k]);ops+=1
                if t1==(len(F[j]) if modes[0]=='S' else 0) and t2==(len(F[k]) if modes[1]=='S' else 0):got=True;break
            assert got==expected
    return {'checks':ops}


def triple_extreme_controls(F,limit=18):
    """Sample source-indexed triple local S/U modes, compare with full assignments."""
    out=[];checks=0
    for ids in itertools.combinations(range(len(F)),3):
        clauses=[F[j] for j in ids]
        scope=[set(map(abs,c)) for c in clauses]
        if sum(bool(scope[a]&scope[b]) for a,b in itertools.combinations(range(3),2))<2:continue
        v=sorted(set.union(*scope));modes={}
        for word in itertools.product('SU',repeat=3):
            expected={};feasible=True
            for c,mode in zip(clauses,word):
                for l in c:
                    val=int(l>0) if mode=='S' else int(l<0)
                    if abs(l) in expected and expected[abs(l)]!=val:feasible=False
                    expected[abs(l)]=val
            observed=False
            for bits in itertools.product((0,1),repeat=len(v)):
                a=dict(zip(v,bits));checks+=1
                if all(sum(litval(l,a) for l in c)==(len(c) if mode=='S' else 0)
                       for c,mode in zip(clauses,word)):
                    observed=True;break
            assert feasible==observed,(ids,word)
            modes[''.join(word)]=feasible
        out.append({'three_original_clause_indices':[x+1 for x in ids],
                    'eight_joint_S_U_modes':modes,'some_coherent_all_extreme_mode_exists':any(modes.values())})
        if len(out)>=limit:break
    return out,checks

def direct_source_cube(F):
    for j,c in enumerate(F):
        for k in range(j+1,len(F)):
            d=F[k]
            for pivot in c:
                if -pivot not in d:continue
                rem=[l for l in c if l!=pivot]+[l for l in d if l!=-pivot]
                if any(-x in rem for x in rem):continue
                res=tuple(sorted(set(rem),key=lambda l:(abs(l),l<0)))
                forced={abs(l):int(l<0) for l in res}
                if len(forced)>5:continue
                assert sum(litval(l,forced) for l in c if abs(l) in forced)==0
                assert sum(litval(l,forced) for l in d if abs(l) in forced)==0
                assert [l for l in c if abs(l) not in forced]==[pivot]
                assert [l for l in d if abs(l) not in forced]==[-pivot]
                # Exact derivation: both parents reduce to complementary unit literals.
                return {'original_parents':[j+1,k+1],'pivot_original_variable':abs(pivot),
                        'source_literals':[pivot,-pivot],'resolvent':list(res),
                        'forbidden_original_variable_cube':{str(i):v for i,v in sorted(forced.items())},
                        'certificate':'under cube, source parents are opposing unit clauses on the pivot',
                        'RUP_checked':True}
    return None


def four_class_spectrum(F,base,check=True):
    """Exact four-category histogram of coherent 0,1,2-flip assignments.

    For strict22 proper 3CNF, each variable participates in four source clauses,
    so number B of singleton 4-vectors is bounded independently of n.  Work
    O(n + m + B^2 + B*(n+|E|)) with simple reconstruction, O(n+m+B^2)
    for histogram alone; E is original-variable cooccurrence pairs, |E|<=3m.
    """
    n=len(base);assert set(base)==set(range(1,n+1))
    N=[0]*4; d={i:[0]*4 for i in base};H=collections.defaultdict(lambda:[0]*4)
    ops=collections.Counter()
    for clause in F:
        assert len(clause)==3 and len({abs(x) for x in clause})==3
        bits=[int(litval(z,base)) for z in clause]
        t=sum(bits); N[t]+=1;ops['original_literal_reads']+=3;ops['original_clause_statuses']+=1
        one=[t+1-2*b for b in bits]
        for pos,l in enumerate(clause):
            for r in range(4):d[abs(l)][r]+=int(one[pos]==r)-int(t==r);ops['single_clausal_updates']+=1
        for p,q in itertools.combinations(range(3),2):
            i,j=sorted((abs(clause[p]),abs(clause[q])))
            both=t+2-2*(bits[p]+bits[q]);h=H[(i,j)]
            for r in range(4):
                h[r]+=int(both==r)-int(one[p]==r)-int(one[q]==r)+int(t==r)
                ops['second_order_clausal_updates']+=1
    D={i:tuple(d[i]) for i in d};freq=collections.Counter(D.values())
    ops['singleton_bucket_inserts']+=n
    def plus(*args):return tuple(map(sum,zip(*args)))
    keys=sorted(freq);h2=collections.Counter();predict=collections.Counter()
    for ii,v in enumerate(keys):
        for w in keys[ii:]:
            ops['bucket_pair_evaluations']+=1
            ct=freq[v]*freq[w] if v!=w else freq[v]*(freq[v]-1)//2
            if ct:
                z=plus(N,v,w);h2[z]+=ct;predict[z]+=ct
    adj=collections.defaultdict(set)
    for (i,j),h in H.items():
        adj[i].add(j);adj[j].add(i)
        z0=plus(N,D[i],D[j]);z1=plus(N,D[i],D[j],tuple(h))
        h2[z0]-=1;h2[z1]+=1
        ops['neighbor_pair_corrections']+=1
    h2={tuple(k):v for k,v in h2.items() if v}
    assert all(v>0 for v in h2.values())
    assert sum(h2.values())==math.comb(n,2)
    h0={tuple(N):1};h1=collections.Counter(plus(N,D[i]) for i in range(1,n+1))
    assert sum(h1.values())==n
    if check and n<=15:
        for dist,hist in ((0,h0),(1,h1),(2,h2)):
            oracle=collections.Counter()
            for flips in itertools.combinations(range(1,n+1),dist):
                a=dict(base)
                for i in flips:a[i]^=1
                oracle[tuple(histogram(F,a))]+=1
            assert dict(oracle)==dict(hist),(dist,oracle,hist)
    # Transferred one-endpoint spectrum: for 3-CNF and base=0, F(~(0 xor S))
    # has vector exactly reversed from F(0 xor S), for every coherent flip set.
    # The algorithm looks for an actual witness, not just a low contradiction count.
    buckets=collections.defaultdict(list)
    for i,v in D.items():buckets[v].append(i)
    witness=None
    def good(v):return v[0]==0 or v[3]==0
    def maybe_record(flips,vec):
        a=dict(base)
        for i in flips:a[i]^=1
        if vec[0]==0:
            w=a;endpoint='base'
        elif vec[3]==0:
            w={i:1-b for i,b in a.items()};endpoint='complement'
        else:return None
        for c in F:ops['witness_source_literal_reads']+=len(c)
        assert ismodel(F,w)
        return {'relative_endpoint':endpoint,'flips':list(flips),'witness':[w[i] for i in range(1,n+1)],
                'original_four_counts':list(vec)}
    if good(tuple(N)):witness=maybe_record([],tuple(N))
    if witness is None:
        for i in range(1,n+1):
            ops['single_witness_candidates']+=1
            vv=plus(N,D[i])
            if good(vv):witness=maybe_record([i],vv);break
    if witness is None and any(good(v) for v in h2):
        for (i,j),h in H.items():
            ops['adjacent_witness_candidates']+=1
            vv=plus(N,D[i],D[j],tuple(h))
            if good(vv):witness=maybe_record([i,j],vv);break
    if witness is None and any(good(v) for v in h2):
        for ii,v in enumerate(keys):
            for w in keys[ii:]:
                ops['nonadjacent_bucket_targets']+=1
                vv=plus(N,v,w)
                if not good(vv):continue
                for i in buckets[v]:
                    for j in buckets[w]:
                        ops['nonadjacent_candidate_scans']+=1
                        if i!=j and j not in adj[i]:
                            witness=maybe_record([i,j],vv);break
                    if witness is not None:break
                if witness is not None:break
            if witness is not None:break
    assert (witness is not None)==any(good(q) for hist in [h0,h1,h2] for q in hist)
    ops['charged_selected_events']=sum(ops.values())
    return {'base_original_N0_N1_N2_N3':N,
            'delta_vector_buckets':[{'delta':list(z),'multiplicity':v} for z,v in sorted(freq.items())],
            'cooccurring_variable_pairs':len(H),'nonzero_second_order_pairs':sum(any(q) for q in H.values()),
            'hamming0_histogram':[{'N':list(k),'count':v} for k,v in sorted(h0.items())],
            'hamming1_histogram':[{'N':list(k),'count':v} for k,v in sorted(h1.items())],
            'hamming2_histogram':[{'N':list(k),'count':v} for k,v in sorted(h2.items())],
            'one_endpoint_complement_histograms_obtained_by_reversing_every_N_vector':True,
            'witness_up_to_two_flips_of_either_endpoint':witness,'charged_work':dict(ops)}

class Ledger:
    def __init__(self):self.events=0;self.clause_reads=0;self.literal_reads=0;self.states=0
    def clause(self,c):self.events+=1;self.clause_reads+=1;self.literal_reads+=len(c);self.events+=len(c)
    def asdict(self):return {'selected_events':self.events,'source_clause_reads':self.clause_reads,
                           'source_literal_reads':self.literal_reads,'DPLL_states':self.states}

def up(F,pin,ledger):
    a=dict(pin);reasons=[]
    while True:
        progress=False
        for j,c in enumerate(F,1):
            ledger.clause(c)
            if any((abs(l) in a and litval(l,a)) for l in c):continue
            rest=[l for l in c if abs(l) not in a]
            if not rest:return None,{'kind':'original_clause_falsified','source_j':j,'assignments':dict(a),'reasons':reasons}
            if len(rest)==1:
                l=rest[0];x=abs(l);a[x]=int(l>0);ledger.events+=1
                reasons.append({'source_j':j,'forced_original_literal':l})
                progress=True;break
        if not progress:return a,None

def dpll(F,n,ledger,pin=None):
    def walk(assign):
        ledger.states+=1;ledger.events+=1
        a,bad=up(F,assign,ledger)
        if bad:return False,{'conflict':bad}
        if len(a)==n:
            assert ismodel(F,a);return True,{'witness':a}
        # Choose fixed ascending original variable (not semantic answer information)
        x=next(x for x in range(1,n+1) if x not in a)
        L=[]
        for val in (0,1):
            q=dict(a);q[x]=val;good,trace=walk(q);L.append({'decision_original_var':x,'value':val,'child':trace})
            if good:return True,trace
        return False,{'branches':L,'unit_assignments':a}
    return walk({} if pin is None else pin)

def second_order(F,base,check=True):
    """Exact count of SAT assignments at distances 0,1,2, O(n+sum |C|^2)."""
    n=max(base);D0=0;delta=[0]*(n+1);hh=collections.defaultdict(int)
    ops={'input_literals_scanned':0,'clause_status_evals':0,'singleton_local_evals':0,
         'pair_local_evals':0,'pair_interaction_updates':0,'bucket_combinations':0,
         'neighbor_adjustments':0,'witness_candidate_checks':0}
    for c in F:
        ops['input_literals_scanned']+=len(c)
        bbits=[int(litval(l,base)) for l in c]
        u=int(sum(bbits)==0);D0+=u;ops['clause_status_evals']+=1
        one=[]
        for pos,l in enumerate(c):
            z=u if False else int(sum(bbits)+1-2*bbits[pos]==0)
            one.append(z);delta[abs(l)]+=z-u;ops['singleton_local_evals']+=1
        for p,q in itertools.combinations(range(len(c)),2):
            both=int(sum(bbits)+2-2*(bbits[p]+bbits[q])==0)
            i,j=sorted((abs(c[p]),abs(c[q])));hh[(i,j)]+=both-one[p]-one[q]+u
            ops['pair_local_evals']+=1;ops['pair_interaction_updates']+=1
    hist=collections.Counter(delta[1:]); counts0=int(D0==0);counts1=sum(D0+d==0 for d in delta[1:])
    wanted=-D0;predicted=0
    for d,ct in sorted(hist.items()):
        e=wanted-d
        if d>e or e not in hist:continue
        predicted+=ct*hist[e] if d<e else ct*(ct-1)//2
        ops['bucket_combinations']+=1
    corrections=0
    adj=collections.defaultdict(set)
    for (i,j),h in hh.items():
        adj[i].add(j);adj[j].add(i)
        before=int(D0+delta[i]+delta[j]==0)
        after=int(D0+delta[i]+delta[j]+h==0)
        corrections+=after-before;ops['neighbor_adjustments']+=1
    exact2=predicted+corrections
    assert exact2>=0
    # Recover any explicit model at radius <=2, without n^2 enumeration.
    witness=None
    if counts0:witness=[]
    if witness is None:
        witness=next(([i] for i in range(1,n+1) if D0+delta[i]==0),None)
    if witness is None:
        for (i,j),h in hh.items():
            ops['witness_candidate_checks']+=1
            if D0+delta[i]+delta[j]+h==0:witness=[i,j];break
    if witness is None and exact2>0:
        buckets=collections.defaultdict(list)
        for i in range(1,n+1):buckets[delta[i]].append(i)
        for i in range(1,n+1):
            for j in buckets.get(wanted-delta[i],[]):
                ops['witness_candidate_checks']+=1
                if i!=j and j not in adj[i]:
                    witness=[i,j];break
            if witness is not None:break
    if witness is not None:
        a=dict(base)
        for i in witness:a[i]^=1
        assert ismodel(F,a),(witness,base)
    assert (witness is not None)==bool(counts0+counts1+exact2)
    # Local checked resource total for this particular source; native elapsed/memory separately.
    ops['counted_selected_operations']=sum(ops.values())
    out={'base_N0':D0,'per_variable_delta':delta[1:],'delta_buckets':dict(sorted(hist.items())),
         'cooccurrence_pair_count':len(hh),'nonzero_interaction_count':sum(h!=0 for h in hh.values()),
         'predicted_pair_models':predicted,'neighbor_correction_to_pair_models':corrections,
         'exact_hamming0_models':counts0,'exact_hamming1_models':counts1,
         'exact_hamming2_models':exact2,'radius2_model_count':counts0+counts1+exact2,
         'reconstructed_flip_set':witness,'operation_ledger':ops}
    if check and n<=15:
        brute=[0,0,0]
        for d in range(3):
            for vs in itertools.combinations(range(1,n+1),d):
                a=dict(base)
                for x in vs:a[x]^=1
                brute[d]+=int(ismodel(F,a))
        assert brute==[counts0,counts1,exact2],(brute,out)
        out['independent_bruteforce_hamming0_1_2_counts']=brute
    return out

def profile(fn,*args):
    tracemalloc.start();t=time.perf_counter();r=fn(*args);wall=time.perf_counter()-t;_,pk=tracemalloc.get_traced_memory();tracemalloc.stop()
    return r,{'wall_seconds':wall,'peak_python_traced_bytes':pk}

def solve_base(F,n):
    led=Ledger();led.events+=sum(len(c)+1 for c in F) # input parsing/source list
    good,tree=dpll(F,n,led);out={'SAT':good,'stats':led.asdict(),
                                 'witness':tree['witness'] if good else None,
                                 'unsat_certificate':tree if not good else None}
    if good:assert ismodel(F,tree['witness'])
    return out

def solve_plus(F,n):
    ledger=Ledger();ledger.events+=sum(len(c)+1 for c in F)
    if all(len(c)==3 and len({abs(z) for z in c})==3 for c in F):
        f=four_class_spectrum(F,{i:0 for i in range(1,n+1)},check=False)
        ledger.events+=f['charged_work']['charged_selected_events']
        win=f['witness_up_to_two_flips_of_either_endpoint']
        ans={i+1:win['witness'][i] for i in range(n)} if win else None
    else:
        # Binary/Horn mixed hostile controls: no false global t->3-t use.
        ans=None
        for val in (0,1):
            base={i:val for i in range(1,n+1)}
            f=second_order(F,base,check=False)
            ledger.events+=f['operation_ledger']['counted_selected_operations']
            if f['reconstructed_flip_set'] is not None:
                ans=base.copy()
                for i in f['reconstructed_flip_set']:ans[i]^=1
                break
    if ans is not None:
        assert ismodel(F,ans)
        ledger.events+=sum(len(c)+1 for c in F)
        return {'SAT':True,'stats':ledger.asdict(),'witness':ans,
                'used':'radius-two-'+('vector-spectrum' if all(len(c)==3 for c in F) else 'mixed-width-scalar-fallback')}
    good,tree=dpll(F,n,ledger)
    return {'SAT':good,'stats':ledger.asdict(),'witness':tree['witness'] if good else None,
            'unsat_certificate':tree if not good else None,'used':'full-UP-DPLL-after-failed-single-vector-spectrum'}

def enumerate_models(F,n):
    if n>15:return None
    counts=[0,0,0];total=0;complement_checks=0
    for mask in range(1<<n):
        a={i+1:mask>>i&1 for i in range(n)}
        t=[sum(tv) for tv in truth(F,a)]
        b={i:1-v for i,v in a.items()}
        u=[sum(tv) for tv in truth(F,b)]
        assert all(z+w==len(F[j]) for j,(z,w) in enumerate(zip(t,u)))
        assert all(z+w==len(F[j]) for j,(z,w) in enumerate(zip(t,u)))
        complement_checks+=len(F)
        if 0 not in t:
            total+=1
            if mask.bit_count()<=2:counts[mask.bit_count()]+=1
    return {'independently_exhausted_full_assignments':1<<n,
            'model_total':total,'models_at_0_endpoint_radius2':counts,
            'independent_complement_clause_checks':complement_checks}

def run_case(label,F,do_pair=True,do_baseline=True):
    n=max(variables(F));a0={i:0 for i in range(1,n+1)};a1={i:1 for i in a0}
    rows=source_extremes(F);pairs,checks=pair_compat(F) if do_pair else ([],0)
    triples,triple_checks=triple_extreme_controls(F)
    lo,lp=profile(second_order,F,a0,True);hi,hp=profile(second_order,F,a1,True)
    if all(len(c)==3 for c in F):
        full,fp=profile(four_class_spectrum,F,a0,True)
        h0=full['hamming0_histogram'];h1=full['hamming1_histogram'];h2=full['hamming2_histogram']
        assert sum(x['count'] for h in (h0,h1,h2) for x in h if x['N'][0]==0)==lo['radius2_model_count']
        assert sum(x['count'] for h in (h0,h1,h2) for x in h if x['N'][3]==0)==hi['radius2_model_count']
    else:full=None;fp=None
    basic=profile(solve_base,F,n) if do_baseline else None
    plus=profile(solve_plus,F,n) if do_baseline else None
    if basic is not None:assert basic[0]['SAT']==plus[0]['SAT']
    if basic is not None and n<=15:
        brute=enumerate_models(F,n)
        assert (brute['model_total']>0)==basic[0]['SAT']
    else:brute=None
    trail=fliptrail(F,a0,[1,3,5,2,4,6] if n>=6 else list(range(1,n+1)))
    return {'case':label,'n':n,'m':len(F),'proper_width3':all(len(c)==3 and len(set(map(abs,c)))==3 for c in F),
            'strict_signed_exact22':exact22(F),'connected_primal':connected(F),
            'clauses':[list(c) for c in F], 'original_occurrences_and_S_U_targets':rows,
            'source_indexed_four_way_compatibility':pairs,'pair_exact_enumeration_checks':checks,
            'partial_extreme_spotcheck':independent_pair_check(F),
            'source_indexed_triple_extreme_checks':triples,'triple_exact_enumeration_checks':triple_checks,
            'endpoint_0':{'N0_N1_N2_N3':histogram(F,a0),'per_clause_literal_truth':truth(F,a0)},
            'endpoint_1':{'N0_N1_N2_N3':histogram(F,a1),'per_clause_literal_truth':truth(F,a1)},
            'intermediate_flip_trail_from_zero':trail,
            'source_parent_prohibited_cube':direct_source_cube(F),
            'four_category_radius2_spectrum_from_zero':full,'four_spectrum_same_run':fp,
            'zero_radius2_spectrum':lo,'zero_spectrum_same_run':lp,
            'one_radius2_spectrum':hi,'one_spectrum_same_run':hp,
            'baseline_solver':dict(basic[0],same_run=basic[1]) if basic else None,
            'two_endpoints_then_fallback':dict(plus[0],same_run=plus[1]) if plus else None,
            'independent_exhaustive_oracle':brute}

def main():
    cases=[('S15_strict22_SAT',parse(S15)),('W1_strict22_UNSAT',parse(W1)),
           ('MUT15_strict22_SAT',parse(MUT15)),('H1_strict22_plateau_SAT',plateau(1)),
           ('H2_strict22_plateau_SAT',plateau(2)),('H4_strict22_plateau_SAT',plateau(4)),
           ('unbalanced_signed_K4_NAE_strict22_SAT',paired_k4()),
           ('Krom_2SAT_SAT',((1,2),(-1,3),(2,3))),
           ('Horn_3CNF_SAT',((-1,-2,3),(-3,4),(-4,1))),
           ('3XOR_ODD_SAT',parity3(False)),
           ('parity_conflict_UNSAT',parity3(False)+parity3(True))]
    # adversarial variable renaming and literal sign flips retain SAT and exact22
    r=random.Random(SEED);src=parse(W1);perm=list(range(1,16));r.shuffle(perm)
    flip={i:r.choice((-1,1)) for i in range(1,16)}
    renamed=tuple(tuple(flip[abs(z)]*perm[abs(z)-1]*(1 if z>0 else -1) for z in c) for c in src)
    cases.append(('W1_renamed_complemented_UNSAT',renamed))
    summary=[];raw=[]
    for label,F in cases:
        r=run_case(label,F,do_pair=(len(F)<=20),do_baseline=True);raw.append(r)
        lo=r['zero_radius2_spectrum'];hi=r['one_radius2_spectrum']
        b=r['baseline_solver'];p=r['two_endpoints_then_fallback']
        summary.append({'case':label,'n':r['n'],'m':r['m'],'strict22':r['strict_signed_exact22'],
                        'SAT':b['SAT'],'zero_endpoint_radius2_count':lo['radius2_model_count'],
                        'one_endpoint_radius2_count':hi['radius2_model_count'],
                        'hamming2_zero':lo['exact_hamming2_models'],
                        'hamming2_one':hi['exact_hamming2_models'],
                        'source_pairs':len(r['source_indexed_four_way_compatibility']),
                        'baseline_DPLL_states':b['stats']['DPLL_states'],
                        'hybrid_DPLL_states':p['stats']['DPLL_states'],
                        'baseline_selected_events':b['stats']['selected_events'],
                        'hybrid_selected_events':p['stats']['selected_events'],
                        'baseline_peak_traced_bytes':b['same_run']['peak_python_traced_bytes'],
                        'hybrid_peak_traced_bytes':p['same_run']['peak_python_traced_bytes'],
                        'baseline_wall_sec':b['same_run']['wall_seconds'],
                        'hybrid_wall_sec':p['same_run']['wall_seconds'],
                        'hybrid_route':p['used']})
    report={'run_id':'SECOND_ORDER_FLIP_SPECTRUM243','seed':SEED,'model':'indexed word RAM logical event proxy + Python time/memory',
            'scope':'exact Hamming spheres of radius<=2, not general SAT solver','summary':summary,'cases':raw}
    text=json.dumps(report,indent=2,sort_keys=True)
    dest=sys.argv[1] if len(sys.argv)>1 else 'SECOND_ORDER_FLIP_SPECTRUM243_raw.json'
    open(dest,'w').write(text+'\n')
    out=dest.replace('_raw.json','_summary.json')
    open(out,'w').write(json.dumps({'run_id':report['run_id'],'seed':SEED,'source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest(),
                                  'raw_sha256':hashlib.sha256((text+'\n').encode()).hexdigest(),'summary':summary},indent=2)+'\n')
    print(json.dumps({'raw':dest,'summary':out,'rows':len(summary),'summary_rows':summary},indent=2))
if __name__=='__main__':main()
