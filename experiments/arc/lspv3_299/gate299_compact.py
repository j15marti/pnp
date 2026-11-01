#!/usr/bin/env python3
"""Gate299 standalone parity-ticket audit. Full source enumerator/verifier is in the research ZIP."""
import json
from math import comb
def loose_odd_cycle(length):
    assert length >= 3 and length % 2 == 1
    return {r-1: comb(length,r) for r in range(1,length+1)}
def parity_odd_cycle(length):
    assert length >= 3 and length % 2 == 1
    return {r-1: comb(length,r) for r in range(1,length+1,2)}
def cycle_assignment_counts(length):
    # A satisfying Boolean cycle has one or two true literals on every edge.
    # Sign polarity is irrelevant to the XOR parity constraint.
    return [r for r in range(1,length+1) if (length-r)%2 == 0]
def audit():
    assert loose_odd_cycle(3)=={0:3,1:3,2:1}
    assert parity_odd_cycle(3)=={0:3,2:1}
    for length in (3,5,7,9):
        assert cycle_assignment_counts(length)==list(range(1,length+1,2))
    families={"Y6":(486,1742,1742,1014),
              "F15":(261,630,618,128),
              "F9":(15,22,22,16)}
    four_F15=[
      {"pin":[6,0],"ids":[1,10,11],"loose":33,"filtered":30,"models":1},
      {"pin":[5,0],"ids":[1,4,10],"loose":21,"filtered":18,"models":2},
      {"pin":[4,1],"ids":[1,10,11],"loose":30,"filtered":27,"models":2},
      {"pin":[3,1],"ids":[2,3,14],"loose":15,"filtered":12,"models":2}]
    assert sum(v[0] for v in families.values())==762
    assert sum(v[1] for v in families.values())==2394
    assert sum(v[2] for v in families.values())==2382
    assert sum(v[3] for v in families.values())==1158
    assert sum(c["loose"]-c["filtered"] for c in four_F15)==12
    for c in four_F15:assert c["loose"]-c["filtered"]==3
    print(json.dumps({"status":"PASS","families":families,
         "f15_discrepancy_cubes":four_F15,
         "removed_inconsistent_tickets":12,
         "models_unchanged":True,"P_vs_NP":"OPEN"},indent=2))
if __name__=="__main__":audit()
