#!/usr/bin/env python3
"""LSPV-3: fully charged guarded-UP certificate reuse on a fixed original CNF.

No oracle is supplied. All mined clauses require a fresh RUP proof against the
unchanged original source.  A complete DPLL fallback decides both labels.
Selected work is a transparent source/word-operation proxy, NOT FLMV time.
"""
from __future__ import annotations
import argparse, collections, hashlib, itertools, json, math, random, pathlib

W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
SWAP6=list(W1);SWAP6[9]=(-5,6,-15);SWAP6[13]=(-3,-6,-15)

def rename(F, seed):
    r=random.Random(seed); vs=sorted({abs(l) for c in F for l in c}); p=vs[:];r.shuffle(p)
    mapping=dict(zip(vs,p)); flips={v:r.randrange(2) for v in vs}
    return [tuple((1 if l>0 else -1)*(-1 if flips[abs(l)] else 1)*mapping[abs(l)] for l in c) for c in F]

def xor4(odd=False):
    edges=list(itertools.combinations(range(4),2)); out=[]
    for v in range(4):
        loc=[i+1 for i,e in enumerate(edges) if v in e]
        b=int(odd and v==0)
        for bits in itertools.product((0,1),repeat=3):
            if sum(bits)%2!=b:
                out.append(tuple(x if bit==0 else -x for x,bit in zip(loc,bits)))
    return out

def random3(seed, n=8, m=24):
    r=random.Random(seed); out=[]
    for _ in range(m):
        xs=r.sample(range(1,n+1),3)
        out.append(tuple(x if r.randrange(2) else -x for x in xs))
    return out

def cases():
    return {'W1_UNSAT':W1,'SWAP6_SAT':SWAP6,
            'W1_RENAMED_UNSAT':rename(W1,122),'SWAP6_RENAMED_SAT':rename(SWAP6,122),
            'XOR4_EVEN_SAT':xor4(False),'XOR4_ODD_UNSAT':xor4(True),
            'HORN_CHAIN_SAT':[(1,),(-1,2),(-2,3),(-3,4)],
            'HORN_CHAIN_UNSAT':[(1,),(-1,2),(-2,3),(-3,)],
            'KROM_SAT':[(1,2),(-1,2),(1,-2)],
            'KROM_UNSAT':[(1,2),(-1,2),(1,-2),(-1,-2)],
            'CHAIN_GUARD_SAT':[(-1,2),(-2,3),(4,5)],
            'RANDOM3_SEED11':random3(11), 'RANDOM3_SEED12':random3(12),
            'RANDOM3_SEED13':random3(13), 'RANDOM3_SEED14':random3(14)}

def nvars(F):return max((abs(l) for c in F for l in c), default=0)

def sat_clause(c,a):return any(a.get(abs(l),0)==int(l>0) for l in c)
def sat_source(F,a):return all(sat_clause(c,a) for c in F)

def count(F,a):return [sum(a.get(abs(l),0)==int(l>0) for l in c) for c in F]

def full_assignment(n, k):return {v:(k>>(v-1))&1 for v in range(1,n+1)}

def encode_bits(F):
    n=nvars(F);w=max(1,math.ceil(math.log2(n+1)))
    return 2*w+sum(3+len(c)*(1+w) for c in F)

def bump(C,key,n=1):
    if C is not None:C[key]+=n

def clause_signed(l):return abs(l),int(l>0)

def unit(F,decisions,extras=(),collect=False,C=None):
    """Deterministic source-wide scans, reason guards built transitively.
    Decisions are a coherent dict var -> bit.  For each source reason j,
    guard is union of guards of the falsifying assigned literals.
    Extras only used in the DPLL stage, never for source-only mining.
    """
    a=dict(decisions)
    G={v:frozenset([(v if b else -v)]) for v,b in a.items()}
    inferred=[]; cause=[]; proofs=[]
    lines=[tuple(c) for c in F]+[tuple(c) for c in extras]
    while True:
        change=False;all_satisfied=True
        for j,c in enumerate(lines):
            bump(C,'clause_visits');bump(C,'source_literal_reads',len(c))
            missing=[]; satisfied=False;used=[]
            for l in c:
                bump(C,'literal_tests')
                v=abs(l)
                if v not in a:missing.append(l)
                elif a[v]==int(l>0):satisfied=True;break
                else:used.append(l)
            if satisfied:continue
            all_satisfied=False
            if not missing:
                gg=frozenset().union(*(G[abs(l)] for l in used))
                return {'status':'conflict','a':a,'guard':sorted(gg,key=lambda x:(abs(x),x)),
                        'reason':j,'inferred':inferred,'proof_reasons':proofs}
            if len(missing)==1:
                lit=missing[0];v=abs(lit)
                gg=frozenset().union(*(G[abs(l)] for l in used))
                a[v]=int(lit>0);G[v]=gg
                bump(C,'propagations')
                inferred.append({'literal':lit,'guard':sorted(gg,key=lambda x:(abs(x),x)),
                                 'source_clause_index':j if j<len(F) else None})
                proofs.append(j)
                change=True
                break
        if not change:
            return {'status':'satisfied' if all_satisfied else 'open',
                    'a':a,'guard':[],'inferred':inferred,'proof_reasons':proofs}

def canon_clause(c):
    c=sorted(set(c),key=lambda x:(abs(x),x))
    if any(-l in c for l in c):return None
    return tuple(c)

def negated_guard(guard,lit=None):
    return canon_clause([-x for x in guard]+([] if lit is None else [lit]))

def rup(F,c,C=None):
    """Original-source RUP, checked without any imported learned clause."""
    bump(C,'rup_attempts')
    if c is None:return False
    forced={}
    for l in c:
        v=abs(l);b=int(l<0)
        if v in forced and forced[v]!=b:return True
        forced[v]=b
    z=unit(F,forced,C=C)
    return z['status']=='conflict'

def select_branch(F, a, C):
    vals=collections.Counter()
    for c in F:
        bump(C,'selector_clause_reads')
        if any(v in a and a[v]==int(l>0) for l in c for v in [abs(l)]):continue
        for l in c:
            bump(C,'selector_literal_tests')
            if abs(l) not in a:vals[abs(l)]+=1
    if not vals:return None
    return min(vals,key=lambda x:(-vals[x],x))

def dpll(F,extra=()):
    C=collections.Counter();n=nvars(F);b=encode_bits(F)
    bump(C,'source_acquisition_bits',b)
    # Simulate physically acquiring and retaining all authenticated input clauses.
    bump(C,'retained_source_descriptor_steps',len(F))
    maximum_depth=0;nodes=0
    def recurse(D):
        nonlocal maximum_depth,nodes
        nodes+=1;maximum_depth=max(maximum_depth,len(D))
        res=unit(F,D,extra,C=C)
        if res['status']=='conflict':
            return False,{'conflict':True,'decisions':sorted(((v,b) for v,b in D.items()))}
        if res['status']=='satisfied' or all(sat_clause(c,res['a']) for c in F):
            model={v:res['a'].get(v,0) for v in range(1,n+1)}
            bump(C,'witness_validation_lits',sum(map(len,F)))
            if not sat_source(F,model):raise AssertionError('bad witness')
            return True,{'witness':''.join(str(model[v]) for v in range(1,n+1))}
        v=select_branch(F,res['a'],C)
        if v is None:raise AssertionError('no branch despite open source')
        lo=dict(D);lo[v]=0
        yes,p0=recurse(lo)
        if yes:return True,{'branch':v,'zero':p0,'one':None}
        hi=dict(D);hi[v]=1
        yes,p1=recurse(hi)
        return yes,{'branch':v,'zero':p0,'one':p1}
    yes,trace=recurse({})
    peak_bits=b+encode_bits(extra)+n*max(1,math.ceil(math.log2(n+2)))+maximum_depth*math.ceil(math.log2(n+2))
    return {'decision':'SAT' if yes else 'UNSAT','nodes':nodes,'max_decisions':maximum_depth,
            'events':dict(C),'selected_operations':sum(C.values()),'peak_model_bits_upper':peak_bits,'proof_tree':trace}

def mine(F, budget=60, max_width=5, max_clauses=40):
    n=nvars(F);C=collections.Counter(); sourcebits=encode_bits(F)
    bump(C,'source_acquisition_bits',sourcebits)
    vs=sorted({abs(l) for c in F for l in c})
    selected=[vs[:min(4,len(vs))]]
    # Deliberately explore disjoint Hamming cylinders and then change the pinned set.
    if len(vs)>=7:selected.extend([vs[2:6],vs[4:8]])
    if len(vs)>=10:selected.append(vs[6:10])
    states=[]
    for subset in selected:
        for i in range(1<<len(subset)):
            g=i^(i>>1)
            D={v:((g>>j)&1) for j,v in enumerate(subset)}
            states.append(D)
    states=states[:budget]
    learned={}; frame=[];hits=0; false_naive=0
    for i,D in enumerate(states):
        cur=unit(F,D,collect=True,C=C)
        candidates=[]
        for ent in cur['inferred']:
            c=negated_guard(ent['guard'],ent['literal'])
            if c is not None and len(c)<=max_width:candidates.append((c,ent))
        if cur['status']=='conflict':
            c=negated_guard(cur['guard'])
            if c is not None and len(c)<=max_width:candidates.append((c,{'literal':None,'guard':cur['guard']}))
        used=[]
        for clause,why in candidates:
            bump(C,'candidate_inspections')
            if clause in learned or tuple(clause) in F:continue
            if not rup(F,clause,C):raise AssertionError('unsound source inference')
            if len(learned)>=max_clauses:continue
            # Charge physical clause bits and an explicit source proof check.
            bump(C,'certificate_storage_bits',len(clause)*(1+math.ceil(math.log2(n+1)))+3)
            learned[clause]={'first_frame':i,'reason_clause':why.get('source_clause_index'),
                             'guard':why['guard']}
            used.append(list(clause))
        if i>0:
            # Nonmonotone reuse is valid if GUARD is still active, not if all
            # the original parent assumptions are present.
            for clause,rec in learned.items():
                guard=rec['guard'];old=states[rec['first_frame']]
                guard_ok=all(D.get(abs(x))==int(x>0) for x in guard)
                old_is_subset=all(D.get(v)==b for v,b in old.items())
                if guard_ok and not old_is_subset:hits+=1
                if (not guard_ok) and clause in learned and not old_is_subset:
                    false_naive+=1
        if i<16:frame.append({'decisions':sorted([[v,b] for v,b in D.items()]),
                             'status':cur['status'],'inferred_count':len(cur['inferred']),
                             'guarded_new_clauses':used})
    clauses=sorted(learned,key=lambda c:(len(c),c))
    # Even unselected clauses have been acquired and proved; charge them.
    return {'clauses':[list(c) for c in clauses], 'provenance':{str(list(c)):learned[c] for c in clauses},
            'mining_frames':frame,'frames_examined':len(states),'cross_backtrack_hits':hits,
            'unguarded_reuse_rejections':false_naive,'events':dict(C),'selected_operations':sum(C.values()),
            'retained_learned_bits':sum(3+len(c)*(1+math.ceil(math.log2(n+1))) for c in clauses)}

def audit_extremes(F):
    n=nvars(F);m=len(F)
    occ=[];modes=[]
    for j,c in enumerate(F,1):
        S={abs(l):int(l>0) for l in c}
        U={v:1-x for v,x in S.items()}
        occ.append({'j':j,'clause':list(c),
                    'S_local':sorted([[v,b] for v,b in S.items()]),
                    'S_inverted_U':sorted([[v,1-b] for v,b in S.items()]),
                    'U_local':sorted([[v,b] for v,b in U.items()]),
                    'U_inverted_S':sorted([[v,1-b] for v,b in U.items()]),
                    'occurrences':[{'variable':abs(l),'signed_literal':l,
                          'S_target':int(l>0),'S_inversion':int(l<0),
                          'U_target':int(l<0),'U_inversion':int(l>0)} for l in c]})
    for j in range(m):
        for k in range(j+1,m):
            row={'source_j':j+1,'source_k':k+1}
            for M in 'SU':
                for V in 'SU':
                    x=dict(occ[j]['S_local' if M=='S' else 'U_local'])
                    y=dict(occ[k]['S_local' if V=='S' else 'U_local'])
                    row[M+V]=all(v not in x or x[v]==b for v,b in y.items())
            modes.append(row)
    endpoints=[]
    for bit in (0,1):
        a={v:bit for v in range(1,n+1)}; vals=count(F,a)
        endpoints.append({'bit':bit,'status':'SAT' if min(vals)>0 else 'UNSAT_ASSIGNMENT',
                          't_by_original_clause':vals,
                          'N_r':{str(k):vals.count(k) for k in range(max(map(len,F),default=0)+1)}})
    flips=[]
    for k in range(min(16,1<<n)):
        g=k^(k>>1)
        a=full_assignment(n,g);v=count(F,a)
        flips.append({'gray_index':k,'assignment_bits':g,
                      'hamming_weight':g.bit_count(),'true_literal_counts':v,
                      'source_clause_sat_count':sum(x>0 for x in v)})
    adaptive=[]
    # This is a heuristic trace only. A local optimum has NO UNSAT authority.
    for start in (0,1):
        a={v:start for v in range(1,n+1)}
        frames=[]
        for step in range(min(n+2,15)):
            ts=count(F,a);viol=ts.count(0)
            frames.append({'step':step,'assignment':[[v,a[v]] for v in range(1,n+1)],
                           'violated_clauses':viol,'source_true_counts':ts})
            if viol==0:break
            best=(viol,None)
            for v in range(1,n+1):
                a[v]^=1
                w=count(F,a).count(0)
                a[v]^=1
                if w<best[0]:best=(w,v)
            if best[1] is None:break
            a[best[1]]^=1
        adaptive.append({'endpoint_start':start,'frames':frames,
                         'status':'SAT_WITNESS' if frames[-1]['violated_clauses']==0 else 'HEURISTIC_STOP_ONLY'})
    return {'clauses_and_occurrences':occ,'pair_matrix':modes,'global_endpoints':endpoints,
            'flip_trail':flips,'adaptive_flip_trails':adaptive}


def brute(F):
    n=nvars(F);count_models=0;witness=None
    for k in range(1<<n):
        a=full_assignment(n,k)
        if sat_source(F,a):
            count_models+=1
            if witness is None:witness=''.join(str(a[i]) for i in range(1,n+1))
    return count_models,witness

def run(selection=None):
    selected=selection or list(cases())
    results={};
    for name in selected:
        F=cases()[name]; mine_data=mine(F)
        baseline=dpll(F)
        improved=dpll(F,[tuple(c) for c in mine_data['clauses']])
        if baseline['decision']!=improved['decision']:raise AssertionError('different labels')
        models,witness=brute(F)
        if (models>0)!=(baseline['decision']=='SAT'):raise AssertionError('exhaustive mismatch')
        results[name]={'original_clauses':[list(c) for c in F], 'n':nvars(F),'m':len(F),
                       'source_encoding_bits':encode_bits(F),'models':models,'witness':witness,
                       'audit':audit_extremes(F),'mining':mine_data,'baseline':baseline,'with_cache':improved,
                       'cache_full_selected_operations':mine_data['selected_operations']+improved['selected_operations'],
                       'cache_live_bits_upper':encode_bits(F)+mine_data['retained_learned_bits']+
                            nvars(F)*max(1,math.ceil(math.log2(nvars(F)+2)))+
                            nvars(F)*math.ceil(math.log2(nvars(F)+2))}
    return results

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--groups',default='all');ap.add_argument('--output',required=True)
    args=ap.parse_args(); keys=list(cases());split={'a':keys[:5],'b':keys[5:10],'c':keys[10:]} ;sel=keys if args.groups=='all' else split[args.groups]
    res=run(sel);pathlib.Path(args.output).write_text(json.dumps({'schema':'arc267-v1','cases':res},indent=1,sort_keys=True)+'\n')
    print(json.dumps({'cases':len(res),'names':list(res),'models':[res[x]['models'] for x in res],
       'total_source_checks':sum(1<<res[x]['n'] for x in res)}))
if __name__=='__main__':main()