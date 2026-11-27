import itertools as it, random, json, hashlib
from sympy import Matrix
from sympy.matrices.normalforms import hermite_normal_form as hnf

def source(n,t):
    E=[(i,j,(i+j)%n) for i in range(n) for j in range(n)]
    E += [(i,j,(i+j+1)%n) for i in range(t) for j in range(n)]
    rng=random.Random(730+n*101+t)
    p=[rng.sample(range(n),n) for _ in range(3)]
    return [(p[0][i],p[1][j],p[2][z]) for i,j,z in E]

def acquire(n,E):
    cells=[[[] for j in range(n)] for i in range(n)]
    for i,j,z in E: cells[i][j].append(z)
    clean=[i for i in range(n) if all(len(c)==1 for c in cells[i]) and len({c[0] for c in cells[i]})==n]
    trials=0
    for a,b in it.permutations(clean,2):
        perm={cells[a][j][0]:cells[b][j][0] for j in range(n)}
        if len(set(perm.values()))!=n: continue
        lam={}; z=0
        while z not in lam: lam[z]=len(lam); z=perm[z]
        if len(lam)!=n: continue
        trials+=1
        v=[lam[c[0]] for c in cells[a]]
        u=[]
        for row in cells:
            ds={(lam[z]-v[j])%n for j,c in enumerate(row) for z in c}
            opts=[h for h in sorted(ds) if all((d-h)%n in (0,1) for d in ds)]
            if not opts: break
            u.append(opts[0])
        if len(u)!=n: continue
        w=[(lam[z]-u[i]-v[j])%n for i,j,z in E]
        assert all(x in (0,1) for x in w)
        upper=len({i for (i,j,z),x in zip(E,w) if x})
        delta=(sum(lam.values())-sum(u)-sum(v))%n
        if delta>upper: return w,upper,delta,trials
    return None

def inc(n,E,w=None):
    A=Matrix.zeros(3*n+(w is not None),len(E))
    for k,(i,j,z) in enumerate(E):
        A[i,k]=A[n+j,k]=A[2*n+z,k]=1
        if w is not None: A[3*n,k]=w[k]
    return A

def member(B,d): return hnf(B.row_join(d))==B

def star_checks(n,E,s):
    A=inc(n,E); checks=0; rng=random.Random(n*19+s)
    Us=[(i,) for i in range(2*n)] if s==1 else list(it.combinations(range(2*n),s))
    if s>1: Us=rng.sample(Us,min(12,len(Us)))
    for U in Us:
        U=set(U); S=[k for k,(i,j,z) in enumerate(E) if i in U or n+j in U]; B=hnf(A[:,[k for k in range(len(E)) if k not in set(S)]])
        if s==1: patterns=[(k,) for k in S]
        else:
            patterns=[]
            for _ in range(12):
                p=rng.sample(range(n),n); H=[]
                for i,j in enumerate(p):
                    if i in U or n+j in U: H.append(rng.choice([k for k,(a,b,c) in enumerate(E) if (a,b)==(i,j)]))
                patterns.append(tuple(H))
        for H in patterns:
            d=Matrix.ones(3*n,1)
            for k in H: d-=A[:,k]
            assert member(B,d), (n,U,H)
            checks+=1
    return checks

def run():
    out=[]
    for n in (6,8,10,12,16,32,64):
        t=n//2-1; E=source(n,t); ans=acquire(n,E); assert ans is not None
        w,upper,delta,trials=ans; assert upper==t and delta>t
        row=dict(n=n,t=t,m=len(E),sha256=hashlib.sha256(json.dumps(E,separators=(',',':')).encode()).hexdigest(),upper=upper,delta=delta,trials=trials)
        if n<=12:
            B=hnf(inc(n,E,w)); checks=[]
            for a in list(range(t+1))+[delta,delta+n]:
                ok=member(B,Matrix([1]*(3*n)+[a])); assert ok==(a%n==delta); checks.append([a,ok])
            row['lattice_checks']=checks
            row['star1']=star_checks(n,E,1)
            if t>2: row['star2_sample']=star_checks(n,E,2)
        out.append(row)
    assert acquire(3,source(3,0)) is None
    print(json.dumps(out,indent=2))
if __name__=='__main__': run()
