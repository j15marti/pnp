#!/usr/bin/env python3
"""ARC-SIGNED-SPILL294 compact source-authenticated certificate runner.
Replays source grammar, UP, dynamically acquired spill, and greedy odd cycles.
Produces NO only with an original-clause proof; otherwise UNRESOLVED.
The full independent exhaustive audit and XOR source are in reproducibility ZIP.
"""
from collections import Counter,defaultdict,deque
import itertools,json
F=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),
   (7,11,13),(8,12,14),(9,13,15),(10,14,15),
   (-1,-2,-11),(-2,-3,-11),(-1,-3,-12),(-4,-5,-13),
   (-5,-6,-14),(-4,-6,-15),(-7,-8,-12),(-8,-9,-13),
   (-9,-10,-14),(-10,-7,-15))
U=(-1,)*6+(0,0,0,0,1,1,1,1,0)
S=(-1,)*6+(1,0,0,0,1,1,1,1,0)

def valid(G,n):
    tally=Counter();seen=set()
    if n%3 or len(G)*3!=4*n:return False
    for c in G:
        if len(c)!=3 or len(set(map(abs,c)))!=3:return False
        if min(map(abs,c))<1 or max(map(abs,c))>n:return False
        if not (all(x>0 for x in c) or all(x<0 for x in c)):return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key);tally.update(c)
    return all(tally[x]==tally[-x]==2 for x in range(1,n+1))

def simplify(G,p,ledger):
    uncovered=[];covered=[]
    for j,c in enumerate(G,1):
        ledger['clause_scans']+=1;ledger['literal_reads']+=3
        if any(p[abs(l)-1]==int(l>0) for l in c):covered.append(j)
        else:uncovered.append((j,tuple(l for l in c if p[abs(l)-1]<0)))
    return uncovered,covered

def propagate(G,p,ledger):
    p=list(p)
    while True:
        R,covered=simplify(G,p,ledger)
        if any(len(c)==0 for _,c in R):return tuple(p),R,covered,False
        units=[c[0] for _,c in R if len(c)==1]
        if not units:return tuple(p),R,covered,True
        for lit in units:
            x=abs(lit)-1; val=int(lit>0)
            if p[x] not in (-1,val):return tuple(p),R,covered,False
            if p[x]==-1:p[x]=val;ledger['UP_assignments']+=1

def oddcycle(E,ledger):
    adj=defaultdict(list)
    for j,x,y in E:adj[x].append((y,j));adj[y].append((x,j))
    color={};par={};pe={}
    for root in sorted(adj):
        if root in color:continue
        color[root]=0;par[root]=None;queue=deque([root])
        while queue:
            x=queue.popleft()
            for y,j in adj[x]:
                ledger['graph_incidence_reads']+=1
                if y not in color:
                    color[y]=1-color[x];par[y]=x;pe[y]=j;queue.append(y)
                elif color[x]==color[y]:
                    A=[];u=x
                    while u is not None:A.append(u);u=par[u]
                    B=[];u=y
                    while u is not None:B.append(u);u=par[u]
                    common=next(u for u in B if u in A)
                    seq=A[:A.index(common)+1]+list(reversed(B[:B.index(common)]))
                    edgeids=[]
                    for a,b in zip(seq,seq[1:]):edgeids.append(pe[a] if par[a]==b else pe[b])
                    edgeids.append(j)
                    assert len(edgeids)%2==1 and len(edgeids)>=3
                    return {'clause_ids':edgeids,'vertices':seq+[x]}
    return None

def gate(G,p):
    ledger=Counter()
    if not valid(G,len(p)):
        return {'result':'REJECT_MALFORMED','ledger':dict(ledger)}
    ledger['grammar_clause_reads']+=len(G);ledger['grammar_literal_reads']+=3*len(G)
    rho,R,covered,stable=propagate(G,p,ledger)
    if not stable:return {'result':'UNSAT','rule':'UP','ledger':dict(ledger)}
    f=rho.count(-1);u=len(R);e=2*f-u;r3=sum(len(c)==3 for j,c in R)
    covered_count=Counter()
    for j in covered:
        ledger['spill_clause_reads']+=1;ledger['spill_literal_reads']+=3
        for lit in G[j-1]:
            if rho[abs(lit)-1]<0:covered_count[lit]+=1
    eta=sum(min(covered_count[x],covered_count[-x]) for x in range(1,len(p)+1) if rho[x-1]<0)
    Delta=sum(abs(covered_count[x]-covered_count[-x]) for x in range(1,len(p)+1) if rho[x-1]<0)
    assert 2*(e-eta)==r3+Delta
    edges=[(j,abs(c[0]),abs(c[1])) for j,c in R if len(c)==2]
    cycles=[]
    while len(cycles)<=e-eta:
        z=oddcycle(edges,ledger)
        if z is None:break
        cycles.append(z); ids=set(z['clause_ids'])
        edges=[edge for edge in edges if edge[0] not in ids]
    return {'result':'UNSAT' if len(cycles)+eta>e else 'UNRESOLVED',
            'rule':'signed_spill_cycle_budget','p_after_UP':rho,'e':e,
            'eta':eta,'r3':r3,'Delta':Delta,'cycles':cycles,
            'original_residual':R,'ledger':dict(ledger)}

def models(G,p):
    variables=[i for i,x in enumerate(p) if x<0]
    for bit in itertools.product((0,1),repeat=len(variables)):
        a=list(p)
        for i,v in zip(variables,bit):a[i]=v
        if all(any(a[abs(l)-1]==int(l>0) for l in c) for c in G):yield tuple(a)

def main():
    assert valid(F,15)
    assert not valid(F+F[:1],15) and not valid(F[:-1],15)
    result={}
    for label,p in (('UNSAT',U),('SAT',S)):
        r=gate(F,p); w=next(models(F,p),None)
        assert (w is None)==(label=='UNSAT')
        assert r['result']==('UNSAT' if label=='UNSAT' else 'UNRESOLVED')
        assert (r['e'],r['eta'],len(r['cycles']),r['r3'])==((2,1,2,1) if label=='UNSAT' else (3,1,2,1))
        result[label]={'decision':label,'gate':r['result'],'e':r['e'],
            'eta':r['eta'],'nu_cert':len(r['cycles']), 'r3':r['r3'],
            'cycles':r['cycles'],'witness':w,'paid_proxy':r['ledger']}
    print(json.dumps({'status':'PASS','source':'one valid connected 15-variable canonical F',
        'paired_partial_source_bit_flip':'x7','results':result,
        'scope':'finite proof replay; no native FLMV resources or global ARC bound'},sort_keys=True,indent=2))
if __name__=='__main__':main()
