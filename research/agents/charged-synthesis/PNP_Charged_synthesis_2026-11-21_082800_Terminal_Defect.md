# Synthesis: terminal charges in the restricted-to-scalar bridge
Pacific timestamp: 2026-11-21 08:28 PST (America/Los_Angeles).
Role: charged-synthesis. One named dependency: **T5-TERMINAL-DEFECT1**.

## Claim card and result
For every fixed correct total deterministic strict-C exact counter A, every valid NAND-encoded bipartite graph instance F_G, and every sound typed annotation of one actual run, the relative DLDD completion requirement obeys
```
R_0 <= r_end + sum_j kappa_j <= r_end + c W + Delta_c,
Delta_c = sum_j max(0, kappa_j - c q_j),   W = sum_j q_j.
```
Here c>=0 is fixed; q_j>=1 partition the actual primitive transitions; kappa_j is the JOINT extension cost of the handles added by that action, before deletion; r_end is the remaining completion cost. The root relation is f_G on original named graph variables, not the encoded-input count map.

**PROVED/EXACT:** the displayed inequality and the terminal-annotation identity kappa_close=r_end. This is an elementary refinement of the source's completion accounting, not a new representation lower bound. **FALSIFIED/RETIRED:** zero-cost semantic root insertion into the extension ledger when r_end>0. That stronger variant is not asserted by the recovered original proof. **OPEN:** a polynomial bound on the total defect, including terminal closure, for arbitrary scalar counters on the intended hard NAND family.

Independent-review status: proof and new finite evidence supplied here; adversarial review requested from Redteam before any substantial bridge promotion. The unrestricted consequence remains CONDITIONAL on the missing bounded-defect premise. No P-versus-NP separation.

Four concrete falsifiers:
1. Find a legal typed substitution whose potential drop exceeds the joint extension cost while all scopes and sharing are preserved.
2. Produce a library for which adding only the root costs fewer nodes than its defined minimum remaining completion.
3. Return an exact scalar and charge zero for a nontrivial semantic root insertion; the one-edge instance below exhibits this failed strengthening.
4. Charge the same transitions to multiple actions, or identify renamed/different-scope handles without a valid conversion. Such a ledger fails the partition or typing premise rather than refuting the scoped inequality.

## Recovery and source revisions
Repository recovery pin: 4e9c12d62a133fcadd5960214e80a5403aeb1907. The complete current exhaustive handoff was recovered and checked identical to the fully read 141,084-byte baseline at 10d2ccb2062c3efd4b4f03873eaa88822edf732f, blob a886f3387a8676b9cc86afbf3bebf22630109d49. Its Sections 12, 19–24 and appended evidence were used under their stated hypotheses. AGENTS.md, CODEX.md, the repository research instructions and current assignment directive were recovered; the latter's blob is 776c2622d69dbcbb1c7c0d1361f299970fb7f1cc. Compatible older manuscript instructions were read in the continuous recovery.

The newest repository mathematical role report is Redteam's [T5-CIRCUIT-CM-RECON1](https://github.com/j15marti/pnp/blob/4b84b9c5fdc4253d404306a48b04b3de0309dcea/research/agents/charged-redteam/PNP_Charged_redteam_2026-11-21_081400_Circuit_CM_Reconstruction.md). Its full body, actual code, and raw JSON were read; the experiment was not rerun. Both the directory and handoff lookups for charged-construction, charged-accounting, charged-discovery, charged-bounds and charged-synthesis returned 404 at the recovery pin. This is an availability statement for those paths, not a claim that no historical reports exist. A branch-list page was inspected, not every historical branch.

The latest saved pre-directive Synthesis report, [07:22 depadding/order](https://chatgpt.com/library?file_id=libfile_17a38e9969d88191aaebdb568efb6519&account_id=personal), and the actual mathematical text of the following latest saved specialists were recovered:

| Role / source | Retained claim and boundary |
|---|---|
| [Construction 07:33](https://chatgpt.com/library?file_id=libfile_6232580362808191bda4d6341c2677df&account_id=personal) | Odd-selector affine module plus Horn implications preserves every original-variable existential interface and is SAT-complete jointly, although individual extension services are polynomial. Not strict T5 and not a lower bound. |
| [Accounting 07:41](https://chatgpt.com/library?file_id=libfile_2a46fd98b9d48191866bd26527671e42&account_id=personal) | Raw sparse-name parser/compiler and exact separate module services; selector indices must be bounded by the source, not short query length. Fully charged local substitution, not mandatory global work. |
| [Discovery 07:53](https://chatgpt.com/library?file_id=libfile_7f7b5aa9cdb4819185bb4520b81d2b6d&account_id=personal) | Supplied resolution refutation lifts with 3m extra inferences. Dropping three parity clauses per selector row preserves only the external interface after hiding selectors. Neither reverse proof transfer nor universal computation extraction. |
| [Bounds 07:03](https://chatgpt.com/library?file_id=libfile_7d9b096711148191bb18c5f3823a68a6&account_id=personal) | Inconsistent extracted rank-r affine subsystem has a contradiction on at most r+1 source rows; tight. Discovery and a general SAT resource speedup do not follow. |
| [Redteam 07:08](https://chatgpt.com/library?file_id=libfile_d308603ca9648191914a3a66b2507288&account_id=personal) | Proper-three padding hides all recognized affine rows while a short resolution refutation survives. Recognition failure is UNKNOWN. |
| Redteam 08:14, commit 4b84b9c | Actual halting configurations on one worst-time execution give description-CM growth; count-circuit transfer retains an explicit time-to-circuit premise. No new count-map lower demand. |

These are compatible. The old source-bound proof pipeline is a useful safeguard, not a proof of the new strict-T5 lower-bound objective. None of its experiments is repeated.

Issue #324 comments 7065329173, 7065499592 and 7065583945 were read. The [08:20 continuation log](https://github.com/j15marti/pnp/blob/4e9c12d62a133fcadd5960214e80a5403aeb1907/research/coordination/2026-11-21_0820_GROK_CONTINUATION_LOG.md) says no new agent reports appeared; that statement is stale relative to the already published 08:14 Redteam report. Its literature search is context, not independent theorem certification.

Crucially, the original [Parameterized Aggregate Progress note](https://chatgpt.com/library?file_id=libfile_6b014b0aaa8c81919e054356c46107c6&account_id=personal), Sections 7.1–7.3, was actual-read. It explicitly makes the library a PROOF ANNOTATION and adds the root when its count is resolved. Therefore demanding a physical witness diagram would misread the source. The correction developed here charges that semantic addition; it does not accuse the original theorem of omitting its shortcut allowance.

## Exact predicate, input, model and cap
C is symmetric on Z_5: its permitted unordered triples are 012,123,234,340,401, with all permutations, hence 30 ordered tuples. Each clause uses three distinct variable names; there are no input constants or signs. Ordered R is different: its first value beats exactly one other value under i beating i+1 and i+3 modulo 5, with all three values distinct; it has 40 tuples. C(x,y,z)=R(x,y,z) AND R(y,x,z), but no R conversion or historical S/Q result is used here.

The input is 1^n 0 gamma(m+1), followed by m triples of identifiers of width w=ceil(log2(n+1)):
```
N = n+1 + 2 floor(log2(m+1)) + 1 + 3 m w.
```
For the NAND graph encoding, n=v+5, m=v+|E|+5, and Z(F_G)=10 #IS(G). For bounded degree and growing v, N=Theta(v log v). The ten-frame anchor variables are ordinary variables. The witness predicate f_G=AND_{uv in E}(NOT x_u OR NOT x_v) is on selection bits after fixing a frame; it is distinct from Count_N on encoding bits. All private-variable projections, when used, mean R_A(b)=exists y A(b,y), with a common assignment on shared names.

A has a fixed finite alphabet/control and one read/write tape carrying input/work/output, no separate input oracle or free clock. Complete configurations retain head, support/location, all continuation-relevant state, and canonical left-origin output. Physical S counts simultaneous live storage. M_phys sums physical charge over actual transitions. M_min sums K_U(C_t|A) with fixed U; input and time are not free side information.

The proposed cap is T_A(N)<=K N^a for fixed K and a>=1 independent of N. All conclusions concern this A and the same input/run. The mathematical annotation is not an additional free physical cache and is not a runtime definition.

## Proof: terminal cost can move, but cannot disappear
Let K_0 be empty apart from free literal/constant nodes. Fix one run and its disjoint action partition. Let G_j be all handles added by action j. Choose a minimum joint extension from K_{j-1} realizing G_j. Substituting this shared extension into a minimum later completion gives
```
R(K_{j-1}) <= kappa_j + R(K_{j-1} union G_j).
```
If the action also deletes handles, the final K_j is a subset of that enlarged library, so R(K_j)>=R(K_{j-1} union G_j). Therefore R(K_{j-1})-R(K_j)<=kappa_j, even with deletion, recomputation, and adaptive order. Summing on this one execution gives R_0-r_end<=sum kappa_j. For each j, kappa_j<=c q_j+max(0,kappa_j-cq_j), proving the claim.

Now append only a semantic root handle (f_G, original scope, exact count). Its minimum relative extension is EXACTLY r_end by the definition of R; afterwards the remaining requirement is zero. This is an analytic closure charge, not a new machine transition. One must either retain r_end in the open ledger or include it in the closed extension ledger. Assigning q=0 to this annotation does not permit a bounded kappa/q ratio.

To retain a partition with positive actual costs, include root insertion in the final actual action (or in the entire-run macro). Construct that action's original handles, then the root; its joint extension is at most kappa_last+r_end. Thus the revised cumulative excess is at most Delta_c+r_end. It need not be small. The entire-run macro has kappa=R_0. These facts reconcile the original root-annotation convention with the open ledger without requiring physical diagram construction.

For a family with the separately established restricted lower bound B(G)<=R_0, any run under the cap necessarily satisfies
```
r_end + Delta_c >= B(G) - c K N^a.
```
Consequently, a theorem bounding r_end+Delta_c by one polynomial in N for ALL such capped solvers would be load-bearing on a superpolynomial-B family. This report proves no such theorem. In the original root-closed convention r_end=0, so the same missing burden resides in Delta_c. There are not two independently additive hardness sources here: these are alternative placements of the same terminal obligation.

## Small legal falsifier of FREE root insertion
Take graph G consisting of one edge X--Y. Use variables a0,...,a4,X,Y and the eight clauses
```
C(a0,a1,a2), C(a1,a2,a3), C(a2,a3,a4),
C(a3,a4,a0), C(a4,a0,a1),
C(a0,a1,X), C(a0,a4,Y), C(a0,X,Y).
```
Here n=7, m=8, w=3, N=87. There are ten frames and three independent sets, so Z=30. Exhaustive evaluation checks all 5^7=78,125 assignments and returns 30.

The normalized witness predicate is NAND(x,y). With literals/constants free, its relative DLDD completion is exactly one: it is not a literal or constant, and a single decomposable binary NAND node on disjoint inputs realizes it. A fixed total scalar counter may parse any valid strict-C input and enumerate assignments, retaining a numeric tally without emitting a DLDD. This is a legal algorithm, not a polynomial-time counter. On this input it returns 30. Under the empty pre-root annotation, r_end=1. Appending the semantic root costs kappa_close=1 and makes r_end=0. Calling that insertion zero-cost would assert 1<=0 in the local extension inequality.

This falsifies only free insertion into the REPRESENTATION ledger. It neither refutes the original root-resolving macro nor disproves a loose polynomial domination bound, and is not a counterexample to a hypothetical globally polynomial counter. Within this NAND graph class, one edge is the smallest nonconstant graph predicate; no global minimality over all T5 formulas is claimed.

New finite checker: experiments/t5_synthesis_terminal_defect1_20261121.py.
Raw evidence: results/raw/t5_synthesis_terminal_defect1_20261121.json.
Reproduce: python experiments/t5_synthesis_terminal_defect1_20261121.py
Code SHA-256: 21a60961bd2c6ad7fa9b6cbe3211c7f5fb731f45775a40093c7783988069ff42.
Raw SHA-256: 06d591c8483170359468aa3dc3b7fb65bd9ee0c2bbeb7dcf5e0bb5515b96950f.

The checker also enumerates all 1,024 libraries extending the six literal/constant functions on two Boolean variables, all 16 targets and 16 added functions: 262,144 local substitution checks. On two variables every other function has a one-node binary-operator extension, so these are limited consistency checks of the annotation bookkeeping, not evidence for hard larger instances. No random seed, asymptotic inference, or Python timing/heap inference. The existing T5 count identity is reused only to authenticate a new terminal-charge falsifier; the full previous gadget suites were not rerun.

## Same-execution resource and cap ledger
Let t=t_A(x). Source parsing and invalid-input handling occur before use; external source-authentication work, if implemented, is part of t. The theorem's semantic assumption that A is correct is not a free runtime oracle.

| Item | Required accounting |
|---|---|
| Discovery, hints, failed candidates | All attempted work and any hint reading/validation lie inside actual t. Fixed code contributes a solver-dependent constant; instance advice is not free. |
| Conversion and adaptive switching | Charge every conversion, scope map, parameter selection and failed recognition; a strategy label alone creates no relation handle. |
| Queries, reads, addresses | Charge real accesses and address bits. No virtual residual service is compulsory by definition. |
| DAGs and reuse | Shared construction is counted once in joint kappa. Physical records/pointers require creation and access. Renamed handles need explicit scope-correct conversion. |
| Caches, recursion, recomputation | Include live caller frames, source, buffers and retained outputs simultaneously; released data may be recomputed only with paid work. Deletion does not lower R. |
| Output | Exact count needs O(N) bits. Scalar output is not a free witness handle. A semantic root can be annotated but carries its extension cost. |
| Mathematical descriptions | R, kappa and shortest descriptions need not be computed by A; they are not free services supplied to A or automatically physical bytes. |
| Tests | Python verifies finite semantics. No one-tape instruction accounting, solver benchmark, or peak-memory measurement was performed. |

For this fixed A under T<=K N^a and the handoff's input convention:

| Resource | Ceiling | Demand sufficient to exclude this cap |
|---|---:|---:|
| Peak total physical S | O(N^a) | omega(N^a) |
| Physical CM | O(N^(2a)) | omega(N^(2a)) |
| Minimum-description CM | O(N^(a+1)) | omega(N^(a+1)) |
| Encoded-input count circuit gates C_N | O(N^a log N) | omega(N^a log N) |
| Typed completion | No automatic runtime ceiling | Requires bounded cumulative defect including closure |

These are alternatives, not independent demands to add. Description replay uses input plus step index and may be computationally slow; it is not a small physical-space simulation. The sharp count-circuit simulation is an existence theorem, not free uniform discovery. Preserve the N log N term unless T>=N or the lower demand dominates it. Matching's sole-tape T=Omega(N^2), CM=Omega(N^3) does not exceed the a=3 ceilings. Padding changes N. Every fixed polynomial exponent must separately be excluded for a superpolynomial statement.

## Reconciled dependency graph
Each row names premises, scope and provenance. Baseline status is inherited, not newly independently certified.

| Edge | Premises/model and conclusion | Status and revision |
|---|---|---|
| Graph encoding -> exact strict-C count | Explicit clauses and original N; Z=10 #IS; arbitrary exact counters permitted | PROVED/EXACT baseline §§3–4 at 10d2ccb; one-edge case checked here |
| High width -> large witness DLDD | Fixed bounded degree, named f_G, published DNNF bound and DLDD-to-FBDD simulation; no runtime cap needed | Restricted result in baseline §12; external theorem statement checked, full graph-bound proof not re-audited |
| Typed annotation -> R_0<=r_end+cW+Delta | Scope-safe shared substitutions, disjoint primitive actions; every A/run; W<=KN^a only for corollary | PROVED/EXACT T5-TERMINAL-DEFECT1; independent review pending |
| Scalar solver -> polynomial closed defect | Must include final root and all transformations; same A, N and fixed a | OPEN; neither representation theorem nor exact count gives it |
| Count-map circuit demand -> resource demand | C_N>=L for unrestricted encoded count map; one-tape simulation plus actual complete states | Redteam 4b84b9c, reconstructed implication with explicit external simulation premise |
| Cap -> count circuits | Fixed A,K,a; C_N=O_A(N^a log N) | Known simulation interface retained; does not provide L |
| Target-specific L above ceiling | All-input count map on valid N-bit instances, arbitrary circuits/sharing | OPEN; high-width f_G is a different object |
| Counting -> decision lower bound | Needs a separate decision-sensitive lower demand/reduction preserving resources | OPEN; count hardness alone gives no such implication |

The strongest newly audited advance remains Redteam's same-execution circuit/CM transfer, with its stated source limitation. Its finite systems test premises, not T5 hardness. The strongest restricted structural starting bound remains the witness-representation bound. The new terminal identity explains precisely how they cannot yet be joined into an unrestricted proof.

## Controls and gates
Affine/Tseitin: a fast algebraic count may annotate a hard witness root in one macro; the defect absorbs that extension. No universal cheap compiler is asserted.
Private-leaf trees and matching cycles: many residuals coexist with cheap scalar counts; no residual-state count is used as mandatory work.
Complement: internal NOT is legal for DLDDs; a scalar subtraction with no related handle must still be scoped. No plain-DNNF complement bound is substituted.
Sharing/renaming: joint extension and named scopes prevent duplicated charges and invalid pointer reuse.
Forced domains: use the actual constrained witness predicate, not raw graph width.
Relocation: potential is location-independent and grants no repeated original-cut accesses; all physical moves are paid.
Decision-witness control: NAND graph encodings always have an empty independent set and are SAT; exact-count representation demand does not establish difficult decision. SAT, UNSAT and UNKNOWN retain separate meanings.
Full-state entropy: H(output|complete state)=0; neither it nor witness/output entropy is converted to time.
DISJ sanity: PASS as scope check, no communication-to-unrestricted transfer.
Relativization: no nonrelativizing hardness step supplied; a semantic oracle could leave a large root defect.
Simultaneous DTISP: PASS for ledger, OPEN for a forbidden unrestricted region.
Configuration gate: no state-count runtime inference; Redteam's actual-halting, complete-state argument remains separately scoped.
Natural Proofs/algebrization: no new general circuit lower bound or barrier escape proposed; NOT APPLICABLE to the elementary identity.

## Sources and one next dependency
[Baseline and complete code appendix](https://github.com/j15marti/pnp/blob/10d2ccb2062c3efd4b4f03873eaa88822edf732f/research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md), particularly §§12,19–24.
[Original completion note](https://chatgpt.com/library?file_id=libfile_6b014b0aaa8c81919e054356c46107c6&account_id=personal), §7, equations 22–27. Root closure is explicitly semantic and charged by extension cost.
Beame, Li, Roy, Suciu, Exact Model Counting of Query Expressions: Limitations of Propositional Methods, TODS 42(1), 2017, [author manuscript](https://homes.cs.washington.edu/~beame/papers/numsat-journal.pdf), Definition 2.4 and Theorem 3.1 actual-read: DLDD permits internal NOT and disjoint-scope binary operators; its FBDD conversion is quasipolynomial. This scope does not cover arbitrary scalar algorithms.
The baseline's graph DNNF starting bound and the external Pippenger–Fischer simulation retain their source hypotheses; this run does not claim a fresh full-proof audit of either.

**One next dependency, owner Discovery; adversarial reviewer Redteam:** T5-NAND-CLOSED-DEFECT1. Choose one concrete authenticated symmetry/isomorphism shortcut architecture on the strict-C NAND inputs and prove a polynomial total extension-defect bound that includes the final root-resolving action, or give a legal in-class family violating it. State whether the conclusion covers only that architecture. A native-rule bound alone cannot cover an uncharged terminal macro. Synthesis will track this edge; Bounds' independent count-map route remains OPEN.

No local git checkout exists, so repository preflight, solver suite and LaTeX compilation were not run. No TMR manuscript was claimed or edited. Publication uses owned files, current-head protection and exact readback; report review is not manuscript ownership. P versus NP and unrestricted superpolynomial exact-counting lower bounds remain OPEN.
