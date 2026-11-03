#!/usr/bin/env python3
"""Finite controls for the ER_2 -> Rmix341 simulation seam.

This is an experiment, not a proof of an asymptotic lower bound.  It emits
strictly checkable source/certificate controls and a resource ledger.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import platform
import resource
import time
from dataclasses import dataclass
from pathlib import Path

Clause = tuple[int, ...]


def canon(clause: list[int] | tuple[int, ...]) -> Clause:
    if any(l == 0 for l in clause):
        raise ValueError("literal zero is not legal inside a clause")
    unique = set(clause)
    if any(-l in unique for l in unique):
        raise ValueError("tautological clause")
    return tuple(sorted(unique, key=lambda x: (abs(x), x < 0)))


def parse_dimacs(text: str) -> tuple[int, list[Clause]]:
    lines = text.splitlines()
    if not lines or not lines[0].startswith("p cnf "):
        raise ValueError("missing first-line header")
    fields = lines[0].split()
    if len(fields) != 4 or fields[:2] != ["p", "cnf"]:
        raise ValueError("malformed header")
    n, m = int(fields[2]), int(fields[3])
    if n < 0 or m < 0:
        raise ValueError("negative dimensions")
    clauses: list[Clause] = []
    for line in lines[1:]:
        if not line or line.startswith("c"):
            raise ValueError("blank/comment lines disallowed in strict control")
        toks = line.split()
        if not toks or toks[-1] != "0" or toks.count("0") != 1:
            raise ValueError("clause must have one terminal zero")
        raw = [int(x) for x in toks[:-1]]
        if len(raw) != len(set(raw)):
            raise ValueError("duplicate source literal")
        if any(abs(x) > n for x in raw):
            raise ValueError("variable out of range")
        clauses.append(canon(raw))
    if len(clauses) != m:
        raise ValueError("clause-count mismatch")
    return n, clauses


def models(n: int, clauses: list[Clause]) -> list[tuple[int, ...]]:
    ans: list[tuple[int, ...]] = []
    for bits in itertools.product((0, 1), repeat=n):
        if all(any((lit > 0) == bool(bits[abs(lit) - 1]) for lit in c) for c in clauses):
            ans.append(bits)
    return ans


def resolve(left: Clause, right: Clause, pivot: int) -> Clause:
    if pivot <= 0 or pivot not in left or -pivot not in right:
        raise ValueError("oriented pivot absent")
    raw = [x for x in left if x != pivot] + [x for x in right if x != -pivot]
    return canon(raw)


@dataclass(frozen=True)
class DefNode:
    out: int
    left: int
    right: int
    op: str

    def slots(self) -> tuple[Clause, Clause, Clause]:
        if self.op != "AND":
            raise ValueError("only the declared AND gate is used in this finite replay")
        if len({abs(self.out), abs(self.left), abs(self.right)}) != 3:
            raise ValueError("gate variables must be distinct")
        if min(self.out, self.left, self.right) <= 0:
            raise ValueError("positive variable identifiers required")
        y, a, b = self.out, self.left, self.right
        return (canon((-y, a)), canon((-y, b)), canon((y, -a, -b)))


def verify_tiny_certificate(source: list[Clause], defnode: DefNode, steps: list[dict]) -> dict:
    slots = defnode.slots()
    pool: dict[str, Clause] = {f"S{i}": c for i, c in enumerate(source)}
    pool.update({f"D{i}": c for i, c in enumerate(slots)})
    for i, step in enumerate(steps):
        if set(step) != {"left", "right", "pivot", "clause"}:
            raise ValueError("bad step fields")
        if step["left"] not in pool or step["right"] not in pool:
            raise ValueError("unknown dependency")
        got = resolve(pool[step["left"]], pool[step["right"]], int(step["pivot"]))
        want = canon(tuple(step["clause"]))
        if got != want:
            raise ValueError(f"wrong resolvent at R{i}")
        pool[f"R{i}"] = got
    if not steps or pool[f"R{len(steps)-1}"] != ():
        raise ValueError("certificate does not end in contradiction")
    return {"def_nodes": 1, "res_nodes": len(steps), "total_nodes": 1 + len(steps)}


def tiny_case() -> tuple[str, DefNode, list[dict]]:
    text = "p cnf 2 3\n1 0\n2 0\n-1 -2 0\n"
    d = DefNode(out=3, left=1, right=2, op="AND")
    # y from a,b and the AND gate; not-y from the source collision and gate slots.
    steps = [
        {"left": "S0", "right": "D2", "pivot": 1, "clause": [3, -2]},
        {"left": "S1", "right": "R0", "pivot": 2, "clause": [3]},
        {"left": "D0", "right": "S2", "pivot": 1, "clause": [-3, -2]},
        {"left": "D1", "right": "R2", "pivot": 2, "clause": [-3]},
        {"left": "R1", "right": "R3", "pivot": 3, "clause": []},
    ]
    return text, d, steps


def bphp(h: int) -> tuple[int, list[Clause]]:
    if h != 2:
        raise ValueError("finite exhaustive control intentionally fixes h=2")
    # Three pigeons, one bit per pigeon; forbid each pair at holes 0 and 1.
    clauses: list[Clause] = []
    for i, j in itertools.combinations(range(1, h + 2), 2):
        clauses.append(canon((i, j)))       # not both 0
        clauses.append(canon((-i, -j)))     # not both 1
    return 3, clauses


def tseitin_k4(charge: int) -> tuple[int, list[Clause]]:
    # Edge variables in lexicographic order; each degree-3 vertex has parity charge.
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    clauses: list[Clause] = []
    charges = [1, 0, 0, 0] if charge else [0, 0, 0, 0]
    for v in range(4):
        incident = [i + 1 for i, e in enumerate(edges) if v in e]
        # Forbid assignments whose parity is not charge.
        for bits in itertools.product((0, 1), repeat=3):
            if (sum(bits) & 1) != charges[v]:
                clause = tuple(-x if b else x for x, b in zip(incident, bits))
                clauses.append(canon(clause))
    return 6, clauses


def sha_json(obj: object) -> str:
    data = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    started = time.time()
    text, d, steps = tiny_case()
    n, src = parse_dimacs(text)
    tiny_models = models(n, src)
    cert = verify_tiny_certificate(src, d, steps)

    sat_neighbor = "p cnf 2 3\n1 0\n2 0\n1 2 0\n"
    sn, sc = parse_dimacs(sat_neighbor)
    sat_models = models(sn, sc)

    deletions = [len(models(n, src[:i] + src[i + 1 :])) for i in range(len(src))]

    malformed = [
        "", "c x\np cnf 1 0\n", "p cnd 1 0\n", "p cnf 1 2\n1 0\n",
        "p cnf 1 1\n2 0\n", "p cnf 1 1\n1\n", "p cnf 1 1\n1 0 0\n",
        "p cnf 2 1\n1 -1 0\n",
    ]
    malformed_rejected = 0
    for bad in malformed:
        try:
            parse_dimacs(bad)
        except (ValueError, TypeError):
            malformed_rejected += 1

    corruptions = []
    c1 = [dict(x) for x in steps]
    c1[0] = dict(c1[0]); c1[0]["pivot"] = 2; corruptions.append(c1)
    c2 = [dict(x) for x in steps]
    c2[-1] = dict(c2[-1]); c2[-1]["clause"] = [3]; corruptions.append(c2)
    c3 = [dict(x) for x in steps[:-1]]; corruptions.append(c3)
    c4 = [dict(x) for x in steps]
    c4[1] = dict(c4[1]); c4[1]["left"] = "R9"; corruptions.append(c4)
    corrupt_rejected = 0
    for bad_steps in corruptions:
        try:
            verify_tiny_certificate(src, d, bad_steps)
        except (ValueError, TypeError, KeyError):
            corrupt_rejected += 1

    bn, bc = bphp(2)
    bmodels = models(bn, bc)
    flip_counts = []
    for ci, clause in enumerate(bc):
        for li, lit in enumerate(clause):
            changed = list(clause); changed[li] = -lit
            altered = list(bc); altered[ci] = canon(changed)
            flip_counts.append(len(models(bn, altered)))

    on, oc = tseitin_k4(1)
    en, ec = tseitin_k4(0)
    odd_models, even_models = models(on, oc), models(en, ec)

    assertions = {
        "tiny_unsat": len(tiny_models) == 0,
        "tiny_certificate_1def_5res": cert == {"def_nodes": 1, "res_nodes": 5, "total_nodes": 6},
        "sat_neighbor_has_all_ones": (1, 1) in sat_models,
        "all_source_deletions_sat": all(x > 0 for x in deletions),
        "all_malformed_rejected": malformed_rejected == len(malformed),
        "all_corruptions_rejected": corrupt_rejected == len(corruptions),
        "bphp2_unsat": len(bmodels) == 0,
        "bphp2_all_sign_flips_one_model": flip_counts == [1] * 12,
        "k4_odd_unsat": len(odd_models) == 0,
        "k4_even_eight_models": len(even_models) == 8,
    }
    if not all(assertions.values()):
        raise AssertionError(assertions)

    raw = {
        "claim_id": "EXTENSION-SIMULATION-BARRIER-REFEREE299",
        "status": "COMPUTATIONAL finite controls supporting a separate exact syntactic simulation proof",
        "assertions": assertions,
        "tiny": {
            "source_dimacs": text,
            "source_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "source_clauses": src,
            "models": len(tiny_models),
            "def": d.__dict__,
            "def_slots": d.slots(),
            "steps": steps,
            "certificate_cost": cert,
            "source_deletion_model_counts": deletions,
            "sat_neighbor_models": sat_models,
        },
        "bphp_h2": {"clauses": bc, "models": 0, "sign_flip_model_counts": flip_counts},
        "tseitin_k4": {"odd_models": len(odd_models), "even_models": len(even_models), "known_rmix_xor_upper_nodes": 15},
        "host": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "elapsed_seconds": time.time() - started,
            "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "pid": os.getpid(),
        },
    }
    raw["content_sha256"] = sha_json(raw)
    out = Path("results/raw/arc/2026-11-02_1648_LSPV5_EXTENSION_SIMULATION_BARRIER_REFEREE299_raw.json")
    out.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(out), "assertions": assertions, "content_sha256": raw["content_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
