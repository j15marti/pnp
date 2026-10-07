#!/usr/bin/env python3
"""Same-realization block-batched frontier DP; no SAT queries.
Run: timeout 30s python batched_frontier.py OUTPUT.json
Requires frontier_wrapper.py in this directory for the independent baseline.
"""
import hashlib,itertools,json,random,signal,sys,time
from pathlib import Path
from frontier_wrapper import solve,truth

def batched(f,n,block=8,cap=12):
    assert block>=1
    counts=dict(source_literal_reads=0,membership_probes=0,transitions=0,
                max_width=0,max_table_bytes=1,peak_last_records=0,blocks=0)
    boundary=[];table=bytearray([1])
    for start in range(0,len(f),block):
        stop=min(start+block,len(f));last={v:-1 for v in boundary}
        # Small block is scanned in place, not copied.
        for j in range(start,stop):
            for lit in f[j]:
                counts['source_literal_reads']+=1
                last[abs(lit)]=j
        # One shared suffix pass supplies all queried variable lifetimes.
        for j in range(stop,len(f)):
            for lit in f[j]:
                counts['source_literal_reads']+=1
                counts['membership_probes']+=1
                if abs(lit) in last:last[abs(lit)]=j
        counts['blocks']+=1
        counts['peak_last_records']=max(counts['peak_last_records'],len(last))
        for i in range(start,stop):
            clause=f[i];u=list(boundary)
            for lit in clause:
                counts['source_literal_reads']+=1
                if abs(lit) not in u:u.append(abs(lit))
            after=[v for v in u if last[v]>i]
            if len(after)>cap:
                counts['cap_exceeded_at_clause']=i
                return None,counts
            bp=[u.index(v) for v in after]
            lp=[(u.index(abs(v)),v>0) for v in clause]
            out=bytearray(1<<len(after));mask=(1<<len(boundary))-1
            counts['max_width']=max(counts['max_width'],len(boundary),len(after))
            counts['max_table_bytes']=max(counts['max_table_bytes'],len(table)+len(out))
            for x in range(1<<len(u)):
                counts['transitions']+=1
                if table[x&mask] and any(bool((x>>p)&1)==val for p,val in lp):
                    out[sum(((x>>p)&1)<<j for j,p in enumerate(bp))]=1
            boundary=after;table=out
            if not any(table):return False,counts
    return bool(table[0]),counts

def main():
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError('25 second budget')))
    signal.alarm(25);start=time.perf_counter();rng=random.Random(20261008)
    clauses=list(itertools.product(*[(i,-i) for i in range(1,4)]))
    cases=[('exhaustive_'+str(s),3,tuple(c for j,c in enumerate(clauses) if (s>>j)&1),None) for s in range(256)]
    for n in [6,8,10]:
        for seed in range(8):
            f=tuple(tuple(v*rng.choice((-1,1)) for v in rng.sample(range(1,n+1),3)) for _ in range(4*n))
            cases.append((f'random_{n}_{seed}',n,f,None))
    for n in [16,32,64,128,256]:
        cases.append((f'chain_{n}',n,tuple([(-v,v+1) for v in range(1,n)]+[(1,)]),True))
    cases += [('empty',0,(),True),('empty_clause',0,((),),False),('unit_conflict',1,((1,),(-1,)),False),
              ('delayed_24',24,tuple([(v,) for v in range(1,25)]+[(-v,v) for v in range(1,25)]),True)]
    rows=[];checks=unknowns=matched=0
    for name,n,f,expected in cases:
        if expected is None:expected=truth(f,n)
        old,oldm=solve(f,n,'local_rescan',cap=12)
        for block in [1,2,4,8,16,32]:
            ans,m=batched(f,n,block,cap=12)
            assert ans==old,(name,block,ans,old)
            if ans is None:unknowns+=1
            else:
                assert ans==expected;checks+=1
            assert m['transitions']==oldm['transitions']
            matched+=1
            L=sum(map(len,f));q=max(map(len,f),default=0)
            assert m['source_literal_reads'] <= (2+(len(f)+block-1)//block)*L
            assert m['peak_last_records']<=12+q*block
            rows.append(dict(name=name,n=n,clauses=len(f),literals=L,block=block,answer=ans,
                             baseline_reads=oldm['source_literal_reads'],**m))
    result=dict(status='COMPUTATIONAL',seed=20261008,cases=len(cases),answer_checks=checks,
                cap_exits=unknowns,matched_traversals=matched,seconds=time.perf_counter()-start,
                code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),rows=rows,
                caveats=['No general width bound or favorable unrestricted SAT exponent.',
                         'Python dict is an implementation; formal deterministic ledger uses balanced tree lookup.',
                         'Counters are literal reads/table payload, not total machine time or RSS.',
                         'Cap returns UNKNOWN; this run does not mix in source-backend fallback bounds.'])
    Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
    print({k:v for k,v in result.items() if k!='rows'})
    for row in rows:
        if row['name']=='chain_256':print(row)
if __name__=='__main__':main()
