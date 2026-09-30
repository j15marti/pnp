#!/usr/bin/env python3
"""Basic repository hygiene checks for active LSPV LaTeX reports."""

from __future__ import annotations

from pathlib import Path
import sys


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    bad = False

    for path in sorted((root / "research").rglob("*.tex")):
        text = path.read_text(encoding="utf-8")
        if len(text.strip()) < 200:
            fail(f"{path.relative_to(root)} is suspiciously small")
            bad = True

        rel = path.relative_to(root).as_posix()
        if rel.startswith("research/main/"):
            if "MAIN SNAPSHOT" not in text or "END_OF_VERIFIED_MAIN" not in text:
                fail(f"{rel} lacks MAIN verification markers")
                bad = True

        for agent in ("lspv-1", "lspv-2", "lspv-3", "lspv-4"):
            prefix = f"research/agents/{agent}/"
            if rel.startswith(prefix):
                number = agent.split("-")[1]
                if f"LSPV-{number} REPORT" not in text:
                    fail(f"{rel} lacks LSPV-{number} report marker")
                    bad = True
                if f"END_OF_VERIFIED_REPORT::LSPV-{number}" not in text:
                    fail(f"{rel} lacks LSPV-{number} sentinel")
                    bad = True

    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
