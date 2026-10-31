#!/usr/bin/env python3
"""LSPV-4 exact, separately replayable restricted ARC cofactor/Kraft audit.
Pure Python 3.11+, no external dependencies. All operation counts are logical proxies, not FLMV steps.
"""
from fractions import Fraction
from math import ceil, log2
from collections import Counter
import json, argparse, itertools, hashlib

W1=[[-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],[5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],[-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],[2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]]
S15=[[-1,-3,14],[2,8,-9],[-10,13,14],[3,-7,-13],[-4,9,-11],[-5,-8,-14],[4,-8,11],[1,7,-13],[1,-7,10],[-5,-6,15],[-2,6,-12],[4,9,-10],[-2,5,-12],[3,6,-15],[-6,7,11],[2,-9,-11],[-4,8,10],[-3,12,15],[5,12,-15],[-1,13,-14]]

def f_name(F): return max(map(abs,itertools.chain.from_iterable(F)))
def val(l,assign):
    v=assign.get(abs(l))
    return None if v is None else (v==(l>0))
def status(F,a): return [sum(1 for l in cl if val(l,a) is True) for cl in F]
def issat(F,a): return all(any(val(l,a) is True for l in cl) for cl in F)
def cofactor(F,pins):
    out=[]; hits=0; tests=0; retained_untouched=0
    for cl in F:
        tests+=len(cl)
        if any(val(l,pins) is True for l in cl): hits+=1;continue
        row=[l for l in cl if val(l,pins) is None]
        if len(row)==3:retained_untouched+=1
        out.append(row)
    return out,dict(source_literal_tests=tests,satisfied_removed=hits,unhit_three_clauses=retained_untouched,child_literal_count=sum(map(len,out)))

def dpll(F,seed=None):
    stats=dict(nodes=0,decisions=0,unit_propagations=0,clause_visits=0,literal_tests=0)
    def recurse(a):
        stats['nodes']+=1
        while True:
            new=False
            for cl in F:
                stats['clause_visits']+=1
                vals=[]
                for l in cl:
                    stats['literal_tests']+=1
                    vals.append(val(l,a))
                if True in vals:continue
                unseen=[cl[i] for i,v in enumerate(vals) if v is None]
                if not unseen:return None
                if len(unseen)==1:
                    l=unseen[0];x=abs(l); req=l>0
                    if x in a and a[x]!=req:return None
                    if x not in a:
                        a[x]=req;stats['unit_propagations']+=1;new=True;break
            if not new:break
        unresolved=[]
        for cl in F:
            stats['clause_visits']+=1
            vals=[]
            for l in cl:
                stats['literal_tests']+=1
                vals.append(val(l,a))
            if True not in vals:unresolved.extend(l for l,v in zip(cl,vals) if v is None)
        if not unresolved:return a
        variable=abs(unresolved[0]);stats['decisions']+=1
        for b in (True,False):
            out=recurse({**a,variable:b})
            if out is not None:return out
        return None
    sol=recurse({} if seed is None else seed.copy())
    stats['selected_work']=stats['clause_visits']+stats['literal_tests']
    return sol,stats

def pair_controls(F):
    ans=[];checked=0
    for i in range(len(F)):
        for j in range(i+1,len(F)):
            a={abs(l):(l>0) for l in F[i]};b={abs(l):(l>0) for l in F[j]}; shared=set(a)&set(b)
            same=any(a[k]==b[k] for k in shared);opposite=any(a[k]!=b[k] for k in shared)
            expected=[not opposite,not same,not same,not opposite]
            keys=sorted(set(a)|set(b));observed=[False]*4
            for bits in itertools.product((False,True),repeat=len(keys)):
                z=dict(zip(keys,bits));r=status([F[i],F[j]],z)
                masks=[(3,3),(3,0),(0,3),(0,0)]
                for t,m in enumerate(masks):observed[t]|=(r==list(m))
            assert expected==observed,(i,j,expected,observed)
            ans.append({'clauses':[i+1,j+1],'SS':expected[0],'SU':expected[1],'US':expected[2],'UU':expected[3]})
            checked+=4
    return ans,checked


def source_resolvent(F):
    for i,a in enumerate(F):
        for j,b in enumerate(F[:i]):
            for l in a:
                if -l not in b:continue
                rr=sorted(set([x for x in a if x!=l]+[x for x in b if x!=-l]),key=lambda v:(abs(v),v<0))
                if any(-x in rr for x in rr):continue
                cube={abs(x):bool(x<0) for x in rr}
                # Every original-source model must satisfy the resolvent.
                n=f_name(F)
                for mask in range(1<<n):
                    if all((bool(mask&(1<<(abs(x)-1))))==cube[abs(x)] for x in rr):
                        aa={v:bool(mask&(1<<(v-1))) for v in range(1,n+1)}
                        assert not issat(F,aa)
                return {'parents':[j+1,i+1],'pivot':abs(l),'resolvent':rr,'forbidden_cube':cube,
                        'proof':'One resolution step on pivot from the two indicated source clauses; falsifying resolvent forbids cube.'}
    raise AssertionError('No nontautological resolvent')

def flmv(c):
    f=Fraction(1);best=Fraction(0);winner=0;details=[]
    for k in range(1,10000):
        f=c*f/(1+f); d=min((1/f-c)/k,c**(-k));details.append({'k':k,'d':str(d)})
        if d>best:best=d;winner=k
        if best>0 and c**(-(k+1))<best:
            return {'c':str(c),'maximum':str(best),'max_k':winner,'checked':details,
                    'tail_start_k':k+1,'tail_upper_strict':str(c**(-(k+1))),
                    'space_margin_over_half':str(best-Fraction(1,2))}
    raise Exception('tail not certified')

def copies(r,unsat):
    parts=[W1 if unsat and i==0 else S15 for i in range(r)]
    return [[(1 if l>0 else -1)*(abs(l)+15*i) for l in cl] for i,part in enumerate(parts) for cl in part]

def target_data(F):
    out=[]
    for j,cl in enumerate(F,1):
        out.append({'j':j,'occurrences':[{'i':abs(l),'signed_literal':l,'S':int(l>0),'invert_S':int(l<0),'U':int(l<0),'invert_U':int(l>0)} for l in cl]})
    return out

def endpoints_and_trail(F,n):
    trials=[0,1,3,7,((1<<n)-1)^7,(1<<n)-1]
    seen=[]
    for msk in trials:
        a={k+1:bool(msk&(1<<k)) for k in range(n)}
        t=status(F,a)
        seen.append({'assignment_mask':msk,'true_literal_counts':t,'N0_to_N3':[t.count(k) for k in range(4)],'sat':0 not in t})
    assert all(x+y==3 for x,y in zip(seen[0]['true_literal_counts'],seen[-1]['true_literal_counts']))
    return seen

def measured(F,h):
    n=f_name(F);one=[];stop=False
    total={'scan_literal_tests':0,'output_literals':0,'solver_nodes':0,'solver_clause_visits':0,'solver_literal_tests':0,'policy_events':0,'cases_attempted':0,'retained_peak_proxy_bits':0}
    leaf_records=[]
    # Canonical exact complete fixed-prefix cube partition. Halt on first SAT witness.
    for bits in itertools.product((False,True),repeat=h):
        pins=dict(zip(range(1,h+1),bits));child,meta=cofactor(F,pins)
        sol,st=dpll(child)
        total['scan_literal_tests']+=meta['source_literal_tests'];total['output_literals']+=meta['child_literal_count']
        total['solver_nodes']+=st['nodes'];total['solver_clause_visits']+=st['clause_visits'];total['solver_literal_tests']+=st['literal_tests'];total['policy_events']+=h+1;total['cases_attempted']+=1
        b=ceil(log2(n+1));total['retained_peak_proxy_bits']=max(total['retained_peak_proxy_bits'],sum(map(len,child))*(b+1)+h*(b+1))
        leaf_records.append({'pin':''.join('1' if v else '0' for v in bits),**meta,'solver_nodes':st['nodes'],'solver_sat':sol is not None})
        if sol is not None:stop=True;break
    total['selected_work']=sum(total[k] for k in ['scan_literal_tests','output_literals','solver_clause_visits','solver_literal_tests','policy_events'])
    total['sat']=stop
    return {'h':h,'q_max':1<<h,'observed':total,'leaves':leaf_records}

def enumerate_models(F,n):
    cnt=0
    for bits in range(1<<n):
        a={i+1:bool(bits&(1<<i)) for i in range(n)}
        if issat(F,a):cnt+=1
    return cnt


def all_leaf_output_audit(F,h):
    # An exhaustive exact SAT/UNSAT partition; do not stop when an early SAT leaf is found.
    n=f_name(F);b=ceil(log2(n+1));records=[]
    total=Counter()
    for bits in itertools.product((False,True),repeat=h):
        pins=dict(zip(range(1,h+1),bits));child,z=cofactor(F,pins)
        answer,stats=dpll(child)
        records.append({'pin':''.join('1' if v else '0' for v in bits),'depth':h,
                        'long_clauses':z['unhit_three_clauses'],'materialized_child_bits':z['child_literal_count']*(b+1),
                        'guest_nodes':stats['nodes'],'guest_sat':answer is not None})
        total['source_literal_reads']+=z['source_literal_tests']
        total['child_output_bits']+=z['child_literal_count']*(b+1)
        total['guest_work_proxy']+=stats['selected_work']
        total['selector_events']+=h+1
        total['guest_nodes']+=stats['nodes']
    total['output_lower_bound_bits']=2**h*(len(F)-4*h)*3*(b+1)
    assert total['child_output_bits']>=total['output_lower_bound_bits']
    total['joint_selected_proxy']=total['source_literal_reads']+total['child_output_bits']+total['guest_work_proxy']+total['selector_events']
    return {'h':h,'leaves':records,'totals':dict(total),'combined_sat':any(r['guest_sat'] for r in records)}

def comb_output(F,q):
    # q-leaf maximally unbalanced tree; every intermediate left branch is terminal guest,
    # with the last fork producing two leaves. Pin indices 1..q-1 on the long spine.
    n=f_name(F);assert 1<=q<=n+1
    paths=[]
    if q==1:paths=[{}]
    else:
        path={}
        for i in range(1,q):
            paths.append({**path,i:False});path[i]=True
        paths.append(path)
    b=ceil(log2(n+1));lengths=[];longs=[]
    for p in paths:
        child,z=cofactor(F,p)
        lengths.append(z['child_literal_count']*(b+1));longs.append(z['unhit_three_clauses'])
    assert len(paths)==q
    # full exact cylinder partition and a per-leaf untouched clause floor
    assert sum(Fraction(1,2**len(p)) for p in paths)==1
    floor=max(0,len(F)-4*(q-1))*3*(b+1)
    assert all(l>=floor for l in lengths)
    return {'q':q,'leaf_depths':list(map(len,paths)),'all_child_bits':lengths,'unhit_three_clauses':longs,
            'total_child_output_bits':sum(lengths),'universal_all_leaf_lower_bits':q*floor,
            'min_actual_child_bits':min(lengths)}

def runs():
    fl=[flmv(Fraction(6,5)),flmv(Fraction(241,200)),flmv(Fraction(7,5)),flmv(Fraction(3,2)),flmv(Fraction(8,5))]
    assert fl[0]['maximum']=='23/45' and fl[1]['maximum']=='11642479/23232400'
    cases=[]
    for name,F in [('W1_UNSAT',W1),('S15_SAT',S15)]:
        n=f_name(F);m=len(F);vars_cnt=Counter(map(abs,itertools.chain.from_iterable(F)))
        assert n==15 and m==20 and all(v==4 for v in vars_cnt.values())
        signs={i:[sum(l==i for cl in F for l in cl),sum(l==-i for cl in F for l in cl)] for i in range(1,n+1)}
        assert all(x==[2,2] for x in signs.values())
        modes,pchecked=pair_controls(F)
        models=enumerate_models(F,n);base_sol,baseline=dpll(F)
        assert bool(models)==(base_sol is not None)
        cases.append({'name':name,'n':n,'m':m,'models':models,'baseline_dpll':baseline,'source_sha256':hashlib.sha256(json.dumps(F,separators=(',',':')).encode()).hexdigest(),'source_clauses':F,
                      'targets':target_data(F),'derived_forbidden_cube':source_resolvent(F),'pair_modes':modes,'pair_modes_checked':pchecked,
                      'endpoints_and_flips':endpoints_and_trail(F,n),
                      'cofactor_partitions':[measured(F,h) for h in range(5)],
                      'all_leaf_partitions':[all_leaf_output_audit(F,h) for h in range(6)],
                      'adaptive_comb_partitions':[comb_output(F,q) for q in [2,4,8,12]]})
    hostile={}
    for name,F in {'HORN_SAT':[[-1,-2,3],[-2,-3,1],[-1,-3,2]],
                   'XOR3_SAT':[[(-i if bool(mask&(1<<(i-1))) else i) for i in (1,2,3)] for mask in range(8) if mask.bit_count()%2==1],
                   'XOR3_UNSAT':[[(-i if bool(mask&(1<<(i-1))) else i) for i in (1,2,3)] for mask in range(8)]}.items():
        n=f_name(F);d=dpll(F); models=enumerate_models(F,n)
        assert (d[0] is not None)==(models>0)
        hostile[name]={'n':n,'m':len(F),'models':models,'dpll':d[1],'cofactor_h2':measured(F,2)}
    asym=[]
    for r in [1,2,4,8,16,32,64]:
        for unsat in [True,False]:
            F=copies(r,unsat);n=f_name(F);m=len(F);b=ceil(log2(n+1));N=3*m*(b+1)
            qcap=max(1,int(N**.6));shallow=(qcap.bit_length()-1)
            bound_clauses=m-4*shallow
            h_leaf=(m-ceil(N**.5/(3*(b+1))))/4
            lowerq=2**max(0,ceil(h_leaf))
            asym.append({'case':('UNSAT_W1_plus_S15' if unsat else 'SAT_S15_product'),'copies':r,'n':n,'m':m,'fixed_width_bits_N':N,
                         'polynomial_q_bound':qcap,'max_short_leaf_depth':shallow,'guaranteed_unhit_clauses':max(0,bound_clauses),'guaranteed_direct_child_bits_lower':3*max(0,bound_clauses)*(b+1),
                         'child_sqrtN_budget':N**.5,'necessary_depth_for_all_short':max(0,ceil(h_leaf)),
                         'necessary_leaf_count_for_all_short':str(lowerq)})
    return {'report_id':'ARC-KRAFT-COFACTOR-COVER264','status':'COMPUTATIONAL / restricted theorem independently provable; P versus NP OPEN','no_randomness':True,
            'flmv_exact':fl,'cases':cases,'hostile_easy_controls':hostile,'scaled_family':asym,
            'scaled_combs':[{'name':'S15_product','copies':r,**comb_output(copies(r,False),q)} for r,q in [(2,8),(4,16),(16,64),(64,128)]],
            'selected_work_disclaimer':'Instrumented logical events only. Peak proxy is materialized residual bits, not exact FLMV high-water space.'}

if __name__=='__main__':
    args=argparse.ArgumentParser();args.add_argument('--output',default='arc_kraft_cofactor264_raw.json');ns=args.parse_args();res=runs()
    with open(ns.output,'w') as f:json.dump(res,f,indent=2)
    print(json.dumps({'status':'PASS','cases':[(x['name'],x['models'],x['baseline_dpll']['selected_work'],[(r['h'],r['observed']['selected_work']) for r in x['cofactor_partitions']]) for x in res['cases']], 'scaled':[(x['copies'],x['case'],x['guaranteed_direct_child_bits_lower'],round(x['child_sqrtN_budget'],2)) for x in res['scaled_family']][:8], 'flmv':[(x['c'],x['maximum'],x['max_k']) for x in res['flmv_exact']]},indent=2))
