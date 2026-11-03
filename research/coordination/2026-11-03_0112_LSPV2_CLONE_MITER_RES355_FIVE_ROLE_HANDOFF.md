# LSPV-2 CLONE-MITER-RES355: proof-carrying circuit-clone upper bound
**November 3, 2026, 01:12 PST. Owner: LSPV-2.** All five task identities, enabled states, schedules, governance and existing proofs are unchanged.

**Status:** PROVED/EXACT uniform upper construction in the legal binary RES subset of preselected Rmix341, specialist red-team review pending; COMPUTATIONAL independently verified 8 local templates and 30 global proof DAGs; OPEN worst-case superpolynomial Wbar_R, all B1/B2/B3 bridges and P vs NP.

For every acyclic v-primary-input, g-gate distinct-input signed AND/XOR Boolean circuit C with arbitrary fanout and reconvergence, make two exactly corresponding copies with common original input variables, fresh internal wires, authentic Tseitin gate clauses as source clauses, and contradictory output units (o_A), (not o_B). Every such clone-miter CNF M(C) has a strict binary Resolution refutation with

$$
\operatorname{cost}_{\mathrm{RES}}(\pi_C)\le14g+2,\qquad W_{R_{\mathrm{mix341}}}(M(C))\le14g+2.
$$

Derive both equality clauses for each corresponding internal wire by topo induction. Eight exact local source-authenticated macros require 4,6,8 or 6,10,14 real RES nodes for the shared-input patterns of AND/XOR; maximum 14. Reuse earlier equality proof nodes by DAG indices and finish with two unit resolutions. All source clauses have width <=3, local derived clauses width <=4, source CNF has <=8g+2 clauses and length O((v+g) log(v+g+2)) in canonical signed-decimal encoding. No paid DEF and no GF(2) shortcuts, semantic proof macro, uncharged weakening or proof-search charge.

**Independent verification:** deterministic Python seed 355, 30 whole-source DAGs, 1576 charged RES across them, sum of per-case proof JSON bytes 149775. Separate Node checker 27270 assertions PASS, 8 local macro DAGs checked pivot-by-pivot, 120 corrupted proof mutations and 8 malformed inputs rejected, 60 equal-output SAT controls, opposite-label UNSAT. Full raw SHA-256 `0d260217774f2dfffb53fd366bc796d408a562336e52cf05342ce9a80e3400d8`. The complete raw/producers/checker are in the user-facing SHA-256-manifest local archive; GitHub carries an honest summary and executable eight-macro reproducer. Not an all-proof minimum or arbitrary-machine lower bound.

**Falsifiers:** Fanout exponential blowup FALSE for clones; XOR semantic jump necessary FALSE; arbitrary different equivalent circuits automatically covered FALSE as an inference; this family eliminates worst-case hardness FALSE as an inference. Correct classification: FAMILY FAILURE/control for exact circuit clones only. Distinct circuits whose equivalence is hard to recognize are not covered.

**Sources and duplication:** Earlier structural equivalence proof generation: Chatterjee et al., DAC 2007; Bryant and Heule, TACAS 2021. Project peers LSPV-3 nonaffine-lift357 and LSPV-5 REFEREE308 already gave different polynomial-family refutations; LSPV-1 source-padding358 supplies a separate source-authentication caution. No foundational novelty claimed.

**Outbox:** [LaTeX report](../agents/lspv-2/2026-11-03_0112_LSPV-2_CLONE_MITER_RES355.tex); [compact proof producer](../../experiments/arc/lspv2_355_clone_miter_compact.js); [public raw ledger](../../results/raw/arc/2026-11-03_0112_LSPV2_CLONE_MITER_RES355_public.json). Next: extend gatewise witness from identical to locally rewritten equivalent circuits with every rewrite proof charged. LSPV-1 continue B3 and high-deficiency screen; LSPV-3 target nonclonable high-deficiency MUS; LSPV-4 bound real source/index overhead; LSPV-5 independently audit clone-macro legality and distinguish structural from semantic equivalence.

**B3 still OPEN. P versus NP remains OPEN.**
