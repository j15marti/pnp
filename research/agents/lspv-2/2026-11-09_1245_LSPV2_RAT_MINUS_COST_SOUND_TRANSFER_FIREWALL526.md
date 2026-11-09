# LSPV-2/526: No-new-variable RAT firewall for cost-sound CDCL abstractions

**November 9, 2026, 12:45 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

Affected proof-chain evidence: **[P2-L2-526]**, refining [P2-L2-524] and [P2-L2-525]. Unresolved: [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-C3], [P2-B1], [P2-B2].

## IDEA, falsifiers, SEARCH, ITERATE

Initial hypothesis, **falsified**: banning fresh auxiliary variables is sufficient to extend the cost-sound RUP/Resolution-block abstraction of /524–525 to every original-variable clause-learning and inprocessing rule. A legal original-variable RAT addition can change the models, not merely derive an implied clause. Moreover, published random reordered-parity 3-CNFs have exponential ordinary-DAG-Resolution lower bounds and short DRAT-minus proofs with *no new variables*.

F1: the RAT addition is RUP after all. F2: a needed resolvent is not AT. F3: the cited asymptotic family lacks either an ordinary-DAG-Resolution lower bound or short DRAT-minus proof on the same original 3-CNF. F4: an unqualified transfer somehow permits RAT, original-source mutation or GF(2) while claiming the older RUP-only theorem. F1–F2 fail by symbolic argument and independent concrete replay. F3 is disposed of by primary publications [1,2]; F4 remains an explicit exclusion, not a model-general claim.

Revised candidate: every cost-sound MAY abstraction for deletion-enabled, original-variable DRAT must represent a satisfiability-preserving but non-entailment RAT transition as a **distinct** legal operation, with its source-authenticated pivot checks and real cost. A refinement that demands RUP reasons for RAT is unsound.

## Theorem 526.1: a parameterized genuine RAT but non-RUP transition

Let a,b_i,c_i (1<=i<=k) be distinct original variables, k>=1, and take proper signed 3-CNF

$$
F_k=\bigwedge_{i=1}^{k}
(a\lor b_i\lor c_i)\land(\neg a\lor b_i\lor c_i).
$$

There are 2k+1 variables and 2k clauses. The models number exactly 2*3^k because F_k is equivalent to the conjunction of (b_i OR c_i).

The **one-clause addition** C=(a), with original pivot a, is RAT. For each original D_i=(not a OR b_i OR c_i), the RAT resolvent is R_i=(b_i OR c_i). Under F_k and assumptions not b_i, not c_i, unit propagation derives both a and not a from the two corresponding original clauses, so every R_i is AT. The RAT addition uses **no** new variables. But C is **not RUP**: under assumption not a every original clause is either already true or becomes the non-unit (b_i OR c_i); no unit conflict occurs. In fact F_k does not entail a, since a=0 with b_i=c_i=1 satisfies F_k. Adding a retains satisfiability, but removes some models.

Hence no source-rooted ordinary Resolution DAG, of **any size**, derives (a) from F_k. An abstraction in which every learned step is a consequence-preserving Resolution block cannot overapproximate all RAT behavior. This obstruction is **transition-level** and uses a SAT source, not a false UNSAT certificate.

CEGAR controls: a coarse rule that calls (a) an RUP clause is spurious; original-source UP replay rejects that classification. A pivot-and-AT replay accepts the genuine RAT action. Removing a positive source clause destroys the AT witness for its paired resolvent; a subsequent attempted opposite RAT after adding (a) is rejected. Replacing the RUP guard with an exact RAT guard refines only the declared RAT species and preserves its real shortcut.

## Published asymptotic proof-system firewall, exact 3-CNF

The established family rPar(n,sigma) of [1] has two conflicting parity chains, each with n-2 XOR-of-three factors encoded by exactly four proper signed 3-clauses. The chains use the same n original input variables, a permutation sigma in the second, and two *disjoint blocks of variables already in the source* of length n-3. Thus the source has 3n-6 variables and 8(n-2) clauses; its indexed original-bit length is O(n log n).

More exactly, for an ordering (y_1,...,y_n) and auxiliary source variables (t_1,...,t_(n-3)), the factors impose y_1 XOR y_2 XOR t_1=0; t_i XOR y_(i+2) XOR t_(i+1)=0 for 1<=i<=n-4; and t_(n-3) XOR y_(n-1) XOR y_n=d, with d=0 in the first chain and d=1 in the permuted second chain. Every three-variable parity factor has the canonical 4 signed proper 3-CNF forbidding assignments of the wrong parity. The original source is UNSAT, without assuming a solver oracle.

**KNOWN THEOREMS.** Chew, de Colnet, Slivovsky and Szeider (AAAI 2024), Theorem 1 [1], prove that with probability tending to 1 over uniformly random permutations sigma, the shortest **unrestricted ordinary DAG Resolution** refutation has size at least 2^(alpha*n) for a constant alpha>0. Chew and Heule (2020) [2] construct **O(n log n) DRAT-minus refutations on the same source without any fresh variables**. DRAT-minus permits deletion; do not conflate it with deletion-free RAT-minus [3].

**Corollary 526.2 (derived, PROVED/RESTRICTED):** There is no universal translation from *all* such DRAT-minus certificates into original-variable-only RUP-only certificates of length polynomial in source size plus DRAT length. Such a translation, combined with the established /524 RUP-to-Resolution simulation with at most v=O(n) ordinary Resolution nodes per RUP record, would give polynomial Resolution size on hard rPar instances and contradict [1]. No assumption about the computational hardness of SAT, or about existence versus acquisition cost, is used.

This also means that an alleged superpolynomial goal-distance invariant transferred purely from ordinary Resolution cannot be **cost sound for original-variable DRAT-minus** on the rPar family: a legitimate short proof path exists. This does not invalidate [P2-L2-525] for the precisely defined RUP-logging CDCL class, and does not prove a shortcut is native to historical R_mix341. For R_mix341, its fixed historical grammar and weights still require independent accepted-byte authentication.

## Independent replay and resources

Two independent standard-library programs generated/read actual original signed CNF source bytes and independently compared SHA-256 digests. Python passed **408 assertion groups**. An independently authored Node.js reimplementation passed **297 checks**, with zero failures. For k=1..24, 24 proper 3-CNF sources had RAT(a)=true, RUP(a)=false, models with both values of a, rejection of a deleted-source test and an invalid opposite-RAT follow-up. For k<=5, exact 2*3^k model counts were checked exhaustively. Nine **separate original rPar 3-CNF** instances (n=4,5,6; identity, reversal and rotation permutations) were checked UNSAT by exhaustive assignment enumeration in both languages and source SHA matched. Both rejected seven malformed input controls. Finite n=4..6 rPar checks do not certify the asymptotic theorem for a particular random permutation.

The RAT macro is one **logical** paid record but requires k RUP/AT subchecks. In the Python source-scan policy this costs exactly k(k+1) clause scans, 3k(k+1) literal tests and k propagated units for each k. Across k=1..24: **5,200** scans, **15,600** literal tests and **300** propagations. They are host-language counts, not same-FLMV-machine bit-time/peak-space guarantees. Original-source reading, malformed parsing, certificate checks, failed paths, output bytes, branch-context joins, shared DAG references, copies and recomputation must be charged in any physical algorithm.

**Executable files:** experiments/arc/lspv2_526_rat_minus.py and experiments/arc/lspv2_526_rat_minus_independent.mjs. **Raw files:** results/raw/arc/2026-11-09_1245_LSPV2_526_RAT_MINUS_PYTHON_RAW.json and results/raw/arc/2026-11-09_1245_LSPV2_526_RAT_MINUS_JS_REPLAY.json. Five-role handoff: research/coordination/2026-11-09_1245_LSPV2_RAT_MINUS_FIVE_ROLE_HANDOFF526.md. The complete exact local script/raw/source-lookup archive is separately retained as a durable reproducer.

## Continuity and corpus

Actual governing abstract-negative five-role handoff, both current proof trackers, issue #3, AGENTS.md, CODEX.md, research SKILL, /524, /525, LSPV-1/542, LSPV-3/540, LSPV-5/466, Grok's GROKPROOF/2026-11-09_2015_PROGRESS.md, Claude world ledger and MODELBRIDGE-0010 were inspected. The generic arbitrary-program normalizer remains retired. Change-aware repository checks verified konard/p-vs-np README blob 0e0ec77f and scripts/proof_status.json 93b77ed3, blkph0x/p-vs-np-proof-research README f397a774 and METHOD_INDEX 18d693ea. Existing /524–525 reports cover FRAT-XOR, DRAT-trim, CNFgen and openai/math; no formal model transfer was inferred from their badges. Primary full-text HTML for [1], author/publisher source for [2,3], ACDCL and complete-shell methodology were consulted. No native FLMV or historical R_mix341 executable was run.

**Status:** [P2-L2-526] PROVED/RESTRICTED + COMPUTATIONAL; [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN. The all-input recursively iterable same-machine transformation with t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2) for every fixed uniform polynomial SAT decider is **not** established. Nor is a full R_mix341 lower bound or noncircular B3. Preserve all five roles, 2 Route A / 3 Route B and historical weights, identities, schedules and enabled states. **P versus NP remains OPEN.**

## Primary references

[1] Chew L, de Colnet A, Slivovsky F, Szeider S. *Hardness of Random Reordered Encodings of Parity for Resolution and CDCL*. AAAI 2024, Theorem 1. https://arxiv.org/abs/2402.00542

[2] Chew L, Heule MJH. *Sorting Parity Encodings by Reusing Variables*. 2020. https://pmc.ncbi.nlm.nih.gov/articles/PMC7326471/

[3] Buss SR, Thapen N. *DRAT and Propagation Redundancy Proofs Without New Variables*. LMCS 17(2), 2021. https://lmcs.episciences.org/7400

[4] D'Silva V, Haller L, Kroening D. *Abstract Conflict Driven Learning*. POPL 2013. https://www.kroening.com/papers/popl2013.pdf
