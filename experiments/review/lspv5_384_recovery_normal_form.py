#!/usr/bin/env python3
"""REFEREE384: exact work/span inside the guarded-Tseitin recovery normal form.

This is deliberately narrower than a global R_mix341 optimum.  It audits the
already published REFEREE383 construction as an AND/OR shared dependency DAG
and proves exact cost only for the declared block-respecting recovery normal
form.  A bounded exhaustive Resolution search independently checks every
canonical local recovery gadget.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "results/raw/review/2026-11-06_0248_LSPV5_ORIGINAL_COORDINATE_RECOVERY383.json"
OUT = ROOT / "results/raw/review/2026-11-06_0348_LSPV5_RECOVERY_NORMAL_FORM384.json"
INPUT_SHA = "524f65bf4f033000ccaa675e14c870654eb758621d26cdb282f95b604b93df7b"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def norm(clause):
    c = frozenset(int(x) for x in clause)
    if any(-x in c for x in c):
        return None
    return c


def resolvents(left, right):
    out = set()
    for pivot in left:
        if -pivot not in right:
            continue
        c = norm((left - {pivot}) | (right - {-pivot}))
        if c is not None:
            out.add((c, pivot))
    return out


def shortest_resolution_nodes(sources, target, max_nodes):
    """Breadth-first exact search over sets of distinct derived clauses."""
    src = tuple(norm(c) for c in sources)
    assert all(c is not None for c in src)
    target = norm(target)
    assert target is not None and target not in src
    states = {frozenset()}
    counts = []
    witness = None
    for depth in range(1, max_nodes + 1):
        nxt = set()
        parents = {} if depth == max_nodes else None
        for derived in states:
            clauses = src + tuple(derived)
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    for clause, pivot in resolvents(clauses[i], clauses[j]):
                        if clause in src or clause in derived:
                            continue
                        new = frozenset(set(derived) | {clause})
                        if target in new:
                            witness = {
                                "nodes": depth,
                                "final_left": sorted(clauses[i], key=lambda x: (abs(x), x)),
                                "final_right": sorted(clauses[j], key=lambda x: (abs(x), x)),
                                "final_pivot": pivot,
                                "target": sorted(target, key=lambda x: (abs(x), x)),
                            }
                            counts.append(len(nxt) + 1)
                            return {"minimum": depth, "state_counts_before_hit": counts, "witness": witness}
                        nxt.add(new)
                        if parents is not None:
                            parents.setdefault(new, (derived, clauses[i], clauses[j], pivot, clause))
        counts.append(len(nxt))
        states = nxt
    return {"minimum": None, "state_counts_before_hit": counts, "witness": None}


def canonical_block(instance, source_pair):
    h = instance["h"]
    edge_count = 3 * h // 2
    g = edge_count + 1
    p, q = instance["source_variables"] - 1, instance["source_variables"]
    s0 = list(source_pair[0]["clause"])
    s1 = list(source_pair[1]["clause"])
    y = next(x for x in s0 if x > g and x not in (p, q))
    a = next(x for x in s0 if abs(x) <= edge_count)
    bc = [x for x in s1 if abs(x) <= edge_count]
    assert len(bc) == 2 and -y in s1 and g in s0
    b, c = bc
    ren = {g: 1, p: 2, q: 3, abs(a): 4, abs(b): 5, abs(c): 6, y: 7}

    def rlit(x):
        return ren[abs(x)] if x > 0 else -ren[abs(x)]

    pads = [[-1, 2, 3], [-1, 2, -3], [-1, -2, 3], [-1, -2, -3]]
    pair = [[rlit(x) for x in s0], [rlit(x) for x in s1]]
    target = [rlit(a), rlit(b), rlit(c)]
    signature = tuple(1 if x > 0 else 0 for x in target)
    return pads + pair, target, signature


def verify_row_necessity(instance):
    h = instance["h"]
    edges = [tuple(e) for e in instance["edges"]]
    rows = []
    for v in range(h):
        mask = 0
        for eid, (u, w) in enumerate(edges):
            if v in (u, w):
                mask ^= 1 << eid
        rows.append((mask, instance["charges"][v]))
    empty_support_subsets = []
    for subset in range(1, 1 << h):
        mask = rhs = 0
        for v, (vmask, vrhs) in enumerate(rows):
            if (subset >> v) & 1:
                mask ^= vmask
                rhs ^= vrhs
        if mask == 0:
            empty_support_subsets.append({"subset": subset, "rhs": rhs})
    assert empty_support_subsets == [{"subset": (1 << h) - 1, "rhs": 1}]
    return {
        "tested_nonempty_subsets": (1 << h) - 1,
        "only_empty_support_subset": "all_vertices",
        "all_vertex_rhs": 1,
    }


def main():
    raw = INPUT.read_bytes()
    assert sha256(raw) == INPUT_SHA
    prior = json.loads(raw)

    # Exact local pad search.
    pads = [[-1, 2, 3], [-1, 2, -3], [-1, -2, 3], [-1, -2, -3]]
    pad_search = shortest_resolution_nodes(pads, [-1], 3)
    assert pad_search["minimum"] == 3

    signatures = {}
    instances_out = []
    for inst in prior["instances"]:
        by_block = {}
        for source in inst["sources"]:
            meta = source["meta"]
            if "pad" in meta:
                continue
            key = (meta["vertex"], tuple(meta["wrong"]))
            by_block.setdefault(key, {})[meta["side"]] = source
        assert len(by_block) == 4 * inst["h"]

        for pair in by_block.values():
            src, target, signature = canonical_block(inst, pair)
            signatures.setdefault(signature, (src, target))

        h = inst["h"]
        m = 4 * h
        phase = {
            "shared_not_g": 3,
            "recover_original_clauses": 2 * m,
            "and3_vertex_rows": 3 * h,
            "xor_all_rows": h - 1,
        }
        work = sum(phase.values())
        assert work == 12 * h + 2 == inst["work"]
        assert inst["span"] == 5 + (h - 1).bit_length()
        instances_out.append({
            "graph": inst["graph"],
            "h": h,
            "source_sha256": inst["source_sha256"],
            "source_clauses": inst["source_clauses"],
            "route_phase_work": phase,
            "exact_route_work": work,
            "exact_route_span": inst["span"],
            "global_mixed_floor_only": 8 * h + 3,
            "row_necessity": verify_row_necessity(inst),
        })

    canonical_search = []
    for signature, (src, target) in sorted(signatures.items()):
        result = shortest_resolution_nodes(src, target, 5)
        assert result["minimum"] == 5
        assert result["state_counts_before_hit"][:4] == [9, 56, 316, 1690]
        canonical_search.append({
            "target_sign_signature": list(signature),
            "sources": src,
            "target": target,
            "exact_total_resolution_nodes_from_six_sources": 5,
            "equivalent_increment_after_shared_not_g": 2,
            "search": result,
        })

    assert len(canonical_search) == 8
    out = {
        "run": "LSPV-5/REFEREE384",
        "timestamp_PST": "2026-11-06 03:48",
        "status": ["PROVED/EXACT (declared recovery normal form)", "COMPUTATIONAL (finite exhaustive local search)", "OPEN (global R_mix341 minimum)", "OPEN (B3)"],
        "input_trace_path": str(INPUT.relative_to(ROOT)),
        "input_trace_sha256": INPUT_SHA,
        "normal_form": {
            "name": "block-respecting original-clause recovery / AND3 / XOR",
            "permits": ["oriented RES pivot order within each private-y block", "one shared not-g subproof", "balanced or unbalanced AND3/XOR trees", "shared-DAG references"],
            "requires": ["derive not-g from the four pad sources", "recover every original Tseitin clause from its two guarded sources plus not-g", "derive each vertex row by binary AND3 from its four recovered clauses", "derive 0=1 by binary XOR from all vertex rows"],
            "excludes_from_this_scoped_optimum": ["cross-block Resolution on original pivots", "DEF", "LOCAL-CONVERT", "branch split/discharge", "a direct mixed derivation that bypasses recovered clauses"],
            "work_theorem": "W_recovery(K(F_h)) = 12h+2",
            "span_theorem": "D_recovery(K(F_h)) = 5+ceil(log2 h)",
            "global_warning": "This is not W_Rmix341(K(F_h)); globally only 8h+3 <= W <= 12h+2 is established.",
        },
        "and_or_accounting": {
            "or_alternatives": "Each block may eliminate y then g or g then y; neither uses fewer than two nodes after shared not-g.",
            "and_obligations": "All four pads; both guarded clauses per original clause; all four recovered clauses per vertex; all h vertex rows.",
            "sharing": "The three-node not-g derivation is retained once and referenced by all 4h recovery blocks.",
            "contexts": "No branch assumptions or discharge occur; every node is in the root source context.",
        },
        "pad_search": pad_search,
        "canonical_block_searches": canonical_search,
        "instances": instances_out,
        "literature_scope": {
            "ordinary_resolution_hardness": "Urquhart 1987 / Ben-Sasson-Wigderson 2001 on suitable expander Tseitin formulas",
            "mixed_shortcut": "historical rule-level /341 AND3 plus GF(2), replayed in REFEREE383",
            "proof_system_warning": "Cook-Reckhow 1979 does not identify this fixed calculus under SAT in P",
        },
        "conclusion": "The 12h+2 construction is work- and span-optimal only inside the explicit recovery normal form. No global mixed minimum, superpolynomial Wbar bound, or B3 bridge follows.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUT.relative_to(ROOT)),
        "sha256": sha256(OUT.read_bytes()),
        "bytes": OUT.stat().st_size,
        "canonical_patterns": len(canonical_search),
        "instances": [{"graph": x["graph"], "work": x["exact_route_work"], "span": x["exact_route_span"]} for x in instances_out],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
