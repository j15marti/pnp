#!/usr/bin/env python3
"""LSPV-2 target-clause resolution compiler, Python producer (no imports beyond stdlib)."""
import itertools, json, hashlib

def normal(cl):
    z=frozenset(cl)
    if any(-x in z for x in z): raise ValueError('tautology')
    return z

def sat(clauses, assign):
    return all(any((assign[abs(l)] if l>0 else not assign[-l]) for l in c) for c in clauses)

def compiler(clauses, target, variables):
    """Compile Gamma |= target to a subclause using no weakening; raises if not implied."""
    src=[normal(c) for c in clauses]; tgt=normal(target)
    vars_=set(variables)
    if not set(map(abs,tgt))<=vars_ or any(not set(map(abs,c))<=vars_ for c in src): raise ValueError('support')
    fixed={abs(x):(x<0) for x in tgt}
    nodes=[{'kind':'source','clause':sorted(c)} for c in src]
    rem=sorted(vars_-set(map(abs,tgt)))
    def rec(depth,assignment):
        if depth==len(rem):
            for i,c in enumerate(src):
                if not sat([c],assignment): return i
            raise ValueError('not entailed')
        v=rem[depth]
        left=rec(depth+1,{**assignment,v:False})
        right=rec(depth+1,{**assignment,v:True})
        a=frozenset(nodes[left]['clause']); b=frozenset(nodes[right]['clause'])
        if v not in a:return left
        if -v not in b:return right
        c=normal((a-{v})|(b-{-v}))
        nodes.append({'kind':'resolve','left':left,'right':right,'pivot':v,'clause':sorted(c)})
        return len(nodes)-1
    root=rec(0,fixed)
    out=frozenset(nodes[root]['clause'])
    assert out<=tgt
    return {'nvars':len(vars_), 'target':sorted(tgt),'sources':len(src), 'new_nodes':len(nodes)-len(src), 'upper_bound':2**len(rem)-1,'root':root,'nodes':nodes}

def verify(cert):
    nodes=cert['nodes']; src=cert['sources']
    for i,n in enumerate(nodes):
        c=normal(n['clause'])
        if i<src:
            assert n['kind']=='source'; continue
        assert n['kind']=='resolve'
        a=n['left']; b=n['right']; v=n['pivot']
        assert a<i and b<i and v>0
        ca=normal(nodes[a]['clause']); cb=normal(nodes[b]['clause'])
        assert v in ca and -v in cb
        assert c==normal((ca-{v})|(cb-{-v}))
    assert normal(nodes[cert['root']]['clause'])<=normal(cert['target'])
    assert len(nodes)-src<=cert['upper_bound']
    return True

def hypercube(d):
    # x1 = u, variables 2..d+1 are y1...yd. Blocks each y assignment when u=False.
    clauses=[]
    for vals in itertools.product((False,True),repeat=d):
        clauses.append([1]+[-(j+2) if bit else (j+2) for j,bit in enumerate(vals)])
    return clauses

def example(d):
    cls=hypercube(d)
    cert=compiler(cls,[1],list(range(1,d+2))); verify(cert)
    assert cert['new_nodes']==(1<<d)-1
    full=cls+[[-1]]
    assert not any(sat(full,{j+1:bits[j] for j in range(d+1)}) for bits in itertools.product((False,True),repeat=d+1))
    for omit in range(len(full)):
        others=full[:omit]+full[omit+1:]
        assert any(sat(others,{j+1:bits[j] for j in range(d+1)}) for bits in itertools.product((False,True),repeat=d+1))
    assert (cert['new_nodes']+1)==2**d
    return {'d':d,'source_clauses':len(full),'minimum_mixed_nodes':2**d,'minimum_RES_nodes':2**d,'single_clause_translation_nodes':cert['new_nodes'],'bound':cert['upper_bound'],'certificate_sha256':hashlib.sha256(json.dumps(cert,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'certificate':cert if d<=4 else {'nvars':cert['nvars'],'root':cert['root'],'new_nodes':cert['new_nodes']}}

def main():
    records=[example(d) for d in range(1,7)]
    failures=0
    t=example(2)['certificate']
    for variant in ['pivot','target','index','conclusion','truncated']:
        c=json.loads(json.dumps(t))
        if variant=='pivot': next(n for n in c['nodes'] if n['kind']=='resolve')['pivot']=9
        if variant=='target': c['target']=[-1]
        if variant=='index': next(n for n in c['nodes'] if n['kind']=='resolve')['left']=10**6
        if variant=='conclusion': next(n for n in c['nodes'] if n['kind']=='resolve')['clause']=[999]
        if variant=='truncated': c['nodes']=c['nodes'][:c['sources']]
        try:verify(c)
        except (AssertionError,IndexError,KeyError,ValueError):failures+=1
    assert failures==5
    controls=[([[1,2],[1,-2]],[1],[1,2]), ([[1,2],[1,-2],[-1] ],[],[1,2]), ([[1,2]], [1,2],[1,2]), ([[1,2,3],[1,2,-3]],[1,2],[1,2,3])]
    for clauses,target,variables in controls:verify(compiler(clauses,target,variables))
    try:compiler([[1]],[2],[1,2])
    except ValueError: failures+=1
    assert failures==6
    data={'status':'COMPUTATIONAL','theorem':'Single target clause consequence with at most 2^(k-|C|)-1 RES nodes; tight full mixed source-core family','source':'lspv2_403_target_clause_producer.py','tests':{'d_range':[1,6], 'malformed_rejections':failures,'both_labels':True,'independent_entailment_controls':len(controls)},'rows':records}
    with open('lspv2_403_target_clause_raw.json','w') as f:json.dump(data,f,indent=2)
    print(json.dumps([{k:v for k,v in r.items() if k!='certificate'} for r in records],indent=2))
    print('malformed_rejections',failures)
if __name__=='__main__':main()
