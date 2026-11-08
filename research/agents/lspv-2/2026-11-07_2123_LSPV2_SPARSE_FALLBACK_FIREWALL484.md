# LSPV-2/484 | Sparse-exception direct-fallback obstruction

**2026-11-07 21:23 PST | Route A primary | PROVED/RESTRICTED conditional on SAT in P; COMPUTATIONAL finite controls. P versus NP OPEN.**

**Tracker nodes:** [P2-A2] universal solver-dependent contraction OPEN; [P2-A5] all-input and recursive closure OPEN; [P2-A4] restricted evidence. Cross-chain [P1-01], [P1-03], [P1-04] OPEN; Route B [P2-B1], [P2-B2], [P2-C3], [P2-D1] OPEN. No historical R_mix341 grammar or weights changed.

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis.** A fast correct subfamily path plus direct unmodified full-input fallback cannot establish the desired *worst-case* FLMV contraction even if only one valid 3-CNF input at each of infinitely many lengths uses fallback.

**Falsifiers stated before source review:** (F1) no polynomial-time recognizable, sparse infinite family of valid 3-CNF exceptions exists; (F2) direct native guest writes are not counted as work/peak; (F3) a single exceptional source at unbounded lengths cannot affect worst-case exponents; (F4) odd-charge signed Tseitin clauses or disjoint side packets change SAT/UNSAT labels. The exact proof excludes F1/F3/F4; F2 is excluded only for *literal unmodified native execution*, not code-aware optimization.

**Sources actually read.** Both complete proof1.txt and proof2.txt, issue #3 and latest peer comments, governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (blob c3889a3e514ddbd747150dcb68607013a3b2d154), AGENTS.md (19656af102604d5f0a721d548cf2e4e72a063561), CODEX.md (754999f50de93cdb693ed37bc8110d31e9e698ef), .codex/skills/pnp-research/SKILL.md (b8df83a7b0b1428f349b0e02ce1387d979e8db7f), LSPV-2/480 and /483, current LSPV-4/485 (ac9819b7378194cf68905299c733890861f4cbe3), LSPV-1/495 CBPHP handoff, GROKPROOF/2026-11-08_0320_PROGRESS.md (72edb3140d8ed798d0905a827f85d3428728e396) and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a).

**External search and exact refs.** Primary: Fortnow et al. 2005 indexed-machine SAT time-space theorem [1] and Ben-Sasson/Wigderson 2001 ordinary Resolution width/size theorem [3]; web searches for SAT worst-case fallback, source hardness, proof formats. No Google-branded separate client. Reviewed actual files: konard/p-vs-np/README.md (0e0ec77f83ad6eec1719a96066108b96ac1c2a95) and scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5) and INDEPENDENT_AUDIT.md (b30515cced93d8911a6415555ee9ec1444502d93); MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd198fc4a698a5a207f67b36a9591b2a3bab); berkeley-abc/abc/README.md (88a9d1a316dd9751acade746de315fd1e6e6c362); openai/math/README.md (cc5b0a03bca6c742f045d683b6647a6f44ef2cae). None proves universal all-input FLMV contraction. No official historical R_mix341 or native FLMV machine was executed.

**Iteration/deduplication.** LSPV-2/480 *already* proved the general direct guest penalty T >= Omega(sum m_i^k), S >= Omega(max m_i^k). This run proves a specific quantifier corollary: even syntactically rare full-size guest fallbacks spoil an all-input worst-case bound. No novelty claim for the padding argument or arbitrary-algorithm hardness.

## Theorem 484.1 (PROVED/RESTRICTED): one rare native fallback defeats universal contraction

Assume a fixed uniform total correct polynomial SAT decider A0 exists, handling SAT, UNSAT and malformed strings. For any sufficiently large fixed integer k>2 exceeding A0's finite time/space exponents, define the uniform total correct decider Ak(x) to visit, write and read (|x|+1)^k distinct native WORK cells, then execute A0(x), returning the exact same classification. These extra steps and high-water positions are genuinely executed on the original machine, not merely encoded. Ak has polynomial time/space exponents t=s=k up to harmless o(1).

Let E={U_j:j>=0} be a polynomial-time generable, polynomial-time recognizable infinite set of valid 3-CNF source encodings with strictly increasing lengths N_j. Let Phi(Ak) be any correct hybrid that uses *any* correct fast algorithm for inputs outside E, but literally invokes unmodified Ak on the full-size source U_j for every j. Then

$$
T_{\Phi(A_k)}(U_j)=\Omega(N_j^k),\qquad
S_{\Phi(A_k)}(U_j)=\Omega(N_j^k).
$$

For sufficiently large k,

$$
k>\max\left(\frac{11}{10},\frac35+\frac{k}{2}\right),
\qquad
k>\max\left(\frac12,\frac{k}{2}\right).
$$

Therefore the intended all-input contraction bounds fail for this exact hybrid. There can be just ONE exceptional valid source at each such length, and every exceptional source may itself be trivially decidable.

**Proof.** The mandatory Ak prefix on U_j visits and reads all (N_j+1)^k native work cells and takes at least that many transitions, before A0 is ever invoked. No fast-path operation on other inputs can alter these actual worst-case costs. As N_j tends to infinity, the two upper exponents strictly below k contradict the compulsory costs. QED.

**Strict limitations.** A code-aware compiler might delete inert padding, replace native calls with a proven equivalent guest, apply algebra, share subcomputations or avoid the full-size fallback. None of those is ruled out. The claim is conditional on SAT in P and is not SAT computational hardness; for any already known language in P the analogous construction is unconditional.

## Exact original 3-CNF and prior published hardness controls

Take connected cubic K4, with one variable on each of 6 edges. Each of its four incident-degree-three parity equations is expanded into exactly four **proper signed 3-clauses**, one clause for each forbidden local pattern. This gives exactly 16 clauses. Every even total charge vector has exactly 8 global edge models, every odd vector is UNSAT. This construction follows the established Tseitin convention, with CNFgen as an executable-format clue [2].

Define U_j from the fixed odd charge vector (1,0,0,0) and j new, pairwise variable-disjoint strict positive three-clauses (a_i OR b_i OR c_i). U_j has 16+j source clauses, 6+3j variables and binary length N_j=Theta(j log(j+2)) under a fixed sign-bit, fixed-width literal-ID encoding. It remains UNSAT, and comparison with its fixed canonical clause sequence is polynomial time. Varying the signs of the j fresh clauses independently yields 8^j distinct valid same-length still-UNSAT sources. Exactly ONE is designated as U_j, giving an exceptional fraction 8^{-j} in this explicit equal-length subset. Such sparse controls are not new proposed hard families.

On suitable *cubic expander* odd-charge Tseitin graph families, established published results give exponential lower bounds for **ordinary DAG Resolution**, not for arbitrary algorithms or historical R_mix341. GF(2) is a short legitimate shortcut. The finite K4 and side-gadget instances are not individually certified asymptotically proof-hard.

## Exact finite verification and charged resource ledger

**Published JavaScript**: experiments/arc/lspv2_484_sparse_fallback.js, Git blob 8b350c1394301144f64096797e63e68835beb28d. Its exact fetched GitHub bytes were replayed in a V8 isolate with explicit node assert/Buffer/console shims, PASS: 834 checks, 48 charge/side-gadget strict-3CNF original-source controls (24 SAT, 24 UNSAT), even model counts 8*7^j and odd zero for j=0,1,2, four malformed objects rejected, one exceptional guest among the 16 controls per j, 3 actual illustrative host allocations totaling 6,256,832 array writes and maximum 2,334,784 bytes.

**Independent Python**: experiments/arc/lspv2_484_independent.py, 192 checks on the 48 original sources, exact rational exponent inequalities and 1+8+64 signed-gadget bitlength variants (no random seeds). Both are bounded finite host controls, NOT native FLMV executions, historical mixed certificates, or proofs of polynomial SAT.

**Resource ledger:** On U_j, the native direct guest alone has time and WORK high-water Omega(N_j^k), and output is the original one-bit classification; all other parsing, source/index/head reads, construction, branch dispatch, restarts, caches, storage, retrieval, verification, failed policies and output increase nonnegative cost. No shared proof inference nodes are used; no exact R_mix341 minimum is claimed. The JS Uint8Array size uses JSON bytes as a *finite host proxy*, not the stipulated binary source or FLMV WORK tape. Host RSS and execution times cannot be promoted to native upper bounds. Underlying A0 is a conditional mathematical object, not a program produced by this run.

**Published raw**: results/raw/arc/2026-11-07_2123_LSPV2_484_SPARSE_FALLBACK_RAW.json. **Handoff**: research/coordination/2026-11-07_2123_LSPV2_SPARSE_FALLBACK_FIVE_ROLE_HANDOFF484.md.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** This strengthens the explicit all-input interpretation of the already-established /480 native guest penalty, but changes no load-bearing status, theorem hypothesis or dependency. Initial proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; initial proof2.txt blob e2e15d8632676257a4cbfcf8ca8ca3b2cd09b011. Neither tracker is edited this run.

Root main.tex could not be safely authenticated as a complete byte stream through the available interface; it was not partially overwritten. All historical R_mix341 rules/weights, roles, IDs, schedules, enabled states and two Route A/three Route B allocation are preserved.

**Remaining precise gap:** Build an effective, solver-dependent, exponent-oblivious, recursively iterable, all-input transformation A -> Phi(A) on the original FLMV machine with SAT/UNSAT/malformed correctness and all-phase time/peak WORK/INDEX charges, while avoiding any uncontracted fallback. [P2-A2], [P2-A5], [P2-B1], [P2-B2], [P2-D1], [P2-C3] and P versus NP remain OPEN.

## References

[1] Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6):835-865 (2005), DOI 10.1145/1101821.1101822.

[2] Massimo Lauria, CNFgen, cnfgen/families/tseitin.py, Git blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab.

[3] Ben-Sasson and Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, JACM 48(2):149-169 (2001), DOI 10.1145/375827.375835.
