#!/usr/bin/env python3
"""Preflight checks and current-state summary for the pnp-research Codex skill."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


AGENTS = ("lspv-1", "lspv-2", "lspv-3", "lspv-4")


def latest(paths: list[Path]) -> str | None:
    if not paths:
        return None
    return sorted(paths, key=lambda p: p.name)[-1].as_posix()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="exit nonzero on any invariant failure")
    parser.add_argument("--json", action="store_true", help="emit machine-readable state")
    args = parser.parse_args()

    here = Path(__file__).resolve()
    root = here.parents[4]
    errors: list[str] = []

    living = root / "main.tex"
    if not living.exists() or living.stat().st_size < 500:
        errors.append("repository-root main.tex is missing or suspiciously small")

    mains = [p for p in root.rglob("main.tex") if ".git" not in p.parts]
    if mains != [living]:
        errors.append("there must be exactly one main.tex and it must be at repository root")

    skill = root / ".codex" / "skills" / "pnp-research" / "SKILL.md"
    if not skill.exists():
        errors.append("pnp-research SKILL.md is missing")
    else:
        text = skill.read_text(encoding="utf-8")
        if not text.startswith("---\nname: pnp-research\n"):
            errors.append("SKILL.md front matter is missing expected skill name")
        if "\ndescription:" not in text.split("---", 2)[1]:
            errors.append("SKILL.md front matter lacks description")

    for required in ("AGENTS.md", "CODEX.md"):
        if not (root / required).exists():
            errors.append(f"{required} is missing")

    ownership: dict[str, bool] = {}
    if living.exists():
        text = living.read_text(encoding="utf-8")
        for i in range(1, 5):
            ok = (
                text.count(f"% BEGIN LSPV-{i} OWNED") == 1
                and text.count(f"% END LSPV-{i} OWNED") == 1
            )
            ownership[f"LSPV-{i}"] = ok
            if not ok:
                errors.append(f"main.tex LSPV-{i} ownership markers are not balanced")

    state = {
        "root": root.as_posix(),
        "main_tex": living.relative_to(root).as_posix() if living.exists() else None,
        "main_tex_size": living.stat().st_size if living.exists() else None,
        "latest_historical_main": latest(list((root / "research" / "main").glob("*.tex"))),
        "latest_agents": {
            agent: latest(list((root / "research" / "agents" / agent).glob("*.tex")))
            for agent in AGENTS
        },
        "ownership_markers": ownership,
        "errors": errors,
    }

    if args.json:
        print(json.dumps(state, indent=2, sort_keys=True))
    else:
        print("PNP RESEARCH PREFLIGHT")
        print(f"root: {state['root']}")
        print(f"living main: {state['main_tex']} ({state['main_tex_size']} bytes)")
        print(f"latest historical main: {state['latest_historical_main']}")
        for agent, path in state["latest_agents"].items():
            print(f"latest {agent}: {path}")
        if errors:
            print("errors:")
            for err in errors:
                print(f"  - {err}")
        else:
            print("status: OK")

    return 1 if (args.check and errors) else 0


if __name__ == "__main__":
    raise SystemExit(main())
