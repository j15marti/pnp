"""Selected-checkpoint error-mass audit, Python 3.10+, exact enumeration.
This checks a normalized randomized wrapper on the pinned diamond source family.
It does not execute a uniform native one-tape parser or count physical runtime.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
from dynamic_accounting_forest_prediction_20261123 import prepare
from dynamic_accounting_signed_cycle_20261123 import source_oracle

def main():
    q = 4
    edges, tree, encode, base, sites, stop, dims = prepare(q)
    chords = sorted(set(range(len(edges))) - tree)
    yes = source_oracle(q, edges)
    r = len(chords)
    sources = {word: encode(word) for word in range(1 << len(edges))}
    pairs = 0
    for word in yes:
        for e in chords:
            other = word ^ (1 << e)
            assert other not in yes
            diffs = {i for i,(a,b) in enumerate(zip(sources[word],sources[other])) if a!=b}
            assert diffs == {i for i,(owner,_) in sites.items() if owner == e}
            assert min(diffs) >= stop
            pairs += 1
    rows = []
    runs = 0
    eta = F(1,8)
    for g in range(1,17):
        guesses = min(g,4)
        no_count = (guesses+1)//2
        yes_count = guesses//2
        assert max(no_count, yes_count) <= 2
        failures = {}
        for word in sources:
            truth = word in yes
            err = 0
            for coin in range(16):
                # Four charged fair bits choose a fixed finite branch.
                if coin < no_count:
                    answer, acquired = False, 0
                elif coin < no_count+yes_count:
                    answer, acquired = True, 0
                else:
                    # This normalized exact branch reads every chord.
                    # In a native implementation the full guard/parser is paid too.
                    answer, acquired = truth, r
                err += answer != truth
                runs += 1
            failures[word] = F(err,16)
        assert max(failures.values()) <= eta
        p = F(g,16)
        gated_hits = F(max(g-4,0)*r,16)
        bound = r*max(F(0),p-2*eta)
        assert gated_hits == bound
        for word in yes:
            e0 = F(no_count,16)
            for e in chords:
                e1 = F(yes_count,16)
                assert gated_hits >= r*max(F(0),p-e0-e1)
                if g == 4:
                    assert e0/p == e1/p == F(1,2)
                    assert gated_hits == 0
        rows.append(dict(gate_probability=str(p),global_error_cap=str(eta),
                         actual_max_error=str(max(failures.values())),
                         conditional_balanced_error=str(F(no_count,g)),
                         conditional_neighbor_error=str(F(yes_count,g)),
                         gated_expected_support_hits=str(gated_hits),
                         conditional_expected_support_hits=str(gated_hits/p),
                         corrected_unconditional_bound=str(bound)))
    deps = {}
    for name in ("dynamic_accounting_forest_prediction_20261123.py",
                 "dynamic_accounting_signed_cycle_20261123.py"):
        deps[name] = hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
    print(json.dumps(dict(q=q,n=dims[0],m=dims[1],N=len(base),r=r,
                         sources=len(sources),balanced=len(yes),opposite_pairs=pairs,
                         exhaustive_coin_source_gate_runs=runs,rows=rows,
                         dependency_sha256=deps,
                         limitation="Normalized branch/event audit; no native timing or kernel build"),
                     indent=2))
if __name__ == "__main__":
    main()

