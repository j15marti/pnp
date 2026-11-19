# RECOVERY-LOCAL4: row-local replay and polarity correction
19 November 2026, Asia/Seoul. P versus NP OPEN. Independent peer review pending.

## Material correction to SELECTOR-ADVERSARY1
The preceding report and its final response incorrectly attributed Fortnow's quasilinear-time/sublinear-space nondeterministic exclusion to SAT. Withdraw that attribution. The complement bar is lost in the retrieved PDF text. Fortnow's proof of Theorem 3.2 explicitly applies its assumed nondeterministic algorithm to **nonsatisfiability questions** (printed page 6, Section 4). Corollary 3.4 is a coNTISP exclusion for NQL. The 2007 Diehl--van Melkebeek--Williams paper also places this lineage on the tautology/NO side. This correction does not affect the deterministic exclusion, the selector realization construction, or the finite CNF audits.

Sources recovered:
- https://lance.fortnow.com/papers/files/npvsnl.pdf, Theorems 3.1–3.2, Corollary 3.4, and Section 4 proof.
- https://research.cs.wisc.edu/techreports/2007/TR1601.pdf, Theorems 1–2, Section 2.1.
- https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/samCCC-cr.pdf, definition of DTISP and Theorem 2.
Screenshot requests returned text placeholders, so this run does not claim visual inspection of the overbar. The polarity correction is established from the proof's explicit nonsatisfiability application and class containments. Direct PDF download failed; web text was available.

## Recovered original project results
Full original bodies were fetched through the GitHub connector (ORBITBATCH was retained in tool storage; displayed output was truncated).

| Source | Recovered scope and use |
|---|---|
| LEAD-0023, research/agents/lead/2026-10-06_1436_LEAD-0023_WRAPPER_AS_SAT_QUANTIFIER_AUDIT.md; blob 89daf73166f90772800e1ad6e713fd0d60b2feab | Under a fixed polynomial exact SAT decider A, compile actual YES and NO machine computations. The compiler pays A's runtime. Existential seeds express one route; they do not enforce all-route correctness. |
| ORBITBATCH1, research/agents/lspv-3/2026-10-05_0235_LSPV-3_ORBITBATCH1.tex | Invertible orbit maps have a common address union. Reuse reduces distinct acquisition, while retained tables and emitted outputs remain paid. Field-domain cardinality is not original SAT length. |
| WRAPPER_INDEX_REPLAY1, research/agents/wrapper-shield1/2026-11-19_WRAPPER_INDEX_REPLAY1.md; blob e54cf82a507ff83f8dc5af581f6b406b77aa33d3 | Sparse record directories give paid source replay. Whole-selector enumeration B^R is a valid generic implementation, but is unnecessary when row predicates factor independently. Its Fortnow nondeterministic-SAT attribution requires the same correction above. |
| PATH3, research/agents/recovery/2026-11-19_1144_PATH3/report.md; blob f82a83cc1e4d7ba592e7c06ce2aeb67bdd78aae0 | Known-clock specialist-to-decision conversion; bounded-certificate enumeration; exact-key reuse with acquisition, collisions, eviction and output paid. |
| SELECTOR-ADVERSARY1, research/agents/redteam/2026-11-19_1222_SELECTOR_ADVERSARY1/report.md; blob c0aa4090847e36826e8bc098fe80839c3484fb44 | Arbitrary selector realization and table size o(N^.5). Construction survives; the nondeterministic-SAT literature row is withdrawn. |

This role is Prior-Work Recovery; no TMR-owned manuscript is reassigned or overwritten. There is no local project checkout, so preflight and manuscript compilation were not run. The corpus review is targeted, not exhaustive. Existing governance read in this conversation remains the workflow baseline; retired trackers were not accessed.

## New elementary theorem: local enumeration rather than strategy enumeration
PROVED/EXACT, with explicit hypotheses; peer review pending.

Let F have the authenticated layout F(z,y)=AND_i F_i(z,y_i), disjoint private variables, and a complete row set Z. Let V(F,z,w) be deterministic with a known clock, universally sound, and complete for the predicate:
    there exists i such that F_i restricted to z is UNSAT.
A witness w includes the index and all needed local NO evidence, or a bounded program that constructs and checks that evidence. Suppose length at row z is at most k_z, replay costs at most v_z, and writable workspace at most s_z. Each invocation starts from the same input F and fixed z; it does not depend on a certificate chosen on another row.

Then F is UNSAT iff for every row z there exists w with V(F,z,w)=1.

Algorithm: enumerate witnesses separately for the first row until one passes; discard its temporary state and continue to the next row. If a row exhausts all candidates, declare SAT; if all rows pass, declare UNSAT. Completeness justifies exhaustion; soundness forbids false NO outputs. Hence
    T <= P + O(sum_z 2^{k_z}(v_z+k_z+1)) + O_output,
    S <= S_layout + O(max_z(s_z+k_z) + log N + log T).
P includes authenticated parsing, construction and preprocessing. v includes access/replay, materialization, every child of either polarity, failures, proof checking and resets. A streamed selector/refutation output is charged in O_output. Buffering the whole output adds its size to S.

Proof: independent existential witnesses commute with the finite conjunction:
    AND_z (EXISTS w_z V_z(w_z)).
Cartesian-product enumeration costs up to 2^{sum k_z}; separate enumeration costs sum 2^{k_z}. No shared-witness condition is assumed. Requiring one w for every row is a different statement. Counterexample: V_0 accepts only 0 and V_1 accepts only 1. Likewise, a succinct shared strategy subject to cross-row constraints cannot be replaced by independent witnesses while claiming to preserve that extra constraint.

This sharpens an implementation choice in WRAPPER_INDEX_REPLAY1; it does not falsify the earlier generic whole-certificate enumeration upper bound. Polynomially many universal rows can be traversed explicitly. An arbitrary alternating game may have exponentially many universal histories and requires a separate strategy/traversal ledger.

## Quantitative integration
For k=alpha log_2 N+O(1) and row replay N^{v+o(1)}, R=N^{.195+o(1)}:
    T <= P + N^{.195+alpha+v+o(1)},
    S <= S_layout + N^{sigma+o(1)} + O(log N).
For a local block verifier costing ell^c, v=.35c only if source access and every child are included or separately paid. Target 1.33 requires alpha+.35c<=1.135, with P<=N^{1.33+o(1)}. At alpha=.65 for block-index enumeration with an exact local decider and no extra proof bits, this reproduces c<=97/70. An arbitrary local refutation need not fit those .65 log N index bits.

Thus a generic polynomial SAT seed gives no new exponent guarantee. Paid hereditary splitting is still OPEN. The formal scanner recurrence has exponent max(1.195,.845+.35t), but iteration is legitimate only for an actual compiler applicable to every child. DELAY wrappers preserve semantics while defeating uncharged seed calls.

For supplied correct local witnesses, acquisition disappears by assumption, but replay still totals sum_z v_z and all source/output costs. The whole selector table may fit below sqrt N without supplying local refutations. Neither fact proves the promised selector is uniformly discoverable.

## Matched SAT path and standard-machine accounting
SAT requires one row and satisfying private assignments for all blocks. A read-only certificate supplying all those values is checked against the original clauses with charged address access. For deterministic acquisition, if local SAT-witness verifiers are independently complete, enumerate witnesses per block, not the Cartesian product over blocks. Search rows until one has witnesses for every block. Empty certificate searches are charged.

To emit a full witness without retaining all blocks, first certify the row, then replay each local search and stream its assignment; this adds a second pass. Workspace includes one current witness and verifier, plus input indexing. Output ordering may require further replay unless blockwise variable order is accepted.

Free polarity routing supplies the answer bit for decision; it does not supply satisfying assignments or NO refutations. A uniform sound specialist, complete on its polarity within known time/space bounds, yields total decision by timeout and verification. A supplied k-bit path must reject every wrong path. General bounded-certificate enumeration is O(2^k(V+k)) time and O(S+k+log V) space. Rereadable external advice uses a different interface: ordinary nondeterministic machines must store reread guesses, or supply a proved alternative consistent-access simulation. Re-guessing without consistency is unsound.

## Corrected exclusion ledger
All statements concern uniform indexed/random-access Turing machines or RAMs with a proved polylog-overhead simulation, encoded input size N, charged address/work tapes, read-only input and write-only output. Arbitrary unit-cost big-integer operations are not covered.

- Deterministic SAT/UNSAT: Buss--Williams Theorem 2 certifies (c,epsilon)=(1.34070,.5), with DTISP using +o(1) exponents. Therefore all-CNF deterministic (1.33,.5) is excluded. Subpolynomial-space benchmark: c<2cos(pi/7)=1.801937....
- Nondeterministic UNSAT (conondeterministic SAT): Fortnow's quasilinear/sublinear-space result belongs here. Diehl--van Melkebeek--Williams give, for c^2 d<4, some e>0 excluding the joint algorithms NTIME(N^c) and NTISP(N^d,N^e) for tautologies. At c=d this yields d<cuberoot(4)=1.587401... with some positive e, not necessarily .5.
- Explicit NO-side positive-space calibration recovered from FLMV Corollary 6.5: d(c)=(1+c)/c^2-c; c=1.10 gives d=.635537..., allowing a (1.10,.5) point with reduction slack. At 1.33 this expression is negative. Primary URL: https://lance.fortnow.com/papers/files/tst.pdf. This run relies on the previously retrieved original statement for this calibration.
- Nondeterministic SAT: no corresponding (1.33,.5) exclusion is established by these sources. The erroneous Fortnow attribution is withdrawn. This is a statement about the reviewed sources, not a claim that no other lower bound exists.
- Resolution and other specified proof systems restrict allowed certificates. Their lower bounds do not transfer to all sound algorithms.
- All-CNF deterministic bounded-certificate corollary from PATH3 survives: V=N^{1.33+o(1)}, S=N^{.5+o(1)}, k<=alpha log_2 N and alpha<.01070 would contradict the deterministic point after enumeration, for either polarity. Independent local replay supplies a potentially sharper simulation when its hypotheses hold.
- No all-CNF exclusion transfers to intrinsic-critical T5 deletions or supplied-layout promises without a compatible reduction.

## Executed checks
row_local_audit.py exhausts all 256 two-row/two-block predicates on disjoint one-bit private assignments. Both algorithms agree with direct semantics: 207 SAT, 49 UNSAT. Row-local enumeration makes 644 local predicate checks; whole-selector enumeration visits 940 candidate tables (these are different work units, not a speed ratio). The shared-certificate counterexample is checked.

T5 H9 control uses threads BBB/FBB/FFF/BB. Endpoint relations are respectively {0,1,2,3}, {0,1,2,4}, {0,2,3,4}, {1,3,4}. Their intersection is empty. Removing any one thread constraint leaves a nonempty intersection; deleting any of its edges makes the two dangling pieces greedily extendable. Thus all 11 edge deletions are SAT. This run checks endpoint relations and extension existence, not stored full color vectors. Rotations leave endpoint differences unchanged. This supplies local verifiable certificates and cheap witnesses in a fixed control, not growing-girth hardness.

## Status and gates
PROVED/EXACT: separate row-certificate enumeration with additive search costs; SAT blockwise replay under independent complete verifiers; prior timeout/enumeration implications at their stated scope.
COMPUTATIONAL: the exhaustive finite predicate audit and T5 endpoint checks.
CORRECTED: Fortnow nondeterministic-SAT attribution in SELECTOR-ADVERSARY1 and WRAPPER_INDEX_REPLAY1.
CONDITIONAL: local certificate length, completeness, source-access bounds and arbitrary-CNF reduction required for any target exponent.
OPEN: hereditary compiler, small uniformly checkable local NO certificates, their acquisition, independent peer audit, P versus NP.

DISJ gate PASS: no rank or entropy hardness inference. Relativization PASS for elementary replay; no separation claimed. Simultaneous DTISP PASS for the conditional ledger, OPEN for a realized all-CNF target. Configuration-count gate PASS as an upper-bound consistency check only. Natural Proofs/algebrization: no circuit separation asserted.

Next lemma: establish a concrete row-local NO verifier with an explicit k_z bound and fully charged v_z,s_z for a hereditary residual class; then apply additive replay before invoking any forbidden region.
