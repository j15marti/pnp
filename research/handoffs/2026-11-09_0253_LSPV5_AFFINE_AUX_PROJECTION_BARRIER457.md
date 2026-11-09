# LSPV-5/457 handoff — pure-affine auxiliary projection barrier

**2026-11-09 02:53 PST | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

New node `[P2-L5-457]` extends `[P2-L1-530]`: for odd $q\ge3$, boundary count $b\ge3$, let $S$ be the valid one-hot modular fiber and $U$ all one-hot tuples. If an arbitrary affine system $Ax+By=d$ has some auxiliary lift for every $s\in S$, then its visible projection is affine, contains $\operatorname{aff}(S)=\operatorname{aff}(U)$, and therefore also lifts every wrong tuple in $U$. Arbitrary fresh linear auxiliaries, widths and sharing do not rescue a **pure GF(2)-affine** separator.

Do not overextend: LSPV-3/530's nonlinear three-state modular adder is a linear-size hostile upper control and escapes the hypothesis. Full nonlinear historical `R_mix341` normalization, `[P2-B1]` and `[P2-B2]` remain OPEN. No grammar/weight/task/schedule/allocation change.

Artifacts: `research/agents/lspv-5/2026-11-09_0253_LSPV5_AFFINE_AUX_PROJECTION_BARRIER457.md`; `experiments/review/lspv5_457_affine_aux_projection_audit.py`; `experiments/review/verify_lspv5_457_affine_aux_projection.js`; `results/raw/arc/2026-11-09_0253_LSPV5_457_AFFINE_AUX_PROJECTION_RAW.json`.

Next decisive red-team target: determine whether historical paid nonlinear definitions plus native GF(2) rows can simulate the compact modular-state chain with authenticated original-source provenance and exact weights; any lower-bound transfer must survive that shortcut rather than ban it.
