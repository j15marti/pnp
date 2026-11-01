#!/usr/bin/env python3
"""Reproducible signed hypergraph + Gray binary state + certified controller audit.

PROVED/EXACT scope of assertions: fixed explicit source-indexed logical encoding;
correct source-indexed signed-spill/odd-cycle deductions; exact AND/OR resolution.
This does NOT implement a native FLMV time/space bound or a universal compressor.
"""
from __future__ import annotations
import argparse
import itertools
import json
from collections import Counter, defaultdict
from dataclasses import dataclass, field

POS15 = [
 (1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),
 (6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15),
]
NEG15 = [
 (1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),
 (4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15),
]
F15 = tuple(POS15 + [tuple(-x for x in c) for c in NEG15])
P6 = [(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
N6 = [(1,2,4),(1,3,6),(2,3,5),(4,5,6)]
Y6 = tuple(P6 + [tuple(-x for x in c) for c in N6])
P_U = dict(zip(range(7,16), (0,0,0,0,1,1,1,1,0)))
P_S = dict(zip(range(7,16), (1,0,0,0,1,1,1,1,0)))


def validate(clauses):
    if not clauses:
        return False
    counts = Counter()
    names = set()
    keys = []
    for c in clauses:
        if len(c)!=3 or any(x==0 for x in c) or len({abs(x) for x in c})!=3:
            return False
        if not (all(x>0 for x in c) or all(x<0 for x in c)):
            return False
        keys.append(tuple(sorted(c)))
        for x in c:
            names.add(abs(x))
            counts[abs(x), x>0]+=1
    return len(set(keys))==len(keys) and names==set(range(1,max(names)+1)) and all(counts[i,sgn]==2 for i in names for sgn in (True,False))


def truth_counts(c,p):
    true=sum((abs(l) in p and p[abs(l)]==int(l>0)) for l in c)
    unassigned=sum(abs(l) not in p for l in c)
    return true,unassigned


def sat(F,a):
    return all(any(a.get(abs(l))==int(l>0) for l in c) for c in F)


def models(F, pin=None):
    pin=pin or {}
    n=max(abs(x) for c in F for x in c)
    free=[x for x in range(1,n+1) if x not in pin]
    for bits in itertools.product((0,1),repeat=len(free)):
        a={**pin,**dict(zip(free,bits))}
        if sat(F,a):
            yield a


def encode_state(F,p,gray=True,verdict=True):
    n=max(abs(x) for c in F for x in c)
    out=0;shift=0
    def push(v):
        nonlocal out,shift
        out|=v<<shift
        shift+=2
    for v in range(1,n+1):
        push(0 if v not in p else (1 if p[v]==0 else 2))
    for c in F:
        t,u=truth_counts(c,p)
        push(t^(t>>1) if gray else t)
        push(u^(u>>1) if gray else u)
        if verdict:
            push(1 if t else (2 if not u else 0))
    return out,shift


def counts_incident(F,v,p):
    hu=ht=sigma=0
    before=encode_state(F,p,gray=True,verdict=True)[0]
    for bit in (0,1):
        q=dict(p);q[v]=bit
        after=encode_state(F,q,gray=True,verdict=True)[0]
        newstatus=0
        for c in F:
            a,b=truth_counts(c,p);z,w=truth_counts(c,q)
            if a==0 and b>0 and (z>0 or w==0):newstatus+=1
        assert (before^after).bit_count()==7+newstatus
        if bit==0: sigma=newstatus
    return sigma


def one_assignment_transition(F,p,v,bit,gray=True,verdict=True):
    a,L=encode_state(F,p,gray,verdict)
    q={**p,v:int(bit)}
    b,L2=encode_state(F,q,gray,verdict)
    assert L==L2
    decided=0;h_unassigned=0;h_true=0
    for c in F:
        t,u=truth_counts(c,p);t2,u2=truth_counts(c,q)
        if u2!=u:
            if u==2:h_unassigned+=1
            if t2==t+1 and t==1:h_true+=1
            if t==0 and u>0 and (t2>0 or u2==0):decided+=1
    d=(a^b).bit_count()
    if gray:assert d==7+(decided if verdict else 0)
    else:assert d==7+h_unassigned+h_true+(decided if verdict else 0)
    return q,d,decided


def trace(F,order,values,gray=True,verdict=True):
    p={};activity=0;record=[]
    prev, width=encode_state(F,p,gray,verdict)
    for v in order:
        p,d,decided=one_assignment_transition(F,p,v,values[v],gray,verdict)
        activity+=d
        record.append({'variable':v,'value':values[v],'d_logic':d,'new_clause_decisions':decided})
    end=encode_state(F,p,gray,verdict)[0]
    return {'n':len(order),'m':len(F),'gray':gray,'include_verdict':verdict,
            'sat':sat(F,p),'cumulative':activity,'endpoint':(prev^end).bit_count(),
            'width':width,'path':record}


def unlocked_clauses(F,p):
    return [(j,c) for j,c in enumerate(F) if not any(abs(l) in p and p[abs(l)]==int(l>0) for l in c)]


def triangle_packing(edges):
    # Source-indexed odd cycles. Triangles suffice for the chosen F15 controls;
    # omission of longer cycles weakens the bound, never creates false deductions.
    tris=[];tests=0
    for comb in itertools.combinations(range(len(edges)),3):
        tests+=1
        rows=[edges[i] for i in comb]
        if len({u for _,u,v in rows for u in (u,v)})!=3:continue
        degree=Counter(x for _,u,v in rows for x in (u,v))
        if set(degree.values())!={2}:continue
        tris.append(tuple(edges[i][0] for i in comb))
    # select maximum edge-disjoint triangle packing by exact backtracking
    # (expensive in general; costs explicitly reported).
    best=();search_nodes=0
    def rec(i,chosen,used):
        nonlocal best,search_nodes
        search_nodes+=1
        if i==len(tris):
            if len(chosen)>len(best):best=tuple(chosen)
            return
        if len(chosen)+len(tris)-i<=len(best):return
        t=tris[i]
        if not any(j in used for j in t): rec(i+1,chosen+[t],used|set(t))
        rec(i+1,chosen,used)
    rec(0,[],set())
    return best,{'triangle_candidate_tests':tests,'triangle_pack_nodes':search_nodes,'found_triangles':len(tris)}


def signed_spill_gate(F,p):
    clauses=unlocked_clauses(F,p)
    n=max(abs(x) for c in F for x in c)
    free=[x for x in range(1,n+1) if x not in p]
    covered={j for j in range(len(F))}-{j for j,_ in clauses}
    sat_occ=Counter()
    for j in covered:
        for l in F[j]:
            if abs(l) not in p:sat_occ[abs(l),l>0]+=1
    eta=sum(min(sat_occ[v,True],sat_occ[v,False]) for v in free)
    w={v:abs(sat_occ[v,True]-sat_occ[v,False]) for v in free}
    preferred={v:(0 if sat_occ[v,True]>sat_occ[v,False] else 1)
               for v in free if w[v]}
    edges=[]
    for j,c in clauses:
        rest=[abs(l) for l in c if abs(l) not in p]
        if len(rest)==2:edges.append((j,rest[0],rest[1]))
    pack,extra=triangle_packing(edges)
    nu=len(pack)
    e=2*len(free)-len(clauses)
    delta=e-eta-nu
    forcing={v:b for v,b in preferred.items() if w[v]>delta>=0}
    ret={'delta':delta,'e':e,'eta':eta,'nu':nu,'forced':forcing,
         'weights':{str(v):w[v] for v in free if w[v]},'packing':pack,
         'cost':{**extra,'original_clauses_scanned':len(F),
         'original_literals_inspected':3*len(F),'covered_occurrences':3*len(covered)}}
    return ret


def exact_one_affine(F,p,packing):
    # Preconditions: an authenticated signed-spill delta=0 gate.
    # All uncovered original clauses outside selected cycles must be exact-one.
    used={j for cyc in packing for j in cyc}
    rows=[];free=[v for v in range(1,max(abs(l) for c in F for l in c)+1) if v not in p]
    for j,c in unlocked_clauses(F,p):
        if j in used:continue
        mask=0;values=[]
        for l in c:
            if abs(l) not in p:
                mask^=(1<<(abs(l)-1));values.append(l)
        rhs=(1 if c[0]>0 else (len(values)-1)&1)
        rows.append([mask,rhs,{j}])
    basis={};row_visits=0;conflict=None
    for mask,rhs,proof in rows:
        while mask:
            row_visits+=1
            pivot=mask.bit_length()-1
            if pivot not in basis:
                basis[pivot]=(mask,rhs,set(proof));break
            bm,br,bp=basis[pivot]
            mask^=bm;rhs^=br;proof^=bp
        if mask==0 and rhs==1:
            conflict=sorted(proof);break
    forced={}
    if conflict is None:
        # reduced row echelon form to expose every directly forced bit
        rev=sorted(basis,reverse=False)
        for pvt in rev:
            mask,rhs,pr=basis[pvt]
            for higher in [i for i in basis if i>pvt and (mask>>i)&1]:
                bm,br,bp=basis[higher]
                mask^=bm;rhs^=br;pr^=bp
            basis[pvt]=(mask,rhs,pr)
        for pvt,(mask,rhs,pr) in basis.items():
            if mask.bit_count()==1:forced[pvt+1]=rhs
    return {'rows':len(rows),'row_xor_steps':row_visits,'contradiction_source_ids':conflict,
            'forced':forced,'provenance_rows':{str(k):sorted(r[2]) for k,r in basis.items()}}

@dataclass
class Ledger:
    solver:str
    nodes:int=0
    clause_scans:int=0
    literal_tests:int=0
    source_gate_scans:int=0
    triangle_tests:int=0
    triangle_search_nodes:int=0
    affine_rows:int=0
    affine_xors:int=0
    forced_assignments:int=0
    propagation_assignments:int=0
    policy_checks:int=0
    branch_edges:int=0
    proof_nodes:int=0
    logical_xor:int=0
    proof_records:list=field(default_factory=list)
    peak_assignment_bits:int=0
    def read(self,F,p):
        self.clause_scans+=len(F); self.literal_tests+=3*len(F)
        return [(j,)+truth_counts(c,p) for j,c in enumerate(F)]
    def assign(self,F,p,v,b,why):
        if v in p:
            assert p[v]==b
            return p
        q,d,_=one_assignment_transition(F,p,v,b)
        self.logical_xor+=d
        self.peak_assignment_bits=max(self.peak_assignment_bits,2*len(q))
        self.proof_records.append({'assigned':v,'value':b,'reason':why,'d_logic':d})
        return q


def simplify_units(F,p,ledger):
    p=dict(p)
    while True:
        ledger.policy_checks+=1
        todo=None
        for j,t,u in ledger.read(F,p):
            if t:continue
            if not u:
                return p,{'type':'UNSAT_EMPTY_CLAUSE','clause_id':j}
            if u==1:
                c=F[j];l=next(l for l in c if abs(l) not in p)
                todo=(abs(l), int(l>0),j);break
        if todo is None:return p,None
        v,b,j=todo
        if v not in p:
            ledger.propagation_assignments+=1
            p=ledger.assign(F,p,v,b,f'unit_clause_{j}')


def controller(F,p,ledger,gate=True,cap=20000):
    def go(p):
        ledger.nodes+=1;ledger.proof_nodes+=1
        if ledger.nodes>cap:return None
        p,terminal=simplify_units(F,p,ledger)
        if terminal:
            ledger.proof_records.append({'reason':'original_empty_clause_after_UP',
                'clause_id':terminal['clause_id'],'p':dict(p)})
            return False
        facts=ledger.read(F,p)
        if all(t>0 for _,t,u in facts):
            n0=max(abs(l) for c in F for l in c)
            witness={v:p.get(v,0) for v in range(1,n0+1)}
            ledger.clause_scans+=len(F);ledger.literal_tests+=3*len(F)
            assert sat(F,witness)
            ledger.proof_records.append({'reason':'checked_original_source_SAT_witness',
                'witness_bits':''.join(str(witness[v]) for v in range(1,n0+1))})
            return True
        if gate:
            ledger.policy_checks+=1
            ret=signed_spill_gate(F,p)
            ledger.source_gate_scans+=ret['cost']['original_literals_inspected']
            ledger.triangle_tests+=ret['cost']['triangle_candidate_tests']
            ledger.triangle_search_nodes+=ret['cost']['triangle_pack_nodes']
            if ret['delta']<0:
                ledger.proof_records.append({'reason':'signed_spill_negative','delta':ret['delta'],
                    'packing':ret['packing'],'p':dict(p)})
                return False
            combined_forced=dict(ret['forced'])
            if ret['delta']==0:
                aff=exact_one_affine(F,p,ret['packing'])
                ledger.affine_rows+=aff['rows'];ledger.affine_xors+=aff['row_xor_steps']
                if aff['contradiction_source_ids'] is not None:
                    ledger.proof_records.append({'reason':'signed_spill_affine_conflict',
                        'delta':0,'p':dict(p),'provenance':aff['contradiction_source_ids']})
                    return False
                for v,b in aff['forced'].items():
                    if v in combined_forced:assert combined_forced[v]==b
                    combined_forced[v]=b
            if combined_forced:
                for v,b in sorted(combined_forced.items()):
                    if v not in p:
                        ledger.forced_assignments+=1
                        p=ledger.assign(F,p,v,b,'signed_spill_or_affine_forced')
                return go(p)
        v=next(i for i in range(1,max(abs(l) for c in F for l in c)+1) if i not in p)
        for b in (0,1):
            ledger.branch_edges+=1
            q=ledger.assign(F,p,v,b,'decision')
            result=go(q)
            if result is True:return True
            if result is None:return None
        ledger.proof_records.append({'reason':'both_binary_branches_unsatisfiable','p':dict(p),'pivot':v})
        return False
    answer=go(p)
    return answer


def result_ledger(z):
    data={k:v for k,v in vars(z).items() if k!='proof_records'}
    data['proof_record_count']=len(z.proof_records)
    data['work_proxy']=z.literal_tests+z.source_gate_scans+z.triangle_tests+z.triangle_search_nodes+z.affine_xors+z.branch_edges
    data['proof_examples']=z.proof_records[:12]
    return data


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',default='/mnt/data/integrated_sat_wrapper_dag_results.json')
    args=p.parse_args()
    assert validate(Y6) and validate(F15)
    assert sum(1 for _ in models(Y6))==20
    assert sum(1 for _ in models(F15))==1032
    assert sum(1 for _ in models(F15,P_U))==0
    assert sum(1 for _ in models(F15,P_S))==2
    controls={}
    for name,F,pin in [('Y6',Y6,{}),('F15',F15,{}),('F15_UNSAT_CUBE',F15,P_U),('F15_SAT_CUBE',F15,P_S),('F15_AFFINE_UNSAT_CUBE',F15,{**P_U,6:0})]:
        baseline=Ledger('UP-DPLL')
        enhanced=Ledger('SIGNED_SPILL_XOR_DAG')
        b=controller(F,pin,baseline,gate=False)
        e=controller(F,pin,enhanced,gate=True)
        actual=next(models(F,pin),None) is not None
        assert b==e==actual,(name,b,e,actual)
        controls[name]={'ground_truth':'SAT' if actual else 'UNSAT',
                        'baseline':result_ledger(baseline),'enhanced':result_ledger(enhanced)}
        if pin:
            gate=signed_spill_gate(F,pin)
            controls[name]['root_gate']=gate
            if gate['delta']<0:assert not actual
            if gate['forced']:
                for a in models(F,pin):
                    assert all(a[v]==b for v,b in gate['forced'].items())
            if gate['delta']==0:
                aff=exact_one_affine(F,pin,gate['packing'])
                controls[name]['root_affine']=aff
                if aff['contradiction_source_ids'] is not None:assert not actual
                else:
                    for a in models(F,pin):
                        assert all(a[v]==b for v,b in aff['forced'].items())
    traces={}
    for name,F in [('Y6',Y6),('F15',F15)]:
        n=max(abs(l) for c in F for l in c)
        order=list(range(1,n+1))
        valuesSAT=next(models(F))
        valuesBAD={v:0 for v in order} # Unsatisfying for both canonical mixed-sign formulas
        assert not sat(F,valuesBAD)
        traces[name]={}
        for t,a in [('satisfying_assignment',valuesSAT),('nonsatisfying_assignment',valuesBAD)]:
            g=trace(F,order,a,gray=True,verdict=True)
            rev=trace(F,list(reversed(order)),a,gray=True,verdict=True)
            binary=trace(F,order,a,gray=False,verdict=True)
            assert g['cumulative']==rev['cumulative']==7*n+len(F)
            assert binary['cumulative']>=g['cumulative']
            traces[name][t]={
                'gray_total':g['cumulative'],'gray_reverse_total':rev['cumulative'],
                'binary_total':binary['cumulative'],'gray_endpoint':g['endpoint'],
                'binary_endpoint':binary['endpoint'],'gray_path':g['path'],
                'values':''.join(str(a[v]) for v in order)
            }
    result={'run':'INTEGRATED_SAT_WRAPPER_DAG1','status':'COMPUTATIONAL + restricted exact identities; P versus NP OPEN',
            'controls':controls,'traces':traces,
            'notes':{'native_FLVM':False,'physical_tape_XOR':False,'proof_DAG_simulated':True,
                     'restored_bits_charged_as_logical_XOR':False,
                     'source_scans_and_triangle_search_charged':'host-language operation proxies, not FLMV native steps',
                     'scope':'F15 opposite-labeled cubes share canonical source; gate partial labels are not canonical roots'}}
    with open(args.output,'w') as f:json.dump(result,f,indent=2)
    print(json.dumps({
        'models':{'Y6':20,'F15':1032,'F15_U_cube':0,'F15_S_cube':2},
        'controls':{k:{'label':v['ground_truth'],'base_nodes':v['baseline']['nodes'],
                       'gate_nodes':v['enhanced']['nodes'],'base_work':v['baseline']['work_proxy'],
                       'gate_work':v['enhanced']['work_proxy']} for k,v in controls.items()},
        'gray_totals':{k:{u:v['gray_total'] for u,v in z.items()} for k,z in traces.items()}},indent=2))

if __name__=='__main__':main()
