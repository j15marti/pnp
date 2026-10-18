#!/usr/bin/env python3
"""RESOURCE-GAUGE5: exact finite audits. Python stdlib only.

Tests GF(2) boundary identities, source-tailored constant-probe mixing,
shared gauge multi-block rank, and NP-complete fixed-path selector mapping.
No empirical complexity lower-bound inference is made.
"""
from __future__ import annotations
import itertools
import json
import hashlib
from pathlib import Path

OUT = Path(__file__).resolve().with_name('RESOURCE_GAUGE5_20261018_raw.json')

def parity(x: int) -> int:
    return x.bit_count() & 1

def rank_gf2(rows: list[int]) -> int:
    pivots = {}
    for row in rows:
        x = row
        while x:
            bit = x.bit_length() - 1
            if bit in pivots:
                x ^= pivots[bit]
            else:
                pivots[bit] = x
                break
    return len(pivots)

def edge_mask(u: int, v: int) -> int:
    return (1 << u) ^ (1 << v)

def cycle_edges(v: int) -> list[tuple[int,int]]:
    return [(i, (i+1)%v) for i in range(v)]

def run_gauge(v: int) -> dict:
    seeds = range(1 << v)
    blocks = [[((i+j)%v, (i+j+1)%v) for j in range(v-1)] for i in range(v)]
    ranks = [rank_gf2([edge_mask(*e) for e in B]) for B in blocks]
    all_rows = [edge_mask(*e) for B in blocks for e in B]
    joint_rank = rank_gf2(all_rows)
    assert all(r == v-1 for r in ranks) and joint_rank == v-1
    assert len(set(tuple(B) for B in blocks)) == v
    checks = 0
    nonlinear_checks = 0
    for z in seeds:
        gauge = [0]+[parity(z & edge_mask(0,j)) for j in range(1,v)]
        for B in blocks:
            for u,w in B:
                direct = ((z >> u)&1) ^ ((z >> w)&1)
                assert direct == (gauge[u] ^ gauge[w]); checks += 1
                a, b = (z>>u)&1,(z>>w)&1
                raw=[(z>>j)&1 for j in range(v)]
                for f in (lambda x,y:x&y, lambda x,y:x|y,
                          lambda x,y:1^(x^y), lambda x,y:(x&y)^x):
                    # Raw latent-vertex table (v bits), not gauge (v-1 bits),
                    # answers arbitrary public nonlinear pairwise functions.
                    assert f(a,b) == f(raw[u],raw[w])
                    nonlinear_checks += 1
        star = [((z >> 0)&1)^((z>>i)&1) for i in range(1,v)]
        m = v-1
        path = [star[j]^star[j+1] for j in range(m-1)] + [star[-1]]
        rebuilt_star = [sum(path[j:])%2 for j in range(m)]
        assert star == rebuilt_star
        assert path == [((z>>(j+1))&1)^((z>>(j+2))&1) for j in range(m-1)] + [((z>>0)&1)^((z>>(v-1))&1)]
        prefix_path = [((z>>j)&1)^((z>>(j+1))&1) for j in range(v-1)]
        prefix_y=[]; a=0
        for x in prefix_path:
            a ^= x
            prefix_y.append(a)
        assert prefix_y == star
    # All shifted path blocks jointly define one elementary linear code.
    # Membership and witness lifting use only graph parity propagation.
    def on_image(outputs):
        assigned={0:0}
        adj=[[] for _ in range(v)]
        for (u,w),bit in outputs:
            adj[u].append((w,bit));adj[w].append((u,bit))
        stack=[0]
        while stack:
            u=stack.pop()
            for w,bit in adj[u]:
                val=assigned[u]^bit
                if w in assigned:
                    if assigned[w]!=val: return False
                else:
                    assigned[w]=val;stack.append(w)
        return len(assigned)==v
    membership_yes=0
    mutation_no=0
    for z in seeds:
        outputs=[((u,w), ((z>>u)&1)^((z>>w)&1)) for B in blocks for u,w in B]
        assert on_image(outputs)
        membership_yes+=1
        for j in range(len(outputs)):
            edited=outputs.copy()
            (e,b)=edited[j]; edited[j]=(e,b^1)
            assert not on_image(edited)
            mutation_no+=1
    # The two globally complemented raw seeds have identical gauge but
    # different AND values, showing why nonlinear outputs need a raw bit.
    raw_zero=[0]*v; raw_one=[1]*v
    assert all(raw_zero[u]^raw_zero[0] == raw_one[u]^raw_one[0] for u in range(v))
    assert (raw_zero[0]&raw_zero[1]) != (raw_one[0]&raw_one[1])
    edges = cycle_edges(v)
    boundary_checks=0
    allowed_dense=0
    max_mix_len=0
    for F in range(1<<len(edges)):
        boundary=0
        for i,(u,w) in enumerate(edges):
            if (F>>i)&1:
                boundary ^= edge_mask(u,w)
        assert boundary.bit_count()%2==0
        for z in seeds:
            original=0
            for i,(u,w) in enumerate(edges):
                if (F>>i)&1:
                    original ^= ((z>>u)&1)^((z>>w)&1)
            assert original == parity(boundary&z)
            boundary_checks += 1
        if boundary.bit_count()<=2 and F.bit_count()>=2:
            allowed_dense+=1
            max_mix_len=max(max_mix_len,F.bit_count())
    return {
        'vertices':v, 'blocks':v, 'block_length':v-1,
        'single_block_ranks':ranks, 'sum_block_ranks':sum(ranks),
        'joint_rank':joint_rank, 'rank_deficit':sum(ranks)-joint_rank,
        'global_gauge_cells':v-1, 'max_probes_per_edge':2,
        'seeds_exhausted':1<<v, 'xor_edge_assertions':checks,
        'nonlinear_pairwise_controls':nonlinear_checks,
        'cycle_subsets_enumerated':1<<v, 'boundary_assertions':boundary_checks,
        'long_source_tailored_two_local_mixes':allowed_dense,
        'max_mixed_edges_at_locality_two':max_mix_len,
        'star_to_path_inverse_max_output_queries':v-1,
        'global_raw_cells_for_nonlinear_pairwise_outputs':v,
        'affine_image_membership_yes_controls':membership_yes,
        'one_bit_mutations_off_image':mutation_no,
        'and_not_gauge_invariant_control':True,
    }

def run_clique_path(v: int) -> dict:
    pairs=list(itertools.combinations(range(v),2))
    all_c = {k:list(itertools.combinations(range(v),k)) for k in range(2,v+1)}
    checks=0
    yes_counts={k:0 for k in all_c}
    for graph_bits in range(1<<len(pairs)):
        E={pairs[i] for i in range(len(pairs)) if (graph_bits>>i)&1}
        for k,Cset in all_c.items():
            target=k*(k-1)//2
            # The selection problem asks for <=k cells whose actual paths
            # wholly contained in C include >=target distinct 2-probe edges.
            success=any(sum((u in C and w in C) for u,w in E)>=target for C in Cset)
            # A set on exactly k vertices has all choose(k,2) edges iff clique.
            clique=any(all(tuple(sorted((u,w))) in E for u,w in itertools.combinations(C,2)) for C in Cset)
            assert success == clique
            checks+=1
            yes_counts[k]+=int(success)
    return {'vertices':v, 'graphs_exhausted':1<<len(pairs),
            'fixed_two_probe_selector_assertions':checks,
            'clique_iff_selector_yes_by_size':yes_counts}

def main():
    result={'report':'RESOURCE-GAUGE5', 'date':'2026-10-18',
            'status':'COMPUTATIONAL verification; exact proof separate',
            'model':'fixed public bit-probe table; GF2 graph-edge outputs and frozen replay-path selector',
            'gauge_controls':[run_gauge(6),run_gauge(8)],
            'clique_controls':[run_clique_path(5),run_clique_path(6)],
            'limitations':['finite exact identities do not imply machine lower bounds',
                           'clique hardness is for frozen path replay selection, not optimal semantic decoding',
                           'KPI remote points may lie outside any graphic affine generator image',
                           'no time/space reduction or P vs NP separation established']}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    digest=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(json.dumps({'code_sha256':digest,'output':str(OUT),'result':result},indent=2))

if __name__=='__main__': main()
