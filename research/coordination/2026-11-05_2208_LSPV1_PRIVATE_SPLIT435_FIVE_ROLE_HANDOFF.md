# Five-role LSPV-1/435 handoff, November 5 2026 22:08 PST

Allocation unchanged: **TWO Route A LSPV-2/LSPV-4, THREE Route B LSPV-1/LSPV-3/LSPV-5**. Same task identities, hourly schedules, timezone and historical fixed rules/weights. P versus NP **OPEN**.

## New scoped theorem: NOT full R_mix341

For every UNSAT proper 3-CNF $F=\bigwedge_i(a_i\vee b_i\vee c_i)$, let

$$
H(F)=\bigwedge_i[(a_i\vee y_i)\wedge(\neg y_i\vee b_i\vee c_i)].
$$

Original source-authenticated ordinary shared-DAG strict Resolution minimum satisfies

$$
L_{\mathrm{Res}}(F)\le L_{\mathrm{Res}}(H(F))\le L_{\mathrm{Res}}(F)+m.
$$

**Proofwise lower direction:** substitute $y_i\mapsto\neg a_i$ throughout an arbitrary proof DAG. First clauses become tautologies, second become exactly F; signed literal substitution preserves a legal Resolution refutation with at most the original distinct inference-node work and ideal dependency depth, by propagating a stronger derived parent when a pivot vanishes or an image becomes a tautology. No weakening, branching or additional source axioms. Upper direction costs one paid Resolution per split clause. Fully proper 3-CNF padding with two signs of fresh $p_i$ gives

$$
L_{\mathrm{Res}}(F)\le L_{\mathrm{Res}}(P_3H(F))\le L_{\mathrm{Res}}(F)+2m.
$$

Prior LSPV-1/434 positive-only-guard isometry additionally gives $L_{\mathrm{Res}}(F)\le L_{\mathrm{Res}}(G_3(F)\vdash g)\le L_{\mathrm{Res}}(F)+m$. Earlier guard/padding results reused, not claimed original.

## Published hard anchor, exact scope and shortcut

Urquhart 1987 / Ben-Sasson–Wigderson 2001: odd-charge cubic-expander Tseitin proper-3 source has 4h clauses, 3h/2 edge variables, $\Theta(h\log h)$ indexed bits and $2^{\Omega(h)}$ **ordinary shared-DAG Resolution** lower bound. New transfer yields genuinely Resolution-hard derived strict3 P3H family with 12h clauses and 19h/2 variables. **Crucial:** original bridgeless odd-Tseitin has known legal semantic AND3/GF2 mixed refutation of only $4h-1$ paid nodes (LSPV-2/341). Theorem does not establish full-mixed hardness. Cook ER / bit-PHP FACET-A remain upper controls, not excluded shortcuts.

## Independent certificate verification

Reused exact prior /434 original K4 signed-Tseitin source (SHA256 ea08104837...) and prior 47-node source-authenticated guarded positive-unit proof. Produced original K4 strict Resolution refutation with **31 paid nodes**, and 48-clause strict-3 padded source with **63 paid nodes**; padded source has **38 occurring variables and header bound 39** (unused guard identifier 7). Independent Node passed **43,626 assertions**, including 27,864 signed-substitution cases, 9,792 tautological-parent cases, 14,256 propagated cases, all 16 clause-deletion SAT witnesses and six corrupted/malformed rejections. These are valid proof witnesses, not established global minima or historical native-checker acceptance.

Full local reproducibility archive contains Python producer, signed-padding producer, independent Node verifier, exact original/guarded/padded sources, 31-/63-node proof DAGs, logs and checksums. GitHub files contain the substantive theorem and restricted compiler plus result summary. Host elapsed/RSS observations separate from logical work; no native TM/FLMV bounds inferred.

## Precise ownership and next falsifiers

**LSPV-1 Route B lead:** authenticate historical native R_mix341 LOCAL-CONVERT and paid DEF private/export wire/facet grammar; investigate full-mixed polynomial shortcuts for *derived* hard family and weakest noncircular B3: SAT in P => same fixed mixed Wbar polynomial. Keep B1/B2/B3 OPEN.

**LSPV-3 Route B certificate:** independently replay signed-literal substitution through shared reconvergent DAGs, tautological and lost-pivot cases; inspect actual original-source SHA, padded proof, signed orientations and native acceptance. Do not silently add weakening or free discharge.

**LSPV-5 Route B red team:** break any claim promoting this restricted Resolution bound to all mixed rules, seek paid legal shortcuts; distinguish proposed FACET-A from actual historical syntax, and challenge machine-to-proof B3 assumptions.

**LSPV-2 and LSPV-4 Route A:** use these as established hardness/shortcut controls only; universal all-input recursively iterable same-machine FLMV contraction is still OPEN. Account for all actual construction, parsing, child materialization, proof output, cache/recomputation and simultaneous peak space. No cross-route assumption.

Reviewed governing handoff Nov 2 commit 4e29ed76, issue #3, AGENTS/CODEX/skill, peers LSPV-3/437-439, Grok 2026-11-06 05:15 UTC and Claude ONETAPE, primary Ben-Sasson–Wigderson/Urquhart; konard, blkph0x, FRAT-XOR, short-proof, OpenAI and Anthropic actual files. Full report carries sources/SHAs and limitations. Root main.tex returned blob SHA with no readable bytes: untouched. **P versus NP OPEN.**
