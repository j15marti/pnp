#!/usr/bin/env python3
"""Sound one-sided source-bound specialist for canonical H_t / H_t-e T5 sources.
This implementation is intentionally O(N) in memory (Python source arrays).
A negative result is returned ONLY after exact syntactic source authentication.
Other/malformed graphs return UNKNOWN.
"""
import json
from lspv3_t5_cycle_chain_essential_cover_20261118 import instance, extension, closure, valid

def encode(n, arcs):
    return f'p t5 {n} {len(arcs)}\n'+''.join(f'v {i}\n' for i in range(n))+''.join(f'a {u} {v}\n' for u,v in arcs)

def specialist(source):
    if not isinstance(source,str) or not source.endswith('\n'):return ('UNKNOWN',None)
    lines=source.splitlines()
    if not lines:return ('UNKNOWN',None)
    parts=lines[0].split()
    if len(parts)!=4 or parts[:2]!=['p','t5']:return ('UNKNOWN',None)
    try:n=int(parts[2]);m=int(parts[3])
    except ValueError:return ('UNKNOWN',None)
    if n<2 or m<0 or lines[0]!=f'p t5 {n} {m}':return ('UNKNOWN',None)
    if len(lines)!=1+n+m:return ('UNKNOWN',None)
    if any(lines[1+i]!=f'v {i}' for i in range(n)):return ('UNKNOWN',None)
    arcs=[]
    for line in lines[1+n:]:
        p=line.split()
        if len(p)!=3 or p[0]!='a':return ('UNKNOWN',None)
        try:u=int(p[1]);v=int(p[2])
        except ValueError:return ('UNKNOWN',None)
        if not (0<=u<n and 0<=v<n) or line!=f'a {u} {v}':return ('UNKNOWN',None)
        arcs.append((u,v))
    for t in range(max(2,(n-4)//3),max(2,n//3)+2):
        N,full,paths=instance(t)
        if N!=n:continue
        missing=None
        if arcs==full:
            return ('UNSAT',{'t':t,'closure':closure(t),'proof':'each link difference=1; excluded closure difference=(-t)%5','source_checked':True})
        if len(arcs)!=len(full)-1:continue
        a=b=0
        while a<len(full) and b<len(arcs):
            if full[a]==arcs[b]:a+=1;b+=1
            elif missing is None:missing=a;a+=1
            else:break
        if b!=len(arcs):continue
        if missing is None:missing=len(full)-1
        if full[:missing]+full[missing+1:]!=arcs:continue
        selected=next(j for j,p in enumerate(paths) if missing in p[1])
        increments=[1]*t
        if selected<2*t:increments[selected//2]=0 if selected%2==0 else 3
        terminal=[0]
        for d in increments:terminal.append((terminal[-1]+d)%5)
        witness={}
        for p in paths:
            assign=extension(p,full,terminal[p[0][0]],terminal[p[0][-1]],missing)
            if assign is None:return ('UNKNOWN',None)
            if any(x in witness and witness[x]!=c for x,c in assign.items()):return ('UNKNOWN',None)
            witness.update(assign)
        colors=[witness[i] for i in range(n)]
        if len(witness)!=n or not all(valid(colors[u],colors[v]) for u,v in arcs):return ('UNKNOWN',None)
        return ('SAT',{'t':t,'missing_arc_index':missing,'colors':colors,'source_checked':True})
    return ('UNKNOWN',None)

def main():
    totals={'full_unsat':0,'deletion_sat':0,'malformed_unknown':0}
    for t in (2,3,4,5,6,7,10,12,20):
        n,arcs,_=instance(t);full=encode(n,arcs)
        assert specialist(full)[0]=='UNSAT';totals['full_unsat']+=1
        for i in range(len(arcs)):
            s,cert=specialist(encode(n,arcs[:i]+arcs[i+1:]))
            assert s=='SAT' and cert['missing_arc_index']==i
            assert len(cert['colors'])==n
            assert all(valid(cert['colors'][u],cert['colors'][v]) for j,(u,v) in enumerate(arcs) if j!=i)
            totals['deletion_sat']+=1
        malformed=[full.replace('p t5','p t4',1),full.replace('v 0','v 999',1),
                   encode(n,arcs[:-2]),encode(n,arcs+[arcs[-1]]),
                   encode(n,[(b,a) if j==0 else (a,b) for j,(a,b) in enumerate(arcs)])]
        for bad in malformed:
            assert specialist(bad)[0]=='UNKNOWN'
            totals['malformed_unknown']+=1
    print(json.dumps(totals,sort_keys=True))

if __name__=='__main__':main()
