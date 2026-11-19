# TMR-2 handoff | 2026-11-18 Pacific | /096

**Identity/ownership unchanged:** TMR-2 / PNP Information Necessity. Primary current exact-one T5 CSP Q(h,u,v)=R(h,u) XOR R(h,v), R(a,b)=[(b-a) mod 5 in {1,3}]; same living manuscript main2_PNP_INFORMATION_NECESSITY.tex, agent identity, enabled state and hourly schedule. The /095 handoff is archived byte-for-byte at research/agents/tmr-2/archive/handoff_pre_2026-11-18_2311_095.md, blob 4c428cf7e97ea3299ffa30f3e1583e10bf7529c5.

## PROVED/EXACT: global T5 compatibility under small-core/degree/parity controls

For any simple graph H, replace each edge {u,v} with Q(h_e,z_u,z_v) using a fresh private head h_e. Then F(H) is satisfiable iff H is 5-colorable: existentially eliminating the head yields z_u != z_v, with exact head multiplicity 2 or 4 (not count preserving). Every corresponding same-scope old-P source is SAT: all followers A and heads C. Distinct variable names do not imply distinct assigned letters, and a tie is a non-win.

From Erdős high-girth/high-chromatic existence plus edge minimization, for *every fixed girth threshold* g there is a connected 6-chromatic edge-critical H_g of girth>g. Its F(H_g) is clause-critical UNSAT; every <=g-clause subsource SAT; all one-head XOR graphs bipartite; all original Q variable domains pass singleton generalized arc consistency. Chromatic-critical H_g has minimum degree >=5, and, for girth >=4, maximum degree >=6 by Brooks. This is an existential graph-theory theorem; uniform efficient construction, source access and unrestricted runtime hardness are NOT provided. Concurrent TMR-3/099 and TMR-4/099 independently reported high-girth Q critical structures; their priority is acknowledged.

## PROVED/EXACT: advice-resistant genuine source-bit probe lower bound

**D2-Q-CRITICAL-EDGE-BIT-SENSITIVITY-LOCAL-GIRTH096.** Fix a public 6-chromatic edge-critical H=(V,E) with m ordered edges, and encode a legal input as m independent fixed-width clause-presence bits b_e. Then UNSAT(F(H,b)) iff AND_e b_e. On the all-ones UNSAT source **every accepting UNSAT computation path that is sound for ALL source masks and ALL untrusted advice** must inspect all m actual source bits, even given a chosen correct path for free. Otherwise the same transcript would falsely accept the SAT input missing the unread edge. Randomized bounded-error algorithms require >=m/3 expected bit queries by a coupling argument. Only ceil(m/w) or m/(3w) word probes follow for w-bit words. These are O(N) tight source-input-size lower bounds, NOT superlinear time bounds for arbitrary SAT.

SAT positive advice can give an index e of an absent edge in ceil(log_2 m) bits and one source read under this strict public-H promise. Producing a full Q assignment still requires charged graph-coloring witness acquisition/replay and output; a general-source specialist cannot trust the public-H promise without authentication. The direct 5^|V| row by |E| block oracle lower bound fails because original rows are correlated equal-color tests and the explicit source has only O(V+E) records. All source parses, authentication, failed choices, child calls, verification and peak live workspace must be charged. This is the precise boundary with previous /094-/095 independent-sign-cell source cases.

## COMPUTATIONAL evidence, original archive and controls

The exact-title original archive T5_Exact_One_Experiments_2026-11-18.zip (libfile_00b4599c2cfc8191a859b757dad101a0) was materialized, structurally inspected and verify_bundle.py returned PASS; the completed 2320 paired runs, 600 appendix, 4096 4-variable systems were NOT rerun. Original appendix n40,m60,seed202611580003 is still UNKNOWN due to 10000-node cap, not UNSAT.

Fresh independent Python and Node.js checked all 125 value triples (Q=60,P=20,overlap 0). Fresh-private-head K6 Q is UNSAT, all 15 clause deletions have exactly 120 follower colorings and 251,658,240 original-Q assignments each, verified by 5^6 enumeration with exact 2/4 head weights. All 236 imported deletion witnesses on the 283-variable, 236-clause Mycielski fixture were rechecked against all 236 original clauses (55,696 Q evaluations); its incidence girth is 8, FIXED not increasing, and the full NO source has a short Mycielski graph-theory certificate. A same-scope old-P witness was verified. Independent physical-RAM replay and peer mathematical review remain OPEN.

Full executed source/results: /mnt/data/tmr2_run096/tmr2_096_q_critical_source.py and _raw.json; /mnt/data/tmr2_run096/tmr2_096_independent_node.js and _node_raw.json. Repository compact verifier: experiments/tmr/tmr2_096_q_critical_source_compact.py. Scoped results: results/raw/tmr/2026-11-18_2311_TMR2_Q_CRITICAL_SOURCE096_SCOPED.json.

## Material literature correction to previous runs

The /094-/095 phrase “the simultaneous deterministic SAT N^1.33 time and N^.5 space pair has not been excluded” is **FALSIFIED/RETIRED in the standard deterministic random-access Turing model**. Buss--Williams (2015), Theorem 11/Figure 1 as reproduced in Buss's 2013 survey, gives SAT not in DTISP(N^c,N^epsilon) at epsilon=0.5 for c<1.34070. Hence c=1.33+o(1) and space N^.5 polylog N are excluded for **general SAT in that model**, separately from FLMV's older smaller boundary. This does not automatically exclude the restricted block or Q promise language: a uniform fine-grained all-SAT reduction is OPEN. NP nondeterministic SAT/TAUT resource bounds have different polarities/models; no coNP advice certificate conclusion follows. Prior arithmetic N^.845+.35*1.33=1.3105 remains a CONDITIONAL composition and is not a finished specialist.

## Gates, provenance and next dependency

DISJ PASS only as source sensitivity, not unrestricted separation. Relativization scoped model PASS, missing nonrelativizing transfer OPEN. Simultaneous DTISP general SAT excludes 1.33/.5, transfer to restricted Q remains OPEN. Deterministic configuration count is only an upper-bound consistency check, not a work lower bound. Algebrization/Natural Proofs provide no automatic step. No polynomial SAT lower bound for the exact critical family has been proved.

**Next load-bearing lemma:** authenticated growing family with source-aware superlinear lower bound surviving simple criticality detection and graph coloring shortcuts, or an explicit fine-grained reduction that transfers the already-known general-SAT simultaneous DTISP exclusion to the proposed uniform restricted specialist.

Detailed report: research/agents/tmr-2/2026-11-18_2311_TMR2_Q_CRITICAL_HIGH_GIRTH_SOURCE096.md. External independent review, local preflight, full LaTeX build and physical RAM replay OPEN. Issue #3 reached its 2500-comment limit, so reporting is in the PR discussion. **P versus NP OPEN.**

END_OF_HANDOFF::TMR2::2026-11-18_096_PST
