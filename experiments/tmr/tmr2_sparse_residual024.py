#!/usr/bin/env python3
"""TMR-2/024: exact finite ordinary MCSP positive-support/residual audit.

Truth table length N=2**n, represented as an N-bit integer.
Circuit basis is fan-in-two AND/OR, fan-in-one NOT, free fan-out; gates counted.
NO circuit-description or state-transition table construction is charged as a
uniform polynomial algorithm. Enumeration is finite external audit only.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import time


def enumerable_circuit_truth_tables(n: int, max_gates: int):
    N = 1 << n
    universe = (1 << N) - 1
    ins = tuple(sum(((a >> v) & 1) << a for a in range(N)) for v in range(n))
    layers = [set(ins)]
    sequence_counts = [1]
    circuits = [ins]
    for gates in range(1, max_gates + 1):
        new_circuits = []
        outputs = set(layers[-1])
        for wires in circuits:
            w = len(wires)
            for a in range(w):
                new = universe ^ wires[a]
                new_circuits.append(wires + (new,))
                outputs.add(new)
            for a in range(w):
                for b in range(a, w):
                    new_and = wires[a] & wires[b]
                    new_or = wires[a] | wires[b]
                    new_circuits.append(wires + (new_and,))
                    new_circuits.append(wires + (new_or,))
                    outputs.add(new_and)
                    outputs.add(new_or)
        layers.append(outputs)
        sequence_counts.append(len(new_circuits))
        circuits = new_circuits
    return layers, sequence_counts


def per_cut_residuals(N: int, YES: set[int]) -> dict:
    """Minimized layered OBDD computed via exact residual languages."""
    assert YES
    M = len(YES)
    layer_counts=[]
    state_maps=[]
    all_suffix_classes=[]
    for cut in range(N+1):
        source_prefix_mask=(1<<cut)-1
        groups={}
        for x in YES:
            p=x & source_prefix_mask
            if p not in groups: groups[p]=set()
            groups[p].add(x >> cut)
        default=frozenset()
        signatures={p:frozenset(v) for p,v in groups.items()}
        unique=set(signatures.values())
        if len(groups)<(1<<cut):unique.add(default)
        canonical={signature:idx for idx,signature in enumerate(sorted(unique,key=lambda r:(len(r),tuple(sorted(r)))))}
        mapping={p:canonical[sig] for p,sig in signatures.items()}
        dead=canonical.get(default,None)
        assert len(groups)<=M
        assert len(canonical)<=M+1
        state_maps.append((mapping,dead))
        all_suffix_classes.append(canonical)
        layer_counts.append({"cut":cut,"active_prefixes":len(groups),
                             "distinct_residuals":len(unique),"dead_state":dead is not None})

    transitions_checked=0
    for cut in range(N):
        source_map, dead=state_maps[cut]
        next_map, next_dead=state_maps[cut+1]
        by_state={}
        for p in range(1<<cut):
            st=source_map.get(p,dead)
            assert st is not None
            dests=[]
            for bit in (0,1):
                p2=p|(bit<<cut)
                nxt=next_map.get(p2,next_dead)
                assert nxt is not None
                dests.append(nxt)
                transitions_checked+=1
            dests=tuple(dests)
            if st in by_state:
                assert by_state[st]==dests,(cut,st)
            else:
                by_state[st]=dests
        assert len(by_state)==len(all_suffix_classes[cut])
    final_map, final_dead=state_maps[N]
    accepted=0
    for x in range(1<<N):
        st=final_map.get(x,final_dead)
        residual=next(sig for sig,index in all_suffix_classes[N].items() if index==st)
        correct=(residual==frozenset({0}))
        assert correct == (x in YES), (N,x)
        accepted+=correct
    assert accepted==M
    return {"positive_count":M,"widths":layer_counts,
            "peak_minimal_width":max(x['distinct_residuals'] for x in layer_counts),
            "sum_minimal_layer_widths":sum(x['distinct_residuals'] for x in layer_counts),
            "terminal_classifications_checked":1<<N,
            "prefix_transition_checks":transitions_checked}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',required=True)
    a=p.parse_args()
    started=time.perf_counter()
    outcomes=[]
    cases=[(2,0),(2,1),(2,2),(2,3),
           (3,0),(3,1),(3,2),(3,3),
           (4,0),(4,1),(4,2),(4,3)]
    cache={}
    for n,s in cases:
        if n not in cache:
            cache[n]=enumerable_circuit_truth_tables(n,max(q for x,q in cases if x==n))
        ys, seq=cache[n]
        info=per_cut_residuals(1<<n,ys[s])
        upper=(s+1)*(n+s+2)*((3*(n+s+2)**2)**s)
        assert len(ys[s])<=upper
        # Domain promise is s in [0,3] for the finite audit, not magnification s>=n.
        info.update({"n":n,"N":1<<n,"threshold_s":s,
                     "topological_gate_sequences_exact_depth":seq[s],
                     "description_upper_bound":upper,
                     "peak_width_vs_positive":f"{info['peak_minimal_width']} <= {len(ys[s])+1}"})
        outcomes.append(info)
    # Hostile fixed-order controls: reverse and interleaved source access.
    order_controls=[]
    N=16
    ys=cache[4][0][2]
    order_map={
        "forward": tuple(range(N)),
        "reverse": tuple(range(N-1,-1,-1)),
        "even_then_odd": tuple(range(0,N,2))+tuple(range(1,N,2)),
        "odd_then_even": tuple(range(1,N,2))+tuple(range(0,N,2)),
    }
    for label,order in order_map.items():
        recoded={sum(((x>>original)&1)<<stream_pos
                     for stream_pos,original in enumerate(order)) for x in ys}
        assert len(recoded)==len(ys)
        z=per_cut_residuals(N,recoded)
        order_controls.append({"order":label,"positive":len(recoded),
                               "peak_width":z['peak_minimal_width'],
                               "states":z['sum_minimal_layer_widths'],
                               "transition_checks":z['prefix_transition_checks']})
    corpus={"name":"TMR2-SPARSE-RESIDUAL024", "status":"COMPUTATIONAL",
            "machine_model":"nonuniform ordered one-pass branching program, fixed gate basis",
            "circuit_basis":"AND,OR fanin2; NOT fanin1; unlimited fanout",
            "cases":outcomes,
            "fixed_order_controls":order_controls,
            "all_tests_passed":True,
            "total_terminal_inputs":sum(x['terminal_classifications_checked'] for x in outcomes)+N*0+4*(1<<N),
            "total_transition_checks":sum(x['prefix_transition_checks'] for x in outcomes)+sum(x['transition_checks'] for x in order_controls),
            "run_seconds":round(time.perf_counter()-started,6),
            "limitations":["not a uniform poly(s)-update streaming machine",
                "enumeration of gate descriptions is offline finite evidence",
                "no claim on search-MCSP with PH oracle gates",
                "no unconditional MCSP lower bound or P-versus-NP conclusion"]}
    corpus['code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    Path(a.output).write_text(json.dumps(corpus,indent=2)+'\n')
    print(json.dumps({"results":[{"n":v['n'],"s":v['threshold_s'],"YES":v['positive_count'],
                                   "width":v['peak_minimal_width'],"states":v['sum_minimal_layer_widths']} for v in outcomes],
                      "total_terminal_inputs":corpus['total_terminal_inputs'],
                      "total_transition_checks":corpus['total_transition_checks'],
                      "run_seconds":corpus['run_seconds'],"failed_assertions":0},indent=2))

if __name__=='__main__':main()
