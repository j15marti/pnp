# LSPV-4 CANONICAL-ONLINE-DECISION-REPLAY312
**November 1, 2026, 12:36 PST. Circuit Resource Auditor.**
**Status: PROVED/EXACT restricted canonical-language instantiation of a PREVIOUSLY PROVED online-update lower-bound method; COMPUTATIONAL independent source-level both-label controls; NOT a new unrestricted lower bound. P versus NP OPEN. External mathematical review pending.**

## One precise obstruction and novelty audit
The all-input adaptive-decomposition program seeks to quantify actual SAT/UNSAT decision WORK without assuming complete assignment recovery. Four-bit ordered transfer relations permit efficient STATIC decision on connected canonical G_t, while a recently published balanced segment DAG permits logarithmically many matrix compositions per point update by retaining O(t) matrices. This begs whether the **same one-bit answer** can be maintained after arbitrary future point replacements without retaining those profiles and without rereading historical updates. The answer is NO in the declared consumed-history dynamic model. **This principle was already proved in this repository for ordinary proper-3CNF scalar chains:** LSPV-4 UPDATE-LOG-REPLAY-FIREWALL215 (2026-10-29) and ADAPTIVE-UPDATE-MEMORY-FIREWALL212 (2026-10-28). The new restricted increment is an authenticated lift of that method to the exact duplicate-free monotone proper Döcker-(2,2) target language via the now verified connected source G_t, with fresh independent source-level controls. No originality is claimed for the abstract streaming argument.

Four falsifiers specified before computation were: **F1** one current SAT/UNSAT bit is a continuation-complete state (FALSIFIED by a valid same-original G_2 pair); **F2** four-bit Boolean boundary relations imply O(1) retained memory for arbitrary consumed update histories (FALSIFIED: at least t bits of midpoint information); **F3** the t-bit lower bound applies when all past updates survive on a re-readable input (FALSIFIED: polynomial-time O(log X)-workspace replay); **F4** the restricted dynamic-memory result establishes an all-input SAT/ARC/FLMV space lower bound (INVALID scope, not proved).

## Fully authenticated canonical original and exact decision predicate
Let F9 have positive source clauses (156),(238),(135),(469),(247),(789), and negative source clauses -(468),-(167),-(234),-(358),-(129),-(579). For t>=1, form G_t from t labeled copies by replacing the positive x5 occurrence in each copy's clause (156) with x5 from the NEXT copy cyclically. This source is connected for t>1, and for every t it is duplicate-free, proper clausewise-monotone 3-CNF, with each ORIGINAL variable appearing precisely twice positively and twice negatively. Thus each G_t is a valid target-language original. Ordinary coherent pinned residuals need not themselves belong to the target language.

In each block choose only two coherent original-variable pin profiles:
```
A: x1=1, x2=0, x3=1, x4=0, x8=0
B: x1=1, x2=1, x3=0, x4=0, x8=0 .
```
With consecutive boundary variables a_i=x5_i, a_(i+1)=x5_(i+1), independent full original-clause enumeration of the eight internal variables gives exact nonnegative matrices
```
W   = [[34,47],[23,36]]  (unrestricted);
W_A = [[ 1, 1],[ 0, 0]];
W_B = [[ 0, 0],[ 0, 0]].
```
For every binary profile word b in {A,B}^t, the exact number of satisfying original-source extensions is trace(W_{b1}...W_{bt}). Since W_A^2=W_A and W_B=0,
```
       SAT(G_t | b)  <=>  b=A^t.
```
This is a **decision-only** identity. It neither requires outputting a witness nor recovering the pin values. An arbitrary pin word can be tested in linear block work by a paid ordered Boolean transfer or by scanning for B. That is an important EASY adversarial control.

## Theorem: dynamic consumed-history decision-only memory
**Declared online query architecture.** Fix the authenticated canonical G_t as a read-only original. Initially the active source-relative cube is A^t. Each point command `SET(i,A)` or `SET(i,B)` overwrites block i's coherent five-pin profile, including x2/x3, without supplying the OLD profile. The algorithm must output the correct one-bit residual SAT answer after every command and for every possible future sequence. Old update commands are consumed, inaccessible for replay; neither a writable shadow source nor an external answer oracle is free. The program is deterministic and uniform.

**THEOREM (restricted, exact).** Immediately after the first t commands `SET(i,b_i)`, i=1,..,t, the updater must have at least 2^t pairwise distinguishable retained configurations. Equivalently at least t bits of TOTAL configuration information are required, although the CURRENT output is only one bit and NO original pin is requested for recovery. On fixed-tape, finite-alphabet machines with polynomially bounded head addresses and a fixed number of tape heads, this implies Omega(t) visited writable cells after accounting for finite-control and head-position bits.

**Proof.** All 2^t profile words b occur after the first t source-profile SET operations, using the same command-index order. Take two distinct words b,c and choose any coordinate i where they differ. Apply the SAME common suffix of t-1 SET commands setting every j!=i to A. The two resulting states have all-A versus exactly-one-B, hence SAT versus UNSAT by the original-source matrix identity. Deterministic identical retained midpoint configurations followed by identical future commands cannot yield opposite answers. Therefore all 2^t midpoint configurations are distinct, requiring at least t bits of distinguishing information. Output tape contents are write-only and cannot be accessed as uncharged memory; head positions must be included in the complete configuration. QED.

**Nuance.** This is stronger than CUBEKEY306's recoverable-syntactic-key claim in one respect: no recovery is demanded, only future correct Boolean answers. It is weaker than an unrestricted algorithm bound: the machine is forced to support an online editable residual under a **NON-REPLAYABLE** update interface. No theorem forces an ordinary static SAT decider, or the all-input adaptive ARC controller, to adopt that interface.

**Direct FLMV-scale comparison.** Under the declared gamma-header fixed-width source grammar,
`N(t)=|gamma(9t)|+|gamma(12t)|+12t(1+3*ceil(log2(9t+1)))=Theta(t log t)`.
Thus the consumed-history midpoint information tariff is Omega(N/log N), exceeding N^(1/2+o(1)) asymptotically. For t=512, N=245,810 source bits and t=512 exceeds sqrt(N)=495.8. This is **not** an FLMV SAT lower bound, because a re-readable input changes the information accounting, and the original target input is static. For the unrestricted proof the missing bridge is a SAME-MACHINE theorem forcing such a consumed-history online state on EVERY arbitrary correct decider A.

## Replay/caching controls and full work accounting
**Re-readable log option:** Encode source G_t and the complete update-command prefix as a read-only input of length X=N(t)+O(H log(t+1)). For each of H decision checkpoints, scan each of t block indices, recover its latest SET value by reading the appropriate prefix of the log, then AND these t recovered control bits. This is a uniform deterministic procedure with O(log X) writable/index/head counter bits and conservative total O(H*t*X*polylog X) native steps, with ALL source decoding, input-head travel and log rereads charged. For H=Theta(t), this is polynomial (roughly cubic in t up to logarithms), not exponential. It is not the one-pass model in the theorem.

**Cached option:** Retain at least t bits representing independent A/B update state, or a larger authenticated ordered Boolean segment DAG; update with charged old-value lookup and zero counter or matrix recomposition. The project LSPV-2 DYNAMIC-DECISION-DAG311 already gives O(log t) matrix compositions per update with O(t) cached matrix records. That work is prior and is not claimed new. The memory theorem explains a restriction on attempts to reduce its dynamic retained workspace while also denying input-history replay.

**Complete all-input recurrence (still unproved polynomial):**
```
W_D(z) = C_grammar/source/index/head
       + sum_{each attempted policy pi} C_discover/select/switch/failed/check(z,pi)
       + C_GE/matroid/cut/proof/cache/replay(z)
       + sum_{each evaluated child y} [C_child/emit/bit/guest(z,y)+W_D(y)].
```
Peak S is the MAXIMUM SIMULTANEOUS live writable/index/ancestor/matrix/proof/cache/guest/child staging; source and output tapes are excluded from FLMV writable-space but not from access/output TIME. Physical fixed-location XOR is recorded only for the declared tape simulator; original-source logical XOR is OFFLINE. An indexed jump may atomically erase its index tape and cannot be charged by naive one-cell-per-bit XOR lower bounds.

## Independent finite experiments and original-source proof
A new standalone original-clause producer and separately authored NO-PRODUCER-IMPORT verifier passed **34,717 verifier checks**. They independently reconstruct G_t and W, W_A, W_B; G_1 has 70 global models and G_2 has 4,614; exact original-source exhaustive SAT/UNSAT models were checked for EVERY one of the 2^t A/B words for t=1,2,3. Same-original G_2 certificates: all-A has an original 18-bit satisfying witness; B/A has a COMPLETE 256-leaf UNSAT cover, each source-indexed false-clause leaf independently checked. The verifier checked all 264 original F9 clause-pair SS/SU/US/UU modes, all 512 full assignment/complement identities, and six malformed original-source variants. No arbitrary occurrence assignments were substituted for actual global variables.

For t<=8, all C(2^t,2) distinct midpoint pairs were explicitly distinguished by the prescribed common future SET suffix. For t up to 128, two independent versions of the incremental pinned-bit updater and replay-on-read log evaluator agreed after all 2t point updates. A direct source-indexed unit-propagating DPLL baseline on original G_1/G_2 solved BOTH A/B labels in one DPLL node per case; this family is intentionally EASY.

| t | N source bits | online t-bit state | no-replay head moves (declared sequential-pin-bit tape) | read-only log-record examinations over 2t outputs |
|---:|---:|---:|---:|---:|
| 2 | 402 | 2 | 2 | 12 |
| 8 | 2138 | 8 | 22 | 620 |
| 32 | 10786 | 32 | 382 | 33,779 |
| 128 | 52,266 | 128 | 5,695 | 2,151,591 |
The head moves count positional movement only between the cached pin-bit cells, NOT all native FLMV source/index tape steps. Actual changed pin bits (physical XOR) are measured separately; zero XOR does not imply zero time. Full implementation-dependent raw traces and complete SAT/UNSAT certificates are included in the independently checksummed reproducibility archive. No executed native end-to-end FLMV SAT simulator or industrial CDCL benchmark is claimed.

## Strict numerical FLMV firewall
Rechecked with exact rational arithmetic using FLMV's indexed model envelope: d*(6/5)=23/45 and d*(241/200)=11642479/23232400, unique maximizing k=2 with k>=4 strictly excluded. For hypothetical target language solver time/space exponents (6/5,1/2), transfer to ordinary SAT still needs a FULLY ADDRESSED ordinary-SAT-to-Döcker reduction with output exponent b and guest per-bit overhead exponent rho satisfying **(6/5)b+rho<241/200** and **b/2<11642479/23232400**, with setup time, output, multiple tapes and simultaneous peak workspace independently bounded. Even rho=0 demands **b<11642479/11616200=1.00226227...**. NP-completeness alone provides NO such numerical transport; no universal arbitrary-decider power-short A->Phi(A) theorem was obtained.

## Literature/search and corpus reconciliation
**Read FIRST:** 01:48 integrated five-role handoff (GitHub), 01:44 SATURATED-CYCLE-AFFINE-TERMINAL1, then AGENTS.md/CODEX.md/pnp-research skill, decision-only handoff, issue #3, latest reports LSPV-1 RANDOMIZED-QUERY309, LSPV-2 DYNAMIC-DAG311/QUOTIENT310, LSPV-4 WINDOW311/FULL-PAYLOAD310, LSPV-5 FIXED-WINDOW REFEREE271, and LSPV-3 prior GATE305. **CRITICAL older duplicate** found in the same repo BEFORE proof: LSPV-4 UPDATE-LOG-REPLAY-FIREWALL215, ADAPTIVE-UPDATE-MEMORY-FIREWALL212, which already establish the generic one-pass memory versus reread/replay dichotomy on ordinary-3CNF; this report claims only target-language G_t instantiation and independent new controls. The role-2 online matrix DAG and role-5 Boolean streaming quotient are also prior work.

**Web primary literature queries:** "Fortnow Lipton van Melkebeek Viglas indexed random access input theorem 5.7", "Döcker Monotone 3-SAT-(2,2)", "Fredman Saks cell probe dynamic data structures 1989", "Slivovsky Szeider SAT 2020 bounded incidence treewidth" (sources: https://doi.org/10.1145/1101821.1101822; https://arxiv.org/abs/1912.08032; https://doi.org/10.1145/73007.73040; https://doi.org/10.1007/978-3-030-51825-7_19). Project GitHub searched "online update replay memory AND t", "point update Boolean relation", "UPDATE_LOG_REPLAY_FIREWALL215", "DYNAMIC_DECISION_DAG311". Separate github.com/openai search "Indexed Turing work tape", "SubexponentialSAT ProgramLogic" and read https://github.com/openai/math/blob/main/lean/OAI/Algorithms/SubexponentialSAT/ProgramLogic.lean; measured trace requirements there support the accounting discipline, but supply no theorem about this canonical target family. No novelty inferred from search absence.

**Publication/root:** This is a new role-4 dated standalone report. Its compact code/raw and five-role additive handoff are published and read back through GitHub, and complete no-import verifier/raw/source certificates are in the archive. Root main.tex remains subject to marker-only governance; **do not risk a >1MB unsafe contents-API overwrite**, and report reconciliation pending if a safe blob-based patch cannot be verified. No existing five task identities, titles, enabled statuses or hourly schedules changed.

## Exact proof status
**KNOWN prior methods:** Fredman-Saks dynamic data-structure accounting; project LSPV-4 212/215 general dynamic information bound; LSPV-2 310/311 exact Boolean semiring and segment-tree transfer.
**NEW scoped verified instantiation:** valid canonical same-original G_t with A/B source pins embeds AND_t into a point-update decision-only task, yielding the conditional t-bit retained-information bound, explicit same-source opposite-label certificate control and paid replay escape.
**UNPROVED:** representation-independent necessary work for every static target original, uniform polynomial TOTAL adaptive work, hereditary all-input arbitrary-A->Phi(A) power-short contractor, strict model-matched FLMV transport, P=NP or P!=NP.

END_OF_LSPV4_REPORT::CANONICAL_ONLINE_DECISION_REPLAY312::P_VS_NP_OPEN
