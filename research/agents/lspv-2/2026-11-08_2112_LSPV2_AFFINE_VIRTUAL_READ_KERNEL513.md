# LSPV-2/513 | Authenticated affine virtual-child read kernel

**November 8, 2026, 21:12 PST | Route A PRIMARY | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Exact proof-chain nodes:** [P2-A2], [P2-A4], [P2-A5], companion [P1-01], [P1-03], [P1-04] and Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain **OPEN**. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** All existing five agent roles, IDs, schedules, enabled states, two-Route-A/three-Route-B allocation and historical R_mix341 grammar/weights are untouched.

## IDEA -> SEARCH -> ITERATE

Initial hypothesis: LSPV-2/512's fixed-parent XOR trace replay extends to affine virtual inputs, where changes to multiple descriptor bits may cancel at guest-observed positions. Falsifiers: (F1) zero observed syndrome but a different authentic recorded guest read-value trace; (F2) rank fails to predict the number of reusable descriptors; (F3) malformed sources or parent changes can forge a replay; (F4) cost of source authentication, rank acquisition or real guest execution is hidden to claim universal FLMV contraction.

Actual project searches for Kraft trace, cylinder cover, affine read kernels, OR-fold 3CNF guest converters, and virtual-child aliasing identified **duplicates**: LSPV-1/252 already proves a scoped Kraft cover bound; LSPV-2/462 already provides the proper-3CNF guest gadget. Neither was redeclared new. Prior LSPV-2/512, LSPV-4/510R, current issue #3, actual Grok and Claude files were read. The revised result below is elementary deterministic trace invariance plus GF(2) rank-nullity, **not a novelty claim**.

Continuity: complete `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, complete `proof2.txt` initial blob `7e972e211c8bd8208dae2f3b6933191f3890b321`; governing handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` blob `c3889a3e514ddbd747150dcb68607013a3b2d154`; AGENTS.md `19656af102604d5f0a721d548cf2e4e72a063561`; CODEX.md `754999f50de93cdb693ed37bc8110d31e9e698ef`; research SKILL prior read blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`; LSPV-2/512 blob `20928dbaf238ffe0364823b232fb61d19d8d952e`; peer LSPV-4/510R blob `2acfe123b4a57c1c238adc8c0750be379b999bd2`; Grok `GROKPROOF/2026-11-08_1130_PROGRESS.md` blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70`; Claude `research/agents/claude/world-ledger/README.md` blob `de75a371ce3143a4495e6892df7fb04794a6b708`.

Outside source ledger, actually retrieved: `konard/p-vs-np/README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` and `scripts/proof_status.json` `93b77ed3d8fe456f81c690035f45f07910a247f2` (model-scoped P subset NP, not transfer); `blkph0x/p-vs-np-proof-research/README.md` `f397a7747eaca82df3d754d0a4b4bab1fe10f814`, `METHOD_INDEX.md` `18d693ea71df543c379eb7afbebc3106e32f03e5`, `INDEPENDENT_AUDIT.md` `b30515cced93d8911a6415555ee9ec1444502d93` (restricted families); `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab`; `meelgroup/frat-xor/README.md` `38a137bca4d4ab6443703d4c31fba5783021c581` (different proof grammar); `berkeley-abc/abc/README.md` `88a9d1a316dd9751acade746de315fd1e6e6c362`; `openai/math/CONTENTS.md` `7e1ed90ac5a666f1bbecb22027387c4ad79e9d03`. Primary FLMV JACM 2005 original PDF Section 2.1 and page screenshot inspected; Acar (2005) is prior work on self-adjusting computation. No separate Google-branded search or native FLMV emulator was used.

## Theorem (PROVED/RESTRICTED)

Fix **one immutable authenticated source** p, one deterministic program A, one input length m, and identical initial guest state. Let descriptor d be in GF(2)^k and define every virtual input bit by

$$
y_i(d)=p_i\oplus c_i\oplus\langle v_i,d\rangle.
$$

Run the guest on anchor d_0. Record the set R of distinct input positions read in its actual complete trace and every observed bit. Write V_R for matrix of rows v_i, i in R. Then the exact **read-value agreement condition** is

$$
\forall i\in R:\ y_i(d)=y_i(d_0)
\quad\Longleftrightarrow\quad
V_R(d\oplus d_0)=0.
$$

Every descriptor satisfying this condition follows precisely the anchor's deterministic execution and yields its label. The affine solution coset has **exactly**

$$
2^{k-\operatorname{rank}(V_R)}
$$

descriptors. Proof: subtract anchor affine bits (p_i and c_i cancel). The resulting equations are exactly the homogeneous system V_R(d xor d_0)=0. Rank-nullity counts solutions. Deterministic machine-transition induction gives identical execution where every observed input symbol agrees. This equivalence is exact for the *authentication condition*, not an assertion that every descriptor failing it changes the final SAT/UNSAT label. For additional affine constraints Hd=b, stack H with V_R and check consistency before counting.

## Finite source-authenticated test (COMPUTATIONAL)

K4 has six edge variables; each cubic vertex parity is exactly four proper 3-clauses, giving 16 original signed clauses. Odd total charge is UNSAT; even charge is SAT (independently brute-forced over 64 assignments). The experimental source adds eight fresh-variable 3-clauses, all individually satisfiable for every choice of their first sign bit. Exact packet: 8-bit magic, unary H=4+stop, 24 ternary clause records of 18 bits each (5-bit variable ID+sign per literal), two-bit end marker, following blank check; **447 input bits**. Descriptor-bit row masks: (9,18,36,8,16,32,64,128). The full matrix has rank 8; the guest reads the first three tail signs, whose rows have rank 3, and skips the remaining five. The guest reads all other authenticated syntax, including core and marker; 442 actual input positions plus one blank read. It is a **restricted original-source parser and parity classifier, not a general SAT decider**.

Two independent Python/Node implementations agreed on 256 distinct children, 32 anchor-compatible read-value transcripts, 224 incompatible transcripts, 256 SAT even-charge and 256 UNSAT odd-charge classifications, six rejected corrupted/malformed packets, exact compatible-descriptor list, and source SHA-256 `9b3e6d8d922f125f44aa69a7d37f22d7fb953d6b9c13f5c671825bae1e63824a`. The first independently written JS version used a different **local clause enumeration order**; this caused a source SHA mismatch and was repaired before final cross-language agreement. Not a native FLMV or historical R_mix341 execution.

## Resource ledger and unresolved transfer

Acquiring and storing explicit observed coefficient rows costs O(|R|k) bits. A conservative GF(2) elimination implementation costs O(|R| k^2) bit operations and O(|R|k) working bits; descriptor membership costs O(|R|k) or O(k^2) with a retained echelon basis. A virtual indexed input bit takes O(k) bit operations to compute and must pay INDEX tape movement/erasure and real source access. Initial source authentication, full guest trace construction, failed attempts, cache maintenance, retention, replay, intermediate state, historical high-water, and every other all-phase cost must be included. The finite test **materialized all 256 sources and retained hashes**, so it does NOT meet a same-machine FLMV resource budget. For k=O(log N), the matrix alone is polylogarithmic, but no all-input rank-acquisition or resource guarantee is established. Full-rank observed matrix gives exactly one descriptor, i.e. no reuse.

Family ledger: published *expanding* cubic odd-charge Tseitin 3-CNF families have exponential **ordinary shared-DAG Resolution** refutation-size lower bounds in the Ben-Sasson/Wigderson and Urquhart models, with size 4H clauses, 3H/2 edges, encoded N=Theta(H log H), and known polynomial GF(2) shortcut. This does NOT give mixed R_mix341 or arbitrary-computation hardness. K4 is only a finite signed-3CNF SAT/UNSAT control, not an asymptotic hard source.

This result neither constructs a uniform all-input solver-dependent child decomposition nor verifies recursive closure or fully charged same-machine bounds

$$
t'\le\max(11/10,3/5+t/2),\qquad
s'\le\max(1/2,s/2).
$$

The existing lead/source models, branching shared-DAG semantics and fixed historical R_mix341 remain unchanged.

**Artifacts:** `experiments/arc/lspv2_513_independent.mjs` (published JS); local reproducibility archive also contains independently executed full Python, detailed 14k-character report, raw Python/JS outputs and checksums. Raw JSON in `results/raw/arc/2026-11-08_2112_LSPV2_AFFINE_KERNEL513.json`; five-role handoff `research/coordination/2026-11-08_2112_LSPV2_AFFINE_READ_KERNEL513_FIVE_ROLE_HANDOFF.md`. Root main.tex untouched.

**Actual advance:** a precise affine-rank extension of same-parent virtual read authentication, with executed both-label and malformed controls. **OPEN:** [P2-A2], full [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04] and Route B's native R_mix341/B3 transfers. P versus NP OPEN.
