#!/usr/bin/env python3
"""Check the five active agent manuscripts without opening retired trackers.

This is a structural workflow check, not a mathematical or LaTeX-build audit.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

MANUSCRIPTS = {
    "TMR-1": "main1_PNP_MACHINE_MODEL_LEAD.tex",
    "TMR-2": "main2_PNP_INFORMATION_NECESSITY.tex",
    "TMR-3": "main3_PNP_TIME_SPACE_TRADEOFFS.tex",
    "TMR-4": "main4_PNP_COST_SOUND_ABSTRACTION.tex",
    "TMR-5": "main5_PNP_MACHINE_BOTTLENECK_REDTEAM.tex",
}
DIRECTIVE = "research/coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md"


def inspect(root: Path) -> dict:
    errors: list[str] = []
    entries: dict[str, dict] = {}
    for required in (DIRECTIVE, "AGENTS.md", "CODEX.md", ".codex/skills/pnp-research/SKILL.md"):
        path = root / required
        if not path.is_file():
            errors.append(f"missing current workflow file: {required}")
    skill = root / ".codex/skills/pnp-research/SKILL.md"
    if skill.is_file():
        try:
            text = skill.read_text(encoding="utf-8")
            if not text.startswith("---\nname: pnp-research\n"):
                errors.append("skill front matter has the wrong name")
            parts = text.split("---", 2)
            if len(parts) < 3 or "\ndescription:" not in parts[1]:
                errors.append("skill front matter lacks description")
        except (OSError, UnicodeError) as exc:
            errors.append(f"cannot read skill: {exc}")
    for owner, filename in MANUSCRIPTS.items():
        path = root / filename
        record = {"path": filename, "exists": path.is_file(), "ownership_ok": False, "document_ok": False}
        if not path.is_file():
            errors.append(f"missing assigned manuscript: {filename}")
        else:
            try:
                text = path.read_text(encoding="utf-8")
                start = f"% BEGIN {owner} OWNED"
                stop = f"% END {owner} OWNED"
                record["ownership_ok"] = text.count(start) == 1 and text.count(stop) == 1 and text.index(start) < text.index(stop)
                record["document_ok"] = text.count("\\begin{document}") == 1 and text.count("\\end{document}") == 1 and text.index("\\begin{document}") < text.index("\\end{document}")
                record["bytes"] = len(text.encode("utf-8"))
                if not record["ownership_ok"]:
                    errors.append(f"unbalanced ownership markers: {filename}")
                if not record["document_ok"]:
                    errors.append(f"invalid document boundary markers: {filename}")
                if not text.strip():
                    errors.append(f"empty assigned manuscript: {filename}")
            except (OSError, UnicodeError) as exc:
                errors.append(f"cannot read {filename}: {exc}")
        entries[owner] = record
    return {"root": root.as_posix(), "workflow": "END_TO_END_AGENT_MANUSCRIPTS", "directive": DIRECTIVE, "manuscripts": entries, "retired_trackers_read": False, "mathematical_validation": "NOT_PERFORMED", "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="return nonzero on structural failures")
    parser.add_argument("--json", action="store_true", help="emit machine-readable status")
    args = parser.parse_args()
    state = inspect(Path(__file__).resolve().parents[4])
    if args.json:
        print(json.dumps(state, indent=2, sort_keys=True))
    else:
        print("PNP END-TO-END MANUSCRIPT PREFLIGHT")
        for owner, entry in state["manuscripts"].items():
            print(f"{owner}: {entry['path']} (exists={entry['exists']}, ownership={entry['ownership_ok']}, document={entry['document_ok']})")
        for error in state["errors"]:
            print(f"ERROR: {error}")
        print("status: FAIL" if state["errors"] else "status: OK (structural checks only)")
    return 1 if args.check and state["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
