"""Finite tests of paid serial restart caps, not a SAT runtime theorem."""
import json,time,signal,hashlib,itertools
from pathlib import Path
signal.alarm(24)
start=time.monotonic()
def race(jobs, cap, rounds=12):
    work=attempts=peak=0
    for e in range(rounds):
        budget=2**e
        for runtime,space,answer in jobs:
            attempts+=1
            used=min(runtime,budget)
            # Synthetic guest allocates its declared workspace at step 1.
            if space>cap:
                used=1
                peak=max(peak,cap)
                work+=used
                continue
            peak=max(peak,space)
            work+=used
            if runtime<=budget and answer is not None:
                return answer,work,peak,attempts
    return None,work,peak,attempts
checks=0
for k in range(1,9):
  for t in range(1,129):
    for winner in range(k):
      jobs=[(10000,1,None)]*k
      jobs[winner]=(t,1,False)
      ans,work,peak,a=race(jobs,8)
      assert ans is False and work<4*k*t and peak<=8
      checks+=1
# Losing guest can blow space even when fastest winner is tiny.
uncapped=race([(10000,1024,None),(64,1,True)],2048)
capped=race([(10000,1024,None),(64,1,True)],8)
assert uncapped[2]==1024 and capped[2]<=8 and capped[0] is True
# All 256 proper three-variable clause sets and all variable permutations.
clauses=[tuple((i+1)*s for i,s in enumerate(signs)) for signs in itertools.product((-1,1),repeat=3)]
def sat(F,a):
  return all(any(a[abs(l)-1]==(l>0) for l in c) for c in F)
coverage=0
assignments=list(itertools.product((False,True),repeat=3))
for mask in range(256):
  F=[clauses[i] for i in range(8) if mask>>i&1]
  truth=any(sat(F,a) for a in assignments)
  for order in itertools.permutations(range(3)):
    branches=[]
    for values in assignments:
      a=[False]*3
      for i,v in zip(order,values):a[i]=v
      branches.append(sat(F,a))
    assert any(branches)==truth
    assert all(not b for b in branches)==(not truth)
    # Partial failure never certifies UNSAT.
    if not any(branches[:4]) and any(branches[4:]):
      assert truth
    coverage+=1
reset=[{"rank_bits":n,"possible_attempts":2**n,"per_attempt_scan_cost":n,"total":n*2**n} for n in range(1,21)]
out={"status":"COMPUTATIONAL","runtime_grid_checks":checks,"cover_checks":coverage,
"uncapped_loser":{"answer":uncapped[0],"work":uncapped[1],"peak":uncapped[2]},
"capped_loser":{"answer":capped[0],"work":capped[1],"peak":capped[2]},
"rank_counterexample":reset,"seed":None,
"limitations":["Synthetic guest work units are not native machine bit steps.","No all-input SAT coverage or shrinker is constructed."],
"elapsed_seconds":time.monotonic()-start,
"code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_suffix(".json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:v for k,v in out.items() if k!="rank_counterexample"},indent=2))

