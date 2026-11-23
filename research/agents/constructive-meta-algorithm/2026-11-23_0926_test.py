from itertools import product

def sat(clauses, bits):
    return all(any((bits[abs(l)-1] if l > 0 else not bits[-l-1]) for l in c) for c in clauses)

def brute(clauses, n):
    return any(sat(clauses, b) for b in product((False, True), repeat=n))

def simplify(clauses, v, value):
    out=[]
    for c in clauses:
        if any(abs(l)==v and (l>0)==value for l in c): continue
        d=tuple(l for l in c if abs(l)!=v)
        if not d: return None
        out.append(d)
    return out

def solve(clauses):
    if clauses is None: return False
    if not clauses: return True
    if all(len(c)<=2 for c in clauses):
        vs=sorted(set(abs(l) for c in clauses for l in c))
        adj={l:set() for v in vs for l in (v,-v)}
        for c in clauses:
            if len(c)==1:
                a=c[0]; adj[-a].add(a)
            else:
                a,b=c; adj[-a].add(b); adj[-b].add(a)
        def reach(a):
            seen={a}; stack=[a]
            while stack:
                for b in adj[stack.pop()]:
                    if b not in seen: seen.add(b); stack.append(b)
            return seen
        return all(-v not in reach(v) or v not in reach(-v) for v in vs)
    v=min(abs(l) for c in clauses for l in c)
    return solve(simplify(clauses,v,False)) or solve(simplify(clauses,v,True))

cases={
 'unsat_core':(3,[(1,2,3),(-1,2,3),(1,-2,3),(1,2,-3),(-1,-2,3),(-1,2,-3),(1,-2,-3),(-1,-2,-3)]),
 'sat_neighbor':(3,[(1,2,3),(-1,2,3),(1,-2,3),(1,2,-3),(-1,-2,3),(-1,2,-3),(1,-2,-3)]),
 'xor_unsat':(3,[(1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3),(-1,-2,-3),(-1,2,3),(1,-2,3),(1,2,-3)]),
 'two_sat_unsat':(2,[(1,2),(1,-2),(-1,2),(-1,-2)]),
 'disconnected_sat':(6,[(1,2,3),(-1,2,3),(4,5,6),(-4,5,6)])
}
for name,(n,clauses) in cases.items():
    actual=solve(clauses)
    expected=brute(clauses,n)
    assert actual==expected,(name,actual,expected)
    print(name,'SAT' if actual else 'UNSAT','verified')
