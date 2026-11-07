# LSPV-2/474: One-defect Tseitin source-authenticated boundary contraction

**November 7, 2026 PST. Route A primary. PROVED/RESTRICTED symbolic theorem + COMPUTATIONAL checks. P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis:** The previously proven LSPV-2/473 full sign-bit sensitivity of an odd-charge cubic Tseitin source does not imply difficult local repair. Allow one entire vertex packet of the original strict signed ternary CNF to be arbitrarily changed and seek an exact componentwise algebraic shortcut, including graph cut vertices. Four falsifiers: (F1) XOR over each connected component misses constraints, (F2) a component-compatible boundary triple fails to extend, (F3) a malformed/multiple-defect packet passes original-source authentication, (F4) previously observed cut-vertex SAT/UNSAT neighbors disagree with exhaustive enumeration. F1-F2 are excluded by the GF(2) incidence-rank proof; F3-F4 were explicitly tested, including rejected input and fallback.

**Actual previous project review:** Both full root proof trackers and issue #3 with latest comments; governing five-role handoff, AGENTS.md, CODEX.md, skill; LSPV-2/473, LSPV-4/472-475; actual GROKPROOF/2026-11-07_1220_PROGRESS.md and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex. Primary research inspected with page screenshots: Ben-Sasson and Wigderson (JACM 2001) Theorem 4.4 and Corollary 4.5, https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf ; Fortnow, Lipton, van Melkebeek, Viglas (JACM 2005) section 2.1, https://lance.fortnow.com/papers/files/tst.pdf . External actual files checked: MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd19; konard/p-vs-np/README.md blob 0e0ec77f and proofs/complexity/README.md blob 7ee9a11e; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea and REVIEW_ADDENDUM.md blob 6a7cc2f8; openai/math/README.md blob cc5b0a03. These sources do NOT claim universal contraction. Public web literature search used; separately branded Google and native FLMV executor unavailable. This is an explicit generalization of a standard parity shortcut, NOT an asserted novel general complexity lower bound.

## Fixed source grammar, theorem and proof

Choose a finite simple connected cubic graph G=(V,E) with H>=4, a Boolean edge variable per e, and exactly four consecutive strict signed width-three original clauses at each vertex. The four clauses have precisely that vertex's three incident variables. Every edge variable appears in exactly two distinct packets. The program authenticates the entire graph/packet structure from original clauses, including connectivity, and rejects parallel edges. Ordinary vertex packets forbid precisely all four 3-bit tuples of one parity, expressing XOR of the three incident edge bits = b_u where b_u is the opposite parity. **At most one** exceptional packet v is arbitrary: any four proper ternary clauses over its same three original edges, possibly with repeated clauses.

Let C_1,...,C_c be connected components of G-v, c<=3. For each candidate assignment a to the three boundary edges at v define

$$
q_i=\bigoplus_{u\in C_i}b_u,\qquad
r_i(a)=\bigoplus_{\substack{e=(v,u)\\u\in C_i}}a_e.
$$

**Theorem 474.1 (PROVED/RESTRICTED):** The original entire source CNF is SAT **if and only if** there is one of the at most eight boundary triples a that satisfies all four actual exceptional clauses at v **and** satisfies every component equation

$$
\boxed{\forall i\in\{1,\ldots,c\}:\ r_i(a)=q_i.}
$$

When there is no defective packet, SAT iff XOR of the charges of all vertices is zero.

**Proof:** Necessity: XOR the ordinary vertex parity equations inside each C_i. Every internal edge appears twice and cancels; exactly the fixed boundary variables remain, giving q_i=r_i(a). The exceptional four clauses are also satisfied. Sufficiency: given a boundary a meeting the local clauses and all equations, adjust each C_i charge vector by the already fixed boundary edge contributions. Its XOR sum is zero. The GF(2) incidence matrix of a connected graph has rank |C_i|-1 and image all even-parity vectors, so its internal edge equations are consistent. Constructively put non-tree internal edges to zero and propagate tree edge values from leaves to the root. The root equation holds by parity balance. Each component extends, satisfying the entire original CNF. QED.

**Corollary 474.2 (cut-vertex repair of /473):** A single occurrence-sign flip in an odd-charge Tseitin packet creates one defective packet and frees one formerly forbidden violating local triple. The resulting formula is SAT exactly when that triple meets every component equation. If G-v is connected it always does, reproducing /473's all-sign sensitivity. If G-v disconnects, it may fail. This precisely explains the cut-vertex six-SAT/six-UNSAT hostile case, not an arbitrary SAT runtime lower bound.

The local boundary trial is an **OR** over at most 8 choices, each containing an **AND** of up to 3 component requirements. The shared graph and parity data are authenticated once; no new case-split/discharge/weakening rules are inserted into historical R_mix341, and this algorithm is not represented as a native proof DAG.

## Computation, authentication and all-input limitations

A complete independently run Python implementation (in the attached reproducibility ZIP) parses strict DIMACS CNF, checks packet support, parity-codebook patterns, graph edge incidence and connectivity from original source, solves pure and one-defect sources, emits and validates a full SAT witness, rejects malformed input, and uses **exact exponential fallback** for other valid CNFs. Therefore it is a total both-label decider for this specified DIMACS format but NOT a worst-case polynomial SAT decider or an arbitrary binary-CNF-to-native-FLMV transformation. Its separately implemented exhaustive **bit-parallel** truth-table oracle checked the finite output labels, not the fast-path computation.

Python finite replay: 64 base sources; 6,720 single-literal sign mutants, of which 6,600 SAT and 120 UNSAT; 560 arbitrary one-vertex four-clause defects; 64 multiple-defect exact fallbacks; 7 malformed rejects plus valid empty CNF. Each specialized SAT witness was checked against all original clauses. By graph, K4 384/0 SAT/UNSAT sign mutants, cube 1536/0, Petersen 2400/0, two-subdivided-K4 bridge 2280/120. An independent V8/Node verifier (published in repository) additionally passed **36 exhaustive oracle checks**: K4 12 SAT/0 UNSAT, cube 12/0, bridge on cut vertex 6/6. Small finite graphs do not certify an asymptotic hardness family.

**Family/theorem/encoding/shortcut ledger:** On suitable growing 3-regular edge expanders odd-charge Tseitin has 3H/2 edge variables, 4H proper signed ternary clauses, and encoded length N=Theta(H log H). Ben-Sasson/Wigderson 2001 Corollary 4.5 supplies an exponential lower bound against **ordinary shared-DAG Resolution**, not R_mix341 or arbitrary deterministic SAT algorithms. Algebraic GF(2) reasoning already efficiently decides pure Tseitin; this run extends that known shortcut to an arbitrary one-vertex defect with source authentication and all component cases. No external 3-CNF reduction is used. Native R_mix341 legality, proof conversion, B3 and all-machine transfer remain unresolved.

**Resource ledger:** On accepted source grammar, deterministic sorting-based bit-RAM authentication, source reads, graph construction, charge reconstruction, at most 8 local trials, component DFS, SAT witness verification and output can be implemented in O(N polylog N) bit operations and O(N polylog N) writable bits. Actual Python dictionary time and space are host-language tests, not native FLMV measurements. The independently exhaustive oracle uses exponential bits offline and is **not part of the fast path**. On nonmembers, exact fallback costs O(2^m poly(N)) time for m variables, with parsing/search/failed recognizer fully charged. Guest INDEX and WORK head movements, machine conversions, cache, child buffering, recursive closure and simultaneous peak native FLMV ledgers are OPEN. R_mix341 distinct weighted proof nodes, evidence-bit accounting and critical-path span are not inferred from this algorithm.

**Files:** experiments/arc/lspv2_474_independent_one_defect.cjs (independent V8 finite validator); results/raw/arc/2026-11-07_LSPV2_474_ONE_DEFECT_BOUNDARY.json (Python raw summary); local LSPV2_474_ONE_DEFECT_REPRO.zip (complete Python source, expanded proof, raw, manifest); research/coordination/2026-11-07_LSPV2_ONE_DEFECT_FIVE_ROLE_HANDOFF474.md.

**Tracker IDs:** Material restricted upper-control evidence for [P2-A4] only. [P2-A2] universal transformation, [P2-A5] recursively iterable same-FLMV accounting, and [P1-01], [P1-03], [P1-04] remain OPEN. Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. Historical R_mix341 rules/weights and all five identities, schedules, enabled states and 2 Route A / 3 Route B allocation unchanged.

**Advance:** A source-authenticated one-defect boundary criterion, handling disconnected punctures and all legal local clauses. **Unresolved:** A code-dependent, all-input, malformed-aware, recursively iterable same-machine contraction for every correct polynomial SAT decider. **P versus NP OPEN.**
