#!/usr/bin/env python3
"""Independent red-team replay of LSPV-1/498 and native-grammar boundary.

This is intentionally independent of the peer JavaScript proof generator.  It
constructs and checks every three-variable LOCAL3-to-Res(PC_1/F2) gadget, then
checks that the attached historical 341 verifier accepts its own baseline but
rejects an otherwise identical certificate whose first rule tag is LOCAL3.
"""

from __future__ import annotations

import copy
import hashlib
import json
import resource
import subprocess
import tempfile
import time
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PEER_JS = ROOT / "scratch_inputs/lspv1_498_local_respc_sim.js"
PEER_RAW = ROOT / "lspv1_498_local_respc_raw_js.json"
HIST_DIR = ROOT / "attachments/native_core_audit/pnp_native_core_audit/historical"
HIST_VERIFY = HIST_DIR / "lspv2_341_independent_verify.js"
HIST_BASELINE = ROOT / "attachments/native_core_audit/pnp_native_core_audit/baseline.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parity(x: int) -> int:
    return x.bit_count() & 1


def equation(mask: int, rhs: int) -> tuple[int, int]:
    assert 0 <= mask < 8 and rhs in (0, 1)
    return mask, rhs


def eq_true(assignment: int, eq: tuple[int, int]) -> bool:
    return parity(assignment & eq[0]) == eq[1]


def assignment_clause(assignment: int) -> tuple[tuple[int, int], ...]:
    # Clause false exactly at assignment: x_i = 1-a_i as disjuncts.
    return tuple(sorted((1 << i, 1 - ((assignment >> i) & 1)) for i in range(3)))


def boolean_axiom(i: int) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(((1 << i, 0), (1 << i, 1))))


def norm_clause(items) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(set(items)))


def entails(source, target) -> bool:
    return all(any(not any(eq_true(a, e) for e in clause) for clause in source) or eq_true(a, target)
               for a in range(8))


class Proof:
    def __init__(self, source):
        self.source = tuple(source)
        self.nodes: list[dict] = []
        self.source_ids = [self.add("src", c, [], index=i) for i, c in enumerate(source)]
        self.axiom_ids = [self.add("ax", boolean_axiom(i), [], index=i) for i in range(3)]

    def add(self, rule, clause, parents, **meta):
        clause = norm_clause(clause)
        assert all(isinstance(p, int) and 0 <= p < len(self.nodes) for p in parents)
        if rule == "src":
            assert clause == self.source[meta["index"]]
        elif rule == "ax":
            assert clause == boolean_axiom(meta["index"])
        elif rule == "weak":
            assert len(parents) == 1
            assert set(self.nodes[parents[0]]["clause"]).issubset(clause)
        elif rule == "sum":
            assert len(parents) == 2
            left = self.nodes[parents[0]]["clause"]
            right = self.nodes[parents[1]]["clause"]
            f, g = meta["f"], meta["g"]
            assert f in left and g in right
            expected = norm_clause(
                [e for e in left if e != f]
                + [e for e in right if e != g]
                + [equation(f[0] ^ g[0], f[1] ^ g[1])]
            )
            assert clause == expected
        elif rule == "del":
            assert len(parents) == 1
            prior = self.nodes[parents[0]]["clause"]
            assert (0, 1) in prior
            assert clause == tuple(e for e in prior if e != (0, 1))
        else:
            raise AssertionError(f"unknown rule {rule}")
        node_id = len(self.nodes)
        self.nodes.append({"id": node_id, "rule": rule, "clause": clause, "parents": tuple(parents), **meta})
        return node_id


def build(source, target):
    assert target[0] != 0 and entails(source, target)
    proof = Proof(source)
    active = {}
    for a in range(8):
        d_a = assignment_clause(a)
        if not eq_true(a, target):
            source_index = source.index(d_a)
            active[a] = proof.add("weak", (*d_a, target), [proof.source_ids[source_index]])
            continue
        terms = []
        for i in range(3):
            if target[0] & (1 << i):
                literal = (1 << i, (a >> i) & 1)
                node = proof.add("weak", (*d_a, literal), [proof.axiom_ids[i]])
                terms.append((node, literal))
        while len(terms) > 1:
            (u, f), (v, g), *rest = terms
            summed = (f[0] ^ g[0], f[1] ^ g[1])
            node = proof.add("sum", (*d_a, summed), [u, v], f=f, g=g)
            terms = [(node, summed), *rest]
        assert terms == [(terms[0][0], target)]
        active[a] = terms[0][0]

    for bit in (2, 1, 0):
        next_active = {}
        for a in sorted(active):
            if a & (1 << bit):
                continue
            b = a ^ (1 << bit)
            f = (1 << bit, 1 - ((a >> bit) & 1))
            g = (1 << bit, 1 - ((b >> bit) & 1))
            left = proof.nodes[active[a]]["clause"]
            right = proof.nodes[active[b]]["clause"]
            assert f in left and g in right
            residue = norm_clause([e for e in left if e != f] + [e for e in right if e != g])
            summed = proof.add("sum", (*residue, (0, 1)), [active[a], active[b]], f=f, g=g)
            next_active[a] = proof.add("del", residue, [summed])
        active = next_active
        assert len(active) == (1 << bit)
    assert proof.nodes[active[0]]["clause"] == (target,)
    return proof


def run_historical(data: dict) -> subprocess.CompletedProcess:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
        json.dump(data, tmp)
        tmp_path = Path(tmp.name)
    try:
        return subprocess.run(
            ["node", str(HIST_VERIFY), str(tmp_path)],
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
    finally:
        tmp_path.unlink(missing_ok=True)


def main():
    started = time.perf_counter()
    aggregate = Counter()
    by_source_size = defaultdict(int)
    rule_counts = Counter()
    example_hashes = []
    for bits in range(256):
        source = [assignment_clause(i) for i in range(8) if bits & (1 << i)]
        for mask in range(1, 8):
            for rhs in (0, 1):
                target = equation(mask, rhs)
                if not entails(source, target):
                    continue
                proof = build(source, target)
                aggregate["acceptedImplications"] += 1
                aggregate["checkedNodes"] += len(proof.nodes)
                aggregate["maxNodes"] = max(aggregate["maxNodes"], len(proof.nodes))
                by_source_size[len(source)] += 1
                rule_counts.update(node["rule"] for node in proof.nodes)
                if target == (7, rhs) and len(source) == 4:
                    payload = json.dumps(proof.nodes, sort_keys=True, default=list, separators=(",", ":")).encode()
                    example_hashes.append(hashlib.sha256(payload).hexdigest())

    assert aggregate == Counter(acceptedImplications=224, checkedNodes=8224, maxNodes=49)
    assert dict(sorted(by_source_size.items())) == {4: 14, 5: 56, 6: 84, 7: 56, 8: 14}

    peer = json.loads(PEER_RAW.read_text())
    peer_projection = {
        "acceptedImplications": peer["acceptedImplications"],
        "checkedNodes": peer["checkedNodes"],
        "maxNodes": peer["maxNodes"],
        "bySourceSize": {int(k): v for k, v in peer["bySourceSize"].items()},
    }
    independent_projection = {
        "acceptedImplications": aggregate["acceptedImplications"],
        "checkedNodes": aggregate["checkedNodes"],
        "maxNodes": aggregate["maxNodes"],
        "bySourceSize": dict(sorted(by_source_size.items())),
    }
    assert peer_projection == independent_projection

    # Explicitly challenge the two other translated rules in Theorem 498.1.
    res = Proof([norm_clause(((1, 0), (2, 0))), norm_clause(((1, 1), (4, 0)))])
    pivot_sum = res.add("sum", ((0, 1), (2, 0), (4, 0)), res.source_ids, f=(1, 0), g=(1, 1))
    resolvent = res.add("del", ((2, 0), (4, 0)), [pivot_sum])
    assert res.nodes[resolvent]["clause"] == ((2, 0), (4, 0))
    xor = Proof([((3, 0),), ((6, 1),)])
    xor_id = xor.add("sum", ((5, 1),), xor.source_ids, f=(3, 0), g=(6, 1))
    assert xor.nodes[xor_id]["clause"] == ((5, 1),)

    baseline = json.loads(HIST_BASELINE.read_text())
    accepted = run_historical(baseline)
    assert accepted.returncode == 0 and '"verifier"' in accepted.stdout
    mutated = copy.deepcopy(baseline)
    mutated["fixtures"][0]["proof"][0]["rule"] = "LOCAL3"
    rejected = run_historical(mutated)
    assert rejected.returncode != 0 and "unknown rule" in rejected.stderr

    result = {
        "status": "PASS; finite syntactic validation only",
        "scope": "independent LOCAL3 -> syntactic Res(PC_1/F2) replay; historical 341 grammar boundary",
        "sourceSubsets": 256,
        "affineTargets": 14,
        **dict(aggregate),
        "bySourceSize": {str(k): v for k, v in sorted(by_source_size.items())},
        "allRuleNodes": dict(sorted(rule_counts.items())),
        "peerAggregateExactMatch": True,
        "ordinaryResolutionTwoStepAccepted": True,
        "unitAffineXorOneStepAccepted": True,
        "historicalBaselineAccepted": True,
        "historicalLOCAL3MutationRejected": True,
        "historicalRejectFragment": "unknown rule",
        "exampleDagSha256": sorted(example_hashes),
        "inputs": {
            str(PEER_JS.relative_to(ROOT)): sha256(PEER_JS),
            str(PEER_RAW.relative_to(ROOT)): sha256(PEER_RAW),
            str(HIST_VERIFY.relative_to(ROOT)): sha256(HIST_VERIFY),
            str(HIST_BASELINE.relative_to(ROOT)): sha256(HIST_BASELINE),
        },
        "claimLimits": [
            "does not replay Pang's asymptotic theorem",
            "does not show R_loc3 is a subcalculus of historical R_mix341",
            "does not prove a historical full-mixed lower bound or B3",
        ],
        "resourceLedger": {
            "wallSeconds": round(time.perf_counter() - started, 6),
            "userSeconds": round(resource.getrusage(resource.RUSAGE_SELF).ru_utime, 6),
            "systemSeconds": round(resource.getrusage(resource.RUSAGE_SELF).ru_stime, 6),
            "maxRssKiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "subprocesses": 2,
            "note": "Includes baseline and hostile historical-checker Node subprocesses; excludes literature/project reads and publication.",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
