#!/usr/bin/env python3
"""LSPV-5/418: JSON string-escape identity audit of recovered /341 checker."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / "replay/413/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json"
CHECKER = ROOT / "replay/413/lspv2_341_independent_verify.js"
OUT = ROOT / "results/raw/review/2026-11-07_1448_LSPV5_JSON_STRING_ESCAPE_ALIAS418.json"
SENTINEL = "__LSPV5_418_SENTINEL__"
STRING_TOKEN = re.compile(r'"(?:\\["\\/bfnrt]|\\u[0-9a-fA-F]{4}|[^"\\\x00-\x1f])*"')


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def replace_once(raw: str, old: str, new: str) -> str:
    if raw.count(old) != 1:
        raise AssertionError(f"target count {raw.count(old)} for {old!r}")
    return raw.replace(old, new, 1)


def value_token(base, path, raw_token: str) -> str:
    obj = json.loads(json.dumps(base))
    cur = obj["fixtures"][0]
    for step in path[:-1]:
        cur = cur[step]
    cur[path[-1]] = SENTINEL
    raw = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
    return replace_once(raw, json.dumps(SENTINEL), raw_token)


def key_token(base, object_path, key: str, raw_key_token: str) -> str:
    obj = json.loads(json.dumps(base))
    cur = obj["fixtures"][0]
    for step in object_path:
        cur = cur[step]
    value = cur.pop(key)
    cur[SENTINEL] = value
    raw = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
    return replace_once(raw, json.dumps(SENTINEL), raw_key_token)


def canonical_strings(raw: str) -> tuple[bool, int, str]:
    try:
        json.loads(raw)
    except json.JSONDecodeError as exc:
        return False, 0, f"parse:{exc.msg}"
    count = 0
    for match in STRING_TOKEN.finditer(raw):
        token = match.group(0)
        decoded = json.loads(token)
        canonical = json.dumps(decoded, ensure_ascii=False, separators=(",", ":"))
        if token != canonical:
            count += 1
    return count == 0, count, ""


def run_checker(raw: str):
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as fh:
        fh.write(raw)
        name = fh.name
    try:
        cp = subprocess.run(
            ["node", str(CHECKER), name], capture_output=True, text=True, timeout=30
        )
        return {
            "accepted": cp.returncode == 0,
            "returncode": cp.returncode,
            "stdout_sha256": sha256(cp.stdout.encode()),
            "stderr_first_line": cp.stderr.splitlines()[0] if cp.stderr else "",
        }
    finally:
        Path(name).unlink(missing_ok=True)


def main():
    base = json.loads(PACKET.read_text())
    compact = json.dumps(base, separators=(",", ":"), ensure_ascii=False)
    baseline = run_checker(compact)
    baseline_canonical = canonical_strings(compact)
    if not baseline["accepted"] or not baseline_canonical[0]:
        raise AssertionError("baseline failed")

    specs = [
        ("source_definition_escape_same", "value", ["clauses", 0, "id"], r'"\u0073\u0030"', True),
        ("source_reference_escape_same", "value", ["proof", 0, "parents", 0], r'"\u0073\u0030"', True),
        ("derived_definition_escape_same", "value", ["proof", 0, "id"], r'"\u0064\u0030"', True),
        ("derived_reference_escape_same", "value", ["proof", 1, "parents", 0], r'"\u0064\u0030"', True),
        ("source_definition_escape_different", "value", ["clauses", 0, "id"], r'"\u0078\u0030"', False),
        ("source_reference_escape_different", "value", ["proof", 0, "parents", 0], r'"\u0078\u0030"', False),
        ("derived_definition_escape_different", "value", ["proof", 0, "id"], r'"\u0078\u0030"', False),
        ("derived_reference_escape_different", "value", ["proof", 1, "parents", 0], r'"\u0078\u0030"', False),
        ("id_key_escape_same", "key", ["clauses", 0], r'"\u0069\u0064"', True),
        ("id_key_escape_different", "key", ["clauses", 0], r'"\u006a\u0064"', False),
        ("parents_key_escape_same", "key", ["proof", 0], r'"\u0070\u0061\u0072\u0065\u006e\u0074\u0073"', True),
        ("parents_key_escape_different", "key", ["proof", 0], r'"\u0071\u0061\u0072\u0065\u006e\u0074\u0073"', False),
        ("malformed_unicode_escape", "value", ["clauses", 0, "id"], r'"\uZZZZ"', False),
    ]

    cases = []
    for name, mode, path, raw_token, expected in specs:
        raw = value_token(base, path, raw_token) if mode == "value" else key_token(base, path, "id" if "id_key" in name else "parents", raw_token)
        result = run_checker(raw)
        lexical_ok, noncanonical_count, lexical_error = canonical_strings(raw)
        result.update({
            "name": name,
            "mode": mode,
            "path": path,
            "raw_token": raw_token,
            "expected_checker_accept": expected,
            "canonical_string_spelling": lexical_ok,
            "noncanonical_string_tokens": noncanonical_count,
            "lexical_error": lexical_error,
            "raw_sha256": sha256(raw.encode()),
            "raw_bytes": len(raw.encode()),
            "same_stdout_as_baseline": result["stdout_sha256"] == baseline["stdout_sha256"],
        })
        if result["accepted"] != expected:
            raise AssertionError(f"unexpected checker result: {result}")
        if lexical_ok:
            raise AssertionError(f"strict canonical spelling accepted mutation: {name}")
        if expected and not result["same_stdout_as_baseline"]:
            raise AssertionError(f"accepted alias changed checker output: {name}")
        cases.append(result)

    record = {
        "experiment": "LSPV-5/418 JSON string-escape identity audit",
        "timestamp_pst": "2026-11-07 14:48 PST",
        "status": "COMPUTATIONAL/PROVED-RESTRICTED",
        "scope": "recovered SOURCE/AND3/XOR checker only",
        "packet": str(PACKET.relative_to(ROOT)),
        "packet_sha256": sha256(PACKET.read_bytes()),
        "checker": str(CHECKER.relative_to(ROOT)),
        "checker_sha256": sha256(CHECKER.read_bytes()),
        "baseline": baseline,
        "baseline_canonical_string_spelling": baseline_canonical[0],
        "case_count": len(cases),
        "accepted_count": sum(c["accepted"] for c in cases),
        "rejected_count": sum(not c["accepted"] for c in cases),
        "canonical_spelling_rejection_count": sum(not c["canonical_string_spelling"] for c in cases),
        "cases": cases,
        "limitations": [
            "No satisfiable source or shorter refutation is produced.",
            "RES, LOCAL-CONVERT, DEF facets, branching and full historical grammar remain unauthenticated.",
            "Canonical packet spelling is a proposed repaired language, not a recovered historical production.",
            "Finite parser behavior is not a proof-size or arbitrary-algorithm lower bound.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({
        "status": "PASS",
        "cases": len(cases),
        "accepted": record["accepted_count"],
        "rejected": record["rejected_count"],
        "canonical_rejected": record["canonical_spelling_rejection_count"],
        "baseline_stdout_sha256": baseline["stdout_sha256"],
        "output": str(OUT.relative_to(ROOT)),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
