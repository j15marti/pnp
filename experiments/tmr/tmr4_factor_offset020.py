#!/usr/bin/env python3
"""TMR-4/020: independent native, finite physical-tape test of a noninjective
factor-and-offset relational quotient.  This is a finite audit, not a TM compiler.
Run: python tmr4_factor_offset020.py > tmr4_factor_offset020_raw.json
"""
import json
from itertools import product

SHIFTS = (0, 1, 2, 3, 4, 7)
F = lambda c: c & 1  # noninjective: {0,2}->0 and {1,3}->1


def source(x, p):
    assert 0 <= p <= len(x)+1
    return '<' if p == 0 else '>' if p == len(x)+1 else x[p-1]


def label(x):
    if len(x)%3: return 'MALFORMED'
    mask = 0
    for j in range(0,len(x),3):
        mask |= 1 << int(x[j:j+3],2)
    return 'UNSAT' if mask == 255 else 'SAT'


def make(d, abstract):
    return dict(phase='U' if d else 'S', left=d, p=0, bh=0, ch=0,
                B={}, C={}, bv={0}, cv={0}, mask=0, buf='', label='', t=0,
                abstract=abstract)


def cell(t,k): return t.get(k,0)


def step(s,x):
    p, ph, q = s['p'],s['phase'],len(x)+1
    reading=source(x,p)
    if ph=='U':
        assert s['left'] > 0 and p==0
        s['ch']+=1; s['cv'].add(s['ch']); s['left']-=1
        if not s['left']:s['phase']='S'
    elif ph=='S':
        assert p<q
        if reading=='1':
            c=cell(s['C'],s['ch']); s['C'][s['ch']]=(c+1)%4
            if not s['abstract']:
                b=cell(s['B'],s['bh']); s['B'][s['bh']]=(b+1)%2
        s['p']+=1
        if s['p']==q:s['phase']='R'
    elif ph=='R':
        assert p>0
        s['p']-=1
        if s['p']==0:
            read=F(cell(s['C'],s['ch'])) if s['abstract'] else cell(s['B'],s['bh'])
            s['phase']='D' if read else 'A'
    elif ph=='D':
        assert p<q
        s['p']+=1
        if s['p']==q:s['phase']='E'
    elif ph=='E':
        assert p>0
        s['p']-=1
        if s['p']==0:s['phase']='A'
    elif ph=='A':
        if p==q:
            s['label']='MALFORMED' if s['buf'] else 'UNSAT' if s['mask']==255 else 'SAT'
            s['phase']='H'
        else:
            assert reading in ('0','1','<')
            if reading in ('0','1'):
                s['buf']+=reading
                if len(s['buf'])==3:
                    s['mask']|=1<<int(s['buf'],2);s['buf']=''
            s['p']+=1
    else:raise AssertionError('halted')
    s['t']+=1


def potential(s,x):
    q=len(x)+1; p=s['p']; z=sum(ch=='1' for ch in x)%2
    return dict(U=s['left']+3*q+1+2*q*z,
                S=3*q-p+1+2*q*z,
                R=p+q+1+2*q*z,
                D=3*q-p+1,
                E=p+q+1,
                A=q-p+1,
                H=0)[s['phase']]


def relation(c,a,d,x):
    for k in ('phase','left','p','bh','ch','mask','buf','label','t'):
        assert c[k]==a[k], (k,c[k],a[k])
    assert c['C']==a['C'] and c['bv']==a['bv'] and c['cv']==a['cv']
    if c['phase']=='U':
        assert c['bh']==0 and c['ch']==d-c['left'] and c['p']==0
        assert not c['B'] and not c['C']
    else:
        assert c['ch']==c['bh']+d
        all_j=set(c['B'])|{j-d for j in c['C']}|{c['bh']}
        for j in all_j:
            if j>=0:assert cell(c['B'],j)==F(cell(c['C'],j+d))
        # Source-aware phase fact, only used on source-reachable graph.
        amount=sum(ch=='1' for ch in x[:max(0,c['p']-1)]) if c['phase']=='S' else x.count('1')
        assert cell(c['C'],c['ch'])==amount%4 if c['phase']=='S' else F(cell(c['C'],c['ch']))==amount%2


def cert_scan():
    # Finite transition-table proof obligations for diagonal *factor* reads.
    # For all certified alphabet values and all source symbols, B writes f(C').
    checks=0; missing=0
    for old in range(4):
        for read in ('0','1','<','>'):
            B=F(old); C=old
            if read=='1':B=(B+1)%2;C=(C+1)%4
            assert B==F(C);checks+=1
    for b,c in product(range(2),range(4)):
        if b != F(c):missing+=1
    assert missing==4
    return checks,missing


def dynamic_bad(d):
    # Start from genuinely related data (B[0]=1,C[d]=1); change only C head.
    B={0:1}; C={d:1}; bh=0; ch=d
    assert cell(B,bh)==F(cell(C,ch))
    ch+=1; derived=ch-bh
    assert cell(B,bh)!=F(cell(C,bh+derived))
    # A quotient that reinterprets offset using head difference now reads 0
    # instead of the genuine physical B[0]=1, losing the expensive detour.
    return True


def audit():
    out=dict(id='TMR4-FO20',model='fixed offset noninjective tape factor',
        implementation='native CPython, independently implemented; no generic TM compiler',
        status='COMPUTATIONAL tests; restricted theorem symbolic; arbitrary 3-SAT processing OPEN',
        shifts=list(SHIFTS),cases=0,steps=0,source_current_cell_reads=0,
        SAT=0,UNSAT=0,MALFORMED=0,odd=0,bellman=0,
        certified_scan_tuples=0,off_factor_pairs=0,dynamic_offset_falsifiers=0,
        off_invariant_gate_witnesses=0,off_invariant_omitted_steps=0,max_source_len=0,errors=0)
    a,b=cert_scan();out['certified_scan_tuples']=a;out['off_factor_pairs']=b
    for d in SHIFTS:
        out['dynamic_offset_falsifiers']+=int(dynamic_bad(d))
    samples=['']
    for n in range(1,10):
        samples.extend(''.join(bits) for bits in product('01',repeat=n))
    samples.extend([''.join(format(j,'03b') for j in range(8)), '0'*45, '1'*51,'100'*16,'101'*17])
    for d in SHIFTS:
        for x in samples:
            c=make(d,False);a=make(d,True)
            relation(c,a,d,x)
            q=len(x)+1;z=x.count('1')%2
            expected_t=d+3*q+1+2*q*z
            assert potential(a,x)==expected_t
            while c['phase']!='H':
                old=potential(a,x);pr=c['p'];ph=c['phase']
                step(c,x);step(a,x)
                relation(c,a,d,x)
                assert old==1+potential(a,x), (d,x,ph,old,potential(a,x))
                out['steps']+=1;out['bellman']+=1
                if ph in ('S','A') and pr>0 and pr<q:
                    out['source_current_cell_reads']+=1
            assert c['label']==a['label']==label(x)
            assert c['t']==a['t']==expected_t and potential(a,x)==0
            assert len(c['bv'])+len(c['cv'])==d+2
            out[c['label']]+=1;out['cases']+=1;out['odd']+=z
            out['max_source_len']=max(out['max_source_len'],len(x))
        for x in ('1','001','1'*9):
            c=make(d,False);a=make(d,True);q=len(x)+1
            # Off-invariant states: the alleged B factor is wrong.
            c.update(phase='R',left=0,p=1,bh=0,ch=d,B={0:1},C={d:0})
            a.update(phase='R',left=0,p=1,bh=0,ch=d,C={d:0})
            while c['phase']!='H':step(c,x)
            while a['phase']!='H':step(a,x)
            assert c['label']==a['label'] and c['t']-a['t']==2*q
            out['off_invariant_gate_witnesses']+=1
            out['off_invariant_omitted_steps']+=2*q
    return out

if __name__=='__main__':print(json.dumps(audit(),sort_keys=True,indent=2))
