#!/usr/bin/env python3
"""ARC203 independent pair-trace last-write block audit, no SAT hardness claim.
This checks an abstract source-authenticated event grammar, not physical TM time.
"""
import copy
import hashlib
import json
import math
from pathlib import Path

SEED = 0
RUN_ID = 'ARC-TRACE-BLOCK-BALANCE203'

def sat5(bits):
    return (bits[0] == 0 and not(bits[1] and bits[2]) and not(bits[3] and bits[4]))

def make_trace(source):
    n=len(source)
    memory={}
    events=[]
    for step in range(4*n+1):
        tape=step%2
        address=(step//2)%(n+1)
        input_pos=(step//2)%n
        key=(tape,address)
        before=memory.get(key,0)
        after=before ^ source[input_pos] ^ (1 if step%5==0 else 0)
        events.append(dict(step=step,tape=tape,addr=address,src_addr=input_pos,
                           src=source[input_pos],before=before,after=after))
        memory[key]=after
    return events

def structural_ok(source,events):
    n=len(source)
    if not n or len(events)!=4*n+1:
        return False
    for i,e in enumerate(events):
        if set(e)!={'step','tape','addr','src_addr','src','before','after'}:
            return False
        if not all(isinstance(e[x],int) for x in e):
            return False
        if (e['step']!=i or e['tape']!=i%2 or e['addr']!=(i//2)%(n+1)
            or e['src_addr']!=(i//2)%n or e['src']!=source[e['src_addr']]
            or e['before'] not in (0,1) or e['after'] not in (0,1)):
            return False
        if e['after']!=(e['before'] ^ e['src'] ^ (i%5==0)):
            return False
    return True

def direct_check(source,events):
    if not structural_ok(source,events):
        return False
    mem={}
    for e in events:
        key=(e['tape'],e['addr'])
        if e['before']!=mem.get(key,0):
            return False
        mem[key]=e['after']
    return True

def bucket_check(source,events,B):
    if not isinstance(B,int) or B<1 or not structural_ok(source,events):
        return False,{'reason':'syntax or source'}
    n=len(source)
    R=len(events)
    scans=0
    clears=0
    maxcache=0
    for tape in range(2):
        for lo in range(0,n+1,B):
            hi=min(lo+B,n+1)
            cache=[0]*(hi-lo)
            clears+=len(cache)
            maxcache=max(maxcache,len(cache))
            for e in events:
                scans+=1
                if e['tape']==tape and lo<=e['addr']<hi:
                    j=e['addr']-lo
                    if cache[j]!=e['before']:
                        return False,{'reason':'last-write','scans':scans,'clears':clears,
                                      'peak_cached_symbols':maxcache,'B':B}
                    cache[j]=e['after']
    return True,{'scans':scans,'clears':clears,'peak_cached_symbols':maxcache,'B':B,
                 'R':R,'n':n,'num_buckets':2*math.ceil((n+1)/B)}

def forge_coherent_local(events,index):
    new=copy.deepcopy(events)
    new[index]['before']^=1
    new[index]['after']^=1
    return new

def run():
    assertions=0
    rows=[]
    hostile=0
    for n in range(1,13):
        sources=[[(mask>>i)&1 for i in range(n)] for mask in range(min(1<<n,64))]
        for source in sources:
            ev=make_trace(source)
            assert structural_ok(source,ev);assertions+=1
            assert direct_check(source,ev);assertions+=1
            R=len(ev)
            capacities=sorted({1,2,3,4,max(1,R//4),max(1,R//2),R})
            for B in capacities:
                passed,c=bucket_check(source,ev,B)
                assert passed,(source,B,c)
                assertions+=1
                assert c['peak_cached_symbols']<=B
                assert c['scans']==R*c['num_buckets']
                assert c['clears']==2*(n+1)
                assertions+=3
                if len(rows)<90:
                    rows.append({'n':n,'source':''.join(map(str,source)),**c})
            for ix in {0,len(ev)//2,len(ev)-1}:
                bad=forge_coherent_local(ev,ix)
                assert structural_ok(source,bad);assertions+=1
                assert not direct_check(source,bad);assertions+=1
                for B in (1,2,R):
                    yes,_=bucket_check(source,bad,B)
                    assert not yes,(n,ix,B)
                    assertions+=1
                    hostile+=1
            bad=copy.deepcopy(ev)
            bad[0]['src']^=1
            assert not structural_ok(source,bad);assertions+=1
            assert not direct_check(source,bad);assertions+=1
            assert not bucket_check(source,bad,2)[0];assertions+=1
    counts={True:0,False:0}
    for mask in range(32):
        src=[(mask>>i)&1 for i in range(5)]
        counts[sat5(src)]+=1
        assert direct_check(src,make_trace(src));assertions+=1
    assert counts=={True:9,False:23},counts
    assertions+=1
    result={'run_id':RUN_ID,'status':'COMPUTATIONAL','assertions':assertions,
            'failures':0,'random_seed':SEED,
            'method':'exhaustive finite bit masks, deterministic event schedule',
            'sat5_counts':{'SAT':counts[True],'UNSAT':counts[False]},
            'forged_local_valid_memory_invalid_cases':hostile,
            'representative_bucket_ledgers':rows,
            'note':'event-level consistency only; not native TM transitions or all-SAT theorem'}
    path=Path(__file__).with_name('arc203_trace_bucket_raw.json')
    path.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'assertions':assertions,'forged_checks':hostile,
          'sat5_counts':result['sat5_counts'],'rows':len(rows),
          'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'raw_sha256':hashlib.sha256(path.read_bytes()).hexdigest()},indent=2))

if __name__=='__main__':
    run()
