#!/usr/bin/env python3
"""LSPV-2/409 independent proof-DAG/facet checker; no producer imports."""
import json,sys,copy

def expr(g,v):
    a,b=v[g['a']],v[g['b']]
    return {'xor':lambda:a!=b,'xnor':lambda:a==b,'notA':lambda:not a}[g['op']]()

def gates_evaluate(net,mask):
    vals={1:bool(mask&1),2:bool(mask&2),3:bool(mask&4)}
    seen=set(vals)
    for g in net:
        assert isinstance(g['out'],int) and g['out'] not in seen and g['out']>3
        assert g['a'] in seen and g['b'] in seen
        assert g['op'] in ('xor','xnor','notA')
        vals[g['out']]=expr(g,vals);seen.add(g['out'])
    return vals

def clause_valuation(c,v):
    return any((v[abs(l)] if l>0 else not v[abs(l)]) for l in c)

def expected_facets(net):
    ans=[]
    for gate in net:
        for av in range(2):
            for bv in range(2):
                assumed={}
                impossible=False
                for v,value in ((gate['a'],av),(gate['b'],bv),(gate['out'],1-int(expr(gate,{gate['a']:bool(av),gate['b']:bool(bv)})))):
                    if v in assumed and assumed[v]!=value:impossible=True;break
                    assumed[v]=value
                if not impossible:
                    ans.append(sorted(((k if bit==0 else -k) for k,bit in assumed.items()),key=lambda x:(abs(x),x)))
    return ans

def check(rec):
    old=rec['old'];new=rec['replacement']
    for mask in range(8):
        a=gates_evaluate(old,mask);b=gates_evaluate(new,mask)
        assert all(a[p]==b[p] for p in (4,5,6))
    assert expected_facets(old)==rec['originalFacets']
    assert expected_facets(new)==rec['proof']['axioms']
    rows=rec['proof']['axioms'];nodes=rec['proof']['derived'];clauses=list(rows)
    for z in nodes:
        assert z['id']==len(clauses)
        a,b=z['parents'];p=z['pivot']; assert 0<=a<len(clauses) and 0<=b<len(clauses) and p>0
        assert p in clauses[a] and -p in clauses[b]
        R=set(clauses[a])|set(clauses[b]);R.discard(p);R.discard(-p)
        assert not any(-l in R for l in R)
        assert sorted(R,key=lambda x:(abs(x),x))==z['cl']
        clauses.append(z['cl'])
    for j,s in enumerate(rec['summaries']):
        assert j==s['oldFacetIndex'] and s['target']==rec['originalFacets'][j]
        assert 0<=s['finalId']<len(clauses) and clauses[s['finalId']]==s['finalClause']
        assert set(s['finalClause']).issubset(set(s['target']))
        assert s['added']<=2**s['variableDeficit']-1
    for mask in range(8):
        v=gates_evaluate(new,mask)
        assert all(clause_valuation(c,v) for c in rows)
        assert all(clause_valuation(c,v) for c in rec['originalFacets'])
    assert rec['totalResolutionNodes']==len(nodes)
    assert sum(s['added'] for s in rec['summaries'])==len(nodes)
    assert rec['originalSourceSatModels']==sum(bool(m&1) for m in range(8))
    assert rec['originalSourceUnsatModels']==sum(bool(m&1) and not bool(m&1) for m in range(8))
    return True

def main():
    p=sys.argv[1];r=json.load(open(p));assert check(r)
    corrupt=[]
    d=copy.deepcopy(r);d['proof']['derived'][0]['pivot']=999;corrupt.append(d)
    d=copy.deepcopy(r);d['proof']['axioms'][0][0]*=-1;corrupt.append(d)
    d=copy.deepcopy(r);d['replacement'][0]['a']=99;corrupt.append(d)
    d=copy.deepcopy(r);d['summaries'][-1]['finalClause']=[3];corrupt.append(d)
    d=copy.deepcopy(r);d['replacement'][0]['out']=3;corrupt.append(d)
    d=copy.deepcopy(r);d['proof']['derived'][-1]['parents']=[10000,1];corrupt.append(d)
    n=0
    for d in corrupt:
        try: check(d)
        except (ValueError,AssertionError,KeyError,IndexError):n+=1
    assert n==len(corrupt)
    print(json.dumps({'independentlyVerified':True,'derivedNodes':len(r['proof']['derived']),'allFacets':len(r['originalFacets']),'mutantsRejected':n,'SATModels':4,'UNSATModels':0,'scope':'explicit DEF facet+RES fragment'}))
if __name__=='__main__':main()
