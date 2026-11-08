#!/usr/bin/env python3
"""LSPV-1/493 deterministic exhaustive greedy affine cover producer.
Source domain: g disjoint AND outputs on 2*g original Boolean inputs.
No assertion that this is a legal historical R_mix341 proof generator.
"""
import json, math, time, sys

def phi(k, u, v):
    return (0, u, v, 1 ^ u ^ v)[k]

def agrees(g, code, x):
    for j in range(g):
        u, v = (x >> (2*j)) & 1, (x >> (2*j+1)) & 1
        if phi((code >> (2*j)) & 3, u, v) != (u & v):
            return False
    return True

def cover(g):
    n = 4**g
    masks = []
    for code in range(n):
        mask = 0
        for x in range(n):
            if agrees(g, code, x):
                mask |= 1 << x
        assert mask.bit_count() == 3**g
        masks.append(mask)
    uncovered = (1 << n) - 1
    picks = []
    while uncovered:
        code = max(range(n), key=lambda j: (uncovered & masks[j]).bit_count())
        gain = (uncovered & masks[code]).bit_count()
        count = uncovered.bit_count()
        assert gain * n >= count * (3**g), "greedy average bound"
        assert gain > 0
        uncovered &= ~masks[code]
        picks.append(code)
    assert len(picks) <= math.ceil((4/3)**g * (g*math.log(4)+1))
    assert all(any(agrees(g, code, x) for code in picks) for x in range(n))
    return dict(g=g,input_assignments=n,templates_total=n,agree_per_template=3**g,
                fourier_lower_bound=math.ceil((4/3)**g),greedy_K=len(picks),
                greedy_indices=picks,greedy_overlap_check="PASS",
                templates_examined=len(picks)*n)

def k4models(charges):
    edges=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    return sum(all((sum((x>>i)&1 for i,e in enumerate(edges) if v in e) & 1)
                   == charges[v] for v in range(4)) for x in range(64))

def main():
    data=[]
    for g in range(1,7):
        t=time.monotonic()
        row=cover(g)
        row["real_time_seconds"]=round(time.monotonic()-t,4)
        print(f"g={g}: {row['greedy_K']} chosen templates",flush=True)
        data.append(row)
    ids=[sum(t<<(2*j) for j in range(3)) for t in range(4)]
    assert ids==[0,21,42,63]
    assert all(any(agrees(3,code,x) for code in ids) for x in range(64))
    assert k4models([1,0,0,0])==0 and k4models([0,0,0,0])==8
    out=dict(result_id="LSPV-1/493",status="PROVED/RESTRICTED symbolic; COMPUTATIONAL finite",
             method="deterministic exhaustive-greedy over 4^g local affine predictors",
             rows=data,g3_explicit_certificate=ids,g3_exact_separable_minimum=4,
             local_affine_falsifier_count=8,source_controls={"odd_K4_models":0,"even_K4_models":8},
             limitation="semantic nonaffine agreement regions, not historical R_mix341 proof")
    path=sys.argv[1] if len(sys.argv)>1 else "lspv1_493_affine_template_raw.json"
    with open(path,'w',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({"g_values":[r["g"] for r in data],
                      "K_values":[r["greedy_K"] for r in data]},indent=2))
if __name__=="__main__":
    main()
