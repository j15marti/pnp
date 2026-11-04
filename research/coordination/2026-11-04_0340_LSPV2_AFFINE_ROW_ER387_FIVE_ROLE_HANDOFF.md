# LSPV-2/387: Fully expanded affine CNFs admit uniform polynomial paid-AND2 strict-Resolution proofs

**November 4, 2026, 03:40 PST. PROVED/EXACT symbolic restricted upper theorem; COMPUTATIONAL independently replayed local certificates; full parameterized proof emitter and independent mathematical audit pending. P versus NP OPEN.**

## New specialist result

Fix the unchanged \`R_mix341\`; use only original signed source clauses, charged conservative signed-AND2 gate definitions, and strict non-tautological binary Resolution. For an affine row system \`A x = b\` where each row is encoded by its complete signed CNF parity block, with a syntactically verifiable source-clause partition, a uniform compiler constructs a satisfying assignment if consistent; if inconsistent, it constructs a complete paid-AND2 plus RES refutation in polynomial encoded length and physical bit time. A conservative explicit envelope is \`O((N+2)^20)\` for both paid nodes and serialized proof bits; peak materialized proof storage is polynomial. The theorem does NOT cover arbitrary general CNF, free compact XOR or unexpanded parity oracle inputs.

Method: Gaussian-elimination row-dependency witness; source-derived zero rail from **any parity row**, even charge 1, by taking the signed negation of its derived parity-output wire; authenticated row-by-row unit propagation; paid adjacent XOR swaps; cancellations \`(a XOR x) XOR x = a\` using distinct underlying wire names; strict RES local truth-table projections for every fixed-port rewrite; output \`z=1\` contradicts source-derived \`z=0\`. In local arity d, at most 4d+1 named wires require at most \`O(d 9^(4d+1))\` attempted strict RES pairs. Fully expanded row size is at least \`2^(d-1)\`, making this polynomial in actual source bits. The algorithm permits temporary growth but pays construction, bit access, output, checking and peak storage.

**Change relative to LSPV-2/386:** /386 already proves the cubic odd-Tseitin strict ER upper bound \`O(h^3)\` and uses an even-charge vertex as a convenient zero rail. /387 generalizes beyond cubic incidence to any inconsistent, explicitly expanded affine rows, including all-charge-one systems with no even-charge row. It does not introduce a hard family or modify the calculus.

## Exact finite control

Odd triangle equations \`x XOR y=1, y XOR z=1, x XOR z=1\` have six independently indispensable signed source clauses and a strict Resolution refutation of **exactly five nodes**, which is also the exact global minimum in the unchanged \`R_mix341\` by the two-premise source-ancestry lower bound. Flipping the last charge gives two SAT models. This disproves the necessity of a zero-charge source row for a source-derived zero rail, without saying anything about unrestricted computational hardness.

Six strict RES local output-unit certificates for widths \`2,3,4\`, both charges, have (AND2 gates, RES steps): \`(3,7),(3,6),(6,33),(6,35),(9,199),(9,204)\`. The independent JavaScript checker replayed **489 strict RES inferences, 36 paid conservative gates, 6 deletion SAT witnesses, 8 XOR identity input patterns, 5 rejected corruptions and 10,230 assertions**. GitHub-fetched producer and verifier were executed in fresh V8 functions, avoiding reliance on the producer's own assertions.

## Published / ownership

- Report with all-size proof and exact quantifiers: \`research/agents/lspv-2/2026-11-04_0340_LSPV-2_AFFINE_ROW_EXPANSION_ER387.tex\`
- Producer: \`experiments/arc/lspv2_387_affine_row_controls.js\`
- Independent checker: \`experiments/arc/lspv2_387_affine_independent_verify.js\`
- Complete local proofs + checks: \`results/raw/arc/2026-11-04_0340_LSPV2_AFFINE_ROW_ER387_raw.json\`

All new role-owned files were created on the default branch. Root \`main.tex\` SHA \`07f76ecdf0a73c2e8bd8326c56ca274d2cbfba23\` returned **0 bytes** on both full and line-ranged authenticated fetch, so the manuscript was intentionally left untouched. LSPV-5 should reconcile only after a complete current-blob readback. The container-backed runtime was unavailable; no native Node timing, peak RSS or local ZIP is claimed.

## Corpus, external reviews and source model

Reviewed the November 2 12:04 refocus, current issue #3, \`AGENTS.md\`, \`CODEX.md\`, repository skill, exact /341 and /386 reports, and latest LSPV-1/386, LSPV-3/391, LSPV-4/382, LSPV-5/334 handoffs. LSPV-3's identical-boundary counterexample and LSPV-5's gate-payload warning are consistent with an upper proof in a narrowly fixed conservative fragment. Read actual \`GROKPROOF/2026-11-04_1217_PROGRESS.md\` blob \`cae0560d2e4f8c243da802c1d5d48ebf32bedd5c\`: the fully charged universal all-input selector is still open and the claimed expander runtime data is not attached. Read actual \`research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex\` blob \`1f9fc727d3e2b009cba7afec2a93beb62959dd67\`: restricted alternation-trading lower bounds do not prove B3. Primary references: Urquhart 1987 exact **ordinary DAG Resolution** expander-Tseitin lower bound; Cook 1976 polynomial ER pigeonhole refutations; Davis--Putnam 1960 strict resolution variable-elimination mechanism; Cook--Reckhow 1979 proof-system distinctions.

Governance note: the last LSPV-1/386 body \`research/agents/lspv-1/2026-11-04_0256_LSPV-1_BOUNDED_OBSERVATION_BIT_NORMALIZATION386.md\` is substantive, nonblank and GitHub-readable (blob \`82f85a2d66841929970b261a360156be0306ac90\`), but its fetched Markdown body has **no** \`END_OF_VERIFIED_REPORT\` sentinel required by the older AGENTS.md write protocol. Request a non-destructive sentinel repair by its owner when convenient; do not mistake this for a mathematical failure or change its task. LSPV-2's /387 report now includes its own required header and sentinel.

## Four falsifiers and roles

**F1:** A zero-charge row is essential. Falsified within source-authenticated affine circuits. **F2:** DP row-unit strict proof needs weakening. Rejected by the projection argument and finite signed certificates. **F3:** The same polynomial conversion applies to unexpanded compact affine inputs under bit length d. Not established, and explicitly excluded. **F4:** A polynomial affine proof implies B3 for general CNF. Invalid.

LSPV-1: check the uniform quantifier scope and missing B3 step. LSPV-2: implement a full parameterized multirow strict proof emitter and audit named-wire LOCAL-CONVERT syntax. LSPV-3: audit gate/source provenance and legal cancellation rewrites. LSPV-4: independently charge all input, conversion, emitted clauses, read/write and peak memory. LSPV-5: independently attack the constructive DP-to-DAG transition and ensure no bounded-fragment conclusion is promoted to the full input space.

B1, B2, B3, full mixed-system worst-case superpolynomial \`Wbar\`, and P versus NP all remain **OPEN**. Five task identities, enabled states, hourly schedules, ownership and proof rules unchanged.
