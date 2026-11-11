"""Exact minimum resolution refutation width (Res(w) saturation) versus
polynomial-time algorithmic decision, for families with known Res lower bounds.
Each family/size is one independent chunk (<~30 s). Output: JSON lines."""
import itertools, json, random, sys, time

def resolve(c, d):
    piv = [l for l in c if -l in d]
    if len(piv) != 1: return None
    l = piv[0]
    return frozenset((c - {l}) | (d - {-l}))

def min_width(clauses, wmax):
    """Smallest w >= initial width such that width-w resolution derives []."""
    w0 = max(len(c) for c in clauses)
    for w in range(w0, wmax + 1):
        S = set(frozenset(c) for c in clauses); frontier = list(S); t0=time.time()
        while frontier:
            new = []
            Sl = list(S)
            for c in frontier:
                for d in Sl:
                    r = resolve(c, d)
                    if r is not None and len(r) <= w and r not in S:
                        if not r: return w
                        S.add(r); new.append(r)
            frontier = new
            if time.time()-t0 > 25: return ('timeout', w)
    return None

def tseitin(edges, charge):
    vs = sorted({v for e in edges for v in e}); clauses=[]
    for v in vs:
        inc = [i+1 for i,e in enumerate(edges) if v in e]
        for signs in itertools.product([1,-1], repeat=len(inc)):
            # forbid assignments with parity != charge[v]
            par = sum(1 for s in signs if s==1) % 2   # literal x true in clause means x=0 forbidden...
            # clause = OR of literals; falsified by assignment x_i = (s_i==-1)
            ones = sum(1 for s in signs if s==-1) % 2
            if ones != charge[v]:
                clauses.append([s*x for s,x in zip(signs,inc)])
    return clauses, len(edges)

def gauss_tseitin(edges, charge):
    """Poly-time GF(2) decision: satisfiable iff total charge even per component."""
    vs = sorted({v for e in edges for v in e}); idx={v:i for i,v in enumerate(vs)}
    rows=[]
    for v in vs:
        r=0
        for i,e in enumerate(edges):
            if v in e: r|=1<<i
        rows.append((r,charge[v]))
    # eliminate
    piv=[]
    for r,b in rows:
        for p,(pr,pb) in piv:
            if r>>p &1: r^=pr; b^=pb
        if r==0:
            if b: return 'UNSAT'
            continue
        p=r.bit_length()-1; piv.append((p,(r,b)))
    return 'SAT'

def php(n):  # n+1 pigeons, n holes
    v=lambda i,j:i*n+j+1; C=[[v(i,j) for j in range(n)] for i in range(n+1)]
    for j in range(n):
        for a,b in itertools.combinations(range(n+1),2): C.append([-v(a,j),-v(b,j)])
    return C, (n+1)*n

def random3(n, m, seed):
    rnd=random.Random(seed); C=[]
    for _ in range(m):
        vs=rnd.sample(range(1,n+1),3); C.append([x*rnd.choice([1,-1]) for x in vs])
    return C

def brute_unsat(C,n):
    for a in range(1<<n):
        if all(any(((a>>(abs(l)-1))&1)==(l>0) for l in c) for c in C): return False
    return True

if __name__=='__main__':
    fam, size = sys.argv[1], int(sys.argv[2])
    t=time.time()
    if fam=='tseitin_cycle_chords':   # 3-regular "circular ladder"/prism on 2k vertices
        k=size; edges=[(i,(i+1)%k) for i in range(k)]+[(k+i,k+(i+1)%k) for i in range(k)]+[(i,k+i) for i in range(k)]
        ch={v:0 for v in range(2*k)}; ch[0]=1
        C,nv=tseitin(edges,ch); dec=gauss_tseitin(edges,ch)
        out=dict(family=fam,k=k,vars=nv,clauses=len(C),gauss=dec,min_res_width=min_width(C,8))
    elif fam=='php':
        C,nv=php(size); out=dict(family=fam,n=size,vars=nv,clauses=len(C),
            counting='UNSAT (n+1>n, O(1) arithmetic)',min_res_width=min_width(C,size+2))
    elif fam=='random3':
        n=size; seed=0
        while True:
            C=random3(n,int(6*n),seed)
            if brute_unsat(C,n): break
            seed+=1
        out=dict(family=fam,n=n,m=len(C),seed=seed,min_res_width=min_width(C,7),
                 note='no known poly-time refuter for constant density (Feige hypothesis)')
    out['seconds']=round(time.time()-t,2); print(json.dumps(out))
