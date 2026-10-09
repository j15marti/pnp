#!/usr/bin/env python3
"""Flattened root-source replay. Bounded partial decision, not total SAT."""
import importlib.util, pathlib, itertools, json, time, signal, hashlib
P=pathlib.Path(__file__)
spec=importlib.util.spec_from_file_location('arc8',P.with_name('2026-10-09_0830_ARC-STRENGTHEN8-test.py'))
a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
signal.alarm(24)
class Exhausted(Exception): pass
class Root:
    def __init__(self,data,limit): self.data=data; self.limit=limit; self.used=0
    def tick(self,n=1):
        self.used+=n
        if self.used>self.limit: raise Exhausted()
    def __len__(self): return len(self.data)
    def __getitem__(self,k):
        self.tick(len(range(*k.indices(len(self.data)))) if isinstance(k,slice) else 1)
        return self.data[k]

def lookup(lit,stack):
    for x,b in reversed(stack):
        if abs(lit)==x: return (lit>0)==b
    return None

def scan(root,stack,cap):
    count=payload=maximum=0; empty=False; alltrue=allfalse=True; candidates=[]
    for w,s,e in a.clauses(root):
        satisfied=False; kept=width=cm=0; pos=neg=False
        for lit in a.literals(root,s,e):
            v=lookup(lit,stack)
            if v is True: satisfied=True
            elif v is None:
                kept+=1; width+=len(tuple(a.uleb(2*abs(lit)-(lit>0)))); cm=max(cm,abs(lit)); pos|=lit>0; neg|=lit<0
        if satisfied: continue
        count+=1; payload+=len(tuple(a.uleb(kept)))+width; maximum=max(maximum,cm)
        empty |= kept==0; alltrue &= pos; allfalse &= neg
        if len(candidates)<cap:
            for lit in a.literals(root,s,e):
                if lookup(lit,stack) is None:
                    root.tick(len(candidates)+1)
                    if abs(lit) not in candidates: candidates.append(abs(lit))
                    if len(candidates)>=cap: break
    bits=8*(4+len(tuple(a.uleb(maximum)))+len(tuple(a.uleb(count)))+payload)
    value=False if empty else (True if count==0 or alltrue or allfalse else None)
    return bits,value,candidates

def solve(data,factor=64):
    n=8*len(data); b=0
    while (b+1)**5<=n: b+=1
    root=Root(data,factor*n*max(1,b)); stack=[]; nodes=0; depth=0; splits=0
    def visit():
        nonlocal nodes,depth,splits
        nodes+=1; depth=max(depth,len(stack))
        m,value,vs=scan(root,stack,b)
        if value is not None: return value
        for x in vs:
            children=[]
            for val in (False,True):
                stack.append((x,val))
                try: z,t,_=scan(root,stack,0)
                finally: stack.pop()
                children.append((z,t))
            if any(t is True for z,t in children): return True
            if all(t is False for z,t in children): return False
            if 100*sum(a.weight(z,m) for z,t in children if t is None)>99*a.Q: continue
            splits+=1; unknown=False
            for val,(z,t) in zip((False,True),children):
                if t is False: continue
                stack.append((x,val))
                try: result=visit()
                finally: stack.pop()
                if result is True: return True
                unknown |= result is None
            return None if unknown else False
        return None
    reason='completed'
    try: result=visit()
    except Exhausted: result=None; reason='global_fuel'
    except a.Unsupported: result=None; reason='unsupported_encoding'
    return {'answer':result,'reason':reason,'events':root.used,'limit':root.limit,'nodes':nodes,'depth':depth,'splits':splits}

def main():
    begin=time.monotonic(); totals={'SAT':0,'UNSAT':0,'UNKNOWN':0}; cases=0; examples={}
    clauses=list(itertools.product(*[(i,-i) for i in (1,2,3)]))
    for mask in range(256):
        f=tuple(c for i,c in enumerate(clauses) if mask>>i&1)
        r=solve(a.encode(f)); truth=a.sat(f)
        if r['answer'] is not None: assert r['answer']==truth
        key='UNKNOWN' if r['answer'] is None else ('SAT' if r['answer'] else 'UNSAT'); totals[key]+=1; cases+=1
        if r['splits'] and 'recursive' not in examples: examples['recursive']={'formula':f,'run':r}
    hard=tuple(tuple((abs(l)+1)*(1 if l>0 else -1) for l in c) for c in a.cyclic(5))
    guarded=tuple((s,)+c for c in hard for s in (1,-1))
    examples['previous_nonclosure']=solve(a.encode(guarded)); assert examples['previous_nonclosure']['answer'] is True
    # Odd cycle of disequalities: UNSAT, each variable occurrence four.
    failures=[]
    for n in (5,9,17,33):
        f=tuple(c for i in range(1,n+1) for c in ((i,i%n+1),(-i,-(i%n+1))))
        r=solve(a.encode(f)); assert r['answer'] in (False,None)
        failures.append({'n':n,'run':r})
    escaped=[]
    for k in (4,8,16,32):
        h=tuple(c for i in range(k) for c in ((2*i+2,2*i+3),(-2*i-2,-2*i-3)))
        g=tuple((z,)+c for c in h for z in (1,-1))
        r=solve(a.encode(g)); assert r['answer'] is None and r['splits']>=1
        escaped.append({'pairs':k,'parent_bits':len(a.encode(g))*8,'child_bits':len(a.encode(h))*8,'run':r})
    examples['guarded_pair_escapes']=escaped
    # Header boundary, empty and repeated-literal controls.
    for f in [(),((),),((1,1),(-1,-1)),((127,),(-128,)),((1,-1),)]:
        r=solve(a.encode(f)); assert r['answer'] is None or r['answer']==a.sat(f)
    examples['fuel_zero']=solve(a.encode(guarded),factor=0); assert examples['fuel_zero']['answer'] is None
    out={'status':'COMPUTATIONAL','cases':cases,'totals':totals,'examples':examples,'odd_cycle_controls':failures,'runtime_seconds':time.monotonic()-begin,'code_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'limitations':'Fuel and failed gates return UNKNOWN. No total SAT algorithm, no arbitrary child-solver random-access adapter.'}
    P.with_name(P.name.replace('-test.py','-results.json')).write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
