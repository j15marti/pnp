# LSPV-3 RUP-CORE-REUSE262: source-authenticated core learning across branches

Date: 2026-10-30 18:24 America/Los_Angeles. Scope: integrated adaptive parameterized residual-SAT / arbitrary-A -> Phi(A) ARC/FLMV. P versus NP **OPEN**. All five roles, schedules, and existing enabled/paused states unchanged.

## Exact bounded claim and provenance

For a fixed original CNF F, suppose previously learned clauses were sequentially proved RUP against F plus older learned clauses. If UP under branch assumptions D contradicts, the learned clause L_D = OR_{l in D} NOT l is a globally implied and RUP-checkable source consequence. It can be retained safely across backtracking, unlike previously recorded *nonconflicting* conditional UP states. A one-pass deletion of assumptions under UP conflict produces an inclusion-minimal UP core, not necessarily a smallest-cardinality proof core. This is a known clause-learning principle with a source-proof and complete UNSAT-tree checker, not a novel SAT lower bound. The invariant has same-source SAT and UNSAT semantics.

The specific deletion routine re-evaluates the smaller assumption set after every removal and charges every attempted trial, decision, source-reason replay and learned-clause insertion. For a single checked leaf at depth d and literal count L_t its naïve bound is O((d+2)nL_t) indexed-word scans. The global number of leaves can remain exponential. No arbitrary-A or native indexed-TM resource conclusion is inferred.

## Falsifiers and measured both-label controls

Tests address: (1) stale successful-probe caching after backtracking; (2) whether shorter proofs mean lower total work; (3) whether a four-test deletion cap is sufficient; (4) whether structural parameters mark universal hardness. Full archive independently replays 1,952 RUP clauses and 7,829 proof-tree nodes across 60 source formulas (50 SAT, 10 UNSAT), checking 3,574 contradiction leaves and seven deliberately corrupt cases. Fifty-five instances have exhaustive truth tables; the 21-variable recognized SAT orbit has a verified original witness. Source-indexed local all-TRUE/all-FALSE and complement extremes are adversarial controls.

Instrumented total selected work includes source clause reads, UP, failed attempts, policy switches, witness/proof verification and source-checked learned writes. These events and Python peak bytes are **not** native FLMV TM steps.

| Source | Baseline UP-DPLL | Full-minimized-core DPLL | Baseline nodes | Core nodes |
|---|---:|---:|---:|---:|
| Easy Krom F9-minus UNSAT | 622,845 | 28,107 | 2,047 | 21 |
| W1 strict22 UNSAT | 20,186 | 68,010 | 143 | 45 |
| SWAP6 strict22 SAT | 10,483 | 37,555 | 78 | 32 |
| XOR K4 UNSAT | 1,755 | 9,685 | 15 | 15 |

A four-test cap costs 664,247 events for F9-minus; sound full minimization costs 28,107. But 2SAT SCC solves that easy source in 356 events, and XOR GE solves its own easy source in 316 events. A charged strict22 recognizer often sensibly selects plain DPLL, not learned cores. Thus none of witness count, branch mass, syntactic width, or proof length is a mandatory universal computation cost.

## Corpus and primary work

Actually read: governance REDIRECT1, CONTRACT1, root main.tex, AGENTS.md, CODEX.md, skill; AFFINE-SMALLBIAS-DESCENT-GATE2 restricted semantic theorem; CONSTRUCTION-STRENGTHEN17; ARC-LINEAR22-SATURATION1; predecessor LSPV-3 ADAPTIVE-SELECTOR-GATE255, MONOTONE-PROBE-RESUME254, BRANCH-MASS-GATE261; LSPV-5 ARC-SOURCE-RETENTION-QUANTIFIER-FIREWALL229 and HITTING-TREE-COMPOSITION-REFEREE222. The earlier opaque-policy acquisition bound and geometric scheduling are already known project results, not rebranded here. Literature: Eén and Sörensson (SAT 2003, DOI 10.1007/978-3-540-24605-3_37), Wetzler-Heule-Hunt (SAT 2014, DOI 10.1007/978-3-319-09284-3_31), FLMV (JACM 2005, DOI 10.1145/1101821.1101822). A local preflight checkout was unavailable; authenticated remote corpus reads were performed.

## Publication custody

Report (readback blob c82c7863864c1bf3d08d3bedf45424f7e1eb3e30): research/agents/lspv-3/2026-10-30_1824_LSPV-3_RUP_CORE_REUSE262.tex.
Producer (readback blob a5982df2da01a1788ab9a753033e2fe240bce598): experiments/arc/2026-10-30_1824_LSPV3_RUP_CORE_REUSE262.py.
Independent verifier (blob cb611f9d9277f679c33a913ee15e461e49aae183): experiments/arc/2026-10-30_1824_LSPV3_RUP_CORE_REUSE262_verify.py.
Compact GitHub summary: results/summaries/arc/2026-10-30_1824_LSPV3_RUP_CORE_REUSE262_summary.json.
Entire original 530 KB ZIP, PDF, full raw 5.9 MB JSON, scripts and checksum manifest were uploaded to persistent Research Library /P-vs-NP/2026-10-30_1824_LSPV-3_RUP_CORE_REUSE262_COMPLETE.zip, Library ID libfile_7285be7f83a88191ae937ee704ebdf96, SHA-256 cf633caeefef686ea90daca435260d44be971998d916d3ae3cb276db1079c490.

## Role-specific next obligation

LSPV-1: quantify all-input hereditary ARC child semantics; a shorter source proof is not a physically smaller ordinary SAT child.
LSPV-2: implement verified certified policy portfolios, retaining both-label source authentication and charged RUP proof replay.
LSPV-3: test whether a uniform, source-observable state condition permits beneficial RUP core reuse on genuinely mixed hard residuals after charging derivation and cache/eviction.
LSPV-4: audit joint input access, guest work, query size, policy acquisition, proof-checking and space in actual FLMV machine, not Python events.
LSPV-5: independent RUP/replay referee and whole-corpus synthesis, reject local lower-bound transfer to arbitrary-A.

No universal A -> Phi(A) contraction has been exhibited; ARC arrow and P vs NP remain OPEN.
