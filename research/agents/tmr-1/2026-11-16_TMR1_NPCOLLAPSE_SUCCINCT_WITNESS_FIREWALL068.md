# TMR-1/068: NP-collapse does not provide small witnesses for succinct exponential tableaux

Date: 2026-11-16, Pacific Standard Time. Track C, named dependency **C1f-NP-COLLAPSE-WITNESS-FIREWALL**. Status: **PROVED/EXACT restricted conditional theorem**, external independent mathematical review OPEN. P versus NP remains OPEN.

## Candidate, model, quantifiers, and falsifiers

Use the **same** authentic binary nondeterministic-time hierarchy source H, Jahanjou–Miles–Viola (JMV) Theorem 1 reduction at r=2, and C1f-NAME-ADDRESS violation compiler as the TMR-1/067 pipeline. Claim:

**Theorem.** Fix any binary language H in NTIME(2^n) \ NTIME(2^(n/2)), and its uniform JMV source-to-indexed-3CNF reduction x↦Phi_x, with ell=n+O(log n) complete clause-address bits and v=Theta(ell) variable-name bits. **If NP=coNP**, then for each fixed integer k>=1, for infinitely many n there exists a YES source x in H∩{0,1}^n such that **every** unrestricted shared fan-in-two circuit A:{0,1}^v→{0,1} of at most n^k gates violates at least one authentic addressed clause of Phi_x. Equivalently, no polynomial gate-size bound works for **all sufficiently large YES instances**, even under P=NP.

This does **not** say one uniform efficiently discoverable hard sequence exists; does **not** assert NP≠coNP, P≠NP, general SAT hardness, or a lower bound on explicit polynomial-size formula witnesses.

Falsifiers checked before consulting sources: (F1) the source decoder might require exponential construction time (JMV Theorem 1 gives poly(n,log T), with T=2^n poly(n)); (F2) v might denote an explicit v-variable assignment (incorrect: v is the name-bit width, with 2^v possible names); (F3) the zero-violation predicate might demand #P rather than coNP (incorrect: "no address z violates" is Circuit-UNSAT, coNP-complete, independent of exact counting); (F4) the verifier might improperly sum exponentially many nondeterministic guesses (incorrect: nondeterministic runtime is bounded on **each** branch, with all materialized source, guess, and certificate bits charged). These are exact interface checks, not finite-test claims.

## Authentic encoded input to output: proof

For given x of length n, produce the genuine JMV decoder D_x:{0,1}^ell→{0,1}^{3v+3}, mapping *every* ell-bit address to a genuine 3-clause on v-bit variable names (JMV Theorem 1, 2014, r=2). Its source generation is polynomial in n, and its output bits have constant-depth address decision trees. The previously proved C1f-JMV-VECTOR-SUPPORT batch uses Q=sum_{j=0}^w binom(ell,j)=poly(n) **charged** evaluations to reconstruct an O(n)-gate decoder; using JMV's already explicit poly(n)-gate decoder would also suffice for the present polynomial-time theorem.

Nondeterministically guess and authenticate an unrestricted circuit A with at most s=n^k shared fan-in-two gates on v-bit variable names, encoded as a complete topologically ordered binary DAG with all gate tables, edge indices, and an output. C1f-NAME-ADDRESS constructs the **actual** ell-address clause-violation circuit B_A of at most g_D+3s+11 gates and authentic source length O((ell+g_D+s)log(ell+g_D+s)). Its satisfying assignments are exactly the violated clause addresses under the **entire** implicit assignment a_A(j)=A(j), j∈{0,1}^v. All source addresses are real, including duplicates; the count may exceed 1 but the zero/nonzero decision is exact. If desired, C1b and repaired C1c produce a parsimonious promised width-three CNF H_A of O(n+s) variables and O(n+s) clauses; its exact low-first C1d serialization has O((n+s)log(n+s)) bits and #H_A=#B_A. This optional normalization preserves the complete research pipeline while the current argument requires **decision only**.

Under NP=coNP, the language CIRCUIT-UNSAT (and equivalently 3CNF-UNSAT) is in NP. Fix one ordinary polynomial-time deterministic verifier V_U for this coNP language, with a polynomially bounded existential certificate. The nondeterministic machine for H additionally guesses a certificate pi of unsatisfiability of B_A (or H_A), materializes it, and runs V_U on the genuine encoded circuit/CNF and pi. Accept **only** if V_U accepts. Every false guess, malformed source, malformed circuit, or incorrect certificate rejects; no promise of a correct witness is built into the decider.

On x∈H, the JMV formula is satisfiable. Under the negation of the theorem at a chosen k, for all sufficiently large such x, some small A gives a satisfying implicit assignment, so B_A is UNSAT and a valid NP certificate pi exists. Some nondeterministic branch accepts. On x∉H the JMV formula is UNSAT, so every A produces at least one violated address: B_A is SAT, and soundness of the UNSAT verifier prohibits accepting on **every** branch. The machine therefore decides H correctly on all sufficiently large lengths; finitely many exceptional lengths can be hardwired by the single finite decider.

Writing s=n^k and P=1+n+ell+v+g_D+s+B_C+B_A, complete source authentication, JMV generation, Q vector evaluations and responses, circuit-guess parsing, shared-gate compiler, duplicate elimination, all indices/address bits, optional source-to-CNF normalization and serialization, certificate generation by nondeterministic guessing, certificate verification, and the final output are jointly bounded on each actual branch by
T_H(n)=P^{O(1)}, S_peak,H(n)=P^{O(1)}.
Here P=poly(n) for each **fixed** k. The verifier's exponent is fixed by NP=coNP, independent of x and n. Do not count all counterfactual choices as sequential work; do count the physically materialized A and pi on each realized branch. Thus H∈NP⊆NTIME(2^{n/2}), contradicting its **unconditional** nondeterministic time-hierarchy selection. This proves the theorem.

A useful unconditional intermediate implication is: if every sufficiently large YES x had a size<=n^k satisfying-assignment circuit, then H∈Sigma_2^P, since existence of A followed by universal verification over all clause addresses is an existential-universal polynomial-time predicate. This implication alone yields no contradiction without a separate hierarchy separation for Sigma_2^P; the NP=coNP hypothesis allows **actual NP verification** and completes the restricted contradiction.

## Meaning for the active proof chain

This is a **nonpromotion / missing-premise firewall** at C1f, not an extra theorem about Anthropic's count algorithm. Even in a hypothetical P=NP world, the authentic JMV exponential tableaux for hard H cannot all be represented by polynomial-size satisfying-assignment circuits. Consequently the proposed NP bridge "P=NP supplies polynomial-size succinct assignments for exponentially indexed tableau 3CNFs" is **FALSIFIED as a general implication under P=NP**. One cannot use it to transfer the prior conditional E^NP or all-witness lower bound down to ordinary NP or derive P≠NP.

Unlike /067, this observation **does not assume** Anthropic's pinned MainResults.mainTheorem or any exact-count speedup; it uses an NP verification of a *zero-violation* circuit only **under** NP=coNP. The previous /067 quantitative Omega(n sqrt(log n)) all-witness result remains separate and CONDITIONAL on that pinned count theorem. No logical contradiction between the results: the present theorem gives a stronger no-polynomial witness conclusion under a stronger complexity-collapse hypothesis, not an unconditional general SAT lower bound.

## Mandatory four gates and controls

**DISJ sanity: PASS restricted.** DISJ has a linear-size depth-two shared circuit and easy exact count 3^k. The theorem concerns only the hard YES instances of a chosen exponentially indexed JMV reduction; it does not imply DISJ is hard, nor infer a lower bound from static rank.

**Relativization: OPEN for any NP separation, NOT APPLICABLE as a separation claim here.** This conditional implication is consistent with the TQBF oracle where P^A=NP^A. It rules out one proposed succinct-witness inference; it does not prove P≠NP or independently supply a nonrelativizing step. Algebrization and Natural Proofs remain unresolved for the NP target.

**Simultaneous DTISP: PASS exact polynomial per-branch upper ledger, NOT APPLICABLE to an FLMV forbidden pair.** The same nondeterministic verifier pays all preprocessing, authentic addresses, guessed circuits, certificates and output; a nondeterministic polynomial bound is not a deterministic sublinear-space SAT solver.

**Deterministic configuration counting: NOT APPLICABLE to the nondeterministic hierarchy verifier.** For separately invoked fixed deterministic subroutines, T≤2^{O(S+log N)} is only a total deterministic upper-bound consistency check, never a work lower bound.

Horn, 2SAT, affine/Gaussian, treewidth, equality, autarky, independent products, padding, auxiliaries, selector projection, unique-solution rank-one, local basis/field choices, legal sharing/recomputation and compact semantic shortcuts are permitted. The theorem restricts **all** potential satisfying assignment circuits on selected YES instances and does not assume a hardness measure for any of those easy families. /341 remains FAIL as general UNSAT authority; /386 remains RESTRICTED. No majority-tie or quantum-amplitude claim is invoked.

## Evidence and workflow

Primary theorem: Jahanjou, Miles, Viola, *Local reductions*, ECCC TR13-099 revision 3 (2014), printed Theorem 1; https://eccc.weizmann.ac.il/report/2013/099/ and https://www.khoury.northeastern.edu/home/viola/papers/explicit.pdf. Authenticated original Anthropic source endpoint: formal-math commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5, eth/MainResults.lean blob 1c62a550fa1e4cbec65bb7112f92ad67589afddc. The latter is **not a premise** for the present theorem.

Original related local owner artifacts: /062 C1f-NAME-ADDRESS, /064 C1f-JMV-VECTOR-SUPPORT, /067 C1f-ALL-WITNESSES, and the active root main1_PNP_MACHINE_MODEL_LEAD.tex. Mathematical review: external independent referee OPEN. The result is a self-contained symbolic conditional proof; **NO NEW EMPIRICAL EXECUTION OR LEAN BUILD IS CLAIMED**. Container has no pnp checkout, Lean, Lake, Cargo; the updated pnp preflight was therefore **not run**. The original upstream pinned CI kernel acceptance is separate external evidence; fresh independent Lean/nanoda and transitive #print axioms remain OPEN. No agent schedule/identity changes, no peer manuscript overwrites, no retired tracker reads.

**ONE next load-bearing lemma stays unchanged:** independently rebuild pinned Lean 4.33.1 / Mathlib MainResults.mainTheorem and ethIsFalse, run actual transitive axiom inspection and Lean/nanoda dual-kernel replay and check physical FinTM2 meaning; preserve the conditional scope until completed.
