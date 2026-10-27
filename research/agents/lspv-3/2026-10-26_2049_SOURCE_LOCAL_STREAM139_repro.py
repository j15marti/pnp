#!/usr/bin/env python3
"""SOURCE-LOCAL-STREAM139 self-contained stdlib proof audit.
This GitHub runner independently checks the structural, Resolution,
source-identity, separated-equality and two-level claims. The extended
18,354,033-check stress runner is also available as a downloadable
conversation artifact; Python's memory is not a TM-space measurement.
"""
from collections import Counter, defaultdict
import itertools, random, json

W = tuple(tuple(map(int,s.split())) for s in
 "-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14".split(';'))
A=((6,0),(11,0)); B=((9,2),(17,2))
FIX=tuple(i for i in range(20) if i not in (6,11,9,17))
BACKDOOR=(2,4,7,14,15)
TESTS=0
def check(x,msg):
    global TESTS
    TESTS+=1
    if not x:raise AssertionError(msg)
def renamed(rows,off):
    return tuple(tuple((1 if z>0 else -1)*(abs(z)+off) for z in row)
                 for row in rows)
def H(a,b):
    c=[list(z) for z in W]
    if not a:
        for i,j in A:c[i][j]=-c[i][j]
    if not b:
        for i,j in B:c[i][j]=-c[i][j]
    return tuple(map(tuple,c))
def satisfied(rows,n):
    z=0
    for mask in range(1<<n):
        if all(any(((mask>>(abs(v)-1))&1)==(v>0) for v in c) for c in rows):
            z+=1
    return z
def regular(rows,n):
    p=Counter(x for c in rows for x in c if x>0)
    q=Counter(-x for c in rows for x in c if x<0)
    return 3*len(rows)==4*n and all(p[i]==q[i]==2 for i in range(1,n+1)) and all(len(set(map(abs,c)))==3 for c in rows)
def connected(rows,n):
    g={i:set() for i in range(1,n+1)}
    for c in rows:
        for z in c:g[abs(z)].update(map(abs,c))
    seen={1};stack=[1]
    while stack:
        u=stack.pop()
        for v in g[u]:
            if v not in seen:seen.add(v);stack.append(v)
    return len(seen)==n
def ring(k):
    out=[]
    for i in range(k):
        c=[list(x) for x in renamed(W,15*i)]
        c[0][0]=-(15*((i-1)%k)+1)
        out.extend(map(tuple,c))
    return tuple(out)
def core(k,i):
    j=(i+1)%k
    c=list(renamed(W[1:],15*i))+list(renamed(W[1:],15*j))
    bridge=list(renamed((W[0],),15*j)[0])
    bridge[0]=-(15*i+1)
    return tuple(c+[tuple(bridge)])
def resolution(rows):
    p=[(frozenset(c),None,None,None) for c in rows]
    table={c:i for i,(c,_,_,_) in enumerate(p)}
    alive=set(table.values())
    while alive:
        empty=next((i for i in alive if not p[i][0]),None)
        if empty is not None:return p,empty
        vars_={abs(x) for i in alive for x in p[i][0]}
        def score(x):
            plus=sum(x in p[i][0] for i in alive)
            minus=sum(-x in p[i][0] for i in alive)
            return plus*minus,plus+minus,x
        x=min(vars_,key=score)
        pp=[i for i in alive if x in p[i][0]]
        nn=[i for i in alive if -x in p[i][0]]
        alive.difference_update(pp);alive.difference_update(nn)
        for i in pp:
            for j in nn:
                c=(p[i][0]|p[j][0])-{x,-x}
                if any(-z in c for z in c):continue
                if c not in table:
                    table[c]=len(p);p.append((c,i,j,x))
                alive.add(table[c])
    raise AssertionError("fixed core was not refuted")
def verify_resolution(p,end,source,rename=lambda x:x):
    out=[]
    check(not p[end][0],"empty line")
    for i,(c,l,r,pivot) in enumerate(p[:end+1]):
        c=frozenset((1 if x>0 else -1)*rename(abs(x)) for x in c)
        if i<len(source):check(c==frozenset(source[i]),"auth premise")
        else:
            check(l is not None and r is not None and l<i and r<i,"prior lines")
            z=rename(pivot)
            check(z in out[l] and -z in out[r],"pivot")
            check(c==(out[l]|out[r])-{z,-z},"resolvent")
        out.append(c)
def equality(a,b):
    modules=[]
    for i,(aa,bb) in enumerate(zip(a,b)):
        modules += [renamed(H(aa,1-bb),30*i),
                    renamed(H(1-aa,bb),30*i+15)]
    rows=[]
    for block in (tuple(i for i,_ in A),FIX,tuple(i for i,_ in B)):
        for mo in modules:
            rows.extend(mo[ci] for ci in block)
    return tuple(rows)
def source_indices(m,j):
    return tuple([2*j+i for i in range(2)]+
                 [4*m+16*j+i for i in range(16)]+
                 [36*m+2*j+i for i in range(2)])
def authenticated(rows,m,i,orientation):
    if m<1 or not 0<=i<m or orientation not in (0,1) or len(rows)<40*m:return False
    j=2*i+orientation
    # The twenty clause IDs, full signed literals and original aliases agree.
    ids=source_indices(m,j)
    target=renamed(tuple(W[c] for c in (6,11,*FIX,9,17)),15*j)
    return all(rows[x]==want for x,want in zip(ids,target))
def encode(rows,n):
    # Legal ordinary DIMACS with constant physical row length per m.
    d=len(str(n))+2
    return (f"p cnf {n} {len(rows)}\n"+
            "".join("".join(f"{z:>{d}d}" for z in c)+" 0\n" for c in rows)).encode()
def parse(raw):
    lines=raw.decode("ascii").splitlines()
    h=lines[0].split()
    check(len(h)==4 and h[:2]==["p","cnf"],"source header")
    n,m=map(int,h[2:])
    check(len(lines)==m+1,"clause count")
    rows=[]
    for line in lines[1:]:
        t=line.split()
        check(len(t)==4 and t[3]=="0","proper line")
        c=tuple(map(int,t[:3]))
        check(all(0<abs(x)<=n for x in c) and len(set(map(abs,c)))==3,"source literal")
        rows.append(c)
    return n,tuple(rows)
def pin(lit,x,y):
    return tuple((lit,a,b) for a in (x,-x) for b in (y,-y))
def main():
    check(not satisfied(W,15),"W UNSAT")
    check(satisfied(W[1:],15)==140,"punctured W models")
    check(connected(W[1:],15),"punctured W connected")
    check(regular(W,15),"W regular")
    hcounts={(a,b):satisfied(H(a,b),15) for a,b in itertools.product((0,1),repeat=2)}
    check(hcounts=={(0,0):772,(0,1):272,(1,0):272,(1,1):0},"H table")
    proof,end=resolution(core(2,0))
    check(len(proof)==200 and end==199,"resolution length")
    verify_resolution(proof,end,core(2,0))
    rings=[]
    for k in (2,3,4,5,8,16):
        rows=ring(k)
        check(regular(rows,15*k) and connected(rows,15*k),"ring regular and connected")
        back={15*j+z for j in range(k) for z in BACKDOOR}
        check(all(any(abs(z) in back for z in c) for c in rows),"tight 5k hitting")
        for i in range(k):
            src=core(k,i)
            ids=([20*i+u for u in range(1,20)]
                 +[20*((i+1)%k)+u for u in range(1,20)]
                 +[20*((i+1)%k)])
            check(tuple(rows[z] for z in ids)==src,"authenticated core")
            tr=lambda z: (15*i+z) if z<=15 else (15*((i+1)%k)+z-15)
            verify_resolution(proof,end,src,tr)
        rings.append((k,15*k,20*k,5*k,39))
    cases=0;sat=0;unsat=0;level2=0
    for m in (1,2,3,4):
        vecs=list(itertools.product((0,1),repeat=m))
        for a,b in itertools.product(vecs,vecs):
            orig=equality(a,b)
            raw=encode(orig,30*m)
            n,rows=parse(raw)
            check(rows==orig and regular(rows,n),"encoded signed exact22")
            # Every input of the same length has the same physical Alice cut.
            lines=raw.splitlines(keepends=True)
            check(len(set(map(len,lines[1:])))==1,"equal-byte DIMACS rows")
            hits=[(i,t) for i in range(m) for t in (0,1) if authenticated(rows,m,i,t)]
            expected=([(i,0) for i in range(m) if a[i]==1 and b[i]==0]
                      +[(i,1) for i in range(m) if a[i]==0 and b[i]==1])
            check(sorted(hits)==sorted(expected),"both-label exact certificate coverage")
            cases+=1
            if a==b:sat+=1
            else:unsat+=1
            if m==3 and hits and level2<6:
                one=orig+pin(1,n+1,n+2)
                two=one+pin(2,n+3,n+4)
                n1,r1=parse(encode(one,n+2))
                n2,r2=parse(encode(two,n+4))
                check(len(r1)==40*m+4 and len(r2)==40*m+8,"physical levels")
                check(r2[:40*m]==orig and authenticated(r1,m,*hits[0])
                      and authenticated(r2,m,*hits[0]),"hereditary source")
                level2+=1
    random.seed(13920261026)
    large=0
    for m in (8,17,31,64):
        for j in range(18):
            a=[random.randint(0,1) for _ in range(m)]
            b=a[:]
            if j%3:
                for i in random.sample(range(m),random.randint(1,min(m,6))):b[i]^=1
            rows=equality(a,b)
            check(any(authenticated(rows,m,i,t) for i in range(m) for t in (0,1))==(a!=b),
                  "large equality mismatch authentication")
            large+=1
    out={"title":"SOURCE-LOCAL-STREAM139 GitHub standalone proof audit",
         "assertion_calls":TESTS,"W_punctured_models":140,
         "H_model_counts":{str(k):v for k,v in hcounts.items()},
         "ring_sizes_k_n_m_backdoor_core":rings,
         "resolution_lines":len(proof),"resolution_premises":39,
         "exact_equality_sources":cases,"SAT":sat,"UNSAT":unsat,
         "random_large":large,"two_ordinary_levels":level2,
         "mathematical_proof_status":"PROVED restricted, peer review pending",
         "arbitrary_UNSAT_coverage":"OPEN","P_vs_NP":"OPEN"}
    print(json.dumps(out,sort_keys=True,indent=2))
if __name__=="__main__":main()
