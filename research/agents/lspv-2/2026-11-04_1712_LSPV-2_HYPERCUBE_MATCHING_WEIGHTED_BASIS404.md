# LSPV-2/404: All-arity hypercube matching theorem for exact weighted CNF bases
**Date:** November 4, 2026, 17:12 PST. **Status:** PROVED/EXACT for a separate output-only weighted exact-CNF basis optimization, COMPUTATIONAL for exhaustive k<=4 atlas; B1/B2/B3, mixed-calculus superpolynomial bounds, and P versus NP OPEN. LSPV-2 role and R_mix341 unchanged; specialist review pending.

## IDEA before SEARCH
Extending the already verified k=3 output-basis maximum 24 in LSPV-5/312, hypothesize that for every k>=2, the **weighted** auxiliary-free exact-basis maximum is 3(k-1)2^(k-1). Proposed mechanism: pair Boolean assignments into hypercube edges and exclude zero, one or both endpoints per edge with one clause. Four falsifiers: (F1) a k=4 relation has minimum weighted basis >72; (F2) an equivalent parity CNF contains a clause omitting a variable; (F3) the result disallows compact auxiliary circuits or GF(2) (invalid overreach); (F4) output weight equals minimum native proof cost or machine time (invalid overreach).

## SEARCH and corpus
Read first the required November 2 five-role refocus (research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md, blob c3889a3e), issue #3, AGENTS.md (19656af1), CODEX.md (754999f5), project skill (b8df83a7), fixed R_mix341 /341 (c87acd11), LSPV-2/358 (60f99ebf), LSPV-2/403 (ec4bcf49), Red Team /312 (5bf58dbe), /315 (66a18447), LSPV-2/374 (eb6f1a03), Grok GROKPROOF/2026-11-04_2315_PROGRESS.md (f5b8ef62), and Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6). Grok still leaves universal charged ARC extraction OPEN; Omega(N^1.1) output writing is not a strict contradiction of N^(1.1+o(1)). Claude's one-tape crossing bound is model-specific; neither proves B3.

Actual general-web searches: CNF parity XOR no auxiliary variables requires 2^(n-1) clauses proof; Tseitin formulas resolution exponential proof Gaussian elimination polynomial XOR reasoning expander; Extended Resolution polynomial proof pigeonhole Cook 1976 Haken; parity CNF encodings auxiliary variables. Read original MFCS 2022 publisher page, Emdin, Kulikov, Mihajlin, Slezkin (DOI 10.4230/LIPIcs.MFCS.2022.47), confirming **known** parity 2^(k-1) minimum and auxiliary-variable tradeoffs. AAAI source denied access, MDPI returned 429; direct Google-branded search unavailable, general search used. Authenticated GitHub queries: openai organization parity CNF xor and resolution proof, project CNF Encodings of Parity, LOCAL-CONVERT, DPLL-IMPLICATE-PRUNE358, binary gate parity k-1. Read OpenAI/math file lean/OAI/Computability/DirectedFeedback/Machines/FinalCNFTime.lean (blob 1d815654); it does not implement an R_mix341 compiler. Source code is not a premise of the theorem. Prior /312 already proved k=3=24; prior /374 already proved a parity portwise representation gap. No academic novelty of the parity clause lower bound is claimed.

## Model and theorem
The **unchanged** R_mix341 has authenticated free CNF sources, unit-paid at-most-binary-parent RES, three-variable AND3, binary GF(2), locally justified LOCAL-CONVERT and conservative two-input DEF. The following is a **separate auxiliary-free output-basis** metric, not native minimum proof DAG cost.

For k>=2 and every relation Q subset {0,1}^k, let Gamma range over all equivalent exact non-tautological auxiliary-free CNFs on the named original variables, with nonempty clauses. For a clause of width s set the already proved LSPV-2/358 safe exact-consequence compiler weight
$$
b_k(s)=2^{k-s}-1+3\max\{s-1,0\}.
$$
Define
$$
M_k=\max_{Q\subseteq\{0,1\}^k}\min_{\Gamma:\operatorname{Mod}(\Gamma)=Q}\sum_{C\in\Gamma}b_k(|C|).
$$
**Theorem 404.1 (PROVED, all k>=2):**
$$
\boxed{M_k=3(k-1)2^{k-1}.}
$$
Both parity relations attain the maximum, with no uniqueness claim at k>=5.

**Proof, universal upper bound.** Partition the k-cube into 2^(k-1) disjoint edges, each with x2...xk fixed and x1 free. For each edge: if neither endpoint is forbidden, emit nothing; if just one is forbidden, emit its width-k blocker; if both are forbidden, emit the width-(k-1) clause whose falsifying assignment on x2...xk matches the edge. These clauses jointly reject exactly the complement of Q. Singletons cost b_k(k)=3(k-1), doubletons b_k(k-1)=3k-5<=3k-3. Total weight is <=3(k-1)2^(k-1).

**Proof, matching lower bound.** Every non-tautological clause in an equivalent auxiliary-free parity CNF must mention all k variables, since otherwise flipping an omitted variable changes parity but leaves the clause false. Every width-k clause rejects one assignment. At least 2^(k-1) clauses are needed to exclude all wrong-parity assignments, each of weight 3(k-1). Equality follows. The no-auxiliary parity clause minimum is classical; the all-k **particular B(k,s) weighted minimax** generalizes the project /312 calculation.

## ITERATE: independent exhaustive finite tests
Python producer uses Dijkstra on the bitmasks of excluded assignments, building unions of clause-exclusion subcubes. An independent Node verifier uses cardinality-layer DP, independent clause polarity enumeration, checks entire distance-vector SHA-256, histogram, parity opposite labels and malformed controls.

| k | All functions | Proper clauses | Max cost | Maximizers | Independent transitions |
|---:|---:|---:|---:|---:|---:|
| 2 | 16 | 8 | 6 | 2 | 128 |
| 3 | 256 | 26 | 24 | 2 | 6,656 |
| 4 | 65,536 | 80 | 72 | 2 | 5,242,880 |

No disagreements. Complete k=4 distance SHA-256: e0199f728eb2b3f49208d005a1f9a33562b4b1961ccb5c0535f92538d68b587a. Both parity relations are SAT separately; their conjunction UNSAT. Six Python and five Node malformed truth-table grammar controls rejected. /312 treated false as an early contradiction with cost 7, while the present exact **CNF basis** optimizer represents false by two contradictory units for weight 6 at k=3; this shifts only one histogram count and does not change 24 or its maximizers.

## Limits, costs and bridge
Haken (1985): for some c>0 and all large h, EVERY ordinary shared-DAG Resolution proof of the explicitly encoded unary PHP_(h+1,h), h(h+1) variables, m_h=(h+1)+h*binom(h+1,2) clauses, N_h=Theta(h^3 log h) signed-index DIMACS bits, has at least 2^(ch) lines. This is not about all SAT algorithms or R_mix341. Cook (1976) gives polynomial Extended Resolution PHP proofs. On odd bounded-degree Tseitin expander CNF the published ordinary Resolution lower bound does not transfer to fixed R_mix341, where the prior exact optimum is 4h-1 paid nodes using AND3/GF(2). These are mandatory controls against reversed transfer.

Explicit auxiliary-free parity output uses 2^(k-1) clauses and Omega(k2^k) literal writes, whereas conservative paid gates and GF(2) have compact encodings. The all-k weighted basis is not a lower bound for native R_mix341 proofs; searching the entire 2^(2^k) atlas is not a polynomial SAT decider. Actual parsing, bit access, intermediate encoding, verification, output and peak live memory are separately charged, with s'<=max{rho,eta,lambda,lambda*s} and transient N-bit preprocessing rho>=1. Opaque LOCAL-CONVERT payloads remain unresolved and REFEREE315 already falsifies logical-node-only evidence domination.

B1, B2, B3, superpolynomial Wbar_Rmix341 and P versus NP remain OPEN. **Next gap:** audit the exact full LOCAL-CONVERT port/payload grammar; test a representation-sensitive compiler that explicitly pays the minimum of equivalent clause, gate and GF(2) realizations, without assuming free semantic conversion. All task identities, roles, enabled states and schedules retained.

Artifacts under experiments/arc/lspv2_404_* and results/raw/arc/2026-11-04_1712_LSPV2_WEIGHTED_BASIS404_*, plus coordination handoff. Root main.tex needs full-blob-safe ownership reconciliation; no incomplete-file overwrite is permitted.

References: Emdin et al., MFCS 2022, DOI 10.4230/LIPIcs.MFCS.2022.47; Haken, TCS 39 (1985), 297-308; Cook, SIGACT News 8(4) (1976), 28-32; project /358 and /312.