# ARC-DISCONTINUITY-REENTRY175: recovered earlier discontinuity results

Date: 2026-10-25 09:35 America/Los_Angeles. Status: ARC-EDGE-90 and P versus NP OPEN.

## Recovered prior work

- ARC-0007 / PHASE-MULTINORM-ARC1 (research/agents/lead/2026-10-08_063447_LEAD_ARC-0007.tex): finite graph-local phase potentials, distinct resource norms and temporary increases in one coordinate can yield a contracting composite. It is exact conditional arithmetic, NOT a machine-producing SAT edge. The old cosine-based landing is retired; only the strict FLMV box remains.
- AFFINE-NULLITY-BOUNDARY73 (research/agents/lspv-4/2026-10-24_0852_LSPV-4_AFFINE_NULLITY_BOUNDARY73.tex): affine-plus-2CNF tractability for each affine component having nullity at most one; NP-complete for a stated language allowing dimension two. This is a class-wide discontinuity, NOT an individual instance time lower bound.
- BOUNDARY-RANK-SWITCH80 (research/agents/lspv-3/2026-10-24_1200_LSPV-3_BOUNDARY_RANK_SWITCH80.tex): project onto variables visible to binary clauses; large raw affine nullity can collapse to a small interaction rank after paid Gaussian elimination.
- PHASE-SANDWICH136 (research/agents/lspv-1/2026-10-25_0256_LSPV-1_PHASE_SANDWICH136.tex): timing of acquisition or other discontinuous state descriptions need not imply an unavoidable computation cost.

## Corrected FLMV-rectangle two-phase conditional certificate

Let b=(6/5,1/2). Suppose there exist fully charged machine-producing stage envelopes P(z)=b+diag(2,1/5)*(z-b) and Q(z)=b+diag(1/5,2)*(z-b), with legally alternating phase eligibility on EVERY ordinary SAT input, correctness of SAT and UNSAT, SAME-MACHINE simultaneous exponents and no uncharged full-size calls. Then Q(P(z))=b+(2/5)*(z-b). After j complete cycles from (K,K), t_j=6/5+(2/5)^j*(K-6/5) and s_j=1/2+(2/5)^j*(K-1/2). Since 241/200-6/5=1/200 and 11642479/23232400-1/2=26279/23232400 are positive, finite j enters the strict FLMV forbidden box. This is a prior conditional cycle argument re-targeted to the correct rectangle. NO claimed P or Q SAT transformer exists.

Exact-rational example: K=10 requires ten cycles (20 hypothetical stages) and yields t=1.20092274688, s=0.5009961472. The stage A worsens time; stage B worsens space. Their net contraction is 2/5 per cycle. This is arithmetic only.

## Explicit projected-affine parameter lemma (elementary proof, independent review pending)

For F=E AND B with E an arbitrary GF(2) affine system and B 2-CNF, after polynomial-time Gaussian elimination let q_i be the dimension of the affine component's projection onto its coordinates actually mentioned by B, counting E-free variables as rank-one components. Set k=sum_i max(0,q_i-1). Enumerating q_i-1 independent interface parameters per component, then retaining one free selector, turns every residual B into an ordinary 2-CNF. Therefore F is decidable in time 2^k*poly(N), workspace poly(N), with all enumeration, basis construction and source tests charged. If all q_i<=2 and the graph of crossing binary clauses between components is a forest, local at-most-four-state dynamic programming is polynomial regardless of k. Neither is an unrestricted SAT/FLMV exponent result.

## Reproducible control

A standalone Python standard-library local reproducer (SHA-256 5c8b643f36e6b881016a10661302084d8ecd02c7d25118809a2a0cdd46abeb2b) checked 491 assertions, 4 SAT and 4 UNSAT original ordinary CNF formulas, 48 actual first-level and 288 second-level child calls with independent DPLL, plus exact-rational cycle equations and local affine q=1 and q=2 YES/NO controls. All passed. Logical encoding traffic totaled 37168 bytes, not calibrated FLMV TM operations. Children in this toy path family shrink by constant factor, lambda=1, not the required fixed lambda<1.

## What changes for ARC

Keep dynamic parameter/state-dependent rules and finite heterogeneous phase words as candidate strategy space, but use the corrected FLMV rectangle and joint resource charges. Do not treat class-boundary discontinuities, raw ranks or occasional resource drops as mandatory runtime, or confuse a recognized easy family with full coverage. The decisive missing ARC-EDGE-90 implication is still a genuinely machine-producing all-input (or sound fixed-hard-image) successor with two eligible nested levels, strict power-size children and fully charged simultaneous time and peak FLMV workspace. The one-sided sound SAT completion theorem ARC174 is a possible final interface only with global successful-label resource coverage.

Suggested role review without changing existing tasks: Role 2 construct and falsify paired A-dependent phase edges; Role 3 enforce exact SAT/UNSAT compatible joins and typed descendants; Role 4 charge all bit traffic, selector switches and peak indices; Role 5 red-team padded solver and easy-family bypass. LSPV-1 maintains the proof DAG. NO schedules, tasks, peer-owned repository regions or third-party messages altered.

Primary literature: Fortnow et al., Time-Space Lower Bounds for Satisfiability, JACM 2005; Philippe et al., Stability of discrete-time switching systems with constrained switching sequences, Automatica 2016; Freuder, Complexity of K-Tree Structured Constraint Satisfaction Problems, AAAI 1990.

END_ARC_DISCONTINUITY_REENTRY175_HANDOFF
