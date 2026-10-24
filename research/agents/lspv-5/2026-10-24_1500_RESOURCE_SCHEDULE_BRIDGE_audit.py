#!/usr/bin/env python3
"""Scheduled circuit controls. Python 3.10+, standard library.
Counters are abstract events, not RAM timings; no separation is inferred.
"""
from __future__ import annotations
import hashlib, itertools, json
from collections import Counter
from fractions import Fraction
from pathlib import Path

CHECKS=Counter()
def check(cond,group):
    CHECKS[group]+=1
    if not cond: raise AssertionError(group)

class LiveMachine:
    def __init__(self):
        self.live={}; self.next_id=0
        self.peak=self.reads=self.gates=self.drops=0
        self.frames=self.peak_frames=0
    def put(self,value):
        key=self.next_id; self.next_id+=1
        self.live[key]=value
        self.peak=max(self.peak,len(self.live))
        return key
    def read(self,value):
        self.reads+=1; return self.put(value)
    def nand(self,a,b):
        self.gates+=1; return self.put(1-(self.live[a]&self.live[b]))
    def invert(self,a):
        self.gates+=1; return self.put(1-self.live[a])
    def drop(self,*keys):
        for key in keys:
            del self.live[key]; self.drops+=1
    def xor(self,a,b):
        t=self.nand(a,b)
        u=self.nand(a,t); self.drop(a)
        v=self.nand(b,t); self.drop(b,t)
        out=self.nand(u,v); self.drop(u,v)
        return out
    def balanced(self,getbit,left,length):
        self.frames+=1; self.peak_frames=max(self.peak_frames,self.frames)
        if length==1: out=self.read(getbit(left))
        else:
            a=self.balanced(getbit,left,length//2)
            b=self.balanced(getbit,left+length//2,length//2)
            out=self.xor(a,b)
        self.frames-=1
        return out
    def run(self,getbit,q,mode):
        if mode=='balanced':
            if q<2 or q&(q-1): raise ValueError('balanced mode needs power of two')
            out=self.balanced(getbit,0,q)
        elif mode=='serial':
            out=self.read(getbit(0)); self.peak_frames=1
            for i in range(1,q): out=self.xor(out,self.read(getbit(i)))
        else: raise ValueError(mode)
        result=self.invert(out); self.drop(out)
        return dict(answer=self.live[result],gates=self.gates,reads=self.reads,
            drops=self.drops,commands=self.gates+self.reads+self.drops,
            peak_live_values=self.peak,peak_generator_frames=self.peak_frames,mode=mode)

def cycle_cnf(bits):
    q=len(bits)
    if q<3: raise ValueError('q>=3')
    clauses=[]
    for i,b in enumerate(bits):
        x=i+1; y=(i+1)%q+1; sy=y if b==0 else -y
        for j,base in enumerate(((-x,sy),(x,-sy))):
            u=q+2*i+j+1
            clauses.extend((base+(u,),base+(-u,)))
    return 3*q,tuple(clauses)

class Source:
    def __init__(self,n,clauses):
        self.n=n; self.clauses=clauses; self.reads=0
    def read(self,i,j):
        self.reads+=1; return self.clauses[i][j]
    def bit(self,i,q):
        return int(self.read(4*i,1)!=((i+1)%q+1))
    def recognize(self):
        m=len(self.clauses)
        if m<12 or m%4 or self.n!=3*(m//4): return None
        q=m//4
        for i in range(q):
            block=[]
            for j in range(4):
                if len(self.clauses[4*i+j])!=3: return None
                block.append(tuple(self.read(4*i+j,k) for k in range(3)))
            x=i+1; y=(i+1)%q+1; s=block[0][1]
            if abs(s)!=y: return None
            u=q+2*i+1; v=u+1
            if block!=[(-x,s,u),(-x,s,-u),(x,-s,v),(x,-s,-v)]: return None
        return q

def satisfies(n,clauses,assignment):
    return all(any(assignment[abs(l)-1]==int(l>0) for l in c) for c in clauses)
def brute(n,clauses,counts=False):
    total=0
    for a in itertools.product((0,1),repeat=n):
        if satisfies(n,clauses,a):
            total+=1
            if not counts: return True
    return total if counts else False

def adaptive(n,clauses,budget):
    # Domain: well-formed ordinary CNFs; outer syntax validation is charged separately.
    src=Source(n,clauses); q=src.recognize(); acquisition=src.reads
    if q is None:
        trials=literal_reads=0; answer=False
        for a in itertools.product((0,1),repeat=n):
            trials+=1; valid=True
            for clause in clauses:
                ok=False
                for l in clause:
                    literal_reads+=1
                    if a[abs(l)-1]==int(l>0): ok=True; break
                if not ok: valid=False; break
            if valid: answer=True; break
        return dict(answer=int(answer),mode='fallback',recognition_literal_reads=acquisition,
            fallback_assignments=trials,fallback_literal_reads=literal_reads,original_variables=n)
    mode='balanced' if (q&(q-1))==0 and budget>=q.bit_length()+2 else 'serial'
    r=LiveMachine().run(lambda i:src.bit(i,q),q,mode)
    r.update(q=q,recognition_literal_reads=acquisition,evaluation_source_reads=src.reads-acquisition,
        value_budget=budget,original_variables=n,clauses=len(clauses))
    return r

def beta(c): return ((c+2)/(c*c)-c)/2

def main():
    orientations=0; model_counts=[]; scaling=[]; controls_out=[]; endpoints=[]
    for q in range(3,9):
        for bits in itertools.product((0,1),repeat=q):
            n,cnf=cycle_cnf(bits); expected=int(sum(bits)%2==0)
            for budget in (4,100):
                r=adaptive(n,cnf,budget)
                check(r['answer']==expected,'hybrid_answers')
                check(r['gates']==4*q-3,'gate_count')
                check(r['commands']==10*q-7,'command_count')
                check(r['recognition_literal_reads']==12*q,'recognition_reads')
                check(r['evaluation_source_reads']==q,'rereads_charged')
                check(r['peak_live_values']<=budget,'value_budget')
                peak=q.bit_length()+2 if r['mode']=='balanced' else 4
                check(r['peak_live_values']==peak,'exact_peak')
            orientations+=1
    for q in (3,4):
        for bits in itertools.product((0,1),repeat=q):
            n,cnf=cycle_cnf(bits); count=brute(n,cnf,True)
            check(count==(0 if sum(bits)%2 else 2**(2*q+1)),'full_model_counts')
            model_counts.append(dict(q=q,bits=''.join(map(str,bits)),models=count))
    for q in (4,16,64,256,1024,4096):
        for label,bits in [('SAT',(0,)*q),('UNSAT',(1,)+(0,)*(q-1))]:
            n,cnf=cycle_cnf(bits)
            for budget in (4,100):
                r=adaptive(n,cnf,budget)
                check(r['answer']==int(label=='SAT'),'scaling_both_labels')
                h=q.bit_length()-1; r['label_control']=label
                r['logical_depth']=3*h+1 if r['mode']=='balanced' else 3*(q-1)+1
                r['sink_pin_wires']=8*q-7; r['fan_in']=2; r['fan_out']=2
                r['unfolded_operations']=6**h if r['mode']=='balanced' else 'not materialized'
                scaling.append(r)
    cube=tuple(tuple(j+1 if row[j]==0 else -(j+1) for j in range(3))
        for row in itertools.product((0,1),repeat=3))
    controls=[('cube-unsat',3,cube),('cube-sat',3,cube[:-1]),
        ('horn-unsat',2,((1,),(-1,2),(-2,))),('horn-sat',2,((1,),(-1,2))),
        ('xor-sat',2,((1,2),(-1,-2))),('xor-unsat',2,((1,2),(-1,-2),(1,),(2,))),
        ('components-sat',4,((1,2),(-3,4))),('components-unsat',4,((1,2),(-3,),(3,)))]
    n,cnf=cycle_cnf((0,0,0)); controls.append(('failed-template-sat',n,tuple(reversed(cnf))))
    for name,n,cnf in controls:
        r=adaptive(n,cnf,4)
        check(r['mode']=='fallback','fallback_selected')
        check(bool(r['answer'])==brute(n,cnf),'fallback_answers')
        r['name']=name; controls_out.append(r)
    cases=[('target',(11,10),(1,5),(6,5),(1,2),True),
        ('slow-generator',(7,5),(1,5),(6,5),(1,2),False),
        ('large-generator-memory',(11,10),(7,10),(6,5),(1,5),False),
        ('recomputation',(11,10),(1,5),(7,5),(1,2),False),
        ('alternative-box',(11,10),(1,5),(13,10),(3,10),True)]
    for name,ga,si,la,pi,expected in cases:
        gamma,sigma,lam,p=map(lambda x:Fraction(*x),(ga,si,la,pi))
        t=max(gamma,lam); s=max(sigma,p)
        c=Fraction(241,200) if t<Fraction(241,200) else t+Fraction(1,100)
        forbidden=c>max(Fraction(1),t) and s<beta(c)
        check(forbidden==expected,'endpoint_cases')
        endpoints.append(dict(name=name,t=str(t),s=str(s),c=str(c),beta=str(beta(c)),forbidden=forbidden))
    check(beta(Fraction(241,200))-Fraction(1,2)==Fraction(26279,23232400),'rational_margin')
    result=dict(status='COMPUTATIONAL; P versus NP OPEN',seed=None,
        exhaustive_orientation_instances=orientations,assignment_level_instances=len(model_counts),
        checks=dict(CHECKS),total_checks=sum(CHECKS.values()),failures=0,
        scaling=scaling,controls=controls_out,endpoint_cases=endpoints,model_counts=model_counts,
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        limitations=['Finite tests do not prove asymptotic bounds.',
        'Live-value counts exclude generator frames and address bits, charged in the theorem.',
        'Recognition and all evaluation rereads are counted.',
        'No all-input fast SAT schedule is constructed.'])
    out=Path(__file__).with_name('RESOURCE_SCHEDULE_BRIDGE_results.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('total_checks','failures','checks')},indent=2))
if __name__=='__main__': main()
