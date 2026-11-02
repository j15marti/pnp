# LSPV-3 GATE317: Paired canonical SAT with exponentially many continuation classes and polynomial decision work

**2026-11-01, 18:24 PST. PROVED/EXACT restricted mathematical construction; COMPUTATIONAL separate no-producer-import verification (448 assertion groups), independent external mathematical review pending. P versus NP OPEN.** This is a *decision-only* work obstruction, not an arbitrary-decider lower bound.

## Exact target and hypotheses

The only original language is valid duplicate-free proper clausewise-monotone Döcker 3-SAT-(2,2): three distinct same-sign literals per clause, every original variable occurring exactly twice positively and negatively; malformed encodings reject. Coherent original-variable pins produce possibly noncanonical residuals.

F1 **FALSIFIED**: a SAT certificate for a fully complementary-paired original remains valid under every coherent future pin. F2 **FALSIFIED**: exact current SAT/model-count equality implies equivalent future decisions. F3 **FALSIFIED**: exponentially many continuation classes imply exponential mandatory decision work. F4 **OPEN**: a polynomial total-work uniformly acquired selector exists on every valid original.

## Source and mathematical theorem

Base original K has positive supports (123),(145),(246),(356) and the matching four negative complements. It is a valid canonical six-variable eight-clause source, with 18 satisfying assignments. Exact original-source counts:
- #SAT(K|x1=0,x2=0)=3; #SAT(K|x1=0,x2=1)=6.
- Appending x4=0 gives respectively 0 and 3, with no already-falsified original source clause. In the zero case, positive source clauses C0,C1,C2 respectively force x3=1,x5=1,x6=1, contradicting C7=(-x3 OR -x5 OR -x6).

For t>=1 take 2t numbered K blocks indexed cyclically by j. In *both* the positive and negative copies of the first clause in block j, replace x_(j,1) by x_(j-1 mod 2t,1). All other source occurrences are unchanged. Call the original P_t. Each variable loses one positive and one negative occurrence and gains one of each in the successor block. Supports remain proper and duplicate-free, and clause incidence remains connected via cross-block first-clause supports and the remaining within-block three supports. The formula is fully complementary paired and has n=12t, m=16t.

Pin every x_(j,1)=0. Divide blocks into t ordered two-block superblocks i. In profile A pin (x_(2i,2),x_(2i+1,2))=(0,1); in profile B pin these values (1,0). Each superblock has 3*6=6*3=18 extensions. For any word w in {A,B}^t, with associated coherent pins p_w, and for r_i={x_(2i,4)=0}, the exact **all-t theorem** is

    #SAT(P_t|p_w)=18^t>0,

    #SAT(P_t|p_w,r_i)=0                       when w_i=A,
                          =9*18^(t-1)        when w_i=B.

Proof: all changed interblock source occurrences concern x1 pins fixed to zero, hence every residual formula factors exactly into its unmodified local K residuals. The local counts above multiply, with a shared original-source unit contradiction for the A continuation. Any two distinct words differ at some i, and the same r_i separates their SAT decisions. Thus the **2^t SAT prefixes have the same exact current model count but occupy 2^t distinct declared continuation classes**.

With fixed common continuation r_all=union_i r_i, SAT iff w=B^t; the single SAT word has 9^t extensions. On the explicitly *promised profile-bit input model*, the accepting B^t execution has exact deterministic decision-query complexity t: each one-A opposite-label neighbor differs only in two pin-value positions of a disjoint superblock, so at least one read per superblock is necessary; one discriminator read per superblock achieves t. This is a **linear** query bound on external coherent pins of a fixed valid original, not a lower bound for all valid canonical-original SAT sources. An irreversible no-reread continuation interface needs at least t retained bits, but an indexed rereadable original can replay histories with charged rereads, so the static FLMV space implication is invalid.

## Existing polynomial alternative and duplication audit

Fully paired originals with coherent pins admit polynomial exact SAT decision via a **KNOWN** graph degree-interval (g,f)-factor algorithm. Make one cubic graph vertex per positive/negative paired source support, and one labelled edge per original variable. If a_v incident edges are pinned TRUE, and d_v are free, the residual demands

    max(0,1-a_v) <= free_TRUE_degree(v) <= min(d_v,2-a_v).

The resulting undirected (g,f)-factor feasibility test is polynomial in explicit source size. This graph-factor reduction and the fully paired satisfiability theorem were already present in Döcker's paired corollary and project LSPV-2 REVERSE-SELECTOR57, WITNESS-DEFECT58, BLOSSOM-FACTOR60 and M22-DEFECT-ADAPTER131. GATE317 **does not claim originality for the matching theorem or source-dual representation**. It supplies a connected, fully paired and equal-exact-count exponential-continuation collision with an already known paid all-future-pin polynomial decider as a hostile model.

## Full charge and status

For original input bit length N=Theta(t log t), a grammar, sign-quota and support-pairing scan, coherent pin/source/index/head lookup, factor acquisition, failures and policy switching, proof and source verification, cache/replay, child/output access and guest DELAY/COPY/RECOMP all remain charged. The generic execution identity is

    W_D(R) = C_grammar+source/index/head+discovery+selection/switch/failed
          + C_GE/matroid/factor/proof/cache/replay+child/output/access+guest
          + sum_{executed successors R'} W_D(R').

S_peak counts all simultaneously live writable/index/ancestor/graph/matrix/cache/proof/guest/output bits. A decreasing free-variable potential bounds one branch but not summed descendants. The paired factor terminal uses polynomial word work, **not proven** FLMV N^(6/5) indexed-native time or N^(1/2) simultaneous space. Exact fallback for general canonical originals may be exponential. The logical XOR calculation is OFFLINE only.

The all-input polynomial-work controller, representation-independent arbitrary-A hereditary power-short A->Phi(A), strict SAME-MACHINE numerical FLMV transfer, and both P=NP and P!=NP remain **OPEN**.

## Independent controls and sources

Full local research archive in the original research run contains the complete manuscript, full producer, separately written no-producer-import verifier, 63 producer and 448 independent assertion groups, independent complete source enumeration of every word and continuation at t=1,2, component multiplication through t=3, source grammars through t=16, complete original-clause SAT witness, UNSAT unit clauses, UP-first DPLL comparisons, F9/Y6/F15 original model counts 70/20/1032, F15 SAT/UNSAT cube labels 2/0, all F9 264 SS/SU/US/UU modes (feasible 37/49/49/37), six malformed tests, 0^n/1^n and complements, and OFFLINE F9 binary/Gray complete aligned logical XOR 4977/3585. U198/V198 previously verified and **not replayed** this run.

**Primary literature**: Döcker, Monotone 3-SAT-(2,2) Is NP-Complete (2019), https://arxiv.org/abs/1912.08032 ; Fortnow et al., Time-Space Lower Bounds for Satisfiability (2005), https://doi.org/10.1145/1101821.1101822 ; Gabow/Sankowski, Algorithms for Weighted Matching Generalizations II, https://doi.org/10.1137/16M1106225 ; de Colnet/Szeider/Zhang, https://doi.org/10.24963/ijcai.2024/367. Prior project reports LSPV-3 GATE314/315/316 and LSPV-1 18:00 high-width paired source were read, with scope and duplication recorded. Project GitHub searches: "paired support nonbipartite", "maximal matching Hall paired", "GATE314", "GATE315"; github.com/openai searches: "SAT", "NAE-3SAT", "dnnf", identifying generic Lean SubexponentialSAT material but no applicable M22 all-input theorem. Absence of hits is not evidence of novelty.

**Next gate**: Paid compositional switching among graph (g,f)-factors, GATE315 future-pin-closed affine matroid components and GATE316 exact parity on connected *nonpaired* canonical originals, with explicit polynomial aggregate acquisition or a concrete counterfamily. P versus NP remains OPEN. No task identities, statuses or schedules changed.
