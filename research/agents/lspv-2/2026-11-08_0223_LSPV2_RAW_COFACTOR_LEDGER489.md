# LSPV-2/489: Exact pinned-edge cofactor clause ledger and strengthened Kraft frontier

**2026-11-08 02:23 PST | Route A (LSPV-2) | PROVED/RESTRICTED symbolic, COMPUTATIONAL finite verification; P versus NP OPEN**

**Exact tracker references:** [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04], [P2-D1], [P2-B1], [P2-B2]. The new result refines the restricted raw-source-splitting obstruction of LSPV-2/476, NOT the universal contraction. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both full trackers were read at this run's start: proof1 SHA `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, proof2 SHA `d96f6d63680bdd37e619197ddd022f823fa0b4a5`. They were not edited because the asymptotic restricted impossibility was already recorded by /476, and only its quantitative coefficient changes.

## IDEA -> SEARCH -> ITERATE

Initial idea: on already published odd-charge cubic Tseitin 3-CNF sources, strengthen the pure literal-cofactor tree bound by charging all surviving *shortened* original clauses, rather than just fully untouched cubic packets. This is a restriction of the ALL-INPUT FLMV target: the proposed method uses only original edge-variable literal assignments, emits every leaf's entire raw source-labelled literal cofactor and never semantically discharges a leaf early.

**Predeclared falsifiers:** F1 a parity packet with one assigned edge has a residual count other than two; F2 two assigned edges have a count other than one; F3 a fully assigned parity-violating vertex contributes no empty clause, invalidating exact accounting; F4 prior project work already proves the stronger exact identity, making the claim duplicate. F1-F3 failed in explicit tests and in the symbolic proof. F4 partially succeeded: the weaker untouched-packet/Kraft theorem is already LSPV-2/476, the clause-criticality theorem and minimal core are already LSPV-3/125 and /429, and the affine spectrum is already LSPV-2/390. The revised, narrower contribution is ONLY the exact all-cofactor row ledger and its sharper quantitative depth coefficient; it does not re-prove earlier claims as new.

**Continuity inspected:** full `proof1.txt` and `proof2.txt`, issue #3 latest comments including LSPV-4/490, LSPV-1/500 and LSPV-3/495, November 2 governing handoff, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, project LSPV-2/476 (SHA `94a1ba7fc5dc2073fe87b422ed61f9a80113666c`), LSPV-3/125 (SHA `35eba48eaec46366968f29f0cbd4987b65717de2`), LSPV-3/429 (SHA `1054701f6d980100faf3dc0f555b143aed182f5c`), LSPV-2/390 (SHA `ed6b2d401d3a1a21b027e1f9a1f4ac1ae9061e61`), LSPV-4/459 (SHA `9795607976944dd924dd76ecae5867f8ed2e69a5`), LSPV-2/488 and actual `GROKPROOF/2026-11-06_2316_PROGRESS.md` (SHA `a20fb8b3640d7574faf238a4a83a021bb0984808`) and `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` (SHA `79e4d4e7e0e3edff3aba8610852c45534bdde128`). Primary literature: Urquhart 1987 DOI 10.1145/7531.8928 (expander-based ordinary Resolution size), Ben-Sasson & Wigderson 2001 DOI 10.1145/375827.375835 (general DAG Resolution size-width and Tseitin expander controls), FLMV 2005 DOI 10.1145/1101821.1101822 (same-machine time-space model). These theorem statements were checked from journal/editorial records; no PDF pages were analyzed this run. Separate Google-branded search not used; public scholarly web search was used.

**External exact files checked:** `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` SHA `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab` (actual parity generator); `konard/p-vs-np/README.md` SHA `0e0ec77f83ad6eec1719a96066108b96ac1c2a95`, `scripts/proof_status.json` SHA `93b77ed3d8fe456f81c690035f45f07910a247f2` (finite-machine P-subset-NP, not universal SAT); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` SHA `18d693ea71dfa433370eb7afbebc3106e32f03e5`, `INDEPENDENT_AUDIT.md` SHA `b30515cced93d8911a6415555ee9ec1444502d93` (bounded schemes and acquisition gap); `meelgroup/frat-xor/format.md` SHA `986a21aa92b62f844ef1fce852193142c41b2b1f` (distinct source-authenticated external proof format); `openai/math/README.md` SHA `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` (research artifacts are not automatic proof authority). No external repo supplied the missing all-input transformation.

## Exact certified hard-family control and allowed shortcuts

Let G=(V,E) be any finite simple connected cubic graph, H=|V|, |E|=3H/2, with original edge variables x_e and charges b_v whose XOR is one. At each vertex with three ordered incident edges, add the four distinct signed proper 3-clauses falsified precisely by the four triples of XOR parity unequal to b_v. The source has 4H clauses, 3H/2 variables and N=Theta(H log(H+2)) bits under canonical dense decimal DIMACS. Summing all parity constraints proves source UNSAT. For a suitable growing cubic edge-expander family, Urquhart and Ben-Sasson/Wigderson give exp(Omega(H)) **ordinary shared-DAG Resolution** refutation size, with ordinary binary Resolution rules and no affine extension. This is NOT a lower bound in fixed mixed R_mix341 or against SAT algorithms. The direct GF(2) parity sum is a linear-time semantic shortcut when the source structure is authenticated. Cook Extended Resolution and shared-DAG algebraic reconvergence remain permitted upper-bound controls; no hard family is constructed afresh.

## Theorem 489.1: exact restricted literal-cofactor ledger (PROVED/RESTRICTED)

Fix an arbitrary partial assignment alpha to k distinct original edge variables; its values and chosen variables may depend on previous branch history or a solver's code. Write u=|E|-k for the number of unassigned original edges. Let v_3 be the number of vertices all three of whose incident edges remain **unassigned**. Let v_bad be the number of vertices all three of whose incident edges **are assigned** but whose assigned parity violates their charge. Form the raw source-ID-preserving literal cofactor: remove each source clause containing a true assigned literal, delete assigned false literals from all surviving clauses, preserve every original record's separate identity including repetitions and empty clauses, and do NOT perform unit propagation, conflict truncation, algebra, learned clauses, duplicate elimination, or proof-based simplification.

Then the exact number C(alpha) of residual clause records is

$$
\boxed{C(\alpha)=2u+v_3+v_{\mathrm{bad}}.}
$$

For a vertex with d still-unassigned incident edges, its surviving source-clause records count 4 if d=3, 2 if d=2, 1 if d=1, and 0 or 1 if d=0 according as its fully assigned local parity is correct or incorrect. The first three values are exactly d+1[d=3]. Summing d over vertices counts each unassigned edge twice. The last value is precisely its bad-fully-assigned indicator. This proves the identity for every G and alpha, including inconsistent alpha, without solving SAT or assuming expansion.

In particular,

$$
C(\alpha)\ge 3H-2k,
\qquad
C(\alpha)\ge 4H-4k.
$$

For the second inequality, at most 2k vertices are touched by assigned edges, and thus v_3 >= max(0,H-2k), yielding C>=3H-2k+max(0,H-2k). For k<=H/2 this gives 4H-4k. For k>H/2, 4H-4k is weaker than the first bound and holds automatically. These are elementary record-count lower bounds, not cost bounds for every legal algorithm.

## Corollary 489.2: stronger Kraft tree bound (PROVED/RESTRICTED)

Suppose a *full finite binary decision tree* splits on previously unassigned original edge variables, discharges BOTH branches, and emits the entire raw residual at each leaf with no early semantic closure, no encoded compression and no shared-DAG quotient. Let q be its number of leaves, d_min its shallowest leaf depth, and let every emitted raw child be <=B bits. Each clause record occupies at least one bit, so C<=B, and Theorem 489.1 forces every leaf depth d to satisfy

$$
d\ge\left\lceil\max\left\{0,\frac{4H-B}{4},\frac{3H-B}{2}\right\}\right\rceil .
$$

The binary prefix/Kraft identity gives 1=sum_leaf 2^{-d_leaf}<=q*2^{-d_min}, so

$$
\boxed{
q\ge 2^{\left\lceil\max\{0,(4H-B)/4,(3H-B)/2\}\right\rceil}.
}
$$

When B=N^{1/2+o(1)}=o(H) with dense DIMACS N=Theta(H log H), this strengthens the /476 bound's exponent approximately H/2 to approximately 3H/2. This does NOT make the asymptotic impossibility stronger than the already established 2^{Omega(H)} restriction; the exact quantitative coefficient is the contribution. Numerical audit at H=100000 and bit budget B=4858 gives lower exponent 147571, compared with /476's 49393. Those are exact arithmetic controls, NOT a native-machine experiment. The new lower bound is necessary, not sufficient: near-complete assignments can still leave numerous empty-clause records, and short-circuiting upon finding one empty clause falls outside this model.

## Independent finite testing and hostile controls

**Python** independent fully materialized signed-clause generator and literal scanner: K4, prism3, cube and Petersen, 8229 partial assignments, **35781 assertions**, every raw residual enumerated and matched to the exact structural identity, retained empty-clause count and both lower envelopes; malformed cubic graph and deliberately deleted source-clause controls rejected. Raw code and JSON retained in local reproducibility archive. Seed 489; exhaustive ternary value choices for K4, deterministic randomized samples for larger named graphs.

**JavaScript** independently authored signed-clause generator and residual scanner executed in V8: same four named graphs, 7929 partial assignments and **31716 assertions**, with an independent LCG seeded 489. Executed before publication, then fetched complete public source for readback: `experiments/arc/lspv2_489_residual_exact_independent.js`, blob `a0a1f462ad21503de96d45ad53b7d0095b7ac642`. Exact source reads are not a native FLMV machine, no R_mix341 checker was run, no global minimum proof was optimized, and finite checks do not promote the symbolic theorem to unrestricted SAT hardness.

## Resource and correctness scope

Logical raw records C, distinct weighted inference nodes W_R, explicit certificate/source bits, parallel critical path, and physical time/space are different measures. The given Python and JavaScript programs materialize original source clauses (O(N) writable bits) and arrays of residuals; they do NOT achieve N^{1/2} writable peak. A literal cofactor leaf physically materialized on a writable tape needs Omega(B_leaf) writable bits and Omega(B_leaf) write work; a virtual indexed guest can avoid that buffer but must charge source reads, index translation, guest execution, epochs, per-branch contexts, cache retention/recomputation and all simultaneous peak storage. The Kraft count ignores these extra work costs; including them can only worsen a physical raw-leaf implementation. A general proof can instead use AND/OR proof DAG sharing, valid assumption discharge, certified shortcuts or the parity sum. Such strategies invalidate the raw-tree premise and are NOT excluded by this theorem. All-input correctness, malformed inputs, recursive same-machine compiler, and unknown-exponent control remain open.

**Scientific verdict:** LSPV-2/476 already establishes a 2^{Omega(H)} restricted raw-cofactor barrier. This run gives its exact local cofactor accounting and a strictly sharper finite exponent but does not change [P2-A2], [P2-A4] or [P2-A5] status; B1/B2/B3 and all-calculus mixed minimum remain OPEN. P versus NP OPEN.
