# LSPV-3/617: Native /386 source-domain vacuity and a rule-soundness audit repair

**2026-11-13 09:24 PST | LSPV-3 Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED plus COMPUTATIONAL | P versus NP OPEN**

**IDs:** [P2-L3-617] restricted source-domain audit and regression; [P2-D1], [P2-C3], [P2-B1] remain OPEN, [P2-B2/B3] separately OPEN. This does NOT authenticate historical mixed R_mix341.

## Candidate and falsifiers fixed before the experiment

**Candidate:** The recovered original /386 checker syntactically permits only odd-charge guarded Tseitin sources. Consequently, its global property "every accepted packet proves an UNSAT source" is incapable by itself of testing inference soundness, even when all signed SOURCE records and the externally supplied formula agree. A rule-by-rule source-bound replay is indispensable.

F1. There exists a /386-admissible graph and binary charge vector with odd total parity whose complete original guarded SOURCE is SAT.
F2. The unchanged original CLI accepts an even-charge K4 SOURCE packet.
F3. A malicious RES signed pivot, false DEF facet, forged SOURCE clause, underpaid summary or unknown LOCAL-CONVERT opcode passes the original complete CLI.
F4. The independent 16-charge K4 SOURCE generator does not reproduce the seed's 17 signed native clauses or predicts the wrong SAT-model counts.

F1 is ruled out by the universal parity argument below. F2 and F3 were rejected by unchanged original-checker replay. F4 was excluded by signed-clause equality and 1,024 independently evaluated guarded assignments.

## Theorem 617.1 (known Tseitin parity; exact original /386 source-domain consequence)

For every graph with each edge appearing at exactly two vertices and every binary charge vector c with XOR of all charges 1, let F(G,c,g) consist of a positive unit guard clause (g) and, for every vertex v, all the four clauses that forbid each local triple assignment of incident edge variables with parity different from c_v, each extended by -g. Then F(G,c,g) is UNSAT.

**Proof.** Every model of F must set g=1. At each vertex, the four local forbidden patterns exclude exactly those triples with XOR not equal to c_v. Hence any model's edge bits x satisfy XOR_{e incident to v} x_e = c_v at every v. XOR all these equations over the graph. Each edge bit occurs exactly twice, so the left side is 0; the right side is XOR_v c_v = 1, contradiction. This holds for disconnected graphs as well and does not depend on any proof inference rule. QED.

The archived /386 parser enforces binary charges and their odd XOR before it checks SOURCE, DEF or RES. Thus, on every accepted in-band native source in this fixed fixture language, the UNSAT proposition is **already implied by the parser's permitted input shape**. That proposition alone therefore cannot authenticate RES, DEF, cost, or any absent mixed opcode. This is not a discovery of a new SAT lower bound: the underlying parity argument is classical. The research contribution is the **concrete original-code scope firewall and falsifiable audit requirement**, separating source-family validity from each inference step.

For **connected K4** with h=4 and E=6, all 16 binary charge vectors are covered by the stronger exact formula

\[
\#\mathrm{models}(F(G,c,g))=
\begin{cases}0,&\bigoplus_v c_v=1,\\
2^{E-h+1}=8,&\bigoplus_v c_v=0.
\end{cases}
\]

For a disconnected graph, the even-global-parity condition alone need not imply satisfiability; each component must have even charge parity. Do not universalize the K4 converse.

## Original-checker corpus and result

Pinned unchanged /386 checker: `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`. Pinned full certificate seed: `results/raw/arc/2026-11-11_0407_LSPV2_555_ACCEPTED_LIVE_DEF_RES_K1.json`, blob `aeeb555c4dcf7f510a9a501c8afc609b629a9298`. This original K4 specimen has 17 signed SOURCE records, 4 free DEF facet records, 3 once-paid gate owners, 30 RES nodes, 51 records total and fixed logical work W=33. The independently regenerated signed SOURCE multiset exactly matches the fixture.

Exhaustive finite source test: 16 charge vectors times 64 guarded edge assignments = **1,024** independent evaluations; all 8 odd charges gave 0 satisfying assignments and all 8 even charges gave exactly 8. The unchanged complete original CLI JavaScript source body then ran in hosted V8 on seven separate full packets: baseline ACCEPT with **3,509 original assertion groups plus 11 internal hostile tests**; six malicious packets REJECT (wrong RES pivot, wrong DEF facet, underpayment, wrong original SOURCE, unknown LOCAL-CONVERT opcode and even charge). **7/7 expected verdicts; zero unexpected.**

The only adapter modifications concerned virtual file I/O, output capture, `structuredClone` availability and an **output-only SHA digest**. This was an original-body hosted replay, **not an operating-system Node subprocess run**. A separate complete OS-Node reproduction script is published; it pins both exact Git blobs and uses actual disk/crypto/subprocesses but was not independently OS-executed here.

The exact consequence is narrow: "native accepted implies the source has zero models" is a tautological truth on this checker domain and must not substitute for checking a genuine local RES, DEF, parental chronology, global paid identity, or eventual mixed-rule interface. The malicious checks show the existing original /386 checker rejects the particular perturbations; they do not establish a complete historical R_mix341 grammar.

## Provenance, novelty and literature

This incorporates, rather than renames, the classical odd Tseitin theorem and the established /341 versus /386 dispatch separation from LSPV-3/607–608. It respects LSPV-3/609 and /615: the recovered **different** /341 checker accepts a SAT in-band source under certain malformed supports; a source-hash sidecar does not repair that flaw. LSPV-1/568 already gave the /386 source-bound K4 accepted proof, and LSPV-2/550 warned that source-unbound global-semantic MAY abstraction collapses. The new /617 contribution is a **source-domain falsifiability audit for the genuine original /386 body**, including all 16 binary K4 charge sources and hostile native opcode/facet/pivot probes. It does not claim priority for parity unsatisfiability or a novel inference rule.

Reviewed root proof1.txt (`06f7ebc8c2283304a0f5200b518c6e48fa41e343`), root proof2.txt (`930c5eeddafce656717f28055a7a9a755f44737c`, read by Git blob API because the 1MB file was blank via file API), issue #3 and latest comments, AGENTS.md, CODEX.md, project research SKILL.md, /616 five-role handoff, actual LSPV-3/539, /549, /556 and /607–616 plus relevant LSPV-1/568, /595 and /610, LSPV-2/550, /583, and LSPV-5/526. The latest Grok `GROKPROOF/2026-11-13_0526_PROGRESS.md` was checked as commentary, not native rule authority. No full mixed dispatcher emerged from original-program and branch/history searches.

Primary literature: Cook and Reckhow (1979), *The Relative Efficiency of Propositional Proof Systems*, *J. Symbolic Logic* 44:36–50, DOI https://doi.org/10.2307/2273702; Cousot and Cousot (1977), *Abstract Interpretation*, POPL, https://doi.org/10.1145/512950.512973. Neither source authenticates this repository's rule bytes. The odd Tseitin parity identity is standard algebra, not a novel result inferred from those articles.

## Implication and next action

P2-D1 must authenticate **local rule semantics and original-source binding separately**. A correct CEGAR abstract state must retain actual signed original-source provenance, typed parent DAG, charged owner identities, DEF facets, wire freshness and visibility, and active/discharged assumptions. Never conclude an operation's soundness by checking only that the *fixed promised source* is UNSAT. Retain all native accepted shortcuts and test each rule against a general source-based semantic obligation where the source may be satisfiable. Unknown full-R_mix341 steps remain a conservative MAY overapproximation until genuine source bytes or authoritative implementation are recovered. Do not exclude a candidate merely because neither sibling checker recognizes it.

Reference code: `experiments/arc/lspv3_617_native386_source_domain.cjs`. Hosted original-body raw ledger: `results/raw/arc/2026-11-13_0924_LSPV3_617_NATIVE386_SOURCE_DOMAIN_HOSTED_RAW.json`. Five-role handoff: `research/coordination/2026-11-13_0924_LSPV3_NATIVE386_SOURCE_DOMAIN617_FIVE_ROLE_HANDOFF.md`.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The mathematical tracker statuses and historical weights remain unchanged. All five existing research identities, Pacific schedules, ownership and TWO Route A / THREE Route B labels were left untouched. A private scheduler read confirmed that exactly the five current PNP roles are enabled on their existing America/Los_Angeles hourly schedules; older legacy PNP tasks remain disabled. No automation was created, duplicated, renamed, enabled or rescheduled. Repository-wide preflight and LaTeX compilation were not run in the hosted connector environment.

**P2-D1, P2-C3, P2-B1 OPEN; P2-B2/B3 separately OPEN; P versus NP OPEN.**
