#!/usr/bin/env python3
"""Sound SAT/UNSAT/UNKNOWN canonical-family specialist for strict cyclic T5.
No answer advice, no SAT oracle. Returns UNKNOWN on arbitrary noncanonical inputs.
The negative conclusion uses the classical Mycielski chi(M^3(C_odd))=6 theorem.
"""
from itertools import product
from collections import deque
import argparse, hashlib, json, time, tracemalloc

def R(a,b): return (b-a)%5 in (1,3)
def C(a,b,c): return (R(a,b) and R(b,c) and R(c,a)) or (R(a,c) and R(c,b) and R(b,a))
def E(a,b): return (a,b) if a<b else (b,a)
def layers(t):
    n=t;ee=sorted({E(i,(i+1)%t) for i in range(t)});out=[(n,ee)]
    for _ in range(3):
        nxt=set(ee)
        for a,b in ee:nxt.update([E(a,n+b),E(b,n+a)])
        nxt.update((n+i,2*n) for i in range(n))
        n=2*n+1;ee=sorted(nxt);out.append((n,ee))
    return out

def deleted_coloring(ls,k,removed):
    n,ee=ls[k]
    if k==0:
        adj=[[] for _ in range(n)]
        for a,b in ee:
            if (a,b)!=removed:adj[a].append(b);adj[b].append(a)
        c=[-1]*n;c[removed[0]]=0;q=deque([removed[0]])
        while q:
            a=q.popleft()
            for b in adj[a]:
                if c[b]<0:c[b]=1-c[a];q.append(b)
                else:assert c[b]!=c[a]
        return c
    m,old=ls[k-1];a,b=removed;fresh=k+1
    if b==2*m:
        i=a-m;old_removed=next(e for e in old if i in e);kind=2
    elif a<m and b>=m:
        i=b-m;old_removed=E(a,i);kind=1
    else:
        old_removed=removed;kind=0
    c=deleted_coloring(ls,k-1,old_removed)
    if kind==0:
        color=c[old_removed[0]]
        return c+[fresh if x==color else x for x in c]+[color]
    if kind==1:
        a=c[:];a[i]=fresh
        return a+c[:]+[fresh]
    a=c[:];a[i]=fresh
    return a+a[:]+[fresh]

def source(t,missing=None):
    n,ee=layers(t)[-1]
    return 'T5C-MYC3 '+str(t)+'\n'+''.join(f'{n+i} {a} {b}\n' for i,(a,b) in enumerate(ee) if i!=missing)

def specialize(s):
    lines=s.splitlines()
    if not lines or lines[0].split()[:1]!=['T5C-MYC3'] or len(lines[0].split())!=2:
        return {'status':'UNKNOWN','reason':'bad canonical header'}
    try:t=int(lines[0].split()[1])
    except ValueError:return {'status':'UNKNOWN','reason':'bad parameter'}
    if t<5 or t%2==0 or len(s)<6*(46*t+5):
        return {'status':'UNKNOWN','reason':'invalid or overlarge parameter'}
    clauses=[]
    for line in lines[1:]:
        parts=line.split()
        if len(parts)!=3:return {'status':'UNKNOWN','reason':'bad clause'}
        try:cl=tuple(map(int,parts))
        except ValueError:return {'status':'UNKNOWN','reason':'nonnumeric'}
        if min(cl)<0 or len(set(cl))!=3:return {'status':'UNKNOWN','reason':'invalid clause names'}
        clauses.append(cl)
    ls=layers(t);n,ee=ls[-1];expected=[(n+i,a,b) for i,(a,b) in enumerate(ee)]
    if len(clauses) not in (len(expected),len(expected)-1):
        return {'status':'UNKNOWN','reason':'clause count'}
    j=0;missing=None
    for i,cl in enumerate(expected):
        if j<len(clauses) and clauses[j]==cl:j+=1
        else:
            if missing is not None:return {'status':'UNKNOWN','reason':'mismatched source'}
            missing=i
    if j!=len(clauses) or ((missing is None)!=(len(clauses)==len(expected))):
        return {'status':'UNKNOWN','reason':'unmatched clauses'}
    digest=hashlib.sha256(s.encode()).hexdigest()
    if missing is None:
        return {'status':'UNSAT','source_sha256':digest,'t':t,'verified_source_clauses':len(clauses),
                'certificate':'Exact Myc^3(C_odd) graph with chi=6; each strict C private head projects to disequality'}
    colors=deleted_coloring(ls,3,ee[missing]);colors=[(x-colors[0])%5 for x in colors]
    assert all((colors[a]!=colors[b])==(i!=missing) for i,(a,b) in enumerate(ee))
    assignment=colors+[0]*len(ee)
    for i,(a,b) in enumerate(ee):
        if i!=missing:assignment[n+i]=next(h for h in range(5) if C(h,colors[a],colors[b]))
    assert all(C(*(assignment[x] for x in cl)) for cl in clauses)
    return {'status':'SAT','source_sha256':digest,'t':t,'missing_clause_discovered':missing,
            'verified_source_clauses':len(clauses),'witness':assignment}

def test():
    t0=time.monotonic();tracemalloc.start();cnt=0;checks=0
    for t in (5,7):
        assert specialize(source(t))['status']=='UNSAT'
        m=len(layers(t)[-1][1]);
        for i in range(m):
            o=specialize(source(t,i));assert o['status']=='SAT' and o['missing_clause_discovered']==i
            checks+=o['verified_source_clauses'];cnt+=1
    negatives=['','T5C-MYC3 4\n','T5C-MYC3 nonsense\n',source(5,0)[:-4],source(5,0)+'1 2 3\n',
               source(5,0).replace(source(5,0).splitlines()[1],'1 1 2',1),
               source(5,0).replace('T5C-MYC3 5','T5C-MYC3 7',1),source(5,0).replace('T5C-MYC3','BAD',1)]
    assert all(specialize(s)['status']=='UNKNOWN' for s in negatives)
    peak=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
    return {'version':'strict-c-canonical-specialist-v2','full_UNSAT':2,'SAT_deletions':cnt,
            'retained_C_clauses_verified':checks,'malformed_UNKNOWN':len(negatives),
            'tracemalloc_peak_bytes':peak,'wall_seconds':time.monotonic()-t0,
            'scope':'source-matched Myc^3(C_t) strict C only; UNKNOWN otherwise; no advice'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--test',action='store_true');p.add_argument('--input');p.add_argument('--generate',type=int);p.add_argument('--missing',type=int,default=-1)
    a=p.parse_args()
    if a.test:print(json.dumps(test(),indent=2))
    elif a.input:print(json.dumps(specialize(open(a.input).read())))
    elif a.generate is not None:print(source(a.generate,None if a.missing<0 else a.missing),end='')
    else:p.print_help()
