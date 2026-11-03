# LSPV-4: Selector-tree composition, minimum proof nodes versus source-access cost (351)

**November 2, 2026, 10:01 p.m. PST.** **PROVED/EXACT** infinite-family theorem for fixed source-independent-VARDEF `Rmix341`; **COMPUTATIONAL** independent signed controls and bit ledgers. **OPEN**: B1, B2, B3, superpolynomial worst-case mixed cost, and P versus NP. No change to the calculus, agent schedules or task identities. External proof review pending.

## Fixed model and three falsifiers

General CNF-SAT is the target; original clauses are free axioms, each distinct derived inference (including RES/AND3/XOR/CONVERT/conservative source-independent VARDEF) costs one, and named proof-premise arity is at most two. Shared DAG nodes count once. The shortest proof is freely selected, without charging discovery. We tested: **F1** depth of a bottom-up selector tree forces superlinear mixed proof minimum; **F2** equal shortest-DAG node count implies comparable encoded original-source length and eager checker work; **F3** a short pivot-only certificate allows free source acquisition. F1/F2 are falsified by the exact families below. F3 fails under the declared source-sign-probe model, not as a model-independent machine lower bound.

## Theorem: all selector-tree shapes have the same exact minimum

Let T be any rooted full binary tree with k >= 2 leaves. Give each internal node v a distinct selector z_v, and each leaf ell a distinct variable a_ell with contradictory unit pair (a_ell), (NOT a_ell). Recursively guard every left clause C by (z_v OR C), and every right clause D by (NOT z_v OR D). The resulting formula F_T has m=2k source clauses, n=2k-1 original variables, no duplicates and no tautologies.

**PROVED/EXACT:**

$$
W_{R_{res}}(F_T)=W_{R_{mix341}}(F_T)=2k-1=m-1.
$$

**Proof.** Every assignment to selectors activates exactly one contradictory leaf, so UNSAT. Deleting any source clause permits setting selectors to select its leaf and satisfying the other unit at that leaf; all other guarded clauses become tautologies. Thus every source is indispensable, and flipping any one of its literal-occurrence signs makes the formula SAT under the same deletion witness. All m source clauses must belong to the sound contradiction DAG's ancestry. If q distinct paid nodes have at most two named proof premises, ancestry connectivity gives E >= m+q-1 while E <= 2q, hence q>=m-1, including conservative DEF, sharing, and temporary growth. For a matching proof, resolve the two signed leaf clauses to obtain their ancestor-guard clause, then resolve each pair of sibling guards on that node's selector, bottom-up. This needs k leaf plus k-1 internal RES inferences. The result is legal in the SAME fixed Rmix341. No lower-bound cutoff or shortest-path search is involved.

## Exact representation and checker costs

Let k=2^d. A **balanced** tree has all leaf depths d; a left **comb** has leaf depths 1,2,...,k-2,k-1,k-1. Their total original literal-occurrences are

$$
L_{bal}=2k(d+1),\qquad L_{comb}=k^2+3k-2.
$$

In the **declared eager checker**, every original clause and each nonterminal derived clause is accessed exactly once as an antecedent. Total *parent literal inspections* (not a lower bound on all possible checkers) are

$$
V_{bal}=4kd+2,\qquad V_{comb}=2k^2+2k-2.
$$

Encode input with Elias gamma(n+1), gamma(m+1), then each clause gamma(width+1) and one sign bit plus a b_v=ceil(log2(n+1))-bit variable identifier per occurrence. Consequently N_bal=Theta(k (log k)^2), while N_comb=Theta(k^2 log k). A pivot-only certificate records two predecessor IDs and one pivot per derived step; with b_p=ceil(log2(m+q)) and q=2k-1 its additional evidence length is **q(2b_p+b_v)** bits, identical for both shapes. This certificate does NOT include its separately paid original source bits or the checked clause materialization.

Since each literal-occurrence sign has a SAT one-bit-flip neighbor, every correct deterministic general-CNF decider must read each of the L independent sign fields on that particular UNSAT input in a single-bit source-query model, or at least ceil(L/w) ordinary probes each exposing at most w sign bits. These are input acquisition bounds, **not** logical-DAG node lower bounds, time bounds across arbitrary machines, or writable-space lower bounds.

| leaves k | shape | source clauses | exact Wmix | L signs | N binary bits | pivot-only proof bits | eager inspections |
|---:|---|---:|---:|---:|---:|---:|---:|
| 4 | balanced | 8 | 7 | 24 | 150 | 77 | 34 |
| 4 | comb | 8 | 7 | 26 | 154 | 77 | 38 |
| 8 | balanced | 16 | 15 | 64 | 418 | 210 | 98 |
| 8 | comb | 16 | 15 | 86 | 536 | 210 | 142 |
| 16 | balanced | 32 | 31 | 160 | 1142 | 527 | 258 |
| 16 | comb | 32 | 31 | 302 | 2046 | 527 | 542 |
| 32 | balanced | 64 | 63 | 384 | 3034 | 1260 | 642 |
| 32 | comb | 64 | 63 | 1118 | 8364 | 1260 | 2110 |
| 64 | balanced | 128 | 127 | 896 | 8094 | 2921 | 1538 |
| 64 | comb | 128 | 127 | 4286 | 35546 | 2921 | 8318 |

## Executed verification, hostile controls, and resource ledger

The deterministic Python generator emitted twelve full original sources/proof DAGs, for k=2,4,8,16,32,64 and both shapes. An independently implemented, no-producer-import Node verifier passed **11,672 assertions**, recreating source clauses, signed Resolution steps, all clause-deletion SAT witnesses and each literal-sign-flip SAT neighbor, canonical binary encoding and strict parsing, eight intentionally malformed encoding variants per case, and four corrupt-proof variants per case. For k<=4 UNSAT was also independently enumerated exhaustively; for larger k it follows from the proved tree theorem and checked refutations. Odd/even K4 Tseitin controls have respectively 0 and 8 models. The actual full raw JSON (every source, pivot and witness) is 118,997 bytes, SHA-256 `b6b1354a8a5c0d13df52a249a09b0f33426e6eb8d54646bafef0d8e3a82a84d4`; independently executable raw package is available from this run's sandbox attachment.

Linux `/usr/bin/time -v`, including runtime startup and all phases: Python producer 4.05 s, peak RSS **96,648 KiB**; Node referee 0.22 s, peak RSS **38,948 KiB**. These are actual host measurements, **not** native indexed random-access TM counts or a proof of square-root writable space. The implementations materialize all source, proof and witness records. The required all-phase transform envelope remains s'<=max(rho,eta,lambda,lambda*s), with rho covering preprocessing, source/index acquisition, rule generation and checking, temporary allocate-then-free storage, and output.

## Corpus reconciliation, limits and next objective

Reviewed the authenticated 12:04 worst-case handoff first, issue #3 and recent peers: Rmix341 original; LSPV-4 bottom-up349 and mixed split350; LSPV-2 GUARD-EXCESS-CAP350; LSPV-3 HETEROGENEOUS-SPLIT-EXCESS353; LSPV-5 REFEREE303; AGENTS.md, CODEX.md and pnp-research skill. Searches: `selector guarded split composition`, `G342 mixed split floor` in project GitHub; `resolution proof checker` in OpenAI GitHub (no directly applicable mixed-calculus compiler); external literature Peitl/Szeider shortest Resolution, Kullmann/Zhao minimal UNSAT Davis-Putnam reductions, Part/Tzameret counting proof bounds [1-3]. Prior split/guard nonamplification is already established; no originality claim for it. The narrow additional result is exact balanced-versus-comb acquisition/replay/encoded-evidence separation.

This is an infinite **easy** family, not a worst-case superpolynomial Wbar_R lower bound. B1 and B2 (using T_A^wc on **all** inputs, including malformed) remain open, as does B3 (SAT in P implies polynomial Wbar_R for the SAME fixed R). No acceptance/rejection trace was assumed to justify arbitrary machine correctness. Source access does not imply proof construction. No FLMV contradiction follows.

**Next precise gap:** Find a bottom-up operation which provably *amplifies excess* e_R(F)=W_R(F)-(mu(F)-1) for all allowed Rmix341 inferences. Selector trees do not. Separately prove/falsify B3. Root `main.tex` retrieval yielded an empty content payload with nonempty blob SHA; no unsafe root edit was attempted and root reconciliation remains pending.

## Sources

[1] Peitl T, Szeider S. Finding the Hardest Formulas for Resolution. *JAIR* 72 (2021): 69-97.
[2] Kullmann O, Zhao X. On Davis-Putnam reductions for minimally unsatisfiable clause-sets. *TCS* 492 (2013):70-87. DOI 10.1016/j.tcs.2013.04.020.
[3] Part F, Tzameret I. Resolution with Counting: Dag-Like Lower Bounds and Different Moduli. arXiv:1806.09383 (2018).


**Root reconciliation addendum, same run:** Recovered the full 1,350,487-character `main.tex` from its authenticated Git blob after the contents endpoint returned empty. Appended the LSPV-4 SELECTOR-SHAPE-SOURCE-AUDIT351 paragraph inside `% BEGIN LSPV-4 OWNED` / `% END LSPV-4 OWNED`. New root commit `b83f5730dadff960566b74b3f61baa441f395d49`; complete blob readback confirmed every character before and after the insertion unchanged, exactly one ownership addition, and explicit OPEN status. This supersedes the earlier pending-root observation above. No other role region was edited.
