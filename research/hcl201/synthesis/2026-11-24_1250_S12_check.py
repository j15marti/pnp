import itertools, json, random
import networkx as nx
from collections import Counter

stats=Counter()
def verify(A,b,x):
    return all(sum(a*v for a,v in zip(row,x))==t for row,t in zip(A,b))
def brute(A,b):
    for x in itertools.product((0,1),repeat=len(A[0])):
        stats['reference_words']+=1
        if verify(A,b,x): return x
    return None

def close(A,b,pins):
    pins=dict(pins)
    while True:
        changed=False
        for row,t in zip(A,b):
            rem=t-sum(row[j]*v for j,v in pins.items())
            free=[j for j,a in enumerate(row) if a and j not in pins]
            def sums(skip=None):
                s={0}
                for j in free:
                    if j!=skip: s=s|{v+row[j] for v in s}
                return s
            stats['row_checks']+=1
            if rem not in sums(): return None
            for j in free:
                s=sums(j); ok=[v for v in (0,1) if rem-row[j]*v in s]
                stats['pin_checks']+=1
                if len(ok)==1:
                    pins[j]=ok[0]; stats['forced_pins']+=1; changed=True; break
            if changed: break
        if not changed: return pins

def terminal(A,b,pins):
    m=len(A[0]); n=len(b); G=nx.Graph(); optional=[]; endpoints={}
    cols={j:[(i,1 if A[i][j]>0 else -1) for i in range(n) for _ in range(abs(A[i][j]))] for j in range(m) if j not in pins}
    quota=[b[i]-sum(A[i][j]*v for j,v in pins.items()) for i in range(n)]
    for occ in cols.values():
        assert len(occ)<=2
        for i,s in occ: quota[i]+=int(s<0)
    for i,k in enumerate(quota):
        if not 0<=k<=sum(r==i for occ in cols.values() for r,s in occ): return None
        G.add_nodes_from(('s',i,h) for h in range(k))
    for j,occ in cols.items():
        if not occ: continue
        ps=[('p',j,h) for h in range(len(occ))]; G.add_nodes_from(ps); endpoints[j]=ps[0]
        for p,(i,s) in zip(ps,occ):
            G.add_edges_from((p,('s',i,h)) for h in range(quota[i]))
        if len(ps)==1:
            leaf=('o',j); optional.append(leaf); G.add_edge(ps[0],leaf)
        elif occ[0][1]==occ[1][1]: G.add_edge(*ps)
        else:
            mid=('m',j); G.add_edges_from((p,mid) for p in ps)
    if len(G)%2:
        optional.append(('dummy',)); G.add_node(('dummy',))
    G.add_edges_from(itertools.combinations(optional,2))
    stats['matching_calls']+=1; stats['max_nodes']=max(stats['max_nodes'],len(G)); stats['max_edges']=max(stats['max_edges'],G.number_of_edges())
    M=nx.max_weight_matching(G,maxcardinality=True)
    if 2*len(M)!=len(G): return None
    mate={a:b for u,v in M for a,b in ((u,v),(v,u))}; x=[pins.get(j,0) for j in range(m)]
    for j,p in endpoints.items():
        active=mate[p][0]=='s'; x[j]=int(active) if cols[j][0][1]>0 else int(not active)
    assert verify(A,b,x); return x

def solve(A,b,pins=None):
    pins=close(A,b,pins or {})
    if pins is None: return None
    bad=[j for j in range(len(A[0])) if j not in pins and sum(abs(row[j]) for row in A)>2]
    if not bad: return terminal(A,b,pins)
    j=bad[0]
    for v in (0,1):
        stats['guard_branches']+=1
        x=solve(A,b,{**pins,j:v})
        if x is not None: return x
    return None

def matrix(n,cols):
    return [[sum(s for i,s in col if i==r) for col in cols] for r in range(n)]

def check(A,b,expected=None,reference=True):
    x=solve(A,b)
    if reference: expected=brute(A,b) is not None
    assert (x is not None)==expected,(A,b,x,expected)
    stats['tests']+=1; stats['sat' if expected else 'unsat']+=1
    if x is not None: assert verify(A,b,x); stats['lifts']+=1

rng=random.Random(20261124)
for trial in range(260):
    n=rng.randint(2,6); m=rng.randint(2,11)
    cols=[[(rng.randrange(n),rng.choice((-1,1))) for _ in range(rng.randint(0,3 if trial%4==0 else 2))] for j in range(m)]
    A=matrix(n,cols); x=[rng.randrange(2) for j in range(m)]
    b=[sum(a*v for a,v in zip(row,x)) for row in A]
    if trial%2: b[rng.randrange(n)]+=rng.choice((-1,1))
    check(A,b)
random_stats=dict(stats)
# Two signed occurrences, opposite signs, and repeated same-row coefficient.
for A,b in [([[2]],[1]),([[2]],[2]),([[1],[-1]],[1,-1]),([[1],[1]],[1,0]),([[-2]],[-2])]: check(A,b)
# Exact-cover width-three controls.
triples=[[(i,1) for i in t] for t in itertools.combinations(range(6),3) if 0 in t]
check(matrix(6,triples),[1]*6); check(matrix(6,triples+[[(i,1) for i in (3,4,5)]]),[1]*6)
# Three odd cycles joined to a single hub: Tutte obstruction; one new cross edge repairs it.
scaling=[]
for L in (3,5,9,17,33,65):
    n=3*L+1; cols=[]
    for k in range(3):
        vs=list(range(1+k*L,1+(k+1)*L))
        cols.extend([[(v,1),(vs[(j+1)%L],1)] for j,v in enumerate(vs)])
        cols.append([(0,1),(vs[0],1)])
    before=stats['matching_calls']; check(matrix(n,cols),[1]*n,False,False)
    check(matrix(n,cols+[[(1,1),(L+1,1)]]),[1]*n,True,False)
    scaling.append(dict(cycle_length=L,rows=n,old_exception_count=len(cols),matching_calls=stats['matching_calls']-before))
print(json.dumps(dict(seed=20261124,networkx=nx.__version__,random=random_stats,total=dict(stats),scaling=scaling),indent=2))
