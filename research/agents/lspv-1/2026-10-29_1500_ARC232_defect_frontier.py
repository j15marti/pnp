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


def owner_scope(c):
    if c['kind']=='cnf':return {abs(lit)-1 for lit in c['lits']}
    if c['kind']=='xor':return set(c['vars'])
    raise ValueError('bad grammar')


def validate_source(P,e_cap):
    n=P['n'];bags=[set(x) for x in P['bags']];k=len(bags)
    edges=P['edges'];owners=P['owners'];source=P['source']
    if k<1 or len(edges)!=k-1 or len(owners)!=k:raise ValueError('bad tree size')
    adj=[set() for _ in range(k)]
    for u,v in edges:
        if u==v or not (0<=u<k and 0<=v<k) or v in adj[u]:raise ValueError('bad edge')
        adj[u].add(v);adj[v].add(u)
    visited={0};q=[0]
    for t in q:
        for u in adj[t]:
            if u not in visited:visited.add(u);q.append(u)
    if len(visited)!=k:raise ValueError('disconnected module tree')
    if any(not 0<=v<n for bag in bags for v in bag):raise ValueError('bad bag variable')
    src={c['id']:c for c in source}
    owned=[cid for ls in owners for cid in ls]
    if len(src)!=len(source) or len(owned)!=len(source) or set(owned)!=set(src) or len(owned)!=len(set(owned)):
        raise ValueError('source ownership mismatch')
    for t,ids in enumerate(owners):
        local={v:i for i,v in enumerate(sorted(bags[t]))};rows=[]
        for cid in ids:
            c=src[cid]
            if not owner_scope(c)<=bags[t]:raise ValueError('cross owner clause')
            if c['kind']=='cnf':
                if len(c['lits'])>2 or any(l==0 or abs(l)>n for l in c['lits']):raise ValueError('bad 2CNF')
            else:
                if c['rhs'] not in (0,1) or len(c['vars'])!=len(set(c['vars'])):raise ValueError('bad XOR')
                rows.append((sum(1<<local[v] for v in c['vars']),c['rhs']))
        if affine_coefficient_rank(rows)>e_cap:raise ValueError('affine rank cap')
    for v in range(n):
        occ={i for i,bag in enumerate(bags) if v in bag}
        if not occ:raise ValueError('missing variable bag')
        connected={min(occ)};q=[min(occ)]
        for t in q:
            for u in adj[t]&occ:
                if u not in connected:connected.add(u);q.append(u)
        if connected!=occ:raise ValueError('running intersection')
    return bags,adj,src


def canonical_2cnf(sep,relation):
    """Exact bijunctivity test by all implied width<=2 clauses and full table replay."""
    sep=tuple(sorted(sep));s=len(sep)
    if not relation:return [()],True
    allbits=set(product((0,1),repeat=s));clauses=[]
    candidates=[]
    for i in range(s):
        for v in (0,1):candidates.append(((i,v),))
    for i,j in combinations(range(s),2):
        for v,w in product((0,1),repeat=2):candidates.append(((i,v),(j,w)))
    def eval_cl(c,bits):return any(bits[i]==v for i,v in c)
    valid=[c for c in candidates if all(eval_cl(c,a) for a in relation)]
    if {a for a in allbits if all(eval_cl(c,a) for c in valid)}!=relation:
        return None,False
    for c in valid:
        clauses.append(tuple(sep[i]+1 if v else -(sep[i]+1) for i,v in c))
    return clauses,True


def source_evaluate(P,full):
    return all((any(full[abs(l)-1]==int(l>0) for l in c['lits']) if c['kind']=='cnf'
                else sum(full[v] for v in c['vars'])%2==c['rhs']) for c in P['source'])


def exact_defect_solver(P, e_cap=1, sep_cap=12, defect_cap=12):
    bags,adj,src=validate_source(P,e_cap)
    k=len(bags);n=P['n'];stats=Counter();stats['source_parse_passes']=1
    parent=[-1]*k;order=[0]
    for t in order:
        for u in sorted(adj[t]):
            if u!=parent[t]:parent[u]=t;order.append(u)
    messages={};records={}
    for t in reversed(order):
        ordered=sorted(bags[t]);pos={v:i for i,v in enumerate(ordered)}
        sep=tuple(sorted(bags[t]&bags[parent[t]])) if parent[t]>=0 else ()
        if len(sep)>sep_cap:return {'status':'UNKNOWN','cause':'edge width cap','stats':dict(stats)}
        C=[];E=[]
        for cid in P['owners'][t]:
            c=src[cid]
            if c['kind']=='cnf':C.append(tuple((pos[abs(l)-1]+1)*(1 if l>0 else -1) for l in c['lits']))
            else:E.append((sum(1<<pos[v] for v in c['vars']),c['rhs']))
        children=sorted(adj[t]-{parent[t]})
        bad=[]
        for child in children:
            cm=messages[child]
            if cm['good']:
                for cl in cm['compiled']:
                    C.append(tuple((pos[abs(l)-1]+1)*(1 if l>0 else -1) for l in cl))
                    stats['child_message_clauses_read']+=1
            else:bad.append(child)
        needed=set(sep)
        for child in bad:needed.update(messages[child]['sep'])
        W=tuple(sorted(needed));w=len(W)
        if w>defect_cap:return {'status':'UNKNOWN','cause':'defect width cap','stats':dict(stats)}
        bfull=set()
        for u in range(k):
            if u!=t:bfull.update(bags[t]&bags[u])
        stats['max_full_interface']=max(stats['max_full_interface'],len(bfull))
        stats['max_defect_width']=max(stats['max_defect_width'],w)
        stats['max_edge_width']=max(stats['max_edge_width'],len(sep))
        feasible=set();witnesses={}
        for values in product((0,1),repeat=w):
            stats['defect_assignments_tested']+=1
            fixed=dict(zip(W,values))
            if any(tuple(fixed[v] for v in messages[u]['sep']) not in messages[u]['table'] for u in bad):
                stats['bad_table_early_reject']+=1;continue
            pinned=C+[((pos[v]+1) if a else -(pos[v]+1),) for v,a in fixed.items()]
            stats['local_2subsat_calls']+=1
            x=subspace2sat(len(ordered),pinned,E,stats)
            if x is None:continue
            sigma=tuple(x[pos[v]] for v in sep)
            if sigma not in feasible:
                feasible.add(sigma)
                witnesses[sigma]={v:x[i] for i,v in enumerate(ordered)}
        compiled,good=canonical_2cnf(sep,feasible)
        messages[t]={'sep':sep,'table':feasible,'good':good,'compiled':compiled,'witness':witnesses}
        stats['good_messages']+=int(good)
        stats['bad_messages']+=int(not good)
        stats['table_entries_written']+=len(feasible)
        stats['total_separator_table_slots']+=1<<len(sep)
    sat=() in messages[0]['table']
    answer=None
    if sat:
        answer=[None]*n
        def reconstruct(t,sigma):
            x=messages[t]['witness'][sigma]
            for v,a in x.items():
                if answer[v] is not None and answer[v]!=a:raise AssertionError('gluing error')
                answer[v]=a
            for child in sorted(adj[t]-{parent[t]}):
                childsep=messages[child]['sep']
                reconstruct(child,tuple(x[v] for v in childsep))
        reconstruct(0,())
        if any(v is None for v in answer) or not source_evaluate(P,answer):
            raise AssertionError('source witness fails')
    return {'status':'SAT' if sat else 'UNSAT','witness':answer,'stats':dict(stats),
            'message_shapes':[{ 'separator':len(messages[t]['sep']), 'good':messages[t]['good'],
                                'ones':len(messages[t]['table'])} for t in order]}


def make_chain(k,rhs,root_parity):
    """k ternary groups; k modules; each affine rank 1; k-1 parity edge tables."""
    assert k>=2
    P={'n':3*k,'bags':[],'edges':[[i,i+1] for i in range(k-1)],'owners':[], 'source':[]}
    for i in range(k):
        bag=list(range(3*i,3*i+3))
        if i<k-1:bag+=list(range(3*i+3,3*i+6))
        P['bags'].append(bag);P['owners'].append([])
    def add(t,kind,**kwargs):
        cid=f'chain:{t}:{len(P["source"])}';P['source'].append(dict(id=cid,kind=kind,**kwargs));P['owners'][t].append(cid)
    for t in range(k-1):
        add(t,'xor',vars=list(range(3*t,3*t+6)),rhs=0)
    add(k-1,'xor',vars=list(range(3*(k-1),3*k)),rhs=rhs)
    for j,v in enumerate((root_parity,0,0)):
        add(0,'cnf',lits=[1+j if v else -(1+j)])
    return P


def make_star(q,bad_rhs):
    """Root with q good binary children and one non-bijunctive parity child."""
    assert q>=0
    n=2*q+3;z=list(range(2*q,n))
    P={'n':n,'bags':[list(range(n))], 'edges':[], 'owners':[[]], 'source':[]}
    def add(t,kind,**kwargs):
        cid=f'star:{t}:{len(P["source"])}';P['source'].append(dict(id=cid,kind=kind,**kwargs));P['owners'][t].append(cid)
    for i in range(q):
        P['bags'].append([2*i,2*i+1]);P['owners'].append([]);P['edges'].append([0,i+1]);
        add(i+1,'cnf',lits=[2*i+1,2*i+2])
        if i==0:add(0,'cnf',lits=[z[0]+1,2*i+1])
        else:add(0,'cnf',lits=[2*(i-1)+1,2*i+1])
    # Large primal clique in the root's *easy 2CNF* part; this rules out
    # inferring general hardness merely from treewidth growing with q.
    for i,j in combinations(range(q),2):
        add(0,'cnf',lits=[2*i+1,2*j+1])
    P['bags'].append(z);P['owners'].append([]);P['edges'].append([0,q+1]);add(q+1,'xor',vars=z,rhs=bad_rhs)
    for v in z:add(0,'cnf',lits=[-(v+1)])
    return P


def brute(P):
    for assignment in product((0,1),repeat=P['n']):
        if source_evaluate(P,assignment):return assignment
    return None


def static_frontier(n):
    points=[]
    for b in range(1,n+1):
        q=max(0,ceil(n/(12*b)-.25-1e-12))
        points.append((b,q,b+q,b))
    best=min(x[2] for x in points)
    minimizers=[x for x in points if x[2]==best]
    pareto=[]
    for x in points:
        # Pareto wrt smaller time exponent and smaller explicit-table space.
        if not any(y[2]<=x[2] and y[3]<=x[3] and (y[2]<x[2] or y[3]<x[3]) for y in points):
            pareto.append(x)
    return {'n':n,'continuous_b_star':sqrt(n/12),'continuous_E_star':sqrt(n/3)-.25,
            'integer_best_E':best,'integer_minimizers':minimizers,
            'first_E_time_equals_E_space':next((x for x in points if x[1]==0),None),
            'pareto_size':len(pareto),'pareto_last':pareto[-1],
            'sample': [points[b-1] for b in (1,2,4,8,9,10,11,12,20,40,100,400,800) if b<=n]}


def run():
    data={'status':'COMPUTATIONAL','seed':2322026,'cases':Counter(), 'family':[], 'max_stats':Counter()}
    rng=random.Random(2322026)
    # Independently compare two-SubSat local procedure with complete brute force.
    for n in range(1,9):
        for e in range(min(3,n)+1):
            for _ in range(24):
                C=[]
                for j in range(rng.randrange(0,2*n+1)):
                    vs=rng.sample(range(n),rng.randint(1,min(2,n)))
                    C.append(tuple((v+1)*(1 if rng.randrange(2) else -1) for v in vs))
                E=[(rng.randint(1,(1<<n)-1),rng.randrange(2)) for j in range(e)]
                stats=Counter();ans=subspace2sat(n,C,E,stats)
                want=next((a for a in product((0,1),repeat=n) if truth(n,C,E,a)),None)
                assert (ans is None)==(want is None),(n,C,E,ans,want)
                data['cases']['local_compared']+=1
    for k in range(2,13):
        for rhs,pin in product((0,1),repeat=2):
            P=make_chain(k,rhs,pin)
            got=exact_defect_solver(P)
            assert got['status']==('SAT' if rhs==pin else 'UNSAT')
            assert got['stats']['max_defect_width']<=6
            assert got['stats']['bad_messages']==k-1
            if k<=4:assert (brute(P) is None)==(got['status']=='UNSAT')
            data['cases']['chain_cases']+=1
            if k in (2,6,12):
                data['family'].append({'kind':'chain','k':k,'rhs':rhs,'root':pin, 'answer':got['status'],'stats':got['stats']})
    for q in (0,1,2,4,8,16,24,32,40):
        for rhs in (0,1):
            P=make_star(q,rhs);got=exact_defect_solver(P)
            assert got['status']==('SAT' if rhs==0 else 'UNSAT')
            assert got['stats']['max_defect_width']<=3
            assert got['stats']['bad_messages']==1
            if q<=3:assert (brute(P) is None)==(got['status']=='UNSAT')
            data['cases']['star_cases']+=1
            data['family'].append({'kind':'star','q':q,'rhs':rhs,'answer':got['status'],
                                   'full_b':2*q+3,'proxy_raw_table_exponent':2*q+3,
                                   'selective_defect_width':3,'stats':got['stats']})
    # Counterexample: ignoring ternary parity table after replacing with its binary hull.
    parity1={a for a in product((0,1),repeat=3) if sum(a)%2==1}
    canon,good=canonical_2cnf((0,1,2),parity1)
    assert not good and canon is None
    assert (0,0,0) not in parity1
    data['cases']['parity_hull_counterexamples']=1
    # Hostile verification: violate running-intersection or source ownership.
    P=make_chain(4,0,0);P['bags'][1].remove(3)
    try:exact_defect_solver(P);raise AssertionError('accepted invalid bag')
    except ValueError:data['cases']['bad_running_intersection_or_scope_rejected']=1
    P=make_chain(3,0,0);P['owners'][0].append(P['owners'][0][0])
    try:exact_defect_solver(P);raise AssertionError('accepted duplicate source')
    except ValueError:data['cases']['duplicate_ownership_rejected']=1
    data['static_frontiers']=[static_frontier(n) for n in (120,1200)]
    data['source_sha256']=hashlib.sha256(open(__file__,'rb').read()).hexdigest()
    data['cases']=dict(data['cases'])
    return data


if __name__=='__main__':
    t=time.perf_counter();out=run();out['wall_seconds']=round(time.perf_counter()-t,3)
    print(json.dumps(out,indent=2,sort_keys=True))