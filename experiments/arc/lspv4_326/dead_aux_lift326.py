#!/usr/bin/env python3
"""LSPV-4 326 same-original F9 SAT/UNSAT dead-auxiliary lift. stdlib only.
Private fan-in-two OR-per-clause then AND-tree architecture; not minimal.
Source, pin residual, and Tseitin CNF retain different grammars.
"""
import itertools, json
from collections import Counter

F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
   (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))

def grammar(F,n):
    if 3*len(F)!=4*n or len({tuple(sorted(c)) for c in F})!=len(F):return False
    ct=Counter()
    for c in F:
        if len(c)!=3 or len({abs(x) for x in c})!=3:return False
        if any(not isinstance(x,int) or x==0 or abs(x)>n for x in c):return False
        if not (all(x>0 for x in c) or all(x<0 for x in c)):return False
        for x in c:ct[x]+=1
    return all(ct[i]==ct[-i]==2 for i in range(1,n+1))

def truth(lit,a):
    v=a.get(abs(lit))
    return None if v is None else (v==(lit>0))

def restrict(F,a):
    return tuple(tuple(x for x in c if truth(x,a) is None)
        for c in F if not any(truth(x,a) is True for x in c))

def up(F,p):
    a=dict(p);probes=0;scans=0
    while True:
        done=True
        for c in F:
            scans+=1;unk=[];sat=False
            for x in c:
                probes+=1;v=truth(x,a)
                if v is True:sat=True;break
                if v is None:unk.append(x)
            if sat:continue
            if not unk:return True,(),probes,scans
            if len(unk)==1:
                a[abs(unk[0])]=unk[0]>0;done=False;break
        if done:break
    return False,restrict(F,a),probes,scans

def circuit(F,n):
    gates=[];depth={i:0 for i in range(1,n+1)}
    def add(op,a,b):
        z=n+len(gates)+1;gates.append((z,op,a,b))
        depth[z]=1+max(depth[abs(a)],depth[abs(b)])
        return z
    outs=[]
    for c in F:
        q=c[0]
        for x in c[1:]:q=add('OR',q,x)
        outs.append(q)
    while len(outs)>1:
        outs=[add('AND',outs[i],outs[i+1]) if i+1<len(outs) else outs[i]
              for i in range(0,len(outs),2)]
    if not outs:return (),(),0,0
    clauses=[]
    for z,op,a,b in gates:
        if op=='OR':clauses.extend(((-a,z),(-b,z),(a,b,-z)))
        else:clauses.extend(((a,-z),(b,-z),(-a,-b,z)))
    clauses.append((outs[0],))
    return gates,tuple(clauses),outs[0],depth[outs[0]]

def eval_source(mask,F):
    return all(any(bool(mask & (1<<(abs(x)-1)))==(x>0) for x in c) for c in F)

def eval_circuit(mask,gates,root,n):
    a={i:bool(mask&(1<<(i-1))) for i in range(1,n+1)}
    for z,op,p,q in gates:
        u,v=truth(p,a),truth(q,a)
        a[z]=(u or v) if op=='OR' else (u and v)
    return a[root]

def count_models(p,models):
    return sum(all(bool(m&(1<<(i-1)))==b for i,b in p.items()) for m in models)

def replicate(t):
    return tuple(tuple((abs(x)+9*k)*(1 if x>0 else -1) for x in c)
          for k in range(t) for c in F)

def pins_repeated(p,t):
    return {i+9*k:b for k in range(t) for i,b in p.items()}

def widths(C):
    return dict(Counter(map(len,C)))

def main():
    assert grammar(F,9)
    g,T,root,dep=circuit(F,9)
    assert (len(g),len(T),dep)==(35,106,6)
    models=[]
    for m in range(512):
        assert eval_source(m,F)==eval_circuit(m,g,root,9)
        if eval_source(m,F):models.append(m)
    assert len(models)==70
    p0={1:False,4:False,5:True,8:False}
    p1={1:True,4:False,5:True,8:False}
    out=[]
    for p,ct,bin_src,bin_t in ((p0,7,5,19),(p1,0,7,23)):
        ss,s,_,_=up(F,p)
        tt,c,_,_=up(T,p)
        assert not ss and not tt and len(s)==bin_src
        assert widths(s)=={2:bin_src} and widths(c)=={2:bin_t,3:1}
        assert (-2,-3,-26) in c
        rr=restrict(F,p);rg,rT,_,_=circuit(rr,9)
        _,r,_,_=up(rT,p)
        assert tuple(sorted(map(tuple,sorted(r))))==tuple(sorted(map(tuple,sorted(s))))
        assert count_models(p,models)==ct and len(rg)==2*bin_src-1
        out.append(dict(x1=int(p[1]),models=ct,source_binary=bin_src,
            compiled_binary=bin_t,compiled_ternary=1,recompiled_gates=len(rg)))
    counts=Counter()
    for vals in itertools.product((None,False,True),repeat=9):
        p={i+1:v for i,v in enumerate(vals) if v is not None}
        contrad,src,_,_=up(F,p)
        if contrad or any(len(c)>2 for c in src):continue
        contrad,enc,_,_=up(T,p)
        if not contrad and any(len(c)==3 for c in enc):
            counts['SAT' if count_models(p,models) else 'UNSAT']+=1
    assert counts=={'SAT':951,'UNSAT':1}
    product_rows=[]
    for t in (1,2,3,4,8):
        G=replicate(t);assert grammar(G,9*t)
        old,oldT,_,d=circuit(G,9*t)
        sat=pins_repeated(p0,t);unsat=dict(sat);unsat[1]=True
        row=dict(t=t,n=9*t,original_clauses=12*t,private_gates=len(old),
                 private_tseitin=len(oldT),source_sat_models=7**t,source_unsat_models=0)
        for label,p,q in (('sat',sat,5*t),('unsat',unsat,5*t+2)):
            bad,source,_,_=up(G,p);assert not bad and widths(source)=={2:q}
            bad,comp,_,_=up(oldT,p);assert not bad
            assert widths(comp)=={2:19*t+(4 if label=='unsat' else 0),3:t}
            re,red,_,_=circuit(restrict(G,p),9*t)
            _,pr,_,_=up(red,p)
            assert widths(pr)=={2:q}
            row[label+'_source_binary']=q
            row[label+'_compiled_ternary']=t
            row[label+'_recompiled_gates']=len(re)
        product_rows.append(row)
    outj={'target':'proper duplicate-free Docker monotone 3-SAT-(2,2)',
       'status':'exact declared architecture; P vs NP OPEN',
       'F9_models':70,'F9_private_gate_count':35,'F9_private_depth':dep,
       'F9_tseitin_clause_count':106,'full_truth_rows':512,'coherent_pin_cubes':3**9,
       'same_original_one_bit_siblings':out,
       'source_binary_but_compiled_ternary_counts':dict(counts),
       'canonical_disjoint_family':product_rows}
    print(json.dumps(outj,indent=2,sort_keys=True))

if __name__=='__main__':main()
