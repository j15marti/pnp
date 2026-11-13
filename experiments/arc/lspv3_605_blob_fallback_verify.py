#!/usr/bin/env python3
"""LSPV-3/605: repeatable local Git blob/working-tree reconciliation audit.

Run in complete j15marti/pnp checkout:
    python3 experiments/arc/lspv3_605_blob_fallback_verify.py

No external libraries or network needed. Does not run either original SAT checker.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
FILES = ("proof1.txt", "proof2.txt", "main.tex")
BEGIN = "% BEGIN LSPV-3 OWNED"
END = "% END LSPV-3 OWNED"
EXPECTED_SOURCE_SHA256 = "3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c"


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def blob_hash(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


def main() -> int:
    ledger: dict = {"run": "LSPV-3/605", "mode": "local immutable Git object/HEAD comparison",
                    "mathematical_status": "P versus NP OPEN", "files": {}}
    for name in FILES:
        work_bytes = (ROOT / name).read_bytes()
        head_bytes = git("show", "HEAD:" + name)
        head_sha = git("rev-parse", "HEAD:" + name).decode().strip()
        assert blob_hash(head_bytes) == head_sha, (name, "bad HEAD object hash")
        assert head_bytes == work_bytes, (name, "uncommitted working tree mismatch")
        assert len(work_bytes) > 100, (name, "missing/truncated read")
        ledger["files"][name] = {
            "head_git_blob_sha1": head_sha, "byte_length": len(work_bytes),
            "sha256": hashlib.sha256(work_bytes).hexdigest(), "work_tree_matches_head": True
        }
    text = (ROOT / "main.tex").read_text("utf-8")
    assert text.count(BEGIN) == text.count(END) == 1, "ownership markers"
    assert text.index(BEGIN) < text.index(END), "reversed ownership region"
    assert text.count("% BEGIN LSPV-4 OWNED") == text.count("% END LSPV-4 OWNED") == 1
    owned = text[text.index(BEGIN):text.index(END)]
    assert "574_k01_SIGNED_SOURCE.cnf" in owned, "missing restored source reconciliation"
    assert "2026-11-12_2128_LSPV3_605" in owned, "missing repair citation"
    assert "P2-D1" in owned and "OPEN" in owned, "lost OPEN status"
    assert text.count("\\end{document}") == 1, "LaTeX end marker"
    src = (ROOT / "results/raw/arc/574_k01_SIGNED_SOURCE.cnf").read_bytes()
    assert hashlib.sha256(src).hexdigest() == EXPECTED_SOURCE_SHA256, "external signed SOURCE changed"
    assert (ROOT / "results/raw/arc/2026-11-12_1412_LSPV2_583_SIGNED_K4_SOURCE.cnf").read_bytes() == src
    ledger["signed_source"] = {"byte_length": len(src), "sha256": EXPECTED_SOURCE_SHA256,
                               "duplicate_583_equal": True}
    ledger["disclaimer"] = ("Repository Git blob and publication verification ONLY. "
                            "No original full R_mix341 checker, lower-bound theorem, "
                            "original Node OS execution, or full scientific preflight is claimed.")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AssertionError, OSError, subprocess.CalledProcessError) as exc:
        print("FAIL:", repr(exc), file=sys.stderr)
        sys.exit(1)
