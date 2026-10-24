#!/usr/bin/env python3
"""M22-COMPONENT-CLOSURE97: exhaustive grammar checks.
python M22_COMPONENT_CLOSURE97_audit.py [path_to_doecker_U_original_source.txt]
No external dependencies. Original U UNSAT imported from Docker's paper.
"""
import ast, hashlib, json, sys
from collections import Counter
from pathlib import Path

Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
H=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))

def key(c): return tuple(sorted(c,key=lambda z:abs(z)))

def grammar(f):
    seen=set(); pos=Counter(); neg=Counter()
    for c in f:
        c=key(c)
        if c in seen or len(c)!=3 or len({abs(x) for x in c})!=3: return False
        if not (all(x>0 for x in c) or all(x<0 for x in c)): return False
        seen.add(c)
        for x in c: (pos if x>0 else neg)[abs(x)]+=1
    return all(pos[x]==neg[x]==2 for x in set(pos)|set(neg))

def paired(f):
    seen=set(map(key,f))
    return all(key([-x for x in c]) in seen for c in f)

def in_star(f): return grammar(f) and not paired(f)

def components(f):
    vars_=sorted({abs(x) for c in f for x in c})
    parent={v:v for v in vars_}
    def root(v):
        while parent[v]!=v:v=parent[v]
        return v
    def union(u,v):parent[root(u)]=root(v)
    for c in f:
        a,b,d=(abs(x) for x in c);union(a,b);union(a,d)
    groups={}
    for j,c in enumerate(f):groups.setdefault(root(abs(c[0])),[]).append(j)
    return [tuple(v) for v in groups.values()]

def models(f):
    vs=sorted({abs(x) for c in f for x in c})
    assert len(vs)<=12
    at={v:i for i,v in enumerate(vs)}
    return sum(all(any(((bits>>at[abs(z)])&1)==int(z>0) for z in c) for c in f)
               for bits in range(1<<len(vs)))

def offset(f,n):return tuple(tuple((abs(x)+n)*(1 if x>0 else -1) for x in c) for c in f)

def survey(f):
    m=len(f);cm=[sum(1<<i for i in c) for c in components(f)]
    valid=star=checks=0
    for mask in range(1<<m):
        sub=[c for i,c in enumerate(f) if mask>>i&1]
        actual=grammar(sub)
        expected=all((mask&x) in (0,x) for x in cm)
        assert actual==expected,(m,mask,cm)
        valid+=int(actual);checks+=1
        if actual:
            required=any((mask&x)==x and not paired([f[i] for i in range(m) if x>>i&1]) for x in cm)
            assert in_star(sub)==required
            checks+=1;star+=int(required)
    return {'clauses':m,'components':[x.bit_count() for x in cm],'subset_checks':1<<m,
            'valid_C_M22_masks':valid,'valid_C_star_masks':star,'assertions':checks}

def projected(f):
    kept=[];removed=0
    for comp in components(f):
        block=[f[i] for i in comp]
        if paired(block): removed+=len(block)
        else:kept.extend(block)
    return tuple(kept),removed

def main():
    assert grammar(Y) and in_star(Y) and models(Y)==20
    assert grammar(H) and paired(H) and models(H)==18
    YH=Y+offset(H,6)
    assert grammar(YH) and in_star(YH) and models(YH)==360
    runs={'Y':survey(Y),'H':survey(H),'Y_plus_H':survey(YH)}
    p,drop=projected(YH)
    assert drop==8 and p==Y and in_star(p)
    checks=6+sum(x['assertions'] for x in runs.values())
    results={'id':'M22-COMPONENT-CLOSURE97','mode':'exhaustive finite subset enumeration',
             'Y_models':models(Y),'H_models':models(H),'YH_models':models(YH),'runs':runs,
             'projection_YH':{'retained_clauses':len(p),'removed_paired_clauses':drop}}
    if len(sys.argv)>1:
        content=Path(sys.argv[1]).read_text()
        U=tuple(tuple(c) for c in ast.literal_eval(content[content.index('[['):]))
        assert len(U)==264 and grammar(U) and in_star(U)
        assert [len(c) for c in components(U)]==[264]
        for i in range(len(U)):assert not grammar(U[:i]+U[i+1:])
        checks+=267
        results['U']={'source_sha256':hashlib.sha256(content.encode()).hexdigest(),
                      'clauses':len(U),'variables':198,'incidence_components':1,
                      'single_clause_deletions_checked':264,
                      'source_label':'UNSAT imported from Docker 2019, not computed'}
        UH=U+offset(H,198)
        pu,removed=projected(UH)
        assert removed==8 and pu==U and in_star(pu)
        checks+=1
        results['projection_UH']={'removed':removed,'retained':len(pu),
                                 'SAT_label':'UNSAT imported from Docker'}
    results['assertion_checks']=checks;results['failures']=0
    results['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    Path(__file__).with_name('M22_COMPONENT_CLOSURE97_results.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
    print(json.dumps(results,indent=2,sort_keys=True))
if __name__=='__main__':main()
