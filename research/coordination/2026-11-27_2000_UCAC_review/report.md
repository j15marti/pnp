# 2026-11-27 20:00 Pacific | UCAC coordinator synthesis
Review window: 18:00–20:00 Pacific, 2026-11-27 (02:00–04:00 UTC Nov 28), plus predecessor links. Status OPEN. No public release.

## New independently executed evidence
Exact native and companion inputs regenerated with the canonical compiler; native SHA256/N, companion SHA256/N, map SHA256 and chart/guard IDs checked. No peer learned clauses provided as advice in the new width-two lane. The shared chart algorithm was reused at its pinned revision and its complete-bucket projection independently checked; this is not a new independent compiler proof. Gauge port 10=0, then complement symmetry discharges gauge for root NO. Source-only chart discovery used only native bytes; separate provenance-map hash authentication is charged, not used for choosing clauses.

| Item | JOINT-24 | RANDOM-3CNF-40 |
|---|---:|---:|
| Native N bits | 5363624 | 5027816 |
| Projected chart variables | 24 | 40 |
| Projected CNF rows | 144 | 184 |
| Candidate width <=2 universe | 1153 | 3201 |
| Candidate attempts | 1025 | 4399 |
| Epochs | 2 | 3 |
| Checked learned rows incl empty | 1014 | 3187 |
| Forward discovery literal visits | 296866 | 3895783 |
| Reverse replay literal visits | 23994 | 114079 |
| Separate occurrence queue replay literal visits | 8419 | 72700 |
| Projection verification operations | 194433 | 180493 |
| Companion CNF proof rows | 1014 | 3199 |
| Companion discovery visits | 346822 | 2909832 |
| Companion occurrence replay visits | 8463 | 85833 |

Full proof data: [width-two replay JSON](https://github.com/j15marti/pnp/blob/f4759759795113923c73cdd443f2be434a3b2e9f/research/coordination/2026-11-27_2000_WIDTH2_REPLAY.json). [Independent checker](https://github.com/j15marti/pnp/blob/7f0d1a2765de39afdb68100518c19fb9283b18fd/research/coordination/2026-11-27_2000_UCAC_review/check.js). Native certs [JOINT](https://github.com/j15marti/pnp/blob/eba13eb39a53dd42f0ab1afbbcadbd700f1b5db1/research/coordination/2026-11-27_2000_UCAC_review/JOINT-24.cert.json), [RANDOM](https://github.com/j15marti/pnp/blob/40d98249263ca4e4373894dc61544312ed675841/research/coordination/2026-11-27_2000_UCAC_review/RANDOM-3CNF-40.cert.json). Bus #7233648589 and #7233649079. All artifacts read back exactly. These are finite refutations, not polynomial speedup: scan counts exceed smaller DPLL proofs. Timings from isolate not equivalent bit-time or complete memory measurement. Chart IDs and original ID ranges in certs. Both empty guards discharged only for root claim; proof chart guard is not EMPTY.

## Matched consumer ablation
Recomputed T1's exact native chart (source and map verified), used separate deterministic propagation and split-tree search. Initial chart UP forced zero assignments on both. JOINT 23 nodes -> 21 with independently RUP-admitted [-594]; 12409 -> 11778 literal visits, plus 1565 admission/reclosure; net continuation alone more costly. RANDOM ordered candidate seeds a=[362,34], b=[362,-33], c=[362,298]. Masks ordered binary a=1,b=2,c=4. All eight published proof streams independently reverse-RUP replayed. Refused requested clauses are not semantic counterexamples. No free imports.

| mask | admitted | refused | nodes | discovery literal visits | admission/reclosure | independent proof replay visits |
|---|---|---|---:|---:|---:|---:|
|0|none|none|63|78346|0|45904|
|1|a|none|59|74287|2720|41562|
|2|none|b|63|78346|540|45904|
|3|a,b|none|59|73441|4200|37975|
|4|none|c|63|78346|1067|45904|
|5|a,c|none|51|61761|4933|31934|
|6|none|b,c|63|78346|1607|45904|
|7|a,b,c|none|43|52167|6403|28476|

Local cones in T1 artifact (0-based chart row indices, sequential previously admitted clauses) independently replayed: 12,9,14 parent rows; 145,67,133 reverse literal visits; all 35 single deletion assignments checked under negated target, and each full local cone has a satisfying assignment. Thus local inclusion-minimality checked, not global minimality. T1 #7233483586, T2 #7233522382, L02 #7233612913. The new full width-two sweep discovers all three independently without receiving their order: b at admission25, a83, c1836, all epoch1. Dependency is on the current closure, not on those exact three as universal logical prerequisites. Compare producer plus all failed work before claiming speedup. Matched source-only versus candidate-assisted chart experiment; no claim of full T2 row-shadow reconstruction, complete provenance-assisted cost comparison or all-six-lane/feedback repeat in coordinator execution.

## Scoped theorem, proof and failure boundary
For a fixed exact CNF chart with n named variables and total input literal length L, define candidate universe of distinct non-tautological clauses of width <=w, including empty: M=sum_{j=0}^w 2^j binom(n,j). Repeat deterministic scans of all candidates, adding only clauses whose negations cause unit-propagation contradiction in current formula. Unit propagation is sound; adding a RUP clause preserves all models. Empty clause is sound rejection. Monotonicity under clause addition ensures a complete no-change sweep is a fixed point for this inference rule. There are at most M admissions and M+1 sweeps. With indexed occurrence queues and explicit word/bit costs, one probe is polynomial in L+wM+n; a crude implementation can use repeated full scans up to n+1 rounds. Thus total bit-work polynomial for fixed w and polynomially acquired chart; no cost reset needed. Initial credit (M+1)^2 probe slots plus polynomial per-probe work tariff suffices, even for failed candidates. The first missing implication is that every NO in strict native E/B admits either a polynomially acquired chart with such a refutation or another universally covered charged terminal. Width-two RUP on a fixed bounded-original-width chart is restricted: a RUP derivation of C can be reconstructed by unit resolution in F restricted by not C and lifted by adding C to each line, allowing weakening, width <= max(original/learned width)+|C|. Hence known unbounded resolution-width examples obstruct fixed-width RUP on the unchanged CNF encoding, not all transformations or unrestricted algorithms. Do not infer P!=NP. General short certificates alone imply NP=coNP if universal, not P=NP without polynomial acquisition. Pure equality/parity/matching controls may bypass proof-system obstruction.

## Active-agent coverage (latest accessible result, not all overlapping runs)
20 enabled, 5 paused. Metadata and latest-result records inspected for all 20; some connector outputs only truncated excerpts, not full earlier run history. Latest visible issue comments lacked timestamps; ordered comment IDs plus dated artifact paths used, not claimed exact time-filtered completeness. Main recent commit query returned 100, branch page returned first 100 with continuation; exhaustive branch/PR/artifact coverage incomplete. Deduplicate same input/certificate/commit, not same title. No new role needed: existing roles cover the new bottleneck. No schedule/state change.

| Active role | Observed status/contribution | Next deliverable / receiving role |
|---|---|---|
| TETRA Interfaces | completed; response quotient, prior three-clause activation | replay identical chart width2 stream at first changed row-shadow operation; TETRA Synthesis |
| Finite Group Classification | completed; orbit obstruction, all eight masks | characterize bounded-width closure escape via exact coset support; Closure Finite Groups |
| Closure Proof Synthesis | completed; persistent RUP credit, local-parent DAG | prove aggregate failed-probe accounting with exact retention and compare above baseline; Cooperative Proof Synthesis |
| Closure Shared Wheels | in progress; latest completed result outside window; L02 later artifact reports exact motif/BFS replay | test sparse motif contraction after full width2 closure, not merely compression; TETRA Matching |
| TETRA Synthesis | completed; persistent-context narrow Hall activation | integrate fair fixed-credit lane, preserve other baselines; coordinator |
| TETRA Multisign | completed; affine projection credit | exact costed guard/coordinate transfer, plus nonaffine falsifier; Algebraic Geometric Closure |
| Monotone Exact-22 | completed; exact count-level decoder and local parent witnesses | blind incidence ranking vs full saturation on growing cases; TETRA Interfaces |
| Cubic Edge Coloring | completed; sparse cut join native contradiction | post-saturation exact sparse cut and row-cap controls; Flow Plateau Research |
| Affine Bijunctive SAT | completed; fixed-chart affine packet credit | exact hybrid beyond bounded RUP on growing hard charts; Strict T5 CSP |
| TETRA Guarded DAG | in progress; latest result guard splice | export occurrence replay / LRAT and verify split credit; Closure Proof Synthesis |
| Ground-Up UNSAT Bounds | completed; refinement costs, parent deletion controls | construct native growing high-width NO + cheap bypass controls, not unrestricted bound; all lanes |
| Algebraic Geometric Closure | completed; quadratic quotient and affine seed | compare polynomial calculus cancellation against RUP closure, explicit degree; TETRA Multisign |
| Closure Cooperative Contraction | completed; persistent CEGAR | prove bounded correction discovery or produce checked stall; Affine Bijunctive SAT |
| Strict T5 CSP | latest run FAILED; last accessible result older cross-scope affine retraction | recover owned artifacts, do not assume new result; Algebraic Geometric Closure |
| Four-Partition NAE | completed; seam merge, pair UP zero-success Fano | replay hostile Fano and growing native family; Ground-Up UNSAT Bounds |
| Closure Finite Groups | completed; exact symmetry transport | check stabilizers and native guard pullback for high-width family; Finite Group Classification |
| Flow Plateau Research | completed; clipped energy, synchronization plateau | exact lower-bound certificate after RUP, pay synchronization and all table costs; Cubic Edge Coloring |
| Closure Exceptional Syndrome | completed; sketch collision and correction | exact correction after width2 stall, zero sketch not SAT; Closure Cooperative Contraction |
| TETRA Matching | completed; Hall contraction and refusal theorem | Hall export on stalled exact chart, independently replay without seed hints; TETRA Interfaces |
| Cooperative Proof Synthesis | coordinator; T4 delta/guard glue; in-progress record | keep global credit and review proof DAG, no public release absent universal theorem |

## Ranked next experiments
1. Universal disjunctive activation theorem: fixed schedule on every original native NO; after polynomial forced closure and fixed-width saturation, either certified terminal or charged productive export by a complementary lane. A proof with a non-resetting polynomial potential and bounded state on EVERY reachable state gives P=NP (given checked NP-completeness and soundness). A certified simultaneous fixed point falsifies only stated lane coverage, not P!=NP. UNKNOWN leaves theorem open. Owners TETRA Synthesis + Cooperative Proof Synthesis; all others supply counterexamples and transfer. Stop on proof/audited falsifier or fixed cap.
2. Growing hostile native controls, with both cheap bypass and hard cases: bounded-width RUP chart obstruction via resolution width, then Gaussian, exact occupancy, matching, separators and guarded DAG escapes. Each scoped survival must preserve exact native adapter and all guards. T3 Ground-Up, Strict T5, Four-Partition, Cubic; T1/T2 verify bypass. If all named tracks stall this refutes their claimed sufficiency, not arbitrary deciders. Need infinite all-decider transfer for P!=NP.
3. Acquire narrow seeds by full bounded-width closure as control before stochastic/heuristic methods. Determine first changed operation on matched exact charts, all masks and both labels; prove activation credits with failures, monotone cache, replay and storage. A finite speedup or short proof is scoped; a universal acquisition/coverage theorem is still needed. Owner Monotone/Interfaces/Closure Proof Synthesis, consumer T4. Stop after exact comparison and first missing arrow. Preserve first-stall feedback protocol and early forced-information in every lane.
4. Arithmetic-to-Boolean transfer only if it proves exact uniform simulation on the correct field/model; no assumption that Boolean decision provides formal coefficient or exact counting access. Track lower-bound specialists and synthesis; require actual checked theorem connecting decision to arithmetic complexity. Otherwise keep external results as scoped background.

## Literature and external checks
Fresh searches: SAT bounded-width RUP, failed literal probing, binary clause learning, Atserias-Dalmau, Ben-Sasson/Wigderson, Cook-Reckhow, LRAT checker, official Anthropic/OpenAI arithmetic separation, Google OR-Tools / DeepMind formal-conjectures, xAI SAT proof repos (no relevant verified result returned). Repository own #328 and recent commit/branch searches; no comprehensive branch pagination. [Atserias-Dalmau ECCC TR02-035](https://eccc.weizmann.ac.il/report/2002/035/) resolution width characterization; [Ben-Sasson/Wigderson JACM 2001](https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf) width/size theorem (original bounded-width formula, not arbitrary chart). [Cook-Reckhow 1979](https://doi.org/10.2307/2273702) proof length versus decision distinction. [OR-Tools probing.h](https://github.com/google/or-tools/blob/stable/ortools/sat/probing.h) binary extraction/failed literal fixed-point implementation, not a complete SAT solver by itself. [LRAT Isabelle checker](https://github.com/lammich/lrat_isa), [Lean lrat-catcher](https://github.com/leansolving/lrat-catcher) candidate independent checkers, not built here. [DeepMind formal-conjectures proof policy](https://github.com/google-deepmind/formal-conjectures/blob/main/PROOFS.md) statement/axiom audit. [Anthropic Statement.lean](https://github.com/anthropics/formal-math/blob/main/vp-vnp/Statement.lean), [reported CI](https://github.com/anthropics/formal-math/actions/runs/45266217321); exact arithmetic circuit and approximation claims, all fields for Hamiltonian, permanent outside characteristic 2; [OpenAI November 24 preprint README](https://github.com/openai/math/blob/main/preprints/Circuit-lower-bounds-for-Hamiltonian-cycle-and-the-permanent-November-24-2026/README.md), exact circuit Lean scope and stronger manuscript bound. External source URLs inspected, exact upstream commit resolution not completed, no independent builds or arithmetic-to-Boolean transport. No external proof assumed. DISJ/relativization/algebrization/Natural Proofs and DTISP transfer not established; fixed-chart proof search does not address unrestricted barriers.

## Accounting and limitations
Actual sequential interleaving (no simultaneous worker benchmark). Candidate attempts, projection verification, literal checks and replay recorded, not equivalent bit clock. Physical peak/cumulative space, full earlier run history, all PRs/branches and full peer-producer discovery cost not recovered. Separate current source-only lane from all historical work; no end-to-end speedup or completeness inferred. No new feedback/residue paired experiment, five-lane benchmark or MFC/transport replay executed by coordinator this pass; role-owned reports retained, mandatory tests assigned. Public gate BLOCK: no universal productive acquisition and no proof of unrestricted lower bound; no public pvsnp edits.
