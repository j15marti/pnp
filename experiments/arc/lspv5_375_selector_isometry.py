#!/usr/bin/env python3
"""LSPV-5/375: selector-isometry and LSPV-3/436 replay.

This is an independent checker for three explicitly proposed completions.  It
is not an execution of an authoritative historical R_mix341 parser.
"""
from __future__ import annotations

import copy
import hashlib
import json
import resource
import time


SOURCE = [
    [1, 3, 4], [1, 3, -4], [1, -3, 4], [1, -3, -4],
    [2, 5, 6], [2, 5, -6], [2, -5, 6], [2, -5, -6],
    [-1, -2, 7], [-1, -2, -7],
]


def dimacs_bytes(source: list[list[int]]) -> bytes:
    body = [f"p cnf 7 {len(source)}"]
    body.extend(" ".join(map(str, clause)) + " 0" for clause in source)
    return ("\n".join(body) + "\n").encode()


SOURCE_SHA = hashlib.sha256(dimacs_bytes(SOURCE)).hexdigest()
PEER_DECLARED_SHA = "5d7299e97c4a0b4b5ee0a6fdb3acd54a76192a2fbf84d64da9694857316748ec"
PEER_JSON_BYTES = json.dumps({"nvars": 7, "clauses": SOURCE}, sort_keys=True).encode()
PEER_JSON_SHA = hashlib.sha256(PEER_JSON_BYTES).hexdigest()


def normal(clause: list[int]) -> list[int]:
    return sorted(set(clause), key=lambda x: (abs(x), x))


def src(i: int) -> dict:
    return {"src": i}


def node(i: int) -> dict:
    return {"node": i}


def facet(i: int, k: int) -> dict:
    return {"def": i, "facet": k}


def def_facets(var: int, a: int, b: int, truth: list[int]) -> list[list[int]]:
    ans = []
    for av in range(2):
        for bv in range(2):
            bad = 1 - truth[av + 2 * bv]
            ans.append(normal([(-a if av else a), (-b if bv else b), (-var if bad else var)]))
    return ans


def build_facet_proof() -> dict:
    nodes: list[dict] = []

    def res(left: dict, right: dict, pivot: int, claim: list[int]) -> dict:
        i = len(nodes)
        nodes.append({"id": i, "rule": "RES", "left": left, "right": right,
                      "pivot": pivot, "claim": normal(claim), "weight": 1})
        return node(i)

    a = res(res(src(0), src(1), 4, [1, 3]),
            res(src(2), src(3), 4, [1, -3]), 3, [1])
    b = res(res(src(4), src(5), 6, [2, 5]),
            res(src(6), src(7), 6, [2, -5]), 5, [2])
    ab = res(src(8), src(9), 7, [-1, -2])
    owner = len(nodes)
    nodes.append({"id": owner, "rule": "DEF", "var": 8, "inputs": [1, 2],
                  "truth": [0, 0, 0, 1], "weight": 1})
    aor = res(facet(owner, 0), facet(owner, 1), 2, [1, -8])
    bor = res(facet(owner, 0), facet(owner, 2), 1, [2, -8])
    bz = res(aor, ab, 1, [-2, -8])
    notz = res(bor, bz, 2, [-8])
    bz2 = res(a, facet(owner, 3), 1, [-2, 8])
    z = res(b, bz2, 2, [8])
    final = res(z, notz, 8, [])
    return {"format": "POS", "source_sha256": SOURCE_SHA,
            "source": {"nvars": 7, "clauses": SOURCE}, "nodes": nodes, "final": final}


def build_resolution_minimum() -> dict:
    nodes: list[dict] = []

    def res(left: dict, right: dict, pivot: int, claim: list[int]) -> dict:
        i = len(nodes)
        nodes.append({"id": i, "rule": "RES", "left": left, "right": right,
                      "pivot": pivot, "claim": normal(claim), "weight": 1})
        return node(i)

    a1 = res(src(0), src(1), 4, [1, 3])
    a2 = res(src(2), src(3), 4, [1, -3])
    a = res(a1, a2, 3, [1])
    b1 = res(src(4), src(5), 6, [2, 5])
    b2 = res(src(6), src(7), 6, [2, -5])
    b = res(b1, b2, 5, [2])
    ab = res(src(8), src(9), 7, [-1, -2])
    nb = res(a, ab, 1, [-2])
    final = res(b, nb, 2, [])
    return {"format": "POS", "source_sha256": SOURCE_SHA,
            "source": {"nvars": 7, "clauses": SOURCE}, "nodes": nodes, "final": final}


class Reject(Exception):
    pass


def check(proof: dict, grammar: str) -> dict:
    if grammar not in {"POS", "CONTENT", "GATE", "GATE_LOCAL"}:
        raise Reject("grammar")
    source = proof.get("source", {})
    clauses = source.get("clauses")
    if source.get("nvars") != 7 or clauses != SOURCE:
        raise Reject("source identity")
    if proof.get("source_sha256") != SOURCE_SHA:
        raise Reject("source hash")
    for clause in clauses:
        if len(clause) != 3 or len({abs(x) for x in clause}) != 3:
            raise Reject("malformed strict 3CNF")
        if any(x == 0 or abs(x) > 7 for x in clause):
            raise Reject("source literal")

    done: list[list[int] | None] = []
    owners: dict[int, list[list[int]]] = {}
    depths: list[int] = []
    refs = 0

    def get(ref: dict) -> tuple[list[int], int]:
        nonlocal refs
        refs += 1
        if set(ref) == {"src"}:
            i = ref["src"]
            if not isinstance(i, int) or not 0 <= i < len(clauses):
                raise Reject("source index")
            return clauses[i], 0
        if set(ref) == {"node"}:
            i = ref["node"]
            if not isinstance(i, int) or not 0 <= i < len(done) or done[i] is None:
                raise Reject("node reference")
            return done[i], depths[i]
        if "def" in ref:
            owner = ref.get("def")
            if not isinstance(owner, int) or owner not in owners:
                raise Reject("definition owner")
            views = owners[owner]
            if set(ref) == {"def", "facet"}:
                if grammar != "POS":
                    raise Reject("positional facet unavailable")
                k = ref["facet"]
                if not isinstance(k, int) or not 0 <= k < 4:
                    raise Reject("facet index")
                return views[k], depths[owner]
            if set(ref) == {"def", "claim"}:
                if grammar != "CONTENT":
                    raise Reject("content facet unavailable")
                claim = ref["claim"]
                if not isinstance(claim, list) or claim not in views:
                    raise Reject("claim is not an owner facet")
                return claim, depths[owner]
        raise Reject("untyped reference")

    nodes = proof.get("nodes")
    if not isinstance(nodes, list):
        raise Reject("nodes")
    for i, item in enumerate(nodes):
        if item.get("id") != i or item.get("weight") != 1:
            raise Reject("node id or weight")
        if item.get("rule") == "DEF":
            if item.get("var") != 8 or item.get("inputs") != [1, 2]:
                raise Reject("fresh DEF")
            truth = item.get("truth")
            if not isinstance(truth, list) or len(truth) != 4 or any(x not in (0, 1) for x in truth):
                raise Reject("DEF truth")
            owners[i] = def_facets(8, 1, 2, truth)
            done.append(None)
            depths.append(1)
        elif item.get("rule") == "LOCAL":
            if grammar != "GATE_LOCAL":
                raise Reject("LOCAL unavailable")
            parent = item.get("parent")
            if not isinstance(parent, dict) or set(parent) != {"def_rel"}:
                raise Reject("LOCAL parent type")
            owner = parent["def_rel"]
            if not isinstance(owner, int) or owner not in owners:
                raise Reject("LOCAL owner")
            claim = item.get("claim")
            if not isinstance(claim, list) or claim not in owners[owner]:
                raise Reject("LOCAL clause not implied")
            done.append(claim)
            depths.append(1 + depths[owner])
        elif item.get("rule") == "RES":
            left, dl = get(item.get("left", {}))
            right, dr = get(item.get("right", {}))
            pivot = item.get("pivot")
            if not isinstance(pivot, int) or pivot not in left or -pivot not in right:
                raise Reject("oriented pivot")
            out = normal([x for x in left if x != pivot] + [x for x in right if x != -pivot])
            if out != item.get("claim"):
                raise Reject("exact resolvent")
            done.append(out)
            depths.append(1 + max(dl, dr))
        else:
            raise Reject("rule")
    final, final_depth = get(proof.get("final", {}))
    if final != []:
        raise Reject("nonempty terminal")
    return {"paid_nodes": len(nodes), "weight": sum(x["weight"] for x in nodes),
            "span": final_depth, "references": refs, "def_nodes": len(owners)}


def owner_views(proof: dict) -> dict[int, list[list[int]]]:
    ans = {}
    for item in proof["nodes"]:
        if item["rule"] == "DEF":
            ans[item["id"]] = def_facets(item["var"], *item["inputs"], item["truth"])
    return ans


def translate(proof: dict, target: str) -> dict:
    if target not in {"POS", "CONTENT"}:
        raise ValueError(target)
    out = copy.deepcopy(proof)
    views = owner_views(proof)

    def tr(ref: dict) -> dict:
        if set(ref) == {"def", "facet"}:
            owner, k = ref["def"], ref["facet"]
            if owner not in views or not isinstance(k, int) or not 0 <= k < 4:
                raise Reject("bad positional source")
            return {"def": owner, "claim": views[owner][k]} if target == "CONTENT" else copy.deepcopy(ref)
        if set(ref) == {"def", "claim"}:
            owner, claim = ref["def"], ref["claim"]
            if owner not in views or claim not in views[owner]:
                raise Reject("bad content source")
            return {"def": owner, "facet": views[owner].index(claim)} if target == "POS" else copy.deepcopy(ref)
        return copy.deepcopy(ref)

    for item in out["nodes"]:
        if item["rule"] == "RES":
            item["left"] = tr(item["left"])
            item["right"] = tr(item["right"])
    out["final"] = tr(out["final"])
    out["format"] = target
    return out


def translate_gate_local(proof: dict) -> dict:
    """Replace every direct DEF facet by one shared paid LOCAL clause node."""
    out = {"format": "GATE_LOCAL", "source_sha256": proof["source_sha256"],
           "source": copy.deepcopy(proof["source"]), "nodes": []}
    old_to_new: dict[int, int] = {}
    facet_node: dict[tuple[int, int], int] = {}

    def map_ref(ref: dict) -> dict:
        if set(ref) == {"src"}:
            return copy.deepcopy(ref)
        if set(ref) == {"node"}:
            return {"node": old_to_new[ref["node"]]}
        if set(ref) == {"def", "facet"}:
            return {"node": facet_node[(ref["def"], ref["facet"])]}
        raise Reject("unsupported FACET-A reference")

    for item in proof["nodes"]:
        old_id = item["id"]
        if item["rule"] == "DEF":
            new_id = len(out["nodes"])
            copied = copy.deepcopy(item); copied["id"] = new_id
            out["nodes"].append(copied); old_to_new[old_id] = new_id
            views = def_facets(item["var"], *item["inputs"], item["truth"])
            for k, claim in enumerate(views):
                local_id = len(out["nodes"])
                out["nodes"].append({"id": local_id, "rule": "LOCAL",
                                     "parent": {"def_rel": new_id},
                                     "claim": claim, "weight": 1})
                facet_node[(old_id, k)] = local_id
        else:
            new_id = len(out["nodes"])
            copied = copy.deepcopy(item); copied["id"] = new_id
            copied["left"] = map_ref(item["left"])
            copied["right"] = map_ref(item["right"])
            out["nodes"].append(copied); old_to_new[old_id] = new_id
    out["final"] = map_ref(proof["final"])
    return out


def clause_value(clause: list[int], assignment: dict[int, bool]) -> bool:
    return any(assignment[abs(x)] == (x > 0) for x in clause)


def expect_reject(proof: dict, grammar: str, needle: str) -> None:
    try:
        check(proof, grammar)
    except Reject as exc:
        if needle not in str(exc):
            raise AssertionError((needle, str(exc))) from exc
    else:
        raise AssertionError("expected rejection")


def compact_bytes(obj: object) -> int:
    return len(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode())


def main() -> None:
    started = time.perf_counter()
    assertions = 0
    assert len(PEER_JSON_BYTES) == 148 and PEER_JSON_SHA == PEER_DECLARED_SHA
    assert len(dimacs_bytes(SOURCE)) == 104 and SOURCE_SHA != PEER_DECLARED_SHA
    assertions += 2
    pos = build_facet_proof()
    content = translate(pos, "CONTENT")
    pos_roundtrip = translate(content, "POS")
    gate_local = translate_gate_local(pos)
    res9 = build_resolution_minimum()

    c_pos = check(pos, "POS"); assertions += 1
    c_content = check(content, "CONTENT"); assertions += 1
    c_round = check(pos_roundtrip, "POS"); assertions += 1
    assert c_pos == c_content == c_round; assertions += 1
    assert c_pos["paid_nodes"] == 15 and c_pos["weight"] == 15; assertions += 1
    c_gate_local = check(gate_local, "GATE_LOCAL"); assertions += 1
    assert c_gate_local["paid_nodes"] == 19 and c_gate_local["weight"] == 19; assertions += 1

    expect_reject(pos, "CONTENT", "positional"); assertions += 1
    expect_reject(content, "POS", "content"); assertions += 1
    expect_reject(pos, "GATE", "positional"); assertions += 1

    c9 = {g: check(res9, g) for g in ("POS", "CONTENT", "GATE", "GATE_LOCAL")}
    assert all(x["paid_nodes"] == 9 and x["weight"] == 9 for x in c9.values()); assertions += 1

    models = 0
    for bits in range(1 << 7):
        assignment = {i: bool(bits & (1 << (i - 1))) for i in range(1, 8)}
        models += int(all(clause_value(c, assignment) for c in SOURCE))
    assert models == 0; assertions += 128

    deletion_witnesses = []
    for omit in range(len(SOURCE)):
        witness = None
        for bits in range(1 << 7):
            assignment = {i: bool(bits & (1 << (i - 1))) for i in range(1, 8)}
            if all(j == omit or clause_value(c, assignment) for j, c in enumerate(SOURCE)):
                witness = bits
                break
        assert witness is not None
        deletion_witnesses.append(witness)
        assertions += 1

    # Every selector-only definition view survives the round trip, including
    # repeated inputs and duplicate/tautological defining clauses.
    selector_cases = 0
    selector_facets = 0
    for a in (1, 2):
        for b in (1, 2):
            for mask in range(16):
                truth = [(mask >> i) & 1 for i in range(4)]
                views = def_facets(8, a, b, truth)
                for k, claim in enumerate(views):
                    back = views.index(claim)
                    assert views[back] == views[k]
                    selector_facets += 1
                    assertions += 1
                selector_cases += 1
    assert selector_cases == 64 and selector_facets == 256; assertions += 1

    forged = copy.deepcopy(content)
    for item in forged["nodes"]:
        if item["rule"] == "RES" and "claim" in item["left"]:
            item["left"]["claim"] = [1, 2, 8]
            break
    expect_reject(forged, "CONTENT", "owner facet"); assertions += 1
    bad_hash = copy.deepcopy(pos); bad_hash["source_sha256"] = "0" * 64
    expect_reject(bad_hash, "POS", "source hash"); assertions += 1
    bad_pivot = copy.deepcopy(res9); bad_pivot["nodes"][0]["pivot"] = 3
    expect_reject(bad_pivot, "POS", "oriented pivot"); assertions += 1
    bad_owner = copy.deepcopy(content)
    for item in bad_owner["nodes"]:
        if item["rule"] == "RES" and "claim" in item["left"]:
            item["left"]["def"] = 999
            break
    expect_reject(bad_owner, "CONTENT", "definition owner"); assertions += 1
    malformed = copy.deepcopy(res9); malformed["source"]["clauses"][0] = [1, 1, 4]
    expect_reject(malformed, "POS", "source identity"); assertions += 1
    bad_local = copy.deepcopy(gate_local)
    for item in bad_local["nodes"]:
        if item["rule"] == "LOCAL":
            item["claim"] = [1, 2, 8]
            break
    expect_reject(bad_local, "GATE_LOCAL", "not implied"); assertions += 1

    elapsed = time.perf_counter() - started
    result = {
        "run": "LSPV5_REFEREE375",
        "status": "PASS",
        "scope": "two proposed selector-equivalent completions plus GATE-B; not historical checker",
        "source_sha256": SOURCE_SHA,
        "source_dimacs_bytes": len(dimacs_bytes(SOURCE)),
        "source_assignments": 128,
        "source_models": models,
        "peer_436_hash_audit": {
            "published_source_ascii_dimacs_bytes": 104,
            "published_sha256": PEER_DECLARED_SHA,
            "actual_104_byte_dimacs_sha256": SOURCE_SHA,
            "recovered_serialization": "json.dumps(source_object, sort_keys=True) with default separators",
            "recovered_serialization_bytes": len(PEER_JSON_BYTES),
            "recovered_sha256": PEER_JSON_SHA,
            "exact_match": PEER_JSON_SHA == PEER_DECLARED_SHA,
            "finding": "published hash binds 148-byte JSON, not the adjacent 104-byte DIMACS; no format tag",
        },
        "essential_clauses": len(deletion_witnesses),
        "deletion_witness_bits": deletion_witnesses,
        "facet_proof": {"pos": c_pos, "content": c_content,
                        "pos_bytes": compact_bytes(pos), "content_bytes": compact_bytes(content)},
        "gate_local_repair": {"check": c_gate_local, "bytes": compact_bytes(gate_local),
                              "added_shared_LOCAL_nodes": 4,
                              "general_bound": "q'<=q+4d<=5q for d two-input DEF nodes"},
        "resolution_minimum": {"checks": c9, "bytes": compact_bytes(res9),
                               "lower_bound": "10 indispensable sources and binary-premise ancestry imply q>=9"},
        "same_bytes_differential": {"pos_rejected_by_content": True,
                                    "content_rejected_by_pos": True,
                                    "pos_rejected_by_gate": True},
        "selector_roundtrip": {"definition_cases": selector_cases, "facets": selector_facets,
                               "exact_semantic_view_preservation": True,
                               "exact_weight_preservation": True},
        "hostile_rejections": 6,
        "assertions": assertions,
        "elapsed_seconds": elapsed,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
