# LSPV-2/462: strict-3CNF clause gadget replay; no native FLMV simulation.
import itertools

def encode(c):
    q = max([abs(x) for x in c], default=0) + 1
    def fresh():
        nonlocal q
        x=q; q+=1
        return x
    k=len(c)
    if any(x==0 for x in c) or len(set(map(abs,c)))!=k:
        raise ValueError('invalid source literals')
    if k==0:
        a,b,d=fresh(),fresh(),fresh()
        return [[s*a,t*b,u*d] for s,t,u in itertools.product((-1,1),repeat=3)]
    if k==1:
        a,b=fresh(),fresh()
        return [[c[0],s*a,t*b] for s,t in itertools.product((-1,1),repeat=2)]
    if k==2:
        a=fresh();return [[c[0],c[1],a],[c[0],c[1],-a]]
    if k==3:return [c]
    y=[fresh() for _ in range(k-3)]
    return [[c[0],c[1],y[0]]]+[[-y[i-1],c[i+1],y[i]] for i in range(1,k-3)]+[[-y[-1],c[-2],c[-1]]]

def witness(cnf,pins):
    v=sorted({abs(l) for c in cnf for l in c}-set(pins))
    return any(all(any(a.get(abs(l),False)==(l>0) for l in c) for c in cnf)
               for bits in itertools.product((False,True),repeat=len(v))
               for a in [{**pins,**dict(zip(v,bits))}])

count=0
for k in range(8):
    c=[(j+1)*(-1 if j&1 else 1) for j in range(k)]
    g=encode(c)
    assert all(len(t)==3 and len(set(map(abs,t)))==3 for t in g)
    for bits in itertools.product((False,True),repeat=k):
        p={i+1:b for i,b in enumerate(bits)}
        assert witness(g,p)==any(p[abs(l)]==(l>0) for l in c)
        count+=1
for bad in [[0],[1,1],[1,-1,3]]:
    try:encode(bad)
    except ValueError:pass
    else:raise AssertionError('corrupt source accepted')
print({'status':'PASS','projected_assignments':count,'corrupt_rejections':3})
