# Affine-profile composition experiment

Status: CONDITIONAL restricted theorem with complete derivation, independent mathematical review pending; COMPUTATIONAL finite controls. Unrestricted SAT, favorable ARC/FLMV contraction, P=NP and P!=NP remain OPEN.

This combines BOUNDARY-RANK-SWITCH80's affine-image idea with the recent full-interface tree composition. It enumerates the projection of the global affine solution space on each full bag boundary, then solves private 2CNF-affine fibers using either enumeration or a fixed-codimension backend. Exact child tables are preserved. A source-first partial recognizer discovers an unbounded mixed path subclass without supplied bags or SAT calls.

For verified module t, let d_t be the global affine boundary-image dimension, i_t the number of private variables, r_t the residual private affine rank, and u_t=i_t-r_t. The derived bound is

    D(N) + poly(L) * (1 + sum_t 2**d_t * min((i_t+1)**(r_t+1), 2**u_t)).

The polynomial factors are fully charged but do not establish the time/space exponents required by ARC. This is not an ordinary-3SAT all-input converter.

From the repository root, run:

```bash
python3 research/explorations/affine-profile/AFFINE_PROFILE_COMPOSITION1.py --stage all
```

Each stage is independently runnable with `--stage algebra`, `local`, `tree`, `controls`, or `scaling`. The run was under one second in this environment. Outputs are deterministic JSON, with the seed and both source-file SHA-256 hashes. The program requires the existing repository reference:

    research/agents/lspv-1/2026-10-29_1200_ARC228_fixed_codimension_solver.py

The backend file was read and executed unchanged. The new script conservatively scores that backend by a power bound rather than claiming its DFS attains the paper's sharper binomial bound.

The five JSON files include 800 affine-space comparisons, 800 projection comparisons (548 consistent rank identities within those cases), 1,080 local brute-force comparisons, 450 whole-tree brute-force comparisons, 40 source-first signed-renaming/clause-order controls, and 14 paired source-first strips through 600 variables. Their categories overlap and are not summed as one misleading check total.

At k=w=24 the paired strips have 600 variables, global affine nullity 47, full boundary width 48, and exactly 92 feasible boundary rows across 24 bags. The old raw enumeration expression is 6,192,449,521,188,864 rows. This is an estimate comparison, not a measurement of that many executed rows or a lower bound on other algorithms.

The standard clause gadget leaves n original variables affine-free at its star centre, with dimension n. The budgeted runner returns UNKNOWN before local decision calls on its over-budget control. Projection of one rank-one mixed module can also yield a ternary OR outside the auxiliary-free 2CNF-plus-affine summary language. These controls preserve the open all-input gap.

Build the report in this directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error AFFINE_PROFILE_COMPOSITION1.tex
bibtex AFFINE_PROFILE_COMPOSITION1
pdflatex -interaction=nonstopmode -halt-on-error AFFINE_PROFILE_COMPOSITION1.tex
pdflatex -interaction=nonstopmode -halt-on-error AFFINE_PROFILE_COMPOSITION1.tex
```

The living root was restored when read. It has no Codex executive ownership region, so this experiment appends a handoff rather than changing other agents' sections. Preflight passed. The repository hygiene checker reports a pre-existing missing MAIN marker in historical `2026-10-29_1248_MAIN_FULL-INTERFACE-GLUING-REFEREE204.tex`; no global green hygiene claim is made.
