#!/usr/bin/env python3
"""ARC234. Exact mixed (2CNF + XOR) block-cut solver at LOCAL GF(2) rank <=1.

Self-contained deterministic source-authenticated prototype. 2SAT and parity
minimal-generator proof follow ARC227, independently reimplemented here.
The rank-e generalization invokes the KNOWN Arvind--Guruswami 2021 theorem;
this executable implements e<=1 only, and returns UNKNOWN for e>=2 blocks.
Python counts are NOT Turing-machine time or space measurements.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, math, random, time, tracemalloc
from collections import defaultdict, Counter
from dataclasses import dataclass
import networkx as nx


def encode(n, cnf, xor):
    lines = [f'p mix {n} {len(cnf)} {len(xor)}\n']
    lines.extend(f'v {i}\n' for i in range(1,n+1))  # explicit variable roster, n <= input bytes
    for i, cl in enumerate(cnf):
        lines.append('c ' + str(i) + ' ' + ' '.join(map(str, cl)) + ' 0\n')
    for i, (scope, rhs) in enumerate(xor):
        lines.append('a ' + str(i) + ' ' + str(rhs) + ' ' + ' '.join(map(str, scope)) + ' 0\n')
    return ''.join(lines).encode('ascii')


def parse(data):
    lines = data.decode('ascii').splitlines(keepends=True)
    h = lines[0].strip().split()
    if len(h) != 5 or h[:2] != ['p', 'mix']:
        raise ValueError('header')
    n, c, a = map(int, h[2:])
    if n < 0 or len(lines) != 1+n+c+a:
        raise ValueError('size')
    for i, line in enumerate(lines[1:1+n],start=1):
        if line != f'v {i}\n': raise ValueError('explicit variable roster')
    cnf, xor, offsets = [], [], []
    off = sum(len(x) for x in lines[:1+n])
    for i, line in enumerate(lines[1+n:]):
        v = line.split(); typ = 'c' if i < c else 'a'
        if len(v) < 3 or v[0] != typ or int(v[1]) != (i if i<c else i-c) or v[-1] != '0':
            raise ValueError('source id')
        if typ == 'c':
            clause = tuple(map(int, v[2:-1]))
            if len(clause)>2 or any(k == 0 or abs(k)>n for k in clause):
                raise ValueError('not 2CNF')
            cnf.append(clause)
        else:
            if len(v)<4:raise ValueError('affine row')
            rhs = int(v[2]); scope=tuple(map(int, v[3:-1]))
            if rhs not in (0,1) or any(k<1 or k>n for k in scope) or len(set(scope))!=len(scope) or tuple(sorted(scope))!=scope:
                raise ValueError('affine row')
            xor.append((scope,rhs))
        offsets.append((typ,i if i<c else i-c,off))
        off += len(line)
    if encode(n, cnf, xor)!=data:
        raise ValueError('noncanonical encoding')
    return n,cnf,xor,offsets


def truth(n,cnf,xor,mask):
    if any(not any((bool(mask&(1<<(abs(l)-1))) if l>0 else not bool(mask&(1<<(abs(l)-1)))) for l in cl) for cl in cnf):
        return False
    for scope,rhs in xor:
        if (sum(bool(mask & (1<<(v-1))) for v in scope)%2)!=rhs:return False
    return True


@dataclass
class Meter:
    calls:int=0
    edges:int=0
    parity_gen:int=0
    local_queries:int=0
    parsed_bytes:int=0
    owned_sources:int=0
    stored_witness_bits:int=0


def twosat(n,clauses,meter):
    meter.calls += 1
    g=[[] for _ in range(2*n)]; rg=[[] for _ in range(2*n)]
    def idx(l): return 2*(abs(l)-1) +(l<0)
    def edge(a,b):
        g[a].append(b);rg[b].append(a);meter.edges+=1
    for cl in clauses:
        if len(cl)==0:return None
        if len(cl)>2:raise ValueError('not 2CNF')
        a=idx(cl[0])
        if len(cl)==1:edge(a^1,a)
        else:
            b=idx(cl[1]);edge(a^1,b);edge(b^1,a)
    seen=[False]*(2*n);order=[]
    for st in range(2*n):
        if seen[st]:continue
        stack=[(st,0)];seen[st]=True
        while stack:
            v,p=stack[-1]
            if p==len(g[v]):order.append(v);stack.pop();continue
            stack[-1]=(v,p+1);w=g[v][p]
            if not seen[w]:seen[w]=True;stack.append((w,0))
    comp=[-1]*(2*n);cc=0
    for st in reversed(order):
        if comp[st]!=-1:continue
        stck=[st];comp[st]=cc
        while stck:
            v=stck.pop()
            for w in rg[v]:
                if comp[w]<0:comp[w]=cc;stck.append(w)
        cc+=1
    for i in range(n):
        if comp[2*i]==comp[2*i+1]:return None
    assignment=tuple(int(comp[2*i]>comp[2*i+1]) for i in range(n))
    assert all(any((assignment[abs(l)-1] if l>0 else 1-assignment[abs(l)-1]) for l in c) for c in clauses)
    return assignment


def oneparity(n,clauses,support,rhs,meter):
    """Based on ARC227's Horn-minimal-generator construction; source rechecked."""
    base=twosat(n,clauses,meter)
    if base is None:return None
    def par(x):return sum(x[i] for i in support)&1
    if par(base)==rhs:return base
    # Flip coordinates relative to base. Every clause now satisfied by zero,
    # so the shifted formula is Horn 2CNF, closed under AND.
    for i in range(n):
        opp=(i+1 if base[i]==0 else -(i+1))
        if twosat(n,[*clauses,(opp,)],meter) is None:continue
        g=[base[j] for j in range(n)]
        for j in range(n):
            keep=(j+1 if base[j] else -(j+1))
            if twosat(n,[*clauses,(opp,),(keep,)],meter) is None:
                g[j]^=1
        meter.parity_gen+=1
        assert g[i]!=base[i]
        assert all(any((g[abs(l)-1] if l>0 else 1-g[abs(l)-1]) for l in c) for c in clauses)
        if par(g)==rhs:return tuple(g)
    return None


def rank01(scopes,rhs,names):
    """Affine rank 0 or 1, with all dependent consistency checks.
    Return (0,None) or (1,(local support,rhs)) or (None,None) for contradictory.
    """
    loc={v:i for i,v in enumerate(names)}
    row=None
    for scope,b in zip(scopes,rhs):
        mask=0
        for v in scope:mask^=1<<loc[v]
        if mask==0:
            if b:return None,None
            continue
        if row is None:row=(mask,b)
        elif row!=(mask,b):
            if row[0]==mask:return None,None
            return 2,None
    if row is None:return 0,None
    return 1,([i for i in range(len(names)) if row[0]>>i&1],row[1])


def block_cut(n,cnf,xor):
    g=nx.Graph();g.add_nodes_from(range(1,n+1))
    sources=[('c',i,cl,tuple(sorted(set(abs(x) for x in cl)))) for i,cl in enumerate(cnf)]
    sources += [('a',i,(scope,rhs),scope) for i,(scope,rhs) in enumerate(xor)]
    for _,_,_,scope in sources:
        for u,v in itertools.combinations(scope,2):g.add_edge(u,v)
    blocks=[set(c) for c in nx.biconnected_components(g)]
    blocks.extend([{v} for v in g if g.degree(v)==0])
    if not blocks and n==0:blocks=[set()]
    belongs=defaultdict(list)
    for i,b in enumerate(blocks):
        for v in b:belongs[v].append(i)
    owner=defaultdict(list)
    for typ,i,body,scope in sources:
        if scope:
            candidates=[j for j in belongs[scope[0]] if set(scope)<=blocks[j]]
            if len(scope)>=2 and len(candidates)!=1:raise AssertionError(('scope crosses block',scope,candidates))
            if not candidates:raise AssertionError(('unowned source',typ,i))
            j=min(candidates)
        else:j=0
        owner[j].append((typ,i))
    for j,ids in owner.items():
        assert len(ids)==len(set(ids))
    assert sum(len(v) for v in owner.values())==len(sources)
    # Block-cut forest via an undirected bipartite graph, with articulation-only vertices.
    tree=nx.Graph();tree.add_nodes_from(('b',i) for i in range(len(blocks)))
    for v,js in belongs.items():
        if len(js)>=2:
            node=('v',v);tree.add_node(node)
            for j in js:tree.add_edge(('b',j),node)
    assert nx.is_forest(tree)
    roots=[];parent={};children=defaultdict(list)
    for component in nx.connected_components(tree):
        root=min(j for kind,j in component if kind=='b'); roots.append(root)
        queue=[('b',root)]; seen={('b',root)}; par={('b',root):None}
        while queue:
            p=queue.pop(0)
            for q in tree[p]:
                if q in seen:continue
                seen.add(q);par[q]=p;queue.append(q)
                if q[0]=='b':
                    assert p[0]=='v'
                    ancestor=par[p]
                    assert ancestor[0]=='b'
                    bchild=q[1]; bparent=ancestor[1]; v=p[1]
                    parent[bchild]=(bparent,v)
                    children[bparent].append((bchild,v))
    assert sum(map(len,blocks))==n+len(blocks)-len(roots), 'exact block-bag identity'
    return blocks,owner,roots,children,parent,tree,g


def solve_encoded(data,cap=1):
    n,cnf,xor,offsets=parse(data)
    blocks,owner,roots,children,parent,tree,g=block_cut(n,cnf,xor)
    meter=Meter(parsed_bytes=len(data),owned_sources=len(offsets))
    bag_occ=sum(map(len,blocks))
    bag_stats={'block_bag_occurrences':bag_occ,'block_bag_identity_rhs':n+len(blocks)-len(roots),
               'max_cached_witness_bits':2*bag_occ,'connected_components':len(roots)}
    stored={}; ranks=[]; status='SAT'
    visited=[]
    def visit(b):
        nonlocal status
        for child,_ in children[b]:visit(child)
        names=sorted(blocks[b]);local={v:i+1 for i,v in enumerate(names)}
        rows=[xor[i] for typ,i in owner[b] if typ=='a']
        rank,pdata=rank01([r[0] for r in rows],[r[1] for r in rows],names)
        ranks.append((b,rank))
        if rank==2:
            status='UNKNOWN';return
        if any(child not in stored for child,_ in children[b]):return
        clauses=[tuple((local[abs(l)] if l>0 else -local[abs(l)]) for l in cnf[i]) for typ,i in owner[b] if typ=='c']
        for child,v in children[b]:
            feasible=set(stored[child])
            if not feasible:clauses.append(())
            if feasible=={0}:clauses.append((-local[v],))
            if feasible=={1}:clauses.append((local[v],))
        pins=(None,) if b not in parent else (0,1)
        outcome={}
        for val in pins:
            current=list(clauses)
            if val is not None:
                vv=parent[b][1];current.append(((local[vv] if val else -local[vv]),))
            meter.local_queries += 1
            if rank is None:ans=None
            elif rank==0:ans=twosat(len(names),current,meter)
            else:ans=oneparity(len(names),current,*pdata,meter)
            if ans is not None:
                out={v:ans[j] for j,v in enumerate(names)}
                for typ,i in owner[b]:
                    if typ=='c':
                        assert any(out[abs(l)] if l>0 else 1-out[abs(l)] for l in cnf[i])
                    else:
                        sc,rhs=xor[i];assert sum(out[v] for v in sc)%2==rhs
                outcome[0 if val is None else val]=out
                meter.stored_witness_bits += len(names)
        stored[b]=outcome;visited.append(b)
    for r in roots:visit(r)
    if status=='UNKNOWN':return {'status':'UNKNOWN','meter':meter.__dict__,'blocks':len(blocks),**bag_stats,'max_rank':max(z[1] for z in ranks if z[1] is not None)},None
    if any(not stored[r] for r in roots):
        return {'status':'UNSAT','meter':meter.__dict__,'blocks':len(blocks),**bag_stats,'primal_edges':g.number_of_edges(),'max_rank':max([z[1] for z in ranks if z[1] is not None],default=0)},None
    ans={}
    def glue(b,key):
        for v,x in stored[b][key].items():
            if v in ans:assert ans[v]==x
            ans[v]=x
        for child,v in children[b]:glue(child,ans[v])
    for r in roots:glue(r,0)
    mask=sum(bit<<(v-1) for v,bit in ans.items())
    assert truth(n,cnf,xor,mask)
    return {'status':'SAT','meter':meter.__dict__,'blocks':len(blocks),**bag_stats,'primal_edges':g.number_of_edges(),'max_rank':max([z[1] for z in ranks if z[1] is not None],default=0)},ans


def path_clique(k,q,contradict=False):
    """Connected path of k biconnected clique blocks with one xor row each.
    Global affine rank =k. Every clique has q+2 vertices, so tw>=q+1.
    Each adjacent pair shares one articulation variable.
    """
    n=k+1+k*q
    a=list(range(1,k+2));blocks=[]
    for j in range(k):
        priv=list(range(k+2+j*q,k+2+(j+1)*q))
        blocks.append([a[j],a[j+1],*priv])
    cnf=[];xor=[]
    for j,b in enumerate(blocks):
        for x,y in itertools.combinations(b,2):cnf.append((x,y))
        # Force private XOR leg to one; each row then forces equality of a_j,a_j+1
        cnf.append((b[2],))
        xor.append(((b[0],b[1],b[2]),0 if (contradict and j==k-1) else 1))
    cnf.extend([(a[0],),(a[-1],)])
    return encode(n,cnf,xor)


def exact_brute(data):
    n,cnf,xor,_=parse(data)
    for mask in range(1<<n):
        if truth(n,cnf,xor,mask):return True
    return False


def test(seed=2332026,random_trials=360):
    rng=random.Random(seed)
    metrics={'random':{'count':0,'sat':0,'unsat':0,'unknown':0},'family':[],'hostile':{},'projection':{},'seed':seed}
    deletion_tests=0
    # Independent exhaustive e=1 audit on every 2-variable CNF over the 8
    # distinct unit/binary clauses, every parity support, and both RHS bits.
    primitive=[(1,),(-1,),(2,),(-2,),(1,2),(1,-2),(-1,2),(-1,-2)]
    exhaustive=0
    for clause_mask in range(1<<len(primitive)):
        cs=[primitive[j] for j in range(len(primitive)) if clause_mask>>j&1]
        for supp_mask in range(4):
            supp=[j for j in range(2) if supp_mask>>j&1]
            for rhs in (0,1):
                meter=Meter()
                got=oneparity(2,cs,supp,rhs,meter)
                feasible=any(truth(2,cs,[(tuple(j+1 for j in supp),rhs)],a) for a in range(4))
                assert (got is not None)==feasible,(cs,supp,rhs,got)
                exhaustive+=1
    metrics['independent_oneparity_2var_exhaustive']=exhaustive
    # Tiny arbitrary mixed sources, only compare recognized cases (rank<=1 in each block).
    for j in range(random_trials):
        n=rng.randint(2,8)
        cnf=[];xor=[]
        for _ in range(rng.randint(0,10)):
            vars_=rng.sample(range(1,n+1),rng.randint(1,2))
            cnf.append(tuple(x if rng.getrandbits(1) else -x for x in vars_))
        for _ in range(rng.randint(0,3)):
            vars_=tuple(sorted(rng.sample(range(1,n+1),rng.randint(1,min(3,n)))))
            xor.append((vars_,rng.getrandbits(1)))
        data=encode(n,cnf,xor)
        r,w=solve_encoded(data)
        if r['status']=='UNKNOWN':metrics['random']['unknown']+=1;continue
        expected=exact_brute(data)
        assert (r['status']=='SAT')==expected,(j,cnf,xor,r)
        metrics['random']['count']+=1
        metrics['random']['sat' if expected else 'unsat']+=1
        if rng.random()<.55:
            subset_cnf=[x for x in cnf if rng.getrandbits(1)]
            subset_xor=[x for x in xor if rng.getrandbits(1)]
            reduced=encode(n,subset_cnf,subset_xor)
            rr,_=solve_encoded(reduced)
            assert rr['status']!='UNKNOWN', ('source-deletion heredity violation',cnf,xor,rr)
            assert (rr['status']=='SAT')==exact_brute(reduced)
            deletion_tests+=1
    metrics['random']['recognized_deletion_tests']=deletion_tests
    # Large family, complete source/cert validation and same-run counts.
    for k,q in [(2,3),(4,5),(8,7),(16,10),(24,14)]:
        for c in (False,True):
            data=path_clique(k,q,c)
            t0=time.perf_counter();tracemalloc.start()
            r,w=solve_encoded(data)
            current,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
            r.update({'k':k,'q':q,'n':parse(data)[0],'bytes':len(data),
                      'global_affine_rank':k,'primal_tw_lower':q+1,
                      'contradict':c,'wall_seconds':round(time.perf_counter()-t0,5),
                      'python_tracemalloc_peak_bytes':peak})
            assert (r['status']=='UNSAT')==c,r
            metrics['family'].append(r)
    # Empty, contradictory and disconnected controls.
    examples=[(3,[(1,),(-1,)],[]),(3,[],[((1,2),0),((1,2),1)]),(3,[],[((1,2),0)]),(3,[(1,),(2,)],[])]
    for n,cnf,xor in examples:
        data=encode(n,cnf,xor);r,w=solve_encoded(data)
        assert r['status']==('SAT' if exact_brute(data) else 'UNSAT')
    # Full-interface fallacy: messages across every articulation are unary, even
    # when all global equations are independent and each clique is wide.
    metrics['hostile']['examples']=len(examples)
    # Rounding / Pareto structural proxy checks.
    n=1200
    pts=[{'b':b,'q':max(0,math.ceil(n/(12*b)-1/4-1e-12))} for b in range(1,n+1)]
    for p in pts:p['Texp']=p['b']+p['q'];p['Sexp']=p['b']
    min_t=min(x['Texp'] for x in pts)
    equal=[x['b'] for x in pts if x['Texp']==min_t]
    first_equal_space=next(x['b'] for x in pts if x['Texp']==x['Sexp'])
    pareto=[p for p in pts if not any(z['Texp']<=p['Texp'] and z['Sexp']<=p['Sexp'] and (z['Texp']<p['Texp'] or z['Sexp']<p['Sexp']) for z in pts)]
    assert min_t==20 and equal==[9,10,11] and first_equal_space==400
    metrics['projection']={'n':n,'min_Texponent':min_t,'b_at_Tmin':equal,'first_q0_b':first_equal_space,
                           'pareto':pareto,'continuous_bstar':math.sqrt(n/12),
                           'normalized_N0':n*math.ceil(math.log2(n+1)),
                           'tau_proxy_at_b9':20/math.log2(n*math.ceil(math.log2(n+1))),
                           'sigma_proxy_at_b9':9/math.log2(n*math.ceil(math.log2(n+1)))}
    return metrics


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=2332026);p.add_argument('--trials',type=int,default=360);p.add_argument('--out',default='ARC234_results.json')
    a=p.parse_args()
    results=test(a.seed,a.trials)
    with open(a.out,'w') as f:json.dump(results,f,indent=2,sort_keys=True)
    print('PASS: random',results['random'],'family cases',len(results['family']),'frontier',results['projection']['min_Texponent'])