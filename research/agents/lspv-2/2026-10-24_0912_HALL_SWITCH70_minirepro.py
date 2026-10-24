#!/usr/bin/env python3
"""HALL-SWITCH70, minimal independent standard-library reproduction.

Run: python research/agents/lspv-2/2026-10-24_0912_HALL_SWITCH70_minirepro.py
Constructs strict signed exact-(2,2) cases, contracts complementary pairs,
tests tautological pivots and finds source-coherent Hall witnesses.
U198 UNSAT is NOT proved by this script; full original audit is distributed
with HALL-SWITCH70's standalone research package.
"""
import ast
import itertools
import json
import pathlib
from collections import Counter, defaultdict, deque

def family(q, shifted=True):
    assert q>=2
    sigma=[(i+1)%q if shifted else i for i in range(q)]
    tau=[(i-1)%q if shifted else i for i in range(q)]
    F=[]
    for i in range(q):
        a,b,c,x,y,z=[6*i+j for j in range(1,7)]
        ap=6*((i+1)%q)+1
        ns=6*sigma[i]+6
        nt=6*tau[i]+6
        F.extend([(ap,b,x),(ap,b,-x),(-a,c,y),(-a,c,-y),
                  (-b,x,z),(-b,-x,-ns),(-c,y,z),(-c,-y,-nt)])
    return F

def check_source(F):
    n=max(abs(x) for c in F for x in c)
    m=len(F)
    assert 4*n==3*m
    assert {abs(x) for c in F for x in c}==set(range(1,n+1))
    assert all(len(c)==3 and len({abs(x) for x in c})==3 for c in F)
    assert len(set(tuple(sorted(c)) for c in F))==m
    ctr=Counter(x for c in F for x in c)
    assert all(ctr[i]==ctr[-i]==2 for i in range(1,n+1))
    return n,m

def contract(F):
    index=defaultdict(lambda:{1:[],-1:[]})
    for j,c in enumerate(F):
        for i,x in enumerate(c):
            index[(tuple(sorted(c[:i]+c[i+1:])),abs(x))][1 if x>0 else -1].append(j)
    used=set();B=[]
    for (other,var),bucket in sorted(index.items()):
        for i in bucket[1]:
            for j in bucket[-1]:
                assert i not in used and j not in used
                used.update((i,j))
                B.append(other)
    T=[c for i,c in enumerate(F) if i not in used]
    assert len(used)==2*len(B)
    return B,T

def taut_pivots(B,T):
    boundary={abs(x) for c in B for x in c}
    occ=defaultdict(list)
    for i,c in enumerate(T):
        for x in c:occ[abs(x)].append((i,x))
    candidates=0;good=0
    for v,rows in occ.items():
        if v in boundary or len(rows)!=2 or rows[0][1]*rows[1][1]>=0:
            continue
        candidates+=1
        i,j=rows[0][0],rows[1][0]
        left=[x for x in T[i] if abs(x)!=v]
        right=[x for x in T[j] if abs(x)!=v]
        if any(-x in right for x in left):
            good+=1
    return candidates,good

def match_clauses(clauses):
    """Hopcroft-Karp over original-source variable identifiers."""
    M=len(clauses)
    n=max((abs(x) for c in clauses for x in c),default=0)
    if M>n:return None,0,0
    adj=[list(dict.fromkeys(abs(x) for x in c)) for c in clauses]
    match=[0]*M;back=[-1]*(n+1);dist=[0]*M
    scans=0
    def bfs():
        nonlocal scans
        queue=deque()
        INF=M+n+1
        for u in range(M):
            if match[u]==0:dist[u]=0;queue.append(u)
            else:dist[u]=INF
        found=False
        while queue:
            u=queue.popleft()
            for v in adj[u]:
                scans+=1
                z=back[v]
                if z<0:found=True
                elif dist[z]==INF:dist[z]=dist[u]+1;queue.append(z)
        return found
    def dfs(u):
        nonlocal scans
        for v in adj[u]:
            scans+=1
            z=back[v]
            if z<0 or (dist[z]==dist[u]+1 and dfs(z)):
                match[u]=v;back[v]=u;return True
        dist[u]=M+n+1
        return False
    while bfs():
        for i in range(M):
            if match[i]==0:dfs(i)
    k=sum(x>0 for x in match)
    return match if k==M else None,k,scans

def verify(F,a):
    return all(any(a[abs(l)]==(l>0) for l in c) for c in F)

def recover(F,B,T,matching,n):
    a={i:False for i in range(1,n+1)}
    for clause,var in zip(B+T,matching):
        lit=next(l for l in clause if abs(l)==var)
        a[var]=(lit>0)
    assert verify(F,a)
    return a

def surplus(q):
    # PAIRPATH73 signed exact-(2,2) 6-variable/8-clause gadget
    F=[]
    for i in range(q):
        a,b,c,x,y,z=[6*i+j for j in range(1,7)]
        F.extend([(a,b,x),(a,b,-x),(-b,c,y),(-b,c,-y),
                  (-c,-a,z),(-c,-a,-z),(x,y,z),(-x,-y,-z)])
    return F

def combine(A,B):
    z=max((abs(l) for c in A for l in c),default=0)
    return list(A)+[tuple((1 if l>0 else -1)*(abs(l)+z) for l in c) for c in B]

def small_control():
    cube=list(itertools.product([0,1],repeat=3))
    U=[tuple((i+1 if b==0 else -(i+1)) for i,b in enumerate(bits)) for bits in cube]
    V=U[:-1]
    def brute(F):
        return any(all(any(((bits[abs(x)-1]==1)==(x>0)) for x in c) for c in F)
                   for bits in cube)
    assert not brute(U) and brute(V)
    return {'proper3_UNSAT_clauses':len(U),'proper3_SAT_clauses':len(V)}

def run():
    results={'run_id':'HALL_SWITCH70','cases':[],'small_controls':small_control(),
             'UNSAT_198_status':'imported DOECKER-CORE-CERT61, not replayed'}
    for q in [2,3,4,8,32,128,256]:
        F=family(q,True)
        n,m=check_source(F)
        B,T=contract(F)
        k,t=taut_pivots(B,T)
        matching,nu,scans=match_clauses(B+T)
        assert (len(B),len(T),k,t,nu)==(2*q,4*q,2*q,0,6*q)
        assert matching is not None
        recover(F,B,T,matching,n)
        results['cases'].append({'q':q,'n':n,'m':m,'p':len(B),'delta':len(T),
                                 'taut_pivots':t,'Hall_matched':nu,'HK_scans':scans,
                                 'SAT_witness_verified':True})
    F=family(8,False)
    n,m=check_source(F)
    B,T=contract(F)
    k,t=taut_pivots(B,T)
    assert (k,t)==(16,16)
    results['unshifted_adaptive_choice']='tautological-pivot cancellation then 2SAT'
    src=pathlib.Path(__file__).parents[1]/'lspv-2'/'2026-10-24_0011_DOECKER61_original_source.txt'
    if src.exists():
        raw='\n'.join(s for s in src.read_text().splitlines() if s.strip() and not s.startswith('#'))
        try:U=[tuple(int(x) for x in c) for c in ast.literal_eval(raw)]
        except (SyntaxError,ValueError):U=None
        if U:
            check_source(U)
            for q in [66,70,128]:
                F=combine(U,surplus(q))
                n,m=check_source(F)
                B,T=contract(F)
                matching,nu,scans=match_clauses(B+T)
                assert len(B)==3*q and m-len(B)<=n and matching is None
                results.setdefault('hall_deficiency',[]).append(
                  {'q':q,'n':n,'reduced_clauses':m-len(B),'matching_size':nu})
    print(json.dumps(results,sort_keys=True,indent=2))

if __name__=='__main__':
    run()
