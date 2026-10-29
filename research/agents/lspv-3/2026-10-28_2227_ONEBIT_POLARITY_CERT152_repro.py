#!/usr/bin/env python3
"""LSPV-3 ONEBIT-POLARITY-CERT152: exact source-ID projection and proof audit.
No external packages. Run: python3 2026-10-28_2227_ONEBIT_POLARITY_CERT152_repro.py
All algorithmic claims here are restricted to the explicit source construction.
"""
from __future__ import annotations
import collections
import copy
import itertools
import json
import random
from pathlib import Path

C = collections.Counter()

def require(pred, why):
    C['assertions'] += 1
    if not pred: raise AssertionError(why)

def source_valid(F,n):
    return all(len(c)==3 and len({abs(v) for v in c})==3 and all(1<=abs(v)<=n for v in c) for c in F)

def sat_clause(c, env):
    return any(env[abs(l)] == (l>0) for l in c)

def source_sat(F,n):
    for bits in itertools.product((False,True), repeat=n):
        env={v+1:bits[v] for v in range(n)}
        if all(sat_clause(c,env) for c in F): return env
    return None

def lift(F,n):
    if not F or not source_valid(F,n):raise ValueError('requires nonempty proper ternary F')
    y=n+1
    G=[]
    for i,(a,b,c) in enumerate(F):
        t=n+2+i
        G.extend([(-y,a,t),(-t,b,c)])
    return tuple(G),y

def verify_lift(G,n):
    if not G or len(G)%2:raise ValueError('malformed pairs')
    y=n+1; F=[]
    for i in range(len(G)//2):
        l,r=G[2*i],G[2*i+1]
        t=n+2+i
        if len(l)!=3 or len(r)!=3 or l[0]!=-y or l[2]!=t or r[0]!=-t:
            raise ValueError('source IDs / pivot / polarity mismatch')
        a,b,c=l[1],r[1],r[2]
        if len({abs(a),abs(b),abs(c)})!=3 or any(abs(q)>n or q==0 for q in (a,b,c)):
            raise ValueError('not proper original ternary')
        F.append((a,b,c))
    return tuple(F),y

def direct_relation(G,n):
    m=len(G)//2; y=n+1
    out=[False,False]
    for word in range(1<<(n+m)):
        env={i+1:bool(word>>(i)&1) for i in range(n)}
        env.update({n+2+i:bool(word>>(n+i)&1) for i in range(m)})
        for ybit in (0,1):
            if out[ybit]:continue
            env[y]=bool(ybit)
            if all(sat_clause(c,env) for c in G):out[ybit]=True
        if all(out):break
    return tuple(out)

def lift_witness(F,n,source_witness, ybit):
    y=n+1
    if ybit==1 and source_witness is None:raise ValueError('no positive witness')
    env={j:False for j in range(1,n+1)} if ybit==0 else dict(source_witness)
    env[y]=bool(ybit)
    for i,(a,b,c) in enumerate(F):
        # If y=1 and a false, t=1 forces b or c true by the F witness.
        env[n+2+i]=(ybit==1 and not sat_clause((a,),env))
    return env

def simplify(F,env):
    clauses=[]
    for j,c in enumerate(F,1):
        if any(abs(l) in env and env[abs(l)]==(l>0) for l in c):continue
        r=tuple(l for l in c if abs(l) not in env)
        clauses.append((j,r))
    return clauses

def graph_from_residual(res):
    graph=collections.defaultdict(list)
    empty=[]
    for source_id,c in res:
        if not c:empty.append(source_id)
        elif len(c)==1:
            l=c[0];graph[-l].append((l,source_id))
        elif len(c)==2:
            a,b=c;graph[-a].append((b,source_id));graph[-b].append((a,source_id))
        else:raise AssertionError('not 2CNF')
    return graph,empty

def path(graph,s,t):
    q=collections.deque([s]);prev={s:None}
    while q:
        v=q.popleft()
        if v==t:break
        for w,source_id in graph[v]:
            if w not in prev:
                prev[w]=(v,source_id);q.append(w)
    if t not in prev:return None
    result=[];v=t
    while v!=s:
        u,source_id=prev[v];result.append([u,v,source_id]);v=u
    return list(reversed(result))

def contradiction_leaf(F,env,remain):
    res=simplify(F,env)
    graph,empties=graph_from_residual(res)
    if empties:return {'type':'empty','id':empties[0]}
    for var in remain:
        p=path(graph,var,-var);q=path(graph,-var,var)
        if p is not None and q is not None:
            return {'type':'scc','var':var,'paths':[p,q]}
    return None

def make_tree(F,n):
    if n<2:raise ValueError('n >= 2')
    def go(i,env):
        if i>n-2:
            leaf=contradiction_leaf(F,env,(n-1,n))
            if leaf is None:raise ValueError('source SAT; no UNSAT certificate exists')
            return leaf
        left=go(i+1,{**env,i:False})
        right=go(i+1,{**env,i:True})
        return {'type':'branch','var':i,'zero':left,'one':right}
    return go(1,{})

def check_tree(G,n,tree,node_budget=100000):
    try:F,y=verify_lift(G,n)
    except ValueError:return False
    budget=[node_budget]
    def go(node,i,env):
        budget[0]-=1
        if budget[0]<0:return False
        if not isinstance(node,dict) or 'type' not in node:return False
        if i<=n-2:
            if node.get('type')!='branch' or node.get('var')!=i or set(node)!={'type','var','zero','one'}:return False
            return go(node['zero'],i+1,{**env,i:False}) and go(node['one'],i+1,{**env,i:True})
        res=simplify(F,env)
        graph,empties=graph_from_residual(res)
        if node.get('type')=='empty':
            return set(node)=={'type','id'} and node.get('id') in empties
        if node.get('type')!='scc' or set(node)!={'type','var','paths'}:return False
        var=node.get('var')
        if var not in (n-1,n):return False
        p=node.get('paths')
        if not isinstance(p,list) or len(p)!=2:return False
        for s,t,steps in ((var,-var,p[0]),(-var,var,p[1])):
            if not isinstance(steps,list) or not steps:return False
            at=s
            for e in steps:
                if not isinstance(e,list) or len(e)!=3:return False
                u,v,source=e
                if u!=at or (v,source) not in graph.get(u,[]):return False
                at=v
            if at!=t:return False
        return True
    try:return go(tree,1,{})
    except (KeyError,TypeError,IndexError,RecursionError):return False

def positive_certificate(F,n):
    w=source_sat(F,n)
    if w is None:return None
    return lift_witness(F,n,w,1)

def check_positive(G,n,w):
    try:
        F,y=verify_lift(G,n)
        return isinstance(w,dict) and set(w)==set(range(1,n+len(F)+2)) and w[y] is True and all(sat_clause(c,w) for c in G)
    except (KeyError,ValueError,TypeError):return False

def test_crossproducts():
    count=0
    for t in range(1,5):
        for word in range(1<<(4*t)):
            a=[bool(word>>(2*i)&1) or bool(word>>(2*i+1)&1) for i in range(t)]
            b=[bool(word>>(2*t+2*i)&1) or bool(word>>(2*t+2*i+1)&1) for i in range(t)]
            expansion=all(x or y for x in a for y in b)
            compact=all(a) or all(b)
            original=any(all(z or x for x in a) and all((not z) or y for y in b) for z in (False,True))
            require(original==expansion==compact,'cross-product projection')
            count+=1
    return count

def exact22_controls():
    U=tuple(tuple(map(int,r.split())) for r in ('-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14').split(';'))
    S=tuple(tuple(map(int,r.split())) for r in '-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14'.split(';'))
    labels={}
    control_tree_stats={}
    for name,F in [('U',U),('S',S)]:
        occ=collections.Counter(l for c in F for l in c)
        require(source_valid(F,15) and len(F)==20,'control proper')
        require(all(occ[i]==occ[-i]==2 for i in range(1,16)),'control exact22')
        w=source_sat(F,15)
        labels[name]='SAT' if w is not None else 'UNSAT'
        G,y=lift(F,15)
        require(verify_lift(G,15)[0]==F,'authentic lift')
        if w is not None:
            require(check_positive(G,15,lift_witness(F,15,w,1)),'source SAT witness')
        else:
            proof=make_tree(F,15)
            require(check_tree(G,15,proof),'strict exact22 source original-clause SCC refutation')
            def count(x):
                if x['type']=='branch':
                    a=count(x['zero']);b=count(x['one']);return (a[0]+b[0],a[1]+b[1],a[2]+b[2])
                return (1,int(x['type']=='scc'),int(x['type']=='empty'))
            leaf_count,scc_count,empty_count=count(proof)
            require(leaf_count==8192,'complete depth thirteen tree')
            control_tree_stats[name]={'depth':13,'leaves':leaf_count,'scc_leaves':scc_count,'empty_source_clauses':empty_count,'encoded_json_bytes':len(json.dumps(proof))}
            # Mutate a source clause in the G encoding; authentication must fail.
            damaged=list(G);damaged[0]=(damaged[0][0],-damaged[0][1],damaged[0][2])
            require(not check_tree(tuple(damaged),15,proof),'tampered source detected')
    return labels,control_tree_stats

def main():
    n=3
    patterns=tuple(tuple(i+1 if (mask>>i)&1 else -(i+1) for i in range(n)) for mask in range(1<<n))
    boundary_counts=collections.Counter()
    input_count=0
    for mask in range(1,1<<len(patterns)):
        F=tuple(patterns[i] for i in range(len(patterns)) if mask>>i&1)
        G,y=lift(F,n)
        decoded,y2=verify_lift(G,n)
        require(F==decoded and y==y2,'source-authentication')
        relation=direct_relation(G,n)
        truth=source_sat(F,n) is not None
        require(relation==(True,truth),'one-bit exact projection')
        boundary_counts['top' if truth else 'neg_y']+=1
        if truth:
            w=positive_certificate(F,n)
            require(check_positive(G,n,w),'positive certificate')
            bad=dict(w);bad[y]=False
            require(not check_positive(G,n,bad),'corrupt SAT witness rejected')
            if len(F)<=4:
                try:make_tree(F,n)
                except ValueError:pass
                else:raise AssertionError('positive input admitted negative proof')
        else:
            negative_tree=make_tree(F,n)
            require(check_tree(G,n,negative_tree),'UNSAT tree checked')
            bad=copy.deepcopy(negative_tree)
            del bad['one']
            require(not check_tree(G,n,bad),'incomplete coverage rejected')
            bad=copy.deepcopy(negative_tree)
            # Corrupt an original clause source ID, not merely tree geometry.
            leaf=bad['zero']
            if leaf['type']=='scc':leaf['paths'][0][0][2]=len(F)+10
            else:leaf['id']=len(F)+10
            require(not check_tree(G,n,bad),'invalid original-clause ID rejected')
            require(not check_tree(G,n,negative_tree,node_budget=1),'explicit timeout rejected')
            require(not check_positive(G,n,None),'false positive rejected')
        input_count+=1
    rng=random.Random(202610282227)
    n4cases=0
    for j in range(200):
        n=4;m=rng.randint(1,8)
        F=tuple(tuple(sign*v for v,sign in zip(rng.sample(range(1,n+1),3),rng.choices((-1,1),k=3))) for _ in range(m))
        G,_=lift(F,n)
        truth=source_sat(F,n) is not None
        require(direct_relation(G,n)==(True,truth),'four-variable independent control')
        n4cases+=1
    cross_count=test_crossproducts()
    labels,control_tree_stats=exact22_controls()
    out={'name':'ONEBIT-POLARITY-CERT152','source_three_variable_subsets':input_count,'four_variable_random_sources':n4cases,'complete_relation_classification':dict(boundary_counts),'crossproduct_assignments':cross_count,'exact22_source_control_labels':labels,'exact22_authenticated_unsat_tree':control_tree_stats,'assertion_groups':C['assertions'],'failures':0,'status':{'one_bit_verification':'MATHEMATICAL PROOF; independently computed finite controls','unrestricted_SAT':'OPEN'}}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
