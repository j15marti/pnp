#!/usr/bin/env python3
"""Independent T5 row-cover verifier; no external packages.
Run from repository root: python experiments/t5/lspv3_reusable_cover_20261118.py
"""
from itertools import product
from pathlib import Path
import hashlib, json

SRC=Path('research/agents/lspv-3/certificates/2026-11-18_LSPV3_H9_BLOCK_COVER.t5')
SHA='15625c3bec0f5281a6a943f42b611995d9607cceec71c52e544bcd48f099d1d2'
OK=lambda u,v:(v-u)%5 in (1,3)
PATHS=((0,2,3,1),(0,4,5,1),(0,6,7,1),(0,8,1))
WORDS=('BBB','FBB','FFF','BB')

def support(word):
    a=len(word)+word.count('B')
    return frozenset((a+2*j)%5 for j in range(len(word)+1)) if len(word)<4 else frozenset(range(5))

def cap(xs):
    v=set(range(5))
    for x in xs:v.intersection_update(x)
    return v

def basis(xs):
    out=[]
    for x in xs:
        out.append(x)
        while True:
            j=next((j for j in range(len(out)) if cap(out[:j]+out[j+1:])==cap(out)),None)
            if j is None:break
            out.pop(j)
        assert len(out)<=4
    return out

def extensions(path,edges,deleted,u,v):
    for interior in product(range(5),repeat=len(path)-2):
        colors=dict(zip(path,(u,)+interior+(v,)))
        if all((a,b)==deleted or OK(colors[a],colors[b]) for a,b in edges if a in colors and b in colors):
            return colors
    return None

def main():
    raw=SRC.read_bytes(); assert hashlib.sha256(raw).hexdigest()==SHA
    lines=raw.decode().splitlines(); assert lines[0]=='p t5 9 11'
    arcs=[tuple(map(int,line.split()[1:])) for line in lines if line.startswith('a ')]
    assert len(arcs)==11 and len({frozenset(a) for a in arcs})==11
    pe=[]
    for path,word in zip(PATHS,WORDS):
        es=[e for x,y in zip(path,path[1:]) for e in arcs if set(e)=={x,y}]
        assert len(es)==len(path)-1
        assert ''.join('F' if e==(x,y) else 'B' for e,(x,y) in zip(es,zip(path,path[1:])))==word
        pe.append(es)
    count=0;cov=[0]*4
    for u,v in product(range(5),repeat=2):
        bad=[]
        for i,(word,path,edges) in enumerate(zip(WORDS,PATHS,pe)):
            found=extensions(path,edges,None,u,v)
            assert bool(found)==((v-u)%5 in support(word))
            if found is None:bad.append(i);cov[i]+=1
            count+=1
        assert len(bad)==1
    assert cov==[5,5,5,10] and not cap([support(w) for w in WORDS])
    for removed in arcs:
        found=None
        for u,v in product(range(5),repeat=2):
            pieces=[extensions(p,es,removed,u,v) for p,es in zip(PATHS,pe)]
            if any(p is None for p in pieces):continue
            labels={x:c for part in pieces for x,c in part.items()}
            if len(labels)==9 and all((a,b)==removed or OK(labels[a],labels[b]) for a,b in arcs):
                found=labels;break
        assert found and not OK(found[removed[0]],found[removed[1]])
    rels=list({support(''.join(w)) for length in (1,2,3) for w in product('FB',repeat=length)})
    assert len(rels)==9
    for code in range(1<<len(rels)):
        xs=[rels[j] for j in range(9) if code>>j&1]
        assert cap(basis(xs))==cap(xs)
    ordered=0
    for length in range(1,6):
        for word in product(range(9),repeat=length):
            xs=[rels[j] for j in word]
            assert cap(basis(xs))==cap(xs)
            ordered+=1
    assert ordered==66429
    print(json.dumps({'source_sha256':SHA,'rows':25,'row_block_checks':count,'cover_sizes':cov,'deletions_sat':11,
                      'distinct_types':9,'subsets':512,'ordered_sequences':ordered,'result':'PASS'},sort_keys=True))

if __name__=='__main__':main()
