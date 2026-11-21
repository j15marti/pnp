"""T5-POSITIVE-OFFSET1: exact construction checks; no hardness claim."""
import itertools as it
import json, hashlib
from collections import Counter, deque
from functools import lru_cache
from pathlib import Path

TRIPLES={frozenset((i,(i+1)%5,(i+2)%5)) for i in range(5)}
def C(*a): return len(set(a))==3 and frozenset(a) in TRIPLES
TABLE=tuple(t for t in it.product(range(5),repeat=3) if C(*t))
def frame(a): return [tuple(a[(i+j)%5] for j in range(3)) for i in range(5)]
def exclusion(k,x,h): return [(k,x,h),((k+2)%5,(k+3)%5,h)]

def validate(p,gates,out):
    if type(p) is not int or p<1: raise ValueError('inputs')
    for i,g in enumerate(gates):
        if not g or g[0] not in ('not','or'): raise ValueError('gate')
        if len(g)!=(2 if g[0]=='not' else 3): raise ValueError('arity')
        if any(type(x) is not int or not 0<=x<p+i for x in g[1:]): raise ValueError('DAG')
    if type(out) is not int or not 0<=out<p+len(gates): raise ValueError('output')

def compile_circuit(p,gates,out):
    validate(p,gates,out)
    b=p+len(gates); nxt=5+b; cs=frame(list(range(5)))
    for x in range(5,5+b):
        for k in (2,3,4): cs+=exclusion(k,x,nxt); nxt+=1
    for i,g in enumerate(gates):
        x=5+p+i; u=5+g[1]
        if g[0]=='not': cs.append((2,u,x))
        else:
            v=5+g[2]; y,z=nxt,nxt+1; nxt+=2
            cs += [(1,2,y),(0,1,z),(4,u,y),(3,v,z),(x,y,z)]
    cs.append((0,2,5+out))
    return nxt,cs

def lift(p,gates,out):
    validate(p,gates,out)
    def shift(x): return x if x<p else x+1
    gg=[(g[0],*(shift(x) for x in g[1:])) for g in gates]
    gg.append(('or',p,shift(out)))
    return p+1,gg,p+1+len(gates)

def source_count(p,gates,out):
    validate(p,gates,out); z=0
    for a in it.product((0,1),repeat=p):
        a=list(a)
        for g in gates: a.append(1-a[g[1]] if g[0]=='not' else int(a[g[1]] or a[g[2]]))
        z+=a[out]
    return z

def encode(n,cs):
    assert all(len(set(t))==3 and all(0<=x<n for x in t) for t in cs)
    s=bin(len(cs)+1)[2:]; w=n.bit_length()
    return '1'*n+'0'+'0'*(len(s)-1)+s+''.join(format(x+1,f'0{w}b') for t in cs for x in t)

def decode(s):
    i=0
    while i<len(s) and s[i]=='1': i+=1
    n=i; i+=1; j=i
    while s[j]=='0': j+=1
    wgamma=j-i+1; m=int(s[j:j+wgamma],2)-1; i=j+wgamma; w=n.bit_length()
    assert len(s)-i==3*m*w
    cs=[]
    for _ in range(m):
        cs.append(tuple(int(s[i+k*w:i+(k+1)*w],2)-1 for k in range(3))); i+=3*w
    assert encode(n,cs)==s
    return n,cs

def split(n,cs):
    copies=[[] for _ in range(n)]; out=[]; nxt=0
    for t in cs:
        out.append(tuple(range(nxt,nxt+3)))
        for i,x in enumerate(t): copies[x].append(nxt+i)
        nxt+=3
    assert all(copies)
    E=0
    for xs in copies:
        for u,v in zip(xs,xs[1:]):
            a=[u]+list(range(nxt,nxt+4)); nxt+=4; E+=1
            out+=frame(a)+[(a[4],v,a[1])]
    return nxt,out,E

@lru_cache(None)
def supports(ds):
    ss=[0,0,0]
    for t in TABLE:
        if all(ds[i]&(1<<t[i]) for i in range(3)):
            for i in range(3): ss[i]|=1<<t[i]
    return tuple(ss)

def generic_count(n,cs):
    # All five colors initially allowed; no frame fixing or gate contraction.
    incident=[[] for _ in range(n)]
    for i,t in enumerate(cs):
        for x in t: incident[x].append(i)
    memo={}; calls=0
    def visit(ds):
        nonlocal calls
        calls+=1; ds=list(ds); q=deque(range(len(cs))); queued=set(q)
        while q:
            i=q.popleft(); queued.remove(i); t=cs[i]
            ss=supports(tuple(ds[x] for x in t))
            if not all(ss): return 0
            for x,s in zip(t,ss):
                if s!=ds[x]:
                    ds[x]=s
                    for j in incident[x]:
                        if j not in queued: q.append(j); queued.add(j)
        ds=tuple(ds)
        if ds in memo: return memo[ds]
        choices=[x for x in range(n) if ds[x].bit_count()>1]
        if not choices: return 1
        x=min(choices,key=lambda x:(ds[x].bit_count(),-len(incident[x]),x)); z=0
        for c in range(5):
            if ds[x]&(1<<c):
                dd=list(ds); dd[x]=1<<c; z+=visit(dd)
        memo[ds]=z; return z
    return visit((31,)*n),calls

def enumerate_gates(p,depth,prefix=()):
    if not depth:
        yield prefix; return
    b=p+len(prefix)
    for g in [('not',x) for x in range(b)]+[('or',x,y) for x in range(b) for y in range(b)]:
        yield from enumerate_gates(p,depth-1,prefix+(g,))

def main():
    cases=[(f'p{p}_g{g}_{i}',p,gs,p+g-1) for p in (1,2) for g in range(3)
           for i,gs in enumerate(enumerate_gates(p,g))]
    cases += [('false',1,(('not',0),('or',0,1),('not',2)),3),
              ('true',1,(('not',0),('or',0,1)),2),
              ('unused_input',3,(),0),
              ('shared_gate',2,(('or',0,1),('or',2,2),('not',3)),4)]
    rows=[]
    for name,p,gs,o in cases:
        z=source_count(p,gs,o); pp,gg,oo=lift(p,gs,o)
        assert source_count(pp,gg,oo)==2**p+z
        stages=[]
        for plus,ps,gates,out,expected in [(False,p,gs,o,z),(True,pp,gg,oo,2**p+z)]:
            b=ps+len(gates); nor=sum(g[0]=='or' for g in gates); nnot=len(gates)-nor
            n,cs=compile_circuit(ps,gates,out); bits=encode(n,cs)
            assert decode(bits)==(n,cs)
            assert (n,len(cs))==(5+4*b+2*nor,6+6*b+5*nor+nnot)
            got,calls=generic_count(n,cs); assert got==10*expected
            nn,ss,E=split(n,cs); sbits=encode(nn,ss)
            assert decode(sbits)==(nn,ss)
            assert E==13+14*b+13*nor+3*nnot
            assert (nn,len(ss))==(70+74*b+67*nor+15*nnot,84+90*b+83*nor+19*nnot)
            assert max(Counter(x for t in ss for x in t).values())<=5
            assert 3*len(ss)-nn==14*E
            row=dict(positive_lift=plus,n=n,m=len(cs),N=len(bits),count=got,generic_calls=calls,
                     E=E,n_split=nn,m_split=len(ss),N_split=len(sbits),split_count=got*2**E,
                     count_method='generic GAC unsplit; split count by equality theorem',
                     status='SAT' if got else 'UNSAT')
            if name in ('false','true'): row.update(clauses=cs,encoding=bits,split_clauses=ss)
            stages.append(row)
        a,d=stages
        assert (d['n']-a['n'],d['m']-a['m'],d['E']-a['E'])==(10,17,41)
        assert (d['n_split']-a['n_split'],d['m_split']-a['m_split'])==(215,263)
        threshold=10*2**(d['E']+p)
        assert (d['split_count']>threshold)==(z>0)
        assert d['split_count']>0
        # SAME encoded length and multiplier: change only the output pin in
        # the augmented circuit to the old output. The new selector is free.
        oldout=o if o<p else o+1
        nm,cm=compile_circuit(pp,gg,oldout); bm=encode(nm,cm)
        zm,calls=generic_count(nm,cm); assert zm==20*z
        nsm,csm,em=split(nm,cm); bsm=encode(nsm,csm)
        assert (nm,len(cm),len(bm),em,nsm,len(csm),len(bsm))==tuple(d[k] for k in ('n','m','N','E','n_split','m_split','N_split'))
        assert cm[:-1]==compile_circuit(pp,gg,oo)[1][:-1]
        assert (zm>0)==(z>0)
        assert d['split_count']==zm*2**em//2+threshold
        negative=dict(n=nm,m=len(cm),N=len(bm),count=zm,generic_calls=calls,E=em,
                      n_split=nsm,m_split=len(csm),N_split=len(bsm),split_count=zm*2**em,
                      status='SAT' if zm else 'UNSAT')
        if name=='false': negative.update(clauses=cm,encoding=bm,split_clauses=csm)
        rows.append(dict(name=name,p=p,gates=gs,out=o,source_count=z,threshold=threshold,stages=stages,negative_twin=negative))
    # Falsifier to SAT(output) iff SAT(source): source 'false' lifts to SAT.
    false=next(r for r in rows if r['name']=='false')
    assert false['source_count']==0 and false['stages'][1]['count']==20
    print(json.dumps(dict(lemma='T5-POSITIVE-OFFSET1',code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                         seed=None,cases=rows,case_count=len(rows),generic_target_counts=3*len(rows),
                         status='PASS; finite checks, not a lower bound or independent review'),separators=(',',':')))

if __name__=='__main__': main()
