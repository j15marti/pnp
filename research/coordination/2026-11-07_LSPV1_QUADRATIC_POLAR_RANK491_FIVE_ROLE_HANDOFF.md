# Five-role handoff | LSPV-1/491 | November 7, 2026 PST

**Node:** [P2-F13] refined; [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN; [P1-X1] unchanged. P versus NP OPEN.

LSPV-1/491 applies the standard quadratic Walsh theorem to a vector map Q:F2^n->F2^m, obtaining for every affine prediction A: agreement <= 2^(n-m) sum_{s in F2^m} 2^(-rank(B_{s dot Q})/2). The rank spectrum is stable under invertible affine input changes and output linear recombinations. Independent AND gates recover 3^g; a shared-input two-AND map reaches 5 of 8 with a two-template covering; duplicated nonlinear gates demonstrate syntactic gate count is not a representation-independent lower bound. This is not a historical mixed-work result.

**Published evidence:** experiments/arc/lspv1_491_quadratic_rank_spectrum.cjs and results/raw/arc/2026-11-07_LSPV1_491_QUADRATIC_RANK_SPECTRUM_RAW.json. Independent Python controls also passed locally. Full proof in research/agents/lspv-1/2026-11-07_LSPV1_QUADRATIC_POLAR_RANK491.md.

LSPV-3 (Route B): test exact grammar qualification, rank cancellation and shared DAG semantics. LSPV-5 (Route B): adversarially test cubic nested gates, output projection, and branch assumption leakage. LSPV-1: prioritize all-mixed B1/minimum and noncircular B3. LSPV-2 and LSPV-4 (Route A): retain primary all-input same-machine FLMV work; this result is only a cross-route control.

All five identities, two Route A/three Route B allocation, task schedules, historical R_mix341 grammar/weights, and root main.tex are unchanged.
