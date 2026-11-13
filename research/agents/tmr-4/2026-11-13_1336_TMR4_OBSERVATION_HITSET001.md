# TMR-4 / OBSERVATION-HITSET-001: an all-machine cost-sound abstraction and its linear ceiling

**Report time:** 2026-11-13 13:36 PST (America/Los_Angeles)  
**Owner:** NEW TMR-4 Cost-Sound Abstraction, j15marti/pnp main.  
**Scientific status:** CANDIDATE symbolic construction and proof, pending independent TMR-5 review; COMPUTATIONAL finite audit. P versus NP OPEN.

## 1. Target, falsifiers and scope

**Target:** Provide an explicit all-transition cost-underestimating abstraction of *actual deterministic multitape Turing-machine executions*, rather than derivations in a handpicked proof calculus. Instantiate a nonzero, checkable potential, and determine its exact limitation for unrestricted deterministic 3-SAT computation.

Predeclared falsification controls: (F1) a real machine step, including a source reread, copy, cache, arithmetic operation, reset, or head movement, lacks an abstract successor with charge no greater than one physical transition; (F2) a correct SAT or UNSAT halt maps to a non-goal state; (F3) a zero-cost read of a distinguishing coordinate reduces the potential, or an overlapping perturbation is falsely charged repeatedly; (F4) the constructed potential is treated as superpolynomial despite only L input-bit coordinates; (F5) the abstraction assumes a one-pass, solver-specific inference, or hidden source oracle.

This report extends TMR-2/INPUT-BLOCK-SENSITIVITY-001 from disjoint sets to *arbitrary overlapping opposite-label difference sets* and gives an exact weighted-transition-system simulation/potential theorem. This is a standard decision-tree certificate-complexity idea made explicit as a machine abstraction, **not an original general complexity separation**. Similar abstract simulation/potential methodology already occurs in LSPV-1/589 and LSPV-5/462 for proof DAGs, but those are not all-machine instantiations.

## 2. Precise machine and input semantics

Use TMR-1's single fixed explicit proper 3-CNF bit encoding, with length L, a read-only two-way input tape and endmarkers, finite controller/alphabet, and a fixed finite number of writable work tapes. A is one fixed **total, correct, deterministic** machine for all binary inputs and lengths; malformed strings reject, both valid SAT and UNSAT classify correctly. Every physical transition costs one time unit. A reads at most one source symbol per transition; all physical work, input rereads and preprocessing are included in that one-transition counter. No random-access unit-word model is silently assumed.

Fix a *single valid* input x of length L and its mathematically established decision label b in {SAT, UNSAT}. Fix any finite collection Y={y_1,...,y_r} of **valid, same-length, opposite-label** inputs. Require for each i that the nonempty difference set

$$
D_i=\{j\in\{0,\ldots,L-1\}:x_j\ne(y_i)_j\}
$$

is nonempty. The collection may overlap heavily, may contain repetitions, and may depend on x. It is chosen in the lower-bound *analysis*, not supplied to A as advice or an oracle. Proving that the selected y_i have opposite labels is a separate semantic obligation. No polynomial-time process for discovering all opposite labels is presumed.

A concrete machine configuration c contains the full current fixed program/control state, actual input x, source-head location, all writable tape contents and work-head locations. To express *trace* distinctions without asserting that the solver stores them, augment the exact operational semantics with a **ghost monitor** H consisting of the original input coordinates actually observed on the trace so far. The full concrete instrumented state is (c,H), initial H=empty. A real transition c->c' costs one and updates H'=H union {j} if the transition reads input bit j, otherwise H'=H (including endmarkers). This is conservative bookkeeping by the analyst, NOT an extra machine tape or a free operation in A; projection back to c is the original computation exactly. It is needed because a complete machine configuration can coincide after histories with different prior input observations.

Define

$$
U(H)=\{i\in\{1,\ldots,r\}:H\cap D_i=\varnothing\}.
$$

The source x, label b and difference family D are fixed parameters of the abstract graph, rather than dynamical oracle answers.

## 3. Explicit cost-sound abstract transition system

Abstract states are (b,U) with U a subset of {1,...,r}; goal states are (b,empty), with SAT and UNSAT **distinct** terminal labels. Initial state is (b,{1,...,r}). The relation is

$$
(c,H)\mathrel{\mathcal R}(b,U)\quad\Longleftrightarrow\quad
U=U(H)\text{ and }b=\mathrm{SAT}(x).
$$

Every physical TM transition is represented by **one** abstract edge:

1. If the machine reads input bit j, set U'=U minus {i in U:j in D_i}; cost 1 if any index is removed, and cost 0 otherwise.
2. If it reads an endmarker or performs a step not observing a source coordinate, U'=U at cost 0.

For all abstract states allow the coordinate-j read edges for **every j**, and the zero-cost stutter edge, even if the specific program's current input head could not make that read next. This deliberate MAY overapproximation includes every actual operation: source reading, copying, arbitrary compact algebra, head moves, sharing, rereading, computation after source copying, and alternative encodings. It may admit spurious shortcuts. The cost of each abstract edge is 0 or 1, hence never exceeds the corresponding physical transition's unit charge.

**Terminal preservation proof.** Assume A halts correctly on x with label b while some i remains in U(H). Then A has not read a position in D_i. On the same-length input y_i, determinism gives an identical step-by-step execution: initial configurations differ only in unread cells; induction preserves every read symbol, work tape, head position, control state and halt label. Thus A outputs b on y_i, contradicting the established opposite label. Therefore every correct concrete SAT/UNSAT terminal projects to (b,empty). The argument works with unlimited rereads, all work tapes and arbitrary encodings. It invokes *both-label correctness*, not a proof calculus.

**All-transition simulation theorem (TMR4-H1).** For each correct fixed A, valid x and proved opposite-label family Y, the initial concrete state relates to the abstract initial state; every concrete legal transition c->c' maps to a finite abstract path of length one with abstract cost <=1; and every correct terminal configuration maps to a same-label abstract goal. Concatenating the actual T_A(x)-transition trace yields

$$
d^\#(b,\{1,\ldots,r\})\le T_A(x),
$$

where d# is the minimum cost over abstract paths to the correct abstract terminal. This is an exact universal *cost-soundness* assertion conditional only on the proven input-label premises; it is **not** a lower bound on SAT time beyond what is computed below. No step restriction to DPLL, Resolution, proof production, a single memory representation or a one-pass streaming protocol occurs.

## 4. A genuine potential and exact abstract optimum

Define the hitting-set number for U:

$$
\tau(U)=\min\{|J|:J\subseteq\{0,\ldots,L-1\},\ 
J\cap D_i\ne\varnothing\text{ for every }i\in U\},
\qquad \tau(\varnothing)=0.
$$

Set Phi(b,U)=tau(U). Every stutter has unchanged potential and zero charge. For any read j taking U to U', adjoining j to a hitting set for U' covers every removed D_i, so

$$
\Phi(b,U)\le 1+\Phi(b,U').
$$

Even when the read has no effect and is charged zero, U'=U and the inequality holds with zero. The goal potential is zero. Hence Phi satisfies the exact lower-bound inequality on **every** MAY edge, including zero-cost cycles, and telescoping proves

$$
\boxed{\tau(\{1,\ldots,r\})\le d^\#\le T_A(x).}
$$

In fact the abstract optimum is *exactly* tau. For the lower direction, any successful abstract path must read a set of coordinates meeting every D_i. For the upper direction, the MAY graph can read the elements of a minimum hitting set, one charged edge each, reaching the goal at total cost tau. Hence

$$
d^\#=\tau(\{1,\ldots,r\}).
$$

**Crucial limitation:** tau<=L, since the full coordinate set is always a hitting set. Even an exponentially large opposite-label family has an abstract optimum at most L. After one complete input observation U is empty even if the actual algorithm needs enormous additional work to decide SAT. No amount of optimizing this pure *first-observation* domain can yield a superpolynomial lower bound. Computing tau itself or proving opposite labels may be expensive for an analyst; no such cost is assumed or credited to the algorithm. This is an exact precision ceiling of the proposed abstraction, NOT a proof of a 3-SAT complexity upper bound or of P=NP.

With *all* opposite-label length-L valid inputs included, tau is the usual input certificate complexity of the total Boolean language obtained by labeling malformed strings REJECT, except that this version's Y restricts to valid inputs. The full-language certificate characterization also follows by allowing all opposite-label binary strings, including malformed strings, and using the same proof. This pre-existing decision-tree concept is recorded in [2].

## 5. Nontrivial strict-3CNF instantiation and hostile shortcuts

Apply the theorem to the TMR-2 equality family E_(a,b), using the precise five-bank proper-width-three encoding. On a fixed satisfiable E_(a,a), the 2n perturbations switching four x_i sign bits in one prefix/suffix unit gadget are all valid UNSAT encodings and have pairwise disjoint nonempty difference sets D_i. Thus

$$
\tau(\{1,\ldots,2n\})=2n,\quad
T_A(E_{a,a})\ge 2n
$$

for *every* all-input correct deterministic A. Its length is L(n)=13n+2+24n(1+max(1,ceil(log2(5n)))). This recovers TMR-2's result inside an explicit all-transition machine abstraction and formalizes its exact potential.

**Overlapping-control falsifier.** Let D1={0,1}, D2={1,2}. Naively charging two independent necessary distinctions produces 2, but a single read of coordinate 1 distinguishes both; tau=1. Likewise four identical sets D_i={0,1,2,3} give tau=1, not four. Summing separate local bounds without disjointness or a proved cost partition is invalid.

**Missing-edge falsifier.** Adding any *genuine* zero-cost abstract edge from nonempty U straight to the goal collapses the abstract optimum to zero and makes Phi(U)>0 violate Phi(U)<=0+Phi(goal). Such a shortcut cannot be erased merely to rescue a desired bound if it represents an actual concrete transition. Conversely, when it is a pure abstract artifact, one must prove it spurious before refining it. This is consistent with the older project paid-history erasure counterexample [4].

**Controls and representation coverage.** Horn, 2-SAT, XOR/Tseitin with elimination, bounded-treewidth DP, products, renaming, padding, fresh auxiliaries and arbitrary recomputation are all included as possible A operations because every physical transition is mapped without inspecting the machine's chosen representation. No claim is made that those controls require more than the certified 0..L first-read cost. TMR-1's source-copy simulator is fully admitted: B reads the source once, after which abstract U may be empty and the remaining B computation is cost-zero in this abstraction. TMR-3's multipass restriction is not imported; it is a separate, more precise restricted model and may yield a superlinear tradeoff there.

## 6. Reproducible executed finite audit

Executed deterministic JavaScript in hosted V8, without randomness, using the exact function later published as a standalone .cjs script:

- Code: experiments/tmr/tmr4_observation_hitset_audit.cjs.
- Immutable data: results/raw/tmr/2026-11-13_1336_TMR4_OBSERVATION_HITSET_RAW.json.
- Enumerated 80,237 families for L=1..6, family cardinality <=4 for L<=5 and <=3 for L=6, plus 6 disjoint cases (r=2n up to 12) and 2 overlapping hostile controls.
- Checked 4,388,166 abstract read-edge potential inequalities, 819,087 exact nonempty abstract-state min-cost identities, all successful.
- For r=2n disjoint sets n=1..6, potential was exactly 2n. For two overlapping sets or four identical sets, potential was exactly 1.
- Added a deliberately invalid zero-cost-to-goal shortcut and verified the potential inequality would fail.
- The finite audit validates the graph arithmetic. It does **not** execute a physical TM, prove family SAT semantics independently, establish asymptotic lower bounds, or discover a general 3-SAT algorithm. A native Node CLI, repository-wide preflight and LaTeX compile were not executed.

## 7. Corpus, statuses, dependencies and next task

Read the superseding TMR five-agent directive first, checked again before publication. Recovered BOTH proof trackers and main.tex via Git blob reads after ordinary fetch_file returned blank for the two large files; reviewed their status headers, goals and relevant end sections. Read issue #3 through newest TMR-2 note, AGENTS.md, CODEX.md, repository research skill, TMR-1/001 and TMR-2/001 full reports/handoffs, TMR-3's newly published handoff, and relevant historical originals LSPV-1/589, LSPV-5/462 and Claude ONETAPE-0001. TMR-5 handoff was not yet available. The older historical proof-DAG abstractions are different models and are not silently promoted to SAT runtime. TMR-2's source-acquisition result is reused, not attributed as new. This report's incremental contribution is a full-history instrumented TM simulation with an exact hitting-set potential and explicit proof of its linear ceiling.

**D0 model: KNOWN THEOREM. TMR4-H1 full-step machine simulation: CANDIDATE until TMR-5 independent review. Exact potential/abstract optimum: CANDIDATE until TMR-5 review. Finite audit: COMPUTATIONAL. Unrestricted superpolynomial D4: OPEN. P versus NP OPEN.** Root [P1-01/03/04] and [P2-D1/C3/B1/B2/B3] unchanged. The new direct-machine theorem is *not* old proof-calculus P2-C3. TRACKERS REVIEWED; NO MATERIAL CHANGE. TMR-5 synthesis ownership blocks any TMR-4 edits to canonical root main.tex until an authorized TMR-4 region exists.

**Next concrete question for TMR-2/3/4:** define and falsify a *repeated computation/reconstruction* charge that survives a full source copy and arbitrary algebraic summaries; prove it is obligatory for every correct machine using a new exact all-transition simulation. A read-footprint-only domain cannot satisfy the needed superpolynomial criterion. TMR-5 should independently test ghost-state soundness, terminal labeling, overlapping-set cost-sharing and the all-machine quantifiers.

## References

[1] P. Cousot and R. Cousot, "Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints," POPL, 1977, pp. 238-252, DOI: https://doi.org/10.1145/512950.512973 . Primary author publication page: https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml .

[2] H. Buhrman and R. de Wolf, "Complexity measures and decision tree complexity: a survey," *Theoretical Computer Science* 288(1), 2002, pp. 21-43. https://doi.org/10.1016/S0304-3975(01)00144-X . Author PDF: https://homepages.cwi.nl/~rdewolf/publ/qc/dectree.pdf .

[3] TMR-2, INPUT-BLOCK-SENSITIVITY-001, research/agents/tmr-2/2026-11-13_1315_TMR2_INPUT_BLOCK_SENSITIVITY001.md .

[4] LSPV-5/462, paid-history erasure counterexample, research/agents/lspv-5/2026-11-09_0759_LSPV5_PAID_HISTORY_ABSTRACTION462.md .

[5] LSPV-1/589, may-edge potential formalization, research/agents/lspv-1/2026-11-12_0400_LSPV-1_MAY_POTENTIAL_DUAL589.tex .

END_OF_REPORT::TMR4_OBSERVATION_HITSET001::2026-11-13_1336_PST
