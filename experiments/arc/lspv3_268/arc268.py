#!/usr/bin/env python3
"""LSPV-3 run 268: restricted Horn minimum guard support via Set Cover.
Independent verification in verify268.py. Non-native selected event counts.
"""
from __future__ import annotations
import collections, itertools, json, pathlib, argparse, random, math, hashlib
import arc267 as prior

# All source clauses have at most 3 literals; a tuple is an ORIGINAL clause.
COVERS = {
 'tiny3': [{0,1},{1,2},{0,2},{2}],
 'cycle5': [{i,(i+1)%5} for i in range(5)],
 'greedy_gap6': [{0,1,2,3},{0,1,4},{2,3,5},{4},{5}],
 'random5x6': [{0,1,2},{0,3},{1,3,4},{2,4},{0,2,4},{1,4}],
}

def make_horn(sets):
    universe=sorted(set.union(*sets)); s=len(sets); m=len(universe)
    assert universe==list(range(m)) and m>=2
    # original d_i positive assumptions, e_u element predicates, chain AND nodes
    d=list(range(1,s+1));e=list(range(s+1,s+1+m));t=s+m+1
    src=[]; origin=[]
    for i,ss in enumerate(sets):
        for u in sorted(ss):
            src.append((-d[i],e[u]));origin.append(('element',i,u))
    # chain all e_u using at most three literals per original Horn clause
    if m==2:src.append((-e[0],-e[1],t));origin.append(('final',0,0))
    else:
        z=t+1
        src.append((-e[0],-e[1],z));origin.append(('and',0,1))
        prev=z
        for u in range(2,m):
            last=(u==m-1); nxt=t if last else t+u
            src.append((-prev,-e[u],nxt));origin.append(('final' if last else 'and',u,0));prev=nxt
    # For every source input, all-false assignment satisfies H; all-true also does.
    return src,d,t,origin

def closure(F, cube, counts=None):
    """Horn forward chaining and checked clause-index proof trace; no SAT oracle."""
    a={abs(l):int(l>0) for l in cube}; reason=[];change=True
    while change:
        change=False
        for j,c in enumerate(F,1):
            if counts is not None:counts['clause_scan']+=1;counts['literal_scan']+=len(c)
            v=[l for l in c if abs(l) not in a]
            if any(abs(l) in a and a[abs(l)]==int(l>0) for l in c):continue
            if not v:return {'label':'UNSAT','assignment':a,'source_contradiction':j,'proof':reason}
            if len(v)==1:
                x=v[0];a[abs(x)]=int(x>0); reason.append([j,x]);change=True;break
    # Horn least model: set all unforced variables to false. Check all original clauses.
    for c in F:
        if not any(a.get(abs(l),0)==int(l>0) for l in c):
            raise AssertionError('Horn least-model error')
    return {'label':'SAT','assignment':a,'proof':reason}

def implicates(F,G,t,counts=None):
    return closure(F,[i for i in G]+[-t],counts)['label']=='UNSAT'

def greedy(sets):
    left=set.union(*sets); chosen=[]
    while left:
        candidates=[i for i in range(len(sets)) if i not in chosen]
        v=max(candidates,key=lambda i:(len(left&sets[i]),-i))
        assert left&sets[v]
        chosen.append(v);left-=sets[v]
    return chosen

def optimal_source(F,d,t,counts):
    """Actual candidate subset enumeration plus original-source UP proof queries."""
    for size in range(len(d)+1):
        for idxs in itertools.combinations(range(len(d)),size):
            counts['candidate_subsets']+=1
            G=[d[i] for i in idxs]
            if implicates(F,G,t,counts):return list(idxs)
    raise AssertionError('all set assumptions are known to force t')

def deletion_min(F,d,t,counts):
    S=d[:]
    for v in d:
        counts['candidate_subsets']+=1
        T=[x for x in S if x!=v]
        if implicates(F,T,t,counts):S=T
    return [d.index(v) for v in S]

def solver(F):
    """Exact staged solver, with exhaustive complete DPLL fallback.
    The diagnostic S/U matrix and Gray trails do NOT influence decisions.
    All class recognition and failed tests are charged.
    """
    count=collections.Counter();n=prior.nvars(F)
    count['input_bits']=prior.encode_bits(F)
    count['endpoint_literal_reads']=2*sum(len(c) for c in F)
    for bit in (0,1):
        a={v:bit for v in range(1,n+1)}
        if prior.sat_source(F,a):
            count['witness_recheck_lits']+=sum(len(c) for c in F)
            return {'method':'endpoint','label':'SAT','nodes':0,'events':dict(count),'work':sum(count.values())}
    for c in F:count['horn_detect_lits']+=len(c)
    if all(sum(l>0 for l in c)<=1 for c in F):
        cc=collections.Counter(); res=closure(F,[],cc)
        count.update(cc);count['certificate_replay_lits']+=sum(len(c) for c in F)
        return {'method':'Horn-UP','label':res['label'],'nodes':0,'events':dict(count),'work':sum(count.values()),'proof':res['proof']}
    for c in F:count['Krom_detect_lits']+=len(c)
    # The complete implication graph is built only if all clauses are binary/units.
    if all(len(c)<=2 for c in F):
        # A real, deterministic 2-SAT SCC decider with original-source edges.
        n2=2*n; E=[[] for _ in range(n2)]; R=[[] for _ in range(n2)]
        idx=lambda l:2*(abs(l)-1)+(1 if l>0 else 0)
        for c in F:
            if len(c)==0:
                return {'method':'2SAT-SCC','label':'UNSAT','nodes':0,'work':sum(count.values()),'events':dict(count)}
            if len(c)==1:pairs=[(-c[0],c[0])]
            else:pairs=[(-c[0],c[1]),(-c[1],c[0])]
            for u,v in pairs:
                i,j=idx(u),idx(v);E[i].append(j);R[j].append(i);count['scc_edge_inserts']+=1
        visited=set();order=[]
        def dfs(v):
            visited.add(v);count['scc_visited']+=1
            for u in E[v]:
                count['scc_edge_walk']+=1
                if u not in visited:dfs(u)
            order.append(v)
        for v in range(n2):
            if v not in visited:dfs(v)
        comp=[-1]*n2
        def back(v,cid):
            comp[v]=cid;count['scc_visited']+=1
            for u in R[v]:
                count['scc_edge_walk']+=1
                if comp[u]<0:back(u,cid)
        cid=0
        for v in reversed(order):
            if comp[v]<0:back(v,cid);cid+=1
        if any(comp[2*(v-1)]==comp[2*(v-1)+1] for v in range(1,n+1)):
            return {'method':'2SAT-SCC','label':'UNSAT','nodes':0,'work':sum(count.values()),'events':dict(count)}
        witness={v:int(comp[2*(v-1)+1]>comp[2*(v-1)]) for v in range(1,n+1)}
        if not prior.sat_source(F,witness):raise AssertionError('bad 2SAT SCC witness')
        count['witness_recheck_lits']+=sum(len(c) for c in F)
        return {'method':'2SAT-SCC','label':'SAT','nodes':0,'work':sum(count.values()),'events':dict(count)}
    # A sound complete XOR detector: recognize 4 distinct clauses per support
    # that forbid one entire parity class, solve over GF(2) by elimination.
    groups=collections.defaultdict(list)
    for c in F:
        count['xor_scan_lits']+=len(c)
        if len(c)!=3 or len(set(map(abs,c)))!=3:groups=None;break
        groups[tuple(sorted(map(abs,c)))].append(c)
    if groups and all(len(v)==4 for v in groups.values()):
        equations=[];ok=True
        for support,cs in groups.items():
            forbidden={tuple(int(next(l for l in c if abs(l)==v)<0) for v in support) for c in cs}
            count['xor_validation_rows']+=len(cs)*3
            if len(forbidden)!=4 or len({sum(x)%2 for x in forbidden})!=1:ok=False;break
            required=1-(sum(next(iter(forbidden)))%2)
            equations.append((sum(1<<(v-1) for v in support),required))
        if ok:
            piv={}; inconsistent=False
            for mask,b in equations:
                while mask:
                    x=mask.bit_length()-1
                    count['gf2_xor_rows']+=1
                    if x not in piv:piv[x]=(mask,b);break
                    mask ^=piv[x][0];b^=piv[x][1]
                if not mask and b:inconsistent=True;break
            if inconsistent:
                return {'method':'complete-XOR-GE','label':'UNSAT','nodes':0,'work':sum(count.values()),'events':dict(count)}
            a=[0]*n
            for x in sorted(piv):
                mask,b=piv[x];a[x]=b ^ (sum(a[k] for k in range(x) if mask>>k&1)%2)
            witness={i+1:v for i,v in enumerate(a)}
            if not prior.sat_source(F,witness):raise AssertionError('bad GF2 witness')
            count['witness_recheck_lits']+=sum(len(c) for c in F)
            return {'method':'complete-XOR-GE','label':'SAT','nodes':0,'work':sum(count.values()),'events':dict(count)}
    base=prior.dpll(F)
    count['failed_detection_guest']+=base['selected_operations']
    return {'method':'UP-DPLL-fallback','label':base['decision'],'nodes':base['nodes'],'work':sum(count.values()),'events':dict(count)}

def charged_solver(F):
    out=solver(F)
    n=prior.nvars(F); source=prior.encode_bits(F); w=max(1,math.ceil(math.log2(n+2)))
    # Host implementation holds more space; this is a declared symbolic envelope
    # for source, policy records, up to 2-SAT edges, proof stack and fallback.
    bound=source+max(2*n*w+4*len(F)*w,source+2*n*w)
    out['declared_live_bit_envelope']=bound
    out['native_FLMV_space_verified']=False
    return out

def run():
    out={'schema':'horn-support268-v1','explanation':'Original clauses, full endpoints and local S/U controls; experiment uses no free advice','cases':{},'general_controls':{}}
    for name, sets in COVERS.items():
        F,d,t,origin=make_horn(sets); all_set=list(range(len(d)))
        count_opt=collections.Counter();count_del=collections.Counter();count_g=collections.Counter()
        opt=optimal_source(F,d,t,count_opt);dele=deletion_min(F,d,t,count_del);gre=greedy(sets)
        assert len(opt)<=len(gre) and implicates(F,[d[i] for i in opt],t)
        # all non-cover subsets have a source-checked SAT completion with t=0
        subset_truth=[]
        for mask in range(1<<len(d)):
            G=[d[i] for i in range(len(d)) if mask>>i&1]
            b=implicates(F,G,t,count_g)
            direct=set.union(*(sets[i-1] for i in G)) if G else set()
            assert b==(direct==set.union(*sets))
            subset_truth.append(int(b))
        sat=F+[(x,) for x in d]+[(t,)]; unsat=F+[(x,) for x in d]+[(-t,)]
        sr=charged_solver(sat);ur=charged_solver(unsat);bs=prior.dpll(sat);bu=prior.dpll(unsat)
        assert (sr['label'],ur['label'])==('SAT','UNSAT')==(bs['decision'],bu['decision'])
        out['cases'][name]={'sets':[sorted(x) for x in sets],'source_H':[list(c) for c in F],
            'source_clause_origin':origin,'assumptions':d,'target':t,'optimal_guard_indices':opt,
            'greedy_guard_indices':gre,'deletion_guard_indices':dele,'subset_implications':subset_truth,
            'mining_work':dict(count_opt),'deletion_work':dict(count_del),
            'all_subset_validation_work':dict(count_g),
            'sat_source':[list(c) for c in sat],'unsat_source':[list(c) for c in unsat],
            'sat_solver':sr,'unsat_solver':ur,'sat_dpll':{k:bs[k] for k in ('decision','nodes','selected_operations')},
            'unsat_dpll':{k:bu[k] for k in ('decision','nodes','selected_operations')},
            'audit_SAT':prior.audit_extremes(sat),'audit_UNSAT':prior.audit_extremes(unsat)}
    more={k:v for k,v in prior.cases().items() if k in ['W1_UNSAT','SWAP6_SAT','W1_RENAMED_UNSAT','SWAP6_RENAMED_SAT','XOR4_EVEN_SAT','XOR4_ODD_UNSAT','KROM_SAT','KROM_UNSAT','HORN_CHAIN_SAT','HORN_CHAIN_UNSAT']}
    for name,F in more.items():
        ad=charged_solver(F);base=prior.dpll(F)
        assert ad['label']==base['decision']
        out['general_controls'][name]={'original_clauses':[list(c) for c in F],
            'baseline_nodes':base['nodes'],'baseline_work':base['selected_operations'],
            'adaptive':ad,'extrema':prior.audit_extremes(F)}
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    res=run();pathlib.Path(a.output).write_text(json.dumps(res,indent=1,sort_keys=True)+'\n')
    print(json.dumps({'covers':len(res['cases']),'controls':len(res['general_controls']),
                      'guards':{k:[len(v['optimal_guard_indices']),len(v['greedy_guard_indices'])] for k,v in res['cases'].items()}}))