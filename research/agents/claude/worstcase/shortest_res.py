"""Exact shortest DAG-Resolution refutation length via SAT encoding.
Cost = number of derived clauses (distinct shared nodes); axioms free.
Resolution + weakening (same minimum length as plain resolution).
Each call: one (instance, L) query, interrupted after TL seconds.
Usage: python3.13 shortest_res.py INSTANCE L  -> appends JSON line to results.jsonl
"""
import sys, json, time, itertools, threading
from pysat.solvers import Glucose4
from pysat.card import CardEnc
from pysat.formula import IDPool

def php(h):  # h+1 pigeons, h holes
    v=lambda i,j: i*h+j+1
    C=[[v(i,j) for j in range(h)] for i in range(h+1)]
    for j in range(h):
        for i,k in itertools.combinations(range(h+1),2): C.append([-v(i,j),-v(k,j)])
    return h*(h+1), C

def tseitin(edges, odd_vertex=0):
    nv=1+max(max(e) for e in edges); C=[]
    for x in range(nv):
        inc=[k+1 for k,e in enumerate(edges) if x in e]
        ch=1 if x==odd_vertex else 0
        for signs in itertools.product([0,1],repeat=len(inc)):
            if sum(signs)%2!=ch:  # forbid assignments of wrong parity
                C.append([(-l if s else l) for l,s in zip(inc,signs)])
    return len(edges), C

K4=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
PRISM=[(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)]
K33=[(a,b) for a in range(3) for b in range(3,6)]
INST={'PHP3_2':lambda:php(2),'PHP4_3':lambda:php(3),'TS_K4':lambda:tseitin(K4),
      'TS_PRISM':lambda:tseitin(PRISM),'TS_K33':lambda:tseitin(K33),
      'FULL3':lambda:(3,[[ (i+1)*(1 if (b>>i)&1 else -1) for i in range(3)] for b in range(8)])}

def encode(n,C,L):
    P=IDPool(); m=len(C); S=m+L; cl=[]
    p=lambda j,u:P.id(('p',j,u)); q=lambda j,u:P.id(('q',j,u))
    for j,c in enumerate(C):
        for u in range(1,n+1):
            cl.append([p(j,u)] if u in c else [-p(j,u)])
            cl.append([q(j,u)] if -u in c else [-q(j,u)])
    for j in range(m,S):
        A=[P.id(('a',j,a)) for a in range(j)]; B=[P.id(('b',j,b)) for b in range(j)]
        V=[P.id(('v',j,u)) for u in range(1,n+1)]
        for lits in (A,B,V):
            cl.append(lits); cl+=CardEnc.atmost(lits,1,vpool=P).clauses
        for u in range(1,n+1):
            cl.append([-p(j,u),-q(j,u)])          # no tautologies (harmless)
            pv=V[u-1]
            for a in range(j):
                sa=A[a]; sb=B[a]
                cl.append([-sa,-pv,p(a,u)]); cl.append([-sb,-pv,q(a,u)])
                cl.append([-sa,-p(a,u),pv,p(j,u)]); cl.append([-sa,-q(a,u),pv,q(j,u)])
                cl.append([-sb,-p(a,u),pv,p(j,u)]); cl.append([-sb,-q(a,u),pv,q(j,u)])
    for u in range(1,n+1): cl+= [[-p(S-1,u)],[-q(S-1,u)]]
    for j in range(m,S-1):  # symmetry/pruning: every derived non-final clause is used later
        cl.append([P.id(('a',k,j)) for k in range(j+1,S)]+[P.id(('b',k,j)) for k in range(j+1,S)])
    return P,cl,p,q

def extract(model,P,n,m,L,p,q):
    M=set(x for x in model if x>0); steps=[]
    for j in range(m,m+L):
        a=next(a for a in range(j) if P.id(('a',j,a)) in M)
        b=next(b for b in range(j) if P.id(('b',j,b)) in M)
        v=next(u for u in range(1,n+1) if P.id(('v',j,u)) in M)
        c=sorted([u for u in range(1,n+1) if p(j,u) in M]+[-u for u in range(1,n+1) if q(j,u) in M],key=abs)
        steps.append((a,b,v,c))
    return steps

def check(C,steps):  # independent proof checker
    D=[frozenset(c) for c in C]
    for a,b,v,c in steps:
        A,B=D[a],D[b]
        if v not in A or -v not in B: return False
        R=(A-{v})|(B-{-v})
        if not R<=frozenset(c): return False
        D.append(frozenset(c))
    return len(D[-1])==0

if __name__=='__main__':
    name=sys.argv[1]; L=int(sys.argv[2]); TL=float(sys.argv[3]) if len(sys.argv)>3 else 25
    n,C=INST[name](); P,cl,p,q=encode(n,C,L)
    s=Glucose4(bootstrap_with=cl); t0=time.time()
    tm=threading.Timer(TL,s.interrupt); tm.start()
    r=s.solve_limited(expect_interrupt=True); tm.cancel(); dt=time.time()-t0
    rec={'inst':name,'n':n,'m':len(C),'L':L,'result':{True:'SAT',False:'UNSAT',None:'TIMEOUT'}[r],'sec':round(dt,2),'enc_clauses':len(cl)}
    if r:
        st=extract(s.get_model(),P,n,len(C),L,p,q); rec['proof_checks']=check(C,st); rec['proof']=st
    print(json.dumps({k:v for k,v in rec.items() if k!='proof'}))
    with open(__file__.replace('shortest_res.py','results.jsonl'),'a') as f: f.write(json.dumps(rec)+'\n')
