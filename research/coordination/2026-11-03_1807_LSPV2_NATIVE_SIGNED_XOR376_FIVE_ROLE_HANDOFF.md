# Five-role handoff: LSPV-2 NATIVE-SIGNED-XOR376

November 3, 2026, 18:07 PST (America/Los_Angeles). Scientific refocus unchanged: begin with established restricted hard families, prioritize the missing sound transfer, and seek a representation/algorithm-independent computational invariant. Existing five task IDs, roles, enabled states, schedules, fixed Rmix341 and publication safeguards remain unchanged. P versus NP OPEN.

## Proven scoped result and its precise scope

**PROVED/EXACT only in the existing signed-AND2 DEF + strict signed RES fragment E_wedge.** For independent distinct original wire inputs a,b, XOR/XNOR requires exactly three paid two-input AND definitions with signed input and output views. This is a minimal circuit gate realization, **not** a global optimum for the full mixed calculus, which admits other gate types and native GF(2). The three-gate construction was already given in LSPV-1/375. The new independently justified increment is a two-gate impossibility proof plus strict source-authenticated RES certificates.

The three paid gates u=a AND NOT b, v=NOT a AND b, w=NOT u AND NOT v realize XOR as signed output NOT w. Six strict RES inferences from the nine authenticated paid DEF slots derive the full four-clause XNOR relation on a,b,w. Four sign combinations have full native clause replay. A k-input prefix uses 3(k-1) paid signed-AND2 gates and, when materializing every interface clause, 6(k-1) paid RES nodes. Its compact chosen DAG is 9(k-1) nodes and O(k log(k+2)) encoded bits, separate from source proof, parsing, physical construction and verification.

An actual complete UNSAT CNF source containing four opposite-polarity binary parity clauses has a **16-paid-node valid E refutation**, consisting of 3 paid DEF and 13 signed RES, with the original clauses authentically free and DEF clause slots *not* free source axioms. This is an upper certificate, not a shortest-proof minimum.

## Explicit falsifiers and controls

F1: 2 signed AND2 gates suffice for XOR, FALSIFIED by the two-input halfcube theorem and 2,304-candidate superset enumeration (constants allowed). F2: the local XOR proof depends on an uncharged implication oracle, FALSIFIED by six actual signed RES steps. F3: a gate circuit itself proves original source parity, FALSIFIED as an inference; the 16-node source example pays all clause ancestry. F4: duplicate-input cancellation, arbitrary circuit-valued LOCAL-CONVERT, and all affine-mask interleavings are already covered, **OPEN**, with full circuit payload and paid constant rails outstanding.

Full independent JavaScript checker passed **75,304 assertions**, including 14 corrupt certificate rejections, 5 malformed DIMACS rejections, 430 parity-prefix assignment checks, 4 sign combinations, six prefix sizes 1,2,3,8,32,128, and a four-clause minimal-UNSAT source. All stages check signed gate freshness and exact binary RES pivots. Python generator 0.72 s / 97,804 KiB peak RSS; independent JS 0.05 s / 33,172 KiB. These host measurements do not establish a machine lower bound. Full source-labelled 462,732-byte dataset SHA-256 cfac2b2e80a9b9835dd998572109a9dce7b46715b2b973b5037e5f4f9f11e8f9 is in the local reproducibility archive. Public JSON is a ledger; public JS is a compact reproducer, not the complete independent checker.

## Mandatory established hardness and direction

Haken (1985): standard explicit unary PHP with h+1 pigeons, h holes, h(h+1) variables, (h+1)+h*C(h+1,2) source CNF clauses and N_h=Theta(h^3 log h) encoded bits has >=2^(c h) lines for **every unrestricted shared-DAG ordinary Resolution proof** for all sufficiently large h, some fixed c>0. This does not imply time lower bounds for arbitrary SAT algorithms, ER2 or full Rmix341. Cook's 1976 short Extended-Resolution PHP proof and LSPV-2/341's exact 4h-1 mixed odd cubic Tseitin cost are mandatory countercontrols. No simulation inequality is reversed.

## Original-peer and independent assessments

Actual Grok path: `GROKPROOF/2026-11-04_0116_PROGRESS.md` blob ca5a835356eb918b8cb4ab94d14de6174edeab03; its universal all-input ARC/FLMV contraction is OPEN. Actual Claude path: `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67; its TPORT barrier is within specified alternation-trading rules, not B3. LSPV-1/375 symbolic X3-to-E polynomial transfer is not fully independently native-certificate replayed; the present local 3-gate/6-RES component is validated. LSPV-3/379 strict E paid gate-source lift is compatible, but its full LOCAL-CONVERT grammar caveat remains. LSPV-4/373 source-bit input floor is an independent *linear input-access* theorem, not superpolynomial all-algorithm hardness.

## Outbox and cross-role next steps

- `research/agents/lspv-2/2026-11-03_1807_LSPV-2_NATIVE_SIGNED_XOR376.tex`
- `experiments/arc/lspv2_376_signed_xor_public.js`
- `results/raw/arc/2026-11-03_1807_LSPV2_NATIVE_SIGNED_XOR376_public.json`
- `research/coordination/2026-11-03_1807_LSPV2_NATIVE_SIGNED_XOR376_FIVE_ROLE_HANDOFF.md`

LSPV-1: use the native slots to audit the four affine mask updates and B3 quantifiers. LSPV-3: audit source/DEF type preservation and repeated variables. LSPV-4: audit literal bit length, bit writes, streaming and full-phase peak memory. LSPV-5: attack the conversion from local authenticated gates to all-rule global polynomial proof simulation. The next missing link is full circuit-valued LOCAL-CONVERT semantics, particularly named internal wire access, followed separately by B3. Full R superpolynomial Wbar, B1/B2/B3 and P versus NP OPEN.

Corpus audit includes current issue #3, approved 2026-11-02 12:04 refocus, AGENTS.md, CODEX.md, pnp-research SKILL, LSPV-2/341 and /373-/375, LSPV-1/375, LSPV-3/379, LSPV-4/373, Grok and Claude actual files. Primary literature searched for Haken, Cook, Urquhart, and Cook-Reckhow; GitHub/openai proof-checker search returned no compatible fixed-R checker. Full repository local preflight could not run because the container lacks a complete checkout. Existing root main.tex may be updated only with full-blob safe owner-region readback.
