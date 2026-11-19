#!/usr/bin/env python3
"""Independent finite audit of two-path rigid-triad T5 DAGs. Standard library only."""
import json, itertools, hashlib, random
R = lambda a,b: (b-a)%5 in (1,3)

def graph(p,q):
    assert p>=2 and q>=2
    es=[]; verts=[]; path_nodes=[]; ws=[]
    s=0;t=1; next_id=2
    for l in (p,q):
        inside=list(range(next_id,next_id+l-1));next_id+=l-1
        seq=[s]+inside+[t];path_nodes.append(seq)
        for a,b in zip(seq,seq[1:]):
            w=next_id;next_id+=1;ws.append((a,w,b));es.extend([(a,b),(a,w),(w,b)])
    assert len(es)==3*(p+q) and next_id==2*(p+q)
    assert len(set(es))==len(es)
    assert not any((b,a) in es for a,b in es)
    return next_id,sorted(es),path_nodes,ws

def count(n,edges,allowed=None,limit=None):
    if allowed is None:allowed=tuple(range(n))
    vs=set(allowed)
    es=[e for e in edges if e[0] in vs and e[1] in vs]
    ns={v:[] for v in vs}
    for a,b in es:ns[a].append((b,1));ns[b].append((a,-1))
    order=sorted(vs,key=lambda v:(-len(ns[v]),v))
    picked={}; total=0
    def rec(k):
        nonlocal total
        if k==len(order):total+=1;return
        v=order[k]
        for c in range(5):
            if all((R(c,picked[w]) if d==1 else R(picked[w],c)) for w,d in ns[v] if w in picked):
                picked[v]=c;rec(k+1);del picked[v]
                if limit is not None and total>=limit:return
    rec(0)
    return total

def certified_count(p,q):return 5 if (p-q)%5==0 else 0

checks=0; examples=[]
# Full graph brute-force with opportunistic arc-pruning, independent of arithmetic formula.
for p in range(2,9):
    for q in range(2,9):
        n,es,paths,ws=graph(p,q)
        actual=count(n,es)
        expected=certified_count(p,q)
        assert actual==expected,(p,q,actual,expected)
        checks+=1
        assert all(R(a,(a+3)%5) and R((a+3)%5,(a+1)%5) and R(a,(a+1)%5) for a in range(5))
        checks+=1
        # DAG by topological heights: all arcs move toward t
        heights={0:0,1:max(p,q)+1}
        for path in paths:
            for j,v in enumerate(path[1:-1],1): heights[v]=j
        for a,w,b in ws: heights[w]=heights[a]+0.25
        assert all(heights[a]<heights[b] for a,b in es)
        checks+=1
        assert len(ws)==p+q and n==2*(p+q) and len(es)==3*(p+q)
        checks+=1
        # no 4-vertex 5-arc forced local NO pattern can fit when t>4
        if p+q>=6:
            for path in paths:
                for v in path[1:-1]:
                    assert count(n,es,[x for x in range(n) if x!=v],limit=1)>0
                    checks+=1
        examples.append(dict(p=p,q=q,n=n,m=len(es),models=actual,expected=expected))

# Small NO graph: exhaustive all proper vertex subsets, confirming local support condition.
full_subset_checks=0
for p,q in ((2,3),(3,4)):
    n,es,paths,ws=graph(p,q)
    tset=set(paths[0]+paths[1]);assert len(tset)==p+q
    for mask in range(1<<n):
        kept=[v for v in range(n) if (mask>>v)&1]
        if not tset.issubset(kept):
            assert count(n,es,kept,limit=1)>0,(p,q,mask)
            full_subset_checks+=1

def canonical_source(n,edges):
    return ('p t5 %d %d\n' % (n,len(edges))) + ''.join('v %d\n'%i for i in range(n)) + ''.join('a %d %d\n'%e for e in sorted(edges))

def strict_parse(src):
    lines=src.splitlines(keepends=True)
    assert lines and all(line.endswith('\n') for line in lines)
    h=lines[0].strip().split(' ')
    assert len(h)==4 and h[:2]==['p','t5']
    def dec(s):
        assert s and s.isascii() and s.isdecimal() and (s=='0' or s[0]!='0')
        return int(s)
    n,m=dec(h[2]),dec(h[3]);assert len(lines)==1+n+m and n>=1
    for i in range(n):assert lines[i+1]==('v %d\n'%i)
    arcs=[]
    for j in range(m):
        parts=lines[1+n+j].strip().split(' ')
        assert len(parts)==3 and parts[0]=='a'
        a,b=dec(parts[1]),dec(parts[2]);assert 0<=a<n and 0<=b<n and a!=b
        arcs.append((a,b))
    assert arcs==sorted(set(arcs))
    assert src==canonical_source(n,arcs)
    return n,arcs

def recognize(n,arcs):
    inc=[[] for _ in range(n)];out=[[] for _ in range(n)]
    for a,b in arcs:out[a].append(b);inc[b].append(a)
    sources=[i for i in range(n) if len(inc[i])==0 and len(out[i])==4]
    sinks=[i for i in range(n) if len(inc[i])==4 and len(out[i])==0]
    if len(sources)!=1 or len(sinks)!=1:return None
    s,t=sources[0],sinks[0]
    ws=[i for i in range(n) if len(inc[i])==len(out[i])==1]
    cores=[i for i in range(n) if i not in ws]
    if len(ws)*2!=n or len(cores)!=len(ws):return None
    if any((len(inc[i]),len(out[i]))!=(2,2) for i in cores if i not in (s,t)):return None
    direct=[];recon=[]
    arcset=set(arcs)
    for w in ws:
        a=inc[w][0];b=out[w][0]
        if a not in cores or b not in cores or (a,b) not in arcset:return None
        direct.append((a,b));recon.extend(((a,b),(a,w),(w,b)))
    if len(set(direct))!=len(direct) or sorted(recon)!=sorted(arcs):return None
    outcore={i:[] for i in cores};incore={i:[] for i in cores}
    for a,b in direct:outcore[a].append(b);incore[b].append(a)
    if len(outcore[s])!=2 or len(incore[s])!=0 or len(outcore[t])!=0 or len(incore[t])!=2:return None
    if any(len(outcore[v])!=1 or len(incore[v])!=1 for v in cores if v not in (s,t)):return None
    paths=[];visited={s,t}
    for first in outcore[s]:
        cur=first;length=1
        while cur!=t:
            if cur in visited or cur not in outcore:return None
            visited.add(cur);length+=1
            if length>n:return None
            cur=outcore[cur][0]
        if length<2:return None
        paths.append(length)
    if visited!=set(cores):return None
    return tuple(sorted(paths))

# Independent source parser, unlabeled recognizer, deliberate corruptions.
rr=random.Random(202611172042)
parser_checks=0
for p,q in ((2,2),(2,3),(3,4),(5,10),(11,15),(10,14),(99,104)):
    n,es,_,_=graph(p,q)
    for _ in range(12):
        perm=list(range(n));rr.shuffle(perm)
        transformed=sorted((perm[a],perm[b]) for a,b in es)
        src=canonical_source(n,transformed)
        n2,e2=strict_parse(src)
        assert recognize(n2,e2)==tuple(sorted((p,q)))
        parser_checks+=1
        # Alter a real original arc; valid but no longer recognized as promised family.
        e3=e2[1:]
        assert recognize(n2,e3) is None
        parser_checks+=1
        # Malformed byte sequence: duplicate arc, wrong declared arc count, bad vertex row.
        for bad in (src+'a 0 1\n',src.replace('v 0\n','v 00\n'),src[:-1]):
            try:strict_parse(bad)
            except AssertionError: pass
            else:raise AssertionError('malformed accepted')
            parser_checks+=1

raw=dict(revision='tmr5-t5-two-path-dag079.py.v1',symbol_set='Z5 R(a,b) iff (b-a)%5 in {1,3}',pairs=len(examples),checks=checks,full_subset_checks=full_subset_checks,parser_checks=parser_checks,failures=0,examples=examples)
p='/mnt/data/TMR5_079_T5_PARALLEL_DAG_RAW.json'
with open(p,'w') as f:json.dump(raw,f,sort_keys=True,indent=2)
print(json.dumps({k:v for k,v in raw.items() if k!='examples'},sort_keys=True))
