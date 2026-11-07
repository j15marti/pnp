#!/usr/bin/env python3
"""LSPV-2/470 finite delay-prefix falsifier. Seek is symbolic, not a machine run."""
import itertools
import json
from collections import Counter

EDGES = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]

def k4(mask):
    out=[]
    for v in range(4):
        ids=[i+1 for i,(u,w) in enumerate(EDGES) if u==v or w==v]
        for bits in itertools.product((0,1),repeat=3):
            if sum(bits)%2!=(mask>>v)&1:
                out.append(tuple(-i if b else i for i,b in zip(ids,bits)))
    assert len(out)==16
    return out

def encode(clauses):
    return 'p cnf 6 16\n'+''.join(' '.join(f'{v:+02d}' for v in c)+' 0\n' for c in clauses)

def parse(source):
    lines=source.splitlines()
    if len(lines)!=17 or lines[0]!='p cnf 6 16': raise ValueError('header')
    out=[]
    for line in lines[1:]:
        tokens=line.split(' ')
        if len(tokens)!=4 or tokens[-1]!='0': raise ValueError('width')
        if any(len(v)!=2 or v[0] not in '+-' or v[1] not in '123456' for v in tokens[:3]):
            raise ValueError('literal')
        clause=tuple(map(int,tokens[:3]))
        if len({abs(v) for v in clause})!=3: raise ValueError('proper')
        out.append(clause)
    return out

def label(source):
    try: cnf=parse(source)
    except ValueError: return 'MALFORMED'
    for assignment in itertools.product((0,1),repeat=6):
        if all(any(assignment[abs(v)-1]==(v>0) for v in clause) for clause in cnf):
            return 'SAT'
    return 'UNSAT'

class Delayed:
    def __init__(self,source,k):
        self.source=source
        self.length=len(source)
        self.k=k
        self.clock=0
        self.limit=self.length**k
        self.lookups=0
    def step(self):
        if self.clock<self.limit:
            self.clock+=1
            return ('WAIT',self.length,self.k,self.clock)
        self.lookups+=1
        return ('ANSWER',label(self.source))
    def symbolic_seek_not_executed(self):
        self.clock=self.limit

def run():
    sources=[encode(k4(mask)) for mask in range(16)]
    assert len({len(s) for s in sources})==1
    labels=[label(s) for s in sources]
    assert labels.count('SAT')==8 and labels.count('UNSAT')==8
    bad=sources[0].replace('+1','?1',1)
    assert len(bad)==len(sources[0]) and label(bad)=='MALFORMED'
    sources.append(bad)
    tally=Counter()
    ratio={}
    n=len(sources[0])
    for k in (2,3,4):
        machines=[Delayed(s,k) for s in sources]
        for tick in range(200):
            states=[machine.step() for machine in machines]
            assert len(set(states))==1
            assert all(machine.lookups==0 for machine in machines)
            tally['executed_prefix_checks']+=len(machines)
        for machine,want in zip(machines,labels+['MALFORMED']):
            machine.symbolic_seek_not_executed()
            assert machine.step()==('ANSWER',want)
            tally['terminal_checks_after_symbolic_seek']+=1
        target=max(1.1,.6+k/2)
        assert target<k
        ratio[str(k)]={'delay_lower_bound_steps':n**k,
                       'contraction_time_exponent':target,
                       'delay_over_contraction_power':n**(k-target)}
    return {'source_bytes':n,'SAT':8,'UNSAT':8,'MALFORMED':1,
            'assertion_counts':dict(tally),'exponents':ratio,
            'warning':'200 actual prefix steps per case/k. Terminal step uses symbolic time skip; no native FLMV run. Brute-force finite control is not a polynomial SAT algorithm.'}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
