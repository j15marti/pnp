# Five-role refocus: worst-case minimum logical derivation cost

**User approved: November 2, 2026, 12:04 PM PST, America/Los_Angeles.**
**Status: research allocation and conditional theorem targets, not a proof of P versus NP.**

This directive refocuses the five existing PNP agents. It supersedes incompatible older scientific priorities, especially canonical-only SAT restrictions and requiring pointwise simulation as the only acceptable bridge. Preserve task IDs, current titles, enabled states, schedules, role ownership, verified mathematics, and publication safeguards. Older paused-state descriptions are historical, not instructions. Do not activate legacy tasks or create another team.

## 1. Shared mathematical target

Work on general encoded CNF-SAT. Fix one sound, complete, effectively specified reduction system R independently of instances and input sizes. Declare encodings, legal rules, justification checks, auxiliary-variable semantics, and nonnegative weights. Ensure a minimum exists, or explicitly use an infimum throughout.

Define

    W_R(F) = min_{pi: F derives contradiction in R} cost_R(pi)
    cost_R(pi) = sum of weights of distinct inference nodes in the derivation DAG
    Wbar_R(N) = max_{F valid UNSAT, |encode(F)| <= N} W_R(F).

Use zero for a maximum over an empty set. Encoded bit length N is not the variable count n.

The target is a superpolynomial worst-case lower bound: for every k, C > 0, and N0, some N >= N0 satisfies Wbar_R(N) > C(N+1)^k. An unbounded hard family suffices; finding the exact worst instance at each size is unnecessary. Do not demand that every formula be hard, that one finite formula defeat all algorithms, or that typical-case hardness hold.

The inner minimum grants free, perfect selection of the best legal derivation. Proof-search/optimizer discovery cost is separate and is NOT an objection to a certified shortest-derivation lower bound. All adaptive rule choices, auxiliary definitions, temporary enlargement, algebraic reasoning, compact circuits, justified representation switches and shared subproofs permitted by R remain available. Do not require every state or every move to shrink. A short final semantic description is not a justified proof.

Fix the combined rule system before declaring a family hard. If R includes two subsystems, it can use either and mix them. Hardness for separate families in separate subsystems does not establish hardness for their combination. No instance-tailored answer axiom, hidden validity oracle, or unrestricted unit-cost F -> false rule is allowed.

## 2. Prioritize the weakest sufficient transfer

For a fixed uniform total correct SAT decider A, define

    T_A^wc(N) = max_{binary strings x, |x| <= N} T_A(x).

A handles SAT, UNSAT, and malformed inputs. Its code is fixed across sizes but its tactics may adapt at every step. Polynomials below may depend on A, not on F or N.

Track three DIFFERENT obligations:

**B1, stronger optional pointwise simulation:**

    for every A, there is a polynomial p_A, for every UNSAT F:
    W_R(F) <= p_A(|encode(F)| + T_A(F)).

An effective computation-to-proof translation would establish this only with an explicit soundness/correctness justification and overhead proof. Completeness alone does not establish it.

**B2, weaker worst-case domination:**

    for every A, there is a polynomial p_A, for every N:
    Wbar_R(N) <= p_A(N + T_A^wc(N)).

The inputs maximizing proof cost and runtime need not coincide. Any polynomial input-length rescaling must be stated and charged explicitly.

**B3, PRIMARY minimal sufficient conditional bridge:**

    SAT in P implies: there exist C,k such that
    for every N, Wbar_R(N) <= C(N+1)^k

for the SAME preselected system R and weight convention.

B1 implies B2, and B2 implies B3. A proved superpolynomial lower bound on Wbar_R plus a proved B3 would exclude polynomial-time SAT. These bridge statements are research targets, NOT established results. Do not assume B3 from the desired separation or a simulation conjecture. A statement that P=NP would yield SOME polynomially bounded proof system does not identify the preselected R. Distinguish proof existence/length, effective proof translation, and efficient proof search. Explain any reflection principle or machine-correctness assumption. An accepting or rejecting machine trace alone is not a sound UNSAT certificate for an arbitrary program.

## 3. Correct counterexample classification

Label failures precisely:

* FAMILY FAILURE: a short permitted R-derivation defeats a proposed hard family.
* POINTWISE-TRANSFER FAILURE: some correct A is fast on a family with large W_R, refuting B1.
* WORST-CASE-TRANSFER FAILURE: evidence actually contradicts B2, including the algorithm's worst-case runtime on all inputs.
* CONDITIONAL-BRIDGE GAP/FAILURE: identify an unsupported step in B3 or a justified conditional countermodel; do not confuse failure to prove it with a mathematical refutation.

The established parity recognizer plus exhaustive fallback refutes B1 for ordinary resolution. It does NOT by itself refute B2 or B3, because its global worst-case runtime can be exponential. Easy inputs or recognizable easy families do not refute a worst-case lower-bound program. They remain essential controls for overly strong claims.

## 4. Five complementary assignments

| Agent | Existing task ID | Immediate research responsibility |
|---|---|---|
| PNP General SAT Lower-Bound Lead | 6ad6f02da1bc8191bfd844daded8e1ec | Own Wbar_R, quantifier order, and B1/B2/B3 implications. Prioritize B3 for a fixed R; audit whether known wrapper/trace/reflection results genuinely supply it, and separate conditional restatement from new proof. |
| PNP SAT-Circuit Reduction Builder | 6ad6f04620a881918aecb8078ce2f2d1 | Implement the fixed combined calculus and independently checkable shortest-DAG certificates. Search finite extremal UNSAT instances, then develop sound hardness-transport constructions without hidden gates, conversion or correctness oracles. |
| PNP Hypergraph & Proof Certificates | 6ad6f05603248191abb281a5b43b3fc2 | Construct growing hard families and invariants valid for EVERY permitted mixed-system derivation. Go beyond the tight linear source-arity bound; test width/cut/potential arguments against algebraic and compact-circuit escapes. |
| PNP Time-Space Resource Auditor | 6ad42a1f03448191b8ded0c1f2dfa791 | Audit weights, encoded evidence size, computational domination direction, input-size rescaling, and separate DAG cost from scheduled machine work/space. Enforce all-phase peak-space costs for any implemented upper bound or FLMV transfer. |
| PNP Independent Proof Red Team | 6ad42a2a9a088191ab9042245f3b4393 | Independently test hard-family claims and each bridge at its correct quantifiers. Try mixed-rule shortcuts, semantic oracles, nonuniform axioms, uncertified machine correctness, and accidental replacement of worst-case claims by pointwise ones. |

The current hourly offsets remain :00, :12, :24, :36, :48 in America/Los_Angeles. This handoff itself does not assert scheduler mutation success; actual task updates require separate readback.

## 5. Preserved controls and accounting

Preserve the latest minimum-cost-DAG definition, general-SAT scope, and all verified restricted lemmas. Keep parity/Tseitin odd/even controls; Horn/2SAT; high-rank equality with compact descriptions; one-boundary guarded SAT; sign-sensitive minimal UNSAT; tiny cores; variable renaming; lazy encodings; temporary growth; DELAY/COPY/RECOMP; and same-source opposite-label cases when relevant. Independently reject malformed inputs and corrupted certificates.

Free proof selection does not make a computational-weight interpretation automatic. Record node count, encoded proof/statement size, and verification work separately. Prove any relation used to infer machine work. Shared derivations count once in the logical DAG; storage, retrieval, and recomputation require a separate execution schedule. Logical-state XOR remains an offline diagnostic, not an arbitrary-machine hardness invariant.

For solver upper bounds and time-space transport charge parsing, source/index/head access, rule validation, policy discovery, failed attempts, switching, conversion, child materialization/access, proof checking, output, caches, all guests, and simultaneously live ancestors. Retain the corrected materialized-child space envelope

    s' <= max{rho, eta, lambda, lambda*s},

where rho bounds EVERY local phase. Allocating N bits and freeing them before child calls still gives rho >= 1. Retain FLMV only as a separately justified, same-machine conditional route; do not infer numerical margins from NP-completeness or shortest-proof size.

## 6. Every-run deliverable and publication

Read this directive first, then current issue #3, peer handoffs, AGENTS.md, CODEX.md, repository pnp-research skill and materially relevant original reports/code. Latest user-approved scope overrides older conflicting governance science, not ownership or safety rules.

Propose 2-4 precise falsifiers. Search current primary literature and relevant project history, including github.com/openai where relevant; log queries, sources, duplicates and access failures. Then prove/falsify one substantive lemma, build one rigorous candidate, or certify one finite optimum. Do not substitute repeated generic cautions for a concrete attempt.

Report: fixed R and weights; exact quantifiers; proved/known/computational/conditional/open status; both-label and malformed controls; what the certified minimum covers; lower-bound cost versus optimizer cost; which bridge is addressed; and the next missing implication. Do not relabel an upper bound as a lower bound or extrapolate finite optima to asymptotics.

Publish dated report/code/raw to existing role-owned paths, with exact outbox, current-head conflict-safe writes and full readback or an explicit documented fallback. Update coordination issue #3 and relevant handoffs. Reconcile main.tex only within authorized ownership and never overwrite a partial large-file response. Preserve all prior artifacts. Administrative refocusing does not require rewriting the mathematical manuscript.

P versus NP remains OPEN. No new theorem or experimental result is asserted by this allocation change.

## LSPV-2 result 341: bridgeless cubic odd-Tseitin exact mixed-DAG optimum (2026-11-02 12:16 PST)

**Status: PROVED/EXACT within fixed Rmix341; independent finite computational replay. P versus NP OPEN.** For any connected simple bridgeless cubic graph with h vertices and odd charge, its general 3-CNF Tseitin encoding has exactly 4h indispensable source clauses. A source-arity argument proves **W_Rmix341(F)>=4h-1** for every binary-premise, unit-cost, conservative derivation DAG, including shared proofs, charged auxiliaries and temporary growth. The fixed combined calculus includes sound binary resolution, exact constant-three-variable truth-table conjunction/normalization, binary GF(2) row addition, local conversions and conservatively charged auxiliary gates, with every new node charged. A matching proof conjoins four local clauses in three binary steps per vertex, then XOR-adds h rows in h-1 more steps, yielding **W_Rmix341(F)=4h-1**. This is a *global minimum in this R* with no optimizer-depth cutoff; no arbitrary machine decision lower bound follows.

Independent verifier: **30,714 checks**, six global optima on K4 / K3,3 / cube / Petersen / prism6 / prism16 (15,23,31,39,47,127 nodes), all-source-deletion SAT witnesses, even-charge SAT controls, malformed and corrupted-proof rejections. A graph with a bridge has only 36/40 independently essential clauses, so its exhibited 39-node proof is an upper bound without a minimum certificate. A four-premise unit-cost XOR extraction in a *different* calculus would shorten the constructed proof to 2h-1, showing system dependence. Known exponential resolution lower bounds on suitable Tseitin expanders do not survive this mixed affine system; no worst-case B2/B3 failure is claimed.

Published, producer and independent verifier re-executed exactly from GitHub readback:
- [Report](../agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex)
- [Code](../../experiments/arc/lspv2_341_mixed_tseitin_min_dag.js) and [independent verifier](../../experiments/arc/lspv2_341_independent_verify.js)
- [Raw proof/source witnesses](../../results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json) and [verification record](../../results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341_independent.json)

**Next exact gap:** exhibit any growing superlinear or superpolynomial W_Rmin in the same combined calculus, versus a general nonaffine family and a proven hardness-transport lower-bound direction. B3 remains unproved and is not supplied by the present infinite sharp linear family.

<!-- BEGIN LSPV4 WORSTCASE DELAY BRIDGE341 -->
## LSPV-4 resource audit: B2 single-decider slowdown does not imply B1 (2026-11-02, 12:37 PST)

**PROVED/EXACT using Haken (1985), finite controls COMPUTATIONAL, universal B2/B3 OPEN.** Fix ordinary DAG resolution R (unit weight per distinct non-tautological binary resolvent). Since there are at most 3^n clauses over n appearing variables, for binary encoded length N, Wbar_R(N)<=3^N. Construct one uniform correct all-CNF decider A_slow recognizing canonical pigeonhole PHP_k in polynomial time; on every other string of length N it runs a genuine 2^N-step DELAY and then correctly solves/rejects the input. On malformed 1^N, T_A^wc(N)>=2^N, hence **B2 for this individual A** holds with p(z)=z^2 for every N. However Haken's exponential DAG-resolution lower bound on PHP_k, whose encoded size is polynomial in k and which A_slow recognizes quickly, makes **B1 for that same A** false for every polynomial bound. This does **not** refute universal B2 or B3; it audits their quantifiers and the need to avoid artificial worst-case slack.

An independent no-import Node verifier passed 8,651 assertion groups, checking PHP k=1,2,3 (0 UNSAT models; 1,2,6 SAT sign-flip-neighbor models), sound resolution DAGs of 2/10/43 derived nodes (only 2 is certified minimum), eight malformed fixtures and corrupted-proof rejection. Declared dense proof-stream bits: 28/270/1892, not minimum physical evidence across encodings. Real DELAY needs an N-bit local counter, so all-phase rho>=1; no square-root-space FLMV transfer.

[Role-owned report](../agents/lspv-4/2026-11-02_1237_LSPV-4_WORSTCASE_DELAY_BRIDGE341.md); [compact code](../../experiments/arc/lspv4_341_worstcase_delay_compact.py); [machine-readable results](../../results/raw/arc/2026-11-02_1237_LSPV4_WORSTCASE_DELAY_BRIDGE341_summary.json). **No task identity/state/schedule changed, P versus NP OPEN.**
<!-- END LSPV4 WORSTCASE DELAY BRIDGE341 -->


<!-- BEGIN LSPV5 B1-B2 VALID-SENTINEL REFEREE295 -->
## LSPV-5 result REFEREE295: valid-SAT slowdown separates the per-decider B2/B1 inequalities (2026-11-02 12:48 PST)

**PROVED/EXACT for fixed source-axiom Resolution+Weakening; system-restricted; P versus NP OPEN.** Every v-variable UNSAT CNF has a blocking-clause refutation of cost at most 2^(v+1)-1. A fixed total correct decider parses/rejects malformed inputs, delays 2^(L^2) charged steps on a dense family of valid SAT sentinels of exact encoded lengths L=6k+3, solves authenticated odd Tseitin systems by GF(2), and uses exact exhaustive fallback elsewhere. On expander Tseitin, the decider is polynomial while shortest Resolution+Weakening proofs are superpolynomial, so its individual B1 inequality fails. The unrelated valid-SAT delay dominates Wbar_R(N)<2^(N+1), so the individual inequality used in B2 holds for this same decider.

**Quantifier firewall:** this proves B2(A-dagger) and not B1(A-dagger). It does **not** prove global B2, which quantifies over every correct decider, and therefore does not establish strictness of the global B1=>B2 implication. It independently reproduces concurrent LSPV-4 result 341 while strengthening its hostile control: malformed strings are not used to inflate worst-case time. It does not refute B3, because the decider is deliberately superpolynomial. XOR reasoning collapses the Tseitin family, so no representation-inclusive lower bound follows. Sixteen SAT sentinels, complete blocking UNSAT controls through six variables, four malformed strings, and an independent 29-check verifier passed; 151 envelope lengths were generator-attested.

[Report](../main/2026-11-02_1248_MAIN_WORST-CASE-RUNTIME-POLLUTION-REFEREE295.md); [code](../../experiments/arc/lspv5_295/b1_b2_separation_referee295.py); [independent verifier](../../experiments/arc/lspv5_295/verify_b1_b2_separation_referee295.py); [raw](../../results/raw/arc/2026-11-02_1248_LSPV5_B1_B2_SEPARATION_REFEREE295_raw.json).
<!-- END LSPV5 B1-B2 VALID-SENTINEL REFEREE295 -->
