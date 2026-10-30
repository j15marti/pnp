#!/usr/bin/env python3
"""ARC258: source-faithful bounded-occurrence cofactor-cover firewall.
All source clause ids stay fixed. No oracle or claim of unrestricted SAT hardness.
Python 3 stdlib only; deterministic seed. Bounded runs complete in <30 s.
"""
from __future__ import annotations
import json, math, random, time, tracemalloc, sys, hashlib, itertools
from collections import Counter
from fractions import Fraction
SEED=202610301424
rng=random.Random(SEED)

W=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
SWAP=list(W);SWAP[9]=(-5,6,-15);SWAP[13]=(-3,-6,-15)

def arc(k):
    assert k>=7 and k%2==1
    f=[]
    for i in range(k):
        for s in range(4):
            sg=1 if s<2 else -1
            f.append((sg*(i+1),sg*(k+(i+s)%k+1),sg*(2*k+(i+2*s)%k+1)))
    return f

def varset(F):return sorted({abs(x) for c in F for x in c})
def signed22(F):
    counts={v:[0,0] for v in varset(F)}
    for c in F:
        assert len(c)==3 and len({abs(x) for x in c})==3
        for x in c:counts[abs(x)][int(x<0)]+=1
    assert all(p==2 and q==2 for p,q in counts.values()),counts
    return True

def bitsource(F):
    n=max(varset(F)); b=1+math.ceil(math.log2(n+1));
    H=math.ceil(math.log2(n+1))+math.ceil(math.log2(len(F)+1))
    return H+len(F)*(2+3*b),b

def status(F,assignment):
    t=[]
    for c in F:
        t.append(sum(assignment.get(abs(x),0)==int(x>0) for x in c))
    C=Counter(t)
    return {'counts':[C[x] for x in range(4)],'true_literals':t,'sat':C[0]==0}

def restrict(F,pins):
    R=[];bad=None
    for j,c in enumerate(F,1):
        if any(abs(l) in pins and pins[abs(l)]==int(l>0) for l in c):continue
        new=tuple(l for l in c if abs(l) not in pins)
        if not new:bad=j;return [],bad
        R.append((j,new))
    return R,bad

def frozen_cnf_bits(R,b):
    H=math.ceil(math.log2(n+1))+math.ceil(math.log2(len(F)+1))
    return H+sum(2+b*len(c) for j,c in R)

def targets(F):
    out=[]
    for j,c in enumerate(F,1):
        s={abs(x):int(x>0) for x in c};u={v:1-z for v,z in s.items()}
        out.append({'j':j,'lits':list(c),'S_j':s,'invert_S_to_U':u,'U_j':u,'invert_U_to_S':s,
                    'occurrences':[{'x_ij':f'x_{abs(l)},{j}', 'literal':l,
                                    'S_value':int(l>0),'inverted_S_U_value':int(l<0),
                                    'U_value':int(l<0),'inverted_U_S_value':int(l>0)} for l in c]})
    return out

def combine(a,b):
    z=dict(a)
    for key,v in b.items():
        if key in z and z[key]!=v:return False
        z[key]=v
    return True

def pair_modes(T):
    pairs=[];same=0;opp=0;none=0;incons=0
    for a in range(len(T)):
        for b in range(a+1,len(T)):
            A=T[a];B=T[b];modes={k:combine(A[u],B[v]) for k,u,v in [('SS','S_j','S_j'),('SU','S_j','U_j'),('US','U_j','S_j'),('UU','U_j','U_j')]}
            so=set(A['S_j'])&set(B['S_j'])
            sp=any(A['S_j'][v]==B['S_j'][v] for v in so)
            op=any(A['S_j'][v]!=B['S_j'][v] for v in so)
            assert modes['SS']==(not op) and modes['UU']==(not op)
            assert modes['SU']==(not sp) and modes['US']==(not sp)
            if not any(modes.values()):
                incon=True
                involved=set(abs(l) for l in A['lits']+B['lits'])
                for mask in range(1<<len(involved)):
                    vals=dict(zip(sorted(involved),[(mask>>i)&1 for i in range(len(involved))]))
                    tt=[sum(vals[abs(l)]==int(l>0) for l in C['lits']) for C in (A,B)]
                    assert tt[0] in [1,2] or tt[1] in [1,2]
                incons+=1
            pairs.append({'j':A['j'],'k':B['j'],'modes':modes,'shared':sorted(so),'same_sign':sp,'opposite_sign':op})
    return pairs,incons

def flips(F,n):
    a={v:0 for v in range(1,n+1)};out=[]
    moves=[1,2,3,1,4,5,2,6] + list(range(7,min(n,11)+1))
    for idx,v in enumerate(moves):
        if v>n:continue
        old=status(F,a);a[v]^=1;new=status(F,a)
        asserted=sum(1 for c in F if v in [abs(l) for l in c] and next(l for l in c if abs(l)==v)>0)
        out.append({'step':idx+1,'flip':v,'counts_before':old['counts'],'counts_after':new['counts'],'counts_delta':[y-x for x,y in zip(old['counts'],new['counts'])],'assignment_bits':[a[i] for i in range(1,n+1)]})
    return out

def endpoint_audit(F):
    n=max(varset(F));zero={v:0 for v in range(1,n+1)};one={v:1 for v in range(1,n+1)}
    E={'zero':status(F,zero),'one':status(F,one),'flips':flips(F,n)}
    for name,a in (('zero',zero),('one',one)):
        s=E[name];compl={v:1-a[v] for v in a};r=status(F,compl)
        assert all(x+y==3 for x,y in zip(s['true_literals'],r['true_literals']))
        assert s['counts']==list(reversed(r['counts']))
    if n<=15:
        for mask in range(1<<n):
            a={v:(mask>>(v-1))&1 for v in range(1,n+1)}
            b={v:1-a[v] for v in a}
            A=status(F,a);B=status(F,b)
            assert A['counts']==list(reversed(B['counts']))
        E['exhaustive_complement_assignments']=1<<n
    else:
        for _ in range(64):
            a={v:rng.randrange(2) for v in range(1,n+1)};b={v:1-a[v] for v in a}
            A=status(F,a);B=status(F,b)
            assert A['counts']==list(reversed(B['counts']))
        E['sampled_complement_assignments']=64
    return E

class Ledger:
    def __init__(self):self.events=0;self.clause_scans=0;self.literal_reads=0;self.nodes=0;self.pruned=0;self.checks=0;self.max_live=0
    def scan(self,c):self.events+=len(c)+1;self.clause_scans+=1;self.literal_reads+=len(c)

def dpll(F,pins=None,L=None):
    if L is None:L=Ledger()
    L.nodes+=1;a=dict(pins or {})
    while True:
        newly=False
        for j,c in enumerate(F,1):
            L.scan(c)
            if any(abs(l) in a and a[abs(l)]==int(l>0) for l in c):continue
            free=[l for l in c if abs(l) not in a]
            if not free:L.pruned+=1;return None
            if len(free)==1:
                lit=free[0];v=abs(lit);z=int(lit>0)
                if v in a:
                    if a[v]!=z:L.pruned+=1;return None
                else:a[v]=z;L.events+=1;newly=True
        if not newly:break
    if all(any(abs(l) in a and a[abs(l)]==int(l>0) for l in c) for c in F):
        L.events+=len(F);L.checks+=1;return a
    unassigned=[v for v in varset(F) if v not in a]
    if not unassigned:raise AssertionError('DPLL terminal inconsistency')
    v=min(unassigned)
    for z in (0,1):
        L.events+=1;ans=dpll(F,a|{v:z},L)
        if ans is not None:return ans
    return None

def model_count(F,n):
    out=0
    for mask in range(1<<n):
        if all(any(((mask>>(abs(l)-1))&1)==int(l>0) for l in c) for c in F):out+=1
    return out

def cover_tree(F,h,maxnodes=300000,policy='min',metric='clauses',solve_children=False):
    n=max(varset(F)); seen=0; counter=Counter();mass=0;weights=Counter();examples=[];peak=0;min_live_depth=None;max_alive_bits=0;child_nodes=0;child_events=0;child_sat=0;child_unsat=0;access_bits=0;control_events=0;first_witness=None
    stack=[({},0)]
    while stack:
        pins,k=stack.pop();seen+=1;access_bits+=bitsource(F)[0];control_events+=len(F)*4+k+1
        if seen>maxnodes:return {'capped':True,'explored':seen,'nonterminal_stack':len(stack),'policy':policy}
        peak=max(peak,len(stack));R,bad=restrict(F,pins)
        if bad is not None:
            counter['source_conflict']+=1;weights['source_conflict']+=1<<(n-k)
            if len(examples)<5:examples.append({'cube':sorted(pins.items()),'reason_source_clause':bad})
            continue
        if (len(R) if metric=='clauses' else f_bittotal(R,F))<=h:
            counter['emitted']+=1;weights['emitted']+=1<<(n-k)
            min_live_depth=k if min_live_depth is None else min(min_live_depth,k)
            max_alive_bits=max(max_alive_bits, f_bittotal(R,F));control_events+=f_bittotal(R,F)
            if solve_children:
                LL=Ledger(); ww=dpll([tuple(c) for j,c in R],L=LL);child_nodes+=LL.nodes;child_events+=LL.events
                if ww is None:child_unsat+=1
                else:
                    child_sat+=1;control_events+=len(F)*4;full=pins|ww
                    assert all(any(full.get(abs(x),0)==int(x>0) for x in cc) for cc in F)
                    if first_witness is None:first_witness=full
            continue
        vs=[v for v in range(1,n+1) if v not in pins]
        if not vs:raise AssertionError('no vars but unresolved')
        if policy=='interleave' and n%3==0:
            z=n//3; order=[w for i in range(z) for w in (i+1,z+i+1,2*z+i+1)];v=next(w for w in order if w not in pins)
        elif policy=='maxdeg':
            deg=Counter(abs(x) for j,c in R for x in c);control_events+=sum(len(c) for j,c in R)+len(vs)
            v=max(vs,key=lambda t:(deg[t],-t))
        else:v=vs[0]
        stack.append((pins|{v:1},k+1));stack.append((pins|{v:0},k+1))
    assert sum(weights.values())==1<<n
    return {'capped':False,'policy':policy,'metric':metric,'visited_nodes':seen,'leaf_counts':dict(counter),'covered_assignments':dict(weights),'partition_fraction':str(Fraction(sum(weights.values()),1<<n)),
            'minimum_emitted_cube_depth':min_live_depth,'maximum_actual_emitted_child_bits':max_alive_bits,
            'peak_pending_cubes':peak,'proof_sample':examples,'source_bit_access_proxy':access_bits,'controller_selected_events':control_events,
            'child_solver_nodes':child_nodes,'child_solver_events':child_events,'child_sat':child_sat,'child_unsat':child_unsat,'SAT_by_OR_children':child_sat>0 if solve_children else None,'first_checked_witness':first_witness}

def f_bittotal(R,F):
    n=max(varset(F));b=1+math.ceil(math.log2(n+1))
    H=math.ceil(math.log2(n+1))+math.ceil(math.log2(len(F)+1))
    return H+sum(2+b*len(c) for j,c in R)

def forbidden_cover_example():
    # Clause G can be any 3CNF. x is fresh. F'=G AND (x OR u OR v).
    # F' |= x iff G UNSAT. Verify both labels on tiny complete controls.
    passed=0
    for mask in range(256):
        G=[]
        # 8 possible clauses on variables 1..3, each forbids a unique triple.
        for i in range(8):
            if mask&(1<<i):G.append(tuple(v if ((i>>(v-1))&1)==0 else -v for v in (1,2,3)))
        extended=G+[(4,5,6)]
        gsat=model_count(G,3)>0
        cover_ok=not any(all(any(((a>>(abs(l)-1))&1)==int(l>0) for l in c) for c in extended) and ((a>>3)&1)==0 for a in range(1<<6))
        assert cover_ok == (not gsat)
        passed+=1
    return {'checked_G':passed,'reduction':'G to Fprime=G AND (x OR u OR v); cover singleton x=1','cover_valid_iff_G_UNSAT':True}

def overlap(F,pins):
    cnt=[sum(abs(l) in pins and pins[abs(l)]==int(l>0) for l in c) for c in F]
    return {'satisfied_original_occurrences':sum(cnt),'deleted_clauses':sum(z>0 for z in cnt),
            'overlap_waste':sum(max(0,z-1) for z in cnt), 'pinned_variables':len(pins)}

def case(name,F,cover=True):
    assert signed22(F)
    n=max(varset(F));m=len(F);N,b=bitsource(F); L=math.floor(N**.5);q=math.floor(N**.6)
    # child clause count <= bit cap; even granting each clause only one bit.
    H=math.ceil(math.log2(n+1))+math.ceil(math.log2(m+1))
    h_phys=max(0,math.floor((L-H)/(2+b)))
    r=max(0,math.ceil((m-h_phys)/2))
    qmin=1<<r
    T=targets(F);pairs,middle=pair_modes(T);E=endpoint_audit(F)
    for _ in range(2048):
        pins={v:rng.randrange(2) for v in range(1,n+1) if rng.randrange(3)==0}
        O=overlap(F,pins)
        assert O['satisfied_original_occurrences']==2*len(pins)
        assert O['deleted_clauses']==2*len(pins)-O['overlap_waste']
        R,bad=restrict(F,pins)
        if bad is None:assert len(R)==m-O['deleted_clauses']
    E['source_signed22_overlap_checks']=2048
    if name.startswith('ARC'):
        k=n//3;E['all_A_prefixes_overlap']=[overlap(F,{v:0 for v in range(1,t+1)}) for t in range(0,k+1)]
    D=Ledger();start=time.perf_counter();witness=dpll(F,L=D);elapsed=time.perf_counter()-start
    sat=witness is not None
    if sat:assert all(any(witness.get(abs(l),0)==int(l>0) for l in c) for c in F)
    out={'name':name,'n':n,'m':m,'N_bits':N,'literal_record_bits':b,'FLMV_proposed_child_bit_cap':L,'FLMV_proposed_child_count_cap':q,
         'original_clause_header_bits':H,'physical_max_child_clauses_at_unit_width':h_phys,
         'certified_min_cube_depth_exact22_polarity_and_min_unit_bitwidth':r,'full_cube_cover_leaf_floor':qmin,
         'pure_complete_cover_exceeds_child_budget':qmin>q,'SAT':sat,
         'UP_DPLL':{'nodes':D.nodes,'events':D.events,'clause_scans':D.clause_scans,'literal_reads':D.literal_reads,'pruned':D.pruned,'time_seconds':elapsed},
         'pair_middle_edges':middle,'endpoint_audit':E,'local_targets':T,'pair_compatibility':pairs}
    if n<=15:
        out['exact_number_of_models']=model_count(F,n)
    if cover:
        h=math.floor(math.sqrt(N)) # optimistic: clause-count cap, NOT physical-bit cap
        out['optimistic_clause_count_cover']={policy:cover_tree(F,h,policy=policy) for policy in ('min','maxdeg')}
        if name.startswith('ARC') and n<=45:out['interleaved_policy_control']=cover_tree(F,h,maxnodes=30000,policy='interleave')
        if n<=15:out['literal_bit_budget_cover']={policy:cover_tree(F,h,policy=policy,metric='bits',solve_children=True) for policy in ('min','maxdeg')}
    return out



def algebraic_control_battery():
    # Reuses the source-authenticated 257 implementation as a separately archived comparator.
    import baseline_detectors257 as alg
    X=[]
    for x in itertools.product((0,1),repeat=3):
        X.append(tuple(-i if x[i-1] else i for i in (1,2,3)))
    parity0=[c for x,c in zip(itertools.product((0,1),repeat=3),X) if sum(x)%2==1]
    parity1=[c for x,c in zip(itertools.product((0,1),repeat=3),X) if sum(x)%2==0]
    controls=[('Horn_SAT',[(1,), (2,),(-1,-2,3)]),
              ('Horn_UNSAT',[(1,), (2,),(-1,-2,3),(-3,)]),
              ('Krom_SAT',[(1,2),(-1,2),(1,-2)]),
              ('Krom_UNSAT',[(1,2),(-1,2),(1,-2),(-1,-2)]),
              ('XOR_SAT',parity0),('XOR_UNSAT',parity0+parity1)]
    result=[]
    for name,F in controls:
        n=max(varset(F));LL=Ledger();d=dpll(F,L=LL)
        a=alg.Ledger();tag,ans=alg.classify(tuple(F),a)
        assert tag!='general' and ans is not None
        b,w=ans
        assert b==(d is not None)==(model_count(F,n)>0)
        if b:assert all(any(w.get(abs(l),0)==int(l>0) for l in c) for c in F)
        result.append({'name':name,'label':b,'detector':tag,'baseline_UP_DPLL_nodes':LL.nodes,
                       'baseline_UP_DPLL_events':LL.events,'algebraic_detector_events':a.events,
                       'algebraic_clause_reads':a.clause_reads,
                       'all_witnesses_original_checked':b})
    return result

def main():
    tracemalloc.start()
    raw={'seed':SEED,'status':'finite controls, not arbitrary SAT bound','cases':[],'cover_verifier_coNP':forbidden_cover_example(), 'algebraic_controls':algebraic_control_battery()}
    for name,F,cover in [('W1_UNSAT',W,True),('SWAP6_SAT',SWAP,True),('ARC_easy22_k7',arc(7),True),('ARC_easy22_k11',arc(11),True),('ARC_easy22_k15',arc(15),True),('ARC_easy22_k31',arc(31),False)]:
        before=time.perf_counter();r=case(name,F,cover);raw['cases'].append(r)
        print(name,'SAT',r['SAT'],'n',r['n'],'Nbits',r['N_bits'],'r',r['certified_min_cube_depth_exact22_polarity_and_min_unit_bitwidth'],
              '2^r',r['full_cube_cover_leaf_floor'],'max q',r['FLMV_proposed_child_count_cap'],
              'DPLL nodes',r['UP_DPLL']['nodes'],'cover',[(p,v.get('leaf_counts',{}),v.get('capped')) for p,v in r.get('optimistic_clause_count_cover',{}).items()],
              'secs',round(time.perf_counter()-before,3),flush=True)
    # check known family witness for every even/odd blocked sign pattern.
    for k in (7,11,15,31):
        F=arc(k);a={i+1:1 for i in range(k)}|{v:0 for v in range(k+1,3*k+1)}
        assert all(any(a[abs(l)]==int(l>0) for l in c) for c in F)
    raw['canonical_family_witness_verified']=[7,11,15,31]
    raw['peak_python_bytes']=tracemalloc.get_traced_memory()[1]
    with open('/mnt/data/arc258/raw.json','w') as f:json.dump(raw,f,indent=2,sort_keys=True)
    summary={k:raw[k] for k in ['seed','status','cover_verifier_coNP','algebraic_controls','canonical_family_witness_verified','peak_python_bytes']}
    summary['cases']=[{k:v for k,v in row.items() if k not in ('endpoint_audit','local_targets','pair_compatibility')} for row in raw['cases']]
    with open('/mnt/data/arc258/summary.json','w') as f:json.dump(summary,f,indent=2,sort_keys=True)
    print('source and summary SHA256',hashlib.sha256(open(__file__,'rb').read()).hexdigest(),hashlib.sha256(open('/mnt/data/arc258/raw.json','rb').read()).hexdigest(),flush=True)

if __name__=='__main__':main()
