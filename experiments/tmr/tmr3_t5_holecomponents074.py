"""TMR-3/074 exact fixed T5 CSP count for triple-incidence graphs with few missing triples.
Uses only Python stdlib. An audit compares with independent five-color hub enumeration.
"""
from itertools import combinations, product
from collections import defaultdict, deque
from math import comb
import json, random, hashlib, sys

REV = 'tmr3-t5-holes-components074-v1'
SEED = 202611171824


def encode_graph(n, arcs):
    width = max(1, (max(2,n)-1).bit_length())
    def bits(v): return ''.join('1' if ((v>>i)&1) else '0' for i in range(width))
    return '1'*n+'0'+'1'*len(arcs)+'0'+''.join(bits(u)+bits(v) for u,v in arcs)


def decode_graph(src):
    if not isinstance(src,str) or any(b not in '01' for b in src):
        raise ValueError('nonbinary')
    pos=0
    def unary():
        nonlocal pos
        start=pos
        while pos < len(src) and src[pos]=='1': pos+=1
        if pos==len(src): raise ValueError('delimiter')
        pos+=1
        return pos-start-1
    n=unary(); m=unary()
    w=max(1,(max(2,n)-1).bit_length())
    if len(src)-pos!=2*w*m: raise ValueError('length')
    arcs=[]
    for t in range(m):
        u=sum((src[pos+i]=='1')<<i for i in range(w))
        v=sum((src[pos+w+i]=='1')<<i for i in range(w))
        pos+=2*w
        if u>=n or v>=n: raise ValueError('endpoint')
        arcs.append((u,v))
    return n,sorted(set(arcs))


def incidence_graph(k, missing):
    missing=set(tuple(sorted(t)) for t in missing)
    present=[t for t in combinations(range(k),3) if t not in missing]
    return k+len(present),[(i,k+j) for j,t in enumerate(present) for i in t]


def recognize(n,arcs):
    inn=[set() for _ in range(n)]; out=[set() for _ in range(n)]
    for u,v in arcs:
        if u==v: return None
        out[u].add(v);inn[v].add(u)
    hub=[i for i in range(n) if not inn[i] and out[i]]
    leaves=[i for i in range(n) if not out[i] and len(inn[i])==3]
    if len(hub)<6 or len(hub)+len(leaves)!=n: return None
    index={v:i for i,v in enumerate(hub)}
    observed=[]
    for v in leaves:
        if not inn[v].issubset(index): return None
        observed.append(tuple(sorted(index[t] for t in inn[v])))
    if len(observed)!=len(set(observed)):return None
    seen=set(observed)
    missing=[t for t in combinations(range(len(hub)),3) if t not in seen]
    k=len(hub)
    if len(missing)>=k-2:return None
    return k,missing


def components(k,missing):
    adj=[set() for _ in range(k)]
    for a,b,c in missing:
        adj[a].update((b,c));adj[b].update((a,c));adj[c].update((a,b))
    groups=[]; used=set()
    for v in range(k):
        if v in used: continue
        Q=[v];used.add(v)
        for u in Q:
            for w in adj[u]:
                if w not in used:used.add(w);Q.append(w)
        groups.append(sorted(Q))
    return groups


def hole_dp(k,missing):
    """Uncolored hubs assigned symbolic 0/1; return exact coefficients A[p,j]."""
    groups=components(k,missing)
    table={(0,0):1}
    for group in groups:
        idx={v:i for i,v in enumerate(group)}
        local_edges=[tuple(idx[v] for v in t) for t in missing if t[0] in idx]
        local=defaultdict(int)
        for mask in range(1<<len(group)):
            p=mask.bit_count();j=0
            for a,b,c in local_edges:
                ca=(mask>>a)&1;cb=(mask>>b)&1;cc=(mask>>c)&1
                if ca==cb==cc:j+=1
            local[(p,j)]+=1
        next_table=defaultdict(int)
        for (p,j),v in table.items():
            for (dp,dj),w in local.items():next_table[(p+dp,j+dj)]+=v*w
        table=next_table
    return table,max(map(len,groups),default=0),len(groups)


def recognized_formula(k,missing):
    d=len(missing);m=comb(k,3)-d
    table,kappa,ncomp=hole_dp(k,missing)
    z=5*(1<<m)
    for (p,j),a in table.items():
        if 0<p<k:
            exponent=comb(p,3)+comb(k-p,3)-j
            if exponent<0:raise AssertionError(('negative exponent',p,j))
            z+=5*a*(1<<exponent)
    return z,kappa,ncomp,table


def forest_count(n,arcs):
    es=set(arcs)
    if any(u==v or (v,u) in es for u,v in arcs): return 0
    adj=[[] for _ in range(n)]
    for u,v in arcs:adj[u].append((v,1));adj[v].append((u,-1))
    visited=set();tree=[];components_count=0;colors=[0]*n
    for root in range(n):
        if root in visited:continue
        components_count+=1;visited.add(root);q=[root]
        for u in q:
            for v,s in adj[u]:
                if v not in visited:
                    visited.add(v);q.append(v);tree.append((u,v,s))
    total=0
    def rec(i):
        nonlocal total
        if i==len(tree):
            total+=all((colors[v]-colors[u])%5 in (1,3) for u,v in arcs)
            return
        u,v,sgn=tree[i]
        for d in (1,3):
            colors[v]=(colors[u]+sgn*d)%5
            rec(i+1)
    rec(0)
    return total*5**components_count


def count_source(src):
    n,arcs=decode_graph(src)
    if any(u==v or (v,u) in set(arcs) for u,v in arcs):
        return {'count':0,'method':'unsat'}
    rec=recognize(n,arcs)
    if rec:
        k,missing=rec
        z,kappa,ncomp,_=recognized_formula(k,missing)
        return {'count':z,'method':'hole-components','k':k,'d':len(missing),'kappa':kappa,'components':ncomp}
    return {'count':forest_count(n,arcs),'method':'forest'}


def independent_hub_count(k,missing):
    holes=set(missing)
    present=[t for t in combinations(range(k),3) if t not in holes]
    out=[{(a+1)%5,(a+3)%5} for a in range(5)]
    total=0
    for x in product(range(5),repeat=k):
        prod=1
        for a,b,c in present:
            prod*=len(out[x[a]] & out[x[b]] & out[x[c]])
            if prod==0: break
        total+=prod
    return total


def independent_binary_formula(k,missing):
    d=len(missing);m=comb(k,3)-d
    z=5*(1<<m)
    for mask in range(1, (1<<k)-1):
        p=mask.bit_count()
        j=sum(((mask>>a)&1)==((mask>>b)&1)==((mask>>c)&1) for a,b,c in missing)
        z+=5*(1 << (comb(p,3)+comb(k-p,3)-j))
    return z


def audit():
    rnd=random.Random(SEED);checks=0;cases=[]
    # Exhaust over all sets of missing triples for k=6 with d<=2, includes disjoint covering U=k
    for k in (6,7):
        triples=list(combinations(range(k),3))
        for i in range(30 if k==6 else 12):
            d=rnd.randrange(min(k-3,4)+1)
            holes=sorted(rnd.sample(triples,d))
            n,arcs=incidence_graph(k,holes)
            got=count_source(encode_graph(n,arcs))
            assert got['method']=='hole-components'
            slow=independent_hub_count(k,holes)
            assert got['count']==slow,(k,holes,got['count'],slow)
            assert got['count']==independent_binary_formula(k,holes)
            checks+=3
        cases.append({'k':k,'tested':30 if k==6 else 12})
    # Explicit coverage of ALL hubs; /073 old s<k is unavailable.
    for k in (6,9,12,15,30):
        missing=[tuple(range(i,i+3)) for i in range(0,k,3)]
        assert len(set(v for t in missing for v in t))==k
        assert len(missing)<k-2
        n,arcs=incidence_graph(k,missing)
        got=count_source(encode_graph(n,arcs))
        assert got['method']=='hole-components' and got['kappa']==3
        if k<=15: assert got['count']==independent_binary_formula(k,missing)
        checks+=3
        cases.append({'k':k,'n':n,'m':len(arcs),'d':len(missing),'kappa':3,'count_digits':len(str(got['count'])),'count_sha256':hashlib.sha256(str(got['count']).encode()).hexdigest()})
    # malformed and valid nonfamily fallback
    for bad in ('10101','2','111','01011','1001100'):
        try:count_source(bad)
        except ValueError:checks+=1
        else:raise AssertionError(('did not reject',bad))
    for n,arcs in ((3,[(0,1),(1,2),(2,0)]),(2,[(0,1)]),(2,[]),(2,[(0,1),(1,0)])):
        got=count_source(encode_graph(n,arcs));assert got['count']==sum(all((x[v]-x[u])%5 in (1,3) for u,v in arcs) for x in product(range(5),repeat=n));checks+=1
    # Falsifier boundary: k=4, d=2 can permit rainbow colors, exactly k-2 missing
    k=4
    F=[(0,1,2),(0,1,3)]
    present=[t for t in combinations(range(k),3) if t not in F]
    has_three=any(len(set(x))>=3 and all(set.intersection(*[{(x[v]+1)%5,(x[v]+3)%5} for v in t]) for t in present) for x in product(range(5),repeat=k))
    # do not require it to occur; threshold is sufficient not necessary for all F
    cases.append({'boundary_k':4,'d':2,'rainbow_witness':has_three})
    output={'revision':REV,'seed':SEED,'checks':checks,'failures':0,'cases':cases}
    print(json.dumps(output,sort_keys=True,separators=(',',':')))


if __name__=='__main__':audit()
