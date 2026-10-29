#!/usr/bin/env python3
"""ARC231: SCC-quotient effective affine rank on authenticated module trees.
Independent structural extension of LSPV1 ARC229 and LSPV4 HYBRID-BAD-MESSAGE228.
Uses a pinned copy of arc229_bijunctive_messages.py from the audited Library
as a known AG-style fixed-codimension solver; NOT a novel AG solver.
Usage: python arc231_effective_scc_rank_tree.py [--output path]
"""
from __future__ import annotations
import argparse, json, random, time, copy
from collections import Counter
from itertools import product
import arc229_bijunctive_messages as b

def rank_mask(masks):
    pivots={}
    for r in masks:
        while r:
            p=r.bit_length()-1
            if p in pivots:r^=pivots[p]
            else:pivots[p]=r;break
    return len(pivots)

def effective_local(n,clauses,rows,max_effective_rank,stats):
    """Check rank AFTER all 2CNF implication SCC identifications.
    No rank bound is placed on original rows. A true 2SAT contradiction or
    0=1 affine row proves this local candidate infeasible immediately.
    """
    scc=b.scc(n,clauses)
    stats['scc_passes']+=1
    if scc is None:
        stats['unsat_2cnf']+=1
        return 'UNSAT',None,0
    # independent quotient: pair of complementary SCCs -> one signed var
    pair_id={};mapping=[]
    for i in range(n):
        p,neg=scc[2*i],scc[2*i+1]
        pair=(min(p,neg),max(p,neg))
        if pair not in pair_id:pair_id[pair]=(len(pair_id),p)
        j,pos=pair_id[pair]
        mapping.append((j,int(p!=pos)))
    m=len(pair_id)
    cs=[]
    for c in clauses:
        new=set()
        for l in c:
            j,flip=mapping[abs(l)-1]
            new.add(j+1 if ((l>0)^bool(flip)) else -(j+1))
        if not any(-l in new for l in new):cs.append(tuple(sorted(new)))
    rr=[]
    for mask,rhs in rows:
        newmask=0
        for i in range(n):
            if mask>>i&1:
                j,flip=mapping[i];newmask^=1<<j;rhs^=flip
        rr.append((newmask,rhs))
    rank=rank_mask([mask for mask,rhs in rr])
    stats['raw_rank_max']=max(stats['raw_rank_max'],rank_mask([mask for mask,rhs in rows]))
    stats['effective_rank_max']=max(stats['effective_rank_max'],rank)
    stats['quotient_variables_reduced']+=n-m
    # A 0=1 row is not a rank increase; a genuine local contradiction.
    reduced=b.reduce_affine(rr)
    if reduced is None:
        stats['unsat_affine']+=1
        return 'UNSAT',None,rank
    if rank>max_effective_rank:
        stats['rank_budget_exceeded']+=1
        return 'UNKNOWN',None,rank
    stats['ag_calls']+=1
    old=stats.get('max_local_rank',None)
    stats['max_local_rank']=max_effective_rank
    witness=b.fixed_codim(m,cs,reduced,stats)
    if old is None:del stats['max_local_rank']
    else:stats['max_local_rank']=old
    if witness is None:
        stats['ag_unsat']+=1
        return 'UNSAT',None,rank
    lifted=tuple(witness[j]^flip for j,flip in mapping)
    assert b.cnf_ok(clauses,lifted) and b.xor_ok(rows,lifted)
    stats['local_witness_checked']+=1
    return 'SAT',lifted,rank

def solve_tree_effective(problem,max_effective_rank=1,max_sep=2):
    # The independent source authenticator checks every original source ID,
    # scope containment, global variable occurrence connectivity, tree edges.
    bags,adj,idx=b.validate(problem,max_rank=len(problem['source'])+1,max_sep=max_sep)
    n=problem['n'];count=len(bags)
    stats=Counter();parent=[-1]*count;order=[0]
    for t in order:
        for u in sorted(adj[t]):
            if u!=parent[t]:parent[u]=t;order.append(u)
    compiled={};tables={};models={};rows_raw={}
    for t in reversed(order):
        names=sorted(bags[t]);pos={v:i for i,v in enumerate(names)}
        C=[];R=[]
        for source_id in problem['owners'][t]:
            c=idx[source_id]
            if c['kind']=='cnf':
                C.append(tuple((pos[abs(l)-1]+1)*(1 if l>0 else -1) for l in c['lits']))
            else:R.append((sum(1<<pos[v] for v in c['vars']),c['rhs']))
        rows_raw[t]=rank_mask([m for m,r in R])
        for child in sorted(adj[t]-{parent[t]}):
            for clause in compiled[child]:
                C.append(tuple((pos[abs(l)-1]+1)*(1 if l>0 else -1) for l in clause))
                stats['child_clauses_read']+=1
        sep=tuple(sorted(bags[t]&bags[parent[t]])) if parent[t]>=0 else ()
        relation=set();local={};unknown=False
        for bits in product((0,1),repeat=len(sep)):
            pinned=list(C)
            for v,value in zip(sep,bits):
                pinned.append(((pos[v]+1) if value else -(pos[v]+1),))
            status,witness,rank=effective_local(len(names),pinned,R,max_effective_rank,stats)
            stats['table_rows_tested']+=1
            if status=='UNKNOWN':unknown=True
            elif status=='SAT':
                relation.add(bits)
                local[bits]={v:witness[pos[v]] for v in names}
        if unknown:
            return {'status':'UNKNOWN_EFFECTIVE_RANK','node':t,'stats':dict(stats)}
        tables[t]=(sep,relation);models[t]=local
        cnf,good=b.from_table_to_2cnf(sep,relation)
        if not good:
            return {'status':'UNKNOWN_NON_BIJUNCTIVE','node':t,'stats':dict(stats)}
        compiled[t]=cnf
        stats['table_bits_stored']+=len(sep)*len(relation)
        stats['compiled_child_clauses']+=len(cnf)
        stats['tables_computed']+=1
    if () not in tables[0][1]:
        return {'status':'UNSAT','stats':dict(stats),'raw_rank_max':max(rows_raw.values())}
    a={}
    def rebuild(t,bits):
        lm=models[t][bits]
        for v,value in lm.items():
            if v in a:assert a[v]==value
            a[v]=value
        for child in sorted(adj[t]-{parent[t]}):
            child_sep=tables[child][0]
            rebuild(child,tuple(lm[v] for v in child_sep))
    rebuild(0,())
    answer=tuple(a[i] for i in range(n))
    assert all(b.eval_constraint(c,answer) for c in problem['source'])
    stats['original_source_witness_checks']=len(problem['source'])
    return {'status':'SAT','witness':list(answer),'stats':dict(stats),
            'raw_rank_max':max(rows_raw.values())}

def source(q,bits):
    # Root owns q independent XOR3 rows, leaf i owns x_i <-> y_i.
    # With xi=yi each root row reduces to z=bits[i].
    z=2*q;root=list(range(2*q+1))
    bags=[root]+[[2*i,2*i+1] for i in range(q)]
    owners=[[] for _ in bags];manifest=[]
    for i,charge in enumerate(bits):
        b.add_constraint(manifest,owners,0,'xor',vars=[2*i,2*i+1,z],rhs=charge)
        b.add_constraint(manifest,owners,i+1,'cnf',lits=[-(2*i+1),2*i+2])
        b.add_constraint(manifest,owners,i+1,'cnf',lits=[2*i+1,-(2*i+2)])
    return {'n':2*q+1,'bags':bags,'edges':[[0,i+1] for i in range(q)],
            'owners':owners,'source':manifest}

def audit():
    out={'designation':'ARC231_EFFECTIVE_SCC_RANK',
         'status':'COMPUTATIONAL_REPLAY',
         'prior':'ARC228 SCC substitution, ARC229 edge<=2 composition, LSPV4 exceptional-union theorem',
         'cases':[],'tampering_rejections':0,'independent_bruteforce':0,'effective_overbudget_controls':0,'random_bruteforce':0,'random_sat':0,'random_unsat':0}
    for q in (1,2,4,8,16,32,64,128):
        for mode in ('SAT_Z0','SAT_Z1','UNSAT_MIXED'):
            rhs=[int(mode=='SAT_Z1')]*q
            if mode=='UNSAT_MIXED':
                if q==1:continue
                rhs[-1]=1
            P=source(q,rhs)
            result=solve_tree_effective(P,1,2)
            exp='UNSAT' if mode=='UNSAT_MIXED' else 'SAT'
            assert result['status']==exp,(q,mode,result)
            if q<=2:
                ref=b.brute_source(P)
                assert (ref is None)==(exp=='UNSAT')
                out['independent_bruteforce']+=1
            assert result['raw_rank_max']==q
            assert result['stats']['effective_rank_max']<=1
            # Global source is truly connected via the common z
            root_var_count=len(P['bags'][0]);assert root_var_count==2*q+1
            out['cases'].append({'q':q,'case':mode,'status':exp,
                'raw_rank':result['raw_rank_max'],
                'effective_rank_max':result['stats']['effective_rank_max'],
                'local_solver_calls':result['stats']['ag_calls'],
                'rows_tested':result['stats']['table_rows_tested'],
                'original_clauses_rows':len(P['source'])})
    assert len(out['cases'])==23
    # Random independent source projections: signed equalities, optional
    # root pins, arbitrary RHS. This exercises both SAT and UNSAT acquisition.
    rng=random.Random(2312026)
    for trial in range(240):
        q=rng.randint(1,4);rhs=[rng.randrange(2) for _ in range(q)]
        P=source(q,rhs)
        for i in range(q):
            if rng.randrange(2):
                for cid in P['owners'][i+1]:
                    c=next(c for c in P['source'] if c['id']==cid)
                    c['lits']=[-(v) for v in c['lits']]
                # flipping both binary clauses changes equality to XOR=1
                # (xi OR -yi) & (-xi OR yi) from equality would still be equality;
                # replace explicitly instead, independently of the old order.
                local=[c for c in P['source'] if c['id'] in P['owners'][i+1]]
                local[0]['lits']=[2*i+1,2*i+2]
                local[1]['lits']=[-(2*i+1),-(2*i+2)]
        if rng.randrange(3)==0:
            b.add_constraint(P['source'],P['owners'],0,'cnf',lits=[(2*q+1)*(1 if rng.randrange(2) else -1)])
        ans=solve_tree_effective(P,1,2)
        truth=b.brute_source(P)
        assert ans['status']!='UNKNOWN_EFFECTIVE_RANK', (trial,ans)
        assert (ans['status']=='SAT')==(truth is not None),(trial,ans,truth)
        out['random_bruteforce']+=1
        out['random_sat']+=int(truth is not None)
        out['random_unsat']+=int(truth is None)
    # Direct no-equivalence case with rank > cap returns UNKNOWN, not NO.
    P={'n':3,'bags':[[0,1,2]],'edges':[],'owners':[[]],'source':[]}
    for i in (0,1):b.add_constraint(P['source'],P['owners'],0,'xor',vars=[i],rhs=1)
    x=solve_tree_effective(P,1,2)
    assert x['status']=='UNKNOWN_EFFECTIVE_RANK',x
    out['effective_overbudget_controls']+=1
    # Forged ownership, omitted clause, disconnected running intersection.
    P=source(3,[0,0,1])
    hostile=[]
    Q=copy.deepcopy(P);Q['owners'][0].pop();hostile.append(Q)
    Q=copy.deepcopy(P);Q['owners'][0].append(Q['owners'][1][0]);hostile.append(Q)
    Q=copy.deepcopy(P);Q['bags'][0].remove(0);hostile.append(Q)
    Q=copy.deepcopy(P);Q['edges']=[[0,1],[1,2],[2,3]];hostile.append(Q)
    for bad in hostile:
        try:solve_tree_effective(bad,1,2)
        except b.InvalidSource:out['tampering_rejections']+=1
        else:raise AssertionError('bad source manifest accepted')
    assert out['tampering_rejections']==4
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='arc231_results.json');args=parser.parse_args()
    t0=time.monotonic();d=audit();d['elapsed_sec']=round(time.monotonic()-t0,3)
    with open(args.output,'w') as f:json.dump(d,f,indent=2,sort_keys=True)
    print(json.dumps(d,indent=2,sort_keys=True))
