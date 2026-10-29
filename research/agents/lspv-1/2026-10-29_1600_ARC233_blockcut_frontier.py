#!/usr/bin/env python3
"""ARC232: mixed Boolean-module exact messages, selective non-bijunctive pins.
Independent source-manifest checks and fixed-codimension 2CNF+XOR subroutine.
Proof scope: certified module trees only, not general SAT or strict exact22.
Pure standard library.  Reproduction: python3 thisfile.py > results.json
"""
from __future__ import annotations
from collections import Counter
from itertools import product, combinations
from math import ceil, sqrt, log2
import hashlib, json, random, time


def truth(n, clauses, rows, assignment):
    bits = sum((int(v)&1)<<i for i,v in enumerate(assignment))
    return (all(any(assignment[abs(l)-1]==int(l>0) for l in c) for c in clauses)
            and all(((bits & mask).bit_count() & 1)==b for mask,b in rows))


def scc(n, clauses):
    g=[[] for _ in range(2*n)]; r=[[] for _ in range(2*n)]
    def node(lit):return 2*(abs(lit)-1)+int(lit<0)
    for clause in clauses:
        if not clause:return None
        if len(clause)>2:raise ValueError('nonbinary clause')
        a,b=clause[0],clause[-1]
        for src,dst in ((-a,b),(-b,a)):
            u,v=node(src),node(dst);g[u].append(v);r[v].append(u)
    seen=[False]*(2*n);order=[]
    for start in range(2*n):
        if seen[start]:continue
        seen[start]=True;stack=[(start,0)]
        while stack:
            u,k=stack[-1]
            if k<len(g[u]):
                v=g[u][k];stack[-1]=(u,k+1)
                if not seen[v]:seen[v]=True;stack.append((v,0))
            else:order.append(u);stack.pop()
    comp=[-1]*(2*n);num=0
    for start in reversed(order):
        if comp[start]>=0:continue
        comp[start]=num;stack=[start]
        while stack:
            u=stack.pop()
            for v in r[u]:
                if comp[v]<0:comp[v]=num;stack.append(v)
        num+=1
    if any(comp[2*i]==comp[2*i+1] for i in range(n)):return None
    return comp


def sat2(n,clauses):
    comp=scc(n,clauses)
    if comp is None:return None
    return tuple(int(comp[2*i]>comp[2*i+1]) for i in range(n))


def affine_reduce(rows):
    pivots={}
    for mask,rhs in rows:
        m,b=mask,rhs
        while m:
            i=m.bit_length()-1
            if i in pivots:
                p,pb=pivots[i];m^=p;b^=pb
            else:pivots[i]=(m,b);break
        if m==0 and b:return None
    return list(pivots.values())


def affine_coefficient_rank(rows):
    r=affine_reduce([(mask,0) for mask,_ in rows])
    return len(r)


def quotient(n,clauses,rows,stats):
    comp=scc(n,clauses)
    if comp is None:return None
    buckets={};mapping=[]
    for i in range(n):
        a,b=comp[2*i],comp[2*i+1];key=min(a,b)
        if key not in buckets:buckets[key]=len(buckets)
        mapping.append((buckets[key],int(a!=key)))
    m=len(buckets);cc=[]
    for c in clauses:
        new=set()
        for lit in c:
            j,flip=mapping[abs(lit)-1]
            sign=(lit>0)^bool(flip)
            new.add(j+1 if sign else -(j+1))
        if not any(-l in new for l in new):cc.append(tuple(sorted(new)))
    rr=[]
    for mask,b in rows:
        z=0
        for i in range(n):
            if (mask>>i)&1:
                j,flip=mapping[i];z^=1<<j;b^=flip
        rr.append((z,b))
    rr=affine_reduce(rr)
    if rr is None:return None
    stats['scc_quotients']+=1
    return m,cc,rr,mapping


def pluck(n,clauses,rows,p):
    eq=next((i for i,(mask,b) in enumerate(rows) if (mask>>p)&1),None)
    assert eq is not None
    pivot,pb=rows[eq];remaining=[i for i in range(n) if i!=p]
    def drop(mask):return sum(((mask>>i)&1)<<j for j,i in enumerate(remaining))
    newrows=[]
    for i,(mask,b) in enumerate(rows):
        if i==eq:continue
        if (mask>>p)&1:mask^=pivot;b^=pb
        newrows.append((drop(mask),b))
    newrows=affine_reduce(newrows)
    if newrows is None:return None
    newclauses=[]
    for c in clauses:
        out=[]
        for lit in c:
            i=abs(lit)-1
            if i==p:continue
            j=i-int(i>p);out.append(j+1 if lit>0 else -(j+1))
        if not out:return None
        newclauses.append(tuple(out))
    return n-1,newclauses,newrows,(pivot,pb,remaining)


def subspace2sat(n,clauses,rows,stats):
    """Explicit deterministic XP search. Every pluck lowers affine rank.
    Source witness is verified on original 2CNF and GF(2) rows.
    """
    base_rows=affine_reduce(rows)
    if base_rows is None:return None
    def rec(n,C,E):
        stats['subspace_nodes']+=1
        q=quotient(n,C,E,stats)
        if q is None:return None
        m,cc,rr,mapping=q
        candidate=sat2(m,cc)
        if candidate is None:return None
        if truth(m,cc,rr,candidate):
            return tuple(candidate[j]^fl for j,fl in mapping)
        for v in range(m):
            if not any(mask>>v&1 for mask,b in rr):continue
            stats['plucks_attempted']+=1
            child=pluck(m,cc,rr,v)
            if child is None:continue
            mm,c2,r2,(pm,pb,remain)=child
            sol=rec(mm,c2,r2)
            if sol is None:continue
            z=pb;ans=[None]*m
            for j,i in enumerate(remain):
                ans[i]=sol[j]
                if (pm>>i)&1:z^=sol[j]
            ans[v]=z
            if not truth(m,cc,rr,ans):raise AssertionError('invalid pluck reconstruction')
            return tuple(ans[j]^flip for j,flip in mapping)
        return None
    ans=rec(n,[tuple(c) for c in clauses],base_rows)
    if ans is not None and not truth(n,clauses,rows,ans):
        raise AssertionError('wrong local witness')
    return ans


# ARC233 additions, 2026-10-29, LSPV-1. ARC232's subspace2sat above is
# reused under its source attribution, not a newly invented AG solver.
import sys, math, json, time, tracemalloc, random, itertools
from collections import defaultdict
from pathlib import Path
sys.setrecursionlimit(100000)


def support(item):
    if item['type'] == 'cnf':
        assert len(item['lits']) <= 2
        return set(abs(l) - 1 for l in item['lits'])
    if item['type'] == 'xor':
        return set(item['vars'])
    raise ValueError('unknown constraint type')


def eval_source(n, source, a):
    for item in source:
        if item['type'] == 'cnf':
            if not any((a[abs(l)-1] == (l > 0)) for l in item['lits']):
                return False
        else:
            if (sum(a[i] for i in item['vars']) % 2) != item['rhs']:
                return False
    return True


def build_primal(n, source):
    g=[set() for _ in range(n)]
    for item in source:
        vertices=sorted(support(item))
        if not vertices and item['type']=='cnf':
            continue
        for i,u in enumerate(vertices):
            if not (0 <= u < n): raise ValueError('invalid scope')
            for v in vertices[i+1:]:
                g[u].add(v);g[v].add(u)
    return g


def blocks_tarjan(g):
    """Recursive Tarjan for finite controls; a stack implementation
    provides the same polynomial-time asymptotic algorithm for unbounded n.
    Includes singleton blocks for isolated vertices."""
    n=len(g);dis=[-1]*n;low=[0]*n;clock=[0];es=[];blocks=[]
    def dfs(u,p):
        dis[u]=low[u]=clock[0];clock[0]+=1
        for v in sorted(g[u]):
            if dis[v]<0:
                es.append((u,v));dfs(v,u)
                low[u]=min(low[u],low[v])
                if low[v]>=dis[u]:
                    comp=set()
                    while True:
                        x,y=es.pop();comp.add(x);comp.add(y)
                        if (x,y)==(u,v):break
                    blocks.append(comp)
            elif v!=p and dis[v]<dis[u]:
                es.append((u,v));low[u]=min(low[u],dis[v])
    for v in range(n):
        if dis[v]<0:
            if not g[v]:blocks.append({v})
            else:dfs(v,-1)
    blocks.sort(key=lambda b:(min(b),len(b),tuple(sorted(b))))
    return blocks


def source_partition(n,source,blocks):
    owners=[[] for _ in blocks]
    for j,item in enumerate(source):
        sp=support(item)
        if not sp:
            raise ValueError('empty source constraint: separately contradictory')
        cand=[i for i,b in enumerate(blocks) if sp <= b]
        if not cand:
            raise ValueError('constraint scope crosses blocks: invalid construction')
        # A singleton source is owned once, by the first containing block.
        if len(sp)>1 and len(cand)!=1:
            raise ValueError('nonunique owner of non-unary source')
        owners[cand[0]].append(j)
    return owners


def tree_edges(blocks):
    by_var=defaultdict(list)
    for i,b in enumerate(blocks):
        for v in b:by_var[v].append(i)
    cuts={v:bs for v,bs in by_var.items() if len(bs)>1}
    return cuts,by_var


def rank_on_block(source,owner,b):
    idx={v:i for i,v in enumerate(sorted(b))}
    rows=[]
    for j in owner:
        item=source[j]
        if item['type']=='xor':
            rows.append((sum(1<<idx[v] for v in item['vars']),0))
    return affine_coefficient_rank(rows)


def solve_block_local(block,source,owner,pins,stat):
    vs=sorted(block);idx={v:i for i,v in enumerate(vs)}
    c=[];e=[]
    for j in owner:
        item=source[j]
        if item['type']=='cnf':
            c.append(tuple((idx[abs(l)-1]+1)*(1 if l>0 else -1) for l in item['lits']))
        else:
            e.append((sum(1<<idx[v] for v in item['vars']),item['rhs']))
    for v,value in pins.items():
        c.append((idx[v]+1 if value else -(idx[v]+1),))
    stat['local_calls']+=1
    a=subspace2sat(len(vs),c,e,stat)
    if a is None:return None
    ans={v:a[idx[v]] for v in vs}
    # Source-authentication: verify every owned constraint, and every pin.
    assert all((item['type']=='cnf' and all(abs(l)-1 in ans for l in item['lits'])
                and any(ans[abs(l)-1]==int(l>0) for l in item['lits']))
               or (item['type']=='xor' and sum(ans[v] for v in item['vars'])%2==item['rhs'])
               for item in [source[j] for j in owner])
    assert all(ans[v]==a0 for v,a0 in pins.items())
    return ans


def blockcut_decide(n,source,e0,stat):
    """One deterministic bottom-up block-cut controller, no answer bit.
    Returns (True,witness), (False,None), or (None,None) for rank violation.
    Caller charges discovery, all attempted local calls, source reads,
    witness reconstruction and final source authentication."""
    # Reject malformed syntax before structural discovery. Empty clauses
    # and inconsistent zero-arity affine rows are immediate UNSAT controls.
    if not isinstance(n,int) or n < 0 or e0 < 0:
        raise ValueError('bad input dimension or cap')
    for item in source:
        if item['type']=='cnf':
            if len(item['lits'])>2 or any(not isinstance(l,int) or l==0 or abs(l)>n for l in item['lits']):
                raise ValueError('malformed 2CNF source')
            if not item['lits']:return False,None
        elif item['type']=='xor':
            if item['rhs'] not in (0,1) or len(set(item['vars']))!=len(item['vars']) or any(not isinstance(v,int) or v<0 or v>=n for v in item['vars']):
                raise ValueError('malformed affine source')
            if not item['vars'] and item['rhs']==1:return False,None
        else:raise ValueError('unknown source type')
    # Consistent empty parity rows can be discarded without changing SAT.
    source=[x for x in source if x['type']!='xor' or x['vars']]
    g=build_primal(n,source)
    blocks=blocks_tarjan(g)
    owner=source_partition(n,source,blocks)
    cuts,by_var=tree_edges(blocks)
    rank=[rank_on_block(source,o,b) for o,b in zip(owner,blocks)]
    if max(rank,default=0)>e0:return None,None
    stat['blocks']=len(blocks);stat['max_block_rank']=max(rank,default=0)
    stat['global_affine_rank']=affine_coefficient_rank([
        (sum(1<<v for v in x['vars']),0) for x in source if x['type']=='xor'])
    stat['max_block_size']=max(map(len,blocks),default=0)
    stat['primal_edges']=sum(len(x) for x in g)//2
    stat['cut_vertices']=len(cuts)
    # Root each connected component of block-cut forest, with articulation
    # nodes as intermediary. This enforces one shared variable per branch.
    seen=set();messages={};local_witness={};children={};roots=[]
    def process(bid, parent_cut=None):
        seen.add(bid); children[bid]=[]
        for v in sorted(blocks[bid]):
            if v==parent_cut or v not in cuts:continue
            for cid in cuts[v]:
                if cid==bid or cid in seen:continue
                process(cid,v)
                children[bid].append((v,cid))
        allowed={}
        for v,cid in children[bid]:
            valset=messages[cid]
            allowed.setdefault(v,set((0,1))).intersection_update(valset)
        if any(not s for s in allowed.values()):
            choices=(0,1) if parent_cut is not None else (None,)
            messages[bid]=set()
            for val in choices:local_witness[(bid,val)]=None
            return
        forced={v:next(iter(s)) for v,s in allowed.items() if len(s)==1}
        choices=(0,1) if parent_cut is not None else (None,)
        feas=set()
        for value in choices:
            pins=forced.copy()
            if value is not None:
                if parent_cut in pins and pins[parent_cut]!=value:
                    local_witness[(bid,value)]=None;continue
                pins[parent_cut]=value
            a=solve_block_local(blocks[bid],source,owner[bid],pins,stat)
            local_witness[(bid,value)]=a
            if a is not None:feas.add(value)
        messages[bid]=feas
    for bid in range(len(blocks)):
        if bid not in seen:
            roots.append(bid);process(bid)
    if any(not messages[bid] for bid in roots):return False,None
    a=[None]*n
    def materialize(bid,p):
        w=local_witness[(bid,p)];assert w is not None
        for v,x in w.items():
            if a[v] is not None:assert a[v]==x
            else:a[v]=x
        for cut,cid in children[bid]:materialize(cid,a[cut])
    for root in roots:materialize(root,None)
    assert all(x is not None for x in a)
    assert eval_source(n,source,a)
    stat['witness_validation_checks']+=len(source)
    return True,tuple(a)


def make_star(q,unsat=False):
    source=[]
    for i in range(q):
        for j in range(i+1,q):
            source.append({'type':'cnf','lits':(i+1,j+1)})
    for i in range(q):
        source.append({'type':'xor','vars':(i,q+2*i,q+2*i+1),'rhs':0})
    if unsat:
        for i in (0,1):
            source.extend([{'type':'cnf','lits':(-(q+2*i+1),)},
                           {'type':'cnf','lits':(-(q+2*i+2),)}])
    return 3*q,source


def brute(n,source):
    for bits in itertools.product((0,1),repeat=n):
        if eval_source(n,source,bits):return bits
    return None


def randint_source(rng,n):
    source=[]
    for _ in range(rng.randrange(0,10)):
        length=rng.choice((1,2))
        js=rng.sample(range(n),min(length,n))
        source.append({'type':'cnf','lits':tuple((v+1)*rng.choice((-1,1)) for v in js)})
    for _ in range(rng.randrange(0,5)):
        js=rng.sample(range(n),rng.randrange(1,min(n,3)+1))
        source.append({'type':'xor','vars':tuple(js),'rhs':rng.randrange(2)})
    return source


def proxy(n):
    out=[]
    for b in range(1,n//3+2):
        q=max(0,math.ceil((n-3*b)/(12*b)))
        out.append({'b':b,'q':q,'time_exp':b+q,'space_exp':b})
    min_e=min(x['time_exp'] for x in out)
    first_equal=next((x for x in out if x['time_exp']==x['space_exp']),None)
    nondom=[x for x in out if not any(y['time_exp']<=x['time_exp'] and
                                           y['space_exp']<=x['space_exp'] and
                                           (y['time_exp']<x['time_exp'] or
                                            y['space_exp']<x['space_exp']) for y in out)]
    return {'n':n,'min_time_exp':min_e,
            'min_b':[x['b'] for x in out if x['time_exp']==min_e],
            'first_equal':first_equal,'pareto':nondom,
            'count_permitted_points':len(out)}


def run():
    rng=random.Random(202610291600)
    out={'metadata':{'seed':202610291600,'algorithm':'block-cut / borrowed ARC232 local AG solver',
                     'model':'Python implementation, not a measured TM time exponent',
                     'tests':'random typed sources plus exact witness comparisons'},
         'random':{},'dense':[],'proxy':proxy(1200)}
    total=0;good=0;unknown=0;nx_matches=0
    import networkx as nx # Independent graph decomposition reference for testing only.
    for n in range(1,9):
        for rep in range(50):
            source=randint_source(rng,n)
            g=build_primal(n,source)
            gg=nx.Graph();gg.add_nodes_from(range(n))
            gg.add_edges_from((u,v) for u,nb in enumerate(g) for v in nb if u<v)
            ours={frozenset(b) for b in blocks_tarjan(g)}
            others={frozenset(b) for b in nx.biconnected_components(gg)}
            others |= {frozenset([v]) for v in gg.nodes if gg.degree(v)==0}
            assert ours==others,(n,source,ours,others)
            nx_matches+=1
            st=defaultdict(int)
            ans,w=blockcut_decide(n,source,2,st)
            exact=brute(n,source)
            if ans is not None:
                assert ans==(exact is not None),(n,source,st)
                if ans:assert eval_source(n,source,w)
                good+=1
            else:unknown+=1
            total+=1
    out['random']={'total':total,'recognized':good,'rank_above_cap':unknown,
                    'networkx_partition_matches':nx_matches,
                    'false_results':0}
    for q in (4,8,16,32):
        for unsat in (False,True):
            n,source=make_star(q,unsat)
            st=defaultdict(int)
            tracemalloc.start();start=time.perf_counter()
            ans,w=blockcut_decide(n,source,1,st)
            duration=time.perf_counter()-start
            peak=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
            assert ans== (not unsat),(q,unsat,st)
            if ans: assert eval_source(n,source,w)
            row={'q':q,'n':n,'m':len(source),'N_json_bytes':len(json.dumps(source)),
                 'unsat':unsat,'result':ans,'seconds':round(duration,6),
                 'python_tracemalloc_peak_bytes':peak,
                 'treewidth_lower_bound':q-1,'local_rank_cap':1,**st}
            out['dense'].append(row)
    return out


if __name__=='__main__':
    res=run()
    print(json.dumps(res,sort_keys=True,indent=2))
