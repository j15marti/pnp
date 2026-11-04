#!/usr/bin/env python3
"""REFEREE338: lossless recoding versus image authentication controls.

The encoder is total on byte strings, injective via duplicated satisfiable
unit tags, and keeps every clause of every valid CNF active under even renaming.
For one fixed polynomial-time recognizable union of known UNSAT families it
also appends an empty source clause.  This is an encoding counterexample, not
a legal R_mix341 inference or a SAT algorithm.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math


checks = 0


def check(ok: bool, msg: str) -> None:
    global checks
    checks += 1
    if not ok:
        raise AssertionError(msg)


def emit(n: int, clauses: list[tuple[int, ...]] | tuple[tuple[int, ...], ...]) -> bytes:
    body = "".join(" ".join(map(str, c)) + (" " if c else "") + "0\n" for c in clauses)
    return (f"p cnf {n} {len(clauses)}\n" + body).encode("ascii")


def parse(src: bytes) -> tuple[int, tuple[tuple[int, ...], ...]]:
    try:
        text = src.decode("ascii")
    except UnicodeError as exc:
        raise ValueError("nonascii") from exc
    lines = text.splitlines()
    if not lines or len(lines[0].split()) != 4 or lines[0].split()[:2] != ["p", "cnf"]:
        raise ValueError("header")
    try:
        n, m = map(int, lines[0].split()[2:])
    except ValueError as exc:
        raise ValueError("numeric header") from exc
    if n < 0 or m < 0 or len(lines) != m + 1:
        raise ValueError("length")
    clauses = []
    for line in lines[1:]:
        try:
            row = [int(x) for x in line.split()]
        except ValueError as exc:
            raise ValueError("clause integer") from exc
        if not row or row[-1] != 0 or any(x == 0 for x in row[:-1]) or any(abs(x) > n for x in row[:-1]):
            raise ValueError("clause syntax")
        clauses.append(tuple(row[:-1]))
    return n, tuple(clauses)


def php(h: int) -> bytes:
    def v(i: int, j: int) -> int:
        return i * h + j + 1
    clauses = [tuple(v(i, j) for j in range(h)) for i in range(h + 1)]
    for j in range(h):
        for i in range(h + 1):
            for k in range(i + 1, h + 1):
                clauses.append((-v(i, j), -v(k, j)))
    return emit(h * (h + 1), clauses)


def recognize_php(src: bytes) -> bool:
    try:
        n, _ = parse(src)
    except ValueError:
        return False
    h = (math.isqrt(4 * n + 1) - 1) // 2
    return h >= 1 and h * (h + 1) == n and src == php(h)


def prism_edges(k: int) -> list[tuple[int, int]]:
    edges = []
    for i in range(k):
        edges.append((i, (i + 1) % k))
    for i in range(k):
        edges.append((k + i, k + (i + 1) % k))
    for i in range(k):
        edges.append((i, k + i))
    return edges


def prism_tseitin(k: int, odd: bool) -> bytes:
    edges = prism_edges(k)
    incident = [[] for _ in range(2 * k)]
    for eid, (u, v) in enumerate(edges, 1):
        incident[u].append(eid)
        incident[v].append(eid)
    clauses: list[tuple[int, ...]] = []
    for vertex, ids in enumerate(incident):
        ids.sort()
        charge = int(odd and vertex == 0)
        for row in itertools.product((0, 1), repeat=3):
            if (sum(row) & 1) != charge:
                clauses.append(tuple(var if bit == 0 else -var for var, bit in zip(ids, row)))
    return emit(len(edges), clauses)


def recognize_odd_prism(src: bytes) -> bool:
    try:
        n, _ = parse(src)
    except ValueError:
        return False
    return n % 3 == 0 and n // 3 >= 3 and src == prism_tseitin(n // 3, True)


def recognizable_unsat(src: bytes) -> str | None:
    if recognize_php(src):
        return "PHP"
    if recognize_odd_prism(src):
        return "ODD_PRISM_TSEITIN"
    return None


def encode(src: bytes) -> bytes:
    try:
        n, clauses = parse(src)
        valid = True
    except ValueError:
        n, clauses, valid = 0, (), False
    family = recognizable_unsat(src) if valid else None
    # Active source clauses are always retained for every valid CNF.
    body = [tuple(2 * lit for lit in clause) for clause in clauses] if valid else []
    if family:
        body.append(())
    bit_count = 8 * len(src)
    for i in range(bit_count):
        bit = (src[i // 8] >> (7 - (i % 8))) & 1
        for copy in range(2):
            j = 2 * i + copy
            a = 2 * j + 1
            body.append((a if bit else -a,))
    return emit(max(2 * n, 4 * bit_count - 1, 0), body)


def decode(encoded: bytes) -> bytes:
    _, clauses = parse(encoded)
    tags: dict[int, int] = {}
    for clause in clauses:
        if len(clause) == 1 and abs(clause[0]) % 2 == 1:
            j = (abs(clause[0]) - 1) // 2
            if j in tags:
                raise ValueError("duplicate tag")
            tags[j] = int(clause[0] > 0)
    if not tags:
        return b""
    if len(tags) % 16 or set(tags) != set(range(len(tags))):
        raise ValueError("missing tag")
    bits = []
    for i in range(len(tags) // 2):
        if tags[2 * i] != tags[2 * i + 1]:
            raise ValueError("corrupt tag pair")
        bits.append(tags[2 * i])
    out = bytearray()
    for i in range(0, len(bits), 8):
        value = 0
        for bit in bits[i:i + 8]:
            value = 2 * value + bit
        out.append(value)
    return bytes(out)


def verify_image(encoded: bytes) -> bool:
    """Authenticate the complete image, not merely recover its payload."""
    try:
        src = decode(encoded)
    except ValueError:
        return False
    return encode(src) == encoded


def model_count(n: int, clauses: tuple[tuple[int, ...], ...]) -> int:
    count = 0
    for mask in range(1 << n):
        if all(any(((mask >> (abs(lit) - 1)) & 1) == int(lit > 0) for lit in clause)
               for clause in clauses):
            count += 1
    return count


def tiny_cases():
    literals = [(1,), (-1,), (2,), (-2,), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    for mask in range(256):
        yield f"2VAR_{mask:03d}", emit(2, [literals[i] for i in range(8) if (mask >> i) & 1])
    for h in (1, 2, 3):
        yield f"PHP_{h}", php(h)
    for k in (3, 4, 5):
        yield f"PRISM_{k}_ODD", prism_tseitin(k, True)
        yield f"PRISM_{k}_EVEN", prism_tseitin(k, False)
    bad = [b"", b"bad", b"\x00\xff", b"p cnf a b\n", b"p cnf 2 1\n3 0\n",
           b"p cnf 2 1\n1 2\n", b"p cnf 2 1\n1 0\n1 0\n", b"p cnf 1 0\nextra\n"]
    for i, src in enumerate(bad):
        yield f"MALFORMED_{i}", src


records = []
for name, src in tiny_cases():
    enc = encode(src)
    check(decode(enc) == src, f"roundtrip {name}")
    en, ec = parse(enc)
    try:
        n, clauses = parse(src)
        valid = True
    except ValueError:
        n, clauses, valid = 0, (), False
    family = recognizable_unsat(src) if valid else None
    active = tuple(tuple(2 * lit for lit in clause) for clause in clauses)
    check(ec[:len(active)] == active, f"active source retention {name}")
    empty_index = len(active)
    check((family is not None) == (empty_index < len(ec) and ec[empty_index] == ()), f"empty clause guard {name}")
    tag_start = empty_index + int(family is not None)
    tags = ec[tag_start:]
    check(len(tags) == 16 * len(src), f"tag count {name}")
    check(all(len(clause) == 1 and abs(clause[0]) % 2 == 1 for clause in tags), f"unit tags {name}")
    check(verify_image(enc), f"image authentication {name}")
    if valid and n <= 15:
        count = model_count(n, clauses)
        if family:
            check(count == 0, f"recognizer soundness {name}")
        if name.startswith("PRISM_"):
            k = int(name.split("_")[1])
            expected = 0 if name.endswith("ODD") else 2 ** (k + 1)
            check(count == expected, f"prism label/count {name}")
    if tags:
        corrupted = list(ec)
        row = list(corrupted[tag_start])
        row[0] = -row[0]
        corrupted[tag_start] = tuple(row)
        try:
            decode(emit(en, corrupted))
            raise AssertionError(f"accepted corrupted tag {name}")
        except ValueError:
            checks += 1
    records.append({"name": name, "valid": valid, "family": family, "input_bytes": len(src),
                    "output_bytes": len(enc), "active_clauses": len(active),
                    "has_empty_source": family is not None, "tag_clauses": len(tags),
                    "source_sha256": hashlib.sha256(src).hexdigest(),
                    "encoded_sha256": hashlib.sha256(enc).hexdigest()})


# A left inverse is not an image verifier: keep the exact payload tags but
# replace the active SAT source clause by an empty clause.  The decoder still
# recovers the source, although the target's projected model set changed.
forge_source = emit(1, [(1,)])
forge_encoded = encode(forge_source)
forge_n, forge_clauses = parse(forge_encoded)
check(forge_clauses[0] == (2,), "forge source active clause")
forged_clauses = list(forge_clauses)
forged_clauses[0] = ()
forged = emit(forge_n, forged_clauses)
check(decode(forged) == forge_source, "left inverse accepts forged active formula")
check(not verify_image(forged), "full-image verifier rejects forged active formula")
sn, sc = parse(forge_source)
en0, ec0 = parse(forge_encoded)
en1, ec1 = parse(forged)
source_models = model_count(sn, sc)
honest_assignment = {2: True}
for clause in ec0[1:]:
    if len(clause) == 1:
        honest_assignment[abs(clause[0])] = clause[0] > 0
encoded_sat = all(any(honest_assignment.get(abs(lit), False) == (lit > 0) for lit in clause)
                  for clause in ec0)
forged_sat = all(any(honest_assignment.get(abs(lit), False) == (lit > 0) for lit in clause)
                 for clause in ec1)
check(source_models == 1, "forge source SAT")
check(encoded_sat, "honest encoding SAT")
check(not forged_sat, "forged target UNSAT")


result = {
    "artifact": "RECOGNIZER-CONDITIONED-RECODING-REFEREE338",
    "checks": checks,
    "cases": len(records),
    "valid_cases": sum(r["valid"] for r in records),
    "malformed_cases": sum(not r["valid"] for r in records),
    "recognized_php": sum(r["family"] == "PHP" for r in records),
    "recognized_odd_prism": sum(r["family"] == "ODD_PRISM_TSEITIN" for r in records),
    "active_source_retained_all_valid": True,
    "roundtrip_all_byte_strings_tested": True,
    "left_inverse_is_not_image_authentication": {
        "source": "p cnf 1 1; (1)",
        "source_models": source_models,
        "honest_encoded_sat": encoded_sat,
        "forged_unsat_by_empty_source": not forged_sat,
        "decoder_recovers_source_from_forge": True,
        "full_image_verifier_rejects_forge": True,
    },
    "special_records": [r for r in records if r["family"]],
    "selected_controls": [r for r in records if r["name"] in
                          {"2VAR_000", "2VAR_003", "2VAR_255", "PRISM_3_EVEN", "MALFORMED_1"}],
    "status": {"encoder": "uniform polynomial-time and injective",
               "decoder": "left inverse only; not semantic/image verifier",
               "repair": "check G equals E(D(G)) or carry equivalent full authentication",
               "model_projection": "exact for every valid CNF",
               "fixed_rmix_prism_original": "published exact 4h-1",
               "fixed_rmix_encoded": "zero paid nodes via empty source",
               "ordinary_resolution_php_original": "published exponential",
               "ordinary_resolution_encoded": "zero paid nodes",
               "B1": "OPEN for R_mix341", "B2": "OPEN", "B3": "OPEN", "P_vs_NP": "OPEN"},
}
payload = json.dumps(result, sort_keys=True, separators=(",", ":"))
result["sha256_without_digest"] = hashlib.sha256(payload.encode()).hexdigest()
print(json.dumps(result, indent=2, sort_keys=True))
