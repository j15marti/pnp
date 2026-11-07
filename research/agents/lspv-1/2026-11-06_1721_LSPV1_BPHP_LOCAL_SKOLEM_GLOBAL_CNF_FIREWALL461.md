# LSPV-1/461: Constant-local splitter Skolemization can incur exponential cross-pigeon CNF expansion
**2026-11-06 17:21 PST. Route B lead. Status: PROVED/RESTRICTED for the exact no-new-auxiliary CNF representation theorem; COMPUTATIONAL finite controls; full mixed R_mix341 transfer and B1/B2/B3 OPEN; P versus NP OPEN.**

## IDEA, falsifiers, revision
Hypothesis before searching: start with an **established**, theorem-qualified ordinary-Resolution-hard graph-FPHP family. Its standard proper-3-CNF encoding uses a *constant* number of private splitter variables per pigeon. Even so, replacing all splitters by local Skolem formulas, then expanding an arbitrary cross-pigeon proof clause into an equivalent original-variable-only flat CNF, need not have polynomial output.

Four falsifiers: (F1) the proposed local Skolem section violates an original satisfying clause; (F2) another equivalent CNF with negative literals and no fresh variables uses fewer clauses; (F3) the chosen published family actually needs growing left degree; (F4) this is falsely interpreted as excluding allowed compact-circuit/paid-definition/alternative proofs in the full R_mix341 minimum. F1–F3 were mathematically checked or refuted; F4 is expressly excluded in the theorem scope.

## Exact published hard-family ledger and 3-CNF encoding
**Known theorem:** de Rezende, Nordström, Risse, Sokolov, *Exponential Resolution Lower Bounds for Weak Pigeonhole Principle and Perfect Matching Formulas over Sparse Graphs*, TheoretiCS 4 (2025), article 9, DOI 10.46298/theoretics.25.9, equations (1.1a–c), Corollary 4.7 (published March 25, 2025). Take *fixed* integer k>=2, fixed 0<epsilon<1, m=n^k pigeons, n holes, n>=d and integer left degree d=(16k/epsilon)^2 >=4 (or admissible fixed rounding), independent uniform d-element neighboring-hole sets per pigeon. For graph G from that model, original FPHP(G) comprises: each pigeon row P_i=OR_{j in N(i)} x_ij; each negative hole collision (not x_ij OR not x_i'j); each negative pigeon functionality pair (not x_ij OR not x_ij'). The formula is UNSAT for m>n. The published lower bound says that asymptotically almost surely, **every original-CNF ordinary unrestricted shared-DAG Resolution refutation** has exp(Omega(n^(1-epsilon))) lines. It does NOT apply to stronger calculi, arbitrary SAT machines, or automatically to the 3-CNF conversion. The global hypothesis m>n is important: the literal k=1 endpoint of the published corollary would give m=n, potentially satisfiable instances, and is not used here.

**Proper signed 3-CNF encoding:** Order each pigeon row's d literals a_{i,1},...,a_{i,d}. Replace it by d-2 chained clauses:
$$
(a_{i,1}\vee a_{i,2}\vee y_{i,1}),\quad
(\neg y_{i,j-1}\vee a_{i,j+1}\vee y_{i,j})\ (2\le j\le d-3),\quad
(\neg y_{i,d-3}\vee a_{i,d-1}\vee a_{i,d}).
$$
Each binary original source clause (u OR v) becomes (u OR v OR z) AND (u OR v OR not z) with a fresh private z. Let B=sum_j binom(deg_G(j),2)+m binom(d,2) be the count of binary sources. The strict source has **exactly** m(d-2)+2B original clauses and md+m(d-3)+B total variables. Signed binary-index source-bit length N=O(m^2 d^2 log(md+2)); constant d makes this polynomial in n. Equisatisfiability is established by projection, but **preservation of published Resolution proof hardness is not established**.

## THEOREM 461.1, exact flat-CNF lower bound, PROVED/RESTRICTED
Choose t distinct pigeon rows with degree d>=4. Denote the first positive literals of row i by a_i,b_i, and its first private splitter by y_i. Define the canonical local Skolem section
$$
y_{i,j}=\bigwedge_{r=1}^{j+1}\neg a_{i,r},\qquad y_i=\neg a_i\wedge\neg b_i.
$$
All satisfying assignments of each original pigeon row extend through this section to a satisfying chained 3-CNF; the all-false row has no satisfying extension.

For the **syntactically possible** joint private-splitter clause C_t=OR_{i=1}^t y_i (not claimed to be a short derived line on the published hard source), its substituted function is
$$
f_t=\bigvee_{i=1}^t(p_i\wedge q_i),\qquad p_i=\neg a_i,\ q_i=\neg b_i,
$$
with all 2t source variables distinct. Then **every source-variable-only ordinary CNF equivalent to f_t**, with no extension variables or circuit annotations, has at least 2^t clauses. The bound is attained by
$$
f_t\equiv\bigwedge_{s\in\{0,1\}^t}
\left(\bigvee_{i=1}^t (s_i=0\ ?\ p_i:q_i)\right).
$$
**Proof:** Distribution gives the upper bound. Let C be any non-tautological implicate of monotone f_t. Deleting all negative literals from C preserves implication, because any hypothetical model of f_t falsifying its remaining positives can be made to falsify all deleted negatives by setting their variables to true; monotonicity preserves f_t. Thus any equivalent CNF can be converted to positive-only clauses with no increase in clause count. Every positive implicate must contain p_i or q_i for every pair i: otherwise the true assignment setting only that pair both true falsifies the clause. For each of 2^t bitstrings s, define a false assignment w_s where the selected literal (p_i if s_i=0, q_i otherwise) is false and its other pair member true. Because f_t(w_s)=0, an equivalent CNF must contain an implicate C false at w_s. The previous observation forces C to include the selected false literal from every pair, so no different w_{s'} falsifies C. There must be at least 2^t distinct clauses. The displayed clauses are prime and have explicit individual deletion witnesses w_s. QED.

**Quantifier/scope firewall:** Taking t=m=n^k yields a potential 2^{n^k}-clause expansion from one O(t log N)-bit clause for this **particular per-line flat-CNF Skolem normalizer**. There is **no** theorem here that all valid Resolution proofs contain this clause, that all translators must expand it, that 3-CNF FPHP is proof-hard, or that R_mix341 has a superpolynomial minimum. The original theorem's lower bound cannot be transferred just from equisatisfiability or this representation theorem. A compact Boolean circuit, legal extension definitions, shared-DAG proof, alternative split/branch strategy, or different proof normalizer may avoid the expansion entirely. Those shortcuts are permitted when minimizing W_R.

## Actual corpus review, primary sources, and no-duplication scope
Read current five-role handoff blob c3889a3e, live j15marti/pnp issue #3, AGENTS/CODEX/skill, original /341 fixed-calculus text blob c87acd11, LSPV-1/449 and /453–/460, peer LSPV-3/461, /432, LSPV-5/REFEREE317/318/334/340, actual GROKPROOF/2026-11-06_2316_PROGRESS.md blob a20fb8b3 and Claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex blob 9a5b05d6. The earlier /449 concerns **expanded ANF**, and /454–455 concern **one row's** Skolem degree/monomials; this theorem separately concerns **many constant-width rows** and cross-row **prime CNF**, not a new computational lower bound. Searched project for "Skolem cross-row", "splitter prime implicate", "exponential CNF substitution", "positive splitter"; no claim of novelty is based on search failure. Required repositories actually inspected: konard/p-vs-np/proofs/p_not_equal_np/README.md SHA 3a030411, blkph0x/p-vs-np-proof-research/METHOD_INDEX.md SHA 18d693ea, meelgroup/frat-xor/format.md SHA 986a21aa, openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean SHA 1ced21f4. FRAT-XOR is not R_mix341. Direct primary journal PDF, including rendered page 6, was inspected; no separate Google-branded session.

## Original-source controls and resource/evidence accounting
Full local independent Python producer, separate no-import Node verifier, original signed strict-3CNF instances, all source hashes and logs are in named reproducibility archive. Producer: **25,169 assertions**, Skolem chain/existential controls for width 4..8, all 2^(2t) Boolean assignments for t=1..7, all 2^t deletion witnesses, corruption and malformed-input rejection. Independent JavaScript: **23,901 assertions**. Original complete functional PHP(4,4) SAT control: 24 injective models, 104 exact-width-3 clauses, 68 variables, DIMACS SHA256 9dd5b27f35b4420203cb485cc6f248a61b3e1d9efac29644ea24e4cf41d332e1. PHP(5,4) UNSAT control: 150 exact-width-3 clauses, 95 variables, SHA256 a911db89e8a868444e73231412616a1e99e5c6fca1038c6d0c57b5d0d96fb357. The latter's UNSAT is by pigeonhole counting, **not** a published proof-size hardness certificate. Python test runtime 7.88 seconds, Python tracemalloc peak 740,879 tracked bytes (NOT host RSS). Actual acquisition, source/index/head reads, independent checking, CNF construction and all serialization/output, reference retrieval, failed controls and peak simultaneously live buffers must be charged if implementing a translator. A direct 2^t materialized expansion has at least Omega(2^t) written clauses, but an ideal W_R minimum charges only the fixed native inference weights, not this optional bad algorithm. Distinguish total work, critical path, and realizable time/space schedules. FLMV s'<=max(rho,eta,lambda,lambda*s) is unaffected.

## OPEN, next implication
Authenticate historical accepted-byte LOCAL-CONVERT/exported/private-wire and DEF-facet rules; test a real **complete** native mixed certificate for a selected published-hard 3CNF instance or prove a fully charged all-rule backtranslation, not flat CNF normalization alone. Independently seek noncircular B3 (SAT in P => Wbar_R polynomial for the *same* fixed R). B1/B2, full-mixed superpolynomial minimum, and P vs NP OPEN.

**References:** [1] de Rezende et al., TheoretiCS 4 (2025), art. 9, doi:10.46298/theoretics.25.9; [2] Cook, SIGACT News 8 (1976), 28–32; [3] Krajíček, Information Processing Letters 112 (2012), 490–493.
