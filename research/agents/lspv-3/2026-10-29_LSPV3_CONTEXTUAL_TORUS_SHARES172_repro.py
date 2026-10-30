#!/usr/bin/env python3
"""LSPV-3 CONTEXTUAL-TORUS-SHARES172: exact strict signed (2,2) controls.
No general SAT polynomiality: polynomial is only on the canonical masked-torus
promise. Uses stdlib, checks independent finite core and connector gate lemma.
Run: python 2026-10-29_LSPV3_CONTEXTUAL_TORUS_SHARES172_repro.py
"""
from __future__ import annotations
from collections import Counter, defaultdict
from itertools import product, combinations
import hashlib, json, math, pathlib, time

W1 = [(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
      (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
      (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
      (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
G = [tuple(-l if abs(l)==4 and i in (6,11) else l for l in c)
     for i,c in enumerate(W1)]
V = [tuple(-l if abs(l)==9 and i in (4,11) else l for l in c)
     for i,c in enumerate(W1)]


def shift(cs,d):
    return [tuple((1 if l>0 else -1)*(abs(l)+d) for l in c) for c in cs]

def complement_var(cs,v):
    return [tuple(-l if abs(l)==v else l for l in c) for c in cs]

def eval_clause(c,a):
    return any(a[abs(l)]==int(l>0) for l in c)

def eval_formula(cs,a):
    return all(eval_clause(c,a) for c in cs)

def assignment(mask,n):
    return {v:((mask>>(v-1))&1) for v in range(1,n+1)}

def models(cs,n):
    for mask in range(1<<n):
        a=assignment(mask,n)
        if eval_formula(cs,a): yield mask

def verify_connected_exact22(cs,n):
    assert len(cs)==4*n//3 and n%3==0
    cnt=Counter(l for c in cs for l in c)
    assert all(cnt[i]==cnt[-i]==2 for i in range(1,n+1))
    assert all(len(c)==3 and len({abs(l) for l in c})==3 for c in cs)
    assert len(cs)==len({tuple(sorted(c)) for c in cs})
    adj=[set() for _ in range(n+1)]
    for c in cs:
        v=[abs(l) for l in c]
        for x in v: adj[x].update(z for z in v if z!=x)
    seen={1};todo=[1]
    while todo:
        x=todo.pop()
        for z in adj[x]-seen:seen.add(z);todo.append(z)
    assert len(seen)==n
    return cnt

def torus(L):
    assert L>=6 and L%6==0
    vid=lambda r,c:1+(r%L)*L+(c%L)
    cs=[]
    for r in range(L):
        for o in (0,1):
            for j in range(L//3):cs.append(tuple(vid(r,o+3*j+t) for t in range(3)))
    for c in range(L):
        for o in (0,1):
            for j in range(L//3):cs.append(tuple(-vid(o+3*j+t,c) for t in range(3)))
    w={vid(r,c):int(r%3==c%3) for r in range(L) for c in range(L)}
    assert eval_formula(cs,w)
    return cs,w

def first_negative(cs):
    return next((i,j,abs(l)) for i,c in enumerate(cs) for j,l in enumerate(c) if l<0)

def connector(a,b):
    na=max(abs(l) for c in a for l in c)
    nb=max(abs(l) for c in b for l in c)
    A=list(a);B=shift(b,na)
    ai,ak,x=first_negative(A);bi,bk,y=first_negative(B)
    g1off=na+nb;g2off=g1off+15
    C1=shift(G,g1off);C2=shift(G,g2off)
    A[ai]=tuple(-g1off-4 if j==ak else l for j,l in enumerate(A[ai]))
    B[bi]=tuple(-g2off-4 if j==bk else l for j,l in enumerate(B[bi]))
    C1[4]=tuple(-x if j==0 else l for j,l in enumerate(C1[4]))
    C2[4]=tuple(-y if j==0 else l for j,l in enumerate(C2[4]))
    C1[6]=tuple(-g2off-8 if j==1 else l for j,l in enumerate(C1[6]))
    C2[6]=tuple(-g1off-8 if j==1 else l for j,l in enumerate(C2[6]))
    return A+B+C1+C2,dict(na=na,nb=nb,ai=ai,ak=ak,x=x,
                             bi=bi,bk=bk,y=y,g1off=g1off,g2off=g2off)

def masked_source(t,r):
    assert t in (0,1) and r in (0,1)
    return complement_var(V if t else W1,9) if r else list(V if t else W1)

def family(L,t,r):
    T,_=torus(L)
    return connector(T,masked_source(t,r))[0]

def raw_shares(F,L):
    # W1 is appended after 4L^2/3 torus clauses; W1 clause 1 v9 untouched
    # W1 clause 4 v9 untouched. Two opposite source-occurrence groups.
    base=4*L*L//3
    x=F[base+1][2]   # original W1 clause 1, 9 when r=0
    y=F[base+4][1]   # original W1 clause 4, -9 when t=r=0
    assert abs(x)==abs(y)==L*L+9
    a=int(x<0)      # a=r
    b=int(y>0)      # b=t XOR r
    return a,b

def validation(F,L,t,r):
    # Always charge an entire canonical comparison, not just sample bits.
    expected=family(L,t,r)
    return F==expected

def make_guard_profiles():
    # Explicit finite 15-variable proof; 32768 candidates checked, not a lookup oracle.
    retained=[c for i,c in enumerate(G) if i not in (4,6)]
    buckets={(x,a):{} for x,a in product((0,1),repeat=2)}
    counts={}
    for x,a in product((0,1),repeat=2):
        profile=Counter()
        for mask in range(1<<15):
            v=assignment(mask,15)
            if not eval_formula(retained,v):continue
            if not ((not x or eval_clause((-9,-11),v)) and (not v[4] or a)):
                continue
            u=int(not v[8]);w=int((not v[4]) or (not v[11]))
            profile[(u,w)]+=1
            buckets[(x,a)].setdefault((u,w),mask)
        counts[f'{x}{a}']={f'{u}{w}':n for (u,w),n in sorted(profile.items())}
    expected={'00':{'01':153},'01':{'00':178,'01':153,'10':170,'11':34},
              '10':{},'11':{'00':25,'10':85,'11':34}}
    assert counts==expected,(counts,expected)
    for x,a,y,b in product((0,1),repeat=4):
        gate=any((v1 or u2) and (v2 or u1)
                 for u1,v1 in buckets[(x,a)] for u2,v2 in buckets[(y,b)])
        assert gate==bool((not x or a) and (not y or b))
    return buckets,counts

def port_remainder(cs,port,val):
    i,k,x=port
    return int(any(val[abs(l)]==int(l>0) for j,l in enumerate(cs[i]) if j!=k))

def sat_witness(L,t,r,info,profiles):
    assert t==1
    T,wa=torus(L)
    # Compute V's first satisfying valuation from raw 20 clauses, not an oracle.
    mask=next(models(V,15))
    wb=assignment(mask,15)
    if r:wb[9]^=1
    assert eval_formula(masked_source(t,r),wb)
    A=T;B=shift(masked_source(t,r),info['na'])
    ab={**wa,**{v+info['na']:w for v,w in wb.items()}}
    x=ab[info['x']];a=port_remainder(A,(info['ai'],info['ak'],info['x']),ab)
    y=ab[info['y']];b=port_remainder(B,(info['bi'],info['bk'],info['y']),ab)
    valid=None
    for (u1,v1),m1 in profiles[(x,a)].items():
        for (u2,v2),m2 in profiles[(y,b)].items():
            if (v1 or u2) and (v2 or u1):valid=(m1,m2);break
        if valid:break
    assert valid is not None
    for offset,mask in zip((info['g1off'],info['g2off']),valid):
        ab.update({offset+j:((mask>>(j-1))&1) for j in range(1,16)})
    return ab

def core_audit():
    # Exact enumeration independent of opposite-label promise.
    w=list(models(W1,15));v=list(models(V,15));g=list(models(G,15))
    assert len(w)==0 and len(v)==54 and len(g)==272
    return dict(W1_models=0,V_models=54,G_models=272,V_first_model=v[0])

def core_unsat_checker():
    # Direct source enumerator, intentionally independent of template controller.
    for mask in range(1<<15):
        if eval_formula(W1,assignment(mask,15)):return False
    return True

def controller(F,L,profiles,full=True):
    """One deterministic controller for BOTH answer classes on canonical promise.
    Tries an inapplicable syntactic 2CNF strategy and charges failure;
    probes both sign shares; regenerates/compares full formula; outputs a
    certified SAT witness or a sound template+finite-core UNSAT transcript.
    Invalid root => UNSUPPORTED, not an UNSAT claim. Complete fallback can be
    added at exponential cost, with no claim that this is polynomial general SAT.
    """
    ledger=dict(read_literal=0,failed_routes=0,source_comparisons=0,
                core_tests=0,gate_tests=0,witness_checks=0,
                switches=0,probe_signs=0,
                template_generation_clauses=0,connectivity_scope_checks=0,
                gate_profile_masks_reserved=4*(1<<15),
                fixed_core_masks_reserved=(1<<15),
                failed_strategy_clause_checks=0)
    n=L*L+45
    if n<81 or L%6 or len(F)!=4*n//3:
        return {'status':'UNSUPPORTED','ledger':ledger}
    # A bounded failed strategy: reject 2CNF by inspecting every clause width.
    ledger['read_literal']+=3*len(F)
    ledger['failed_strategy_clause_checks']=len(F)
    if any(len(c)>2 for c in F):
        ledger['failed_routes']+=1;ledger['switches']+=1
    # Raw data without label oracle. Each individual probe has zero target entropy gain.
    a,b=raw_shares(F,L);ledger['probe_signs']=2
    t=a^b;r=a
    ledger['source_comparisons']+=3*len(F)
    ledger['template_generation_clauses']=len(F)
    if not validation(F,L,t,r):
        return {'status':'UNSUPPORTED','ledger':ledger,'observed_shares':[a,b]}
    # Recheck every syntactic clause and signed occurrence, connectedness.
    verify_connected_exact22(F,n)
    ledger['connectivity_scope_checks']=len(F)
    ledger['read_literal']+=3*len(F)
    ledger['switches']+=1
    if t:
        T,_=torus(L);_,info=connector(T,masked_source(t,r))
        wit=sat_witness(L,t,r,info,profiles)
        assert eval_formula(F,wit)
        ledger['witness_checks']=len(F)
        return {'status':'SAT','witness':wit,'ledger':ledger,
                'observed_shares':[a,b],'mode':t,'mask':r}
    else:
        assert core_unsat_checker()
        ledger['core_tests']=1<<15
        ledger['gate_tests']=16
        return {'status':'UNSAT','certificate':{
            'rule':'verified_connector_AND','source':'W1','sign_complement':r,
            'source_clauses':20,'source_unsat_valuations_checked':1<<15,
            'gate_rows_checked':16,'connector_guard_source_sha_label':'G_15_20',
            'full_canonical_source_validated':True},
            'ledger':ledger,'observed_shares':[a,b],'mode':t,'mask':r}

def independent_certificate_checker(F,L,res):
    if res['status'] not in ('SAT','UNSAT'):return False
    a,b=raw_shares(F,L)
    t=a^b;r=a
    if not validation(F,L,t,r):return False
    if res['status']=='SAT':
        w=res['witness']
        return t==1 and len(w)==L*L+45 and eval_formula(F,w)
    cert=res.get('certificate',{})
    if t!=0 or cert.get('rule')!='verified_connector_AND' or cert.get('source')!='W1':return False
    if cert.get('sign_complement')!=r:return False
    if cert.get('source_unsat_valuations_checked')!=(1<<15):return False
    if cert.get('gate_rows_checked')!=16:return False
    # Independently checks fixed source W1 and exact four-row connector relation.
    return core_unsat_checker() and gate_checker_independent()

def gate_checker_independent():
    # Independent gate-satisfiability computation, no stored profiles accepted.
    profiles={}
    removed=[c for i,c in enumerate(G) if i not in (4,6)]
    for x,a in product((0,1),repeat=2):
        pairs=set()
        for mask in range(1<<15):
            v=assignment(mask,15)
            if eval_formula(removed,v) and (not x or eval_clause((-9,-11),v)) and (not v[4] or a):
                pairs.add((int(not v[8]),int((not v[4]) or (not v[11]))))
        profiles[(x,a)]=pairs
    for x,a,y,b in product((0,1),repeat=4):
        possible=any((v or uu) and (vv or u) for u,v in profiles[(x,a)] for uu,vv in profiles[(y,b)])
        if possible!=bool((not x or a) and (not y or b)):
            return False
    return True

def sha_json(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
    core=core_audit();profiles,counts=make_guard_profiles();out=[]
    for L in (6,12,18,24):
        for t,r in product((0,1),repeat=2):
            F=family(L,t,r)
            verify_connected_exact22(F,L*L+45)
            a,b=raw_shares(F,L)
            assert (a,b)==(r,t^r)
            res=controller(F,L,profiles)
            assert res['status']==('SAT' if t else 'UNSAT')
            # Verify a small-independent high-cost source proof for each UNSAT L,
            # and SAT clause-by-clause validation for all SAT.
            if L==6 or t==1:
                assert independent_certificate_checker(F,L,res)
            altered=[tuple(c) for c in F]
            altered[0]=tuple(-l if j==0 else l for j,l in enumerate(altered[0]))
            assert controller(altered,L,profiles)['status']=='UNSUPPORTED'
            audit=dict(L=L,t=t,r=r,n=L*L+45,m=len(F),
                       sha256=sha_json(F),shares=[a,b],
                       status=res['status'],ledger=res['ledger'],
                       witness_bits=len(res.get('witness',{})),
                       unsat_proof_kind='template+fixed_exhaustive_AND_gate' if t==0 else None)
            out.append(audit)
    # Exact decision entropy H(t)=1; uniform four possible (t,r) pairs.
    for idx in (0,1):
        for value in (0,1):
            subset=[(t,r) for t,r in product((0,1),repeat=2)
                    if (r,t^r)[idx]==value]
            assert len(subset)==2 and set(t for t,r in subset)=={0,1}
    assert all(len({t for t,r in product((0,1),repeat=2) if (r,t^r)==(a,b)})==1 for a,b in product((0,1),repeat=2))
    # Every individual share zero, the pair one, and a duplicate contributes zero.
    symbolic={'H_target':1,'gain_first_share':0,'gain_second_share':0,
              'gain_pair':1,'marginal_second_given_first':1,
              'gain_duplicate_after_first':0,'context_equal_mask_then_label_determined':True,
              'negative_drift_example':{'initial_remaining_tasks':1,'invalidated_cached_tasks':5,
                'new_remaining_tasks':6,'realized_value_remaining_tasks':-5}}
    # Tampering with certificate must be caught by independent checker.
    F=family(6,0,1);res=controller(F,6,profiles)
    tamper=dict(res);tamper['certificate']=dict(tamper['certificate']);tamper['certificate']['sign_complement']=0
    assert not independent_certificate_checker(F,6,tamper)
    # Sentinel demonstration: a false sign reconstruction should not claim UNSAT.
    bad=list(F);q=list(bad[4*6*6//3+4]);q[1]*=-1;bad[4*6*6//3+4]=tuple(q)
    assert controller(bad,6,profiles)['status']=='UNSUPPORTED'
    result={'id':'LSPV3_CONTEXTUAL_TORUS_SHARES172','seed':'exhaustive_no_random',
            'core':core,'gate_profile':counts,'info':symbolic,
            'tests':out,'model_scope':'indexed word-RAM operations; fixed finite source enumeration, no TM timing',
            'status':'RESTRICTED_PROVED_IF_CONNECTOR231_FINITE_LEMMA;COMPUTATIONAL_TESTED',
            'limitations':['canonical promise, not arbitrary variable permutation',
                'UNSAT proof is template-semantic, not ordinary Resolution',
                'all-instance fallback not claimed polynomial',
                'treewidth derived from torus grid, not measured exact tw',
                'entropy computed under specified four-template uniform prior']}
    path=pathlib.Path(__file__).with_name('2026-10-29_CONTEXTUAL_TORUS_SHARES172_raw.json')
    path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'source_labels':core,'cases':len(out),'statuses':dict(Counter(z['status'] for z in out)),
                      'max_n':max(z['n'] for z in out),'max_signed_occurrence_error':0,
                      'raw_sha256':hashlib.sha256(path.read_bytes()).hexdigest()},indent=2))

if __name__=='__main__':main()
