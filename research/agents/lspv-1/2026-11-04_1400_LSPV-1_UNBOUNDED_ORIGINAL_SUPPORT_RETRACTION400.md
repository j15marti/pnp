# LSPV-1/400: Unbounded Original-Support Inflation Under Source Retraction

**November 4, 2026, 14:00 PST.** **Status: PROVED/EXACT elementary all-k theorem under a declared origin-support interpretation, pending independent specialist review; COMPUTATIONAL nine finite controls.** Original R_mix341 rules, five roles, schedules, enabled states and weights unchanged. B1/B2/B3 and P versus NP OPEN.

## IDEA before SEARCH

Initial falsifiable idea: under SAT in P, polynomial-normalized refutation budgets yield a polynomial-time exact proof extractor without converting the SAT decider trace. Project search found this result already in LSPV-1/364, expanded by Red Team REFEREE344. **Retired as duplicate** rather than claimed as novelty.

Revised idea: peer LSPV-3/402 exhibited a four-input case where copying every inference after source retraction invalidates the AND3 original-support type. **Prediction:** the mismatch can grow without bound even when the evaluator has a constant four-node refutation. This tests the missing representation transfer rather than regenerating a hard family.

## SEARCH and documented corpus

Read the Nov. 2 12:04 governing directive (current blob c3889a3e), coordination issue #3, AGENTS.md (19656af1), CODEX.md (754999f5), research skill (b8df83a7), the original mixed rule specification in LSPV-2/341 (c87acd11), LSPV-1/364 (0a8e47cd), /397 (0568e162), current /398 and /399 issue handoffs, Red Team REFEREE344 (3b374229), and the underlying LSPV-3/402 original-support report (4b301395). The four-input counterexample is ALREADY /402. The increment here is an all-k, explicitly counted family and independent verification. LSPV-1/397 already contains the correct restricted alternative of compiling typed local steps to Res(oplus) before cofactoring paid gates, at exponential possible backtranslation overhead.

Read actual Grok GROKPROOF/2026-11-04_2113_PROGRESS.md (a5bba58d) and Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6). Neither supplies the missing all-input B3 compiler. Grok's statement that a strict Omega(N^1.1) writing cost is already beyond N^(1.1+o(1)) was corrected in LSPV-1/399 and is not reused. Claude's one-tape bound cannot be transferred to general random-access SAT.

General web queries: Cook Reckhow polynomial bounded proof search; substitution variable by circuit resolution proof width; Tseitin gate encoding proof source retraction; Thapen resolution width tradeoff. Relevant primary literature: Haken (1985) unrestricted shared-DAG ordinary Resolution PHP lower bound; Cook (1976) polynomial Extended Resolution PHP proofs; Cook--Reckhow (1979); Thapen (2016) width-length tradeoff in a different restricted model. GitHub organization openai queries: ExecCNFNodeSearchCosts, CookLevin, Resolution proof checker, Tseitin encoding gate, support variables. Actually read openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (blob 1ced21f4): it accounts for a specific executed SAT search and stack work, not source-retracting proof conversions. Direct Google-branded search was unavailable; general web search and authenticated GitHub were used instead.

## Fixed calculus and published hard-family distinction

Fix unchanged R=R_mix341. Valid general signed DIMACS original clauses cost zero; each distinct RES, AND3, GF(2) XOR, justified LOCAL-CONVERT or conservative two-input DEF DAG node costs one. Every new node has at most two paid ancestor/source parents. AND3 accepts two conditions with at most THREE ORIGINAL source variables in their combined support. We use the transitive original-support interpretation of paid gate outputs used by LSPV-3/402, not an unproved atomic-auxiliary reinterpretation of the native grammar.

Haken: for constants c>0,h0, for every h>=h0 and EVERY ordinary unrestricted shared-DAG Resolution refutation of the explicit unary PHP(h+1,h) CNF, at least 2^(c h) proof lines are required. The source has h(h+1) variables, (h+1)+h*binom(h+1,2) clauses, binary indexed input length Theta(h^3 log h). This is NOT an Extended Resolution, Res(oplus), mixed R, or arbitrary SAT-machine lower bound. Cook's polynomial ER PHP proof is the mandatory escape. Our small examples below are transfer controls, not claimed hard instances.

For valid UNSAT F, W_R(F) is the minimum number of distinct paid nodes in any genuine shared-DAG refutation, and Wbar_R(N) is its maximum over valid UNSAT encodings of length at most N, or zero when empty. B1: for every total correct uniform A, some polynomial p_A satisfies W_R(F)<=p_A(N(F)+T_A(F)) on every UNSAT F. B2: for every A, Wbar_R(N)<=p_A(N+T_A^wc(N)), worst case over ALL binary inputs including malformed. B3: SAT in P implies Wbar_R(N)=N^O(1) for this SAME R. B1 implies B2 implies B3. All remain OPEN.

## ITERATE: theorem and proof

**Theorem 400 (origin-support noncommutation).** For every k>=4, there is an UNSAT signed source formula F_k with O(k log k) input bits and a polynomial-length source-authenticated fan-in-two evaluator CNF E_k containing 3k+1 source clauses. E_k has a four-paid-node valid mixed refutation. Its last AND3 node observes one original evaluator variable, but after promotion of that evaluator variable to a paid conservative gate output of the original F_k, its input-condition support contains all k original variables. Consequently a translation which unconditionally copies every typed AND3 node unchanged is UNSOUND AS A TYPED TRANSLATION under transitive original-support semantics.

Proof: put
$$
F_k=(x_1)\land\cdots\land(x_k)\land(\neg x_k).
$$
Let p_2=x_1 AND x_2, p_j=p_(j-1) AND x_j for 3<=j<=k, p=p_k, and r=p AND NOT x_k. Construct E_k from the three standard source clauses for each of the k AND2 gates, plus the source unit (r). A gate z=a AND b, allowing b to be a negated input literal, contributes
$$
(\neg z\lor a),\quad(\neg z\lor b),\quad(z\lor\neg a\lor\neg b).
$$
Every original assignment extends uniquely to gates, so SAT(E_k) iff SAT(F_k); both are UNSAT. In E_k, p and r are original evaluator source variables. Three valid strict Resolution steps give:
$$
(r),(\neg r\lor p)\vdash(p),\qquad
(r),(\neg r\lor\neg x_k)\vdash(\neg x_k),\qquad
(\neg x_k),(\neg p\lor x_k)\vdash(\neg p).
$$
AND3 combines (p) and (NOT p) into contradiction. The combined support of its input conditions is the one original E_k variable p. But after retraction p is paid, with defining Boolean function AND_(i=1)^k x_i. Each x_i is essential to this function, so the union of original supports of the SAME INPUT CONDITIONS has size k>3. The original typing does not survive unchanged. QED.

**Precise scope:** the source-retracted original formula F_k has an immediate one-node Resolution proof from (x_k) and (NOT x_k). Even the problematic fourth step can be replaced by a legal RES from (p),(NOT p) to empty. Thus this example does NOT falsify an appropriate cost-reflection inequality, the existence of a different polynomial compiler, or B3. If the actual native rule counts paid gate outputs as atomic support variables, the original grammar must be authenticated separately; the theorem is deliberately conditional on origin-support typing. Source-retraction and local-rule normalization cannot be assumed to commute without checking this typing.

Falsifiers: F1, all AND3 nodes copy unchanged, **FALSIFIED** for every k>=4. F2, canonicalizing the constant FALSE output repairs input support, **REJECTED**, since AND3 checks combined premise support. F3, no sound source-retracting proof exists, **FALSE**, direct RES repairs the example. F4, the four-node witness proves physical machine hardness, **FALSE**, all sources and proofs are polynomially encoded.

## COMPUTATIONAL and physical cost ledger

The dependency-free Python producer tested k=4,5,6,7,8,10,16,32,64, checks every gate's 4 local assignments, all three strict pivots, both source labels, origin supports 1->k, forged pivots and malformed variable IDs. For k<=6 it additionally exhaustively checks all 2^(2k) evaluator assignments. A separately written JavaScript checker reconstructed the gate clauses, truth assignments and pivots from published raw records and passed **1,944 independent assertions**. Finite programs do NOT verify every native R_mix341 operation.

Evaluator has 3k+1 clauses, 2k variables and O(k log k) indexed source bits. Source construction, bit reads, pivot evaluation, type bookkeeping, verification and output require additional polynomial work and memory beyond the four PAID logical nodes. No FLMV same-machine transfer is inferred; all-phase peak space and any allocate-then-free stage must be charged using s'<=max{rho,eta,lambda,lambda*s}. Any expensive intermediate representation is allowed but not uncharged.

## Outbox and next handoff

Report: research/agents/lspv-1/2026-11-04_1400_LSPV-1_UNBOUNDED_ORIGINAL_SUPPORT_RETRACTION400.md
Producer: experiments/arc/lspv1_400_support_retraction.py
Independent checker: experiments/arc/lspv1_400_independent_verify.js
Raw: results/raw/arc/2026-11-04_1400_LSPV1_SUPPORT_RETRACTION400.json
Coordination: research/coordination/2026-11-04_1400_LSPV1_SUPPORT_RETRACTION400_FIVE_ROLE_HANDOFF.md

Root main.tex fetch_file returned blob SHA 761af522c1d47594e1aa3ff3555c47626688c9b7 **but zero file bytes**. A full preservation comparison is unavailable, so no potentially destructive partial overwrite was attempted. The dated report and handoff constitute the explicit publication fallback.

LSPV-2: authenticate paid-gate support and LOCAL-CONVERT export semantics. LSPV-3: audit source-retraction typing and factor replay. LSPV-4: charge proof compiler, bit access and peak space. LSPV-5: test substitution RES, GF(2), auxiliary and semantic shortcuts. LSPV-1: independently pursue B3 and a superpolynomial worst-case mixed minimum. **P versus NP remains OPEN.**
