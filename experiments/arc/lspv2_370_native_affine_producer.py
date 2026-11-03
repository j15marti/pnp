#!/usr/bin/env python3
"""LSPV2-370: source-labelled Res(XOR) semantic-weakening and affine-cut macros.
Deterministic finite test cases only. No proof-search optimum is claimed.
"""
import json, itertools, hashlib, sys
from pathlib import Path

def e(mask,rhs): return [mask,rhs]
def blocker(a,d): return [e(1<<k,1-((a>>k)&1)) for k in range(d)]
def parity(a): return a.bit_count()%2

def parity_case(d):
    rows=[]; sources=[]
    def put(op, clause, **kw):
        z={'op':op,'clause':clause}; z.update(kw); rows.append(z);return len(rows)-1
    roots=[]
    for rhs in [0,1]:
        source_index={}
        for a in range(1<<d):
            if parity(a)!=rhs:
                c=blocker(a,d); idx=put('src',c);sources.append(c);source_index[a]=idx
        E=e((1<<d)-1,rhs)
        leaves=[]; fallback=next(iter(source_index.values()))
        for a in range(1<<d):
            ref=source_index.get(a,fallback)
            leaves.append(put('weak',[E]+blocker(a,d),parent=ref))
        for k in range(d):
            new=[]
            for i in range(0,len(leaves),2):
                a,b=leaves[i],leaves[i+1]
                rest=[e(1<<t,1-((i>>(t-k))&1)) for t in range(k+1,d)]
                new.append(put('cut',[E]+rest,parents=[a,b],pivot=e(1<<k,1)))
            leaves=new
        assert len(leaves)==1
        roots.append((leaves[0],E))
    a,E0=roots[0]; b,E1=roots[1]; E3=e(0,1)
    w=put('weak',[E3,e(E1[0],1-E1[1])],parent=a)
    c=put('cut',[E3],parents=[w,b],pivot=e(E1[0],1-E1[1]))
    put('weak',[],parent=c)
    return dict(kind='opposite_parity',d=d,source=sources,lines=rows,
                expected_models=0,paid=sum(z['op']!='src' for z in rows))

def factor_case(d,seed):
    M=1<<d; a_bad={a for a in range(M) if ((a*7+seed*11)%13)<5}
    b_bad={a for a in range(M) if ((a*5+seed*3)%11)<4}
    if not a_bad: a_bad.add(0)
    if not b_bad: b_bad.add(1)
    rows=[];source=[];ind={}
    for tag,bad in [('A',a_bad),('B',b_bad)]:
        for a in sorted(bad):
            C=blocker(a,d); k=len(rows);rows.append(dict(op='src',clause=C))
            source.append(C);ind[(tag,a)]=k
    output=[]
    for a in sorted(a_bad|b_bad):
        tag='A' if a in a_bad else 'B'
        k=len(rows); rows.append(dict(op='weak',clause=blocker(a,d),
                                      parent=ind[(tag,a)])); output.append(k)
    return dict(kind='canonical_factor',d=d,seed=seed,source=source,
        lines=rows,output=output,bad_A=sorted(a_bad),bad_B=sorted(b_bad),
        paid=len(output),expected_models=M-len(a_bad|b_bad))

def main():
    cases=[parity_case(d) for d in range(2,6)]
    cases += [factor_case(d,s) for d in (2,3,4,5) for s in range(1,7)]
    data=dict(run='LSPV2_370_NATIVE_AFFINE_LOCAL_PROFILE',
        model='Res(XOR): affine equations, semantic weakening, complementary affine cut',
        cases=cases,seed='deterministic formula (no RNG)',
        not_full_R_checker=True,not_optimality_certificate=True)
    path=Path(sys.argv[1] if len(sys.argv)>1 else 'raw.json')
    path.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'cases':len(cases),'paid':sum(c['paid'] for c in cases),
                      'bytes':path.stat().st_size,
                      'sha256':hashlib.sha256(path.read_bytes()).hexdigest()},indent=2))
if __name__=='__main__': main()
