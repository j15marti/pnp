import itertools, random, json, math
from collections import Counter

rng=random.Random(20261125)
st=Counter()
def basis(vs):
    b={}
    for v in vs:
        while v:
            p=v.bit_length()-1
            if p not in b: b[p]=v; break
            v^=b[p]; st['rank_xors']+=1
    return list(b.values())

def coordinate(v, rows):
    b={}
    for i,x in enumerate(rows):
        z=1<<i
        while x:
            p=x.bit_length()-1
            if p not in b: b[p]=(x,z);break
            a,c=b[p];x^=a;z^=c
        else: raise AssertionError('dependent basis')
    z=0
    while v:
        a,c=b[v.bit_length()-1];v^=a;z^=c
    return z

def extend(rows, more):
    out=list(rows); b=basis(rows)
    for x in more:
        new=basis(b+[x])
        if len(new)>len(b):out.append(x);b=new
    return out

def intersection(A,C):
    b={}; out=[]
    for i,x in enumerate(A+C):
        z=1<<i
        while x:
            p=x.bit_length()-1
            if p not in b: b[p]=(x,z); break
            y,v=b[p];x^=y;z^=v
        if not x:
            t=0
            for j,a in enumerate(A):
                if z>>j&1:t^=a
            if t:out.append(t)
    return basis(out)

def parity_unique(eqs, mask):
    st['coefficient_queries']+=1; b={}
    for a,v in eqs:
        x=a&mask
        while x:
            p=x.bit_length()-1
            if p not in b:b[p]=(x,v);break
            y,z=b[p];x^=y;v^=z;st['equation_xors']+=1
        if not x and v:return 0
    return int(len(b)==mask.bit_count())

def bands(w,h,d):
    lo=max(0,h-d);hi=min(w,h)
    return [sum(1<<j for j in S) for k in range(lo,hi+1) for S in itertools.combinations(range(w),k)]

def solve_equs(eqs,r):
    b={}
    for a,v in eqs:
        while a:
            p=a.bit_length()-1
            if p not in b:b[p]=(a,v);break
            x,z=b[p];a^=x;v^=z
        if not a and v:return None
    x=0
    for p in sorted(b):
        a,v=b[p]
        if (a&x).bit_count()%2!=v:x|=1<<p
    return x

def valid(P,x):
    return all(((a&x).bit_count()%2+2*((b&x).bit_count()%2))!=s for a,b,s in P)

def strict(P,r):
    m=len(P)
    if len(basis([a for p in P for a in p[:2]]))!=r:return False
    d=m-r
    return all(len(basis([a for j,p in enumerate(P) if t>>j&1 for a in p[:2]]))>=t.bit_count()-d for t in range(1<<m))

def direct_count(P,r):
    st['source_words']+=1<<r
    return sum(valid(P,x) for x in range(1<<r))

def pit(P,r,cap=3000):
    m=len(P);d=m-r
    pref=[[]];suff=[None]*(m+1);suff[m]=[]
    for a,b,_ in P:pref.append(basis(pref[-1]+[a,b]))
    for i in range(m-1,-1,-1):suff[i]=basis(suff[i+1]+list(P[i][:2]))
    B=[intersection(pref[i],suff[i]) for i in range(m+1)]
    h=[i-r+len(suff[i]) for i in range(m+1)]
    widths=[sum(math.comb(len(B[i]),k) for k in range(max(0,h[i]-d),min(len(B[i]),h[i])+1)) for i in range(m+1)]
    if max(widths)>cap:return None, {'peak_band':max(widths),'peak_boundary':max(map(len,B)),'declined':True}
    masks=[bands(len(B[i]),h[i],d) for i in range(m+1)]
    live=[(1,())];peak=1
    for i,(a,b,s) in enumerate(P,1):
        D=extend(B[i],B[i-1]+[a,b]);k=len(D)-len(B[i]);assert k==len(suff[i-1])-len(suff[i])<=2
        drop=((1<<len(D))-1)^((1<<len(B[i]))-1)
        old=[coordinate(v,D) for v in B[i-1]]
        opts=[(coordinate(a,D),1^(s&1)),(coordinate(b,D),1^(s>>1)),(coordinate(a^b,D),1^((s&1)^(s>>1)))]
        # Only construct columns reached by the retained actual coefficient basis.
        active=0
        for v,_ in live:active|=v
        cols=[{}, {}, {}]
        for j,M in enumerate(masks[i-1]):
            if not (active>>j&1):continue
            eqs=[(old[t],1) for t in range(len(old)) if M>>t&1]
            for aidx,opt in enumerate(opts):
                out=0
                for l,Q in enumerate(masks[i]):
                    if parity_unique(eqs+[opt],Q|drop):out|=1<<l
                cols[aidx][j]=out
        piv={};new=[]
        for v,path in live:
            for aidx in range(3):
                z=0;vv=v
                while vv:
                    j=(vv&-vv).bit_length()-1;vv&=vv-1;z^=cols[aidx][j]
                x=z
                while x:
                    j=x.bit_length()-1
                    if j not in piv:
                        piv[j]=x;new.append((z,path+(aidx,)));break
                    x^=piv[j];st['span_xors']+=1
                st['coefficient_vectors']+=1
        live=new;peak=max(peak,len(live));st['stages']+=1
        if not live:return False,{'peak_band':max(widths),'peak_boundary':max(map(len,B)),'peak_live':peak,'declined':False}
    assert masks[-1]==[0] and live[0][0]==1
    path=live[0][1];eq=[]
    for (a,b,s),j in zip(P,path):eq.append(([a,b,a^b][j],[1^(s&1),1^(s>>1),1^((s&1)^(s>>1))][j]))
    x=solve_equs(eq,r);assert x is not None and valid(P,x);st['verified_witnesses']+=1
    return True,{'peak_band':max(widths),'peak_boundary':max(map(len,B)),'peak_live':peak,'declined':False}

F=[]
def c(i):return 0 if i==1 else 1<<(i-2)
for i in range(1,8):
    for j in range(i+1,8):
        k=i^j
        if k>j:F.append((c(i)^c(j),c(i)^c(k),0))

def expand(P,r):
    triples=[]; shifts=[]
    for i,(a,b,s) in enumerate(P):
        p,q,v=[1<<(r+3*i+j) for j in range(3)]
        triples.extend([(p,v,2),(p,q,3),(p^q,p^v,1)])
        shifts.append((a^q,b^v,s))
    return triples+shifts,r+3*len(P)

def expand_one(P,r):
    a,b,s=P[0];p,q,v=[1<<(r+j) for j in range(3)]
    return [(p,v,2),(p,q,3),(p^q,p^v,1),(a^q,b^v,s)]+P[1:],r+3

cases=[]
def test(P,r,name,ref=True):
    if len(P)<=12:assert strict(P,r)
    label,info=pit(P,r);n=direct_count(P,r) if ref else None
    if ref:assert label==(n>0),(name,label,n)
    else:assert label is (name.endswith('SAT neighbor'))
    cases.append(dict(name=name,r=r,m=len(P),d=len(P)-r,result=label,models=n,**info))
    st['cases']+=1
for i in range(-1,7):
    for s in ([0] if i<0 else [1,2,3]):test([(a,b,s if j==i else 0) for j,(a,b,_) in enumerate(F)],6,'Fano root' if i<0 else f'Fano {i}/{s}')
for sign in [0,1]:
    P=[(a,b,sign if i==0 else s) for i,(a,b,s) in enumerate(F)];Q,r=expand_one(P,6);test(Q,r,'single expansion '+str(sign))
for d in range(3):
    done=0
    while done<16:
        r=rng.randrange(3,6);P=[]
        for _ in range(r+d):
            a,b=rng.sample(range(1,1<<r),2);P.append((a,b,rng.randrange(4)))
        if not strict(P,r):continue
        test(P,r,f'random d={d}/{done}');done+=1
# Full RT21 first layer: all unshifted triples, then shifted source owners.
for sign in [0,1]:
    P=[(a,b,sign if i==0 else s) for i,(a,b,s) in enumerate(F)];Q,r=expand(P,6)
    test(Q,r,'full expansion '+('SAT neighbor' if sign else 'UNSAT root'),False)
print(json.dumps(dict(stats=dict(st),cases=cases),indent=2))
