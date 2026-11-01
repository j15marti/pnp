#!/usr/bin/env python3
"""LSPV-2 315: exact source-labeled decision-only Boolean bucket elimination.
Plain Python implementation.  No external solver or oracle.  This is a restricted
width-capped policy, returning UNRESOLVED on cap failure; it is not an all-input
polynomial SAT algorithm.  Certification by independent verifier recommended.
"""
from collections import Counter
from itertools import product
import json

F9_P=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
F9_N=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
F9=tuple(F9_P+[tuple(-x for x in c) for c in F9_N])
F15P=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
F15N=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=tuple(F15P)+tuple(tuple(-x for x in c) for c in F15N)
Y6=tuple([(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)])

def gcycle(t):
    o=[]
    for j in range(t):
        for q,c in enumerate(F9_P):
            o.append(tuple(9*j+x if (q,x)!=(0,5) else 9*((j+1)%t)+5 for x in c))
        o += [tuple(-(9*j+x) for x in c) for c in F9_N]
    return tuple(o)

def pins_of(block,k):
    p={}
    for j,a in enumerate(block):
        off=9*j
        for x,v in a.items():p[off+x]=v
    return p

def valid(F, n):
    if n<3 or n%3 or len(F)*3 != 4*n:return False
    pos=Counter();neg=Counter();seen=set()
    for c in F:
        if len(c)!=3 or len(set(map(abs,c)))!=3 or any(abs(x)<1 or abs(x)>n for x in c):return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key)
        (pos if c[0]>0 else neg).update(map(abs,c))
    return all(pos[i]==neg[i]==2 for i in range(1,n+1))

def clauses_satisfied(F,a):
    return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)

def factor_val(f, vals, charges):
    scope,mask,_=f; code=0
    for j,x in enumerate(scope):
        charges['table_address']+=1
        code|=(vals[x]&1)<<j
    charges['table_reads']+=1
    return (mask>>code)&1

def exact_factor(F,pins,charges):
    result=[]
    for i,c in enumerate(F):
        charges['clause_scans']+=1
        true_pin=False; free=[];signs=[]
        for lit in c:
            charges['literal_reads']+=1
            v=abs(lit)
            if v in pins:
                charges['pin_reads']+=1
                if pins[v]==int(lit>0):true_pin=True
            else:
                free.append(v);signs.append(int(lit>0))
        if true_pin:continue
        scope=tuple(sorted(free))
        mask=0
        for row in range(1<<len(scope)):
            charges['initial_table_cells']+=1
            if any(((row>>scope.index(v))&1)==sgn for v,sgn in zip(free,signs)):
                mask|=1<<row
        result.append((scope,mask,('source',i)))
    return result

def _best_elim(factors, remaining, charges):
    best=None
    for x in remaining:
        neighbors=set()
        for scope,mask,_ in factors:
            charges['selector_factor_tests']+=1
            if x in scope:neighbors.update(scope)
        width=len(neighbors)
        key=(width,x)
        if best is None or key<best[:2]:best=(width,x,tuple(sorted(neighbors)))
    return best

def bucket_decide(F,n,pins=None,width_cap=10,save_trace=True,recover_witness=True):
    pins=dict(pins or {})
    charges=Counter()
    charges['grammar_clause_reads']=len(F)
    charges['grammar_literal_reads']=3*len(F)
    if not valid(F,n):return {'status':'MALFORMED','charged':dict(charges),'trace':[]}
    if any(not isinstance(k,int) or k<1 or k>n or v not in (0,1) for k,v in pins.items()):
        return {'status':'MALFORMED_PIN','charged':dict(charges),'trace':[]}
    factors=exact_factor(F,pins,charges)
    remaining=set(range(1,n+1))-set(pins)
    trace=[];maxwidth=0;peak_bits=0; elimination_count=0
    while remaining:
        width,x,scope=_best_elim(factors,remaining,charges)
        charges['policies_considered']+=len(remaining)
        maxwidth=max(maxwidth,width)
        if width>width_cap:
            charges['failed_width_cap']+=1
            return {'status':'UNRESOLVED','width':width,'eliminated':elimination_count,
                    'charged':dict(charges),'peak_factor_bits':peak_bits,
                    'remaining':len(remaining),'trace':trace if save_trace else []}
        bucket=[f for f in factors if x in f[0]]
        factors=[f for f in factors if x not in f[0]]
        free=tuple(z for z in scope if z!=x)
        mask=0
        for row in range(1<<len(free)):
            values={v:(row>>j)&1 for j,v in enumerate(free)}
            exists=False
            for bit in (0,1):
                values[x]=bit
                charges['branch_eval']+=1
                if all(factor_val(f,values,charges) for f in bucket):
                    exists=True;break
            if exists:mask|=1<<row
            charges['table_writes']+=1
        newfactor=(free,mask,('elim',x))
        factors.append(newfactor)
        charges['eliminations']+=1; elimination_count+=1
        peak_bits=max(peak_bits,sum(1<<len(f[0]) for f in factors+bucket))
        if save_trace:
            trace.append({'x':x,'bucket':[{'scope':s,'mask':m,'from':list(prov)} for s,m,prov in bucket],
                          'result':{'scope':free,'mask':mask},'width':width})
        remaining.remove(x)
    assert all(not s for s,_,_ in factors)
    sat=all(mask&1 for s,mask,_ in factors)
    result={'status':'SAT' if sat else 'UNSAT','width':maxwidth,
            'charged':dict(charges),'eliminated':elimination_count,
            'peak_factor_bits':peak_bits,
            'trace':trace if save_trace else [],
            'final':[{'scope':s,'mask':m,'from':list(prov)} for s,m,prov in factors]}
    if sat and recover_witness and save_trace:
        witness=dict(pins)
        for node in reversed(trace):
            x=node['x']; bucket=[(tuple(f['scope']),f['mask'],tuple(f['from'])) for f in node['bucket']]
            for b in (0,1):
                witness[x]=b
                if all(factor_val(f,witness,charges) for f in bucket):break
            else:raise AssertionError('source reconstruction failed')
        assert clauses_satisfied(F,witness)
        charges['witness_original_clause_reads']+=len(F)
        charges['witness_original_literal_reads']+=3*len(F)
        result['witness']=[witness[i] for i in range(1,n+1)]
        result['charged']=dict(charges)
    return result

def up_dpll(F,n,pins=None):
    """Reference exact UP-DPLL, instrumenting original clause and literal visits.
    A U leaf is a falsified original clause under proven UP consequences; recursive
    branching on two values covers the remaining cube.  Returns a proof tree.
    """
    stats=Counter()
    def unitprop(assignment):
        a=dict(assignment)
        while True:
            changed=False
            for j,c in enumerate(F):
                stats['clause_visits']+=1
                un=[];true=False
                for z in c:
                    stats['literal_visits']+=1
                    v=abs(z)
                    if v not in a:un.append(z)
                    elif a[v]==int(z>0):true=True;break
                if true:continue
                if not un:return a,j
                if len(un)==1:
                    z=un[0]; v=abs(z);value=int(z>0)
                    if v in a and a[v]!=value:return a,j
                    if v not in a:a[v]=value;stats['unit_writes']+=1;changed=True
            if not changed:return a,None
    def rec(a):
        stats['nodes']+=1
        a,bad=unitprop(a)
        if bad is not None:return {'conflict_clause':bad,'cube':sorted(a.items())}
        if len(a)==n:return {'witness':[a[i] for i in range(1,n+1)]}
        x=next(i for i in range(1,n+1) if i not in a)
        for b in (0,1):
            child=rec(dict(a,**{x:b})) if False else rec({**a,x:b})
            if 'witness' in child:return child
            if b==0:first=child
        return {'split':x,'zero':first,'one':child}
    proof=rec(pins or {})
    return {'status':'SAT' if 'witness' in proof else 'UNSAT', 'charged':dict(stats),'proof':proof}

def bucket_heap(F,n,pins=None,width_cap=11,save_trace=True,recover_witness=True):
    """Source-authenticated exact Boolean VE with *incremental* min-scope heap.
    Same deterministic elimination order and matrices as bucket_decide, but
    updates only source-scopes whose factor incidences changed.  Heap entries
    are versioned and stale entries count as paid processing.  No free width
    discovery, proof, original-source check or semantic oracle.
    """
    import heapq
    pin=dict(pins or {})
    C=Counter(grammar_clause_reads=len(F),grammar_literal_reads=3*len(F))
    if not valid(F,n):return {'status':'MALFORMED','charged':dict(C),'trace':[]}
    if any(not isinstance(k,int) or not 1<=k<=n or v not in (0,1) for k,v in pin.items()):
        return {'status':'MALFORMED_PIN','charged':dict(C),'trace':[]}
    original=exact_factor(F,pin,C)
    alive={i:z for i,z in enumerate(original)}; nextid=len(alive)
    remaining=set(range(1,n+1))-set(pin)
    inc={i:set() for i in remaining}
    for fid,(scope,_,_) in alive.items():
        for x in scope:inc[x].add(fid);C['incidence_writes']+=1
    heap=[]; version=Counter(); trace=[];maxwidth=0;peak_bits=0;peak_heap=0;peak_inc=0
    def update_key(x):
        if x not in remaining:return
        u=set()
        for i in inc[x]:
            C['incidence_reads']+=1
            u.update(alive[i][0]);C['scope_union_scans']+=len(alive[i][0])
        version[x]+=1
        heapq.heappush(heap,(len(u),x,version[x]));C['heap_push']+=1
        return u
    for x in sorted(remaining):update_key(x)
    while remaining:
        while True:
            width,x,v=heapq.heappop(heap);C['heap_pop']+=1
            if x in remaining and v==version[x]:break
            C['stale_pop']+=1
        neighbors=set()
        bucket_ids=sorted(inc[x])
        bucket=[alive[fid] for fid in bucket_ids]
        for scope,_,_ in bucket:
            neighbors.update(scope);C['scope_union_scans']+=len(scope)
        assert len(neighbors)==width
        maxwidth=max(maxwidth,width)
        if width>width_cap:
            C['failed_width_cap']+=1
            return {'status':'UNRESOLVED','width':width,'eliminated':C['eliminations'],
                    'charged':dict(C),'peak_factor_bits':peak_bits,'peak_heap_entries':peak_heap,
                    'peak_incidence_entries':peak_inc,'remaining':len(remaining),
                    'trace':trace if save_trace else []}
        scope=tuple(sorted(neighbors))
        free=tuple(z for z in scope if z!=x)
        mask=0
        for row in range(1<<len(free)):
            a={z:(row>>i)&1 for i,z in enumerate(free)}
            exists=False
            for b in (0,1):
                a[x]=b;C['branch_eval']+=1
                if all(factor_val(f,a,C) for f in bucket):exists=True;break
            if exists:mask|=1<<row
            C['table_writes']+=1
        new=(free,mask,('elim',x))
        if save_trace:
            trace.append({'x':x,
             'bucket':[{'scope':s,'mask':m,'from':list(prov)} for s,m,prov in bucket],
             'result':{'scope':free,'mask':mask},'width':width})
        for fid in bucket_ids:
            old=alive.pop(fid)
            for z in old[0]:
                inc[z].remove(fid);C['incidence_writes']+=1
        remaining.remove(x);del inc[x]
        alive[nextid]=new
        for z in free:
            inc[z].add(nextid);C['incidence_writes']+=1
        nextid+=1
        for z in free:update_key(z)
        C['eliminations']+=1
        peak_bits=max(peak_bits,sum(1<<len(z[0]) for z in alive.values()))
        peak_heap=max(peak_heap,len(heap));peak_inc=max(peak_inc,sum(map(len,inc.values())))
    assert all(not scope for scope,_,_ in alive.values())
    sat=all(mask&1 for scope,mask,_ in alive.values())
    out={'status':'SAT' if sat else 'UNSAT','width':maxwidth,
         'charged':dict(C),'eliminated':C['eliminations'],
         'peak_factor_bits':peak_bits,'peak_heap_entries':peak_heap,
         'peak_incidence_entries':peak_inc,
         'trace':trace if save_trace else [],
         'final':[{'scope':s,'mask':m,'from':list(prov)} for s,m,prov in alive.values()]}
    if sat and save_trace and recover_witness:
        a=dict(pin)
        for node in reversed(trace):
            x=node['x']
            for b in (0,1):
                a[x]=b
                if all(factor_val((tuple(f['scope']),f['mask'],tuple(f['from'])),a,C)
                       for f in node['bucket']):break
            else:raise AssertionError('failed source reconstruction')
        assert clauses_satisfied(F,a)
        C['witness_original_clause_reads']+=len(F)
        C['witness_original_literal_reads']+=3*len(F)
        out['witness']=[a[i] for i in range(1,n+1)]
        out['charged']=dict(C)
    return out


def smoke():
    """Standalone short rerun without external SAT oracle or fixture downloads.
    Full original U198/V198 input and independent verifier are separate artifacts.
    """
    A={5:1}; B={5:1,4:0,6:0}; Z={}; Q={1:0,5:0,6:0}
    cases=[('Y6',Y6,6,{}),
       ('F9_S',F9,9,{1:0,2:0,8:1,9:1}),
       ('F9_U',F9,9,{8:0,3:0,7:0,6:0,1:1,5:1}),
       ('F15_S',F15,15,dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))),
       ('F15_U',F15,15,dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0))))]
    for t in (2,4,8):
        for name,profiles in [('AZ',[A,Z]*(t//2)),('BQ',[B,Q]*(t//2))]:
            cases.append((f'G{t}_{name}',gcycle(t),9*t,pins_of(profiles,t)))
    out=[]
    for name,F,n,pins in cases:
        h=bucket_heap(F,n,pins,width_cap=11,save_trace=True,recover_witness=True)
        full=bucket_decide(F,n,pins,width_cap=11,save_trace=True,recover_witness=True)
        assert h['status']==full['status']
        assert h['trace']==full['trace']
        d=up_dpll(F,n,pins)
        assert d['status']==h['status']
        out.append({'case':name,'status':h['status'],'width':h['width'],
             'selector_incidence_scope_scans':h['charged'].get('scope_union_scans',0),
             'global_selector_factor_tests':full['charged'].get('selector_factor_tests',0),
             'UP_DPLL_nodes':d['charged']['nodes']})
    return out

if __name__=='__main__':
    print(json.dumps({'run':'PAID-INCREMENTAL-BUCKET315','status':'PASS',
                       'scope':'only parsed canonical sources; no binary parser',
                       'P_vs_NP':'OPEN','cases':smoke()},indent=2))