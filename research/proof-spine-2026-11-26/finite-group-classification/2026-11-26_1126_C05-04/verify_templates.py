# Standalone independent finite occupancy check for the certificate table.
import json
from itertools import combinations
from pathlib import Path
def masks(T):
    ports=[(0,0),(0,1),(1,0),(1,1)]
    private={(0,2),(1,2),(2,0),(2,1)}
    out=set()
    for a,b in combinations(T,2):
        rows=[(c,x) for t in (a,b) for c,x in enumerate(t)]
        if len(set(rows))==6 and private<=set(rows):
            out.add(sum(1<<i for i,p in enumerate(ports) if p in rows))
    return sorted(out)
data=json.loads(Path(__file__).with_name("templates.json").read_text())
assert len(data)==15 and len({tuple(d["support"]) for d in data})==15
for d in data:
    assert masks(d["tuples"])==d["support"]
print("15 exact support checks passed")
