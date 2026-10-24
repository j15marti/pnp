#!/usr/bin/env python3
"""CONTEXT-STREAM-QUOTIENT87, reproducible standard-library finite audit.
This is not an unrestricted SAT hardness theorem or ARC successor.
"""
from itertools import product
from math import ceil, log2
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json

class Builder:
    def __init__(self):
        self.v=0
        self.public=[]
        self.x_block=[]
        self.y_block=[]
    def new(self):
        self.v+=1
        return self.v
    def append(self,where,cl):
        assert len(cl)==3 and len({abs(z) for z in cl})==3
        assert all(z!=0 for z in cl)
        getattr(self,where).append(tuple(cl))
    def unit(self,lit,where):
        a,b=self.new(),self.new()
        for p,q in product((1,-1),repeat=2):
            self.append(where,(lit,p*a,q*b))
    def xor(self,a,b,c,where='public'):
        for va,vb,vc in product((0,1),repeat=3):
            if vc != (va^vb):
                self.append(where,tuple(-v if bit else v for v,bit in zip((a,b,c),(va,vb,vc))))
    def finish(self):
        return self.public+self.x_block+self.y_block

def build(h,x,y,kind):
    B=Builder()
    u=[B.new() for _ in range(h)]
    v=[B.new() for _ in range(h)]
    if kind=='eq':
        for a,b in zip(u,v):
            z,w=B.new(),B.new()
            for cl in ((-a,b,z),(-a,b,-z),(a,-b,w),(a,-b,-w)):
                B.append('public',cl)
        g,a,b=B.new(),B.new(),B.new()
        for p,q in product((1,-1),repeat=2):
            B.append('public',(g,p*a,q*b))
        for j in range(h-1):
            B.append('public',(g,u[j],u[j+1]))
    elif kind=='parity':
        r=[B.new() for _ in range(2*h+1)]
        for j,data in enumerate(u+v):
            B.xor(r[j],data,r[j+1])
        B.unit(-r[0],'public')
        B.unit(-r[-1],'public')
    else:
        raise ValueError(kind)
    for i,z in enumerate(u):
        B.unit(z if x[i] else -z,'x_block')
    for i,z in enumerate(v):
        B.unit(z if y[i] else -z,'y_block')
    f=B.finish()
    expected=(8*h+3,13*h+3) if kind=='eq' else (8*h+5,16*h+8)
    assert (B.v,len(f))==expected
    return B,f

def encode(B,clauses):
    n,m=B.v,len(clauses)
    w=ceil(log2(64*(n+m+1)))
    words=[n,m]
    for cl in clauses:
        words.extend((3,*[2*abs(lit)+(lit<0) for lit in cl]))
    assert len(words)==4*m+2
    assert all(0<=int(z)<2**w for z in words)
    raw=''.join(format(int(z),f'0{w}b') for z in words)
    return raw,w

def decode(raw,w):
    words=[int(raw[j:j+w],2) for j in range(0,len(raw),w)]
    n,m=words[:2]
    assert len(words)==4*m+2
    clauses=[]
    for j in range(m):
        typ,*lits=words[2+4*j:2+4*j+4]
        assert typ==3
        cl=tuple(-(z//2) if z%2 else z//2 for z in lits)
        assert all(0<abs(z)<=n for z in cl)
        clauses.append(cl)
    return n,clauses

def dpll(clauses,assign=None,counters=None):
    if assign is None: assign={}
    if counters is None: counters=Counter()
    counters['calls']+=1
    while True:
        reduced=[]
        units=[]
        for cl in clauses:
            active=[]
            satisfied=False
            for lit in cl:
                val=assign.get(abs(lit))
                if val is None:
                    active.append(lit)
                elif val==(lit>0):
                    satisfied=True
                    break
            if satisfied: continue
            if not active: return False
            if len(active)==1: units.append(active[0])
            reduced.append(tuple(active))
        if not reduced: return True
        changed=False
        for lit in units:
            var,truth=abs(lit),lit>0
            if var in assign:
                if assign[var]!=truth: return False
            else:
                assign[var]=truth
                changed=True
        if changed:
            clauses=reduced
            continue
        break
    counts=Counter(abs(lit) for cl in reduced for lit in cl)
    candidate=max(counts,key=lambda z:counts[z])
    for val in (True,False):
        trial=assign.copy()
        trial[candidate]=val
        if dpll(reduced,trial,counters): return True
    return False

def signature_rows(h,kind):
    m=1<<h
    return [tuple((x==y) if kind=='eq' else ((x^y).bit_count()%2==0)
                  for y in range(m)) for x in range(m)]

def pass_protocol(x,y,p):
    """Full-pass sign-field checker; actual padded bit-stream cost charged analytically."""
    h=len(x)
    z=(h+p-1)//p
    maxsaved=0
    reads=0
    for b in range(p):
        lo=b*z
        hi=min(h,(b+1)*z)
        saved=tuple(x[lo:hi])
        maxsaved=max(maxsaved,len(saved))
        reads+=2*h
        if saved!=tuple(y[lo:hi]):
            return False,maxsaved,reads
    return True,maxsaved,reads

def run():
    c=Counter()
    sizes={}
    dpll_calls=0
    labels=Counter()
    first_one={}
    for kind in ('eq','parity'):
        for h in range(1,7):
            rows=signature_rows(h,kind)
            q=len(set(rows))
            expected=(1<<h) if kind=='eq' else 2
            assert q==expected
            c['root_context_assertions']+=1
            if h==6:
                first_one[kind]=dict(h=h,classes=q,context_bits=ceil(log2(q)))
            x0=tuple(0 for _ in range(h))
            y0=x0
            B,F=build(h,x0,y0,kind)
            raw,w=encode(B,F)
            n,decoded=decode(raw,w)
            assert F==decoded and n==B.v
            sizes[f'{kind}_{h}']={'n':n,'m':len(F),'N':len(raw),'word_bits':w}
            c['encoding_checks']+=1
            for x in product((0,1),repeat=h):
                for y in product((0,1),repeat=h):
                    answer=(x==y) if kind=='eq' else ((sum(x)+sum(y))%2==0)
                    row=rows[int(''.join(map(str,x)),2)]
                    assert row[int(''.join(map(str,y)),2)]==answer
                    c['semantic_matrix_checks']+=1
                    for passes in range(1,h+1):
                        result,retained,reads=pass_protocol(x,y,passes)
                        assert result==(x==y)
                        assert retained<=(h+passes-1)//passes
                        assert reads<=passes*2*h
                        c['complete_pass_controls']+=1
                    parity_x=sum(x)%2
                    stream_result=(parity_x==sum(y)%2)
                    assert stream_result==((sum(x)+sum(y))%2==0)
                    c['onebit_parity_controls']+=1
                    if h<=3:
                        BB,FF=build(h,x,y,kind)
                        full,width=encode(BB,FF)
                        _,gg=decode(full,width)
                        assert FF==gg
                        assert len(full)==len(raw)
                        tally=Counter()
                        found=dpll(gg,{},tally)
                        dpll_calls+=tally['calls']
                        assert found==answer,(kind,h,x,y)
                        labels[(kind,'SAT' if found else 'UNSAT')]+=1
                        c['independent_dpll_checks']+=1
            assert q==len(set(signature_rows(h,kind)))
            c['repeat_context_checks']+=1
    for h in range(1,65):
        for p in range(1,16):
            lb=(h+2*p-2)//(2*p-1)
            assert (2*p-1)*lb>=h
            c['communication_arithmetic']+=1
    assert labels[('eq','SAT')]>0 and labels[('eq','UNSAT')]>0
    assert labels[('parity','SAT')]>0 and labels[('parity','UNSAT')]>0
    result={
        'run':'CONTEXT-STREAM-QUOTIENT87',
        'status':'COMPUTATIONAL finite checks, restricted theorem symbolic',
        'counts':dict(c),'dpll_recursive_calls':dpll_calls,
        'DPLL_controls':{'_'.join(k):v for k,v in labels.items()},
        'sizes':sizes,'largest_context':first_one,'discrepancies':0,
        'exclusions':['not arbitrary SAT decision lower bound',
                      'not FLMV random-access model',
                      'not all-input ARC successor',
                      'no cost-free contextual quotient']
    }
    data=json.dumps(result,sort_keys=True,indent=2)+'\n'
    with open(Path(__file__).with_name('CONTEXT87_raw.json'),'w') as fp:
        fp.write(data)
    print('checks',sum(c.values()),'DPLL calls',dpll_calls,
          'labels',result['DPLL_controls'],
          'SHA256',sha256(data.encode()).hexdigest())
    print('max sizes',sizes['eq_6'],sizes['parity_6'])

if __name__=='__main__':
    run()
