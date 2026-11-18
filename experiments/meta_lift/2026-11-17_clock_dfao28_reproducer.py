#!/usr/bin/env python3
"""CLOCKDFAO28 compact independent dyadic-section reproducer (stdlib only)."""
from itertools import product

assertions=0

def check(x):
    global assertions
    assertions+=1
    assert x

def endpoint(word, schedule, rule):
    q=0
    for i,b in enumerate(word):
        q=rule[schedule[i]][q][b]
    return q

def tables(n,delta,out,rule):
    A=len(delta);K=len(rule[0]);R=[];M=[None]
    base=[[0]*K for _ in range(A)]; bits={}
    for a in range(A):
        for p in range(K):
            for b in (0,1):
                q=rule[out[a]][p][b]
                base[a][p]|=1<<q
                bits.setdefault((a,p,q),b)
    R.append(base)
    for h in range(1,n+1):
        current=[[0]*K for _ in range(A)];choice={}
        for a in range(A):
            left=R[-1][delta[a][0]];right=R[-1][delta[a][1]]
            for p in range(K):
                for r in range(K):
                    if left[p]>>r&1:
                        for q in range(K):
                            if right[r]>>q&1:
                                current[a][p]|=1<<q
                                choice.setdefault((a,p,q),r)
        R.append(current);M.append(choice)
    return R,M,bits

def recover(i,n,delta,R,M,bits,target):
    a=p=0;q=target
    check(R[n][a][p]>>q&1)
    for h in range(n,0,-1):
        r=M[h][(a,p,q)]
        b=i>>(h-1)&1
        p,q=(p,r) if b==0 else (r,q)
        a=delta[a][b]
    return bits[(a,p,q)]

for d in range(16):
    delta=[((d>>(2*a))&1,(d>>(2*a+1))&1) for a in range(2)]
    for o in range(4):
        out=[o&1,(o>>1)&1]
        schedule=[]
        for i in range(8):
            a=0
            for sh in (2,1,0):a=delta[a][i>>sh&1]
            schedule.append(out[a])
        for c in range(16):
            r0=[tuple(c>>(2*p+b)&1 for b in (0,1)) for p in range(2)]
            r1=[tuple((c^10)>>(2*p+b)&1 for b in (0,1)) for p in range(2)]
            rule=[r0,r1]
            R,M,bits=tables(3,delta,out,rule)
            reachable={endpoint(w,schedule,rule) for w in product((0,1),repeat=8)}
            expected={q for q in range(2) if R[3][0][0]>>q&1}
            check(reachable==expected)
            for target in reachable:
                recovered=[recover(i,3,delta,R,M,bits,target) for i in range(8)]
                check(endpoint(recovered,schedule,rule)==target)

# Aperiodic address-dependent unique-word control (Thue-Morse prefix).
delta=[(0,1),(1,0)];out=[0,1];n=6
rule=[[tuple(0 if b==t else 1 for b in (0,1)),(1,1)] for t in (0,1)]
R,M,bits=tables(n,delta,out,rule)
g=[recover(i,n,delta,R,M,bits,0) for i in range(1<<n)]
check(g==[i.bit_count()%2 for i in range(1<<n)])
print({'assertions':assertions,'failures':0,'models':1024,'source_cases':262144})
