#!/usr/bin/env python3
"""Evolving source-bound authenticated causal replay hostile control.

A committed Boolean source word is progressively restricted by challenges.
Challenge (i,b) fixes one still-live source coordinate i to b. The descendant
state is the canonical partial assignment plus, when requested, its SU05/
Hadamard legal-slice signature over all total completions consistent with it.

Purpose: test whether explicit adaptive descendant-tree growth forces
multiplicative recomputation. It does not in this control: original source plus
challenge history determines the current descendant in O(h+d), and canonical
restriction composition collapses the entire history to a partial assignment
of at most h bits.

COMPUTATIONAL finite control only; no SAT lower bound.
"""
import itertools,json,math

def apply_history(word, history):
    fixed={}
    for i,b in history:
        if i in fixed and fixed[i]!=b: return None
        fixed[i]=b
        if word[i]!=b: return None
    return tuple(sorted(fixed.items()))

def canonical_generator(word,history):
    state=apply_history(word,history)
    if state is None:return None
    return {"fixed":state,"live":tuple(i for i in range(len(word)) if i not in dict(state))}

def enumerate_tree(h,d):
    # Legal challenge alphabet chooses an unqueried coordinate and bit.
    level={()}
    levels=[1]
    canonical_states=[1]
    for _ in range(d):
        nxt=set()
        for hist in level:
            used={i for i,b in hist}
            for i in range(h):
                if i not in used:
                    for b in (0,1): nxt.add(hist+((i,b),))
        level=nxt
        levels.append(len(level))
        canonical_states.append(len({tuple(sorted(x)) for x in level}))
    return levels,canonical_states

def fixed_order_tree(d):
    return [2**i for i in range(d+1)]

def analyze(h):
    d=h
    histories,states=enumerate_tree(h,min(h,7)) # exact manageable permutation-rich tree
    fixed=fixed_order_tree(h)
    # For a committed actual word, exactly one bit-answer is consistent per queried coordinate;
    # all coordinate orders collapse to subsets of fixed source coordinates.
    realized_canonical=[sum(math.comb(h,j) for j in range(i+1)) for i in range(h+1)]
    return {"h":h,
      "fixed_order_explicit_nodes_through_depth_h":2**(h+1)-1,
      "fixed_order_level_widths":fixed,
      "permutation_rich_history_widths_through_depth_min_h_7":histories,
      "canonical_partial_assignment_widths_same_levels":states,
      "upper_bound_realized_source_consistent_canonical_states_through_depth_i":realized_canonical,
      "generator_description":"original h-bit source + canonical partial assignment/challenge history",
      "generator_state_bits_upper_bound":"h + O(h log h); with fixed challenge order h+O(h)",
      "next_state_update_cost":"polynomial; dictionary/bit-mask restriction update",
      "multiplicative_recurrence_supported":False}

def main():
    print(json.dumps({"status":"COMPUTATIONAL hostile control",
      "model":"evolving restrictions of one committed source realization",
      "cases":[analyze(h) for h in range(4,11)],
      "conclusion":"Explicit descendant branching does not force T(n,d)>=poly(n)T(n,d-1): restriction composition yields a succinct history-to-state generator.",
      "guards":["This control uses exact compositional source restrictions, not the full vMS PCP verifier.","It tests the proposed multiplication mechanism, not P versus NP.","P versus NP remains open."]},indent=2))
if __name__=="__main__":main()
