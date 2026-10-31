# LSPV-1 ARC-QUERY-SPECTRUM275 (2026-10-31, 09:35 PDT)

**STATUS:** PROVED/EXACT restricted theorem (independent mathematical review pending); COMPUTATIONAL finite tests; CONDITIONAL hereditary ARC recurrence; P versus NP **OPEN**. This extends LSPV-5 REFEREE243's homogeneous DELAY call test to an adaptive heterogeneous query-length spectrum. It is **not** an arbitrary-SAT lower bound.

## Target and exact quantifiers
The project seeks a single uniform, hereditary, source-authenticated compiler applicable to every fixed correct polynomial ordinary-SAT decider A with **unknown** exponents K,L on the **same FLMV indexed-input Turing model**, satisfying both labels and
[
K'\le\max(11/10,3/5+K/2),\quad L'\le\max(1/2,L/2).
]
The all-input `A -> Phi(A)` compiler remains unconstructed.

## Four falsifiers
F1. Average-short calls compensate for a rare N^(1/2+epsilon) compulsory long call: **FALSE** for an answer-driven opaque guest after a sufficiently large polynomial DELAY wrapper.
F2. N^(3/5+epsilon) calls each of near-square-root length satisfy the time recurrence: **FALSE**, for the same restricted architecture.
F3. Serial query time can be accounted by only the maximum individual child: **FALSE**. Time sums completed calls, while serial guest workspace may be reused, with retained/visited physical storage charged.
F4. These counterexamples exclude every code-aware compiler: **FALSE**. The theorem requires an opaque, timing-oblivious, actually executed guest; code-aware avoidance is outside its quantifiers.

## Exact theorem and proof
Fix a correct uniform polynomial SAT decider A0. Let C[A] be a **boolean-answer-driven** deterministic oracle-style controller, whose ordinary-SAT query strings depend only on original source and previously returned SAT bits, never on A's code, running time, or internal steps. All calls must actually complete. On a source F of length N its transcript is y1,...,yq with positive physical lengths Mi. For each integer D above A0's exponent, define a correct SAT machine A_D that executes Θ((M+1)^D) dummy transitions before A0. Replies and therefore adaptive transcripts are unchanged for A_D.

Set W_D(F)=sum_i (Mi+1)^D. The guest-execution time is Ω_D(W_D(F)). If qb(F)=number of queries with 2^b <= Mi < 2^(b+1) and B=floor(log2(max Mi)), then
[
\boxed{\max_b q_b 2^{Db}\le W_D\le 2^D(B+1)\max_b q_b 2^{Db}.}
]
Each term in band b lies between 2^(Db) and 2^(D(b+1)); summing and comparing to the largest band proves the inequalities. For polynomial query lengths B=O(log N), so the exponent of W_D equals the largest band-population exponent plus D times its length exponent, up to o_D(1). Any claimed uniform ARC recurrence necessarily requires
[
\sup_{|F|=N}W_D(F)\le N^{\max(11/10,3/5+D/2)+o_D(1)}
]
for every sufficiently large fixed integer D. Thus an obligatory query of length N^(1/2+epsilon) on infinitely many inputs fails the recurrence for sufficiently large D; likewise N^(3/5+epsilon) compulsory calls of length N^(1/2-o(1)). This is a **necessary** condition for the specified opaque execution architecture, not a sufficient ARC construction.

A direct faithful guest that visits (M+1)^D fresh tape cells also induces a corresponding **restricted physical guest-space** tariff; arbitrary compiler space lower bounds do not follow. Fully writing N^(3/5) ordinary children of N^(1/2) bytes already costs N^(11/10) output steps, saturating alpha=11/10. An extra compulsory positive polynomial per-byte overhead violates that specific materializing stage; polylog factors do not.

## Same-original-source SAT and UNSAT controls
For any CNF F and source variable x, SAT(F) iff SAT(F|x=0) OR SAT(F|x=1), since a witness restricts to a child and any child witness extends by x. Appending disjoint positive fresh-variable ternary clauses preserves SAT and UNSAT for every child. Original G7 (seven of eight signed ternary clauses, omitting x OR not-y OR z) has one witness 010; original G8 (all eight) is UNSAT. The two Shannon children of G7 have SAT/UNSAT labels, and both children of G8 are UNSAT. Every child is explicitly serialized as ordinary DIMACS and checked. Padding makes these **larger**, not power-short, and is not presented as a SAT speedup.

Per-source S and U all-literal extremes, inversions, source occurrence indices, the SS/SU/US/UU matrix, global 0^n and 1^n assignments, flip trails and non-tautological resolvent-forbidden cubes remain adversarial controls. Failing both endpoints does **not** certify UNSAT.

The standard UP-DPLL baseline used **11 nodes and 185 literal probes** across both sources. The 16 padded ordinary children used **140 nodes and 3,146 literal probes**, plus **1,403 physical output bytes**. The two sources contained 45 original signed occurrences, 196 clause-pair mode checks, and 21 source resolvent blockers. An independent Python verifier passed **723 checks** and rejected three injected corruptions. Five separate symbolic heterogeneous workloads, with D=2,4,8,16,32, agreed with the exact rational exponent inequalities. Host-language counters and synthetic workloads are **not native FLMV time/space measures**, nor commensurable operations.

## Full machine tariff
Charge source parsing and indexed probes, class/backdoor discovery and rejected attempts, policy switching, cache/replay, exact child materialization or complete child accessors, every query/guest and index-tape operation, proof/witness checking, physical work-tape positions and retained ancestors. Correct branch joins, certification and dynamic parameter discovery are not free. The producer does not measure all of these resources; the fully charged recurrence remains OPEN.

## Original literature and internal peer reconciliation
FLMV 2005, Theorem 5.7: https://lance.fortnow.com/papers/files/tst.pdf . Read governance redirect 2026-10-30 09:48, universal FLMV contract, AGENTS/CODEX/pnp-research skill, AFFINE-SMALLBIAS-DESCENT-GATE2, CONSTRUCTION-STRENGTHEN17, ARC-LINEAR22-SATURATION1, previous LSPV-1 UNKNOWN-EXPONENT-EPOCH274, LSPV-2 mixed Horn/Krom interface, LSPV-3 backdoor acquisition, LSPV-4 anchored index, LSPV-5 REFEREE243. The affine MCSP theorem is only a **restricted semantic no-go**. New incremental component here is the adaptive **heterogeneous band identity**, not the already known homogeneous DELAY barrier. Independent peer mathematical review is pending.

Full four-page formal LaTeX/PDF report, 10 KB producer, separate Python verifier, 80+ KB original-clause-indexed raw data, SHA-256 manifest and replay ZIP were generated locally at `/mnt/data/pnp_lspv1_275/`; the persistent Library upload failed with `container_session_unavailable`. The compact code and summary are separately committed for reproducibility; full raw/LaTeX mirror to GitHub remains pending if direct byte transfer is unavailable. No tasks, schedules, or status were modified.

**ONE LOAD-BEARING OPEN ARROW:** all-input correct, physically power-short SAT children or certified terminal decisions with exact acquisition/guest/space bounds, for arbitrary fixed correct A and unknown exponents. `P vs NP OPEN`.

END_LSPV1::ARC_QUERY_SPECTRUM275::P_VS_NP_OPEN
