#!/usr/bin/env python3
"""LSPV-2/435 finite audit: charge-bit sensitivity and read-footprint nonreuse.
This host-language program is not a native FLMV-machine implementation.
"""
import json, hashlib, itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parent
MAGIC='10100111'

def graphs():
    k4=tuple(itertools.combinations(range(4),2))
    cube=tuple((i,j) for i in range(8) for j in range(i+1,8) if (i^j).bit_count()==1)
    p_edges={(i,(i+1)%5) if i<(i+1)%5 else ((i+1)%5,i) for i in range(5)}
    p_edges.update(tuple(sorted((5+i,5+(i+2)%5))) for i in range(5))
    p_edges.update((i,5+i) for i in range(5))
    return {'K4':(4,tuple(sorted(k4))), 'cube':(8,tuple(sorted(cube))), 'Petersen':(10,tuple(sorted(p_edges)))}

def edge_slots(h,edges):
    assert all(0<=u<v<h for u,v in edges)
    adj=[[] for _ in range(h)]
    for i,(u,v) in enumerate(edges): adj[u].append(i);adj[v].append(i)
    assert all(len(z)==3 for z in adj)
    stack=[0];visited=set()
    while stack:
        v=stack.pop()
        if v in visited: continue
        visited.add(v)
        for i in adj[v]:
            a,b=edges[i];stack.append(b if a==v else a)
    assert len(visited)==h
    return [tuple(sorted(z)) for z in adj]

def make(h,edges,charge):
    slots=edge_slots(h,edges);m=len(edges);w=max(1,m.bit_length()); assert len(charge)==h
    s=MAGIC+'1'*h+'0'+'1'*m+'0'
    s+=''.join(f'{u:0{w}b}{v:0{w}b}' for u,v in edges)
    rows=[]; pivots=[]
    for v,(a,b,c) in enumerate(slots):
        changed=[]
        for p,q in itertools.product((0,1),repeat=2):
            r=p^q^1^charge[v]       # one of four forbidden local parity rows
            clause=((p,a),(q,b),(r,c));rows.append(clause)
            for j,(sign,ei) in enumerate(clause):
                pos=len(s)
                if j==2:changed.append(pos)
                s+=str(sign)+f'{ei:0{w}b}'
        pivots.append(changed)
    s+='00'
    return s,rows,pivots

def clause_satisfied(clause,edge_assignment):
    return any((edge_assignment[ei]^sign)==1 for sign,ei in clause)

def actual_charge(h,edges,assignment):
    c=[0]*h
    for i,(u,v) in enumerate(edges):c[u]^=assignment[i];c[v]^=assignment[i]
    return tuple(c)

def main():
    groups=[];checks=0;fixtures=[]
    for name,(h,edges) in graphs().items():
        m=len(edges);slots=edge_slots(h,edges)
        assert m*2==3*h
        for c in (0,1):
            for a,b,d in slots:
                rows=[((p,a),(q,b),(p^q^1^c,d)) for p,q in itertools.product((0,1),repeat=2)]
                for z in itertools.product((0,1),repeat=3):
                    satisfied=all(clause_satisfied(row,{a:z[0],b:z[1],d:z[2]}) for row in rows)
                    assert satisfied == ((z[0]^z[1]^z[2])==c)
                    checks+=1
        reachable=set()
        for bits in itertools.product((0,1), repeat=m):reachable.add(actual_charge(h,edges,bits));checks+=1
        assert len(reachable)==2**(h-1)
        root,rootrows,rootpos=make(h,edges,(0,)*h)
        allcharges={}; lengths=set()
        for value in range(1<<h):
            charge=tuple((value>>v)&1 for v in range(h))
            s,rows,pivots=make(h,edges,charge);allcharges[charge]=(s,pivots);lengths.add(len(s))
            assert (charge in reachable)==(sum(charge)%2==0)
            for v in range(h):
                flip=list(charge);flip[v]^=1; sf,_,pf=make(h,edges,flip)
                diff={i for i,(a,b) in enumerate(zip(s,sf)) if a!=b}
                assert diff==set(pivots[v])==set(pf[v]) and len(diff)==4
                assert (charge in reachable)!=(tuple(flip) in reachable)
                checks+=1
        assert len(lengths)==1
        # Generic theorem has only one necessary read per vertex; choose any of four.
        # Every distinct charge vector flips the chosen source bit of some vertex.
        for c,(s,pivots) in allcharges.items():
            read_positions=[p[0] for p in pivots]
            assert len(read_positions)==h
            for c2,(s2,_) in allcharges.items():
                same=all(s[p]==s2[p] for p in read_positions)
                assert same==(c==c2)
                checks+=1
        # Reachable charge set from explicit edge valuations is exact certificate for finite graphs.
        # Include a compact original source for external independent replay.
        zeros=(0,)*h; odd=(1,)+(0,)*(h-1)
        for label,chi in [('SAT',zeros),('UNSAT',odd)]:
            source,rows,pivs=make(h,edges,chi)
            fixtures.append({'graph':name,'label':label,'source_bits':source,
                'charge_bits':''.join(map(str,chi)),
                'sha256':hashlib.sha256(source.encode('ascii')).hexdigest()})
        groups.append({'name':name,'vertices':h,'edges':m,'clauses':4*h,
            'encoding_bits':len(root),'num_charge_instances':1<<h,
            'reachable_charge_vectors':len(reachable),'charged_read_lower_bound':h,
            'footprint_cache_hit_count':0,'graph_edges':[list(x) for x in edges]})
    results={'id':'LSPV-2/435','status':'COMPUTATIONAL finite control',
        'encoding':'fixed-width binary proper 3-CNF, separate original graph metadata',
        'theorem':'For any deterministic all-input correct SAT decider, R_A(enc(F_chi)) intersects the four changed sign bit positions D_v for every vertex v. Consequently its read-footprint certificate cannot be reused for any distinct charge vector on the same connected cubic graph.',
        'assertions':checks,'families':groups,'fixtures':fixtures,
        'limitations':['Finite host-language checks do not certify original machine resource bounds',
          'K4, cube and Petersen are not an asymptotic expander family',
          'Read-footprint nonreuse does not imply SAT hardness or failure of algebraic reuse',
          'No fixed R_mix341 native grammar was altered or checked']}
    (ROOT/'lspv2_435_raw.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({'assertions':checks,'groups':groups},indent=2))

if __name__=='__main__':main()
