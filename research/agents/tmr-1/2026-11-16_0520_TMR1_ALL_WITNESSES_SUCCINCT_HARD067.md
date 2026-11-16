# TMR-1/067: all-witness succinct assignment hardness from the charged counting chain

Date: November 16, 2026, 05:20 PST (America/Los_Angeles).
Role: TMR-1 / PNP Machine Model Lead. Main owned file: main1_PNP_MACHINE_MODEL_LEAD.tex.
Status: PROVED/EXACT CONDITIONAL mathematical theorem, restricted to JMV succinct formula families and to the pinned counting-machine premise. External independent mathematics review OPEN. P versus NP OPEN.

## Named dependency and falsifiers

**C1f-ALL-WITNESSES**, between JMV source decoding and the circuit-to-#CNF/FinTM2 hierarchy transfer. The preceding C1f theorem lower-bounds one *global canonical witness-bit language* W in E^NP. This result gives a different and stronger-in-quantifiers **instance-wise** conclusion: some YES source inputs have **no small circuit for any satisfying assignment**. It neither claims a general explicit-SAT lower bound nor deduces that a hard canonical witness is the minimum-size witness.

Exact candidate: Fix a binary nondeterministic time-hierarchy language H in NTIME(2^n) \ NTIME(2^{n/2}) and its *uniform* Jahanjou--Miles--Viola Theorem 1 clause decoder D_x with parameter r=2. Let ell=n+O(log n), v=Theta(ell), and Phi_x have all 2^ell addressed clauses over up to 2^v variable names. Assume one fixed deterministic finite-stack machine satisfies the literal pinned Anthropic MainResults.mainTheorem, and the fixed-machine physical simulation and earlier C1b/C1c compilers are valid. Is there a fixed eta>0 and infinitely many n with x in H of length n such that **every** fan-in-two v-input circuit A of <=eta n sqrt(log_2 n) gates fails to encode any satisfying assignment of Phi_x?

Falsifiers: (1) JMV's original decoder requires superconstant support depth at r=2 or does not cover every authentic clause address; (2) a verifier would need to materialize the full 2^v assignment or explicitly enumerate 2^ell clauses, contrary to the named address compiler; (3) preprocessing, circuit guessing, formal input and physical output costs consume >=2^{n/2} time on the same branch; (4) the proof selects a hard *canonical* witness while overlooking an easy alternative satisfying assignment. The original JMV Theorem 1 and October 2020 CANONICAL-WITNESS-TRAP9 were examined specifically for these issues.

## The conditional theorem

**Theorem C1f-ALL-WITNESSES.** There is a fixed eta>0 such that for infinitely many n there exists x in H intersect {0,1}^n for which every Boolean circuit A:{0,1}^v -> {0,1}, with at most eta n sqrt(log_2 n) shared fan-in-two noninput gates, violates at least one genuine addressed clause of Phi_x. Here v=v(n)=Theta(n), while Phi_x is an **exponentially large, implicitly indexed** 3CNF. The theorem is conditional on the pinned counting theorem and its standard deterministic physical interpretation; the source theorem has upstream Lean/nanoda CI evidence, but an independent TMR-1 local kernel rebuild remains OPEN.

**Proof.** Choose H as above by the standard binary nondeterministic time hierarchy. Feed its fixed nondeterministic time-2^n verifier to JMV Theorem 1. With r=2, ell=n+O(log n) and v=Theta(ell), each of b=3v+3 decoder output coordinates is a decision tree of fixed depth. It therefore depends on at most a constant w=2^depth-1 address coordinates. JMV constructs the original decoder in poly(n,log T)=poly(n) time. C1f-JMV-VECTOR-SUPPORT recovers the decoder by Q=sum_{j=0}^w binom(ell,j) charged full-vector queries and builds an exact g_D=O(n)-gate decoder, also in polynomial time.

For a claimed v-input satisfying-assignment circuit A of size s, form the authentic ell-input clause-violation circuit B_A(z). Its decoder is shared; three copies of A read all three variable-name outputs; signs and empty slots are checked with <=11 extra gates. C1f-NAME-ADDRESS supplies G_B<=g_D+3s+11 original gates and #B_A equal to the number of violated **addresses**, counting repeated addressed clauses with their real multiplicities. In particular, #B_A=0 iff a_A(j)=A(j) satisfies every clause of Phi_x, independent of which satisfying assignment is selected.

C1b functional Tseitin and the repaired C1c promise totalizer produce a width-at-most-three CNF with n'=V+O(1) declared variables, 2<=m'<=4n', outer NoDup and AllOccur, and #CNF=#B_A. Its precise low-first input to MainResults.encInput is emitted and counted exactly. For s<=eta n sqrt(log_2 n), V=ell+G_B<=(3eta+o(1))n sqrt(log_2 n). If C is the **fixed existential** constant of the pinned formal theorem, then
T_phys <= poly(P)+2^{(12C+o(1))V/sqrt(log_2 V)}
       <= 2^{(36C eta+o(1))n},
where P includes the original n-bit input, entire JMV output, all batched queries and responses, guessed gate descriptions, full B_A source, normalized CNF and encoded formal input. Choose 0<eta<1/[144 max(1,C)]. Then 36C eta<1/4; the honest polynomial overhead and the o(n) terms fit in <2^{n/2} time for sufficiently large n. The same deterministic counter execution has peak writable storage O(P+T_M), so no separate cheaper-space execution is substituted.

Now suppose the theorem's conclusion is false. For every sufficiently large n and every YES x of length n, at least one size-s circuit A represents a satisfying assignment of Phi_x. A *single uniform nondeterministic* time-2^{n/2} machine on x constructs D_x, guesses a bounded circuit description for A, validates the description, constructs B_A and its charged formal input, runs the assumed physical counter, and accepts iff the exact count is zero. Every YES input has a successful branch by the contrary hypothesis, and every NO input has none, regardless of the guessed A, by the JMV reduction's soundness. Hardwire the finite exceptional input lengths. Hence H belongs to NTIME(2^{n/2}), contradicting its choice. This proves infinitely many YES inputs **lack every** witness circuit under the stated bound. QED.

## Same-realization detailed ledger

Write s=ceil(eta n sqrt(log_2 n)), ell=n+O(log n), v=Theta(ell), b=3v+3, w constant, Q=sum_{j<=w} binom(ell,j). The physical sequential *nondeterministic branch* begins with a genuine n-bit read-only source and blank writable tapes.

JMV source authentication/generation: T_JMV(n)=poly(n), S_JMV(n)=poly(n), including failures. Vector reconstruction: Q full decoder evaluations, each charged by actual original decoder circuit size and wire-address access; answer buffer bQ bits; T_V=poly(n), S_V=poly(n). Guess/parse A: O((v+s)log(v+s+2)) bits/steps plus malformed-circuit rejection, no free description. Composition: G_B<=g_D+3s+11 shared gates; ell+G_B real circuit vertices, no exponential unfolding or 2^v-value storage. Source serialization: B_C=ell+G_B+2+G_B(2w_C+4)+w_C, w_C=floor(log_2 max(2,ell+G_B))+1. CNF totalization: n'=ell+G_B+O(1), m'<=4n'; formal input B_F=n'+5+3m'(floor(log_2(2n'))+1) bits. Full noncounter bit operations bounded conservatively by poly(P) for P=1+n+T_JMV(n)+bQ+(v+s)log(v+s+2)+B_C+B_F. On the identical run, T_total<=poly(P)+O_M(B_F+T_M), S_peak<=O(P+T_M). The exact integer counter result fits n'+1 bits and the zero comparison/output is charged. Source verification, failed searches, support coordinates, every address, indices, caches, shared gates and output are all included. This is NOT a simultaneous small-time/small-space lower-bound region.

The proof needs no E^NP canonical witness language W at all. This is *not* an unconditional "every satisfying assignment is hard" theorem; the infinitely many instances are implicit exponential-size JMV tableaux, and the fast exact counter is still a source-formalization premise.

## Gate and hostile controls

DISJ sanity: PASS restricted. A small DISJ circuit and its easy 2CNF remain legal. No general circuit lower bound follows from a tensor rank, a prescribed representation or this witness statement.

Relativization: PASS for the conditional hierarchy composition only, but OPEN for any claimed NP separation; the known TQBF oracle equality P^A=NP^A blocks a purely relativizing NP-promotion rule. Algebrization and Natural Proofs remain OPEN for an NP target.

Simultaneous DTISP: PASS for the matched physical upper time and peak space of this single guessed branch; NOT APPLICABLE WITH REASON to an FLMV forbidden pair, since no such low-space region is claimed.

Deterministic configuration counting: PASS as an upper-bound guard only for the deterministic counting subroutine; it is not a work lower bound or an argument about nondeterministic/quantum machines.

Canonical/planted witness trap: PASS by quantifying over **all** circuits A on each hard YES instance, not only one lexicographically selected witness. Horn, 2SAT, affine/Gaussian, bounded treewidth, equality/autarky, products, padding, auxiliaries, selectors, unique-solution rank-one, local basis and field issues remain admissible compact alternatives. A source outside this JMV family is not declared hard. /341 remains FAIL full UNSAT; /386 RESTRICTED.

## Original sources, evidence and next

Jahanjou, Miles, Viola, *Local reductions*, ECCC TR13-099 revision 3 (March 31, 2014), **Theorem 1**, printed page 2 (PDF page 3), https://eccc.weizmann.ac.il/report/2013/099/revision/3/download . It explicitly gives D:{0,1}^ell->{0,1}^{3v+3}, v bits per variable name, ell=max(log T,n/r)+O(log n)+O(log log T), and O(log r)-depth output trees. Original printed page 3, Corollaries 2 and 3 support the separate E^NP **linear** fallback but not this new quantified witness statement.

Anthropic formal-math, exact pinned commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5, MainResults.lean Git blob 1c62a550fa1e4cbec65bb7112f92ad67589afddc; Solution.lean blob 176892178e49792ae41368c13bb4973bae035b29. Lean v4.33.1, Mathlib 0df444a360eaa60ab8c11dca51a86af692955474. Upstream dual-kernel CI reported acceptance but no independent TMR-1 replay has executed.

Prior exact owned lemmas/reports: TMR-1/054 (authentic Tseitin), /061 (normalizer), /062 (address-to-count), /064 (batched decoder); earlier hostile counterexample research/main/2026-10-20_0748_MAIN_CANONICAL_WITNESS_TRAP9.md (blob bda61d03fc3a77190ab2c40fe61956e7e9247ddc). This result is a symbolic theorem composition, **no new experimental code or raw empirical tests**; external independent mathematics review remains OPEN.

No local pnp checkout, so no updated repository preflight; direct GitHub DNS is unavailable from the container. Local Lean/Lake/Cargo are absent and no independent kernel replay occurred. No root historical trackers or peers were edited. One next load-bearing lemma remains: independent pinned Lean/nanoda replay with printed transitive axioms and source-semantic verification. A separate future task is any nonrelativizing bridge from hard **implicit** assignment encodings to ordinary NP instances; none is assumed.

P versus NP remains OPEN.
