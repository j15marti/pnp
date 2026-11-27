# T4-02 | Global queue credit and cross-gauge certificate transport
2026-11-27 Pacific. Cooperative Proof Synthesis. PROVED WITH SCOPE (local derivations, independent implementations; peer review requested); COMPUTATIONAL for benchmark traces. P versus NP OPEN.

## Source and objective
STRICT-EB4-v1: finite simple signed four-regular graph, four distinct incident ports per vertex; E means all equal, B means integer weight two, edge means XOR sign. No geometry promise or free pins. RT01 e71b388635cd817b4fd3f641a3ab938ccdca906c (blob e9e0df120353a909d4d43aecc1c045d1fdc22f98) reviewed: 3SAT -> anchored NAE4 -> two NAE3 -> B4 with unique slack -> duplicate for even fanout -> E paths -> private K5-minus-edge wire gadgets. Both directions and complement symmetry follow as described. For the common compiler the long-clause split is existentially equivalent. NP completeness is for strict source, not a narrower geometric variant.

Read pinned directives shared EB 869007811cfe4a6b703e7f111111b820f3afcb03, shared UNSAT b1e93ffb3f7698009554e3a6fe19c20e0d06067a, identifiers 67fe81e50ce5c54a67966d5dda1bb0843b84da3c, registry 0c14cdc57925788cf7a451dcd5aa171dce860f2c, public release fc87c43ad1a247e4133b931911f7cfa4afeb17c0; recovered AGENTS, CODEX and research skill via connector (long combined display truncated). Issue 328 newest comments read before source, peer replay, and publication. No local checkout (git network DNS unavailable); preflight not run. Additive role-owned report; no legacy manuscript overwrite or scheduler mutation.

Exact primary data: compiler 21b9d53fb8166c819b24e708656c742cd3c24f10, corpus e315349cd6c1fe3fa696504859f28312f6aab69a. Executed pinned compile function in JS isolate. SHA-256 recomputed, standard abc vector checked, both registry bytes, CNFs and map hashes match. Native source-only methods do not consult map or reference labels. CNF comparator separate, no reference proof imported as free solver advice.

| Instance | Full native SHA256 | N bits | CNF SHA256 | CNF N |
|---|---|---:|---|---:|
| EB-JOINT-24@e84a0ab6dc6f | e84a0ab6dc6f74deb8daeea2ccd41cca90e3d1294411877a813471760897c209 | 5363624 | 68d21d234f32956200617b3a714d9f81f992cf2fa373f1285d639d6a703fa22b | 13416 |
| EB-RANDOM-3CNF-40@8a18e86479df | 8a18e86479df916ea5c7fdd760ccd561e4fea3737a94517ab8dc2d28cc7e6bdb | 5027816 | cfaccaa692ef736e2b5eaadde2eda83ca7351e30cf066237fbe5c63eedb55e67 | 17480 |

Map SHA256 JOINT dd44a7eee2ade0cb42bf9e29c08bd1bc96dad43dfe2a5e06b02f1d09fd97c998; RANDOM 3a3dc143d60bd7b6b2f2d17b1eaa32ccdb2d3613d23d68489c48abd40ca219c3. Model IDs STRICT-EB4-v1 and DIMACS-CNF-v1; full ID is model:sha256:digest. Root certificates guard EMPTY and residual ROOT; original IDs all vertices, ports and edges in their original indexed ranges as recorded in certificates. Internally a BFS signed equality component has canonical minimum port and offset bit; CNF variable is minimum port +1. Every port has a reverse expression in its representative. Global complement preserves all native constraints, so port 0=0 is an exact symmetry quotient, not an arbitrary assumption about witnesses. For T3 parent gauge, carrier 11=0 is different and not silently equated.

## Named obligation: queue credit with all failed discovery
For any finite explicit Boolean factor system of n appearing carriers and m factors of scopes at most k, choose deterministic queue scheduling. Only consider an exact elimination if full incident bucket union contains at most k carriers. Replace ALL incident factors by their joint existential projection eliminating x; output scope at most k-1. A tautology may be discarded; identical factors may be deduplicated. If contradiction, stop; if no candidate, stop UNKNOWN unless an independently correct terminal applies. Each retained projected row has at least one extension in the exact original bucket, giving reverse reconstruction by testing two values in reverse elimination order. Gauge transformation and signed equality have separate reverse maps. No semantic oracle.

Let Q be number of queued distinct candidates, I number of live factor/carrier incidences, e number of eliminated carriers; n is initial count. Define
  Phi = Q + I + (2k+1)(n-e).
Initialization Phi <= n+km+(2k+1)n after preprocessing/gauge insertion. At every pop, Q decreases 1. A failed or stale candidate changes nothing else. Deleting factors with t incidences can requeue at most t distinct candidates and reduces I by t. Adding at most one projected factor of scope s<=k-1 changes I+Q by at most 2s. On a successful elimination n-e decreases 1. Therefore every nonterminal pop decreases Phi by >=1 (successful pops by >=4). If a contradiction is found, retire the entire obligation. Duplicate/tautology discards only improve bound. Phi is nonnegative integer, numeric O(k(m+n)); no per-pop replenishment of global credit. A queued candidate need only be reconsidered if some incident factor changed. Queue exhaustion certifies no permitted bucket operation remains under the chosen exact width test, NOT infeasibility. A terminal or another productive operation is needed.

A conservative deterministic implementation may use sorted lists and explicit row membership scans, so each pop costs poly(N,k)4^k bit operations (including indexing, failed scans, local tables, trace, checking); number of factors never increases after initialization, and each factor has <=2^k rows. Thus the queue stage is polynomial for k <= c log_2 N with fixed c. Independently rechecking complete bucket rows and retaining reverse maps also costs poly(N,k)4^k. Initial authentication, signed normalization, reverse maps, physical sharing and verification are paid. Uniform bit strings, exact integer addresses and deterministic operations suffice. JS benchmark code uses small exact bit masks and bounded input lengths; arbitrary k and N require bit arrays and a standard full-length SHA library rather than the experimental 32-bit shifts and short-input hash.

## Global branch credit, conditional terminal only
A fixed depth limit d allows B(d)=2^(d+1)-1 structural jobs. B(d)=1+2B(d-1); retire parent allocation and distribute both child allocations. Assign a fixed per-job polynomial budget R(N) for closure, failed probes, switching and proof checking. Reserve all of it up front, independently of the queue-stage credit; include a fixed number of replicas/imports in R and do not reset the allowance on child states. If a terminal cannot be obtained before a budget or depth cap, return UNKNOWN. For k,d=O(log N) with fixed constants this is a uniform polynomial partial decision/refutation procedure, not universal coverage. A satisfying residual lifts via reverse maps; sound NO via all closed leaves. Only a proved bound for EVERY NO input would permit interpreting timeout as YES. Bounds on full bit-time are analytic, not measured. A conservative same-run bound poly(N,k)4^k * 2^d includes explicit checking and all branch nodes; memory can store full traces of polynomial size under the cap, and cumulative memory is bounded by peak storage times total bit-time. A branch proof supplied after discovery is not acquisition for free.

## Executed independent lanes and integrated result
All executed sequentially on copies of same authenticated native bytes. Initial exact signed normalization, local coordinate-support forced closure (lane A), all exact bucket factors (lane B), separate direct CNF DPLL (lane C, provenance-side comparator). Lane A and naive full-scan bucket hybrid both UNKNOWN at 2.5M instrumented events per lane per case. This is certified finite stagnation relative to the cap, not hardness. Source-only queue-based contraction used no peer certificate. Independent full-scan row checker enumerated output assignments and both values of eliminated bit; separate CNF tree checker reconstructs unit propagation from original projected CNF and checks both branches. Native independent replay of T3 performed only after solo discovery. Closure replayed at root after import batch; not live after every individual bucket/peer clause. No claim that run fully implements all desired closure schedules.

| Counter | JOINT | RANDOM |
|---|---:|---:|
| original B factors | 788 | 736 |
| initial normalized carriers | 643 | 593 |
| A local support scan events (UNKNOWN) | 2500006 | 2500002 |
| B naive bucket scan events (UNKNOWN) | 2500001 | 2500002 |
| C original CNF scans, UNSAT | 4714 | 18975 |
| C branch jobs | 41 | 63 |
| incremental candidate/row events | 31153 | 34413 |
| eliminated carriers | 591 | 552 |
| retained implementation factors | 172 | 185 |
| peak live factor count | 395 | 369 |
| full-scan exact bucket checks | 12463 | 14536 |
| exact projected checker CNF clauses | 395 | 369 |
| source-only branch jobs | 43 | 119 |
| source-only max branch depth | 13 | 12 |
| solo discovery clause scans | 11744 | 36133 |
| solo checker clause scans | 26157 | 80317 |
| queue pops | 1535 | 1411 |
| failed or stale pops | 944 | 859 |
| Phi initial | 9293 | 8589 |
| Phi final (queue empty) | 1128 | 1188 |
| minimum observed decrease | 1 | 1 |

Both exact independent refutations returned UNSAT. Potential instrumented by recomputation before and after every pop on separately repeated execution, verifying same elimination trace. Extra instrumentation scans, parsing, hash, graph construction, original source/peer map and certificate reads, allocation, sorting, row comparison inner costs and I/O are unmetered separately; heterogeneous primary events are not interchangeable bit clocks. Earlier failed lanes and all repetitions are paid, not ignored. Code and raw traces below record counts, not full physical cost. No end-to-end speedup claim; no common bit-clock across tracks. Source-only actual artifact sizes 22195 and 24325 bytes; hybrid 22897 and 25447. Peak recorded factor count is not physical memory measurement.

## Complementary hybrid: cross-gauge clause transport
Independently replayed T3 JOINT and RANDOM exact incident bucket traces, local factor entailment of base clauses and all RUP steps including final empty clause. No need for full prime-implicate completeness for sound negative proof. Parent proofs verified, but only nonempty clauses in first half with all involved carriers and anchor live were imported, not the final empty clause. For a native complement-invariant relation F, if F AND g=0 entails C, then F AND g=1 entails bar(C) where every literal is complemented: apply global complement to any model with g=1. Thus F entails both (g OR C) and (!g OR bar(C)). This is a genuinely unconditional source consequence; different gauge representations are not silently merged. Exact existential projection preserves any consequence involving only live coordinates. Check every literal and gauge in residual, then reclose. T1 same-gauge import in #7225821446/#7225821956 complements this result. No free inverse compiler needed.

| Counter | JOINT | RANDOM |
|---|---:|---:|
| T3 bucket steps | 614 | 552 |
| T3 independent projection checks | 13948 | 12328 |
| T3 independent local entailment row checks | 4886 | 5167 |
| T3 independent RUP scans | 10253 | 41490 |
| nonempty imported parent clauses | 5 | 25 |
| resulting unconditional clauses | 10 | 50 |
| hybrid branch jobs | 3 | 31 |
| hybrid discovery clause scans | 2718 | 11112 |
| hybrid independent checker scans | 2371 | 25782 |

Replayed false root-leaf certificates rejected on both controls. Hybrid source-parent links in artifacts; parent replay and communication cost cannot be omitted. The decrease in terminal search work is not a reduction in fully charged work once proof acquisition/replay is included. Parent proof is already a complete independent contradiction: hybrid is a representation/transport experiment, not new decision coverage. All standalone and hybrid tree searches used the same 2.5M clause-scan cap.

## Secondary MFC-13 audit
After primary cases, independently reconstructed T2 atom from certificate b70ec35dfee5f4b7d465dfcc650e301cef0384e2, digest e8cb93975de906ca732db671a523b43f1007ab729a301738070eae0a1aee2b06; source bytes SHA 09605e18791f9bc666d42fd56f6d4a02c84ee3aa2864cf4aca56962966ccdeb5, N=544, model MFC13-PLANE-LIST-v1. Enumerated all 1024 coefficient words, 243 nonzero-plane words, 3888 mask/fiber comparisons, all 16 quotient classes and 128 affine predictors/class. Verified distribution (forced syndromes,predictors)=(63,1):1,(11,0):9,(4,8):6; unique unattained target 29. This independently confirms T2's refusal of a global affine predictor on nine response classes, not a general lower bound. No new reciprocal-lift, Nov26 replay or CHARGED-UNSAT-TRANSPORT1 experiment this run; prior T4 report remains historical. No unverified import. 

## Source search and barriers
Queries used: SAT bounded variable elimination resolution proof logging Een Biere effective preprocessing Davis Putnam; SAT proof checking RUP DRAT LRAT bounded variable elimination proof complexity resolution width; Ben Sasson Wigderson short proofs narrow proofs resolution width lower bound original paper; site:github.com/arminbiere/cadical elim.cpp bounded variable elimination; site:github.com/anthropics/formal-math VP VNP Statement Lean; site:github.com/openai/math 379 VP VNP; site:github.com/xai-org SAT solver formal proof; site:github.com/google-research SAT proof solver; site:github.com/google-deepmind SAT proof formal mathematics solver; site:github.com/google/or-tools SAT presolve; site:github.com/google-deepmind formal theorem proving alphaproof code; site:github.com P versus NP formalization SAT proof checker cadical lean. Repository search j15marti/pnp 'bucket credit', 'T3_rup_replay' (no results), branch query T4 returned five ccr branches, not deep inspected; issue 328 latest inspected at relevant points. Failed local git DNS; missing guessed helper path at pin 5214a4fa84961675b8f44d68b106603a938a4b57 (404), replaced by actual peer artifacts. No matching xAI/Google Research repository implementation identified by bounded search; no dependency inferred.

1. Een, Biere, SAT 2005, https://cca.informatik.uni-freiburg.de/papers/EenBiere-SAT05.pdf, section 2 original PDF page 3 inspected. Clause distribution replaces all pivot clauses by resolvents, equisatisfiable. Our bounded exact table projection is an analogous existential operation, not a novel universal theorem. Their results practical, not worst-case P.
2. Ben-Sasson, Wigderson, JACM 2001 https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf, pp 149-150 inspected. Width/size tradeoffs concern resolution refutations, not unrestricted deciders. Counterweight to universal bounded representation assumptions.
3. CaDiCaL src/elim.cpp actual blob fa457892162d79ed71d86081334f3adfc5b1262a, bounded variable elimination focuses changed variables; no executed build. https://github.com/arminbiere/cadical
4. Google OR-Tools cp_model_presolve.cc blob 7525a2da86f12a077744109344f7e4b65a635353 inspected header, not audited full algorithm or built; https://github.com/google/or-tools.
5. Google DeepMind formal-conjectures PROOFS.md blob edf4eb1afdbf0182fd9ac603d0f23adf97003d4c: statement repository distinguishes sorry and checked proof. No Boolean resolution claimed. https://github.com/google-deepmind/formal-conjectures
6. Anthropic formal-math vp-vnp/Statement.lean blob e64db90a929defe35d5b76d6eaa9bc0c87843ad3 and README; exact/approximate arithmetic separation statements over every field, permanent except characteristic 2, Hamiltonian cycle every field. Reported CI success Nov23, not independently built nor faithful formalization independently audited. https://github.com/anthropics/formal-math/blob/main/vp-vnp/Statement.lean. Recent issue 55 discusses per-instance recorded computation, not a verified counterexample to uniform class separation.
7. OpenAI math lean/docs/379.md blob b1a856319056d10c922672e8dda0bb924355aaa4: updated scope document for Nov24 family 379; exact arithmetic VP/VNP separation claimed, paper border bounds stronger, no build or independent proof term audit. Earlier standalone 379 scope has been subsumed. https://github.com/openai/math/blob/main/lean/docs/379.md
8. Specialist proof-generating BDD solver https://github.com/rebryant/pgbdd (README, extended resolution proof and LRAT checker, not built; no commit pin obtained), CryptoMiniSat https://github.com/msoos/cryptominisat (README incremental XOR interface, not built; no commit pin obtained). No credible Boolean complete proof acquired. External arithmetic claims not mathematical dependencies.

Falsifiers: (i) a failed/stale pop increases Phi (none in 2946 recorded pops); (ii) a missing or extra projected row (full replay matched both); (iii) mismatched gauge import or eliminated carrier, refused by live-coordinate and complement adapter checks; (iv) bogus root conflict rejected both. Additional universal falsifier: positive remaining Phi with empty queue and unresolved residual, actually present in both. General equality/matching/compact-circuit/padding/relabeling regression suite not newly executed. Exact equality normalization itself validated by hashes and signed consistency. DISJ sanity PASS scoped (both branches checked, no all-decider inference). Relativization/algebrization/Natural Proofs: not applicable to scoped explicit-table algorithm, universal barriers OPEN; no claimed barrier bypass. Simultaneous DTISP: analytical same-execution upper bound only; physical measurements incomplete; no lower-bound claim. Deterministic configuration: no lower bound extracted; finite deterministic transcript is a function of source.

## Evidence, review and next arrow
replay.js 6e12082ca59f582b4763a3856c73de42b6b16361; results.json fa29830a65d4054ec5958878379bc9e27f7f2a94; incremental.js 7356e07fa9d31c3ce0a3d3cc4dbdc04fa42bedb3; incremental-results.json 6c0e03b7ec56a0244268a16f4b5f4446b33e066b; certificate-check.js 33563564ab2d3f0cf815ccbb72645c72ef05cb75; certificate-results.json 9362e9dcd6d5f9d12c8934c212d818b68708a985; instrumented.js e5dfdaddcc5fde78721ccb317328d8cdcd99b3eb; potential-ledger.json 07e5ae8acfa9e6f1a188ddb8c564d74af6e9ba52. Exact cert artifacts:
JOINT solo 2d9746b7b349be997fd5c31539d0c04c37f72418, CERT-v1:sha256:9fa94e40cba228743ad90500acb99003b5a8d385b7cfaee266b3b04265a84e5e; hybrid 764a78ec481376ed399da8abe5b53cad5940d1f6, CERT-v1:sha256:76163bcbb690a34c19518cbfe16ea4362dfde32a2b6bd6aec186354ac8e9bc09.
RANDOM solo b5a25b62bbfc44c11f2a567ac09553531a675a7b, CERT-v1:sha256:febb43e883a962983bff9ffc11abf0a1288d73d8ad68e2d4e7e8c2345c96f576; hybrid 10684c39977ac51440cb03c3474076ffeb2049d8, CERT-v1:sha256:26d7360c9dbe82f999a4376a74d9da531e4cb0a365308f987a4f453989da775b. Broadcast #7225902055 and #7225902592. All four certificate contents were read back exactly. Checkers executed as functions in isolate with pinned inputs; standalone Node CLI not executed. Separate peer mathematical review pending.

First unresolved arrow: queue exhaustion with unresolved factors -> polynomially acquired productive contraction or a globally paid terminal. It does not follow from Phi being bounded. Next lemma: an adaptive width/cut/affine change must reduce a *global* potential on every unresolved NO residual while also paying failed candidate acquisition and all required branches; either prove it or construct a native family that defeats the precisely specified portfolio. No resolution, no public release in pvsnp, no README change. Release blocker is universal polynomial coverage/credit theorem and independent audit, not document preparation.
