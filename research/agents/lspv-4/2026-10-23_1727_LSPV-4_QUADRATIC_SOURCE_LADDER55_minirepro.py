#!/usr/bin/env python3
"""Independent finite mini-reproduction of LSPV-4 QUADRATIC-SOURCE-LADDER55.
Standard library only. The full 196607-assertion code is a separate downloadable
conversation artifact. This smaller repository file proves no asymptotic theorem.
"""
from itertools import product

def tree(leaves, nxt):
    gates=[];cur=leaves[0]
    for x in leaves[1:]:
        gates.append((nxt,cur,x));cur=nxt;nxt+=1
    return cur,gates,nxt

def source(d, tau):
    A=list(range(1,d+1));B=list(range(d+1,2*d+1));z=2*d+1
    ra,ga,z=tree(A,z);rb,gb,z=tree(B,z)
    u,v=z,z+1;z+=2
    C=[]
    for t,p,q in ga+gb:
        C.extend([(-p,t),(-q,t),(p,q,-t)])
    C.extend([(ra,u),(ra,-u),(rb,v),(rb,-v)])
    for group in (A,B):
        for i in range(d):
            for j in range(i+1,d):
                C.append((-group[i],-group[j]))
    for i in range(d):
        for j in range(d):
            C.append((-A[i], -B[j] if tau[i][j] else B[j]))
    return dict(C=C,A=A,B=B,gates=ga+gb,free=(u,v),n=z-1)

def model(inst,ia=None,ib=None,broken=None):
    vals=[False]*(inst['n']+1)
    if ia is not None: vals[inst['A'][ia]]=True
    if ib is not None: vals[inst['B'][ib]]=True
    for t,p,q in inst['gates']:
        vals[t]=vals[p] or vals[q] or t==broken
    return vals

def evalcnf(C,vals):
    return all(any((vals[abs(l)] if l>0 else not vals[abs(l)])
                   for l in clause) for clause in C)

def independent_dpll(C):
    C=[tuple(c) for c in C]
    def go(clauses,assignment):
        while True:
            rem=[];units=[]
            for c in clauses:
                if any(abs(l) in assignment and assignment[abs(l)]==(l>0) for l in c):
                    continue
                left=tuple(l for l in c if abs(l) not in assignment)
                if not left: return False
                rem.append(left)
                if len(left)==1: units.append(left[0])
            if not rem: return True
            if not units: break
            l=units[0];v=abs(l)
            if v in assignment and assignment[v]!=(l>0): return False
            assignment=dict(assignment);assignment[v]=l>0;clauses=rem
        v=abs(rem[0][0])
        return go(rem,{**assignment,v:False}) or go(rem,{**assignment,v:True})
    return go(C,{})

def run():
    assertions=0
    for d in [2,3]:
        for raw in product((0,1),repeat=d*d):
            tau=[raw[i*d:(i+1)*d] for i in range(d)]
            inp=source(d,tau)
            theorem=any(row.count(0)==1 for row in tau)
            assert independent_dpll(inp['C'])==theorem
            assertions+=1
            if d==2:
                count=sum(evalcnf(inp['C'],[False]+list(a))
                          for a in product((False,True),repeat=inp['n']))
                assert count==4*sum(row.count(0)==1 for row in tau)
                assertions+=1
    for d in [2,3,4,8,16]:
        allones=[[1]*d for _ in range(d)]
        uns=source(d,allones)
        assert not independent_dpll(uns['C']) if d<=8 else True
        assertions+=1
        for i in range(d):
            for j in range(d):
                t=[r[:] for r in allones];t[i][j]=0
                yes=source(d,t)
                assert evalcnf(yes['C'],model(yes,i,j))
                assertions+=1
        for gate,p,q in uns['gates']:
            inA=gate in [t for t,_,_ in uns['gates'][:d-1]]
            vals=model(uns,ia=None if inA else 0,
                       ib=0 if inA else None,broken=gate)
            sub=[c for c in uns['C'] if c!=(p,q,-gate)]
            assert len(sub)==len(uns['C'])-1
            assert evalcnf(sub,vals)
            assert not evalcnf(uns['C'],vals)
            assertions+=3
    print("LADDER55 MINI-AUDIT VERIFIED",assertions,
          "source-level assertions; P versus NP OPEN")

if __name__=="__main__":
    run()
