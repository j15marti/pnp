# LSPV-2/399 five-role handoff: input-query lower bound versus CNF padding

November 4, 2026, 13:12 PST. Task ID 6ad6f04620a881918aecb8078ce2f2d1. R_mix341 and all existing agent settings unchanged. B1/B2/B3, complete mixed superpolynomial minimum and P vs NP remain OPEN.

## IDEA -> SEARCH -> ITERATE

Initial hypothesis: every pivotal sign bit of an explicitly encoded minimally UNSAT signed hypergraph forces a native read by any correct unrestricted general-CNF SAT solver, and this might be representation-independent. Falsifiers: a solver skipping a pivotal bit; a sound duplicate-free encoding that eliminates sign pivotality; bounded-error randomized avoidance; block sensitivity disappearing with singleton sensitivity.

Search terms actually used: "Nisan 1991 CREW PRAMs decision trees sensitivity"; "Boolean function sensitivity randomized decision tree complexity"; "Tseitin tautologies expander graph exponential resolution Urquhart 1987"; "Tight Bounds for Tseitin Formulas 2022"; "Short Proofs Are Narrow". Read Nisan SIAM publisher, Ben-Sasson and Wigderson JACM authors' record, and Itsykson/Riazanov/Smirnov SAT 2022 publisher HTML, whose lower bound is for regular Resolution and OBDD-reordering. Read Nov 2 five-role refocus, issue #3, AGENTS.md, CODEX.md, the repo research skill, LSPV-2/341/390/393/394/397/398, latest handoff, GROKPROOF/2026-11-04_1217_PROGRESS.md, and Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex. Follow-up duplication audit read research/main/2026-11-03_2148_MAIN_END-TO-END-SIGN-ACQUISITION-REFEREE329.md and research/agents/lspv-4/2026-11-04_1236_LSPV-4_HAKEN_SOURCE_SIGN_BRIDGE_CALIBRATION394.tex. REFEREE329 already established the general randomized coupling and invertible-recoding counterexample; LSPV4/394 specialized it to Haken PHP. Thus the generic query lemma is NOT claimed as original new theory.

Actual OpenAI GitHub files read: openai/math/lean/ComparatorChallenges/SATVariance.lean SHA 5ecf51d9; openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFWidthSearch.lean SHA 14a9f16d. Neither proves our missing bridge. Direct branded Google search unavailable; general web and authenticated GitHub search used. Grok's cut-cost observations and Claude's sequential one-tape bounds do not establish B3.

## Proved results, scope, counterexamples

On every odd bridgeless cubic Tseitin F(G,chi) with h vertices, 4h three-literal clauses are individually indispensable (LSPV-2/341). Under explicit independent one-bit signs and fixed-width binary indices, all 12h original source sign bits are pivotal. Every total deterministic exact unrestricted SAT decider must read all 12h on that UNSAT input. A total randomized decider with error epsilon<1/2 on every valid input needs expected >=(1-2epsilon)*12h distinct sign reads. This is the established source-star query theorem instantiated here, not a new unrestricted computational lower bound. Explicit input length N=Theta(h log h), so only Omega(N/log N) bit probes. Both-label SAT neighbors must be in the decider's domain. It fails as an argument on a promise restricted solely to Tseitin encodings.

For every UNSAT F, duplicate-free source padding P_z(F) = AND_C [C AND(C OR z) AND(C OR NOT z)] is exactly SAT-equivalent to F, with constant-factor explicit bit expansion; it is a source-to-source transformation, not a free R_mix341 rule. Flipping any one sign or variable-index bit in any one padded clause (provided the resulting CNF encoding is valid) leaves UNSAT, because the remaining original C and/or two intact guards still force F. Thus all padded literal-data bits have zero individual sensitivity, even when F has 12h sensitive sign bits.

Stronger quantified amplification: for minimally UNSAT F with L sign-bit occurrences and every r>=1, repeated guard padding P_r makes the least number of sign-bit flips needed to restore SAT EXACTLY r+1. Under any assignment at least one original clause C is false and r+1 distinct records (C plus one guard per z_j) are false. <=r individual changes cannot repair all of them. A witness for F minus C, with all z_j=0, becomes satisfying after flipping the chosen literal sign in original C and in its r positive guards. All L such (r+1)-bit pivot blocks are pairwise disjoint. This reuses /394 repair-distance amplification and adds precise sign-bit Hamming geometry. Singleton sensitivity vanishes for r>=1, but higher-order block sensitivity remains >=L. No claim of universal representation-invariant block sensitivity or computational separation follows.

Haken 1985 certified ordinary shared-DAG Resolution exponential PHP lower bound uses explicit h(h+1) variables, Theta(h^3) clauses, N=Theta(h^3 log h) indexed input bits, and quantifies over every Resolution refutation for all large h. It is NOT a lower bound for GF(2), ER, R_mix341 or arbitrary SAT algorithms. Cook 1976 polynomial ER PHP proofs are countercontrols. Existing expander Tseitin ordinary Resolution hardness is likewise defeated by paid native affine deductions.

## Reproducibility and costs

Local independent Python producer: 2,491 assertions; 5 malformed inputs rejected; K4, K3,3, cube, Petersen, respectively 16/24/32/40 deletion SAT witnesses, 48/72/96/120 individual opposite-label sign witnesses and as many independent padded block witnesses. K4 and K3,3: every valid single literal-data-bit edit in padding was exhaustively truth-table tested UNSAT (632 and 936 edits). Independent JS verifier: 721 assertions, 3 malformed rejected; K4/K3,3 exhaustive original single flips, padded single sign flips, padded two-bit flips, and minimum violated-source counts exactly r+1 for r=1,2,3. No randomized seeds. Source bit lengths 292/502/664/824; padded lengths 966/1706/2266/3268. Direct GitHub readback of JS executed successfully and reproduced totals.

Artifacts:
- research/agents/lspv-2/2026-11-04_1312_LSPV-2_BIT_SENSITIVITY_PADDING399.md
- experiments/arc/lspv2_399_independent_check.js
- results/raw/arc/2026-11-04_1312_LSPV2_BIT_SENSITIVITY_PADDING399_raw.json
- Python and JS downloadable archive also created in the local conversation.

Bit queries are not machine runtime: source parsing, expansion, bit-writing, candidate acquisition, validity checking, bit indexing, updating, proof output, cache, verification, and peak space all cost physical resources. The padding cost is polynomial but not zero. Logical DAG node costs, including sharing, are distinct. The FLMV space envelope s'<=max{rho,eta,lambda,lambda*s} remains necessary. No B1/B2/B3 implication is obtained.

Root main.tex authenticated fetch yielded SHA ad2f01d5fdcbe355dbac6eeff0a11a7778921713 and zero-length content, so no byte-safe reconciliation was possible; no overwrite was attempted.

## Requests to all existing specialist roles

LSPV-1: preserve quantifier order and distinguish fixed-input query sensitivity from B3. LSPV-2: test typed charged LOCAL-CONVERT representations and polynomial cost-reflection; no unverified SAT-label tag. LSPV-3: audit full block sensitivity under all legal representation conversions. LSPV-4: charge conversion, indexes, lazy payloads, and all-phase peak space. LSPV-5: attack proposed transfer of bounded-radius signed-source influence to superpolynomial machine runtime, and distinguish promise versus total correctness. Existing schedules/roles preserved.

P versus NP remains OPEN.
