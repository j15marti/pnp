#!/usr/bin/env python3
"""REDTEAM19: fixed-terminal full-table trajectories and compact witness controls.
Reproduces exact combinatorial controls; no succinct-transition lower bound.
"""
from itertools import permutations
from math import log2, factorial
import json

def path_census(t):
    seen = set()
    steps = 0
    for middle in permutations(range(1, t)):
        seq = (0,) + middle + (t,)
        f = list(range(t + 1))
        for a, b in zip(seq, seq[1:]):
            f[a] = b
        v, generated = 0, [0]
        for _ in range(t):
            v = f[v]
            generated.append(v)
            steps += 1
        assert tuple(generated) == seq and generated[-1] == t
        seen.add(seq)
    assert len(seen) == factorial(t - 1)
    return dict(t=t, paths=len(seen), endpoint=t, transition_checks=steps)

def log_circuits(s, k):
    return log2(s + 1) + 4*s + (2*s + k)*log2(s + k + 2)

def bound(t):
    k = (t + 1 - 1).bit_length() if (t + 1) & t == 0 else (t + 1).bit_length()
    # k is ceil(log2(t+1)); use bit_length(t), exactly.
    k = t.bit_length()
    target = sum(log2(i) for i in range(2, t))
    valid = [s for s in range(t + 1) if log_circuits(s, k) < target]
    return dict(t=t, k=k, log2_paths=target, excluded_max_s=max(valid),
                hard_path_gate_lower_bound=max(valid)+1)

def diagonal(n, s=2):
    N = 1 << n
    mask = (1 << N)-1
    variables = [sum(((x >> i) & 1) << x for x in range(N))
                 for i in range(n)] + [0, mask]
    signals = set(variables)
    prefixes = [variables]
    candidates = len(variables)
    for _ in range(s):
        new = []
        for ws in prefixes:
            for a in ws:
                for b in ws:
                    signal = (~(a & b)) & mask
                    new.append(ws + [signal])
                    signals.add(signal)
                    candidates += 1
        prefixes = new
    least = next(i for i in range(1 << N) if i not in signals)
    assert least not in signals
    return dict(n=n, s=s, distinct_tables=len(signals),
                netlist_signal_checks=candidates, lex_first_missing=least)

def controls():
    cases = [path_census(t) for t in range(3,9)]
    bounds = [bound(t) for t in (16,32,64,128,256,512,1024,2048,4096)]
    for m in (5,17,65):
        for t in (0,1,2,17,100,1000):
            x = 0
            for _ in range(t):
                x = (x + 1) % m
            assert x == t % m
    local = [(lambda a,b:a==0),
             (lambda a,b:b==1-a),
             (lambda a,b:b==0)]
    assert all(any(p(a,b) for a in (0,1) for b in (0,1)) for p in local)
    assert not any(all(p(a,b) for p in local) for a in (0,1) for b in (0,1))
    return dict(run="REDTEAM_FIXED_ENDPOINT_SHARED_WITNESS19",
                status="PASS",paths=cases,counting_bounds=bounds,
                diagonal_controls=[diagonal(n) for n in (2,3,4)],
                exact_transition_checks=sum(c["transition_checks"] for c in cases),
                increment_controls=18,quantifier_controls=3,
                unexpected_failures=0,p_vs_np="OPEN")

if __name__ == "__main__":
    print(json.dumps(controls(),indent=2))
