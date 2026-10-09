#!/usr/bin/env python3
"""Exact encoded-size split acquisition; semantic test, not a full SAT compiler."""
import itertools, json, time, signal, hashlib
from pathlib import Path
signal.alarm(24)
Q=1<<20
class Unsupported(Exception): pass

def uleb(v):
    while v>=128:
        yield (v&127)|128; v >>= 7
    yield v

def encode(f):
    return bytes(itertools.chain(b'CNF1',uleb(max((abs(x) for c in f for x in c),default=0)),uleb(len(f)),*(itertools.chain(uleb(len(c)),*(uleb(2*abs(x)-(x>0)) for x in c)) for c in f)))

def uint(a,p,cap):
    v=0; shift=0
    while True:
        if p>=len(a) or shift>cap.bit_length()+7: raise Unsupported()
        b=a[p]; p+=1; v |= (b&127)<<shift
        if v>cap: raise Unsupported()
        if b<128: return v,p
        shift+=7

def clauses(a):
    if a[:4]!=b'CNF1': raise Unsupported()
    cap=8*len(a); _,p=uint(a,4,cap); k,p=uint(a,p,cap)
    for _ in range(k):
        w,p=uint(a,p,cap); start=p
        for _ in range(w):
            z,p=uint(a,p,2*cap)
            if not z: raise Unsupported()
        yield w,start,p
    if p!=len(a): raise Unsupported()

def literals(a,start,end):
    p=start
    while p<end:
        z,p=uint(a,p,16*len(a))
        yield (z+1)//2 if z&1 else -(z//2)

def residual_stats(a,x,b):
    k=0; maximum=0; payload=0; empty=False
    for w,s,e in clauses(a):
        satisfied=False; kept=0; width=0; cm=0
        for lit in literals(a,s,e):
            if abs(lit)==x:
                if (lit>0)==b: satisfied=True
            else:
                kept+=1; width+=len(tuple(uleb(2*abs(lit)-(lit>0)))); cm=max(cm,abs(lit))
        if not satisfied:
            k+=1; maximum=max(maximum,cm); payload+=len(tuple(uleb(kept)))+width
            empty |= kept==0
    bits=8*(4+len(tuple(uleb(maximum)))+len(tuple(uleb(k)))+payload)
    return {'bits':bits,'clauses':k,'maxvar':maximum,'terminal':False if empty else (True if k==0 else None)}

def emit(a,x,b):
    st=residual_stats(a,x,b)
    yield from b'CNF1'; yield from uleb(st['maxvar']); yield from uleb(st['clauses'])
    for w,s,e in clauses(a):
        satisfied=False; kept=0
        for lit in literals(a,s,e):
            if abs(lit)==x:
                satisfied |= (lit>0)==b
            else: kept+=1
        if satisfied: continue
        yield from uleb(kept)
        for lit in literals(a,s,e):
            if abs(lit)!=x: yield from uleb(2*abs(lit)-(lit>0))

def ceilroot5(n):
    lo=0; hi=1<<((n.bit_length()+4)//5)
    while lo<hi:
        mid=(lo+hi)//2
        if mid**5<n: lo=mid+1
        else: hi=mid
    return lo

def weight(m,n):
    # ceil(Q*(m/n)^(6/5)), certified with integer arithmetic.
    return ceilroot5((m**6*Q**5+n**6-1)//n**6)

def acquire(a):
    n=8*len(a); budget=0
    while (budget+1)**5<=n: budget+=1
    candidates=[]
    try:
        for w,s,e in clauses(a):
            for lit in literals(a,s,e):
                x=abs(lit)
                if x not in candidates and len(candidates)<budget: candidates.append(x)
        for x in candidates:
            st=[residual_stats(a,x,b) for b in (False,True)]
            if any(z['terminal'] is True for z in st): return {'kind':'VALUE','value':True,'pivot':x}
            unresolved=[z['bits'] for z in st if z['terminal'] is None]
            if not unresolved: return {'kind':'VALUE','value':False,'pivot':x}
            if 100*sum(weight(m,n) for m in unresolved)<=99*Q:
                return {'kind':'SPLIT','pivot':x,'stats':st,'parent_bits':n}
    except Unsupported:
        return {'kind':'UNKNOWN','reason':'unsupported or malformed encoding'}
    return {'kind':'UNKNOWN','reason':'no certified pivot within cap'}

def restrict(f,x,b):
    return tuple(tuple(l for l in c if abs(l)!=x) for c in f if not any(abs(l)==x and (l>0)==b for l in c))
def sat(f):
    vs=sorted({abs(l) for c in f for l in c})
    return any(all(any(a[abs(l)]==(l>0) for l in c) for c in f) for a in (dict(zip(vs,b)) for b in itertools.product((False,True),repeat=len(vs))))
def cyclic(n):
    f=[]
    for i in range(n):
        c=(i+1,(i+1)%n+1,-((i+2)%n+1)); f.extend((c,tuple(-l for l in c)))
    return tuple(f)

def main():
    start=time.monotonic(); counts={'formulas':0,'accessor_checks':0,'VALUE':0,'SPLIT':0,'UNKNOWN':0}
    # All subsets of the 8 proper 3-clauses over 3 variables.
    base=list(itertools.product(*[(i,-i) for i in (1,2,3)]))
    for mask in range(256):
        f=tuple(c for i,c in enumerate(base) if mask>>i&1); a=encode(f); truth=sat(f)
        r=acquire(a); counts['formulas']+=1; counts[r['kind']]+=1
        if r['kind']=='VALUE': assert r['value']==truth
        if r['kind']=='SPLIT':
            assert truth==any(sat(restrict(f,r['pivot'],b)) for b in (False,True))
        for x in (1,2,3):
            for b in (False,True):
                expected=encode(restrict(f,x,b)); got=bytes(emit(a,x,b))
                assert got==expected and residual_stats(a,x,b)['bits']==8*len(expected)
                counts['accessor_checks']+=1
    controls=[]
    for n in (5,6,8,16,32,64,128):
        f=cyclic(n); a=encode(f); sizes=[]
        for x in range(1,n+1):
            pair=[residual_stats(a,x,b)['bits'] for b in (False,True)]
            assert 100*sum(weight(m,len(a)*8) for m in pair)>99*Q
            sizes.append(pair)
        assert acquire(a)['kind']=='UNKNOWN'
        controls.append({'variables':n,'bits':len(a)*8,'min_child_bits':min(map(min,sizes)),'all_pivots_rejected':True})
    # Long clauses, duplicate literals, tautologies, empty clauses, large IDs.
    for f in [((1,-1,1),), ((),), ((1,1,2),(-1,-1,-2)),((1000000,),)]:
        r=acquire(encode(f))
        if r['kind']=='VALUE': assert r['value']==sat(f)
    wins=[]
    for k in (4,8,16,32):
        f=tuple(c for i in range(2,k+2) for c in ((1,i),(-1,-i)))
        r=acquire(encode(f)); assert r['kind']=='SPLIT'
        wins.append({'clauses':len(f),'bits':8*len(encode(f)),'children':[x['bits'] for x in r['stats']]})
    hard=tuple(tuple((abs(l)+1)*(1 if l>0 else -1) for l in c) for c in cyclic(5))
    guarded=tuple((s,)+c for c in hard for s in (1,-1))
    ga=encode(guarded); gr=acquire(ga)
    assert gr['kind']=='SPLIT' and gr['pivot']==1
    assert bytes(emit(ga,1,False))==bytes(emit(ga,1,True))==encode(hard)
    assert acquire(encode(hard))['kind']=='UNKNOWN'
    nonclosure={'parent_bits':len(ga)*8,'child_bits':len(encode(hard))*8,'duplicate_executions':2,'child_result':'UNKNOWN'}
    out={'nonclosure':nonclosure,'status':'COMPUTATIONAL','counts':counts,'split_wins':wins,'hostile_controls':controls,'runtime_seconds':time.monotonic()-start,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limitations':'Acquisition and sequential emitter only; no cheap recursive random-access interface or all-input coverage.'}
    Path(__file__.replace('-test.py','-results.json')).write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
