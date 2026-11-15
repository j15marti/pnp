#!/usr/bin/env python3
"""Independent exhaustive small-graph audit of cut-rank expander 2CNF barrier.
No external dependencies, no randomness. Evaluates a complete assignment relation,
not SAT as a function of formula encodings.
"""
import itertools, json, hashlib

def cube(dim):
    n=1<<dim
    return n, [(u,v) for u in range(n) for v in range(u+1,n) if (u^v).bit_count()==1]

def cycle(n):
    return n, [(i,(i+1)%n) if i<n-1 else (0,n-1) for i in range(n)]

def petersen():
    edges={(min(i,(i+1)%5),max(i,(i+1)%5)) for i in range(5)}
    edges|={(min(i,i+5),max(i,i+5)) for i in range(5)}
    edges|={(min(i+5,((i+2)%5)+5),max(i+5,((i+2)%5)+5)) for i in range(5)}
    return 10,sorted(edges)

def rank(rows):
    pivots={}
    for mask in rows:
        while mask:
            p=mask.bit_length()-1
            if p not in pivots:
                pivots[p]=mask
                break
            mask^=pivots[p]
    return len(pivots)

def matrix_rows(n,edges,left):
    right=[i for i in range(n) if i not in left]
    rows=[]
    for a in range(1<<len(left)):
        mask=0
        for b in range(1<<len(right)):
            values=[0]*n
            for j,v in enumerate(left): values[v]=(a>>j)&1
            for j,v in enumerate(right): values[v]=(b>>j)&1
            if not any(values[u] and values[v] for u,v in edges): mask|=1<<b
        rows.append(mask)
    return rows

def find_greedy_induced(n, edges,left):
    cut=[(u,v) for u,v in edges if ((u in left)!=(v in left))]
    neighbors=[set() for _ in range(n)]
    for u,v in edges: neighbors[u].add(v);neighbors[v].add(u)
    remain=cut[:]; chosen=[]
    while remain:
        u,v=remain[0];chosen.append((u,v))
        closed={u,v}|neighbors[u]|neighbors[v]
        remain=[(a,b) for a,b in remain if a not in closed and b not in closed]
    endpoints=[q for e in chosen for q in e]
    assert len(endpoints)==len(set(endpoints))
    for i,(u,v) in enumerate(chosen):
        for x,y in chosen[i+1:]:
            assert (x not in neighbors[u] and y not in neighbors[u] and x not in neighbors[v] and y not in neighbors[v])
    return len(chosen),len(cut)

def audit(name,gen):
    n,edges=gen
    edges=sorted({tuple(sorted(e)) for e in edges})
    d=max(sum((v==u or w==u) for v,w in edges) for u in range(n))
    total=0;minrank=10**10;minr=10**10;maxrank=0;minratio=10**20
    rankhist={}; tight=0; bad=0; mincut=999
    for size in range((n+2)//3,(2*n)//3+1):
        for positions in itertools.combinations(range(n),size):
            if 0 not in positions: continue
            left=set(positions)
            rr=rank(matrix_rows(n,edges,positions))
            im,cross=find_greedy_induced(n,edges,left)
            assert rr >= 2**im, (name,positions,rr,im)
            total+=1
            minrank=min(minrank,rr);maxrank=max(maxrank,rr);minr=min(minr,im)
            mincut=min(mincut,cross)
            if rr==2**im:tight+=1
            rankhist[rr]=rankhist.get(rr,0)+1
            if rr != 0 and cross: minratio=min(minratio,rr/(2**im))
    return {"graph":name,"vertices":n,"edges":len(edges),"max_degree":d,"balanced_cuts_checked_up_to_transpose":total,"minimum_cross_edges":mincut,"minimum_greedy_induced_matching":minr,"minimum_cut_matrix_rank_GF2":minrank,"maximum_cut_matrix_rank_GF2":maxrank,"rank_histogram":dict(sorted(rankhist.items())),"matching_rank_tight_cuts":tight,"failures":bad}

if __name__=='__main__':
    data=[audit('cycle_6',cycle(6)),audit('cube_Q3',cube(3)),audit('petersen_10',petersen())]
    assert rank([0b11,0b01])==2
    obj={"test":"TMR-5/046 every-balanced-cut IS-CNF GF2 rank vs induced-matching bound","mode":"exhaustive all balanced bipartitions up to complement, direct row enumeration, GF(2) elimination","random_seed":None,"graphs":data,"failures":sum(g['failures'] for g in data),"limitations":"finite graphs not proof of uniform expander theorem; zero-all SAT witness and linear Horn/2CNF upper; full-assignment matrix not formula-encoding SAT decision; symbolic induced-matching argument holds all fields"}
    print(json.dumps(obj,indent=2,sort_keys=True))
