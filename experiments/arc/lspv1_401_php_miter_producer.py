#!/usr/bin/env python3
"""LSPV-1/401: PHP cofactor-miter proof-system firewall.
Dependency-free. Run from repository root: python experiments/arc/lspv1_401_php_miter_producer.py
Finite tests do NOT prove Haken's asymptotic theorem.
"""
import json, math, itertools, hashlib, pathlib
OUT = pathlib.Path('results/raw/arc/2026-11-04_1500_LSPV1_PHP_COFAC_MITER401_raw.json')
checks = 0

def ck(x, msg='assertion'):
    global checks
    checks += 1
    if not x: raise AssertionError(msg)

def php(h):
    def p(i,a): return (i-1)*h+a
    pos = [tuple(p(i,a) for a in range(1,h+1)) for i in range(1,h+2)]
    neg = [(-p(i,a),-p(j,a)) for a in range(1,h+1)
           for i in range(1,h+2) for j in range(i+1,h+2)]
    return tuple(pos+neg), p

def satisfied(form, bits):
    return all(any(bits[abs(l)-1]==int(l>0) for l in clause) for clause in form)

def gamma(v):
    assert v>0
    b=format(v,'b')
    return '0'*(len(b)-1)+b

def encode(F, V):
    w=max(1,math.ceil(math.log2(V+1)))
    return '1011'+gamma(V+1)+gamma(len(F)+1)+''.join(
        gamma(len(c)+1)+''.join(('1' if l<0 else '0')+format(abs(l),f'0{w}b') for l in c)
        for c in F)

def decode(bits):
    j=0
    def take(n):
        nonlocal j
        if j+n>len(bits): raise ValueError('truncated')
        v=bits[j:j+n];j+=n;return v
    if take(4)!='1011': raise ValueError('wrong tag')
    def ungamma():
        nonlocal j
        zeros=0
        while True:
            b=take(1)
            if b=='1':break
            zeros+=1
        return int('1'+take(zeros),2)
    V=ungamma()-1; M=ungamma()-1
    if V<1 or M<0 or V>10000 or M>100000:raise ValueError('bad dimensions')
    w=max(1,math.ceil(math.log2(V+1)))
    clauses=[]
    for _ in range(M):
        L=ungamma()-1
        if L<1 or L>V*2+2:raise ValueError('bad clause width')
        c=[]
        for _ in range(L):
            sign=take(1)
            var=int(take(w),2)
            if var<1 or var>V:raise ValueError('bad id')
            c.append(-var if sign=='1' else var)
        clauses.append(tuple(c))
    if j != len(bits): raise ValueError('trailing')
    return V,tuple(clauses)

def resolvent(a,b,pivot):
    if pivot in a and -pivot in b:
        return tuple(sorted((set(a)-{pivot})|(set(b)-{-pivot})))
    if -pivot in a and pivot in b:
        return tuple(sorted((set(a)-{-pivot})|(set(b)-{pivot})))
    raise ValueError('not opposite pivots')

def verify_resolution(F,proof):
    nodes=list(F)
    for rec in proof:
        ia,ib,v,claimed=rec
        if not (isinstance(ia,int) and isinstance(ib,int) and ia>=0 and ib>=0 and ia<len(nodes) and ib<len(nodes)):
            raise ValueError('bad references')
        r=resolvent(nodes[ia],nodes[ib],v)
        if len(set(r))!=len(r) or any(-l in r for l in r): raise ValueError('tautology')
        if tuple(sorted(claimed)) != r:raise ValueError('bad resolvent')
        nodes.append(r)
    return len(proof)>0 and nodes[-1]==()

rows=[]
for h in (1,2,3):
    P,p=php(h)
    n=h*(h+1)
    M=(h+1)+h*(h+1)*h//2
    ck(len(P)==M,'php clause count')
    target=(-p(1,1),-p(2,1))
    ck(P.count(target)==1,'collision unique')
    Pdel=tuple(c for c in P if c!=target)
    witness=[0]*n
    for pigeon in range(1,h+2):
        hole=1 if pigeon<=2 else pigeon-1
        witness[p(pigeon,hole)-1]=1
    ck(satisfied(Pdel,witness),'deleted PHP SAT sibling')
    ck(not satisfied(P,witness),'original PHP witness must fail')
    n_original_models=0
    for uv in itertools.product((0,1),repeat=n):
        n_original_models+=int(satisfied(P,uv))
    ck(n_original_models==0,'PHP must be UNSAT at tested h')
    for k in (1,h+1):
        V=n+k
        for i in range(1,k+1):
            others=tuple(-(n+j) for j in range(1,k+1) if j!=i)
            D=P+tuple((z,) for z in others)
            Ddel=Pdel+tuple((z,) for z in others)
            b=encode(D,V)
            vv,parsed=decode(b)
            ck(vv==V and parsed==D,'binary encoding roundtrip')
            ck(satisfied(Ddel,tuple(witness+[0]*k)),'SAT neighbor of miter')
            ck(not satisfied(D,tuple(witness+[0]*k)),'UNSAT original under sibling witness')
            evaluated=0
            for u in itertools.product((0,1),repeat=n):
                Pval=int(satisfied(P,u));Pdelval=int(satisfied(Pdel,u))
                for xa in itertools.product((0,1),repeat=k):
                    a=int(any(xa))
                    C=a & Pval
                    ck(C==0,'bad semantic constant claim')
                    only_other=int(any(xa[j] for j in range(k) if j!=i-1))
                    f0=only_other & Pval
                    f1=Pval
                    d=f0 ^ f1
                    miter=Pval & (1-only_other)
                    ck(d==miter,'miter identity')
                    if xa[i-1]==0:
                        full=list(u)+list(xa)
                        ck(int(satisfied(D,full))==miter,'CNF cofactor identity')
                    if Pdelval and only_other==0:
                        ck((only_other & Pdelval)^Pdelval==1,'SAT cofactor distinction')
                    evaluated+=1
            proof_nodes=None
            if h==1:
                idx1=D.index((p(1,1),))
                idx2=D.index((p(2,1),))
                idxn=D.index((-p(1,1),-p(2,1)))
                r1=tuple(sorted((-p(2,1),)))
                proof=[(idx1,idxn,p(1,1),r1),(idx2,len(D),p(2,1),())]
                ck(verify_resolution(D,proof),'valid strict proof')
                proof_nodes=len(proof)
                for bad in [ [(idx1,idxn,987,r1),proof[1]],
                             [(idx1,idxn,p(1,1),()),proof[1]],
                             [(idx1,10000,p(1,1),r1),proof[1]] ]:
                    try:verify_resolution(D,bad)
                    except ValueError: ck(True)
                    else:ck(False,'corrupted proof accepted')
            rows.append({'holes':h,'pigeons':h+1,'k':k,'pivot_x':i,
                         'variables_php':n,'php_clauses':len(P),'php_literal_occurrences':sum(map(len,P)),
                         'full_miter_variables':V,'miter_clauses':len(D),
                         'miter_encoded_bits':len(b),'miter_checked_assignments':evaluated,
                         'deleted_clause':list(target),'witness_pigeon_locations':
                         [1 if q<=2 else q-1 for q in range(1,h+2)],
                         'source_php_models':n_original_models,
                         'strict_res_upper_nodes_if_h1':proof_nodes})
for bad in ['0000'+b[4:], b[:-1],b+'1','']:
    try:decode(bad)
    except (ValueError,IndexError):ck(True)
    else:ck(False,'malformed source accepted')
result={
 'identifier':'LSPV1_401_PHP_COFAC_MITER_FIREWALL',
 'status':'FINITE CONTROLS ONLY. Haken asymptotic lower bound is published theorem, not computed.',
 'model':'explicit CNF signed-ID grammar, fixed source P_h, ordinary shared-DAG strict Resolution versus ER',
 'theorem':'D_i = P_h AND all negative other-x units; every Resolution refutation needs 2^Omega(h) lines by restriction; ER has poly(h) lines; semantic support of C=0.',
 'rows':rows,'producer_assertions':checks,
 'checked_at':'2026-11-04 PST',
 'sha256_source_pseudocode':'hash raw independent of proof-system lower bound'
}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'rows':len(rows),'assertions':checks,'output':str(OUT),'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest()},indent=2))
