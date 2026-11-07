# LSPV-1/465 five-role handoff | 2026-11-06 21:11 PST

**Route B lead. PROVED/RESTRICTED theorem + COMPUTATIONAL finite controls; P versus NP OPEN.**

Both shared trackers read at run start: proof1 blob e417a1a376d3347e6ef8f6915307005f5fa40972 and proof2 blob d3f6779c030a17e920fdba9302915169aae161d7. Material requested node **[P2-B9]**, linked to [P2-B1], [P2-B2], [P2-C1], [P2-C3], [P2-F8], [P2-D1]. [P1-01], [P1-03], [P1-X3] unchanged.

**Exact restricted result:** For any UNSAT original CNF F(X), any auxiliary CNF G(X,Y) with one total fixed-output conservative Skolem section on each leaf of a full binary decision tree over X with L leaves, the minimum distinct paid ordinary shared-DAG Resolution inference nodes satisfy

$$
S_{\mathrm{Res}}(F)\le L\bigl(S_{\mathrm{Res}}(F\land G)+1\bigr)-1.
$$

All G sources disappear by a legal partial restriction on each leaf. Lift the restricted F-source-only Resolution proof without weakening; discharge both child branches at each internal node using no more than one native oriented RES. Share paid nodes once across the final DAG. This is *not* historical full R_mix341 normalization, nor a general Boolean-circuit backtranslation. Optimal tree discovery is not free in physical time bounds.

**Published-family control:** Chvátal-Szemerédi 1988 random proper signed 3CNF at c=6, exponential ordinary RES lower bounds with high probability. If G_n admits a section tree with L_n=2^{o(n)}, exponential RES hardness survives for the augmented sources. No claim for GF(2), AND3, LOCAL-CONVERT, definitions or B3; Cook ER and Tseitin parity shortcuts remain decisive upper controls.

**Finite exact-source check:** K4 odd-charge proper signed 3CNF: 16 original clauses on 6 edge variables, odd 0/64 models and even 8/64. Five strict ternary conservative clauses encode y=x1 AND x2 using two pad variables; the total section has 3 leaves. Branch conclusions x1, (not x1 OR x2), (not x1 OR not x2) are legally joined on x2 and x1 in a verified 31-paid-node original-source Resolution DAG of span 6. This is an upper certificate, not certified optimum or asymptotic hard instance. Python 502 assertions, independent Node 1182 assertions, standalone Node 1123 assertions; each of three checkers rejects five deliberate corruptions. No authoritative historical checker ran.

**Handoffs:** LSPV-3: authenticate historical native typed grammar, investigate whether any paid rule admits a section-restriction simulation, particularly branch scopes and multi-premise hyperedges. LSPV-5: attack this theorem's quantifier "every individual G clause tautological under each leaf" and find allowed nonlinear/mixed shortcuts invalidating a proposed all-mixed generalization; treat all stronger claims as OPEN. LSPV-2 and LSPV-4: do not turn ideal Resolution proof size into an all-input recursively iterable same-machine SAT contraction; audit physical work/depth, construction and peak space only as cross-route critique. LSPV-1: seek noncircular B3 instead of assuming short rejecting traces imply native proofs.

**Published artifacts:** `research/agents/lspv-1/2026-11-06_2111_LSPV1_NONLINEAR_SECTION_TREE_RES465.md`; `experiments/arc/lspv1_465_nonlinear_section_tree_standalone.cjs`; `results/raw/arc/2026-11-06_2111_LSPV1_465_NONLINEAR_SECTION_TREE_SUMMARY.json`. A full locally reproducible archive also contains independent Python/Node implementations and JSON source-indexed certificate. Root main.tex returned blob 68188a24badda635a5983fda1c381cdb694fd497 but zero content bytes; not edited. No task ID, enabled state, title, schedule, role, historical R_mix341 weight or rule changed.

**OPEN:** [P2-D1], [P2-B1], [P2-B2], [P2-C3]; P versus NP.
