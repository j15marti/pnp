#!/usr/bin/env python3
"""GUARDED-PROFILE-TRANSPORT86 independent compact verifier.
Python-stdlib experiment, NOT a FLMV runtime/space certificate."""
from itertools import product
from fractions import Fraction
import json

def width(n,m): return (64*(n+m+1)-1).bit_length()
def lit(v): return 2*abs(v)+int(v<0)
def encode(n,H):
    w=width(n,len(H)); fields=[n,len(H)]
    for c in H:
        assert len(c)==3 and len(set(map(abs,c)))==3
        fields += [3,*map(lit,c)]
    return ''.join(format(v,f'0{w}b') for v in fields)

def guard(n,H):
    m=len(H); x=n+m+1; out=[]
    for i,(a,b,c) in enumerate(H,1):
        out += [(-x,a,n+i),(-(n+i),b,c)]
    return x,out

def query_bit(n,H,k):
    m=len(H); v=n+m+1; w=width(v,2*m)
    assert 0<=k<(8*m+2)*w
    word,bit=divmod(k,w)
    if word<2: value=(v,2*m)[word]
    else:
        j,f=divmod(word-2,4); i,which=divmod(j,2)
        a,b,c=H[i]; aux=n+i+1
        fields=((3,lit(-v),lit(a),lit(aux)),
                (3,lit(-aux),lit(b),lit(c)))
        value=fields[which][f]
    return (value>>(w-1-bit))&1

def accepts(n,H,which=None):
    for assignment in product((0,1),repeat=n):
        if which is not None and assignment[-1]!=which: continue
        if all(any(assignment[abs(t)-1]==int(t>0) for t in clause)
               for clause in H): return True
    return False

def run():
    clauses=[tuple(-v if ((mask>>(v-1))&1) else v
                   for v in (1,2,3)) for mask in range(8)]
    checks=0; labels={"SAT":0,"UNSAT":0}
    for mask in range(1,256):
        H=[c for j,c in enumerate(clauses) if mask>>j&1]
        source=accepts(3,H)
        labels["SAT" if source else "UNSAT"]+=1
        nG,G=guard(3,H); serialized=encode(nG,G)
        assert len(serialized)==(8*len(H)+2)*width(nG,2*len(H))
        for k,b in enumerate(serialized):
            assert query_bit(3,H,k)==int(b)
            checks+=1
        assert accepts(nG,G)
        assert accepts(nG,G,0)
        assert accepts(nG,G,1)==source
        checks+=3
    U=clauses
    V=clauses[:-1]+[clauses[0]]
    for H,label in ((U,False),(V,True)):
        nG,G=guard(3,H)
        assert accepts(3,H)==label and accepts(nG,G)
        assert accepts(nG,G,1)==label
        assert len(encode(3,H))==340
        assert len(encode(nG,G))==726
        checks+=4
    c=Fraction(241,200)
    beta=((c+2)/c**2-c)/2
    assert beta==Fraction(11642479,23232400)>Fraction(1,2)
    print(json.dumps({"run":"GUARDED-PROFILE-TRANSPORT86-MINI",
          "source_cases":255,"assertions":checks,
          "matched_labels":labels,"beta":str(beta),"errors":0},
          indent=2,sort_keys=True))

if __name__=="__main__": run()
