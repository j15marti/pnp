#!/usr/bin/env python3
"""LSPV-3 SOURCE-DELTA-PROOF270: independent-source paired longitudinal SAT/UNSAT test.
Deterministic, offline experimental environment. No claim of native FLMV bounds.
"""
import json, hashlib, itertools, sys, time, tracemalloc
from pathlib import Path

HERE=Path(__file__).resolve().parent

def satisfied_clause(c,a):
    return any((a[abs(l)] == (l>0)) for l in c)

def true_count(c,a):
    return sum(a[abs(l)] == (l>0) for l in c)

def sat_source(src,rho,n,a):
    return all(a.get(k,-1)==v for k,v in rho.items()) and all(satisfied_clause(c,a) for c in src.values())

def cost_source(src):
    return sum(1+len(c) for c in src.values())

def up(src,a,counter):
    b=dict(a); trail=[]
    while True:
        unit=None
        for cid,c in src.items():
            counter[0]+=1
            true=False; open_l=[]
            for l in c:
                counter[0]+=1
                v=b.get(abs(l))
                if v is None: open_l.append(l)
                elif v==(l>0):true=True; break
            if true:continue
            if not open_l:
                return b, trail, cid
            if len(open_l)==1:
                unit=(cid,open_l[0]);break
        if unit is None:return b,trail,None
        cid,l=unit
        b[abs(l)]=int(l>0)
        trail.append((cid,l));counter[0]+=2

def dpll(src,rho,n,counter):
    nodes=[0]
    def go(a):
        nodes[0]+=1; counter[0]+=1
        b,steps,conflict=up(src,a,counter)
        if conflict is not None:
            return None, {'type':'conflict','steps':steps,'cid':conflict}
        if all(satisfied_clause(c,{i:b.get(i,0) for i in range(1,n+1)}) for c in src.values()):
            complete={i:b.get(i,0) for i in range(1,n+1)}
            # Must not confuse a not-yet-assigned literal with permanent FALSE
            if sat_source(src,rho,n,complete):
                return complete, {'type':'sat','steps':steps,'witness':complete}
        x=next((i for i in range(1,n+1) if i not in b),None)
        if x is None:
            # Cannot happen if propagate correctly; a full contradictory source would conflict.
            raise AssertionError('full-assignment conflict not detected')
        no, p0=go({**b,x:0})
        if no is not None:return no,{'type':'sat','steps':steps,'witness':no}
        yes, p1=go({**b,x:1})
        if yes is not None:return yes,{'type':'sat','steps':steps,'witness':yes}
        return None, {'type':'branch','steps':steps,'var':x,'lo':p0,'hi':p1}
    answer, tree=go(dict(rho))
    return answer, tree, nodes[0]

def deps(tree):
    r=set()
    def visit(t):
        for cid,l in t.get('steps',[]):r.add(int(cid))
        if t['type']=='conflict':r.add(int(t['cid']))
        if t['type']=='branch':visit(t['lo']);visit(t['hi'])
    visit(tree)
    return r

def valid_rho_extension(old,new):
    return all(new.get(int(k))==v for k,v in old.items())

def complement_diag(src,n):
    clauses=list(src.items()); all0={i:0 for i in range(1,n+1)};all1={i:1 for i in range(1,n+1)}
    # Original occurrence extreme targets for width <=3.
    extrema=[];pairs=[]
    for cid,c in clauses:
        S={str(abs(l)):int(l>0) for l in c};U={str(abs(l)):int(l<0) for l in c}
        assert {k:1-v for k,v in S.items()}==U
        extrema.append({'cid':cid,'signed_occurrences':list(c),'S':S,'invert_S_to_U':U,'U':U,'invert_U_to_S':S})
    for ii,(ci,a) in enumerate(clauses):
        for cj,b in clauses[ii+1:]:
            A={abs(l):1 if l>0 else 0 for l in a};B={abs(l):1 if l>0 else 0 for l in b}
            same=any(A[v]==B[v] for v in A.keys()&B.keys())
            opp=any(A[v]!=B[v] for v in A.keys()&B.keys())
            pairs.append({'i':ci,'j':cj,'SS':not opp,'SU':not same,'US':not same,'UU':not opp})
    def cats(a):
        t=[true_count(c,a) for _,c in clauses]; return {'counts':t,'N':[t.count(i) for i in range(4)],'satisfied':all(v>0 for v in t)}
    trails=[]
    a=dict(all0)
    for i in range(0,min(n,12)+1):
        trails.append({'flip_prefix':i,'status':cats(a)})
        if i<n:a[i+1]=1
    # Gray-code partial prefixes, n<=12 only for finite audit not online exhaustive solver
    gray=[]
    for g in range(min(1<<min(n,8),256)):
        v=g^(g>>1);a={i:int(bool(v&(1<<(i-1)))) for i in range(1,n+1)}
        gray.append([g,v,cats(a)['N']])
    return {'endpoint0':cats(all0),'endpoint1':cats(all1),'extrema':extrema,'modes':pairs,'prefix_flips':trails,'gray_layers':gray}

def physical_cache_bits(entries):
    # Conservative explicit text-bit storage upper envelope, not Python peak.
    return 8*len(json.dumps(entries,separators=(',',':'),sort_keys=True))

def source_version(src,n,kind,base_witness=None):
    base=dict(src);old=list(src)
    first=old[0];c=src[first]
    a=base_witness or {i:1 for i in range(1,n+1)}
    keep=1 if a[1] else -1
    moved={**base,max(old)+1:(keep,)}
    opposite={**base,max(old)+2:(-keep,)}
    deleted=dict(base);del deleted[first]
    flipped=dict(base);flipped[first]=(-c[0],)+tuple(c[1:])
    return [
        ('base',base,{}),
        ('added_pass_unit',moved,{}),
        ('remove_added',base,{}),
        ('added_opposite_unit',opposite,{}),
        ('return_base',base,{}),
        ('delete_first_clause',deleted,{}),
        ('restore_base',base,{}),
        ('flip_first_occurrence',flipped,{}),
        ('restore_again',base,{}),
        ('assume_x1_false',base,{1:0}),
        ('assume_x1_true',base,{1:1}),
        ('final_base',base,{})
    ]

_LITMASK_CACHE={}
def literal_masks(n):
    if n in _LITMASK_CACHE:return _LITMASK_CACHE[n]
    u=(1<<(1<<n))-1
    result={}
    for i in range(1,n+1):
        block=1<<(i-1)
        s=('0'*block+'1'*block)*(1<<max(0,n-i))
        yes=int(s[::-1],2)
        result[i]=yes;result[-i]=u^yes
    _LITMASK_CACHE[n]=(u,result)
    return u,result

def brute_models(src,rho,n):
    # Exhaustive exact Boolean mask oracle, 2^n assignment bits in a packed integer.
    universe,masks=literal_masks(n)
    feasible=universe
    for k,v in rho.items():feasible &= masks[k if v else -k]
    for c in src.values():
        clausemask=0
        for l in c:clausemask |= masks[l]
        feasible &= clausemask
        if not feasible:return []
    first=(feasible&-feasible).bit_length()-1
    return [first]

def perform(cases, use_cache):
    counts={'SAT':0,'UNSAT':0,'fresh_nodes':0,'events':0,'fresh':0,'hits_sat':0,'hits_unsat':0,'cache_candidates_rejected':0,'source_scans':0,'source_lit_probes':0,'cache_memb_probes':0,'peak_cache_bits':0,'peak_declarative_live_bits':0,'child_calls':0,'physical_child_bits':0,'proof_output_bytes':0,'query_parent_calls':0,'switched_policies':0}
    logs=[];global_cache=[]
    tracemalloc.start()
    for name,x in cases.items():
        n=x['n'];src={i+1:tuple(cl) for i,cl in enumerate(x['original_clauses'])}
        assert src and all(len(set(map(abs,c)))==len(c) for c in src.values())
        orig_answer=bool(brute_models(src,{},n))
        seed_wit=None
        if orig_answer:
            # Workload generator determines edits offline; not available to policy as oracle
            seed_wit=next({i:(mask>>(i-1))&1 for i in range(1,n+1)} for mask in brute_models(src,{},n))
        versions=source_version(src,n,'SAT' if orig_answer else 'UNSAT',seed_wit)
        entries=[];case_logs=[]
        for label,newsrc,rho in versions:
            events=[0]
            events[0]+=cost_source(newsrc);counts['source_scans']+=1;counts['source_lit_probes']+=cost_source(newsrc)
            decision=None;reason='fresh';witness=None;ptree=None;ref_origin=None
            if use_cache:
                for e in reversed(entries):
                    events[0]+=1+len(rho);counts['cache_memb_probes']+=1+len(rho)
                    if e['label']=='UNSAT' and valid_rho_extension(e['rho'],rho):
                        # Validate concrete original clauses by (source-ID, signed literal content).
                        ok=True
                        for cid,cl in e['reasons'].items():
                            events[0]+=len(cl)+1;counts['cache_memb_probes']+=len(cl)+1
                            if newsrc.get(int(cid))!=tuple(cl):ok=False;break
                        if ok:
                            decision=False;reason='reuse_UNSAT';ref_origin=e['origin_version'];counts['hits_unsat']+=1;break
                        counts['cache_candidates_rejected']+=1
                    if e['label']=='SAT':
                        a={int(k):v for k,v in e['witness'].items()}
                        events[0]+=len(a)+cost_source(newsrc);counts['cache_memb_probes']+=len(a)+cost_source(newsrc)
                        if sat_source(newsrc,rho,n,a):
                            decision=True;witness=a;reason='reuse_SAT';ref_origin=e['origin_version'];counts['hits_sat']+=1;break
                        counts['cache_candidates_rejected']+=1
            if decision is None:
                counts['fresh']+=1
                witness,ptree,nodes=dpll(newsrc,rho,n,events)
                counts['fresh_nodes']+=nodes;counts['query_parent_calls']+=1
                if use_cache:counts['switched_policies']+=1
                decision=witness is not None
                # Charge physical certificate output and a conservative source proof replay tariff.
                serialized=json.dumps(ptree,separators=(',',':'))
                events[0]+=len(serialized)+cost_source(newsrc)*nodes
                counts['proof_output_bytes']+=len(serialized)
                if use_cache:
                    if decision:
                        entries.append({'label':'SAT','rho':rho,'witness':witness,'origin_version':label})
                    else:
                        R=deps(ptree)
                        entries.append({'label':'UNSAT','rho':rho,'reasons':{cid:newsrc[cid] for cid in sorted(R)},'proof_tree':ptree,'origin_version':label})
                    if len(entries)>4:entries.pop(0)
            answer=bool(brute_models(newsrc,rho,n))
            if decision!=answer:raise AssertionError((name,label,decision,answer))
            counts['SAT' if answer else 'UNSAT']+=1;counts['events']+=events[0]
            envelope=physical_cache_bits(entries) if use_cache else 0
            counts['peak_cache_bits']=max(counts['peak_cache_bits'],envelope)
            childbytes=0 if ptree is None else len(json.dumps(ptree,separators=(',',':')))
            declared_source=8*len(json.dumps(newsrc,sort_keys=True,separators=(',',':')))
            declared_live=declared_source+envelope+8*childbytes+16*n
            counts['peak_declarative_live_bits']=max(counts['peak_declarative_live_bits'],declared_live)
            log={'case':name,'version':label,'src':{str(k):list(c) for k,c in newsrc.items()},'rho':{str(k):v for k,v in rho.items()},'label':'SAT' if answer else 'UNSAT','mechanism':reason,'reused_from':ref_origin,'events':events[0],'certificate':{'witness':{str(k):v for k,v in witness.items()} if decision and witness else None,'tree':ptree if not decision and ptree else None},'declared_cache_bits':envelope,'declared_live_bits':declared_live,'guest_full_parent':int(reason=='fresh'),'child_bits':0}
            case_logs.append(log)
        logs.extend(case_logs)
    current,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    counts['python_tracemalloc_peak_bytes']=peak
    return counts,logs

def main():
    raw=json.loads((HERE/'inputs270.json').read_text())
    cases=raw['cases'];assert len(cases)>=8
    for name,x in cases.items():
        if x['n']>15:raise AssertionError('oracle audit supports n<=15')
    fresh,base_logs=perform(cases,False)
    cache,cached_logs=perform(cases,True)
    original_controls={name:complement_diag({i+1:tuple(cl) for i,cl in enumerate(x['original_clauses'])},x['n']) for name,x in cases.items()}
    raw={'schema':'source-delta-proof270-v1','seed':0,'cases':cases,'baseline':base_logs,'cached':cached_logs,'original_diagnostics':original_controls,'counts':{'fresh':fresh,'cache':cache},'limitations':['native FLMV time/space not measured','legacy original input loaded from verified prior archive and copied into inputs270','cached only sound proof-dependent transfers','no arbitrary-A successor','full exhaustive checker is external experimental oracle not online solver']}
    path=HERE/'raw270.json';path.write_text(json.dumps(raw,sort_keys=True,separators=(',',':'))+'\n')
    by_label={}
    for meth,logs in [('baseline',base_logs),('cache',cached_logs)]:
        by_label[meth]={label:{'events':sum(r['events'] for r in logs if r['label']==label),'sessions':sum(r['label']==label for r in logs),'cache_hits':sum(r['label']==label and r['mechanism'].startswith('reuse') for r in logs)} for label in ('SAT','UNSAT')}
    summary={'by_label':by_label,'schema':'source-delta-proof270-summary-v1','originals':len(cases),'versions':len(cached_logs),'baseline':fresh,'cache':cache,'raw_bytes':path.stat().st_size,'raw_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    (HERE/'summary270.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
