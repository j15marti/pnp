#!/usr/bin/env python3
"""Fast source audit for the canonical P-vs-NP proof-spine manuscripts.

This linter checks only documentary and accounting guards.  Passing it does
not prove any mathematical claim and does not prove P != NP.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CANONICAL = ("main4.tex", "main5.tex", "main9.tex", "main10.tex")
ALLOWED_STATUS_WORDS = (
    "PROVED/EXACT",
    "COMPUTATIONAL",
    "OPEN",
    "FALSIFIED/RETIRED",
)


def bib_keys(text: str) -> list[str]:
    return re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", text)


def cite_keys(text: str) -> set[str]:
    out: set[str] = set()
    for group in re.findall(r"\\cite(?:\[[^]]*\])?\{([^}]*)\}", text):
        out.update(key.strip() for key in group.split(",") if key.strip())
    return out


def main() -> int:
    findings: list[dict[str, object]] = []
    checked: list[str] = []
    texts: dict[str, str] = {}
    for name in CANONICAL:
        path = ROOT / name
        if not path.exists():
            findings.append({"severity": "ERROR", "file": name, "line": 0,
                             "rule": "canonical-file-present", "text": "missing"})
            continue
        text = path.read_text(encoding="utf-8")
        texts[name] = text
        checked.append(name)

        rules = (
            (r"GENERATOR-COLLAPSE1", "retired-generator-label", ()),
            (
                r"2b\s*\\le\s*h",
                "retired-output-width-guard",
                ("former", "old", "unnecessary", "remove", "artifact", "retired", "with no"),
            ),
            (r"Scoped No-Go", "invalid-status-label", ()),
            (
                r"(?:<|below)\s*2\\cos\s*\(\\pi/7\)",
                "retracted-universal-endpoint-pattern",
                ("retired", "retract", "prior formulation", "reject"),
            ),
        )
        lines = text.splitlines()
        for pattern, rule, allowed_context in rules:
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                line = text.count("\n", 0, match.start()) + 1
                context = " ".join(lines[max(0, line - 2):min(len(lines), line + 1)]).lower()
                if any(marker in context for marker in allowed_context):
                    continue
                findings.append({"severity": "ERROR", "file": name, "line": line,
                                 "rule": rule, "text": match.group(0)})

        for match in re.finditer(r"^\s*\\item(?!\[\])", text, flags=re.MULTILINE):
            line = text.count("\n", 0, match.start()) + 1
            findings.append({"severity": "ERROR", "file": name, "line": line,
                             "rule": "item-empty-label-convention", "text": "\\item"})

        required = {
            "Williams published product endpoint": r"\\varphi|\\phi",
            "Fortnow endpoint citation": r"\\cite(?:\[[^]]*\])?\{[^}]*fortnow2000",
            "open-status guard": r"\\Open|OPEN",
        }
        for label, pattern in required.items():
            if not re.search(pattern, text, flags=re.IGNORECASE):
                findings.append({"severity": "ERROR", "file": name, "line": 0,
                                 "rule": "required-claim-marker", "text": label})

    bib_path = ROOT / "spines.bib"
    bib = bib_path.read_text(encoding="utf-8") if bib_path.exists() else ""
    keys = bib_keys(bib)
    duplicate_keys = sorted({key for key in keys if keys.count(key) > 1})
    for key in duplicate_keys:
        findings.append({"severity": "ERROR", "file": "spines.bib", "line": 0,
                         "rule": "duplicate-bib-key", "text": key})
    available = set(keys)
    for name, text in texts.items():
        for key in sorted(cite_keys(text) - available):
            findings.append({"severity": "ERROR", "file": name, "line": 0,
                             "rule": "missing-bib-key", "text": key})

    status = "PASS" if not findings else "FAIL"
    result = {
        "claim": "DEFENSE-MANUSCRIPT-LINT1",
        "status": status,
        "scope": (
            "Source-level guard only. PASS does not validate theorem proofs, "
            "close the charged acquisition arrow, or decide P versus NP."
        ),
        "allowed_status_vocabulary": ALLOWED_STATUS_WORDS,
        "checked_files": checked,
        "finding_count": len(findings),
        "findings": findings,
    }
    out = ROOT / "defense_manuscript_lint_results.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "finding_count": len(findings), "output": out.name}))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
