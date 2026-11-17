#!/usr/bin/env python3
"""Independent finite audit of KGRAM-EULER-SECTION19.
Pure Python, deterministic. Proof is symbolic; finite checks are not an asymptotic proof.
"""
from collections import Counter, deque
from itertools import product
from random import Random
import json, hashlib, datetime

SEED = 202611180511
rng = Random(SEED)


def binary_bigram_canonical(w):
    """Closed-form two-run-plus-alternating-tail normal form for k=2."""
    assert len(w)>=2
    z=Counter(tuple(w[i:i+2]) for i in range(len(w)-1))
    flips=z[(0,1)]+z[(1,0)]
    if flips==0: return tuple(w[0] for _ in w)
    first=w[0]
    same=z[(first,first)]
    opposite=z[(1-first,1-first)]
    g=[first]*(same+1)+[1-first]*(opposite+1)
    g.extend(first ^ (j&1) for j in range(flips-1))
    assert len(g)==len(w)
    return tuple(g)

def vout(t, k):
    return t[:k-1],t[1:]


def edge_counts(w, k):
    return Counter(tuple(w[i:i+k]) for i in range(len(w)-k+1))


def bfs_path(counts, start, target, k):
    if start == target:
        return []
    par = {start: None}
    queue=deque([start])
    while queue:
        v=queue.popleft()
        for b in (0, 1):
            e=tuple(v)+(b,)
            if counts[e] <= 0: continue
            nxt=e[1:]
            if nxt not in par:
                par[nxt]=(v,e)
                if nxt == target:
                    path=[]
                    cur=nxt
                    while cur!=start:
                        prev,edge=par[cur]
                        path.append(edge)
                        cur=prev
                    return path[::-1]
                queue.append(nxt)
    raise AssertionError('No source-to-target directed support path')


def simple_cycle(counts, k):
    usable=[e for e,c in counts.items() if c>0]
    if not usable: return None
    v=min(e[:k-1] for e in usable)
    visited={}
    edges=[]
    while v not in visited:
        visited[v]=len(edges)
        for b in (0,1):
            e=tuple(v)+(b,)
            if counts[e]>0:
                edges.append(e)
                v=e[1:]
                break
        else:
            raise AssertionError('Residual circulation lost balance')
    return edges[visited[v]:]


def section_blocks_from_counts(counts, start, end, k):
    """Construct a polynomially short periodic-block section, no length-N expansion."""
    cnt=Counter(counts)
    path=bfs_path(cnt,start,end,k)
    rem=cnt.copy()
    for e in path:
        assert rem[e]>0
        rem[e]-=1
    cycles=[]
    while any(rem.values()):
        cyc=simple_cycle(rem,k)
        weight=min(rem[e] for e in cyc)
        for e in cyc:rem[e]-=weight
        cycles.append((cyc,weight))
    assert not any(rem.values())
    blocks=[((e,),1) for e in path]
    pending=list(cycles)
    while pending:
        success=False
        # Source-length-independent search of O(2^k) periodic blocks,
        # each of period <=2^(k-1), for a shared vertex.
        for j,(cyc,weight) in enumerate(pending):
            src=cyc[0][:k-1]
            cyc_vertices=[src]
            for e in cyc:cyc_vertices.append(e[1:])
            index={v:i for i,v in enumerate(cyc_vertices[:-1])}
            cur=start; total_off=0
            for pat,m in blocks:
                v=cur
                for off,e in enumerate(pat):
                    assert e[:k-1]==v
                    if v in index:
                        r=index[v]
                        rotated=cyc[r:]+cyc[:r]
                        blocks=insert_at(blocks,total_off+off,rotated,weight)
                        pending.pop(j); success=True; break
                    v=e[1:]
                if success:break
                if v in index:
                    r=index[v]
                    rotated=cyc[r:]+cyc[:r]
                    blocks=insert_at(blocks,total_off+len(pat),rotated,weight)
                    pending.pop(j);success=True;break
                if m>1: assert v==cur, 'Repeated block must be a closed walk'
                cur=v
                total_off+=len(pat)*m
            if success:break
            # Empty initial walk: it contains just the start vertex.
            if not blocks and start in index:
                r=index[start]
                blocks=[(tuple(cyc[r:]+cyc[:r]),weight)]
                pending.pop(j);success=True;break
        if not success: raise AssertionError('Cycle intersection scheduling failed')
    assert len(blocks)<=len(path)+5*len(cycles)
    assert len(cycles)<=len(cnt)
    assert all(len(pat)<= (1<<(k-1)) for pat,m in blocks)
    # Verify weighted edges by blocks, not source expansion.
    got=Counter()
    cur=start
    for pat,m in blocks:
        for e in pat:
            assert e[:k-1]==cur
            cur=e[1:]
        if m>1: assert cur==pat[0][:k-1]
        for e in pat: got[e]+=m
    assert cur==end
    assert got==+cnt
    return blocks,len(path),len(cycles)

def realize_blocks(blocks, start):
    edges=[]
    for pat,num in blocks:
        edges.extend(pat*num)
    cur=start
    visits=[cur]
    for e in edges:
        assert e[:len(start)] == cur
        cur=e[1:]
        visits.append(cur)
    return edges, visits


def normalize_blocks(blocks):
    return [(tuple(p),m) for p,m in blocks if p and m>0]


def split_block(block, j):
    pat,m=block
    d=len(pat)
    assert 0<=j<=m*d
    q,r=divmod(j,d)
    pre=[];post=[]
    if q:pre.append((pat,q))
    if r:
        pre.append((pat[:r],1))
        post.append((pat[r:],1))
        if m-q-1: post.append((pat,m-q-1))
    else:
        if m-q:post.append((pat,m-q))
    return pre,post


def insert_at(blocks, offset, pat, multiplicity):
    assert multiplicity>0
    acc=0
    for j, (pattern,m) in enumerate(blocks):
        length=len(pattern)*m
        if offset<=acc+length:
            pre,post=split_block(blocks[j], offset-acc)
            return normalize_blocks(blocks[:j]+pre+[(tuple(pat),multiplicity)]+post+blocks[j+1:])
        acc+=length
    assert offset==acc
    return normalize_blocks(blocks+[(tuple(pat),multiplicity)])


def witness(w, k):
    assert 2<=k<=len(w)
    N=len(w)
    cnt=edge_counts(w,k)
    start=tuple(w[:k-1]); end=tuple(w[-k+1:])
    blocks,path,cyc=section_blocks_from_counts(cnt,start,end,k)
    actual=tuple(random_access(blocks,start,i) for i in range(N))
    assert edge_counts(actual,k)==cnt
    assert tuple(actual[:k-1])==start
    return actual,blocks,path,cyc


def random_access(blocks, prefix, i):
    # Simulates a circuit of O(number of blocks * poly(n, 2^k)) for each output address.
    if i<len(prefix):return prefix[i]
    j=i-len(prefix)
    for pat,m in blocks:
        length=len(pat)*m
        if j<length:
            return pat[j%len(pat)][-1]
        j-=length
    raise IndexError(i)


def run():
    checks=0; words=0;cases=[];max_blocks=0;strict=0
    for n, ks, samples in [(2,range(2,5),None),(3,range(2,7),None),(4,range(2,7),750)]:
        N=1<<n
        ws=product((0,1),repeat=N) if samples is None else (tuple(rng.randrange(2) for _ in range(N)) for _ in range(samples))
        for w in ws:
            for k in ks:
                g,blocks,path,cyc=witness(w,k)
                assert len(g)==N
                assert edge_counts(w,k)==edge_counts(g,k)
                assert g[:k-1]==w[:k-1]
                assert g[-k+1:]==w[-k+1:]
                checks+=4
                if k==2:
                    h=binary_bigram_canonical(w)
                    assert edge_counts(h,2)==edge_counts(w,2)
                    assert h[0]==w[0] and h[-1]==w[-1]
                    checks+=3
                for i in range(N):
                    assert random_access(blocks,g[:k-1],i)==g[i]
                    checks+=1
                words+=1
                strict+=int(g!=w)
                max_blocks=max(max_blocks,len(blocks))
                if words<=8:cases.append({'n':n,'k':k,'original':''.join(map(str,w)),'representative':''.join(map(str,g)),'blocks':[(len(pat),num) for pat,num in blocks]})
    large=[]
    for n,k in [(17,3),(18,5),(19,7)]:
        N=1<<n
        # Fixed low-complexity source, scanned once; no length-N witness expansion.
        bits=tuple(int(((i//13)%3==0) or ((i%97) in (5,6,7))) for i in range(N))
        cnt=edge_counts(bits,k)
        blocks,path,cyc=section_blocks_from_counts(cnt, tuple(bits[:k-1]),tuple(bits[-k+1:]),k)
        for i in [0,1,N//4,N//2,3*N//4,N-1]+[rng.randrange(N) for _ in range(80)]:
            v=random_access(blocks, bits[:k-1],i)
            assert v in (0,1)
            checks+=1
        assert sum(len(pat)*m for pat,m in blocks)==N-k+1
        checks+=1
        large.append({'n':n,'N':N,'k':k,'block_count':len(blocks),'path_edges':path,'cycle_kinds':cyc,'source_scan_bits':N,'max_period':max(map(lambda b:len(b[0]),blocks))})
    result={'artifact':'KGRAM-EULER-SECTION19','date_utc':'2026-11-17','seed':SEED,'input_cases':words,'assertions':checks,'failures':0,'nonidentical_representatives':strict,'max_periodic_blocks':max_blocks,'large_compressed_tests':large,'sample_cases':cases,'scope':'exact k-gram counts + source prefix and suffix, nonuniform circuit witness, one-tape quotient scan is possible but fails promise purity, NOT P!=NP'}
    return result

if __name__=='__main__':
    result=run()
    print(json.dumps(result,indent=2))
