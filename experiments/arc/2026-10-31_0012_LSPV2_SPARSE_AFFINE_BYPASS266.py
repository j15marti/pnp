#!/usr/bin/env python3
"""LSPV-2 AFFINE-BYPASS266: authenticated 3CNF parity projection and charged output.
Run: python affine_bypass266.py --out results266.json
All numbers are Python event proxies, not FLMV tape bounds.
"""
import argparse,collections,itertools,json,random,time,math,hashlib,sys
from pathlib import Path

SEED=2661031

def satisfied(c,a):
    return any((a[abs(x)] == (x>0)) for x in c)

def parity(k): return k.bit_count()&1

def xor3(x,y,z,rhs=0):
    out=[]
    for s in itertools.product((0,1),repeat=3):
        if (sum(s)&1)!=rhs:
            out.append(tuple(v if not bit else -v for v,bit in zip((x,y,z),s)))
    return out

def pin3(x,u,v,wanted):
    return [tuple((x if wanted else -x, u if not a else -u, v if not b else -v)) for a,b in itertools.product((0,1),repeat=2)]

def h7(vars_,target):
    return [tuple(v if not bit else -v for v,bit in zip(vars_,s)) for s in itertools.product((0,1), repeat=3) if tuple(s)!=tuple(target)]

def build_family(b,k,target_parity=0, conflicting=False):
    assert b==4
    # H7 pins the boundary in overlapping triples without any complete 4-clause affine block.
    first=(0,0,1)
    last=(0,1,1)  # unique boundary assignment 0011 has XOR parity zero.
    clauses=h7((1,2,3),first)+h7((2,3,4),last)
    nextid=b+1
    for copy in range(k):
        z=1
        for j in range(2,b+1):
            out=nextid;nextid+=1
            clauses+=xor3(z,j,out,0)
            z=out
        u,v=nextid,nextid+1;nextid+=2
        charge=(1-target_parity) if conflicting and copy==k-1 else target_parity
        clauses+=pin3(z,u,v,charge)
    return clauses,nextid-1

def signed_rename(F,n,seed):
    rng=random.Random(seed);p=list(range(1,n+1));rng.shuffle(p)
    neg={i:rng.randrange(2) for i in range(1,n+1)}
    return [tuple((1 if l>0 else -1)*( -1 if neg[abs(l)] else 1)*p[abs(l)-1] for l in c) for c in F],dict(enumerate(p,1)),neg

def recognize(F,stats):
    groups=collections.defaultdict(list)
    for j,c in enumerate(F):
        stats['source_clause_reads']+=1; stats['source_literal_reads']+=len(c)
        if len(c)==3 and len({abs(x) for x in c})==3:
            groups[tuple(sorted(abs(x) for x in c))].append(j)
    taken=set();blocks=[];rows=[]
    for support,ids in sorted(groups.items()):
        stats['recognition_tests']+=1
        if len(ids)!=4: continue
        forbidden=set()
        for j in ids:
            c=F[j]; falsifier=tuple(0 if next(l for l in c if abs(l)==v)>0 else 1 for v in support)
            forbidden.add(falsifier)
        if len(forbidden)!=4:continue
        p={sum(t)&1 for t in forbidden}
        e=None;kind=None
        if len(p)==1:
            kind='xor3'; e=(sum(1<<v for v in support),1-next(iter(p)))
        else:
            for q,v in enumerate(support):
                vals={t[q] for t in forbidden}
                if len(vals)==1:
                    other={tuple(t[i] for i in range(3) if i!=q) for t in forbidden}
                    if len(other)==4:kind='pin';e=(1<<v,1-next(iter(vals)));break
        if kind is None:continue
        taken.update(ids)
        block={'kind':kind,'support':support,'clause_indices':ids,'mask':e[0],'rhs':e[1]}
        blocks.append(block)
        rows.append({'mask':e[0],'rhs':e[1],'support':[v for v in support if e[0]>>v&1], 'orig_row_id':len(rows),'clause_indices':ids})
    H=[(j,c) for j,c in enumerate(F) if j not in taken]
    B=sorted({abs(l) for _,c in H for l in c})
    return blocks,rows,H,B

def eliminate(rows,B,n,stats):
    Bset=set(B);P=[i for i in range(1,n+1) if i not in Bset]
    basis=[[r['mask'],r['rhs'],1<<i] for i,r in enumerate(rows)]
    idx=0
    for col in P:
        bit=1<<col
        t=next((j for j in range(idx,len(basis)) if basis[j][0]&bit),None)
        stats['gauss_row_probes']+=max(0,len(basis)-idx)
        if t is None:continue
        basis[idx],basis[t]=basis[t],basis[idx]
        for j in range(len(basis)):
            if j!=idx and (basis[j][0]&bit):
                basis[j][0]^=basis[idx][0];basis[j][1]^=basis[idx][1];basis[j][2]^=basis[idx][2]
                stats['gauss_row_xors']+=1
        idx+=1
    proj=[x for x in basis[idx:] if x[0] or x[1]]
    # RREF on the projected boundary rows; keep a source-block provenance combination.
    j=0
    for col in B:
        t=next((q for q in range(j,len(proj)) if proj[q][0] & (1<<col)),None)
        if t is None:continue
        proj[j],proj[t]=proj[t],proj[j]
        for q in range(len(proj)):
            if q!=j and (proj[q][0] & (1<<col)):
                for t1 in range(3):proj[q][t1]^=proj[j][t1]
                stats['gauss_row_xors']+=1
        j+=1
    contradiction=next((p for p in proj if p[0]==0 and p[1]==1),None)
    if contradiction is not None:proj=[contradiction]
    else: proj=[p for p in proj if p[0]]
    return [{'mask':q[0],'rhs':q[1],'source_row_ids':[t for t in range(len(rows)) if q[2]>>t&1]} for q in proj],P

def eliminate_sparse(rows,B,n,stats):
    """Exact existential GF(2) elimination with genuinely sparse supports and source-row provenance.
    This is a charged in-memory word-RAM analogue; no FLMV time bound is claimed.
    """
    private=set(range(1,n+1))-set(B)
    active={i:[set(row['support']), row['rhs'],{i}]
            for i,row in enumerate(rows)}
    incidence={v:set() for v in private}
    for k,(support,rhs,prov) in active.items():
        for v in support:
            if v in private:incidence[v].add(k);stats['initial_incidence_inserts']+=1
        stats['sparse_initial_support_reads']+=len(support)
    for v in sorted(private):
        bucket=sorted(incidence[v]);stats['private_degree_tests']+=1
        stats['bucket_sort_proxy']+=len(bucket)*math.ceil(math.log2(len(bucket)+1))
        stats['max_live_private_degree']=max(stats['max_live_private_degree'],len(bucket))
        if not bucket:continue
        p=bucket[0]
        pv,pr,pp=active[p]
        for k in bucket[1:]:
            old,rhs,prov=active[k]
            new=old.symmetric_difference(pv);newrhs=rhs^pr;newprov=prov.symmetric_difference(pp)
            stats['sparse_support_touches']+=len(old)+len(pv)+len(new)
            stats['sparse_provenance_touches']+=len(prov)+len(pp)+len(newprov)
            stats['sparse_row_xors']+=1
            for t in old:
                if t in private:incidence[t].remove(k);stats['incidence_mutations']+=1
            for t in new:
                if t in private:incidence[t].add(k);stats['incidence_mutations']+=1
            active[k]=[new,newrhs,newprov]
        for t in pv:
            if t in private:incidence[t].remove(p);stats['incidence_mutations']+=1
        del active[p]
    projected=[]
    for support,rhs,prov in active.values():
        assert not support.intersection(private)
        if support or rhs:projected.append([sum(1<<v for v in support),rhs,sum(1<<v for v in prov)])
    # RREF on boundary variables (small for measured compression families), retain provenance.
    j=0
    for v in B:
        t=next((i for i in range(j,len(projected)) if projected[i][0]&(1<<v)),None)
        stats['boundary_row_tests']+=max(0,len(projected)-j)
        if t is None:continue
        projected[j],projected[t]=projected[t],projected[j]
        for k in range(len(projected)):
            if k!=j and projected[k][0]&(1<<v):
                for h in range(3):projected[k][h]^=projected[j][h]
                stats['boundary_row_xors']+=1
        j+=1
    contradiction=next((r for r in projected if r[0]==0 and r[1]==1),None)
    projected=([contradiction] if contradiction is not None else [r for r in projected if r[0]])
    return [{'mask':r[0],'rhs':r[1],'source_row_ids':[q for q in range(len(rows)) if r[2]>>q&1]} for r in projected],sorted(private)

def encode_projected(H,B,projected):
    relabel={x:i+1 for i,x in enumerate(B)}
    out=[tuple(relabel[abs(l)]*(1 if l>0 else -1) for l in c) for _,c in H]
    nextid=len(B)+1
    for row in projected:
        xs=[relabel[x] for x in B if (row['mask']>>x)&1];rhs=row['rhs']
        if not xs:
            if rhs==1:out=[tuple()];break
        elif len(xs)==1:out.append((xs[0] if rhs else -xs[0],))
        elif len(xs)==2:
            x,y=xs
            out.extend([(x,y),(-x,-y)] if rhs else [(x,-y),(-x,y)])
        else:
            a=xs[0]
            for x in xs[1:-2]:
                z=nextid;nextid+=1;out.extend(xor3(a,x,z,0));a=z
            out.extend(xor3(a,xs[-2],xs[-1],rhs))
    return out, nextid-1, relabel

def solve_linear(rows,Bvals,n,stats):
    piv={};bs=0;bm=0
    for x,v in Bvals.items():bs|=int(v)<<x;bm|=1<<x
    for row in rows:
        mask=row['mask'] & ~bm;rhs=row['rhs'] ^ parity(row['mask']&bs)
        stats['reconstruction_support_reads']+=len(row['support'])
        while mask:
            p=mask.bit_length()-1
            stats['reconstruction_pivot_tests']+=1
            if p not in piv:piv[p]=(mask,rhs);break
            mask^=piv[p][0];rhs^=piv[p][1]
            stats['reconstruction_row_xors']+=1
        if not mask and rhs:return None
    a=dict(Bvals)
    for p,(mask,rhs) in sorted(piv.items()):
        v=rhs;rem=mask & ~(1<<p)
        while rem:
            bit=rem&-rem;j=bit.bit_length()-1;rem^=bit
            v^=a.get(j,0);stats['reconstruction_bit_reads']+=1
        a[p]=v
    for j in range(1,n+1):a.setdefault(j,0)
    return a

def dpll(F,n,limit=5_000_000):
    stat=collections.Counter()
    def go(a):
        stat['nodes']+=1
        if stat['nodes']>limit:raise RuntimeError('DPLL_NODE_CAP')
        a=dict(a)
        while True:
            unit=None;all_sat=True
            for j,c in enumerate(F):
                stat['clause_scans']+=1;undec=[];sat=False
                for l in c:
                    stat['literal_tests']+=1
                    v=abs(l)
                    if v in a:
                        if a[v]==int(l>0):sat=True;break
                    else:undec.append(l)
                if sat:continue
                all_sat=False
                if len(undec)==0:
                    stat['conflicts']+=1
                    return None
                if len(undec)==1:unit=undec[0];break
            if all_sat:
                for x in range(1,n+1):a.setdefault(x,0)
                return a
            if unit is None:break
            v=abs(unit); val=int(unit>0)
            if v in a and a[v]!=val:return None
            a[v]=val;stat['propagations']+=1
        # Branch on the first unassigned variable in an unsatisfied clause.
        x=next(abs(l) for c in F for l in c if abs(l) not in a)
        stat['branches']+=1
        for bit in (0,1):
            b=go({**a,x:bit})
            if b is not None:return b
        return None
    ans=go({})
    return ans,dict(stat)

def unsat_tree(F,n):
    """Construct a finite exact DPLL+UP refutation with explicit clause reasons.
    Leaf nodes carry an input-source or emitted-child clause index falsified by its
    proved assignments. No invocation of a semantic UNSAT oracle.
    """
    def rec(assignment):
        a=dict(assignment);units=[]
        while True:
            next_unit=None;conflict=None;all_sat=True
            for j,c in enumerate(F):
                sat=False;undec=[]
                for lit in c:
                    v=abs(lit)
                    if v in a:
                        if a[v]==int(lit>0):sat=True;break
                    else:undec.append(lit)
                if sat:continue
                all_sat=False
                if not undec:conflict=j;break
                if len(undec)==1:next_unit=(undec[0],j);break
            if conflict is not None:
                return {'units':units,'conflict_source_clause':conflict}
            if all_sat:raise AssertionError('UNSAT proof requested for a SAT formula')
            if next_unit is None:break
            lit,j=next_unit;v=abs(lit)
            assert v not in a
            a[v]=int(lit>0)
            units.append({'variable':v,'value':a[v],'reason_clause':j})
        branch=next(abs(l) for c in F for l in c if abs(l) not in a)
        return {'units':units,'branch':branch,'children':[rec({**a,branch:0}),rec({**a,branch:1})]}
    return rec({})

def count_proof_nodes(node):
    return 1+sum(count_proof_nodes(c) for c in node.get('children',[]))

def count_proof_units(node):
    return len(node['units'])+sum(count_proof_units(c) for c in node.get('children',[]))

def count_proof_replay_literals(node,F):
    total=sum(len(F[u['reason_clause']]) for u in node['units'])
    if 'conflict_source_clause' in node:total+=len(F[node['conflict_source_clause']])
    return total+sum(count_proof_replay_literals(c,F) for c in node.get('children',[]))

def dimacs(F,n):
    return f'p cnf {n} {len(F)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in F)

def extremes(F,n,maxpairs=12):
    audit=[]
    for j,c in enumerate(F):
        if len(c)!=3 or len({abs(l) for l in c})!=3:continue
        arr=[{'variable':abs(l),'signed_occurrence':l,'S':int(l>0),'invert_S_U':int(l<0),'U':int(l<0),'invert_U_S':int(l>0)} for l in c]
        audit.append({'source_clause':j,'occurrences':arr})
    pair=[]
    for a,b in itertools.combinations(audit[:maxpairs],2):
        modes={}
        for q,r in itertools.product(('S','U'),repeat=2):
            assignments={};possible=True
            for w,mode in ((a,q),(b,r)):
                for t in w['occurrences']:
                    v=t['variable'];x=t[mode]
                    if v in assignments and assignments[v]!=x:possible=False
                    assignments[v]=x
            modes[q+r]=possible
        pair.append({'source_indices':[a['source_clause'],b['source_clause']],**modes})
    # Real, coherent 0^n, 1^n, single and two flips and full inversion.
    select=list(range(1,min(n,2)+1))
    layers=[{},dict.fromkeys(range(1,n+1),1)]
    if select:layers.append({select[0]:1})
    if len(select)>1:layers.append({v:1 for v in select})
    frames=[]
    for a in layers:
        ca={i:int(a.get(i,0)) for i in range(1,n+1)}
        counts=[sum(ca[abs(l)]==int(l>0) for l in c) for c in F]
        hist=[sum(v==r for v,c in zip(counts,F) if len(c)==3) for r in range(4)]
        frames.append({'ones':sorted(i for i,x in ca.items() if x),'source_true_counts':counts,'N0_N1_N2_N3_width3':hist,'satisfied':all(v>0 for v in counts)})
    return {'occurrences':audit,'pairs_checked':pair,'coherent_flip_frames':frames}

def sample_resolvents(F,limit=8):
    found=[]
    for i,c in enumerate(F[:min(len(F),80)]):
        for j in range(i+1,min(len(F),80)):
            d=F[j]
            for l in c:
                if -l not in d:continue
                r=set(c)|set(d);r.discard(l);r.discard(-l)
                if any(-x in r for x in r):continue
                vals=sorted(r,key=lambda x:(abs(x),x<0))
                rec={'source_parents':[i,j],'pivot':abs(l),'clause':vals,'prohibited_cube':{str(abs(x)):int(x<0) for x in vals}}
                if rec not in found:found.append(rec)
                if len(found)>=limit:return found
    return found

def deepbytes(obj):
    seen=set()
    def visit(x):
        k=id(x)
        if k in seen:return 0
        seen.add(k);size=sys.getsizeof(x)
        if isinstance(x,dict):size+=sum(visit(a)+visit(b) for a,b in x.items())
        elif isinstance(x,(list,tuple,set)):size+=sum(visit(t) for t in x)
        return size
    return visit(obj)

def run_one(name,F,n,benchmark=False,diagnostics=False):
    started=time.monotonic();st=collections.Counter();N=len(dimacs(F,n))
    blocks,rows,H,B=recognize(F,st)
    # Selector pays the complete incidence scan; no semantic class answer is free.
    Bset=set(B)
    degrees=collections.Counter(v for row in rows for v in row['support'] if v not in Bset)
    st['policy_discovery_row_var_probes']=sum(len(row['support']) for row in rows)
    maxdegree=max(degrees.values(),default=0)
    choice='sparse' if maxdegree<=2 else 'dense'
    st['policy_selections']=1
    if choice=='sparse':project,P=eliminate_sparse(rows,B,n,st)
    else:project,P=eliminate(rows,B,n,st)
    child,nchild,rmap=encode_projected(H,B,project)
    M=len(dimacs(child,nchild));st['child_output_bits']=M
    st['child_input_bits']=N
    st['source_scan_bits_lower_bound']=N
    st['private_variables']=len(P)
    st['boundary_variables']=len(B)
    st['retained_source_clause_records']=len(F)
    st['source_rows']=len(rows)
    st['projected_rows']=len(project)
    ca,childsearch=dpll(child,nchild)
    if ca is not None:
        original_B={x:ca[q] for x,q in rmap.items()}
        original=solve_linear(rows,original_B,n,st)
        assert original is not None
        for c in F:
            st['source_witness_clauses']+=1
            sat=False
            for l in c:
                st['source_witness_literal_tests']+=1
                if original[abs(l)]==int(l>0):sat=True;break
            assert sat
    else:original=None
    base=None
    if benchmark:
        ab,basest=dpll(F,n,limit=250000)
        assert (ab is not None)==(ca is not None)
        if ab is not None:assert all(satisfied(c,ab) for c in F)
        base=basest
    shortening=(M <= math.isqrt(N))
    route='short_child_guest' if shortening else 'exact_source_fallback'
    st['child_guest_calls']=int(shortening)
    st['strategy_switches']=1
    st['failed_length_candidates']=int(not shortening)
    st['source_fallbacks']=int(not shortening)
    st['parser_input_bits_charged']=N
    st['retained_python_heap_bytes_snapshot']=deepbytes((F,blocks,rows,H,B,project,P,child,ca,original))
    chosen=childsearch if shortening else base
    def solver_events(c):
        return sum(c.get(t,0) for t in ('nodes','clause_scans','literal_tests','propagations','branches','conflicts')) if c else 0
    accounting_keys=('source_literal_reads','policy_discovery_row_var_probes','initial_incidence_inserts',
        'sparse_initial_support_reads','private_degree_tests','bucket_sort_proxy',
        'sparse_row_xors','sparse_support_touches','sparse_provenance_touches','incidence_mutations',
        'boundary_row_tests','boundary_row_xors','gauss_row_probes','gauss_row_xors',
        'reconstruction_support_reads','reconstruction_pivot_tests','reconstruction_row_xors',
        'reconstruction_bit_reads','source_witness_clauses','source_witness_literal_tests',
        'source_clause_reads','recognition_tests','policy_selections','strategy_switches',
        'failed_length_candidates','source_fallbacks','child_guest_calls')
    local_proxy=N+M+sum(st.get(k,0) for k in accounting_keys)
    st['charged_local_event_proxy']=local_proxy
    st['charged_controller_event_proxy']=local_proxy+solver_events(chosen)
    st['charged_baseline_event_proxy']=(N+solver_events(base)) if base else None
    proof=None
    if ca is None:
        proof=unsat_tree(child if shortening else F, nchild if shortening else n)
        st['unsat_proof_nodes']=count_proof_nodes(proof)
        st['unsat_proof_unit_steps']=count_proof_units(proof)
        st['unsat_proof_replay_literal_tests']=count_proof_replay_literals(proof,child if shortening else F)
        # Physical proof/certificate bit length is charged separately from source/child.
        st['unsat_proof_serialized_bits']=len(json.dumps(proof,separators=(',',':')))*8
        st['charged_controller_event_proxy']+=st['unsat_proof_serialized_bits']+st['unsat_proof_replay_literal_tests']
    sample={'name':name,'n_vars':n,'n_clauses':len(F),'source_dimacs_bits':N,'child_dimacs_bits':M,
     'source_clauses':[list(x) for x in F], 'child_clauses':[list(x) for x in child],
     'child_n_vars':nchild,'selected_projection_policy':choice,'controller_route':route,'boundary_vars':B,'private_var_count':len(P),'boundary_relabel':rmap,
     'authenticated_blocks':blocks,'authenticated_rows':rows,'projected_rows':project,
     'ordinary_residual_source_indices':[j for j,c in H],
     'SAT':bool(ca),'child_witness':ca,'source_witness':original,'UNSAT_certificate':proof,
     'child_dpll':childsearch,'source_baseline_dpll':base,
     'ledger':dict(st),'elapsed_seconds':round(time.monotonic()-started,6)}
    if diagnostics:
        sample['source_extreme_audit']=extremes(F,n,maxpairs=(24 if len(F)<=300 else 12))
        sample['resolution_implicates']=sample_resolvents(F)
    assert sample['SAT']==(original is not None)
    return sample

def main(out):
    cases=[];rng=random.Random(SEED)
    for k in (1,2,4,8,16,64,384):
        for parity_target in (0,1):
            F,n=build_family(4,k,parity_target)
            name=f'k{k}_b4_H7_parity{parity_target}'
            cases.append((name,F,n,True,k<=8))
    for k in (2,8,32):
        F,n=build_family(4,k,0,conflicting=True)
        cases.append((f'conflicting_charges_k{k}',F,n,k<=8,k<=8))
    for seed in (13,17,19):
        F,n=build_family(4,3,seed&1)
        R,_,_=signed_rename(F,n,seed)
        cases.append((f'renamed_polarity_seed{seed}',R,n,True,True))
    with open(Path(__file__).with_name('matched_cases260.json'), encoding='utf-8') as source_file:
        matched=json.load(source_file)
        for key,F in matched.items():
            cases.append((key,[tuple(c) for c in F],max(abs(l) for c in F for l in c),True,True))
    # High-width easy, Horn, dual-Horn, Krom, and random controls.
    cases.extend([
        ('easy_highwidth',[(1,2,3,4,5,6,7,8,9,10,11,12)],12,True,True),
        ('horn_sat',[(1,-2,-3),(-1,-2,-3),(2,)],3,True,True),
        ('dualhorn_unsat',[(1,2,3),(-1,),(-2,),(-3,)],3,True,True),
        ('krom_unsat',[(1,2),(-1,2),(1,-2),(-1,-2)],2,True,True)])
    for seed in (100,101,102,103):
        rng=random.Random(seed);F=[]
        for j in range(8):
            s=rng.sample(range(1,7),3);F.append(tuple(v if rng.randrange(2) else -v for v in s))
        cases.append((f'random_{seed}',F,6,True,True))
    samples=[]
    for name,F,n,bench,diagnostic in cases:
        r=run_one(name,F,n,bench,True)
        samples.append(r)
        print(name,'SAT' if r['SAT'] else 'UNSAT','N',r['source_dimacs_bits'],'M',r['child_dimacs_bits'],
              'rows',len(r['projected_rows']),'secs',r['elapsed_seconds'],flush=True)
    raw={'report_id':'LSPV2_AFFINE_BYPASS266','seed':SEED,'mode':'deterministic_exhaustive_finite_controls',
         'reference_scenario':'same-source exact projected ordinary CNF, no arbitrary-A ARC claim',
         'samples':samples}
    Path(out).write_text(json.dumps(raw,sort_keys=True,separators=(',',':')))
    summ={'id':raw['report_id'],'seed':SEED,'cases':len(samples),
      'SAT':sum(s['SAT'] for s in samples),'UNSAT':sum(not s['SAT'] for s in samples),
      'recognized_blocks':sum(len(s['authenticated_blocks']) for s in samples),
      'source_scans':sum(s['ledger']['source_clause_reads'] for s in samples),
      'output_bits':sum(s['child_dimacs_bits'] for s in samples),
      'power_short_cases':[s['name'] for s in samples if s['child_dimacs_bits'] <= math.isqrt(s['source_dimacs_bits'])],
      'baseline':{k:sum(s['source_baseline_dpll'].get(k,0) for s in samples if s['source_baseline_dpll']) for k in ('nodes','literal_tests','clause_scans')},
      'child':{k:sum(s['child_dpll'].get(k,0) for s in samples if s['source_baseline_dpll']) for k in ('nodes','literal_tests','clause_scans')},
      'total_controller_selected_events':sum(s['ledger']['charged_controller_event_proxy'] for s in samples),
      'total_baseline_selected_events':sum(s['ledger']['charged_baseline_event_proxy'] for s in samples if s['ledger']['charged_baseline_event_proxy'] is not None),
      'max_python_heap_snapshot_bytes':max(s['ledger']['retained_python_heap_bytes_snapshot'] for s in samples),
      'output_json_sha256':hashlib.sha256(Path(out).read_bytes()).hexdigest()}
    Path(out).with_name('summary266.json').write_text(json.dumps(summ,indent=2,sort_keys=True))
    print('SUMMARY',json.dumps(summ))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',default='results266.json');a=p.parse_args();main(a.out)
