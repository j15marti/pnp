#!/usr/bin/env python3
"""ARC branch/certificate mass gate: exact, explicitly restricted cofactor trees.
All published metrics are independently reproducible, no SAT oracle is used by controller.
"""
import json, math, itertools, collections, random, hashlib, pathlib
from fractions import Fraction

W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
SWAP6=list(W1);SWAP6[9]=(-5,6,-15);SWAP6[13]=(-3,-6,-15)

def orbit(k=7):
    assert k>=7 and k%2
    out=[]
    for i in range(k):
        for s in range(4):
            a=(i+1,k+((i+s)%k)+1,2*k+((i+2*s)%k)+1)
            out.append(tuple(v if s<2 else -v for v in a))
    return out

def xor_k4(odd=False):
    edges=list(itertools.combinations(range(4),2));F=[]
    for v in range(4):
        local=[i+1 for i,e in enumerate(edges) if v in e]
        b=(1 if odd and v==0 else 0)
        for bits in itertools.product((0,1),repeat=3):
            if sum(bits)%2 != b:
                F.append(tuple(x if val==0 else -x for x,val in zip(local,bits)))
    return F

def rename(F, seed=81):
    vs=sorted({abs(x) for c in F for x in c});r=random.Random(seed);p=vs[:];r.shuffle(p)
    trans=dict(zip(vs,p));switch={v:r.randrange(2) for v in vs}
    return [tuple((1 if x>0 else -1)*(-1 if switch[abs(x)] else 1)*trans[abs(x)] for x in c) for c in F]

def enc_bits(F, n=None):
    n=n or max((abs(x) for c in F for x in c),default=1)
    w=max(1,math.ceil(math.log2(n+1)))
    return 2*w+sum(3+len(c)*(w+1) for c in F)

def residual(F,a):
    return [tuple(l for l in c if abs(l) not in a) for c in F
      if not any(abs(l) in a and a[abs(l)]==int(l>0) for l in c)]

def clause_scan(F,a,C):
    """One source pass, counts every signed literal truth test in selected-event ledger."""
    rem=[];firstunit=None;falseidx=None
    # Indexed encoding width acquired by a paid complete initial scan on each visit.
    C['width_discovery_literal_reads']+=sum(len(c) for c in F)
    w=max(1,math.ceil(math.log2(max((abs(x) for cl in F for x in cl),default=1)+1)))
    for j,c in enumerate(F):
        C['clause_visits']+=1
        live=[];satisfied=False
        for l in c:
            C['literal_tests']+=1
            C['source_bit_reads']+=w+1
            if abs(l) in a:
                if a[abs(l)]==int(l>0):satisfied=True;break
            else:live.append(l)
        if satisfied:continue
        rem.append(j)
        if not live:
            falseidx=j;break
        if len(live)==1 and firstunit is None:firstunit=(j,live[0])
    return rem,firstunit,falseidx

def choose(F,rem,a,policy,C):
    vs=sorted({abs(l) for j in rem for l in F[j] if abs(l) not in a})
    if policy=='first':
        C['candidate_tests']+=1
        return vs[0]
    scores={v:0 for v in vs}
    for j in rem:
        for l in F[j]:
            C['candidate_tests']+=1
            if abs(l) in scores:scores[abs(l)]+=1
    if policy=='max':return min(vs,key=lambda v:(-scores[v],v))
    if policy=='min':return min(vs,key=lambda v:(scores[v],v))
    raise ValueError(policy)

def models(F,n,partial=None):
    partial=partial or {}
    free=[v for v in range(1,n+1) if v not in partial]
    count=0;witness=None
    for bits in itertools.product((0,1),repeat=len(free)):
        a=dict(partial);a.update(zip(free,bits))
        if all(any(a[abs(l)]==int(l>0) for l in c) for c in F):
            count+=1;witness=a if witness is None else witness
    return count,witness

def branch_partition(F,n,limit,policy='first',record_limit=40):
    C=collections.Counter(); leaves=[];snapshots=[];limit_nodes=500000
    def rec(a,history):
        C['visited_nodes']+=1
        if C['visited_nodes']>limit_nodes:raise ValueError('node cap')
        rem,unit,conflict=clause_scan(F,a,C)
        if conflict is not None:
            assert all(abs(l) in a and a[abs(l)]!=int(l>0) for l in F[conflict])
            leaves.append(dict(kind='P',depth=len(a),decisions=list(history),reason=conflict+1,vars=dict(a)))
            C['proof_checks']+=len(F[conflict]);return
        if unit is not None:
            j,l=unit;v=abs(l);b=int(l>0)
            assert v not in a
            bad=dict(a);bad[v]=1-b
            assert all(abs(z) in bad and bad[abs(z)]!=int(z>0) for z in F[j]);C['proof_checks']+=len(F[j]);C['unit_inferences']+=1
            leaves.append(dict(kind='P',depth=len(bad),decisions=list(history),reason=j+1,vars=bad))
            new=dict(a);new[v]=b
            rec(new,history+[('unit',v,b,j+1)])
            return
        m_res=len(rem)
        if len(snapshots)<record_limit:
            h=collections.Counter(len([l for l in F[j] if abs(l) not in a]) for j in rem)
            sats=sum(any(abs(l) in a and a[abs(l)]==int(l>0) for l in c) for c in F)
            sum_true=sum(sum(abs(l) in a and a[abs(l)]==int(l>0) for l in c) for c in F)
            omega=sum(max(0,sum(abs(l) in a and a[abs(l)]==int(l>0) for l in c)-1) for c in F)
            assert sats == sum_true-omega
            C['parameter_clause_reads']+=len(F)
            C['parameter_literal_reads']+=sum(len(c) for c in F)*3
            snapshots.append({'depth':len(a),'alive':m_res,'omega':omega,'satisfied':sats,'hist':dict(h),'history':history[-5:]})
        if not rem:
            leaves.append(dict(kind='S',depth=len(a),vars=dict(a),decisions=list(history)));return
        if m_res<=limit:
            C['emission_clause_reads']+=len(F)
            C['emission_literal_reads']+=sum(len(c) for c in F)
            R=residual(F,a)
            assert len(R)==m_res
            # source indexed literal list, no aux gadgets, and exact support of clauses
            C['child_literal_writes']+=sum(len(c) for c in R)
            C['child_clause_writes']+=len(R)
            C['physical_child_bits_written']+=enc_bits(R,n=n)
            leaves.append(dict(kind='E',depth=len(a),vars=dict(a),decisions=list(history),residual=[list(c) for c in R],residual_m=m_res,child_bits=enc_bits(R,n=n)))
            return
        v=choose(F,rem,a,policy,C)
        for b in (0,1):
            C['decision_edges']+=1
            nxt=dict(a);nxt[v]=b;rec(nxt,history+[('decision',v,b)])
    rec({},[])
    total=sum(1<<(n-e['depth']) for e in leaves)
    assert total==1<<n, ('Kraft failure',total,n)
    measure={kind:sum(1<<(n-e['depth']) for e in leaves if e['kind']==kind) for kind in ('P','S','E')}
    assert sum(measure.values())==1<<n
    tstar=max(0,math.ceil((len(F)-limit)/2)) if all(sum(abs(l)==v and int(l>0)==b for c in F for l in c)==2 for v in range(1,n+1) for b in (0,1)) else None
    if tstar is not None:
        assert all(e['depth']>=tstar for e in leaves if e['kind']=='E')
        assert measure['E'] <= len([e for e in leaves if e['kind']=='E'])*(1<<max(0,n-tstar))
        for e in leaves:
            if e['kind']=='E':
                sumtrue=sum(sum(abs(l) in e['vars'] and e['vars'][abs(l)]==int(l>0) for l in c) for c in F)
                omega=sum(max(0,sum(abs(l) in e['vars'] and e['vars'][abs(l)]==int(l>0) for l in c)-1) for c in F)
                assert len(F)-e['residual_m']==sumtrue-omega==2*e['depth']-omega
    positive=measure['S'];child_true=0;guest_events=0;guest_nodes=0
    # Ground-truth oracle, explicitly excluded from the production-controller cost.
    for e in leaves:
        if e['kind']=='E':
            t,_=models(F,n,e['vars']);child_true+=t
            ans,stats=dpll([tuple(z) for z in e['residual']],n)
            assert ans==(t>0)
            if ans:
                witness=dict(stats['witness']);witness.update(e['vars'])
                assert all(any(witness.get(abs(z),0)==int(z>0) for z in c) for c in F)
                C['witness_verification_literal_reads']+=sum(len(c) for c in F)
            guest_events+=stats['total_events'];guest_nodes+=stats['nodes']
    gt,_=models(F,n)
    assert positive+child_true==gt,('model count mismatch',positive,child_true,gt)
    q=sum(e['kind']=='E' for e in leaves)
    ledger={'nodes':C['visited_nodes'],'proof_leaves':sum(e['kind']=='P' for e in leaves),'sat_terminal_leaves':sum(e['kind']=='S' for e in leaves),'child_leaves':q,'total_leaves':len(leaves),'pruned_volume':measure['P'],'sat_terminal_volume':measure['S'],'child_volume':measure['E'],'cube_universe':1<<n,'min_child_depth':min([e['depth'] for e in leaves if e['kind']=='E'],default=None),'tstar':tstar,'oracle_model_count':gt,'child_model_count':child_true,'guest_nodes':guest_nodes,'guest_events':guest_events,'controller_selected_events':sum(C.values()),'combined_events':sum(C.values())+guest_events,'max_child_bits':max([e.get('child_bits',0) for e in leaves],default=0),'source_bits':enc_bits(F,n),'first_snapshots':snapshots,'counts':dict(C),'all_leaf_records':[{'kind':e['kind'],'depth':e['depth'],'vars':e['vars'],**({'reason':e['reason']} if e['kind']=='P' else {}),**({'residual':e['residual'],'child_bits':e['child_bits']} if e['kind']=='E' else {})} for e in leaves], 'peak_retained_leaf_records':sum(len(e.get('vars',{}))+len(e.get('decisions',[]))+len(e.get('residual',[]))+7 for e in leaves),'peak_stored_child_bits':sum(e.get('child_bits',0) for e in leaves),'proof_examples':[{'vars':e['vars'],'reason':e['reason'],'depth':e['depth']} for e in leaves if e['kind']=='P'][:10],'child_examples':[{'vars':e['vars'],'m':e['residual_m'],'child_bits':e['child_bits']} for e in leaves if e['kind']=='E'][:10]}
    return ledger

def dpll(F,n,pins=None):
    C=collections.Counter();pins=pins or {}
    witness=[None]
    def rec(a):
        C['nodes']+=1
        while True:
            rem,unit,conf=clause_scan(F,a,C)
            if conf is not None:return False
            if unit is None:break
            j,l=unit;a[abs(l)]=int(l>0);C['units']+=1
        if not rem:
            witness[0]={i:a.get(i,0) for i in range(1,n+1)}
            return True
        v=choose(F,rem,a,'first',C)
        for b in (0,1):
            C['decisions']+=1
            c=dict(a);c[v]=b
            if rec(c):return True
        return False
    out=rec(dict(pins));C['total_events']=sum(v for k,v in C.items() if k not in ('nodes','total_events'))
    stats=dict(C)
    if out:stats['witness']=witness[0]
    return out,stats

def original_audit(F,n):
    full3=all(len(c)==3 and len(set(abs(l) for l in c))==3 for c in F)
    if not full3:return {'applicable':False}
    targets=[];pairs=[]
    for j,c in enumerate(F,1):
        s={str(abs(l)):int(l>0) for l in c};u={x:1-b for x,b in s.items()}
        targets.append({'j':j,'signed_occurrences':[{'x':abs(l),'sign':1 if l>0 else -1,'S':int(l>0),'invert_S_to_U':int(l<0),'U':int(l<0),'invert_U_to_S':int(l>0)} for l in c], 'S':s,'not_S_is_U':u,'U':u,'not_U_is_S':s})
    for j in range(len(F)):
        for k in range(j+1,len(F)):
            shared=set(abs(x) for x in F[j])&set(abs(x) for x in F[k])
            same=any(next(x for x in F[j] if abs(x)==v)*next(x for x in F[k] if abs(x)==v)>0 for v in shared)
            opp=any(next(x for x in F[j] if abs(x)==v)*next(x for x in F[k] if abs(x)==v)<0 for v in shared)
            modes={'SS':not opp,'SU':not same,'US':not same,'UU':not opp}
            for A in (0,1):
                for B in (0,1):
                    targ={}
                    valid=True
                    for which,cl in ((A,F[j]),(B,F[k])):
                        for l in cl:
                            val=int(l>0) if which==1 else int(l<0)
                            if abs(l) in targ and targ[abs(l)]!=val:valid=False
                            targ[abs(l)]=val
                    assert valid==modes[('S' if A else 'U')+('S' if B else 'U')]
            pairs.append({'clauses':[j+1,k+1],'same':same,'opposite':opp,'SS_SU_US_UU':[int(modes[k]) for k in ('SS','SU','US','UU')]})
    def hist(a):
        counts=[sum(a[abs(l)]==int(l>0) for l in c) for c in F]
        return {'per_clause':counts,'N':[counts.count(r) for r in range(4)]}
    a={i:0 for i in range(1,n+1)};b={i:1 for i in range(1,n+1)}
    ha,hb=hist(a),hist(b)
    assert all(x+y==3 for x,y in zip(ha['per_clause'],hb['per_clause']))
    trail=[]
    for i in [1,2,3,5,7,11,13,15]:
        if i>n:continue
        a[i]^=1
        h=hist(a);inv=hist({v:1-z for v,z in a.items()})
        assert all(x+y==3 for x,y in zip(h['per_clause'],inv['per_clause']))
        trail.append({'flip':i,'statuses':h['N'],'complement_statuses':inv['N']})
    return {'applicable':True,'per_clause_targets':targets,'pair_matrix':pairs,'endpoints':{'zero':ha,'one':hb},'flip_trail':trail}

def main():
    cases={'W1_UNSAT':W1,'SWAP6_SAT':SWAP6,'W1_RENAMED_UNSAT':rename(W1,81),'SWAP6_RENAMED_SAT':rename(SWAP6,81),'XOR_K4_SAT':xor_k4(False),'XOR_K4_UNSAT':xor_k4(True),'HORN3_SAT':[(-1,-2,3),(-3,-4,5),(-5,-6,7)],'HORN_SHORT_UNSAT':[(1,),(-1,)],'ORBIT21_EASY_SAT':orbit(7)}
    result={'id':'ARC-BRANCH-MASS-GATE261','seed':81,'status':'exact restricted theorem; finite measurements only','sources':{},'tests':[]}
    for name,F in cases.items():
        n=max(abs(l) for c in F for l in c);audit=original_audit(F,n)
        if n>16:truth=None
        else:truth=models(F,n)[0]
        up,ud=dpll(F,n)
        if truth is not None:assert up==(truth>0)
        row={'n':n,'m':len(F),'source_bits':enc_bits(F,n),'source_clauses':[list(c) for c in F],'complete_model_count':truth,'DPLL_result':up,'DPLL':ud,'S_U':audit,'thresholds':{}}
        if n<=15:
            for cutoff in [0,4,8,12]:
                g=branch_partition(F,n,cutoff,'first')
                assert g['oracle_model_count']==truth
                row['thresholds'][str(cutoff)]=g
        else:
            witness={i:1 for i in range(1,8)}|{i:0 for i in range(8,22)}
            assert all(any(witness[abs(l)]==int(l>0) for l in c) for c in F)
            row['canonical_witness']=witness
            for cutoff in [24]:row['thresholds'][str(cutoff)]=branch_partition(F,n,cutoff,'first')
        result['sources'][name]=row
    # An additional exact test: all cube measures sum to 2^n, child-depth gate holds in regular sources.
    for name,row in result['sources'].items():
        for r,s in row['thresholds'].items():
            assert s['pruned_volume']+s['sat_terminal_volume']+s['child_volume']==s['cube_universe']
            if s['tstar'] is not None and s['child_leaves']:
                assert s['min_child_depth']>=s['tstar']
            result['tests'].append({'source':name,'cutoff':int(r),'total_nodes':s['nodes'],'q_children':s['child_leaves'],'tstar':s['tstar'],'pruned_fraction':str(Fraction(s['pruned_volume'],s['cube_universe'])),'terminal_sat_fraction':str(Fraction(s['sat_terminal_volume'],s['cube_universe'])),'child_fraction':str(Fraction(s['child_volume'],s['cube_universe'])),'total_events':s['combined_events'],'dpll_events':row['DPLL']['total_events']})
    P=pathlib.Path(__file__).with_name('raw.json');P.write_text(json.dumps(result,sort_keys=True,indent=2))
    s={'id':result['id'],'tests':result['tests'],'source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'raw_sha256':hashlib.sha256(P.read_bytes()).hexdigest()}
    pathlib.Path(__file__).with_name('summary.json').write_text(json.dumps(s,sort_keys=True,indent=2))
    print(json.dumps(s,indent=2))
if __name__=='__main__':main()
