#!/usr/bin/env python3
"""Exact six-variable regular monotone 3-SAT q=3 fixed-four-color control; no third-party packages."""
import itertools,json,hashlib,sys
from collections import Counter
T=tuple(itertools.combinations(range(6),3))
H=tuple(tuple(E) for E in itertools.combinations(T,4) if all(sum(v in e for e in E)==2 for v in range(6)))
PARTS=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))
COLORS=list(itertools.product(range(4),repeat=6))
BITS=list(itertools.product(range(2),repeat=6))
assert len(H)==75
records=[];histo=Counter();q3_fail=0;q3_success=0;countq3=0;first_fail=None;countnae0=0; allnae0=0
for P in H:
    E={(u,v) for e in P for u,v in itertools.combinations(e,2)}
    valid_colors=[c for c in COLORS if c[0]==0 and all(c[u]!=c[v] for u,v in E)]
    assert valid_colors
    c=min(valid_colors)
    for Q in H:
        q=4-len(set(P)&set(Q));histo[q]+=1
        sat=[b for b in BITS if all(any(b[v] for v in e) for e in P) and all(any(1-b[v] for v in e) for e in Q)]
        nae=[b for b in BITS if all(0<sum(b[v] for v in e)<3 for e in set(P)|set(Q))]
        if not nae: allnae0+=1
        if q==3:
            countq3+=1
            forbidden=[]
            for i,part in enumerate(PARTS):
                sides={v:j for j,grp in enumerate(part) for v in grp}
                failed=tuple(e for e in Q if len({sides[c[v]] for v in e})==1)
                forbidden.append(failed)
            failed=all(forbidden)
            if failed:
                q3_fail+=1
                if first_fail is None:
                    first_fail={'P':[[v+1 for v in e] for e in P], 'Q':[[v+1 for v in e] for e in Q], 'color0to3':list(c), 'blocked':[[[v+1 for v in e] for e in bad] for bad in forbidden], 'sat_model_count':len(sat),'nae_model_count':len(nae),'sat_witness': ''.join(str(v) for v in sat[0]),'nae_witness':''.join(str(v) for v in nae[0])}
            else: q3_success+=1
            if not nae:countnae0+=1
assert q3_fail+q3_success==1680
assert not countnae0 and not allnae0
assert first_fail is not None
# Infinite target family: core followed by h disjoint fully paired components.
def lifted(h):
    # Use the precise counterexample rather than H[0].
    cp=tuple(tuple(e) for e in first_fail['P'])
    cq=tuple(tuple(e) for e in first_fail['Q'])
    pp=list(cp);qq=list(cq)
    for j in range(1,h+1):
        pp.extend(tuple(v+6*j for v in e) for e in cp)
        qq.extend(tuple(v+6*j for v in e) for e in cp)
    k=6*(h+1);m=8*(h+1)
    assert len(pp)==len(qq)==4*(h+1)
    assert len(set(pp))==len(pp) and len(set(qq))==len(qq)
    assert all(sum(v in e for e in pp)==2 and sum(v in e for e in qq)==2 for v in range(1,k+1))
    assert len(set(pp)-set(qq))==3
    witness=tuple([0,0,1,1,1,0]*(h+1))
    assert all(0<sum(witness[v-1] for v in e)<3 for e in set(pp)|set(qq))
    # Explicit bad four-coloring, repeated per component, remains proper for P.
    col=tuple([0,1,2,2,0,1]*(h+1))
    assert all(len({col[v-1] for v in e})==3 for e in pp)
    for part in PARTS:
        side={v:i for i,a in enumerate(part) for v in a}
        assert any(len({side[col[v-1]] for v in e})==1 for e in qq)
    w=(k+1).bit_length()-1 if 2**((k+1).bit_length()-1)==k+1 else (k+1).bit_length()
    N=3*w+2+3*m*(w+1)
    return {'h':h,'k':k,'m':m,'N_dense_example':N,'q':3,'witness_repeated_001110':True,'all_three_partitions_fail_for_displayed_four_coloring':True}
lift_checks=[lifted(h) for h in range(6)]
out={'run':'M22-Q3-PALETTE-FIREWALL144','status':'COMPUTATIONAL exact exhaustive k=6', 'code_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest(), '6var_positive_support_families':len(H),'ordered_PQ_pairs':len(H)**2,'q_histogram':dict(sorted(histo.items())), 'q3_instances':countq3,'q3_first_lex_color_no_partition':q3_fail,'q3_first_lex_color_partition_success':q3_success,'q3_no_NAE_witness':countnae0,'all_5625_no_NAE_witness':allnae0, 'counterexample':first_fail,'lift_controls':lift_checks,'interpretation':'A particular legitimate four-coloring can fail to coarsen under all three pair partitions, though another coloring/NAE solution exists; not SAT-hardness.'}
print(json.dumps(out,indent=2,sort_keys=True))
