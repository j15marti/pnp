#!/usr/bin/env python3
"""LSPV-3 BINARY-ADHESION-COMPOSITION166, deterministic exact tree-message audit.

Proves by implementation the *restricted* dynamic program for source-owned
module trees with 0/1/2-variable edge adhesions. Mixed local modules carry
2CNF + at most one affine row (implemented via 2SAT meet generators).
A separate finite-template control uses authenticated proper strict exact22
3CNF source blocks, each at most 17 variables, with exhaustive local solvers.
No unrestricted SAT algorithm or source-to-module compiler is asserted.

Run: python3 2026-10-29_1355_LSPV-3_BINARY_ADHESION_COMPOSITION166_repro.py
The file emits 2026-10-29_1355_BINARY_ADHESION_COMPOSITION166_raw.json alongside itself.
"""
import itertools, json, random, hashlib, pathlib, collections, time

SEED = 1661029
HERE=pathlib.Path(__file__).resolve().parent


def truth(lit, a):
    return a[abs(lit)] == int(lit>0)


def cnf_true(cs, a):
    return all(any(truth(lit,a) for lit in c) for c in cs)


def affine_true(eqs,a):
    return all(sum(a[v] for v in vs)%2 == rhs for vs,rhs in eqs)


def solve_2sat(vs, cls, pins=(), stats=None):
    if stats is not None: stats['two_sat_calls']+=1
    vs=sorted(set(vs)); pos={x:i for i,x in enumerate(vs)}; k=len(vs)
    g=[[] for _ in range(2*k)]; gr=[[] for _ in range(2*k)]
    def vertex(l): return 2*pos[abs(l)]+(0 if l>0 else 1)
    for c in list(cls)+[(v if b else -v,) for v,b in pins]:
        if len(c)==0: return None
        assert 1 <= len(c) <= 2
        if len(c)==1:
            x=vertex(c[0]); y=x^1
            g[y].append(x);gr[x].append(y)
        else:
            x,y=vertex(c[0]),vertex(c[1])
            g[x^1].append(y);gr[y].append(x^1)
            g[y^1].append(x);gr[x].append(y^1)
    seen=set();order=[]
    for x in range(2*k):
        if x in seen: continue
        seen.add(x); stack=[(x,0)]
        while stack:
            v,j=stack[-1]
            if j==len(g[v]):order.append(v);stack.pop();continue
            stack[-1]=(v,j+1);w=g[v][j]
            if w not in seen:seen.add(w);stack.append((w,0))
    comp=[-1]*(2*k); label=0
    for x in reversed(order):
        if comp[x]>=0:continue
        comp[x]=label; stack=[x]
        while stack:
            v=stack.pop()
            for w in gr[v]:
                if comp[w]<0:comp[w]=label;stack.append(w)
        label+=1
    a={}
    for x in vs:
        i=vertex(x)
        if comp[i]==comp[i^1]:return None
        a[x]=int(comp[i]>comp[i^1])
    assert cnf_true(cls,a) and all(a[v]==b for v,b in pins)
    return a


def solve_2cnf_one_aff(vs, cls, eqs, pins=(), stats=None):
    """Known fixed-e local solver, implemented and checked for e<=1.

    The 2SAT solution relation is majority closed. After translating by any
    solution a, it is AND-closed and its meet generators g_i span its GF(2)
    affine hull. Each g_i can be obtained from O(n) pinned 2SAT queries.
    Thus a linear parity functional changes somewhere iff it changes on
    a generator. This certifies YES witness and NO by replayable 2SAT queries.
    """
    if stats is not None:stats['mixed_local_calls']+=1
    vs=tuple(sorted(set(vs))); pins=tuple(sorted(pins))
    if len(eqs)>1:raise ValueError('implementation supports rank <=1')
    if len({v:b for v,b in pins})<len(set(v for v,b in pins)):
        return None
    a=solve_2sat(vs,cls,pins,stats)
    if a is None:return None
    if not eqs or affine_true(eqs,a):return a
    mask,rhs=eqs[0]
    if not mask:return None
    for i in vs:
        pin_i=pins+((i,1-a[i]),)
        if solve_2sat(vs,cls,pin_i,stats) is None: continue
        gen={}
        for j in vs:
            q=solve_2sat(vs,cls,pin_i+((j,a[j]),),stats)
            gen[j]=int(q is None)
        candidate={j:a[j]^gen[j] for j in vs}
        assert cnf_true(cls,candidate) and all(candidate[v]==b for v,b in pins)
        if affine_true(eqs,candidate):return candidate
    return None


def local_bounded3(vs,cls,pins,cache,tid,stats):
    """Brute local bag of constant width, not a global SAT fallback."""
    stats['bounded_local_calls']+=1
    if tid not in cache:
        vs=tuple(sorted(vs)); index={x:i for i,x in enumerate(vs)}
        masks=[]
        for c in cls:
            pm=nm=0
            for lit in c:
                if lit>0:pm|=1<<index[abs(lit)]
                else:nm|=1<<index[abs(lit)]
            masks.append((pm,nm))
        accepted=[]
        for a in range(1<<len(vs)):
            if all((a & p) or (nm & ~a) for p,nm in masks):accepted.append(a)
        cache[tid]=(vs,index,accepted)
        stats['bounded_preprocessing_assignments']+=1<<len(vs)
        stats['bounded_stored_models']+=len(accepted)
    vs,index,models=cache[tid]
    pin_idx=tuple((index[x],b) for x,b in pins)
    for mask in models:
        stats['bounded_candidate_models']+=1
        if all(((mask>>i)&1)==b for i,b in pin_idx):
            a={x:(mask>>i)&1 for i,x in enumerate(vs)}
            assert cnf_true(cls,a)
            return a
    return None


def child_cnf(separator, feasible):
    """Exact <=2-var relation CNF. Every forbidden tuple adds one clause."""
    separator=tuple(sorted(separator)); assert len(separator)<=2
    res=[]
    for bits in itertools.product((0,1), repeat=len(separator)):
        if bits not in feasible:
            res.append(tuple(x if b==0 else -x for x,b in zip(separator,bits)))
    for bits in itertools.product((0,1),repeat=len(separator)):
        a=dict(zip(separator,bits))
        assert cnf_true(res,a)==(bits in feasible)
    return res


def source_map(nodes):
    ans={}
    for tid,t in nodes.items():
        for j,c in enumerate(t['clauses']):
            key=('C',tid,j)
            assert key not in ans;ans[key]=('C',tuple(c))
        for j,e in enumerate(t.get('affine',())):
            key=('A',tid,j)
            assert key not in ans;ans[key]=('A',(tuple(e[0]),e[1]))
    return ans


def validate_tree(nodes,expected,mode,stats):
    stats['discovery_validation_nodes']+=len(nodes)
    keys=set(nodes);root=[t for t in keys if nodes[t]['parent'] is None]
    assert len(root)==1
    children={t:[] for t in keys}
    for t,node in nodes.items():
        p=node['parent']
        if p is not None:
            assert p in keys and p!=t
            children[p].append(t)
    visited=set();post=[]
    def dfs(t):
        assert t not in visited
        visited.add(t)
        for c in sorted(children[t]):dfs(c)
        post.append(t)
    dfs(root[0]);assert visited==keys
    bags={t:set(x['bag']) for t,x in nodes.items()}
    loc=collections.defaultdict(set)
    for t,bag in bags.items():
        assert bag
        for v in bag:loc[v].add(t)
    # Independently verify running intersection for every variable.
    for v,sites in loc.items():
        seed=min(sites);seen={seed};stack=[seed]
        while stack:
            t=stack.pop()
            adj=children[t]+([nodes[t]['parent']] if nodes[t]['parent'] is not None else [])
            for u in adj:
                if u in sites and u not in seen:seen.add(u);stack.append(u)
        assert seen==sites,(v,sites,seen)
    assert source_map(nodes)==expected,'source omitted, duplicated or fabricated'
    for t,node in nodes.items():
        bag=bags[t]
        for c in node['clauses']:
            assert all(abs(x) in bag for x in c)
            assert len(c)<= (2 if node['kind']=='mixed' else 3)
        for mask,b in node.get('affine',()):
            assert set(mask)<=bag and b in (0,1)
        if node['kind']=='mixed':assert len(node.get('affine',()))<=1
        else:assert node['kind']=='bounded3' and len(node['bag'])<=17 and not node.get('affine')
        if node['parent'] is not None:
            sep=bags[t]&bags[node['parent']]
            assert len(sep)<=2,('adhesion exceeds two',t,len(sep))
    return root[0],children,post,bags,loc


def solve_tree(nodes,expected=None,stats=None):
    """One deterministic algorithm with exact child-message composition.

    Output: SAT witness or NO with complete table transcript. Every negative
    table entry is replayable by the polynomial local algorithm, not asserted
    to have a polynomial ordinary-Resolution or LRUP proof.
    """
    if stats is None:stats=collections.Counter()
    if expected is None:expected=source_map(nodes)
    root,children,post,bags,loc=validate_tree(nodes,expected,'auto',stats)
    cache={}; tables={};sep_vars={};steps=[]
    for t in post:
        node=nodes[t];bag=tuple(sorted(bags[t]));parent=node['parent']
        sep=tuple(sorted(bags[t]&bags[parent])) if parent is not None else ()
        sep_vars[t]=sep
        extra=[]
        for c in sorted(children[t]):
            cs=child_cnf(sep_vars[c],set(tables[c]))
            extra.extend(cs)
            stats['derived_child_clauses']+=len(cs)
        assert all(len(c)<=2 for c in extra)
        augmented=list(node['clauses'])+extra
        table={}
        for sig in itertools.product((0,1),repeat=len(sep)):
            pins=list(zip(sep,sig));stats['local_entries_examined']+=1
            if node['kind']=='mixed':
                model=solve_2cnf_one_aff(bag,augmented,node.get('affine',()),pins,stats)
            else:
                model=local_bounded3(bag,augmented,pins,cache,t,stats)
            if model is None:continue
            for c in children[t]:
                s=tuple(model[v] for v in sep_vars[c]);assert s in tables[c]
            assert cnf_true(node['clauses'],model) and affine_true(node.get('affine',()),model)
            table[sig]=model
        tables[t]=table
        steps.append({'node':t,'parent_separator':list(sep),'feasible':[list(x) for x in sorted(table)],
                      'children':sorted(children[t]),'local_kind':node['kind'],
                      'source_clause_count':len(node['clauses']),'source_affine_count':len(node.get('affine',()))})
    if () not in tables[root]:
        return {'status':'UNSAT','tables':tables,'steps':steps,'model':None,'stats':dict(stats)}
    result={}
    def reconstruct(t,sig):
        a=tables[t][sig]
        for v,x in a.items():
            if v in result:assert result[v]==x
            else:result[v]=x
        for c in sorted(children[t]):
            reconstruct(c,tuple(a[v] for v in sep_vars[c]))
    reconstruct(root,())
    assert set(result)==set(loc)
    for node in nodes.values():
        assert cnf_true(node['clauses'],result) and affine_true(node.get('affine',()),result)
    return {'status':'SAT','tables':tables,'steps':steps,'model':result,'stats':dict(stats)}


def brute_global(nodes):
    vs=sorted({v for x in nodes.values() for v in x['bag']})
    assert len(vs)<=16
    for values in itertools.product((0,1),repeat=len(vs)):
        a=dict(zip(vs,values))
        if all(cnf_true(n['clauses'],a) and affine_true(n.get('affine',()),a) for n in nodes.values()):return a
    return None


def random_mixed_tree(rng,k):
    nextvar=1;nodes={}
    for t in range(k):
        if t==0:
            parent=None; sep=[]; numnew=rng.randint(2,3)
        else:
            parent=rng.randrange(t)
            parentbag=nodes[parent]['bag']
            sep=rng.sample(parentbag,k=rng.randint(1,min(2,len(parentbag))))
            numnew=rng.randint(1,2)
        fresh=list(range(nextvar,nextvar+numnew));nextvar+=numnew
        bag=sorted(set(sep+fresh));cs=[]
        for _ in range(rng.randint(0,6)):
            w=rng.randint(1,min(2,len(bag)))
            c=tuple((1 if rng.randrange(2) else -1)*v for v in rng.sample(bag,w))
            cs.append(c)
        aff=[]
        if rng.randrange(3):
            mask=tuple(sorted(rng.sample(bag,rng.randint(1,len(bag)))))
            aff=[(mask,rng.randrange(2))]
        nodes[t]={'parent':parent,'bag':bag,'kind':'mixed','clauses':cs,'affine':aff}
    return nodes


def wide_star(m, root_affine=False, contrary=False):
    """m binary adhesions, central total shared boundary 2m, yet O(m) messages.

    Child projects an XOR3 + unit-w=0 to equality or inequality on a,b.
    Root has only 2CNF, optionally one long parity equation.
    """
    bag=list(range(1,2*m+1)); cs=[]
    for j in range(m):
        a,b=2*j+1,2*j+2
        cs.append((a,));
        if contrary and j==0:cs.append((-b,))
        else:cs.append((b,))
    aff=[(tuple(bag),0)] if root_affine else []
    nodes={0:{'parent':None,'bag':bag,'kind':'mixed','clauses':cs,'affine':aff}}
    for j in range(m):
        a,b=2*j+1,2*j+2; w=2*m+j+1
        # choose XOR parity 0 if root sets both a,b true, parity 1 in contrary first leaf
        rhs=0
        nodes[j+1]={'parent':0,'bag':[a,b,w],'kind':'mixed','clauses':[(-w,)],
                    'affine':[((a,b,w),rhs)]}
    return nodes

# Prior SOURCE-RUP-CHAIN164 immutable source clauses, reproduced verbatim.
G=[(-5,-12,15),(-5,-6,-15),(-4,-9,-11),(-4,-8,-11),(-3,6,-15),
   (-3,12,15),(-2,-6,12),(-2,5,-12),(-1,3,-14),(-1,13,14),
   (1,-7,10),(1,7,13),(2,-9,11),(2,-8,9),(3,7,-13),
   (4,8,-10),(4,9,-10),(5,8,-14),(6,-7,11),(10,-13,14)]
NEG_SLOTS={0:(2,3),1:(15,16)}

def build_strict22_chain(modes, tuples=None):
    k=len(modes);assert k>=2
    blocks=[]
    for i,mode in enumerate(modes):
        off=15*i;bl=[]
        for c in G:
            bl.append([(1 if x>0 else -1)*(-1 if mode and abs(x)==4 else 1)*(abs(x)+off) for x in c])
        blocks.append(bl)
    for i in range(k-1):
        il=NEG_SLOTS[modes[i]][1];ir=NEG_SLOTS[modes[i+1]][0]
        a=-4-15*i;b=-4-15*(i+1)
        assert a in blocks[i][il] and b in blocks[i+1][ir]
        blocks[i][il][blocks[i][il].index(a)]=b
        blocks[i+1][ir][blocks[i+1][ir].index(b)]=a
    nodes={}
    for i in range(k):
        bag=set(range(1+15*i,16+15*i))
        if i>0:bag.add(4+15*(i-1))
        if i+1<k:bag.add(4+15*(i+1))
        cs=[tuple(c) for c in blocks[i]]
        if tuples is not None:
            t=tuples[i]
            for v,bit in zip((1,2,13),((t>>j)&1 for j in range(3))):
                x=v+15*i;cs.append((x if bit else -x,))
        nodes[i]={'parent':i-1 if i else None,'bag':sorted(bag),
                  'kind':'bounded3','clauses':cs,'affine':[]}
    original=[tuple(c) for bl in blocks for c in bl]
    occ=collections.Counter(x for c in original for x in c)
    assert all(occ[v]==occ[-v]==2 for v in range(1,15*k+1))
    assert all(len(c)==len({abs(x) for x in c})==3 for c in original)
    adj=collections.defaultdict(set)
    for c in original:
        for x in c:
            for y in c:adj[abs(x)].add(abs(y))
    seen={1};stack=[1]
    while stack:
        for u in adj[stack.pop()]-seen:seen.add(u);stack.append(u)
    assert len(seen)==15*k
    return nodes


def exact_binary_consequence_cnf(separator, feasible):
    """Strongest 2CNF on the separator; report whether it is lossless.

    For s=O(log N), the comparison with the exact full relation is
    polynomial; for s>2, the compressed relation may overapproximate.
    """
    separator=tuple(separator); n=len(separator); feasible=set(feasible)
    clauses=[]
    for width in (1,2):
        for inds in itertools.combinations(range(n),width):
            for values in itertools.product((0,1),repeat=width):
                if not any(all(row[i]==v for i,v in zip(inds,values)) for row in feasible):
                    clauses.append(tuple(separator[i] if v==0 else -separator[i]
                                         for i,v in zip(inds,values)))
    if not feasible: clauses.append(())
    equivalent=True
    for bits in itertools.product((0,1),repeat=n):
        assignment=dict(zip(separator,bits))
        if cnf_true(clauses,assignment)!=(bits in feasible):equivalent=False
    return clauses,equivalent

def majority(xs):
    return tuple(int(sum(row[i] for row in xs)>=2) for i in range(len(xs[0])))


def ternary_obstruction():
    # Three-bit even and odd parity are distinct child messages. Every 1/2-bit
    # projection is full, so retaining only binary consequences accepts an
    # inconsistent pair of parity constraints when both are joined.
    R0={b for b in itertools.product((0,1),repeat=3) if sum(b)%2==0}
    R1={b for b in itertools.product((0,1),repeat=3) if sum(b)%2==1}
    for R in (R0,R1):
        for inds in itertools.combinations(range(3),2):
            assert {tuple(b[i] for i in inds) for b in R}==set(itertools.product((0,1),repeat=2))
    w=(0,0,0),(1,1,0),(1,0,1)
    assert all(x in R0 for x in w) and majority(w)==(1,0,0) and majority(w) not in R0
    assert R0.isdisjoint(R1)
    assert not exact_binary_consequence_cnf((1,2,3),R0)[1]
    assert not exact_binary_consequence_cnf((1,2,3),R1)[1]
    # A higher-arity bijunctive relation, by contrast, compiles exactly.
    equality={(0,0,0),(1,1,1)}
    assert exact_binary_consequence_cnf((1,2,3),equality)[1]
    return {'even':sorted([list(t) for t in R0]),'odd':sorted([list(t) for t in R1]),
            'binary_closure_of_each':'tautology','actual_join':'UNSAT',
            'binary_approximated_join':'SAT','majority_counterexample':[list(t) for t in w]}


def run():
    rng=random.Random(SEED);stats=collections.Counter();records=[]
    for rep in range(270):
        nodes=random_mixed_tree(rng,rng.randint(1,5))
        output=solve_tree(nodes,source_map(nodes),stats)
        ref=brute_global(nodes)
        assert (ref is not None)==(output['status']=='SAT'),(rep,nodes,output)
        if ref is not None:assert all(cnf_true(x['clauses'],output['model']) and affine_true(x['affine'],output['model']) for x in nodes.values())
        records.append(output['status'])
    # Two-child and multi-edge wide stars: full center boundary grows linearly;
    # child summaries remain exact 2CNFs with no 2^m center enumeration.
    star=[]
    for m,ra,contra in [(8,False,False),(8,False,True),(12,True,False),(12,True,True),(64,False,False),(64,False,True)]:
        nodes=wide_star(m,ra,contra)
        res=solve_tree(nodes,source_map(nodes),stats)
        assert res['status']==('UNSAT' if contra or (ra and m%2) else 'SAT')
        root_seen={v for x in nodes.values() if x is not nodes[0] for v in x['bag'] if v in nodes[0]['bag']}
        assert len(root_seen)==2*m
        assert res['stats']['local_entries_examined']-0>0
        star.append({'leaves':m,'root_affine':ra,'contrary':contra,'status':res['status'],
                     'root_full_shared_interface':len(root_seen),'max_edge_adhesion':2,
                     'entries_total_at_most':4*(m+1)})
    # Physical strict22 roots and their ordinary pinned cofactors.
    strict=[]
    for modes,tuples in [((0,0),None),((0,1),None),((0,0),(1,1)),((0,1),(1,1)),((1,0),(1,1)),((0,1,0),(1,1,1)),((0,0,0),(1,1,1))]:
        nodes=build_strict22_chain(modes,tuples)
        result=solve_tree(nodes,source_map(nodes),stats)
        expected='UNSAT' if tuples is not None and len(set(modes))>1 else 'SAT'
        # A 3-block 010 pattern has conflicting t=1 port requirements.
        assert result['status']==expected,(modes,tuples,result['status'])
        strict.append({'modes':list(modes),'cofactor_tuples':list(tuples) if tuples is not None else None,
                       'status':result['status'],'root_strict22':tuples is None,
                       'n':15*len(modes),'source_ternary_clauses':20*len(modes),
                       'max_bag':max(len(x['bag']) for x in nodes.values()),
                       'max_edge_adhesion':2})
    # Validator hostile controls.
    base=random_mixed_tree(random.Random(711),3); src=source_map(base)
    bad=__import__('copy').deepcopy(base)
    bad[0]['clauses'].append((999,))
    try:solve_tree(bad,src)
    except AssertionError:stats['tamper_rejected']+=1
    else:raise AssertionError('fabricated source clause was accepted')
    bad=__import__('copy').deepcopy(base)
    if 1 in bad and bad[1]['parent'] is not None:
        bad[0]['bag']=sorted(set(bad[0]['bag'])|{501,502,503})
        bad[1]['bag']=sorted(set(bad[1]['bag'])|{501,502,503})
    try:solve_tree(bad,src)
    except AssertionError:stats['tamper_rejected']+=1
    else:raise AssertionError('over-wide separator was accepted')
    # An incorrect child table would be caught by independently recomputing.
    control={'seed':SEED,'status':'COMPUTATIONAL implementation; theorem proved separately',
             'random_mixed_cases':len(records),'random_sat':records.count('SAT'),
             'random_unsat':records.count('UNSAT'),
             'star_cases':star,'strict22_controls':strict,
             'ternary_obstruction':ternary_obstruction(),
             'stats':dict(sorted(stats.items())),
             'no_unrestricted_SAT_claim':True,'local_codimension_implemented':1}
    return control

if __name__=='__main__':
    output=run()
    p=HERE/'2026-10-29_1355_BINARY_ADHESION_COMPOSITION166_raw.json'
    p.write_text(json.dumps(output,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k not in ('star_cases','strict22_controls','ternary_obstruction')},sort_keys=True,indent=2))
    print('RAW',p)