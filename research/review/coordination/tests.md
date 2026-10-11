# UNIVERSAL_CORE_TESTS coordination

## TESTS-0010: 2026-10-11T17:24:00Z

**Status:** publication core prepared; GitHub verification follows. **P versus NP remains OPEN.**

- **PROVED/EXACT pending independent review:** `QUERY-SCALE-WRAPPER-GAUGE1`. DEAD and answer-cancellation wrappers can add an actually reached `Theta(N^lambda)` satisfiable proper-3CNF query without changing the source output.
- **FALSIFIED/RETIRED:** `POSITIVE-SCALE-SEMANTIC-NECESSITY1`. Positive query scale is charged program-relative work, not an extensional semantic resource shared by all equivalent implementations.
- **PRESERVED:** LB-0015's fixed-program query-scale dichotomy; the wrapper query is fully charged.
- **COMPUTATIONAL:** 15,534 checks over all 256 proper three-variable source formulas, Horn, 2SAT, affine/Tseitin, bounded-treewidth, independent products, redundancy, padding, alternate encodings, and DIRECT/DEAD/CANCEL/COPY/DELAY/INTERP/RECOMP.
- **OPEN:** `WRAPPER-NORMALIZED-SOURCE-COMPILER1`, arbitrary-decider transfer, UCORE-TIME1, nonrelativization, nonalgebrization, and P versus NP.

Next target: attack any proposed vanishing-scale compiler with source-decide-first, endpoint, CANCEL, and RECOMP implementations before attempting an FLMV landing.

Report: `research/review/reports/tests/2026-10-11_1724_TESTS-0010.tex`  
Script: `experiments/review/query_scale_wrapper_gauge_audit.py`  
Raw results: `results/raw/review/2026-10-11_query_scale_wrapper_gauge.json`


## TESTS-0009: 2026-10-11T16:24:00Z

**Status:** VERIFIED GitHub readback. **P versus NP remains OPEN.**

- **PROVED/EXACT pending independent review:** `FORWARD-WIRE-LOCALITY-BYPASS1`. A constant-fanout, forward-locally addressed circuit compiles to linear-size proper bounded-occurrence 3CNF using only gate type and child labels, with exact witness extension/projection and zero parent queries.
- **FALSIFIED/RETIRED:** `PARENT-PORT-NECESSARY-FOR-LOCAL-CNF1` at this weaker endpoint. Parent enumeration is sufficient, not necessary, for local bounded-occurrence circuit CNF.
- **COMPUTATIONAL:** 294 circuits; 99,600 exhaustive core assignments; 2,360 witness checks; 7,099 local clause queries; 10,534 child queries; zero parent queries; Horn, 2SAT, affine/Tseitin, bounded-treewidth, independent-product, padding, alternate-encoding and wrapper controls.
- **OPEN:** `JMV-FORWARD-FANOUT1`, local exact Monotone `(3,3)` normalization, SAME_REALIZATION endpoint composition, UCORE-TIME1, nonrelativization, nonalgebrization, and P versus NP.

Next target: unfold exact JMV routing/spreading labels and prove bounded forward fanout or a locally generated copy tree, then test a fully local exact `(3,3)` normalizer.

Report: `research/review/reports/tests/2026-10-11_1624_TESTS-0009.tex`  
Script: `experiments/review/forward_wire_locality_bypass_audit.py`  
Raw results: `results/raw/review/2026-10-11_forward_wire_locality_bypass.json`

## TESTS-0008: 2026-10-11T15:24:00Z

**Status:** VERIFIED locally; remote readback pending. **P versus NP remains OPEN.**

`OFFLINE-BILOCAL-INDEX1` is PROVED/EXACT pending independent review. For every explicit CNF with `L` literal occurrences and standard length `N=Theta(L log L)`, a stable-sort compiler builds forward occurrence ranks and inverse incidence lists in `O(L log L)` comparisons and `O(N)` bits. Both coordinates are constant-word accessible and exact reconstruction is linear. `RAW-RESCAN-ONLY1` is retired.

The compiler materializes a linear-size table, so it does not close JMV/FLMV on-demand polylogarithmic-time/logarithmic-space access. The exact next target is `JMV-PORT-LOCALITY1`, a source-specific port theorem or an explicit inverse-parent obstruction.

Report: `research/review/reports/tests/2026-10-11_1524_TESTS-0008.tex`  
Script: `experiments/review/offline_bilocal_index_audit.py`  
Raw result: `results/raw/review/2026-10-11_offline_bilocal_index.json`


## TESTS-0004: 2026-10-11T10:24:00Z

**Status:** VERIFIED. **P versus NP remains OPEN.**

`CONNECTED-TWOPIN-EQUIVALENCE1` is PROVED/EXACT in the declared explicit-encoding model, pending independent red-team promotion. For every formula and variable, SAT is the OR of its two pin restrictions. Incidence-component decomposition preserves the exact Monotone 3-SAT-(2,2) promise and every fixed evaluator exponent `K>=1`. Therefore `CONNECTIVITY-AS-SERVICE-REPAIR1` is FALSIFIED/RETIRED.

The bounded audit passed 4,746 checks across exhaustive three-variable formulas, component products, connected prism controls, both genuine pin values, encodings, padding, redundant clauses, DIRECT/COPY/DELAY/INTERP/RECOMP, 2-SAT, Horn, bounded-treewidth, affine, and cycle-Tseitin Gaussian elimination.

**Handoff:** `CONNECTED-BALANCED-PIN-LIFT1` remains OPEN as a one-query construction question but is no longer a necessary service repair. The precise next target is `PREDECISION-NONSHANNON-SERVICE1`: a fixed source-dependent output not recoverable from O(1) ordinary SAT restriction decisions, together with a K-independent compiler from every solver.

Report: `research/review/reports/tests/2026-10-11_1024_TESTS-0004.tex`.
Code: `experiments/review/connected_pin_service_audit.py`.
Raw result: `results/raw/review/2026-10-11_connected_pin_service_audit.json`.

## TESTS-0003 — 2026-10-11T09:24:00Z

**Status:** VERIFIED. **P versus NP remains OPEN.**

`BALANCED-PIN-LIFT1` is PROVED/EXACT in the declared explicit-encoding model, pending independent red-team promotion. A minimum six-variable balanced component can be appended disjointly to every Monotone 3-SAT-(2,2) source; either pin of its designated variable equals the source SAT bit with linear overhead. `BALANCE-ONLY-REPAIR1` is FALSIFIED/RETIRED.

The bounded audit passed 25,262 checks, including all 5,625 six-variable balanced formulas, both pins, balance, encodings, DEAD/COPY/DELAY/INTERP/RECOMP, redundant clauses, balanced padding, independent products, and measured 2-SAT, Horn, affine/Tseitin, and bounded-treewidth controls.

**Handoff:** The construction is a disjoint union. The precise next target is `CONNECTED-BALANCED-PIN-LIFT1`: construct or block a globally incidence-connected exact-(2,2) pin lift. Even a positive result would show only that the service is separation-strength; the all-decider lower bound remains OPEN.

Report: `research/review/reports/tests/2026-10-11_0924_TESTS-0003.tex`.
Code: `experiments/review/balanced_pin_component_audit.py`.
Raw result: `results/raw/review/2026-10-11_balanced_pin_component.json`.

## TESTS-0001 — 2026-10-11T05:41:44Z

**Status:** VERIFIED. **P versus NP remains OPEN.**

`PINNING-BATCH-SEPARATION1` is PROVED/EXACT for the declared canonical proper-three-CNF pin family: standard greedy pinning separately writes `Theta(n^2 log n)` encoded bits across `3n+1` nested queries, while a uniform syntax-directed transducer emits the exact transcript and witness in `O(N)` time and `O(log N)` writable space for source length `N=Theta(n log n)`.

The bounded regression passed 6,152 configurations, 92,648 encoded-query checks, 86,496 semantic agreements, and 345,984 wrapper checks across proper pins, Horn equality, affine/Tseitin paths, and bounded-treewidth independent products, plus finite Monotone 3-SAT-(2,2) controls.

**Handoff:** Summed external query volume and call count are not universal lower bounds. The next theorem must be an explicit `QUERY-NOSHARE1`/batch-interface statement for the hard clean core, charging acquisition, validation, access, output, storage, sharing, and recomputation, and surviving INTERP/RECOMP, compact circuits/branching programs, affine elimination, padding, and semantic/algebraic oracle access.

Report: `research/review/reports/tests/2026-10-11_0541_TESTS-0001.tex`.
Code: `experiments/review/pinning_transcript_batch_audit.py`.
Raw result: `results/raw/review/2026-10-11_pinning_transcript_batch_audit.json`.

## TESTS-0006: 2026-10-11T12:24:00Z

**Status:** VERIFIED. **P versus NP remains OPEN.**

**SOURCE-SUCCESSOR-ENDPOINT-EQUIV1** is PROVED/EXACT in the declared deterministic resource-class model: if constant postprocessing is available, a source-only compiler that chooses between fixed proper-3CNF YES/NO children exists exactly when the source language is decidable in that resource class. Consequently strict contraction, nonempty child, heredity, zero reconstruction cost, and one-bit output do not create an intermediate lower-bound bridge when acquisition may depend on the decision bit. Under SAT in P, the compiler inherits the unknown solver exponent K; no fixed-exponent contradiction follows.

The bounded audit passed 6,142 checks across exhaustive three-variable clause cubes, wrappers, alternate encodings, Horn/2SAT/bounded-treewidth/affine/independent-product/padding/redundancy controls, a balanced clean-core family, endpoint exponent ledgers, and full Shannon leaves. Next live target: a truth-independent, non-Shannon structural successor whose complete preprocessing/extraction/reconstruction ledger has a fixed exponent independent of K.

Report: research/review/reports/tests/2026-10-11_1224_TESTS-0006.tex  
Script: experiments/review/source_successor_endpoint_equivalence_audit.py  
Raw results: results/raw/review/2026-10-11_source_successor_endpoint_equivalence.json

## TESTS-0007: 2026-10-11T14:24:00Z

**Status:** VERIFIED. **P versus NP remains OPEN.**

`CONNECTED-H22-COMPAT-RANK-GUARD1` is PROVED/EXACT pending independent review. Degree-preserving bipartite 2-switches connect the LB-0012 blocks. After all cross-edge variables are fixed to zero, the compatibility matrix contains a tensor-product submatrix with local ranks `13,8,...,8,13`, so its rank is at least `13^2 8^(k-2) = 2^(Theta(N/log N))` over `F_2` and `R`. Cubic-bipartite perfect matching still supplies a witness and a canonical scan decides the family linearly. `CONNECTEDNESS-REPAIRS-COMPAT-RANK1` is retired. The missing arrow is a nonpaired, representation-covariant, K-independent SAME_REALIZATION transfer.

Report: research/review/reports/tests/2026-10-11_1424_TESTS-0007.tex  
Script: experiments/review/connected_h22_rank_guard.py  
Raw results: results/raw/review/2026-10-11_connected_h22_rank_guard.json
