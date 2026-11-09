# LSPV-5/469 local validation limitation and durable fallback

**2026-11-09 14:59 PST | exact limitation recorded; GitHub publication/readback remains verified**

After the verified GitHub publication, the prescribed local commands were attempted in `/workspace/scratch/356568f234f0`:

```text
python .codex/skills/pnp-research/scripts/preflight.py
python scripts/check_research_reports.py
python .codex/skills/pnp-research/scripts/preflight.py --check
```

The scratch directory is not a full repository checkout.  The first command reported that root `main.tex`, `AGENTS.md`, `CODEX.md`, and the locally expected skill path were absent; the second command failed because `scripts/check_research_reports.py` was absent.  Therefore no local preflight/report-checker success is claimed, and the chained final `--check` did not execute.

Durable fallback actually completed before this limitation was discovered:

- complete governing files, trackers, peer reports and skill text were fetched through authenticated GitHub reads at immutable SHAs;
- both independent experiments executed locally and passed their stated finite checks;
- content commit `d94ea44e60e478a7cb58eaa671c82071cec2a036` and receipt commit `2c5405ffaacc896540f3d373a64c942a11311ddc` were lease-protected;
- all role-owned blobs were fetched back and compared byte-for-byte;
- complete `proof2.txt` prefix preservation and one-node count were verified;
- complete 1,834,859-character `main.tex` was fetched by blob, with exactly one `REFEREE469` and exact equality of all bytes outside the LSPV-5 markers;
- issue #3 comment `6753747659` was fetched and matched exactly.

This fallback verifies publication integrity, not the unavailable repository-wide local checker.  `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]`, B3 and P versus NP remain **OPEN**.
