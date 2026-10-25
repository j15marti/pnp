#!/usr/bin/env python3
"""Independent reproduction of the named PC22 global-clone-order port sensitivity.
Python 3.10+, standard library. No SAT oracle, no local files required.
"""
import collections
import itertools
import json
import math

Q=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
Q=[c for c in Q if c!=(1,7,13)]

def source(q, changed=None, unsat=False):
    F=[(1,3,4),(1,2,3),(2,3,4)]
    F += [(4 if j==changed else 1,3,j+5) for j in range(q)]
    if unsat:
        z=q+5
        F += [tuple((z+i) if s>0 else -(z+i)
                    for i,s in enumerate(t))
              for t in itertools.product((-1,1), repeat=3)]
    assert all(len(set(map(abs,c)))==3 for c in F)
    assert len({tuple(sorted(c)) for c in F})==len(F)
    return F

def compile22(F):
    n=max(abs(a) for c in F for a in c);m=len(F);s=n+1
    U=[]
    for j,(a,b,c) in enumerate(F):
        y=n+2+2*j;z=y+1
        U += [(s,a,y),(-y,b,c),(-s,-a,z),(-z,-b,-c)]
    B=U+U; occ=collections.defaultdict(lambda:[[],[]])
    for j,c in enumerate(B):
        for p,l in enumerate(c):
            occ[abs(l)][int(l<0)].append((j,p))
    C=[[0]*3 for _ in B]; groups={}; count=0
    for x in sorted(occ):
        pos,neg=occ[x]
        assert len(pos)==len(neg) and len(pos)>=2
        group=[]
        for p,k in zip(pos,neg):
            count+=1;group.append(count)
            C[p[0]][p[1]]=count
            C[k[0]][k[1]]=-count
        groups[x]=group
    assert count==12*m
    edges=[]
    for x,g in groups.items():
        edges += [(a,b,x) for a,b in zip(g,g[1:]+g[:1])]
    pads=[]
    for i,(a,b,x) in enumerate(edges):
        off=count+15*(i//3)
        pads.append((-a,b,off+(1,7,13)[i%3]))
    rest=[]
    for j in range(count//3):
        off=count+15*j
        rest += [tuple((off+abs(l))*(1 if l>0 else -1)
                       for l in c) for c in Q]
    out=list(map(tuple,C))+pads+rest
    assert len(out)==96*m
    return out,edges,groups

def check_one(q, unsat):
    F=source(q,unsat=unsat);m=len(F);L=2*(q+2)
    i=L-1; old=1; new=L+1
    bit=new.bit_length()-1
    checked=0
    assert ((old>>bit)&1)==0 and ((new>>bit)&1)==1;checked+=1
    T,edges,groups=compile22(F)
    assert len(groups[1])==L and len(groups[2])==4;checked+=1
    assert edges[i][1]==old and T[8*m+i][1]==old;checked+=1
    counts=collections.Counter(l for c in T for l in c)
    assert all(counts[x]==counts[-x]==2 for x in range(1,72*m+1))
    assert all(len(set(map(abs,c)))==3 for c in T)
    assert len({tuple(sorted(c)) for c in T})==len(T);checked+=3
    for j in range(q):
        E=source(q,changed=j,unsat=unsat)
        Eout,Eedges,Eg=compile22(E)
        assert len(Eg[1])==L-2 and len(Eg[2])==4;checked+=1
        assert Eedges[i][1]==new and Eout[8*m+i][1]==new;checked+=1
        assert sum(F[h]!=E[h] for h in range(m))==1;checked+=1
    return checked, {'q':q,'label':'UNSAT' if unsat else 'SAT',
                     'm':m,'old':old,'new':new,'index':8*m+i,
                     'necessary_disjoint_source_fields':q}

def sat_brute(F):
    n=max(abs(l) for c in F for l in c)
    for v in range(1<<n):
        if all(any(bool((v>>(abs(l)-1))&1)==(l>0) for l in c)
               for c in F):
            return True
    return False

def main():
    checks=0;cases=[]
    for q in (1,2,3,4,5,7,12):
        for unsat in (False,True):
            n,row=check_one(q,unsat);checks+=n;cases.append(row)
    for q in (1,2,3):
        for bad in (False,True):
            assert sat_brute(source(q,unsat=bad))== (not bad);checks+=1
            for j in range(q):
                assert sat_brute(source(q,changed=j,unsat=bad))==(not bad)
                checks+=1
    sizes=[]
    for bad in (False,True):
        F=source(1,unsat=bad)
        g,_,_=compile22(F)
        h,_,_=compile22(g)
        assert len(g)==96*len(F) and len(h)==96*96*len(F);checks+=1
        sizes.append({'label':'UNSAT' if bad else 'SAT',
                      'first_clauses':len(g),'second_clauses':len(h)})
    result={'id':'M22-PC22-PORT-PROBE104','status':'COMPUTATIONAL',
            'checks':checks,'failures':0,'cases':cases,
            'two_level':sizes,'scope':'Named compiler only, not all SAT solvers'}
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
