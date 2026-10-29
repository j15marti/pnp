#!/usr/bin/env python3
"""Independent exact mixed-affine/2CNF solver, with paid VC discovery and projected-rank fallback.
No external packages. Results are finite controls, not a general SAT proof.
"""
import itertools, json, random, math
from collections import Counter

class DSU:
    def __init__(self,n): self.p=list(range(n))
    def root(self,a):
        while self.p[a]!=a:
            self.p[a]=self.p[self.p[a]];a=self.p[a]
        return a
    def join(self,a,b):
        a,b=self.root(a),self.root(b)
        if a!=b: self.p[b]=a

def varlist(mask):
    while mask:
        bit=mask & -mask
        yield bit.bit_length()-1
        mask ^= bit

def eval_clause(clause, bits):
    return any(bool((bits>>(abs(l)-1))&1)==(l>0) for l in clause)

def verify(n,eqs,clauses,bits):
    return all((bits & mask).bit_count()%2==rhs for mask,rhs in eqs) and all(eval_clause(c,bits) for c in clauses)

def gaussian(n,eqs,vars_):
    """RREF all equations in explicitly specified variable coordinates. Return (particular,basis)."""
    loc={v:i for i,v in enumerate(vars_)}
    rows=[]
    for glob,rhs in eqs:
        local=0
        for v in varlist(glob):
            assert v in loc
            local ^= (1<<loc[v])
        rows.append([local,rhs])
    piv=[]; r=0
    for col in range(len(vars_)):
        pick=next((z for z in range(r,len(rows)) if rows[z][0]>>col & 1),None)
        if pick is None:continue
        rows[r],rows[pick]=rows[pick],rows[r]
        for t in range(len(rows)):
            if t!=r and (rows[t][0]>>col&1):
                rows[t][0]^=rows[r][0];rows[t][1]^=rows[r][1]
        piv.append(col);r+=1
    if any(mask==0 and rhs==1 for mask,rhs in rows):return None
    free=[j for j in range(len(vars_)) if j not in set(piv)]
    def glob(local):
        return sum(1<<vars_[j] for j in range(len(vars_)) if local>>j&1)
    part=sum(1<<vars_[piv[i]] for i in range(r) if rows[i][1])
    basis=[]
    for f in free:
        vec=1<<f
        for i,p in enumerate(piv):
            if rows[i][0]>>f&1:vec|=1<<p
        basis.append(glob(vec))
    return part,basis

def independent_columns(vectors, visible_mask):
    piv={}; chosen=[]
    for v in vectors:
        red=v & visible_mask
        while red:
            hi=red.bit_length()-1
            if hi not in piv:
                piv[hi]=red;chosen.append(v);break
            red^=piv[hi]
    return chosen

def simplify_B(clauses):
    """Remove tautologies, duplicate literals. Clauses of length 0,1,2 allowed."""
    out=[]
    for clause in clauses:
        assert len(clause)<=2
        xs=tuple(dict.fromkeys(clause))
        if any(-l in xs for l in xs): continue
        out.append(xs)
    return out

def cluster_instances(n,eqs,B):
    d=DSU(n)
    for mask,_ in eqs:
        vv=list(varlist(mask))
        for v in vv[1:]:d.join(vv[0],v)
    affine_root=[d.root(v) for v in range(n)]
    e=DSU(n)
    for c in B:
        if len(c)==2:e.join(affine_root[abs(c[0])-1],affine_root[abs(c[1])-1])
    clusters={}
    for v in range(n):clusters.setdefault(e.root(affine_root[v]),set()).add(v)
    out=[]
    for vv in clusters.values():
        subset=sum(1<<v for v in vv)
        rows=[row for row in eqs if row[0] & subset]
        assert all(row[0]&~subset==0 for row in rows)
        cs=[c for c in B if all(abs(l)-1 in vv for l in c)]
        out.append((sorted(vv),rows,cs))
    return out

def calc_affine_components(vars_,eqs,clauses):
    d=DSU(max(vars_)+1 if vars_ else 0)
    for mask,_ in eqs:
        v=list(varlist(mask))
        for w in v[1:]:d.join(v[0],w)
    groups={}
    for v in vars_:groups.setdefault(d.root(v),[]).append(v)
    out=[]
    for grp in groups.values():
        s=set(grp);rows=[(mask,rhs) for mask,rhs in eqs if mask and next(varlist(mask)) in s]
        sol=gaussian(max(vars_)+1,rows,grp)
        if sol is None: return None
        part,basis=sol
        visible=set(abs(l)-1 for c in clauses for l in c)&s
        vismask=sum(1<<v for v in visible)
        selected=independent_columns(basis,vismask)
        out.append({'variables':grp,'part':part,'selected':selected,'rank':len(selected)})
    return out

def two_sat_solve(m, clauses):
    """Literals (index 0..m-1, required true bit). Returns bitmask of true variables, or None."""
    g=[[] for _ in range(2*m)];gr=[[] for _ in range(2*m)]
    def node(l):return 2*l[0] + (0 if l[1] else 1)
    def edge(a,b):g[a].append(b);gr[b].append(a)
    for clause in clauses:
        if len(clause)==0:return None
        if len(clause)==1:
            a=node(clause[0]);edge(a^1,a)
        else:
            a,b=node(clause[0]),node(clause[1]);edge(a^1,b);edge(b^1,a)
    seen=[False]*len(g);order=[]
    for v in range(len(g)):
        if seen[v]:continue
        stack=[(v,False)]
        while stack:
            x,done=stack.pop()
            if done:order.append(x);continue
            if seen[x]:continue
            seen[x]=True
            stack.append((x,True))
            stack.extend((y,False) for y in g[x] if not seen[y])
    comp=[-1]*len(g);cid=0
    for v in reversed(order):
        if comp[v]!=-1:continue
        stack=[v];comp[v]=cid
        while stack:
            x=stack.pop()
            for y in gr[x]:
                if comp[y]==-1:comp[y]=cid;stack.append(y)
        cid+=1
    if any(comp[2*i]==comp[2*i+1] for i in range(m)):return None
    return sum(1<<i for i in range(m) if comp[2*i]>comp[2*i+1])

def vc_bounded(edges,budget,stats):
    def rec(edges,k,picked):
        stats['vc_discovery_nodes']+=1
        if not edges:return picked
        if k==0:return None
        u,v=edges[0]
        for w in (u,v):
            left=tuple(pair for pair in edges if w not in pair)
            z=rec(left,k-1,picked+(w,))
            if z is not None:return z
        return None
    return rec(tuple(edges),budget,tuple())

def get_cover(edges,K,stats):
    for depth in range(K+1):
        res=vc_bounded(edges,depth,stats)
        if res is not None:return res
    return None

def vc_solve(n,vars_,eqs,B,cover,stats):
    for bits in range(1<<len(cover)):
        stats['vc_assignments']+=1
        forced=[(1<<v,(bits>>i)&1) for i,v in enumerate(cover)]
        forced_values={v:(bits>>i)&1 for i,v in enumerate(cover)}
        valid=True
        for c in B:
            unsatisfied=[];sat=False
            for lit in c:
                v=abs(lit)-1
                if v in forced_values:
                    if forced_values[v]==int(lit>0):sat=True;break
                else:unsatisfied.append(lit)
            if sat:continue
            if len(unsatisfied)==0:valid=False;break
            if len(unsatisfied)>1:raise AssertionError('cover failed to cover binary edge')
            lit=unsatisfied[0];forced.append((1<<(abs(lit)-1),int(lit>0)))
        if not valid:continue
        solution=gaussian(n,eqs+forced,vars_)
        if solution is None:continue
        part,_=solution
        assert verify(n,eqs,B,part)
        return part
    return None

def rank_solve(n,vars_,eqs,B,ac,stats):
    components=[]
    for i,a in enumerate(ac):
        first=a['selected'][:-1] if a['rank']>=1 else []
        last=a['selected'][-1] if a['rank']>=1 else 0
        components.append((a['part'],first,last))
    owner={v:i for i,a in enumerate(ac) for v in a['variables']}
    prefixbits=sum(len(x[1]) for x in components)
    assert prefixbits==sum(max(a['rank']-1,0) for a in ac)
    for pref in range(1<<prefixbits):
        stats['rank_assignments']+=1
        state=[a[0] for a in components];offset=0
        for i,(_,col,_) in enumerate(components):
            for v in col:
                if pref>>offset&1:state[i]^=v
                offset+=1
        remaining={i:j for j,i in enumerate(i for i,a in enumerate(ac) if a['rank']>0)}
        reduced=[]
        for clause in B:
            cl=[]; satisfied=False
            for lit in clause:
                v=abs(lit)-1;i=owner[v];base=(state[i]>>v)&1
                last=(components[i][2]>>v)&1
                if last:
                    desired=base ^ int(lit>0)
                    cl.append((remaining[i],bool(desired)))
                elif base==int(lit>0):satisfied=True;break
            if satisfied:continue
            cl=list(dict.fromkeys(cl))
            if any((i,not b) in cl for i,b in cl):continue
            reduced.append(cl)
        stats['scc_calls']+=1
        sat=two_sat_solve(len(remaining),reduced)
        if sat is None:continue
        solution=0
        for i,base in enumerate(state):
            if i in remaining and (sat>>remaining[i]&1):base^=components[i][2]
            solution^=base
        assert verify(n,eqs,B,solution)
        return solution
    return None

def solve(n,eqs,clauses):
    B=simplify_B(clauses)
    if any(len(c)==0 for c in B):
        return None,Counter({'empty_clause_conflict':1}),[]
    if any(mask==0 and rhs==1 for mask,rhs in eqs):
        return None,Counter({'inconsistent_empty_equation':1}),[]
    eqs=[(mask,rhs) for mask,rhs in eqs if mask!=0]
    if n==0:return 0,Counter({'empty_instance_satisfied':1}),[]
    stats=Counter({'vc_discovery_nodes':0,'vc_assignments':0,'rank_assignments':0,'scc_calls':0,'clusters':0})
    branch=[];global_answer=0
    for vars_,rows,cs in cluster_instances(n,eqs,B):
        stats['clusters']+=1
        ac=calc_affine_components(vars_,rows,cs)
        if ac is None:return None,stats,branch
        K=sum(max(a['rank']-1,0) for a in ac)
        edges=sorted(set(tuple(sorted((abs(c[0])-1,abs(c[1])-1))) for c in cs if len(c)==2 and abs(c[0])!=abs(c[1])))
        cover=get_cover(edges,K,stats)
        if cover is not None:
            branch.append({'K':K,'k':len(cover),'chosen':'vertex_cover','vars':len(vars_),'binary_edges':len(edges)})
            found=vc_solve(n,vars_,rows,cs,cover,stats)
        else:
            branch.append({'K':K,'k':f'>{K}','chosen':'projected_rank','vars':len(vars_),'binary_edges':len(edges)})
            found=rank_solve(n,vars_,rows,cs,ac,stats)
        if found is None:return None,stats,branch
        global_answer|=found
    assert verify(n,eqs,B,global_answer)
    return global_answer,stats,branch

def brute(n,eqs,clauses):
    return next((z for z in range(1<<n) if verify(n,eqs,clauses,z)),None)

def build_heterogeneous(p,q,unsat=False):
    # Cluster A: p exposed variables free modulo affine auxiliaries, one-vertex-cover star.
    # Cluster B: q separate affine components, each exposes one bit, complete binary clique.
    eqs=[];cs=[]; nxt=0
    A=list(range(nxt,nxt+p));nxt+=p
    for v in A[1:]:
        aux=nxt;nxt+=1
        eqs.append(((1<<A[0])|(1<<v)|(1<<aux),0))
        cs.append((A[0]+1,v+1))
    B=[]
    for i in range(q):
        exposed=nxt;nxt+=1
        a=nxt;nxt+=1;b=nxt;nxt+=1
        B.append(exposed)
        eqs.append(((1<<exposed)|(1<<a)|(1<<b),0))
    for i in range(q):
        for j in range(i+1,q):cs.append((-(B[i]+1),-(B[j]+1)))
    if unsat:
        cs.extend([((B[0]+1),), (-(B[0]+1),)])
    return nxt,eqs,cs

def run():
    rng=random.Random(20261029)
    stats=Counter();per_case=[]
    # Random independent oracle checks, positive and negative.
    for n in range(1,10):
        for r in range(90):
            eqs=[];cs=[]
            for _ in range(rng.randrange(0,7)):
                mask=sum(1<<v for v in range(n) if rng.random()<.37)
                eqs.append((mask,rng.randrange(2)))
            for _ in range(rng.randrange(0,11)):
                size=rng.randrange(0,min(2,n)+1)
                cs.append(tuple((v+1)*rng.choice((-1,1)) for v in rng.sample(range(n),size)))
            true=brute(n,eqs,cs)
            got,st,blocks=solve(n,eqs,cs)
            assert (true is None)==(got is None),(n,eqs,cs,true,got)
            if got is not None:assert verify(n,eqs,cs,got)
            stats.update(st);stats['random_cases']+=1
            stats['random_sat' if got is not None else 'random_unsat']+=1
    # Planted SAT: all constraints generated to respect a chosen assignment.
    for n in range(1,10):
        for _ in range(40):
            planted=rng.randrange(1<<n);eqs=[];cs=[]
            for _ in range(7):
                mask=sum(1<<v for v in range(n) if rng.random()<.33)
                eqs.append((mask,(planted&mask).bit_count()%2))
            for _ in range(8):
                size=rng.randrange(1,min(2,n)+1)
                selected=rng.sample(range(n),size)
                clause=[(v+1)*rng.choice((-1,1)) for v in selected]
                if not eval_clause(clause,planted):clause[0]=-clause[0]
                cs.append(tuple(clause))
            got,st,blocks=solve(n,eqs,cs)
            assert got is not None and verify(n,eqs,cs,got)
            stats.update(st);stats['planted_sat']+=1
    # Exhaustive two-variable 2SAT encodings, independently brute checked.
    lits=[(v,bool(value)) for v in range(2) for value in (0,1)]
    possibilities=[[a] for a in lits] + [list(pair) for pair in itertools.combinations(lits,2)]
    for sel in range(1<<len(possibilities)):
        clauses=[c for i,c in enumerate(possibilities) if sel>>i&1]
        expected=next((bits for bits in range(4) if all(any(bool(bits>>v&1)==wanted for v,wanted in c) for c in clauses)),None)
        observed=two_sat_solve(2,clauses)
        assert (expected is None)==(observed is None)
        stats['two_sat_exhaustive']+=1
    # More random 2SAT controls, including contradictory and densely cyclic digraphs.
    for m in range(3,9):
        for _ in range(120):
            clauses=[]
            for _ in range(16):
                size=rng.randrange(1,3)
                clause=[(rng.randrange(m),bool(rng.randrange(2))) for _ in range(size)]
                clauses.append(clause)
            expected=next((bits for bits in range(1<<m) if all(any(bool(bits>>v&1)==wanted for v,wanted in c) for c in clauses)),None)
            observed=two_sat_solve(m,clauses)
            assert (expected is None)==(observed is None)
            stats['two_sat_random']+=1
    assert solve(0,[],[])[0]==0
    assert solve(0,[],[()])[0] is None
    assert solve(0,[(0,1)],[])[0] is None
    stats['zero_var_controls']+=3
    # Pay for vertex-cover detection and compare against exhaustive minima.
    for n in range(2,8):
        for _ in range(30):
            edges=[(u,v) for u in range(n) for v in range(u+1,n) if rng.randrange(2)]
            optimum=next(k for k in range(n+1) if any(all(u in cov or v in cov for u,v in edges) for cov in itertools.combinations(range(n),k)))
            cover=get_cover(edges,optimum,stats)
            assert cover is not None and len(cover)==optimum
            if optimum>0:assert get_cover(edges,optimum-1,stats) is None
            stats['vc_discovery_crosschecks']+=1
    for p,q in ((5,6),(10,11),(20,20)):
        for unsat in (False,True):
            n,eqs,cs=build_heterogeneous(p,q,unsat)
            got,st,blocks=solve(n,eqs,cs)
            assert (got is None)==unsat
            # Two interaction clusters; A has K=p-1, k=1 and B has K=0, k=q-1.
            assert sorted((b['chosen'],b['K']) for b in blocks)==[('projected_rank',0),('vertex_cover',p-1)]
            assert st['vc_assignments']<=2 and st['rank_assignments']==1
            stats.update(st)
            per_case.append({'p':p,'q':q,'n':n,'clauses':len(cs),'sat':not unsat,'blocks':blocks,'counts':dict(st)})
    # Fano no forced literals, affine+binary conjunction UNSAT: regression.
    triples=((0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5))
    eqs=[(sum(1<<v for v in triple),1) for triple in triples]
    cs=[(-(u+1),-(v+1)) for triple in triples for u,v in itertools.combinations(triple,2)]
    assert brute(7,eqs,cs) is None
    got,st,blocks=solve(7,eqs,cs);assert got is None
    stats['fano_checked']+=1
    return {'status':'PASS','seed':20261029,'counters':dict(stats),'heterogeneous_controls':per_case,
            'original_connected_audit_sha256':'05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca',
            'limitations':['Tests not proof of arbitrary instance soundness.','Native TM steps and peak tape cells not directly measured.','The combined parameter may be linear on unrestricted SAT.']}
if __name__=='__main__': print(json.dumps(run(),indent=2,sort_keys=True))
