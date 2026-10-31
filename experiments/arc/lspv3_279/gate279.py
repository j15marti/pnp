#!/usr/bin/env python3
"""LSPV-3 GATE279: implicit primal-articulation / streamed cofactor experiment.
Finite reference connectivity uses BFS (linear memory); logspace existence is a
separate consequence of Reingold (JACM 2008), not a claim about this Python.
All costs are instrumented source-semantic events, not native FLMV steps.
"""
from collections import Counter, deque
from itertools import product
from pathlib import Path
import json, random, hashlib, sys
ROOT=Path(__file__).resolve().parent
SEED=2791031

class Meter:
    def __init__(self): self.c=Counter()
    def add(self,k,v=1): self.c[k]+=v


def stars(k,wrong=False):
    F=[];n=1
    for i in range(k):
        y=n+1;z=n+2;n+=2
        s=1 if wrong and i==k-1 else -1
        for a,b in product((1,-1),repeat=2):F.append((s,a*y,b*z))
        for j in range(k-1):
            u=n+1;v=n+2;n+=2;F.append((y,u,v))
    return F,n


def rename(F,n,seed):
    r=random.Random(seed);p=list(range(1,n+1));r.shuffle(p)
    tr={i+1:p[i] for i in range(n)}
    return [tuple((1 if l>0 else -1)*tr[abs(l)] for l in c) for c in F]


def controls():
    h7=[tuple((i if mask&(1<<(i-1)) else -i) for i in range(1,4)) for mask in range(1,8)]
    h8=[tuple((i if mask&(1<<(i-1)) else -i) for i in range(1,4)) for mask in range(8)]
    parity=[tuple((i if mask&(1<<(i-1)) else -i) for i in range(1,4)) for mask in range(8) if mask.bit_count()%2==0]
    return [('H7_SAT',h7,3),('H8_UNSAT',h8,3),('XOR_SAT',parity,3),
            ('HORN_SAT',[(1,),(-1,2),(-2,3)],3),
            ('HORN_UNSAT',[(1,),(-1,2),(-2,3),(-3,)],3),
            ('KROM_SAT',[(1,2),(-1,2),(1,-2)],2),
            ('KROM_UNSAT',[(1,2),(-1,2),(1,-2),(-1,-2)],2),
            ('NO_ARTIC_HORN',[(1,2,3),(1,2,4),(1,3,4),(2,3,4)],4),
            # Articulation 1 with a large dense, all-positive component.
            ('UNBALANCED_ARTIC',[(1,2,3),(1,7,8)]+[tuple(t) for t in __import__('itertools').combinations((2,3,4,5,6),3)],8)]


def adj(F,u,v,x=None,meter=None):
    if u==v or u==x or v==x:return False
    for c in F:
        if meter:meter.add('source_clause_scans')
        if u in [abs(l) for l in c] and v in [abs(l) for l in c]: return True
    return False


def reachable(F,n,u,v,x,meter=None):
    """Finite reference implementation; holds seen O(n) space, not USTCON-in-L."""
    if u==x or v==x:return False
    todo=deque([u]);seen={u}
    while todo:
        z=todo.popleft()
        if z==v:return True
        for w in range(1,n+1):
            if w not in seen and w!=x and adj(F,z,w,x,meter):
                seen.add(w);todo.append(w)
    return False


def components(F,n,x,meter=None):
    """Independent representative-minimum partition, no graph materialization."""
    members=[i for i in range(1,n+1) if i!=x]
    groups=[]
    for v in members:
        if any(reachable(F,n,v,r,x,meter) for r in (G[0] for G in groups)):continue
        group=[w for w in members if reachable(F,n,v,w,x,meter)]
        groups.append(group)
    return groups


def raw_child(F,x,b,group):
    G=set(group);out=[];sources=[]
    for j,c in enumerate(F,1):
        vs={abs(l) for l in c if abs(l)!=x}
        if not vs or not vs.issubset(G):continue
        if any(abs(l)==x and ((l>0)==b) for l in c):continue
        out.append(tuple(l for l in c if abs(l)!=x));sources.append(j)
    return out,sources


def boundary_ok(F,x,b):
    for c in F:
        if any(abs(l)!=x for l in c):continue
        if not any(((l>0)==b) for l in c):return False
    return True


def bit_encode(F,n):
    """Declared, fixed-width, prefix-free for fixed n: n, clause count, each clause width then signed IDs."""
    w=max(1,n.bit_length());h=max(2,(n*n*n+2).bit_length())
    s=format(n,'0%db'%w)+format(len(F),'0%db'%h)
    for c in F:
        s+=format(len(c),'03b')
        for lit in c: s+=('1' if lit>0 else '0')+format(abs(lit),'0%db'%w)
    return s


def emitted_bit(F,n,x,b,representative,q,meter):
    """Source-scanning bit accessor: reference BFS handles connectivity; no child stored.
    Crucially total number of clauses is recomputed by a full source sweep.
    """
    assert x is not None and representative!=x
    w=max(1,n.bit_length());h=max(2,(n*n*n+2).bit_length())
    def belongs(c):
        vs=[abs(l) for l in c if abs(l)!=x]
        if not vs:return False
        return reachable(F,n,representative,vs[0],x,meter)
    total=0
    for c in F:
        meter.add('emitter_source_visits')
        if belongs(c) and not any(abs(l)==x and ((l>0)==b) for l in c):total+=1
    assert total < 2**h
    header=format(n,'0%db'%w)+format(total,'0%db'%h)
    if q<len(header):return header[q]
    k=len(header)
    for c in F:
        meter.add('emitter_source_visits')
        if not belongs(c) or any(abs(l)==x and ((l>0)==b) for l in c):continue
        cc=[l for l in c if abs(l)!=x]
        fragment=format(len(cc),'03b')+''.join(('1' if lit>0 else '0')+format(abs(lit),'0%db'%w) for lit in cc)
        if q<k+len(fragment):return fragment[q-k]
        k+=len(fragment)
    raise ValueError('outside child')


def select(F,n,meter):
    baseline=len(components(F,n,None,meter))
    options=[]
    for x in range(1,n+1):
        meter.add('candidate_policies')
        gs=components(F,n,x,meter)
        if len(gs)<=baseline:continue
        # Scan the original encoding to assess actual serialized child lengths.
        maxlen=max((len(bit_encode(raw_child(F,x,b,g)[0],n)) for b in (False,True) for g in gs),default=0)
        options.append((maxlen,x,gs))
    return (min(options,key=lambda z:z[0]) if options else None)


def dpll(F,n):
    meter=Meter();nodes=[0]
    def solve(a):
        nodes[0]+=1;meter.add('dpll_nodes')
        while True:
            forced=False;all_sat=True
            for c in F:
                meter.add('dpll_clause_visits');un=[];sat=False
                for l in c:
                    meter.add('dpll_literal_visits');v=abs(l)
                    if v not in a:un.append(l)
                    elif a[v]==(l>0):sat=True;break
                if sat:continue
                all_sat=False
                if not un:return None
                if len(un)==1:
                    l=un[0];v=abs(l)
                    if v in a and a[v]!=(l>0):return None
                    if v not in a:a[v]=(l>0);forced=True;meter.add('dpll_forced_literals')
            if all_sat:return dict(a)
            if not forced:break
        freq=Counter()
        for c in F:
            if any(abs(l) in a and a[abs(l)]==(l>0) for l in c):continue
            for l in c:
                if abs(l) not in a:freq[abs(l)]+=1
        v=max(freq,key=freq.get);meter.add('dpll_branches')
        for b in (False,True):
            q=dict(a);q[v]=b;w=solve(q)
            if w is not None:return w
        return None
    return solve({}),dict(meter.c)


def audit(F,n):
    c={'zero':[],'one':[],'trail':[],'extrema':[],'pairs':[]}
    z={v:False for v in range(1,n+1)}
    def cnt(a):return [sum((l>0)==a[abs(l)] for l in cc) for cc in F]
    for key,a in [('zero',z),('one',{v:True for v in z})]:
        tt=cnt(a);c[key]={'true_counts':tt,'histogram':[tt.count(i) for i in range(4)],'SAT':0 not in tt}
    a=dict(z)
    for v in list(range(1,n+1))[:min(n,7)]:
        old=cnt(a);a[v]=not a[v];new=cnt(a)
        c['trail'].append({'flip':v,'h':[new.count(i) for i in range(4)],'delta':[new[i]-old[i] for i in range(len(F))]})
    for j,cc in enumerate(F,1):
        s={str(abs(l)):int(l>0) for l in cc};u={str(abs(l)):int(l<0) for l in cc}
        c['extrema'].append({'j':j,'S':s,'invert_S':u,'U':u,'invert_U':s})
    for j,cc in enumerate(F,1):
        for k in range(j+1,len(F)+1):
            dd=F[k-1];co={abs(l):(l>0) for l in cc};do={abs(l):(l>0) for l in dd};share=co.keys()&do.keys()
            same=any(co[v]==do[v] for v in share);opp=any(co[v]!=do[v] for v in share)
            c['pairs'].append({'j':j,'k':k,'SS':not opp,'SU':not same,'US':not same,'UU':not opp})
    return c


def experiment():
    tests=[]
    for k in (2,3):
        for charge in (False,True):
            F,n=stars(k,charge)
            for rr in (False,True):
                f=rename(F,n,SEED+k+int(charge)) if rr else F
                tests.append((f'STAR{k}_{"UNSAT" if charge else "SAT"}'+('_RENAME' if rr else ''),f,n))
    tests.extend(controls())
    records=[]
    for name,F,n in tests:
        F=[tuple(z) for z in F];m=Meter()
        choice=select(F,n,m)
        witness,baseline=dpll(F,n)
        row={'name':name,'n':n,'m':len(F),'N_bits':len(bit_encode(F,n)),'label':'SAT' if witness is not None else 'UNSAT','baseline_DPLL':baseline,
             'selector_counts':dict(m.c),'selector':None,'audit':audit(F,n),'source':[list(c) for c in F]}
        if choice:
            largest,x,gs=choice
            children=[];dpll_cost=Counter();calls=0
            solutions={};proof=[]
            for b in (False,True):
                ok=boundary_ok(F,x,b);parts=[];allgood=ok
                for g in gs:
                    ch,idx=raw_child(F,x,b,g)
                    w,cc=dpll(ch,n);dpll_cost.update(cc);calls+=1
                    if w is None:allgood=False
                    parts.append({'representative':min(g),'component_variables':g,'source_clause_indices':idx,'clauses':[list(c) for c in ch],'child_bits':len(bit_encode(ch,n)),'SAT':w is not None,'witness':w})
                proof.append({'b':b,'boundary_ok':ok,'components':parts,'allgood':allgood})
                if allgood:
                    sol={x:b}
                    for pp in parts:sol.update(pp['witness'])
                    # Assign any unused variables arbitrarily, then verify ALL original clauses.
                    sol.update({v:sol.get(v,False) for v in range(1,n+1)})
                    assert all(any(sol[abs(l)]==(l>0) for l in c) for c in F)
                    solutions[b]=sol
            assert bool(solutions)==(witness is not None)
            # Independently compare physically serialized children against bit-by-bit source-emitter.
            q_checks=[];em=Meter()
            for pp in proof[:2]:
                for child in pp['components'][:2]:
                    bits=bit_encode(child['clauses'],n);rep=child['representative']
                    offsets=sorted(set([0,len(bits)//4,len(bits)//2,3*len(bits)//4,len(bits)-1]))
                    for off in offsets:
                        got=emitted_bit(F,n,x,pp['b'],rep,off,em)
                        assert got==bits[off],(name,b,rep,off)
                        q_checks.append({'b':pp['b'],'r':rep,'position':off,'value':got})
            row['selector']={'x':x,'components':gs,'largest_child_bits':largest,'verified_child_calls':calls,
                             'component_solver_DPLL_cost':dict(dpll_cost),'branch_proofs':proof,
                             'streamed_bits_checked':len(q_checks),'emitter_probe_counts':dict(em.c),'probe_samples':q_checks}
        records.append(row)
        print(name,row['label'],'n',n,'m',len(F),'sep',row['selector']['x'] if row['selector'] else None,
              'source_scans',row['selector_counts'].get('source_clause_scans',0),
              'DPLL_nodes',baseline.get('dpll_nodes'))
    out={'run':'GATE279','seed':SEED,'model':'finite implicit adjacency scans with reference BFS memory, NOT Reingold implementation or native FLMV',
         'records':records,'status':'COMPUTATIONAL','analysis':['selector logspace theorem follows separately by reduction to Reingold USTCON',
         'source-implicit discovery may require many paid rescans; this Python reference does not use logarithmic space']}
    raw=ROOT/'raw279.json';raw.write_text(json.dumps(out,separators=(',',':')))
    totals=Counter()
    for r in records:
        totals[r['label']]+=1
        totals['scan_source_clause_visits']+=r['selector_counts'].get('source_clause_scans',0)
        totals['dpll_nodes']+=r['baseline_DPLL'].get('dpll_nodes',0)
        if r['selector']:
            totals['separator_cases']+=1
            totals['guest_nodes']+=r['selector']['component_solver_DPLL_cost'].get('dpll_nodes',0)
            totals['emitter_source_scans']+=r['selector']['emitter_probe_counts'].get('source_clause_scans',0)
            totals['emitter_source_visits']+=r['selector']['emitter_probe_counts'].get('emitter_source_visits',0)
            totals['bit_probes']+=r['selector']['streamed_bits_checked']
    summary={'run':'GATE279','cases':len(records),'totals':dict(totals),'raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),
             'rows':[{'name':r['name'],'N':r['N_bits'],'SAT':r['label']=='SAT','sep':r['selector']['x'] if r['selector'] else None,
              'max_child_bits':r['selector']['largest_child_bits'] if r['selector'] else None,
              'scan_source_clause_visits':r['selector_counts'].get('source_clause_scans',0),
              'baseline_nodes':r['baseline_DPLL'].get('dpll_nodes',0),
              'guest_nodes':r['selector']['component_solver_DPLL_cost'].get('dpll_nodes',0) if r['selector'] else None} for r in records]}
    (ROOT/'summary279.json').write_text(json.dumps(summary,indent=2))
    print('TOTAL',dict(totals),'RAW_SHA256',summary['raw_sha256'])

if __name__=='__main__':experiment()