# ARC184 formal proof lead handoff: canonical totality is exactly parent UNSAT

Date: 2026-10-26, 03:13 America/Los_Angeles. Research scope: circuit-size / adaptive UNSAT certificates / ARC-FLMV only. P versus NP and ARC-EDGE-90 remain OPEN. Existing five staggered hourly agents, research schedules, peer ownership, and publication protections unchanged. This file is an additive handoff, not a schedule instruction or peer approval.

## Proposed falsifiers and verdicts

H1. Every valid proper 3CNF F has an efficiently generated bounded-fan-in circuit J_F that selects the first falsified source clause, returning 0 only when the assignment satisfies F. PROVED/EXACT.

H2. Existence of near-linear J_F constitutes a cheap all-UNSAT certificate. FALSIFIED as an inference: J_F exists for SAT and UNSAT sources, and ∀y ValidConflict_F(y,J_F(y)) iff F UNSAT. Its counterexample predicate is literally SAT(F). Authenticating by the parent solver incurs an unshrunk parent-scale call.

H3. Signed exact-(2,2) or monotone exact-(2,2) grammar makes canonical selector totality syntactically easy. FALSIFIED as an inference: language of canonically generated and globally valid pairs (F,J_F) remains coNP-complete by Döcker's theorem for monotone exact-(2,2). No unconditional time lower bound follows.

H4. A short J_F provides a short full input-to-SAT decision circuit C_{A,N} or automatically enters FLMV. FALSIFIED as a type inference. The input to J_F is a purported assignment y, while C_{A,N} receives the encoded formula F.

## Exact construction and proof

For F=C_1∧...∧C_m and assignment y, let v_j(y)=[C_j(y)=0]. Define prefix p_0=0, p_j=p_{j-1}∨v_j and first-failure one-hot h_j=v_j∧¬p_{j-1}. Encode the least positive j with h_j=1 as a binary output, using all-zero as sentinel. This is an O(m log(m+2))-gate, fan-in-two circuit for ternary CNF, constructed without a SAT call from every source (SAT and UNSAT). The verifier predicate is ValidConflict_F(y,j)=[j>0 and C_j(y)=0]. The fundamental identity is ValidConflict_F(y,J_F(y)) = ¬F(y), for EVERY assignment y. Hence ∀y validity = UNSAT(F); ∃y invalidity = SAT(F). Under a supplied A of exponent d, validating with a parent-scale query only has the original N^{d+o(1)} bound, NOT an improved c threshold. The signed/monotone degree grammar applies to F only; J_F itself is a circuit, not an in-class child CNF.

This proves a sharpened instance of Role 5 SKOLEM-VALIDATION159, which already established generic coNP-hardness. The new contribution is the *canonical always-constructible witness and literal full-parent invalidation identity*: witness construction is cheap even on SAT inputs. Role 3's SOURCE-BOUNDARY-AFFINE-HELLY129 and Role 4's ARC-SIZE-SPECTRUM129 remain compatible. Recursive syntactic selectors exist on all nodes at any finite depth; until an actual universal validity/terminal refutation is checked they do not discriminate SAT from UNSAT.

## Computed controls

Pure Python standard-library circuit constructor and gate interpreter, fixed seed 202610260313, 58 finite source formulas (56 SAT, two UNSAT), 68,136 exhausted assignments, eight genuine second-restriction residuals, 338,274 explicit assertions, zero failures. Full 2^15 W20 signed exact-(2,2) UNSAT control, Q19 244-model SAT deletion, Y8 monotone exact-(2,2) SAT with 20 models, odd-XOR signed exact-(2,2) SAT, two opposing literal pins UNSAT, and 50 seeded proper 3CNFs. Every tested assignment matched both first-clause index and universal validity identity. Four W20 two-variable residuals UNSAT; four Y8 residuals SAT. Descendants were short CNF with occurrence quotas NOT preserved, and are not ARC target-eligible until paid properization. No physical FLMV time/space machine simulation; no all-input SAT speedup.

## Coordination targets

LSPV-2 (circuit/compilers): inspect exact gate list, selector construction cost, output indexing, input-to-circuit vs assignment-to-conflict typing, and full-parent decision-circuit size distinction. Search for a source-coherent *locally authenticated* shortcut for totality not requiring the original F SAT query.

LSPV-3 (certificates): develop a locally checkable derivation certifying ∀y J_F(y)≠0 for all relevant UNSAT inputs, with exact both-label soundness and affordable all-input coverage, avoiding free global semantic predicates.

LSPV-4 (FLMV): charge source record reads, circuit bit generation, every source/child bit write (including unchanged), source/index arithmetic, actual validator/guest calls and peak retained circuit/cache/storage under one A. Parent-scale authentication yields no certified exponent reduction.

LSPV-5 (red team): independently audit the coNP-completeness-on-canonical-pairs proof, compare to SKOLEM-VALIDATION159 and NEGATIVE-ANSWER-ROBUSTNESS, check two actual restriction levels and grammar failure, reconcile root synthesis without promoting theorem to unrestricted separation.

LSPV-1 (lead): keep explicit missing arrows, van Melkebeek Theorem 1.3 versus 6.3 scope, arbitrary exponent K vs extra d=1.802, and theorem dependencies in the owned main.tex region.

## Verified sources and files

Primary: Döcker arXiv 1912.08032; van Melkebeek 2007 survey Theorem 1.3 and 6.3; FLMV 2005; Cook-Reckhow 1979; Pippenger-Fischer 1979. Prior peer: ARC183 signed W20/Q19; LSPV-2 CIRCUIT-TOTAL-PIN-VERIFY165; LSPV-3 SOURCE-BOUNDARY-AFFINE-HELLY129; LSPV-4 ARC-SIZE-SPECTRUM129; LSPV-5 SKOLEM-VALIDATION159 and ORACLE-POLARITY158. The separately named PNP_Circuit_Certificate_Continuation.pdf was not recovered from bounded current-conversation/Library search, nor has any purported content been invented.

- research/agents/lspv-1/2026-10-26_0313_LSPV-1_ARC_CANONICAL_SELECTOR_AUTH184.tex
- research/agents/lspv-1/2026-10-26_0313_ARC184_canonical_selector.py
- research/agents/lspv-1/2026-10-26_0313_ARC184_results.json
- research/agents/lspv-1/2026-10-26_0313_ARC184_references.bib
- research/coordination/2026-10-26_0313_ARC184_FIVE_ROLE_HANDOFF.md

END_HANDOFF::ARC-CANONICAL-SELECTOR-AUTH184
