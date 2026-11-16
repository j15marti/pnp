#!/usr/bin/env python3
"""Independent TMR-5/052 replay of TMR-3/055 with all-head oblivious macro schedule.
Checks authentic parsing, dual-rail source compiler, and exact physical head motions.
Python traces are *not* a native Turing microcode or a Lean proof.
"""
from __future__ import annotations
import json,random,hashlib,sys
from collections import Counter
from pathlib import Path
SEED=20261115
REV='tmr5-fullhead-cvp052.v1'
checks=Counter()
def ck(cond,label):
    if not cond: raise AssertionError(label)
    checks[label]+=1

def encode(g):
    n=len(g);assert n>=1
    rows=['1'*n+'0'];
    for j,(op,a,b) in enumerate(g):
        assert op in range(4)
        if op<2:assert a is None and b is None
        else:assert 0<=a<j and 0<=b<j
        rows += [format(op,'02b'), ''.join('1' if i==a else '0' for i in range(n)),
                 ''.join('1' if i==b else '0' for i in range(n))]
    return ''.join(rows)

def parse_authentic(s):
    if not s or any(c not in '01' for c in s):raise ValueError('nonbinary')
    n=0
    while n<len(s) and s[n]=='1':n+=1
    if not n or n>=len(s) or s[n]!='0':raise ValueError('header')
    N=2*n*n+3*n+1
    if len(s)!=N:raise ValueError('length')
    g=[]; pos=n+1
    for j in range(n):
        op=int(s[pos:pos+2],2);pos+=2
        masks=[]
        for t in range(2):
            bits=s[pos:pos+n];pos+=n
            ones=[i for i in range(n) if bits[i]=='1']
            if op<2:
                if ones:raise ValueError('constant mask')
                masks.append(None)
            else:
                if len(ones)!=1 or ones[0]>=j:raise ValueError('bad onehot')
                masks.append(ones[0])
        g.append((op,*masks))
    assert pos==N
    return g

def eval_mono(g):
    values=[]
    for op,a,b in g:
        values.append(op if op<2 else ((values[a] & values[b]) if op==2 else (values[a] | values[b])))
    return values

def eval_original(g):
    vals=[]
    for rec in g:
        if rec[0]=='c':v=rec[1]
        elif rec[0]=='not':v=1-vals[rec[1]]
        elif rec[0]=='and':v=vals[rec[1]]&vals[rec[2]]
        else:v=vals[rec[1]]|vals[rec[2]]
        vals.append(v)
    return vals[-1]

def dual_rail(g):
    out=[];rail=[]
    def cons(v):out.append((v,None,None));return len(out)-1
    def gate(o,a,b):out.append((o,a,b));return len(out)-1
    for rec in g:
        if rec[0]=='c': a=cons(rec[1]);b=cons(1-rec[1])
        elif rec[0]=='not':
            pa,pb=rail[rec[1]]
            a=gate(2,pb,pb);b=gate(2,pa,pa)
        else:
            pa,na=rail[rec[1]];pb,nb=rail[rec[2]]
            if rec[0]=='and':a=gate(2,pa,pb);b=gate(3,na,nb)
            else:a=gate(3,pa,pb);b=gate(2,na,nb)
        rail.append((a,b))
    gate(2,rail[-1][0],rail[-1][0])
    return out

def simulate_physical(s):
    # Complete source acquisition first. Authenticity ensures all later rows are legal.
    gates=parse_authentic(s);n=len(gates);N=len(s);d=2+2*n
    value=[0]*n; ip=0;vp=0; Im=Vm=reads=writes=0
    source_schedule=[];value_schedule=[];record_values=[]
    def iset(new):
        nonlocal ip,Im
        Im+=abs(ip-new);ip=new;source_schedule.append(ip)
    def vset(new):
        nonlocal vp,Vm
        Vm+=abs(vp-new);vp=new;value_schedule.append(vp)
    # Authentication fixed full scan and rewind.
    for p in range(1,N+1):iset(p)
    for p in range(N-1,-1,-1):iset(p)
    for j in range(n):
        # From left marker, physically traverse the entire record prefix.
        start=n+1+j*d
        for p in range(1,start+1):iset(p)
        op=int(s[ip:ip+2],2)
        iset(ip+1);iset(ip+1)  # read 2 op bits; source always advances
        # Mask A sweep
        A=0
        for i in range(n):
            ck(vp==i,'synchronized_first_mask')
            A|=(s[ip]=='1') & value[vp]
            reads+=1
            iset(ip+1)
            if i+1<n:vset(i+1)
        for i in range(n-2,-1,-1):vset(i)
        # Mask B sweep
        B=0
        for i in range(n):
            ck(vp==i,'synchronized_second_mask')
            B|=(s[ip]=='1') & value[vp]
            reads+=1
            iset(ip+1)
            if i+1<n:vset(i+1)
        # Back from high VALUE index to write slot j, then reset to zero.
        for i in range(n-2,j-1,-1):vset(i)
        val=op if op<2 else (A&B if op==2 else A|B)
        value[j]=val;writes+=1;record_values.append(val)
        for i in range(j-1,-1,-1):vset(i)
        # Source return all the way to the left marker, even for constants.
        for p in range(ip-1,-1,-1):iset(p)
    ck(ip==0 and vp==0,'heads_return_left')
    im_formula=2*N+2*n*(n+1)*(n+2)
    vm_formula=4*n*(n-1)
    ck(Im==im_formula,'exact_input_head_moves')
    ck(Vm==vm_formula,'exact_value_head_moves')
    ck(reads==2*n*n,'exact_value_reads')
    ck(writes==n,'exact_value_writes')
    ck(value==eval_mono(gates),'all_intermediate_gate_values')
    # Note the input schedule includes all intermediate positions and is independent of data.
    return {'answer':value[-1], 'n':n,'N':N,'input_moves':Im,
            'value_moves':Vm,'reads':reads,'writes':writes,
            'input_schedule_digest':hashlib.sha256(bytes((p%251 for p in source_schedule))).hexdigest(),
            'value_schedule_digest':hashlib.sha256(bytes((p%251 for p in value_schedule))).hexdigest(),
            'values':value}

def run():
    rng=random.Random(SEED);cases=0;duals=0;max_n=0
    for n in range(1,13):
        schedule_pair=None
        for trial in range(36):
            g=[]
            for j in range(n):
                op=(rng.randrange(2) if not j else rng.randrange(4))
                g.append((op,None,None) if op<2 else (op,rng.randrange(j),rng.randrange(j)))
            s=encode(g);res=simulate_physical(s)
            ck(res['answer']==eval_mono(g)[-1],'source_to_terminal')
            ck(res['N']==2*n*n+3*n+1,'exact_source_bit_length')
            key=(res['input_schedule_digest'],res['value_schedule_digest'])
            if schedule_pair is None:schedule_pair=key
            else:ck(key==schedule_pair,'both_heads_source_independent')
            cases+=1;max_n=max(max_n,n)
        zero=encode([(0,None,None)]*n)
        one=encode([(1,None,None)]*n)
        z=simulate_physical(zero);o=simulate_physical(one)
        ck((z['input_schedule_digest'],z['value_schedule_digest'])==
           (o['input_schedule_digest'],o['value_schedule_digest']) and z['answer']==0 and o['answer']==1,
           'same_both_head_graph_opposite_answers')
    for gsize in range(1,11):
        for trial in range(38):
            g=[]
            for j in range(gsize):
                op=rng.choice(['c','c','not','and','or']) if j else 'c'
                if op=='c':g.append(('c',rng.randrange(2)))
                elif op=='not':g.append((op,rng.randrange(j)))
                else:g.append((op,rng.randrange(j),rng.randrange(j)))
            mono=dual_rail(g)
            res=simulate_physical(encode(mono))
            ck(res['answer']==eval_original(g),'fully_charged_dualrail_output')
            ck(len(mono)==2*len(g)+1,'linear_gate_reduction')
            duals+=1;max_n=max(max_n,len(mono))
    s=encode([(0,None,None),(1,None,None),(2,0,1)])
    malformed=['', '0','1'*3,'2',s+'0',s[:-1], '00'+s]
    chars=list(s)
    n=3;start=n+1+2*(2+2*n)+2
    chars[start]='1';chars[start+1]='1';malformed.append(''.join(chars))
    for bad in malformed:
        try:parse_authentic(bad)
        except ValueError:checks['malformed_reject']+=1
        else:raise AssertionError('malformed accepted')
    return {'revision':REV,'seed':SEED,'python':sys.version.split()[0],
        'cases':cases,'dual_rail_reductions':duals,'max_gates':max_n,
        'assertions':sum(checks.values()),'by_category':dict(checks),
        'failures':0,'symbolic_claim':'For each n>=1, every accepted source has the SAME complete INPUT and VALUE head macro schedules; output remains P-complete via logarithmic-space dual-rail CVP reduction. Auxiliary counter heads can be padded to fixed schedules.',
        'exact_ledger':{'source_length':'N=2n^2+3n+1','source_head_moves':'2N+2n(n+1)(n+2)','value_head_moves':'4n(n-1)','value_reads':'2n^2','value_writes':'n','time':'O(n^3 log(n+2)) padded bit-machine upper bound','peak_space':'O(n+log(n+2)) writable bits'},
        'limitations':['Macro-head traces from Python, not full native TM transition replay','No Lean formalization or lower bound L!=P','Ordinary bit-model padded-counter schedule symbolic, not independently microcoded','Only valid equal-n inputs have common head schedule']}

if __name__=='__main__':
    x=run()
    path=Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:x[k] for k in ('cases','dual_rail_reductions','max_gates','assertions','failures')},indent=2))
