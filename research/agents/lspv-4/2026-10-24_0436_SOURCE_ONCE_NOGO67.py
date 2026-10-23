#!/usr/bin/env python3
"""Exhaust all Boolean relations on three selectors for source-once parsimony."""
truth_subsets=range(8)
valid=[]
checked=0
for relation in range(1<<8):
    counts=[]
    for truth_mask in truth_subsets:
        legal=sum(1 for sel in range(8)
                  if relation & (1<<sel) and (sel & ~truth_mask)==0)
        counts.append(legal)
        checked+=1
    if all(counts[t]==int(t!=0) for t in truth_subsets):
        valid.append(relation)
assert valid==[],valid
print({'source_once_relations_checked':256,'source_truth_sets':8,
       'total_pairs':checked,'parsimonious_relations':0})
