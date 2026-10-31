#!/usr/bin/env python3
"""Exact abstract-work-tape counterexample; no SAT-complexity lower bound."""
import json,math
from pathlib import Path
p=Path(__file__).resolve().parent
out=[]
for N in (16,32,64,128,256,512,1024):
 # Policy H takes N semantic source reads and log N writable bits on a promise
 # input; policy X emits one dummy work-tape cell per step and never certifies.
 # Restart scheduler executes X first in every 2^j budget round.
 J=math.ceil(math.log2(N));live=0;charged=0
 for j in range(J+1):
  budget=2**j
  # X exceeds this budget by one attempted step and writes one cell each step.
  charged+=budget+1;live=max(live,budget+1)
  # H either consumes budget+1 and restarts, or returns certified YES at step N.
  charged+=N if budget>=N else budget+1
  if budget>=N:break
 cap=int(N**0.5)
 # A simulated hard cap would kill X after cap+1 allocated bits in each round,
 # retaining low space but still charging its unsuccessful attempts.
 capped_peak=min(live,cap+1)
 out.append({'source_length_parameter':N,'fast_complete_steps':N,'fast_live_bits':J+1,'loser_peak_bits':live,'race_total_semantic_steps':charged,'ratio_loser_to_fast_memory':round(live/(J+1),3),'restricted_space_cap':cap,'capped_peak_bits':capped_peak,'all_input_FLVM_claim':False})
(p/'space275.json').write_text(json.dumps({'status':'PROVED/EXACT abstract trace','cases':out,'warning':'A synthetic two-policy tape model; does not lower-bound arbitrary SAT decisions or implement a native FLMV machine.'},indent=2))
print(json.dumps(out,indent=2))
