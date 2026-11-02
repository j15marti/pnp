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
