#!/usr/bin/env python3
"""ARC220 independent integer-mask pivot elimination exhaustive control."""
import json
from pathlib import Path
counts={}
for t in range(1,5):
    cnt=0
    for word in range(1<<(4*t)):
        A=[bool((word>>(2*i))&3) for i in range(t)]
        B=[bool((word>>(2*t+2*j))&3) for j in range(t)]
        proj=all(A) or all(B)
        expanded=all(a or b for a in A for b in B)
        assert proj==expanded,(t,word)
        cnt+=1
    counts[str(t)]=cnt
assert sum(counts.values())==69904
record={"counts":counts,"total":sum(counts.values()),"status":"PASS"}
Path(__file__).with_suffix('.json').write_text(json.dumps(record,sort_keys=True,indent=2)+"\n")
print(json.dumps(record,sort_keys=True))
