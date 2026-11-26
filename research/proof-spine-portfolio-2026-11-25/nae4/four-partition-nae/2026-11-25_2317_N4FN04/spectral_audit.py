import sympy as s, json
from collections import Counter
P=[[(0,1,2),(3,4,5),(6,7,8)],[(0,3,6),(1,4,7),(2,5,8)],[(0,4,8),(1,5,6),(2,3,7)],[(0,5,7),(1,3,8),(2,4,6)]]
C=sum(P,[]);minor=[1,1,0,1,2,1,1,1,1,1,2,0];x=s.symbols('x')
def B(z):
    M=s.zeros(9)
    for c,h in zip(C,minor):
        d=[int(i==h) for i in range(3)]
        for i in range(3):
            for j in range(3):
                if i!=j:M[c[i],c[j]]+=s.sympify(z)**(d[j]-d[i])
    return M
F=B(1).charpoly(x).as_poly().sqf_part()*B(-1).charpoly(x).as_poly().sqf_part();F=F.sqf_part()
f=B(2).charpoly(x).as_poly();g=B(3).charpoly(x).as_poly()
def modpoly(f,p):
    return s.Poly.from_list([int(c.p)*pow(int(c.q),-1,p)%p for c in f.all_coeffs()],x,modulus=p)
assert s.gcd(modpoly(f,101),modpoly(g,101)).degree()==0
print('f2 mod 101',modpoly(f,101).as_expr());print('f3 mod 101',modpoly(g,101).as_expr());print('F',s.factor(F.as_expr()))
def charcase(k):
    cs=[];seen=set()
    for p in P:
        a=[]
        for c in p:
            h=minor[C.index(c)]
            for t in range(k):
                u=tuple(v*k+(t+int(j==h))%k for j,v in enumerate(c));a.extend(u);cs.append(u)
                for i in range(3):
                    for j in range(i):
                        e=tuple(sorted((u[i],u[j])));assert e not in seen;seen.add(e)
        assert sorted(a)==list(range(9*k))
    if k%2==0:assert all(len({(v%k)%2 for v in c})==2 for c in cs)
    Q=1000000//k+1
    while not s.isprime(Q*k+1):Q+=1
    q=Q*k+1;z=pow(int(s.primitive_root(q)),Q,q)
    def mul(a,b):return [[sum(a[i][t]*b[t][j] for t in range(9))%q for j in range(9)] for i in range(9)]
    def rank(a):
        a=[r[:] for r in a];d=0
        for j in range(9):
            t=next((i for i in range(d,9) if a[i][j]),None)
            if t is None:continue
            a[d],a[t]=a[t],a[d];v=pow(a[d][j],-1,q);a[d]=[(w*v)%q for w in a[d]]
            for i in range(d+1,9):
                c=a[i][j]
                if c:a[i]=[(u-c*v)%q for u,v in zip(a[i],a[d])]
            d+=1
        return d
    nullity=0;active=[];co=[int(v)%q for v in F.all_coeffs()]
    for h in range(k):
        w=pow(z,h,q);A=[[0]*9 for i in range(9)]
        for c,a in zip(C,minor):
            for i in range(3):
                for j in range(3):
                    if i!=j:A[c[i]][c[j]]=(A[c[i]][c[j]]+pow(w,int(j==a)-int(i==a),q))%q
        M=[[0]*9 for i in range(9)]
        for v in co:
            M=mul(M,A)
            for i in range(9):M[i][i]=(M[i][i]+v)%q
        r=9-rank(M);nullity+=r
        if r:active.append([h,r])
    return dict(sheets=k,variables=9*k,q=q,mod_kernel=nullity,active=active,parity_witness_verified=k%2==0)
res=[charcase(k) for k in [5,10,22,34,62,334]]
print(json.dumps(res))
