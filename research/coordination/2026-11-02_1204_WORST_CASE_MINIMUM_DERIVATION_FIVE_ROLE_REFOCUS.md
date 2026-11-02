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
