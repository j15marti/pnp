#!/usr/bin/env python3
"""LSPV-3 364: signed RES proof certificates for heterogeneous guarded Horn chains."""
import json,random,hashlib
from pathlib import Path
SEED=202611030624
OUT=Path(__file__).resolve().parent
def norm(clause):
    t=set(clause)
    if 0 in t or any(-x in t for x in t):raise ValueError('bad clause')
    return sorted(t,key=lambda x:(abs(x),x))
def make(n,b):
    leaf_paths=[];sources=[];srcmeta=[]
    for leaf in range(1<<b):
        path=list(range(1,n+1))
        random.Random(SEED+1000*n+100*b+leaf).shuffle(path)
        leaf_paths.append(path)
        guard=[(n+j+1) if ((leaf>>(b-1-j))&1)==0 else -(n+j+1) for j in range(b)]
        parts=[[path[0]]]+[[-path[j],path[j+1]] for j in range(n-1)]+[[-path[-1]]]
        for j,core in enumerate(parts):
            sources.append(norm(guard+core));srcmeta.append([leaf,j])
    m=len(sources);allclauses={i:tuple(c) for i,c in enumerate(sources)};proof=[];leaves=[]
    def resolve(a,c,p):
        left=set(allclauses[a]);right=set(allclauses[c])
        assert p in left and -p in right
        out=norm((left-{p})|(right-{-p}));k=m+len(proof)
        proof.append(dict(id=k,left=a,right=c,pivot=p,clause=out));allclauses[k]=tuple(out)
        return k
    for leaf,path in enumerate(leaf_paths):
        j0=leaf*(n+1);acc=j0
        for j in range(n-1):acc=resolve(acc,j0+j+1,path[j])
        acc=resolve(acc,j0+n,path[-1]);leaves.append(acc)
    layer=leaves
    for depth in range(b-1,-1,-1):
        z=n+depth+1
        layer=[resolve(layer[2*j],layer[2*j+1],z) for j in range(len(layer)//2)]
    assert len(layer)==1 and allclauses[layer[0]]==tuple()
    assert len(proof)==m-1
    dimacs='p cnf %d %d\n'%(n+b,m)+''.join(' '.join(map(str,c))+' 0\n' for c in sources)
    return {'n':n,'b':b,'seed':SEED,'paths':leaf_paths,'source':sources,'source_meta':srcmeta,
            'proof':proof,'root':layer[0],'dimacs':dimacs,'dimacs_bits':8*len(dimacs.encode()),
            'metadata':{'m':m,'q':len(proof),'num_leaf_paths':1<<b}}
def main():
    instances=[make(n,b) for (n,b) in ((3,0),(4,1),(5,2),(6,3),(8,2),(8,3))]
    payload={'id':'LSPV3-364','status':'CONSTRUCTED_RES_UPPER_NOT_GENERAL_LOWER','instances':instances}
    s=json.dumps(payload,ensure_ascii=True,separators=(',',':'),sort_keys=True)+'\n'
    (OUT/'lspv3_364_certificates.json').write_text(s)
    compact={'id':'LSPV3-364','seed':SEED,
             'dataset_sha256':hashlib.sha256(s.encode()).hexdigest(),
             'instances':[{'n':o['n'],'b':o['b'],'clauses':o['metadata']['m'],
                           'nodes':o['metadata']['q'],'input_bits':o['dimacs_bits'],
                           'proof_json_bytes':len(json.dumps(o['proof'],separators=(',',':')).encode())}
                          for o in instances]}
    (OUT/'lspv3_364_producer_summary.json').write_text(json.dumps(compact,indent=2)+'\n')
    print(json.dumps(compact,indent=2))
if __name__=='__main__':main()
