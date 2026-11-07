# LSPV-3/462: Dual Skolem sections and globally shared source retraction

2026-11-06 18:19 PST | Route B | PROVED/RESTRICTED symbolic, COMPUTATIONAL finite checks. P versus NP OPEN; historical R_mix341 grammar and unit weights unchanged.

## IDEA, falsifiers, search, revision

Hypothesis: LSPV-1/461's exponential flat-CNF image of a syntactically possible cross-row splitter line under a fixed prefix Skolem section can be eliminated by an alternative **suffix** section chosen for that line, but coherent use of the SAME row sections across two opposing lines creates an exact minimax tradeoff. Falsifiers: F1, exact source gadget projection fails; F2, a smaller flat exact CNF exists; F3, conditional-expectations selector violates its output bound; F4, the scoped result is mistakenly promoted to a legal proof-to-proof transfer. F1-F3 passed proofs and independent finite verification. F4 is explicitly excluded.

## Existing certified hard-family anchor and exact encoding

Source: de Rezende, Nordström, Risse, Sokolov, Exponential Resolution Lower Bounds for Weak Pigeonhole Principle and Perfect Matching Formulas over Sparse Graphs, TheoretiCS 4 (2025) article 9, DOI 10.46298/theoretics.25.9, published March 25, 2025. Peer LSPV-1/461 specifies an eligible regime: fixed integer k>=2, epsilon in (0,1), m=n^k pigeons, n holes, fixed constant left degree d=(16k/epsilon)^2 (appropriate integral rounding), and independently sampled d-hole neighbors. Original functional-PHP CNF uses d-literal pigeon rows and binary collision/functionality clauses; the paper proves exp(Omega(n^(1-epsilon))) ordinary shared-DAG Resolution clauses with high probability in its theorem regime. This is not historical mixed-system hardness.

Standard proper strict-three encoding chains each original pigeon row of width d into d-2 proper width-three clauses using d-3 fresh private splitters. Each original binary clause (u OR v) may be padded to strict-three using fresh z as (u OR v OR z) AND (u OR v OR not z). If B is binary source count, the result has m(d-2)+2B strict-three clauses and md+m(d-3)+B variables. This is satisfiability preserving, NOT yet lower-bound preserving. The independent width-four examples below are only semantic controls, not an invented hard formula or a sampled UNSAT certificate.

Predecessors: LSPV-3/445 gives the isolated chain projection and exact local consequence cost. LSPV-1/461 (blob 135408d71d69695dbb492e86a68987e8f518a425) proves a FIXED prefix-section cross-row 2^t flat CNF obstacle, without claiming the syntactic line is legally derived. This run adds a genuine alternate-section shortcut, a two-line shared-choice exact tradeoff, and a global deterministic conditional-expectations bound, without claiming novelty beyond that precise distinction.

## Theorem 462.1: Two total exact Skolem sections

For a width-k clause C=l_1 OR ... OR l_k, k>=4, let its private proper 3-CNF chain comprise first clause l_1 OR l_2 OR y_1, middle clauses (not y_(j-1) OR l_(j+1) OR y_j) for 2<=j<=k-3, and last clause (not y_(k-3) OR l_(k-1) OR l_k).

Two whole-chain total sections for EVERY original assignment are

$$
P:\quad y_j=\bigwedge_{r=1}^{j+1}\neg l_r,\qquad
S:\quad y_j=\bigvee_{r=j+2}^{k}l_r.
$$

Under P every chain clause except the last is a tautology, and the last is exactly C. Under S every clause except the first is a tautology, and the first is exactly C. Consequently the entire gadget after either section equals C on ALL original assignments. This is a semantic source projection, not a native R_mix341 derived proof line.

For independent four-literal rows C_i=a_i OR b_i OR c_i OR d_i, the chain is (a_i OR b_i OR y_i) and (not y_i OR c_i OR d_i), and the two sections are P: y_i=not a_i AND not b_i; S: y_i=c_i OR d_i.

Consider a syntactically possible clause D with exactly one signed first-splitter literal from each of some independent rows, with no other literals. Choose one section sigma_i in {P,S} for each row globally. Let mismatch count m(D,sigma) count positive y_i assigned P and negative y_i assigned S.

**Exact flat source-CNF theorem** (full Boolean equivalence, no additional variables or circuits):

$$
\operatorname{CNFsize}(D^\sigma)=2^{m(D,\sigma)}.
$$

Proof: matched signs become source disjunctions; mismatched signs become conjunctions of TWO signed original literals with disjoint underlying variables. Distributing gives the upper bound. Set all matched disjunct literals false and apply the 2^m distinct one-true/one-false assignment witnesses across m independent pairs. Every non-tautological implicate must contain a literal falsified in every pair and can exclude at most one of these witnesses, requiring 2^m clauses. When m=0 the result is a single clause.

**New positive shortcut:** For ANY ONE such line, choose S on its positive splitters and P on its negative splitters. Then m=0 and the flat source image is ONE clause, regardless of line width. Therefore the fixed-prefix exponential example is not unavoidable under free single-line choice.

## Theorem 462.2: Globally coherent section tradeoff

For t disjoint four-literal rows consider two syntactically possible lines

$$
D_+=\bigvee_{i=1}^t y_i,\qquad
D_-=\bigvee_{i=1}^t\neg y_i.
$$

With p globally prefix and q=t-p globally suffix sections, the exact *separately equivalent* flat CNF clause counts are 2^p and 2^q. Thus

$$
\min_\sigma(2^p+2^q)
=2^{\lfloor t/2\rfloor}+2^{\lceil t/2\rceil},
$$

$$
\min_\sigma\max(2^p,2^q)=2^{\lceil t/2\rceil}.
$$

These are bounds on **separate linewise no-new-variable equivalent CNFs**, NOT on the joint conjunction, existence of short native proof lines, an actual refutation DAG, or any proof system admitting shared definitions. Each splitter has one globally coherent meaning; adapting independently for two lines silently changes the semantics.

## Theorem 462.3: Deterministic all-line choice

For explicitly supplied signed splitter clauses D_1,...,D_L with at most one splitter per independent row in each line, let T(sigma)=sum_j 2^{m(D_j,sigma)}. If rows independently select P or S uniformly and k_j counts splitter literals in D_j, then

$$
\mathbb{E}_{\sigma}T(\sigma)=\sum_{j=1}^L(3/2)^{k_j}
$$

and hence there exists one GLOBAL section assignment with

$$
\min_\sigma T(\sigma)\le\sum_{j=1}^L(3/2)^{k_j}.
$$

A deterministic polynomial-bit-cost conditional-expectations algorithm finds one: set each remaining row to whichever P/S choice minimizes the expected remaining total. A line with a already mismatched and r unassigned splitter literals contributes 2^a 3^r/2^r, so all rational calculations have O(number_of_rows + log(L+1)) bits. Actual explicit CNF construction may still require exponential output; paid-DEF/circuit alternatives and different derivations remain valid.

## Verification, source and trust boundaries

Python independently exhaustively checked all original assignments t=1..4 and 2^t orientations, verified each canonical representation and clause-deletion witnesses through t=3 (2,164,878 counted tests); exact size ledger t=1..8. Separate deterministic optimizer checked 64 n<=8 line collections including opposite-polarity pairs, against brute-force optima. Independently written no-import Node verifier passed **6,459,851** assertions and rejected four corruption controls. Focused SAT control source: three disjoint strict-three private chains, SHA256 6975625848dc4c641fb261847ad2b9b938fb49faaa79d25be74b41382dd52e99. Python producer wall 23.85 sec and tracemalloc peak 22,632 tracked bytes (NOT process RSS). Full raw cases, code, independent verifier and hashes in conversation archive LSPV3_462_DUAL_SECTION_SHARED_OPTIMIZER_REPRO.zip; repository small replay and summary also supplied.

All claims concern exact linewise Boolean representations. **No actual cross-row line is proved to occur in a legal refutation of the established hard family**. Substitution of Resolution lines does NOT by itself yield Resolution steps. Historical accepted-byte DEF facets, exported/private LOCAL-CONVERT ports and checker remain unauthenticated; no P2-B1, B2 or B3 result. Soundness demands source IDs, assumption scope, globally fresh definitions and legal branch AND obligations. Paid logical work, proof evidence bits, serialization, verifier, time, depth and peak space remain separate.

## Tracker and external corpus audit

Both current root trackers read: proof1.txt blob 0c24df268207e9436d51519ec168a984ab10ae3e and proof2.txt (current-head read). Relevant P1-01/P1-03/P1-X1 and P2-D1/D2/B1/B2/B5/F3/F4/F6/F7/C1/C3, all still correctly OPEN where load-bearing. Material narrow evidence for P2-F6/F7 recorded as new role-owned P2-L3-462, not a promotion of the proof spine.

Read governing AGENTS.md, CODEX.md, pnp-research skill, original /341 blob c87acd11, 2026-11-02 five-role handoff, LSPV-1/461, LSPV-3/445, LSPV-5 REFEREE350 blob 569ddc1f, actual GROKPROOF progress blob a20fb8b3 and Claude WORLD-LEDGER blob 79e4d4e7. External files read: konard/p-vs-np scripts/proof_status.json blob 93b77ed3; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea and resolution_width_lab/THEOREM.md blob b9030425; meelgroup/frat-xor/format.md blob 986a21aa; openai/math/README.md blob cc5b0a03. No other repo has the authoritative native R_mix341 acceptance grammar. Issue #3 body was located with connected GitHub search; full comments not exhaustively read. A limited root main.tex read returned zero bytes for blob f43c4e1e, so no unsafe manuscript overwrite. Local repo preflight unavailable without full checkout.

**Next obligation:** certify an actually legally derived, source-authenticated mixed shared-DAG proof-line pair on an established hard strict-three family or a polynomial rule-specific accepted-byte backtranslation. B3 same-preselected-system reflection remains OPEN. Maintain 2 Route A / 3 Route B, exactly five agents, all original task IDs/schedules/titles/weights, and P versus NP OPEN.

References: [1] de Rezende et al. TheoretiCS 4 (2025) article 9, https://theoretics.episciences.org/15419. [2] Cook, A Short Proof of the Pigeon Hole Principle Using Extended Resolution, SIGACT News 8(4) (1976). [3] Project LSPV-1/461 and LSPV-3/445. [4] FRAT-XOR/format.md (different proof language).