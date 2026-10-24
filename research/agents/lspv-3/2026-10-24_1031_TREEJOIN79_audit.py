#!/usr/bin/env python3
"""LSPV-3 TREEJOIN79: deterministic exact forest-CSP / SAT controls.
No third-party dependencies; runs in under 30s. Output is machine-readable JSON.
"""
import json, itertools, time, hashlib, pathlib
OUT=pathlib.Path(__file__).resolve().parent/'TREEJOIN79_raw.json'
checks=0

def verify(cond,detail='assertion'):
    global checks
    checks+=1
    if not cond: raise AssertionError(detail)

def add_xor3_odd(clauses, v):
    ids=[3*v+c+1 for c in range(3)]
    for bits in itertools.product((0,1),repeat=3):
        if sum(bits)%2==0:
            clauses.append(tuple(-ids[j] if bits[j] else ids[j] for j in range(3)))

def mixed_formula(q, edges, second_pin):
    # Each component has one XOR3=1 and three local NAND clauses.
    # Difference between the two labels is the sign of exactly one unit.
    c=[]
    for v in range(q):
        add_xor3_odd(c,v)
        ids=[3*v+j+1 for j in range(3)]
        c.extend([(-ids[0],-ids[1]),(-ids[0],-ids[2]),(-ids[1],-ids[2])])
    for u,v in edges:
        for j in range(3): c.append((-(3*u+j+1),-(3*v+j+1)))
    c.append((1,))
    c.append((4 if second_pin else -4,))
    return c

def evaluate(clauses,assignment):
    return all(any((assignment[abs(x)-1] if x>0 else not assignment[abs(x)-1]) for x in cl) for cl in clauses)

def brute_cnf(clauses,n):
    for a in itertools.product((False,True),repeat=n):
        if evaluate(clauses,a): return True,a
    return False,None

def threecolor(q,edges,second_pin):
    for colors in itertools.product(range(3),repeat=q):
        if colors[0]!=0:continue
        if ((colors[1]==0) != bool(second_pin)):continue
        if all(colors[u]!=colors[v] for u,v in edges):return True,colors
    return False,None

def forest_dp(q,edges,second_pin):
    adj=[[] for _ in range(q)];parent=list(range(q))
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]];x=parent[x]
        return x
    for u,v in edges:
        assert 0<=u<q and 0<=v<q and u!=v
        if find(u)==find(v):return {'forest':False}
        parent[find(u)]=find(v)
        adj[u].append(v);adj[v].append(u)
    seen=set(); feasible=[[False]*3 for _ in range(q)]
    parent_node=[-1]*q;roots=[];order=[]
    for root in range(q):
        if root in seen:continue
        roots.append(root)
        seen.add(root);stack=[root]
        while stack:
            v=stack.pop();order.append(v)
            for u in adj[v]:
                if u==parent_node[v]:continue
                if u in seen: raise AssertionError('bad DFS parent')
                seen.add(u);parent_node[u]=v;stack.append(u)
    local_tests=0;compat_tests=0
    for v in reversed(order):
        for color in range(3):
            local_tests+=1
            ok=(v!=0 or color==0) and (v!=1 or (color==0)==bool(second_pin))
            if ok:
                for u in adj[v]:
                    if parent_node[u]!=v:continue
                    support=False
                    for d in range(3):
                        compat_tests+=1
                        if color!=d and feasible[u][d]:support=True
                    if not support:ok=False;break
            feasible[v][color]=ok
    sat=all(any(feasible[root]) for root in roots)
    witness=None
    if sat:
        colors=[None]*q
        for root in roots:
            colors[root]=next(c for c in range(3) if feasible[root][c])
            stack=[root]
            while stack:
                v=stack.pop()
                for u in adj[v]:
                    if parent_node[u]==v:
                        colors[u]=next(c for c in range(3) if feasible[u][c] and c!=colors[v])
                        stack.append(u)
        witness=tuple(colors)
    return {'forest':True,'sat':sat,'witness':witness,'local_tests':local_tests,
            'compat_tests':compat_tests,'components':len(roots),'max_domain':3}

def properize(clauses,n):
    out=[];new_n=n
    for cl in clauses:
        if len(cl)==3:out.append(cl)
        elif len(cl)==2:
            new_n+=1;t=new_n
            out.extend((tuple(cl)+(t,),tuple(cl)+(-t,)))
        elif len(cl)==1:
            new_n+=2;a,b=new_n-1,new_n
            for x,y in itertools.product((1,-1),repeat=2):
                out.append((cl[0],x*a,y*b))
        else:raise ValueError('bad clause width')
    return out,new_n

def check_small_gadgets():
    for vals in itertools.product((False,True),repeat=2):
        base=(vals[0] or vals[1])
        gadget=all(any((vals[0],vals[1],t)) for t in (True,False))
        verify(base==gadget,'binary gadget')
    for lit in (False,True):
        # Test a four-clause unit gadget for each aux assignment.
        for a,b in itertools.product((False,True),repeat=2):
            conj=all(lit or (a if sa==1 else not a) or (b if sb==1 else not b) for sa,sb in itertools.product((1,-1),repeat=2))
            verify(conj==lit,'unit gadget')

def path(q):return [(i,i+1) for i in range(q-1)]
def star(q):return [(0,i) for i in range(1,q)]

def run():
    check_small_gadgets()
    stats={'exhaustive':[], 'larger':[], 'nonforest_controls':[]}
    for q in range(2,5):
        for structure,edges in [('path',path(q)),('star',star(q))]:
            for bit in (0,1):
                c=mixed_formula(q,edges,bit);result=forest_dp(q,edges,bit)
                actual,wit=brute_cnf(c,3*q)
                ct,col=threecolor(q,edges,bit)
                verify(result['forest'] and result['sat']==actual==ct,'small SAT label')
                if result['sat']:
                    verify(result['witness'] is not None,'missing DP witness')
                    onehot=tuple(i==color for color in result['witness'] for i in range(3))
                    verify(evaluate(c,onehot),'replayed witness')
                verify(result['local_tests']==3*q,'local tests')
                if structure=='path':
                    verify(len(c)==10*q-1,'mixed clause count')
                    three,nprime=properize(c,3*q)
                    verify(nprime==9*q+1 and len(three)==16*q+2,'proper encoding counts')
                    verify(all(len(k)==3 and len(set(abs(x) for x in k))==3 for k in three),'proper clauses')
                    # Witness lifting: set all fresh auxiliary values False.
                    if result['sat']:
                        assignment=list(onehot)+[False]*(nprime-3*q)
                        verify(evaluate(three,assignment),'proper witness lifting')
                stats['exhaustive'].append({'q':q,'shape':structure,'second_pin':bit,
                                             'sat':actual,'dp_local':result['local_tests'],
                                             'dp_pairs':result['compat_tests']})
    for q in (8,64,512,1024):
        for structure,edges in [('path',path(q)),('star',star(q))]:
            for bit in (0,1):
                c=mixed_formula(q,edges,bit)
                ans=forest_dp(q,edges,bit)
                verify(ans['forest'] and ans['sat']==(bit==0),'scalable label')
                verify(ans['local_tests']==3*q,'scalable local count')
                verify(ans['compat_tests']<=9*(q-1),'scalable compatibility bound')
                if ans['sat']:
                    witness=tuple(i==color for color in ans['witness'] for i in range(3))
                    verify(evaluate(c,witness),'scalable source replay')
                stats['larger'].append({'q':q,'shape':structure,'second_pin':bit,
                                        'sat':ans['sat'],'local':ans['local_tests'],
                                        'pairs':ans['compat_tests'], 'clauses':len(c)})
    for edges in [[(0,1),(1,2),(2,0)],[(0,1),(1,2),(2,3),(3,0)],
                  [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]]:
        q=max(max(e) for e in edges)+1
        for bit in (0,1):
            verify(not forest_dp(q,edges,bit)['forest'],'cycle falsely recognized')
            sat,_=threecolor(q,edges,bit)
            stats['nonforest_controls'].append({'vertices':q,'edges':len(edges),'second_pin':bit,'sat':sat,'forest_recognized':False})
    # Independent-forest partial pin control: connectedness not assumed.
    for bit in (0,1):
        edges=[(0,1),(2,3)]
        ans=forest_dp(4,edges,bit)
        verify(ans['forest'] and ans['components']==2 and ans['sat']==(bit==0),'disconnected control')
    stats['assertions']=checks
    return stats
if __name__=='__main__':
    start=time.time();r=run();r['elapsed_seconds']=round(time.time()-start,4)
    r['algorithm']='TREEJOIN79 forest message passing; original onehot XOR3 + NAND encoded CNF'
    r['random_seed']=None
    OUT.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'assertions':r['assertions'],'elapsed_seconds':r['elapsed_seconds'],
                      'exhaustive_count':len(r['exhaustive']),'large_count':len(r['larger']),
                      'nonforest_count':len(r['nonforest_controls']),'raw_path':str(OUT)},indent=2))
