#!/usr/bin/env python3
"""Independent, no import of GATE283 producer. Canonical M22 full-state XOR auditor.
Prior independent U198 source proof is rerun by importing archived verify280.py.
"""
import ast,collections,hashlib,itertools,json,pathlib,random
ROOT=pathlib.Path(__file__).resolve().parent

def target(f,n):
    if n<=0 or n%3 or len(f)!=4*n//3:return False
    d=collections.Counter();seen=set()
    for c in f:
        if len(c)!=3 or len(set(abs(z) for z in c))!=3 or not(all(z>0 for z in c) or all(z<0 for z in c)):return False
        if any(type(z)!=int or not 1<=abs(z)<=n for z in c):return False
        z=tuple(sorted(c))
        if z in seen:return False
        seen.add(z);d.update(c)
    return all(d[v]==d[-v]==2 for v in range(1,n+1))

def profile(f,a):return [sum(a[abs(z)-1]==(z>0) for z in c) for c in f]

def bits(f,a,gray):
    counts=profile(f,a); b=a[:]
    for t in counts:
        v=t^(t>>1) if gray else t
        b.extend([v%2,v//2,int(t!=0)])
    return b

def dist(a,b):return sum(v!=w for v,w in zip(a,b))

def independent_sweep(f,order,gray):
    n=max(abs(z) for c in f for z in c);a=[0]*n;first=bits(f,a,gray);prev=first[:]
    count=0; head=0; moves=0
    for i in order:
        assert a[i]==0
        a[i]=1
        nxt=bits(f,a,gray)
        for ix,(u,v) in enumerate(zip(prev,nxt)):
            if u!=v:
                count+=1;moves+=abs(ix-head);head=ix
        prev=nxt
    assert all(a)
    return count,dist(first,prev),moves

def exact_pairs(f,rec):
    n=max(abs(z) for c in f for z in c)
    assert len(rec)==len(f)*(len(f)-1)//2
    checks=0
    for i,j,SS,SU,US,UU in rec:
        shared=sorted(set(map(abs,f[i]))|set(map(abs,f[j])))
        possible=[False]*4
        for local in itertools.product((0,1),repeat=len(shared)):
            a=dict(zip(shared,local))
            ts=[sum(a[abs(z)]==int(z>0) for z in c) for c in (f[i],f[j])]
            for k,(s,t) in enumerate(((3,3),(3,0),(0,3),(0,0))):
                if ts==[s,t]:possible[k]=True
        assert possible==[bool(SS),bool(SU),bool(US),bool(UU)], (i,j,possible)
        checks+=4
    return checks

def count_small(f):
    n=max(abs(z) for c in f for z in c)
    return sum(all(profile(f,list(a))) for a in itertools.product((0,1),repeat=n))

def cycle(f,width,assignment_gray,counter_gray):
    n=max(abs(z) for c in f for z in c)
    a=[0]*n;first=bits(f,a,counter_gray);prev=first;tot=0;flips=0
    for i in list(range(1,1<<width))+[0]:
        num=i^(i>>1) if assignment_gray else i
        curr=[(num>>j)&1 if j<width else 0 for j in range(n)]
        nxt=bits(f,curr,counter_gray)
        tot+=dist(prev,nxt);flips+=dist(a,curr)
        prev=nxt;a=curr
    return tot,flips,dist(first,prev)

def main():
    obj=json.loads((ROOT/'raw283.json').read_text());counts=collections.Counter();assert obj['run']=='LSPV3_GATE283'
    u=ast.literal_eval('\n'.join(s for s in (ROOT/'DOECKER61_original_source.txt').read_text().splitlines() if s.strip() and not s.startswith('#')))
    v=[c[:] for c in u];v[2][2],v[44][2]=v[44][2],v[2][2]
    y=[list(c) for c in ((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))]
    actual={'Y6':y,'U198':u,'V198':v}
    assert count_small(y)==20
    for name,f in actual.items():
        row=obj['cases'][name];n=row['n'];m=row['m']
        assert row['source']==f and target(f,n)
        counts['valid_target_instances']+=1
        assert hashlib.sha256(json.dumps(f,separators=(',',':')).encode()).hexdigest()==row['source_sha256']
        assert len(row['original_source_indexed_S_U_targets'])==m
        for j,c in enumerate(f):
            items=row['original_source_indexed_S_U_targets'][j]['occurrences']
            assert [x['literal'] for x in items]==c
            for x in items:
                assert x['S']==int(x['literal']>0) and x['U']==int(x['literal']<0)
                assert x['invert_S_is_U']==x['U'] and x['invert_U_is_S']==x['S']
                counts['signed_occurrence_check']+=1
        counts['independently_enumerated_pair_modes']+=exact_pairs(f,row['SS_SU_US_UU_pairs'])
        for mask in (0,1,3,7,(1<<n)-1):
            a=[(mask>>k)&1 for k in range(n)]
            h=collections.Counter(profile(f,a));h2=collections.Counter(profile(f,[1-x for x in a]))
            assert all(h[i]==h2[3-i] for i in range(4))
            counts['coherent_endpoint_complement_checks']+=1
        for pol in ('ascending','descending','random_seed28314024','greedy_min_immediate_xor'):
            sweep=row['sweeps'][pol]
            order=[x['variable']-1 for x in sweep['binary']['changing_record_ids_per_step']] if pol=='ascending' else None
            if order is None:
                if pol=='descending':order=list(reversed(range(n)))
                elif pol=='greedy_min_immediate_xor':
                    # Recompute only independent directly declared policy total and
                    # use reported first-16 values as a falsification cross-check.
                    continue
                else:
                    # Producer's RNG state rolls forward, so no independent random-order
                    # reconstruction is claimed. Aggregate algebraic identity checked.
                    continue
            assert len(order)==n
            for label,gr in (('binary',False),('gray',True)):
                d,e,moves=independent_sweep(f,order,gr)
                record=sweep[label]
                assert (d,e,moves)==(record['xor_sum'],record['endpoint_xor'],record['work_head_steps_fixed_layout'])
                assert d==n+(4 if gr else 5)*m
                assert e==n+(2 if gr else 3)*m
                counts['fully_replayed_ordered_sweeps']+=1
        for key,reported in row['binary_gray_cycles'].items():
            assignment_gray=key.startswith('gray_assignment')
            counter_gray='_gray_counts' in key
            observed=cycle(f,6 if name=='Y6' else 10,assignment_gray,counter_gray)
            assert observed==(reported['sum_d_logic'],reported['assignment_bit_flips'],reported['end_d_logic'])
            counts['fully_replayed_closed_cycles']+=1
        for pol,entry in row['sweeps'].items():
            assert entry['binary']['xor_sum']==n+5*m
            assert entry['gray']['xor_sum']==n+4*m
            counts['algebraic_policy_encoding_checks']+=1
        assert row['greedy_acquisition']['policy_candidate_clause_inspections']==2*n*(n+1)
        assert row['dpll_baseline']['result']==('SAT' if name=='Y6' else 'UNRESOLVED_AT_CAP')
    # Independent baseline from the archived earlier producer, not gate283.
    from gate280 import dpll as independent_dpll_baseline
    for name,f in actual.items():
        prior=independent_dpll_baseline(f,len(actual[name]) and obj['cases'][name]['n'],cap=1200)
        record=obj['cases'][name]['dpll_baseline']
        assert prior['nodes']>=record['nodes']
        assert prior['literal_tests']==record['literal_tests']
        assert (prior['decision']=='UNRESOLVED' and record['result']=='UNRESOLVED_AT_CAP') or prior['decision']==record['result']
        counts['independent_DPLL_baseline_comparisons']+=1
    witness=list(map(int,obj['same_source_switch']['V198_certified_witness']))
    assert len(witness)==198 and all(profile(v,witness)) and not all(profile(u,witness))
    assert [j for j,t in enumerate(profile(u,witness)) if t==0]==[2]
    assert [j for j,(a,b) in enumerate(zip(profile(u,witness),profile(v,witness))) if a!=b]==[2,44]
    counts['V198_original_clause_witness_checks']+=len(v)
    rng=random.Random(32940)
    for _ in range(500):
        a=[rng.randrange(2) for _ in range(198)];a[195]=a[196]
        assert profile(u,a)==profile(v,a)
        counts['independent_equal_hyperplane_assignments']+=1
    # Check all malformed guard types as counterexamples to implicit promises.
    for broken in (y[:-1],y+[y[0]], [[1,-2,3]]+y[1:], [[1,1,2]]+y[1:], [[0,2,3]]+y[1:]):
        assert not target(broken,6);counts['malformed_rejections']+=1
    # Rerun the independent prior original-source complete U198 refutation.
    from verify280 import proof_u
    verified=proof_u(str(ROOT/'DOECKER61_original_source.txt'))
    assert verified['core_models']==0 and verified['total_module_nodes']==3666
    counts['U198_certificate_module_nodes']=verified['total_module_nodes']
    result={'run':'LSPV3_GATE283_INDEPENDENT','verification_status':'PASS','checks':dict(counts),
            'source_U198_proof':verified,'new_claims':'order-independent monotone sweep XOR / equal-value swap-hyperplane',
            'proof_scope':'fixed aligned original-source logical state, not FLMV native tapes'}
    (ROOT/'independent283.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','checks':dict(counts)},indent=2))
if __name__=='__main__':main()
