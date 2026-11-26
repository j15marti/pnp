import itertools as I, random, collections as C, json
from fg19 import T0,PORT,region,rows,enumerate_words,sat2
import audit as old

def project(f,k):
    # Exact local bijunctive test: conjunction of all unary/binary projections.
    if not f:return None
    P=[]
    for J in [(i,) for i in range(k)]+list(I.combinations(range(k),2)):
        D={tuple(w>>i&1 for i in J):0 for w in f};P.append((J,D))
    if any(w not in f and all(tuple(w>>i&1 for i in J) in D for J,D in P) for w in range(1<<k)):return None
    return P

def choices(L,f,B):
    k=len(L);D={}
    for J in [(i,) for i in range(k)]+list(I.combinations(range(k),2)):
        a=sum(1<<i for i in J)
        if any(g and project(g,k) is None for b in (0,1) for g in [{w:0 for w in f if (w&a).bit_count()%2==b}]):continue
        raw=sum(1<<L[i] for i in J);v,_=old.norm(B,raw)
        D[v]=(raw,a)
    return D

def acquire(C0,cap):
    scans=0
    def rec(U,L,d):
        nonlocal scans
        scans+=1;D=next((D for D in C0 if all(old.norm(U,v)[0] for v in D)),None)
        if D is None:return L
        if not d:return None
        for v,(raw,a) in sorted(D.items()):
            V=U.copy();assert old.add(V,v,0);s=rec(V,L+[raw],d-1)
            if s is not None:return s
        return None
    for d in range(cap+1):
        z=rec({},[],d)
        if z is not None:return z,scans
    return None,scans

def solve(F,cap=5,B0=None):
    if any(not f for _,f in F):return False,None,0,0
    B=old.affine(F) if B0 is None else B0
    if B is None:return False,None,0,0
    D=[choices(L,f,B) if project(f,len(L)) is None else None for L,f in F];C0=[d for d in D if d is not None];assert all(C0)
    G,scans=acquire(C0,cap)
    if G is None:return None,None,None,scans
    for b in I.product((0,1),repeat=len(G)):
        A=B.copy();assert all(old.add(A,g,x) for g,x in zip(G,b));terms=[];bad=False
        for raw,x in zip(G,b):
            L=[i for i in range(raw.bit_length()) if raw>>i&1];terms.append((L,{z:0 for z in I.product((0,1),repeat=len(L)) if sum(z)%2==x}))
        for (L,f),d in zip(F,D):
            if d is not None:
                raw,m=next((raw,m) for raw,m in d.values() if old.norm(A,raw)[0]==0);x=old.norm(A,raw)[1];f={w:0 for w in f if (w&m).bit_count()%2==x}
            if not f:bad=True;break
            P=project(f,len(L));assert P is not None
            terms.extend(([L[i] for i in J],g) for J,g in P)
        if bad:continue
        z=sat2(terms)
        if z is not None:
            assert all(sum(z[e]<<i for i,e in enumerate(L)) in f for L,f in F);return True,z,len(G),scans
    return False,None,len(G),scans

def run():
    rng=random.Random(2611261902);cnt=C.Counter();ex=0;maxrank=0
    for k in range(500):
        n=5+k%5;F=[]
        for j in range(3+k%7):
            ar=3+(j+k)%2;L=rng.sample(range(n),ar);p=rng.randrange(2);S=[x for x in range(1<<ar) if x.bit_count()%2==p and rng.random()<.6];S=S or [p];F.append((L,dict.fromkeys(S,0)))
        ref=any(all(sum(z[e]<<i for i,e in enumerate(L)) in f for L,f in F) for z in I.product((0,1),repeat=n));v,z,r,s=solve(F)
        if v is not None:assert v==ref;maxrank=max(maxrank,r or 0)
        cnt[str(v)]+=1
    # Native two-shore weighted tables, local support only, acquired rank, both source labels.
    native=[]
    for k in range(30):
        P={} if k==0 else ({28:1,8:k%2} if k<5 else {rng.randrange(30):rng.randrange(2) for _ in range(k%5)})
        f,_=region(True,P,[0]*30);g,_=region(False,P,[0]*30)
        v,z,r,s=solve([(PORT,f),(PORT,g)]);ref=next(enumerate_words(rows(T0),range(30),P),None) is not None;assert v==ref;native.append((v,r,s))
    # Actual source chain, affine necessary raw chart, candidate cap directions from local attained support.
    ladder=[];f,_=region(True,{},[0]*30)
    for k in (1,2,4,8,16,32):
        T=[list(v+10*i for v in t) for i in range(k) for t in T0]
        for i in range(k-1):
            c=1+i%2;a=30*i+29;b=a+30;T[a][c],T[b][c]=T[b][c],T[a][c]
        A={};assert all(old.add(A,sum(1<<j for j in r),1) for r in rows(T));D=[choices([30*i+j for j in PORT],f,A) for i in range(k)];G,s=acquire(D,1);assert G is not None and len(G)==1;ladder.append({'tuples':30*k,'rank':len(G),'scans':s,'selected_mask':hex(G[0])})
    out={'seed':2611261902,'abstract':dict(cnt),'max_rank':maxrank,'native':native,'ladder':ladder};print(json.dumps(out,indent=2));return out
if __name__=='__main__':open('guard19_results.json','w').write(json.dumps(run(),indent=2)+'\n')
