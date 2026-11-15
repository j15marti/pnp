# TMR-5/038: Selected-interpolant circuit hardness does not lower-bound cheapest separation; independent leaf-core replay

**2026-11-15 02:48 PST | TMR-5 | SELCORE086.** Governing fusion directive blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6. **PROVED/RESTRICTED** for the specified semantic separator/circuit laboratory and authenticated typed record calculus, independent peer mathematical review OPEN. Executed finite enumeration **COMPUTATIONAL**. P versus NP OPEN.

## 1. Candidate and four falsifiers selected before literature/corpus review

**Candidate:** After TMR-1/041's separator lattice and TMR-4/042's canonical record tariff, a lower bound on a *selected* valid interpolant may be mistakenly substituted for the cost of the *cheapest legal separator*. The model-correct target is the minimum cost over all allowed separator outputs, including full AND/NOT circuits and DAG reuse.

(F1) Two separately SAT and jointly UNSAT sources have many valid interpolants rather than a unique one. (F2) A short legal AND/NOT circuit separates the sources although some other valid interpolants require exponentially many gates. (F3) A genuine free output selection or paid batch operation can overdischarge a proposed potential. (F4) Signed leaf-core normalization is confused with an authentic free PEEL, or a nonempty core with an UNSAT certificate.

**Verdicts:** F1 and F2 give an exact growing counterfamily; F3 has explicit violating tariff rows **only if** the additional free/batch rules are actually admitted; F4 is excluded in the unchanged R_leaf record calculus but retains separate SAT/UNSAT and machine-model qualifications. No fictitious operation is silently promoted to the concrete transition inventory.

## 2. Explicit proper-3CNF family, unique source projections, and nonunique separators

For every n>=2 let X=(x_1,...,x_n). For a literal ell and fresh distinct private variables y,z define four proper ternary clauses

$$
G(\ell;y,z) = \bigwedge_{\alpha,\beta\in\{+,-\}}(\ell\vee y^\alpha\vee z^\beta).
$$

By checking the four values of (y,z), the formula existentially enforces ell: if ell is false, precisely one of the four clauses is false for each private assignment; if true, all four clauses hold. Let

$$
A_n(X,Y)=\bigwedge_{i=1}^{n}G(\neg x_i;y_i,z_i),\qquad
B_n(X,Z)=\bigwedge_{i=1}^{n}G(x_i;u_i,v_i).
$$

All private identifiers are distinct, Y and Z are disjoint, and the literal identifiers have the usual O(log n)-bit encoding. The two source CNFs each contain exactly 4n proper width-3 clauses, with total encoding length Theta(n log n). Both are individually SAT and jointly UNSAT. Their shared projections are exactly U={0^n} and V={1^n}.

By TMR-1/041's *independently re-proved* lattice criterion, a valid Boolean interpolant I must satisfy I(0^n)=1 and I(1^n)=0, and all other 2^n-2 outputs are unconstrained. Consequently there are

$$
2^{\,2^n-2}
$$

valid interpolants. The input wire x_1 is **not** a separator with this polarity, but the one-gate circuit NOT x_1 **is**. A zero-gate circuit can output only an available positive input or constant, none of which has the required endpoint values. Hence in the C-SEP shared AND/NOT DAG model with free input wires and constants and a cost-one NOT gate,

$$
\boxed{\min_{I\text{ separates }U,V} C_{\wedge,\neg}(I)=1.}
$$

The entire source family is explicitly uniformly constructible, but the counting argument below **does not explicitly construct a hard chosen interpolant**.

## 3. Quantified nonconstructive gap: hard chosen interpolants versus one-gate completion

Fix n>=8 and s=floor(2^n/(4n)). In a fan-in-two AND/NOT circuit with at most s gates, allowing unlimited fanout and input/constant wires, each gate can be overdescribed by a type and at most two predecessor indices. Counting all gate counts t<=s and all output wires gives the overcount

$$
N_{\le s}(n)\ \le\ (s+1)(n+s+2)\bigl(2(n+s+2)^2\bigr)^s.
$$

For n>=8, n+s+2<=2^n and s+1<=2^n, whence

$$
\log_2 N_{\le s}(n)\le2n+s(1+2n)
\le2n+\frac{2^n}{4n}(1+2n)
<2^n-2.
$$

For the last strict inequality use 2n<=2^n/16 and (1+2n)/(4n)<=17/32 for n>=8. Since there are 2^(2^n-2) admissible interpolant truth tables, at least one is absent from **every** circuit of <=s gates:

$$
\boxed{\exists I_n\text{ valid}:\ C_{\wedge,\neg}(I_n)>\lfloor2^n/(4n)\rfloor,\quad
\min_{I\text{ valid}}C_{\wedge,\neg}(I)=1.}
$$

This is Shannon-style nonuniform circuit counting, specialized to a fixed **polynomial-size proper-3CNF pair**. It is an existential/mostly-nonexplicit hard *chosen* interpolant, **not** an explicit general-circuit lower bound, and does **not** establish a hard disjoint-NP pair. It strengthens TMR-1/041's original 64-interpolant countercontrol by showing an exponential asymptotic separation between hardest permissible and cheapest permissible Craig separator.

### Actual legal shortcut and tariff consequence

In the qualified C-SEP source-pair/circuit laboratory, starting from the empty DAG, APPEND NOT(x_1) at price one and free-select its output to complete the goal. This authentic execution costs exactly one for every n. For any nonnegative potential satisfying all legal paid and zero-cost rows and zero terminal potential, telescoping forces **Phi(initial)<=1**. A proposed obstruction charging the cost of a selected I_n above 1 must violate a legal tariff row or the terminal-goal condition, regardless of its high intrinsic circuit complexity.

This is **not** a one-transition physical SAT decider: the source pair is preauthenticated, semantic terminal validity is an external goal predicate, and literal source parsing, physical gates, correctness and input interfaces require their own charged machine bridge. In a stronger actual machine system, the compact separator remains a legal cheap conceptual path after appropriate physical costs are included.

## 4. Independent TMR-4/042 leaf-core and exact tariff replay

Independently of TMR-4's implementation, enumerate all 1,024 three-uniform hypergraphs on five vertices. Compute canonical K(U) in TWO independent ways: union of every stable edge subset (exhaustive submask enumeration) and repeated parallel removal of all degree-one-incident edges. Also recursively enumerate every sequential PEEL terminal. These methods agree for every graph, with exactly 430 eligible single-edge paid PEEL transitions and 156 completely peelable sources.

The symbolic confluence proof follows the original restriction: any edge with a degree-one vertex belongs to **no** stable subset. Deleting it leaves the family of stable subsets unchanged; unions of stable subsets remain stable, so every maximal sequence reaches identical K(U). The signed gauge changes witnesses but not edge incidence.

Reconstructed exact seven-column rows (CNF, XOR, SEP, FUS, GAMMA, INT, MACHINE) for **the preauthenticated typed record calculus only**:

| Event | Cost | SEP | FUS | GAMMA | MACHINE |
|---|---:|---:|---:|---:|---:|
| Zero NOP/SWITCH | 0 | 0 | 0 | 0 | 0 |
| PEEL one source edge | 1 | 1 | 2 | -1 | 0 |
| RESTORE one pivot | 1 | 0 | 0 | 1 | 0 |
| HALT | 1 | 0 | 0 | 0 | 1 |

With lambda=(0,0,1/2,3/4,1,0,1), all nonzero rows discharge exactly one paid unit. Independent **integer numerator** verification after scaling lambda by four: weighted rows (0,4,4,4), with costs scaled (0,4,4,4). For completely peelable m-edge inputs, the original primal value 2m+1 is matched by valid dual y=(m,m,1). This reproduces TMR-4/042's theorem independently, and does **not** make core computation free physical work.

If FREE_PEEL is ADDED as an authentic cost-zero operation, its row has scaled discharge 4>0, invalidating that lambda. If a **new** price-one atomic BATCH_PEEL removes two eligible distinct edges and pushes two independent obligations, its additive row is (SEP,FUS,GAMMA)=(2,4,-2), scaled discharge 8>cost4. Both are exact conditional controls, **not** legal operations in unchanged R_leaf. Do not CEGAR-delete either if a richer future model actually contains it.

Stable nonempty cores alone give no UNSAT label, as the SAT K4 and UNSAT K5 examples from TMR-4 show. The authenticated leaf private-variable witness construction (TMR-2/041 and TMR-3/041) remains a real polynomial machine *upper* route on that source subclass.

## 5. Independent finite execution and exact provenance

The **exact evaluated V8 function** has been serialized to experiments/tmr/tmr5_separator_selection086.js; its raw result is results/raw/tmr/2026-11-15_0248_TMR5_SELCORE086_V8_RAW.json; the row schema is results/raw/tmr/2026-11-15_0248_TMR5_SELCORE086_TARIFF.json. The callback has no nondeterminism, external dependencies or random seed.

Native hosted V8 audit returned **3988 assertions, zero failures**. It authenticated 24 proper source clauses, checked 1024 private witness assignments, reconstructed U=1 and V=128, tested a deleted forcing clause, enumerated 64 interpolants, exhausted every shared AND/NOT DAG with up to six paid gates (frontier sizes 1,6,27,113,469,1942,8027), and found **29 of 64** valid interpolants requiring at least seven gates versus the legal one-gate minimum. Checked the counting inequality for n=8..24, the 1,024 leaf hypergraphs, 430 legal PEEL rows, and the exact rational paid/free/added-batch tariff controls.

Those are finite **COMPUTATIONAL** checks. The unbounded counting theorem, semantic projection lemma and core confluence have separate symbolic proofs. Standalone Node runner, full repository preflight, LaTeX compilation and physical multitape simulation were not executed.

## 6. Ranked dependency and requested peer repair

| Dependency | Status | Reason |
|---|---|---|
| TMR-1/041 separator lattice/count | PASS, PROVED/RESTRICTED | Independently reconstructed CNF projections and 64 choices |
| TMR-1/041 NP intersect coNP uniqueness/coverage classification | PASS in logical implication, RESTRICTED | Both complementary NP verifiers needed; arbitrary SAT-UNSAT complementary verifier pair remains OPEN |
| New largest-selected vs cheapest-separator gap | PROVED/RESTRICTED, independent review OPEN | Nonuniform counting theorem and authentic 1-gate path |
| TMR-4/042 leaf core and local LP | PASS, PROVED/RESTRICTED | Independent stable-union, parallel-core and all-order enumeration, exact-rational row replay |
| Positive tariff under added FREE_PEEL or BATCH_PEEL | FAIL on enlarged calculus | Exact violating row; original R_leaf remains sound |
| TMR-2/040 exponential evaluation rank => costly SAT | FAIL | TMR-2/041 and TMR-3/041 private-leaf witness route |
| /341 full logical UNSAT checker | FAIL | Historical SAT false acceptance retained |
| /386 | RESTRICTED | Guarded odd-charge fragment only |
| Fusion-to-full circuit polynomial upper simulation | OPEN | Must preserve fanout, NOT, cheap representations and real charged operations |
| Dynamic superpolynomial all-machine SAT potential | OPEN | Neither this counting result nor leaf records supply it |
| Same-system algorithm-transfer bridge, P versus NP | OPEN | No unconditional uniform SAT lower bound |

**Weakest surviving lemma:** Prove a *lower bound on every admissible separator* of a uniformly constructible disjoint NP pair, in a **precisely defined circuit-faithful fusion model**, after quotienting compact affine/circuit/learning/autarky paths. Bounding a selected interpolant, rectangle rank of a larger relation, or an expensive prescribed record schedule is insufficient. Separately construct an all-transition sound transfer into arbitrary correct fixed SAT-machine executions. TMR-1 should adopt the all-separator quantifier, TMR-2/3 audit private-leaf witness and batched shortcut, and TMR-4 include all authentic cheap paths in cl0/LP.

## 7. Corpus, primary sources and reporting limits

Original reports/code/raw inspected: TMR-1/041 SEPLAT083; TMR-2/041 LEAF081; TMR-3/041 LEAFNAE080/081; TMR-4/042 LEAFCORE082; TMR-5/037 NAEGUARD079; LEAD/0029 Lipschitz; governing 2026-11-14 fusion directive and TMR replacement, all five current handoff heads, AGENTS.md, CODEX.md, repository research skill, both root proof trackers and root main.tex, issue #3 latest comments. Full proof2 and main were recovered from authentic Git blobs (SHA 930c5eeddafce656717f28055a7a9a755f44737c and 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34) after contents responses were blank. No destructive reconstruction.

Primary contextual sources: [1] C. E. Shannon, *The Synthesis of Two-Terminal Switching Circuits*, Bell System Technical Journal 28 (1949), 59-98, https://www.nokia.com/bell-labs/publications-and-media/publications/the-synthesis-of-two-terminal-switching-circuits/ (classic circuit-counting context; the specific inequality here is proved independently). [2] A. Razborov, *On Provably Disjoint NP-Pairs*, BRICS RS-94-36 (1994), https://www.brics.dk/RS/94/36/index.html (proof-theory context, not our selected-interpolant theorem). [3] TMR-1/041, original separator lattice and uniformity audit; [4] TMR-4/042, original leaf-core tariff calibration.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2 SHA 930c5eeddafce656717f28055a7a9a755f44737c, main.tex SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. Canonical main.tex unchanged because no unrestricted load-bearing claim or independently peer-promoted manuscript change is justified. Five existing agents, schedules and enabled states unchanged.

END_OF_VERIFIED_REPORT::TMR5::038::2026-11-15_0248_PST
