"""Compact independent LSPV-1 public checker; no external dependencies.
Expanded source-indexed witness/proof/operation audit is in separate local ZIP.
"""
from collections import defaultdict
from itertools import combinations
import json

def build(edges):
    k=max(max(e) for e in edges)+1
    bags=[[] for _ in range(k)]
    for var,(u,v) in enumerate(edges,1):
        bags[u].append(var);bags[v].append(var)
    assert all(len(b)==3 for b in bags)
    source=[]
    for bag in bags: source += [tuple(bag),tuple(-x for x in bag)]
    return source

def truth(c,a):
    return sum(((a>>(abs(z)-1))&1)==(z>0) for z in c)

def check(form):
    n=max(abs(z) for c in form for z in c)
    return [a for a in range(1<<n) if all(truth(c,a)>0 for c in form)]

def solve_balanced_paired(form):
    if len(form)%2 or any(len(c)!=3 or len({abs(x) for x in c})!=3 for c in form):return None
    # Compact checker expects authenticated complement pairs in consecutive indices.
    # The expanded original-source recognizer finds pairs.
    pairs=len(form)//2
    if any(form[2*p+1]!=tuple(-i for i in form[2*p]) for p in range(pairs)):return None
    occurrence=defaultdict(list)
    for p in range(pairs):
        for lit in form[2*p]: occurrence[abs(lit)].append((p,int(lit<0)))
    if any(len(v)!=2 or v[0][0]==v[1][0] for v in occurrence.values()):return None
    adj=[[] for _ in range(pairs)]
    for i,((u,a),(v,b)) in occurrence.items():
        adj[u].append((v,a^b,i));adj[v].append((u,a^b,i))
    if any(len(x)!=3 for x in adj):return None
    e={}
    for start in range(pairs):
        if start in e:continue
        e[start]=0; stack=[start]
        while stack:
            u=stack.pop()
            for v,d,i in adj[u]:
                if v in e:
                    if e[v]!=e[u]^d:return None
                else:e[v]=e[u]^d;stack.append(v)
    g={i:(b[0][1]^e[b[0][0]]) for i,b in occurrence.items()}
    owner=[-1]*pairs;orig=[-1]*pairs
    def augment(u,seen):
        for v,d,i in adj[u]:
            if v in seen:continue
            seen.add(v)
            if owner[v]<0 or augment(owner[v],seen):
                owner[v]=u;orig[v]=i;return True
        return False
    assert all(augment(u,set()) for u in range(pairs))
    red=set(orig)
    witness=sum((int(i in red)^g[i])<<(i-1) for i in occurrence)
    assert all(truth(c,witness)>0 for c in form)
    return witness

def mode_matrix(c,d):
    s={abs(x):x>0 for x in c};t={abs(x):x>0 for x in d}
    same=[x for x in s.keys()&t.keys() if s[x]==t[x]]
    opp=[x for x in s.keys()&t.keys() if s[x]!=t[x]]
    return {'SS':not opp,'SU':not same,'US':not same,'UU':not opp}

k4=build(list(combinations(range(4),2)))
assert mode_matrix(k4[0],k4[1])=={'SS':False,'SU':True,'US':True,'UU':False}
w=solve_balanced_paired(k4)
assert w is not None and all(truth(c,w)>0 for c in k4)
assert len(check(k4))==18
unbalanced=k4.copy()
unbalanced[0]=(-unbalanced[0][0],)+unbalanced[0][1:]
unbalanced[1]=tuple(-x for x in unbalanced[0])
assert solve_balanced_paired(unbalanced) is None
assert len(check(unbalanced))==20
k5=[]
for tri in combinations(range(1,6),3):
    k5.extend((tri,tuple(-x for x in tri)))
assert solve_balanced_paired(k5) is None
assert check(k5)==[]
for f in (k4,unbalanced,k5):
    n=max(abs(x) for c in f for x in c)
    for a in range(1<<n):
        b=((1<<n)-1)^a
        assert all(truth(c,a)>0 for c in f)==all(truth(c,b)>0 for c in f)
        categories=[sum(truth(c,a)==t for c in f) for t in range(4)]
        assert categories[0]==categories[3]
print(json.dumps({'K4_sat_models':18,'K4_witness':w,
 'unbalanced_K4_sat_models':20,'K5_all_assignments_UNSAT':32,
 'K4_source_pair_SS_SU_US_UU':mode_matrix(k4[0],k4[1]),
 'status':'COMPUTATIONAL checks passed; full theorem requires separate proof'},sort_keys=True))
