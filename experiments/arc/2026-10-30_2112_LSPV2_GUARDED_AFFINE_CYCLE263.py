#!/usr/bin/env python3
"""Source-preserving guarded XOR/GF(2) certificate controller, run 263.
No dependence on external packages. All source records are signed original clauses.
Finite controls are not complexity lower bounds. The source-pair resolution and
GF(2) inference are separate, independently checkable proof rule types.
"""
from collections import defaultdict, Counter
from itertools import product
import json, math, random, time, sys, tracemalloc


def sat_clause(c, assignment):
    return any((assignment[abs(l)] == (l > 0)) for l in c)

def eval_cnf(clauses, assignment):
    return all(sat_clause(c, assignment) for c in clauses)

def mvar(F):
    return max([abs(l) for c in F for l in c] or [0])

def xor_bad_clauses(a,b,c,rhs):
    """List of four width-three clauses excluding wrong-parity triples."""
    out=[]
    for x,y,z in product((0,1),repeat=3):
        if (x^y^z)!=rhs:
            out.append(tuple(v if not bit else -v for v,bit in zip((a,b,c),(x,y,z))))
    return out

def force_literal(lit, p,q):
    return [(lit,a*p,b*q) for a,b in product((1,-1),repeat=2)]

def make_cycle(r, mode='free', rename=()):
    assert r>=4 and r%2==0
    anchor=r+1
    guards=list(range(r+2,2*r+2))
    nextvar=2*r+2
    F=[]; rows=[]
    for i in range(r):
        vars_=(i+1, ((i+1)%r)+1, anchor)
        rhs=1 if i==r-1 else 0
        pairs=[]
        for bad_c in xor_bad_clauses(*vars_,rhs):
            z=nextvar;nextvar+=1
            p=len(F)
            F += [(guards[i],bad_c[0],z),(-z,bad_c[1],bad_c[2])]
            pairs.append([p,p+1])
        rows.append(dict(guard=guards[i],vars=list(vars_),rhs=rhs,pairs=pairs))
    if mode!='free':
        fixed=[1]+[0]*(r-1) if mode=='sat' else [0]*r
        for g,v in zip(guards,fixed):
            a,b=nextvar,nextvar+1;nextvar+=2
            F+=force_literal(g if v else -g,a,b)
    if rename:
        neg=set(rename)
        F=[tuple(-l if abs(l) in neg else l for l in clause) for clause in F]
        for row in rows:
            if row['guard'] in neg:row['guard']=-row['guard']
    return F,rows,guards

def discover(F):
    """Recognize only complete authentic parity blocks; no supplied row/index promise.
    Resolve each two-parent private-variable gadget; retain parent indices.
    Row guards may be signed, source-variable names/values may be renamed.
    """
    M=defaultdict(list)
    ops=Counter()
    for j,c in enumerate(F):
        for lit in c:
            M[abs(lit)].append((j,lit));ops['source_literal_reads']+=1
    pairs=[]
    for v,occ in M.items():
        ops['candidate_split_checks']+=1
        if len(occ)!=2 or {1 if x[1]>0 else -1 for x in occ}!={1,-1}:
            ops['rejected_split_candidates']+=1
            continue
        (a,_),(b,_)=occ
        remaining=[l for l in F[a] if abs(l)!=v]+[l for l in F[b] if abs(l)!=v]
        if len(remaining)!=4 or len(set(map(abs,remaining)))!=4:
            ops['rejected_split_candidates']+=1
            continue
        pairs.append(dict(parents=(a,b),res=tuple(remaining),splitvar=v))
    groups=defaultdict(list)
    for pair in pairs:
        for guard in pair['res']:
            triple=tuple(l for l in pair['res'] if l!=guard)
            key=(guard,tuple(sorted(map(abs,triple))))
            groups[key].append((pair,triple))
            ops['guard_template_trials']+=1
    rows=[]
    for (g,vars_),cand in groups.items():
        ops['parity_template_trials']+=1
        # Each data clause must falsify a DISTINCT bad triple, exactly all four
        # assignments of the wrong parity, with disjoint private split parents.
        if len(cand)!=4 or len(set(vars_))!=3:continue
        masks=[]
        for pair,triple in cand:
            signs={abs(x):x for x in triple}
            if len(signs)!=3 or set(signs)!=set(vars_):break
            bad=tuple(int(signs[v]<0) for v in vars_)
            masks.append((bad,pair))
        if len(masks)!=4 or len({p for p,_ in masks})!=4:continue
        parities={sum(p)%2 for p,_ in masks}
        if len(parities)!=1:continue
        expected={p for p in product((0,1),repeat=3) if sum(p)%2 in parities}
        if {p for p,_ in masks}!=expected:continue
        # Same split variable cannot be reused for two rows; source provenance
        # must remain unambiguous. The format allows multiple distinct rows.
        sourcepairs=tuple(tuple(pair['parents']) for _,pair in masks)
        rows.append(dict(guard=g,variables=vars_,rhs=1-next(iter(parities)),parents=sourcepairs))
        ops['authenticated_rows']+=1
    # Distinct source blocks may be discovered twice in pathological encodings.
    # Retain only disjoint four-split blocks to preserve reconstruction policy.
    used=set();out=[]
    for row in sorted(rows,key=lambda x:(min(j for p in x['parents'] for j in p),x['guard'])):
        ps={j for p in row['parents'] for j in p}
        if ps&used:
            ops['overlap_rejections']+=1;continue
        used |= ps;out.append(row)
    ops['recognized_rows']=len(out)
    return out,dict(ops)

def gf2_blocker(rows):
    basis={};trace=[];ops=Counter();skipped=[]
    for index,row in enumerate(rows):
        mask=sum(1<<(v-1) for v in row['variables'])
        rhs=row['rhs'];comb=1<<index
        while mask:
            p=mask.bit_length()-1
            ops['xor_pivots']+=1
            if p not in basis:
                basis[p]=(mask,rhs,comb)
                trace.append(dict(op='basis',row=index,pivot=p))
                break
            old,oldrhs,oldcomb=basis[p]
            mask^=old;rhs^=oldrhs;comb^=oldcomb
            trace.append(dict(op='xor',row=index,pivot=p))
            ops['xor_row_updates']+=1
        else:
            if rhs:
                ids=[i for i in range(len(rows)) if comb>>i&1]
                guards=sorted(set(rows[i]['guard'] for i in ids),key=lambda l:(abs(l),l))
                if any(-x in guards for x in guards):
                    skipped.append(dict(rows=ids,why='tautological_guard_union'))
                    ops['incoherent_dependency_rejections']+=1
                else:
                    ops['source_blockers']+=1
                    return dict(clause=guards,row_ids=ids,trace=trace),dict(ops),skipped
            else:
                ops['dependent_consistent_rows']+=1
    return None,dict(ops),skipped

def dpll(F,extra=()):
    """Complete UP-DPLL, with assignments/actual work counted; no false NO from timeout."""
    clauses=list(map(tuple,F))+list(map(tuple,extra))
    n=mvar(clauses);C=Counter();nodes=[]
    def solve(assigned,depth):
        C['search_nodes']+=1
        assigned=assigned.copy()
        while True:
            changed=False;all_satisfied=True
            for j,c in enumerate(clauses):
                C['clause_scans']+=1
                u=[];s=False
                for lit in c:
                    C['literal_tests']+=1
                    v=abs(lit)
                    if v in assigned:
                        if assigned[v]==(lit>0):s=True;break
                    else:u.append(lit)
                if s:continue
                all_satisfied=False
                if not u:
                    C['conflict_leaves']+=1;nodes.append((depth,j))
                    return None
                if len(u)==1:
                    v=abs(u[0]);val=int(u[0]>0)
                    if v in assigned and assigned[v]!=val:
                        C['conflict_leaves']+=1;return None
                    if v not in assigned:
                        assigned[v]=val;C['unit_assignments']+=1;changed=True
                        break
            if not changed:break
        if all_satisfied:
            witness={i:assigned.get(i,0) for i in range(1,n+1)}
            if not eval_cnf(clauses,witness):raise AssertionError('bad sat witness')
            C['source_witness_literal_tests']+=sum(map(len,F))
            return witness
        # Deterministic max-frequency decision, including assigned bookkeeping
        degree=Counter()
        for c in clauses:
            C['branch_clause_scans']+=1
            if any((abs(l) in assigned and assigned[abs(l)]==(l>0)) for l in c):continue
            for l in c:
                C['branch_literal_checks']+=1
                if abs(l) not in assigned:degree[abs(l)]+=1
        if not degree: raise AssertionError('inconsistent terminal')
        v=max(degree,key=lambda x:(degree[x],-x));C['branch_decisions']+=1
        for bit in (0,1):
            nxt=assigned.copy();nxt[v]=bit
            w=solve(nxt,depth+1)
            if w is not None:return w
        return None
    ans=solve({},0)
    # Fallback tree is not a syntactically emitted resolution proof in this run.
    return ans,dict(C),nodes

def extreme_controls(F,nflips=4):
    n=mvar(F);out={};proper=[(j,tuple(c)) for j,c in enumerate(F) if len(c)==3 and len(set(map(abs,c)))==3]
    out['original_occurrence_targets']=[dict(clause=j,occurrence=k,variable=abs(l),signed_literal=l,
              S=int(l>0),invert_S=int(l<0),U=int(l<0),invert_U=int(l>0))
        for j,c in proper for k,l in enumerate(c)]
    def states(bits):
        a={i:int(bits[i-1]) for i in range(1,n+1)}
        t=[sum(a[abs(l)]==(l>0) for l in c) for c in F]
        cnt=[sum(k==j for k in (t[i] for i,c in enumerate(F) if len(c)==3)) for j in range(4)]
        return dict(bits=''.join(map(str,bits)),true_literal_counts=t,N0_to_N3=cnt,SAT=all(ti>0 for ti in t))
    zero=[0]*n;one=[1]*n
    out['global_0']=states(zero);out['global_1']=states(one)
    out['flips']=[states(zero)]
    arr=zero[:]
    for i in range(min(n,nflips)):
        arr[i]^=1;out['flips'].append(states(arr))
    out['complement_of_last_flip']=states([1-b for b in arr])
    # Complete matrix with clause IDs, and no claim of globally simultaneously
    # realizable S/U targets across all clauses.
    pairs=[]
    for a,(j,c) in enumerate(proper):
        for k,d in proper[a+1:]:
            a_sign={abs(l):int(l>0) for l in c};b_sign={abs(l):int(l>0) for l in d}
            shared=set(a_sign)&set(b_sign)
            same=any(a_sign[v]==b_sign[v] for v in shared)
            opp=any(a_sign[v]!=b_sign[v] for v in shared)
            pairs.append(dict(j=j,k=k,SS=not opp,SU=not same,US=not same,UU=not opp))
    out['clause_pair_extreme_matrix']=pairs
    return out

def selected_work(m):
    return sum(v for k,v in m.items() if k in ('source_literal_reads','candidate_split_checks','guard_template_trials','parity_template_trials',
      'authenticated_rows','recognized_rows','xor_pivots','xor_row_updates','incoherent_dependency_rejections','source_blockers',
      'search_nodes','clause_scans','literal_tests','unit_assignments','conflict_leaves','branch_clause_scans','branch_literal_checks','branch_decisions','source_witness_literal_tests','source_clause_rescan','certificate_checks','policy_recognitions','policy_switches','failed_policy_trials'))

def source_resolve(c1,c2,pivot):
    """Check strict source-resolution node and return deduplicated resolvent."""
    if pivot not in c1 or -pivot not in c2:
        raise AssertionError('invalid resolution pivot')
    r=tuple(sorted(set(c1)-{pivot}|(set(c2)-{-pivot}),key=lambda x:(abs(x),x)))
    if any(-l in r for l in r):raise AssertionError('tautological resolution')
    return r

def source_guard_force_proof(F,literal):
    """Find four original proper3 clauses which resolve to `literal`."""
    groups=defaultdict(dict)
    for j,c in enumerate(F):
        if literal not in c or len(c)!=3:continue
        rem=[l for l in c if l!=literal]
        if len(rem)!=2 or len(set(map(abs,rem)))!=2:continue
        vs=tuple(sorted(map(abs,rem)))
        groups[vs][tuple(1 if next(l for l in rem if abs(l)==v)>0 else 0 for v in vs)]=j
    for (u,v),idx in groups.items():
        if len(idx)!=4:continue
        # A=(l∨u∨v), B=(l∨u∨¬v), C=(l∨¬u∨v), D=(l∨¬u∨¬v)
        a,b,c,d=[idx[bits] for bits in ((1,1),(1,0),(0,1),(0,0))]
        first=source_resolve(F[a],F[b],v)
        second=source_resolve(F[c],F[d],v)
        third=source_resolve(first,second,u)
        if third!=(literal,):raise AssertionError('bad forcing resolution')
        return dict(literal=literal,source_ids=[a,b,c,d],resolved_intermediate=[list(first),list(second),list(third)],pivots=[v,v,u])
    return None

def hybrid_unsat_certificate(F,blocker):
    """A two-calculus certificate, not misrepresented as plain resolution.
    Source resolutions authenticate each row; GF2 proves guarded blocker;
    separate source resolutions derive each opposite guard and the empty clause.
    """
    if not blocker:return None
    forced=[source_guard_force_proof(F,-lit) for lit in blocker['clause']]
    if any(p is None for p in forced):return None
    cur=tuple(blocker['clause']);chain=[]
    for unit in forced:
        v=-unit['literal'];now=tuple(l for l in cur if l!=v)
        chain.append(dict(pivot=v,prior=list(cur),unit=unit['literal'],result=list(now)))
        cur=now
    if cur:raise AssertionError('nonempty final refutation')
    return dict(proof_system='source_resolution_plus_guarded_GF2',source_guard_forces=forced,from_blocker_to_empty=chain)

def test_run():
    t0=time.perf_counter();record={"id":"GUARDED-AFFINE-CYCLE263","seed":202610302112,"cases":{},"falsifiers":{},"status":"COMPUTATIONAL finite tests; restricted mathematical proof separately"}
    base_cases=[]
    for r in (4,6,8):
        for mode in ('free','sat','unsat'):
            F,decl,guards=make_cycle(r,mode)
            base_cases.append((f'cycle_{r}_{mode}',F,1 if mode!='unsat' else 0, {'family':'cycle','r':r,'mode':mode,'guardvars':guards}))
        for mode in ('sat','unsat'):
            F,decl,guards=make_cycle(r,mode,rename=(1,r+1,guards[1],2*r+2))
            base_cases.append((f'cycle_{r}_{mode}_renamed',F,1 if mode!='unsat' else 0,{'family':'cycle','r':r,'mode':mode,'signed_rename':True}))
    # Incomplete block: missing one original source clause invalidates its four-falsifying-pattern certificate.
    F,_,_=make_cycle(4,'free');base_cases.append(('missing_source_parent',F[1:],1,{'family':'incomplete','expected_reject':True}))
    # Crossed guards: individual parity equations conflict but cannot both activate.
    F=[];nv=5
    for g,rhs in ((4,0),(-4,1)):
        for cs in xor_bad_clauses(1,2,3,rhs):
            F.append((g,cs[0],nv));F.append((-nv,cs[1],cs[2]));nv+=1
    base_cases.append(('opposed_guard_tautology',F,1,{'family':'crossguard','expected_tautology':True}))
    # ordinary hard/easy controls; every control preserves original signing.
    base_cases += [('horn',[(1,-2,-3),(-1,2,3)],1,{'family':'easy'}),
        ('dual_horn',[(1,2,-3),(-1,-2,3)],1,{'family':'easy'}),
        ('two_sat',[(1,2),(-1,3),(-2,3),(-3,1)],1,{'family':'easy'}),
        ('easy_high_width',[(1,2,3,4,5),(-1,2,3,4,5)],1,{'family':'easy'}),
        ('parity_sat',xor_bad_clauses(1,2,3,0),1,{'family':'parity'}),
        ('parity_unsat',xor_bad_clauses(1,2,3,0)+xor_bad_clauses(1,2,3,1),0,{'family':'parity'})]
    # Matched strict22 W1 UNSAT / S15 SAT, from the prior independently checked archive.
    try:
        import zipfile
        with zipfile.ZipFile('/mnt/data/LSPV2_TYPED_TRANSACTION260_2026-10-30.zip') as z:
            past=json.loads(z.read('matched_cases260.json'))
            for name,F0 in past.items():
                label=0 if 'UNSAT' in name else 1
                base_cases.append((name,[tuple(c) for c in F0],label,{'family':'prior_verified_strict22'}))
    except Exception as e:
        record['archive_import_error']=repr(e)
    for name,F,label,meta in base_cases:
        t1=time.perf_counter()
        rows,dis=discover(F);blocker,gops,skips=gf2_blocker(rows)
        policy=Counter(dis);policy.update(gops)
        policy['policy_recognitions']=1
        if blocker:
            # Count proof checking: each two-parent resolution and 4-clause parity pattern,
            # and each XOR dependency bit. The checker is written separately.
            sel=[rows[i] for i in blocker['row_ids']]
            for row in sel:
                for a,b in row['parents']:
                    policy['certificate_checks']+=len(F[a])+len(F[b])
                policy['certificate_checks']+=8
            policy['certificate_checks']+=sum(len(row['variables']) for row in sel)
        else:
            policy['failed_policy_trials']=1
        if blocker:
            assert all(l in set([row['guard'] for row in rows]) for l in blocker['clause'])
        baseline,bc,btr=dpll(F)
        hybrid,dc,dtr=dpll(F,[tuple(blocker['clause'])] if blocker else [])
        policy['policy_switches']=1
        for k,v in dc.items(): policy[k]+=v
        actual=int(baseline is not None)
        if actual!=label or (hybrid is None)!=(baseline is None):
            raise AssertionError((name,actual,label,hybrid is None,baseline is None))
        if hybrid is not None and not eval_cnf(F,hybrid):raise AssertionError('bad reconstructed witness')
        Fmeta=meta.copy();Fmeta['n']=mvar(F);Fmeta['m']=len(F)
        rowdump=[dict(row,parents=[list(p) for p in row['parents']]) for row in rows]
        mixed_cert=hybrid_unsat_certificate(F,blocker) if baseline is None else None
        if mixed_cert:
            policy['certificate_checks']+=sum(8 for _ in mixed_cert['source_guard_forces'])+len(mixed_cert['from_blocker_to_empty'])
        result=dict(meta=Fmeta,F=[list(c) for c in F],source_rows=rowdump,blocker=blocker,
            certified_mixed_UNSAT=mixed_cert,
            rejected_dependencies=skips,discovery=dis,algebra=gops,hybrid_ledger=dict(policy),
            baseline_ledger=bc,baseline_nodes=bc.get('search_nodes',0),hybrid_nodes=dc.get('search_nodes',0),
            baseline_selected_work=selected_work(bc),hybrid_selected_work=selected_work(policy),
            baseline_sat_assignment=baseline,hybrid_sat_assignment=hybrid,
            original_extremes=extreme_controls(F,nflips=4),elapsed_seconds=time.perf_counter()-t1)
        if len(F)>120:raise AssertionError('unexpected input size')
        record['cases'][name]=result
    import resource; peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024
    summary={'cases':len(record['cases']),'SAT':sum(x['baseline_sat_assignment'] is not None for x in record['cases'].values()),
       'UNSAT':sum(x['baseline_sat_assignment'] is None for x in record['cases'].values()),
       'blockers':sum(x['blocker'] is not None for x in record['cases'].values()),
       'mixed_UNSAT_certificates':sum(x['certified_mixed_UNSAT'] is not None for x in record['cases'].values()),
       'learned_clause_lengths':sorted([len(x['blocker']['clause']) for x in record['cases'].values() if x['blocker']]),
       'recognition_failures':sum(x['hybrid_ledger'].get('failed_policy_trials',0) for x in record['cases'].values()),
       'baseline_nodes':sum(x['baseline_nodes'] for x in record['cases'].values()),
       'hybrid_nodes':sum(x['hybrid_nodes'] for x in record['cases'].values()),
       'baseline_selected_work':sum(x['baseline_selected_work'] for x in record['cases'].values()),
       'hybrid_selected_work':sum(x['hybrid_selected_work'] for x in record['cases'].values()),
       'original_pair_modes':sum(4*len(x['original_extremes']['clause_pair_extreme_matrix']) for x in record['cases'].values()),
       'peak_python_bytes':peak,'elapsed_seconds':time.perf_counter()-t0}
    record['summary']=summary
    return record

if __name__=='__main__':
    out=test_run();path=sys.argv[1] if len(sys.argv)>1 else 'guarded_affine263_raw.json'
    with open(path,'w') as f:json.dump(out,f,sort_keys=True,separators=(',',':'))
    print(json.dumps(out['summary'],indent=2))