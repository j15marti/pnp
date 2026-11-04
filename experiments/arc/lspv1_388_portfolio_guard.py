#!/usr/bin/env python3
"""Finite toy control only, not a Blum-speedup construction or SAT theorem.
Canonical binary words: 0 or 1[01]*. Empty or leading-zero longer words are malformed.
Toy label is popcount parity; all four implementations always return correct labels.
"""
import json

def label(x):
    if not x or (x[0] == "0" and x != "0"):
        return "M"
    return "SAT" if x.count("1") % 2 == 0 else "UNSAT"

def times(x):
    n = len(x)
    if label(x) == "M":
        return [3+n, 2+n*n, 4+n, 2]
    return [2**(n+5), 2**(2*n+2), 2**(n+6)+n, n+2]

def main():
    cases = [""] + [format(i, "0%db" % n)
                        for n in range(1,9) for i in range(2**n)]
    assert len(cases) == 511
    totals = {lab: sum(label(x) == lab for x in cases)
              for lab in ("SAT", "UNSAT", "M")}
    rows = []
    checks = 0
    for N in range(1,9):
        sub = [x for x in cases if len(x) <= N]
        worst = [max(times(x)[i] for x in sub) for i in range(4)]
        for x in sub:
            lab = label(x)
            ts = times(x)
            assert lab in ("SAT","UNSAT","M")
            assert all(t >= 1 for t in ts)
            assert ts[3] <= min(ts[:3]) or lab == "M"
            checks += 3
        assert worst[3] < min(worst[:3])
        rows.append({"N":N,"all_binary_count":len(sub),"worst":worst,
                     "strict_toy_improvement":True})
    assert totals == {"SAT":128,"UNSAT":128,"M":255}
    out = {"status":"COMPUTATIONAL synthetic controls only",
           "claim":"all-binary max-quantifier toy, NOT Blum f",
           "input_grammar":"valid 0 or 1[01]*; other strings malformed",
           "total_test_strings":511,"assertions":checks+10,
           "both_labels":totals,"rows":rows}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__ == "__main__":
    main()
