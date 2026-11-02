#!/usr/bin/env python3
"""Source-support boundary340 finite controls. Python stdlib only."""
import json, itertools, hashlib, sys
def formula(t,k):
    z=list(range(2,t+2))
    x=[[t+2+j*k+i for i in range(k)] for j in range(t)]
    H=[[-1]+z]; indices=[]
    for a,X in zip(z,x):
        start=len(H)
        H.append([-1,-a,X[0]])
        for u,v in zip(X,X[1:]):H.append([-1,-a,-u,v])
        H.append([-1,-a,-X[-1]])
        indices.append(list(range(start,len(H))))
    return 1+t+t*k,H,z,x,indices
def evalc(c,mask):
    return any(bool(mask & (1<<(abs(v)-1)))==(v>0) for v in c)
def witness(n,H,b=None):
    for mask in range(1<<n):
        if b is not None and (mask&1)!=b:continue
        if all(evalc(c,mask) for c in H):return mask
    return None
def replay(H,z,x,indices):
    db=[set(c) for c in H];steps=0;neg=[]
    def resolve(i,j,p):
        nonlocal steps
        assert p in db[i] and -p in db[j]
        result=(db[i]-{p})|(db[j]-{-p})
        assert all(-v not in result for v in result)
        db.append(result);steps+=1
        return len(db)-1
    for a,X,idx in zip(z,x,indices):
        r=idx[0]
        for i,v in enumerate(X):r=resolve(r,idx[i+1],v)
        assert db[r]=={-1,-a}
        neg.append(r)
    r=0
    for a,node in zip(z,neg):r=resolve(r,node,a)
    assert db[r]=={-1}
    return steps
def k4(odd):
    ed=[(i,j) for i in range(4) for j in range(i+1,4)]
    C=[]
    for v in range(4):
        ids=[i+1 for i,e in enumerate(ed) if v in e]
        for bits in itertools.product(range(2),repeat=3):
            if sum(bits)%2 != int(odd and v==0):
                C.append([(-i if b else i) for i,b in zip(ids,bits)])
    return C
def parser(text):
    lines=[x.strip() for x in text.splitlines() if x.strip() and not x.lstrip().startswith('c')]
    if not lines:raise ValueError('missing header')
    p=lines.pop(0).split()
    if len(p)!=4 or p[:2]!=['p','cnf']:raise ValueError('bad header')
    try:n,m=map(int,p[2:]);numbers=[int(q) for line in lines for q in line.split()]
    except ValueError:raise ValueError('bad int')
    if n<0 or m<0:raise ValueError('negative')
    C=[];cur=[]
    for v in numbers:
        if v==0:C.append(cur);cur=[]
        elif abs(v)>n:raise ValueError('out of range')
        else:cur.append(v)
    if cur or len(C)!=m:raise ValueError('unterminated or wrong count')
    return n,C
def run():
    cases=[]
    for t in range(1,4):
        for k in range(1,4):
            n,H,z,x,I=formula(t,k)
            assert witness(n,H,0) is not None
            assert witness(n,H,1) is None
            assert parser(f'p cnf {n} {len(H)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in H))==(n,H)
            p=replay(H,z,x,I);assert p==len(H)-1
            core=[[v for v in c if v!=-1] for c in H]
            assert witness(n,core) is None
            flips=deletions=0
            for j,C in enumerate(H):
                wo=H[:j]+H[j+1:]
                w=witness(n,wo,1)
                assert w is not None and not evalc(C,w)
                deletions+=1
                for i,lit in enumerate(C):
                    mod=[c[:] for c in H];mod[j][i]=-lit
                    assert all(evalc(q,w) for q in mod)
                    assert witness(n,mod,1) is not None
                    assert witness(n,mod,0) is not None
                    flips+=1
            assert flips==t*(4*k+3)+1
            cases.append(dict(t=t,k=k,variables=n,clauses=len(H),sign_occurrences=flips,
                              verified_sign_flips=flips,verified_clause_deletions=deletions,
                              resolution_inferences=p,lower_bound=len(H)-1))
    assert witness(6,k4(1)) is None
    assert witness(6,k4(0)) is not None
    malformed=['x cnf 1 2\n1 0\n-1 0\n','p cnf 0 1\n1 0\n',
               'p cnf 1 2\n1 0\n','p cnf 1 1\n1\n','p cnf 1 1\nx 0\n']
    for f in malformed:
        try:parser(f)
        except ValueError:continue
        raise AssertionError('accepted malformed')
    out={'run':'BOUNDARY_SOURCE_SUPPORT340','cases':cases,'malformed_rejected':len(malformed),
         'parity_controls':[{'graph':'K4','charge':'odd','label':'UNSAT'},
                            {'graph':'K4','charge':'even','label':'SAT'}],
         'totals':{'families':len(cases),'sign_flips':sum(c['verified_sign_flips'] for c in cases),
                   'deleted_clause_witnesses':sum(c['verified_clause_deletions'] for c in cases),
                   'certified_inferences':sum(c['resolution_inferences'] for c in cases),'all_passed':True}}
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':run()