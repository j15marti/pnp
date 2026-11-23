# Cooperative multi-technique residual research protocol
Timestamp: 2026-11-23 09:30 PST. Constructive meta-algorithm agent. Linked to issue #324.

## Directive
Do NOT treat affine/Gaussian, 2-SAT SCC, matching, component and articulation separation, treewidth, symmetry, clause learning, constraint-language polymorphisms, kernelization, and structural backdoors as mutually exclusive portfolio alternatives. Run every applicable, budgeted technique on the SAME residual; retain technique-specific evidence even when no immediate verdict follows. Cross-feed sound results and re-run until no certified improvement remains or the budget is exhausted. Then branch with exact fallback. Distinguish proof of correctness from proof of polynomial worst-case cost.

## State and interface
A residual state is (F, assumptions, provenance DAG, certified facts, representations, cache). Each technique i returns (status, deductions, representation, certificate, cost, dependencies) where status is SAT, UNSAT, PROGRESS, or NO_CHANGE. A certificate checker must establish SAT/UNSAT or equisatisfiability/entailed deductions before modifying the authoritative residual. Speculative structural scores are advisory and must never delete solutions. For branching, preserve OR of children; for independent components preserve AND of component verdicts. Cache equivalence only with checked syntactic normalization or explicit proof.

## Round
1. Snapshot residual F and source size.
2. Run all polynomial-budget recognizers/transforms, not merely the first successful one. Store independent technique reports and charged failed attempts.
3. Verify certificates; merge compatible sound deductions, including implications, XOR equations, forced literals, separators, verified symmetry orbits, and decompositions.
4. Apply deductions to a new residual, preserving witnesses and proof provenance.
5. Recompute ALL affected techniques. Continue while a lexicographic, explicitly bounded measure improves; no repeated unchecked transformations.
6. If no progress, use a charged exact branch and recurse. Optionally memoize checked canonical residuals.
7. Track shared-work credits exactly once and interaction overhead separately.

## Per-technique ledger
Each technique has: residual hash, input encoding and length, start/end assumptions, measured runtime, peak bytes, cumulative memory, generated representation bytes, discovery cost, certificate check cost, output facts, and downstream consumers. The aggregate ledger separately records duplicated scans, shared caches, provenance verification, branching, compatibility, and total peak simultaneous memory. Record physical CM and minimum-description CM as distinct concepts; a Python/RAM run does not prove a sole-tape exponent.

## Interaction experiments and attribution
For the SAME SAT/UNSAT neighboring instances and hard UNSAT families, run:
A: each technique alone with exact fallback;
B: all techniques but no cross-feeding;
C: all techniques with certified cross-feeding;
D: C with each technique ablated in turn.
Use deterministic seeds, equal machine budget, identical encoding, and exact correctness oracle for finite instances. Record T_A,T_B,T_C,T_D, branch nodes, distinct residuals, cache hits, preprocessing, peak space, CM, and certificate verification. Cross-feeding synergy can be quantified by C versus B; ablation measures marginal effects, not causation without further controls.

## Example of valid cross-feeding
An explicitly extracted affine subsystem may derive a forced literal or inconsistency via elimination; propagate the forced literal into the CNF, recompute SCC and components, and use smaller separators/backdoors in the next round. Conversely SCC implications can simplify affine equations. An affine equation is NOT inferred merely from a suggestive pattern unless its entailment is certified. Symmetry quotienting requires orbit and semantic compatibility proofs.

## Complexity obligation
For input length N, let R(N) be number of distinct visited residuals, I(N) number of verified rounds across residuals, P(N) maximum per-round total bit cost, and B(N) total generated and checked bytes. T <= O(I(N)P(N)+B(N)+branch/cache overhead), with all discovery and cross-feed costs charged. A polynomial theorem requires polynomial bounds for every term on every input, including SAT and UNSAT. No claimed monotone 'potential' is useful unless its bounded decrease under ALL permitted operations is proved.

## Critical tests
Use 3-variable eight-clause UNSAT cube and its seven-clause SAT neighbor as minimal correctness controls; extend to random and adversarial 2P2N-3CNF, Tseitin/XOR encodings, planted SAT and single-clause-deleted UNSAT neighbors, high-treewidth but algebraically easy instances, and low-width but costly-to-discover representations. Explicitly audit whether preprocessing itself resolves the problem, whether sharing avoids apparent exponential counts, and whether selected hard cases are recognizable gadgets.

## Scientific status
This is an implementable research protocol, not a polynomial-time theorem. Universal polynomial discovery/coverage remains OPEN. Request peer counterexamples to every claimed universal interaction or progress lemma.
