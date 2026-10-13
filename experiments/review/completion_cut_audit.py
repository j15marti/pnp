#!/usr/bin/env python3
"""COMPLETIONCUT1: exact bounded audits of completion-time random snapshots.
This tests causal protocols, not a SAT runtime lower bound. No randomness is
assumed of SHA-256: every tiny digest fiber is counted exactly. All source
bitstreams in the stated finite domains are enumerated. Each batch has a
25-second cooperative deadline. Run batches separately.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import time

RUN_ID = 'COMPLETIONCUT1'

class Audit:
    def __init__(self) -> None:
        self.start = time.monotonic()
        self.checks: Counter[str] = Counter()
    def check(self, condition: bool, name: str) -> None:
        if time.monotonic() - self.start > 25:
            raise TimeoutError('25-second batch budget exceeded')
        self.checks[name] += 1
        if not condition:
            raise AssertionError(name)
    def result(self, batch: str, data: dict) -> dict:
        return dict(run_id=RUN_ID, batch=batch, status='COMPUTATIONAL', seed=None,
                    method='exact exhaustive finite enumeration', failures=0,
                    assertions=sum(self.checks.values()), checks=dict(self.checks),
                    elapsed_seconds=time.monotonic()-self.start, data=data,
                    code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())

def value(bits: tuple[int, ...]) -> int:
    out = 0
    for b in bits:
        out = (out << 1) | b
    return out

def fraction(x: Fraction) -> str:
    return str(x)

def stop(stream: tuple[int, ...], program: int) -> int:
    # A stopping time: the decision at t depends only on the first t bits.
    if stream[0] == (program & 1):
        return 1
    if stream[1] == ((program >> 1) & 1):
        return 2
    return 3

def prediction(stream: tuple[int, ...], p: int, width: int, q: int) -> tuple[int, set[int]]:
    t = stop(stream, p)
    prior = value(stream[:t])
    choices = {((p * 3) ^ prior) + j for j in range(q)}
    return t, {v % (1 << width) for v in choices}

def precommit_batch(a: Audit) -> dict:
    rows = []
    for width, count, q in [(2,2,1),(3,4,1),(4,8,1),(5,8,2)]:
        horizon = 3 + width
        hits = [0] * count
        fail_all = 0
        first_common = None
        prefix_counts: dict[tuple, Counter[int]] = {}
        for s in itertools.product((0,1), repeat=horizon):
            successes=[]
            for p in range(count):
                t, choices = prediction(s,p,width,q)
                r=value(s[t:t+width])
                prefix_counts.setdefault((p,t,s[:t]),Counter())[r] += 1
                good = r in choices
                hits[p] += good
                successes.append(good)
                # A compact post-release copier always produces the raw challenge.
                a.check(value(tuple(s[t:t+width])) == r, 'postrelease_copy')
            if not any(successes):
                fail_all += 1
                if first_common is None:
                    first_common=''.join(map(str,s))
        total=1<<horizon
        for h in hits:
            a.check(Fraction(h,total) == Fraction(q,1<<width),'per_program_exact_hit_rate')
        for counts in prefix_counts.values():
            a.check(len(counts)==(1<<width) and len(set(counts.values()))==1,
                    'freshness_conditional_on_stop_and_prefix')
        union=Fraction(total-fail_all,total)
        bound=Fraction(count*q,1<<width)
        a.check(union<=bound,'common_stream_union_bound')
        a.check(fail_all>0,'common_stream_all_precommits_fail')
        rows.append(dict(block_bits=width, programs=count,list_size=q,stream_bits=horizon,
                         streams=total, per_program_hits=hits,
                         union_success=fraction(union),union_bound=fraction(bound),
                         all_failed_streams=fail_all, first_all_failed_stream=first_common))
    return dict(rows=rows)

# Each bit of a cube mask denotes one proper 3-clause on variables 1,2,3.
CUBE=[tuple((j+1)*(1 if not (p>>j&1) else -1) for j in range(3)) for p in range(8)]
def sat(mask:int) -> int:
    clauses=[CUBE[j] for j in range(8) if mask>>j&1]
    for x in range(8):
        if all(any(bool(x>>(abs(l)-1)&1)==(l>0) for l in c) for c in clauses):
            return 1
    return 0
MASKS=(1,127,255,129)
ANS=tuple(sat(m) for m in MASKS)

def digest(state:int, ans:int, r:int, stamp:int|None=None) -> int:
    data=[state,ans,r]
    if stamp is not None:data.append(stamp)
    return hashlib.sha256(bytes(data)).digest()[0] & 3

def run_path(stream:tuple[int,...], mode:str, stamp:bool=False,
             blocks:tuple[int,...]|None=None) -> tuple:
    state=0; clock=0; logical=[]; full=[]; work=0; waits=0
    for i in range(3):
        ans=ANS[state]; formula=MASKS[state]
        duration=1 if mode=='fast' else 1+ans
        if mode=='early_wait':
            work+=1; waits+=duration-1
        else:work+=duration
        clock+=duration
        tau=clock
        r=blocks[i] if blocks is not None else value(stream[tau:tau+2])
        state=digest(state,ans,r,tau if stamp else None)
        clock+=2
        logical.append((formula,ans,r,state))
        full.append((formula,ans,tau,r,state))
    return tuple(logical), tuple(full), work, waits, clock

def replay_batch(a:Audit) -> dict:
    h=12; cf=Counter();cs=Counter();sf=Counter();ss=Counter()
    unequal=0;same_timed=0; both_results=set()
    for stream in itertools.product((0,1), repeat=h):
        f=run_path(stream,'fast');s=run_path(stream,'slow')
        e=run_path(stream,'early_wait')
        cf[f[0]]+=1;cs[s[0]]+=1
        unequal += f[0]!=s[0]
        blocks=tuple(row[2] for row in s[0])
        replay=run_path((),'slow',blocks=blocks)
        a.check(replay[1]==s[1],'sample_record_exact_replay')
        a.check(e[1]==s[1], 'same_completion_hash_early_compute_wait')
        a.check(e[2]<s[2] and e[2]+e[3]==s[2], 'active_wait_accounting_not_in_hash')
        same_timed += e[1]==s[1]
        both_results.update(row[1] for row in s[0])
        sf[run_path(stream,'fast',True)[0]]+=1
        ss[run_path(stream,'slow',True)[0]]+=1
    a.check(cf==cs,'event_transcript_law_independent_of_speed')
    a.check(unequal>0,'same_stream_pathwise_difference')
    a.check(sf!=ss,'timestamp_fed_controller_excluded_from_law_claim')
    a.check(both_results=={0,1},'genuine_sat_and_unsat_steps')
    return dict(streams=1<<h,stream_bits=h,stages=3,block_bits=2,
                fast_slow_different_logical_paths=unequal,
                fast_slow_pathwise_difference=fraction(Fraction(unequal,1<<h)),
                logical_distribution_support_fast=len(cf),logical_distribution_support_slow=len(cs),
                distribution_equal=True,early_wait_exact_timed_matches=same_timed,
                timestamp_in_hash_distribution_equal=sf==ss,
                logical_distribution=[dict(trace=k,count=v) for k,v in sorted(cs.items())])

def fibers_batch(a:Audit) -> dict:
    rows=[]
    for state in range(4):
        for ans in (0,1):
            counts=Counter(digest(state,ans,r) for r in range(64))
            mu=Fraction(max(counts.values()),64)
            a.check(sum(counts.values())==64,'digest_fiber_partition')
            a.check(mu>=Fraction(1,4),'digest_max_fiber_bound')
            rows.append(dict(state=state,answer=ans,counts=dict(counts),max_guess_probability=str(mu)))
    stopping=Counter();nextblock=Counter()
    for s in itertools.product((0,1),repeat=5):
        t=next((i+1 for i in range(3) if s[i]),3)
        stopping[s[t-1]]+=1;nextblock[value(s[t:t+2])]+=1
    a.check(stopping[1]==28 and stopping[0]==4,'current_stopping_bit_selection_bias')
    a.check(nextblock==Counter({0:8,1:8,2:8,3:8}),'after_stopping_block_fresh')
    return dict(raw_block_bits=6,digest_bits=2,rows=rows,
                current_stopping_bit_counts=dict(stopping),fresh_next_block_counts=dict(nextblock))

def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--batch',choices=['precommit','replay','fibers'],required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();a=Audit()
    data={'precommit':precommit_batch,'replay':replay_batch,'fibers':fibers_batch}[args.batch](a)
    result=a.result(args.batch,data)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:result[k] for k in ['batch','assertions','failures','elapsed_seconds','code_sha256']}))
if __name__=='__main__':main()
