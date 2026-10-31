#!/usr/bin/env python3
"""Reproducible original-source parity cut and policy-acquisition controls.
No claimed native FLMV measurements. Python3 stdlib only.
"""
import argparse, json, hashlib, itertools, math, time, tracemalloc
from collections import Counter

W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
SWAP6=list(W1);SWAP6[9]=(-5,6,-15);SWAP6[13]=(-3,-6,-15)

def edges(k):
    # v in [0,k) top, [k,2k) bottom
    d=[[] for _ in range(2*k)]
    for i in range(k):
        for a,b,e in ((i,(i+1)%k,i+1), (k+i,k+(i+1)%k,k+i+1),(i,k+i,2*k+i+1)):
            d[a].append(e);d[b].append(e)
    return [tuple(sorted(x)) for x in d]

def make_prism(k,charges):
    vv=edges(k); assert len(charges)==2*k
    out=[]
    for v,(a,b,c) in enumerate(vv):
        for pattern in itertools.product((0,1),repeat=3):
            if (sum(pattern)&1)!=charges[v]:
                out.append(tuple((var if bit==0 else -var) for var,bit in zip((a,b,c),pattern)))
    return out

def encode_bits(n,clauses):
    # Declared self-delimited ordinary-CNF encoding: unary n,m, unary clause widths, 1 sign + ceil(log2(n+1)) index
    w=math.ceil(math.log2(n+1))
    return (n+1)+(len(clauses)+1)+sum((len(c)+1)+len(c)*(1+w) for c in clauses)

def true_count(clause,assignment):
    return sum(((assignment>>(abs(l)-1))&1)==(1 if l>0 else 0) for l in clause)

def models(n,clauses,cap=None):
    ans=0;wit=None; checked=0
    for a in range(1<<n):
        checked+=1
        if all(true_count(c,a)>0 for c in clauses):
            ans+=1
            if wit is None: wit=a
    return ans,wit,checked

def local_pattern(clause,state):
    # A locally consistent extreme, not a global occurrence assignment
    return {str(abs(l)):(int(l>0) if state=='S' else int(l<0)) for l in clause}

def endpoint(n,clauses,a):
    ct=[true_count(c,a) for c in clauses]
    return {"mask":a,"histogram":[ct.count(i) for i in range(4)],"statuses":ct,"sat":min(ct)>0 if ct else True}

def compatible(a,b,mode):
    demands={}
    for c,tag in ((a,mode[0]),(b,mode[1])):
        for l in c:
            variable=abs(l); val=int(l>0) if tag=='S' else int(l<0)
            if variable in demands and demands[variable]!=val: return False
            demands[variable]=val
    return True

def pair_masks(clauses):
    # Four-bit mask SS SU US UU; all ORIGINAL clauses.
    return [[(sum((1<<j) for j,t in enumerate(('SS','SU','US','UU')) if compatible(a,b,t))) for b in clauses[i+1:]] for i,a in enumerate(clauses)]

def gray_flip_trail(n,clauses,limit=24):
    hist=Counter(); trail=[];prev=0
    for j in range(min(limit,1<<n)):
        a=j^(j>>1);h=tuple(endpoint(n,clauses,a)['histogram']);hist[str(h)]+=1
        trail.append({"step":j,"assignment":a,"flipped_var":None if j==0 else ((a^prev).bit_length()),"N0":h[0],"N3":h[-1]})
        prev=a
    return trail,dict(hist)


def gray_complete_search(n,clauses):
    # Actual complete Gray-code traversal in proper globally coherent assignments.
    masks=[]
    for c in clauses:
        support=sum(1<<(abs(l)-1) for l in c)
        forbidden=sum(1<<(abs(l)-1) for l in c if l<0)
        masks.append((support,forbidden))
    tests=0
    for j in range(1<<n):
        a=j^(j>>1)
        okay=True
        for sup,bad in masks:
            tests+=1
            if (a&sup)==bad:okay=False;break
        if okay:return {'status':'SAT','witness':a,'visits':j+1,'source_clause_tests':tests}
    return {'status':'EXHAUSTIVE_UNSAT','witness':None,'visits':1<<n,'source_clause_tests':tests}

def greedy_flip(n,clauses,limit=24):
    # deterministic strict descent from 0^n with equal-score stays avoided; never certifies UNSAT
    a=0; visited={a};trail=[];work=0
    for step in range(limit):
        vals=[true_count(c,a) for c in clauses];work+=len(clauses)*3
        trail.append({'step':step,'assignment':a,'N0':vals.count(0),'N3':vals.count(3)})
        if 0 not in vals: return trail,'SAT_WITNESS',work
        best=None
        for x in range(n):
            b=a^(1<<x)
            if b in visited: continue
            count=sum(true_count(c,b)==0 for c in clauses);work+=len(clauses)*3
            if best is None or (count,x)<(best[0],best[1]):best=(count,x,b)
        if best is None or best[0]>=vals.count(0):break
        a=best[2];visited.add(a)
    return trail,'UNRESOLVED',work

def up_dpll(n,clauses,order=None,cut=None,cap_nodes=1000000):
    """Plain UP-first complete DPLL with optional source-proved parity cut check.
    Counters are declared work proxy, not TM transitions.
    """
    stats=Counter(); first_witness=None
    def propagate(ass):
        stats['assignment_copy_slots']+=len(ass)
        ass=dict(ass)
        while True:
            changed=False
            for clause in clauses:
                stats['clause_scans']+=1;stats['literal_inspections']+=len(clause)
                remaining=[]; satisfied=False
                for lit in clause:
                    if abs(lit) in ass:
                        if ass[abs(lit)]==int(lit>0):satisfied=True;break
                    else:remaining.append(lit)
                if satisfied:continue
                if not remaining:return None
                if len(remaining)==1:
                    lit=remaining[0];v=abs(lit);b=int(lit>0)
                    if v in ass and ass[v]!=b:return None
                    if v not in ass:ass[v]=b;changed=True;stats['propagated']+=1
            if not changed:return ass
    def visit(ass):
        nonlocal first_witness
        stats['nodes']+=1
        stats['max_partial_assignment_vars']=max(stats['max_partial_assignment_vars'],len(ass))
        if stats['nodes']>cap_nodes:raise RuntimeError('DPLL node cap; do not interpret as UNSAT')
        ass=propagate(ass)
        if ass is None:
            stats['conflicts']+=1;return False
        if cut:
            vars_cut,required=cut
            stats['cut_checks']+=1
            # charge reading all values, even on incomplete cube
            stats['cut_literal_reads']+=len(vars_cut)
            if all(x in ass for x in vars_cut):
                if (sum(ass[x] for x in vars_cut)&1)!=required:
                    stats['cut_prunes']+=1;return False
        stats['terminal_clause_scans']+=len(clauses)
        stats['terminal_probe_source_lits']+=sum(len(c) for c in clauses)
        if all(any((abs(l) in ass and ass[abs(l)]==int(l>0)) for l in c) for c in clauses):
            a=sum(ass.get(x,0)<<(x-1) for x in range(1,n+1))
            if all(true_count(c,a)>0 for c in clauses):
                first_witness=a;return True
            # partial assignment should already satisfy every clause, so arbitrary padding OK
            raise AssertionError('invalid terminal witness')
        stats['selector_variable_tests']+=n
        avail=[v for v in (order or list(range(1,n+1))) if v not in ass]
        if not avail:stats['conflicts']+=1;return False
        v=avail[0];stats['branches']+=1
        for bit in (0,1):
            stats['branch_assignment_copy_slots']+=len(ass)+1
            ass2=dict(ass);ass2[v]=bit
            if visit(ass2):return True
        return False
    sat=visit({})
    stats['selected_work']=sum(stats[k] for k in ('clause_scans','literal_inspections','propagated','nodes','cut_checks','cut_literal_reads','terminal_clause_scans','terminal_probe_source_lits',
            'selector_variable_tests','assignment_copy_slots','branch_assignment_copy_slots'))
    return bool(sat),first_witness,dict(stats)

def recognize_canonical(k,clauses):
    expected=edges(k);q=len(expected)
    if len(clauses)!=4*q:return None,{'block_queries':0,'literal_reads':0,'reason':'size'}
    bits=[];cnt=Counter()
    for v,triple in enumerate(expected):
        cnt['block_queries']+=1;cnt['literal_reads']+=12
        block=clauses[4*v:4*v+4]; forbidden=[]
        for c in block:
            if len(c)!=3 or tuple(sorted(abs(t) for t in c))!=triple:return None,dict(cnt)
            d={abs(l):int(l<0) for l in c}
            forbidden.append(sum(d[x]<<i for i,x in enumerate(triple)))
        if len(set(forbidden))!=4 or len({(x.bit_count()&1) for x in forbidden})!=1:return None,dict(cnt)
        bits.append(1-(forbidden[0].bit_count()&1))
    return bits,dict(cnt)

def recognize_affine(clauses):
    # Full materialized group detector, not cheap canonical streaming. Source authenticated.
    groups={};work=Counter()
    for c in clauses:
        work['literal_reads']+=len(c)
        if len(c)!=3:return None,dict(work)
        key=tuple(sorted(abs(l) for l in c))
        if len(set(key))!=3:return None,dict(work)
        groups.setdefault(key,[]).append(c)
    eq=[]
    for key,block in sorted(groups.items()):
        work['group_tests']+=1
        if len(block)!=4:return None,dict(work)
        forbidden={sum((int(next(t for t in c if abs(t)==x)<0)<<i) for i,x in enumerate(key)) for c in block}
        if len(forbidden)!=4 or len({x.bit_count()&1 for x in forbidden})!=1:return None,dict(work)
        parity=1-(next(iter(forbidden)).bit_count()&1)
        eq.append((sum(1<<(v-1) for v in key),parity,key))
    return eq,dict(work)

def solve_linear(n,equations):
    # Gaussian elimination with a source row provenance mask; exact both labels.
    piv={}
    for i,(mask,b,_) in enumerate(equations):
        row=[mask,b,1<<i]
        while row[0]:
            p=row[0].bit_length()-1
            if p not in piv:piv[p]=row;break
            q=piv[p];row=[row[0]^q[0],row[1]^q[1],row[2]^q[2]]
        else:
            if row[1]:return {'sat':False,'dependency':[j for j in range(len(equations)) if (row[2]>>j)&1]}
    a=0
    for p,row in sorted(piv.items()):
        rhs=row[1]^((row[0] & ~(1<<p) & a).bit_count()&1)
        if rhs:a|=1<<p
    return {'sat':True,'witness':a}


def horn_decide(n,clauses,dual=False):
    # Source scan is charged even on rejection; dual swaps literal signs.
    ticks=0
    for c in clauses:
        ticks+=len(c)+1
        if sum(((l<0) if dual else (l>0)) for l in c)>1:
            return None,{'source_lit_tests':ticks,'class':'dual_Horn' if dual else 'Horn','accepted':False}
    truth={i:int(dual) for i in range(1,n+1)}
    loops=0
    for _ in range(n+1):
        loops+=1;change=False
        for c in clauses:
            ticks+=len(c)+1
            transformed=[-l if dual else l for l in c]
            positives=[l for l in transformed if l>0]
            negatives=[-l for l in transformed if l<0]
            if all((truth[v]==int(not dual)) for v in negatives):
                if not positives:
                    return {'sat':False}, {'source_lit_tests':ticks,'loops':loops,'accepted':True}
                v=positives[0]
                if truth[v]!=int(not dual):
                    truth[v]=int(not dual);change=True
        if not change:
            witness=sum(truth[v]<<(v-1) for v in range(1,n+1))
            assert all(true_count(c,witness)>0 for c in clauses)
            return {'sat':True,'witness':witness}, {'source_lit_tests':ticks,'loops':loops,'accepted':True}
    raise AssertionError('Horn monotonic closure exceeded n changes')

def krom_decide(n,clauses):
    ticks=0
    for c in clauses:
        ticks+=len(c)+1
        if len(c)>2:return None,{'source_lit_tests':ticks,'accepted':False}
    size=2*n;g=[[] for _ in range(size)];rg=[[] for _ in range(size)]
    def node(l):return 2*(abs(l)-1)+int(l>0)
    for c in clauses:
        if not c:return {'sat':False},{'source_lit_tests':ticks,'accepted':True,'edges':0}
        a=c[0];pairs=[(-a,a)] if len(c)==1 else [(-c[0],c[1]),(-c[1],c[0])]
        for u,v in pairs:
            g[node(u)].append(node(v));rg[node(v)].append(node(u))
    seen=set();order=[];visits=0
    def dfs1(v):
        nonlocal visits
        seen.add(v);visits+=1
        for u in g[v]:
            if u not in seen:dfs1(u)
        order.append(v)
    for v in range(size):
        if v not in seen:dfs1(v)
    comp=[-1]*size
    def dfs2(v,k):
        nonlocal visits
        comp[v]=k;visits+=1
        for u in rg[v]:
            if comp[u]<0:dfs2(u,k)
    for v in reversed(order):
        if comp[v]<0:dfs2(v,max(comp)+1)
    if any(comp[2*i]==comp[2*i+1] for i in range(n)):
        return {'sat':False},{'source_lit_tests':ticks,'accepted':True,'vertices':size,'dfs_visits':visits}
    witness=sum((comp[2*i+1]>comp[2*i])<<i for i in range(n))
    assert all(true_count(c,witness)>0 for c in clauses)
    return {'sat':True,'witness':witness},{'source_lit_tests':ticks,'accepted':True,'vertices':size,'dfs_visits':visits}

def source_extremes(clauses):
    return [{'clause_index':i+1,'literals':list(c),
              'S':local_pattern(c,'S'),'invert_S_is_U':local_pattern(c,'U'),
              'U':local_pattern(c,'U'),'invert_U_is_S':local_pattern(c,'S'),
              'occurrences':[{'var':abs(l),'sign':1 if l>0 else -1,
                              'S':int(l>0),'invert_S':int(l<0),'U':int(l<0),'invert_U':int(l>0)} for l in c]} for i,c in enumerate(clauses)]

def cut_certificate(k,charges,vertices):
    incidence=edges(k)
    counts=Counter(v for i in vertices for v in incidence[i]);boundary=sorted(x for x,t in counts.items() if t%2)
    return {'vertex_ids':[x+1 for x in vertices], 'boundary':boundary,
            'required_parity':sum(charges[v] for v in vertices)&1,
            'derivation':'XOR of exactly these authenticated original parity blocks cancels every twice-covered internal edge'}

def evaluate(name,n,clauses,k=None,charges=None,do_count=True):
    tracemalloc.start();t0=time.perf_counter()
    diag={};stats=Counter()
    all0=endpoint(n,clauses,0);all1=endpoint(n,clauses,(1<<n)-1)
    stats['endpoint_clause_tests']+=2*len(clauses)
    gray,hist=gray_flip_trail(n,clauses)
    gray_full=gray_complete_search(n,clauses)
    greed,greed_status,greed_work=greedy_flip(n,clauses)
    stats['gray_clause_tests']+=len(gray)*len(clauses)
    stats['greedy_selected_work']+=greed_work
    ex=source_extremes(clauses);pm=pair_masks(clauses)
    # diagnostics are laboratory probes, NOT included in candidate controller bound
    stats['diagnostic_pair_tests']+=4*len(clauses)*(len(clauses)-1)//2
    actual_models,witness,assignments=models(n,clauses) if do_count else (None,None,0)
    diagnostic={'occurrences':ex,'pair_matrix_4bit':pm,'endpoints':[all0,all1],
                'gray_first':gray,'gray_histogram':hist,'gray_full':gray_full,'adaptive_flip_first':greed,
                'adaptive_flip_status':greed_status,'full_enumeration_models':actual_models,
                'full_enumeration_assignments':assignments,'first_model':witness}
    # Exact UP first baseline and the same search with authenticated cut on prism;
    # disable full-syndrome termination in controlled cut comparison.
    base_sat,base_w,base=up_dpll(n,clauses)
    recognize=None;blockstats={}
    attempted_k=n//3 if n>=9 and n%3==0 else None
    if attempted_k:
        recognize,blockstats=recognize_canonical(attempted_k,clauses)
    else:
        recognize=None;blockstats={'block_queries':0,'literal_reads':0,'reason':'size_not_matching_canonical_grammar'}
    if recognize is not None:
        assert k==attempted_k
        k=attempted_k
    generic,awork=recognize_affine(clauses)
    affine=solve_linear(n,generic) if generic is not None else None
    # Exactly one policy selected; other tests are separately charged only on rejected policies.
    horn=None;horn_cost={};dual=None;dual_cost={};krom=None;krom_cost={}
    if recognize is None and generic is None:
        horn,horn_cost=horn_decide(n,clauses)
        if horn is None:
            dual,dual_cost=horn_decide(n,clauses,dual=True)
            if dual is None:krom,krom_cost=krom_decide(n,clauses)
    endpoints_witness = 0 if all0['sat'] else ((1<<n)-1 if all1['sat'] else None)
    attempts=['ENDPOINT_TEST','CANONICAL_PRISM']
    if recognize is None:attempts.append('SOURCE_GROUP_AFFINE')
    if recognize is None and generic is None:
        attempts.append('HORN')
        if horn is None:
            attempts.append('DUAL_HORN')
            if dual is None:
                attempts.append('KROM')
                if krom is None:attempts.append('DPLL_FALLBACK')
    selected=('ENDPOINT_WITNESS' if endpoints_witness is not None else
              'CANONICAL_PRISM' if recognize is not None else
              'SOURCE_GROUP_AFFINE' if generic is not None else
              'HORN' if horn is not None else 'DUAL_HORN' if dual is not None else
              'KROM' if krom is not None else 'DPLL_FALLBACK')
    selected_result=(True if endpoints_witness is not None else
       sum(recognize)%2==0 if recognize is not None else
       affine['sat'] if affine is not None else horn['sat'] if horn is not None else
       dual['sat'] if dual is not None else krom['sat'] if krom is not None else base_sat)
    assert selected_result==base_sat
    # Charged symbolic selected events; not bit-time on the FLMV machine.
    scan=N=encode_bits(n,clauses)
    endpoint_lit_tests=2*sum(len(c) for c in clauses)
    acquisition=(endpoint_lit_tests + (blockstats.get('literal_reads',0)+blockstats.get('block_queries',0) if endpoints_witness is None else 0)
       + (awork.get('literal_reads',0)+awork.get('group_tests',0) if recognize is None else 0)
       + horn_cost.get('source_lit_tests',0)+dual_cost.get('source_lit_tests',0)
       + krom_cost.get('source_lit_tests',0)+krom_cost.get('dfs_visits',0)
       + max(0,len(attempts)-1))
    guest_work=base['selected_work'] if selected=='DPLL_FALLBACK' else 0
    # Source parse, acquisition, child bits or fallback guest work, and witness proof check.
    child_len=(encode_bits(1,[(1,)] if selected_result else [(1,),(-1,)]) if
        selected not in ('DPLL_FALLBACK','ENDPOINT_WITNESS') else 0)
    proof_check=(sum(len(c) for c in clauses) if selected_result and selected not in ('DPLL_FALLBACK','ENDPOINT_WITNESS') else 0)
    measured_controller_work=N+acquisition+guest_work+child_len+proof_check
    if affine and affine['sat']:
        assert all(true_count(c,affine['witness']) for c in clauses)
    if recognize is not None:
        assert recognize==charges
        decision=(sum(recognize)&1)==0
        syndrome={'parity':sum(recognize)&1,'decision':decision,
                  'ordinary_child_cnf':[[1]] if decision else [[1],[-1]],
                  'physical_bits':encode_bits(1,[(1,)] if decision else [(1,),(-1,)])}
        cut=cut_certificate(k,charges,list(range(k)))
        # Rungs first. Otherwise the cut is not exercised early enough.
        order=list(range(2*k+1,3*k+1))+list(range(1,2*k+1))
        plain_sat,_,rung_base=up_dpll(n,clauses,order=order)
        cut_sat,_,rung_cut=up_dpll(n,clauses,order=order,cut=(cut['boundary'],cut['required_parity']))
        assert base_sat==plain_sat==cut_sat==decision
        source_bits=encode_bits(n,clauses)
        assert syndrome['physical_bits']<source_bits**.5
        cut['forbidden_boundary_patterns']= [a for a in range(1<<len(cut['boundary'])) if (a.bit_count()&1)!=cut['required_parity']]
        diag.update({'canonical_recognition':recognize,'syndrome':syndrome,'cut':cut,
                     'rung_order_baseline':rung_base,'rung_order_cut':rung_cut})
    else:
        diag.update({'canonical_recognition':None,'syndrome':None,'cut':None})
    assert gray_full['status']==('SAT' if base_sat else 'EXHAUSTIVE_UNSAT')
    if gray_full['witness'] is not None: assert all(true_count(c,gray_full['witness'])>0 for c in clauses)
    assert base_sat==(actual_models>0) if do_count else True
    if affine is not None:assert base_sat==affine['sat']
    measured_bytes=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
    return {'name':name,'n':n,'m':len(clauses),'physical_source_bits':encode_bits(n,clauses),
            'clauses':[list(c) for c in clauses],
            'source_charges':charges,'k':k,'baseline':base,'baseline_sat':base_sat,
            'canonical_acquisition':blockstats,'affine_acquisition':awork,'affine_decision':affine,
            'controller_selected':selected,'controller_attempts':attempts,
            'controller_failure_count':len(attempts)-1,
            'controller_sat':selected_result,'controller_selected_work':measured_controller_work,
            'controller_work_ledger':{'source_bit_parse':N,'acquisition_and_switches':acquisition,
                'endpoint_literal_tests':endpoint_lit_tests,
                'DPLL_fallback_guest':guest_work,'child_output_bits':child_len,
                'original_witness_check_lits':proof_check,'full_source_materialization_Python':True,
                'candidate_FLVM_work_bound_certified':False},
            'horn_acquisition':horn_cost,'dual_horn_acquisition':dual_cost,'krom_acquisition':krom_cost,
            'horn_decision':horn,'dual_horn_decision':dual,'krom_decision':krom,
            'diagnostics_work_separate':dict(stats),'diagnostics':diagnostic,
            'peak_python_bytes_lab_only':measured_bytes,'wall_seconds_lab_only':round(time.perf_counter()-t0,4),
            'rung_order_baseline':diag.get('rung_order_baseline'),
            'rung_order_cut':diag.get('rung_order_cut'),
            'cut_certificate':diag.get('cut'),
            'terminal_child':diag.get('syndrome')}

def cases():
    for k in (3,4,5,6):
        q=2*k
        for label,charge in [('SAT',[1,1]+[0]*(q-2)),('UNSAT',[1]+[0]*(q-1))]:
            yield f'prism_q{q}_{label}',3*k,make_prism(k,charge),k,charge
    # A signed variable complementation, with source syntax protected in groups but not canonical grammar
    for label,charge in [('SAT',[1,1]+[0]*4),('UNSAT',[1]+[0]*5)]:
        src=make_prism(3,charge);changed=[]
        for c in reversed(src):changed.append(tuple((-l if abs(l)%3==0 else l) for l in c))
        yield f'renamed_prism_q6_{label}',9,changed,None,None
    yield 'W1_UNSAT',15,W1,None,None
    yield 'SWAP6_SAT',15,SWAP6,None,None
    yield 'Horn_SAT',3,[(1,),(-1,2),(-2,-3),(-3,)],None,None
    yield 'Horn_UNSAT',3,[(1,),(-1,2),(-2,-3),(-3,),(3,)],None,None
    yield 'Krom_SAT',2,[(1,2),(-1,-2)],None,None
    yield 'Krom_UNSAT',2,[(1,2),(1,-2),(-1,2),(-1,-2)],None,None

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--only',default='all')
    args=ap.parse_args();data={'run_id':'CUT-ACQUISITION266','seed':0,'model':'indexed original CNF, Python selected-work proxies, not native FLMV TM',
                 'encoding':'self-delimiting unary n,m and each clause width; signed literal (sign+ceil(log2(n+1)) index bits)',
                 'formulas':[]}
    for name,n,cls,k,c in cases():
        if args.only!='all' and args.only not in name:continue
        print('RUN',name,flush=True)
        record=evaluate(name,n,cls,k,c)
        data['formulas'].append(record)
        print(' ->',record['baseline_sat'],record['baseline']['nodes'],'events',record['baseline']['selected_work'],flush=True)
    with open(args.out,'w') as fd:json.dump(data,fd,separators=(',',':'))
    print('RESULT',len(data['formulas']),'formulas',hashlib.sha256(open(args.out,'rb').read()).hexdigest())
if __name__=='__main__':main()