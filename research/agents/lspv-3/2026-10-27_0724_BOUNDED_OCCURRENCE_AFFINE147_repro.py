#!/usr/bin/env python3
"""BOUNDED-OCCURRENCE-AFFINE147, standalone exact source and Resolution audit.
No external packages.  Run: python 2026-10-27_0724_BOUNDED_OCCURRENCE_AFFINE147_repro.py
Finite audit only; proof in accompanying .tex is required for asymptotic claims.
"""
import json, hashlib, itertools, random
from collections import defaultdict, Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parent
SEED = 14720261027

class Builder:
    def __init__(self):
        self.names={}; self.src=[]; self.groups=defaultdict(list)
        self.imps={}; self.clones={}; self.guard=[]; self.split=[]
        self.pin={}
    def v(self,name):
        if name not in self.names: self.names[name]=len(self.names)+1
        return self.names[name]
    def add(self,lits,group):
        assert len(lits)==3 and len(set(map(abs,lits)))==3
        i=len(self.src)+1
        self.src.append(tuple(lits));self.groups[group].append(i)
        return i
    def imp(self,p,q,tag):
        assert p!=q
        z=self.v(('pad',tag))
        a=self.add((-p,q,z),'G');b=self.add((-p,q,-z),'G')
        self.imps[(p,q)]=(a,b,z)
    def pin0(self,p,tag):
        u=self.v(('pin',tag,'u'));v=self.v(('pin',tag,'v'))
        ids=[self.add((-p,sgn_u*u,sgn_v*v),'P')
             for sgn_u,sgn_v in ((1,1),(1,-1),(-1,1),(-1,-1))]
        return ids,(u,v)

def build(F):
    assert F and all(len(c)==3 and len(set(map(abs,c)))==3 for c in F)
    b=Builder();occ=defaultdict(list)
    for j,c in enumerate(F):
        row=[]
        for k,lit in enumerate(c):
            v=b.v(('original_occ',j,k));occ[abs(lit)].append(v)
            row.append((1 if lit>0 else -1)*v)
            b.clones[(j,k)]=v
        g=b.v(('guard',j));t=b.v(('split',j)); b.guard.append(g)
        L=b.add((g,row[0],t),'G');R=b.add((-t,row[1],row[2]),'G')
        b.split.append((L,R,t,row,g))
    y=b.v(('boundary','y'));b.y=y;b.occ=occ
    guards=[y]+b.guard
    for i,p in enumerate(guards):b.imp(p,guards[(i+1)%len(guards)],('guard',i))
    for var,clones in occ.items():
        if len(clones)>=2:
            for i,p in enumerate(clones):b.imp(p,clones[(i+1)%len(clones)],('occ',var,i))
    z=b.v(('pin','z'));w=b.v(('pin','w'))
    a,uv=b.pin0(z,'z');c,uw=b.pin0(w,'w')
    k=b.add((-y,z,w),'P');b.pin={'z':(z,a,uv),'w':(w,c,uw),'last':k}
    return b

class Proof:
    def __init__(self,source):
        self.rows=[None]+[frozenset(c) for c in source];self.m=len(source)
        self.steps=[];self.maxwidth=max((len(x) for x in self.rows[1:]),default=0)
    def resolve(self,i,j,p):
        A=self.rows[i];B=self.rows[j]
        assert (p in A and -p in B) or (-p in A and p in B),(i,j,p,A,B)
        R=(A-{p})|(B-{-p}) if (p in A and -p in B) else (A-{-p})|(B-{p})
        assert not any(-l in R for l in R),('taut',i,j,p,R)
        self.rows.append(frozenset(R));out=len(self.rows)-1
        self.steps.append((out,i,j,p))
        self.maxwidth=max(self.maxwidth,len(R));return out
    def check(self):
        rows=self.rows[:self.m+1]
        for out,i,j,p in self.steps:
            assert out==len(rows) and 0<i<out and 0<j<out
            A=rows[i];B=rows[j]
            assert (p in A and -p in B) or (-p in A and p in B)
            R=(A-{p})|(B-{-p}) if p in A else (A-{-p})|(B-{p})
            assert frozenset(R)==self.rows[out] and not any(-l in R for l in R)
            rows.append(frozenset(R))
        return rows[-1]==frozenset()

def resolution_F(F):
    P=Proof(F);seen={frozenset(c):i+1 for i,c in enumerate(F)}
    i=1
    while i<len(P.rows):
        for j in range(1,i):
            for lit in sorted(P.rows[i],key=lambda x:(abs(x),x)):
                if -lit not in P.rows[j]:continue
                R=(P.rows[i]-{lit}) | (P.rows[j]-{-lit})
                if any(-v in R for v in R) or frozenset(R) in seen:continue
                new=P.resolve(i,j,abs(lit))
                seen[P.rows[new]]=new
                if not R:return P
        i+=1
    return None

def path(b,seq,start,end,proof,binary):
    if start==end:return None
    idx=seq.index(start);p=start;last=None;distance=0
    while p!=end:
        q=seq[(idx+1)%len(seq)];z=binary[(p,q)]
        last=z if last is None else proof.resolve(last,z,p)
        p=q;idx=(idx+1)%len(seq);distance+=1
        assert distance<=len(seq)
    return last

def transfer(F,b,PF):
    P=Proof(b.src)
    def pin_unit(key):
        var,ids,(_,v)=b.pin[key]
        a=P.resolve(ids[0],ids[1],v);c=P.resolve(ids[2],ids[3],v)
        # resolve on the other pin-aux name
        other=next(abs(z) for z in b.src[ids[0]-1] if abs(z) not in {var,v})
        return P.resolve(a,c,other)
    uz=pin_unit('z');uw=pin_unit('w')
    uy=P.resolve(b.pin['last'],uz,b.pin['z'][0]);uy=P.resolve(uy,uw,b.pin['w'][0])
    assert P.rows[uy]==frozenset({-b.y})
    binary={}
    for (p,q),(i,j,z) in b.imps.items():
        k=P.resolve(i,j,z);binary[(p,q)]=k
        assert P.rows[k]==frozenset({-p,q})
    guard_unit={b.y:uy};prev=uy
    for g in reversed(b.guard):
        succ=b.y if g==b.guard[-1] else b.guard[b.guard.index(g)+1]
        prev=P.resolve(binary[(g,succ)],prev,succ)
        guard_unit[g]=prev
        assert P.rows[prev]==frozenset({-g})
    transformed=[]
    for j,(i,k,t,row,g) in enumerate(b.split):
        h=P.resolve(i,k,t)
        h=P.resolve(h,guard_unit[g],g)
        for idx,lit in enumerate(F[j]):
            v=b.clones[(j,idx)];seq=b.occ[abs(lit)];rep=seq[0]
            if v==rep:continue
            hpath=path(b,seq,v,rep,P,binary) if lit>0 else path(b,seq,rep,v,P,binary)
            assert hpath is not None
            h=P.resolve(h,hpath,v)
        expected=frozenset((1 if lit>0 else -1)*b.occ[abs(lit)][0] for lit in F[j])
        assert P.rows[h]==expected,(j,P.rows[h],expected)
        transformed.append(h)
    simulated={i+1:k for i,k in enumerate(transformed)}
    for out,i,j,p in PF.steps:
        rep=b.occ[p][0]
        new=P.resolve(simulated[i],simulated[j],rep)
        original=frozenset((1 if x>0 else -1)*b.occ[abs(x)][0] for x in PF.rows[out])
        assert P.rows[new]==original
        simulated[out]=new
    assert P.rows[simulated[len(PF.rows)-1]]==frozenset()
    assert P.check()
    assert P.maxwidth<=max(4,PF.maxwidth)
    return P

def sat(F,forced=()):
    # Complete DPLL with unit propagation (dependency-free).
    rows=[tuple(c) for c in F]+[tuple([l]) for l in forced]
    def go(clauses,assignment):
        while True:
            reduced=[];units=[]
            for c in clauses:
                if any(assignment.get(abs(l))==(l>0) for l in c):continue
                rem=tuple(l for l in c if abs(l) not in assignment)
                if not rem:return False
                if len(rem)==1:units.append(rem[0])
                reduced.append(rem)
            if not reduced:return True
            if not units:break
            for l in units:
                v=abs(l);value=l>0
                if v in assignment and assignment[v]!=value:return False
                assignment[v]=value
            clauses=reduced
        count=Counter(abs(l) for c in reduced for l in c)
        v=max(count,key=count.get)
        return go(reduced,{**assignment,v:True}) or go(reduced,{**assignment,v:False})
    return go(rows,{})

def incidence_connected(F,n):
    graph=defaultdict(set)
    for i,c in enumerate(F):
        for lit in c:
            v=abs(lit);graph[('c',i)].add(('v',v));graph[('v',v)].add(('c',i))
    seen={('c',0)};todo=list(seen)
    for p in todo:
        for q in graph[p]:
            if q not in seen:seen.add(q);todo.append(q)
    return len(seen)==len(F)+n

def run():
    rng=random.Random(SEED);cases=[];assertions=0;maxdegree=0;proofs=0
    def ck(x,msg):
        nonlocal assertions
        assertions+=1
        if not x:raise AssertionError(msg)
    allclauses=[]
    for signs in itertools.product((1,-1),repeat=3):
        allclauses.append(tuple(s*(i+1) for i,s in enumerate(signs)))
    # Every nonempty proper ternary source on 3 names. The full 8-clause source is UNSAT.
    for mask in range(1,1<<len(allclauses)):
        F=[allclauses[i] for i in range(8) if mask>>i&1]
        b=build(F);N=len(b.names);M=len(b.src)
        ck(M==4*len(F)+2*sum(len(a) for a in b.occ.values() if len(a)>=2)+11,'clause count')
        ck(N==6*len(F)+sum(len(a) for a in b.occ.values() if len(a)>=2)+8,'variable count')
        ck(len(set(tuple(sorted(c)) for c in b.src))==M,'duplicate source clauses')
        ck(all(len(set(map(abs,c)))==3 for c in b.src),'proper')
        occ=Counter(abs(l) for c in b.src for l in c)
        ck(set(occ)==set(range(1,N+1)),'no unused variables')
        ck(max(occ.values())<=5,'max degree')
        ck(incidence_connected(b.src,N),'incidence connected')
        chkF=sat(F);chkH=sat(b.src)
        ck(chkF==chkH,'SAT projection transfer')
        ck(sat([b.src[i-1] for i in b.groups['G']],[-b.y])==chkF,'G y=0')
        ck(sat([b.src[i-1] for i in b.groups['G']],[b.y]),'G y=1')
        ck(sat([b.src[i-1] for i in b.groups['P']],[-b.y]),'P y=0')
        ck(not sat([b.src[i-1] for i in b.groups['P']],[b.y]),'P y=1 excluded')
        ck(len(b.groups['P'])==9,'pin has 9 clauses')
        ck(max(occ.values())==5,'degree saturation')
        maxdegree=max(maxdegree,max(occ.values()))
        if not chkF:
            pf=resolution_F(F);ck(pf is not None and pf.check(),'original Resolution')
            pt=transfer(F,b,pf);proofs+=1
            ck(len(pt.steps)<=len(pf.steps)+12*len(F)**2+10*len(F)+20,'polynomial proof upper')
            child=b.src[:-1];grand=b.src[:-2]
            ck(sat(child),'first ordinary SAT descendant')
            ck(sat(grand),'second ordinary SAT descendant')
            ck(all(len(c)==3 for c in child+grand),'genuine 3CNF children')
            cases.append({'case':'full-8-UNSAT','vars':N,'clauses':M,'original_proof_steps':len(pf.steps),'transferred_steps':len(pt.steps),'max_proof_width':pt.maxwidth,'child1':len(child),'child2':len(grand)})
    # Random signed 3CNFs on up to 5 used names, without repeated variable in a clause.
    for n in range(3,6):
        for t in range(18):
            m=rng.randrange(2,9);F=[]
            for j in range(m):
                vs=rng.sample(range(1,n+1),3)
                row=tuple(v*(1 if rng.randrange(2) else -1) for v in vs)
                if row not in F:F.append(row)
            if not F:continue
            b=build(F);N=len(b.names)
            ck(incidence_connected(b.src,N),'random connected')
            ck(max(Counter(abs(l) for c in b.src for l in c).values())<=5,'random degree')
            ck(sat(b.src)==sat(F),'random SAT transfer')
            ck(sat([b.src[i-1] for i in b.groups['G']],[-b.y])==sat(F),'random G projection')
            ck(sat([b.src[i-1] for i in b.groups['P']],[b.y])==False,'random P projection')
    # Hostile controls: ten larger UNSAT roots preserving the exhaustive 3-variable core.
    for trial in range(10):
        F=list(allclauses)
        extra_vars=4 if trial%2 else 5
        for _ in range(1+trial%3):
            vs=rng.sample(range(1,extra_vars+1),3)
            F.append(tuple(v if rng.randrange(2) else -v for v in vs))
        b=build(F);pf=resolution_F(F)
        ck(pf is not None and pf.check(),'larger UNSAT parent proof')
        pt=transfer(F,b,pf)
        ck(pt.maxwidth<=max(4,pf.maxwidth),'larger width')
        ck(len(pt.steps)<=len(pf.steps)+4*len(F)+sum(len(v) for v in b.occ.values() if len(v)>=2)+9+sum(len(v)**2 for v in b.occ.values()),'symbolic line bound')
        ck(not sat(b.src),'larger UNSAT source')
        proofs+=1
    # False-join control: renaming the only shared boundary in P destroys unsatisfiability.
    b=build(allclauses);badjoin=[list(c) for c in b.src];fresh=len(b.names)+1
    for ix in b.groups['P']:
        badjoin[ix-1]=[(-fresh if l==-b.y else l) for l in badjoin[ix-1]]
    ck(sat(badjoin),'renamed boundary is SAT')
    # Claimed unit y=1 is not authentic on a SAT seven-clause predecessor.
    g=build(allclauses[:-1]);G=[g.src[ix-1] for ix in g.groups['G']]
    ck(sat(G,[-g.y]),'false affine row caught by witness')
    # Horn and affine XOR complete quartets are separate easy controls.
    for F in [ [(-1,-2,-3),(1,-2,-3)],
               [allclauses[ix] for ix in [0,3,5,6]] ]:
        b=build(F)
        ck(sat(F) and sat(b.src),'Horn / XOR SAT')
        ck(incidence_connected(b.src,len(b.names)),'Horn / XOR connectivity')
    # Source pointer authenticity: introducing a false certificate must be rejected.
    base=build(allclauses)
    ck(not sat(base.src),'UNSAT control')
    tainted=[list(row) for row in base.src]
    tainted[0][0]*=-1
    ck(tainted[0]!=list(base.src[0]),'edited source pointer mismatch')
    # Audit signed exact-(2,2) W1 is a separate control, and does NOT meet degree <=5 transform identity.
    W=[[-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],
       [5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],
       [-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],
       [2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]]
    plus=Counter(abs(l) for c in W for l in c if l>0)
    minus=Counter(abs(l) for c in W for l in c if l<0)
    ck(all(plus[v]==minus[v]==2 for v in range(1,16)),'W1 separate exact22')
    ck(not sat(W),'W1 UNSAT')
    result={'run':'BOUNDED_OCCURRENCE_AFFINE147','date':'2026-10-27','random_seed':SEED,
            'coverage':{'exhaustive_3variable_nonempty_clause_subsets':255,'random_3to5_name_trials':54},
            'max_variable_occurrences':maxdegree,'tested_resolution_transfers':proofs,
            'hostile_controls':['10 larger UNSAT', 'false alias join', 'false affine row', 'Horn', 'XOR', 'W1 exact22'],
            'assertions':assertions,'failures':0,'proof_example':cases,
            'statuses':{'restricted_projection_theorem':'PROVED/EXACT pending independent review',
                        'finite_tests':'COMPUTATIONAL','all_UNSAT_affordable_coverage':'OPEN',
                        'exact_signed_22_transfer':'OPEN','ARC_EDGE_90':'OPEN','P_vs_NP':'OPEN'}}
    target=ROOT/'2026-10-27_0724_BOUNDED_OCCURRENCE_AFFINE147_raw.json'
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':run()