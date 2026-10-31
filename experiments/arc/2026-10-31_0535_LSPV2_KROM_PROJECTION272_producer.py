#!/usr/bin/env python3
"""LSPV-2: source-indexed Davis-Putnam projection of private Krom variables.
Run: python krom_projection272.py [output.json]. Requires Python standard library only.
The independent verifier is verify_krom_projection272.py.
"""
import json, itertools, random, sys, time, tracemalloc, hashlib
from collections import Counter

SEED = 2712026

def canon(c):
    s=set(c)
    if any(-z in s for z in s): return None
    return tuple(sorted(s,key=lambda x:(abs(x),x<0)))

def sat(F,a):
    return all(any(a[abs(l)] == (l>0) for l in c) for c in F)

def enum_witness(F,n):
    for bits in itertools.product((False,True),repeat=n):
        a={i+1:bits[i] for i in range(n)}
        if sat(F,a):return a
    return None

def DPLL(F,n,work):
    def rec(a):
        work['nodes']+=1
        while True:
            changed=False; active=[]
            for c in F:
                work['literal_probes']+=len(c)
                if any(abs(l) in a and a[abs(l)]==(l>0) for l in c):continue
                un=[l for l in c if abs(l) not in a]
                if not un:return None
                if len(un)==1:
                    l=un[0];v=abs(l);value=l>0
                    if v in a and a[v]!=value:return None
                    if v not in a:
                        a[v]=value;work['unit_updates']+=1;changed=True
                active.append(un)
            if not changed:break
        if not active:return {i:a.get(i,False) for i in range(1,n+1)}
        # Shortest-clause and stable signed-order policy, all selection charged.
        v=abs(min(min(active,key=len),key=lambda l:(abs(l),l<0)))
        work['selection_tests']+=sum(len(c) for c in active)
        for value in (False,True):
            q=a.copy();q[v]=value
            z=rec(q)
            if z is not None:return z
        return None
    return rec({})

def project(F):
    n=max([abs(l) for c in F for l in c],default=0)
    H=[(i,c) for i,c in enumerate(F) if len(c)>2]
    C=[(i,c) for i,c in enumerate(F) if len(c)<=2]
    B=sorted({abs(l) for _,c in H for l in c})
    P=sorted({abs(l) for _,c in C for l in c}-set(B))
    meter=Counter();meter['scan_literals']=sum(map(len,F));meter['policy_tests']=2
    nodes=[{'kind':'source','id':i,'clause':list(c)} for i,c in enumerate(F)]
    work={canon(c):i for i,c in C}
    work={k:v for k,v in work.items() if k is not None}
    histories=[]
    for p in P:
        pos=[(c,node) for c,node in work.items() if p in c]
        neg=[(c,node) for c,node in work.items() if -p in c]
        meter['clauses_examined']+=len(work)
        nextw={c:node for c,node in work.items() if p not in c and -p not in c}
        histories.append({'pivot':p,'positive':[list(c) for c,_ in pos], 'negative':[list(c) for c,_ in neg]})
        for a,ia in pos:
            for b,ib in neg:
                meter['resolvent_trials']+=1
                raw=[l for l in a if l!=p]+[l for l in b if l!=-p]
                meter['resolution_literal_ops']+=len(a)+len(b)+len(raw)
                r=canon(raw)
                if r is None:meter['tautologies']+=1;continue
                if r not in nextw:
                    idx=len(nodes)
                    nodes.append({'kind':'resolve','id':idx,'clause':list(r),'parents':[ia,ib],'pivot':p})
                    nextw[r]=idx;meter['new_clauses']+=1
                else: meter['deduplicates']+=1
        work=nextw
    remaining=sorted((c,node) for c,node in work.items())
    clist=sorted({tuple(c) for _,c in H}|{tuple(c) for c,_ in remaining})
    remap={v:i+1 for i,v in enumerate(B)}
    output=[tuple(sorted((remap[abs(l)]*(1 if l>0 else -1) for l in c),key=lambda x:(abs(x),x<0))) for c in clist]
    parentmap={tuple(c):i for i,c in H}
    parentmap.update({c:node for c,node in remaining})
    proofs=[parentmap[c] for c in clist]
    proof={'source':F,'boundary':B,'private':P,'nodes':nodes,'histories':histories,
           'source_final_clauses':[list(c) for c in clist],'proof_ids':proofs}
    return output,proof,dict(meter)

def reconstruct(source,proof,bassign):
    a={old:bassign[i+1] for i,old in enumerate(proof['boundary'])}
    for row in reversed(proof['histories']):
        p=row['pivot'];needs=[]
        for side in ('positive','negative'):
            for c in row[side]:
                rest=[l for l in c if abs(l)!=p]
                if not any(abs(l) in a and a[abs(l)]==(l>0) for l in rest):
                    needs.append(side=='positive')
        if needs and len(set(needs))>1:raise ValueError('projection witness contradictory')
        a[p]=needs[0] if needs else False
    for v in range(1,max([abs(l) for c in source for l in c],default=0)+1):
        a.setdefault(v,False)
    if not sat(source,a):raise ValueError('witness reconstruction failed')
    return a

def serializer(G,n):
    header=f'p cnf {n} {len(G)}\n'
    clauses=[' '.join(map(str,c))+(' ' if c else '')+'0\n' for c in G]
    offsets=[len(header)]
    for c in clauses:offsets.append(offsets[-1]+len(c))
    from bisect import bisect_right
    def indexed(i):
        if not 0<=i<offsets[-1]:return None
        if i<len(header):return header[i]
        k=bisect_right(offsets,i)-1
        return clauses[k][i-offsets[k]]
    return header,clauses,offsets,indexed

def endpoints(F,n):
    trace={}
    for tag,a in [('zeros',{i:False for i in range(1,n+1)}),('ones',{i:True for i in range(1,n+1)})]:
        trace[tag]=[sum(a[abs(l)]==(l>0) for l in c) for c in F]
    mask={i:False for i in range(1,n+1)}
    trail=[]
    for v in range(1,min(n,5)+1):
        old=[sum(mask[abs(l)]==(l>0) for l in c) for c in F]
        mask[v]=not mask[v]
        new=[sum(mask[abs(l)]==(l>0) for l in c) for c in F]
        trail.append({'flip':v,'before':old,'after':new})
    # Preserve all indexed original S and U targets and their inversions.
    records=[]
    for j,c in enumerate(F):
        for l in c:
            records.append({'clause':j,'variable':abs(l),'sign':1 if l>0 else -1,
                            'S':l>0,'invert_S':l<0,'U':l<0,'invert_U':l>0})
    modes=[]
    # Full pair matrix is a diagnostic control, limited to small sources.
    if len(F)<=100:
        for j,c in enumerate(F):
            for k,d in enumerate(F[:j]):
                pair={}
                for e1,e2 in ('SS','SU','US','UU'):
                    wants={}
                    good=True
                    for l,e in [(x,e1) for x in c]+[(x,e2) for x in d]:
                        v=abs(l);want=(l>0) if e=='S' else (l<0)
                        if v in wants and wants[v]!=want:good=False
                        wants[v]=want
                    pair[e1+e2]=good
                modes.append({'j':j,'k':k,'modes':pair})
    return {'endpoint':trace,'flips':trail,'occurrences':records,'pairs':modes}

def source_resolution_refutation(proof,projected=True,max_nodes=5000):
    """Ordinary source-indexed DP refutation; no semantic oracle or omitted parents."""
    if projected:
        work={tuple(c):idx for c,idx in zip(proof['source_final_clauses'],proof['proof_ids'])}
        pivots=proof['boundary']
        nodes=proof['nodes']
    else:
        nodes=proof['nodes']
        work={canon(c):i for i,c in enumerate(proof['source'])}
        pivots=sorted({abs(l) for c in proof['source'] for l in c})
    events=Counter()
    if () in work:return work[()],dict(events)
    for p in pivots:
        pos=[(c,i) for c,i in work.items() if p in c]
        neg=[(c,i) for c,i in work.items() if -p in c]
        new={c:i for c,i in work.items() if p not in c and -p not in c}
        events['refutation_scans']+=len(work)
        for a,ia in pos:
            for b,ib in neg:
                events['refutation_trials']+=1
                events['refutation_literal_ops']+=len(a)+len(b)
                r=canon([l for l in a if l!=p]+[l for l in b if l!=-p])
                if r is None:continue
                if r not in new:
                    if len(nodes)>=max_nodes:return None,dict(events)
                    idx=len(nodes)
                    nodes.append({'kind':'resolve','id':idx,'clause':list(r),
                                  'parents':[ia,ib],'pivot':p})
                    new[r]=idx;events['refutation_derived']+=1
        work=new
        if () in work:return work[()],dict(events)
    return None,dict(events)

def build_cases():
    cases=[]
    for k in (2,5,10,20,1000):
        for yes in (True,False):
            F=[[1,2,3]]
            for i in range(k):
                p=4+i;F.extend([[-1,p],[-p,2]])
            F.extend([[1],[2 if yes else -2]])
            cases.append((f'repeated_wire_{k}_{"SAT" if yes else "UNSAT"}',F))
    for k in (2,3,5,8):
        for yes in (True,False):
            p=2*k+3;t=2*k+1;s=2*k+2
            F=[]
            for v in range(1,2*k+1):F.append([v,t,s])
            F.append([t])
            for i in range(1,k+1):F.append([-i,p])
            for j in range(k+1,2*k+1):F.append([-p,j])
            F.extend([[1],[k+1 if yes else -(k+1)]])
            cases.append((f'star_{k}_{"SAT" if yes else "UNSAT"}',F))
    cases.extend([
       ('pure_horn', [[-1,2],[-2,3],[1]]),
       ('pure_2sat_unsat', [[1],[-1,2],[-2]]),
       ('mixed_3sat', [[1,2,3],[-1,-2,-3],[1,-2,3],[-1,2,-3]]),
       ('xor3_unsat', [[1,2,3],[-1,-2,3],[-1,2,-3],[1,-2,-3],[1],[-2],[-3]]),
       ('highwidth_easy', [[1,2,3,4,5,6,7,8],[1]]),
       ('empty_clause', [[]]),('empty_formula', [])
    ])
    rng=random.Random(SEED)
    for i in range(20):
        n=5+(i%3)
        F=[]
        for _ in range(7+(i%5)):
            vars=rng.sample(range(1,n+1),rng.choice([1,2,2,3]))
            F.append([v if rng.getrandbits(1) else -v for v in vars])
        cases.append((f'random_{i}',F))
    # The exact 20-clause matched signed-support controls from the project's prior W1/S15 record.
    W1=[[-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],
        [5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],
        [-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],
        [6,-7,11],[2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]]
    S15=[[-1,-3,14],[2,8,-9],[-10,13,14],[3,-7,-13],[-4,9,-11],
         [-5,-8,-14],[4,-8,11],[1,7,-13],[1,-7,10],[-5,-6,15],
         [-2,6,-12],[4,9,-10],[-2,5,-12],[3,6,-15],
         [-6,7,11],[2,-9,-11],[-4,8,10],[-3,12,15],[5,12,-15],[-1,13,-14]]
    cases.extend([('W1_strict22_UNSAT',W1),('S15_matched_support_SAT',S15)])
    # Signing/renaming invariance controls, deliberately reverse some polarities.
    for j,(name,F) in enumerate(cases[:6]):
        n=max((abs(l) for c in F for l in c),default=0)
        perm=list(range(1,n+1));rng.shuffle(perm)
        flips={v:bool(rng.getrandbits(1)) for v in range(1,n+1)}
        copied=[[(-1 if flips[abs(l)] else 1)*(1 if l>0 else -1)*perm[abs(l)-1] for l in c] for c in F]
        cases.append((f'renamed_{name}',copied))
    return cases

def run():
    results=[];counts=Counter();start=time.monotonic();tracemalloc.start()
    for name,F in build_cases():
        n=max([abs(l) for c in F for l in c],default=0)
        F=[list(canon(c)) if canon(c) is not None else [] for c in F]
        bwork=Counter();baseline=DPLL(F,n,bwork)
        G,proof,ledger=project(F)
        cn=len(proof['boundary'])
        header,lines,offs,idx=serializer(G,cn)
        serialized=header+''.join(lines)
        assert all(idx(i)==serialized[i] for i in range(len(serialized)))
        cwork=Counter();childw=DPLL(G,cn,cwork)
        if childw is not None:
            srcw=reconstruct(F,proof,childw)
        else:srcw=None
        if (srcw is not None)!=(baseline is not None):raise AssertionError(name+' SAT status mismatch')
        source_bytes=len(serializer(F,n)[0]+''.join(serializer(F,n)[1]))
        child_bytes=len(serialized)
        selected=(len(proof['private'])>0 and child_bytes<source_bytes)
        if selected:
            route='COMMIT_PROJECTED_CHILD';rwork=cwork;route_witness=srcw
        else:
            route='REJECT_SIZE_OR_NO_PRIVATE__FALLBACK'
            rwork=Counter();route_witness=DPLL(F,n,rwork)
            if (route_witness is not None)!=(baseline is not None):raise AssertionError('fallback mismatch')
        if baseline is None:
            root,rledger=source_resolution_refutation(proof,projected=selected)
            proof['refutation_root']=root
            proof['refutation_stage']='projected_source' if selected else 'original_source'
            proof['refutation_meter']=rledger
            counts['UNSAT_refutation_roots' if root is not None else 'UNSAT_refutation_pending']+=1
        else:
            proof['refutation_root']=None;proof['refutation_meter']={}
        checks=sum(map(len,F)) if route_witness is not None else 0
        selected_projector_events=sum(ledger.values())+sum(proof['refutation_meter'].values())
        provenance_check_events=sum(2+len(node['clause'])+2*len(node.get('parents',[])) for node in proof['nodes'])
        charge=source_bytes+selected_projector_events+child_bytes+sum(rwork.values())+checks+provenance_check_events+2
        basecharge=source_bytes+sum(bwork.values())
        counts['controller_selected_events']+=charge
        counts['baseline_selected_events']+=basecharge
        counts['committed' if selected else 'fallback']+=1
        counts['controller_route_nodes']+=rwork['nodes']
        # Check all boundary profiles only while small; independently checked later.
        if n<=11:
            for tup in itertools.product((False,True),repeat=cn):
                a={i+1:tup[i] for i in range(cn)}
                possible=False
                for vals in itertools.product((False,True),repeat=n-cn):
                    assign={i+1:False for i in range(n)}
                    for i,v in enumerate(proof['boundary']):assign[v]=tup[i]
                    for i,v in enumerate(proof['private']):assign[v]=vals[i]
                    if sat(F,assign):possible=True;break
                if possible!=sat(G,a):raise AssertionError('cofactor mismatch '+name)
                counts['profile_exact_checks']+=1
        counts['cases']+=1;counts['SAT' if baseline is not None else 'UNSAT']+=1
        counts['baseline_nodes']+=bwork['nodes'];counts['child_nodes']+=cwork['nodes']
        counts['projection_resolvents']+=ledger.get('new_clauses',0)
        audit=endpoints(F,n)
        counts['pair_extremes']+=4*len(audit['pairs'])
        outcome={ 'case':name,'n':n,'label':'SAT' if baseline is not None else 'UNSAT', 'source_bits':source_bytes*8,
            'child_bits':child_bytes*8,'baseline':dict(bwork),'projector':ledger,'guest':dict(cwork),
            'route':route,'route_work':dict(rwork),'provenance_check_events':provenance_check_events,'baseline_selected_events':basecharge,'controller_selected_events':charge,
            'source_witness':srcw,'child_witness':childw,'proof':proof,'child':G,
            'child_serialization':serialized,'audit':audit}
        results.append(outcome)
    peak=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
    document={'run':'LSPV2_KROM_RESOLUTION_PROJECTION272','seed':SEED,'status':'COMPUTATIONAL','models':'Python operation proxies, not FLMV TM',
              'run_seconds':round(time.monotonic()-start,3),'python_peak_bytes':peak,'totals':dict(counts),'cases':results}
    target=sys.argv[1] if len(sys.argv)>1 else '/mnt/data/lspv2_272/raw272.json'
    with open(target,'w') as f:json.dump(document,f,sort_keys=True,separators=(',',':'))
    print(json.dumps({'raw':target,'sha256':hashlib.sha256(open(target,'rb').read()).hexdigest(),'counts':dict(counts),'peak_bytes':peak,'seconds':document['run_seconds']},sort_keys=True))
if __name__=='__main__':run()