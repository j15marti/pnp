#!/usr/bin/env python3
"""Compact independent ADAPTIVEPROOFRACE83 checker.
The 9,966-assertion complete audit is a separate conversation artifact.
This reproduces exact source/circuit identities and a geometric race bound.
Python 3 standard library. No SAT lower bound is claimed.
"""
from itertools import product

def val(clause,a):
    return any(a[abs(l)-1] == (l > 0) for l in clause)

def sat(f,n):
    return any(all(val(c,a) for c in f) for a in product([False,True],repeat=n))

def ladder(q,bits):
    z=lambda i:i+1
    u,v=q+2,q+3
    return [(z(0),u),(z(0),-u),(-z(q),v),(-z(q),-v)] + [
        (-z(i-1),z(i) if bits[i-1] else -z(i)) for i in range(1,q+1)
    ]

def h(g):
    f=[]
    x=lambda i:3*i+1
    y=lambda i:3*i+2
    z=lambda i:3*i+3
    for i in range(g):
        f += [(x(i),-y(i),z(i)),(x(i),-y(i),-z(i)),
              (-x(i),y(i),z((i+1)%g)),(-x(i),y(i),-z((i+1)%g))]
    return f

def compile3(f,n):
    assert f and all(len(c)==3 for c in f)
    nextid=n+1
    gates=[]; cnf=[]; neg={}
    for v in range(1,n+1):
        u=nextid;nextid+=1;neg[v]=u
        gates.append(('NOT',u,v,0))
        cnf += [(u,v),(-u,-v)]
    def lit(l):return l if l>0 else neg[-l]
    def gate(op,a,b):
        nonlocal nextid
        u=nextid;nextid+=1
        gates.append((op,u,a,b))
        if op=='OR':
            cnf.extend([(-a,u),(-b,u),(a,b,-u)])
        else:
            cnf.extend([(a,-u),(b,-u),(-a,-b,u)])
        return u
    leaves=[gate('OR',gate('OR',lit(a),lit(b)),lit(c))
            for a,b,c in f]
    root=leaves[0]
    for out in leaves[1:]:
        root=gate('AND',root,out)
    cnf.append((root,))
    assert len(gates)==n+3*len(f)-1
    assert sum(1 if g[0]=='NOT' else 2 for g in gates)==n+6*len(f)-2
    assert len(cnf)==2*n+9*len(f)-2
    return gates,cnf,root

def extension(gates,source):
    a=list(source)
    for op,output,x,y in gates:
        xx=a[x-1]
        answer=not xx if op=='NOT' else (
            xx or a[y-1] if op=='OR' else xx and a[y-1])
        assert output==len(a)+1
        a.append(bool(answer))
    return a

def geometric_tick_count(times,priority):
    # Executable schedule with no knowledge of the completing expert at runtime.
    # A specialist emits t successful yield ticks and halts on the next resume.
    s=len(priority);remaining=times.copy();spent=0;switches=0
    for r in range(32):
        for i,name in enumerate(priority):
            switches+=1
            for _ in range(2**max(0,r-i)):
                if remaining[name]==0:
                    return name,spent+switches
                remaining[name]-=1;spent+=1
    raise AssertionError("schedule cutoff")

def main():
    checks=0
    for q in range(1,7):
        for b in product([0,1],repeat=q):
            assert sat(ladder(q,b),q+3)==(not all(b))
            checks+=1
    for g in (1,2,3):
        f=h(g); n=3*g
        for a in product([False,True],repeat=n):
            eq=all(a[3*i]==a[3*i+1] for i in range(g))
            assert all(val(c,a) for c in f)==eq
            checks+=1
        assert sat(f,n)
        gates,cnf,root=compile3(f,n)
        for a in product([False,True],repeat=n):
            ext=extension(gates,a)
            assert all(val(c,ext) for c in cnf)==all(val(c,a) for c in f)
            assert ext[root-1]==all(val(c,a) for c in f)
            checks+=2
    # The source-only scheduler can prioritize different correct solvers
    # without obtaining the label; the suffix methods are not SAT oracles.
    for first in range(4):
        priority=list(range(first,4))+list(range(first))
        for t in (1,3,8,21):
            times={i:10+t*i for i in range(4)}
            winner,spent=geometric_tick_count(times,priority)
            idx=priority.index(winner)
            R=idx+(times[winner]+1-1).bit_length()
            assert spent<=8*(2**idx)*(times[winner]+1)+4*(R+1)
            checks+=1
    print({'run':'ADAPTIVEPROOFRACE83-mini','assertions':checks,'failed':0,
           'scope':'finite syntax, unique circuit extensions, scheduled events'})

if __name__=='__main__':main()
