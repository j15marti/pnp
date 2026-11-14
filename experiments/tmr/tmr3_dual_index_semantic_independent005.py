"""Independent Python exact source-CNF semantic check for TMR-3/005 n<=2."""
import json, itertools

def src(n,a,b):
    w=max(1,(5*n-1).bit_length())
    z='1'*(5*n)+'0'+'1'*(8*n)+'0'
    for side,arr in enumerate((a,b)):
        for j in range(n):
            aux=(n if side==0 else 3*n)+2*j
            for u,v in itertools.product((0,1), repeat=2):
                for sign,vid in ((1-arr[j],j),(u,aux),(v,aux+1)):
                    z+=str(sign)+format(vid,f'0{w}b')
    return z

def parse(z):
    p=z.index('0');N=p;p+=1;stop=z.index('0',p);M=stop-p;p=stop+1
    w=max(1,(N-1).bit_length()); clauses=[]
    for _ in range(M):
        cl=[]
        for _ in range(3):
            s=int(z[p]); v=int(z[p+1:p+1+w],2);p+=1+w
            cl.append((s,v))
        clauses.append(cl)
    assert p==len(z)
    return N,clauses

def sat(z):
    N,C=parse(z)
    for a in itertools.product((0,1),repeat=N):
        if all(any(a[v] == s for s,v in clause) for clause in C):
            return True
    return False

checks=0
for n in (1,2):
    for a in itertools.product((0,1),repeat=n):
        for b in itertools.product((0,1),repeat=n):
            assert sat(src(n,a,b))==(a==b)
            checks+=1
print(json.dumps({'independent_python_bruteforce_cases':checks,'max_n':2,'failures':0}))
