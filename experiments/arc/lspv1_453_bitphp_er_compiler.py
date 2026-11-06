#!/usr/bin/env python3
"""Strict3 bit-PHP to unary-PHP, proof-carrying *proposed ER* upper simulation.
No historical R_mix341 checker or unrestricted lower-bound claims.
"""
import json, argparse, time, hashlib, itertools, os

def norm(c):
    a=set(c)
    if any(-l in a for l in a): raise AssertionError(f'tautology {c}')
    return sorted(a,key=lambda l:(abs(l),l<0))

def res(a,b,p):
    if p in a and -p in b:
        return norm([x for x in a if x!=p]+[x for x in b if x!=-p])
    if -p in a and p in b:
        return norm([x for x in a if x!=-p]+[x for x in b if x!=p])
    raise AssertionError(('invalid pivot',p,a,b))

def build(ell,pigeons=None):
    assert ell>=2
    n=1<<ell; pigeons=pigeons or n+1; original=pigeons*ell
    bit=lambda i,t:i*ell+t+1
    nxt=original
    sources=[]; steps=[]; defs=[]; byid={}; idn=0
    def add(kind,clause,parents=None,pivot=None,gate=None):
        nonlocal idn
        idn+=1; row={'id':idn,'kind':kind,'clause':norm(clause)}
        if parents is not None:row['parents']=parents
        if pivot is not None:row['pivot']=pivot
        if gate is not None:row['gate']=gate
        byid[idn]=row;steps.append(row)
        if kind=='src': sources.append(row)
        return idn
    def R(a,b,p):
        return add('res',res(byid[a]['clause'],byid[b]['clause'],p),[a,b],p)
    def fresh():
        nonlocal nxt
        nxt+=1; return nxt
    def signed_match(i,t,h):return bit(i,t) if (h>>t)&1 else -bit(i,t)
    # Standard binary split into proper 3clauses, then derive original 2ell-clause by strict resolution.
    source_orig={}
    for i,j in itertools.combinations(range(pigeons),2):
        for h in range(n):
            wide=[-signed_match(i,t,h) for t in range(ell)]+[-signed_match(j,t,h) for t in range(ell)]
            k=len(wide); zs=[fresh() for _ in range(k-3)]
            ids=[add('src',[wide[0],wide[1],zs[0]])]
            for t in range(1,k-3):
                ids.append(add('src',[-zs[t-1],wide[t+1],zs[t]]))
            ids.append(add('src',[-zs[-1],wide[-2],wide[-1]]))
            cur=ids[0]
            for t in range(k-3):
                cur=R(cur,ids[t+1],zs[t])
            assert byid[cur]['clause']==norm(wide)
            source_orig[(i,j,h)]=cur
    # Defs: share a two-input signed-AND gate for each address prefix of length >= 2.
    gates={}; tops={}; forward={}; reverse={}
    for i in range(pigeons):
        prefix={}
        for depth in range(2,ell+1):
            for pref in range(1<<depth):
                right=signed_match(i,depth-1,pref)
                left=(signed_match(i,0,pref) if depth==2 else prefix[(depth-1,pref&((1<<(depth-1))-1))]['out'])
                out=fresh();gateid=len(defs)+1
                facets=[[-out,left],[-out,right],[out,-left,-right]]
                d={'gate':gateid,'out':out,'inputs':[left,right],'facets':[]}
                defs.append(d)
                for f in facets:d['facets'].append(add('facet',f,gate=gateid))
                prefix[(depth,pref)]=d
        for h in range(n):
            ls=[signed_match(i,t,h) for t in range(ell)]
            chain=[prefix[(depth,h&((1<<depth)-1))] for depth in range(2,ell+1)]
            left=chain[-1]['out']
            tops[(i,h)]=left;gates[(i,h)]=chain
            # reverse: final out or negated all original matching inputs
            cur=chain[-1]['facets'][2]
            for d in chain[-2::-1]:
                # cur contains -d.out and d.reverse contains +d.out
                cur=R(cur,d['facets'][2],d['out'])
            assert byid[cur]['clause']==norm([left]+[-x for x in ls])
            reverse[(i,h)]=cur
            # forward: top implies each original match literal
            for t in range(ell):
                # Generic forward path from top to leaf using AND structure.
                cur=chain[-1]['facets'][0] if t<ell-1 else chain[-1]['facets'][1]
                if t<ell-1:
                    target_idx=max(0,t-1)
                    for idx in range(ell-3,target_idx-1,-1):
                        d=chain[idx]
                        cur=R(cur,d['facets'][0],d['out']) if idx>target_idx else R(cur,d['facets'][0 if t==0 else 1],d['out'])
                    # For ell=2, current was top first facet, need direct if t=0 (first input) or t=1 (second input).
                    if ell==2: cur=chain[0]['facets'][t]
                assert byid[cur]['clause']==norm([-left,ls[t]]), (ell,i,h,t,byid[cur]['clause'],[-left,ls[t]])
                forward[(i,h,t)]=cur
    # Unary at least one hole per pigeon, via Shannon resolution of all n reverse facets
    atleast={}
    for i in range(pigeons):
        layer={h:reverse[(i,h)] for h in range(n)}
        for t in reversed(range(ell)):
            nxt_layer={}
            for h in range(1<<t):
                a=layer[h]; b=layer[h+(1<<t)]
                # At step t, bit literal of position t complementary.
                nxt_layer[h]=R(a,b,bit(i,t))
            layer=nxt_layer
        assert len(layer)==1
        atleast[i]=layer[0]
        assert set(byid[atleast[i]]['clause'])==set(tops[(i,h)] for h in range(n))
    # Pairwise noncollision from original wide clause with ell*2 gate forward facets.
    uniqueness={}
    for i,j in itertools.combinations(range(pigeons),2):
        for h in range(n):
            cur=source_orig[(i,j,h)]
            for t in range(ell):cur=R(cur,forward[(i,h,t)],bit(i,t))
            for t in range(ell):cur=R(cur,forward[(j,h,t)],bit(j,t))
            assert byid[cur]['clause']==norm([-tops[(i,h)],-tops[(j,h)]])
            uniqueness[(i,j,h)]=cur
    return {'ell':ell,'holes':n,'pigeons':pigeons,'bit_vars':original,'total_vars':nxt,
            'sources':len(sources),'def_gates':len(defs),'res_nodes':sum(x['kind']=='res' for x in steps),
            'derived_unary_atleast':len(atleast),'derived_unary_uniqueness':len(uniqueness),
            'steps':steps,'defs':defs,'atleast':list(atleast.values()),'uniqueness':list(uniqueness.values()),
            'status':'Polynomial-source-to-unary-PHP compiler in separate ER gate-facet calculus; not R_mix341'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--ell',type=int,nargs='+',default=[2,3]);ap.add_argument('--out',default='/mnt/data/lspv1_453');ap.add_argument('--sat-control',action='store_true');args=ap.parse_args();os.makedirs(args.out,exist_ok=True)
    sums=[]
    cases=[(e,None) for e in args.ell]+([(2,4)] if args.sat_control else [])
    for ell,pigeons in cases:
        start=time.perf_counter(); result=build(ell,pigeons)
        raw=json.dumps(result,sort_keys=True,separators=(',',':'))
        path=f'{args.out}/bitphp_ell{ell}_pigeons{result["pigeons"]}_er_compiler.json';open(path,'w').write(raw+'\n')
        stats={k:v for k,v in result.items() if k not in ('steps','defs','atleast','uniqueness')};stats['time_sec']=round(time.perf_counter()-start,5);stats['raw_bytes']=os.path.getsize(path);stats['sha256']=hashlib.sha256((raw+'\n').encode()).hexdigest();sums.append(stats)
        print(stats)
    open(f'{args.out}/results.json','w').write(json.dumps(sums,indent=2)+'\n')
if __name__=='__main__':main()
