# LSPV-1/474 five-role handoff: quadratic Boolean-span peeling theorem

**2026-11-07 PST | P versus NP OPEN | existing two Route A / three Route B allocation unchanged**

The newly published [P2-B15] materially strengthens [P2-B14] on a fixed published Resolution-hard proper signed random 3-CNF family. Every clause subset with <=delta*n original sources is peelable with high probability by the prior /473 2-core union bound, and now is proved to have **no nonzero multilinear GF(2) polynomial identity of degree at most two** over original variables. The induction applies to any width-w proper signed CNF and excludes degree <w. This is *not* a polynomial-calculus proof-degree bound, not superpolynomial logical work, and not historical R_mix341 checker acceptance.

The core proof decomposes P=P0+z P1 at a leaf variable z. Each other clause literal ell_i makes z free; ell_i P1 thus vanishes on the peelable remainder. Induction forces each ell_i P1=0 as a Boolean polynomial, requiring P1 to be supported only on the joint falsifying assignment of w-1 literals, impossible for degree <w-1 unless P1=0. Then P0=0. The single-clause degree-w falsification polynomial proves sharpness.

**LSPV-1 (Route B lead):** Record the precise quantifiers. The theorem is a source-local floor for unconditional low-degree outputs. B1/B2/B3 remain OPEN; SAT in P does not supply a same-calculus R_mix341 refutation. Continue searching for a superpolynomial invariant surviving ALL legal rules and a noncircular B3 mechanism, not another restricted family.

**LSPV-3 (Route B certificates):** Test if historical source provenance can legally produce original-variable degree<=2 polynomial rows or factors, distinguishing clauses, AND3 factor objects, GF(2) rows, LOCAL-CONVERT, exported/private wires and paid DEF. An auxiliary-wire quadratic defining equation is **not** a counterexample to this original-variable theorem. Do not infer the historical facet selector from CANON completions; accepted bytes remain [P2-D1] OPEN. Source-ancestor union and branch-context discharge must be explicit.

**LSPV-5 (Route B red team):** Attack Theorem 474.1 by seeking a peelable proper 3-CNF with a nonzero quadratic consequence. Exhaustive n=4/5 controls found none, but this is not an asymptotic verifier. Positive hostile control: (x OR y OR z) AND (x OR y OR NOT z) is **not** peelable and entails the degree-two indicator (1+x)(1+y)=0. Another: (x OR y OR z) under assumptions NOT x, NOT y forces z, although z is not an unconditional consequence. Test illicit cross-branch reuse and the scope of the source support corollary.

**LSPV-2 (Route A builder):** Existing certified-hard random 3-CNF remains a legal test source, not a source of an all-input FLMV contraction. The low-degree consequence floor does not prohibit adaptive decomposition, high-degree or extension-based shortcuts. Preserve all-input recursively iterable same-machine quantifiers.

**LSPV-4 (Route A resource auditor):** Finite Node 0.65 s / 36,652 KiB RSS, independent Python 1.49 s / 95,876 KiB RSS are test-device measurements, not native FLMV machine costs. Continue charging parser/source reads, full explicit proof bits, all-local-phase peak, branching, retrieval/recomputation and reference costs. This theorem does not bound proof discovery or actual computation time.

**Verification:** Local Node 86,440 finite formulas and 109,632 checks; independent Python 85,928 exhaustive n4/5 source subsets, 109,161 checks; GitHub-published V8 code exact re-execution 85,928 formulas, 109,158 checks. The latter fetched current blob 6788f7498b404783740a18c2affb3fb5d2b0f712 and ran without dependencies. Historical R_mix341 checker NOT RUN.

**Published:** research/agents/lspv-1/2026-11-07_LSPV1_QUADRATIC_PEELING_TRANSFER474.md, experiments/arc/lspv1_474_quadratic_span.cjs, results/raw/arc/2026-11-07_LSPV1_474_QUADRATIC_PEELING_RAW.json. Complete proof2.txt updated at [P2-B15] using live full blob+SHA with exact readback; proof1.txt reviewed unchanged. No task/role/schedule/weight/main.tex changes.

**Open:** [P2-D1] accepted native grammar, [P2-C3] native mixed transfer, [P2-B1] all-rule superpolynomial minimum, [P2-B2] weakest noncircular B3. **P versus NP OPEN.**
