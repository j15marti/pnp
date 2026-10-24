# LSPV-3 | GUARD-BOUNDARY90 | Additive evidence and gap handoff

**P versus NP: OPEN. ARC-EDGE-90: OPEN.** No changes to research tasks, schedules, or other agents' files.

## Current result
Given any ordered proper 3CNF (H=igwedge_i(ell_{i1}eeell_{i2}eeell_{i3})), form connected proper 3CNF
(G_H=igwedge_i[(
eg xeeell_{i1}ee a_i)wedge(
eg a_ieeell_{i2}eeell_{i3})]), where every (a_i) is fresh. **PROVED/EXACT in the promised projection language:**
- (existsmathbf y,mathbf a,G_H[x=0]=1), and all-zero (x,mathbf a,mathbf y) satisfies (G_H) and all deletion subformulas.
- (existsmathbf y,mathbf a,G_H[x=1]iffoperatorname{SAT}(H)).
- Deciding one feasible-boundary membership, its size (one vs two), or its affine-hull dimension (zero vs one) is NP-complete under the generator promise, even though (operatorname{SAT}(G_H)=1) for every (H).
- Pinning (x=1) with four ordinary proper-3CNF clauses preserves SAT(H), but yields a self-contained child with (M'=2m+4,n'=n+m+3), (N'=(8m+18)w(n+m+3,2m+4)=N_G^{1+o(1)}), not (N_G^{1/2+o(1)}).
- A source-oblivious oracle restricted to even arbitrary adaptive deletion-only SAT questions sees only SAT, for both SAT and UNSAT base sources. This is not all-decider coverage.

**Novelty/deduplication:** The two-clause guarded disjunction is **not novel**: original SHIELD1 OR3-PROJECTION-AUDIT1 already has it. The present result specializes that construction into exact one-bit boundary-membership NP-completeness with connected always-SAT root and explicit pinned ordinary-child nonshrink. The report does not claim original invention of a gadget. Role 3 PIN89 and Role 5 NAMED125 already establish unrelated source-anonymous and name-preserving profile firewalls.

## Matched resource and semantics ledger
- Source (H): (n) active variables and (mge1) proper ternaries, declared word width (w(n,m)=lceillog_2(64(n+m+1))ceil).
- Parent (G_H): (n_G=n+m+1,M_G=2m,N_G=(8m+2)w(n+m+1,2m)). The active clause-variable incidence graph is connected via common selector (x) and private (a_i).
- Projection (Sigma_H): exactly ({0}) or ({0,1}). Unlike affine or NAE sign-cycle rank, this is the cardinality of a emph{non-affine feasible} exact boundary relation. Discovering it is SAT-hard even though deciding the parent is trivial.
- Ordinary pins (K_H^b): (n'=n+m+3,M'=2m+4). The fixed record encoding is self-contained and charged; no source pointer qualifies as a tiny child.
- Adaptive policy state: parsed source/pointer and guard recognition first; then recognized unpinned/x=0 branch outputs the universal all-zero witness; x=1 branch uses a suitable observed-evidence solver (Horn/SCC/affine/DPLL fallback). Neither base SAT label is given in advance.
- Resource vector: primitive bit work; read-only source reads; writable reads/writes (changed and unchanged); actual complete-state flips; peak live writable bits; cumulative bit-time; program/representation length. Include selection, failed attempts, source validation, child headers/bits, indexes and any cache. No FLMV pair improvement obtained.

## Reproducibility
- Standalone report: `research/agents/lspv-3/2026-10-24_1924_LSPV-3_GUARDED_BOUNDARY_ACQUISITION90.tex`, report blob `6b157d9ef18676a195d052bc436d5df42656dda3` (verified header/body/final sentinel).
- Full Python standard-library reproducer: `research/agents/lspv-3/2026-10-24_1924_GUARD_BOUNDARY90_repro.py`.
- Immutable raw: `results/raw/2026-10-24_LSPV3_GUARD_BOUNDARY90_raw.json`.
- 4,076 assertion-counted checks, zero discrepancies; exhaustive **255** nonempty subsets of all eight three-variable sign clauses and **64** additional seeded proper-CNF controls; 254 SAT and one UNSAT among the 255 exhaustive base formulas.
- Deterministic JSON SHA-256: `4a4197a9a1058e03880af264a19e7dc53e2c840aae868c52d96a428dab2b7aad`. Finite controls are COMPUTATIONAL, not an asymptotic lower bound.

## Source coverage increment
- Original Drive user-supplied `PROOF-SYNTHESIS-0013`, URL `https://docs.google.com/document/d/1QirzuNPCG-CrE3EX6WweqsPdDbtoblCDEE4YI0HGyC0`, full 22,415-character text fetched. Supports existential achievable-region contraction only.
- Original GitHub `main13.tex` blob `87dbaad5e18932b1db7fca57fc40e0ac020a6f49`, fetched; same-realization and FLMV endpoint examined.
- Root `main.tex` fetched; latest root blob must be refetched for role-owned reconciliation because other agents write concurrently.
- Governance `AGENTS.md` c5265db0, `CODEX.md` 754999f5 and repository skill b8df83a7 fetched.
- Original SHIELD1 OR3 report `research/agents/shield1/2026-10-15_1453Z_SHIELD1_OR3_PROJECTION_AUDIT1.tex` blob 4b917b55, **full body read**.
- Role 5 `NAMED-PROFILE-IDENTITY125` blob a305dee0, Role 1 `ADAPTIVE-LOCAL-DEPTH126` blob d28d6e47, Role 4 `NESTED-VIRTUAL-TRANSCRIPT84` blob c62e80e0, Role 3 `PIN-PROFILE-JOIN-FIREWALL89` blob f0f1713e all read.
- Earlier `KROM-PROJECTION-CEILING99`, `PROJECTION-BLOWUP59` read at the relevant proofs. Latest predecessor LSPV-2 directory was listed; at inspection there was a new 19:12 mini reproducer but no verified matching complete report. Do not reconstruct its missing research claims.
- Original FLMV author-hosted PDF machine model and Corollary 5.8, visually reviewed PDF page indices 3 and 17. Canonical URL `https://lance.fortnow.com/papers/files/tst.pdf`.
- Drive exact-title search `HEREDITARY-SCOPED10` returned one continuity-log document, not the original compiler; search does not prove it never existed. Broad LOG/SIL/BOOL/PROVED_EXACT pagination, earlier main2-main12, and full manual review of the inherited 3,532-file pinned keyword census remain outstanding. No claim of exhaustive current archive review.
- Repository-local preflight could not be executed without a checked-out repository; GitHub connector readback is the publication check.

## Acceptance ledger
**FILLED/PROVED/EXACT restricted:** exact one-bit projection, NP-completeness of guarded contextual membership, deletion-SAT-oracle blindness and ordinary-pin source-length accounting.
**PARTIAL/RESTRICTED:** guard-language recognition and straightforward root witness; appropriate source-aware algorithms can bypass projection.
**FALSIFIED/RETIRED:** single-bit boundary necessarily provides cheap table, all deletion SAT answers reveal one-bit context, pinning yields fractional-size ordinary ARC child.
**OPEN:** full source of ARC-HEREDITARY-SCOPED10, global source-coherent reusable child contractor, existential achievable-pair improvement, cofinal charged route, P versus NP.

**Next exact experiment:** obtain HEREDITARY-SCOPED10's full construction and compare a second generation of its ordinary children with guarded-one-bit examples. Require semantic equivalence for arbitrary parent SAT/UNSAT instances and bound discovery, call count, child bit generation, reconstruction and live memory. A cheap restricted recognizer with expensive general fallback is insufficient.