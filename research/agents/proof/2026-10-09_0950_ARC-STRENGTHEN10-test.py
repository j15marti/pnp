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
    root=Root(data,factor*n*max(1,b)); stack=[]; nodes=0; depth=0; splits=0; merges=0; comparisons=0
    def visit():
        nonlocal nodes,depth,splits,merges,comparisons
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
            if all(t is None for z,t in children):
                comparisons+=1
                if siblings_equal(root,stack,x):
                    merges+=1; stack.append((x,False))
                    try: return visit()
                    finally: stack.pop()
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
    return {'answer':result,'reason':reason,'events':root.used,'limit':root.limit,'nodes':nodes,'depth':depth,'splits':splits,'merges':merges,'comparisons':comparisons}


def tokens(root,assignment):
    for w,s,e in a.clauses(root):
        satisfied=False; kept=0
        for lit in a.literals(root,s,e):
            v=lookup(lit,assignment)
            satisfied |= v is True
            kept += v is None
        if satisfied: continue
        yield ('width',kept)
        for lit in a.literals(root,s,e):
            if lookup(lit,assignment) is None: yield ('literal',lit)

def siblings_equal(root,stack,x):
    left=tokens(root,tuple(stack)+((x,False),))
    right=tokens(root,tuple(stack)+((x,True),))
    missing=object()
    for l,r in itertools.zip_longest(left,right,fillvalue=missing):
        root.tick()
        if l!=r: return False
    return True

def main():
    start=time.monotonic(); tests=0; totals={'SAT':0,'UNSAT':0,'UNKNOWN':0}
    clauses=list(itertools.product(*[(i,-i) for i in (1,2,3)]))
    for mask in range(256):
        f=tuple(c for i,c in enumerate(clauses) if mask>>i&1); data=a.encode(f)
        result=solve(data); truth=a.sat(f)
        assert result['answer'] is None or result['answer']==truth
        totals['UNKNOWN' if result['answer'] is None else ('SAT' if result['answer'] else 'UNSAT')]+=1
        for x in (1,2,3):
            got=siblings_equal(Root(data,10**9),[],x)
            expected=a.encode(a.restrict(f,x,False))==a.encode(a.restrict(f,x,True))
            assert got==expected; tests+=1
    rows=[]
    for d in range(9):
        f=tuple(itertools.product(*[(i,-i) for i in (d+1,d+2,d+3)]))
        for z in range(d,0,-1): f=tuple((s,)+c for c in f for s in (z,-z))
        r=solve(a.encode(f)); assert r['answer'] is False and r['merges']>=d
        rows.append({'guards':d,'bits':len(a.encode(f))*8,'run':r})
    escapes=[]
    for k in (4,8,16,32):
        h=tuple(c for i in range(k) for c in ((2*i+2,2*i+3),(-2*i-2,-2*i-3)))
        g=tuple((z,)+c for c in h for z in (1,-1))
        r=solve(a.encode(g)); assert r['answer'] is None and r['merges']>=1
        escapes.append({'pairs':k,'run':r})
    # Equal-sized residuals can have opposite truth; cannot merge by size alone.
    f=((1,2),(1,-2),(-1,3),(-1,3)); data=a.encode(f)
    assert len(a.encode(a.restrict(f,1,False)))==len(a.encode(a.restrict(f,1,True)))
    assert not siblings_equal(Root(data,10**9),[],1)
    assert a.sat(a.restrict(f,1,False))!=a.sat(a.restrict(f,1,True))
    out={'status':'COMPUTATIONAL','semantic_cases':256,'totals':totals,'exact_comparison_checks':tests,'guards':rows,'remaining_escapes':escapes,'equal_size_opposite_truth_control':'PASS','runtime_seconds':time.monotonic()-start,'code_sha256':hashlib.sha256(P.read_bytes()).hexdigest()}
    P.with_name(P.name.replace('-test.py','-results.json')).write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
