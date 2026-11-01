#!/usr/bin/env python3
"""Exact XP parameterized signed-slack affine SAT/#SAT terminal.
Original-source proper monotone 3-SAT-(2,2), complete SAT and UNSAT
on residuals with r<=cap. This is NOT a uniform polynomial SAT solver.
Compact independently rerunnable counterpart to LSPV-2 report296.
"""
from itertools import product
from collections import Counter

Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
N15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-v for v in c) for c in N15)
F9_U={8:0,3:0,7:0,6:0,1:1,5:1}
F15_U=dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))
F15_S=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))

def valid(F):
    if not F: return False
    n=max(abs(l) for c in F for l in c)
    counts=Counter(l for c in F for l in c)
    return (len(F)*3==4*n and n%3==0
            and len({tuple(sorted(c)) for c in F})==len(F)
            and all(len(c)==3 and len({abs(l) for l in c})==3
                    and (all(l>0 for l in c) or all(l<0 for l in c)) for c in F)
            and all(counts[v]==counts[-v]==2 for v in range(1,n+1)))

def sat(F,a):
    return all(any(a[abs(l)]==int(l>0) for l in c) for c in F)

def affine(rows,free):
    basis={}
    for mask,rhs in rows:
        while mask:
            pivot=mask.bit_length()-1
            if pivot not in basis:
                basis[pivot]=(mask,rhs)
                break
            m,b=basis[pivot];mask^=m;rhs^=b
        if not mask and rhs:
            return (0,None)
    bits=0
    for pivot in sorted(basis):
        mask,rhs=basis[pivot]
        if rhs^((mask&bits).bit_count()&1):
            bits|=1<<pivot
    return (1<<(len(free)-len(basis)),{v:(bits>>(v-1))&1 for v in free})

def exact(F,p,cap=2):
    if not valid(F):return ('MALFORMED',None)
    n=max(abs(l) for c in F for l in c)
    if any(type(v)!=int or v not in range(1,n+1) or b not in (0,1) for v,b in p.items()):
        return ('MALFORMED',None)
    free=[v for v in range(1,n+1) if v not in p]
    uncovered=[];sp=Counter()
    for j,c in enumerate(F):
        if any(abs(l) in p and p[abs(l)]==int(l>0) for l in c):
            for l in c:
                if abs(l) not in p:sp[abs(l),l>0]+=1
        else:
            rem=[l for l in c if abs(l) not in p]
            if not rem:return ('UNSAT',0)
            uncovered.append((j,rem))
    eta=sum(min(sp[v,True],sp[v,False]) for v in free)
    prefer={v:int(sp[v,False]>sp[v,True]) for v in free if sp[v,True]!=sp[v,False]}
    r=2*len(free)-len(uncovered)-eta
    if r<0:return ('UNSAT',0)
    if r>cap:return ('UNRESOLVED',None)
    groups=[]
    for v,b in prefer.items():
        groups.append([(('var',v),abs(sp[v,True]-sp[v,False]),{v:1-b})])
    for j,rem in uncovered:
        choices=[]
        if len(rem)==2:
            choices.append((('clause',j),1,{abs(l):int(l>0) for l in rem}))
        if len(rem)==3:
            for k in range(3):
                choices.append((('clause',j),1,{abs(l):int(l>0) if i!=k else int(l<0)
                                           for i,l in enumerate(rem)}))
            choices.append((('clause',j),2,{abs(l):int(l>0) for l in rem}))
        if choices:groups.append(choices)
    answer=0;first=None;branches=0
    def visit(i,selected,cost):
        nonlocal answer,first,branches
        if cost>r:return
        if i<len(groups):
            visit(i+1,selected,cost)
            for event in groups[i]:
                if cost+event[1]<=r:
                    visit(i+1,selected+[event],cost+event[1])
            return
        if cost!=r:return
        branches+=1
        events=[e for e,_,_ in selected]
        defects={e[1] for e in events if e[0]=='clause'}
        opposite={e[1] for e in events if e[0]=='var'}
        rows=[(1<<(v-1),b^(v in opposite)) for v,b in prefer.items()]
        for j,rem in uncovered:
            if j not in defects:
                rows.append((sum(1<<(abs(l)-1) for l in rem),
                             1 if rem[0]>0 else 1^(len(rem)&1)))
        for event,weight,bits in selected:
            if event[0]=='clause':
                rows.extend((1<<(v-1),b) for v,b in bits.items())
        count,a=affine(rows,free)
        if count:
            witness={**p,**a}
            assert sat(F,witness),('false original-source SAT',selected,witness)
            answer+=count
            if first is None:first=witness
    visit(0,[],0)
    return ('SAT' if answer else 'UNSAT',{'count':answer,'branches':branches,'witness':first,'r':r})

def brute(F,p):
    n=max(abs(l) for c in F for l in c)
    free=[v for v in range(1,n+1) if v not in p]
    return sum(sat(F,{**p,**dict(zip(free,b))}) for b in product((0,1),repeat=len(free)))

def main():
    for name,F,p in [('F9_PIN_UNSAT',F9,F9_U),('F15_U_UNSAT',F15,F15_U),
                     ('F15_S_SAT',F15,F15_S),('Y6_ROOT',Y6,{})]:
        decision,result=exact(F,p)
        actual=brute(F,p)
        if decision!='UNRESOLVED':
            assert actual==(result['count'] if isinstance(result,dict) else result)
        print(name,decision,result if isinstance(result,int) else
              {k:v for k,v in result.items() if k!='witness'} if result else None,
              'original_models',actual)
    assert exact(F9,F9_U)[0]=='UNSAT'
    assert exact(F15,F15_U)[0]=='UNSAT'
    assert exact(F15,F15_S)[1]['count']==2
    print('PASS: restricted exact slack affine SAT/#SAT; all-input hardness OPEN')
if __name__=='__main__':main()
