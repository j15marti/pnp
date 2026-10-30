#!/usr/bin/env python3
"""Standalone GitHub checker for LSPV-2 SIGNED-AUGMENTING-FLIPS242.
Checks every coherent assignment for all 64 signed K4 and all 512 signed K3,3
sources. Full first-generation RUP, indexed flip traces, fallback DPLL and
2.2MB raw records are in Library libfile_924eecce1e408191b786d777dae163b9.
This independent checker does not import the full run's solver.
"""
import json

def run(k):
    if k == 4:
        edges = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
        r = 4
    elif k == 6:
        edges = [(i,3+j) for i in range(3) for j in range(3)]
        r = 6
    else:
        raise ValueError(k)
    n = len(edges)
    witness_counts = []
    for sign in range(1 << n):
        first = []
        for clause_index in range(r):
            literals = []
            for original_var_index, (p,q) in enumerate(edges):
                v = original_var_index + 1
                if p == clause_index:
                    literals.append(v)
                elif q == clause_index:
                    literals.append(-v if sign >> original_var_index & 1 else v)
            assert len(literals) == 3
            first.append(literals)
        F = first + [[-x for x in clause] for clause in first]
        assert all(len({abs(x) for x in clause}) == 3 for clause in F)
        for i in range(1,n+1):
            assert sum(x == i for c in F for x in c) == 2
            assert sum(x == -i for c in F for x in c) == 2
        models = 0
        for a in range(1 << n):
            sat = all(any(
                (bool((a >> (abs(l)-1)) & 1) if l > 0
                    else not bool((a >> (abs(l)-1)) & 1))
                for l in clause) for clause in F)
            models += int(sat)
        assert models > 0, ("counterexample",k,sign)
        witness_counts.append(models)
    return dict(base_clauses=r,variables=n,
                signings=len(witness_counts),
                minimum_witnesses=min(witness_counts),
                maximum_witnesses=max(witness_counts),
                mean_witnesses=sum(witness_counts)/len(witness_counts))

if __name__ == "__main__":
    print(json.dumps([run(4),run(6)],indent=2))
