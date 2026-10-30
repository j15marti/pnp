#!/usr/bin/env python3
"""Separate width-two and affine controls, not silently relabeled as proper 3CNF."""
import itertools,json

def sat(F,a):return all(any(a[abs(z)] == (z>0) for z in c) for c in F)
def two_sat_scc(F,n):
    def key(l):return (abs(l)-1)*2+(0 if l>0 else 1)
    E={i:[] for i in range(2*n)}
    for cid,(u,v) in enumerate(F,1):
        E[key(-u)].append((key(v),cid));E[key(-v)].append((key(u),cid))
    def reach(start):
        seen={start};q=[start]
        for v in q:
            for u,_ in E[v]:
                if u not in seen:seen.add(u);q.append(u)
        return seen
    conflict=[i for i in range(1,n+1) if key(-i) in reach(key(i)) and key(i) in reach(key(-i))]
    return not bool(conflict),conflict,E

def run():
    sources={'2SAT_sat':((1,2),(-1,2),(1,-2)), '2SAT_unsat':((1,2),(-1,2),(1,-2),(-1,-2))}
    out={}
    for name,F in sources.items():
        models=[]
        for x,y in itertools.product((False,True),repeat=2):
            a={1:x,2:y}
            if sat(F,a):models.append([int(x),int(y)])
        ans,conflict,edges=two_sat_scc(F,2)
        assert ans==bool(models)
        out[name]={'width':2,'separate_descendant_or_control':True,'source_clauses':F,'SAT':ans,'models':models,'SCC_opposite_reach_conflict_variables':conflict,'source_indexed_implication_edges':{str(i):E for i,E in edges.items()},'complete_assignments_checked':4}
    # All four clauses of parity3 encode exactly one rank-one GF(2) equation.
    for b in (0,1):
        C=[]
        for vals in itertools.product((0,1),repeat=3):
            if sum(vals)%2==b:continue
            C.append(tuple(-(i+1) if vals[i] else i+1 for i in range(3)))
        for vals in itertools.product((0,1),repeat=3):
            a={i+1:bool(vals[i]) for i in range(3)}
            assert sat(C,a)==((sum(vals)%2)==b)
        out['XOR3_parity_'+str(b)]={'width':3,'signed_clauses':C,'affine_GF2_equation':'x1 xor x2 xor x3 = '+str(b),'rank':1,'codimension':1,'complete_assignments_checked':8}
    with open('CONNECTED_LOG_FLIPS247_2sat_affine_controls.json','w') as f:json.dump(out,f,indent=2)
    print('PASS distinct 2SAT SCC SAT/UNSAT and GF(2) parity controls')
if __name__=='__main__':run()