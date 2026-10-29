#!/usr/bin/env python3
"""Connected exact-(2+,2-) strict 3CNF cyclic port-splice controls.
Pure Python 3.11; exact exhaustive 15-variable profiles, no SAT/oracle call.
Expected data generated from a fixed W1 source and a single balanced two-sign flip.
All supported formulas are explicitly recognized before making any decision.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, pathlib, time, random

SOURCE_W1 = (
    (-1,3,-14), (2,-8,9), (10,-13,14), (3,7,-13), (-4,-9,-11),
    (5,8,-14), (4,-8,-11), (1,7,13), (1,-7,10), (-5,-6,-15),
    (-2,-6,12), (-4,9,-10), (-2,5,-12), (-3,6,-15),
    (6,-7,11), (2,-9,11), (4,8,-10), (-3,12,15),
    (-5,-12,15), (-1,13,14)
)
C_STAR = SOURCE_W1[0]
PORT = -1


def signed_mutation():
    """Flip the x1 sign in clauses 7 and 19 (0-based) and leave C* untouched."""
    c = [list(z) for z in SOURCE_W1]
    for i in (7,19):
        p = next(j for j,v in enumerate(c[i]) if abs(v)==1)
        c[i][p] = -c[i][p]
    return tuple(map(tuple,c))

SOURCE_M = signed_mutation()
assert SOURCE_M[0] == C_STAR


def val(lit: int, mask: int) -> bool:
    return bool((mask >> (abs(lit)-1)) & 1) == (lit > 0)


def sat_clause(c, mask):
    return any(val(l,mask) for l in c)


def profile_exhaustive(clauses):
    """R(p_i,p_next), including all 2^15 source assignments; p_i is truth of -x1."""
    assert len(clauses)==20 and clauses[0]==C_STAR
    U=clauses[1:]
    counts={(a,b):0 for a in (0,1) for b in (0,1)}
    exemplars={}
    unpinned={}
    residual_models=0
    for mask in range(1<<15):
        if not all(sat_clause(c,mask) for c in U):continue
        residual_models+=1
        a=int(val(PORT,mask))
        unpinned.setdefault(a,mask)
        h=sat_clause(C_STAR[1:],mask)
        for b in (0,1):
            if b or h:
                counts[a,b]+=1
                exemplars.setdefault((a,b),mask)
    return counts,exemplars,unpinned,residual_models


def decorate(c,block):
    return tuple((1 if l>0 else -1)*(abs(l)+15*block) for l in c)


def build_cycle(k, kinds):
    assert k>=2 and len(kinds)==k and set(kinds)<={'W','M'}
    blocks=[]
    for i,typ in enumerate(kinds):
        source=SOURCE_W1 if typ=='W' else SOURCE_M
        blocks.append([decorate(c,i) for c in source])
    # One same-signed literal occurrence from every block moves to the previous
    # block. No fresh variables or clauses are introduced.
    for i in range(k):
        incoming=(i+1)%k
        c=list(blocks[i][0])
        assert c[0] == -(15*i+1)
        c[0]=-(15*incoming+1)
        blocks[i][0]=tuple(c)
    out=[]
    for block in blocks:out.extend(block)
    return out


def connected_and_quota(clauses,k):
    n=15*k
    assert len(clauses)==20*k
    signs=collections.Counter()
    seen=set()
    adj=[set() for _ in range(n+1)]
    for c in clauses:
        assert len(c)==3 and len({abs(l) for l in c})==3
        assert all(1<=abs(l)<=n for l in c)
        tup=tuple(sorted(c,key=lambda z:(abs(z),z)))
        assert tup not in seen
        seen.add(tup)
        for l in c:signs[l]+=1
        vs={abs(l) for l in c}
        for v in vs:adj[v]|=vs-{v}
    assert all(signs[v]==2 and signs[-v]==2 for v in range(1,n+1))
    reached={1};front=[1]
    while front:
        for u in adj[front.pop()]-reached:
            reached.add(u);front.append(u)
    assert len(reached)==n
    return {'n':n,'m':len(clauses),'connected':True,'exact22':True,
            'unique_proper_clauses':True}


def fill_assignment(mask,block,out):
    for j in range(15):out[15*block+j+1]=int(bool((mask>>j)&1))


def original_checked(clauses,assignment,skip=None):
    for idx,c in enumerate(clauses):
        if idx==skip:continue
        if not any(assignment[abs(l)]==int(l>0) for l in c):return False
    return True


def independent_csp_decide(kinds,profiles):
    """Same deterministic algorithm on both labels, no supplied answer bit."""
    k=len(kinds)
    states=[]
    # Enumerate both values of first port and propagate exact support sets.
    for initial in (0,1):
        reachable={initial}
        sizes=[]
        for typ in kinds:
            reachable={b for a in reachable for b in (0,1) if profiles[typ].get((a,b),0)>0}
            sizes.append(len(reachable))
        states.append({'start':initial,'frontier_sizes':sizes,'accept':initial in reachable})
    return any(t['accept'] for t in states),states


def dimacs(clauses,k):
    return 'p cnf %d %d\n'%(15*k,len(clauses))+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)


def parse_dimacs(s):
    lines=[l.strip() for l in s.splitlines() if l.strip() and not l.startswith('c')]
    h=lines.pop(0).split()
    assert len(h)==4 and h[:2]==['p','cnf']
    n=int(h[2]); m=int(h[3]); cl=[]
    for line in lines:
        ints=list(map(int,line.split()))
        assert ints[-1]==0 and len(ints)==4
        cl.append(tuple(ints[:-1]))
    assert len(cl)==m and all(0<abs(z)<=n for c in cl for z in c)
    return n,cl


def source_auth(clauses,k,kinds):
    """Verify every ordinary source clause, type, sign, slot, and quota."""
    return clauses==build_cycle(k,kinds) and connected_and_quota(clauses,k)


def certify_ring(k,kinds,profiles,proof_models,unpinned):
    C=build_cycle(k,kinds)
    n,C2=parse_dimacs(dimacs(C,k))
    assert n==15*k and C2==C
    source_auth(C,k,kinds)
    status,states=independent_csp_decide(kinds,profiles)
    if kinds.count('W')==0:
        assert status
        # A model of each local pair (0,0) glues into a source model.
        A={}
        for i,t in enumerate(kinds):fill_assignment(proof_models[t][0,0],i,A)
        assert original_checked(C,A)
    elif kinds.count('W')==1:
        assert not status
        # Cross-clause deletion should restore SAT for every cyclic bridge.
        for cut in range(k):
            ports=[0]*k
            if cut>0:
                for i in range(1,cut+1):ports[i]=1
            A={}
            for i,t in enumerate(kinds):
                a=ports[i]; b=ports[(i+1)%k]
                mask=unpinned[t][a] if i==cut else proof_models[t][a,b]
                fill_assignment(mask,i,A)
            assert original_checked(C,A,skip=20*cut)
            assert not original_checked(C,A)
    return {'k':k,'type_counts':dict(collections.Counter(kinds)),
            'decision':'SAT' if status else 'UNSAT',
            'clauses':len(C),'encoded_ascii_bytes':len(dimacs(C,k).encode()),
            'frontier_max':max(sz for x in states for sz in x['frontier_sizes']),
            'local_port_table_entries':sum(int(v>0) for typ in kinds for v in profiles[typ].values()),
            'source_sha256':hashlib.sha256(dimacs(C,k).encode()).hexdigest(),
            'all_bridge_deletions_SAT':k if kinds.count('W')==1 else None}



def canon(c):
    return tuple(sorted(set(c),key=lambda z:(abs(z),z)))


def dp_resolution_template(source):
    """Explicit two-parent resolution proof of local projected interface clauses.

    Inputs have local source ids 1..20; variable 16 is the incoming port
    in the moved first clause. Charge all generated clauses and failed pairs.
    """
    original=[canon((-16,3,-14))]+[canon(c) for c in source[1:]]
    seen={c:i+1 for i,c in enumerate(original)}
    active=original[:]; steps=[]; pivots=[]; candidates=0; max_live=len(active)
    for _ in range(14):
        choices=[]
        for v in range(2,16):
            if v in pivots: continue
            pos=[c for c in active if v in c]
            neg=[c for c in active if -v in c]
            choices.append((len(pos)*len(neg),len(pos)+len(neg),v,pos,neg))
        _,_,v,pos,neg=min(choices,key=lambda t:t[:3])
        pivots.append(v)
        new=[c for c in active if v not in c and -v not in c]
        for a in pos:
            for b in neg:
                candidates+=1
                resolvent=canon((set(a)-{v})|(set(b)-{-v}))
                if any(-z in resolvent for z in resolvent):
                    continue
                if resolvent not in seen:
                    ident=21+len(steps)
                    steps.append({'id':ident,'parents':[seen[a],seen[b]],'pivot':v,
                                  'clause':list(resolvent)})
                    seen[resolvent]=ident
                new.append(resolvent)
        active=[]
        for clause in sorted(set(new),key=lambda c:(len(c),c)):
            if not any(set(a).issubset(clause) for a in active):
                active.append(clause)
        max_live=max(max_live,len(active))
    assert all(abs(z) in (1,16) for clause in active for z in clause)
    return {'initial':original, 'steps':steps,'final':[list(c) for c in active],
            'final_ids':[seen[c] for c in active], 'pivot_order':pivots,
            'attempted_pairs':candidates,'max_live':max_live}


def translate(template_clause, i, k):
    r=[]
    for z in template_clause:
        target=((i+1)%k)*15+1 if abs(z)==16 else i*15+abs(z)
        r.append(target if z>0 else -target)
    return canon(r)


def independent_resolution_checker(source, proof):
    """Separate source-ID checker. Refuses missing/wrong-parent derivations."""
    db={i+1:tuple(c) for i,c in enumerate(source)}
    assert len(db)==len(source)
    for index,row in enumerate(proof,1+len(source)):
        assert row['id']==index
        assert row['parents'][0] in db and row['parents'][1] in db
        a,b=(db[p] for p in row['parents'])
        v=row['pivot']
        assert v>0 and v in a and -v in b
        new=set(a)-{v}
        new.update(set(b)-{-v})
        assert not any(-z in new for z in new)
        cl=tuple(sorted(new,key=lambda z:(abs(z),z)))
        assert tuple(row['clause'])==cl
        db[row['id']]=cl
    assert tuple(proof[-1]['clause'])==(), 'proof must end in empty clause'
    return {'original_clause_count':len(source),'derived_clauses':len(proof),
            'final_empty_verified':True,'largest_resolvent_width':max(len(r['clause']) for r in proof)}


def construct_resolution_proof(k,Wtmpl,Mtmpl):
    assert k>=2
    kinds=['W']+['M']*(k-1)
    source=build_cycle(k,kinds)
    total=len(source)
    proof=[]; local_ids={}; concluding={}
    for i,t in enumerate(kinds):
        x=Wtmpl if t=='W' else Mtmpl
        # Source ids 1..20 in each local template map to the exact physical
        # original clause id, with no repairs or semantic clauses inserted.
        local={j:i*20+j for j in range(1,21)}
        for step in x['steps']:
            g={'id':total+len(proof)+1,'parents':[local[p] for p in step['parents']],
               'pivot':i*15+step['pivot'],'clause':list(translate(step['clause'],i,k))}
            proof.append(g);local[step['id']]=g['id']
        final={tuple(c):local[id_] for c,id_ in zip(x['final'],x['final_ids'])}
        if i==0:
            assert (1,) in final and (-1,-16) in final
            # Resolve W's (x1) with (-x1 or -next_x1), obtaining unit -next_x1.
            p=total+len(proof)+1
            proof.append({'id':p,'parents':[final[(1,)],final[(-1,-16)]],
                          'pivot':1,'clause':[-16]})
            concluding['positive_root']=final[(1,)]; concluding['negative_next']=p
        else:
            assert (1,-16) in final
            concluding[i]=final[(1,-16)]
    tail=concluding['negative_next']
    for i in range(1,k):
        prev=tail
        tail=total+len(proof)+1
        proof.append({'id':tail,'parents':[concluding[i],prev],
                      'pivot':i*15+1,
                      'clause':[-((((i+1)%k)*15)+1)]})
    proof.append({'id':total+len(proof)+1,
                  'parents':[concluding['positive_root'],tail],
                  'pivot':1,'clause':[]})
    info=independent_resolution_checker(source,proof)
    # Corrupt a parent clause and ensure the independent verifier rejects.
    corrupted=[dict(x) for x in proof]
    corrupted[-1]=dict(corrupted[-1],pivot=2)
    rejected=False
    try:independent_resolution_checker(source,corrupted)
    except AssertionError:rejected=True
    assert rejected
    info.update({'k':k,'resolvent_pairs_checked':len(proof),
                 'proof_corruption_rejected':True,
                 'first_three_steps':proof[:3],
                 'last_three_steps':proof[-3:]})
    return info,proof


def permuted_order_controls(k,UNSAT,proof,models,seed):
    """Hostile identifier renaming and exact clause-order permutation tests."""
    kinds=['W']+['M']*(k-1) if UNSAT else ['M']*k
    source=build_cycle(k,kinds)
    rng=random.Random(seed)
    n=15*k
    new_names=list(range(1,n+1));rng.shuffle(new_names)
    names={i+1:new_names[i] for i in range(n)}
    index=list(range(len(source)));rng.shuffle(index)
    shuffled=[tuple((1 if l>0 else -1)*names[abs(l)] for l in source[j]) for j in index]
    connected_and_quota(shuffled,k)
    n2,clauses=parse_dimacs(dimacs(shuffled,k))
    assert n2==n and clauses==shuffled
    if not UNSAT:
        A={}
        for i in range(k):fill_assignment(models['M'][0,0],i,A)
        renamed={names[v]:b for v,b in A.items()}
        assert original_checked(shuffled,renamed)
        return {'k':k,'UNSAT':False,'permutation_seed':seed,'witness_checked':True}
    assert proof is not None
    old_to_new_src={j+1:index.index(j)+1 for j in range(len(source))}
    def tr(l):return names[abs(l)] if l>0 else -names[abs(l)]
    converted=[]
    for step in proof:
        converted.append({'id':step['id'],
                          'parents':[old_to_new_src.get(p,p) for p in step['parents']],
                          'pivot':names[step['pivot']],
                          'clause':list(sorted((tr(z) for z in step['clause']),key=lambda z:(abs(z),z)))})
    validation=independent_resolution_checker(shuffled,converted)
    return {'k':k,'UNSAT':True,'permutation_seed':seed,
            'resolution_steps_checked':validation['derived_clauses']}

def main():
    t0=time.monotonic()
    W,EW,PW,nW=profile_exhaustive(SOURCE_W1)
    M,EM,PM,nM=profile_exhaustive(SOURCE_M)
    assert W=={(0,0):0,(0,1):140,(1,0):0,(1,1):0},W
    assert M=={(0,0):84,(0,1):140,(1,0):0,(1,1):84},M
    assert nW==140 and nM==224
    assert len(EW)==1 and set(EM)=={(0,0),(0,1),(1,1)}
    profiles={'W':W,'M':M};exemplars={'W':EW,'M':EM};unpinned={'W':PW,'M':PM}
    per=[]
    for k in (2,3,4,8,16,32,64):
        per.append(certify_ring(k,['M']*k,profiles,exemplars,unpinned))
        per.append(certify_ring(k,['W']+['M']*(k-1),profiles,exemplars,unpinned))
    WT=dp_resolution_template(SOURCE_W1)
    MT=dp_resolution_template(SOURCE_M)
    assert WT['final']==[[1],[-1,-16]],WT['final']
    assert MT['final']==[[1,-16]],MT['final']
    proof_cases=[]
    permutation_checks=[]
    for k in (2,3,4,8,16,32,64):
        info,certificate=construct_resolution_proof(k,WT,MT)
        proof_cases.append(info)
        if k in (2,3,4,8):
            for repetition in range(2):
                permutation_checks.append(permuted_order_controls(k,False,None,exemplars,
                                                                 230+100*k+repetition))
                permutation_checks.append(permuted_order_controls(k,True,certificate,exemplars,
                                                                 230+100*k+repetition+10000))
        if k==2:
            p=pathlib.Path(__file__).with_name('2026-10-29_1225_LSPV-2_MIXED_PORT_CYCLE230_resolution_k2.json')
            p.write_text(json.dumps({'source':build_cycle(k,['W','M']),'derived':certificate},sort_keys=True,indent=2)+'\n')
    # Unlike all-W cyclic splice, one-W chain cannot be rejected by a proper
    # subset of its inter-module bridge constraints.
    # Test that the UNSAT ring is *not* UNSAT if ANY cross-edge clause is removed.
    out={'status':'COMPUTATIONAL certification of PROVED/EXACT restricted theorem',
         'source':'W1 from project SOURCE_RUP_CHAIN164/CONNECTED_SPLICE_LOCAL_CORE133',
         'mutation':'reverse x1 sign in 0-based clause 7 and clause 19',
         'port_clause':list(C_STAR),'rotated_literal':PORT,
         'W_residual_models':nW,'M_residual_models':nM,
         'W_profile':{f'{x},{y}':W[x,y] for x in (0,1) for y in (0,1)},
         'M_profile':{f'{x},{y}':M[x,y] for x in (0,1) for y in (0,1)},
         'exemplar_masks':{'W':{str(k):v for k,v in EW.items()},'M':{str(k):v for k,v in EM.items()}},
         'cases':per,
         'total_15_variable_assignment_evaluations':2*(1<<15),
         'total_bridge_deletion_witness_checks':sum(v['all_bridge_deletions_SAT'] or 0 for v in per),
         'resolution_template_info': {'W':{z:WT[z] for z in ('pivot_order','attempted_pairs','max_live','final')}, 'M':{z:MT[z] for z in ('pivot_order','attempted_pairs','max_live','final')}},
         'resolution_proof_cases':proof_cases,
         'renaming_and_clause_order_controls':permutation_checks,
         'elapsed_s':round(time.monotonic()-t0,4)}
    raw=json.dumps(out,sort_keys=True,indent=2)+'\n'
    p=pathlib.Path(__file__).with_name('2026-10-29_1225_LSPV-2_MIXED_PORT_CYCLE230_raw.json')
    p.write_text(raw)
    print(json.dumps({'profiles':{'W':out['W_profile'],'M':out['M_profile']},
                      'number_cases':len(per),
                      'all_deletion_witness_checks':out['total_bridge_deletion_witness_checks'],
                      'max_k':max(c['k'] for c in per),
                      'elapsed_s':out['elapsed_s'],
                      'source_authenticated_resolution_cases':len(proof_cases),
                      'renaming_and_order_controls':len(permutation_checks),
                      'raw_sha256':hashlib.sha256(raw.encode()).hexdigest()},indent=2))

if __name__=='__main__':main()