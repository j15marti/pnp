# LSPV-3/420: Exact signed-gauge covariance of the typed mixed semantic DAG

**2026-11-05 03:24 PST.** Role LSPV-3, task 6ad6f05603248191abb281a5b43b3fc2. **Status: PROVED/RESTRICTED** semantic calculus; independently checked finite tests **COMPUTATIONAL**; exact native byte parser/facet exports and B1/B2/B3 **OPEN**. Fixed R_mix341 and all unit weights unchanged. P versus NP OPEN.

## IDEA before SEARCH: a falsifiable all-rule repair

Prior LSPV-3/418 proved paid-DEF output-polarity gauge and the GF(2) RHS fix only for the DEF fragment. Hypothesis: the same **source-fixed** polarity assignment acts as a cost-preserving automorphism of the *entire enumerated typed semantic rule closure*, if every downstream consumer is transformed, never left with its old signed payload. Falsifiers: broken signed RES pivot, incorrect GF(2) sum after RHS repair, violation of AND3 <=3-original-coordinate eligibility, an uncharged PRIVATE LOCAL-gate antecedent. The last is outside the literal enumerated grammar, not a legal native example.

## SEARCH: authoritative records, peer critique, external primary references

Read FIRST handoff 'research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md' at commit 4e29ed7 blob 033b54b8; issue #3; AGENTS.md (19656af1), CODEX.md (754999f5), skill .codex/skills/pnp-research/SKILL.md (b8df83a7). Exact original 'research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex' blob c87acd11 describes free original CNF axioms and charged one-node RES, AND3 with <=3 original-variable support, binary XOR, constant-support LOCAL-CONVERT and globally fresh functional two-input DEF. The /384 source addendum at 'research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md' blob bbcdad9a excludes unbounded free LOCAL output inputs.

Substantively reviewed LSPV-3/418 blob 50aebf1, LSPV-3/419 'research/agents/lspv-3/2026-11-05_0254_LSPV-3_AFFINE_SEED_LINEAGE_SPARSE419.md' blob 3d2acbd, LSPV-1/414 blob 202bd4d, and LSPV-5 REFEREE359 'research/main/2026-11-05_0248_MAIN_NATIVE-CLOSURE-BALANCE-IMPLICIT-FIREWALL-REFEREE359.md' blob a0d80016. REFEREE359 already proves literal paid-root closure and conditional polynomial semantic canonical encoding, so neither is claimed new here. Actual 'GROKPROOF/2026-11-05_1218_PROGRESS.md' blob d3183283 leaves all-input FLMV transfer OPEN. Actual Claude TPORT-0002 (1f9fc727) and ONETAPE-0001 (9a5b05d6) are restricted model results, not B3.

Indexed web queries used: 'Haken 1985 intractability of resolution pigeonhole principle exponential lower bound original paper 1985', 'Cook Reckhow 1979 relative efficiency propositional proof systems polynomial bounded P NP coNP PDF', 'Krajicek implicit proofs circuit describes resolution proof p-simulation extended Frege', 'Raz Tzameret 2008 resolution over linear equations proof system Tseitin'. Opened primary publisher/institutional bibliographic and abstract pages [1-4], plus Cook's author page and its erratum. Direct Google-branded search was unavailable. Authenticated github.com/openai searches 'ExecCNFNodeSearchCosts', 'WitnessEncodingLemmas', 'resolution certificate check' and full reads of openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (1ced21f4) and openai/math/lean/OAI/Computability/PerfectCompleteness/Machines/WitnessCircuit.lean (6b29b9) give no matching fixed-calculus B3/compiler.

The locally required repo skill preflight was not executable without a complete local checkout. Direct GitHub source retrieval authenticated the governing files. Root main.tex not edited because no complete safe compare-and-write read was available.

## ITERATE: explicit theorem with exact scope

Let F be any original DIMACS source over original variable names X. Let pi be any finite valid, acyclic **root-only typed semantic** derivation under the enumerated unchanged /341 rule semantics, including globally fresh DEF outputs z_1,...,z_a. Parents reference paid roots (or explicitly authenticated fixed facets), not private LOCAL gate names. Let delta(x)=0 for all original x, and choose arbitrary delta(z_i) in {0,1}. Define the Boolean valuation bijection G_delta(a)(v)=a(v) XOR delta(v).

For a condition C, write C^delta for the pullback along this bijection: C^delta(G_delta(a))=C(a), for ALL assignments a, not only source models. This flips a signed clause literal if and only if its auxiliary name is complemented. The typed GF(2) equation and paid DEF gate require

$$
\left(\bigoplus_{v\in S}v=b\right)^\delta:
\quad \bigoplus_{v\in S}v'=b\oplus\bigoplus_{v\in S}\delta(v),
$$

$$
f_i^\delta(s,t)=f_i(s\oplus\delta(u_i),t\oplus\delta(v_i))\oplus\delta(z_i).
$$

**Theorem (semantic mixed-DAG polarity covariance, PROVED/RESTRICTED).** For every such F, every such pi, and every delta, pi^delta obtained by transforming each typed node is a valid source-authenticated derivation with the EXACT same node IDs, inference rule types, graph, original source-label dependencies, number q of paid nodes, unit weights, and terminal contradiction. Each named original source condition remains byte-identical as a mathematical source clause. This holds for shared DAGs, nested gates, repeated inputs, reconvergence and large supports, insofar as their nodes are actual legal /341 conditions. It is NOT a byte-level parser or compiler for unspecified native selector syntax.

**Proof by induction over nodes.** Original axioms do not change because the map fixes X. For RES, simultaneous literal sign flipping preserves complementary pivot pairs and commutes with deleting the pivot and forming the resolvent. For AND3, pulling back exact conjunction equals conjunction of pulled-back parents; a bijection fixing the original coordinates preserves the number of original variables in the eligible <=3 support, and equality with any exact affine annotation survives the explicitly corrected row RHS. For XOR, parity-shift bits add modulo two; hence the RHS correction commutes with symmetric difference of parent row masks. For LOCAL-CONVERT, an exact local logical implication remains an implication under a bijection; fixed original support is preserved and an output clause remains a clause. For DEF, the transformed two-input truth table is still functional and globally fresh, yielding a unique extension at every stage. These steps are local and preserve parent edges, so node count and weights are exactly unchanged. The empty clause and 0=1 are fixed by the gauge. QED.

**Falsification boundary:** this proves *typed semantic* rule covariance only. The /341 prose does not specify bytes for DEF facet selectors, private LOCAL exports or arbitrary GF(2) admissions; invented instructions cannot be included or asserted to be accepted. Preexisting LSPV-3/414 demonstrates why equality merely on source models fails for GF(2) consumers. No lower bound on actual machine work follows.

## Independent B3 meta-barrier (PROVED/EXACT as a logical equivalence)

Let Res denote the different conventional **ordinary shared-DAG Resolution** proof system on standard CNF input encoding, with each inference paid. Haken [4] proves that the standard unary pigeonhole CNF PHP_h, for h+1 pigeons into h holes, with polynomial bit length in h, requires 2^{Omega(h)} Resolution steps for EVERY ordinary Resolution refutation. Consequently the worst-case minimal Resolution cost Wbar_Res is unconditionally superpolynomial.

Define B3(S) = 'SAT in P implies Wbar_S polynomially bounded'. Since the consequent of B3(Res) is unconditionally false, elementary implication logic yields

$$
\boxed{\operatorname{B3}(\mathrm{Res})\Longleftrightarrow
\mathrm{SAT}\notin\mathrm P\Longleftrightarrow \mathrm P\ne\mathrm{NP}.}
$$

Therefore a blanket **system-agnostic** B3 theorem asserted for *all* sound effective complete proof systems, or even for any class including ordinary Resolution, would itself prove P != NP. Completeness, bounded antecedent count and polynomial-time local checking cannot alone furnish that theorem. **This is not a refutation or a proof of B3 for the strictly stronger fixed R_mix341.** Haken's restricted lower bound does NOT carry over to native GF(2) or ER; the project's exact linear-cost odd-Tseitin refutations and Cook's ER PHP shortcut are mandatory controls. Cook-Reckhow yields SOME bounded proof system under NP=coNP, not a system-independent compiler into this preselected one.

## Verification and cost accounting

Producer 'experiments/arc/lspv3_420_mixed_gauge_check.py' exhaustively checks 256 two-gate networks over 2 original inputs/2 auxiliaries with all 4 gauge masks and original assignments, 4-wire signed clause transformations and exact RES pivots, all 4-wire affine rows and XOR pairings, every pair of two-input Boolean functions for LOCAL implication and AND conjunction, plus negative controls. **12,645 assertions passed.** Separately implemented JS verifier 'experiments/arc/lspv3_420_independent_verify.js' passed **15,717**. Rejected controls: uncorrected GF(2) RHS, wrong RES pivot, false LOCAL implication, duplicate paid names and free internal LOCAL port. Source SAT/UNSAT controls passed. These are finite semantics fixtures, not a certified native DIMACS grammar implementation.

Proof node q counts shared inference nodes once and is invariant under gauge. Separate costs: explicit supplied evidence E bits requires at least Omega(E) reads to fully authenticate; transforming/materializing records and checking them consumes polynomial time/space in E+N+q if records are explicitly given, with all intermediate lengths, output, source dictionaries, verification and peak live buffers charged. REFEREE359's semantic canonical length O(N+q(n+q)log(n+q)) uses a charged dictionary of actually occurring source variable names (n<=N) so exponentially large DIMACS header coordinate values do not force dense arrays. This is NOT a machine-time lower bound, a proof-search bound, a B1/B2/B3 theorem, or an FLMV contraction.

## Next obligation

Freeze a native finite-alphabet input grammar for all paid facets/root selectors and GF(2) admission. Only then implement a checker and prove the byte translator accepts **exactly** legal /341 derivations. Separately prove a noncircular same-Rmix341 p-simulation/reflection for B3, or provide an explicit legal counterexample. No role, agent state, schedule, proof-system rule, or historical theorem changed. **P versus NP OPEN.**

## Sources

[1] Cook & Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36–50, https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/abs/relative-efficiency-of-propositional-proof-systems/218048250981F835B4B2A4080205A0BA

[2] Raz & Tzameret, *Resolution over Linear Equations and Multilinear Proofs*, APAL 155 (2008), 194–224, https://weizmann.elsevierpure.com/en/publications/resolution-over-linear-equations-and-multilinear-proofs/

[3] Krajíček, *Implicit Proofs*, JSL, https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/abs/implicit-proofs/B6E778CBA3308E4A172F66FFDEB07054

[4] Haken, *The Intractability of Resolution*, TCS 39 (1985), 297–308, https://doi.org/10.1016/0304-3975(85)90144-6

[5] Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4) (1976), 28–32.
