#!/usr/bin/env python3
"""LSPV-3 PC-BRANCH-COLOUR134 finite reproducibility audit, stdlib only.
Not a computational validation of asymptotic PC degree lower bounds.
Run: python 2026-10-26_0731_PC_BRANCH_COLOUR134_repro.py [raw.json]
"""
from __future__ import annotations
import collections, hashlib, itertools, json, random, sys
SEED=13420261026
rng=random.Random(SEED)
checks=collections.Counter()
def ck(ok,key):
    checks[key]+=1
    if not ok: raise AssertionError(key)

def add(f,g,p):
    out=dict(f)
    for a,v in g.items():
        v=(out.get(a,0)+v)%p
        if v: out[a]=v
        else: out.pop(a,None)
    return out

def mul(f,g,p):
    out={}
    for a,x in f.items():
        for b,y in g.items():
            t=frozenset(a|b)
            v=(out.get(t,0)+x*y)%p
            if v: out[t]=v
            else:out.pop(t,None)
    return out

def const(c,p):return {frozenset():c%p} if c%p else {}
def var(v):return {frozenset([v]):1}
def one_minus(v,p):return add(const(1,p),{frozenset([v]):-1},p)
def prod(items,p):
    a=const(1,p)
    for item in items:a=mul(a,item,p)
    return a

def restrict_poly(f,alpha,p):
    out={}
    for mon,c in f.items():
        if any(v in alpha and alpha[v]==0 for v in mon):continue
        t=frozenset(v for v in mon if v not in alpha)
        x=(out.get(t,0)+c)%p
        if x:out[t]=x
        else:out.pop(t,None)
    return out

def delta(alpha,p):return prod([var(x) if b else one_minus(x,p) for x,b in alpha.items()],p)

def quartet(x,y,z,b):
    a=[]
    for t in itertools.product((0,1),repeat=3):
        if (sum(t)&1)!=b:
            # clause forbids this word; exactly three distinct variables
            a.append(tuple((-v if bit else v) for v,bit in zip((x,y,z),t)))
    return a

def bool_clause(clause,assignment):return any(assignment.get(abs(z),0)==(1 if z>0 else 0) for z in clause)

def pc_clause(clause,p):
    # Boolean falsity polynomial: source clause must evaluate to zero on models
    return prod([one_minus(z,p) if z>0 else var(-z) for z in clause],p)

def graph_edges(kind):
    if kind=='K3': return 3,[(0,1),(0,2),(1,2)]
    if kind=='K4': return 4,list(itertools.combinations(range(4),2))
    if kind=='K7': return 7,list(itertools.combinations(range(7),2))
    if kind=='K33': return 6,[(i,j) for i in range(3) for j in range(3,6)]
    if kind.startswith('CIRC'):
        v=int(kind[4:]);return v, sorted({tuple(sorted((i,(i+j)%v))) for i in range(v) for j in (1,2,3)})
    raise ValueError(kind)

def independent_3col(v,edges):
    adj=[set() for _ in range(v)]
    for u,w in edges:adj[u].add(w);adj[w].add(u)
    order=sorted(range(v),key=lambda i:-len(adj[i]));colour={}
    def walk(i):
        if i==v:return True
        node=order[i]
        for c in range(3):
            if all(colour.get(x)!=c for x in adj[node]):
                colour[node]=c
                if walk(i+1):return True
                del colour[node]
        return False
    return walk(0)

def graph_cnf(v,edges):
    def x(i,c):return 3*i+c+1
    base=[];binary=[]
    for i in range(v):
        base.append(tuple(x(i,c) for c in range(3)))
        for a,b in itertools.combinations(range(3),2):binary.append((-x(i,a),-x(i,b)))
    for i,j in edges:
        for c in range(3):binary.append((-x(i,c),-x(j,c)))
    base.extend(binary)
    proper=base[:v];lifts=[]
    for k,(a,b) in enumerate(binary):
        z=3*v+k+1
        proper.extend(((a,b,z),(a,b,-z)))
        lifts.append(z)
    return base,proper,lifts,3*v+len(binary)

def dimacs(F,n):
    return 'p cnf %d %d\n'%(n,len(F))+''.join(' '.join(map(str,c))+' 0\n' for c in F)

def parse(s):
    raw=s.splitlines(True)
    ck(bool(raw),'nonempty_header')
    h=raw[0].strip().split();ck(len(h)==4 and h[:2]==['p','cnf'],'header_syntax')
    n,m=map(int,h[2:]);ck(len(raw)==m+1,'header_clause_count')
    F=[];offsets=[];pos=len(raw[0].encode())
    for line in raw[1:]:
        offsets.append(pos);pos+=len(line.encode());bits=[int(z) for z in line.split()]
        ck(bits[-1]==0,'clause_zero');clause=tuple(bits[:-1]);ck(len(clause)==3,'proper_width')
        ck(len({abs(z) for z in clause})==3 and all(1<=abs(z)<=n for z in clause),'proper_names')
        F.append(clause)
    ck(pos==len(s.encode()),'source_offsets')
    return n,F,offsets

def pin(lit,n):
    a,b=n+1,n+2
    return [(lit,s*a,t*b) for s in (1,-1) for t in (1,-1)],n+2

def dpll(F):
    def rec(clauses,A):
        while True:
            pending=[];unit=None
            for C in clauses:
                if any(abs(z) in A and A[abs(z)]==(z>0) for z in C):continue
                R=tuple(z for z in C if abs(z) not in A)
                if not R:return False
                if len(R)==1:unit=R[0];break
                pending.append(R)
            if unit is None:break
            idx=abs(unit);val=unit>0
            if idx in A and A[idx]!=val:return False
            A[idx]=val
        if not pending:return True
        node=collections.Counter(abs(z) for C in pending for z in C).most_common(1)[0][0]
        for val in (True,False):
            A2=A.copy();A2[node]=val
            if rec(pending,A2):return True
        return False
    return rec(F,{})

W1_SOURCE='''-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'''
W1=[tuple(map(int,z.split())) for z in W1_SOURCE.split(';')]

def main():
    paths=[]
    for p in (2,5):
        for h in range(1,6):
            for _ in range(70):
                alpha={i:rng.randrange(2) for i in rng.sample(range(9),h)}
                f={}
                for _ in range(7):
                    mon=frozenset(rng.sample(range(9),rng.randrange(4)))
                    f=add(f,{mon:rng.randrange(p)},p)
                lhs=mul(delta(alpha,p),f,p)
                rhs=mul(delta(alpha,p),restrict_poly(f,alpha,p),p)
                ck(lhs==rhs,'delta_restriction_identity')
                x=next(i for i in range(10) if i not in alpha)
                alpha0={**alpha,x:0};alpha1={**alpha,x:1}
                ck(add(delta(alpha0,p),delta(alpha1,p),p)==delta(alpha,p),'branch_delta_merge')
        u,v,w=20,21,22
        q1=mul(var(u),one_minus(v,p),p)
        q2=mul(var(v),one_minus(w,p),p)
        lhs=add(mul(q1,one_minus(w,p),p),mul(var(u),q2,p),p)
        rhs=mul(var(u),one_minus(w,p),p)
        ck(lhs==rhs,'implication_path_PC_degree3')
    for b in (0,1):
        clauses=quartet(1,2,3,b)
        ck(len(clauses)==4,'xor_quartet_count')
        f={}
        for C in clauses:f=add(f,pc_clause(C,2),2)
        target=add(add(var(1),var(2),2),add(var(3),const(b,2),2),2)
        ck(f==target,'quartet_XOR_GF2_identity')
        for bits in itertools.product((0,1),repeat=3):
            truth={i+1:bits[i] for i in range(3)}
            ck(all(bool_clause(C,truth) for C in clauses)==((sum(bits)&1)==b),'quartet_semantics')
    for kind in ['K3','K4','K33','K7','CIRC8','CIRC9']:
        v,edges=graph_edges(kind);base,F,lifts,n=graph_cnf(v,edges)
        source=dimacs(F,n);nn,FF,offsets=parse(source)
        ck(F==FF and n==nn,'roundtrip')
        ck(all(len(c)==3 and len({abs(x) for x in c})==3 for c in F),'source_proper_3cnf')
        restricted=[tuple(x for x in C if abs(x) not in lifts) for C in F if not any(x<0 and -x in lifts for x in C)]
        ck(restricted==base,'fresh_zero_projection_equals_binary_original')
        expected=independent_3col(v,edges)
        actual=dpll(F)
        ck(actual==expected,'signed_proper_3CNF_iff_3colorable')
        for p in (2,5):
            for i,(a,b0) in enumerate(base[v:]):
                z=lifts[i];a_clause=(a,b0,z);b_clause=(a,b0,-z)
                ck(restrict_poly(pc_clause(a_clause,p),{z:0},p)==pc_clause((a,b0),p),'PCR_fresh_zero_preserves_binary_axiom')
                ck(restrict_poly(pc_clause(b_clause,p),{z:0},p)=={},'PCR_fresh_zero_kills_other_lift')
        paths.append(dict(graph=kind,vertices=v,edges=len(edges),SAT=expected,core_variables=3*v,proper_variables=n,base_clauses=len(base),proper_clauses=len(F),dimacs_bytes=len(source.encode()),first_clause_offset=offsets[0]))
    # One genuine SAT->SAT->UNSAT descendant chain with original alias identities.
    v,edges=graph_edges('K3');base,F,lifts,n=graph_cnf(v,edges)
    C1,n1=pin(1,n);C2,n2=pin(2,n1)
    stages=[(F,n),(F+C1,n1),(F+C1+C2,n2)];chain=[]
    for FF,nn in stages:
        s=dimacs(FF,nn);nn2,parsed,off=parse(s)
        ck(nn2==nn and parsed==FF,'descendant_roundtrip')
        chain.append(dict(bytes=len(s.encode()),clauses=len(FF),variables=nn,SAT=dpll(FF)))
    ck([r['SAT'] for r in chain]==[True,True,False],'SAT_SAT_UNSAT_two_levels')
    # Exact signed-(2,2) UNSAT W1 and local-under-global controls from peer source.
    occ=collections.Counter((abs(z),z>0) for c in W1 for z in c)
    ck(len(W1)==20 and all(occ[(v,True)]==2 and occ[(v,False)]==2 for v in range(1,16)),'W1_signed_2_2')
    ck(not dpll(W1),'W1_unsat')
    for i in range(len(W1)):ck(dpll(W1[:i]+W1[i+1:]),'W1_minimally_unsat')
    # Hostile SAT control: every clause in a SAT W1 deletion is still properly signed ternary.
    ck(all(len(c)==3 and len({abs(z) for z in c})==3 for c in W1),'W1_proper')
    res={'id':'PC-BRANCH-COLOUR134','status':'finite computational audit only; asymptotic theorem proved separately',
         'seed':SEED,'checks':sum(checks.values()),'failures':0,'by_test':dict(sorted(checks.items())),
         'graphs':paths,'two_real_descendants':chain,'W1':{'variables':15,'clauses':20,'unsat':True,'minimal':True},
         'PC_fields':[2,5], 'guest_A_calls':0,
         'non_claims':['not a measured PC degree lower bound','not signed-(2,2) graph colouring','not all-proof-systems lower bound','no deterministic SAT seed','ARC-EDGE-90 and P versus NP OPEN']}
    raw=json.dumps(res,indent=2,sort_keys=True)+'\n';res['normalized_sha256']=hashlib.sha256(raw.encode()).hexdigest()
    if len(sys.argv)>1:
        with open(sys.argv[1],'w') as f:json.dump(res,f,indent=2,sort_keys=True)
    print(json.dumps(res,indent=2,sort_keys=True))
if __name__=='__main__':main()