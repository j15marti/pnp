#!/usr/bin/env python3
"""Independent source-language/brute assignment crosscheck, not a physical TM."""
from random import Random
from itertools import product
import json,sys

def rho(i): return 2*i+(i.bit_count()&1)
def source(r,mask_rows):
    w=(6*r+1).bit_length(); N=(1<<w)-1
    core=[rho(i) for i in range(1,3*r+1)]
    spare=[i for i in range(1,N+1) if i not in set(core)]
    clauses=[]
    for g,ms in enumerate(mask_rows):
        for m in ms: clauses.append([(core[3*g+j],(m>>j)&1) for j in range(3)])
    for k in range(0,len(spare),3):
        batch=spare[k:k+3]
        for v in spare:
            if len(batch)==3: break
            if v not in batch: batch.append(v)
        clauses.append([(v,0) for v in batch])
    M=len(clauses)
    return '1'*N+'0'+'1'*M+'0'+''.join(f'{sgn}{vid:0{w}b}' for cl in clauses for vid,sgn in cl)

def decode(s):
    a=s.find('0');assert a>=0
    b=s.find('0',a+1); assert b>a
    N=a; M=b-a-1
    if not N or not M:return None
    w=N.bit_length()
    if (1<<w)-1!=N or len(s)!=b+1+3*M*(w+1):return None
    clauses=[];seen=[0]*(N+1)
    p=b+1
    for _ in range(M):
        row=[]
        for j in range(3):
            sg=int(s[p]);vid=int(s[p+1:p+w+1],2);p+=w+1
            if not (1<=vid<=N):return None
            row.append((vid,sg));seen[vid]+=1
        if len(set(vid for vid,_ in row))!=3:return None
        clauses.append(row)
    if any(x==0 for x in seen[1:]):return None
    return clauses

def actual_sat(rows,r,N):
    core=[rho(i) for i in range(1,3*r+1)]
    filler=set(range(1,N+1))-set(core)
    assignment={j:1 for j in filler}
    # Every valid two-field edit can affect at most two filler variables in
    # core clauses; independently test their four valuations and all core assignments.
    affected=sorted({vid for cl in rows[:8*r] for vid,_ in cl if vid in filler})
    if len(affected)>2:raise AssertionError('unexpected affected fillers')
    for a in range(1<<(3*r)):
        for i,v in enumerate(core):assignment[v]=(a>>i)&1
        for b in range(1<<len(affected)):
            for j,v in enumerate(affected):assignment[v]=(b>>j)&1
            if all(any((assignment[vid]^sgn)==1 for vid,sgn in cl) for cl in rows):
                return True
    return False

def run():
    rnd=Random(771023)
    out={'model':'full strict source parse, independently brute SAT witnesses','seed':771023,'cases':[]}
    for r,nchecks in [(1,None),(2,3000),(3,500)]:
        masks=[[1,2,3,4,5,6,7,7] for _ in range(r)]
        s=source(r,masks);N=s.find('0');M=s.find('0',N+1)-N-1
        p=list(range(N+M+2,len(s)))
        # Independent field enumeration (excludes two unary headers).
        tested=0;valid=0;invalid=0;unsat=0
        choices=list((i,j) for a,i in enumerate(p) for j in p[a+1:]) if nchecks is None else [(rnd.choice(p),rnd.choice(p)) for _ in range(nchecks)]
        for i,j in choices:
            if i==j:continue
            t=list(s)
            for q in (i,j):t[q]='0' if t[q]=='1' else '1'
            rows=decode(''.join(t));tested+=1
            if rows is None:invalid+=1;continue
            valid+=1
            if not actual_sat(rows,r,N):unsat+=1
        out['cases'].append({'r':r,'L':len(s),'tested':tested,'valid':valid,'invalid':invalid,'sat_failures':unsat})
        assert unsat==0
    return out
if __name__=='__main__':print(json.dumps(run(),indent=2))
