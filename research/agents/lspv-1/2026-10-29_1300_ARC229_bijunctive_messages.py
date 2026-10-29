#!/usr/bin/env python3
"""ARC229: source-authenticated 2CNF/low-rank-affine tree composition.
Finite reproducer and exact deterministic solver on a recognized promise class.
No inference about unrestricted SAT or strict exact-(2,2) SAT.
Standard library only; Python 3.10+.
"""
from __future__ import annotations
import argparse
from collections import Counter
from itertools import combinations, product
import json, random, hashlib


def xor_ok(rows, a):
    bits = sum((x & 1) << i for i,x in enumerate(a))
    return all(((bits & m).bit_count() & 1) == b for m,b in rows)

def cnf_ok(clauses, a):
    return all(any(a[abs(l)-1] == (l>0) for l in c) for c in clauses)

def scc(n, clauses):
    g=[[] for _ in range(2*n)]; gr=[[] for _ in range(2*n)]
    ix=lambda lit:2*(abs(lit)-1)+(lit<0)
    for c in clauses:
        if len(c)>2: raise ValueError('not a 2CNF clause')
        if not c:return None
        x,y=c[0],c[-1]
        for u,v in ((-x,y),(-y,x)):
            u,v=ix(u),ix(v)
            g[u].append(v);gr[v].append(u)
    seen=[False]*(2*n);order=[]
    for i in range(2*n):
        if seen[i]:continue
        seen[i]=True;stack=[(i,0)]
        while stack:
            v,j=stack[-1]
            if j<len(g[v]):
                w=g[v][j];stack[-1]=(v,j+1)
                if not seen[w]:seen[w]=True;stack.append((w,0))
            else:order.append(v);stack.pop()
    comp=[-1]*(2*n);k=0
    for i in reversed(order):
        if comp[i]>=0:continue
        comp[i]=k;stack=[i]
        while stack:
            v=stack.pop()
            for w in gr[v]:
                if comp[w]<0:comp[w]=k;stack.append(w)
        k+=1
    if any(comp[2*i]==comp[2*i+1] for i in range(n)):return None
    return comp

def solve_2sat(n,clauses):
    comp=scc(n,clauses)
    return None if comp is None else tuple(int(comp[2*i]>comp[2*i+1]) for i in range(n))

def reduce_affine(rows):
    """GF(2) rank and consistency, no exponential row enumeration."""
    basis={}
    for mask,rhs in rows:
        m=mask;b=rhs
        while m:
            lead=m.bit_length()-1
            if lead in basis:
                bm,bb=basis[lead];m^=bm;b^=bb
            else:
                basis[lead]=(m,b);break
        if not m and b:return None
    return sorted(basis.values(),key=lambda x:x[0].bit_length(),reverse=True)

def compress(n,clauses,rows,stats):
    comp=scc(n,clauses)
    if comp is None:return None
    reps={};mapping=[]
    for i in range(n):
        a,b=comp[2*i],comp[2*i+1];key=min(a,b)
        if key not in reps:reps[key]=len(reps)
        mapping.append((reps[key],int(a!=key)))
    m=len(reps);cc=[]
    for c in clauses:
        out=set()
        for l in c:
            j,flip=mapping[abs(l)-1]
            s=(l>0)^bool(flip)
            out.add(j+1 if s else -(j+1))
        if not any(-l in out for l in out):cc.append(tuple(sorted(out)))
    rr=[]
    for mask,rhs in rows:
        newmask=0
        for i in range(n):
            if (mask>>i)&1:
                j,flip=mapping[i];newmask^=1<<j;rhs^=flip
        rr.append((newmask,rhs))
    rr=reduce_affine(rr)
    if rr is None:return None
    stats['scc_quotients']+=1
    return m,cc,rr,mapping

def pluck(n,clauses,rows,v):
    pi=next((i for i,(mask,_) in enumerate(rows) if mask>>v&1),None)
    if pi is None:raise ValueError('variable absent from affine equations')
    pm,pb=rows[pi]
    rem=[i for i in range(n) if i!=v]
    drop=lambda mask:sum(((mask>>i)&1)<<j for j,i in enumerate(rem))
    newrows=[]
    for i,(mask,rhs) in enumerate(rows):
        if i==pi:continue
        if (mask>>v)&1:mask^=pm;rhs^=pb
        newrows.append((drop(mask),rhs))
    newrows=reduce_affine(newrows)
    if newrows is None:return None
    newclauses=[]
    for c in clauses:
        out=[]
        for l in c:
            j=abs(l)-1
            if j==v:continue
            j-=int(j>v)
            out.append(j+1 if l>0 else -(j+1))
        if not out:return None
        newclauses.append(tuple(out))
    return n-1,newclauses,newrows,(pm,pb,rem)

def fixed_codim(n,clauses,rows,stats):
    """Certified deterministic n^{O(e)} branching, an independently proved
    variant of the known Arvind-Guruswami fixed-codimension XP theorem.
    SCC quotient is necessary for model-flip-path completeness.
    """
    rows=reduce_affine(rows)
    if rows is None:return None
    if len(rows)>stats.get('max_local_rank',10**6):raise ValueError('rank budget')
    source_c=[tuple(c) for c in clauses];source_r=list(rows)
    def recurse(n,C,R):
        stats['local_nodes']+=1
        q=compress(n,C,R,stats)
        if q is None:return None
        m,cc,rr,mapping=q
        a=solve_2sat(m,cc)
        if a is None:return None
        if xor_ok(rr,a):
            stats['local_base_hits']+=1
            return tuple(a[j]^flip for j,flip in mapping)
        for v in range(m):
            if not any(mask>>v&1 for mask,_ in rr):continue
            stats['failed_or_successful_plucks']+=1
            p=pluck(m,cc,rr,v)
            if p is None:continue
            nn,c2,r2,(pm,pb,rem)=p
            child=recurse(nn,c2,r2)
            if child is None:continue
            val=pb
            out=[None]*m
            for j,i in enumerate(rem):
                out[i]=child[j]
                if pm>>i&1:val^=child[j]
            out[v]=val
            assert cnf_ok(cc,out) and xor_ok(rr,out)
            return tuple(out[j]^flip for j,flip in mapping)
        return None
    ans=recurse(n,source_c,source_r)
    if ans is not None:
        assert cnf_ok(source_c,ans) and xor_ok(source_r,ans)
        stats['source_witness_verified']+=1
    return ans

class InvalidSource(ValueError):pass


def scope(c):
    if c['kind']=='cnf':return set(abs(l)-1 for l in c['lits'])
    if c['kind']=='xor':return set(c['vars'])
    raise InvalidSource('unrecognized constraint kind')

def validate(problem, max_rank=2, max_sep=16):
    """Verify against independent original constraint manifest; not owner assertions."""
    n=problem['n'];bags=[set(x) for x in problem['bags']]
    k=len(bags);edges=[tuple(x) for x in problem['edges']]
    if k<1 or len(edges)!=k-1:raise InvalidSource('tree edge count')
    adj=[set() for _ in bags]
    for u,v in edges:
        if not (0<=u<k and 0<=v<k) or u==v or v in adj[u]:
            raise InvalidSource('invalid tree edge')
        adj[u].add(v);adj[v].add(u)
    seen={0};todo=[0]
    for u in todo:
        for v in adj[u]:
            if v not in seen:seen.add(v);todo.append(v)
    if len(seen)!=k:raise InvalidSource('disconnected tree')
    for bag in bags:
        if any(not 0<=x<n for x in bag):raise InvalidSource('out of range variable')
    manifest=problem['source']
    ids=[c['id'] for c in manifest]
    if len(ids)!=len(set(ids)):raise InvalidSource('duplicate source ids')
    idx={c['id']:c for c in manifest}
    owners=problem['owners']
    if len(owners)!=k:raise InvalidSource('incorrect number of owner lists')
    owned=[i for a in owners for i in a]
    if len(owned)!=len(idx) or len(set(owned))!=len(owned) or set(owned)!=set(ids):
        raise InvalidSource('source constraint missing, duplicated or invented')
    for t,assigned in enumerate(owners):
        for i in assigned:
            c=idx[i]
            if not scope(c)<=bags[t]:raise InvalidSource('constraint crosses owner scope')
            if c['kind']=='cnf':
                if len(c['lits'])>2:raise InvalidSource('non-2CNF local clause')
                if any(l==0 or abs(l)>n for l in c['lits']):raise InvalidSource('bad literal')
            else:
                if len(c['vars'])!=len(set(c['vars'])) or c['rhs'] not in (0,1):
                    raise InvalidSource('bad affine row')
        variables=sorted(bags[t]);pos={v:i for i,v in enumerate(variables)}
        rows=[]
        for i in assigned:
            c=idx[i]
            if c['kind']=='xor':rows.append((sum(1<<pos[v] for v in c['vars']),c['rhs']))
        # Coefficient rank, including on inconsistent right-hand sides, is structural.
        rr=reduce_affine([(mask,0) for mask,rhs in rows])
        if rr is None or len(rr)>max_rank:raise InvalidSource('local affine rank above cap')
    for v in range(n):
        occ={t for t,bag in enumerate(bags) if v in bag}
        if not occ:raise InvalidSource('undeclared variable')
        seen={min(occ)};todo=[min(occ)]
        for u in todo:
            for w in adj[u]&occ:
                if w not in seen:seen.add(w);todo.append(w)
        if seen!=occ:raise InvalidSource('running intersection violated')
    for u,v in edges:
        if len(bags[u]&bags[v])>max_sep:raise InvalidSource('oversize edge separator')
    return bags,adj,idx

def from_table_to_2cnf(sep,feasible):
    """Exact canonical 2CNF encoding, or counterexample to bijunctivity."""
    sep=tuple(sorted(sep));k=len(sep)
    possible=set(product((0,1),repeat=k));R=set(feasible)
    if not R:
        return [()],True
    candidates=[]
    for i in range(k):
        for sign in (0,1):
            candidates.append(((i,sign),))
    for i,j in combinations(range(k),2):
        for a,b in product((0,1),repeat=2):
            candidates.append(((i,a),(j,b)))
    def holds(cl,x):return any(x[i]==val for i,val in cl)
    kept=[cl for cl in candidates if all(holds(cl,x) for x in R)]
    reconstructed={x for x in possible if all(holds(cl,x) for cl in kept)}
    if R!=reconstructed:
        return [],False
    return [tuple((sep[i]+1) if val else -(sep[i]+1) for i,val in c) for c in kept],True

def majority_bad_triple(rel):
    for a,b,c in combinations(sorted(rel),3):
        out=tuple(int(x+y+z>=2) for x,y,z in zip(a,b,c))
        if out not in rel:return (a,b,c,out)
    return None

def eval_constraint(c,a):
    if c['kind']=='cnf':return any(a[abs(l)-1]==(l>0) for l in c['lits'])
    return sum(a[v] for v in c['vars'])%2==c['rhs']

def solve_tree(problem,max_rank=2,max_sep=16):
    bags,adj,idx=validate(problem,max_rank,max_sep)
    n=problem['n'];k=len(bags)
    stats=Counter();stats['max_local_rank']=max_rank
    parent=[-1]*k;order=[0]
    for t in order:
        for u in sorted(adj[t]):
            if u!=parent[t]:parent[u]=t;order.append(u)
    msgs={};tables={}; localmodels={}
    for t in reversed(order):
        loc=sorted(bags[t]);positions={v:i for i,v in enumerate(loc)}
        clauses=[];rows=[]
        for cid in problem['owners'][t]:
            c=idx[cid]
            if c['kind']=='cnf':
                clauses.append(tuple((positions[abs(l)-1]+1)*(1 if l>0 else -1) for l in c['lits']))
            else:
                rows.append((sum(1<<positions[v] for v in c['vars']),c['rhs']))
        for child in sorted(adj[t]-{parent[t]}):
            for clause in msgs[child]:
                clauses.append(tuple((positions[abs(l)-1]+1)*(1 if l>0 else -1) for l in clause))
                stats['child_message_clauses_accessed']+=1
        sep=tuple(sorted(bags[t]&bags[parent[t]])) if parent[t]>=0 else ()
        feasible=set();models={}
        for bits in product((0,1),repeat=len(sep)):
            stats['parent_separator_assignments']+=1
            C=list(clauses)
            for v,val in zip(sep,bits):
                C.append(((positions[v]+1) if val else -(positions[v]+1),))
            model=fixed_codim(len(loc),C,rows,stats)
            stats['local_solver_calls']+=1
            if model is not None:
                feasible.add(bits);models[bits]={v:model[positions[v]] for v in loc}
                stats['local_witness_rows']+=1
        tables[t]=(sep,feasible);localmodels[t]=models
        cnf,recognized=from_table_to_2cnf(sep,feasible)
        stats['message_projection_bits']+=len(sep)*len(feasible)
        if not recognized:
            return {'status':'UNKNOWN_NON_BIJUNCTIVE','node':t,'separator':sep,
                    'feasible':[list(x) for x in sorted(feasible)],
                    'majority_falsifier':majority_bad_triple(feasible),
                    'stats':dict(stats)}
        msgs[t]=cnf;stats['messages_compiled']+=1
        stats['message_clauses_written']+=len(cnf)
    if not tables[0][1]:return {'status':'UNSAT','stats':dict(stats)}
    global_values={}
    def rebuild(t,bits):
        local=localmodels[t][bits]
        for v,val in local.items():
            if v in global_values:assert global_values[v]==val
            global_values[v]=val
        for child in sorted(adj[t]-{parent[t]}):
            s,_=tables[child]
            rebuild(child,tuple(local[v] for v in s))
    rebuild(0,())
    a=tuple(global_values[i] for i in range(n))
    assert all(eval_constraint(c,a) for c in problem['source'])
    stats['global_witness_checked']=1
    return {'status':'SAT','witness':list(a),'stats':dict(stats)}

def add_constraint(source,owners,t,kind,**kwargs):
    cid=f's{len(source):06d}'
    source.append({'id':cid,'kind':kind,**kwargs});owners[t].append(cid)

def star(q,parity):
    bags=[list(range(2*q))]+[[2*i,2*i+1] for i in range(q)]
    source=[];owners=[[] for _ in bags]
    add_constraint(source,owners,0,'xor',vars=list(range(2*q)),rhs=parity)
    for i in range(q):add_constraint(source,owners,i+1,'xor',vars=[2*i,2*i+1],rhs=0)
    return {'n':2*q,'bags':bags,'edges':[[0,i+1] for i in range(q)],'owners':owners,'source':source}

def path(k,charge):
    # k nodes with one coupling row and private row at every node, rank two;
    # strict local co-dimension two but unbounded total rank.
    n=(k+1)+2*k
    bags=[];source=[];owners=[[] for _ in range(k)]
    for i in range(k):
        p=k+1+2*i;q=p+1
        bags.append([i,i+1,p,q])
        add_constraint(source,owners,i,'xor',vars=[i,i+1],rhs=0)
        add_constraint(source,owners,i,'xor',vars=[p,q],rhs=0)
        add_constraint(source,owners,i,'cnf',lits=[i+2,p+1])
    add_constraint(source,owners,0,'cnf',lits=[-1])
    add_constraint(source,owners,k-1,'cnf',lits=[(k+1) if charge else -(k+1)])
    return {'n':n,'bags':bags,'edges':[[i,i+1] for i in range(k-1)],'owners':owners,'source':source}

def brute_source(problem):
    n=problem['n']
    for a in product((0,1),repeat=n):
        if all(eval_constraint(c,a) for c in problem['source']):return a
    return None

def rand_small(rng):
    k=rng.randrange(1,5);bags=[];edges=[]
    current=0
    for t in range(k):
        if t==0:
            w=rng.randrange(2,5);bags.append(list(range(w)));current=w
        else:
            par=rng.randrange(t)
            shared=rng.sample(bags[par],min(len(bags[par]),rng.randrange(0,3)))
            priv=list(range(current,current+rng.randrange(1,3)))
            current+=len(priv);bags.append(shared+priv);edges.append([par,t])
    if current>12:return None
    source=[];owners=[[] for _ in bags]
    for t,bag in enumerate(bags):
        for _ in range(rng.randrange(1,5)):
            if rng.randrange(2):
                vs=rng.sample(bag,rng.randrange(1,min(2,len(bag))+1))
                add_constraint(source,owners,t,'cnf',lits=[(v+1)*(1 if rng.randrange(2) else -1) for v in vs])
            else:
                vs=rng.sample(bag,rng.randrange(1,len(bag)+1))
                add_constraint(source,owners,t,'xor',vars=vs,rhs=rng.randrange(2))
    return {'n':current,'bags':bags,'edges':edges,'owners':owners,'source':source}

def audit(seed=2292026):
    rng=random.Random(seed)
    results={'seed':seed,'random_compared':0,'random_SAT':0,'random_UNSAT':0,
             'stars':[],'paths':[],'invalid_controls':0,'fixed_codim':{},
             'edge3':{},'archive_seeds_note':'Library controls re-read separately; not claimed to establish general coverage'}
    for n in range(1,7):
        for e in (0,1,2):
            for _ in range(48):
                C=[];rows=[]
                for _ in range(rng.randrange(0,2*n+1)):
                    a=rng.sample(range(n),rng.randrange(1,min(2,n)+1))
                    C.append(tuple((i+1)*(1 if rng.randrange(2) else -1) for i in a))
                for _ in range(e):rows.append((rng.randrange(1,1<<n),rng.randrange(2)))
                stats=Counter();got=fixed_codim(n,C,rows,stats)
                ref=next((a for a in product((0,1),repeat=n) if cnf_ok(C,a) and xor_ok(rows,a)),None)
                assert (got is None)==(ref is None),(n,C,rows,got,ref)
                results['fixed_codim']['cases']=results['fixed_codim'].get('cases',0)+1
    # Unitary counterexample missing from original ARC227 binary-only observation set.
    unsat_units={'n':3,'bags':[[0,1,2]],'edges':[],'owners':[[]],'source':[]}
    add_constraint(unsat_units['source'],unsat_units['owners'],0,'xor',vars=[0,1,2],rhs=1)
    for v in range(3):add_constraint(unsat_units['source'],unsat_units['owners'],0,'cnf',lits=[-(v+1)])
    assert solve_tree(unsat_units,max_rank=1)['status']=='UNSAT'
    results['arc227_unary_counterexample']='UNSAT, corrected solver catches it'
    for q in (1,2,4,8,16,32,64):
        for charge in (0,1):
            P=star(q,charge)
            r=solve_tree(P,max_rank=1,max_sep=2)
            assert r['status']==('SAT' if charge==0 else 'UNSAT')
            assert r['stats']['local_solver_calls']==q*4+1
            results['stars'].append({'q':q,'rhs':charge,'status':r['status'],'center_b':2*q,
                                     'max_edge':2,'local_calls':r['stats']['local_solver_calls'],
                                     'nodes':r['stats']['local_nodes'],
                                     '2CNF_messages':r['stats']['messages_compiled']})
    for k in (1,2,4,8,16):
        for end in (0,1):
            P=path(k,end);r=solve_tree(P,max_rank=2,max_sep=2)
            assert r['status']==('SAT' if end==0 else 'UNSAT')
            if k<=3:assert (brute_source(P) is None)==(r['status']=='UNSAT')
            results['paths'].append({'k':k,'end':end,'status':r['status'],
                                     'global_affine_rank':2*k,'local_calls':r['stats']['local_solver_calls']})
    # Random source-authenticated tree instances, excluding oversize separators.
    for trial in range(320):
        P=rand_small(rng)
        if P is None:continue
        try:r=solve_tree(P,max_rank=2,max_sep=2)
        except InvalidSource as e:
            if 'rank above cap' in str(e):continue
            raise
        assert r['status']!='UNKNOWN_NON_BIJUNCTIVE',r
        ref=brute_source(P)
        assert (ref is None)==(r['status']=='UNSAT'),(trial,P,r,ref)
        results['random_compared']+=1
        if ref is None:results['random_UNSAT']+=1
        else:results['random_SAT']+=1
    P=star(3,0)
    hostile=[]
    # A false source owner: omission, duplication, scope violation, and running intersection.
    import copy
    Q=copy.deepcopy(P);Q['owners'][1]=[];hostile.append(Q)
    Q=copy.deepcopy(P);Q['owners'][1].append(Q['owners'][0][0]);hostile.append(Q)
    Q=copy.deepcopy(P);Q['bags'][1]=[2,3];hostile.append(Q)
    Q=path(3,0);Q['bags'][2].append(0);hostile.append(Q)  # disconnected occurrence of x0
    # Running-intersection failure: introduce x0 into two leaves but not center.
    Q=copy.deepcopy(P);Q['bags'][0]=[v for v in Q['bags'][0] if v!=0];hostile.append(Q)
    for Q in hostile:
        try:solve_tree(Q,max_rank=1,max_sep=3)
        except InvalidSource:results['invalid_controls']+=1
        else:raise AssertionError('source or decomposition forgery accepted')
    # Exhaustive closure check on every Boolean relation of arity <=3.
    # At arity two every relation is 2CNF-definable. At arity three,
    # the 2CNF reconstruction agrees exactly with majority closure.
    results['relation_exhaustive']={}
    for dim in range(4):
        universe=list(product((0,1),repeat=dim))
        recognized=0; nonbij=0
        for mask in range(1<<len(universe)):
            rel={row for i,row in enumerate(universe) if mask>>i&1}
            compiled,accepted=from_table_to_2cnf(range(dim),rel)
            fail=majority_bad_triple(rel)
            assert accepted==(fail is None),(dim,mask,rel,compiled,fail)
            recognized+=int(accepted);nonbij+=int(not accepted)
        if dim<=2:assert nonbij==0
        results['relation_exhaustive'][str(dim)]={'total_relations':1<<len(universe),
                        'recognized_2CNF':recognized,'not_2CNF':nonbij}
    # A ternary parity message is not bijunctive, so cannot be inserted as 2CNF.
    tri={'n':3,'bags':[[0,1,2],[0,1,2]],'edges':[[0,1]],'owners':[[],[]],'source':[]}
    for v in range(3):add_constraint(tri['source'],tri['owners'],0,'cnf',lits=[-(v+1)])
    add_constraint(tri['source'],tri['owners'],1,'xor',vars=[0,1,2],rhs=1)
    r=solve_tree(tri,max_rank=1,max_sep=3)
    assert r['status']=='UNKNOWN_NON_BIJUNCTIVE' and r['majority_falsifier']
    results['edge3']['parity_message']=r
    # Three-coordinate separator can still pass if its actual message is 2CNF.
    tri2={'n':3,'bags':[[0,1,2],[0,1,2]],'edges':[[0,1]],'owners':[[],[]],'source':[]}
    add_constraint(tri2['source'],tri2['owners'],1,'xor',vars=[0,1,2],rhs=1)
    add_constraint(tri2['source'],tri2['owners'],1,'cnf',lits=[-1])
    add_constraint(tri2['source'],tri2['owners'],0,'cnf',lits=[-1])
    r2=solve_tree(tri2,max_rank=1,max_sep=3)
    assert r2['status']=='SAT'
    results['edge3']['bijunctive_ternary_table']='SAT'
    results['all_assertions_passed']=True
    return results

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,default=2292026)
    opt=ap.parse_args();print(json.dumps(audit(opt.seed),sort_keys=True,indent=2))