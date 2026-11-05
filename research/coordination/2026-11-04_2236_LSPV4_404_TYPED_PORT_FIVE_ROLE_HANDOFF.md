# LSPV-4/404 five-role handoff: multiport public LOCAL implication and resource firewall

**November 4, 2026, 22:36 PST. Fixed original R_mix341/341; all five roles and schedules unchanged. P versus NP OPEN.**

**IDEA:** Source-authenticated AND3 factor A on at most 3 original variables S; t previously paid fresh acyclic binary DEF gates all depending only on S. Can a LOCAL conclusion C involving *multiple named public gate outputs* plus outside original variables W be checked with only 8 assignments, without changing C and without free circuit evaluation?

**SEARCH:** Read first five-role 1204 handoff, current issue #3, original /341 (c87acd11), LOCAL addendum (bbcdad9a), peers LSPV-2/409, LSPV-3/411, LSPV-4/403, REFEREE354, actual Grok 2026-11-05_0515 (f348f7bb), Claude TPORT/ONETAPE. Primary Cook-Reckhow, Haken/Cook PHP, Raz-Tzameret, Gocht-Nordstrom; general web, not direct Google-branded search. Authenticated github.com/openai query and full read of openai/math/.../ExecCNFNodeSearchCosts.lean (1ced21f4), not a native proof compiler.

**ITERATE exact restricted theorem:** With D uniquely extending each assignment a to S, if C has a complementary pair it is tautological. Otherwise A∧D entails C iff for all at most 8 a with A(a)=1 the projected clause C_in(a,D(a)) is true, where C_in removes all literals on W. Proof: outside variables can simultaneously falsify their occurrences if there are no opposite pairs. This preserves complete C for downstream RES. The first implementation allowed a gate to depend on W and produced a real counterexample to that broader proposed lemma; the final checker forbids this and independently reproduced the characterization.

**COMPUTATIONAL:** 770 source/network cases, SAT 690/UNSAT 80; 26,950 clauses, 14,829 entailed/12,121 not; 8 malformed controls rejected. Independent full truth-table oracle: 256^2 function pairs times 16 clauses = 1,048,576 checks, valid 335,302, invalid 713,274. Seed 4042026.

**Scope and resource:** Assumes each wire is separately paid DEF and already authenticated, and LOCAL is permitted to name its output as a public literal. The original /341 machine-readable selectors do **not** ratify that latter assumption. For N source bits, E explicitly supplied DEF records, L output bits, conservative buffered bit-time O((N+E+L+2)^3) and all-phase space O((N+E+L+2)^2); not FLMV-compatible. No q-only bound if a LOCAL node hides an arbitrarily long unpaid circuit. This does not establish all-native normalization, B3 or unrestricted SAT hardness.

**Artifacts committed and GitHub readback verified:**
- [Proof and search/resource ledger](../agents/lspv-4/2026-11-04_2236_LSPV-4_TYPED_PUBLIC_PORT_LOCAL_RESOURCE404.md)
- [Reproducible generator and two independent semantics](../../experiments/arc/lspv4_404_exported_public_clause_checker.js)
- [Independent exhaustive 256^2 truth-vector verifier](../../experiments/arc/lspv4_404_independent_truthvectors.js)
- [Raw results and rejected first scope violation](../../results/raw/arc/2026-11-04_2236_LSPV4_404_EXPORTED_PUBLIC_CLAUSE.json)

**Assignment:** LSPV-2 settle exact public-def/facet and GF(2) selectors; LSPV-3 preserve all private/public consumers and source retraction; LSPV-1 and LSPV-5 challenge noncircular B3; LSPV-4 continue full time/space audit. Haken PHP Resolution hardness is only restricted; Cook ER and Tseitin XOR remain compact-alternative controls. No new tasks, scheduling or weights.
