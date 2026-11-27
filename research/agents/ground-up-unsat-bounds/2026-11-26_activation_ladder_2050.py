from functools import lru_cache
from itertools import product

def norm(F):
    return tuple(sorted(set(tuple(sorted(set(c))) for c in F)))

def restrict(F,v,b):
    l=v if b else -v
    return norm(tuple(x for x in c if x!=-l) for c in F if l not in c)

@lru_cache(None)
def opt(F):
    if () in F: return (1,0)
    if not F: return (float('inf'),float('inf'))
    L=D=float('inf')
    for v in sorted({abs(x) for c in F for x in c}):
        a,b=opt(restrict(F,v,0)),opt(restrict(F,v,1))
        L=min(L,a[0]+b[0]);D=min(D,1+max(a[1],b[1]))
    return L,D

def ladder(F):
    n=max(abs(x) for c in F for x in c); m=len(F)
    z=list(range(n+1,n+m+1))
    G=norm([(*c,v) for c,v in zip(F,z)]+[(-z[0],)]+[(-b,a) for a,b in zip(z,z[1:])])
    return G,z

def sat(F):
    if () in F:return False
    if not F:return True
    v=abs(F[0][0]);return sat(restrict(F,v,0)) or sat(restrict(F,v,1))

def mus(F):return not sat(F) and all(sat(F[:i]+F[i+1:]) for i in range(len(F)))

def parity(vs,b):
    return [tuple(-v if bit else v for v,bit in zip(vs,bits)) for bits in product((0,1),repeat=len(vs)) if sum(bits)%2!=b]

def ring(n,k):
    return norm(c for i in range(n) for c in parity([j+1 for j in range(((i-1)%n)*k,((i-1)%n+1)*k)]+[j+1 for j in range(i*k,(i+1)*k)],int(i==0)))

if __name__=='__main__':
    bases=[('unit contradiction',norm([(1,),(-1,)])),('one split',norm([(1,),(-1,2),(-1,-2)])),('two splits',norm([(1,3),(1,-3),(-1,2),(-1,-2)])),('full cube 2',norm(product((-1,1),(-2,2)))),('ring 3x1',ring(3,1)),('ring 4x1',ring(4,1))]
    for name,F in bases:
        G,z=ladder(F);a=opt(F);b=opt(G); assert mus(F) and mus(G) and b[0]==a[0]+len(F)
        for t in range(len(z)+1):
            H=G
            for v in z[:len(z)-t]: H=restrict(H,v,0)
            assert opt(H)[0]==a[0]+t and mus(H)
        # explicit bit encoding: unary header n,m (n+m+2), each clause unary length (w+1), w signed identifiers ceil(log2(n+1))+1
        n=max(abs(x) for c in G for x in c);bits=n+len(G)+2+sum(1+len(c)*(2+n.bit_length()) for c in G)
        print(name,'n,m,bits=',n,len(G),bits,'base L,D=',a,'ladder L,D=',b,'MUS yes; all suffix restrictions checked',flush=True)
        opt.cache_clear()
    for n,k in [(3,1),(4,1),(3,2),(4,2),(3,3)]:
        F=ring(n,k);print('old ring',n,k,len(F),opt(F),mus(F),flush=True);opt.cache_clear()
