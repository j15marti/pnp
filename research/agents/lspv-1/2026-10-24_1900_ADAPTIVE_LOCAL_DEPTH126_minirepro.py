#!/usr/bin/env python3
"""ADAPTIVE-LOCAL-DEPTH126: finite reproducibility controls only.
No P!=NP claim, and Python memory/runtime is NOT FLMV machine accounting.
"""
from itertools import product
import json, hashlib

def unit(ell,a,b):
    return [(ell,i*a,j*b) for i,j in product((1,-1),repeat=2)]

def build(unsat,k=0):
    core=[]
    for i in range(8):
        scope=(1,2,3) if unsat else (3*i+1,3*i+2,3*i+3)
        bits=tuple((i>>(2-j))&1 for j in range(3))
        core.append(tuple(-scope[j] if bits[j] else scope[j] for j in range(3)))
    bridges=[(25,i,27+i) for i in range(1,25)]
    padding=[(25,52+2*j,53+2*j) for j in range(k)]
    return tuple(core+bridges+unit(25,26,27)+padding)

def profile(cl):
    return tuple(int(any((b[i]==1 if cl[i]>0 else b[i]==0)
                         for i in range(3)))
                 for b in product((0,1),repeat=3))

def pin(cl,b):
    src=tuple((1 if x>0 else -1)*(i+1) for i,x in enumerate(cl))
    return (src,)+tuple(sum((unit(i+1 if b[i] else -(i+1),
                                  4+2*i,5+2*i) for i in range(3)),[]))

def eval_clause(cl,a):
    return any(a.get(abs(x),-1)==int(x>0) for x in cl)

def simplify(clauses,assignment):
    out=[]
    for c in clauses:
        if any(eval_clause((x,),assignment) for x in c
               if abs(x) in assignment):continue
        t=tuple(x for x in c if abs(x) not in assignment)
        if not t:return None
        out.append(t)
    return out

def dpll(clauses,assignment=None,stats=None):
    if assignment is None:assignment={}
    if stats is None:stats={'nodes':0,'unit':0,'pure':0}
    stats['nodes']+=1
    while True:
        if not clauses:return assignment
        if any(not c for c in clauses):return None
        one=next((c[0] for c in clauses if len(c)==1),None)
        if one is not None:
            v,val=abs(one),int(one>0)
            if v in assignment and assignment[v]!=val:return None
            assignment={**assignment,v:val};stats['unit']+=1
            clauses=simplify(clauses,assignment)
            if clauses is None:return None
            continue
        signs={}
        for c in clauses:
            for x in c:signs.setdefault(abs(x),set()).add(x>0)
        pv=next(((v,next(iter(ss))) for v,ss in signs.items()
                 if len(ss)==1),None)
        if pv:
            assignment={**assignment,pv[0]:int(pv[1])};stats['pure']+=1
            clauses=simplify(clauses,assignment)
            if clauses is None:return None
            continue
        break
    v=abs(clauses[0][0])
    for val in (1,0):
        trial={**assignment,v:val}
        simp=simplify(clauses,trial)
        if simp is not None:
            ans=dpll(simp,trial,stats)
            if ans is not None:return ans
    return None

def oracle(source):
    """Adaptive clause-local schedule; no parent variable IDs exposed."""
    queries=[];state=0xA5712
    for j in range(512):
        ix=(state*73+11*j+17)%len(source)
        b=((state>>3)^j^ix)%8
        bits=((b>>2)&1,(b>>1)&1,b&1)
        child=(tuple(source[ix]),)
        depth=((state>>7)+j)%4
        for d in range(depth):
            y=child[(state+d)%len(child)]
            child=pin(y,bits)
        answer=profile(child[(state+j)%len(child)])[b]
        queries.append((ix,depth,b,answer))
        state=(state*1664525+1013904223+answer*7919+ix)%2**32
    return queries

def main():
    assert all(profile((-1,-2,-3))[i] in (0,1) for i in range(8))
    results={}
    for k in (0,1,4,32):
        U,V=build(True,k),build(False,k)
        assert len(U)==len(V)==36+k
        assert max(abs(x) for c in U for x in c)==51+2*k
        assert max(abs(x) for c in V for x in c)==51+2*k
        assert len(set(U))==len(U) and len(set(V))==len(V)
        assert all(len(set(map(abs,c)))==3 for c in U+V)
        assert [profile(c) for c in U]==[profile(c) for c in V]
        a,b={'nodes':0,'unit':0,'pure':0},{'nodes':0,'unit':0,'pure':0}
        assert dpll(list(U),stats=a) is None
        witness=dpll(list(V),stats=b)
        assert witness is not None
        assert all(eval_clause(c,witness) for c in V)
        assert oracle(U)==oracle(V)
        if k==0:
            for c,d in zip(U,V):
                for row in product((0,1),repeat=3):
                    idx=4*row[0]+2*row[1]+row[2]
                    assert profile(c)[idx]==int(any(
                        row[i]==int(c[i]>0) for i in range(3)))
                    assert [profile(x) for x in pin(c,row)]==[
                        profile(x) for x in pin(d,row)]
        results[k]={'n':51+2*k,'m':36+k,
                    'N':(4*(36+k)+2)*((64*(88+3*k)-1).bit_length()),
                    'U_dpll':a,'V_dpll':b,'same_512_queries':True}
    U,V=build(True),build(False)
    results['sha_unsat']=hashlib.sha256(repr(U).encode()).hexdigest()
    results['sha_sat']=hashlib.sha256(repr(V).encode()).hexdigest()
    results['status']='COMPUTATIONAL controls; theorem separately by induction'
    print(json.dumps(results,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
