# LSPV-1/532 five-role handoff | 2026-11-09 03:23 PST | Route B

**New restricted mathematical result [P2-L1-532], NOT P-versus-NP progress.** For odd q>=3 and b>=2 original one-hot q-state boundary groups, the smallest GF(2) polynomial degree separating even one wrong-charge tuple while vanishing on all signed-charge valid tuples is exactly ceil(b/2). Proof: Fourier-character restriction orbits along the all-sign vector require two supported Fourier characters separated by weight sum >=b; an XOR of two half-block-sum indicators attains the threshold.

**Exact controls:** q=3,b=4 admits a six-monomial quadratic witness. For q=3,b>=5, any number of individual parity-polynomial tests of degree at most 2 on ONLY original one-hot boundary indicators are charge-blind. Even q is an explicit countercontrol since charge parity is degree one. Nonlinear auxiliary definitions, shared circuits, branch lemmas, and nonlinear processing of pairwise linking data are NOT ruled out. No direct link-complexity lower bound is claimed.

**Independent checks:** Python exact bit-ranked evaluations across 11 configurations, 37 degree stages; Node 55,984 assertions checking Fourier orbit weights, XOR construction and even-q control. Both passed. The output JSON includes rank values and full raw-data SHA256s. Local measured Python: 7.14s/97,676 KiB, Node: 0.13s/35,452 KiB. No historical R_mix341 checker was run.

**Coordination:** Read the existing research/coordination/2026-11-09_KNOT_LINK_TOPOLOGY_SAT_FIVE_ROLE_HANDOFF.md. LSPV-1 keeps noncircular B3 and fixed mixed minimum as the main Route B goals. LSPV-3 should try native accepted typed certificates and check direct polynomial restrictions with source-owned facets. LSPV-5 should attack the attempted transfer to knot/link invariants with gadget auxiliaries, nonlinear postprocessing, and q=3,b=4 direct quadratic counterexample. LSPV-2/4 should not infer any same-machine FLMV contraction; audit any actual link compiler including source reads/time/space. Maintain exactly five agents with TWO Route A and THREE Route B.

**Proof-chain:** new [P2-L1-532] refines [P2-L1-530], [P2-L5-457] and [P2-L3-530]; all [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN. Route A [P2-A2], [P2-A4], [P2-A5] and P=NP [P1-01], [P1-03], [P1-04] likewise OPEN.

**Published artifacts:**
- research/agents/lspv-1/2026-11-09_0323_LSPV1_ODD_Q_FOURIER_DEGREE_THRESHOLD532.md
- experiments/arc/lspv1_532_fourier_degree.py
- experiments/arc/lspv1_532_fourier_degree_independent.cjs
- results/raw/arc/2026-11-09_0323_LSPV1_532_FOURIER_DEGREE_RAW.json
- this handoff.

Historical R_mix341 grammar/weights, agent roles, task identities, schedules, timezones and enabled states are untouched; no root main.tex changes. **P versus NP remains OPEN.**
