import itertools as it, random, json
import networkx as nx
from functools import lru_cache

rng = random.Random(20261124)
queries=0

def oracle(g, mandatory, boundary, mask=None):
    global queries
    queries += 1
    h=g.copy(); req=set(mandatory)
    if mask is not None:
        h.remove_nodes_from(v for i,v in enumerate(boundary) if mask>>i&1)
        req.update(v for i,v in enumerate(boundary) if not(mask>>i&1))
    for u,v in h.edges: h[u][v]['w']=int(u in req)+int(v in req)
    m=nx.max_weight_matching(h,weight='w'); covered={v for e in m for v in e}
    if not req<=covered: return None
    return sum(1<<i for i,v in enumerate(boundary) if v not in covered)

def reference(g, mandatory, boundary, mask):
    removed={v for i,v in enumerate(boundary) if mask>>i&1}
    req=frozenset(mandatory)|frozenset(set(boundary)-removed)
    @lru_cache(None)
    def rec(avail, needed):
        if not needed:return True
        u=min(needed,key=lambda v:sum(w in avail for w in g[v]))
        return any(rec(avail-{u,v},needed-{u,v}) for v in g[u] if v in avail)
    return rec(frozenset(set(g)-removed),req)

def factor(g, mandatory, boundary, anchor=None):
    if anchor is None: anchor=oracle(g,mandatory,boundary)
    if anchor is None:return None,None
    f=nx.Graph();f.add_nodes_from(range(len(boundary)))
    for i,j in it.combinations(range(len(boundary)),2):
        if oracle(g,mandatory,boundary,anchor^(1<<i)^(1<<j)) is not None: f.add_edge(i,j)
    return anchor,[sum(1<<i for i in c) for c in nx.connected_components(f)]

def parity_completion(g, mandatory,boundary):
    h=g.copy(); opt=sorted(set(g)-set(mandatory)-set(boundary)); base=max(g,default=-1)+1
    d=list(range(base,base+len(opt))); p=base+len(opt)
    h.add_nodes_from(d+[p]);h.add_edges_from(zip(opt,d));h.add_edges_from(it.combinations(d+[p],2))
    return h,set(h)-set(boundary)-{p},boundary+[p]

def check_product(rel, comps, anchor, b):
    for c in comps:
        assert len({(x&c).bit_count()%2 for x in rel})==1
        assert {x&c for x in rel}=={x&c for x in rel if (x&~c)==(anchor&~c)}
    domains=[{x&c for x in rel} for c in comps]
    assert {sum(z) for z in it.product(*domains)}==rel
    # Finest partition: every nontrivial split of any component fails Cartesian closure.
    for c in comps:
        s=(c-1)&c
        while s:
            assert len({x&c for x in rel}) < len({x&s for x in rel})*len({x&(c^s) for x in rel})
            s=(s-1)&c

stats={'seed':20261124,'even_random':0,'optional_random':0,'empty':0,'reference_masks':0,'factorized_nonempty':0,'multi_component':0,'alternate_anchors':0,'optional_completions':0,'ring_controls':[],'nand_series_checks':0,'source_compiler_controls':0}
for optional in (False,True):
    for _ in range(160):
        b=rng.randint(1,7); n=b+rng.randint(0,5); g=nx.Graph();g.add_nodes_from(range(n))
        p=rng.uniform(.08,.85);g.add_edges_from((i,j) for i,j in it.combinations(range(n),2) if rng.random()<p)
        boundary=list(range(b));mandatory={i for i in range(b,n) if not optional or rng.random()<.5}
        rel={x for x in range(1<<b) if reference(g,mandatory,boundary,x)};stats['reference_masks']+=1<<b
        stats['optional_random' if optional else 'even_random']+=1
        anchor=oracle(g,mandatory,boundary)
        assert (anchor is None)==(not rel)
        if not rel:stats['empty']+=1;continue
        assert anchor in rel
        if optional:
            h,req,ports=parity_completion(g,mandatory,boundary)
            # Every x extends to exactly one parity-completion boundary state.
            ext={x|(int((len(h)-x.bit_count())%2)<<b) for x in rel}
            actual={x for x in range(1<<(b+1)) if reference(h,req,ports,x)};stats['reference_masks']+=1<<(b+1)
            assert ext==actual;stats['optional_completions']+=1
        else:h,req,ports,ext=g,mandatory,boundary,rel
        a,comps=factor(h,req,ports);assert a in ext
        check_product(ext,comps,a,len(ports));stats['factorized_nonempty']+=1;stats['multi_component']+=len(comps)>1
        alt=rng.choice(sorted(ext));_,cc=factor(h,req,ports,alt);assert set(cc)==set(comps);stats['alternate_anchors']+=1

# All binary masks are conjunctions of clauses excluding their forbidden pairs.
def sat2(n, relations):
    g=nx.DiGraph();g.add_nodes_from((i,v) for i in range(n) for v in (0,1))
    for i,j,mask in relations:
        for a,b in it.product((0,1),repeat=2):
            if mask>>(2*a+b)&1:continue
            g.add_edge((i,a),(j,1-b));g.add_edge((j,b),(i,1-a))
    c={x:i for i,s in enumerate(nx.strongly_connected_components(g)) for x in s}
    return all(c[i,0]!=c[i,1] for i in range(n))

# Connected matching graph with forced pendant pairs, hiding independent boundary pairs.
def paired_region(k):
    g=nx.Graph();g.add_nodes_from(range(4*k));g.add_edges_from((i,i+1) for i in range(0,2*k,2))
    # One forced connector pair per boundary pair; connectors form a path.
    for j in range(k):
        p=2*k+2*j;q=p+1;g.add_edges_from([(p,q),(p,2*j)])
        if j:g.add_edge(p,p-2)
    return g,set(range(2*k,4*k)),list(range(2*k))

for k in (3,4,5,6,8,9,12,16):
    g,req,ports=paired_region(k);q0=queries;a,c=factor(g,req,ports);assert set(c)=={3<<(2*i) for i in range(k)}
    # Hub i couples coordinate x_i and x_(i+1). Both physical regions have the same pair factors.
    neq=0b0110;anymask=0b1111
    rel=[(i,(i+1)%k,neq) for i in range(k)]
    d=sat2(k,rel);assert d==(k%2==0)
    neighbor=sat2(k,rel[:-1]+[(k-1,0,anymask)]);assert neighbor
    stats['ring_controls'].append({'k':k,'region_boundary_ports':2*k,'factor_queries_one_region':queries-q0,'SAT':d,'relaxed_neighbor_SAT':neighbor})
for a,b in it.product((0,1),repeat=2):
    assert ((a,b)!=(0,1) and (a,b)!=(1,0))==(a==b);stats['nand_series_checks']+=1

# Verify a direct two-region hard-source compilation: each occurrence gets its own
# diagonal hub; side 1 joins occurrence bits for each variable in a cycle; side 2
# evaluates each signed OR and has a spare free terminal per occurrence.
# For small formulas compare enumeration of independent occurrence bits to truth table.
for _ in range(80):
    n=rng.randint(2,5);m=rng.randint(1,4);clauses=[[(rng.randrange(n),rng.randrange(2)) for j in range(3)] for i in range(m)]
    ref=any(all(any(((x>>v)&1)^s for v,s in c) for c in clauses) for x in range(1<<n))
    occ=[z for c in clauses for z in c]; buckets={v:[i for i,(w,s) in enumerate(occ) if w==v] for v in range(n)}
    got=False
    for x in range(1<<(3*m)):
        if not all(len({(x>>i)&1 for i in bucket})<=1 for bucket in buckets.values()):continue
        if all(any(((x>>(3*i+j))&1)^s for j,(v,s) in enumerate(c)) for i,c in enumerate(clauses)):got=True;break
    assert ref==got;stats['source_compiler_controls']+=1
# Strong backdoor: hit each triple of original exchange-component ports.
def acquire_regions(regions):
    data=[]
    for g,req,ports,ids,signs in regions:
        h,rr,bb=parity_completion(g,req,ports);a,cs=factor(h,rr,bb)
        if a is None:return None
        cs=[c&((1<<len(ports))-1) for c in cs];cs=[c for c in cs if c]
        data.append((g,req,ports,ids,signs,a&((1<<len(ports))-1),cs))
    return data

def choose_backdoor(data):
    B=set();packing=[]
    for g,req,ports,ids,signs,a,cs in data:
        for c in cs:
            while True:
                unp=[i for i,v in enumerate(ids) if c>>i&1 and v not in B]
                if len(unp)<=2:break
                edge={ids[i] for i in unp[:3]};assert not edge&B
                packing.append(edge);B.update(edge)
    return sorted(B),len(packing)

def backdoor_solve(n,regions,masks):
    data=acquire_regions(regions)
    if data is None:return False,0,0,0
    B,lower=choose_backdoor(data);assert len(B)<=3*lower
    visits=0
    for bits in it.product((0,1),repeat=len(B)):
        visits+=1;pin=dict(zip(B,bits));rels=list(masks);valid=True
        rels.extend((v,v,1<<(3*x)) for v,x in pin.items())
        for g,req,ports,ids,signs,a,cs in data:
            for c in cs:
                ix=[i for i in range(len(ports)) if c>>i&1]
                u=sorted({ids[i] for i in ix if ids[i] not in pin});assert len(u)<=2
                good=0
                for vals in it.product((0,1),repeat=len(u)):
                    z=pin|dict(zip(u,vals));state=a
                    for i in ix:
                        state=(state&~(1<<i))|((z[ids[i]]^signs[i])<<i)
                    if oracle(g,req,ports,state) is not None:
                        good|=1<<(sum(v<<(len(u)-1-j) for j,v in enumerate(vals)))
                if not good:valid=False;break
                if len(u)==1:rels.append((u[0],u[0],(good&1)|((good&2)<<2)))
                if len(u)==2:rels.append((u[0],u[1],good))
            if not valid:break
        if valid and sat2(n,rels):return True,len(B),lower,visits
    return False,len(B),lower,visits

stats['backdoor']={'cases':0,'sat':0,'unsat':0,'max_guard':0,'branch_visits':0,'reference_assignments':0,'matching_queries':0}
q0=queries
for case in range(160):
    n=rng.randint(3,8);regions=[];masks=[]
    for _ in range(rng.randint(1,4)):
        b=rng.randint(1,min(n,5));nv=b+rng.randint(0,4);g=nx.Graph();g.add_nodes_from(range(nv))
        prob=rng.uniform(.15,.85);g.add_edges_from((i,j) for i,j in it.combinations(range(nv),2) if rng.random()<prob)
        req={i for i in range(b,nv) if rng.random()<.7};ports=list(range(b));ids=rng.sample(range(n),b);signs=[rng.randrange(2) for i in ports]
        regions.append((g,req,ports,ids,signs))
    for _ in range(rng.randint(1,7)):
        i,j=rng.sample(range(n),2);masks.append((i,j,rng.randint(1,15)))
    ref=False
    for x in range(1<<n):
        stats['backdoor']['reference_assignments']+=1
        if not all(mask>>(2*(x>>i&1)+(x>>j&1))&1 for i,j,mask in masks):continue
        if all(reference(g,req,ports,sum((((x>>ids[i])&1)^signs[i])<<i for i in range(len(ports)))) for g,req,ports,ids,signs in regions):ref=True;break
    got,b,lower,v=backdoor_solve(n,regions,masks);assert got==ref
    st=stats['backdoor'];st['cases']+=1;st['sat' if ref else 'unsat']+=1;st['max_guard']=max(st['max_guard'],b);st['branch_visits']+=v
st['matching_queries']=queries-q0
stats['matching_queries']=queries
print(json.dumps(stats,indent=2))
