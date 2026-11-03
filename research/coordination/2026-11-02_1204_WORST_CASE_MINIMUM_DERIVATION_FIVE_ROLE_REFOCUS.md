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


<!-- BEGIN LSPV3 PROVENANCE KRAFT342 -->
## LSPV-3: exact shared-DAG provenance-read optimum, November 2, 2026, 12:49 PST

**PROVED/EXACT, fixed Rmix341 rules with a separately declared explicit-source-list input-read weight; independently checked finite controls. General P versus NP OPEN.** For every sound conservative at-most-binary-premise proof DAG of clause-minimally UNSAT $m$-clause $F$, define source ancestry $\sigma(s_j)=\{j\}$ and $\sigma(v)=\bigcup_{u\in\mathrm{parents}(v)}\sigma(u)$. Charge each derived node $\max\{1,\sum_{u\in\mathrm{parents}(v)}|\sigma(u)|\}$ source-ID input reads. One source-authenticated root-to-leaf path for every indispensable clause defines $m$ distinct prefix-free binary words, even with DAG reconvergence. Kraft/Huffman gives the **universal weighted minimum lower bound**
\[
W_{\rm src}(F)\ \ge\ L(m)=m\lfloor\log_2m\rfloor+2(m-2^{\lfloor\log_2m\rfloor}).
\]
This is explicitly a **materialized source-support scan** model, not arbitrary-machine work. A fixed-width $b=\lceil\log_2(m+1)\rceil$ source-ID convention gives $bL(m)$ bit scans. This strengthens the old tight linear source-fan-in bound **only within the declared weighted representation**.

For the growing minimally UNSAT odd cubic Tseitin graphs $K_4$, prism$_k$ ($k\ge3$, $h=2k$), the existing fixed **mixed** Rmix341 (binary AND3, XOR and resolution, conservative auxiliaries) realizes a balanced local-four-clause AND tree followed by a Huffman-balanced XOR tree. Thus both minima are globally attained:
\[
W_{\rm unit}(F_h)=4h-1,\quad W_{\rm src}(F_h)=L(4h),\quad W_{\rm bits}(F_h)=\lceil\log_2(4h+1)\rceil L(4h).
\]
There are $m=4h$ clauses, $n=3h/2$ variables, and signed ASCII DIMACS length $N(h)=\Theta(h\log h)$. Consequently the first weighted minimum is $\Theta(N)$ and the explicit-bit-scan minimum $\Theta(N\log N)$; lazy pointers/compact XOR eliminate the claimed necessity of explicit provenance reads. No superpolynomial $W_{\rm mix341}$ lower bound or B3 implication follows.

**Finite verification:** seven $h=4,6,8,10,16,20,40$ cases, exact weighted read volumes $64,112,160,216,384,512,1184$, full 416 clause-deletion SAT witnesses on the same odd originals; even-charge SAT counterparts; exhaustive paired label counts for $h\le8$: $(0,8),(0,16),(0,32)$; and nine malformed/corrupted certificate rejections. Independent verifier reconstructs source local parity, every AND/XOR edge, ancestry and reading weight. Both programs were evaluated against GitHub readback; separate container curl failed on DNS resolution, with no unsupported native-host benchmark claim.

Artifacts, GitHub readback verified:
- [Role-owned formal report](../agents/lspv-3/2026-11-02_1249_LSPV-3_PROVENANCE_KRAFT342.tex)
- [Producer](../../experiments/arc/lspv3_342_provenance_kraft.js)
- [Independent verifier](../../experiments/arc/lspv3_342_independent_verify.js)
- [Raw exact proof archive](../../results/raw/arc/2026-11-02_1249_LSPV3_PROVENANCE_KRAFT342.json)

**Next gap:** find a nonaffine hard UNSAT family and a superpolynomial invariant robust under \emph{all} Rmix341 rules and compact representations. B3 for the same preselected R is still OPEN. Root main.tex was fetched but returned 0 content with a SHA; no owner-region rewrite was risked. Existing task identity/state/schedule unchanged.
Additional independent general-DIMACS input-grammar audit: [parser code](../../experiments/arc/lspv3_342_dimacs_controls.js), 14 generated odd/even source roundtrips, two valid edge cases, ten malformed strings rejected; totals stored in the raw JSON. This is grammar testing, not a universal SAT decider.
Explicit stronger-rule falsifier: extending to a single four-premise local XOR-row extractor at charge equal to the four source-list entries gives $4h+4L(h)=L(4h)-4h$, e.g. $48<64$ at $h=4$. The binary-premise Kraft bound is therefore not invariant under uncharged fan-in enlargement; this does not affect the fixed Rmix341 optimum.
<!-- END LSPV3 PROVENANCE KRAFT342 -->


<!-- BEGIN LSPV3 BPHP EXTENSION343 -->
## LSPV-3 BPHP-EXTENSION343 (November 2, 2026, 13:24 PST)

**PROVED/EXACT (conditional on established Cook--Reckhow polynomial ER PHP family), COMPUTATIONAL finite checks; new unreviewed 2026 literature item. P versus NP OPEN.** The standard bit-pigeonhole CNF with n=2^ell holes and n+1 pigeons has M=n*binom(n+1,2) essential clauses, 2ell M sensitive literal signs, and actual ASCII DIMACS encoded bits N=Theta(n^3 ell^2). Every source clause has an explicit deletion-SAT witness (only its designated pigeon pair collides in its designated hole).

**Crucial combined-system FAMILY FAILURE:** In the *already fixed* Rmix341 with charged conservative two-input DEF and binary RES, introduce every pigeon-prefix indicator p(i,s) using O(n^2) gates; derive unary PHP totality and collision clauses from binary originals via O(n^3 ell^2) source-authenticated RES steps; append Cook--Reckhow polynomial Extended Resolution PHP refutation. Therefore W_Rmix341(BPHP)<=n^O(1). A full generic ER proof compiler is not yet emitted, and defining clauses' accessibility is an explicit rule assumption. Sign sensitivity and indispensable sources DO NOT imply hard mixed proofs.

**New primary literature:** Kamil Braun, September 19 2026 preprint arXiv:2609.23015 claims > exp(n/(32768 ell^2)) unrestricted depth-free DAG Res(oplus) proof nodes (including sources), ell>=32, linked Lean 4 formalization. Not independently executed/peer-reviewed here. Subtracting M source nodes, if valid, yields superpolynomial worst-case Wbar for a fixed *restricted* Res(oplus) calculus, but extensions in Rmix341 defeat this same family. Neither B2 nor B3 transfers.

**Independent small controls:** ell=1,2,3; source counts 6/40/288; encoded bits 416/4064/48488; 334 same-source deletion-SAT witnesses, 1900 sign-flip SAT witnesses, 19096 local binary/unary equivalence checks, 30 malformed DIMACS rejects, 6 corrupted fixtures. Independent Node checked 103953 assertions. GitHub readback JS producer replay matched the raw totals. See [role report](../agents/lspv-3/2026-11-02_1324_LSPV-3_BPHP_EXTENSION343.tex), [code](../../experiments/arc/lspv3_343_bitphp_extension.js), [independent verifier](../../experiments/arc/lspv3_343_independent_verify.js), [raw](../../results/raw/arc/2026-11-02_1324_LSPV3_BPHP_EXTENSION343.json) and [full handoff](2026-11-02_1324_LSPV3_BPHP_EXTENSION343_HANDOFF.md).

**Next gap:** a superpolynomial minimum for a nonaffine family robust to conservative ER extension in *one fixed full combined R*, and an independently justified B3 for that same R. Historical claims preserved; root main.tex fetch returned zero text with SHA, so not risked.
<!-- END LSPV3 BPHP EXTENSION343 -->


## LSPV-2 verified finite result 342: strict mixed nonaffine DAG gap (2026-11-02 13:16 PST)

**PROVED/EXACT under preselected binary-premise Rmix341; independent computational verifier. P versus NP OPEN.** A four-variable six-clause minimally UNSAT general CNF G has exact mixed-calculus minimum W_Rmix341(G)=6, strictly above its essential-source lower bound m-1=5. Proof: all six source clauses are indispensable (single-deletion SAT model counts 1,3,3,3,1,1); with only five at-most-binary-premise inferences every source must occur exactly once in a source-disjoint binary tree. A COMPLETE 63-subset truth-mask dynamic program, allowing FREE sound exact aliasing among clause/three-variable factor/GF(2) representations, enumerated all five-node combined-rule trees and excluded false in its 54 terminal states. This stronger-relaxation exclusion is a global lower certificate, not an optimizer cutoff. Six independently checked ordinary-resolution inferences reach contradiction, giving matching upper certificate. A second minimally UNSAT H has W_resolution(H)=6 but W_Rmix341(H)=5 via three-variable factor conjunction plus one resolution, demonstrating a real mixed-system shortcut. The finite extremal sample (seed 3422026, 30,000 draws) is NOT an exhaustive maximum or a growing lower bound.

Controls: independent 345 assertion groups, 36 renamings/complements, eight malformed-DIMACS rejections, three corrupted-proof rejections, original SAT neighbors and guarded opposite-label, parity odd/even, Horn, high-rank equality. Logical six-node minimum is distinct from 844 semantic optimizer operand tests, proof serialization/checking and all-phase peak memory. Github report: research/agents/lspv-2/2026-11-02_1316_LSPV-2_MIXED_NONAFFINE_GAP342.tex; compact executable: experiments/arc/lspv2_342_compact.js; source/certificates: results/raw/arc/2026-11-02_1316_LSPV2_MIXED_NONAFFINE_GAP342.json. No superpolynomial Wbar_R(N) or B3 transfer is proved; P versus NP remains OPEN.

<!-- BEGIN LSPV4 NODE-EVIDENCE-DOMINATION342 -->
## PNP Time-Space Resource Auditor: NODE-EVIDENCE-DOMINATION342 (2026-11-02, 13:33 PST)

**PROVED/EXACT, fixed encoding only; independently COMPUTATIONAL. P versus NP OPEN.** For the previously fixed binary-premise mixed Rmix341 calculus (RES, constant-support AND3/LOCAL-CONVERT, binary XOR, charged conservative two-input DEF with one new variable per node), every q-node refutation uses at most n+q variables. Each derived line can be encoded in at most 2K+8 ceil(log2 K)+64 bits, K=N+q+2, by dense signed clause masks, affine masks, parent/source indices and bounded local factor/gate data. Consequently, for one fixed declared certificate encoding,
```
W_R(F) <= L_R(F) <= C(N+W_R(F)+2)^2,
Wbar_R(N) <= Lbar_R(N) <= C(N+Wbar_R(N)+2)^2.
```
This validates node count as a polynomially equivalent **encoded-proof-length** metric within this particular calculus. It does not make W_R a compulsory resource of arbitrary SAT deciders, prove any of B1/B2/B3 or furnish native FLMV work.

**FALSIFIER:** Adding a fixed, explicit TABLEAU rule (one inference supplying a false-source-clause index for each assignment) is sound, complete and polynomial-checkable in *certificate length*, but has Wbar<=1 while one step can require 2^n ceil(log2(m+1)) evidence bits and 2^n checks. It is excluded from the accepted unit-weight hardness calculus: a justified semantic inference is not automatically a constant-time machine operation. The padded unit contradiction at n=16 occupies 140 source ASCII bytes and 327,680 explicit TABLEAU evidence bits.

Independent Python/no-import Node controls: 10 SAT/UNSAT sources, K4 odd/even (0/8 solutions), eight malformed source rejections, 16 same-original source-deletion SAT witnesses, corrupted-cert rejection, 198 independent assertion groups. A K4 odd mixed proof with 12 AND3 plus 3 XOR nodes independently verifies the previously known exact 15-node optimum; no superlinear mixed hardness is inferred.

[Formal report](../agents/lspv-4/2026-11-02_1333_LSPV-4_NODE_EVIDENCE_DOMINATION342.tex), [standalone JS reproducer](../../experiments/arc/lspv4_342_node_evidence_compact.js), [public raw](../../results/raw/arc/2026-11-02_1333_LSPV4_NODE_EVIDENCE_DOMINATION342_summary.json). Full producer, independent JS verifier, proof DAG, raw and hashes in the user-facing reproducibility archive. Root main.tex authenticated fetch returned empty content despite nonempty SHA; root left unchanged to preserve other agents' bytes.

**Exact next gap:** A superpolynomial Wbar for one fixed representation-inclusive calculus together with B3 for that same calculus. Free choice of best proof remains legitimate. All-phase local space rho, machine source/index/head, conversions, scheduling and simultaneous peak must still be charged. No task identity/state/schedule changes.
<!-- END LSPV4 NODE-EVIDENCE-DOMINATION342 -->


<!-- BEGIN LSPV5 BLACK-BOX RELATIVIZATION REFEREE296 -->
## LSPV-5 REFEREE296: unchanged-calculus relativization firewall (2026-11-02 13:48 PST)

**PROVED/EXACT method barrier; PROVED/CONDITIONAL sufficient bridge; P versus NP OPEN.** If a fixed ordinary calculus R has superpolynomial Wbar_R, no B3 proof can fully relativize the SAT solver while leaving R ordinary and unchanged. For a Baker--Gill--Solovay oracle O with P^O=NP^O, ordinary SAT is in P^O, while ordinary R-derivations and Wbar_R are unchanged. A fully relativizing B3 implication would contradict the assumed lower bound. This does **not** falsify ordinary B3; it proves that a successful bridge must use nonrelativizing ordinary-code/correctness structure or a stronger proof-system hypothesis.

Independently verified LSPV-1 CLOCKED-OPTIMALITY-REFLECTION336: if the same ordinary R is size-optimal among ordinary Cook--Reckhow UNSAT proof systems and node cost is polynomially dominated by proof length, then unary-clock verification yields B1 for every fixed total correct ordinary decider. This survives the firewall because an oracle decider yields an oracle verifier, outside ordinary size optimality. Forged-transcript, changed-calculus, size-optimality and scope-overclaim falsifiers were applied. SAT, two UNSAT, six malformed, corrupted-proof and missing-evidence controls passed; independent verifier checked 34 assertion groups.

[Report](../main/2026-11-02_1348_MAIN_BLACK-BOX-RELATIVIZATION-FIREWALL-REFEREE296.md); [handoff](2026-11-02_1348_LSPV5_TO_FIVE_ROLE_BLACK_BOX_RELATIVIZATION_REFEREE296.md); [code](../../experiments/arc/lspv5_296/black_box_relativization_referee296.py); [raw](../../results/raw/arc/2026-11-02_1348_LSPV5_BLACK_BOX_RELATIVIZATION_REFEREE296_raw.json).

**Next gap:** a superpolynomial Wbar lower bound and an ordinary nonrelativizing B3 bridge for the same preselected representation-inclusive mixed calculus.
<!-- END LSPV5 BLACK-BOX RELATIVIZATION REFEREE296 -->


<!-- BEGIN LSPV2 LOW-SUPPORT-MINCORE343 -->
## LSPV-2 LOW-SUPPORT-MINCORE343 (2026-11-02, 14:18 PST): exact small-support global optimum

**PROVED/EXACT for the unchanged fixed Rmix341; COMPUTATIONAL independent finite audit.** Let mu(F) be the smallest UNSAT source-labelled subformula cardinality. For every general UNSAT CNF whose original-variable support has at most three variables, the global free-choice refutation DAG optimum is **W_Rmix341(F)=mu(F)-1**. Lower: any sound conservative binary-premise q-node refutation has at least mu source ancestors and q>=mu-1 by connected dependency edge counting. Upper: a sequential AND3 tree on a minimum core uses mu-1 legal exact local truth-table conjunctions and ends in false. Shared DAGs, conservative auxiliaries, algebraic rows and temporary growth are already covered by the lower bound. An indispensable-clause deletion-witness injection gives mu<=2^r, r<=3, so the exact global worst case over **all** UNSAT CNFs on at most r original variables is 2^r-1, attained by the complete assignment-blocking cube: r=0,1,2,3 yields 0,1,3,7 derived nodes. This maximum is over the entire syntactic class of variable-support at most three, not a random sample and not Wbar_R(N) for unbounded r.

**Essential limitation:** the already verified four-variable six-clause G342 has mu=6 and W_Rmix341(G)=6>5, so extending equality to growing support is false. The result is a bounded-support family-hardness escape, not a contradiction to B2/B3. It does not prove a superpolynomial bound or any unconditional SAT separation.

**Controls:** independent no-import JS verifier 5,238 assertions, 885,507 enumerated source-subset masks, 165 checked AND3 proof nodes; 278 exhaustive cube subfamilies, 400 seeded random general 0/1/2/3-CNF fixtures (280 UNSAT, 120 SAT), 72 signed renamings, ten malformed encodings rejected and eight corrupted proof DAGs rejected. Odd/even XOR, Horn, 2SAT, empty-core and duplicate-clause controls passed. Logical node counts are separate from input access, the 256-mask source-core optimizer, proof serialization/checking and peak host space.

**Artifacts (verified GitHub readback):** [report](../agents/lspv-2/2026-11-02_1418_LSPV-2_LOW_SUPPORT_MINCORE343.tex), [standalone compact reproducer](../../experiments/arc/lspv2_343_compact.js), [public raw and hashes](../../results/raw/arc/2026-11-02_1418_LSPV2_LOW_SUPPORT_MINCORE343.json). Full Python producer, independent JS verifier and 416 KB raw results are in the companion local reproducibility archive.

**Next:** pursue a growing-support **combined-calculus** lower bound and the separate ordinary, nonrelativizing weakest B3 bridge; P versus NP OPEN. No task identity/state/schedule changes.
<!-- END LSPV2 LOW-SUPPORT-MINCORE343 -->


<!-- BEGIN LSPV4 FLMV-MARGIN-OUTPUT-STREAM343 -->
## LSPV-4 343: sharp conditional FLMV robustness and output retention (2026-11-02 14:36 PST)

**PROVED conditional algebraic margin theorem and model-specific allocation falsifiers; COMPUTATIONAL finite checks; B1/B2/B3, splitter and same-machine FLMV transfer OPEN.** For sequential child count N^a, child length N^b, aggregate local time N^d, all-local-phase peak N^rho, retained state N^eta, an actually implemented repeatable transformation would obey exponent envelope t'<=max(d,a+bt), s'<=max(rho,eta,b,bs); limits are t*=max(d,a/(1-b)), s*=max(rho,eta,b). These are bounds on a HYPOTHETICAL transformed SAT machine, not a bridge from W_R to arbitrary-decider runtime.

For beta(c)=((c+2)/c^2-c)/2 and baseline a=3/5,b=1/2,d=11/10,rho=eta=1/2, t*=6/5, s*=1/2 and beta(t*)-s*=1/90. The unique ccrit>1 solving c^3+c^2-c-2=0 is 1.2055694304005903. Holding other exponents fixed, a positive fanout exponent increase must stay below 0.0027847152, child-length increase below 0.0023098754, local-time increase below 0.10556943; N^gamma per-child source access requires gamma<0.60556943. A source scan of N bits for all N^.6 children costs N^1.6, and an N-bit temporary writable source copy forces all-phase rho>=1. Eagerly retaining q=N^.6 one-bit answers sets eta>=.6, and materializing all q child descriptions of N^.5 bits uses N^1.1 writable bits. Online OR or AND aggregation can instead retain a single result bit, conditional on paid sequential child generation and correct combination.

Independent pure-Python and no-import Node controls: 78 Node assertions PASS, source-minimal 3-clause UNSAT has exact two-node binary-premise resolution optimum and SAT sign-flip neighbor with one model; odd/even K4 Tseitin controls 0/8 models; eight malformed DIMACS encodings rejected. Allocation schedules reported for N=10^4,10^6,10^8. Logical source/answer bit counts are not host heap, native FLMV or proof of general hardness. No shortest-proof optimizer is charged to W_R; all actual solver-policy/guest/source/index/head costs remain chargeable. P vs NP remains OPEN.

[Role-owned report](../agents/lspv-4/2026-11-02_1436_LSPV-4_FLMV_MARGIN_OUTPUT_STREAM343.md), [standalone JS producer](../../experiments/arc/lspv4_343_margin_stream_compact.js), [public raw](../../results/raw/arc/2026-11-02_1436_LSPV4_FLMV_MARGIN_OUTPUT_STREAM343_summary.json). Complete local independent Python+Node, raw, hashes in dated reproducibility archive. No task changes.
<!-- END LSPV4 FLMV-MARGIN-OUTPUT-STREAM343 -->


<!-- BEGIN LSPV5 ORACLE NO-REPEAT RANK REFEREE297 -->
## LSPV-5 REFEREE297: exact noisy-oracle no-repeat rank (2026-11-02 14:48 PST)

**PROVED/EXACT sampling theorem; not a SAT lower bound; P versus NP OPEN.** For a unique witness, independent effective correct-bit probability q, and successive product-weighted assignment sampling without replacement,
[
E[R]=1+sum_{d=1}^n {nchoose d}rac{r^d}{1+r^d},quad r=(1-q)/q,
]
and
[
(q^{-n}+1)/2le E[R]le q^{-n}.
]
Thus never repeating an assignment improves iid witness sampling by at most a factor of two. Every fixed q<1—including 99.5%—remains exponential; polynomial expected rank needs q=1-O(log n/n), plus polynomial paid acquisition of witness-correlated advice.

This sharpens the existing F15 oracle/nogood experiment rather than duplicating it. If stated p means “oracle-correct, else fair random,” q=(1+p)/2. At n=9, p=66/75/90/95/99% gives exact expected ranks 4.969/3.150/1.563/1.250/1.046, explaining the finite speedup. The million-check crossings are n=75/104/270/546/2757. UNSAT has no correct witness bits. A unique-unit SAT control is source-easy and its UNSAT sibling has a one-node Resolution proof, so proposal work is not W_R. B1, global B2 and B3 remain OPEN.

Controls: one-model SAT, zero-model UNSAT, six malformed, 60 exact rows, ten exact thresholds; independent verifier passed 269 assertion groups. [Report](../main/2026-11-02_1448_MAIN_ORACLE-NO-REPEAT-RANK-REFEREE297.md); [handoff](2026-11-02_1448_LSPV5_TO_FIVE_ROLE_ORACLE_NO_REPEAT_RANK_REFEREE297.md); [code](../../experiments/arc/lspv5_297/oracle_no_repeat_rank_referee297.py); [raw](../../results/raw/arc/2026-11-02_1448_LSPV5_ORACLE_NO_REPEAT_RANK_REFEREE297_raw.json).
<!-- END LSPV5 ORACLE NO-REPEAT RANK REFEREE297 -->

## LSPV-2 344 cross-role calculus and weight firewall (November 2, 2026, 15:32 PST)

**PROVED/EXACT within fixed declared rule/weight models, independent finite verification; B3 and P versus NP OPEN.** LSPV-2 Rmix341 charges every binary-premise inference one unit. LSPV-3 guarded-expander Rmix1 permits four-premise PARITY4 extraction in ONE unit. These are different fixed systems: odd K4 Tseitin has the historical exact 15 under binary Rmix341, but the unit-cost combined rule set has a checked **seven-node** proof (four PARITY4 extracts and three XOR additions). Hence 15 is NOT the minimum of the unweighted union. A general indispensable-source accounting lemma for any sound conservative proof DAG with explicit r-premise nodes and fixed weights w(r)>=max(1,r-1) proves W>=mu(F)-1, including sharing, growth and auxiliaries. Under these predeclared arity-compensated weights, the same K4 proof costs 4*3+3=15, matching the lower bound. This is a WEIGHT-CHOICE proposal, not authorization to silently change the lead's shared R: **all five roles must name an identical fixed calculus and weight convention before reporting unified optima.**

Exact additional selector theorem: Sel_z(F)=AND_i(z OR C_i) AND AND_i(NOT z OR C_i) obeys mu(Sel_z(F))=2mu(F) for every UNSAT F. If F is source-minimally UNSAT with a source-once m-1-node Resolution tree, then W_weighted(F)=m-1 and W_weighted(Sel_z(F))=2m-1. All-assignment blocker instances n=1..5 were fully audited. For nonaffine G342, only 11<=W_weighted(Sel(G342))<=13 is currently certified, not an exact guarded optimum. This is linear source-core accounting, NOT a superpolynomial bit-length lower bound, not a B3 transfer, and not general hardness transport without restriction-closure.

Independent no-producer-import verifier: 2,859 assertions, 39,924 complete assignment evaluations, 333 proof nodes, 26 rejected malformed/corrupt controls. The fully detailed local producer/checker archive is retained in the run; public GitHub artifacts passed full contents readback: [report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-11-02_1532_LSPV-2_FANIN_WEIGHTED_UNION_GUARD344.tex), [compact executable](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv2_344_fanin_union_guard_compact.js), [source-labelled K4 raw proof](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-02_1532_LSPV2_FANIN_WEIGHTED_UNION_GUARD344_public.json). Root reconciliation remains an independently checked ownership operation. No tasks or schedules changed; P versus NP remains OPEN.


<!-- BEGIN LSPV4 SPACE-CAPPED-PORTFOLIO344 -->
## PNP Time-Space Resource Auditor: SPACE-CAPPED-PORTFOLIO344 (2026-11-02 15:44 PST)

**PROVED/EXACT only in a declared fixed-guest, indexed read-only-input multitape scheduling model; COMPUTATIONAL host controls; all-input B1/B2/B3 and P versus NP OPEN.** Starting from LSPV-1 MOVING-DECIDER-MINIMAX338, take any fixed finite family of total correct SAT deciders and a computable all-phase writable cap B(N). Persistent geometric blocks of 1,2,4,... additional guest steps, with one shared active input-index port and fully charged O(B) index save/restore per guest activation, give for inputs with at least one B-space-feasible decider of time T*: T_port=O_m(N+C_B(N)+T*+B(1+log(T*+1))), S_peak=O_m(B+log(N+T*+2)). All failed guests, source queries, dormant ancestor/index tapes, and code dispatch are included. This is not a theorem about the exact FLMV matched machine without a separately proved simulation.

**NEW EXACT TOTALITY FALSIFIER:** Correct deciders may allocate and retain 2N writable cells before brute-force SAT. Any finite portfolio of such correct deciders fails the B=sqrt(N) cap even on trivial SAT, UNSAT, malformed inputs. Its output must be UNRESOLVED or a separately charged complete fallback. A fallback that allocates N writable bits, even if freed before guest calls, has all-phase rho>=1. Therefore the finite correct-program portfolio lemma alone does not yield a sqrt-space all-input decider or B3, and mixing minimum time of one guest with minimum space of another is invalid.

**Charged scheduling sensitivity:** symbolic N=10^6, B=10^3, m=3, T*=10^4 gives <60000 guest steps, <=90000 block-index copied bits versus 60000000 copied bits for a declared naive flat one-step switch, dormant guest buffer <=3000 bits plus active index/counters. These are upper-budget calculations, NOT native FLMV benchmarks. A Python producer plus no-import Node referee independently verified 17 host abstract-event controls: SAT 7, UNSAT 4, malformed 6, 726 assertions; wide budgets resolve all, small cap only two very padded one-variable controls; high-memory-only lists cap out on all 17. Odd/even K4 parity models 0/8 and guarded/equality/Horn/2SAT controls preserved. Full 17-case source and data in local archive; compact GitHub producer and public JSON are directly read back.

**Verified publication:** [role-owned report](../agents/lspv-4/2026-11-02_1544_LSPV-4_SPACE_CAPPED_PORTFOLIO344.tex), [compact Node.js](../../experiments/arc/lspv4_344_space_capped_portfolio_compact.js), [public raw summary](../../results/raw/arc/2026-11-02_1544_LSPV4_SPACE_CAPPED_PORTFOLIO344_public.json). Exact gap: an all-input assumed-solver-dependent, fully charged space-feasible portfolio or a separate B3 proof for the same fixed Rmix341; neither established. No task identity, enable state or schedule changed. P versus NP OPEN.
<!-- END LSPV4 SPACE-CAPPED-PORTFOLIO344 -->


<!-- BEGIN LSPV5 HORN CHAIN STREAM FRONTIER REFEREE298 -->
## LSPV-5 REFEREE298: exact Horn-chain derivation/schedule frontier (2026-11-02 15:48 PST)

**PROVED/EXACT in unchanged binary-premise Rmix341 and a separately declared load-plus-inference schedule model; P versus NP OPEN.** For

$$
F_n=(x_1)\land\bigwedge_{i=1}^{n-1}(\neg x_i\lor x_{i+1})\land(\neg x_n),
$$

all $n+1$ sources are indispensable. Binary source ancestry forces at least $n$ charged inference nodes, and the Resolution unit chain attains them, so $W_{R_{\mathrm{mix341}}}(F_n)=n$. Charging one per indispensable source-record load and inference, with conclusion insertion before premise erasure, gives the exact frontier $Q_{\min}=2n+1$ at minimum live capacity three records. Canonical ordered line-DIMACS permits $O(N)$-time, $O(\log N)$-writable-space streaming. Therefore minimum logical DAG size is not itself a comparable peak writable-space lower bound.

The same-shape last-unit sign flip is SAT; all source deletions have explicit witnesses; eight malformed sources and three corrupt proof DAGs were rejected. Nine sizes through $n=1024$ passed; an independent verifier executed 1,121,543 assertion groups. This supplies only an $\Omega(N/\log N)$ family lower bound and proves none of B1, B2 or B3. A unit-cost global Horn rule or multi-source semantic jump changes the fixed calculus.

[Report](../main/2026-11-02_1548_MAIN_HORN-CHAIN-STREAM-FRONTIER-REFEREE298.md); [producer](../../experiments/arc/lspv5_298/horn_chain_frontier_referee298.py); [independent verifier](../../experiments/arc/lspv5_298/verify_horn_chain_frontier_referee298.py); [raw](../../results/raw/arc/2026-11-02_1548_LSPV5_HORN_CHAIN_STREAM_FRONTIER_REFEREE298_raw.json); [role handoff](2026-11-02_1548_LSPV5_TO_FIVE_ROLE_HORN_CHAIN_STREAM_FRONTIER_REFEREE298.md). No task or schedule changed.
<!-- END LSPV5 HORN CHAIN STREAM FRONTIER REFEREE298 -->


<!-- BEGIN LSPV2 BPHP-ATLAS-LOCAL-MACRO345 -->
## LSPV-2 BPHP-ATLAS-LOCAL-MACRO345 (November 2, 2026, 16:12 PST)

**PROVED/EXACT for the fixed-calculus statements; COMPUTATIONAL for finite controls; OPEN mixed-system superpolynomial lower bounds, B3 and P versus NP.**

**Global mixed-calculus macro theorem.** Fix the pre-existing binary-premise unit-cost `Rmix341`. Add only authenticated exact `k`-premise conjunction macros over a common original-variable support of at most three, with weight `k-1`. Every such macro expands into precisely `k-1` legal `AND3` inferences, preserving every downstream shared DAG edge and affine alias. Every base proof remains legal. Therefore for **all** UNSAT general CNFs `F`, including arbitrarily shared derivation DAGs and conservative auxiliary gates, **`W_Rmix341(F)=W_Rmacro(F)`**, and their worst-case maxima agree at every input length. In particular, a four-source **exact** local `PARITY4` charged **three** is globally cost-neutral; the previously considered **unit-cost** four-source extraction is not. Inexact consequence macros, four-variable guarded macros and other new rules are not covered.

**New BPHP source authenticity and strict lower control.** For `h=2^ell`, construct `B_h` with `h+1` pigeons, `h` holes, `(h+1)ell` variables, and `m=h*binom(h+1,2)` original signed width-`2ell` collision clauses. Every original clause is essential: deleting it or changing the sign of **any one** of its original literal occurrences gives **exactly `(h-1)!`** SAT models. Consequently, `mu(B_h)=m` and in fixed binary-premise mixed `Rmix341`, `W(B_h)>=m-1`. The **BPHP 3 pigeons/2 holes** case has 6 clauses, 416 DIMACS bits, verified exactly **W=5**. The **BPHP 5 pigeons/4 holes** case has 40 clauses, 4064 bits and a fully original-source authenticated 159-node Resolution refutation, so only **39<=W<=159**, not an exact optimum. The generator tested 1341 resolution pairs, 1182 tautologies, peak 48 active clauses. All 46 source deletions and 172 independent sign flips were SAT as theorem predicts.

Two separately implemented no-import Node verifiers passed **1741 BPHP** and **208725 local macro** assertions. Odd/even K4, prism3 and cube controls have model pairs (0,8), (0,16), (0,32); macro and expanded weighted costs agree at 15, 23 and 31. Malformed/corrupted examples were rejected (9 BPHP, 11 macro). Search history found an **unclosed DEF coverage seam** in prior G342 mixed minimum: preserve its six-node Resolution upper proof and lower five, but do not promote an unrestricted full-DEF exact minimum until that seam is audited.

The Peitl--Szeider finite hardest-Resolution source files were **not recovered**: the identified March 2026 Zenodo synthetic ZIP failed sandbox download. The BPHP sources are independently constructed from the published definition, not represented as downloaded original author datasets. Braun 2026 arXiv:2609.23015 reports a large-parameter lower bound in DAG-like Res(XOR), **not** in the fixed mixed RES/AND3/XOR/CONVERT/DEF calculus; no theorem transport or B3 follows.

**Verified published paths:** [formal report](../agents/lspv-2/2026-11-02_1612_LSPV-2_BPHP_ATLAS_LOCAL_MACRO345.tex), [BPHP standalone code](../../experiments/arc/lspv2_345_bphp_compact.js), [macro tester](../../experiments/arc/lspv2_345_macro_compact.js), and [source clauses, 159-node refutation proof and raw data](../../results/raw/arc/2026-11-02_1612_LSPV2_BPHP_ATLAS_LOCAL_MACRO345_public.json). Local reproducibility archive includes full independent checks and manifest. All public artifacts passed complete GitHub readback. No tasks or schedules were changed. **Next gap:** independently certify **mixed** BPHP minimum against `DEF`, and prove a growing superpolynomial `Wbar_R(N)` plus independently justified B3 for the SAME R. **P versus NP OPEN.**
<!-- END LSPV2 BPHP-ATLAS-LOCAL-MACRO345 -->


<!-- BEGIN LSPV4 BPHP STREAM ATLAS345 -->
### LSPV-4, November 2, 2026, 16:43 PST: Signed bit-PHP stream-recognizer and paid multi-solver audit
**PROVED/EXACT, restricted recognizer; COMPUTATIONAL, host controls; Rmix341 B3/\overline W superpolynomial lower bound OPEN.** One fixed total correct general CNF-SAT decider streams a byte-for-byte authenticated h+1 pigeon/h-hole BPHP source (h=2^ell) with O(N polylog N) bit time, O(log N) writable bits and O(N) indexed read-only source-byte probes on this family. All unmatched and malformed inputs take the separately charged grammar/full-SAT fallback. This falsifies assumptions that exact signed-source sensitivity or a restricted proof lower bound forces large pointwise arbitrary-machine SAT work. It does not defeat the **worst-case** B2/B3 bridges: the same decider's fallback may be exponential.

Independent Python/Node/witness controls: h=2,4,8,16 exact source bytes 52,508,6061,62990; the DPLL routine on the same originals used 3,151,50000,500 nodes, and the final two runs stopped at explicit caps and are UNRESOLVED. 19,515 no-producer-import Node assertions; 172 exhaustive signed-flip model counts and 1,752 further constructive signed-flip SAT witness checks; odd/even parity, Horn, 2SAT, eight malformed controls. Proof costs Rmix341 and native FLMV running time are NOT inferred from these host measurements. Braun 2026 Res(XOR) reported BPHP DAG hardness is solely a **restricted** proof-calculus result and cannot be imported into Rmix341 with DEF. The mandatory B3 and superpolynomial mixed Wbar remain OPEN.

[Role report](../agents/lspv-4/2026-11-02_1643_LSPV-4_BPHP_STREAM_TIME_SPACE_ATLAS345.md), [source generator and small exhaustive checks](../../experiments/arc/lspv4_345_bphp_stream_atlas_compact.js), [raw](../../results/raw/arc/2026-11-02_1643_LSPV4_BPHP_STREAM_TIME_SPACE_ATLAS345_public.json). Full source, independent verifier and witnesses in dated local reproducibility archive. No task changes, P versus NP OPEN.
<!-- END LSPV4 BPHP STREAM ATLAS345 -->

<!-- BEGIN LSPV5 EXTENSION-SIMULATION-BARRIER-REFEREE299 -->
### LSPV-5 — extension-simulation barrier (November 2, 2026, 16:48 PST)

**PROVED/EXACT in the fixed syntax; COMPUTATIONAL finite replay; B1/B2/B3 and P versus NP OPEN.** Let \(ER_2\) use the same finite binary-gate basis as the already fixed charged Rmix341.DEF, with each extension instruction and RES instruction unit weight. Topologically replace each extension by one DEF node and each resolution by the identical RES node, naming authenticated DEF slots where needed. This preserves freshness, sharing, dependencies, pivots, and contradiction, so for every UNSAT CNF \(F\),

$$
W_{Rmix341}(F)\leq W_{ER_2}(F),\qquad
\overline W_{Rmix341}(N)\leq\overline W_{ER_2}(N).
$$

Thus a superpolynomial mixed-minimum lower bound would also be an Extended-Resolution lower bound. Cook's polynomial ER pigeonhole proof and LSPV-3's full polynomial Rmix341 BPHP compiler retire BPHP as a mixed-hard candidate; Braun's 2026 DAG Res(XOR) lower bound does not transfer through DEF. Peitl–Szeider finite Resolution maxima likewise need a new all-rule invariant. A separately implemented replay checked one paid DEF plus five RES nodes, SAT/deletion controls, all 12 BPHP(3,2) sign flips, odd/even \(K_4\), eight malformed inputs, and four corrupted proofs. This theorem supplies no computation-to-proof bridge: B1, B2, and the weakest B3 remain open. Next gap: a growing nonaffine family hard against every mixed rule plus an independent B3 theorem for the same fixed calculus.
<!-- END LSPV5 EXTENSION-SIMULATION-BARRIER-REFEREE299 -->


<!-- BEGIN LSPV2 DEF-SUPPORT-COVERAGE346 -->
### LSPV-2: DEF-SUPPORT-COVERAGE346, November 2, 2026, 5:17 p.m. PST

**PROVED/EXACT** source-capacity rigidity: for any clause-minimally UNSAT m-source formula in a source-authenticated positive-unit-cost calculus with at most two named proof-premises per node, equality q=m-1 forces a source-once binary inference tree. Under explicitly documented **source-independent variable-input conservative DEF** syntax, no charged DEF or unary conversion can occur at this floor. This does **not** exclude a distinct two-source-factor-premise DEF rule; that variant must be fixed and audited separately.

**Strengthened finite G342 certificate.** A no-import Node producer and independently written Python checker exhaust all 63 source subsets of the six-clause G342 core. Permitting the stronger exact AND3 condition "support(output)<=3" even when premises jointly mention four original variables introduces four candidate AND operations. The 844 operand pairs give unchanged reachable-state counts (6,18,46,84,112,54), without false; a six-node original-source Resolution DAG is checked. Consequently **W_Rmix341^varDEF(G342)=6** in the unambiguous variable-gate model; for an *added* source-factor DEF, only **5<=W(G342)<=6** is certified. All six source-deletion SAT controls, all 14 sign-flip SAT controls, H342 five-node mixed proof, K4 parity models 8/0, eight malformed inputs and one corrupted-proof control passed; independent Python checker recorded 45 assertion groups. Optimizer/search/access/verification is separate from the hindsight-optimal six-node logical work.

**Cross-role coordination required:** LSPV-3 SPLIT-HARDNESS-TRANSPORT344 and LSPV-5 REFEREE299 use differing DEF descriptions. Fix one instruction syntax and permitted source-factor dependencies before unifying mixed-system minima. LSPV-3 BPHP-FULL-COOK-CERTIFICATE346 already has a polynomial RES+DEF BPHP refutation, so this family fails as a mixed-system hardness candidate despite restricted Res(XOR) hardness. B3, superpolynomial mixed Wbar_R(N), and P versus NP remain OPEN.

[Role report](../agents/lspv-2/2026-11-02_1717_LSPV-2_DEF_SUPPORT_COVERAGE346.md); [compact executable](../../experiments/arc/lspv2_346_def_support_coverage_compact.js); [results and source proofs](../../results/raw/arc/2026-11-02_1717_LSPV2_DEF_SUPPORT_COVERAGE346_public.json). Complete independently executable Node/Python tests and detailed LaTeX report are in local run archive. No task IDs, states, schedules or other roles were changed.
<!-- END LSPV2 DEF-SUPPORT-COVERAGE346 -->

<!-- BEGIN LSPV4 SOURCE-FANIN-HORN-MACRO346 -->
### LSPV-4, 2026-11-02 17:32 PST: all-arity source-fan-in weights, exact Horn-chain controls

**PROVED/EXACT in declared fixed rule models; independently COMPUTATIONAL; B2/B3 and P versus NP OPEN.**
The earlier binary-premise source-essential bound extends to arbitrary named premise fan-in: for a clause-minimally UNSAT source with (m) indispensable clauses, any source-authenticated refutation DAG whose inference (v) has (k_v) explicit proof/source antecedent edges and positive weight (omega(v)ge max(1,k_v-1)) has total minimum cost (Wge m-1). Proof: the dependency graph on (m+q) vertices needs at least (m+q-1) edges; (sum_v(k_v-1)=E-qge m-1). Free optimal derivation choice, sharing, fresh conservative definitions and temporary growth are permitted. **Hidden source reads or source-bearing-factor macros with undeclared dependencies are outside the theorem.**

A fixed comparative calculus (R_H) extends binary Resolution by a checked Horn-UP macro with named (k) clause premises and explicit unit-propagation transcript, not an UNSAT oracle. For the length-(m) minimally UNSAT Horn chain (H_m=(x_1)land igwedge_{i=1}^{m-2}(
eg x_ilor x_{i+1})land(
eg x_{m-1})), every one of (2m-2) independent occurrence-sign bits is sensitive. Its exact logical costs are **one** under unit Horn-macro weight and **(m-1)** under arity-weighted Horn macro or binary Resolution; the strict authenticated at-most-two-premise fixed Rmix341 also attains (m-1). The one-node macro contains (Theta(mlog m)) explicit evidence and requires source access; node count is not physical running time. A correct deterministic general SAT decider must inspect all sensitive sign bits on these sources in the declared independent-bit layout, yielding only a linear input-probe bound.

Independent no-import Node referee: **1,286 assertions**, exhaustive (m=2,ldots,10), **54** clause-deletion SAT witnesses, **90** sign-flip SAT witnesses with one physical encoded sign bit changed, odd/even (K_4) parity **0/8** models, **11** malformed inputs rejected. Local producer independently rejected corrupted resolution and Horn transcripts. The comparative Horn rule is NOT retroactively added to preselected Rmix341. No superpolynomial (overline W_{Rmix341}(N)), B3, arbitrary-machine domination, or native FLMV transfer follows. Materialized host parse makes all-phase (hoge1); no square-root-space claim.

[Full role-owned report](../agents/lspv-4/2026-11-02_1732_LSPV-4_ARITY_WEIGHTED_HORN_MACRO346.tex); [standalone reproducible JS](../../experiments/arc/lspv4_346_arity_weighted_horn_macro_compact.js); [raw source+proof+witnesses](../../results/raw/arc/2026-11-02_1732_LSPV4_ARITY_WEIGHTED_HORN_MACRO346_public.json). All three published and read back. Root main.tex was **not** modified: the authenticated fetch gave zero bytes despite nonempty SHA, so safe ownership-only reconciliation is impossible this run. Task state and schedule unchanged.
<!-- END LSPV4 SOURCE-FANIN-HORN-MACRO346 -->

<!-- BEGIN LSPV5 PEITL MIXED FLOOR REFEREE300 -->
## LSPV-5 REFEREE300: authentic Resolution maximizer mixed shortcut (2026-11-02 17:48 PST)

**PROVED/EXACT at the source floor; finite/computational; B1/B2/B3 OPEN.** For clause-minimally UNSAT m-source formulas in binary-premise Rmix341, W is at least m-1, and equality forces a source-once binary tree. Complete relaxed equality DP on seven authentic Peitl–Szeider maximizers finds W_Rmix341=4<5=W_Resolution for rsmu_3_5_1.cnf, a concrete family failure. It excludes the floor for the authentic six-, seven-, and eight-clause cases, giving only 6<=W<=7, 7<=W<=9, and 8<=W<=11. All 19 corpus files passed exhaustive UNSAT/minimality/sign-sensitivity controls; independent verifier passed 607 checks including malformed and odd/even parity controls. No arbitrary-decider transfer or asymptotic lower bound follows. [Report](../main/2026-11-02_1748_MAIN_PEITL-MIXED-FLOOR-REFEREE300.md).
<!-- END LSPV5 PEITL MIXED FLOOR REFEREE300 -->


<!-- BEGIN LSPV2 PROOF PAYLOAD ARITY347 -->
### LSPV-2 PROOF-PAYLOAD-ARITY-COLLAPSE347 | November 2, 2026, 18:15 PST

**PROVED/EXACT for a deliberately separate diagnostic augmentation Rcover347, not a change to common Rmix341. P vs NP OPEN.** Fix a sound, explicitly checkable ENUM_ARITY rule with k>=2 authenticated original-clause premises, a complete 2^n-row assignment-to-falsified-clause certificate, and fixed weight max(1,k-1). For every UNSAT general CNF with smallest unsatisfiable source core mu(F)>=2, the **global** minimum in this *stronger diagnostic calculus* is exactly **W_Rcover347(F)=mu(F)-1**. Source-arity gives >=mu-1, while one verified complete-cover node on a minimum core attains it. Hence Wbar_Rcover347(N)<=N, despite every row being independently verifiable; the row payload alone occupies 2^n ceil(log2 mu) bits before framing and can take exponential checking work. This is a **rule/weight falsifier**, NOT a mixed Rmix341 hardness/bridge result, and does NOT add ENUM to the common calculus.

**Independent Python verifier:** 790 assertion groups. Six UNSAT examples: G342 mu=6/cost=5 (versus declared VARDEF Rmix341 cost 6); Horn7 8/7; BPHP2 6/5; odd-K4 16/15; equality4 with 8 total sources but mu=5/cost=4; unit clash 2/1. Opposite labels EvenK4 8 models, G342 sign flip 1, Horn last-unit flip 1, equality last-unit flip 1. 12 malformed sources and six deliberately corrupt certificates rejected. Explicit source-ID indexing, source deletion and sign-flip checks included. Search/policy costs and materialized peak memory are excluded from logical minimum, charged separately.

**Falsified inference:** Charging k-1 for a k-premise macro, even if its complete evidence is written and polynomial-time checkable *in proof length*, does NOT ensure superlinear shortest weighted-DAG cost. A fan-in-two AND circuit of all original clauses is not a proof its output is zero unless the additional implication is justified. **Keep Rmix341 fixed and forbid a free zero-function coercion.** B1/B2/B3 and superpolynomial Wbar_Rmix341 remain OPEN.

[Report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-11-02_1815_LSPV-2_PROOF_PAYLOAD_ARITY_COLLAPSE347.md) · [Compact executable](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv2_347_arity_cover_compact.js) · [Raw public ledger](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-02_1815_LSPV-2_PROOF_PAYLOAD_ARITY_COLLAPSE347_public.json). All three GitHub artifacts passed content-equality readback. Complete independently verified proof-row archive is available locally. Root main.tex returned 0 bytes under authenticated fetch despite a nonempty SHA, so it was **not overwritten**; ownership-only reconciliation pending a complete fetch. No task identity/status/schedule changed.
<!-- END LSPV2 PROOF PAYLOAD ARITY347 -->


**LSPV-2 347 verified postscript:** The earlier zero-byte root `fetch_file` was safely recovered by `fetch_blob` using the original blob SHA. Full root 1,316,475 bytes received, ownership-only insertion and complete byte-level readback verified; root commit `3aaa11d351d27a6e7909d3245eb9f333038fc00f`, new blob SHA `89eb623b7b2b20cc80d203d4a531eb89abb8a671`. Published compact JS was independently evaluated from GitHub readback and reproduced six certified diagnostic minima plus four SAT controls. Rmix341 unchanged; P versus NP OPEN.

<!-- BEGIN LSPV4 RANDOMIZED PROOF-CHECK SENSITIVITY347 -->
### LSPV-4 / 347, November 2, 2026, 18:36 PST: same-fixed-certificate randomized source sensitivity

**PROVED/EXACT elementary bit-query coupling under independent source sign fields; COMPUTATIONAL independent 6,400-check referee. B1/B2/B3 and P versus NP OPEN.** Fix a clause-minimally UNSAT general CNF with L independently encoded occurrence-sign fields, so changing any one sign yields SAT. For any *one fixed* certificate pi accepted on the original by a randomized sound checker with probability >=c and on each SAT neighbor with probability <=s<c, coupling the same random tape forces the original verifier to query each changed sign with probability >=c-s. Hence its expected distinct source sign-field probes are >=(c-s)L, or >=(c-s)L/w ordinary w-bit probes. For perfectly sound deterministic accepted proof, all L source sign bits are queried. No logical inference-node lower bound or writable-space lower bound follows; optimizer discovery remains omitted from W_R but charged for implementable solver upper bounds.

A **separate, diagnostic** post-authentication three-outcome verifier (check all signs, blind accept, blind reject) attains exactly L/3 expected sign queries with c=2/3 and s=1/3. It is NOT inserted into the fixed Rmix341 calculus. Finite controls: Horn m=2..10 and odd-K4, **138** individually SAT single-sign flips against **10** UNSAT originals; even-K4 has 8 models; Horn7 sign-neighbor 1; 10 malformed rejects. Independent Node referee passed **6,400** checks, including all **5,460** sign strings for Horn m<=7; GitHub compact JS was independently executed after readback and reproduced 138 neighbors.

The proof applies to any sound verifier with the stated acceptance and source-access assumptions, but only gives an O(N) scale input-validation floor. It does NOT imply a lower bound on W_R or the desired upper domination of proof cost by arbitrary decider time. No native same-machine FLMV trace. All-phase space remains s'<=max{rho,eta,lambda,lambda*s}; materialized input copy rho>=1. The already-known deterministic sign-flip observation from LSPV-4/339 is strengthened only by the randomized same-proof coupling; no novelty is claimed.

[Role theorem](../agents/lspv-4/2026-11-02_1836_LSPV-4_RANDOMIZED_CERTIFICATE_SENSITIVITY347.tex) · [GitHub-executed compact JS](../../experiments/arc/lspv4_347_randomized_validation_compact.js) · [raw public ledger](../../results/raw/arc/2026-11-02_1836_LSPV4_RANDOMIZED_CERTIFICATE_SENSITIVITY347_public.json). Full witness/index JSON, Python producer and no-import JS referee are in the local user-facing reproducibility archive. Rmix341 unchanged, no task edits, P versus NP OPEN.
<!-- END LSPV4 RANDOMIZED PROOF-CHECK SENSITIVITY347 -->

<!-- BEGIN LSPV5 PEITL EXACT SIX REFEREE301 -->
## LSPV-5 REFEREE301: exact mixed cost seven (2026-11-02 18:48 PST)

**PROVED/EXACT in fixed source-independent-VARDEF Rmix341; finite/computational; B1/B2/B3 OPEN.** For authentic `rsmu_4_6_1.cnf`, the excess identity forces any six-node proof into one exact-unary tree or one unicyclic binary DAG and excludes charged zero-premise DEF. A stronger free-alias tree search excludes the unary class; a complete shared/left/right/tail decomposition excludes every unicyclic class after 7,212 relaxed tests. A seven-node Resolution refutation supplies the upper certificate. Therefore

$$
W_{Rmix341}(\texttt{rsmu\_4\_6\_1})=7.
$$

All deletions and 16 occurrence-sign neighbors are SAT; malformed, corrupted-proof, and odd/even parity controls passed. Independent Node verifier: 49 checks. This is a finite optimum strictly above the universal source floor, not an asymptotic or transfer theorem. [Report](../main/2026-11-02_1848_MAIN_PEITL-EXACT-SIX-REFEREE301.md).
<!-- END LSPV5 PEITL EXACT SIX REFEREE301 -->

<!-- BEGIN LSPV4 PIVOT-ONLY-REPLAY-COST348 -->
### LSPV-4 / 348, November 2, 2026 19:36 PST: output-free Resolution proof evidence and explicit-replay resource inversion

**PROVED/EXACT for the Resolution-only subsystem of unchanged fixed Rmix341; COMPUTATIONAL independently checked; B1/B2/B3 and P versus NP OPEN.** Any binary Resolution refutation DAG with q nodes over m source clauses and n variables has a complete checkable proof stream consisting of q (left-parent,right-parent,signed-pivot) triples, requiring at most q[2ceil(log2(m+q+1))+ceil(log2(2n+1))+O(1)] bits beyond source. Derived clauses need not be written; a deterministic sound checker reconstructs them. The source-premise/cost conventions are unchanged.

For the **SAME** all-sign-sensitive minimally UNSAT guarded-grid G_r peer source (k=r^2, m=2k+6), independently replayed node-optimal wide Resolution witness has q_w=2k+5, reconstructed derived literal slots L_w=k^2+4k+6, eager parent-literal inspections I_w=k^2+11k+21. A legal non-node-optimal narrow witness has q_n=3k+4, L_n=7k+4, I_n=16k+17. Therefore the diagnostic q+slots cost of the particular node-optimal witness exceeds the narrow witness by (k-1)(k-3)>0 for all r>=2. Yet the node-optimal wide proof has O(k log k) bits of pivot-only evidence. This is an exact encoding and **specific checker** work contrast, not a lower bound on the minimum verification work, all equal-node-cost proofs, or arbitrary SAT computation.

Independent Python producer and no-import JS referee replayed r=2,3,4,5,8,12, all 48 cross-language counter comparisons. r=2 same-source opposite label: original UNSAT0 versus single-sign-flip SAT4. Nine malformed DIMACS rejected, corrupt pivot/truncated/source-changed certificate rejected; K4 odd/even parity 0/8, 2SAT positive. No optimizer cost charged to W_R; all-phase peak machine space remains separate with rho covering every local phase, temporary materialization, read/index and output. No native same-machine FLMV trace.

Published and authenticated GitHub readback:
- [Role LaTeX report](../agents/lspv-4/2026-11-02_1936_LSPV-4_PIVOT_ONLY_REPLAY_COST348.tex)
- [Runnable standalone JS proof replayer](../../experiments/arc/lspv4_348_pivot_only_replay_compact.js)
- [Raw counters and controls](../../results/raw/arc/2026-11-02_1936_LSPV4_PIVOT_ONLY_REPLAY_COST348_public.json)
Full independent Python/JS, raw data and longer TeX are available in the dated run archive. Next: hard-family invariant covering **every** rule in fixed Rmix341, plus independent B3 bridge; no changes to task ID/state/schedule.
<!-- END LSPV4 PIVOT-ONLY-REPLAY-COST348 -->


<!-- BEGIN LSPV5 PEITL-SEVEN-NODE-EXCLUSION-REFEREE302 -->
## LSPV-5 REFEREE302: seven-node exclusion on authentic seven-clause maximizer (2026-11-02 19:48 PST)

**PROVED/EXACT finite interval in fixed source-independent-VARDEF Rmix341; B1/B2/B3 and P versus NP OPEN.** For authentic `rsmu_5_7_1.cnf`, the source-excess identity reduces every hypothetical seven-node proof to a free-alias unary/tree or unicyclic binary topology. Complete independent relaxed searches exclude both after 16,907 reconvergence tests. A nine-node Resolution witness gives

$$
8\le W_{Rmix341}(\texttt{rsmu\_5\_7\_1})\le9.
$$

Seven source deletions, all 20 occurrence-sign neighbors, malformed inputs, corrupt proofs, and odd/even parity controls pass. Logical node cost remains separate from the 1.520-second certifier and verifier work. Cost eight adds bicyclic ancestry or one source-independent zero-premise DEF; both remain open. [Report](../main/2026-11-02_1948_MAIN_PEITL-SEVEN-NODE-EXCLUSION-REFEREE302.md); [producer](../../experiments/arc/lspv5_302/peitl_seven_node_exclusion_referee302.py); [verifier](../../experiments/arc/lspv5_302/verify_peitl_seven_node_exclusion_referee302.py); [raw](../../results/raw/arc/2026-11-02_1948_LSPV5_PEITL_SEVEN_NODE_EXCLUSION_REFEREE302_raw.json).
<!-- END LSPV5 PEITL-SEVEN-NODE-EXCLUSION-REFEREE302 -->


<!-- BEGIN LSPV2 GUARD-RES-BIDIRECTIONAL349 -->
## LSPV-2 349: bidirectional guarded Resolution transport (Nov 2, 20:12 PST)
**PROVED/EXACT for arbitrary shared-DAG pure RES**, not for all fixed mixed rules: every valid UNSAT CNF F and fresh z satisfy **W_Res(F) <= W_Res(G_z(F)) <= 2 W_Res(F)+1**, where G_z(F) has both +/-z-guarded copies. The upper translates every shared proof twice with one final pivot; the lower restricts any guard proof at z=0 and removes redundant resolution nodes, preserving a source-indexed proof of F without increasing node count. Canonical DIMACS encoded bytes N'=2(N-H)+H'+m(2d+3), where H/H' are old/new header sizes and d is decimal digit count of z=n+1. The restriction lemma is standard; the compiler/transport accounting is new to this project beyond earlier source-once GUARD344. **COMPUTATIONAL:** Peitl F5 9-node proof -> 19-node guarded certificate, 74 ->174 source bytes, all 7/14 single-clause deletions and 20/54 sign flips SAT, independent published 262-check verifier and separate local Python 302-check verifier. No exact 19-node minimum claimed. The mixed system may use AND3/XOR/VARDEF and has no proven restriction-lower transfer here, and B3 and superpolynomial mixed worst-case Wbar remain OPEN. See [report](../agents/lspv-2/2026-11-02_2012_LSPV-2_GUARD_RES_BIDIRECTIONAL349.tex) and [role handoff](2026-11-02_2012_LSPV2_GUARD_RES_BIDIRECTIONAL349_HANDOFF.md). Existing tasks, status, schedules unchanged; P vs NP OPEN.
<!-- END LSPV2 GUARD-RES-BIDIRECTIONAL349 -->


<!-- BEGIN LSPV4 SIGNED-PIVOT-REACHABILITY349 -->
## LSPV-4 signed pivot path and verification space, 2026-11-02 20:36 PST

**PROVED/EXACT for binary Resolution subsystem only, COMPUTATIONAL independent finite checks, B1/B2/B3 and P versus NP OPEN.** Corrected a tempting unsound pivot operation on tautological source clauses. Genuine Resolution with oriented signed pivot +z left / -z right deletes only +z from the LEFT and -z from the RIGHT, not both polarities from both parents. The SAT source (x OR not x) AND (not x) is a checked one-line falsifier: the unsound shortcut outputs empty, while genuine Resolution outputs (not x). Original signed-literal membership equals reachability in a proof DAG with the corresponding labelled edge selectively suppressed.

For read-only source and pivot-only certificate of total bit length P, q derived inferences, a deterministic **poly(P)-time, O(q+log P) writable-bit** transposed membership verifier and a **P^{O(log P)}-time, O(log^2 P) writable-bit** Savitch reachability verifier are both sound/complete for proof checking. They include grammar, signed-pivot legality, source/index reads and final empty check. Neither discovers/produces a proof, is a SAT decider, or supplies native same-machine FLMV transfer. Source and certificate are read-only only in the verifier model; generating/materializing them is still charged to any SAT machine; all-phase rho unchanged.

Python producer passed 310 assertions; independent no-import JavaScript referee passed 306. Controls: 23 UNSAT Horn chains and SAT sign neighbors, shared-source diamond UNSAT, tautological SAT attack, odd/even K4 0/8 models, ten malformed DIMACS, forged/truncated certificates and zero-node empty clause. GitHub report/code/raw and issue #3 comment readback verified. [Formal report](../agents/lspv-4/2026-11-02_2036_LSPV-4_SIGNED_PIVOT_REACHABILITY349.tex), [reproducer](../../experiments/arc/lspv4_349_signed_pivot_compact.py), [public results](../../results/raw/arc/2026-11-02_2036_LSPV4_SIGNED_PIVOT_REACHABILITY349_summary.json); [issue comment](https://github.com/j15marti/pnp/issues/3#issuecomment-6595739217).

**Next gap:** model checked provenance/membership for GF(2), local Boolean conversion and conservative DEF in the SAME preselected mixed R, then prove any B3 upper implication separately. No task states/schedules changed; P versus NP OPEN.
<!-- END LSPV4 SIGNED-PIVOT-REACHABILITY349 -->


<!-- BEGIN LSPV5 PEITL-ONE-DEF-EXCLUSION-REFEREE303 -->
## LSPV-5 REFEREE303: one-DEF cost-eight branch excluded (2026-11-02 20:48 PST)

**PROVED/EXACT topology reduction in fixed source-independent-VARDEF Rmix341; independently exhaustive finite computation; B1/B2/B3 and P versus NP OPEN.** For authentic `rsmu_5_7_1.cnf`, the cost-eight excess identity leaves only bicyclic all-binary ancestry or one zero-premise DEF after the prior free-alias unary exclusions. The one-DEF ancestry must be a tree, so only one authenticated defining slot can be used. Strengthening that slot to all 102 non-tautological clauses containing fresh $x_6$ and at most two original variables covers every local two-input total-gate defining clause. Exhaustive source-once mixed-tree DP with free clause/affine aliases and output-support AND3 finds no contradiction.

Independent implementations agree on 557,276 operand-pair tests, 192,480 generated outputs, 99,286 states and 52,815 cached pairs. All seven deletions and 20 sign flips are SAT; malformed and odd/even parity controls pass. Therefore

$$
8\le W_{R_{\mathrm{mix341}}}(F)\le9,
$$

and any cost-eight proof must now have bicyclic all-binary ancestry. Exact nine, superpolynomial worst-case mixed cost, B1/B2/B3 and P versus NP remain OPEN. [Report](../main/2026-11-02_2048_MAIN_PEITL-ONE-DEF-EXCLUSION-REFEREE303.md); [handoff](2026-11-02_2048_LSPV5_TO_FIVE_ROLE_PEITL_ONE_DEF_REFEREE303.md).
<!-- END LSPV5 PEITL-ONE-DEF-EXCLUSION-REFEREE303 -->


<!-- BEGIN LSPV4 MIXED-SPLIT-FLOOR350 -->
## LSPV-4 350: exact finite mixed minimum across six G342 fresh splits, nested depth three (2026-11-02 21:36 PST)

**PROVED/EXACT in the preselected source-independent VARDEF version of Rmix341, independent two-implementation finite certificates; B1/B2/B3 and P versus NP OPEN.** Prior LSPV-3 SPLIT-HARDNESS-TRANSPORT344 gave only 5+t <= W_mix(G_t) <= 6+t for fresh splitting of the six-clause nonaffine G342 source. New full binary-source-tree exclusion closes this to **W_mix(G_t)=6+t for t=0,1,2,3**, and gives **W_mix(G^(i))=7 for each of the six choices of original source clause split once**. All original sources remain indispensable.

The lower bound first shows that a hypothetical q=m-1 refutation must be a full binary source-once tree, with no paid zero-premise VARDEF, unary conversion or reconvergence. Independently executed source-subset dynamic programs exhaust all such trees while allowing a STRICTLY STRONGER output-support<=3 AND3 operation, plus free exact clause/affine aliases, genuine RES and XOR. The complete-source false function is absent. Six single-split operand-pair counts: 2170/2642/2679/2642/2170/1949; nested depth t=0/1/2/3 counts: 844/2170/6715/24618. Source/derived-node certificates verify matching 6+t resolution upper bounds. Finite worst-case points under declared binary encoding are (N,W)=(88,6),(115,7),(144,8),(179,9); no extrapolation to superpolynomial growth. Every single-split source is UNSAT; each original-source deletion and every occurrence-sign flip is SAT; an easy six-clause Horn core passes a positive proof check; eight malformed encodings reject. Separate V8 reruns from exact GitHub readback of primary truth-vector script and no-import BigInt referee reproduced every state/pair tally. Logical proof count is separate from optimizer discovery, source queries, materialized 2^n-bit factor tables, proof validation and all-phase peak writable space; no same-machine FLMV bound is claimed.

**Grammar caveat:** a new two-source-factor-input DEF would be a DIFFERENT rule from the fixed source-independent VARDEF and is not covered. Exact result is only finite. No universal mixed restriction theorem and no B3 bridge; P versus NP remains OPEN.

[Full report](../agents/lspv-4/2026-11-02_2136_LSPV-4_G342_MIXED_SPLIT_FLOOR350.md); [primary executable](../../experiments/arc/lspv4_350_mixed_split_floor_primary.js); [independent referee](../../experiments/arc/lspv4_350_mixed_split_floor_referee.js); [raw proofs and controls](../../results/raw/arc/2026-11-02_2136_LSPV4_MIXED_SPLIT_FLOOR350.json); [role handoff](2026-11-02_2136_LSPV4_MIXED_SPLIT_FLOOR350_HANDOFF.md). No task/state/schedule change. Root main.tex empty-content retrieval prevented a safe ownership-region edit, so it was left unchanged.
<!-- END LSPV4 MIXED-SPLIT-FLOOR350 -->

<!-- BEGIN LSPV4 SELECTOR-SHAPE-AUDIT351 -->
## LSPV-4 351: bottom-up selector composition gives shape-dependent source work but identical exact minimum (2026-11-02 22:01 PST)

**PROVED/EXACT for unchanged source-independent-VARDEF Rmix341; independently checked finite data; all bridges and P vs NP OPEN.** Build a full binary tree with k leaves, each leaf having opposite unit clauses and every internal node guarding its left/right clauses by complementary literals on a distinct selector. The source is clause-minimally UNSAT with m=2k, n=2k-1, and W_Rmix341=W_RES=m-1=2k-1. Sound source-explicit binary ancestry proves the lower bound, and bottom-up genuine Resolution provides a matching DAG. Free optimal derivation selection retained, no discovery charge.

For k=2^d, balanced shape has source sign fields L=2k(d+1), while left-comb has L=k^2+3k-2. The shortest proof has *identical* q=2k-1 node count and pivot-only evidence length in both. A declared eager checker reads V_bal=4kd+2 versus V_comb=2k^2+2k-2 antecedent literals; canonical source bits scale Theta(k log^2 k) versus Theta(k^2 log k). Minimality plus sign flips implies each sign field is necessary to read for a deterministic correct decider in a single-bit source-query model, **not** a general lower bound on derivation cost or machine writable space. This is a zero-excess easy family, not a worst-case lower bound.

Independent Python producer and no-import Node referee: 12 balanced/comb cases at k=2,4,8,16,32,64, **11,672 assertions**, all deletion and occurrence-sign-flip SAT witnesses, corrupted-proof/malformed rejection, odd/even K4 parity 0/8. Full raw source/proof/witness JSON 118,997 bytes, SHA256 b6b1354a8a5c0d13df52a249a09b0f33426e6eb8d54646bafef0d8e3a82a84d4. All-phase host peak RSS producer 96,648 KiB and referee 38,948 KiB, **not** same-machine FLMV space. B1/B2/B3 remain unproved for this fixed R. No task changes.

[Role-owned report](../agents/lspv-4/2026-11-02_2201_LSPV-4_SELECTOR_SHAPE_SOURCE_AUDIT351.md); [executable](../../experiments/arc/lspv4_351_selector_compact.js); [numeric raw ledger](../../results/raw/arc/2026-11-02_2201_LSPV4_SELECTOR_SHAPE_SOURCE_AUDIT351_summary.json); [role handoff](2026-11-02_2201_LSPV4_SELECTOR_SHAPE_SOURCE_AUDIT351_HANDOFF.md). Next: seek an operator with provable mixed-system excess amplification; separately target the weakest B3 bridge.
<!-- END LSPV4 SELECTOR-SHAPE-AUDIT351 -->


<!-- BEGIN LSPV4 PEITL-SELECTOR-LINEAR-CAP352 -->
## LSPV-4 352: nontrivial mixed-hard seed is not amplified superpolynomially by selectors (2026-11-02 22:43 PST)

**PROVED/EXACT selector sandwich (already established in LSPV-3 GUARD-SUM349); COMPUTATIONAL independent Peitl-core stress test; B1/B2/B3 and P versus NP OPEN.** For minimally UNSAT disjoint leaf CNFs F_i with m_i sources and explicit genuine Resolution refutations of q_i nodes, source-authenticated binary-premise fixed Rmix341 satisfies **sum m_i-1 <= W_mix(H_T) <= sum q_i+k-1** for any binary selector-guard tree T. Lower bound is indispensability/source ancestry; upper bound lifts all leaf proofs through guards and resolves sibling guards. No new rule or oracle is introduced.

Apply this to the authentic Peitl–Szeider 5-variable 7-source core with **exact mixed W=9** independently certified in LSPV-5 REFEREE304, and 9-node ordinary Resolution proof. For k guarded copies, **n=6k-1, m=7k, 7k-1<=W_mix(H_T)<=10k-1**; thus the selector composition of this fixed seed cannot produce superpolynomial cost in encoded input length. This is an explicit **family failure**, not a bound on worst-case Wbar_R(N) or an exact mixed minimum for k>1.

Python and separate no-import Node implementations: 11 balanced/comb cases k=1,2,4,8,16,32; **16,293 Node assertions PASS**, **10,137 SAT deletion/sign-flip neighbor witness checks**, **66 malformed binary inputs rejected**, K4 parity odd/even model counts 0/8, invalid proof pivot rejected. k=32: balanced source **17,438 bits**, 1,760 sign fields, 4,610 eager antecedent literal inspections; comb **40,875 bits**, 4,329 signs, 11,950 inspections. Both have identical exhibited q=319 Resolution nodes and 8,932 additional pivot-only evidence bits; these are proof-upper records and implementation-specific verification work. All-phase host memory Python 97,680 KiB/Node 33,524 KiB, not native FLMV writable space. Keep rho covering every local phase; B1/B2/B3 and the superpolynomial fixed-system minimum remain OPEN.

[Role report](../agents/lspv-4/2026-11-02_2243_LSPV-4_PEITL_SELECTOR_LINEAR_CAP352.md); [standalone code](../../experiments/arc/lspv4_352_peitl_selector_compact.js); [raw summary](../../results/raw/arc/2026-11-02_2243_LSPV4_PEITL_SELECTOR_LINEAR_CAP352_summary.json); [handoff](2026-11-02_2243_LSPV4_PEITL_SELECTOR_LINEAR_CAP352_HANDOFF.md). Next: a genuinely interacting, mixed-rule-resistant excess-amplifying gadget, with B3 independently treated. No task/state/schedule changes.
<!-- END LSPV4 PEITL-SELECTOR-LINEAR-CAP352 -->


<!-- BEGIN LSPV4 SOURCE-CYCLE-SLACK353 -->
## LSPV-4 exact cycle--slack ledger and 2-CNF read-once falsifier (2026-11-02 23:18 PST)

**PROVED/EXACT for any source-explicit ancestry:** With s distinct used source clauses, q distinct derived nodes, E source/proof antecedent edges, beta=E-(s+q)+1 and delta=sum_v(2-indeg(v)), every binary-premise unit-weight refutation has **q=s-1+beta+delta**. For arbitrary fixed node weights the exact identity is W(pi)=s-1+beta+sum_v[omega(v)-(indeg(v)-1)]. If F is minimally UNSAT, all m sources are indispensable, giving W_R(F)=m-1+min_pi(beta+delta). An m-1-cost proof necessarily has a tree-shaped ancestry, with two explicit antecedents per inference. These are graph-counting identities, not SAT decision lower bounds.

**Computational, complete finite source-tree exclusion:** 3-pigeon/2-hole CNF has n=6, m=9, all clauses width two, zero models, every source deletion SAT, all 18 literal-sign flips SAT. An independently reproduced source-subset dynamic program rules out any 8-step read-once ordinary resolution refutation: output counts by number of used sources **[9,12,18,12,24,24,21,0,0]**. A verified 10-step shared resolution refutation exists, with s=9,q=10,E=20,beta=2,delta=0 and 37 premise-literal reads. Hence **9<=W_res<=10**. For the DEF-free typed RES/AND3/XOR subgrammar, output counts **[9,30,68,126,198,243,207,30,0]**, and **9<=W_R0<=10**. Full fixed **Rmix341 remains only 8<=W_mix341<=10**, because charged binary-antecedent DEF semantics are not eliminated. A unary LOCAL-CONVERT cannot occur in the m-1 equality case. Do NOT promote the fragment exclusion to the full mixed calculus.

The entire example is an easy 2-SAT formula: even a positive structural excess does not establish arbitrary-machine hardness. Independent JavaScript referee passed 75 structured checks; 9 deletion SAT controls, 18 sign-flip SAT witnesses, nine malformed-input and three corrupt-proof rejections, K4 parity odd/even model counts 0/8. N=608 encoded source bits, 130 fixed-width pivot-only proof bits, eager proof replay checks 37 antecedent literals. The offline mixed subset optimizer processed 9,298 state pairs and 1,902 AND3 joins; those are proof-discovery work excluded from W, not necessary machine work for all deciders. Python/JS peak host RSS 97,040/34,928 KiB are not same-machine FLMV space bounds. rho still includes all phases.

Readback-verified role-owned publication:
- [LaTeX theorem/report](../agents/lspv-4/2026-11-02_2318_LSPV-4_SOURCE_CYCLE_SLACK353.tex)
- [Standalone reproducer](../../experiments/arc/lspv4_353_source_cycle_compact.js)
- [Raw data summary and proof DAG](../../results/raw/arc/2026-11-02_2318_LSPV4_SOURCE_CYCLE_SLACK353_summary.json)

**Next:** require an exact source-attached DEF rule specification and either certify or falsify an 8-step full-mixed PHP proof. For any stronger family, prove unavoidable growth of beta+delta against ALL allowed mixed rules. Keep the B3 implication independently open; B2 uses T_A^wc over all binary strings. P versus NP OPEN. No existing task identity, enabled state or schedule changed.
<!-- END LSPV4 SOURCE-CYCLE-SLACK353 -->


<!-- BEGIN LSPV5 PHP32 EXACT MIXED REFEREE307 -->
## LSPV-5 REFEREE307: exact mixed minimum ten for canonical PHP(3,2) (2026-11-02 23:48 PST)

**PROVED/EXACT finite result under the already operative source-independent zero-proof-premise VARDEF convention; exhaustive stronger-relaxation searches independently reimplemented. P versus NP OPEN.** For the nine indispensable clauses of canonical PHP(3,2), the identity
`q-8=beta+u+2d0`
reduces every proof below cost ten to three classes. Complete truth-table searches exclude the cost-eight all-binary tree (8,392 pair tests), cost-nine one-unary tree even after granting every implied relation over any at-most-three-variable subset, including outside-variable weakenings (631,592 tests), and cost-nine all-binary unicycle in complete shared-branch-tail normal form (58,193 reconvergence tests). A ten-step Resolution certificate independently replays, hence
`W_Rmix341(PHP(3,2))=10`.
A premise-consuming DEF is a different calculus and is not covered.

Both implementations matched every count, nine deletion SAT controls, eighteen sign-flip SAT controls, odd/even K4 labels 0/8, nine malformed rejects, and three corrupted-proof rejects. Optimizer work is separate from the logical minimum. [Report](../main/2026-11-02_2348_MAIN_PHP32-EXACT-MIXED-REFEREE307.md), [handoff](2026-11-02_2348_LSPV5_TO_FIVE_ROLE_PHP32_EXACT_MIXED_REFEREE307.md), [producer](../../experiments/arc/lspv5_307/php32_exact_mixed_referee307.py), [independent verifier](../../experiments/arc/lspv5_307/verify_php32_exact_mixed_referee307.js), [raw](../../results/raw/arc/2026-11-02_2348_LSPV5_PHP32_EXACT_MIXED_REFEREE307_raw.json). B1/B2/B3 and a superpolynomial worst-case minimum remain OPEN.
<!-- END LSPV5 PHP32 EXACT MIXED REFEREE307 -->


<!-- BEGIN LSPV5 NONAFFINE-LIFT-ER2-COLLAPSE-REFEREE308 -->
## LSPV-5 REFEREE308: nonaffine lifted Tseitin collapses to polynomial ER2 cost (2026-11-03 00:48 PST)

**PROVED/RESTRICTED in unchanged Rmix341; exact finite templates independently replayed; B1/B2/B3 and P versus NP OPEN.** The fresh-output AND3 gap in LSPV-3 LOCAL-PROJECTION356 is avoidable. After its ordinary-Resolution local projection, legal source-independent two-input AND/XOR definitions plus strict Resolution reassociate, permute, copy, and pair-cancel all edge-output occurrences. For connected simple cubic h-vertex lifts,

$$
W_{Rmix341}(F_{G,g,\sigma})\le |E|c(k)+\sum_v3^{M_v}+69(3h)^3+9.
$$

Thus linear-size gadgets with k=O(log h) have polynomial minimum cost. For the explicit AND2 lift,

$$
W_{Rmix341}(F_h)\le1863h^3+\frac{163}{2}h+17.
$$

Twelve ordinary-Resolution templates, including an independent four-gate true-rail certificate, retain 86 RES nodes in 165 certificate lines; independent Node replay PASS. Odd/even K4 controls have 0/8 models and malformed encodings reject. This retires one family only; it is not B1, B2, or B3. [Report](../main/2026-11-03_0048_MAIN_NONAFFINE-LIFT-ER2-COLLAPSE-REFEREE308.md); [handoff](2026-11-03_0048_LSPV5_TO_FIVE_ROLE_NONAFFINE-LIFT-ER2-COLLAPSE-REFEREE308.md); [raw](../../results/raw/arc/lspv5_308/xor_rewrite_er2_referee308.json).
<!-- END LSPV5 NONAFFINE-LIFT-ER2-COLLAPSE-REFEREE308 -->


<!-- BEGIN LSPV5 LOCAL-REWRITE-MITER-FIREWALL-REFEREE309 -->
## LSPV-5 REFEREE309: paid local circuit rewrites (2026-11-03 01:48 PST)

**PROVED/RESTRICTED.** For same-input AND/XOR circuits connected by a supplied, syntactically checked trace of (r) commutativity/associativity rewrites, with (a_i) the number of distinct affected ancestor gates rebuilt at step (i), the fixed source-independent calculus Rmix341 has a shared-DAG refutation satisfying

$$
W_{R_{\mathrm{mix341}}}(M(C_0,C_r)) \le 34r+24\sum_{i=1}^{r}a_i+2.
$$

The exact checker verified 11 templates, 113 strict binary-resolution inferences and 210 retained lines; associative miters are non-clones, SAT neighbors remain SAT, and seven malformed controls reject. Arbitrary semantic equivalence is not covered: an unprovided equivalence oracle would be a forbidden semantic jump. B1, B2, B3 and P versus NP remain **OPEN**.

[Full report](../main/2026-11-03_0148_MAIN_LOCAL-REWRITE-MITER-FIREWALL-REFEREE309.md) · [role handoff](2026-11-03_0148_LSPV5_TO_FIVE_ROLE_LOCAL-REWRITE-MITER-FIREWALL-REFEREE309.md) · [raw certificate summary](../../results/raw/arc/lspv5_309/local_rewrite_miter_referee309.json)
<!-- END LSPV5 LOCAL-REWRITE-MITER-FIREWALL-REFEREE309 -->


<!-- BEGIN LSPV5 LOCAL-COMPILER-COEFFICIENT-REFEREE310 -->
## LSPV-5 REFEREE310: local compiler coefficient correction (2026-11-03 02:48 PST)

**PROVED/RESTRICTED in the unchanged Boolean-local fragment; full mixed calculus and B1/B2/B3 OPEN.** A complete output blocker on at most three variables has one falsifying assignment. Some authenticated premise clause is false there and is a subclause of the blocker, so explicit paid weakening costs at most six nodes. With at most eight blockers per factor, the LSPV-1 compiler359 simulation strengthens from 440 to 48:

$$
W_{L_3}(F)\le W_E(F)\le48W_{L_3}(F)+O(1).
$$

Resolution subsumption closure also gives a 32-node general local compiler (or a <=26-node local refutation). Independent Python/Node replay: 56 signed weakening certificates, all 256 relations, 1,889 entailed clauses, canonical maximum seven RES nodes, both parity labels, 11 malformed and five corrupt controls; 4,114 Node assertions PASS. Raw SHA-256 `7ec254731b204e7bbaba33fe4726911588e7db2197f0b2c86d2da16bf10f331e`. This corrects the coefficient, not the soundness of the prior 440 upper bound. Global XOR/circuit-valued CONVERT, superpolynomial mixed Wbar, B1/B2/B3 and P versus NP remain OPEN.

[Report](../main/2026-11-03_0248_MAIN_LOCAL-COMPILER-COEFFICIENT-REFEREE310.md) · [handoff](2026-11-03_0248_LSPV5_TO_FIVE_ROLE_LOCAL-COMPILER-COEFFICIENT-REFEREE310.md) · [raw](../../results/raw/arc/lspv5_310/local_compiler_coefficient_referee310.json)
<!-- END LSPV5 LOCAL-COMPILER-COEFFICIENT-REFEREE310 -->


<!-- BEGIN LSPV4 PROOF-SLACK-REPLAY358 -->
## LSPV-4 resource audit 358: source-cycle rank controls proof DAG unfolding (2026-11-03 03:36 PST)

**PROVED/EXACT graph theorem, KNOWN Sethi–Ullman register result, COMPUTATIONAL independent strict-RES replay; B1/B2/B3, full mixed-output normalization, superpolynomial worst-case minimum and P versus NP OPEN.** No rule, task, or schedule changed.

For any sound source-explicit at-most-two-premise shared contradiction DAG, retain only its final contradiction ancestry. Let \(s\) be used source clauses, \(q\) charged inference nodes, \(E\) named antecedent edges, \(V=s+q\), \(\beta=E-V+1\) the undirected cycle rank, and \(\delta=\sum_v(2-k_v)\) the missing binary-premise slots. Then:

$$
q=s-1+\beta+\delta.
$$

For clause-minimally UNSAT inputs, sound conservative proofs use all \(m\) indispensable source clauses, so \(s=m\). Full tree unfolding copies each node once per directed path to the sink. Since every non-sink vertex has positive consumer count and \(\sum_{v\ne sink}(d^+(v)-1)=\beta\), the number of paths from any vertex to the sink is at most \(2^\beta\). Thus \(U\le V2^\beta\) unfolded nodes and at most \(s2^\beta\) source-leaf occurrences. A favorable Sethi–Ullman schedule needs at most \(\lfloor\log_2 L\rfloor+2\) simultaneously live value records if distinct output buffers are required. This is an **upper bound on replaying a supplied proof**, not a SAT-runtime lower bound. Controller construction, source/index/head reads, schedule bits, large record fields and all-phase peak scratch remain charged.

**Counterexample to naive DAG-cycle hardness:** An authenticated nonaffine minimally UNSAT five-clause source has a five-step RES proof with one shared source, \((s,q,\beta,U)=(5,5,1,11)\). After eight fresh source splits, \((13,13,1,43)\). Binary selector-gating \(k\) disjoint copies gives minimally UNSAT sources with \(s=5k\), \(q=6k-1\), \(\beta=k\) but \(U=12k-1\). Large \(\beta\) alone does not imply large proof cost or expensive replay. Easy Horn controls have \(\beta=0\). Unary rules contribute \(\delta\) and must not be miscounted as cycles.

Separate Python producer and no-import Node referee replayed all 19 signed RES DAGs (nine fresh splits, five selector groups, five Horn chains): **501 Python assertion groups and 1,440 independent Node assertions**. Small same-source clause-deletion and sign-flip neighbors all SAT; ten malformed DIMACS and two corrupt proofs reject; odd/even K4 controls have 0/8 models. The 96,784 KiB Python and 30,580 KiB Node host RSS measurements are not FLMV writable-space bounds. Full-source materialization still prevents an all-phase \(\rho<1\) claim.

Files read back:
- [Role report](../agents/lspv-4/2026-11-03_0336_LSPV-4_PROOF_SLACK_REPLAY358.tex)
- [Standalone executable](../../experiments/arc/lspv4_358_proof_slack_replay.js)
- [Raw summary](../../results/raw/arc/2026-11-03_0336_LSPV4_PROOF_SLACK_REPLAY358_summary.json)

Root \`main.tex\` was reconciled strictly in a new LSPV-4-owned region using authenticated Git blob read/write and verified that **every old byte outside the insertion was preserved**. Next exact gap: finalize downstream-preserving bounded-record semantics for all Rmix341 LOCAL-CONVERT/DEF outputs and prove an actual charged scheduler, without treating either as B3. The weakest sufficient bridge and superpolynomial worst-case minimum remain OPEN.
<!-- END LSPV4 PROOF-SLACK-REPLAY358 -->


<!-- BEGIN LSPV5 FACTOR-EARLY-CONTRADICTION-REFEREE311 -->
## LSPV-5 REFEREE311: false factors terminate early, improving 48 to 42 (2026-11-03 03:48 PST)

**PROVED/RESTRICTED local simulation correction; exhaustive finite audit independently replayed; B1/B2/B3, superpolynomial worst-case minimum, and P versus NP OPEN.** Keep the preselected Rmix341 and weights unchanged. REFEREE310 compiled each at-most-three-variable output blocker in at most six paid Resolution-plus-source-independent-VARDEF nodes and allowed eight blockers, giving coefficient 48. DPLL-IMPLICATE-PRUNE358's branch compiler is sound, but its statement that the full-factor coefficient cannot improve is false: a satisfiable source entails only a nonfalse output factor, hence at most seven blockers; an unsatisfiable source terminates with contradiction in at most seven nodes. Therefore

$$
W_{L_3}(F)\le W_E(F)\le42W_{L_3}(F)+O(1).
$$

All 6,561 entailed pairs of three-variable relations were enumerated: 6,305 satisfiable-input pairs, 256 false-input pairs, maximum corrected accounting 42 on exactly eight singleton pairs. An explicit unique-model binary source produced seven authenticated six-node blocker certificates (42 total); the false-factor cube resolved to contradiction in seven nodes. A separate Node verifier replayed all definitions/pivots, checked even/odd parity labels, and rejected ten malformed records plus five corruptions. Raw SHA-256: `9f484c07ed07c2c42fe7557c00389943a91cb4792c6227844d49b0d1e585c9d7`.

This is an improved restricted upper compiler, not an exact global mixed minimum. The explicit 42-node control saturates only the prescribed independent-blocker recipe; cross-blocker sharing may improve it. It proves none of B1, B2, or B3 and is not a lower bound. No task identity, enabled state, ownership, or schedule changed.

[Report](../main/2026-11-03_0348_MAIN_FACTOR-EARLY-CONTRADICTION-REFEREE311.md) · [handoff](2026-11-03_0348_LSPV5_TO_FIVE_ROLE_FACTOR-EARLY-CONTRADICTION-REFEREE311.md) · [producer](../../experiments/arc/lspv5_311/factor_early_contradiction_referee311.py) · [independent verifier](../../experiments/arc/lspv5_311/verify_factor_early_contradiction_referee311.js) · [raw](../../results/raw/arc/lspv5_311/factor_early_contradiction_referee311.json)
<!-- END LSPV5 FACTOR-EARLY-CONTRADICTION-REFEREE311 -->


<!-- BEGIN LSPV5 SEMANTIC-CNF-BASIS-COMPILER-REFEREE312 -->
## LSPV-5 REFEREE312: exact CNF bases improve local coefficient 42 to 24 (2026-11-03 04:48 PST)

**PROVED/RESTRICTED computer-assisted local simulation; exhaustive finite classification independently replayed; B1/B2/B3, superpolynomial worst-case minimum, and P versus NP OPEN.** Keep Rmix341, E, L3, and all weights unchanged. Replacing each explicit at-most-three-variable factor by an exact CNF basis, rather than every false-row blocker, is compositional: the basis has exactly the same models, and every downstream local node consumes the same relation.

Using DPLL-IMPLICATE-PRUNE358's safe width costs

$$
 b_1=3,\qquad b_2=4,\qquad b_3=6,
$$

complete dynamic programming over all 256 relations and all 26 nonempty non-tautological clauses proves

$$
\max_{Q\ne\bot}\min_{\Gamma:\operatorname{Mod}(\Gamma)=Q}
\sum_{C\in\Gamma}b_{|C|}=24.
$$

Only even and odd parity attain 24; every exact basis has at most four clauses. Topologically compiling each basis clause from the already authenticated input bases yields

$$
W_{L_3}(F)\le W_E(F)\le24W_{L_3}(F)+O(1).
$$

Independent checks re-enumerated 256 relations and 6,561 entailed relation pairs, replayed an explicit 24-node even-parity basis derivation from a unique-`000` binary source, replayed a one-node false-factor contradiction, checked both parity labels, and rejected twelve malformed records plus five corrupted proofs. Raw SHA-256: `4ce8c020f4f9e98bdd54cc8d382d119876701cc556d81c923c9d0c86dd8f3204`.

This is an improved restricted upper compiler, not an exact shortest joint mixed proof coefficient. Cross-clause sharing, auxiliaries, global XOR, or circuit conversion may lower it. The 256-entry basis map is fixed and input-independent or recomputable by the published finite DP, so it is not instance advice. No task identity, enabled state, ownership, or schedule changed.

[Report](../main/2026-11-03_0448_MAIN_SEMANTIC-CNF-BASIS-COMPILER-REFEREE312.md) · [handoff](2026-11-03_0448_LSPV5_TO_FIVE_ROLE_SEMANTIC-CNF-BASIS-COMPILER-REFEREE312.md) · [producer](../../experiments/arc/lspv5_312/semantic_cnf_basis_compiler_referee312.py) · [independent verifier](../../experiments/arc/lspv5_312/verify_semantic_cnf_basis_compiler_referee312.js) · [raw](../../results/raw/arc/lspv5_312/semantic_cnf_basis_compiler_referee312.json)
<!-- END LSPV5 SEMANTIC-CNF-BASIS-COMPILER-REFEREE312 -->
