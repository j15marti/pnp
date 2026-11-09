# LSPV-2/510: Compositional live-in and write-effect replay

2026-11-08 19:15 PST | Route A | PROVED/RESTRICTED abstract-machine lemma + COMPUTATIONAL finite controls | P versus NP OPEN.

**Exact nodes:** [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04] remain OPEN. Cross-route [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Historical R_mix341, all five agents, schedules, Route A/B allocation and root main.tex unchanged.

## IDEA (declared falsifiers before search)

Hypothesis: Two authenticated deterministic guest phases P then Q with frame-preserving effects can be combined into one trusted effect summary. A different caller may reuse the combined computation without importing any untouched anchor-private memory. Exact original live-ins include only those Q cells which P did not already write. Reuse remains source- and context-scoped, and all replay/search/provenance/history costs must be charged.

Falsifiers: F1: P writes a cell which Q then reads, but compositional matching incorrectly requires the original caller value. F2: changing a true original live-in alters a dynamic write address yet still passes eligibility. F3: last-write collision or copying anchor poststate overwrites a target cell not written by either guest. F4: input or register mismatch, corrupted summary, or ancestral WORK high-water is lost through cache reuse.

## SEARCH and verified literature/repository baseline

Read BOTH complete root trackers on GitHub main. Preflight full SHA/content lengths: proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, 18,553 characters; proof2.txt blob 061aee5ffdf27393ff5ea96c807f2da91efd5367, 592,669 characters. Also reviewed current issue #3, governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md, AGENTS.md, CODEX.md, and .codex/skills/pnp-research/SKILL.md.

Exact peer reports: research/agents/lspv-2/2026-11-08_1813_LSPV2_FRAME_PRESERVING_EFFECT_REPLAY509.md, blob cd11b940ba5c4ac6a96fe8f0df475b1ba7c37ba6; research/agents/lspv-4/2026-11-08_1804_LSPV4_FULL_CHARGE_PARITY_CYLINDER_COVER507.md, blob 20cf9f97f61d52eca52b71163041bf6e32c210d2; and research/agents/lspv-4/2026-11-08_LSPV4_CHARGE_SEMANTIC_QUOTIENT508.md. The LSPV-4/508 result explicitly distinguishes a small semantic charge-parity DAG from the exponentially large complete-input answer trace cache. This work deals instead with caller-private memory effects.

Actual independent files inspected: GROKPROOF/2026-11-08_1130_PROGRESS.md, blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70, and research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex, blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67.

Required external sources inspected by actual path and blob:
- konard/p-vs-np: README.md 0e0ec77f83ad6eec1719a96066108b96ac1c2a95; SOLUTION_STRATEGIES.md 62f59558c1b3892b1582fd47a87fff48eede6711; scripts/proof_status.json 93b77ed3d8fe456f81c690035f45f07910a247f2. Its theorem tests do not establish P versus NP.
- blkph0x/p-vs-np-proof-research: README.md f397a7747eaca82df3d754d0a4b4bab1fe10f814; METHOD_INDEX.md 18d693ea71dfa433370eb7afbebc3106e32f03e5; INDEPENDENT_AUDIT.md b30515cced93d8911a6415555ee9ec1444502d93. Its bounded and conditional local methods leave acquisition of arbitrary-input prerequisites OPEN.
- meelgroup/frat-xor/README.md blob 38a137bca4d4ab6443703d4c31fba5783021c581 is a distinct external XLRUP pipeline; MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab is an original source generator; berkeley-abc/abc/README.md blob 88a9d1a316dd9751acade746de315fd1e6e6c362 concerns DAG-aware rewriting; openai/math/CONTENTS.md blob 7e1ed90ac5a666f1bbecb22027387c4ad79e9d03 is a mathematics index, not a native FLMV simulator.

Primary research: Fortnow, Lipton, van Melkebeek, Viglas, Time-Space Lower Bounds for Satisfiability, JACM 52(6), 2005, https://doi.org/10.1145/1101821.1101822. Acar, Blelloch, Blume, Harper, Tangwongsan, An Experimental Analysis of Self-Adjusting Computation, TOPLAS 32(1), 2009, https://doi.org/10.1145/1596527.1596530. Acar, Blume, Donham, A Consistent Semantics of Self-Adjusting Computation, JFP 2013, https://doi.org/10.1017/S0956796813000099. These supply prior art for dynamic dependence, side effects, and resource accounting; no novelty claim. Public web search was used; a separate Google-branded search endpoint was not available.

## ITERATE: exact compositional effect lemma (PROVED/RESTRICTED)

Let a genuine trusted deterministic execution of phase P, followed by Q from P's actual terminal state, record immutable input read maps Q_P,Q_Q, first-read-before-first-write WORK maps L_P,L_Q, WORK written address sets W_P,W_Q and last-write maps V_P,V_Q. Entry/terminal registers, guest code, address semantics and control state are authenticated. Each phase may dynamically choose addresses based on previously observed WORK and input.

For a different caller input and original WORK state, sufficient compatibility is matching the recorded input positions and matching precisely the surviving original live-in cells:

$$
Q_{P;Q}=Q_P\cup Q_Q,\qquad
L_{P;Q}=L_P\cup(L_Q\setminus W_P).
$$

The combined written domain is W_P union W_Q. The last-write map is **right-biased**: V_{P;Q}(a)=V_Q(a) if Q wrote a, else V_P(a) if P wrote a. For every address a, the target memory after *both* guest phases is

$$
M'_{\mathrm{out}}(a)=
\begin{cases}
V_{P;Q}(a),& a\in W_P\cup W_Q,\\
M'_{\mathrm{in}}(a),& a\notin W_P\cup W_Q.
\end{cases}
$$

**Proof:** Apply the single-guest transition induction of LSPV-2/509 to P, giving exactly P's anchor control flow and write effects. At the start of Q, every original live-in cell that P has written has the original anchor value because P's writes are the same. Every other original Q live-in is explicitly matched by L_Q minus W_P. Thus each Q input and WORK read agrees, and deterministic induction gives identical subsequent control flow, dynamic addresses and Q last writes. Choosing the latest writer establishes the equation; cells in neither write domain retain their target caller's original values. Repeating this induction proves the chain formula with L_i minus all earlier W_j. Source identity and branch-assumption scope must match; case-split/discharge rules are not added to R_mix341. QED.

**Resource limit:** This semantic composition is not a free native random-access machine operation. A direct summary uses O((|Q|+|L|+|W|)log(N+H+2)) evidence bits at largest accessed address H, plus exact code/provenance and register data. Pay construction, all input/WORK comparisons, replays, failed matches, retrieval/recomputation, INDEX operations, resets, storage, and physical WORK access. Retain inherited historic WORK-read high-water from the caller; do not infer it from terminal configuration alone. No all-input N^(1/2+o(1)) space or N^(11/10+o(1)) time bound follows. The finite guest classifier is exponential, not a hypothetical polynomial SAT solver.

## Established family, encoding and shortcut ledger

Connected cubic G=(V,E), H=|V|, m=3H/2 edge variables; each vertex charge contributes four signed, proper width-three **original** clauses forbidding the local assignments of the opposite parity. This is 4H clauses and Theta(H log H) source bits in a growing numeric encoding. SAT holds iff the XOR of vertex charges is zero. On suitable expander graph families, established ordinary shared-DAG Resolution refutations are exponentially large in H (model-specific results by Urquhart and Ben-Sasson/Wigderson); unrestricted GF(2) Gaussian elimination is a polynomial algorithmic shortcut and a mandatory separate-proof-system control. K4 is merely a finite source control, not asymptotic evidence. Equisatisfiable reencoding alone transfers no proof-size lower bound into R_mix341.

## Independent computation and attacks

The full, independently executed local Node.js verifier generates 16 original signed K4 source CNFs (6 variables, 16 clauses each) from source vertices/edges and brute-force parses/classifies them. Eight charge patterns are SAT and eight UNSAT. Six additional malformed encodings are rejected. P first reads WORK[2], then writes WORK[2] and WORK[5]. Q reads those P-written cells, reads original WORK[8], chooses a write address 12+WORK[8], writes WORK[8], then reads it again. Composite first-live-in set is exactly {2,8}, not {2,5,8}; anchor write set {2,5,8,12}. WORK[13] and WORK[99] must stay caller-owned.

The full control passed **1,915 assertions**, over 22 sources times 32 memory variants: **176** sound replays, **528** intentionally disallowed combinations, and **88** accepted replays preserving an ancestral symbolic WORK peak of 1,048,576. It also checked input changes and entry register mismatches. A separately written small JavaScript control published at experiments/arc/lspv2_510_composed_effect_control.cjs passed **52** checks on 64 memory configurations with 16 correct replays and 48 rejected matches; it checks parity labels on all 16 K4 charges but is **not** a native source parser. Neither is a native FLMV emulator or authoritative historical R_mix341 checker. Finite replay asserts behavior, not global minimum cost.

Full local verifier SHA-256: 17d1278a34cd134dfd29c70c6bef72cd9d19536d75c0cd3a27d315e572031528. Full local raw result SHA-256: e8e880d87a94ba2c0d3c8ab423e06b1936b43a862ef609ae707c51ecabe20185. These are available in the separately supplied reproducibility ZIP.

## Remaining gap

**Actual advance:** a two-phase/finite-chain trusted-effect formula and successful independent adversarial controls with precise ownership and historical WORK peak. **No universal reduction:** worst-case cache hit rate may be zero, and summary acquisition plus source parsing could be as costly as the original guest. [P2-A2] general solver-dependent child construction, [P2-A4] fully charged all-input time/space, and [P2-A5] recursive same-machine closure remain OPEN. [P1-01]/[P1-03]/[P1-04] and Route B [P2-D1]/[P2-C3]/[P2-B1]/[P2-B2] remain OPEN. **P versus NP remains OPEN.**


## Additional independent Python replay (verification addendum, same scope)

An independently authored Python model regenerated the **identical K4 source SHA-256** for the first charge assignment: d2947ac9567bd6ed42c5557f2abaccfc69b745b1cdfe29ee7ad761761ea73273, matching the original source digest independently recorded in LSPV-2/509. It independently brute-force classified 16 signed original K4 3-CNFs and rejected six malformed controls. Across 22 source strings and 64 caller-memory configurations it passed **3,938 assertions**, including **352 exact frame-preserving composite replays** and **1,056 guarded nonreuses**. The test matrix also contains 176 eligible targets flagged with million-cell **symbolic ancestral peaks**; this Python program does not natively measure FLMV space, unlike the separate Node abstract ledger.

Python source SHA-256: e713ec5cd63f804427b58b98304b49a696dd8b9000fe93a4efbf4261233c4d8d. Independent source, raw output and SHA256SUMS are packaged alongside the original Node verifier at LSPV2_510_COMPOSED_EFFECT_REPRO.zip delivered with this run. A second implementation language strengthens finite validation only and does not change any universal proof-chain status.
