# TMR-5/069: An unconditional witness-versus-certifier bottleneck for authentic succinct SAT

Date: November 16, 2026, Pacific Time. Owner: TMR-5 / PNP Machine Bottleneck Redteam.
Status: PROVED/EXACT elementary **disjunction**, conditional on the standard nondeterministic time hierarchy and an authentic uniformly generated indexed-CNF reduction. External independent mathematics review OPEN. P versus NP OPEN.

## Chosen dependency, precise model, and falsifiers

Named dependency: C1f-WITNESS-OR-VERIFY, between source-derived indexed clauses, a proposed succinct assignment representation, the paid zero-violation verifier, and the nondeterministic hierarchy consequence. This is an independent full-chain audit of /066, not an attempt to promote its conditional witness lower bound.

Choose one fixed binary language H in NTIME(2^n) \ NTIME(2^(n/2)), guaranteed by the nondeterministic time hierarchy. Fix a uniform deterministic polynomial-time map x in {0,1}^n to a circuit D_x on ell(n)=O(n) address bits, with three signed v(n)-bit variable names per output clause, v(n)=O(n). Every one of the 2^ell addresses is authentic. Its indexed 3CNF Phi_x is satisfiable iff x belongs to H. Jahanjou--Miles--Viola (2014), Theorem 1 with T=2^n and r=2, supplies such a reduction, but **the constant-locality/junta property is not used by this lemma**: polynomial-time source-to-decoder generation, bounded-length names, total address coverage and the iff reduction suffice.

An assignment description A is a genuine shared fan-in-two Boolean circuit on the v name bits, with an authenticated complete gate table and designated output. It defines all 2^v assignment bits coherently. For every authentic address z, construct
B_{x,A}(z)=1 exactly when **all three** signed literals in D_x(z) are false under the assignment represented by A. Thus
Z(x,A) iff for all z in {0,1}^ell, B_{x,A}(z)=0
iff A defines a satisfying assignment of Phi_x.
The source D_x is shared once, and three physical A copies/references, signs and each gate's actual input name bits are paid. No clauses or truth table of exponential length are silently preloaded.

Falsifiers fixed before the independent check: (F1) D_x construction is not uniform or not polynomial in n; (F2) the indexed domain has unauthenticated addresses or A's shared circuit bits cannot be reused consistently; (F3) the proposed certifier is only correct on a handpicked subset of pairs or receives unpaid access to a huge truth table; (F4) the existential quantifiers over the verifier exponent d, size exponent epsilon and YES input are silently reversed.

## New unconditional bottleneck dichotomy

Use a prefix-decodable original-source/pair format. A length-n source x is explicit. A valid circuit A has s gates, v original named inputs and fan-in two, with all gate functions, predecessor indices, output and malformed-source handling explicit. Its actual encoded length is O(n+(s+v+1)log(s+v+2)); the source-to-pair constructor and decoder fit (n+s+2)^c time and writable space for one fixed integer c>=2 independent of s, d and n.

For fixed rational epsilon>0, put s_epsilon(n)=2^floor(epsilon*n). Define the **total** language
Z_epsilon = { encode(x,A) : A is a well-formed circuit of <=s_epsilon(|x|) gates and B_{x,A} is identically zero on its COMPLETE authentic clause-address domain }.
Malformed words have answer NO. This is a uniform coNP language: its complement is witnessed either by a polynomial-time malformed-source check or by a violated ell-bit address z, and evaluating B(z) takes polynomial time in the complete encoded pair. No equivalence oracle is assumed.

**Theorem (uniform verifier-exponent dichotomy).** For every fixed positive integer d there exists a rational epsilon_d>0 such that at least one of the following is true:

(A) For infinitely many n there is x in H intersect {0,1}^n for which every shared v(n)-input assignment circuit of at most s_epsilon_d(n) gates violates some authentic clause address; or

(B) The total language Z_epsilon_d has no **uniform** nondeterministic verifier running on all its encoded inputs in O(m^d) time, with m the genuine full pair length.

This is an **unconditional disjunction**, not an unconditional proof of (A) or (B) separately and not a lower bound for ordinary explicitly encoded SAT.

**Proof.** Let a>=2 be a fixed integer large enough that source generation, complete circuit guessing/parsing, pair serialization and all local workspace/source bookkeeping take at most (n+s+2)^a physical steps (each step with constant-size finite tape alphabets). All gate indices use O(log(n+s+2)) bits; the full pair length satisfies m<=C(n+s+2)^a. Fix d, set D=a(d+1)+a, and choose rational 0<epsilon_d<1/(8D). Suppose (A) fails and (B) fails. Failure of (A) means every sufficiently large YES x has a genuine satisfying A with at most s_epsilon_d(n) gates. Failure of (B) yields one uniform nondeterministic machine V_d deciding Z_epsilon_d on every valid and malformed input of length m, in O(m^d) time on ALL branches.

On source x, one uniform nondeterministic machine guesses an A within the size limit, pays for construction and parsing of its complete canonical pair, and simulates V_d. All nondeterministic choices of V_d are part of the same nondeterministic branch; no false accepting certificate exists on an invalid or violating pair. For YES sources there exists a satisfying A and accepting V_d branch; for NO sources no A is satisfying because the original reduction is iff. All branches run in
T(n) <= O((n+s+2)^a + [C(n+s+2)^a]^d)
     <= (n+s+2)^D
     = 2^((D*epsilon_d+o(1))*n)
     < 2^(n/2)
for sufficiently large n. Peak live space on THE SAME branch is at most T(n) writable cells, including source/authentication, A, V_d's live certificate, head positions and output. Finite exceptional shorter sources can be hardwired into the uniform finite control. This would put H in NTIME(2^(n/2)), contradicting its selection. Hence (A) or (B). QED.

**Quantifier firewall.** The theorem is forall d exists epsilon_d, NOT exists epsilon forall d. Thus this statement does not prove Z_epsilon outside NP for a single fixed epsilon, and cannot claim an unconditional exponential assignment-circuit lower bound. This is the exact missing input needed for a class-level inference.

**Recovery of /066 under NP=coNP.** Ordinary CIRCUIT-UNSAT has one fixed polynomial-size NP certificate verifier if NP=coNP. The fully paid uniform reduction (x,A)->B_{x,A} is polynomial in the pair size with an exponent independent of epsilon. Consequently there is a fixed d_0, independent of epsilon, for which EVERY Z_epsilon is in NTIME(m^d_0) using that same compiler/verifier. Apply the theorem with d_0. Alternative (B) is false; therefore (A) holds. This reproduces and explains /066. Merely knowing "for each epsilon separately, Z_epsilon is in NP" without a shared degree would NOT justify choosing epsilon after d.

## Resource partition and relation to TMR-1 through TMR-4

The total pair decoder authenticates x, circuit-record count, gate tables, two complete predecessor addresses per gate, the final output and the exact size promise. It either rejects malformed sources, or constructs on demand D_x and B_{x,A}; all complete address bits count. Coherent variable bits are reused by actual three A references. The generic V_d may use any compact method; its declared time is charged including failed guesses and all internal reads. Nothing assumes an exponentially large assignment or clause list is stored. The two time components account for disjoint outer preparation and inner verification; the same branch's peak space includes both while simultaneously live.

An alternate short-circuit SAT solver on a restricted source is legal. DISJ, Horn, 2SAT, affine/Gaussian, bounded treewidth, equality, autarkies, product, padding, selector, unique-solution rank-one, local basis/field, and shared/cache/recompute controls remain genuine cheap paths. No static rank/mass necessary-work argument is used.

This result removes **JMV constant-junta locality** and the **Anthropic exact #SAT theorem** as hypotheses from the /066 barrier. The actual JMV source theorem is sufficient, not essential; any uniformly polynomial-generated COMPLETE indexed 3CNF reduction from the chosen hierarchy H supplies the same dichotomy. It makes the rate-limiting choice explicit: succinct satisfying-assignment circuits or efficient zero-violation certification. It does NOT give a universal lower bound on both, an NP separation, an E^NP quantitative lower bound, or any speedup of a solver.

## Four gates

DISJ sanity: PASS RESTRICTED. Cheap DISJ implementations are allowed and are not compelled to occupy the hard hierarchy YES family.

Relativization: OPEN for an oracle-lift of source generation and the nondeterministic hierarchy. No P-vs-NP separation is asserted; BGS, algebrization and Natural Proofs remain barriers to promotion.

Simultaneous DTISP: PASS for the stated one-branch nondeterministic upper-bound contradiction, but NOT APPLICABLE to an FLMV deterministic forbidden pair. The same actual T and S are charged; no parallel span substituted for work.

Deterministic configuration counting: NOT APPLICABLE to the nondeterministic hierarchy machine. The known upper bound T<=2^O(S+log N) applies only to the declared deterministic, total, read-only-input subroutines and does not imply a work lower bound.

Historical /341 is FAIL as a general logical UNSAT authority; /386 remains RESTRICTED. No majority tie, quantum or error/amplitude model used.

## Provenance, independent review, and one next lemma

Primary JMV original: Jahanjou, Miles and Viola, "Local reductions," ECCC TR13-099 revision 3 (March 31, 2014), printed Theorem 1, original PDF https://eccc.weizmann.ac.il/report/2013/099/revision/3/download/ . Original source checked as printed; output arity is 3v+3, address ell and name width v; production poly(n,log T); iff with a T-bit witness. Nondeterministic time hierarchy: Seiferas, Fischer and Meyer, "Separating Nondeterministic Time Complexity Classes", JACM 25 (1978). Project predecessor: TMR-1/068 and independent TMR-5/066 on the current draft branches. This is an elementary symbolic theorem, not an executed Lean or brute-force proof. No new empirical seed, run, or raw file is claimed.

The complete TMR-5 manuscript was recovered from the current draft branch before any edit; root proof trackers were not read. No checkout exists locally, so updated repository preflight was NOT RUN. Lean 4.33.1, transitive axioms, nanoda, native source-to-machine microcode and manuscript LaTeX build were NOT RUN. External independent mathematical review remains OPEN.

**ONE highest-value next target remains unchanged:** independently rebuild Anthropic's pinned Lean 4.33.1/Mathlib counting and ETH proof, replay printed axioms and both kernels, then separately audit fixed FinTM2-to-ordinary-machine and E^NP consequences. The new dichotomy is not a substitute for that trust dependency.