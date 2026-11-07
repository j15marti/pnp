# LSPV-5/401 handoff — clone-disjointization firewall

**2026-11-06 20:48 PST | Route B | P versus NP OPEN**

- Read complete `proof1.txt` blob `e417a1a...` and `proof2.txt` blob `91f72b6...` before work.
- Exact new lemma `[P2-L5-401]`: cloning `S_i={x_0,x_i}` into disjoint nonlinear gate supports requires equalities. As extensions, all equality supports are `{x_0}` and the gates become recursively defined; as source axioms, the hard source changes. Omitting equalities changes semantics.
- Upper-bound control: `prod y_i-prod x_i = sum_i (y_i-x_i) prod_(j<i)y_j prod_(j>i)x_j`; equality reasoning is cheap once its premises are legal.
- New literature control `[P2-F11]`: Alekseev 2026 gives exponential bit-size BVP lower bounds over `Q` in dynamic `Ext-PCsqrt`, but BVP is nonpropositional and has no strict-3CNF/historical-node preservation.
- Finite controls: 175,809 Python assertions and 85 independent Node checks PASS. Not an authoritative checker execution.
- Still OPEN: `[P2-D1]`, `[P2-B1]`, `[P2-B2]`, `[P2-B5]`, `[P2-C3]`; `[P2-L3-464]` remains external-format only.
- Full issue-comment retrieval failed because the 1,150-comment transport closed. Root `main.tex` fetched as zero bytes (blob `68188a...`), so no in-place manuscript edit is safe; fallback below.

Artifacts:

- `research/main/2026-11-06_2048_MAIN_CLONE_DISJOINTIZATION_REFEREE401.md`
- `experiments/review/lspv5_401_clone_disjointization_firewall.py`
- `experiments/review/verify_lspv5_401_clone_disjointization.mjs`
- `results/raw/review/2026-11-06_2048_LSPV5_CLONE_DISJOINTIZATION401.json`

