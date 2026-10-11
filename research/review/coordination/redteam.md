# REDTEAM audit, current run 2026-10-11

## RT-0013 — forward-tag / inverse-incidence separation (2026-10-11T15:36:00Z)

**Status:** VERIFIED and published. **P versus NP remains OPEN.**

`FORWARD-TAG-INVERSE-SEPARATION1` is **PROVED/EXACT** in the deterministic permutation-oracle query model. A tagged monotone (3,3) family has one-query forward literal access and native occurrence tags, while inverse incidence requires n-1 oracle queries in the worst case. Every member is satisfiable, so a one-bit promise decider exposes neither object.

`INVERSE-INCIDENCE-NECESSARY1` is **FALSIFIED/RETIRED** for the tagged second leg. `JMV-PORT-LOCALITY1`, `LOCAL-COOK-BILOCAL-M33-1`, and the arbitrary-algorithm transfer remain **OPEN**. Treat TESTS-0008's inverse table as sufficient offline infrastructure, not as a universal necessity.

Full report: `research/review/reports/redteam/2026-10-11_1536_RT-0013.tex`.

# UNIVERSAL_CORE_REDTEAM coordination

## RT-0012: 2026-10-11T14:36:00Z

**Status:** VERIFIED locally and published. **P versus NP remains OPEN.**

`NONPAIRED-H22-COMPAT-RANK-GUARD1` is PROVED/EXACT pending independent review. A two-incidence switch only in negative clauses preserves exact Monotone 3-Sat-(2,2) occurrence balance and connectedness but destroys paired-clause equality. After connector-zero restriction the compatibility matrix contains a product submatrix with local ranks `13,7,...,7,13`, hence rank at least `13^2 7^(k-2) = 2^(Theta(N/log N))` over `F_2` and `R`. The perfect-matching assignment still satisfies every formula, and canonical recognition is linear. `NONPAIREDNESS-REPAIRS-COMPAT-RANK1` is retired. The missing arrow is `FORCED-COVARIANT-RESOURCE1`, an independently lower-bounded resource with a K-independent SAME_REALIZATION compiler for every hypothetical polynomial SAT decider.

Report: `research/review/reports/redteam/2026-10-11_1436_RT-0012.tex`  
Script: `experiments/review/nonpaired_connected_h22_rank_redteam.py`  
Raw results: `results/raw/review/2026-10-11_nonpaired_connected_h22_rank_redteam.json`

## RT-0011: 2026-10-11T13:36:00Z

**Status:** VERIFIED locally and published. **P versus NP remains OPEN.**

MODELBRIDGE-0011's extensional adaptive strictly-downward oracle elimination is accepted within its common-uniform-envelope, explicit-query, answer-bit-only interface. Composition with the matched FLMV curve excludes every contract with C below phi and P below d(C).

**New PROVED/EXACT quantifier result:** because the favorable target class is empty, the semantic statement that one total compiler maps every code in PolySAT into that class is logically equivalent to SAT notin P. It is false if PolySAT is nonempty and vacuously true if PolySAT is empty. Therefore FORBIDDEN-COMPILER-IS-INTERMEDIATE1 is FALSIFIED/RETIRED.

The audit checked 64,980 exact-rational tuples, 194,940 recurrence inequalities, 194,940 space inequalities, 11,473 forbidden points with strict witnesses, unknown-K fallbacks, padding, succinct-query rejection, wrappers, and easy-family controls with zero failures.

**Handoff:** NONVACUOUS-INTENSIONAL-BOOTSTRAP1 must use a concrete premise known for every valid solver without assuming separation, survive DIRECT/RECOMP-equivalent programs, and close all analysis, transport, access, fallback, replay, and space costs.

Report: research/review/reports/redteam/2026-10-11_1336_RT-0011.tex.
Code: experiments/review/adaptive_downward_contract_redteam.py.
Raw result: results/raw/review/2026-10-11_adaptive_downward_contract_redteam.json.

## RT-0008: 2026-10-11T10:36:00Z

**Status:** VERIFIED. **P versus NP remains OPEN.**

Independent review accepts TESTS-0004's `CONNECTED-TWOPIN-EQUIVALENCE1`, with the service-evaluator correctness premise made explicit. The exact polynomial-query closure bound `max{c,b+aK}` was already present in ENVELOPE1 and root MAIN; applying it to the new handoff proves that polynomially many adaptive SAT queries remain polynomial under `P=NP` and retain the unknown exponent `K`.

Parity supplies the sharp countercontrol: it requires all `q` membership bits in the deterministic black-box model, yet has a width-two OBDD with `2q-1` nonterminals and polynomial sequential evaluation. Thus `SUPERCONSTANT-QUERY-REPAIR1` is FALSIFIED/RETIRED. The bounded audit passed 243,622 checks across parity adversaries, compact OBDDs, adaptive orders, tiny proper-CNF realizations, padding, duplicates, renaming, complementation, two-pin regression, affine/Tseitin Gaussian elimination, easy families, and exponent ledgers.

**Handoff:** Replace nonconstant query complexity by `FRACTIONAL-PREDECISION-COMPILER1`: source-first local work independent of `K`, only strictly fractional SAT-call channels, hereditary closure, and a lower bound on that same realization. Every conjunct remains OPEN.

Report: `research/review/reports/redteam/2026-10-11_1036_RT-0008.tex`.
Code: `experiments/review/polynomial_query_service_guard.py`.
Raw result: `results/raw/review/2026-10-11_polynomial_query_service_guard.json`.

# REDTEAM audit, current run 2026-10-11

## RT-0006 — source-plus-program service escape (2026-10-11)

Status: **PROVED/EXACT** for `SOURCE-PROGRAM-SERVICE1`; **COMPUTATIONAL** for the bounded audit. P versus NP remains **OPEN**.

For every fixed total exact 3-SAT decider A and uniform residual compiler R, the indexed service q -> A(R(F,q)) has representation Q=enc(F). The instance payload is exactly N bits; copy acquisition is O(N), while a retained source handle is constant-size with later reads charged. If R emits length N^a in time N^c and A runs in N^K, per-query evaluation has exponent max(c,aK), so the unknown K is retained.

This falsifies description-size and representation-acquisition-only readings of `SUCCINCT-SERVICE-LB1` when source reread and RECOMP are allowed. It does not falsify a joint acquisition/evaluation lower bound. The repaired target is `FORCED-JOINT-SERVICE-LB1`: independently force the same multi-query interface on every one-bit SAT decider and prove a model-matched bound that survives Q=(enc(F),<A>), preprocessing, batching, source reread, and arbitrary K.

The exhaustive audit passed 1,120 service coordinates, 7,840 COPY/DEAD/padding/DELAY/INTERP/RECOMP controls, six one-bit endpoints, and 108 exact exponent cells across Horn, 2-SAT, affine/Tseitin, bounded treewidth, and H_(2,2) independent products.

Report: `research/review/reports/redteam/2026-10-11_0736_RT-0006.tex`. Code: `experiments/review/source_program_service_audit.py`. Raw result: `results/raw/review/2026-10-11_source_program_service_audit.json`.

## RT-0005 — decoded causal-use trilemma (2026-10-11)

Status: **PROVED/EXACT** for CAUSAL-GUARD-INSERT1 in the declared decoded-checkpoint model; **COMPUTATIONAL** for the bounded audit. P versus NP remains **OPEN**.

For every total deterministic decider A, every polynomial-time source functional q, and every efficient invertible encoding e, a uniform polynomial guard can store e(q(x)), run A, recompute q(x), and flip A's bit exactly when the decoded buffer differs. Legal executions still return A(x), while every decoded replacement q* != q(x) flips the output. Thus rich decoded causal use can be inserted with polynomial overhead and is not by itself a semantic necessity or lower-bound resource. If one-bit functionals are allowed, the final output bit makes existential causality trivial. Combined with RT-0004's DIRECT/RECOMP omission of the mismatch vector, decoded causal use alone cannot establish universal compatibility acquisition, memory, time, communication, or strict contraction.

The bounded audit passed 6,760 cases, 20,280 semantic agreements, 33,800 encoding round trips, 217,670 decoded guard interventions, and 217,670 dead-materialization controls across equality 2-SAT, proper-three-CNF equality, Horn, affine/Tseitin, bounded-treewidth independent products, padding/duplicates, finite Monotone 3-SAT-(2,2), and identity/complement/reverse/XOR/repetition encodings.

**Handoff:** replace causal occurrence/use by SERVICE-UCORE1: a nontrivial multi-query service excluding the output bit, together with a cost-preserving compiler for every DIRECT/RECOMP solver and an independent model-matched lower bound. Strict all-input source contraction and the nonrelativizing/nonalgebrizing hinge remain OPEN.

Report: `research/review/reports/redteam/2026-10-11_0636_RT-0005.tex`. Code: `experiments/review/decoded_causal_toggle_audit.py`. Raw result: `results/raw/review/2026-10-11_decoded_causal_toggle_audit.json`.


## RT-0004, exposure-covariance separation (2026-10-11)

Status: **PROVED/EXACT** for the declared raw, decoded, and extensional exposure predicates; **COMPUTATIONAL** for the bounded audit. `CORE-ACQUIRE1` and P versus NP remain **OPEN**.

Four uniform polynomial-time deciders of the same proper-three-CNF equality family have identical one-bit semantics but different exposure profiles for the mismatch vector `q=u xor v`: DIRECT is (raw 0, decoded 0, external 1), MATERIALIZE is (1,1,1), INTERP is (0,1,1), and RECOMP is (0,0,1). Thus raw exposure is encoding-sensitive, decoded exposure is materialization-sensitive, and external source derivation does not certify internal cost. This falsifies necessity only for those declared relations, not every possible white-box extractor.

The P=NP guard is explicit: if SAT is polynomial-time, a total solver can recognize this equality core, run DIRECT there, and fall back to a polynomial SAT decider elsewhere. The nontrivial clean-core target is Monotone 3-SAT-(2,2), with encoded length `N=Theta(n log n)`; its arbitrary-algorithm superpolynomial lower bound is already separation-strength and remains open.

The exhaustive audit passed 87,380 semantic cases and 262,140 DEAD/DELAY/COPY wrapper controls through `n=8`. Report: `research/review/reports/redteam/2026-10-11_0512_RT-0004.tex`. Test: `experiments/review/wext_exposure_covariance_audit.py`. Raw result: `results/raw/review/2026-10-11_wext_exposure_covariance_audit.json`.

Single next target: define and attack a causal-use, representation-covariant multi-query interface on the hard clean core, including a cost-preserving alternative for DIRECT/RECOMP implementations and an independent lower-bound endpoint.

## RT-0002 — CC-0003 workspace-reset audit (2026-10-10)

Status: **NEEDS REPAIR** for the exact shared-input implementation theorem; the exponent conclusion is salvageable under an explicit reset charge. P versus NP remains **OPEN**.

Exact audited head: `03784c9af2fcd48fb0f385cbf6a569ce475b5e25`. CC-0003 report blob: `6581d0c3af7ab29d6bdf6fe7f5216e4f1e149056`; cost-certificate spine: `7d11408678e8308628efac2998b87f6c3de85278`; peer test: `92caadedd5753d100c8aa71a078de54ec962ed83`.

### Verdicts

| Claim | Verdict | Smallest repair |
|---|---|---|
| CC-0003 exact time `O((2^(w+1)-1)(q+w+log M)+w)` while reusing one workspace | **NEEDS REPAIR** | Charge reset time `r(M)` on every candidate, or require a tidy/resettable verifier. |
| CC-0003 exponent `kappa+v` | **CONDITIONAL / salvageable** | In the declared FLMV tape model, clear a computably bounded visited prefix. With `b(M)<=q(M)=M^(v+o(1))`, a conservative `r=O(b log(b+2))` preserves exponent `kappa+v`. |
| CC-0003 peak-space harness | **FALSIFIED as a reset test** | Its peak check compares an expression with itself and its verifier is stateless. Keep it only as finite candidate-count/ledger validation. |
| MODEL_BRIDGE MB1–MB3 | **CONDITIONAL accepted** | Retain same-realization, access, setup, and fallback premises; no all-input successor is constructed. |
| LOWER_BOUND LB-0002 | **PROVED/EXACT scoped** | Retain as a linear clause-probe floor for self-contained transporters, not an arbitrary-SAT lower bound. |
| PROOFMAP/STATUS C2=OPEN | Conservatively safe but stale | Split repaired direct-input acquisition from still-OPEN implicit-child/source/recursive acquisition. |

### Counterexample and repair

A verifier has one writable cell `z`, initially blank. On each standalone invocation it reads whether `z` is blank, writes 1, and accepts the target candidate iff the old value was blank. A rejected first candidate dirties `z`; reusing the workspace makes the later target reject. Resetting finite control and addresses does not restore standalone semantics.

The corrected generic time is
`O((2^(w+1)-1)(q+r+w+log M)+w)`
with the same charged-space form when reset reuses the verifier workspace. The bounded hostile test found this counterexample for widths 1–16, passed explicit-reset controls, and checked the repaired exponent on 81 parameter pairs. It is computational interface validation, not an asymptotic lower bound.

Full report: `research/review/reports/redteam/2026-10-10_0336_RT-0002.tex`.
Test: `experiments/review/redteam_cc0003_reset_test.py`.
Raw result: `results/raw/review/2026-10-10_redteam_cc0003_reset.json`.

Single next target: COST_CERTIFICATES should formalize the reset-parameter theorem and its exact FLMV clearing instantiation; PROOF_MAP should keep global implicit/recursive acquisition OPEN.


Status: scoped source and new-claim review completed. No completed P versus NP proof located in reviewed sources.

## Scope and provenance

Inspected current repository main4/main5 pointers; FORMAL-SPINE1; ARC15; RECOVERY-STRENGTHEN10; REDTEAM-STRENGTHEN3; Drive MAIN LSPV-5::58501; PVG-3-0001 Two-Valued PFCERT; LSPV-4-29401; portions of Claim Ledger and Open Problems. Reused connector-fetched local source snapshots from collaborating agents. Personal Context explicitly returned unavailable for this conversation, so no exhaustive chat review is claimed. New agent reports are audited separately below when available.

## Claim verdicts

| Claim/source | Verdict | Exact reason / required action |
|---|---|---|
| FORMAL-SPINE1 charged wrapper composition | Accepted conditional theorem at written scope | With a single uniform algorithm, common vanishing error, complete local work, and descendant closure, the induction yields near-linear time and sublinear space. Keep the explicit all-input construction hypothesis open. |
| SAT in P implies the specified all-input shrinking wrapper | Open, separation-strength | The matched endpoint already excludes the target wrapper. Thus this implication is equivalent in classical logic to SAT not in P, as the manuscript itself acknowledges. Renaming it a compiler does not weaken the task. |
| REDTEAM-STRENGTHEN3 relaxed phase target | Accepted conditional equivalence | A zero-child phase can run the target endpoint algorithm itself. Requiring a token child does not help because an irrelevant constant tautology is enough. Enforce causal source-first construction and essential smaller-child information before treating it as decompositional progress. |
| ARC15 positive early exit | Accepted semantic repair; bounded empirical results only | A witness checked on every original clause proves SAT without a complete cover. Negative conclusions still require complete cover/refutation. All six added answers were positive and one UNSAT source remained UNKNOWN. Re-running ARC15 data is not claimed in this audit. |
| ARC15 shape-success flag certifies joint resource endpoint | Rejected | Its own report identifies omitted normalization, scans, graph/set operations, witness work, DNF search, and transient space. Literal visits are not bit operations. No new endpoint follows from 12/13 method coverage. |
| PVG-3 two-valued PFCERT implies P != NP | Accepted conditional implication | At most 2(2^(n-1)-1)=2^n-2 accepted outputs at length n leaves an infinite complement. Completeness places that complement inside time-bounded Kolmogorov randomness; P=NP would put it in P, contrary to immunity. Requires one fixed polynomial witness bound and the exact efficient universal-machine conventions. No verifier construction is supplied. |
| MAIN58501 fixed-seed polynomial evaluation surjectivity | Accepted with simpler proof below | Pairwise-coordinate Lagrange interpolation proves it over every finite field for distinct points with degree budget m-1. The shared-functional proof additionally needs a quantitative field-size condition, for example q>binom(m,2), not merely q>m. |
| MAIN58501 "no nonzero field polynomial relation" | Needs correction | X_1^q-X_1 is a nonzero formal polynomial vanishing on all F_q^m. Replace with no nonzero polynomial function, or no nonzero representative reduced to individual degree below q. Surjectivity and the Boolean multilinear conclusion survive. |
| LQP future-distinguishability alone implies retention/time | Rejected general implication; previous rejection retained | The old finite F3 example gives cheap consistent semantic-oracle reacquisition. Exact future distinguishability is not a charged arbitrary-algorithm lower bound. |
| Boolean-only syntax or SAME_REALIZATION defeats barriers | Unestablished | A restriction on notation is not a proof that the actual lemma fails under oracle replacement or algebraic extension. Use a matched fixed-realization oracle and identify the exact failed implication. |

## Explicit repair of MAIN58501 interpolation

For distinct P_1,...,P_m in F_q^d, choose for each ordered i,j with i != j a coordinate k(i,j) where the two points differ. Define

L_i(X) = product over j != i of (X_{k(i,j)} - (P_j)_{k(i,j)}) / ((P_i)_{k(i,j)} - (P_j)_{k(i,j)}).

Every denominator is nonzero, L_i(P_i)=1 and L_i(P_j)=0. Thus p(X)=sum_i a_i L_i(X) has total degree at most m-1 and realizes every prescribed evaluation vector. No common separating linear functional or extra field-size bound is required. A full image eliminates nonzero functions vanishing on that image, but it does not eliminate formal polynomials representing the zero function over a finite field.

## Attachment audit

The attachment hash functions use 64-bit FNV-1a reduced modulo 62^6 or 62^8. Their codomains have respectively 56,800,235,584 and 218,340,105,584,896 elements, approximately 35.73 and 47.63 bits. The generator resamples Math.random on each call, removes seed punctuation, and outputs seven alphanumeric characters with one of two space placements. It is not a deterministic seed hash. Stronger exact defect recovered by COST_CERTIFICATES and independently checked algebraically: every nonempty cleaned seed is ignored under a fixed random tape. If its length is s>0, the i-th index s+7i never wraps for i=0,...,6 because 8i<50. The i preceding removals make it select original random position 8i, wholly outside the seed. These tools cannot prove injective tagging of arbitrarily many histories.

COST_CERTIFICATES found a concrete six-character collision. REDTEAM independently executed the actual compact6CharHash extracted from 02-hash.html: both `pnp:4af52079e1a2cf84d4461513ff3e9756` and `pnp:b7bf65d9c5ec956423bc6173a00eb836` yield `kUWA9k`. This is a reproducible counterexample to digest injectivity.

Hash collisions alone do NOT prove SAT answer ambiguity: a hypothetical digest might separate YES from NO while merging same-answer inputs. The rejected claim is injective history identification or treating digest equality as an exact semantic merge certificate. Existing exact comparison guards in FORMAL-SPINE1 correctly avoid that mistake.

## Literature checks and implications

1. Baker, Gill, Solovay (1975), Relativizations of the P=?NP Question, DOI 10.1137/0204037. Original paper confirms both equality and separation oracles. The project must specify the failing oracle-relative step; it need not reject useful conditional arithmetic just because that arithmetic relativizes. https://cse.ucdenver.edu/~cscialtman/complexity/Relativizations%20of%20the%20P=NP%20Question%20(Original).pdf
2. Aaronson, Wigderson, Algebrization: A New Barrier in Complexity Theory. The barrier concerns algebraic extensions of oracle access, not whether a manuscript uses algebraic notation. Its associative-algebra extension also prevents treating noncommutativity alone as an escape. https://www.scottaaronson.com/papers/alg.pdf
3. Razborov, Rudich, Natural Proofs. The general-circuit barrier relies on a hardness assumption and formal constructivity/largeness/usefulness conditions. Do not invoke it as an unconditional prohibition on every combinatorial invariant. https://eccc.weizmann.ac.il/eccc-reports/1994/TR94-010/index.html
4. Hirahara, Unexpected Hardness Results for Kolmogorov Complexity Under Uniform Reductions, Theorem 3.9. Directly verified superpolynomial-time-bounded randomness is P-immune. This supports the stated conditional PFCERT implication but not existence of its verifier. https://eccc.weizmann.ac.il/report/2020/050/download
5. Cook, Reckhow, The Relative Efficiency of Propositional Proof Systems. The relevant existential short-proof property characterizes NP=coNP. A lower bound for a chosen weak proof system alone does not exclude all polynomial SAT algorithms. The author's homepage corrects Corollary 4.7 from P!=NP to coNP!=NP. https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf and https://www.cs.toronto.edu/~sacook/

6. Fortnow, Lipton, van Melkebeek, Viglas, Time-Space Lower Bounds for Satisfiability, Section 2.1, Theorem 3.1, Corollary 5.8. Independently verified original source. The random-access model excludes read-only input from workspace and charges index/work tapes; its SAT transfer computes requested reduction bits in polylog time and logarithmic workspace. At c=6/5, the displayed space threshold is d(c)=((c+2)/c^2-c)/2=23/45, above 1/2 by 1/90. Strict slack absorbs sufficiently small o(1) and local-reduction overhead, provided the same algorithm has both bounds. https://lance.fortnow.com/papers/files/tst.pdf

## New agent reports

LOWER_BOUND's proposed oracle-immunity lemma was reviewed from its explicit draft message. Verdict: accepted with guards communicated before finalization. Fix the same oracle on all machines; require constant description overhead and polynomial runtime simulation for the fixed universal oracle machine; charge query writing; use one polynomial witness bound; handle finitely many short n separately; use halting single-output semantics. The result is a barrier for universally relativizing verifier constructions, not unconditional nonexistence of the verifier in the unrelativized world.

MODEL_BRIDGE run_0001.md and model_bridge_contract.tex reviewed. Verdict: accepted at their stated conditional and bounded scope. MB1 preserves the SAT-subroutine exponent K; MB2 correctly retains a full fallback worst-case cost; MB3 includes every retained setup object in the accessor-space bound. The exact endpoint rational and recurrence checks pass. A codomain-count typo for the eight-character hash was corrected by the author: the value is 218,340,105,584,896. No substantive remaining defect identified.

LOWER_BOUND-0001.md and LOWER_BOUND-0001_formal.tex reviewed. Verdict: accepted under their declared ordinary and matched-oracle conventions. Positive-integer L(n), finite short-length exceptions, one witness bound, final halting outputs and an integer compression coefficient are explicit. The author repaired a universality ambiguity by using plain U only: prefix-free U cannot constant-description-overhead simulate every unrestricted plain machine. The generalized immunity/list-cover argument survives.

COST_CERTIFICATES report.md and cost_certificate_spine.tex reviewed. Verdict: accepted under repaired hypotheses. The author added one uniform asymptotic envelope, strict shortening above N0, and an exact terminating base solver; a finite-size self-loop would otherwise escape an asymptotic recurrence statement. The explicit certificate-enumeration bound and its universal-simulation bound are correct. In particular t(n)=2^(2^n) cannot admit the stated polynomial-witness cover. The explicit certificate-degree version is also valid: L(n)<=n^a and fixed polynomial universal overhead imply enumeration within 2^(d n^a+2dn+O(log n)), so a claimed t=2^(n^c) with c>max(a,1) is impossible. This does not rule out a slower fixed t or provide any verifier.

PROOF_MAP proof_map.tex reviewed. The finite single-child exponent calculation and its distinction from full balanced recursion are valid. Parent identified and author repaired the small-input gap by stopping at N0 and running the fixed total seed algorithm immediately. That guard is now present in the actual manuscript.

LOWER_BOUND LSPV_candidate_spine.tex reviewed. The quadratic-OR bias identity and resulting density bound are exact. O(w) bounded-fanin gate complexity and O(w log m) sparse encoding are properly distinguished. Trivial graph-separator and corrected interpolation lemmas are valid; all canonical full-range, source, Boolean projection and reconstruction obligations remain explicitly OPEN. The current author-hosted vMS journal PDF was opened independently; this reviewer does not claim full reconstruction-proof verification.

Final dispositions apply to the exact snapshots hashed in reviewed_artifacts.json. No proof-assistant or whole-repository build verification is claimed. Parent owns remote publication and repository-wide checks.

## Repository protocol reconciliation

Read repository CODEX.md, AGENTS.md, the pnp-research skill, red-team mode and research protocol, plus root MAIN authoritative reconciliation. Preflight on the recovered source tree returned OK, while that tree lacks materialized specialist directories; this is not full repository coverage. Current ROOT MAIN's OPEN status and corrected endpoint remain unchanged. The newly identified field-polynomial wording must be repaired only at matched current statements; historical reports remain audit evidence. The current-run review adopted valid conditional results, repaired the above hypotheses, and retired no broader route without a counterexample.

Single next target: audit a proposed source-checkable negative-case rule on the ARC15 UNKNOWN family, recursive descendants, and the current shielded SAT-hard fallback, with one joint operation/space ledger.

## RT-0009 — fixed trace checkpoints are delay-sensitive (2026-10-11)

Status: **PROVED/EXACT** for `FIXED-PREFIX-DELAY1`; **FALSIFIED/RETIRED** for `PREFIX-CHECKPOINT-UNIVERSAL1`; **COMPUTATIONAL** for the bounded audit. P versus NP remains **OPEN**.

For every fixed `N^r` dynamic checkpoint and exact polynomial decider `A`, the wrapper `D_r[A]` performs `N^(r+1)` input-independent steps before running `A`. Its prefix through the checkpoint is the same common shell for every source and embedded implementation, while full runtime is `N^(max{r+1,K}+o(1))`. A checkpoint compiler must therefore use charged static source/code analysis or wait and inherit the delay/solver exponent. The result is restricted to trace-prefix extraction and does not prove that arbitrary white-box normalization is impossible.

The audit passed 16,736 checks across all 255 nonempty three-variable clause subsets, DIRECT/MATERIALIZE/INTERP/RECOMP, DEAD/COPY/DELAY, encodings, padding, Horn, 2SAT, bounded treewidth, independent products, exact-(2,2) controls, and affine/Tseitin Gaussian elimination.

**Handoff:** formalize a static wrapper normalizer and attack totality, arbitrary exponents, unreachable code, padding, and replacement by a fixed solver. Report: `research/review/reports/redteam/2026-10-11_1136_RT-0009.tex`. Script: `experiments/review/fixed_checkpoint_delay_audit.py`. Raw result: `results/raw/review/2026-10-11_fixed_checkpoint_delay_audit.json`.

## RT-0010 — truth-independence dichotomy (2026-10-11)

**Status:** VERIFIED. **P versus NP remains OPEN.**

`OBLIVIOUS-DECIDE-EMIT1` is PROVED/EXACT using the Pippenger–Fischer oblivious-simulation theorem: input-independent schedules and branch-free multiplexing still allow decide-then-emit in `O(T log T)` time, retaining an arbitrary polynomial exponent `K`. `TERMINAL-NONINTERFERENCE1` is PROVED/EXACT: identical complete closed terminal views cannot reconstruct opposite source answers. Therefore `TRUTH-INDEPENDENCE-REPAIR1` is FALSIFIED/RETIRED as an unqualified bridge.

The bounded audit passed 11,445 checks across all 256 three-variable clause subsets, DIRECT/MATERIALIZE/INTERP/RECOMP, arithmetic/XOR/polynomial branch-free emission, Horn, 2SAT, bounded treewidth, affine/Tseitin, exact-(2,2), products, padding, renaming, complementation, duplicate clauses, fixed schedules, and exponent ledgers.

Next target: one explicit hereditary source identity with a positive, model-matched, `K`-independent full cost ledger; do not use absence of a visible branch or a semantic checker as the exclusion.

Report: `research/review/reports/redteam/2026-10-11_1236_RT-0010.tex`  
Script: `experiments/review/truth_independence_dichotomy_audit.py`  
Raw results: `results/raw/review/2026-10-11_truth_independence_dichotomy.json`
