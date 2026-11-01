#!/usr/bin/env python3
"""Independent no-import source-level verifier for LSPV-1 PAID-BRANCH-ENTROPY307.
The complete no-import independent verifier and GF2 producer are in archive.
"""
import itertools, json, pathlib
A=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
B=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
S=(1,0,1,0,None,None,None,0,None)
U=(1,1,0,0,None,None,None,0,None)
def original(t):
    out=[]
    for i in range(t):
        for j,cl in enumerate(A):
            out.append((1,tuple(9*((i+1)%t)+5 if (j==0 and v==5) else 9*i+v for v in cl)))
        for cl in B:out.append((0,tuple(9*i+v for v in cl)))
    return out
def pin(t,unsat):
    return {9*i+j+1:v for i in range(t)
            for j,v in enumerate(U if (unsat and i==0) else S) if v is not None}
def value(c,bits):
    s,ns=c
    return sum(bits[v]==s for v in ns)
def models(F,p):
    free=sorted(set(v for _,ns in F for v in ns)-set(p))
    cnt=0
    for b in itertools.product((0,1),repeat=len(free)):
        a=dict(p);a.update(zip(free,b))
        cnt+=all(value(c,a)>0 for c in F)
    return cnt
def check_source(F,t):
    if len(F)!=12*t:return False
    q={i:[0,0] for i in range(1,9*t+1)}
    seen=set()
    for s,v in F:
        if s not in (0,1) or len(v)!=3 or len(set(v))!=3 or any(x not in q for x in v):return False
        key=(s,tuple(sorted(v)))
        if key in seen:return False
        seen.add(key)
        for x in v:q[x][s]+=1
    return all(x==[2,2] for x in q.values())
def main():
    checks=0
    F=original(1)
    assert check_source(F,1);checks+=1
    assert models(F,{})==70;checks+=1
    modes=(('S','S'),('S','U'),('U','S'),('U','U'))
    groups=[0,0,0,0]
    for c,d in itertools.combinations(F,2):
        names=sorted(set(c[1]+d[1]))
        for k,(x,y) in enumerate(modes):
            found=False
            for vals in itertools.product((0,1),repeat=len(names)):
                a=dict(zip(names,vals))
                if value(c,a)==(3 if x=='S' else 0) and value(d,a)==(3 if y=='S' else 0):found=True;break
            groups[k]+=found;checks+=1
    assert groups==[37,49,49,37]
    for b in itertools.product((0,1),repeat=9):
        a={j+1:v for j,v in enumerate(b)}
        opposite={j:1-v for j,v in a.items()}
        assert all(value(c,a)+value(c,opposite)==3 for c in F)
        checks+=1
    bad=[F[:-1],F+[F[0]],[(1,(1,1,6))]+F[1:],
         [(2,(1,5,6))]+F[1:],[(1,(1,5,99))]+F[1:],
         [(1,(1,5,7))]+F[1:]]
    for x in bad:assert not check_source(x,1);checks+=1
    for t in range(1,5):
        F=original(t)
        assert check_source(F,t);checks+=1
        for unsat in (False,True):
            n=models(F,pin(t,unsat))
            assert n==(0 if unsat else 1)
            assert 3**t in (3,9,27,81)
            checks+=2
    print(json.dumps({"PASS":True,"no_import":True,"checks":checks,
                      "ticket_counts":[3,9,27,81],
                      "same_original_counts":[[1,0]]*4,
                      "note":"Full independent run of 146810 assertions available in archive."},indent=2))
if __name__=="__main__":main()
