from itertools import combinations
from collections import Counter, defaultdict

# SWITCH-LITERAL-NULL5
# Exact finite hostile test for literal-labelled contact DAGs on D(4,8).
#
# D(4,8) can be identified with choosing 8 of the 32 edges of Q4.
# UNSAT iff the chosen edges form a perfect matching.
# SAT iff some Q4 vertex has degree != 1.
#
# We test:
# 1. safe literal-conjunction certificates of length <=4;
# 2. the x / not-x null-fork wrapper that destroys raw cut-width invariance;
# 3. an explicit 48-contact all-negative read-once switch DAG for SAT;
# 4. exhaustive correctness on all C(32,8)=10,518,300 promised inputs.

def q4():
    edges=[]; idx={}
    for v in range(16):
        for d in range(4):
            w=v^(1<<d)
            if v<w:
                idx[(v,w)]=len(edges)
                edges.append((v,w,d))
    stars=[]
    for v in range(16):
        st=[]
        for d in range(4):
            a,b=sorted((v,v^(1<<d)))
            st.append(idx[(a,b)])
        stars.append(tuple(st))
    return edges,idx,stars

EDGES,IDX,STARS=q4()

def perfect_matchings():
    adj=[[] for _ in range(16)]
    for e,(u,v,d) in enumerate(EDGES):
        adj[u].append((v,e)); adj[v].append((u,e))
    out=[]
    def rec(rem,chosen):
        if not rem:
            m=0
            for e in chosen: m|=1<<e
            out.append(m); return
        u=min(rem)
        for v,e in adj[u]:
            if v in rem:
                rec(rem-{u,v},chosen+[e])
    rec(set(range(16)),[])
    return out

PMS=perfect_matchings()
assert len(PMS)==272

def safe_term(pos,neg):
    pm=0; nm=0
    for e in pos: pm|=1<<e
    for e in neg: nm|=1<<e
    return not any((F&pm)==pm and (F&nm)==0 for F in PMS)

def minimal_safe_terms_upto4():
    ans=Counter()
    examples={}
    for k in range(1,5):
        for vs in combinations(range(32),k):
            for signmask in range(1<<k):
                pos=[vs[i] for i in range(k) if (signmask>>i)&1]
                neg=[vs[i] for i in range(k) if not ((signmask>>i)&1)]
                if not safe_term(pos,neg): continue
                minimal=True
                for j,e in enumerate(vs):
                    p2=pos.copy(); n2=neg.copy()
                    if e in p2: p2.remove(e)
                    else: n2.remove(e)
                    if safe_term(p2,n2):
                        minimal=False; break
                if minimal:
                    key=(k,len(pos),len(neg))
                    ans[key]+=1
                    examples.setdefault(key,(tuple(pos),tuple(neg)))
    return ans,examples

def is_pm(mask):
    deg=[0]*16
    for e,(u,v,d) in enumerate(EDGES):
        if (mask>>e)&1:
            deg[u]+=1; deg[v]+=1
    return all(x==1 for x in deg)

def negstar_accept(mask):
    return any(all(((mask>>e)&1)==0 for e in st) for st in STARS)

# Build the 48-controlled-contact negative-star DAG.
# Dimensions 0 and 3 are shared between the two endpoint-star paths.
# Dimensions 1 and 2 have one occurrence per Q4 vertex.
def build_negative_star_dag():
    next_node=1
    source=0
    sink=None
    ctrl=[]   # (u,v,label_edge,polarity), polarity=-1 means not x_e
    free=[]

    d0_post={}
    for e,(u,v,d) in enumerate(EDGES):
        if d==0:
            z=next_node; next_node+=1
            ctrl.append((source,z,e,-1))
            d0_post[e]=z

    v_after2={}
    for v in range(16):
        e0=STARS[v][0]; e1=STARS[v][1]; e2=STARS[v][2]
        pre1=next_node; next_node+=1
        free.append((d0_post[e0],pre1))
        post1=next_node; next_node+=1
        ctrl.append((pre1,post1,e1,-1))
        post2=next_node; next_node+=1
        ctrl.append((post1,post2,e2,-1))
        v_after2[v]=post2

    d3_pre={}
    for e,(u,v,d) in enumerate(EDGES):
        if d==3:
            z=next_node; next_node+=1
            d3_pre[e]=z
            free.append((v_after2[u],z))
            free.append((v_after2[v],z))

    sink=next_node; next_node+=1
    for e,z in d3_pre.items():
        ctrl.append((z,sink,e,-1))

    assert len(ctrl)==48

    # Enumerate all source-sink paths as controlled-label sequences.
    cadj=defaultdict(list)
    for u,v,e,p in ctrl: cadj[u].append((v,e))
    for u,v in free: cadj[u].append((v,None))

    paths=[]
    def dfs(u,labs):
        if u==sink:
            paths.append(tuple(labs)); return
        for v,e in cadj[u]:
            if e is None: dfs(v,labs)
            else: dfs(v,labs+[e])
    dfs(source,[])
    assert len(paths)==16
    assert {frozenset(p) for p in paths}=={frozenset(s) for s in STARS}
    assert all(len(p)==4 for p in paths)
    return next_node,ctrl,free,paths

def exhaustive_verify():
    total=sat=unsat=0
    for S in combinations(range(32),8):
        m=0
        for e in S: m|=1<<e
        pm=is_pm(m)
        acc=negstar_accept(m)
        assert acc==(not pm)
        total+=1
        unsat+=pm
        sat+=not pm
    return total,sat,unsat

if __name__=="__main__":
    terms,examples=minimal_safe_terms_upto4()
    print("minimal_safe_term_counts",dict(sorted(terms.items())))
    print("examples",examples)

    # Consequences:
    assert sum(v for (k,p,n),v in terms.items() if k==1)==0
    assert sum(v for (k,p,n),v in terms.items() if k==2)==96
    assert terms[(2,2,0)]==96
    assert sum(v for (k,p,n),v in terms.items() if k==3)==0
    assert terms[(4,0,4)]==16

    nodes,ctrl,free,paths=build_negative_star_dag()
    print("negative_star_DAG_nodes",nodes)
    print("negative_star_controlled_contacts",len(ctrl))
    print("negative_star_free_edges",len(free))
    print("negative_star_accepting_paths",len(paths))

    total,sat,unsat=exhaustive_verify()
    print("exhaustive_promised_inputs",total)
    print("SAT",sat,"UNSAT",unsat)

    print("NULL_FORK_WRAPPER")
    print("For any literal switch DAG N and any variable x_i, prepend two parallel")
    print("contacts labelled x_i and not x_i from a new source to the old source.")
    print("Exactly one is live on every Boolean input, so the function is unchanged,")
    print("while the new physical source cut has only two controlled edges.")
    print("Therefore raw physical cut width is not wrapper-invariant in the full literal model.")

    print("STATUS")
    print("Complement contacts do not create any safe 1-literal or 3-literal certificate.")
    print("All 96 minimal safe length-2 certificates are positive conflict pairs.")
    print("The first purely negative certificates have length 4: exactly the 16 Q4 vertex stars.")
    print("A 48-contact all-negative syntactic read-once DAG computes D(4,8) SAT on the promise.")
    print("No claim is made that 48 is optimal for unrestricted literal-labelled semantic DAGs.")
