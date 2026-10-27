#!/usr/bin/env python3
"""ARC196: connected minimally UNSAT proper 3CNF, authenticated Resolution and sign-probe controls.
Deterministic standard library only, no third-party dependencies or randomness.
Designed to finish in under 30 seconds. Output: JSON to local working directory.
"""
import hashlib
import json
from pathlib import Path

def make_chain(k):
    assert k >= 1
    x=list(range(1,k+2))
    z=list(range(k+2,2*k+2))
    a,b,c,d=range(2*k+2,2*k+6)
    first=[(x[0],sa*a,sb*b) for sa,sb in ((1,1),(1,-1),(-1,1),(-1,-1))]
    links=[]
    for i in range(k):
        links.extend([(-x[i],x[i+1],z[i]),(-x[i],x[i+1],-z[i])])
    last=[(-x[-1],sa*c,sb*d) for sa,sb in ((1,1),(1,-1),(-1,1),(-1,-1))]
    clauses=first+links+last
    return clauses,dict(x=x,z=z,a=a,b=b,c=c,d=d,v=2*k+5,m=2*k+8,k=k)

def evaluate(clauses,witness):
    return all(any((witness[abs(lit)] if lit>0 else not witness[abs(lit)]) for lit in clause) for clause in clauses)

def deletion_witness(info,j,clauses):
    k=info['k'];x=info['x']
    w={v:False for v in range(1,info['v']+1)}
    if j<4:
        pass
    elif j<4+2*k:
        i=(j-4)//2
        for h in range(i+1): w[x[h]]=True
    else:
        for v in x: w[v]=True
    for lit in clauses[j]:
        v=abs(lit)
        if v not in x: w[v]=(lit<0)
    return w

def certify_resolution(clauses,info):
    proof=[(tuple(c),None,None) for c in clauses]
    def resolve(i,j,pivot):
        a,b=set(proof[i][0]),set(proof[j][0])
        assert pivot in a and -pivot in b,(i,j,pivot,a,b)
        c=(a-{pivot})|(b-{-pivot})
        assert all(-t not in c for t in c)
        proof.append((tuple(sorted(c,key=lambda t:(abs(t),t<0))),(i,j),pivot))
        return len(proof)-1
    b=info['b'];a=info['a']
    p=resolve(0,1,b);q=resolve(2,3,b);current=resolve(p,q,a)
    for i in range(info['k']):
        idx=4+2*i;z=info['z'][i];x=info['x'][i]
        link=resolve(idx,idx+1,z)
        current=resolve(current,link,x)
    idx=4+2*info['k'];c=info['c'];d=info['d']
    p=resolve(idx,idx+1,d);q=resolve(idx+2,idx+3,d);last=resolve(p,q,c)
    terminal=resolve(current,last,info['x'][-1])
    assert proof[terminal][0]==()
    assert len(proof)-len(clauses)==len(clauses)-1
    pending=[terminal];seen=set()
    while pending:
        cur=pending.pop()
        if cur in seen:continue
        seen.add(cur)
        if proof[cur][1] is not None:pending.extend(proof[cur][1])
    assert set(range(len(clauses)))<=seen
    for i,(cl,parents,pivot) in enumerate(proof):
        if parents is None:assert cl==clauses[i]
        else:
            l,r=parents;assert l<i and r<i
            aa,bb=set(proof[l][0]),set(proof[r][0])
            assert pivot in aa and -pivot in bb
            assert set(cl)==(aa-{pivot})|(bb-{-pivot})
    return len(proof),len(proof)-len(clauses)

def encode(clauses,info):
    width=max(info['v'],info['m']).bit_length()
    header=('1'*width)+'0'+f"{info['v']:0{width}b}"+f"{info['m']:0{width}b}"
    records=[''.join(('1' if l<0 else '0')+f'{abs(l):0{width}b}' for l in c)+'1' for c in clauses]
    bits=header+''.join(records)
    assert len(bits)==3*width+1+info['m']*(3*(width+1)+1)
    return bits,[len(header)+j*(3*(width+1)+1) for j in range(len(clauses))],width

def independent_unsat_exhaustive(clauses,v):
    for mask in range(1<<v):
        w={i+1:bool(mask&(1<<i)) for i in range(v)}
        if evaluate(clauses,w):return False
    return True

def run():
    assertions=0;rows=[]
    for k in range(1,33):
        clauses,info=make_chain(k);v=info['v'];M=info['m']
        assert len(clauses)==2*k+8 and v==2*k+5;assertions+=2
        assert len(set(clauses))==M;assertions+=1
        assert all(len(c)==3 and len({abs(z) for z in c})==3 for c in clauses);assertions+=1
        var_adj={i:set() for i in range(1,v+1)}
        for C in clauses:
            vs=[abs(t) for t in C]
            for i in vs:var_adj[i].update(z for z in vs if z!=i)
        seen={1};stack=[1]
        while stack:
            t=stack.pop()
            for j in var_adj[t]-seen:seen.add(j);stack.append(j)
        assert len(seen)==v;assertions+=1
        for j,C in enumerate(clauses):
            w=deletion_witness(info,j,clauses)
            assert not evaluate(clauses,w);assertions+=1
            assert evaluate(clauses[:j]+clauses[j+1:],w);assertions+=1
            for h in range(3):
                cc=list(clauses);c=list(C);c[h]=-c[h];cc[j]=tuple(c)
                assert evaluate(cc,w);assertions+=1
        lines,inferences=certify_resolution(clauses,info);assertions+=1
        bits,starts,width=encode(clauses,info);assertions+=1
        for j,C in enumerate(clauses):
            for h in range(3):
                loc=starts[j]+h*(width+1)
                edited=bits[:loc]+('0' if bits[loc]=='1' else '1')+bits[loc+1:]
                assert len(edited)==len(bits) and sum(a!=b for a,b in zip(bits,edited))==1
                assertions+=1
        if k<=4:
            assert independent_unsat_exhaustive(clauses,v);assertions+=1
            c=list(clauses[0]);c[0]=-c[0]
            f=list(clauses);f[0]=tuple(c)
            assert not independent_unsat_exhaustive(f,v);assertions+=1
        rows.append({'k':k,'variables':v,'clauses':M,'source_bits':len(bits),
            'critical_sign_bits':3*M,'resolution_inferences':inferences,
            'resolution_lines':lines,'connected':True,'minimally_unsat':True,
            'source_sha256':hashlib.sha256(bits.encode()).hexdigest()})
    raw={'run_id':'ARC196_CONNECTED_MUS_SOURCE_PROBE','seed':None,
         'mode':'symbolic proof with deterministic finite controls',
         'assertions':assertions,'failures':0,'n_values':[1,32],
         'exhaustive_truth_tables_k':[1,2,3,4],
         'model':'ordinary proper 3CNF, canonical fixed-width signed literal fields, NOT signed exact-(2,2)',
         'rows':rows,
         'scope':'Finite checks corroborate; symbolic proof establishes infinite claims; no superlinear SAT bound.'}
    output=Path('2026-10-27_0031_ARC196_probe_resolution_raw.json')
    output.write_text(json.dumps(raw,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'assertions':assertions,'failed':0,'sample':rows[0],'last':rows[-1],
        'json_sha256':hashlib.sha256(output.read_bytes()).hexdigest()},indent=2))

if __name__=='__main__':run()
