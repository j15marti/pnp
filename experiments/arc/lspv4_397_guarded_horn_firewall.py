#!/usr/bin/env python3
"""LSPV-4/397: deterministic proper-3CNF guarded entailment and Horn proof controls.
Standard library only; independent expanded local reproducer is supplied in the archive.
"""
import itertools,json
BASE=[(1,),(-1,),(2,),(-2,),(1,2),(1,-2),(-1,2),(-1,-2)]

def sat(cnf,a):
    return all(any((a[abs(l)-1] if l>0 else not a[abs(l)-1]) for l in C) for C in cnf)
def models(cnf,n):
    return sum(sat(cnf,a) for a in itertools.product([False,True],repeat=n))
def guard(cnf):
    clauses=[];n=3
    for C in cnf:
        if len(C)==1:
            n+=1;clauses.extend([(-3,C[0],n),(-3,C[0],-n)])
        elif len(C)==2: clauses.append((-3,*C))
        else:
            n+=1;clauses.extend([(-3,C[0],n),(-n,C[1],C[2])])
    assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in clauses)
    return clauses,n

def resolve(a,b,p):
    assert p in a and -p in b
    u=(set(a)-{p}) | (set(b)-{-p})
    assert all(-l not in u for l in u)
    return tuple(sorted(u,key=lambda z:(abs(z),z<0)))
def trace_horn(cnf):
    horn=[(i,c) for i,c in enumerate(cnf) if sum(l>0 for l in c)<=1]
    known={c[0]:('source',i) for i,c in horn if len(c)==1}
    nodes=[]
    def val(ref): return cnf[ref[1]] if ref[0]=='source' else nodes[ref[1]][3]
    for _ in range(2*len(cnf)+3):
        for l,ref in list(known.items()):
            if -l in known:
                a,b=ref,known[-l]
                assert resolve(val(a),val(b),l)==()
                nodes.append((a,b,l,()))
                return 'UNSAT',nodes
        changed=False
        for i,c in horn:
            if any(l in known for l in c):continue
            false=[l for l in c if -l in known]
            remaining=[l for l in c if -l not in known]
            if len(remaining)>1 or (len(remaining)==1 and remaining[0] in known):continue
            ref=('source',i)
            for l in false:
                unit=known[-l];result=resolve(val(ref),val(unit),l)
                nodes.append((ref,unit,l,result))
                ref=('derived',len(nodes)-1)
            if not remaining:
                assert val(ref)==()
                return 'UNSAT',nodes
            assert val(ref)==(remaining[0],)
            known[remaining[0]]=ref;changed=True
        if not changed:break
    return 'PARTIAL',nodes

if __name__=='__main__':
    stats={'SAT':0,'UNSAT':0};assertions=0
    for mask in range(256):
        H=[c for j,c in enumerate(BASE) if mask & (1<<j)]
        truth=models(H,2)>0
        F,n=guard(H)
        stats['SAT' if truth else 'UNSAT']+=1
        assert models(F,n)>0
        assert (models(F+[(3,)],n)>0)==truth
        assert models(F+[(-3,)],n)>0
        assertions+=3
    assert stats=={'SAT':95,'UNSAT':161}
    plus=[(1,),(-1,2),(2,3)]
    impossible=[(1,),(-1,2),(-2,)]
    assert models(plus,3)>0 and models(impossible,2)==0
    for F in (plus,impossible):
        status,nodes=trace_horn(F)
        for j,(a,b,p,r) in enumerate(nodes):
            def get(v):return F[v[1]] if v[0]=='source' else nodes[v[1]][3]
            assert (a[0]=='source' or a[1]<j) and (b[0]=='source' or b[1]<j)
            assert resolve(get(a),get(b),p)==r;assertions+=2
        if F is impossible:assert status=='UNSAT' and nodes[-1][3]==()
    print(json.dumps({'status':'PASS','cases':256,'classifications':stats,
                      'assertions':assertions,'signed_Horn_RES_replay':'PASS'}))
