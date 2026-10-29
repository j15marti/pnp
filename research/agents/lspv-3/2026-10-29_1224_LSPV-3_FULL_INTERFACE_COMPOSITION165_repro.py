#!/usr/bin/env python3
"""Dependency-free LSPV-3 full-interface composition test (2026-10-29).

Works constructively for local affine codimension <= 1 by the 2SAT
meet-generator theorem. The report's general constant-codimension extension
invokes Arvind--Guruswami Theorem 17, not this implementation.

All local source constraints are indexed and maintained, and the global
brute-force reference solver is used ONLY in finite independent validation.
"""
import itertools
import json
import random
from collections import defaultdict


def sat_lit(l, a):
    return a[abs(l)] == int(l > 0)


def check_2cnf(cs, a):
    return all(any(sat_lit(l, a) for l in c) for c in cs)


def check_aff(eqs, a):
    return all((sum(a[v] for v in vs) % 2) == rhs for vs, rhs in eqs)


def solve2(vars_, clauses, pins=()):
    """Deterministic 2SAT SCC algorithm, return checked model or None."""
    vs = sorted(set(vars_))
    pos = {v: i for i, v in enumerate(vs)}
    nn = 2 * len(vs)
    g = [[] for _ in range(nn)]
    gr = [[] for _ in range(nn)]

    def vertex(l):
        return 2 * pos[abs(l)] + (0 if l > 0 else 1)

    for c in list(clauses) + [(v if b else -v,) for v, b in pins]:
        if not c:
            return None
        assert len(c) <= 2
        if len(c) == 1:
            x = vertex(c[0]); y = x ^ 1
            g[y].append(x); gr[x].append(y)
        else:
            x, y = vertex(c[0]), vertex(c[1])
            g[x ^ 1].append(y); gr[y].append(x ^ 1)
            g[y ^ 1].append(x); gr[x].append(y ^ 1)
    used = [False] * nn
    order = []
    for v in range(nn):
        if used[v]:continue
        used[v]=True
        stack=[(v,0)]
        while stack:
            z,i=stack[-1]
            if i>=len(g[z]):
                order.append(z);stack.pop();continue
            stack[-1]=(z,i+1)
            u=g[z][i]
            if not used[u]:used[u]=True;stack.append((u,0))
    comp = [-1] * nn
    k = 0
    for v in reversed(order):
        if comp[v] >= 0:continue
        comp[v]=k
        stack=[v]
        while stack:
            z=stack.pop()
            for u in gr[z]:
                if comp[u]<0:comp[u]=k;stack.append(u)
        k+=1
    a = {}
    for v in vs:
        p = vertex(v)
        if comp[p] == comp[p ^ 1]:return None
        a[v] = int(comp[p] > comp[p ^ 1])
    if not check_2cnf(clauses, a) or any(a[v] != b for v,b in pins):
        raise AssertionError(('2SAT implementation error',vs, clauses,pins,a,comp))
    return a


def solve2_one_aff(vars_, clauses, eqs, pins=(), stats=None):
    """Polynomial 2SAT+rank<=1 deterministic model acquisition.

    For each i active relative to an arbitrary 2SAT model a, constructs
    g_i = coordinatewise AND of all (x XOR a) with x_i != a_i.
    Since 2SAT model relations are majority-closed, g_i belongs to the
    XOR-shifted relation, and the g_i span its GF(2) linear span.
    """
    if stats is not None:stats['calls'] += 1
    vs = sorted(set(vars_))
    pins = tuple(sorted(dict(pins).items()))
    if len(eqs) > 1:
        raise ValueError('Implementation requires <= one affine row')
    base = solve2(vs, clauses, pins)
    if stats is not None:stats['two_sat_queries'] += 1
    if base is None:return None
    if not eqs or check_aff(eqs,base):return base
    (mask,rhs), = eqs
    if not mask:return None
    for i in vs:
        # x_i != a_i ensures this set of solutions is nonempty.
        p1 = pins + ((i, 1-base[i]),)
        candidate=solve2(vs,clauses,p1)
        if stats is not None:stats['two_sat_queries'] += 1
        if candidate is None:continue
        gen = {}
        for j in vs:
            p2 = p1 + ((j,base[j]),)
            x = solve2(vs, clauses, p2)
            if stats is not None:stats['two_sat_queries'] += 1
            gen[j] = int(x is None)
        x = {j:base[j]^gen[j] for j in vs}
        assert check_2cnf(clauses,x) and all(x[v] == b for v,b in pins)
        if check_aff(eqs,x):return x
    return None


def root_and_tables(nodes, stats=None, source=None):
    """Nodes: dict records {id,parent,bag,private,clauses,affine}.

    Returns model, table sizes and detailed authenticated witness records.
    Rejects invalid running-intersection or source ownership.
    """
    n=len(nodes)
    children=defaultdict(list)
    roots=[]
    for t,rec in nodes.items():
        p=rec['parent']
        (roots if p is None else children[p]).append(t)
    assert len(roots)==1
    root=roots[0]
    order=[]
    visited=set()
    def dfs(t):
        assert t not in visited
        visited.add(t)
        for c in sorted(children[t]):dfs(c)
        order.append(t)
    dfs(root)
    assert len(visited)==n
    bags={t:set(rec['bag']) for t,rec in nodes.items()}
    # All repeated variables must appear on a connected subtree.
    loc=defaultdict(set)
    for t,bag in bags.items():
        for v in bag:loc[v].add(t)
    for v,sites in loc.items():
        start=min(sites)
        unseen=[start]; reached={start}
        while unseen:
            x=unseen.pop()
            for y in list(children[x]) + ([nodes[x]['parent']] if nodes[x]['parent'] is not None else []):
                if y in sites and y not in reached:reached.add(y);unseen.append(y)
        assert reached == sites
    # Syntactic audit: every source constraint fits in its assigned bag.
    assigned={}
    for t,rec in nodes.items():
        for j,c in enumerate(rec['clauses']):
            assert len(c)<=2 and all(abs(l) in bags[t] for l in c)
            sid=rec.get('clause_ids', [('C',t,u) for u in range(len(rec['clauses']))])[j]
            assert sid not in assigned
            assigned[sid]=('C',tuple(c))
        for j,(mask,rhs) in enumerate(rec['affine']):
            assert all(v in bags[t] for v in mask) and rhs in (0,1)
            sid=rec.get('affine_ids',[('A',t,u) for u in range(len(rec['affine']))])[j]
            assert sid not in assigned
            assigned[sid]=('A',(tuple(mask),rhs))
    # When the original input is supplied, check every original source ID
    # appears exactly once; no omitted or fabricated constraint is accepted.
    if source is not None:assert source==assigned
    # Every private variable has exactly one owner and is not shared.
    privs={v:t for t,rec in nodes.items() for v in rec['private']}
    assert len(privs)==sum(len(rec['private']) for rec in nodes.values())
    for v,t in privs.items():assert loc[v]=={t}
    full_interfaces={t:sorted(bags[t]-set(nodes[t]['private'])) for t in nodes}
    tables={}
    sizes={}
    for t in order:
        rec=nodes[t]
        allv=sorted(bags[t]); B=full_interfaces[t]
        p=rec['parent']
        S=sorted(bags[t]&bags[p]) if p is not None else []
        assert set(S)<=set(B)
        local={}
        for values in itertools.product((0,1), repeat=len(B)):
            pins=dict(zip(B, values))
            # Validate each child table on the FULL overlap.
            ok=True
            ks={}
            for c in children[t]:
                sep=sorted(bags[c]&bags[t])
                sig=tuple(pins[v] for v in sep)
                if sig not in tables[c]:ok=False;break
                ks[c]=sig
            if not ok:continue
            w=solve2_one_aff(allv,rec['clauses'],rec['affine'],pins.items(),stats)
            if w is None:continue
            assert check_2cnf(rec['clauses'],w) and check_aff(rec['affine'],w)
            sig=tuple(pins[v] for v in S)
            if sig not in local:local[sig]={'local':w,'children':ks,'full_sig':tuple(values)}
        tables[t]=local
        sizes[t]=len(local)
    if () not in tables[root]:return None,sizes,tables
    total={}
    def recover(t,sig):
        r=tables[t][sig]
        for v,x in r['local'].items():
            if v in total:assert total[v]==x
            else:total[v]=x
        for c,csig in r['children'].items():recover(c,csig)
    recover(root,())
    assert len(total)==len(loc)
    for rec in nodes.values():
        assert check_2cnf(rec['clauses'],total) and check_aff(rec['affine'],total)
    return total,sizes,tables


def global_brute(nodes):
    allv=sorted({v for x in nodes.values() for v in x['bag']})
    for vec in itertools.product((0,1),repeat=len(allv)):
        a=dict(zip(allv,vec))
        if all(check_2cnf(rec['clauses'],a) and check_aff(rec['affine'],a) for rec in nodes.values()):return a
    return None


def generate(rng,k,star=False,force=False):
    """Randomized SOURCE-owned tree modules with actual shared variables."""
    parents={0:None}
    for t in range(1,k):parents[t]=0 if star else rng.randrange(t)
    edgevar={t:k+t for t in range(1,k)}
    globalvar=2*k
    nodes={}
    for t in range(k):
        bag={t+1,globalvar}
        for u,p in parents.items():
            if p==t:bag.add(edgevar[u])
        if t>0:bag.add(edgevar[t])
        bag=sorted(bag)
        clauses=[]
        # Two-variable clauses include arbitrary local and shared variables.
        for _ in range(rng.randrange(1,7)):
            l=rng.choice(bag);r=rng.choice(bag)
            clauses.append((l if rng.randrange(2) else -l, r if rng.randrange(2) else -r))
        eqs=[]
        if rng.randrange(5)!=0:
            mask=tuple(v for v in bag if rng.randrange(2))
            rhs=rng.randrange(2)
            if mask or force:eqs.append((mask,rhs))
        nodes[t]={'parent':parents[t],'bag':bag,'private':[t+1],
                  'clauses':clauses,'affine':eqs}
    return nodes


def run():
    rng=random.Random(1651029)
    stats={'calls':0,'two_sat_queries':0,'generated_instances':0,'SAT':0,'UNSAT':0,'max_full_boundary':0,'max_table_entries':0,'total_table_entries':0,'star_tests':0,'guard_tests':0}
    # Explicit local affine codim-one oracle independently checked on <=8 vars.
    for n in range(1,9):
        for z in range(150):
            cs=[]
            for j in range(rng.randrange(0,3*n+1)):
                c=tuple((v if rng.randrange(2) else -v) for v in rng.choices(range(1,n+1),k=rng.choice((1,2))))
                cs.append(c)
            mask=tuple(v for v in range(1,n+1) if rng.randrange(2))
            eqs=[(mask,rng.randrange(2))]
            pins=dict((v,rng.randrange(2)) for v in range(1,n+1) if rng.randrange(4)==0)
            csp=cs+[(v if b else -v,) for v,b in pins.items()]
            witness=solve2_one_aff(list(range(1,n+1)),cs,eqs,pins.items(),stats)
            answers=[dict(zip(range(1,n+1),a)) for a in itertools.product((0,1),repeat=n)]
            truth=any(check_2cnf(csp,a) and check_aff(eqs,a) for a in answers)
            assert (witness is not None)==truth
            if witness is not None:assert check_2cnf(csp,witness) and check_aff(eqs,witness)
            stats['guard_tests']+=1
    for k in range(2,7):
        for z in range(75):
            star=(z%2==0)
            nodes=generate(rng,k,star=star)
            source={}
            for t,rec in nodes.items():
                for j,c in enumerate(rec['clauses']):source[('C',t,j)]=('C',tuple(c))
                for j,row in enumerate(rec['affine']):source[('A',t,j)]=('A',(tuple(row[0]),row[1]))
            got,sizes,tables=root_and_tables(nodes,stats,source)
            brute=global_brute(nodes)
            assert (got is not None)==(brute is not None)
            stats['generated_instances']+=1
            stats['SAT' if got is not None else 'UNSAT']+=1
            stats['max_full_boundary']=max(stats['max_full_boundary'],max(len(set(rec['bag'])-set(rec['private'])) for rec in nodes.values()))
            stats['max_table_entries']=max(stats['max_table_entries'],max(sizes.values()))
            stats['total_table_entries']+=sum(sizes.values())
            stats['star_tests']+=int(star)
    # Bad running intersection / unassigned source clause must be rejected.
    bad={0:{'parent':None,'bag':[1,3],'private':[3], 'clauses':[],'affine':[]},
         1:{'parent':0,'bag':[2],'private':[2], 'clauses':[],'affine':[]},
         2:{'parent':1,'bag':[1,4],'private':[4], 'clauses':[],'affine':[]}}
    for variant in range(3):
        changed={t:dict(rec) for t,rec in bad.items()}
        if variant==1:
            # Repair the running-intersection, then introduce a cross-bag clause.
            changed[1]['bag']=[1,2]
            changed[0]['clauses']=[(4,)]
        if variant==2:
            # Correct bags, but original input has an extra unassigned source.
            changed[1]['bag']=[1,2]
            src={('C',9,9):('C',(1,))}
        else:src=None
        try:
            root_and_tables(changed,stats,src)
        except (AssertionError,KeyError):stats.setdefault('malformed_rejected',0);stats['malformed_rejected']+=1
        else:raise AssertionError('invalid certificate structure accepted')
    # Adversarial separator undercount: each edge separator ONE, hub full boundary m.
    # Local model is trivial, yet this *particular enumeration* explores 2^m hub assignments.
    guard=[]
    for m in (4,8,12):
        nodes={0:{'parent':None,'bag':list(range(1,m+1)),'private':[], 'clauses':[],'affine':[]}}
        for i in range(1,m+1):nodes[i]={'parent':0,'bag':[i],'private':[], 'clauses':[(i,)],'affine':[]}
        full=len(set(nodes[0]['bag']))
        sep=max(len(set(nodes[t]['bag']) & set(nodes[0]['bag'])) for t in range(1,m+1))
        guard.append({'m':m,'edge_separator_max':sep,'full_center_boundary':full,'naive_center_assignments':2**full})
    stats['star_separator_guard']=guard
    return stats

if __name__=='__main__':
    r=run()
    print(json.dumps(r,indent=2,sort_keys=True))
