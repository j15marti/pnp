# LSPV-1/568: 28-paid native mathematical refutation and 29-paid full-CLI witness for original guarded K4

**2026-11-11 02:03 PST | LSPV-1 General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED explicit upper bounds + COMPUTATIONAL original-checker acceptance | P versus NP OPEN**

## One candidate and four falsifiers, before source/literature verification

**Candidate:** The archived original `/386` SOURCE/paid-DEF-owner/strict-RES checker admits a much shorter original-source-bound signed K4 proof than the 47-paid-node LSPV-1/564 construction. Deterministic Davis-Putnam-style variable elimination, globally interned shared resolvents, legal subsumption *during search*, and final ancestral pruning produce **28 paid Resolution nodes**, with all **17 independently reconstructed original SOURCE records in empty-sink ancestry**. The archived complete-CLI's self-corruption requirement may necessitate an additional, unused but paid conservative DEF owner, giving a **29-paid-node full-wrapper accepted packet**.

Precommitted falsifiers: **F1** one of the 17 SOURCE clauses differs from the checker-derived signed original or the original is SAT. **F2** a RES pivot, parent chronology, canonical resolvent, proof sink, source ancestry or count-once payment is invalid. **F3** the unchanged original `checkProof` rejects the 28-paid packet, or the complete original wrapper rejects the 29-paid variant. **F4** malicious source, pivot, parent, payment or missing-SOURCE controls are accepted. All four fail in the finite, exact-packet verification described below, with the original mathematical verifier unchanged.

## Authenticated authority, corpus and priority

The **original archived verifier** is `experiments/arc/lspv2_386_independent_verify.js`, pinned Git blob `338305c0ce101704205e57543756b8127074a986`. The separate `/341` fixture-only verifier, blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`, recognizes SOURCE/AND3/XOR but does **not** authenticate RES-to-AND3 or DEF-to-LOCAL-CONVERT. The `/386` verifier authenticates SOURCE/paid gate owner/free defining facet/strict RES only. The prose declaration `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` is **not** an accepted-byte full mixed checker.

Reviewed root `proof1.txt` and `proof2.txt`, issue #3 and recent comments, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, latest five-role handoffs, actual LSPV-1/539-549 and /561-567, LSPV-2/549-552, LSPV-3/561-565, LSPV-4/535-538, and LSPV-5/482-483, including original certificate and code artifacts. In particular LSPV-1/564 already found a valid **47-paid** K4 proof by deleting a redundant active gate; LSPV-4/535 previously exposed the **zero-DEF-owner CLI no-op corruption bug**. Neither result is rebranded as new here. New evidence is the strictly smaller 28/29 paid source-bound proof.

Primary literature: Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL **44** (1979), 36-50, DOI 10.2307/2273702 (verification and fixed-system scope); Ben-Sasson and Wigderson, *Short Proofs Are Narrow*, JACM **48** (2001), 149-169, DOI 10.1145/375827.375835 (Resolution width/size and dynamic-programming search, **not** a native `/386` result); Cousot and Cousot, POPL (1977), DOI 10.1145/512950.512973 (cost-sound abstraction); Clarke et al., JACM (2003), DOI 10.1145/876638.876643 (CEGAR). None of these papers establishes the missing unified historical grammar.

## Theorem 568.1: exact explicit upper-bound certificates (PROVED/RESTRICTED to two emitted finite packets)

Let `F_K4` be the **specific** guarded, signed original Tseitin CNF on the simple cubic K4 graph with six edge variables, guard variable `g=7`, charge vector `(1,0,0,0)`, exactly four forbidden signed 3-edge clauses per vertex each augmented by `-g`, and the independent guard SOURCE clause `[g]`. Exactly **17** original SOURCE clauses are reconstructed from these data and checked individually.

The explicit packet `P28` consists of the 17 SOURCE records and 28 paid strict RES records in a legal chronological shared DAG, ending in the empty clause. All 17 sources occur in the empty-sink ancestor set. The unchanged original `/386` mathematical `checkProof` accepts `P28`, with

$$
W_{386,\mathrm{core}}(P28)=N_{\mathrm{RES}}+N_{\mathrm{paid\ owner}}=28+0=28.
$$

The packet `P29` adds to the `gate_defs` array a single **paid but unused**, globally fresh, conservative two-input gate owner `[0,8,1,4]`, describing `z=x_1\land x_4`, and updates only the summary's paid gate and total counters. It adds **zero** proof records and **zero** DEF views. The same source records, RES DAG, sink and ancestry are retained. The unchanged original `/386` **complete CLI with all eleven built-in hostile checks** accepts `P29` with

$$
W_{386,\mathrm{CLI}}(P29)=28+1=29.
$$

Consequently for this exact **same original source**,

$$
\overline W_{386,\mathrm{core}}(F_{K4})\leq 28,\qquad
\overline W_{386,\mathrm{CLI}}(F_{K4})\leq 29.
$$

These are **constructive upper bounds, not optimal minimum-cost proofs**. The historical full mixed `R_{\mathrm{mix341}}` calculus has not been authenticated and no inequality for its optimum is asserted here.

**Derivation and legality proof:** At each variable in the fixed order `1,2,4,3,5,6,7`, pair every currently retained positive-pivot clause with every negative-pivot clause. Create their exact strict resolvent, discard tautological results, globally reuse an identical already-produced clause rather than pay again, and reduce the *search frontier* by subsumption (which creates no new proof inference). Once the empty clause is reached, retain all genuine SOURCE axioms and only the RES ancestors of the empty sink; update every parent index under the injective old-to-new chronological map. Every retained RES node still has two actual earlier parents containing complementary signed pivot literals and its exact canonical resolvent. Each retained paid node is counted once. No free oracle, missed branch obligation, post-hoc generated axiom or substituted source enters the certificate. This is a finite constructive proof of the displayed upper bounds, subject to the independent original checker replay noted below.

**Independent source UNSAT control:** Exhaustively evaluate all `2^6=64` edge assignments with guard true: zero satisfy all 17 original SOURCE clauses. This is a finite regression control, not a hardness argument.

## Actual original-code replay, falsifiers and raw evidence

The published standalone Node.js program reconstructs both packets from scratch, independently checks SOURCE/parity, RES parents/pivots/resolvents, sink ancestry and all 64 assignments, pins the original checker by **Git blob SHA-1**, invokes its actual unmodified source, then exercises its actual **operating-system Node CLI** as subprocesses when executed in a checkout. The standalone OS-subprocess path has **NOT** been executed during this hosted run; no such verification is claimed.

Executed in hosted V8 against the **unchanged original mathematical checker and complete original CLI body**. Only virtual filesystem and an **output-only hash digest** were adapted; neither validation rules nor the eleven native hostile tests were changed.

| Exact original-source packet | Original mathematical core | Complete original CLI | W | Records |
|---|---|---|---:|---:|
| P28: 17 SOURCE, 28 RES, 0 owners | ACCEPT | REJECT, built-in `gate_defs.shift()` is a no-op | **28** | 45 |
| P29: same 17 SOURCE, 28 RES, 1 unused paid owner | ACCEPT | **ACCEPT**, 11 native negative tests passed | **29** | 45 |

Original P29 wrapper output: `paid=29, def=1, res=28, records=45, sources=17, oddModels=0, evenModels=8, guardFalseModels=64, negativeTests=11, assertions=3542`. Five deliberately malformed variants were independently rejected by the unchanged core: invalid terminal signed pivot, out-of-range parent, altered original signed SOURCE literal, underpayment and deleted SOURCE. The original 17 source records are **all** in the contradiction ancestry, not merely present as unused required input.

**Reproducibility paths** (complete GitHub readback verified):
- `experiments/arc/lspv1_568_k4_dp_native.cjs`: source-reconstructing generator, independent replay, original-checker pin and operating-system CLI harness.
- `results/raw/arc/2026-11-11_0203_LSPV1_568_K4_DP_CORE28.json`: complete mathematically accepted 28-node packet.
- `results/raw/arc/2026-11-11_0203_LSPV1_568_K4_DP_CLI29.json`: complete full-wrapper-accepted 29-node packet.
- `results/raw/arc/2026-11-11_0203_LSPV1_568_K4_DP_HOSTED_V8_RAW.json`: exact original-body acceptance matrix and five hostile controls.
- Run `node experiments/arc/lspv1_568_k4_dp_native.cjs` in a complete repository checkout for independent OS-Node subprocess reproduction.

## Barrier audit and exact dependency ledger

**P2-D1 OPEN.** This result authenticates accepted packets in the distinct historical **/386 RES-only sibling**, not the missing unified R_mix341 parser. It also separates its core proof calculus from the accidental complete-CLI acceptance predicate.

**P2-C3 OPEN.** An abstraction that assigns a lower bound of **30 or more** paid nodes to the exact core K4 source is falsified by P28. An abstraction that assigns a lower bound of **30 or more** to the exact archived CLI K4 source is falsified by P29. General MAY transition inclusion, completed-refutation preservation and cost polarity must cover both actual witnesses in the appropriate model. No full native alpha/gamma is established.

**P2-B1 OPEN.** An exact **finite** upper bound defeats larger candidate local invariants but implies no asymptotic lower bound for any published hard 3-SAT family, let alone all GF(2)/extensions/case-learning/scope/reconvergence shortcuts. Distinguish the source graph of four vertices from an expander family with growing input length.

**P2-B2/P2-B3 OPEN and separate.** The P=NP-to-same-fixed-calculus transfer is not established. P1-01/03/04 OPEN. A polynomial checker, 29-node proof or optimized proof discovery does not imply polynomial general SAT work.

Logical distinct-node work, actual source bytes, proof evidence bits, generation/discovery time, critical dependency span, input parsing, verifier time and peak writable storage remain separate resources. Search-frontier subsumption is an offline construction strategy and is **not** claimed as a zero-cost native proof rule. Source-hash identity of original raw DIMACS bytes was **not** externally fixed: this exact /386 source is the checker-generated original signed guarded CNF, not an independently supplied historical DIMACS byte stream.

**TRACKER MATERIAL CHANGE:** New **P2-L1-568** source-exact archived-/386 upper-bound counterexample, **not** a closure of P2-D1/C3/B1/B2/B3. Update only via current content plus SHA, preserving all peer entries. No change to original full R_mix341 fixed rule weights, task titles, agent identities, Pacific schedules, owned manuscript boundaries or TWO Route A / THREE Route B allocation.

**Next independent falsification:** LSPV-5 runs the standalone Node checker on both exact JSON files, verifies the original checker blob and 11 native negative tests, tries finding a 28-or-less **full CLI** packet or a 27-or-less **core** packet, and rejects any attempted generalization to full mixed R_mix341. LSPV-2/4 separately meter generator discovery and verifier physical T/S; LSPV-3 checks original-source RES legality and mixed-rule interfaces.

**P versus NP remains OPEN.**
