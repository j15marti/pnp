#!/usr/bin/env python3
"""Exact minimum DAG-like resolution refutation size (number of derived clauses) via SAT
(Peitl-Szeider style encoding; no weakening, tautologies excluded). Each call <= ~30s budget:
usage: min_res_dag.py FORMULA [smax]. Prints per-s SAT/UNSAT so results are checkpointed."""
import sys, itertools, time
from pysat.solvers import Cadical153

def php(p,h):
    v=lambda i,j:i*h+j+1
    cl=[[v(i,j) for j in range(h)] for i in range(p)]
    for j in range(h):
        for a in range(p):
            for b in range(a+1,p): cl.append([-v(a,j),-v(b,j)])
    return cl,p*h
def tseitin(edges,charges,n):
    ev={e:i+1 for i,e in enumerate(edges)}
    cl=[]
    for u in range(n):
        inc=[ev[e] for e in edges if u in e]
        for bits in itertools.product([0,1],repeat=len(inc)):
            if sum(bits)%2!=charges[u]:  # forbid this assignment
                cl.append([(-x if b else x) for x,b in zip(inc,bits)])
    return cl,len(edges)
FORM={'php32':lambda:php(3,2),'php43':lambda:php(4,3),
 'tri':lambda:tseitin([(0,1),(1,2),(0,2)],[1,0,0],3),
 'k4':lambda:tseitin([(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],[1,0,0,0],4)}

def solve(cl,nv,s):
    m=len(cl); T=m+s; vid=[0]
    def new(): vid[0]+=1; return vid[0]
    lit={(i,x,g):new() for i in range(m,T) for x in range(1,nv+1) for g in (0,1)}
    pa={(i,x,g):new() for i in range(m,T) for x in range(1,nv+1) for g in (0,1)}
    pb={(i,x,g):new() for i in range(m,T) for x in range(1,nv+1) for g in (0,1)}
    a={(i,j):new() for i in range(m,T) for j in range(i)}
    b={(i,j):new() for i in range(m,T) for j in range(i)}
    pv={(i,x):new() for i in range(m,T) for x in range(1,nv+1)}
    S=Cadical153(); add=S.add_clause
    ax=[{(abs(l),1 if l>0 else 0) for l in c} for c in cl]
    def L(j,x,g):  # returns ('c',bool) or ('v',var)
        return ('c',(x,g) in ax[j]) if j<m else ('v',lit[(j,x,g)])
    for i in range(m,T):
        for grp in (a,b):
            vs=[grp[(i,j)] for j in range(i)]
            add(vs)
            for u,w in itertools.combinations(vs,2): add([-u,-w])
        vs=[pv[(i,x)] for x in range(1,nv+1)]; add(vs)
        for u,w in itertools.combinations(vs,2): add([-u,-w])
        for x in range(1,nv+1):
            add([-lit[(i,x,1)],-lit[(i,x,0)]])  # no tautologies
            for g in (0,1):
                add([-lit[(i,x,g)],pa[(i,x,g)],pb[(i,x,g)]])
                add([-lit[(i,x,g)],-pv[(i,x)]])
                add([-pa[(i,x,g)],pv[(i,x)],lit[(i,x,g)]])
                add([-pb[(i,x,g)],pv[(i,x)],lit[(i,x,g)]])
                for j in range(i):
                    for (grp,P) in ((a,pa),(b,pb)):
                        t,val=L(j,x,g)
                        if t=='c':
                            add([-grp[(i,j)], P[(i,x,g)] if val else -P[(i,x,g)]])
                        else:
                            add([-grp[(i,j)],-val,P[(i,x,g)]]); add([-grp[(i,j)],val,-P[(i,x,g)]])
            # pivot: parent a has x positive, parent b has x negative
            for j in range(i):
                for (grp,g) in ((a,1),(b,0)):
                    t,val=L(j,x,g)
                    if t=='c':
                        if not val: add([-grp[(i,j)],-pv[(i,x)]])
                    else: add([-grp[(i,j)],-pv[(i,x)],val])
    for x in range(1,nv+1):
        for g in (0,1):
            t,val=L(T-1,x,g)
            if t=='v': add([-val])
            elif val: return None
    r=S.solve(); S.delete(); return r

if __name__=='__main__':
    name=sys.argv[1]; smax=int(sys.argv[2]) if len(sys.argv)>2 else 30
    cl,nv=FORM[name](); t0=time.time()
    print(name,'vars',nv,'axioms',len(cl),flush=True)
    for s in range(1,smax+1):
        r=solve(cl,nv,s)
        print(' s=%d %s  (%.1fs)'%(s,'SAT' if r else 'UNSAT',time.time()-t0),flush=True)
        if r: print('MIN_DERIVED_CLAUSES',s); break
        if time.time()-t0>1500: print('BUDGET_STOP at s=%d: lower bound %d'%(s,s+1)); break
