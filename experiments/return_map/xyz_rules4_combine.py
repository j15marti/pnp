from dataclasses import dataclass
from typing import FrozenSet, Tuple
import itertools, math, json

@dataclass(frozen=True)
class ExtState:
    X: FrozenSet[str]
    Y: FrozenSet[Tuple[int,...]]
    Z: FrozenSet[str]
    R: str
    C: FrozenSet[str]
    Q: FrozenSet[str]
    D: FrozenSet[str]
    G: str
    answer: str = 'UNKNOWN'

def classify_transition(a,b):
    detail_preserved = (a.Y == b.Y and a.Z <= b.Z) or (len(b.Y) >= len(a.Y) and a.Z <= b.Z)
    certified = bool(b.C - a.C)
    reacquired = bool(b.Q - a.Q)
    combined = b.G != a.G and b.G != 'NONE'
    lost_detail = (b.Y != a.Y) or not (a.Z <= b.Z)
    labels=[]
    if detail_preserved: labels.append('PRESERVE')
    if certified: labels.append('CERTIFY')
    if reacquired: labels.append('REACQUIRE')
    if combined: labels.append('COMBINE')
    if lost_detail and not labels: labels.append('UNACCOUNTED')
    return labels

def binary_combine_cost(m):
    return max(0,m-1), 1 if m else 0

def balanced_depth(m):
    return 0 if m <= 1 else math.ceil(math.log2(m))

if __name__ == '__main__':
    rows=[]
    for m in [1,2,4,8,16,32,64,128,256,1024]:
        gates,out=binary_combine_cost(m)
        rows.append({'live_obligations':m,'fan_in_2_gates':gates,'balanced_depth':balanced_depth(m),'final_summary_bits':out,'count_potential_drop':max(0,m-out),'drop_per_gate':0 if gates==0 else (m-out)/gates})
    print(json.dumps(rows,indent=2))
