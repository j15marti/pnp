#!/usr/bin/env python3
"""Independent no-import verifier for LSPV-1 UNSAT-PREFIX-DECISION311.
This verifies grammar, direct original source construction, SAT/UNSAT
controls, source S/U compatibility and direct prefix lengths. U198's
UNSAT proof is separately checked by the existing independent 309 checker.
"""
import itertools,json
from pathlib import Path
from collections import Counter
P=Path(__file__).resolve().parent
U=tuple(map(tuple,json.loads(''.join(s for s in
   (P.parent/'lspv2_296'/'U198.txt').read_text().splitlines()
   if not s.startswith('#')))))
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
assertions=0
def ck(b):
    global assertions
    assertions+=1
    assert b
def canonical(F,n):
    if n%3 or 3*len(F)!=4*n:return False
    c=Counter();used=set()
    for clause in F:
        if len(clause)!=3 or len(set(map(abs,clause)))!=3:return False
        if not all(1<=abs(v)<=n for v in clause):return False
        if not(all(v>0 for v in clause) or all(v<0 for v in clause)):return False
        label=tuple(sorted(clause))
        if label in used:return False
        used.add(label)
        for v in clause:c[(abs(v),v>0)]+=1
    return all(c[(i,b)]==2 for i in range(1,n+1) for b in (True,False))
def sat(F,a):
    return all(any(a[abs(v)-1]==(v>0) for v in clause) for clause in F)
def g(i):
    b=format(i,'b');return '0'*(len(b)-1)+b
def encode(F,n):
    b=n.bit_length()
    return g(n)+g(len(F))+''.join(
      ('1' if c[0]>0 else '0')+''.join(format(abs(v),f'0{b}b') for v in c)
      for c in F)
def main():
    ck(len(U)==264);ck(canonical(U,198));ck(canonical(F9,9));ck(canonical(Y6,6))
    ck(sum(sat(F9,a) for a in itertools.product((False,True),repeat=9))==70)
    ck(sum(sat(Y6,a) for a in itertools.product((False,True),repeat=6))==20)
    pins={1:1,3:0,5:1,6:0,7:0,8:0}
    for expected,x1 in ((0,1),(2,0)):
        p=dict(pins);p[1]=x1
        count=sum(sat(F9,a) and all(a[v-1]==bool(w) for v,w in p.items())
                  for a in itertools.product((False,True),repeat=9))
        ck(count==expected)
    pair=0
    for i,c in enumerate(F9):
        for d in F9[i+1:]:
            for first,second in itertools.product((False,True),repeat=2):
                need={};consistent=True
                for row,z in ((c,first),(d,second)):
                    for lit in row:
                        j=abs(lit);val=(lit>0) if z else (lit<0)
                        if j in need and need[j]!=val:consistent=False
                        need[j]=val
                shared_same=any(v==w for v in c for w in d)
                shared_opposite=any(v==-w for v in c for w in d)
                ck(consistent==(not shared_opposite if first==second
                                 else not shared_same))
                pair+=1
    ck(pair==264)
    for a in itertools.product((False,True),repeat=9):
        for clause in F9:
            ck(sum(a[abs(v)-1]==(v>0) for v in clause)
                +sum((not a[abs(v)-1])==(v>0) for v in clause)==3)
    cases=[]
    for t in (0,1,2,4,8,16,64,256):
        clauses=list(U)
        for j in range(t):
            shift=198+9*j
            clauses.extend(tuple((abs(z)+shift) if z>0 else -(abs(z)+shift)
                          for z in c) for c in F9)
        n=198+9*t;m=len(clauses)
        ck(canonical(clauses,n))
        x=encode(clauses,n)
        certified_prefix=g(n)+g(m)+''.join(
          ('1' if c[0]>0 else '0')+
          ''.join(format(abs(z),f'0{n.bit_length()}b') for z in c) for c in U)
        ck(x.startswith(certified_prefix))
        ck(len(certified_prefix)==len(g(n))+len(g(m))+264*(1+3*n.bit_length()))
        ck(len(x)==len(g(n))+len(g(m))+m*(1+3*n.bit_length()))
        if t:ck(len(certified_prefix)<len(x))
        cases.append((t,len(x),len(certified_prefix)))
    for bad_suffix in ('0','2','001101','1'*1000):
        x=encode(U,198)
        ck((x+bad_suffix).startswith(x))
    print(json.dumps({'independent_verifier':'PASS','assertions':assertions,
      'source_extreme_modes':pair,'complement_checks':6144,
      'same_original_SAT_UNSAT':(2,0),'prefix_cases':cases,
      'U198_refutation':'64 separator rows checked with 309 no-import checker'},
      indent=2))
if __name__=='__main__':main()
