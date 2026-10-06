# LEAD-0009 — FSC local/global certification gate
Timestamp: 2026-10-06 07:42 PT

**GLOBAL STATUS: OPEN. P versus NP remains open.**

## Primary-source verification
van Melkebeek–Mocelin Sdroievski (Computational Complexity 34:15, 2025), Section 4: RMV outputs m-bit strings with m <= Delta^(1/100). Lemma 4.4 takes a co-nondeterministic circuit D of size m. Corollary 4.6 also quantifies over co-nondeterministic D; SAT-oracle access belongs to the reconstructor, not D. FSC must therefore land in the exact coND size-m interface.

## Source-side resource audit
EXTEVAL1/LOCALBIT1 show that for one declared SU05/Hadamard realization, a fixed RMV output coordinate can be evaluated by streaming an orbit point, seed/mask, and loop state in O(r log p + log m)+W_oracle workspace. With an already available random-access LDE table, coordinate arithmetic is polylogarithmic in explicit table size. These are evaluation facts, not acquisition/certification facts.

## LOCAL-GLOBAL-GATE1 — PROVED/EXACT as an interface decomposition
Let deterministic local evaluator E^G(sigma)=y make q oracle queries to source G. A certificate containing the q query-answer pairs plus E's deterministic transcript establishes only that some partial oracle with those answers makes E output y. FSC needs the stronger statement that there exists a globally legal SAME_REALIZATION source G in the canonical accepted-source family, consistent with all queried answers, for which E^G(sigma)=y.

Therefore local streaming evaluation alone cannot close FSC. The missing predicate is an exact extension/consistency predicate for the canonical source family. This is a logical decomposition, not a lower bound on that predicate.

## FSC-EXTEND1 — CANDIDATE/OPEN
For Q={(x_j,a_j)} equal to the source coordinates queried to produce one RMV point, define EXTEND_src(c,Q)=1 iff there exists one perfectly accepted canonical PCPP/LDE source G consistent with every pair in Q.

Target: an exact existential verifier of size <=m for EXTEND_src. Combined with the streaming evaluator, this would yield the desired source-image certificate. A current-scale SAT call, full proof replay, or probabilistic/interactive proximity test does not close the bridge.

For an unconstrained degree-Delta polynomial, point-value extension is algebraic/interpolation. The active source is stronger: the LDE of a perfectly accepted PCPP proof tied to the target computation. Dropping accepted-proof membership enlarges the source family and may destroy ASCS miss.

## Quantitative conclusion
FSC-SPACE1 is not retired on workspace grounds: algebraic evaluation can have small streaming state. But generic bounded-space verification is not the remaining bottleneck. The bottleneck is exact local-to-global accepted-source consistency.

## Hostile controls
- Interpolation-only verifier: may forget accepted-proof membership.
- PCP/PCPP local testing: probabilistic soundness is not exact existential verification.
- Full source witness: may violate size-m verifier budget.
- SAT-based extension test under P=NP: risks current-scale SAT reacquisition and oracle shadowing.
- Hadamard is a declared legal realization, not uniquely forced.
- FSC-EXTEND1 must preserve absolute ordinary-source semantics under the ASCS oracle-break.

## Status
RMV m<=Delta^(1/100): PROVED/source-verified.
coND size-m interface: PROVED/source-verified.
small streaming evaluator: PROVED/EXACT for declared SU05/Hadamard realization per EXTEVAL1/LOCALBIT1.
LOCAL-GLOBAL-GATE1: PROVED/EXACT interface decomposition.
FSC-EXTEND1: CANDIDATE/OPEN.
ASCS/FSC: OPEN.
P versus NP: OPEN.

## Main-file decision
This materially sharpens FSC, but main2/main3 are not edited until the exact EXTEND_src quantifier structure is checked against the vMS PCPP construction.

## Handoffs
**PROOF:** formalize EXTEND_src for the exact vMS PCPP/LDE source and determine its quantifier class before any P=NP simplification.
**RED:** construct partial LDE answer sets that extend to low-degree polynomials but not to any perfectly accepted canonical proof; attack interpolation-only verification.
**RESEARCH:** search exact local-to-global extension certificates for Reed-Muller/PCPP encodings and deterministic proof-of-proximity variants.
**WRITE:** preserve the distinction between local RMV evaluation and global accepted-source consistency.

## Next target
Write exact EXTEND_src(c,Q) from the vMS generator's PCPP construction, expose its quantifiers, and determine whether perfect acceptance plus linear LDE structure collapses global consistency to deterministic algebra or retains an NP/SAT-hard accepted-proof component.
