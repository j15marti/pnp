# ARC192 | Jump-invariant reversal-space and local UNSAT certificate firewall
Date: 2026-10-26 20:56 PDT. Lead: LSPV-1. P versus NP OPEN. Independent mathematical review pending. No schedules, enabled states or peer-owned files changed.

## What was proved (strictly model- and promise-scoped)
Use the exact 15-variable/20-clause proper signed exact-(2,2) W1 gadget with two balanced sign switches from BINARY-WORK-SAT4. Its four model counts are 772,272,272,0. In the explicit left 2m variable-sign clauses, fixed 16m clauses, right 2m variable-sign clauses encoding, the m-fold disjoint source F_m(a,b) is SAT iff a and b are disjoint, with length N_m=Theta(m log m).

Fix ONE deterministic total machine correct on every F_m(a,b), with ONE read-only input head allowed target-only signed jumps of radius J (J may equal/exceed input length), and k fixed sequential work tapes. Let S count simultaneously visited work cells, T count all transitions, and R count direction reversals of all nonzero input-head displacements, including jumps. There is a YES source F_m(a,not a) on which

  (R+1) (S+log_2(N+TJ+2)+1) = Omega(m) = Omega(N/log N).

Proof: a complete two-party transcript across one Alice/fixed/Bob cut records work values, every work-head position, control, destination input-head position and read timing in O_k(S+log(N+TJ)) bits per side transfer. The 2^m YES pairs (a,not a) form a deterministic fooling set; some YES transcript has Omega(m/B) transfers. Across a single cut, side-transfer directions must alternate, even if jumps skip its physical cells, so R+1 >= transfers. For polynomial time/space/jump ceilings, r+s >= 1 is a necessary promise-family exponent condition, independently of jump exponent j. This is a **jump-invariant input-head REVERSAL bound**, NOT an input-head travel bound or any indexed-RAM time lower bound.

Separately an M_J -> Mk ordinary sequential-input simulator expands each radius-J jump into O(J+polylog) unit moves with O(log(N+TJ)) work cells, so conditional on native HEADMOVE-1 for this source, the augmented distinct-model exponent satisfies t+s+j >=2. Preserve that conditional source hypothesis, and never infer an unrestricted RAT/RAM tape product.

## Locally authenticated proof control
An UNSAT F_m with a_i=b_i=1 has a directly source-authenticated 205-record Resolution refutation using only its twenty W1 clauses, 20 original-clause pointers plus 185 binary inferences, maximum width 8. The explicit fixed record template has O(log N) physical bits for component numbering, clause/source offsets, parents and pivots. A rejecting coSAT branch can nondeterministically guess the component and verify it; deterministic all-input discovery and YES case checking remain distinct.

## Reproducibility
- report: research/agents/lspv-1/2026-10-26_2056_LSPV-1_ARC_JUMP_REVERSAL_CERT192.tex
- executable: research/agents/lspv-1/2026-10-26_2056_ARC192_jump_reversal_audit.py
- raw: research/agents/lspv-1/2026-10-26_2056_ARC192_jump_reversal_raw.json
- bibliography: research/agents/lspv-1/2026-10-26_2056_ARC192_references.bib

Python zero-dependency reproducer deterministically passed **36,536** counted assertions, **zero** failures, on all 2^15 assignment controls for each W1 variant, 126 YES fooling cases and 2,667 hostile cross pairs, 11 complete authentic Resolution transcripts, 8 genuine two-level SAT/UNSAT residuals, 180 jump/head-reversal itineraries. Source encoder, parser, two-swap quota and source-record verification included. Finite tests are not a physical time-space experiment.

## Exact role assignments
LSPV-2: complete direct ordinary-source Rank/Select/inverse sorting, charge the full source parse and its pinned twice-regularized output floor.
LSPV-3: search for locally authenticated adaptive certificate grammar covering all ordinary UNSAT, distinguish guessed NO proof from deterministic acquisition and all YES paths.
LSPV-4: independently audit the all-jumps two-party transcript, completeness of snapshots, input-head target timing, jump-to-sequential simulation, and strict same-machine FLMV transport.
LSPV-5: red-team the new reversal-vs-travel distinction with multi-input-head, indexed-work and output-materialization countermodels; synthesize status in root only with explicit review.

## Proof DAG
PROVED/EXACT RESTRICTED, **independent review pending**: W1 signed source semantics, connected machine transcript argument for one-head jumps and reversal-space, source pointer certificate.
CONDITIONAL: t+s+j >=2 requires matching native HEADMOVE sequential tape theorem.
FALSIFIED as inference: arbitrary radius-J jumps erase input-reversal cost; short NO certificate implies short deterministic all-input discovery; tape-head reversal cost lower bounds FLMV indexed SAT time.
OPEN: sound all-UNSAT affordable source-authenticated certificates; fully charged arbitrary unknown-K ARC successor on ordinary SAT; ARC-EDGE-90; P != NP.

All numerical information is native to its declared model and the same fixed machine, not a diagonal assembled from separate solvers.