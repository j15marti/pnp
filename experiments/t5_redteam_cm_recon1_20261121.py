"""Finite transition-system audit, not a T5 lower-bound experiment."""
from itertools import product
import json

def run(delta,start):
    halt=len(delta);seen=set();path=[];s=start
    while s!=halt and s not in seen:
        seen.add(s);path.append(s);s=delta[s]
    return s==halt,path

def main():
    rows=[]
    for q in range(1,6):
        halting=looping=0;longest=0
        for delta in product(range(q+1),repeat=q):
            for start in range(q):
                stops,path=run(delta,start)
                if stops:
                    halting+=1;longest=max(longest,len(path))
                    # Independent bounded replay, including the terminal state.
                    s=start;post=[]
                    for _ in path:s=delta[s];post.append(s)
                    assert s==q and len(set(post))==len(path)
                else:
                    looping+=1
                    # A repeat means no later halting, even if run for extra cycles.
                    s=start
                    for _ in range(3*q+1):
                        assert s!=q;s=delta[s]
        rows.append(dict(nonhalting_state_universe=q,halting_runs=halting,looping_runs=looping,longest_actual_run=longest))
    # Taking a pointwise maximum before summing changes the quantity.
    runs=[[9,1,1],[1,9,1],[1,1,9]]
    real=max(map(sum,runs));envelope=sum(max(r[t] for r in runs) for t in range(3))
    assert (real,envelope)==(11,27)
    # One transition to halt, then unrolled stuttering: no injective T-code argument.
    actual=[1];padded=actual*16
    assert len(set(actual))==1 and len(set(padded))==1
    print(json.dumps({'scope':'finite functional graphs; no circuit-size or T5 runtime measurement',
        'exhaustive_transition_systems':rows,'maximum_sum_control':{'per_run_max':real,'layer_envelope':envelope},
        'posthalt_control':{'actual_transitions':1,'padded_layers':16,'distinct_poststates':1}},indent=2))
if __name__=='__main__':main()
