#!/usr/bin/env python3
"""Independent ARC265 raw-result verifier, not importing producer.py.
Exhaustive both-label source oracle up to n=18; independent pair-mode enumeration.
"""
import json,hashlib,itertools,collections,pathlib,copy
SOURCE=pathlib.Path(__file__).with_name('raw.json')

def models(F,n):
    masks=[]
    for cl in F:
        pm=nm=0
        for l in cl:
            if l>0:pm|=1<<(l-1)
            else:nm|=1<<(-l-1)
        masks.append((pm,nm))
    mask=(1<<n)-1;total=0
    for a in range(1<<n):
        if all((pm&a) or (nm&(~a&mask)) for pm,nm in masks):total+=1
    return total

def eval_clause(cl,partial):return sum(partial[abs(l)]==int(l>0) for l in cl)

def independent_grouped_xor(F,n):
    grouped=collections.defaultdict(list)
    for cl in F:
        if len(cl)!=3 or len({abs(l) for l in cl})!=3:return None
        su=tuple(sorted(abs(x) for x in cl))
        mask=tuple(int(x<0) for x in sorted(cl,key=abs))
        grouped[su].append(mask)
    # Reconstruct linear system from source clauses only, solve by independent GF(2) elimination.
    rows=[]
    for sup,patterns in grouped.items():
        if len(patterns)!=4 or len(set(patterns))!=4:return None
        if len({sum(x)&1 for x in patterns})!=1:return None
        rhs=1-(sum(patterns[0])&1)
        mask=sum(1<<(v-1) for v in sup)
        rows.append([mask,rhs])
    r=0
    for v in range(n):
        pivot=next((i for i in range(r,len(rows)) if rows[i][0]&(1<<v)),None)
        if pivot is None:continue
        rows[r],rows[pivot]=rows[pivot],rows[r]
        for i in range(len(rows)):
            if i!=r and rows[i][0]&(1<<v):
                rows[i][0]^=rows[r][0];rows[i][1]^=rows[r][1]
        r+=1
    return not any(mask==0 and rhs for mask,rhs in rows)

def check_case(case,exhaustive=True):
    F=[tuple(c) for c in case['source_clauses']];n=case['n'];m=len(F)
    assert m==case['m']
    assert hashlib.sha256(json.dumps(case['source_clauses']).encode()).hexdigest()==case['source_sha256']
    N=models(F,n) if exhaustive else None
    if N is not None:
        assert N==case['gray']['model_count'],(case['name'],N,case['gray']['model_count'])
        assert case['gray']['states']==(1<<n)
        assert (N>0)==(case['baseline']['label']=='SAT')
    assert case['portfolio']['label']==case['baseline']['label']
    assert case['endpoints']=={'zero':[sum(sum(l<0 for l in cl)==r for cl in F) for r in range(4)],'one':[sum(sum(l>0 for l in cl)==r for cl in F) for r in range(4)]}
    if case['recognized_label'] is not None:
        assert case['recognition']
        assert case['recognized_label']==case['baseline']['label']
    if case['portfolio']['winner'] in ('canonical','generic_xor'):
        yes=independent_grouped_xor(F,n)
        assert yes is not None
        assert (case['portfolio']['label']=='SAT')==yes
        assert (case['child'] is not None)==(case['recognition'])
    if case['child'] is not None:
        child=[tuple(c) for c in case['child']]
        cc=models(child,1)
        assert (cc>0)==(case['baseline']['label']=='SAT')
    e=case['extremes']
    assert len(e['source_extremes'])==len(F)
    assert len(e['pair_modes'])==m*(m-1)//2
    pair_checked=0;ext_checked=0
    for i,cl in enumerate(F):
        r=e['source_extremes'][i]
        assert r['clause']==i+1 and r['literals']==list(cl)
        assert len(r['occurrences'])==len(cl)
        for l in cl:
            v=str(abs(l))
            assert r['S'][v]==int(l>0) and r['U'][v]==int(l<0)
            assert r['invert_S_to_U'][v]==int(l<0) and r['invert_U_to_S'][v]==int(l>0)
            ext_checked+=1
    for p in e['pair_modes']:
        j=p['j']-1;k=p['k']-1
        assert j<k
        cl,other=F[j],F[k]
        vs=sorted(set(abs(x) for x in cl+other));actual={s:False for s in ('SS','SU','US','UU')}
        for b in itertools.product((0,1),repeat=len(vs)):
            a=dict(zip(vs,b));cj=eval_clause(cl,a);ck=eval_clause(other,a)
            left='S' if cj==len(cl) else 'U' if cj==0 else '-'
            right='S' if ck==len(other) else 'U' if ck==0 else '-'
            if left!='-' and right!='-':actual[left+right]=True
        assert p['matrix']==actual,(case['name'],p,actual)
        pair_checked+=4
    # Independent source flip-law checks across a fixed 16-mask path.
    for idx in range(min(16,1<<n)):
        a=[(idx>>v)&1 for v in range(n)]
        b=[1-x for x in a]
        for cl in F:
            assert sum(a[abs(l)-1]==int(l>0) for l in cl)+sum(b[abs(l)-1]==int(l>0) for l in cl)==len(cl)
    return {'clauses':m,'source_extremes':ext_checked,'pair_modes':pair_checked,'assignments':1<<n}

def check_all(raw):
    result=collections.Counter()
    for c in raw['cases']:
        x=check_case(c)
        result.update(x)
    return dict(result)

def main():
    raw=json.loads(SOURCE.read_text());summary=check_all(raw)
    broken=0
    for method in ('wrong_label','wrong_pair','wrong_extreme'):
        bad=copy.deepcopy(raw)
        if method=='wrong_label':bad['cases'][0]['portfolio']['label']='UNSAT'
        elif method=='wrong_pair':bad['cases'][0]['extremes']['pair_modes'][0]['matrix']['SS']=not bad['cases'][0]['extremes']['pair_modes'][0]['matrix']['SS']
        else:bad['cases'][0]['extremes']['source_extremes'][0]['S']['1']=1-bad['cases'][0]['extremes']['source_extremes'][0]['S']['1']
        try:check_all(bad)
        except AssertionError:broken+=1
    assert broken==3
    summary['corrupt_rejections']=broken;summary['cases']=len(raw['cases'])
    print(json.dumps(summary,indent=2))
    pathlib.Path(__file__).with_name('verification.json').write_text(json.dumps(summary,indent=2)+'\n')
if __name__=='__main__':main()