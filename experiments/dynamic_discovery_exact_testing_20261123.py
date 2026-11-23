"""Exact finite test of forest prediction and uniform cotree sampling.

Python 3.10+. Rational arithmetic, exhaustive subsets, no Monte Carlo.
This tests the stated sampling rule, not the Adriaens--Apers tester.
"""
from fractions import Fraction
from itertools import combinations, product
import json


def balanced_words(q, edges):
    return {tuple(x[u]^x[v] for u,v in edges)
            for tail in product((0,1), repeat=q-1) for x in [(0,)+tail]}


def main():
    out = []
    total = 0
    for q in (4,5):
        edges = list(combinations(range(q),2))
        chords = [i for i,(u,v) in enumerate(edges) if u != 0]
        yes = balanced_words(q,edges)
        r = len(chords)
        tests = 0
        for word in yes:
            potentials = [0]+[word[edges.index((0,v))] for v in range(1,q)]
            prediction = tuple(potentials[u]^potentials[v] for u,v in edges)
            assert prediction == word
            for e in chords:
                neighbor = list(word)
                neighbor[e] ^= 1
                neighbor = tuple(neighbor)
                assert neighbor not in yes
                assert all(neighbor[i] == word[i] for i,(u,v) in enumerate(edges) if u == 0)
                for t in range(r+1):
                    samples = list(combinations(chords,t))
                    rejects = sum(any(neighbor[i] != prediction[i] for i in s) for s in samples)
                    assert Fraction(rejects,len(samples)) == Fraction(t,r)
                    # Sound three-valued wrapper: no sampled conflict is UNKNOWN unless all checked.
                    for s in samples:
                        conflict = any(neighbor[i] != prediction[i] for i in s)
                        result = 'UNSAT' if conflict else 'SAT' if t == r else 'UNKNOWN'
                        assert result != 'SAT'
                    tests += 1
        total += tests
        out.append(dict(q=q,k=len(edges),cotree=r,balanced_words=len(yes),
                        exact_sampling_comparisons=tests,
                        false_acceptance_by_sample_size=[str(1-Fraction(t,r)) for t in range(r+1)],
                        with_replacement_miss_after_r_draws=str(Fraction(r-1,r)**r),
                        two_sided_error_one_third_query_lower_bound=str(Fraction(r,3))))
    print(json.dumps(dict(cases=out,total_exact_sampling_comparisons=total,
                         rule='sample t cotree edges uniformly without replacement',
                         source_machine_timings='not measured in this normalized experiment'),indent=2))


if __name__ == '__main__':
    main()
