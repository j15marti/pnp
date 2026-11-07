#!/usr/bin/env python3
"""LSPV-5/412: audit the missing AND3 parent nonterminal in /341 prose.

This is deliberately NOT an implementation of the historical checker.  It
constructs two sound, unit-weight audit grammars that agree on the original
K4 odd-Tseitin certificate and disagree on the split certificate's first
RES -> AND3 edge.  The disagreement is evidence of specification
underdetermination, not evidence that either grammar is historically native.
"""
from __future__ import annotations

import copy
import hashlib
import json
import resource
import time
from itertools import product


class Reject(ValueError):
    pass


def canon_clause(xs):
    if not isinstance(xs, list) or any(type(x) is not int or x == 0 for x in xs):
        raise Reject("malformed clause")
    if len(set(xs)) != len(xs) or any(-x in xs for x in xs):
        raise Reject("non-proper clause")
    want = sorted(xs, key=lambda x: (abs(x), x < 0))
    if xs != want:
        raise Reject("noncanonical clause")
    return tuple(xs)


def canon_bytes(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def source_hash(source):
    return hashlib.sha256(canon_bytes(source)).hexdigest()


def parity(bits):
    return sum(bits) & 1


def lit_value(lit, env):
    v = env[abs(lit)]
    return v if lit > 0 else 1 - v


def eval_relation(rel, env):
    if rel["kind"] == "clause":
        return int(any(lit_value(x, env) for x in rel["clause"]))
    if rel["kind"] == "factor":
        s = rel["support"]
        return rel["truth"][sum(env[v] << i for i, v in enumerate(s))]
    if rel["kind"] == "affine":
        return int(parity([env[v] for v in rel["mask"]]) == rel["rhs"])
    raise Reject("unknown relation")


def relation_support(rel):
    if rel["kind"] == "clause":
        return sorted({abs(x) for x in rel["clause"]})
    if rel["kind"] == "factor":
        return list(rel["support"])
    if rel["kind"] == "affine":
        return list(rel["mask"])
    raise Reject("unknown relation")


def exact_factor(left, right):
    support = sorted(set(relation_support(left)) | set(relation_support(right)))
    if len(support) > 3:
        raise Reject("AND3 support")
    truth = []
    for z in range(1 << len(support)):
        env = {v: (z >> i) & 1 for i, v in enumerate(support)}
        truth.append(eval_relation(left, env) & eval_relation(right, env))
    return {"kind": "factor", "support": support, "truth": truth}


def xor_row(a, b):
    return {
        "kind": "affine",
        "mask": sorted(set(a["mask"]) ^ set(b["mask"])),
        "rhs": a["rhs"] ^ b["rhs"],
    }


def oriented_resolvent(a, b, pivot):
    aa, bb = set(a), set(b)
    choices = []
    if pivot in aa and -pivot in bb:
        choices.append((aa - {pivot}) | (bb - {-pivot}))
    if -pivot in aa and pivot in bb:
        choices.append((aa - {-pivot}) | (bb - {pivot}))
    out = []
    for c in choices:
        if any(-x in c for x in c):
            continue
        out.append(tuple(sorted(c, key=lambda x: (abs(x), x < 0))))
    return out


class Checker:
    """Two proposed byte grammars.

    EXTENSIONAL allows any earlier clause/factor view as an AND3 condition.
    TAGGED allows only SOURCE clause or AND3 factor producers.  Both retain
    complete ordinary RES, identical unit weights, and semantic checking.
    """

    def __init__(self, mode):
        if mode not in ("EXTENSIONAL", "TAGGED"):
            raise Reject("bad mode")
        self.mode = mode
        self.rows = 0

    def check(self, doc, require_refutation=True):
        if set(doc) != {"schema", "source", "source_sha256", "nodes"}:
            raise Reject("document keys")
        if doc["schema"] != "LSPV5-412-AUDIT-GRAMMAR":
            raise Reject("schema")
        source = doc["source"]
        if not isinstance(source, list):
            raise Reject("source")
        source = [canon_clause(c) for c in source]
        if doc["source_sha256"] != source_hash([list(c) for c in source]):
            raise Reject("source hash")
        rels = {}
        origins = {}
        for i, c in enumerate(source):
            rels[("source", i, "clause")] = {"kind": "clause", "clause": list(c)}
            origins[("source", i, "clause")] = "SOURCE"

        def ref(x, now):
            if not isinstance(x, dict):
                raise Reject("bad ref")
            if x.get("kind") == "source" and set(x) == {"kind", "id", "view"}:
                key = ("source", x["id"], x["view"])
            elif x.get("kind") == "node" and set(x) == {"kind", "id", "view"}:
                if type(x["id"]) is not int or x["id"] >= now:
                    raise Reject("forward/invalid ref")
                key = ("node", x["id"], x["view"])
            else:
                raise Reject("bad ref shape")
            if key not in rels:
                raise Reject("missing view")
            return rels[key], origins[key]

        nodes = doc["nodes"]
        if not isinstance(nodes, list):
            raise Reject("nodes")
        for i, n in enumerate(nodes):
            if not isinstance(n, dict) or n.get("id") != i or type(n.get("id")) is not int:
                raise Reject("nonsequential id")
            rule = n.get("rule")
            if rule == "RES":
                if set(n) != {"id", "rule", "left", "right", "pivot", "clause"}:
                    raise Reject("RES keys")
                a, _ = ref(n["left"], i)
                b, _ = ref(n["right"], i)
                if a["kind"] != "clause" or b["kind"] != "clause" or type(n["pivot"]) is not int:
                    raise Reject("RES types")
                got = canon_clause(n["clause"])
                if got not in oriented_resolvent(a["clause"], b["clause"], n["pivot"]):
                    raise Reject("wrong RES")
                key = ("node", i, "clause")
                rels[key] = {"kind": "clause", "clause": list(got)}
                origins[key] = "RES"
            elif rule == "AND3":
                allowed = {"id", "rule", "left", "right", "factor"}
                if "affine" in n:
                    allowed.add("affine")
                if set(n) != allowed:
                    raise Reject("AND3 keys")
                a, ao = ref(n["left"], i)
                b, bo = ref(n["right"], i)
                if a["kind"] not in ("clause", "factor") or b["kind"] not in ("clause", "factor"):
                    raise Reject("AND3 semantic parent")
                if self.mode == "TAGGED" and (ao not in ("SOURCE", "AND3") or bo not in ("SOURCE", "AND3")):
                    raise Reject("TAGGED AND3 parent")
                want = exact_factor(a, b)
                f = n["factor"]
                if not isinstance(f, dict) or set(f) != {"support", "truth"}:
                    raise Reject("factor shape")
                if f["support"] != want["support"] or f["truth"] != want["truth"]:
                    raise Reject("wrong factor")
                self.rows += 1 << len(want["support"])
                fkey = ("node", i, "factor")
                rels[fkey] = want
                origins[fkey] = "AND3"
                if "affine" in n:
                    q = n["affine"]
                    if not isinstance(q, dict) or set(q) != {"mask", "rhs"}:
                        raise Reject("affine shape")
                    if q["mask"] != sorted(set(q["mask"])) or q["rhs"] not in (0, 1):
                        raise Reject("affine canonical")
                    qr = {"kind": "affine", "mask": q["mask"], "rhs": q["rhs"]}
                    if not set(qr["mask"]).issubset(want["support"]):
                        raise Reject("affine support")
                    support = want["support"]
                    for z in range(1 << len(support)):
                        env = {v: (z >> j) & 1 for j, v in enumerate(support)}
                        if eval_relation(want, env) != eval_relation(qr, env):
                            raise Reject("false affine annotation")
                        self.rows += 1
                    akey = ("node", i, "affine")
                    rels[akey] = qr
                    origins[akey] = "AND3"
            elif rule == "GF2":
                if set(n) != {"id", "rule", "left", "right", "affine"}:
                    raise Reject("GF2 keys")
                a, _ = ref(n["left"], i)
                b, _ = ref(n["right"], i)
                if a["kind"] != "affine" or b["kind"] != "affine":
                    raise Reject("GF2 parent")
                want = xor_row(a, b)
                if n["affine"] != {"mask": want["mask"], "rhs": want["rhs"]}:
                    raise Reject("wrong GF2")
                key = ("node", i, "affine")
                rels[key] = want
                origins[key] = "GF2"
            else:
                raise Reject("unknown rule")
        if require_refutation:
            if not nodes:
                raise Reject("empty proof")
            final = rels.get(("node", len(nodes) - 1, "affine"))
            if final != {"kind": "affine", "mask": [], "rhs": 1}:
                raise Reject("not contradiction")
        return {"paid_nodes": len(nodes), "rows_checked": self.rows}


def src_ref(i):
    return {"kind": "source", "id": i, "view": "clause"}


def node_ref(i, view):
    return {"kind": "node", "id": i, "view": view}


def k4_source(charges):
    edges = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
    edge_id = {e: i + 1 for i, e in enumerate(edges)}
    incident = {v: [] for v in range(1, 5)}
    for e, i in edge_id.items():
        incident[e[0]].append(i)
        incident[e[1]].append(i)
    source, packets = [], []
    for v in range(1, 5):
        vs = sorted(incident[v])
        packet = []
        for bits in product((0, 1), repeat=3):
            if parity(bits) != charges[v - 1]:
                packet.append(len(source))
                source.append(sorted([x if b == 0 else -x for x, b in zip(vs, bits)], key=lambda x: (abs(x), x < 0)))
        packets.append((packet, vs, charges[v - 1]))
    return source, packets


class Builder:
    def __init__(self, source):
        self.source = source
        self.nodes = []
        self.rels = {("source", i, "clause"): {"kind": "clause", "clause": c} for i, c in enumerate(source)}

    def relation(self, r):
        return self.rels[(r["kind"], r["id"], r["view"])]

    def add_res(self, left, right, pivot, clause):
        i = len(self.nodes)
        node = {"id": i, "rule": "RES", "left": left, "right": right, "pivot": pivot, "clause": clause}
        self.nodes.append(node)
        self.rels[("node", i, "clause")] = {"kind": "clause", "clause": clause}
        return node_ref(i, "clause")

    def add_and3(self, left, right, affine=None):
        i = len(self.nodes)
        f = exact_factor(self.relation(left), self.relation(right))
        node = {"id": i, "rule": "AND3", "left": left, "right": right,
                "factor": {"support": f["support"], "truth": f["truth"]}}
        if affine is not None:
            node["affine"] = {"mask": affine[0], "rhs": affine[1]}
        self.nodes.append(node)
        self.rels[("node", i, "factor")] = f
        if affine is not None:
            self.rels[("node", i, "affine")] = {"kind": "affine", "mask": affine[0], "rhs": affine[1]}
        return node_ref(i, "factor"), node_ref(i, "affine") if affine is not None else None

    def add_gf2(self, left, right):
        i = len(self.nodes)
        q = xor_row(self.relation(left), self.relation(right))
        node = {"id": i, "rule": "GF2", "left": left, "right": right,
                "affine": {"mask": q["mask"], "rhs": q["rhs"]}}
        self.nodes.append(node)
        self.rels[("node", i, "affine")] = q
        return node_ref(i, "affine")

    def doc(self):
        return {"schema": "LSPV5-412-AUDIT-GRAMMAR", "source": self.source,
                "source_sha256": source_hash(self.source), "nodes": self.nodes}


def add_packets(builder, packet_refs, packets):
    rows = []
    for refs, (_, support, rhs) in zip(packet_refs, packets):
        a, _ = builder.add_and3(refs[0], refs[1])
        b, _ = builder.add_and3(refs[2], refs[3])
        _, q = builder.add_and3(a, b, (support, rhs))
        rows.append(q)
    cur = rows[0]
    for q in rows[1:]:
        cur = builder.add_gf2(cur, q)
    return cur


def base_document(charges):
    source, packets = k4_source(charges)
    b = Builder(source)
    refs = [[src_ref(i) for i in packet] for packet, _, _ in packets]
    add_packets(b, refs, packets)
    return b.doc(), packets


def split_document(charges):
    base, packets = k4_source(charges)
    split = []
    pairs = []
    for i, c in enumerate(base):
        a = 7 + i
        p = sorted([c[0], c[1], a], key=lambda x: (abs(x), x < 0))
        q = sorted([c[0], c[2], -a], key=lambda x: (abs(x), x < 0))
        pairs.append((len(split), len(split) + 1, a, c))
        split.extend([p, q])
    b = Builder(split)
    reconstructed = []
    for p, q, a, c in pairs:
        reconstructed.append(b.add_res(src_ref(p), src_ref(q), a, c))
    refs = [[reconstructed[i] for i in packet] for packet, _, _ in packets]
    add_packets(b, refs, packets)
    return b.doc(), packets


def model_count(source):
    n = max(abs(x) for c in source for x in c)
    count = 0
    for bits in product((0, 1), repeat=n):
        env = {i + 1: bits[i] for i in range(n)}
        if all(any(lit_value(x, env) for x in c) for c in source):
            count += 1
    return count


def rejected(doc, mode, mut):
    d = copy.deepcopy(doc)
    mut(d)
    try:
        Checker(mode).check(d)
    except Reject:
        return True
    return False


def main():
    started = time.perf_counter()
    odd, _ = base_document([1, 0, 0, 0])
    even, _ = base_document([0, 0, 0, 0])
    split, _ = split_document([1, 0, 0, 0])

    odd_a = Checker("EXTENSIONAL").check(odd)
    odd_b = Checker("TAGGED").check(odd)
    split_a = Checker("EXTENSIONAL").check(split)
    tagged_reason = None
    try:
        Checker("TAGGED").check(split)
    except Reject as e:
        tagged_reason = str(e)
    assert tagged_reason == "TAGGED AND3 parent"
    try:
        Checker("EXTENSIONAL").check(even)
        raise AssertionError("even charge accepted as contradiction")
    except Reject as e:
        assert str(e) == "not contradiction"

    mutations = {
        "source_hash": lambda d: d.__setitem__("source_sha256", "0" * 64),
        "bad_res_pivot": lambda d: d["nodes"][0].__setitem__("pivot", 1),
        "forward_ref": lambda d: d["nodes"][16]["left"].__setitem__("id", 999),
        "huge_node_id": lambda d: d["nodes"][0].__setitem__("id", 2**63),
        "wrong_factor": lambda d: d["nodes"][16]["factor"]["truth"].__setitem__(0, 1 - d["nodes"][16]["factor"]["truth"][0]),
        "wrong_affine": lambda d: d["nodes"][18]["affine"].__setitem__("rhs", 1 - d["nodes"][18]["affine"]["rhs"]),
        "wrong_gf2": lambda d: d["nodes"][-1]["affine"].__setitem__("rhs", 0),
        "bad_source_clause": lambda d: (d["source"][0].__setitem__(1, d["source"][0][0]), d.__setitem__("source_sha256", source_hash(d["source"]))),
        "unknown_rule": lambda d: d["nodes"][0].__setitem__("rule", "SEMANTIC_ORACLE"),
    }
    mutation_results = {name: rejected(split, "EXTENSIONAL", f) for name, f in mutations.items()}
    assert all(mutation_results.values())

    # Repeated-input condition: exact conjunction is idempotent.  This is a
    # semantic control, not a new historical rule or a complete refutation.
    r = {"kind": "clause", "clause": odd["source"][0]}
    idem = exact_factor(r, r)
    support = idem["support"]
    repeated_ok = all(
        eval_relation(idem, {v: (z >> i) & 1 for i, v in enumerate(support)})
        == eval_relation(r, {v: (z >> i) & 1 for i, v in enumerate(support)})
        for z in range(1 << len(support))
    )
    assert repeated_ok

    out = {
        "schema": "LSPV5/412-AND3-PARENT-UNDERDETERMINATION",
        "status": "PROVED/EXACT specification-nonuniqueness; COMPUTATIONAL traces; historical checker OPEN",
        "historical_source": {
            "path": "research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex",
            "blob": "c87acd11d32ccfc3b7acd3667ef11daeb60079cb",
            "missing_nonterminal": "condition / admissible AND3 serialized parent views",
        },
        "trackers": {"proof1_blob": "96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b",
                     "proof2_start_blob": "af757c6238edcc9140eb4c183c5c7964302cdf3b"},
        "k4": {"base_source_clauses": 16, "split_source_clauses": 32,
               "odd_base_models": model_count(odd["source"]),
               "even_base_models": model_count(even["source"]),
               "base_paid_nodes": len(odd["nodes"]), "split_paid_nodes": len(split["nodes"]),
               "base_bytes": len(canon_bytes(odd)), "split_bytes": len(canon_bytes(split)),
               "base_sha256": hashlib.sha256(canon_bytes(odd)).hexdigest(),
               "split_sha256": hashlib.sha256(canon_bytes(split)).hexdigest()},
        "grammar_outcomes": {
            "EXTENSIONAL_base": odd_a, "TAGGED_base": odd_b,
            "EXTENSIONAL_split": split_a, "TAGGED_split_rejection": tagged_reason,
        },
        "controls": {"even_charge_rejected": True, "repeated_input_idempotent": repeated_ok,
                     "mutations_rejected": mutation_results,
                     "def_facets": "not exercised: fragment contains no DEF node"},
        "claim_boundary": {
            "proved": "the /341 prose plus its exhibited source/AND3/GF2 traces does not uniquely determine whether a RES clause view is an AND3 byte parent",
            "not_proved": "which grammar the unavailable historical checker accepts, or any mixed lower bound/B3/P-vs-NP result",
        },
        "resources": {"wall_seconds": time.perf_counter() - started,
                      "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
