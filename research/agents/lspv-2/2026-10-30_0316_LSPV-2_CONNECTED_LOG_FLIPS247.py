#!/usr/bin/env python3
"""Exact connected-logarithm compilation for bounded-degree clause flip spectra.
Python 3.10+ standard library. An indexed-RAM arithmetic-operation prototype,
NOT a P-vs-NP solver or a Turing-machine time claim. All original clause IDs kept.
Usage: python 2026-10-30_0316_LSPV-2_CONNECTED_LOG_FLIPS247.py output.json
"""
from __future__ import annotations
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
from math import comb, lcm
import json, sys, random, time, tracemalloc

W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
S15='-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14'

def parse(s): return tuple(tuple(int(x) for x in c.split()) for c in s.split(';'))
def plateau(r):
    v=lambda j,i:6*(j%r)+i
    F=[]
    for j in range(r):
        F.extend(((v(j-1,1),v(j,3),v(j,5)),(v(j,1),-v(j,3),v(j,6)),(-v(j,1),v(j,4),v(j,5)),(-v(j,1),-v(j,4),v(j,6)),(v(j,2),v(j,3),-v(j,5)),(v(j,2),-v(j,3),-v(j,6)),(-v(j,2),v(j,4),-v(j,5)),(-v(j,2),-v(j,4),-v(j,6))))
    return tuple(F)
def parity(even=True):
    return tuple(tuple(-(i+1) if bits[i] else i+1 for i in range(3)) for bits in product((0,1),repeat=3) if sum(bits)%2!=int(even))
def numvars(F): return max(abs(x) for c in F for x in c)
def litval(l,a):return (a[abs(l)]==int(l>0))
def counts(F,a):return tuple(Counter(sum(litval(l,a) for l in c) for c in F)[i] for i in range(4))
def source_properties(F):
    n=numvars(F); cnt=Counter(l for c in F for l in c)
    graph={i:set() for i in range(1,n+1)}
    for c in F:
        for x,y in combinations(c,2):graph[abs(x)].add(abs(y));graph[abs(y)].add(abs(x))
    seen={1};todo=[1]
    for v in todo:
        for z in sorted(graph[v]-seen):seen.add(z);todo.append(z)
    return dict(connected=len(seen)==n,n=n,m=len(F),max_occ=max(cnt[i]+cnt[-i] for i in range(1,n+1)),proper3=all(len(c)==3 and len(set(map(abs,c)))==3 for c in F),strict22=all(cnt[i]==cnt[-i]==2 for i in range(1,n+1)),positive=[cnt[i] for i in range(1,n+1)],negative=[cnt[-i] for i in range(1,n+1)])

def source_audit(F):
    n=numvars(F); rows=[]
    for j,c in enumerate(F,1):
        occ=[dict(original_clause=j,variable=abs(x),signed_occurrence=x, S=int(x>0),invert_S_to_U=int(x<0),U=int(x<0),invert_U_to_S=int(x>0)) for x in c]
        rows.append(dict(j=j,original_literals=c,occurrences=occ,S_j={str(abs(x)):int(x>0) for x in c},U_j={str(abs(x)):int(x<0) for x in c},invert_S_j_to_U_j={str(abs(x)):int(x<0) for x in c},invert_U_j_to_S_j={str(abs(x)):int(x>0) for x in c}))
    pairs=[]; enumerations=0
    for j,k in combinations(range(len(F)),2):
        sj={abs(x):int(x>0) for x in F[j]};sk={abs(x):int(x>0) for x in F[k]}
        common=sj.keys()&sk.keys();same=sorted(i for i in common if sj[i]==sk[i]);opp=sorted(i for i in common if sj[i]!=sk[i]);allowed={'SS':not bool(opp),'SU':not bool(same),'US':not bool(same),'UU':not bool(opp)}
        scope=sorted(sj.keys()|sk.keys());observed={q:False for q in allowed}
        for vals in product((0,1),repeat=len(scope)):
            a=dict(zip(scope,vals));tr=[sum(litval(l,a) for l in F[t]) for t in (j,k)];mode=''.join('S' if tr[z]==3 else 'U' if tr[z]==0 else 'M' for z in (0,1))
            if mode in observed:observed[mode]=True
            enumerations+=1
        assert allowed==observed
        pairs.append(dict(j=j+1,k=k+1,same=same,opposite=opp,SS_SU_US_UU=allowed,mandatory_middle=not any(allowed.values())))
    trails={}
    for b in (0,1):
        a={i:b for i in range(1,n+1)};rec=[]
        for event,var in [('endpoint',0)]+[(f'flip_{i}',i) for i in range(1,min(5,n)+1)]+[('complete_inversion',-1)]:
            if var==-1:a={i:1-x for i,x in a.items()}
            elif var>0:a[var]^=1
            t=[sum(litval(l,a) for l in c) for c in F];N=[t.count(i) for i in range(4)];rec.append(dict(event=event,values=''.join(str(a[i]) for i in range(1,n+1)),t_by_original_clause=t,N=N,SAT=(N[0]==0)))
        trails[str(b)+'^n']=rec
    return dict(clauses=rows,pair_extreme_matrix=pairs,global_endpoint_flip_trails=trails,exact_pair_enumerations=enumerations)

def resolution_cube(F):
    for j,k in combinations(range(len(F)),2):
        for pivot in F[j]:
            if -pivot not in F[k]:continue
            R=set(F[j]+F[k])-{pivot,-pivot}
            if any(-l in R for l in R):continue
            a={abs(l):int(l<0) for l in R}
            for x in (0,1):
                check=dict(a);check[abs(pivot)]=x
                assert not all(any(litval(l,check) for l in F[t]) for t in (j,k))
            return dict(parents=[j+1,k+1],pivot=abs(pivot),resolvent=sorted(R,key=lambda x:(abs(x),x<0)),forbidden_cube=a,certificate='Falsifying this non-tautological resolvent makes opposite source-parent units; both pivot choices refuted.')
    return None

Z4=(0,0,0,0)
def vv_add(a,b):return tuple(x+y for x,y in zip(a,b))
def add_key(poly,key,val):
    poly[key]+=val
    if not poly[key]:del poly[key]

def connected_spectrum(F,base,r,allowed=None):
    """Return exact histogram and work ledger via logarithmic connected supports."""
    n=numvars(F); assert set(base)==set(range(1,n+1))
    eligible=set(base) if allowed is None else set(allowed)
    assert eligible<=set(base) and r<=len(eligible)
    N0=counts(F,base); inc={i:[] for i in eligible};neigh={i:set() for i in eligible};base_t=[];work=Counter()
    for cid,c in enumerate(F):
        base_t.append(sum(litval(x,base) for x in c));work['initial_clause_scan']+=len(c)
        for x in c:
            if abs(x) in eligible:inc[abs(x)].append(cid)
        for x,y in combinations(c,2):
            if abs(x) in eligible and abs(y) in eligible:
                neigh[abs(x)].add(abs(y));neigh[abs(y)].add(abs(x))
    def delta(S):
        clauses=set(t for i in S for t in inc[i]);D=[0]*4
        for cid in clauses:
            c=F[cid];t=base_t[cid]
            q=t+sum(1 if not litval(z,base) else -1 for z in c if abs(z) in S)
            D[t]-=1;D[q]+=1;work['source_incidence_clause_visits']+=1
        return tuple(D)
    if r==0:
        return {tuple(N0):1},dict(work),dict(connected_supports=0,max_interaction_degree=0,log_monomials=0,histogram_buckets=1)
    # All vertex subsets whose induced co-occurrence graph is connected.
    connected={frozenset((i,)) for i in eligible}
    frontier=set(connected)
    for _ in range(2,r+1):
        fresh=set()
        for S in frontier:
            pool=set.union(*(neigh[i] for i in S)) if S else set()
            for u in pool-S:fresh.add(S|{u});work['connected_support_extensions']+=1
        connected.update(fresh);frontier=fresh
    # Build B_i(T) in log Z(z,T) = sum B_i z^i, for i <= r.
    scale=lcm(*range(1,r+1))
    B=[defaultdict(int) for _ in range(r+1)]
    for H in sorted(connected,key=lambda s:(len(s),tuple(sorted(s)))):
        vertices=tuple(sorted(H));h=len(vertices)
        A=defaultdict(int)
        for mask in range(1,1<<h):
            S={vertices[i] for i in range(h) if (mask>>i)&1}
            alpha=tuple(int(i in S) for i in vertices)
            D=delta(S);A[(alpha,D)]+=1;work['support_weight_subsets']+=1
        # Power A^k yields coefficient of log(1+A) via +/- 1/k. The
        # nonempty H-support terms alone are assigned to this H once.
        power={(tuple(0 for i in vertices),Z4):1}
        for k in range(1,r+1):
            nxt=defaultdict(int)
            for (aa,da),ca in power.items():
                for (bb,db),cb in A.items():
                    new=tuple(a+b for a,b in zip(aa,bb));size=sum(new)
                    if size>r:continue
                    add_key(nxt,(new,vv_add(da,db)),ca*cb);work['formal_polynomial_products']+=1
            power=nxt
            for (alpha,D),val in power.items():
                if all(alpha):add_key(B[sum(alpha)],D,((-1)**(k-1))*(scale//k)*val);work['log_connected_terms']+=1
    # Exp coefficient recurrence: k Z_k = sum_{i=1}^k i B_i Z_{k-i}.
    Z=[defaultdict(Fraction) for _ in range(r+1)];Z[0][Z4]=Fraction(1)
    for k in range(1,r+1):
        for i in range(1,k+1):
            for x,c in B[i].items():
                for y,v in Z[k-i].items():
                    add_key(Z[k],vv_add(x,y),Fraction(i*c,k*scale)*v);work['exponential_polynomial_products']+=1
    result={}
    for d,c in Z[r].items():
        assert c.denominator==1 and c>=0,(d,c)
        if c:
            hist=vv_add(N0,d);assert min(hist)>=0
            result[hist]=result.get(hist,0)+int(c)
    assert sum(result.values())==comb(len(eligible),r),(r,len(eligible),sum(result.values()),comb(len(eligible),r))
    return result,dict(work),dict(connected_supports=len(connected),max_interaction_degree=max(map(len,neigh.values())),log_monomials=sum(map(len,B)),histogram_buckets=len(result))

def extract_witness_self_reduction(F,base,r,require_N3=False):
    """Polynomial-in-n FPT witness extraction via greedy conditioned histogram tests.
    At most n+1 full charged compilers; never guesses an unverified SAT answer.
    """
    n=numvars(F);eligible=set(range(1,n+1));forced=set();calls=0;ledger=Counter()
    def possible(T,E):
        nonlocal calls
        a={i:base[i] ^ int(i in T) for i in base}
        k=r-len(T)
        if k>len(E):return False
        hist,w,_=connected_spectrum(F,a,k,allowed=E);calls+=1;ledger.update(w)
        return any(c and ((N[3] if require_N3 else N[0])==0) for N,c in hist.items())
    if not possible(forced,eligible):return None,dict(calls=calls,work=dict(ledger))
    for i in sorted(base):
        if len(forced)==r:break
        if len(eligible)==r-len(forced):forced.update(eligible);eligible.clear();break
        remaining=eligible-{i}
        if possible(forced,remaining):eligible=remaining
        else:forced.add(i);eligible=remaining
    assert len(forced)==r
    a={i:base[i] ^ int(i in forced) for i in base}
    if require_N3:a={i:1-v for i,v in a.items()}
    assert counts(F,a)[0]==0
    return a,dict(calls=calls,work=dict(ledger),forced_flip_set=sorted(forced),source_verification_literal_reads=sum(map(len,F)))

def brute_hist(F,a,r):
    n=numvars(F); hist=Counter();read=0
    for S in combinations(range(1,n+1),r):
        b=dict(a)
        for i in S:b[i]^=1
        hist[counts(F,b)]+=1
        read+=sum(map(len,F))
    return dict(hist),read

def dpll(F):
    """Plain chronological UP-DPLL with a replayable assignment conflict tree."""
    n=numvars(F);work=Counter();clauses=tuple(tuple(c) for c in F)
    def dfs(A):
        work['DPLL_states']+=1; A=dict(A); events=[]
        while True:
            changed=False
            for cid,c in enumerate(clauses,1):
                work['source_literal_reads']+=len(c)
                if any((abs(l) in A and litval(l,A)) for l in c):continue
                unset=[l for l in c if abs(l) not in A]
                if not unset:
                    work['conflict_leaves']+=1
                    return None,{'conflicting_original_clause':cid,'assignments':A,'units':events}
                if len(unset)==1:
                    z=unset[0];v=int(z>0)
                    if abs(z) in A:assert A[abs(z)]==v
                    A[abs(z)]=v;events.append({'source_clause':cid,'forced_literal':z});work['UP_events']+=1;changed=True;break
            if not changed:break
        if len(A)==n:
            assert all(any(litval(l,A) for l in c) for c in F)
            return A,{'witness':A,'units':events}
        v=next(i for i in range(1,n+1) if i not in A)
        children=[]
        for t in (0,1):
            R=dict(A);R[v]=t;out,pr=dfs(R);children.append((t,pr))
            if out is not None:return out,{'decision':v,'units':events,'child':(t,pr)}
        return None,{'decision':v,'units':events,'children':children}
    witness,proof=dfs({});return witness,dict(work),proof

def chunk(F,tag,r,full_audit=True,brute=True,solve=True):
    n=numvars(F);base={i:0 for i in range(1,n+1)}
    record={'name':tag,'source_clauses':F,'properties':source_properties(F),'r':r,'endpoint_N':[counts(F,base),counts(F,{i:1 for i in base})], 'resolution_cube':resolution_cube(F)}
    if full_audit:record['mandatory_source_audit']=source_audit(F)
    tracemalloc.start();tic=time.perf_counter();hist,w,meta=connected_spectrum(F,base,r);record['connected_elapsed_s']=time.perf_counter()-tic;record['connected_peak_python_B']=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
    record['connected_work']=w;record['connected_details']=meta;record['histogram']=[{'N':list(N),'count':v} for N,v in sorted(hist.items())];record['hist_sum']=sum(hist.values())
    if brute:
        tracemalloc.start();tic=time.perf_counter();exact,reads=brute_hist(F,base,r);record['explicit_elapsed_s']=time.perf_counter()-tic;record['explicit_peak_python_B']=tracemalloc.get_traced_memory()[1];tracemalloc.stop();record['explicit_clause_literal_reads']=reads
        assert exact==hist,(tag,r,hist,exact)
    if solve:
        tracemalloc.start();tic=time.perf_counter();witness,ledger,proof=dpll(F);record['dpll_elapsed_s']=time.perf_counter()-tic;record['dpll_peak_python_B']=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
        record['baseline_dpll_work']=ledger;record['baseline_dpll_SAT']=witness is not None;record['baseline_witness']=witness
        record['baseline_proof_tree_leaf_count']=ledger.get('conflict_leaves',0)
        if witness is None: record['complete_original_source_unsat_tree']=proof
        if witness is not None:assert all(any(litval(x,witness) for x in c) for c in F)
        # Explicit uniform endpoint+radius prepass, measured separately.
        tracemalloc.start();tic=time.perf_counter();stages=[];model=None
        for val in (0,1):
            a={i:val for i in base};stages.append({'stage':str(val)+'^n','N':counts(F,a),'source_literal_reads':sum(map(len,F))})
            if counts(F,a)[0]==0:model=a;break
        if model is None:
            hh,ww,mm=connected_spectrum(F,base,r);stages.append({'stage':'cluster_compilation','work':ww,'meta':mm})
            if any(N[0]==0 for N in hh):
                model,reclog=extract_witness_self_reduction(F,base,r)
                stages.append({'stage':'witness_reconstruction_self_reduction','ledger':reclog})
        if model is None:
            model,other,tree=dpll(F);stages.append({'stage':'DPLL_fallback','work':other})
        record['hybrid_total_elapsed_s']=time.perf_counter()-tic;record['hybrid_peak_python_B']=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
        record['hybrid_stages']=stages;record['hybrid_SAT']=model is not None;assert (model is not None)==(witness is not None)
    return record

def main(path):
    rng=random.Random(247); cases=[('H1',plateau(1),3),('H2',plateau(2),4),('H3',plateau(3),3),('W1_UNSAT',parse(W1),3),('S15_SAT',parse(S15),3),('XOR_even',parity(True),3),('XOR_odd',parity(False),3),('Horn',((1,-2,-3),(-1,-2,3),(-1,2,-3)),3)]
    dense_rng=random.Random(247)
    dense=tuple(tuple(v if dense_rng.randrange(2) else -v for v in dense_rng.sample(range(1,9),3)) for _ in range(24))
    cases.append(('dense_random8',dense,3))
    changed=[tuple(-z if abs(z)==1 else z for z in c) for c in plateau(2)]
    cases.append(('H2_polarity_rename',tuple(changed),3))
    out={'seed':247,'timestamp':'2026-10-30T03:16:00-07:00','theorem':'connected logarithmic support expansion of all radius-r clause-status histograms','cases':[]}
    filt=set(sys.argv[2:])
    for name,F,r in cases:
        if filt and name not in filt:continue
        t=time.perf_counter();res=chunk(F,name,r,full_audit=True,brute=True,solve=True);out['cases'].append(res)
        print(name,'n',numvars(F),'r',r,'hist',res['connected_details']['histogram_buckets'],'t',round(time.perf_counter()-t,3),'s',flush=True)
    # Separate bigger controlled instances; full source compatibility matrix is NOT a solver input.
    for k in (4,6):
        if filt and ('H'+str(k)) not in filt:continue
        name='H'+str(k);F=plateau(k);r=3
        t=time.perf_counter();out['cases'].append(chunk(F,name,r,full_audit=True,brute=True,solve=False))
        print(name,'n',numvars(F),'r',r,'t',round(time.perf_counter()-t,3),'s',flush=True)
    with open(path,'w') as fp:json.dump(out,fp,indent=2)
    print('PASS',len(out['cases']),'cases','saved',path)
if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else 'CONNECTED_LOG_FLIPS247_raw.json')