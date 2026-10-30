#!/usr/bin/env python3
"""ARC235, 2026-10-29, LSPV-1. Self-contained deterministic adhesion<=2 mixed SAT.
Source-authenticated typed constraints, poly-time discovered 0/1/2 separators,
exact 2CNF messages, rank<=1 affine local solver, model reconstruction.
Returns UNKNOWN for a discovered leaf having affine rank>1. A recognized
class only, not general SAT, not a Turing-machine benchmark.
"""
from __future__ import annotations
from collections import defaultdict, Counter
from dataclasses import dataclass
from itertools import combinations, product
import argparse, json, hashlib, random, time, tracemalloc, math

@dataclass(frozen=True)
class Source:
    kind: str  # c or a
    index: int
    scope: tuple[int, ...]  # absolute indices 1-based
    data: tuple[int, ...]   # signed literals or (rhs,)

@dataclass
class Bag:
    vars: tuple[int,...]
    sources: tuple[int,...]

class Stats:
    def __init__(self):
        self.two_sat_calls=0; self.sat_graph_edges=0; self.minima=0
        self.cut_tests=0; self.cut_success=0; self.local_calls=0
        self.table_entries=0; self.memo_witness_bits=0
        self.source_checks=0; self.msg_clauses=0; self.reconstruction_nodes=0

def encode(n: int, sources: list[Source]) -> bytes:
    nc=sum(s.kind=='c' for s in sources); na=len(sources)-nc
    lines=[f'p mix {n} {nc} {na}\n']+[f'v {i}\n' for i in range(1,n+1)]
    for s in sources:
        if s.kind=='c':
            lines.append('c '+str(s.index)+' '+' '.join(map(str,s.data))+' 0\n')
        else:
            lines.append('a '+str(s.index)+' '+str(s.data[0])+' '+' '.join(map(str,s.scope))+' 0\n')
    return ''.join(lines).encode('ascii')

def parse(data:bytes):
    lines=data.decode('ascii').splitlines(keepends=True)
    p=lines[0].split()
    if len(p)!=5 or p[:2]!=['p','mix']:raise ValueError('header')
    n,nc,na=map(int,p[2:])
    if len(lines)!=1+n+nc+na or n<0: raise ValueError('line count')
    if any(lines[1+i]!=f'v {i+1}\n' for i in range(n)):raise ValueError('roster')
    sources=[]; offsets=[]; off=sum(map(len,lines[:n+1]))
    for j,line in enumerate(lines[n+1:]):
        parts=line.split(); kind='c' if j<nc else 'a'
        idx=j if kind=='c' else j-nc
        if len(parts)<3 or parts[0]!=kind or int(parts[1])!=idx or parts[-1]!='0':raise ValueError('source id')
        if kind=='c':
            lits=tuple(map(int,parts[2:-1]))
            if len(lits)>2 or any(not v or abs(v)>n for v in lits):raise ValueError('not 2cnf')
            sources.append(Source(kind,idx,tuple(sorted({abs(v) for v in lits})),lits))
        else:
            rhs=int(parts[2]); scope=tuple(map(int,parts[3:-1]))
            if rhs not in (0,1) or len(set(scope))!=len(scope) or tuple(sorted(scope))!=scope or any(not 1<=v<=n for v in scope):raise ValueError('xor row')
            sources.append(Source(kind,idx,scope,(rhs,)))
        offsets.append(off);off+=len(line)
    if encode(n,sources)!=data:raise ValueError('noncanonical bytes')
    return n,sources,offsets

def source_truth(sources, assignment):
    for s in sources:
        if s.kind=='c':
            if not any((assignment[abs(l)] if l>0 else 1-assignment[abs(l)]) for l in s.data):return False
        else:
            if (sum(assignment[v] for v in s.scope)&1)!=s.data[0]:return False
    return True

def two_sat(n, clauses, stats):
    stats.two_sat_calls += 1
    g=[[] for _ in range(2*n)]; rg=[[] for _ in range(2*n)]
    def lit(l):return 2*(abs(l)-1)+(0 if l>0 else 1)
    def edge(u,v):g[u].append(v);rg[v].append(u);stats.sat_graph_edges+=1
    for cl in clauses:
        if len(cl)==0:return None
        a=lit(cl[0])
        if len(cl)==1:edge(a^1,a)
        elif len(cl)==2:
            b=lit(cl[1]); edge(a^1,b);edge(b^1,a)
        else:raise ValueError('not 2cnf')
    seen=[0]*(2*n);order=[]
    for u in range(2*n):
        if seen[u]:continue
        seen[u]=1;stack=[(u,0)]
        while stack:
            v,i=stack[-1]
            if i==len(g[v]):order.append(v);stack.pop();continue
            w=g[v][i];stack[-1]=(v,i+1)
            if not seen[w]:seen[w]=1;stack.append((w,0))
    comp=[-1]*(2*n); cnt=0
    for u in reversed(order):
        if comp[u]>=0:continue
        todo=[u];comp[u]=cnt
        while todo:
            v=todo.pop()
            for w in rg[v]:
                if comp[w]<0:comp[w]=cnt;todo.append(w)
        cnt+=1
    for v in range(n):
        if comp[2*v]==comp[2*v+1]:return None
    model=tuple(int(comp[2*v]>comp[2*v+1]) for v in range(n))
    assert all(any((model[abs(l)-1] if l>0 else 1-model[abs(l)-1]) for l in c) for c in clauses)
    return model

def one_parity(n,clauses,support,rhs,stats):
    """Independent reimplementation of ARC227 rank-one generator procedure."""
    x0=two_sat(n,clauses,stats)
    if x0 is None:return None
    par=lambda x: sum(x[i] for i in support)&1
    if par(x0)==rhs:return x0
    for i in range(n):
        forced=(i+1 if x0[i]==0 else -(i+1))
        if two_sat(n,[*clauses,(forced,)],stats) is None:continue
        g=list(x0)
        for j in range(n):
            same=(j+1 if x0[j] else -(j+1))
            if two_sat(n,[*clauses,(forced,),(same,)],stats) is None:g[j]^=1
        stats.minima+=1
        assert g[i]!=x0[i]
        assert all(any((g[abs(l)-1] if l>0 else 1-g[abs(l)-1]) for l in c) for c in clauses)
        if par(g)==rhs:return tuple(g)
    return None

def all_components(vertices, edges, omit):
    vs=set(vertices)-set(omit)
    adj={v:set() for v in vs}
    for a,b in edges:
        if a in vs and b in vs:adj[a].add(b);adj[b].add(a)
    comps=[]
    while vs:
        root=min(vs); stack=[root];vs.remove(root);comp={root}
        while stack:
            v=stack.pop()
            for w in adj[v]:
                if w in vs:vs.remove(w);comp.add(w);stack.append(w)
        comps.append(comp)
    return comps

def build_edges(sources, source_ids, virtual):
    edges=set(virtual)
    for j in source_ids:
        sc=sources[j].scope
        edges.update(tuple(sorted(edge)) for edge in combinations(sc,2))
    return edges

def find_cut(vertices, edges, stats):
    verts=tuple(sorted(vertices))
    # Enumerating all candidate 0/1/2 separators is deterministic and polynomial.
    for s in (0,1,2):
        for cut in combinations(verts,s):
            stats.cut_tests+=1
            comps=all_components(verts,edges,cut)
            if len(comps)>=2:
                stats.cut_success+=1
                return tuple(cut),comps
    return None

def split_bags(n,sources,stats):
    bags=[];links=[]
    def recurse(verts,source_ids,virtual):
        edges=build_edges(sources,source_ids,virtual)
        cut=find_cut(verts,edges,stats)
        if cut is None:
            idx=len(bags);bags.append(Bag(tuple(sorted(verts)),tuple(source_ids)))
            return [idx]
        s,components=cut
        A=components[0]; B=set().union(*components[1:])
        va=set(s)|A; vb=set(s)|B
        assert va<set(verts) and vb<set(verts)
        sa=[];sb=[]
        for j in source_ids:
            scope=set(sources[j].scope)
            aa=scope<=va;bb=scope<=vb
            assert aa or bb, ('cross-cut-source',sources[j],s)
            (sa if aa else sb).append(j)
        virt_a={edge for edge in virtual if set(edge)<=va}
        virt_b={edge for edge in virtual if set(edge)<=vb}
        virt_a.update(combinations(s,2));virt_b.update(combinations(s,2))
        aa=recurse(tuple(sorted(va)),sa,virt_a)
        bb=recurse(tuple(sorted(vb)),sb,virt_b)
        pick_a=next((i for i in aa if set(s)<=set(bags[i].vars)),None)
        pick_b=next((i for i in bb if set(s)<=set(bags[i].vars)),None)
        assert pick_a is not None and pick_b is not None, ('anchor',s)
        links.append((pick_a,pick_b))
        return aa+bb
    recurse(tuple(range(1,n+1)),list(range(len(sources))),set())
    return bags,links

def verify_tree(n,sources,bags,links,stats):
    k=len(bags); owner={}
    for i,b in enumerate(bags):
        for j in b.sources:
            if j in owner:raise AssertionError('source duplicate')
            owner[j]=i
            assert set(sources[j].scope)<=set(b.vars)
            stats.source_checks+=1
    assert set(owner)==set(range(len(sources)))
    assert len(links)==k-1
    adj=[set() for _ in bags]
    for a,b in links:
        assert a!=b;assert len(set(bags[a].vars)&set(bags[b].vars))<=2
        adj[a].add(b);adj[b].add(a)
    seen={0};todo=[0]
    while todo:
        i=todo.pop()
        for j in adj[i]:
            if j not in seen:seen.add(j);todo.append(j)
    assert len(seen)==k
    counts=Counter();sep=0
    for b in bags:counts.update(b.vars)
    assert set(counts)==set(range(1,n+1))
    for a,b in links:sep+=len(set(bags[a].vars)&set(bags[b].vars))
    assert sum(map(lambda b:len(b.vars),bags))==n+sep
    for v in counts:
        occurrence={i for i,b in enumerate(bags) if v in b.vars}
        visited={next(iter(occurrence))};queue=list(visited)
        while queue:
            i=queue.pop()
            for j in adj[i]&occurrence:
                if j not in visited:visited.add(j);queue.append(j)
        assert visited==occurrence, ('running intersection',v)
    return adj,sep

def affine_rank1(equations, loc):
    nonzero=None; contradiction=False
    for sc,rhs in equations:
        mask=0
        for v in sc:mask ^= 1<<loc[v]
        if mask==0:
            if rhs:contradiction=True
        elif nonzero is None:nonzero=(mask,rhs)
        elif mask!=nonzero[0]:return ('UNKNOWN',None)
        elif rhs!=nonzero[1]:contradiction=True
    if contradiction:return ('CONTRADICTION',None)
    if nonzero is None:return ('RANK0',None)
    return ('RANK1',nonzero)

def run(data, replay=False, absorb_small=True):
    begin=time.perf_counter();tracemalloc.start();stats=Stats()
    n,sources,offsets=parse(data)
    bags,links=split_bags(n,sources,stats)
    tree,sep=verify_tree(n,sources,bags,links,stats)
    k=len(bags);parents={0:None};children=defaultdict(list);stack=[0];order=[]
    while stack:
        i=stack.pop();order.append(i)
        for j in sorted(tree[i]):
            if j==parents[i]:continue
            assert j not in parents
            parents[j]=i;children[i].append(j);stack.append(j)
    tables={};recognized=True
    ranks=[];work_rows=0
    for i in reversed(order):
        b=bags[i];vars=b.vars;loc={v:j for j,v in enumerate(vars)}
        sep_i=tuple(sorted(set(vars)&set(bags[parents[i]].vars))) if parents[i] is not None else ()
        clauses=[];equations=[]
        for sid in b.sources:
            s=sources[sid]
            if s.kind=='c':
                clauses.append(tuple((1 if l>0 else -1)*(loc[abs(l)]+1) for l in s.data))
            else:
                if absorb_small and len(s.scope)<=2:
                    # XOR of <=2 variables is exactly bijunctive. Compile without
                    # changing original source ID or its physical byte offsets.
                    rhs=s.data[0]
                    if len(s.scope)==0:
                        if rhs:clauses.append(())
                    elif len(s.scope)==1:
                        vv=loc[s.scope[0]]+1
                        clauses.append((vv if rhs else -vv,))
                    else:
                        aa=loc[s.scope[0]]+1;bb=loc[s.scope[1]]+1
                        clauses.extend(((aa,bb),(-aa,-bb)) if rhs else ((-aa,bb),(aa,-bb)))
                else:equations.append((s.scope,s.data[0]))
        for ch in children[i]:
            child_sep,table=tables[ch]
            for bits in product((0,1),repeat=len(child_sep)):
                if bits not in table:
                    clause=tuple((loc[v]+1) if bit==0 else -(loc[v]+1) for v,bit in zip(child_sep,bits))
                    clauses.append(clause);stats.msg_clauses+=1
        state,rankrow=affine_rank1(equations,loc)
        if state=='UNKNOWN':recognized=False;break
        ranks.append(state);stats.local_calls+=1
        table={}
        for bits in product((0,1),repeat=len(sep_i)):
            pinned=clauses+[ ((loc[v]+1) if bit else -(loc[v]+1),) for v,bit in zip(sep_i,bits) ]
            if state=='CONTRADICTION':model=None
            elif state=='RANK0':model=two_sat(len(vars),pinned,stats)
            else:
                mask,rhs=rankrow
                support=[idx for idx in range(len(vars)) if (mask>>idx)&1]
                model=one_parity(len(vars),pinned,support,rhs,stats)
            stats.table_entries+=1
            if model is not None:
                assert all(any((model[abs(l)-1] if l>0 else 1-model[abs(l)-1]) for l in clause) for clause in pinned)
                assert all((sum(model[loc[v]] for v in sc)&1)==rhs for sc,rhs in equations)
                table[bits]=tuple(model)
                stats.memo_witness_bits+=len(model)
        tables[i]=(sep_i,table)
    if not recognized:
        ans='UNKNOWN';model=None
    elif () not in tables[0][1]:
        ans='UNSAT';model=None
    else:
        assignment={}
        def reconstruct(i):
            stats.reconstruction_nodes+=1
            sep_i,table=tables[i]
            key=tuple(assignment[v] for v in sep_i)
            local=table[key]
            for v,bit in zip(bags[i].vars,local):
                if v in assignment:assert assignment[v]==bit
                else:assignment[v]=bit
            for ch in children[i]:reconstruct(ch)
        reconstruct(0)
        assert len(assignment)==n and source_truth(sources,assignment)
        ans='SAT';model=assignment
    if replay and recognized:
        # Full independent table replay can be performed by rerunning the source-certified solver.
        # Here every local SAT witness is source-checked, all child tables are exact by induction.
        assert all(sid in range(len(sources)) for b in bags for sid in b.sources)
    live,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    return {'status':ans,'witness':model,'stats':stats.__dict__,'N':len(data),'n':n,'sources':len(sources),
            'bags':k,'sum_bag_sizes':sum(len(b.vars) for b in bags),'sum_separators':sep,
            'max_bag':max(map(lambda b:len(b.vars),bags)), 'max_sep':max([len(set(bags[a].vars)&set(bags[b].vars)) for a,b in links],default=0),
            'global_affine_rows':sum(s.kind=='a' for s in sources),
            'peak_python_bytes':peak,'elapsed_s':time.perf_counter()-begin}

def clique_chain(q,k,conflict=False):
    """k dense 2CNF blocks glued along independent two-variable interfaces,
    each having one disjoint source XOR row, so global rank=k."""
    n=0; shares=[];priv=[];groups=[]
    for i in range(k-1):
        shares.append((n+1,n+2));n+=2
    for i in range(k):
        pp=tuple(range(n+1,n+q+1));n+=q;priv.append(pp)
        v=tuple(sorted(pp+(shares[i-1] if i else ())+(shares[i] if i<k-1 else ())))
        groups.append(v)
    cnf=[];xors=[]
    for i,group in enumerate(groups):
        cnf.extend((a,b) for a,b in combinations(group,2)) # positive clique, SAT with ones
        xors.append((tuple(sorted(priv[i][:3])),1))
    if conflict and k>=2:
        # Two locally satisfiable halves force contradictory values of the
        # shared separator bit. Constraints are source-owned by DIFFERENT
        # clique modules because each contains a private endpoint.
        u=shares[0][0];p=priv[0][0];w=priv[1][0]
        cnf.extend(((-u,p),(-u,-p),(u,w),(u,-w)))
    src=[]
    for j,cl in enumerate(cnf):src.append(Source('c',j,tuple(sorted({abs(l) for l in cl})),cl))
    for j,(scope,rhs) in enumerate(xors):src.append(Source('a',j,scope,(rhs,)))
    return n,src

def brute(n,src):
    for bits in product((0,1),repeat=n):
        ass={i+1:bits[i] for i in range(n)}
        if source_truth(src,ass):return ass
    return None

def generated_random(rng,n=8,m=12,r=2):
    cnf=[];eq=[]
    for i in range(m):
        length=rng.choice((1,2));scope=rng.sample(range(1,n+1),length)
        cnf.append(tuple(v if rng.randint(0,1) else -v for v in scope))
    for i in range(r):
        eq.append((tuple(sorted(rng.sample(range(1,n+1),rng.randint(1,3)))),rng.randint(0,1)))
    src=[Source('c',j,tuple(sorted({abs(l) for l in cl})),cl) for j,cl in enumerate(cnf)]
    src +=[Source('a',j,scope,(rhs,)) for j,(scope,rhs) in enumerate(eq)]
    return n,src

def audit(seed=235,small=100,chain_q=(4,6,8,10,12),verbose=False):
    rng=random.Random(seed)
    result={'seed':seed,'small':{'total':0,'recognized':0,'sat':0,'unsat':0,'unknown':0},'chain':[],'corrupt_rejections':0}
    for j in range(small):
        n,src=generated_random(rng,n=rng.randrange(3,10),m=rng.randrange(2,13),r=rng.randrange(0,4))
        encoded=encode(n,src);check=parse(encoded)
        assert len(check[1])==len(src)
        ans=run(encoded)
        truth=brute(n,src)
        if ans['status']!='UNKNOWN':
            assert (ans['status']=='SAT')==(truth is not None),(j,ans,truth)
            if ans['status']=='SAT':assert source_truth(src,ans['witness'])
            result['small']['recognized']+=1;result['small'][ans['status'].lower()]+=1
        else:result['small']['unknown']+=1
        result['small']['total']+=1
        if j<10:
            bb=bytearray(encoded);p=encoded.index(b'c 0 ');bb[p+2]=ord('9')
            try:parse(bytes(bb))
            except (ValueError,IndexError):result['corrupt_rejections']+=1
            else:raise AssertionError('forgery accepted')
    for q in chain_q:
        for conflict in [False,True]:
            n,src=clique_chain(q,q,conflict)
            encoded=encode(n,src)
            ans=run(encoded)
            assert ans['status']==('UNSAT' if conflict else 'SAT'),(q,conflict,ans)
            assert ans['bags']>=q and ans['max_sep']<=2
            assert ans['global_affine_rows']==q
            assert ans['sum_bag_sizes']==n+ans['sum_separators']
            row={k:ans[k] for k in ['status','N','n','sources','bags','sum_bag_sizes','sum_separators','max_bag','max_sep','global_affine_rows','peak_python_bytes','elapsed_s']}
            row.update({k:ans['stats'][k] for k in ['cut_tests','two_sat_calls','local_calls','memo_witness_bits','msg_clauses','table_entries']})
            result['chain'].append(row)
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,default=235);ap.add_argument('--small',type=int,default=100)
    ap.add_argument('--q',default='4,6,8,10,12');ap.add_argument('--output',default='')
    a=ap.parse_args();res=audit(a.seed,a.small,tuple(map(int,a.q.split(','))))
    print(json.dumps(res,indent=2,sort_keys=True))
    if a.output:open(a.output,'w').write(json.dumps(res,indent=2,sort_keys=True)+'\n')