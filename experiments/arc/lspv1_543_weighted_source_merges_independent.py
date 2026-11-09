#!/usr/bin/env python3
"""Independent partition-state Dijkstra and knapsack controls for LSPV-1/543.
Only a declared MAY abstraction: never an execution of the historical checker.
"""
import itertools, json, heapq

def dp_m(m, types):
    d=[0]+[float('inf')]*(m-1)
    for k in range(2,m+1):
        d[k-1]=min(c+d[max(1,k-min(r,k)+1)-1] for r,c in types if r>=2)
    return d[-1]

def knapsack(m,types):
    d=[float('inf')]*m; d[0]=0
    for p in range(1,m):
        d[p]=min(c+d[max(0,p-(r-1))] for r,c in types if r>=2)
    return d[-1]

def merge(part,indices):
    rest=[]; union=set()
    for i,b in enumerate(part):
        if i in indices: union.update(b)
        else: rest.append(b)
    rest.append(tuple(sorted(union)))
    return tuple(sorted(tuple(x) for x in rest))

def explicit_search(m,types):
    initial=tuple((i,) for i in range(m))
    best={initial:0}; pq=[(0,initial)]; expanded=0
    while pq:
        d,state=heapq.heappop(pq)
        if d!=best[state]: continue
        expanded+=1
        if len(state)==1: return d,expanded,len(best)
        for r,c in types:
            for size in range(2,min(r,len(state))+1):
                for subset in itertools.combinations(range(len(state)),size):
                    t=merge(state,subset); nd=d+c
                    if nd<best.get(t,float('inf')):
                        best[t]=nd; heapq.heappush(pq,(nd,t))
    raise ValueError('unreachable')

def main():
    configurations=[
        [(2,1)],[(2,1),(3,2)],[(2,1),(4,1)],[(3,2)],
        [(4,0),(2,1)],[(2,3),(3,1)],[(2,2),(3,4),(4,3)]
    ]
    rows=[]; checks=0
    for types in configurations:
        for m in range(2,7):
            a=dp_m(m,types); b=knapsack(m,types)
            c,expanded,states=explicit_search(m,types)
            assert a==b==c,(m,types,a,b,c); checks+=1
            rho=min(w/(r-1) for r,w in types)
            assert (m-1)*rho-1e-8<=a; checks+=1
            assert a<=(m-1)*rho+min(w for r,w in types if w/(r-1)==rho)+1e-8; checks+=1
            rows.append({'m':m,'types':types,'exact':a,'states':states,'expanded':expanded})
    print(json.dumps({'run':'LSPV-1/543','status':'COMPUTATIONAL','configurations':len(configurations),'instances':len(rows),'assertion_groups':checks,'all_pass':True,'cases':rows},indent=2))

if __name__=='__main__':main()
