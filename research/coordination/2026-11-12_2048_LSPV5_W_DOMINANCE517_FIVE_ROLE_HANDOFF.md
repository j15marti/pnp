# LSPV-5/517 five-role handoff: accepted paid counts are upper bounds only (guarded-K4 /386)

**2026-11-12 20:48 PST | LSPV-5 Independent Proof Red Team, historical Route B | PROVED/EXACT (restricted to the pinned spec and checker) + COMPUTATIONAL native OS | P versus NP OPEN.**

**Finding.** On the single guarded K4 Tseitin source (17 signed clauses), the unchanged /386 CLI (Git blob `338305c0ce101704205e57543756b8127074a986`) **accepts** two inflated packets:

- the literal tree-unrolled W38 (index-23 RES duplicated), with paid **39**;
- W29 plus one dead duplicate RES, with paid **30**.

W38 has the same spec as W29. Its two extra gates, 9=8∧8 and 10=9∧9, are idempotent copies. W29's own gate 8=1∧4 has zero DEF views and is dead.

Deleting that dead gate gives 28 RES and paid 28. The unchanged core accepts it. The CLI rejects it only through the known LSPV-1/590 `gate_defs.shift()` sentinel.

A Davis–Putnam sweep over all 5,040 elimination orders gives a minimum cone of 28 RES at order (1,2,4,3,5,6,7). That cone is **byte-identical** to the dead-gate-deleted W29.

Conclusion: native `paid` values are upper bounds on the inner min of W̄_R and never lower-bound witnesses. **FALSIFIED/RETIRED:** reading accepted W29, W30, W38 or W39 as min cost. The shared-DAG minimum on this source being below 28 remains OPEN.

**Peer closure.**
- LSPV-3/604 runner: native OS exit 0 (W29 accept, 3,542 assertions, pivot-999 hostile rejected).
- LSPV-4/576 `--native`: exit 0 (W38, unfolded 39, /341 and /386 CLIs exit 0).

Both "not OS executed" gaps are closed. The `main.tex` and `proof2.txt` readability blocker that LSPV-3/604 reported was connector-side: both files are readable in a git checkout of `4127667e`.

**Bridge red team.** For R=Resolution, Haken and Urquhart make the bridge SAT∈P ⇒ W̄_R ≤ poly equivalent to P≠NP. It is weak only for strong R. Pich–Santhanam (arXiv:2405.02232) is the nearest literature instance, "EF not p-bounded ⇒ P≠NP", and it holds only under extra hypotheses (CONDITIONAL).

**Requests by role (suggestions; boundaries unchanged):**
- **LSPV-1 (A):** formalize a "certified-minimum only" admissibility rule for the inner min.
- **LSPV-2 (A):** exact shared-DAG minimum on the guarded K4 source (is it below 28?).
- **LSPV-3 (B):** apply cone pruning and idempotent-gate elimination to every accepted fixture before citing its cost.
- **LSPV-4 (A):** keep W38 labelled "accepted, non-minimal".
- **LSPV-5 (B):** extend the dominance audit to /341 fixtures.

**Artifacts:**
- `research/agents/lspv-5/2026-11-12_2048_LSPV5_NATIVE386_W_DOMINANCE_REDTEAM517.tex`
- `experiments/review/lspv5_517_w_dominance_redteam.py`
- `experiments/review/lspv5_517_w_dominance_native.cjs`
- `results/raw/review/2026-11-12_2048_LSPV5_517_*.json`

These are pushed to session branch `ccr-1695bd63-51orq6`, pending owner merge to main.

**TRACKERS REVIEWED; ONE ENTRY ADDED ([P2-L5-517]).** Five roles, titles, schedules, the TWO Route A / THREE Route B allocation and the historical weights are unchanged. P2-D1, P2-C3, P2-B1 OPEN; P2-B2/B3 separately OPEN; P versus NP OPEN.
