#!/usr/bin/env python3
"""TMR-2/094: original-source and independent-query controls; Python stdlib."""
from functools import lru_cache
from itertools import product
import json
from tmr2_t5_cycle_syndrome093_compact import theta, count_dp

def bad(z,positive):
    return (not bool(z[0])) if positive else bool(z[0])

def cnf_family(q,positive_second):
    # Each block ((C or y) and (C or not y)) projects exactly to C.
    counts=[0,0]
    for z in product((0,1),repeat=q):
        cover=(bad(z,True) or bad(z,positive_second))
        counts[int(cover)]+=1
        for p in (True,positive_second):
            c=not bad(z,p)
            assert all(((c or y) and (c or (not y)))==c for y in (0,1))
    return counts

def decision_depth(rows,cols):
    @lru_cache(None)
    def go(state):
        for i in range(rows):
            row=state[i*cols:(i+1)*cols]
            if 1 not in row and -1 not in row:
                return 0
        if all(1 in state[i*cols:(i+1)*cols] for i in range(rows)):
            return 0
        return 1+min(max(go(state[:i]+(b,)+state[i+1:]) for b in (0,1))
                     for i,x in enumerate(state) if x==-1)
    return go((-1,)*(rows*cols)),go.cache_info().currsize

def direct_t5(n,edges):
    count=0
    for a in product(range(5),repeat=n):
        bad_arc=next((i for i,(u,v) in enumerate(edges)
                      if (a[v]-a[u])%5 not in (1,3)),None)
        if bad_arc is None: count+=1
        else:
            u,v=edges[bad_arc]
            assert (a[v]-a[u])%5 not in (1,3)
    assert count==count_dp(n,edges)[0]
    return count

def main():
    for q in range(1,9):
        assert cnf_family(q,False)==[0,2**q]
        assert cnf_family(q,True)==[2**(q-1),2**(q-1)]
    depths=[(r,c,*decision_depth(r,c)) for r,c in ((2,2),(2,3),(4,2))]
    assert [x[2] for x in depths]==[4,6,8]
    no=((1,1),(1,1,1),(1,1,-1),(-1,-1,-1))
    n,E=theta(no)
    EY=[(v,u) if i==0 else (u,v) for i,(u,v) in enumerate(E)]
    trans=[(i,j) for i in range(4) for j in range(i+1,4)]
    induced=[(i,j) if ((j-i)%5 in (1,3)) else (j,i) for i,j in trans]
    cases=[(n,E),(n,EY),(4,trans),(4,induced)]
    counts=[direct_t5(num,edges) for num,edges in cases]
    assert counts==[0,135,0,5],counts
    print(json.dumps({'revision':'TMR2_094_SCOPED','cnf_family_q_max':8,
         'query_decision_depths':depths,'T5_original_counts':counts,
         'status':'COMPUTATIONAL finite checks; P versus NP OPEN'},sort_keys=True))
if __name__=='__main__': main()
