#!/usr/bin/env python3
"""SCOPED-BLOCK-REBUILDER92: source-name-preserving scoped compiler.
Restricted exact algorithm; NOT an all-input ARC contraction.
"""
from __future__ import annotations
from itertools import product
from math import isqrt, log2
import json

# Events: ("O", id), ("C", (signed literal, signed literal, signed literal)), ("D", id).
def scan(events):
    active=set(); previous=set(); cuts=[tuple()]; width=0; clauses=[]
    for evt in events:
        op=evt[0]
        if op=='O':
            x=evt[1]; assert x>0 and x not in previous
            active.add(x);previous.add(x)
        elif op=='C':
            lits=evt[1];assert len(lits)==3 and len({abs(t) for t in lits})==3
            assert all(abs(t) in active for t in lits)
            clauses.append(tuple(lits))
        elif op=='D':
            x=evt[1];assert x in active;active.remove(x)
        else:raise AssertionError(evt)
        cuts.append(tuple(sorted(active)));width=max(width,len(active))
    assert not active
    return cuts,width,clauses,len(previous)

def build_stream(clauses):
    first={};last={}
    for i,c in enumerate(clauses):
        for lit in c:
            v=abs(lit);first.setdefault(v,i);last[v]=i
    events=[]
    for i,c in enumerate(clauses):
        for v in sorted(v for v in first if first[v]==i):events.append(('O',v))
        events.append(('C',tuple(c)))
        for v in sorted((v for v in last if last[v]==i),reverse=True):events.append(('D',v))
    scan(events)
    return tuple(events)

def encode_length(events):
    _,_,clauses,n=scan(events);m=len(clauses)
    h=(64*(n+m+1)-1).bit_length()
    return (2+4*n+4*m)*h

def pin(events,v,bit,nextid):
    a,b=nextid,nextid+1
    events.extend((('O',a),('O',b)))
    z=v if bit else -v
    for u,t in product((1,-1),repeat=2):events.append(('C',(z,u*a,t*b)))
    events.extend((('D',b),('D',a)))
    return nextid+2

def make_child(block,left,right,left_bits,right_bits):
    assert len(left)==len(left_bits) and len(right)==len(right_bits)
    mapping={};out=[];nextid=1;alive=set();right_set=set(right)
    def local(v):
        nonlocal nextid
        if v not in mapping:mapping[v]=nextid;nextid+=1
        return mapping[v]
    for v in left:
        loc=local(v);out.append(('O',loc));alive.add(v)
    for v,bit in zip(left,left_bits):nextid=pin(out,local(v),bit,nextid)
    for ev in block:
        if ev[0]=='O':
            v=ev[1];loc=local(v);out.append(('O',loc));alive.add(v)
        elif ev[0]=='C':
            out.append(('C',tuple((local(abs(l)) if l>0 else -local(abs(l))) for l in ev[1])))
        else:
            v=ev[1]
            if v not in right_set:out.append(('D',local(v)));alive.remove(v)
    assert alive==right_set,(alive,right_set)
    for v,bit in zip(right,right_bits):nextid=pin(out,local(v),bit,nextid)
    for v in sorted(right,reverse=True):out.append(('D',local(v)))
    out=tuple(out);scan(out)
    return out

def dpll(clauses):
    def go(cs):
        while True:
            if not cs:return True
            if any(not c for c in cs):return False
            units=[c[0] for c in cs if len(c)==1]
            if not units:break
            lit=units[0]
            cs=tuple(tuple(z for z in c if z!=-lit) for c in cs if lit not in c)
        lit=cs[0][0]
        for chosen in (lit,-lit):
            rem=tuple(tuple(z for z in c if z!=-chosen) for c in cs if chosen not in c)
            if go(rem):return True
        return False
    return go(tuple(map(tuple,clauses)))

class Audit:
    def __init__(self):
        self.queries=0;self.skipped=0;self.child_max=0
        self.width_max=0;self.memo={};self.last=[]
    def solve(self,events,depth,blockmax=None):
        cuts,w,cl,n=scan(events)
        if depth==0 or len(events)<=5:return dpll(cl)
        if blockmax is None:blockmax=max(1,isqrt(len(events)))
        ranges=[(i,min(len(events),i+blockmax)) for i in range(0,len(events),blockmax)]
        reachable={()};information=[]
        for low,high in ranges:
            left=cuts[low];right=cuts[high];future=set()
            for ua in product((0,1),repeat=len(left)):
                if tuple(ua) not in reachable:continue
                for vb in product((0,1),repeat=len(right)):
                    common=set(left)&set(right)
                    if any(ua[left.index(x)]!=vb[right.index(x)] for x in common):
                        self.skipped+=1;continue
                    child=make_child(events[low:high],left,right,ua,vb)
                    _,ww,child_cl,_=scan(child)
                    self.width_max=max(self.width_max,ww)
                    self.child_max=max(self.child_max,encode_length(child))
                    if child not in self.memo:
                        self.queries+=1
                        self.memo[child]=self.solve(child,depth-1) if depth>1 else dpll(child_cl)
                    if self.memo[child]:future.add(tuple(vb))
            information.append({'left':len(left),'right':len(right),
                'left_reachable':len(reachable),'right_reachable':len(future)})
            reachable=future
            if not reachable:return False
        assert cuts[-1]==()
        self.last=information
        return () in reachable

def direct_pinned_block(block,left,right,ua,vb):
    # Independent exhaustive check; never used by the solver.
    fixed={}
    for v,bit in list(zip(left,ua))+list(zip(right,vb)):
        if v in fixed and fixed[v]!=bit:return False
        fixed[v]=bit
    cs=[e[1] for e in block if e[0]=='C']
    vs=sorted({abs(t) for c in cs for t in c}|set(left)|set(right))
    free=[v for v in vs if v not in fixed]
    for bits in product((0,1),repeat=len(free)):
        a={**fixed,**dict(zip(free,bits))}
        if all(any((a[abs(t)]==1) if t>0 else (a[abs(t)]==0) for t in c) for c in cs):
            return True
    return False

def tests():
    cases=[]
    all8=[tuple(((-1 if (bits>>i)&1 else 1)*(i+1)) for i in range(3))
          for bits in range(8)]
    for k in range(9):cases.append(('cube-%d'%k,all8[:k]))
    cases.extend([
        ('xor-sat',[all8[i] for i in [0,3,5,6]]),
        ('xor-unsat',all8),
        ('horn-sat',[(-1,2,3),(-2,3,4),(-3,4,5)]),
        ('horn-unsat',all8),
        ('2sat-pad-sat',[(1,2,3),(1,2,-3),(-1,4,5),(-1,4,-5)]),
        ('2sat-pad-unsat',all8),
        ('separate-yes',[(1,2,3),(4,5,6)]),
        ('separate-no',all8+[(4,5,6)]),
        ('indexed-easy',[(1,2,3),(1,-2,4),(-1,2,4),(-4,3,5)]),
        ('shared-pin-sat',[(t,u*a,v*b) for t,a,b in ((1,2,3),(1,4,5))
                            for u,v in product((1,-1),repeat=2)]),
        ('shared-pin-unsat',[(t,u*a,v*b) for t,a,b in ((1,2,3),(-1,4,5))
                              for u,v in product((1,-1),repeat=2)]),
    ])
    checked=0;data=[];pins_checked=0
    for name,clauses in cases:
        if not clauses:continue
        stream=build_stream(clauses)
        baseline=dpll(clauses)
        a=Audit();answer=a.solve(stream,1)
        assert baseline==answer,(name,baseline,answer)
        cuts,w,_,_=scan(stream)
        assert a.width_max<=w+2,(name,a.width_max,w)
        if checked<12:
            blockmax=max(1,isqrt(len(stream)))
            for low in range(0,len(stream),blockmax):
                high=min(len(stream),low+blockmax)
                left,right=cuts[low],cuts[high]
                for ua in product((0,1),repeat=len(left)):
                    for vb in product((0,1),repeat=len(right)):
                        child=make_child(stream[low:high],left,right,ua,vb)
                        expected=direct_pinned_block(stream[low:high],left,right,ua,vb)
                        assert dpll(scan(child)[2])==expected,(name,low,high,ua,vb)
                        pins_checked+=1
        data.append({'name':name,'label':int(answer),'source_N':encode_length(stream),
                     'w':w,'calls':a.queries,'largest_child_N':a.child_max})
        checked+=1
    for name,clauses in [('two-level-sat',[(1,2,3),(4,5,6)]),('two-level-unsat',all8)]:
        stream=build_stream(clauses)
        a=Audit();found=a.solve(stream,2)
        assert dpll(clauses)==found,(name,found)
        data.append({'name':name,'label':int(found),'source_N':encode_length(stream),
                     'w':scan(stream)[1],'calls':a.queries,'largest_child_N':a.child_max})
        checked+=1
    scaling=[]
    for m in (100,1000,10000):
        stream=build_stream([(1,2,3)]*m)
        cuts,w,_,_=scan(stream)
        b=max(1,isqrt(len(stream)))
        low=min(b,len(stream)-b);high=min(low+b,len(stream))
        child=make_child(stream[low:high],cuts[low],cuts[high],
                         tuple(1 for _ in cuts[low]),tuple(1 for _ in cuts[high]))
        sb,cb=encode_length(stream),encode_length(child)
        assert scan(child)[1]<=w+2
        scaling.append({'source_clauses':m,'source_bits':sb,'child_bits':cb,
            'source_width':w,'child_width':scan(child)[1],
            'apparent_exponent':round(log2(cb)/log2(sb),6)})
    return {'size_scaling':scaling,'pin_profile_checks':pins_checked,
       'test_cases':checked,'sat':sum(x['label'] for x in data),
       'unsat':sum(1-x['label'] for x in data),
       'max_calls':max(x['calls'] for x in data),
       'max_child_N':max(x['largest_child_N'] for x in data),
       'cases':data,'result':'COMPUTATIONAL: all checked labels matched'}

if __name__=='__main__':
    print(json.dumps(tests(),indent=2,sort_keys=True))
