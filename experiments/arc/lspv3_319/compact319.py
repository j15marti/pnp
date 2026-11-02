#!/usr/bin/env python3
"""LSPV3 GATE319: paid clause-frontier SAT/Circuit-SAT on canonical F9/G2."""
from collections import Counter
from itertools import product
from json import dumps
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F=tuple(P)+tuple(tuple(-v for v in c) for c in N)
def source(n,t):
    if t==1:return F
    out=[]
    for b in range(t):
        for j,c in enumerate(P):
            a=[9*b+v for v in c]
            if j==0:a[0]=9*((b+1)%t)+1
            out.append(tuple(a))
        out.extend(tuple(-9*b-v for v in c) for c in N)
    return tuple(out)
def valid(C,n):
    if 3*len(C)!=4*n or len(C)!=len(set(tuple(sorted(c)) for c in C)):return False
    q=Counter(v for c in C for v in c)
    return all(len(c)==3 and len(set(map(abs,c)))==3 and len({v>0 for v in c})==1 and all(1<=abs(v)<=n for v in c) for c in C) and all(q[i]==q[-i]==2 for i in range(1,n+1))
def tr(C,a):return all(any(a[abs(v)]==int(v>0) for v in c) for c in C)
def frontier(C,n,order,pins=None):
    pins=pins or {};S=[set(map(abs,c)) for c in C];done=set();cross=[]
    for k in range(n+1):
        cross.append(tuple(j for j,z in enumerate(S) if z&done and z-done))
        if k<n:done.add(order[k])
    states={0:1};live=1;operations=0
    done=set()
    for k,v in enumerate(order):
        a=cross[k];b=cross[k+1];position={j:h for h,j in enumerate(a)}
        incident=[j for j,c in enumerate(C) if v in S[j]];after=done|{v};new={}
        for mask,count in states.items():
            for bit in ((pins[v],) if v in pins else (0,1)):
                operations+=1
                status={j:bool((mask>>i)&1) for i,j in enumerate(a)}
                for j in incident:
                    lit=next(x for x in C[j] if abs(x)==v)
                    status[j]=status.get(j,False) or (bit==int(lit>0))
                if any(S[j]<=after and not status[j] for j in incident):continue
                sig=sum((1<<h) for h,j in enumerate(b) if status.get(j,False))
                new[sig]=new.get(sig,0)+count
        states=new;done=after;live=max(live,len(states))
    return {'models':states.get(0,0),'peak_states':live,'peak_crossing':max(map(len,cross)),'transitions':operations}
def bdd(C,order):
    table=[int(tr(C,dict(zip(order,bits)))) for bits in product((0,1),repeat=len(order))]
    nodes={}
    def rec(level,values):
        if min(values)==max(values):return values[0]
        mid=len(values)//2
        left=rec(level+1,values[:mid]);right=rec(level+1,values[mid:])
        if left==right:return left
        key=(level,left,right)
        if key not in nodes:nodes[key]=len(nodes)+2
        return nodes[key]
    rec(0,table)
    return len(nodes)
def main():
    assert valid(F,9)
    bad=(((1,1,2),)+F[1:],F+(F[0],),F[:-1])
    assert all(not valid(z,9) for z in bad)
    orders={'natural':tuple(range(1,10)),'reverse':tuple(range(9,0,-1)),
            'min_crossing':(1,2,3,5,8,4,6,7,9),'best_OBDD':(2,6,7,9,8,4,3,1,5)}
    x={name:dict(frontier(F,9,o),obdd_nodes=bdd(F,o)) for name,o in orders.items()}
    assert [x[z]['obdd_nodes'] for z in orders]==[66,70,66,52]
    p={1:0,3:0,5:1,6:0,7:0,8:0};q=dict(p);q[1]=1
    po=tuple(p)+tuple(v for v in range(1,10) if v not in p)
    cases={'same_original_SAT':frontier(F,9,po,p),'same_original_UNSAT':frontier(F,9,po,q)}
    assert (cases['same_original_SAT']['models'],cases['same_original_UNSAT']['models'])==(2,0)
    G=source(18,2);assert valid(G,18)
    good=tuple(range(1,19));mixed=tuple(v for i in range(1,10) for v in (i,i+9))
    y={'block':frontier(G,18,good),'interleaved':frontier(G,18,mixed)}
    assert y['block']['models']==y['interleaved']['models']==3878
    print(dumps({'F9':x,'F9_pins':cases,'connected_G2':y,'malformed_rejections':len(bad)},sort_keys=True,indent=2))
if __name__=='__main__':main()
