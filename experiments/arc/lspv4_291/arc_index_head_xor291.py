#!/usr/bin/env python3
"""ARC-INDEX-HEAD-XOR291: finite, audited FLMV-legal head-motion microtraces.

The head coordinates here are OFFLINE binary/Gray descriptions, not written
index-tape cells.  A head step is native. No SAT complexity conclusion follows.
"""
from __future__ import annotations
from pathlib import Path
from collections import Counter
from fractions import Fraction
import json,itertools,hashlib

P=Path(__file__).resolve().parent
U=json.loads((P/'U_source.json').read_text())
Y=json.loads((P/'Y6_source.json').read_text())
V=[c[:] for c in U]
V[1][0],V[7][0]=V[7][0],V[1][0]
W=json.loads((P/'V_witness.json').read_text())


def valid(f,n):
    if len(f)*3 != 4*n:return False
    p=[0]*(n+1);q=[0]*(n+1);seen=set()
    for c in f:
        if len(c)!=3 or len({abs(x) for x in c})!=3:return False
        if any(x==0 or abs(x)>n for x in c):return False
        if any((x>0)!=(c[0]>0) for x in c):return False
        sig=tuple(sorted(c))
        if sig in seen:return False
        seen.add(sig)
        for z in c:
            (p if z>0 else q)[abs(z)]+=1
    return all(p[i]==q[i]==2 for i in range(1,n+1))

def true(lit,a):return int((a[abs(lit)-1]==1)==(lit>0))
def counts(f,a):return [sum(true(z,a) for z in c) for c in f]
def hist(f,a):return [counts(f,a).count(k) for k in range(4)]

def gray(x):return x^(x>>1)
def encoder(f,n):
    m=len(f);b=m.bit_length()
    return '1'*b+'0'+format(n,f'0{b}b')+format(m,f'0{b}b')+''.join(('1' if z>0 else '0')+format(abs(z),f'0{b}b') for c in f for z in c)

def pairs(f):
    out=[]
    for i in range(len(f)):
        x={abs(z):(z>0) for z in f[i]}
        for j in range(i+1,len(f)):
            y={abs(z):(z>0) for z in f[j]};keys=x.keys()&y.keys()
            same=any(x[k]==y[k] for k in keys)
            opp=any(x[k]!=y[k] for k in keys)
            out.append({'clause_pair':[i,j], 'SS_SU_US_UU':[int(not opp),int(not same),int(not same),int(not opp)]})
    return out

def logical_bits(f,a):
    cs=counts(f,a)
    return list(a)+[v for t in cs for v in ((t>>1)&1,t&1)]+[int(t>0) for t in cs]

def controls(f,n):
    original=[]
    for i,c in enumerate(f):
        s=[[abs(z),int(z>0)] for z in c]
        u=[[abs(z),int(z<0)] for z in c]
        original.append({'source_clause_index':i,'signed_occurrences':c,'S_local_all_true':s,
                         'U_local_all_false':u,'inverted_S_to_U':u,'inverted_U_to_S':s})
    a=[0]*n;flips=[]
    for i in range(min(n,8)):
        old=counts(f,a);lb=logical_bits(f,a);a[i]^=1
        now=counts(f,a);la=logical_bits(f,a)
        changed=[j for j,(x,y) in enumerate(zip(old,now)) if x!=y]
        flips.append({'variable':i+1,'changed_original_clause_ids':changed,
                      'logical_xor_popcount':sum(x!=y for x,y in zip(lb,la)),
                      'new_histogram':[now.count(k) for k in range(4)]})
    return {'original':original,'pair_modes':pairs(f),'allzero_hist':hist(f,[0]*n),
            'allone_hist':hist(f,[1]*n), 'flip_trail':flips}

def microtrace(bits,h_override=None):
    h=bits.bit_length()-1 if h_override is None else h_override
    start=(1<<h)-1
    if start+1>=bits:
        h-=1;start=(1<<h)-1
    R=8*start # even and provides substantial head churn
    # Native legal phase I: head starts at 0, advances to 2**h-1.
    # Native legal phase II: alternate the index-tape head at p,p+1.
    prev=0;prep_binary=prep_gray=0
    for head in range(1,start+1):
        prep_binary+=(head^prev).bit_count()
        prep_gray+=(gray(head)^gray(prev)).bit_count()
        prev=head
    binary_step=(start^(start+1)).bit_count()
    gray_step=(gray(start)^gray(start+1)).bit_count()
    assert binary_step==h+1 and gray_step==1 and R%2==0
    return {'source_bits':bits,'h':h,'boundary':start,'other':start+1,'prep_steps':start,
            'oscillation_steps':R,'total_native_head_moves':start+R,
            'head_position_code_width':h+1,'index_tape_content_writes':0,
            'index_tape_erasure_events':0,'source_payload_changes':0,
            'prep_binary_head_xor':prep_binary,'prep_gray_head_xor':prep_gray,
            'oscillation_binary_head_xor':R*binary_step,
            'oscillation_gray_head_xor':R*gray_step,
            'oscillation_control_bit_xor':R, 'oscillation_tape_content_xor':0,
            'oscillation_full_binary_code_xor':R*(h+2),
            'oscillation_full_gray_code_xor':2*R,
            'oscillation_full_endpoint_xor':0,
            'total_binary_head_xor':prep_binary+R*binary_step,
            'total_gray_head_xor':prep_gray+R*gray_step,
            'binary_per_step':binary_step,'gray_per_step':gray_step,
            'unrestricted_model_note':'This describes a legal FLMV index-head walk, not a native compiled SAT solver.'}

def flmv(c):
    f=Fraction(1);terms=[]
    for k in range(1,4):
        f=c*f/(1+f)
        terms.append(str(min((1/f-c)/k,c**(-k))))
    return {'c':str(c),'k_1_2_3':terms,'tail_cap':str(c**(-4)),'winner':'2'}

def up_dpll(f,limit=300):
    nodes=0
    class Budget(Exception):pass
    def rec(clauses):
        nonlocal nodes
        nodes+=1
        if nodes>limit:raise Budget
        while True:
            if not clauses:return True
            if any(len(c)==0 for c in clauses):return False
            single=next((c[0] for c in clauses if len(c)==1),None)
            if single is None:break
            clauses=[[x for x in c if x!=-single] for c in clauses if single not in c]
        pivot=clauses[0][0]
        for bit in (pivot,-pivot):
            nxt=[[x for x in c if x!=-bit] for c in clauses if bit not in c]
            if rec(nxt):return True
        return False
    try:result='SAT' if rec(f) else 'UNSAT'
    except Budget:result='UNKNOWN'
    return {'nodes':nodes,'status':result,'node_limit':limit}


def main():
    data={'theorem':'Binary encoding of legal index-head positions can amplify adjacent XOR without any tape-content writes.',
          'microtrace_semantics':'Index head positions encode offline in fixed binary and reflected Gray; underlying FLMV head moves identical.',
          'sources':{},'flmv':[flmv(Fraction(6,5)),flmv(Fraction(241,200))],
          'falsifiers':{'F1':'full-state binary XOR <= constant*physical writes: FALSE',
                        'F2':'XOR invariant under Gray recoding: FALSE',
                        'F3':'zero data-bit XOR means zero work: FALSE',
                        'F4':'head code entropy distinguishes SAT from UNSAT: FALSE'}}
    for label,f,n in [('Y6_SAT',Y,6),('U198_UNSAT',U,198),('V198_SAT',V,198)]:
        assert valid(f,n)
        encoded=encoder(f,n)
        micro=microtrace(len(encoded))
        source={'label':label,'n':n,'m':len(f),'encoded_bits':len(encoded),
                'source_sha256':hashlib.sha256(encoded.encode()).hexdigest(),
                'controls':controls(f,n),'head_motion':micro,
                'head_motion_logspace':microtrace(len(encoded),max(2,(len(encoded).bit_length()-1).bit_length()-1)),
                'dpll_300':up_dpll(f,300)}
        if label=='Y6_SAT':
            source['exhaustive_models']=sum(all(x>0 for x in counts(f,a)) for a in itertools.product((0,1),repeat=n))
            assert source['exhaustive_models']==20
        if label=='V198_SAT':
            witness=list(map(int,W));assert all(x>0 for x in counts(f,witness))
            source['witness_sha256']=hashlib.sha256(W.encode()).hexdigest()
        data['sources'][label]=source
    out=P/'arc_index_head_xor291_raw.json';out.write_text(json.dumps(data,indent=2))
    compact={'run':'ARC-INDEX-HEAD-XOR291','sources':{k:{'label':v['label'],'n':v['n'],'encoded_bits':v['encoded_bits'],
           'head_motion':v['head_motion'],
           'head_motion_logspace':v['head_motion_logspace'],'dpll_300':v['dpll_300']} for k,v in data['sources'].items()},
           'flmv':data['flmv'],'full_native_SAT_solver_benchmarked':False,
           'logical_XOR_is_physical_lower_bound':False,'all_target_ARC_construction':'OPEN','P_vs_NP':'OPEN'}
    (P/'arc_index_head_xor291_summary.json').write_text(json.dumps(compact,indent=2))
    print(json.dumps(compact,indent=2))
if __name__=='__main__':main()