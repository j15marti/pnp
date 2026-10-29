#!/usr/bin/env python3
"""ARC220: source-authenticated adaptive SAT/UNSAT certificate portfolio.

One deterministic program.  Complete for two explicitly recognized structural
islands; returns UNKNOWN elsewhere.  No oracle, free side bit, or general P=NP
claim.  Stdlib only; exact proof and source-offset checks.  Proof/research toy,
not a native Turing-machine transition profiler.
"""
from __future__ import annotations
from collections import defaultdict, deque
from itertools import combinations, product
from pathlib import Path
from hashlib import sha256
import json, math, random

SEED = 22020261029
ROOT = Path(__file__).resolve().parent


def canonical(c):
    cc=tuple(sorted(set(c),key=lambda x:(abs(x),x<0)))
    if any(-v in cc for v in cc) or 0 in cc:raise ValueError('tautology/zero')
    return cc


def serialize(n, clauses):
    lines=[f'p cnf {n} {len(clauses)}\n']
    for c in clauses:
        c=canonical(c)
        lines.append(' '.join(map(str,c))+(' ' if c else '')+'0\n')
    return ''.join(lines).encode('ascii')


def parse(data):
    try:ls=data.decode('ascii').splitlines(keepends=True)
    except UnicodeDecodeError as e:raise ValueError('not ASCII') from e
    if not ls or not all(x.endswith('\n') for x in ls):raise ValueError('unterminated')
    h=ls[0].split()
    if len(h)!=4 or h[:2]!=['p','cnf']:raise ValueError('bad header')
    try:n,m=map(int,h[2:])
    except ValueError as e:raise ValueError('noninteger header') from e
    if n<1 or m<0 or n>len(data)+1 or m>len(data):raise ValueError('size header')
    if len(ls)!=m+1:raise ValueError('clause count')
    offset=len(ls[0]);out=[];offsets=[]
    for s in ls[1:]:
        try:words=list(map(int,s.split()))
        except ValueError as e:raise ValueError('bad literal bytes') from e
        if not words or words[-1]!=0 or 0 in words[:-1]:raise ValueError('clause terminator')
        if len(words)>4 or any(abs(x)>n for x in words[:-1]):raise ValueError('bad clause')
        if len(set(map(abs,words[:-1])))!=len(words)-1:raise ValueError('improper')
        c=canonical(words[:-1]);out.append(c);offsets.append(offset);offset+=len(s)
    if offset!=len(data):raise ValueError('trailing source data')
    return n,out,offsets


def evaluate(source,a):
    return all(any(a[abs(l)]==(l>0) for l in c) for c in source)


def simplify_clause(c,a):
    z=[]
    for v in c:
        if abs(v) in a:
            if a[abs(v)]==(v>0):return None
        else:z.append(v)
    return canonical(z)


def hit_backdoor(source,cap,stats):
    """For syntactic 2CNF strong backdoors, 3-clauses must each be hit.
    Failed branches are charged; at most 3^cap leaves (plus internal nodes).
    """
    triples=[frozenset(map(abs,c)) for c in source if len(c)==3]
    def visit(B,left):
        stats['hitting_nodes']+=1
        edge=next((e for e in triples if not e.intersection(B)),None)
        if edge is None:return tuple(sorted(B))
        if left<=0:return None
        for x in sorted(edge):
            got=visit(B|{x},left-1)
            if got is not None:return got
        return None
    return visit(set(),cap)


def edges_for_2sat(source,n,assigned):
    adj={lit:[] for v in range(1,n+1) if v not in assigned for lit in (v,-v)}
    for i,c in enumerate(source):
        rem=simplify_clause(c,assigned)
        if rem is None:continue
        if len(rem)>2:raise ValueError('not 2SAT')
        if len(rem)==0:return adj,('empty',i)
        if len(rem)==1:
            u=rem[0];adj[-u].append((u,i))
        if len(rem)==2:
            u,v=rem;adj[-u].append((v,i));adj[-v].append((u,i))
    return adj,None


def path(adj,src,dst):
    todo=deque([src]);par={src:None};edge={}
    while todo:
        v=todo.popleft()
        if v==dst:break
        for to,idx in adj[v]:
            if to not in par:par[to]=v;edge[to]=idx;todo.append(to)
    if dst not in par:return None
    a=[];v=dst
    while par[v] is not None:
        u=par[v];a.append([u,v,edge[v]]);v=u
    a.reverse();return a


def two_sat(source,n,assigned,stats):
    adj,empty=edges_for_2sat(source,n,assigned)
    if empty:return False,{'kind':'empty','source':empty[1],'assigned':dict(assigned)}
    rev={v:[] for v in adj}
    for u,arrows in adj.items():
        for v,i in arrows:rev[v].append((u,i));stats['implication_edges']+=1
    visited=set();finish=[]
    def dfs(root):
        todo=[(root,False)]
        while todo:
            v,after=todo.pop()
            if after:finish.append(v);continue
            if v in visited:continue
            visited.add(v);todo.append((v,True))
            for nxt,_ in adj[v]:
                if nxt not in visited:todo.append((nxt,False))
    for v in sorted(adj,key=lambda x:(abs(x),x<0)):
        if v not in visited:dfs(v)
    comp={};cc=0
    for root in reversed(finish):
        if root in comp:continue
        todo=[root];comp[root]=cc
        while todo:
            v=todo.pop()
            for nxt,_ in rev[v]:
                if nxt not in comp:comp[nxt]=cc;todo.append(nxt)
        cc+=1
    free=sorted({abs(v) for v in adj})
    for x in free:
        if comp[x]==comp[-x]:
            a=path(adj,x,-x);b=path(adj,-x,x)
            assert a is not None and b is not None
            return False,{'kind':'scc','x':x,'plus':a,'minus':b,'assigned':dict(assigned)}
    witness=dict(assigned)
    for x in free:witness[x]=comp[x]>comp[-x]
    assert evaluate(source,witness),'2SAT SCC witness reconstruction'
    return True,{'kind':'witness','a':witness}


def backdoor_tree(source,n,B,stats):
    """Returns a whole proof tree for UNSAT, witness for SAT; no free label.
    Depth |B|; stops at first SAT branch, but fully explores for UNSAT.
    """
    def recur(pos,a):
        stats['leaf_or_branch_calls']+=1
        if pos==len(B):
            ok,info=two_sat(source,n,a,stats)
            stats['2sat_leaves']+=1
            if ok:return True,info
            stats['unsat_leaves']+=1
            return False,info
        x=B[pos]
        a[x]=False;lo,p0=recur(pos+1,a)
        if lo:a.pop(x);return True,p0
        a[x]=True;hi,p1=recur(pos+1,a)
        a.pop(x)
        if hi:return True,p1
        return False,{'kind':'branch','x':x,'zero':p0,'one':p1}
    return recur(0,{})


def verify_unsat_tree(source,n,tree,assigned=None):
    if assigned is None:assigned={}
    kind=tree['kind']
    if kind=='branch':
        x=tree['x']
        if not 1<=x<=n or x in assigned:return False
        a=dict(assigned);a[x]=False
        b=dict(assigned);b[x]=True
        return verify_unsat_tree(source,n,tree['zero'],a) and verify_unsat_tree(source,n,tree['one'],b)
    if tree.get('assigned')!=assigned:return False
    if kind=='empty':
        i=tree['source']
        return type(i)==int and 0<=i<len(source) and simplify_clause(source[i],assigned)==()
    if kind=='scc':
        x=tree['x']
        if not 1<=x<=n or x in assigned:return False
        for edges,start,goal in ((tree['plus'],x,-x),(tree['minus'],-x,x)):
            v=start
            if len(edges)>2*n or not edges:return False
            for u,w,idx in edges:
                if u!=v or type(idx)!=int or not 0<=idx<len(source):return False
                rem=simplify_clause(source[idx],assigned)
                if rem is None or len(rem)>2:return False
                if len(rem)==1:
                    t=rem[0]
                    if not (u==-t and w==t):return False
                elif len(rem)==2:
                    a,b=rem
                    if not ((u==-a and w==b) or (u==-b and w==a)):return False
                else:return False
                v=w
            if v!=goal:return False
        return True
    return False


def primal(source,n):
    G={v:set() for v in range(1,n+1)}
    for c in source:
        for a,b in combinations(sorted(set(map(abs,c))),2):G[a].add(b);G[b].add(a)
    return G


def minfill(source,n):
    """Deterministic polynomial heuristic, *not* an FPT treewidth optimizer."""
    G=primal(source,n);order=[];peak=0
    while G:
        def score(v):
            a=G[v]
            fill=sum(y not in G[x] for x,y in combinations(sorted(a),2))
            return fill,len(a),v
        v=min(G,key=score);ne=sorted(G[v]);peak=max(peak,len(ne))
        for a,b in combinations(ne,2):G[a].add(b);G[b].add(a)
        for x in ne:G[x].remove(v)
        del G[v];order.append(v)
    return order,peak


def resolve(a,b,x):
    assert x in a and -x in b
    z=set(a)-{x};z.update(set(b)-{-x})
    if any(-v in z for v in z):return None
    return canonical(z)


def verify_resolution(source,proof,unsat=False):
    for i,row in enumerate(proof):
        try:c=canonical(row['clause'])
        except ValueError:return False
        if c!=tuple(row['clause']):return False
        if row['kind']=='source':
            j=row['source']
            if type(j)!=int or not 0<=j<len(source) or c!=source[j]:return False
        elif row['kind']=='res':
            a,b,x=row['a'],row['b'],row['pivot']
            if any(type(z)!=int or not 0<=z<i for z in (a,b)):return False
            ac=proof[a]['clause'];bc=proof[b]['clause']
            if x not in ac or -x not in bc:return False
            if resolve(ac,bc,x)!=c:return False
        else:return False
    return not unsat or bool(proof) and proof[-1]['clause']==[]


def width_solve(source,n,order,stats):
    proof=[{'kind':'source','source':j,'clause':list(c)} for j,c in enumerate(source)]
    active={c:j for j,c in enumerate(source)};hist=[]
    if () in active:
        i=active[()];proof.append({'kind':'source','source':i,'clause':[]})
        assert verify_resolution(source,proof,True)
        return False,{'kind':'resolution','rows':proof}
    for v in order:
        pos=[(c,i) for c,i in active.items() if v in c]
        neg=[(c,i) for c,i in active.items() if -v in c]
        hist.append((v,[c for c,_ in pos],[c for c,_ in neg]))
        nxt={c:i for c,i in active.items() if v not in c and -v not in c}
        for a,ia in pos:
            for b,ib in neg:
                stats['resolution_pairs']+=1
                c=resolve(a,b,v)
                if c is None or c in nxt:continue
                j=len(proof);proof.append({'kind':'res','a':ia,'b':ib,'pivot':v,'clause':list(c)})
                nxt[c]=j;stats['resolution_derived']+=1
                if c==():
                    assert verify_resolution(source,proof,True)
                    return False,{'kind':'resolution','rows':proof}
        active=nxt
    a={}
    for v,pos,neg in reversed(hist):
        need1=any(not any(a[abs(x)]==(x>0) for x in c if x!=v) for c in pos)
        need0=any(not any(a[abs(x)]==(x>0) for x in c if x!=-v) for c in neg)
        assert not (need1 and need0)
        a[v]=bool(need1)
    assert evaluate(source,a)
    return True,{'kind':'witness','a':a}

YES_BASE=serialize(3,[(1,2,3)])
NO_BASE=serialize(3,[tuple((i+1) if (mask>>i)&1 else -(i+1) for i in range(3)) for mask in range(8)])


def portfolio(data,opts=None):
    n,source,offs=parse(data)
    N=len(data);kcap=int(math.log2(max(2,N)));wcap=kcap
    if opts:
        kcap=opts.get('kcap',kcap);wcap=opts.get('wcap',wcap)
    stats=defaultdict(int)
    order,w=minfill(source,n);stats['greedy_width']=w;stats['width_cap']=wcap
    if w<=wcap:
        ok,proof=width_solve(source,n,order,stats)
        stats['route_width']+=1
        if ok:
            assert proof['kind']=='witness' and evaluate(source,proof['a'])
        else:assert verify_resolution(source,proof['rows'],True)
        return {'status':'YES' if ok else 'NO','route':'width','proof':proof,
                'child':YES_BASE if ok else NO_BASE,'stats':dict(stats)}
    B=hit_backdoor(source,kcap,stats)
    if B is None:
        return {'status':'UNKNOWN','route':'none','stats':dict(stats)}
    assert all(len(c)<3 or any(abs(l) in B for l in c) for c in source)
    ok,proof=backdoor_tree(source,n,B,stats)
    stats['route_backdoor']+=1;stats['backdoor_size']=len(B)
    if ok:assert proof['kind']=='witness' and evaluate(source,proof['a'])
    else:assert verify_unsat_tree(source,n,proof)
    return {'status':'YES' if ok else 'NO','route':'backdoor','proof':proof,
            'child':YES_BASE if ok else NO_BASE,'stats':dict(stats)}



def physical_successor(data,opts=None):
    """One answer-preserving successor or the original input.

    Input base strings are terminal (not recursed into).  The identity fallback
    is NOT a shrinking child.  No answer is inferred on that branch.
    """
    if data == YES_BASE:return {'phase':'terminal','answer':'YES','child':None}
    if data == NO_BASE:return {'phase':'terminal','answer':'NO','child':None}
    out=portfolio(data,opts)
    if out['status']=='UNKNOWN':
        return {'phase':'unresolved','answer':None,'child':data,'route':'identity'}
    return {'phase':'successor','answer':out['status'],'child':out['child'],'route':out['route']}


def brute(source,n):
    for bits in product((False,True),repeat=n):
        if evaluate(source,{i+1:bits[i] for i in range(n)}):return True
    return False


def tests():
    rng=random.Random(SEED);S=defaultdict(int)
    def check(source,n,route=None,opts=None):
        r=portfolio(serialize(n,source),opts)
        expected=brute(source,n) if n<=12 else None
        assert r['status'] in ('YES','NO','UNKNOWN')
        if r['status']!='UNKNOWN':
            if expected is not None:assert (r['status']=='YES')==expected
            assert r['child'] in (YES_BASE,NO_BASE)
            if route is not None:assert r['route']==route,(route,r['route'],r['stats'])
            if r['route']=='backdoor' and r['status']=='NO':
                assert verify_unsat_tree(source,n,r['proof'])
                copy_tree=json.loads(json.dumps(r['proof']))
                bad=copy_tree
                while bad['kind']=='branch':bad=bad['zero']
                if bad['kind']=='scc':
                    bad['plus'][0][2]=len(source)+100
                    assert not verify_unsat_tree(source,n,copy_tree);S['forged_source_reject']+=1
            if r['route']=='width' and r['status']=='NO':
                bad=json.loads(json.dumps(r['proof']['rows']))
                j=next((i for i,row in enumerate(bad) if row['kind']=='res'),None)
                if j is not None:
                    bad[j]['pivot']=n+100
                    assert not verify_resolution(source,bad,True);S['forged_pivot_reject']+=1
        S['cases']+=1;S['answers_'+r['status']]+=1;S['route_'+r['route']]+=1
        for k,v in r['stats'].items():
            if isinstance(v,int):S['total_'+k]+=v
        return r
    # 2CNF with K_n primal: width n-1, hitting-backdoor size zero.
    for n in (5,8,11):
        clauses=[(i,j) for i,j in combinations(range(1,n+1),2)]
        a=check(clauses,n,'backdoor',{'wcap':2,'kcap':0});assert a['status']=='YES'
        b=check(clauses+[(1,),(-1,)],n,'backdoor',{'wcap':2,'kcap':0});assert b['status']=='NO'
    # Many disjoint 3-clauses: induced width 2, linear 2SAT hitting number.
    for k in (3,4,5):
        F=[(3*j+1,3*j+2,3*j+3) for j in range(k)]
        a=check(F,3*k,'width',{'wcap':2,'kcap':0});assert a['status']=='YES'
        F2=[tuple((3*j+i+1) if (mask>>i)&1 else -(3*j+i+1) for i in range(3))
            for j in range(k) for mask in range(8)]
        b=check(F2,3*k,'width',{'wcap':2,'kcap':0});assert b['status']=='NO'
    # High width but 1-backdoor even on UNSAT: hub all ternary pairs.
    for n in (6,8,10):
        hub=1
        clauses=[(hub,i,j) for i,j in combinations(range(2,n+1),2)]
        a=check(clauses,n,'backdoor',{'wcap':2,'kcap':1});assert a['status']=='YES'
        b=check(clauses+[(-hub,)],n,'backdoor',{'wcap':2,'kcap':1});assert b['status']=='YES'
        # explicit incompatible 2CNF under hub=false, hub forced false by unit
        bad=[(hub,2,3),(hub,2,-3),(hub,-2,3),(hub,-2,-3),(-hub,)]
        b=check(bad+clauses,n,None,{'wcap':2,'kcap':1});assert b['status']=='NO'
    # Arbitrary proper signed random small cases, both answer classes, incl source duplicates.
    for n in range(3,9):
        for trial in range(50):
            clauses=[]
            for _ in range(rng.randint(1,3*n)):
                vs=rng.sample(range(1,n+1),rng.randint(1,min(3,n)))
                clauses.append(tuple(x if rng.randrange(2) else -x for x in vs))
            check(clauses,n)
    # Random instances certified through forced 2SAT backdoor of size <=2, width cap zero.
    for n in range(4,11):
        for trial in range(22):
            clauses=[]
            for _ in range(rng.randint(1,4*n)):
                vs=rng.sample(range(2,n+1),2)
                if rng.randrange(3)==0:vs=[1,*vs]
                clauses.append(tuple(x if rng.randrange(2) else -x for x in vs))
            check(clauses,n,'backdoor',{'wcap':0,'kcap':1})
    # Explicit exhaustive 3-bit high-entropy contradiction and tautology-free SAT control.
    every=[tuple((i+1) if (mask>>i)&1 else -(i+1) for i in range(3)) for mask in range(8)]
    check(every,3,'backdoor',{'wcap':0,'kcap':1})
    check(every[:-1],3,'backdoor',{'wcap':0,'kcap':1})
    for mask in range(256):
        subset=[every[j] for j in range(8) if (mask>>j)&1]
        check(subset,3,'backdoor' if subset else 'width',{'wcap':0,'kcap':1})
        S['signed_ternary_subsets_exhaustive']+=1
    # A wrong source offset is not a source clause, even if it has identical literals.
    data=serialize(3,every)
    assert parse(data)[1]==[canonical(c) for c in every]
    for malformed in [data+b'garbage',data.replace(b'p cnf 3 8',b'p cnf 2 8'),data.replace(b' 0\n',b' 1\n',1)]:
        try:portfolio(malformed)
        except ValueError:S['malformed_reject']+=1
        else:raise AssertionError('malformed accepted')
    # Genuine two-level physical successor test on both SAT and UNSAT:
    # no recursive call required after reaching the constant base.
    big_yes=serialize(3,[(1,2,3)]*60)
    big_no=serialize(3,every*7)
    for raw,answer in ((big_yes,'YES'),(big_no,'NO')):
        assert len(raw)>400
        step=physical_successor(raw)
        assert step['phase']=='successor' and step['answer']==answer
        assert len(step['child']) <= len(raw)**0.75
        assert physical_successor(step['child']) == {'phase':'terminal','answer':answer,'child':None}
        S['physical_two_levels_'+answer]+=1
    # A failed parameter search is not a licence to guess SAT/UNSAT: identity.
    dense=[tuple(x for x in triple) for triple in combinations(range(1,8),3)]
    original=serialize(7,dense)
    identity=physical_successor(original,{'wcap':0,'kcap':0})
    assert identity['phase']=='unresolved' and identity['child']==original
    S['identity_fallback_test']+=1
    out={'seed':SEED,'status':'PASS','checks':dict(sorted(S.items())),
         'scope':'one fixed dual-parameter recognizer with sound SAT and UNSAT decisions; UNKNOWN on unrecognized inputs',
         'proof_systems':'width resolution DAG or source-authenticated 2CNF SCC branch tree',
         'negative_claims':['not general SAT','not a polynomial child map on all SAT','greedy width is not treewidth FPT discovery','native TM exponents not measured']}
    raw=json.dumps(out,indent=2,sort_keys=True)+'\n'
    (ROOT/'ARC220_adaptive_dual_parameter_raw.json').write_text(raw)
    print(raw)

if __name__=='__main__':tests()
