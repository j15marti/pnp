"""New bounded-occurrence controls; no physical solver timing claim."""
from itertools import product, combinations
from pathlib import Path
import hashlib,json
from t5_construction_occurrence5_20261121 import C, graph, split, encode, decode, graph_count

def source_witness(v,edges,colors):
    vals=list(range(5))+list(colors)
    for x in colors:
        vals.extend([next(p for p in range(5) if C(0,x,p)),next(q for q in range(5) if C(1,x,q))])
    vals.extend(next(l for l in range(5) if C(colors[u],colors[w],l)) for u,w in edges)
    return vals

def lift(vals,nn,copies,links,flips):
    a=[None]*nn
    for v,xs in enumerate(copies):
        for x in xs:a[x]=vals[v]
    for j,b in enumerate(links):
        s=a[b['u']]; d=-1 if j in flips else 1
        for k,z in enumerate(b['aux'],1): a[z]=(s+d*k)%5
    return a

def main():
    cases=[]
    graphs=[('K23',[(i,j) for i in range(2) for j in range(2,5)]),('K4_isolate',list(combinations(range(4),2)))]
    for name,edges in graphs:
        n,cs=graph(5,edges);nn,out,copies,links=split(n,cs)
        colors=[list(a) for a in product(range(3),repeat=5) if all(a[u]!=a[v] for u,v in edges)]
        z=graph_count(5,edges);bits=encode(nn,out)
        assert decode(bits)==(nn,out) and (nn,len(out),len(bits),len(links))==(211,243,6059,37)
        row=dict(name=name,edges=edges,n_source=n,m_source=len(cs),N_source=len(encode(n,cs)),n=nn,m=len(out),N=len(bits),E=len(links),graph_colorings=len(colors),source_count=z,target_count=z*(1<<len(links)),label='SAT' if colors else 'UNSAT',clauses=out,encoding=bits)
        if colors:
            w=source_witness(5,edges,[x+2 for x in colors[0]])
            assert all(C(*(w[x] for x in t)) for t in cs)
            canonical=lift(w,nn,copies,links,set());checks=0;seen=set()
            # Exhaust all first-eight orientation choices; hold other29 at+.
            for mask in range(256):
                a=lift(w,nn,copies,links,{j for j in range(8) if mask>>j&1})
                assert all(C(*(a[x] for x in t)) for t in out)
                seen.add(tuple(a));checks+=1
            assert len(seen)==256
            # Also flip each of all37 coordinates separately.
            for j in range(37):
                a=lift(w,nn,copies,links,{j})
                assert a!=canonical and all(C(*(a[x] for x in t)) for t in out)
                checks+=1
            reflected=[(-x)%5 for x in canonical]
            assert all(C(*(reflected[x] for x in t)) for t in out)
            perm=list(reversed(range(nn)));renamed=[tuple(perm[x] for x in t) for t in out]
            rv=[0]*nn
            for x in range(nn):rv[perm[x]]=canonical[x]
            assert all(C(*(rv[x] for x in t)) for t in renamed)
            row.update(canonical_witness=canonical,source_witness=w,checked_lifts=checks,distinct_eight_bit_lifts=len(seen),independent_orientation_best_guess_denominator=1<<37)
        else: assert z==0
        cases.append(row)
    # Smallest E=1 source in clause/variable counts: two clauses sharing one name.
    n=5;cs=[(0,1,2),(0,3,4)];nn,out,cp,lk=split(n,cs)
    assert len(lk)==1
    source=next(a for a in product(range(5),repeat=n) if all(C(*(a[x] for x in t)) for t in cs))
    a=lift(source,nn,cp,lk,set());b=lift(source,nn,cp,lk,{0})
    assert a!=b and all(C(*(b[x] for x in t)) for t in out)
    tiny=dict(n=nn,m=len(out),N=len(encode(nn,out)),source_clauses=cs,clauses=out,witnesses=[a,b],E=1,conditional_orientation_entropy_bits=1)
    # Two independent coins have four equiprobable pairs: canonical sampler
    # may output a valid witness but matches an independently requested coin1/2.
    matches=sum(x==y for x,y in product(range(2),repeat=2))
    assert matches==2
    r=dict(status='PASS',cases=cases,minimal=tiny,independent_coin_matches=[matches,4],code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),dependency_sha256=hashlib.sha256(Path(__file__).with_name('t5_construction_occurrence5_20261121.py').read_bytes()).hexdigest(),scope='finite witness lifting and exact graph coloring; no full expanded count or arbitrary solver trace enumeration',seed=None)
    print(json.dumps(r,indent=2,sort_keys=True))
if __name__=='__main__':main()
