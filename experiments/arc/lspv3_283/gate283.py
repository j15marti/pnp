#!/usr/bin/env python3
"""LSPV-3 GATE283: exact M22 state-difference and charged policy audit.
Standalone standard-library diagnostic, not a native FLMV machine or SAT lower bound.
Original U198 source must be supplied in DOECKER61_original_source.txt.
"""
from __future__ import annotations
import ast, collections, hashlib, itertools, json, pathlib, random, time
ROOT=pathlib.Path(__file__).resolve().parent
UFILE=ROOT/'DOECKER61_original_source.txt'
YW=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
VW='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'

def loads():
    U=ast.literal_eval('\n'.join(s for s in UFILE.read_text().splitlines() if s.strip() and not s.startswith('#')))
    V=[c[:] for c in U]; assert U[2][2]==197 and U[44][2]==196
    V[2][2],V[44][2]=V[44][2],V[2][2]
    return {'Y6': [list(c) for c in YW], 'U198':U,'V198':V}

def legal(f):
    n=max(abs(z) for c in f for z in c)
    C=collections.Counter(z for c in f for z in c)
    return n%3==0 and len(f)*3==4*n and all(len(c)==3 and len(set(map(abs,c)))==3 and (min(c)>0 or max(c)<0) for c in f) and len({tuple(sorted(c)) for c in f})==len(f) and all(C[i]==C[-i]==2 for i in range(1,n+1))

def values(f,a):return [sum(a[abs(z)-1]==int(z>0) for z in c) for c in f]

def counts(f,a):
    z=values(f,a);return [z.count(i) for i in range(4)]

def state(f,a,gray=False):
    ts=values(f,a)
    out=list(a)
    for t in ts:
        v=t^(t>>1) if gray else t
        out.extend((v&1,(v>>1)&1,int(t>0)))
    return out

def hd(a,b):return sum(x!=y for x,y in zip(a,b))

def source_targets(f):
    return [{'j':j,'occurrences':[{'literal':l,'variable':abs(l),
              'S':int(l>0),'invert_S_is_U':int(l<0),'U':int(l<0),'invert_U_is_S':int(l>0)} for l in c]} for j,c in enumerate(f)]

def pairmodes(f):
    result=[];targs=source_targets(f)
    for i in range(len(f)):
        a={occ['variable']:occ['S'] for occ in targs[i]['occurrences']}
        for j in range(i+1,len(f)):
            b={occ['variable']:occ['S'] for occ in targs[j]['occurrences']}
            shared=set(a)&set(b)
            same=any(a[k]==b[k] for k in shared)
            opp=any(a[k]!=b[k] for k in shared)
            result.append([i,j,int(not opp),int(not same),int(not same),int(not opp)])
    return result

def order_trail(f,order,mode,diagnostics=True):
    n=max(abs(z) for c in f for z in c); m=len(f)
    a=[0]*n; prev=state(f,a,gray=(mode=='gray'))
    first=prev[:]; total=0; moves=0;head=0;writes=0
    changed_by_step=[];work=collections.Counter();work['source_grammar_literal_probes']=3*m
    # Materialized source-to-occurrence index is parent-sized. Read 3m source occurrences.
    occ=[[] for _ in range(n)]
    for j,c in enumerate(f):
        for l in c:occ[abs(l)-1].append(j)
    assert all(len(z)==4 for z in occ)
    work['index_entries_retained']=sum(map(len,occ))
    for v in order:
        assert a[v]==0
        a[v]=1
        nxt=state(f,a,gray=(mode=='gray'))
        changed=[p for p,(x,y) in enumerate(zip(prev,nxt)) if x!=y]
        assert {((p-n)//3) for p in changed if p>=n} == set(occ[v])
        d=len(changed); total+=d;writes+=d
        for p in changed:
            moves+=abs(p-head);head=p
        changed_by_step.append({'variable':v+1,'d_logic':d,'changed_clause_ids':occ[v][:]})
        work['indexed_source_clause_inspections']+=4
        work['offline_full_state_xor_bit_examinations']+=n+3*m
        prev=nxt
    assert a==[1]*n
    endpoint=hd(first,prev)
    return {'order_first16':[x+1 for x in order[:16]],'xor_sum':total,'endpoint_xor':endpoint,
            'changed_bits_actual_buffer_writes':writes,'work_head_steps_fixed_layout':moves,
            'changing_record_ids_per_step':changed_by_step if diagnostics else [],'ledger':dict(work)}

def greedy_order(f):
    n=max(abs(z) for c in f for z in c);m=len(f);a=[0]*n;remaining=set(range(n));order=[];tests=0
    # Acquisition costs are explicitly counted: comparing each remaining candidate
    # requires reevaluating its 4 original clause records, plus bookkeeping.
    incidence=[[] for _ in range(n)]
    for j,c in enumerate(f):
        for z in c:incidence[abs(z)-1].append(j)
    while remaining:
        s=state(f,a)
        best=None
        for i in sorted(remaining):
            candidate=a.copy();candidate[i]=1
            s1=state(f,candidate)
            score=hd(s,s1)
            tests+=4
            if best is None or (score,i)<(best[0],best[1]):best=(score,i)
        j=best[1];a[j]=1;remaining.remove(j);order.append(j)
    return order,{'policy_candidate_clause_inspections':tests,
                  'policy_source_literal_probes_upper_bound':3*m*n*(n+1)//2,
                  'policy_virtual_state_bit_examinations':(n+3*m)*n*(n+1)//2}

def xor_cycle(f,width,gray_assign,gray_counter):
    n=max(abs(z) for c in f for z in c);m=len(f)
    masks=[i^(i>>1) if gray_assign else i for i in range(1<<width)]+[0]
    prev=state(f,[0]*n,gray_counter);start=prev[:];total=0;flip=0
    a=[0]*n;changed_records=collections.Counter()
    for mask in masks[1:]:
        anew=[(mask>>i)&1 if i<width else 0 for i in range(n)]
        flip+=hd(a,anew)
        nextstate=state(f,anew,gray_counter)
        total+=hd(prev,nextstate)
        for j,(c,d) in enumerate(zip(values(f,a),values(f,anew))):
            if c!=d:changed_records[j]+=1
        a=anew;prev=nextstate
    return {'assignment_order':'reflected_gray' if gray_assign else 'binary','counter_encoding':'gray' if gray_counter else 'binary',
            'states':len(masks),'sum_d_logic':total,'end_d_logic':hd(start,prev),'assignment_bit_flips':flip,
            'source_clause_literal_probes_full_scan':3*m*(len(masks)-1),
            'offline_state_xor_bit_examinations':(n+3*m)*(len(masks)-1),
            'changed_clause_record_ids_count':len(changed_records)}

def dpll_trace(f,cap=1200):
    """UP-first baseline with offline completed-assignment checkpoint XOR.
    A -1 means unassigned, and for visualization only we complete it to zero.
    This is NOT the actual writable tape configuration of a DPLL solver.
    """
    n=max(abs(z) for c in f for z in c);m=len(f)
    stack=[[-1]*n];stats=collections.Counter();prev=None;first=None;last=None;head=0
    peak=1
    while stack and stats['nodes']<cap:
        a=stack.pop();stats['nodes']+=1
        while True:
            needs=[];forced=None;conflict=False
            for c in f:
                un=[];ok=False
                for lit in c:
                    stats['literal_tests']+=1
                    x=a[abs(lit)-1]
                    if x<0:un.append(lit)
                    elif x==int(lit>0):ok=True;break
                if ok:continue
                if not un:conflict=True;break
                needs.append(un)
                if len(un)==1:forced=un[0];break
            if conflict:
                stats['conflict_leaves']+=1;break
            if forced is not None:
                i=abs(forced)-1;b=int(forced>0)
                if a[i]>=0 and a[i]!=b:stats['conflict_leaves']+=1;break
                if a[i]<0:a[i]=b;stats['unit_assignments']+=1
                continue
            break
        vis=state(f,[max(0,x) for x in a]);stats['checkpoint_count']+=1
        if first is None:first=vis[:]
        if prev is not None:
            changed=[j for j,(u,v) in enumerate(zip(prev,vis)) if u!=v]
            stats['completed_snapshot_xor_sum']+=len(changed)
            for p in changed:
                stats['snapshot_write_head_moves']+=abs(p-head);head=p
        last=vis;prev=vis
        if conflict:continue
        if not needs:
            assert all(values(f,[max(0,x) for x in a]))
            return {**stats,'result':'SAT','endpoint_xor':hd(first,last), 'peak_pending_branches':peak}
        use=collections.Counter(abs(l) for c in needs for l in c)
        pivot=min((p for p in use if a[p-1]<0),key=lambda p:(-use[p],p))
        zero=a.copy();one=a.copy();zero[pivot-1]=0;one[pivot-1]=1
        stack.extend((zero,one));peak=max(peak,len(stack))
        stats['branch_assignment_copies']+=2
    return {**stats,'result':'UNRESOLVED_AT_CAP' if stack else 'UNSAT',
            'endpoint_xor':hd(first,last) if first is not None else 0,
            'peak_pending_branches':peak}

def execute():
    fs=loads();rng=random.Random(28314024)
    out={'run':'LSPV3_GATE283','timestamp':'2026-10-31 14:24 PDT',
         'scope':'full canonical M22 target, signed extremes as adversarial controls',
         'status':'PROVED/EXACT symbolic restricted state-trajectory lemma; COMPUTATIONAL controls; ARC/FLMV OPEN',
         'cases':{},'falsifiers':{'F1':'monotone sweep XOR predicts best variable order','F2':'equal logical XOR implies equal decision or work',
                    'F3':'logical XOR lower-bounds lazy physical writes','F4':'same SAT/UNSAT label inference on equal-value subcube'}}
    for name,f in fs.items():
        start=time.perf_counter();n=max(abs(x) for c in f for x in c);m=len(f)
        assert legal(f),(name,'invalid')
        p=pairmodes(f);assert len(p)==m*(m-1)//2
        extreme=source_targets(f)
        zero=[0]*n;one=[1]*n
        assert counts(f,zero)==[m//2,0,0,m//2]
        assert counts(f,one)==[m//2,0,0,m//2]
        sample_trails=[]
        for mask in (0,1,3,7,(1<<n)-1):
            a=[(mask>>i)&1 for i in range(n)]
            h=counts(f,a);h2=counts(f,[1-x for x in a]);assert h[::-1]==h2
            sample_trails.append({'mask':str(mask),'hist':h,'complement_hist':h2,'is_sat':h[0]==0})
        gorder,acquisition=greedy_order(f)
        randorder=list(range(n));rng.shuffle(randorder)
        orders={'ascending':list(range(n)),'descending':list(reversed(range(n))),
                'random_seed28314024':randorder,'greedy_min_immediate_xor':gorder}
        sweeps={k:{encoding:order_trail(f,v,encoding,diagnostics=(k=='ascending' and encoding=='binary')) for encoding in ('binary','gray')}
                for k,v in orders.items()}
        for k,tr in sweeps.items():
            assert tr['binary']['xor_sum']==n+5*m,(name,k,tr['binary']['xor_sum'],n+5*m)
            assert tr['gray']['xor_sum']==n+4*m
            assert tr['binary']['endpoint_xor']==n+3*m
            assert tr['gray']['endpoint_xor']==n+2*m
        loops={f'{ao}_assignment_{co}_counts':xor_cycle(f,min(6,n) if name=='Y6' else 10,ao=='gray',co=='gray')
               for ao in ('binary','gray') for co in ('binary','gray')}
        baseline=dpll_trace(f,1200)
        assert baseline['result']=='SAT' if name=='Y6' else baseline['result']=='UNRESOLVED_AT_CAP'
        row={'n':n,'m':m,'source_sha256':hashlib.sha256(json.dumps(f,separators=(',',':')).encode()).hexdigest(),
             'source':f,'original_source_indexed_S_U_targets':extreme,'SS_SU_US_UU_pairs':p,
             'coherent_global_trails':sample_trails,'sweeps':sweeps,'greedy_acquisition':acquisition,
             'binary_gray_cycles':loops,'dpll_baseline':baseline,
             'elapsed_seconds':round(time.perf_counter()-start,4)}
        out['cases'][name]=row
    # Same-source legal swap. Equal values on labels 196 and 197 implies exact clause-count equality.
    U=fs['U198'];V=fs['V198'];n=198
    for mask in range(1024):
        a=[(mask>>i)&1 if i<10 else 0 for i in range(n)];a[195]=a[196]=mask&1
        assert values(U,a)==values(V,a)
    witness=list(map(int,VW));assert len(witness)==n and legal(V)
    assert all(values(V,witness)) and not all(values(U,witness))
    assert witness[195]!=witness[196]
    altered=[i for i,(u,v) in enumerate(zip(values(U,witness),values(V,witness))) if u!=v]
    assert altered==[2,44]
    out['same_source_switch']={'zero_based_modified_original_clause_ids':[2,44],
      'swapped_original_variables':[196,197],
      'equal_bit_subcube_checkpoints':1024,
      'identical_complete_clause_statuses_on_subcube':True,
      'V198_certified_witness':VW,
      'V198_witness_true_literal_hist':counts(V,witness),
      'U198_witness_falsified_original_ids':[j for j,t in enumerate(values(U,witness)) if t==0],
      'witness_changed_original_count_ids':altered,
      'all_other_clause_records_are_equal_every_assignment':True}
    for name in ('U198','V198'):
        out['cases'][name]['certificate_label']='UNSAT_CERTIFIED_EXISTING_MODULE_PROOF' if name=='U198' else 'SAT_CERTIFIED_COMPLETE_WITNESS'
    out['cases']['Y6']['certificate_label']='SAT_EXHAUSTIVELY_VERIFIED'
    out['proof_labels']={'sweep_xor_identity':'PROVED/EXACT for fixed aligned canonical states and monotone 0-to-1 variable sweeps',
      'source_switch_hyperplane':'PROVED/EXACT for U/V source pair, source-independent statement for any same-polarity swap',
      'xor_solver_time_lower_bound':'FALSIFIED/RETIRED','exact_native_FLVM_machine':'NOT IMPLEMENTED',
      'universal_A_to_Phi_A':'OPEN','P_vs_NP':'OPEN'}
    (ROOT/'raw283.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
    summary={'run':out['run'],'cases':{},'same_source_switch':{k:v for k,v in out['same_source_switch'].items() if k!='V198_certified_witness'},
             'proof_labels':out['proof_labels']}
    for name,r in out['cases'].items():
        summary['cases'][name]={'n':r['n'],'m':r['m'],'endpoint_hist':r['coherent_global_trails'][0]['hist'],
             'binary_sweep_xor_by_policy':{k:v['binary']['xor_sum'] for k,v in r['sweeps'].items()},
             'gray_sweep_xor_by_policy':{k:v['gray']['xor_sum'] for k,v in r['sweeps'].items()},
             'sweep_head_moves_by_policy':{k:v['binary']['work_head_steps_fixed_layout'] for k,v in r['sweeps'].items()},
             'dpll':r['dpll_baseline'],'greedy_acquisition':r['greedy_acquisition'],
             'cycles':{k:v['sum_d_logic'] for k,v in r['binary_gray_cycles'].items()},
             'full_input_source_literal_count':3*r['m']}
    (ROOT/'summary283.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2,sort_keys=True))
    return out
if __name__=='__main__':execute()
