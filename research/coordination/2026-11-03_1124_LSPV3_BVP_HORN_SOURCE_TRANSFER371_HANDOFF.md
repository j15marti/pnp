# LSPV-3 BVP-HORN-SOURCE-TRANSFER371: five-role handoff

**November 3, 2026, 11:24 AM PST.** PNP Hypergraph & Proof Certificates / LSPV-3. Fixed same Rmix341, one unit charge per derived node, at most two proof parents, all authenticated sources, paid RES, GF(2), AND3, LOCAL-CONVERT, conservative VARDEF. Task ID, current enabled state, schedule, ownership and other rules unchanged. KNOWN THEOREM for Alekseev 2026; PROVED/EXACT for the output-size implication conditional on that theorem and prior BVP354; COMPUTATIONAL local controls. B1/B2/B3 and superpolynomial mixed Wbar remain OPEN; P versus NP OPEN.

## Established theorem and precise missing transport

Alekseev (Theory of Computing 22(4), June 21, 2026, Theorem 3.5) proves every rational Ext-PC-sqrt algebraic refutation of BVP_n

$$
\Gamma_n=\{1+\sum_{i=1}^{n}2^{i-1}x_i=0,\ x_i^2-x_i=0 \text{ for }1\le i\le n\}
$$

needs at least Omega(2^n) ENCODED BITS. Ext-PC-sqrt allows exact square root and conservative arbitrary-depth algebraic extensions, and p-simulates Extended Frege. This does not imply CNF refutation-node hardness or unrestricted SAT machine-time hardness.

Previously verified LSPV-3 BVP-BITBLAST-COLLAPSE354 (Git blob aa462fbe0350d1b21be2942a2be243a620909b73) provides a 5n+2 clause Boolean carry CNF B_n with EXACT global mixed minimum W_Rmix341(B_n)=2n+1. New simple syntactic observation: EVERY carry clause is Horn, including the two boundary units. The Boolean instance has encoded length N_n=Theta(n log(n+1)) bits.

**New quantitative backtranslation lemma:** Fix the explicit (2n+1)-node Resolution proof pi_n for B_n. ANY converter, even with nonuniform advice and free discovery, which outputs a valid Ext-PC-sqrt proof of the ORIGINAL algebraic Gamma_n must emit at least

$$
|\tau(B_n,\pi_n)|_{\mathrm{bits}}
=\Omega(2^n)=2^{\Omega(N_n/\log(N_n+2))}.
$$

Therefore there is no polynomial OUTPUT-BIT-overhead converter between these precise sources. A sequential bit-output converter also has Omega(2^n) output operations. This is not a SAT algorithm lower bound. A purported polynomial source compiler cannot BOTH derive translated carry CNF source axioms from original algebraic Gamma_n in polynomial proof bits AND simulate the short Resolution proof with polynomial bit overhead. Concatenation contradicts Alekseev. This locates the source-introduction gap, rather than confusing two equisatisfiable presentations.

## Four falsifiers and controls

1. F1 FALSIFIED: semantic equisatisfiability makes all Boolean encodings inherit algebraic BVP hardness. The Horn family has an exact linear mixed proof.
2. F2 FALSIFIED: a polynomial-output-bit converter gives original algebraic BVP refutations from the short Boolean proofs. Contradiction with published Theorem 3.5.
3. F3 FALSIFIED: a short CNF proof automatically certifies the original algebraic source. Source axiom derivation is a separate charged obligation.
4. F4 OPEN: these facts establish B3 or superpolynomial mixed-system Wbar. They do not.

A standalone no-import Node runner was executed locally on n=1,2,3,4,5,6,8,12,16,32,64. 740 assertion groups passed; all signed RES pivots and all indispensable source deletion witnesses were checked; 11 corrupted final pivots rejected. All clauses verified Horn. Exhaustive controls through n=6: 0 original UNSAT models, 1 model for each opposite-boundary SAT variant. Mandatory K4 Tseitin: 8 even-charge solutions, 0 odd-charge solutions. The n=64 instance used 322 source clauses, 129 charged proof nodes, 26656 encoded DIMACS bits and 176168 JSON proof bits. These are not optimizer time or FLMV machine resource bounds. Preserve all-phase rho in s'<=max{rho,eta,lambda,lambda*s}.

## Corpus, peer, Grok and Claude review

Read the pinned November 2, 12:04 PST refocus from commit 4e29ed7646f484707767acb6e63ec5f38afd98a8 (blob 033b54b87b7cbe94912af5cf67daa52859143a07), current issue #3, AGENTS.md, CODEX.md, repository pnp-research SKILL; LSPV-3 BVP354/BPHP369/CYCLIC370, latest LSPV-2 368, LSPV-1 368, LSPV-4 366 and LSPV-5 318 handoffs. Prior BVP source construction was credited rather than repeated.

Live directory listings confirmed GROKPROOF/, research/agents/grok/, and research/agents/claude/. Read GROKPROOF/2026-11-03_1912_PROGRESS.md (blob dbec4959d96f19554061511cd240745f398272ec): all-input, fully charged FLMV transformation remains OPEN, with earlier invalid upper-runtime-to-lower-query-cost inference already identified. Read research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex (blob b7150bb9ed964affd5fb90ecd24b0aa35d600bf9): alternation-trading restricted portfolio only, not B3. Read research/agents/claude/2026-09-30_CLAUDE-0266_review.tex (blob 694c1c8169d9a193397b94e6ee572c476e639a94): its claim that only affine Boolean functions have algebraic immunity one is false; xy is nonaffine with annihilator 1+x. These assessments are evidence, not authorities.

Original external searches included Alekseev 2026 (original PDF theorem and page screenshot), Haken PHP, Braun bit PHP, Buss Frege PHP, Pich-Santhanam 2026 proof/circuit transfers and github.com/openai (no relevant source translator found). No local repository checkout, so the repository-wide preflight could not execute.

## Exact outbox and preservation

Report: research/agents/lspv-3/2026-11-03_1124_LSPV-3_BVP_HORN_SOURCE_TRANSFER371.tex (readback blob 9697ea458fba05df107a252ee9e7dc18b3035941).
Code: experiments/arc/lspv3_371_bvp_source_audit.js (readback blob 44602c78220e86a69d53b575964d79efed5f2555).
Raw: results/raw/arc/2026-11-03_1124_LSPV3_BVP_HORN_SOURCE_TRANSFER371_raw.json (readback blob ba0cc7e6ccb533262f9bbec4d20f52de5aa41815).
Handoff: research/coordination/2026-11-03_1124_LSPV3_BVP_HORN_SOURCE_TRANSFER371_HANDOFF.md.

All first three files were committed and exact-content read back. Root main.tex path fetch initially returned ZERO content for prior blob d07161c26020ac3d985b278211f101ba8b976ef8. A direct authenticated fetch_blob recovered the complete 1,466,943-byte body. LSPV-3 owned-region reconciliation succeeded safely in commit ca827e0717b5c7f07fff77e16f54eded1a434238, new blob de806b993234136277685f859bb50940e74d61ac; full readback confirmed the entire 1,468,978-byte document, and removing the 2,035-character insertion yields exactly the former document byte-for-byte. No outside content modified. No task writes or legacy role activation. Historical artifacts untouched.

**Next decisive gap:** Establish a lower bound applying to every rule in the SAME fixed R, with exact source and encoding, or a justified polynomial-cost proof backtranslation in the correct direction that survives GF(2), ER and LOCAL-CONVERT. Existing Haken, Braun and Alekseev sources fail this transfer. Separately B3 remains SAT in P implies polynomially bounded Wbar_R for the SAME R, OPEN. P versus NP OPEN.