#!/usr/bin/env python3
"""Charged clause-frontier SAT DP. Run: python frontier_wrapper.py OUTPUT.json
No SAT queries. Tables are capped; None means budget exceeded, never UNSAT.
Each batch has a 25-second alarm. Read-only formula allocated outside measurement.
"""
import itertools, json, random, signal, sys, time, hashlib
from pathlib import Path

def solve(f,n,mode='rescan',cap=12):
    m=dict(source_literal_reads=0,index_probes=0,transitions=0,max_width=0,
           max_table_bytes=1,index_records=0,peak_variable_slots=0)
    first=last=None
    if mode=='index':
        first=[len(f)]*(n+1);last=[-1]*(n+1);m['index_records']=2*(n+1)
        for j,c in enumerate(f):
            for lit in c:
                m['source_literal_reads']+=1;v=abs(lit)
                first[v]=min(first[v],j);last[v]=j
    def boundary(i,candidates):
        if mode=='local_rescan':
            a=[]
            for v in candidates:
                live=False
                for j in range(i+1,len(f)):
                    for lit in f[j]:
                        m['source_literal_reads']+=1
                        if abs(lit)==v:live=True
                if live:a.append(v)
                if len(a)>cap:return None
            return a
        a=[]
        for v in range(1,n+1):
            if mode=='index':
                m['index_probes']+=2;live=first[v]<=i<last[v]
            else:
                before=after=False
                for j,c in enumerate(f):
                    for lit in c:
                        m['source_literal_reads']+=1
                        if abs(lit)==v:
                            if j<=i:before=True
                            else:after=True
                live=before and after
            if live:
                a.append(v)
                if len(a)>cap:return None
        return a
    a=[];table=bytearray([1])
    for i,clause in enumerate(f):
        u=list(a)
        for lit in clause:
            m['source_literal_reads']+=1
            if abs(lit) not in u:u.append(abs(lit))
        b=boundary(i,u)
        if b is None:
            m['cap_exceeded_at_clause']=i
            return None,m
        # a is a prefix of u, so its assignment is the low bits.
        bp=[u.index(v) for v in b]
        lp=[(u.index(abs(lit)),lit>0) for lit in clause]
        out=bytearray(1<<len(b))
        m['max_width']=max(m['max_width'],len(a),len(b))
        m['max_table_bytes']=max(m['max_table_bytes'],len(table)+len(out))
        m['peak_variable_slots']=max(m['peak_variable_slots'],len(a)+len(b)+len(u)+len(bp)+2*len(lp))
        mask=(1<<len(a))-1
        for x in range(1<<len(u)):
            m['transitions']+=1
            if not table[x&mask]:continue
            if not any(bool((x>>p)&1)==val for p,val in lp):continue
            y=sum(((x>>p)&1)<<j for j,p in enumerate(bp))
            out[y]=1
        table=out;a=b
        if not any(table):return False,m
    return bool(table[0]),m

def truth(f,n):
    return any(all(any(bool((x>>(abs(l)-1))&1)==(l>0) for l in c) for c in f) for x in range(1<<n))

def main():
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError('25-second batch limit')))
    signal.alarm(25);start=time.perf_counter();rows=[]
    clauses=list(itertools.product(*[(i,-i) for i in range(1,4)]))
    cases=[('exhaustive_'+str(s),3,tuple(c for j,c in enumerate(clauses) if (s>>j)&1),None) for s in range(256)]
    rng=random.Random(20261007)
    for n in [6,8,10]:
        for seed in range(6):
            f=tuple(tuple(v*rng.choice([-1,1]) for v in rng.sample(range(1,n+1),3)) for _ in range(4*n))
            cases.append((f'random_{n}_{seed}',n,f,None))
    for n in [8,16,32,64]:
        chain=tuple([(-v,v+1) for v in range(1,n)]+[(1,)])
        paired=tuple(c for v in range(1,n+1) for c in [(v,),(-v,v)])
        delayed=tuple([(v,) for v in range(1,n+1)]+[(-v,v) for v in range(1,n+1)])
        cases.extend([(f'chain_{n}',n,chain,True),(f'paired_{n}',n,paired,True),(f'delayed_{n}',n,delayed,True)])
    cases.extend([('empty',0,(),True),('empty_clause',0,((),),False),('unit_conflict',1,((1,),(-1,)),False),('xor_unsat',2,((1,2),(-1,-2),(1,-2),(-1,2)),False)])
    checks=unknowns=fallback_checks=0
    for name,n,f,expected in cases:
        if expected is None:expected=truth(f,n)
        for mode in ['rescan','index','local_rescan']:
            ans,metrics=solve(f,n,mode)
            if ans is None:
                unknowns+=1
                from source_backed_wrapper import propagated_source_solve
                fallback,fallback_metrics=propagated_source_solve(f,n)
                assert fallback==expected
                fallback_checks+=1
                metrics['fallback_metrics']=fallback_metrics
            else:assert ans==expected,(name,mode,ans,expected);checks+=1
            rows.append(dict(name=name,n=n,clauses=len(f),literals=sum(map(len,f)),mode=mode,answer=ans,expected=expected,**metrics))
    # Complementation and variable-renaming keep the boundary cardinalities.
    invariance=0
    for name,n,f,expected in cases[256:274]:
        base,_=solve(f,n)
        g=tuple(tuple((n+1-abs(l))*(-1 if l>0 else 1) for l in c) for c in f)
        ans,_=solve(g,n);assert ans==base;invariance+=1
    result=dict(status='COMPUTATIONAL',cases=len(cases),answer_checks=checks,cap_exits=unknowns,
                invariance_checks=invariance,fallback_checks=fallback_checks,errors=0,seconds=time.perf_counter()-start,
                seed=20261007,cap=12,code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),rows=rows,
                caveats=['Logical table payload only, not Python peak memory.',
                         'Rescans and index construction/probes charged; no formula reordering discovery.',
                         'None is budget exhaustion; no generic small-width guarantee.'])
    Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
    print({k:v for k,v in result.items() if k!='rows'})
    for r in rows:
        if r['name'] in ['paired_64','delayed_64','chain_64','random_10_0']:print(r)
if __name__=='__main__':main()
