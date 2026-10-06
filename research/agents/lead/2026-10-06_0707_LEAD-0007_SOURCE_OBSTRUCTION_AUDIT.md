# LEAD-0007 — Source-obstruction audit

Timestamp: 2026-10-06 07:07 PT

**GLOBAL STATUS: OPEN.** P versus NP remains open.

## Highest-value live gap
Can an arbitrary polynomial-time exact SAT implementation A force a cheap, source-sensitive certificate on a hard sibling pair that is unavailable to a maximal semantic oracle and strong enough to break recursive obstruction growth?

## Duplication / older-result audit
Drive LSPV-4-29401 already falsified SAME_REALIZATION as a generic nonrelativizing hinge: a maximal fixed-realization oracle O_R can answer every extensional future predicate consistently. A 2026-09-27 MANUSCRIPT-RESEARCH report proves an extensional-relativization closure for formula-only Boolean invariants. Therefore SOURCE-OBSTRUCTION-BREAK1 cannot merely use Phi(A,R) when its acceptance predicate factors through A's input/output behavior.

## ORACLE-SHADOW-PAIR1
**PROVED/EXACT, interface-scoped.**

Fix a deterministic exact SAT implementation A. Suppose a proposed pair certificate C_A(F,u,v) is computed by a polynomial-time adaptive transducer E that accesses A only through query/answer pairs (q,A(q)), together with extensional formula data. Then replacing A by a SAT oracle reproduces the complete E transcript and the final certificate exactly.

### Proof
Because A is exact, A(q)=SAT(q) for every query q. Initially E has identical extensional input in both worlds. Inductively, identical prior transcripts imply the same next query q; A and the SAT oracle return the same bit; hence the next E state is identical. The final certificate is identical. Any soundness/coverage theorem uniform in this interface therefore survives semantic-oracle replacement.

This is not a P-vs-NP separation and gives no runtime lower bound.

## Consequence
A viable source-obstruction certificate must inspect an intensional property of A that is not reconstructible from polynomially many semantic SAT answers. However, wrapper covariance remains mandatory: DEAD/COPY/DELAY/INTERP/RECOMP cannot empty the qualifying witness set. Source dependence by itself is not nonrelativization.

## SOURCE-OBSTRUCTION-BREAK2
**CANDIDATE/OPEN.**

For every exact polynomial-time SAT realization A, require a wrapper-covariant witness relation W_A on critical obstruction sibling pairs such that:

1. W_A proves one-sided SAT dominance.
2. Critical-pair coverage contracts obstruction depth by a fixed fraction, not merely O(1).
3. Witness acquisition has exponent coefficient <1 in A's exponent and contains no current-scale A call.
4. No polynomial semantic-oracle transducer reconstructs the witness relation.
5. A separate affine/algebraic-oracle audit shows the load-bearing implication does not merely algebrize.

## Barrier audit
- **Relativization:** ORACLE-SHADOW-PAIR1 kills all A-dependent pair certificates exposed only through adaptive semantic answer queries.
- **Algebrization:** still separately OPEN. Algebraic/RMV source features do not establish escape merely by being intensional.
- **Natural Proofs:** no large constructive circuit property is asserted here; relevance remains unresolved.
- **Wrappers:** existential witness-set covariance, not witness identity, is the correct target.
- **Model matching:** any final contradiction still requires the extracted object to land in the exact resource model of the endpoint theorem.

## Literature check
Williams' Circuit-SAT self-improvement remains a genuine algorithmic bootstrapping precedent, not an arbitrary-SAT-decider extraction theorem. Williams' 2025 square-root-space simulation sharpens time-space context but does not supply CSE. Hirahara-Lu-Ren bounded relativization warns that even techniques classed as nonrelativizing can retain substantial oracle robustness. Aaronson-Wigderson and affine-relativization work keep nonalgebrization as a separate obligation. Restricted DPLL lower bounds do not transfer to arbitrary SAT algorithms.

## main2/main3 decision
No edit this run. This lemma sharpens the oracle-shadow guard already present in the main files but does not change theorem status, proof dependencies, or the central OPEN bridge.

## Handoffs
**PROOF:** formalize ORACLE-SHADOW-PAIR1 in the current CSE/SOURCE-TRANSPORT notation; inspect every active pair-certificate primitive for whether it factors through adaptive semantic answers.

**RED:** attack SOURCE-OBSTRUCTION-BREAK2 using equivalent implementations and maximal semantic plus affine/algebraic oracles. Try to prove witness-set emptiness after wrappers.

**RESEARCH:** search specifically for intensional machine/code lower-bound methods that are wrapper-covariant yet provably not semantic-oracle simulable. Distinguish full nonrelativization from bounded relativization.

**WRITE:** add the pair-certificate oracle-shadow lemma only when synchronizing the barrier ledger. Do not describe source dependence itself as a nonrelativizing hinge.

## Next target
Construct one concrete witness whose soundness genuinely uses code/realization structure while existence survives semantics-preserving wrappers. If no such witness survives, retire the source-obstruction route rather than adding more formula-only signatures.
