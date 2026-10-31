#!/usr/bin/env python3
"""LSPV-2 271 public standalone check: exact SAT/UNSAT prefix projection,
original-indexed resolution, direct indexed ordinary-DIMACS bytes, parity
prefix obstruction. Restricted finite mathematics, ARC and P vs NP OPEN."""
import bisect,itertools,json
def canonical(cl):return tuple(sorted(set(cl),key=lambda z:(abs(z),z<0)))
def resolve(a,b,p):
    assert p in a and -p in b
    z=canonical((set(a)-{p})|(set(b)-{-p}))
    assert all(-x not in z for x in z)
    return z
def pin(x,p,q):return [(x,p,q),(x,p,-q),(x,-p,q),(x,-p,-q)]
def holds(F,a):return all(any(a[abs(l)]==(l>0) for l in c) for c in F)
def exists(F,n,fixed):
    rest=[x for x in range(1,n+1) if x not in fixed]
    return any(holds(F,{**fixed,**dict(zip(rest,values))})
               for values in itertools.product((0,1),repeat=len(rest)))
def child_index(b,guards):
    header=f'p cnf {b} {len(guards)}\n'
    rows=[' '.join(str(-i-1 if bit else i+1) for i,bit in enumerate(g))
          +(' ' if g else '')+'0\n' for g in guards]
    starts=[0]
    for row in rows:starts.append(starts[-1]+len(row))
    def get(i):
        if not 0<=i<len(header)+starts[-1]:return ' '
        if i<len(header):return header[i]
        t=i-len(header);j=bisect.bisect_right(starts,t)-1
        return rows[j][t-starts[j]]
    return header+''.join(rows),get
def case(b,unsat):
    p,q,r,s=b+1,b+2,b+3,b+4
    F=pin(1,p,q)+sum(([(i,r,s),(-i,r,s)] for i in range(2,b+1)),[])
    if unsat:F+=pin(-1,p,q)
    a=[canonical(c) for c in F]
    pos=resolve(resolve(a[0],a[1],q),resolve(a[2],a[3],q),p)
    assert pos==(1,)
    if unsat:
        j=4+2*(b-1)
        neg=resolve(resolve(a[j],a[j+1],q),
                    resolve(a[j+2],a[j+3],q),p)
        assert neg==(-1,) and resolve(pos,neg,1)==()
        guards=[()]
    else:guards=[(0,)]
    output,char_at=child_index(b,guards)
    assert all(char_at(i)==output[i] for i in range(len(output)))
    for v in itertools.product((0,1),repeat=b):
        expected=exists(F,b+4,dict(zip(range(1,b+1),v)))
        actual=all(any(v[i]!=(bit) for i,bit in enumerate(g)) for g in guards)
        assert expected==actual
    return {'b':b,'SAT':not unsat,'source_clauses':len(F),
            'boundary_profiles_verified':2**b,'indexed_characters':len(output)}
def parity(b):
    for t in range(b):
        for prefix in itertools.product((0,1),repeat=t):
            signs={sum(prefix+tail)%2 for tail in
                   itertools.product((0,1),repeat=b-t)}
            assert signs=={0,1}
    return {'b':b,'required_exact_boundary_blockers':2**(b-1)}
def main():
    output={'same_source_both_labels':[case(b,u) for b in range(3,9)
                                      for u in (False,True)],
            'parity_obstruction':[parity(b) for b in range(2,9)],
            'status':'PASS; ARC and P vs NP OPEN'}
    print(json.dumps(output,sort_keys=True,indent=2))
if __name__=='__main__':main()
