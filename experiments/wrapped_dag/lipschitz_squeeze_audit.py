#!/usr/bin/env python3
import json, math
gamma=2*math.cos(math.pi/7)
rows=[]
for m in [4,8,12,16,24,32,40]:
    N=2**m
    rows.append({
      "m":m,
      "truth_table_length":N,
      "raw_semantic_mass":N,
      "one_XOR_gate_raw_mass_change":N//2,
      "raw_B_over_L":2.0,
      "log_mass_total":m,
      "one_XOR_gate_log_mass_change":max(1,m-1),
      "parity_fanin2_XOR_gate_count":max(0,m-1),
      "generic_truth_table_counting_lb_approx":N/max(1,m)
    })
print(json.dumps({"gamma":gamma,"rows":rows},indent=2))
