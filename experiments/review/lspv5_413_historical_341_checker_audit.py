#!/usr/bin/env python3
"""LSPV-5/413: replay and scope the historical /341 producer/checker chain.

This is an audit of exact repository bytes, not a replacement grammar.
It intentionally treats the historical verifier as authoritative only for
the two rule tags that the verifier actually implements.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path


EXPECTED_SHA256 = {
    "producer": "4dd134c4e97fca273668480c64bb220201d67917c2cfe70c471a7bc785e396fc",
    "certificate": "12d723c92c683ec1a59e17d95d0d47156babe7febe27b7432dc01279abcb8d95",
    "checker": "0a8167fc65f324860f60abd2a0e0176d0def968cb6ee7055b6aa1bfd43c255ae",
    "record": "af477923155e6e4340a643a4df5b437751b443f03993bbc04dbe73c8587bf7be",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_checker(checker: Path, cert: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["node", str(checker), str(cert)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--producer", type=Path, required=True)
    ap.add_argument("--certificate", type=Path, required=True)
    ap.add_argument("--checker", type=Path, required=True)
    ap.add_argument("--record", type=Path, required=True)
    args = ap.parse_args()

    checks = 0
    def ck(value: bool, msg: str) -> None:
        nonlocal checks
        checks += 1
        if not value:
            raise AssertionError(msg)

    paths = {
        "producer": args.producer,
        "certificate": args.certificate,
        "checker": args.checker,
        "record": args.record,
    }
    hashes = {name: sha256(path) for name, path in paths.items()}
    for name, expected in EXPECTED_SHA256.items():
        ck(hashes[name] == expected, f"{name} SHA-256 drift")

    raw_bytes = args.certificate.read_bytes()
    raw = json.loads(raw_bytes)
    record = json.loads(args.record.read_text())
    ck(raw["version"] == "LSPV2-MIXED-TSEITIN-MINDAG341/v1", "version")
    ck(len(raw["fixtures"]) == 7, "fixture count")
    ck(record["checks"] == 30714, "historical record check count")

    produced = subprocess.run(
        ["node", str(args.producer)],
        text=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    ck(produced.returncode == 0, "producer exit")
    ck(json.loads(produced.stdout) == raw, "producer semantic replay")
    ck(raw_bytes == produced.stdout, "producer replay is not byte-identical")

    baseline = run_checker(args.checker, args.certificate)
    ck(baseline.returncode == 0, "checker rejected historical certificate")
    baseline_json = json.loads(baseline.stdout)
    ck(baseline_json == record, "checker output differs from historical record")

    source = args.checker.read_text()
    tags = set(re.findall(r'p\.rule==="([A-Z0-9_-]+)"', source))
    ck(tags == {"AND3", "XOR"}, f"implemented rule tags: {sorted(tags)}")
    ck('else throw Error("unknown rule")' in source, "unknown rule is not closed")
    ck('src.set(c.id,{kind:"factor"' in source, "source clause-to-factor coercion absent")
    ck('a.kind==="factor"&&b.kind==="factor"&&p.kind==="factor"' in source,
       "AND3 factor typing absent")
    ck('a.row&&b.row&&p.row&&p.kind==="affine"' in source, "XOR row typing absent")
    for absent in ("RES", "LOCAL-CONVERT", "DEF"):
        ck(f'p.rule==="{absent}"' not in source, f"unexpected {absent} implementation")

    mutations = {}
    for tag in ("RES", "LOCAL-CONVERT", "DEF"):
        changed = json.loads(json.dumps(raw))
        changed["fixtures"][0]["proof"][0]["rule"] = tag
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(changed, tmp)
            tmp_path = Path(tmp.name)
        try:
            got = run_checker(args.checker, tmp_path)
        finally:
            tmp_path.unlink(missing_ok=True)
        ck(got.returncode != 0, f"{tag} mutation accepted")
        ck("unknown rule" in got.stderr, f"{tag} rejected for unexpected reason")
        mutations[tag] = {
            "accepted": False,
            "reason": next(
                (line.strip() for line in got.stderr.splitlines() if "unknown rule" in line),
                "unknown rule",
            ),
        }

    summaries = []
    for fixture in raw["fixtures"]:
        summaries.append({
            "name": fixture["graph"]["name"],
            "variables": fixture["properties"]["variables"],
            "sourceClauses": fixture["properties"]["sourceClauses"],
            "proofNodes": len(fixture["proof"]),
            "ruleTags": sorted({node["rule"] for node in fixture["proof"]}),
            "oddUnsat": fixture["properties"]["oddUnsat"],
            "evenSat": fixture["properties"]["evenSat"],
        })
        ck(set(summaries[-1]["ruleTags"]) <= {"AND3", "XOR"}, "unexpected exhibited tag")

    result = {
        "run": "LSPV-5/413",
        "status": "PROVED/EXACT historical-chain scope; COMPUTATIONAL replay",
        "hashes": hashes,
        "producer": {
            "semanticEqual": True,
            "byteIdentical": True,
        },
        "historicalChecker": {
            "baselineAccepted": True,
            "recordChecks": record["checks"],
            "implementedRuleTags": sorted(tags),
            "sourceCoercion": "original clause -> factor",
            "AND3": "factor x factor -> factor",
            "XOR": "row-bearing parents -> affine",
            "unimplementedDeclaredTags": ["RES", "LOCAL-CONVERT", "DEF"],
            "crossRuleRESIntoAND3": "not representable/decided by this checker",
        },
        "mutations": mutations,
        "fixtures": summaries,
        "auditAssertions": checks,
        "conclusion": (
            "The historical chain authenticates the exhibited source/AND3/XOR "
            "Tseitin certificates, but it is not a full R_mix341 accepted-byte checker."
        ),
        "open": ["P2-D1", "P2-C3", "P2-B1", "P2-B2"],
        "pVsNP": "OPEN",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
