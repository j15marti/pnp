# LSPV-3/445 | Exact mixed-work minimum for recovering an isolated private-chain clause
**November 6, 2026, 03:05 PST | Route B | PROVED/RESTRICTED symbolic, COMPUTATIONAL finite. P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE
**Hypothesis (before search):** The standard strict-three private-chain encoding of a width-k clause (k>=4) needs exactly k-3 unit-paid at-most-binary inferences to recover the original clause, even granting perfect legal proof choice and sharing. **Falsifiers:** (1) omit one gadget clause and still imply the original; (2) a conservative source-free DEF eliminates a needed source; (3) fewer than k-3 paid binary nodes connect k-2 necessary source leaves; (4) the purported RES upper proof uses a wrong oriented pivot or invalid three-literal source. These four fail for the isolated gadget by the proof and finite checks below.

Previously LSPV-3/440 gave the k-3-step **upper** recovery for bit-PHP chains. LSPV-3/444 and LSPV-5/REFEREE382 show that long fresh-wire gates cannot simply be treated as <=3 original-coordinate LOCAL premises. This run does not claim to rediscover either result. It establishes **matching isolated-gadget minimality** with no DEF/LOCAL rules, and proves only the correct upper simulation direction for the complete chain encoding.

## Source / exact theorem
Let C=l_1 OR ... OR l_k be a width-k non-tautological clause with k distinct underlying original variables. Introduce private fresh y_1,...,y_(k-3) and precisely k-2 source clauses:
$$
A_1=l_1\lor l_2\lor y_1,\quad
A_j=\neg y_{j-1}\lor l_{j+1}\lor y_j\quad(2\le j\le k-3),\quad
A_{k-2}=\neg y_{k-3}\lor l_{k-1}\lor l_k.
$$
All original clauses are strict width-three with three distinct variables. Let G_k(C) be their conjunction. Define W_R^{=>C}(G_k(C)) as the least paid-node work of a valid **unconditional derivation of C**, with *only* the k-2 indexed gadget sources free, all auxiliary definitions conservative, and every paid inference at most binary. This is a consequence minimum, not an UNSAT-refutation minimum.

**Theorem (PROVED/RESTRICTED, all k>=4):** In every sound, source-explicit, unit-weight, at-most-binary-premise calculus containing ordinary oriented binary Resolution, including any additional legal conservative AND3/GF(2)/DEF operations,
$$
\boxed{W_R^{\Rightarrow C}(G_k(C))=k-3.}
$$

**Lower bound.** On any original assignment falsifying all l_i, the gadget becomes the Horn chain
$$
y_1,\ \neg y_1\lor y_2,\ \ldots,\ \neg y_{k-4}\lor y_{k-3},\ \neg y_{k-3}.
$$
Deleting indexed clause A_j makes this Horn chain SAT: set y_t=1 for t<j and 0 for t>=j (for the last deletion, all y=1). The original clause C remains false. Therefore G_k(C) with any one source removed does **not** entail C, and no sound conservative refutation/derivation of C may omit any one of its k-2 original sources. Source-free conservative DEF gates cannot remove that countermodel. A single-root DAG of q paid nodes with at most two input references per paid node has at most q+1 distinct source leaves in its connected dependency union. Therefore q>=k-3. This grants free after-the-fact choice of every legal DAG, including sharing; weights were not revised.

**Upper bound.** Starting from A_1, resolve sequentially against A_2,...,A_(k-2), with oriented pivots y_1,...,y_(k-3). Each intermediate clause is the accumulated original literals plus the next y; the final output is exactly C. There are k-3 native RES inferences, paid once each. This uses no historical private/exported port assumptions, LOCAL, DEF facets, branching, weakening, or semantic oracle. Lower and upper coincide.

**Semantic projection (separate).** Any original assignment satisfying C has an extension y_j=1 iff all l_1,...,l_(j+1) are false. Therefore for each original assignment a, (exists y G_k(C)(a,y)) iff C(a). This is stronger than mere global equisatisfiability, but is NOT a lower-bound-preserving proof simulation.

## Established hardness family / encoding / direction
Braun's original bit-PHP has n=2^ell holes, n+1 pigeons, and M=n*binom(n+1,2) pair-and-hole collision clauses C_(i,j,h), each of width 2ell on original pigeon bits. With private independent chains, the direct strict-3-CNF has S=M(2ell-2) source clauses and V=(n+1)ell+M(2ell-3) variables. The **exhibited native RES upper proof** recovering every original collision clause has exactly U=M(2ell-3) paid nodes. Concatenating any original *ordinary Resolution* refutation yields
$$
W_{\mathrm{RES}}(\operatorname{Chain}_3(F))\le M(2\ell-3)+W_{\mathrm{RES}}(F).
$$
This is only original-to-encoded **upper proof simulation**. No Res(XOR) reverse lower-bound-preserving translation from the encoded strict-three source was proved. In globally UNSAT bit-PHP, other collision gadgets can imply any target C vacuously. The local lower bounds **cannot** be summed into a minimum for that global formula.

Braun (arXiv:2609.23015v2, November 3, 2026, AI-assisted and unrefereed) states unrestricted shared-DAG Res(XOR) line lower bound >exp(n/(32768 ell^2)) for the **original** width-2ell bit-PHP at ell>=32, without paid ER definitions. Pang (arXiv:2610.00837) gives stronger degree-size bounds in its specified Res(PC_r) model, likewise not historical mixed R. Neither paper is a full R_mix341 lower bound. For direct strict-three controls, established cubic odd-Tseitin has exponential ordinary Resolution lower bound but the existing 4h-1-node AND3/GF(2) mixed shortcut, while random 8n-clause strict-three CNF is exponentially hard for ordinary Resolution but only the previous /443 linear bounded-premise minimum source-support bound is transferred to full mixed work.

## Independent verification
Exact Braun collision-sign patterns (one pair and one hole) tested for ell=2,3,4,5. Width k=4/6/8/10; strict-three sources 2/4/6/8; **exact isolated consequence minima** 1/3/5/7 paid inferences. For these cases the original clause has 15/63/255/1023 satisfying original assignments respectively and precisely one falsifying original assignment. Python producer exhaustively validated projection, checked every deleted-source witness and the no-extension assignment. A separately written Node verifier reconstructed exact ASCII DIMACS and source SHA-256, validated each RES pivot and consequence, and completed **2,269 assertions**, with eight corrupted sources/certificates rejected. It is not the authoritative native R_mix341 parser. Full original DIMACS, raw proof DAGs, deletion witnesses, checksums, Python and independent Node source and resource measurements are in the separate reproducibility ZIP.

The exact logical work k-3 omits discovery by design. Materialized translation must charge parsing and source/index/head reads, source hashing, inference construction, each intermediate clause, node references, evidence serialization, output, verifier work, caches/retrieval/recomputation and simultaneous peak. One straightforward all-M proof uses O(M ell^2 log(M ell)) output bits, versus U=M(2ell-3) distinct paid logical nodes. Python producer measured ~1.33 CPU seconds / 96,028 KiB RSS; the independent Node replay measured ~30.8 MB process RSS. These are host measurements, not FLMV time-space exponents.

## Actual primary / project source audit
Read the November 2 governing handoff, current issue #3, historical /341 (blob c87acd11), /427 branch RES lift, /439-441, /443, /444 (blob 5e74533a), REFEREE358/367/382, AGENTS.md, CODEX.md, pnp-research skill, GROKPROOF/2026-11-06_0920_PROGRESS.md (6b32bc30), and Claude TPORT-0002 (1f9fc727). Searched project for an identical exact isolated-gadget minimum; found prior **upper** steps but no matching all-rule local lower proof. A wider-literature novelty assertion is not made. Authenticated external records actually inspected: konard/p-vs-np proofs/experiments/np_subset_p_proof_attempt.md (f07e4821), blkph0x/p-vs-np-proof-research PROOF_PORTFOLIO_BRIDGE_REPORT.md (22215cec), meelgroup/frat-xor format.md (986a21aa), tanyongkiam/cake_lpr README.md (e94f45e9), peitl/short-proof README.md (93d2090d), and openai/math ExecCNFNodeSearchCosts.lean (1ced21f4). None supplies an R_mix341 parser or noncircular B3. Used indexed web search for Braun, Pang, Chvatal-Szemeredi and the standard SAT-to-3SAT chain; direct Google-branded search and full arXiv PDF access were unavailable.

**Publication/scope:** This is a complete symbolic theorem about a *local consequence*, not a certified global mixed UNSAT refutation. Existing role allocation Route A LSPV-2/4 and Route B LSPV-1/3/5, all task IDs, schedules and weights preserved. Root main.tex not edited because authenticated fetch returned zero readable bytes. Remaining: native historical LOCAL/DEF/facet/private/exported syntax, reverse size-preserving lower-bound simulation across the strict-three encoding, full mixed normalization, superpolynomial Wbar_R, noncircular B3 and P vs NP, all OPEN.

### References
[1] Braun K. An exponential lower bound for the bit pigeonhole principle in resolution over parities. arXiv:2609.23015v2, 2026-11-03.  
[2] Pang S. A Degree-Size Relation for Resolution over Polynomials. arXiv:2610.00837, 2026.  
[3] Chvatal V, Szemeredi E. Many hard examples for resolution. J ACM. 1988;35:759-768.  
[4] OpenDSA. Reduction of SAT to 3-SAT, Virginia Tech.
