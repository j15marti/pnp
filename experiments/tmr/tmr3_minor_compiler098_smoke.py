#!/usr/bin/env python3
"""TMR-3/098 compact independent smoke: minor-stable separators and free-path controls."""
import itertools, math
from functools import lru_cache

def cube(d):
    return [(u,u^(1<<j)) for u in range(1<<d) for j in range(d)
            if not (u&(1<<j))]

def minor_model(d,k=2):
    v=1<<d
    branch={u:{(u,j) for j in range(k)} for u in range(v)}
    E=set()
    for u in range(v):
        for j in range(k-1):
            E.add(frozenset(((u,j),(u,j+1))))
    for u,w in cube(d):
        a=("aux",u,w)
        branch[u].add(a)
        E.add(frozenset((a,(u,k-1))))
        E.add(frozenset((a,(w,k-1))))
    V=set().union(*branch.values())
    return V,E,branch

def components(V,E,removed):
    adj={u:set() for u in V if u not in removed}
    for edge in E:
        x,y=tuple(edge)
        if x in adj and y in adj:
            adj[x].add(y);adj[y].add(x)
    seen=set(); out=[]
    for start in adj:
        if start in seen: continue
        C={start}; todo=[start];seen.add(start)
        for x in todo:
            for y in adj[x]:
                if y not in seen:seen.add(y); C.add(y);todo.append(y)
        out.append(C)
    return out

def bound(d,B):
    v=1<<d
    return math.ceil(v*(d-math.log2(B))/(2*d-math.log2(B))-1e-10)

def oracle_depth(R,M):
    rows=[((1<<M)-1)<<(z*M) for z in range(R)]
    full=(1<<(R*M))-1
    @lru_cache(None)
    def f(read,ones):
        can_sat=any((read & row & ~ones)==0 for row in rows)
        can_unsat=all((read & ones & row)!=row for row in rows)
        if not (can_sat and can_unsat):return 0
        best=R*M+1
        todo=full^read
        while todo:
            bit=todo&-todo;todo-=bit
            best=min(best,1+max(f(read|bit,ones),f(read|bit,ones|bit)))
        return best
    return f(0,0)

def main():
    checks=0
    for d,k,B in [(2,2,2),(3,2,3),(3,2,4),(3,3,3)]:
        V,E,X=minor_model(d,k)
        assert len(set().union(*X.values()))==len(V); checks+=1
        for u,w in cube(d):
            assert any(a in X[u] and b in X[w] or
                       a in X[w] and b in X[u]
                       for edge in E for a,b in [tuple(edge)]); checks+=1
        for size in range(bound(d,B)):
            for selection in itertools.combinations(V,size):
                assert max(map(len,components(V,E,set(selection))),default=0)>B
                checks+=1
    for R,M in [(1,1),(2,2),(2,3),(3,2),(3,3)]:
        assert oracle_depth(R,M)==R*M; checks+=1
    for d in range(1,9):
        col=lambda u:u.bit_count()%5
        assert all((col(w)-col(u))%5==1 for u,w in cube(d));checks+=1
    for r,s in [(2,4),(3,5)]:
        for z in range(1<<s):
            assert [i for i in range(1<<r)
                    if (z&((1<<r)-1))==i]==[z&((1<<r)-1)]
            checks+=1
    print(f"TMR3-098 compact smoke: {checks} checks, 0 failures")
if __name__=="__main__":main()
