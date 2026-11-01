#!/usr/bin/env python3
"""ARC-PREFIX-AFFINE-CERT300. Source-authenticated rollback-GF2 certificate DAG.
Finite exhaustive controls and work proxies, NOT FLMV indexed-machine timings.
Deterministic, no random seed; standard-library only.
"""
from collections import Counter
from itertools import product,combinations
import json,math
from pathlib import Path

Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
F15_POS=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
F15_NEG=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=F15_POS+tuple(tuple(-x for x in c) for c in F15_NEG)
F9_POS=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
F9_NEG=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F9=F9_POS+tuple(tuple(-x for x in c) for c in F9_NEG)
F9_U={8:0,3:0,7:0,6:0,1:1,5:1}
F15_U=dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))
F15_S=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))


def grammar(F):
    if not F or not all(len(c)==3 for c in F):return False
    n=max(abs(x) for c in F for x in c)
    if n%3 or len(F)*3!=4*n:return False
    if len(set(tuple(sorted(c)) for c in F))!=len(F):return False
    counts=Counter((abs(l),l>0) for c in F for l in c)
    return all(len({abs(l) for l in c})==3 and
        (all(l>0 for l in c) or all(l<0 for l in c)) and
        all(1<=abs(l)<=n for l in c) for c in F) and all(
        counts[v,True]==counts[v,False]==2 for v in range(1,n+1))

def valid_pin(p,n):return all(type(v)==int and 1<=v<=n and type(a)==int and a in (0,1) for v,a in p.items())

def truth(F,a):return all(any(a[abs(l)]==int(l>0) for l in c) for c in F)

def extensions(F,p):
    n=max(abs(l) for c in F for l in c)
    free=[x for x in range(1,n+1) if x not in p]
    for vals in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,vals))}
        if truth(F,a):yield a

def target_gate(F,p):
    if not grammar(F):return {'status':'MALFORMED'}
    n=max(abs(x) for c in F for x in c)
    if not valid_pin(p,n):return {'status':'MALFORMED_PIN'}
    free=[v for v in range(1,n+1) if v not in p]
    uncovered=[];covered=[];literal_scans=0
    for j,c in enumerate(F):
        literal_scans+=len(c)
        if any(abs(l) in p and p[abs(l)]==int(l>0) for l in c):covered.append(j)
        else:uncovered.append(j)
    if any(all(abs(l) in p for l in F[j]) for j in uncovered):
        return {'status':'UNSAT_EMPTY','empty_original_clause_ids':[j for j in uncovered if all(abs(l) in p for l in F[j])], 'literal_scans':literal_scans}
    c=Counter()
    for j in covered:
        for l in F[j]:
            if abs(l) not in p:c[abs(l),l>0]+=1
    eta=sum(min(c[v,True],c[v,False]) for v in free)
    prefs={v:(0 if c[v,True]>c[v,False] else 1) for v in free if c[v,True]!=c[v,False]}
    edges=[(j,tuple(abs(l) for l in F[j] if abs(l) not in p)) for j in uncovered]
    edges=[(j,vs[0],vs[1]) for j,vs in edges if len(vs)==2]
    triangles=[];checks=0
    for comb in combinations(edges,3):
        checks+=1
        deg=Counter(v for _,a,b in comb for v in (a,b))
        if len(deg)==3 and all(v==2 for v in deg.values()):
            triangles.append(tuple(sorted(j for j,_,_ in comb)))
    used=set();cycles=[]
    for cyc in sorted(triangles):
        if not used.intersection(cyc):
            cycles.append(cyc);used.update(cyc)
    e=2*len(free)-len(uncovered)
    return {'status':'GATE','n':n,'free':free,'uncovered':uncovered,'covered':covered,
            'prefs':prefs,'eta':eta,'e':e,'nu':len(cycles),'delta':e-eta-len(cycles),
            'cycles':cycles,'literal_scans':literal_scans,'triangle_candidate_checks':checks,
            'triangle_hits':len(triangles)}

def row_desc(F,p,g):
    n=g['n'];r=[];cycle_edges={j for cyc in g['cycles'] for j in cyc}
    for j in g['uncovered']:
        if j in cycle_edges:continue
        free=[l for l in F[j] if abs(l) not in p]
        mask=sum(1<<(abs(l)-1) for l in free)
        # XOR of original-variable bits = odd literal parity.
        rhs=1^((len(free)&1) if F[j][0]<0 else 0)
        r.append((mask,rhs,('parity',j)))
    for v,b in sorted(g['prefs'].items()):r.append((1<<(v-1),b,('preference',v)))
    return r

def rows_for_choice(F,p,cyc,choice):
    r=[]
    for j in cyc:
        free=[abs(l) for l in F[j] if abs(l) not in p]
        assert len(free)==2
        if j==choice:
            val=int(F[j][0]>0)
            r.extend([(1<<(v-1),val,('cycle_both_true',j,v)) for v in free])
        else:
            r.append(((1<<(free[0]-1))^(1<<(free[1]-1)),1,('cycle_one_true',j)))
    return r

class RollbackGF2:
    def __init__(self,n):
        self.n=n;self.rows=[];self.basis={};self.history=[];self.counter=Counter();self.peak_bits=0
    def snapshot(self):return len(self.history)
    def add(self,row):
        mask,rhs,tag=row;idx=len(self.rows)
        self.rows.append(row);self.counter['rows_installed']+=1
        origmask=1<<idx;mat=mask
        while mat:
            self.counter['pivot_probes']+=1
            p=mat.bit_length()-1
            if p not in self.basis:
                self.basis[p]=(mat,rhs,origmask)
                self.history.append(p)
                self.counter['new_pivots']+=1
                self._peak();return None
            bm,br,bp=self.basis[p]
            mat^=bm;rhs^=br;origmask^=bp
            self.counter['row_xors']+=1
            self.counter['xor_bits_charged_proxy']+=max(1,bm.bit_length(),bp.bit_length())
        self.history.append(None)
        self._peak()
        if rhs:
            terms=[{'mask':m,'rhs':r,'tag':list(t)} for idx2,(m,r,t) in enumerate(self.rows) if (origmask>>idx2)&1]
            assert not (sum((x['rhs'] for x in terms))%2)==0
            xmask=0
            for x in terms:xmask^=x['mask']
            assert xmask==0
            self.counter['contradictions']+=1
            return terms
        return None
    def _peak(self):
        # Fixed-layout estimate for explicit basis rows and provenance bit vectors,
        # excludes source and guest, not native TM bit-level peak.
        R=len(self.rows);f=self.n
        self.peak_bits=max(self.peak_bits,len(self.basis)*(f+R+1)+R*(f+1))
    def undo(self,size):
        while len(self.history)>size:
            pivot=self.history.pop()
            if pivot is not None: del self.basis[pivot]
            self.rows.pop()
    def witness(self,p):
        bits=0
        for pivot in sorted(self.basis):
            mask,rhs,_=self.basis[pivot]
            bit=rhs ^ ((mask&bits).bit_count()&1)
            if bit:bits|=1<<pivot
        return {v:(p[v] if v in p else (bits>>(v-1))&1) for v in range(1,self.n+1)}
    def rank(self):return len(self.basis)

def source_cert(F,p,max_cases=250000):
    g=target_gate(F,p)
    if g['status']!='GATE':return {'label':'UNSAT' if g['status']=='UNSAT_EMPTY' else g['status'], 'gate':g}
    if g['delta']<0:return {'label':'UNSAT_GAP','gate':g,'proof':{'delta':g['delta']}}
    if g['delta']!=0:return {'label':'UNRESOLVED','gate':g}
    bound=math.prod(len(c) for c in g['cycles'])
    if bound>max_cases:return {'label':'UNRESOLVED_CAP','gate':g,'max_cases':max_cases}
    machine=RollbackGF2(g['n']);base=row_desc(F,p,g)
    for row in base:
        fail=machine.add(row)
        if fail is not None:
            return {'label':'UNSAT_AFFINE','gate':g,'branch_bound':bound,'prefix_nodes':0,
                    'contradictory_prefixes':1,'certificate':[{'choices':[], 'row_proof':fail}],
                    'proxy':dict(machine.counter),'peak_basis_bit_estimate':machine.peak_bits,
                    'model_count':0}
    cert=[];branches=0;prefix_nodes=0;models=0;one_witness=None
    def dfs(depth, choices):
        nonlocal branches,prefix_nodes,models,one_witness
        if depth==len(g['cycles']):
            branches+=1
            a=machine.witness(p)
            assert truth(F,a),('false SAT terminal',p,a,choices)
            # Soundness implies ALL affine solutions in this leaf satisfy F.
            total=1<<(len(g['free'])-machine.rank())
            models+=total
            if one_witness is None: one_witness=a
            return
        for choice in g['cycles'][depth]:
            prefix_nodes+=1
            before=machine.snapshot();fail=None
            for row in rows_for_choice(F,p,g['cycles'][depth],choice):
                fail=machine.add(row)
                if fail is not None:break
            if fail is not None:cert.append({'choices':list(choices)+[choice], 'row_proof':fail})
            else:dfs(depth+1,list(choices)+[choice])
            machine.undo(before)
    dfs(0,())
    assert models>=0
    return {'label':'SAT' if models else 'UNSAT_AFFINE','gate':g,'branch_bound':bound,
      'prefix_nodes':prefix_nodes,'consistent_leaves':branches,
      'contradictory_prefixes':len(cert),'certificate':cert,
      'proxy':dict(machine.counter),'peak_basis_bit_estimate':machine.peak_bits,
      'model_count':models,'witness':one_witness}

def disjoint_copy(F,offset):
    return tuple(tuple((1 if l>0 else -1)*(abs(l)+offset) for l in c) for c in F)

def baseline_dpll(F,p):
    n=max(abs(l) for c in F for l in c);count=Counter()
    def step(a):
        count['nodes']+=1;a=dict(a)
        while True:
            unit=None;live=[]
            for c in F:
                undec=[];sat=False
                for l in c:
                    count['literal_tests']+=1
                    if abs(l) not in a:undec.append(l)
                    elif a[abs(l)]==int(l>0):sat=True;break
                if sat:continue
                if not undec:return False
                live.append(undec)
                if len(undec)==1:unit=undec[0];break
            if unit is None:break
            v=abs(unit);bit=int(unit>0)
            if v in a and a[v]!=bit:return False
            a[v]=bit;count['units']+=1
        if not live:return True
        x=min(abs(l) for c in live for l in c)
        for bit in (0,1):
            if step({**a,x:bit}):return True
        return False
    verdict=step(p)
    return dict(count)|{'SAT':verdict}

def logical_state(F,a,gray=False):
    b=[a[i] for i in range(1,len(a)+1)]
    for c in F:
        t=sum(a[abs(l)]==int(l>0) for l in c)
        v=t^(t>>1) if gray else t
        b.extend([v&1,(v>>1)&1,int(t>0)])
    return tuple(b)

def controls(F):
    n=max(abs(l) for c in F for l in c)
    endpoints={}
    for b in (0,1):
        a={v:b for v in range(1,n+1)}
        hist=Counter(sum(a[abs(l)]==int(l>0) for l in c) for c in F)
        endpoints[str(b)]=[hist[i] for i in range(4)]
    compat=Counter();pair_checks=0
    for j,k in combinations(range(len(F)),2):
        jvars={abs(l):int(l>0) for l in F[j]}
        kvar={abs(l):int(l>0) for l in F[k]}
        commons=set(jvars)&set(kvar)
        opp=any(jvars[v]!=kvar[v] for v in commons)
        same=any(jvars[v]==kvar[v] for v in commons)
        mode=(int(not opp),int(not same),int(not same),int(not opp))
        compat[''.join(map(str,mode))]+=1
        # Independent truth table on union of two clause supports.
        names=sorted(set(jvars)|set(kvar))
        seen=set()
        for bits in product((0,1),repeat=len(names)):
            a=dict(zip(names,bits))
            s=sum(a[abs(l)]==int(l>0) for l in F[j]);t=sum(a[abs(l)]==int(l>0) for l in F[k])
            if s in (0,3) and t in (0,3):seen.add((s,t))
        assert mode==tuple(int(x in seen) for x in ((3,3),(3,0),(0,3),(0,0)))
        pair_checks+=4
    occurrence=[]
    for j,c in enumerate(F):
        for l in c:
            occurrence.append({'j':j,'literal':l,'S':int(l>0),'U':int(l<0),
                'invert_S_to_U':int(l<0),'invert_U_to_S':int(l>0)})
    trail=[];deltas=[];a={v:0 for v in range(1,n+1)}
    prev_b=logical_state(F,a);prev_g=logical_state(F,a,True)
    first_b=prev_b;first_g=prev_g
    for v in range(min(n,6)+1):
        if v:a[v]=1
        hist=Counter(sum(a[abs(l)]==int(l>0) for l in c) for c in F)
        trail.append({'flip':v,'counts':[hist[i] for i in range(4)]})
        cur_b=logical_state(F,a);cur_g=logical_state(F,a,True)
        deltas.append({'flip':v,'source_variable':v,
          'd_logic_binary':sum(x!=y for x,y in zip(prev_b,cur_b)),
          'd_logic_gray':sum(x!=y for x,y in zip(prev_g,cur_g)),
          'changed_original_clause_ids':[j for j,c in enumerate(F) if v>0 and any(abs(l)==v for l in c)]})
        prev_b=cur_b;prev_g=cur_g
    return {'original_occurrences':occurrence,'four_way_pair_extreme_matrix_count':dict(compat),
       'pair_truth_table_modes_checked':pair_checks, 'endpoints_0_1':endpoints,'flip_trail':trail,
       'xor_diagnostic':{'representation':'fixed aligned assignment bits and 2 count bits plus SAT bit per ORIGINAL clause',
          'binary_delta_sum':sum(x['d_logic_binary'] for x in deltas),
          'gray_delta_sum':sum(x['d_logic_gray'] for x in deltas),
          'binary_endpoint_delta':sum(x!=y for x,y in zip(first_b,prev_b)),
          'gray_endpoint_delta':sum(x!=y for x,y in zip(first_g,prev_g)),
          'steps':deltas,'mode':'OFFLINE; NOT native physical TM writes',
          'd_phys':'NOT_MEASURED_FLMV_TAPE_MODEL_NOT_IMPLEMENTED'}}

def main():
    rows={'run':'ARC_PREFIX_AFFINE_CERT300','mode':'source-authenticated incremental rollback Gaussian prefix certificate DAG',
      'canonical':['Y6','F9','F15'],'params':{'seed':None,'exhaustive':True},'cases':{},'controls':{}}
    for name,F in [('Y6',Y6),('F9',F9),('F15',F15)]:
        assert grammar(F)
        rows['controls'][name]=controls(F)
    malformed=[(),((1,1,2),),((1,2,3),(1,2,3)),((1,2,-3),),((1,2,3),)]
    assert all(source_cert(bad,{})['label']=='MALFORMED' for bad in malformed)
    rows['malformed_rejected']=len(malformed)
    instances=[];all_saturated_records=[]
    for name,F,bases in [('Y6',Y6,[{}]),('F9',F9,[F9_U]),('F15',F15,[F15_U,F15_S])]:
        results=Counter();details=[];sat0=unsat0=0;old_total=0;new_total=0
        for base in bases:
            free=[v for v in range(1,max(abs(l) for c in F for l in c)+1) if v not in base]
            for ss in product((-1,0,1),repeat=len(free)):
                p={**base,**{v:s for v,s in zip(free,ss) if s!=-1}}
                result=source_cert(F,p)
                label=bool(next(extensions(F,p),None))
                if result['label'] in ('SAT','UNSAT_AFFINE','UNSAT_GAP','UNSAT_EMPTY'):
                    assert (result['label']=='SAT')==label,(name,p,result)
                    if result['label']=='SAT':
                        assert result['model_count']==sum(1 for _ in extensions(F,p))
                    if result.get('gate',{}).get('delta')==0:
                        results['delta_zero_decided']+=1
                        if label:sat0+=1
                        else:unsat0+=1
                else:results['unresolved']+=1
                results[result['label']]+=1;results['cases']+=1
                if result.get('gate',{}).get('delta')==0:
                    # Immutable original-source branch certificate for independent verifier.
                    all_saturated_records.append({'source':name,'pins':p,
                        'gate':{'delta':result['gate']['delta'],'cycles':result['gate']['cycles'],
                                'prefs':result['gate']['prefs'],'uncovered':result['gate']['uncovered']},
                        'label':result['label'],'source_sat':label,
                        'model_count':result.get('model_count',0),
                        'certificate':result.get('certificate',[]),
                        'rank_of_consistent_leaves':result.get('proxy',{}).get('new_pivots',0)})
                    naive=baseline_dpll(F,p)
                    results['reference_dpll_nodes_sum']+=naive.get('nodes',0)
                    results['reference_dpll_literal_tests_sum']+=naive.get('literal_tests',0)
                    results['prefix_nodes_sum']+=result.get('prefix_nodes',0)
                    results['affine_row_xors_sum']+=result.get('proxy',{}).get('row_xors',0)
                    results['affine_row_installs_sum']+=result.get('proxy',{}).get('rows_installed',0)
                    results['triangle_candidate_checks_sum']+=result.get('gate',{}).get('triangle_candidate_checks',0)
                    if len(details)<4 or (not label and result.get('contradictory_prefixes',0)>0 and not any(z['label']=='UNSAT_AFFINE' for z in details)):
                        details.append({'partial':p,'label':result['label'],'source_sat':label,
                            'delta':result['gate']['delta'],'cycle_count':result['gate']['nu'],
                            'prefix_nodes':result.get('prefix_nodes'),'full_choice_count':result.get('branch_bound'),
                            'conflicts':result.get('contradictory_prefixes'),'models':result.get('model_count'),
                            'rank_proxy':result.get('proxy',{}).get('new_pivots'),
                            'proof_prefixes':[z['choices'] for z in result.get('certificate',[])][:30]})
        rows['cases'][name]={'summary':dict(results),'delta_zero_SAT':sat0,'delta_zero_UNSAT':unsat0,'examples':details}
    # Special F9 parity-only false positive with explicit three full contradictions
    f9=source_cert(F9,F9_U);assert f9['label']=='UNSAT_AFFINE';assert f9['gate']['delta']==0
    assert f9['gate']['cycles']==[(3,4,10)]
    assert len(f9['certificate'])==3 and f9['model_count']==0
    rows['F9_adversarial']={'pins':F9_U,'delta':f9['gate']['delta'],
       'cycle':f9['gate']['cycles'][0], 'proof_branches':f9['certificate'],
       'source_models':sum(1 for _ in extensions(F9,{})),
       'cube_models':sum(1 for _ in extensions(F9,F9_U)),
       'work_proxy':f9['proxy'],'peak_basis_bit_estimate':f9['peak_basis_bit_estimate']}
    # Same-source SAT and UNSAT delta-zero states in F15 are required.
    assert rows['cases']['F15']['delta_zero_SAT']>0 and rows['cases']['F15']['delta_zero_UNSAT']>0
    # Adversarial repeated canonical components test actual prefix cover/pruning.
    GG=F9+disjoint_copy(F9,9)
    pp={**F9_U,**{x+9:v for x,v in F9_U.items()}}
    repeated=source_cert(GG,pp)
    assert grammar(GG) and repeated['gate']['delta']==0 and repeated['gate']['nu']==2
    assert repeated['label']=='UNSAT_AFFINE' and repeated['branch_bound']==9
    assert repeated['prefix_nodes']==3 and len(repeated['certificate'])==3
    assert sum(1 for _ in extensions(GG,pp))==0
    rows['two_component_UNSAT_prefix_prune']={'n':18,'m':24,
       'nu':2,'full_potential_leaves':repeated['branch_bound'],
       'prefix_visited':repeated['prefix_nodes'],'conflict_prefixes':len(repeated['certificate']),
       'refutation_prefixes':[z['choices'] for z in repeated['certificate']],
       'models':repeated['model_count'], 'status':repeated['label']}
    HH=F15+disjoint_copy(F15,15)
    qq={**F15_S,**{x+15:v for x,v in F15_S.items()}}
    rep_sat=source_cert(HH,qq)
    assert grammar(HH) and rep_sat['gate']['delta']==0 and rep_sat['gate']['nu']==4
    assert rep_sat['label']=='SAT' and rep_sat['model_count']==4
    rows['two_component_SAT']={'n':30,'m':40,'nu':rep_sat['gate']['nu'],
       'full_potential_leaves':rep_sat['branch_bound'],
       'prefix_visited':rep_sat['prefix_nodes'],
       'consistent_leaves':rep_sat['consistent_leaves'],
       'models':rep_sat['model_count'], 'status':rep_sat['label']}
    records=Path(__file__).with_name('prefix_certificates300.jsonl')
    records.write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in all_saturated_records))
    rows['records']={'path':str(records),'count':len(all_saturated_records)}
    dest=Path(__file__).with_name('raw_prefix300.json');dest.write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'run':rows['run'],'F9':{'branch_refutations':len(f9['certificate']),'row_xors':f9['proxy'].get('row_xors')},'cases':{k:v['summary'] for k,v in rows['cases'].items()},'raw':str(dest)},indent=2))
if __name__=='__main__':main()
