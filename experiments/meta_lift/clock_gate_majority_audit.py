#!/usr/bin/env python3
"""CLOCKGATE-MAJORITY1 finite audits. Python stdlib only; no random seeds."""
import itertools
import json

def majority(a, b, c):
    return tuple(int(x + y + z >= 2) for x, y, z in zip(a, b, c))

def onehot(j):
    return tuple(int(k == j) for k in range(3))

def closed_under_majority(points):
    s = set(points)
    return all(majority(a, b, c) in s
               for a in s for b in s for c in s)

def component_count(m):
    w = [tuple(v for symbol in letters for v in onehot(symbol))
         for letters in itertools.product(range(3), repeat=m)]
    count_closed = 0
    max_card = 0
    number_at_max = 0
    for mask in range(1 << len(w)):
        subset = [w[i] for i in range(len(w)) if mask & (1 << i)]
        if closed_under_majority(subset):
            count_closed += 1
            if len(subset) > max_card:
                max_card, number_at_max = len(subset), 1
            elif len(subset) == max_card:
                number_at_max += 1
    assert max_card == 2**m
    return {
        "onehot_universe": 3**m,
        "subsets_exhaustively_checked": 1 << (3**m),
        "majority_closed_subsets": count_closed,
        "largest_majority_closed_subset": max_card,
        "maximal_subsets_count": number_at_max,
        "proved_theorem_control": 2**m
    }

def clause_masks(assignments):
    n = len(assignments[0])
    masks = []
    for i in range(n):
        for b in (0, 1):
            masks.append(sum(1<<j for j,v in enumerate(assignments)
                             if v[i] == b))
    for i in range(n):
        for k in range(i+1, n):
            for a in (0, 1):
                for b in (0, 1):
                    masks.append(sum(1<<j for j,v in enumerate(assignments)
                                     if v[i] == a or v[k] == b))
    return masks

def is_2cnf_relation(mask, clause_masks_, universe_mask):
    closure = universe_mask
    for clause in clause_masks_:
        if mask & ~clause == 0:
            closure &= clause
    return closure == mask

def relation_equivalence():
    a = list(itertools.product((0,1), repeat=3))
    masks = clause_masks(a)
    count_majority = count_2cnf = 0
    for relation in range(1 << 8):
        points = [a[i] for i in range(8) if relation & (1<<i)]
        majority_yes = closed_under_majority(points)
        cnf_yes = is_2cnf_relation(relation, masks, 255)
        assert majority_yes == cnf_yes
        count_majority += majority_yes
        count_2cnf += cnf_yes
    return {
        "relations_checked": 256,
        "majority_closed": count_majority,
        "2cnf_definable": count_2cnf,
        "disagreements": 0
    }

def adaptive_two_probe():
    a = list(itertools.product((0,1), repeat=3))
    masks = clause_masks(a)
    checked = 0
    relations = set()
    for leaves in itertools.product((0,1), repeat=4):
        for value in (0,1):
            mask = 0
            for i,(root,left,right) in enumerate(a):
                branch_bit = left if root == 0 else right
                observed = leaves[2*root + branch_bit]
                if observed == value:
                    mask |= (1<<i)
            assert is_2cnf_relation(mask, masks, 255)
            checked += 1
            relations.add(mask)
    return {
        "leaf_patterns":16,
        "target_bit_values":2,
        "tests":checked,
        "distinct_preimage_relations":len(relations),
        "failures":0
    }

def main():
    results={
      "report":"CLOCKGATE-MAJORITY1",
      "date":"2026-10-18",
      "model":"Boolean adaptive two-probe equality, coordinate projection",
      "three_variable_relation_control":relation_equivalence(),
      "adaptive_two_probe_preimages":adaptive_two_probe(),
      "disjoint_onehot_product":{str(m):component_count(m) for m in (1,2)},
      "status":"COMPUTATIONAL finite controls; proof is symbolic and separately recorded",
      "limits":"No SAT lower bound or completeness follows from these finite checks."
    }
    print(json.dumps(results, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
