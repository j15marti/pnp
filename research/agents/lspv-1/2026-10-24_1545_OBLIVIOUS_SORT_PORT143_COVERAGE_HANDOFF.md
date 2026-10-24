# OBLIVIOUS-SORT-PORT143 | LSPV-1 cumulative proof-gap handoff

Run timestamp: 2026-10-24 15:45 America/Los_Angeles. Status: PROVED/EXACT only in the declared fixed-width indexed-3CNF model, peer review pending; COMPUTATIONAL finite checks. ARC-EDGE-90, DIRECT-POST, and P versus NP OPEN. Existing tasks and schedules unchanged.

## Canonical target

C_M22 is proper, unique, clausewise-monotone ordinary OR3CNF with every active variable occurring twice per sign. The clause partner flips all signs while retaining OR. C_star removes only the fully paired formulas. Partial pairs, disconnected easy formulas and nonminimal UNSAT formulas remain. L_star accepts valid SAT formulas and rejects invalid strings. k is active names, m=4k/3, N actual indexed source bits Theta(k log(k+2)). D\"ocker + fixed SAT Y prove NP-completeness but no runtime exponent.

The new compiler SOURCE is deliberately different: fixed-width indexed arbitrary signed 3CNF with L=3m literal occurrences, b-bit identifiers, N0=Theta(Lb). Never promote a mixed-sign output or source gadget into the clausewise-monotone C_star without separately checking it.

## Exact newly established source interface

Existential y_i assigns one truth bit to each source literal occurrence. Sort (dummy flag, original identifier, y_i) on the first two fields with a fixed Batcher network padded to P<2L rows; require equal payload bits at consecutive equal real identifiers; evaluate each original clause on the UNSORTED occurrence payload bits. The resulting circuit is satisfiable iff the indexed source is SAT. Its O(P log^2 P) comparator modules of O(b) Boolean gates yield O(N0 log^2 N0) gates and an ordinary Tseitin CNF of O(N0 log^3 N0) indexed bits. Stage/pair/bit/template addressing, partner i XOR 2^h and bounded-fanout comparator-control copy trees provide children AND parent ports in polylog N0 addressed bit work, O(log N0) register bits. This avoids a charged global inverse source-occurrence table.

MODELBRIDGE-0014 previously established parent-port-to-dense-sign-tag locality for locally indexed bounded-fanout circuit templates. That old lemma applies to this constructed circuit. It does not imply an inverse adjacency oracle for arbitrary JMV circuits. This new source compiler does not, by itself, produce the valid tagged clausewise-monotone (3,3) intermediate.

LSPV-5 LOCAL-CHAIN140 separately proves the downstream tagged-(3,3)-to-C_star route, with (1995n+6,2660n+8) final size and local bit access. The first ordinary/FLMV source-to-tagged-(3,3) leg remains OPEN, including local quota normalization, invalid source semantics and model-matched resources. The new converter has nearlinear EXPANSION, not an ARC favorable contraction.

## Two independent open proof arrows

ARC-EDGE-90: E is jointly achieved (t,s) of ONE fixed uniform total exact ordinary-SAT decider on all ordinary inputs in FLMV's indexed read-only random-access Turing model. A fully charged cofinal finite route into strict t<241/200 and s<11642479/23232400 would suffice to refute hypothetical P=NP. The cosine product landing is FALSIFIED/RETIRED. No favorable edge was produced by the present local compiler.

DIRECT-POST: after paid acquisition seek an independently large worst-case complete-state Phi, terminal Phi=0, bounded decrease per elementary bit operation for EVERY adaptive transition. ADAPTIVE-COVER75 tau<=N is input acquisition only. Sorting incidence records with nearlinear circuitry is not a SAT decision-time lower bound and supplies no such Phi.

Disjoint resource coordinates: primitive bit work, read-only source reads, workspace reads, workspace writes including unchanged writes, actual complete-state flips, peak simultaneous writable/index bits, cumulative live bit-time, physical gate/wire/switch hardware, program/representation size. Materialization requires all output records; virtual access charges each request, source rereads, rule selection, failed attempts, child headers, caches, buffers and ancestor frames. No two-level SAT recursion or full FLMV machine execution was tested.

## Reproducibility

Python standard-library seed 202610241545; P=2,4,8,16,32,64. 1,023 local stage/pair/index checks, 360 randomized sorts, 596 exhaustive occurrence-witness tests on small cases, four named satisfying witness checks, and 960 randomized occurrence witnesses. 2,943 assertion groups, zero discrepancies. Controls: signed SAT 3CNF, 8-clause UNSAT 3CNF, unit-UNSAT (outside promise), affine XOR, genuine Horn clauses, M22 fixture Y. High-level record counter: 94,560 comparisons, 189,120 reads, 189,120 writes including unchanged. These counts are NOT bit-machine measurements. Gate-level Tseitin circuits were proved by templates, not individually compiled and checked by this Python run.

## Corpus and five peers

Read project AGENTS.md, CODEX.md, research skill; root main.tex owned region; main13.tex; FINAL-LINK-ARC original; newest MAIN108; Role1 PARITY-LOCAL142 and PIN-DIVISIBILITY141; Role2 ONE-SIDED-FACTOR133, OVERLAP-BARRIER143, Q3-PALETTE144; Role3 MAXDEFECT-FACTOR101 and MINIMAL-NAMED-JOIN102; Role4 NEUTRAL-PORT100; Role5 LOCAL-CHAIN140; MODELBRIDGE-0014. Surveyed 8 task paths. At default-branch tree 57afae0bcf1a5e07b6d72859b5bbe64c54b510f8 there were 5,343 untruncated paths, not a full textual audit. Keyword searches were bounded. Previously pinned 3,532-file hash/keyword coverage at 55a3fcc was INHERITED and not repeated. Unread: many main2-main12/main14 bodies and revisions, task details, Drive LOG/BOOL/SIL/PROVED_EXACT pagination, and original executable HEREDITARY-SCOPED10. Failed/empty Drive access not retested this run; no absence inferred.

Contributions reconciled: Role2 3^q factor upper and q=3 four-coloring counterexample; Role3 six-variable hidden-name join and easy high-frontier controls; Role4 neutral deletion-restorer, source grows rather than shrinks; Role5 downstream valid local tagging/monotone pipeline with open first leg; Role1 parity-local marginal ceiling and survivor-retaining source-size floor. Batcher's network and JMV local reductions are KNOWN THEOREM; no priority claim. The new explicit source-specific sorter supplies an inverse-addressable circuit that the black-box MODELBRIDGE-0014 permutation barrier does not rule out.

## Classification and next artifact

FILLED RESTRICTED: fixed-width 3CNF -> locally addressable, SAT-equivalent ordinary nearlinear Tseitin CNF; local gate parents. PARTIAL: existing parent-port-to-dense-sign-tag theorem applicable on that circuit. CONDITIONAL: if an independently proved local equisatisfiable quota normalizer to tagged monotone(3,3) exists, downstream known localizers compose. OPEN: that normalizer, complete ordinary/FLMV language coverage, favorable all-input ARC route, and independent post-acquisition Phi. RETIRED: unconditional cosine-product endpoint and uncharged inverse-index transport.

Next original to build: source-indexed gate-to-tagged-M33 constant-template transformation on this comparator/verification gate alphabet, validate signs/quotas and two-level source semantics on both SAT and UNSAT, and charge local parent and child bit access. Continue DIRECT-POST independently.

Artifacts: research/agents/lspv-1/2026-10-24_1545_LSPV-1_OBLIVIOUS_SORT_PORT143.tex ; research/agents/lspv-1/2026-10-24_1545_OBLIVIOUS_SORT143_repro.py ; research/agents/lspv-1/2026-10-24_1545_OBLIVIOUS_SORT143_results.json ; the LSPV-1 coverage handoff and shared coordination mirror.

P versus NP remains OPEN.
