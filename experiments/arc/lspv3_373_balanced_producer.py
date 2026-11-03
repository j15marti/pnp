#!/usr/bin/env python3
"""Reproduce balanced authenticated Rmix341 Tseitin proofs, pure standard library."""
import json,hashlib,math,pathlib,sys

def graph(name):
    if name=='K4':
        V=list(range(4)); E=[(a,b) for a in V for b in V if a<b]
    elif name=='K33':
        V=list(range(6)); E=[(a,b) for a in range(3) for b in range(3,6)]
    elif name=='Cube':
        V=list(range(8)); E=[(a,b) for a in V for b in V if a<b and (a^b).bit_count()==1]
    elif name.startswith('Prism'):
        k=int(name[5:]); V=list(range(2*k))
        E=[tuple(sorted((l+i,l+(i+1)%k))) for l in (0,k) for i in range(k)]
        E += [(i,k+i) for i in range(k)]
    else:raise ValueError(name)
    E=sorted(set(E))
    assert all(sum(v in e for e in E)==3 for v in V)
    return V,E

def produce(name):
    V,E=graph(name); h=len(V);n=len(E)
    inc={v:[i+1 for i,e in enumerate(E) if v in e] for v in V}
    chi={v:int(v==0) for v in V}
    sources=[]; nodes=[]; tables={}; row={}
    for v in V:
        ls=[]
        for t in range(8):
            bits=[(t>>j)&1 for j in range(3)]
            if (sum(bits)&1)==chi[v]:continue
            lits=[(-a if b else a) for a,b in zip(inc[v],bits)]
            ident='s'+str(len(sources))
            sources.append({'id':ident,'v':v,'lits':lits})
            tables[ident]=[int(any(((k>>j)&1)==int(l>0) for j,l in enumerate(lits))) for k in range(8)]
            ls.append(ident)
        pairs=[]
        for a,b in ((ls[0],ls[1]),(ls[2],ls[3])):
            ident='d'+str(len(nodes))
            T=[u&v for u,v in zip(tables[a],tables[b])]
            nodes.append({'id':ident,'type':'AND3','vertex':v,'parents':[a,b],'table':T})
            tables[ident]=T; pairs.append(ident)
        a,b=pairs
        ident='d'+str(len(nodes)); T=[u&v for u,v in zip(tables[a],tables[b])]
        assert T==[int((k.bit_count()&1)==chi[v]) for k in range(8)]
        alias={'mask':inc[v],'rhs':chi[v]}
        nodes.append({'id':ident,'type':'AND3','vertex':v,'parents':[a,b],'table':T,'alias':alias})
        tables[ident]=T;row[ident]=alias
    layer=list(row)
    while len(layer)>1:
        nxt=[]
        for j in range(0,len(layer),2):
            if j+1==len(layer):nxt.append(layer[j]);continue
            a,b=layer[j:j+2]
            ra,rb=row[a],row[b]
            rr={'mask':sorted(set(ra['mask'])^set(rb['mask'])),'rhs':ra['rhs']^rb['rhs']}
            ident='d'+str(len(nodes))
            nodes.append({'id':ident,'type':'XOR','parents':[a,b],'row':rr})
            row[ident]=rr;nxt.append(ident)
        layer=nxt
    assert row[layer[0]]=={'mask':[],'rhs':1}
    assert len(sources)==4*h and len(nodes)==4*h-1
    depths={'s'+str(i):0 for i in range(len(sources))}
    for obj in nodes:depths[obj['id']]=1+max(depths[p] for p in obj['parents'])
    assert depths[layer[0]]==math.ceil(math.log2(4*h))
    dimacs=f'p cnf {n} {len(sources)}\n'+''.join(' '.join(map(str,s['lits']))+' 0\n' for s in sources)
    return {'format':'LSPV3_BALANCED_373','name':name,'vertices':h,'edges':E,
            'charge':[chi[v] for v in V],'nvariables':n,'dimacs':dimacs,
            'sources':sources,'nodes':nodes,'root':layer[0],
            'claimed':{'m':len(sources),'q':len(nodes),'depth':depths[layer[0]],
                       'dimacs_utf8_bits':8*len(dimacs.encode())}}

def main(folder):
    p=pathlib.Path(folder);p.mkdir(parents=True,exist_ok=True)
    ledger=[]
    for name in ['K4','K33','Cube','Prism3','Prism6','Prism16']:
        obj=produce(name)
        raw=json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n'
        (p/('certificate_'+name+'.json')).write_text(raw)
        ledger.append({'name':name,**obj['claimed'],'certificate_utf8_bits':8*len(raw.encode()),
                       'sha256':hashlib.sha256(raw.encode()).hexdigest()})
    (p/'producer_results.json').write_text(json.dumps(ledger,indent=2)+'\n')
    print(json.dumps(ledger,indent=2))
if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else '.')
