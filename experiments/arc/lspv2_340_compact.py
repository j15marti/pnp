#!/usr/bin/env python3
"""Minimal reproducible source-labelled odd-XOR cycle R2 DAG construction."""
import json, itertools, sys

def norm(c): return tuple(sorted(c,key=lambda z:(abs(z),z)))
def pair(i,j,b):
    return [norm((i,j)),norm((-i,-j))] if b else [norm((i,-j)),norm((-i,j))]
def source(h,odd):
    return [c for i in range(1,h+1) for c in pair(i,1 if i==h else i+1,int(odd and i==h))]
def resolve(a,b,p):
    A,B=set(a),set(b)
    if p in A and -p in B:r=(A-{p})|(B-{-p})
    elif -p in A and p in B:r=(A-{-p})|(B-{p})
    else:return None
    return None if any(-x in r for x in r) else norm(r)
def proof(h):
    initial=source(h,True);seen=list(initial);nodes=[]
    def derive(a,b,p,expect):
        got=resolve(seen[a],seen[b],p)
        assert got==expect and got not in seen
        seen.append(got);nodes.append({'a':a,'b':b,'pivot':p,'out':list(got)})
        return len(seen)-1
    left=(0,1)
    for i in range(2,h):
        right=(2*(i-1),2*(i-1)+1);target=pair(1,i+1,0);fresh=[]
        for c in target:
            a,b=next((a,b) for a in left for b in right if resolve(seen[a],seen[b],i)==c)
            fresh.append(derive(a,b,i,c))
        left=tuple(fresh)
    right=(2*h-2,2*h-1);units=[]
    for c in ((h,),(-h,)):
        a,b=next((a,b) for a in left for b in right if resolve(seen[a],seen[b],1)==c)
        units.append(derive(a,b,1,c))
    derive(units[0],units[1],h,())
    assert len(nodes)==2*h-1
    return nodes

def check(h,nodes):
    seen=source(h,True)
    for d in nodes:
        assert d['a']<len(seen) and d['b']<len(seen)
        c=resolve(seen[d['a']],seen[d['b']],d['pivot'])
        assert c==tuple(d['out']);seen.append(c)
    assert seen[-1]==()
    return True

def sat_count(F,h):
    return sum(all(any(((a>>(abs(l)-1))&1)==(l>0) for l in c) for c in F) for a in range(1<<h))

def main():
    out={}
    for h in (3,4,5,6,8,10,16,32):
        p=proof(h);check(h,p)
        rec={'source_clauses':2*h,'proven_lower_bound':2*h-1,'achieved_nodes':len(p)}
        if h<=10:rec.update({'odd_models':sat_count(source(h,True),h),'even_models':sat_count(source(h,False),h)})
        if h<=6:rec['proof']=p
        out[str(h)]=rec
    print(json.dumps(out,sort_keys=True,indent=2))
if __name__=='__main__':main()
