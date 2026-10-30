#!/usr/bin/env python3
"""ARC-ONEHOT-COFACTOR-SELECT253, finite exact audit. Stdlib only.
Inputs are explicit, proper, original-indexed 3CNFs. Not an FLMV machine.
"""
import json, math, hashlib, itertools, sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

@dataclass
class Meter:
    source_sign_probes: int = 0
    child_bits: int = 0
    guest_literal_visits: int = 0
    guest_nodes: int = 0
    child_writes: int = 0
    scans: int = 0
    cache_bits: int = 0
    other_events: int = 0
    def total(self):
        return sum((self.source_sign_probes,self.child_bits,self.guest_literal_visits,
                    self.guest_nodes,self.child_writes,self.scans,self.other_events))


def source(m,mark,unsat=False):
    # x=1, z=2, a_i=i+3, u,v,w=m+3,m+4,m+5
    # one source occurrence of x is positive, m-1 are negative.
    clauses=[tuple([1 if i==mark else -1,i+3,2]) for i in range(m)]
    if unsat:
        u,v,w=m+3,m+4,m+5
        clauses += [tuple(s[i]*q for i,q in enumerate((u,v,w)))
                    for s in itertools.product((-1,1),repeat=3)]
    return tuple(clauses),m+5


def restrict(formula,var,val):
    ans=[]
    for clause in formula:
        if any((lit>0)==val for lit in clause if abs(lit)==var):
            continue
        ans.append(tuple(lit for lit in clause if abs(lit)!=var))
    return tuple(ans)


def encode(formula,n):
    # Physical binary encoding: w-bit n, w-bit m, then fixed width(2 bits)
    # and 3 slots of (sign + w-bit ID), with zero IDs as pads.
    w=max(1,(n+8).bit_length())
    maxval=(1<<w)-1
    assert len(formula)<=maxval and n<=maxval
    b=f'{n:0{w}b}'+f'{len(formula):0{w}b}'
    for c in formula:
        assert len(c)<=3
        b+=f'{len(c):02b}'
        for lit in tuple(c)+(0,)*(3-len(c)):
            b+=('1' if lit<0 else '0')+f'{abs(lit):0{w}b}'
    return b


def decode(b,n):
    w=max(1,(n+8).bit_length()); p=0
    nn=int(b[p:p+w],2);p+=w
    cc=int(b[p:p+w],2);p+=w
    assert nn==n
    ans=[]
    for _ in range(cc):
        k=int(b[p:p+2],2);p+=2
        row=[]
        for j in range(3):
            s=int(b[p]);p+=1
            a=int(b[p:p+w],2);p+=w
            if j<k: row.append((-1 if s else 1)*a)
            else: assert a==0
        ans.append(tuple(row))
    assert p==len(b)
    return tuple(ans)


def sat_dpll(formula,meter):
    def solve(clauses):
        meter.guest_nodes+=1
        while True:
            unit=None
            new=[]
            for c in clauses:
                meter.guest_literal_visits+=len(c)
                if not c: return False
                if len(c)==1 and unit is None: unit=c[0]
            if unit is None: break
            new=[]
            for c in clauses:
                meter.guest_literal_visits+=len(c)
                if unit in c: continue
                new.append(tuple(t for t in c if t!=-unit))
            clauses=tuple(new)
        if not clauses:return True
        x=abs(clauses[0][0])
        for val in (False,True):
            new=restrict(clauses,x,val)
            meter.guest_literal_visits+=sum(len(c) for c in clauses)
            if solve(new):return True
        return False
    return solve(formula)


def scan_mark(m,mark,meter):
    for j in range(m):
        meter.source_sign_probes+=1
        if j==mark: return j
    raise AssertionError('one-hot promise violated')


def virtual_child_bits(m,mark,unsat,n,cache,meter):
    # For every bit request, a no-index generator must locate a unique
    # marked record. The cached mode locates it once and retains its address.
    core=source(m,mark,unsat)[0][m:]
    w=max(1,(n+8).bit_length())
    count=1+len(core)
    record=2+3*(1+w)
    bits=2*w+count*record
    if cache:
        index=scan_mark(m,mark,meter)
        meter.cache_bits=max(1,(m-1).bit_length())
    else:
        index=None
    out=[]
    for t in range(bits):
        meter.child_bits+=1
        if t<2*w:
            val=n if t<w else count
            off=t if t<w else t-w
            out.append(f'{val:0{w}b}'[off])
            continue
        row=(t-2*w)//record
        pos=(t-2*w)%record
        if row==0:
            j=index if cache else scan_mark(m,mark,meter)
            c=(j+3,2)
        else:
            c=core[row-1]
        if pos<2: bit=f'{len(c):02b}'[pos]
        else:
            slot=(pos-2)//(w+1)
            sub=(pos-2)%(w+1)
            lit=c[slot] if slot<len(c) else 0
            bit=('1' if lit<0 else '0') if sub==0 else f'{abs(lit):0{w}b}'[sub-1]
        out.append(bit)
    return ''.join(out)


def evaluate(cnf,assign):
    return all(any(assign[abs(lit)]==(lit>0) for lit in clause) for clause in cnf)


def profile(cnf,assign):
    counts=[sum(assign[abs(lit)]==(lit>0) for lit in c) for c in cnf]
    return {'per_clause':counts,'N':[counts.count(i) for i in range(4)],'SAT':all(x>0 for x in counts)}


def extremes(c):
    s={abs(lit):(lit>0) for lit in c}
    u={i:not v for i,v in s.items()}
    return {'S':s,'inverted_S_is_U':u,'U':u,'inverted_U_is_S':s}


def compatible(left,right):
    d={}
    for a in 'SU':
        for b in 'SU':
            A=extremes(left)[a]; B=extremes(right)[b]
            common=A.keys() & B.keys()
            d[a+b]=all(A[x]==B[x] for x in common)
    return d


def brute_compat(c,d):
    vs=sorted(set(abs(l) for l in c+d))
    out={k:False for k in ('SS','SU','US','UU')}
    for seq in itertools.product((False,True),repeat=len(vs)):
        a=dict(zip(vs,seq))
        k1='S' if all(a[abs(l)]==(l>0) for l in c) else 'U' if all(a[abs(l)]!=(l>0) for l in c) else 'M'
        k2='S' if all(a[abs(l)]==(l>0) for l in d) else 'U' if all(a[abs(l)]!=(l>0) for l in d) else 'M'
        if 'M' not in (k1,k2):out[k1+k2]=True
    return out


@lru_cache(None)
def min_identify_queries(mask):
    if mask.bit_count()<=1:return 0
    return 1+min_identify_queries(mask & (mask-1))


@lru_cache(None)
def min_parity_queries(mask):
    inds=[i for i in range(mask.bit_length()) if (mask>>i)&1]
    if not inds or all((i%2)==(inds[0]%2) for i in inds): return 0
    best=mask.bit_count()
    for i in inds:
        cand=1+min_parity_queries(mask&~(1<<i))
        if cand<best: best=cand
    return best


def resolve(a,b,pivot):
    assert pivot in a and -pivot in b
    row=tuple(sorted((set(a)-{pivot}) | (set(b)-{-pivot}), key=lambda v:(abs(v),v<0)))
    assert all(-x not in row for x in row)
    return row


def polarity_countercontrols():
    ep=((1,2,3),(1,2,-3),(1,-2,3),(1,-2,-3))
    em=tuple(tuple(-lit if abs(lit)==1 else lit for lit in c) for c in ep)
    both=ep+em
    p1=resolve(ep[0],ep[1],3);p2=resolve(ep[2],ep[3],3)
    up=resolve(p1,p2,2)
    n1=resolve(em[0],em[1],3);n2=resolve(em[2],em[3],3)
    un=resolve(n1,n2,2)
    empty=resolve(up,un,1)
    assert set(up)=={1} and set(un)=={-1} and not empty
    assert sat_dpll(ep,Meter()) and sat_dpll(em,Meter()) and not sat_dpll(both,Meter())
    assert not sat_dpll(restrict(ep,1,False),Meter()) and sat_dpll(restrict(ep,1,True),Meter())
    assert not sat_dpll(restrict(both,1,False),Meter()) and not sat_dpll(restrict(both,1,True),Meter())
    return {'source_clauses':[list(c) for c in both],
            'proof':[{'parents':[0,1],'pivot':3,'result':list(p1)},
                     {'parents':[2,3],'pivot':3,'result':list(p2)},
                     {'parents':['R0','R1'],'pivot':2,'result':list(up)},
                     {'parents':[4,5],'pivot':3,'result':list(n1)},
                     {'parents':[6,7],'pivot':3,'result':list(n2)},
                     {'parents':['R3','R4'],'pivot':2,'result':list(un)},
                     {'parents':['R2','R5'],'pivot':1,'result':list(empty)}],
            'Eplus_sat':True,'Eplus_x0_sat':False,'Eplus_x1_sat':True,
            'Eplus_and_Eminus_sat':False}


def run():
    results=[]
    for m in (4,6,8,10,12):
        opt=min_parity_queries((1<<m)-1)
        assert opt==m//2,(m,opt)
        assert min_identify_queries((1<<m)-1)==m-1
        for is_unsat in (False,True):
            for mark in (0,m//2,m-1):
                orig,n=source(m,mark,is_unsat)
                c0=restrict(orig,1,False);c1=restrict(orig,1,True)
                assert len(c0)==1+(8 if is_unsat else 0)
                assert len(c1)==m-1+(8 if is_unsat else 0)
                direct=encode(c0,n)
                assert decode(direct,n)==c0
                assert decode(encode(c1,n),n)==c1
                mt1=Meter();v1=virtual_child_bits(m,mark,is_unsat,n,False,mt1)
                mt2=Meter();v2=virtual_child_bits(m,mark,is_unsat,n,True,mt2)
                assert direct==v1==v2
                base=Meter();result=sat_dpll(orig,base)
                cmet0=Meter();d0=sat_dpll(decode(v2,n),cmet0)
                cmet1=Meter();d1=False
                if not d0:
                    d1=sat_dpll(c1,cmet1)
                assert result==(d0 or d1)==(not is_unsat)
                # Treat data probes separately from Python runtime/allocations.
                assert mt1.source_sign_probes>=mt2.source_sign_probes
                for i,j in itertools.combinations(range(len(orig)),2):
                    assert compatible(orig[i],orig[j])==brute_compat(orig[i],orig[j])
                # all-0/all-1, complement and true-literal counts.
                zero={i:False for i in range(1,n+1)}
                one={i:True for i in range(1,n+1)}
                p0=profile(orig,zero);p1=profile(orig,one)
                assert all(p0['per_clause'][j]+p1['per_clause'][j]==3 for j in range(len(orig)))
                for idx in range(min(m,5)):
                    flipped=zero.copy();flipped[idx+1]=True
                    ff=profile(orig,flipped)
                    opposite=profile(orig,{i:not v for i,v in flipped.items()})
                    assert all(a+b==3 for a,b in zip(ff['per_clause'],opposite['per_clause']))
                item={'m':m,'mark':mark,'unsat_core':is_unsat,'label':'UNSAT' if is_unsat else 'SAT',
                      'original_n':n,'original_clauses':len(orig),
                      'child_zero_clauses':len(c0),'child_one_clauses':len(c1),
                      'original_bits':len(encode(orig,n)),'short_child_bits':len(direct),
                      'long_child_bits':len(encode(c1,n)),'parity_bit_query_worstcase':opt,
                      'stateless_source_probes':mt1.source_sign_probes,
                      'cached_source_probes':mt2.source_sign_probes,
                      'cached_summary_bits':mt2.cache_bits,
                      'child_output_bits':mt1.child_bits,
                      'baseline_DPLL':base.__dict__,'child0_DPLL':cmet0.__dict__,
                      'child1_DPLL':cmet1.__dict__,
                      'parent_zero':p0['N'],'parent_one':p1['N']}
                base_events=len(encode(orig,n))+base.guest_literal_visits+base.guest_nodes
                # Declared selected-event accounting, not native FLMV bit steps:
                # parsing original source; scanning m clause records for chosen
                # policy; making and parsing child0 bits; completed guest;
                # if child0 NO, scanning and writing child1; second guest.
                common=len(encode(orig,n))+m+1+2*len(direct)
                first_guest=cmet0.guest_literal_visits+cmet0.guest_nodes
                second_guest=cmet1.guest_literal_visits+cmet1.guest_nodes
                after_zero=(m+2*len(encode(c1,n))+second_guest+1) if not d0 else 0
                item['charged_event_proxy']={
                    'baseline':base_events,
                    'cached_controller':common+mt2.source_sign_probes+first_guest+after_zero,
                    'stateless_controller':common+mt1.source_sign_probes+first_guest+after_zero,
                    'controller_input_scan_bits':len(encode(orig,n)),
                    'controller_policy_search_records':m,
                    'child0_written_and_decoded_bits':2*len(direct),
                    'child1_written_and_decoded_bits':2*len(encode(c1,n)) if not d0 else 0,
                    'child0_cached_locator_bits':mt2.cache_bits,
                    'max_child_retained_bits':max(len(direct),len(encode(c1,n)) if not d0 else 0)}
                if m==6 and mark==0:
                    item['original_clause_source']=[list(c) for c in orig]
                    item['original_clause_extreme_targets']=[extremes(c) for c in orig]
                    item['pair_matrices']=[{'source_clause_indices':[i,j],**compatible(orig[i],orig[j])}
                                           for i,j in itertools.combinations(range(len(orig)),2)]
                    item['zero_per_clause']=p0['per_clause'];item['one_per_clause']=p1['per_clause']
                    item['flip_trail']=[{'flipped_source_var':q,'profile':profile(orig,{i:(i==q) for i in range(1,n+1)})}
                                        for q in (1,2,3)]
                results.append(item)
    raw={'claim':'For one-hot m even source masks, one selected parity output bit needs exactly m/2 indexed sign probes without persisted data, worst-case.',
         'status':'PROVED/EXACT restricted; finite check COMPUTATIONAL','seed':None,'tests':{'family_cases':len(results),'minimax_states':min_parity_queries.cache_info().currsize,'minimax_stats':str(min_parity_queries.cache_info()),'index_identification_tested':True},
         'cases':results,'polarity_resolution_controls':polarity_countercontrols()}
    return raw

if __name__=='__main__':
    r=run()
    path=Path(sys.argv[1] if len(sys.argv)>1 else 'arc_selector253_raw.json')
    path.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'cases':r['tests']['family_cases'],
                      'minimax':r['tests']['minimax_stats'],
                      'output':str(path),
                      'example':[{k:v for k,v in x.items() if k in ('m','mark','label','original_bits','short_child_bits','long_child_bits','parity_bit_query_worstcase','stateless_source_probes','cached_source_probes','baseline_DPLL')}
                                 for x in r['cases'] if x['m']==8 and x['mark']==0]},indent=2))