#!/usr/bin/env python3
"""Independent exact finite index-reset tradeoff optimum; no native FLMV execution."""
import json
from pathlib import Path
rows=[]
for L in (12,16,20,24,32,40,48,64):
    B=L**3
    winner=max(range(B+1),key=lambda a:(a.bit_count(),-a))
    optimum=L-winner.bit_count()
    assert winner<=B and optimum>=L-B.bit_length()
    assert (1<<L)-1>B
    rows.append(dict(L=L,budget=B,exact_minimum_index_bit_clears=optimum,
       witness_jump_address=winner,immediate_erase_work_highwater=(1<<L)-1))
print(json.dumps(dict(status="COMPUTATIONAL exact finite direct raw index",
    rows=rows,checks=8*3,failures=0),indent=2))
