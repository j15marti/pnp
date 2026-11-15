# TMR-2/052: One unique selector collapses exponential all-balanced-cut slice ranks

**2026-11-15 13:14 PST | PNP Information Necessity | Track A | `tmr2_unique_selector_rank052.v1`.**

**Status:** **PROVED/EXACT for the scoped symbolic algebra and strict 3-CNF construction**, independent mathematical review OPEN. Benchmarks COMPUTATIONAL. The proposed unrestricted rank-to-SAT-work implication is **FALSIFIED** by a polynomial-work shortcut. P versus NP OPEN.

## Candidate, objects and precommitted falsifiers

**Candidate attacked:** Requiring large tensor-flattening ranks at every balanced cut, in both values of one uniquely determined interface bit, might make the corresponding fixed-formula obstruction survive existential contraction. **Object:** the two partial existential projections of a *single fixed formula's satisfying-assignment indicator*, with only the original variables as row and column axes. It is NOT the SAT decision function on encoded formulas or a physical machine execution trace.

Falsifiers: (1) another balanced cut or characteristic has low slice rank; (2) a functional one-bit selector contracts both individually high-rank matrices to rank one; (3) auxiliary multiplicity, padding or inaccurate 3-CNF size invalidates the projection; (4) a legal compact gate circuit, Horn/2-SAT recognition, cache or alternative contraction yields polynomial work. Falsifiers (2) and (4) succeed.

## Exact theorem (new increment to TMR-5/046)

Let G=(V,E) be any simple graph, n=|V|, m=|E|>=2. Put

\[
I_G(x)=\prod_{\{u,v\}\in E}(1-x_u x_v),\qquad
z=1-I_G(x)=\bigvee_{\{u,v\}\in E}(x_u\land x_v).
\]

For a cut V=A disjoint-union B let D_{A,B}(a,b)=I_G(a,b), J the conformable all-ones matrix, and H_z the matrix obtained by fixing the real selector to z and *existentially projecting only the other functional gate auxiliaries*.

**Theorem 052-A (all fields).** A strict proper duplicate-free width-exactly-three CNF Psi_G exists with

\[
V_{\rm CNF}=n+2m+2,\quad C_{\rm CNF}=6m+4,\quad L_{\rm occ}=18m+12,
\]

and for **every** assignment to original x there is **exactly one** satisfying extension to z and all other auxiliary variables. Over **every** field K and for **every** cut of original variables,

\[
H_0=D_{A,B},\quad H_1=J-D_{A,B},\quad
{\rm rank}_K H_1\ge {\rm rank}_K H_0-1,
\quad H_0+H_1=J,\quad {\rm rank}_K J=1.
\]

This is also an **integer exact-count identity**, not merely Boolean OR: the sum over all full auxiliary extensions equals one for every x. Thus existentially forgetting the **one output selector z**, after uniquely eliminating the other gates, collapses both slices to a rank-one all-ones relation.

**Proof.** For each edge e={u,v} create a functional AND gate t_e=x_u AND x_v. For j=2,...,m create an OR gate p_j=p_{j-1} OR t_j, taking p_1=t_1 and p_m=z. Standard three-clause functional AND and three-clause functional OR representations each determine their output uniquely from their inputs. Replace each binary gate clause (a OR b) by (a OR b OR q). Introduce three pins (q,a,b) with the seven proper ternary clauses excluding every truth assignment except (0,0,0). These clauses force q=a=b=0, so every padded binary clause retains its meaning. Counting m AND gates, m-1 OR gates and seven pin clauses gives 6m+4 proper ternary clauses, all with distinct variables. Exactly m+(m-1)+3=2m+2 auxiliaries occur. Functional induction gives unique extension and the stated selector semantics. The ranks follow from H_1=J-H_0 and rank(J)=1 by rank(A-B)>=rank(A)-rank(B). Finally H_0+H_1=J entrywise, even in characteristic two. QED.

**Exact gate ledger:** AND clauses (-x_u,-x_v,t_e), (x_u,-t_e,q), (x_v,-t_e,q). OR clauses (-p_{j-1},p_j,q), (-t_j,p_j,q), (p_{j-1},t_j,-p_j). Seven pinned three-variable clauses each exclude one nonzero pin assignment. The compact shared circuit has **2m-1 binary gates** and **4m-2 gate-input wires**, counted once, not one copy per cut. Signed-index literal records require (18m+12)(1+ceil(log2(V_CNF+1))) bits in the declared fixed-width grammar plus its actual header and delimiters. Total encoded length N=O(m log(n+m)+log n), when n=O(m), and O((n+m)log(n+m)) without that condition. Clause parsing, index arithmetic and source validation are charged.

**All-balanced amplification:** TMR-5/046 already proved that for a graph with max degree d and edge-expansion h>0, every original-variable partition whose two sides have >=n/3 vertices has a DISJ-matching minor of order r>=hn/[6d(d+1)], hence rank(D)>=2^r over every field. This run **does not reclaim** that earlier theorem. Applying Theorem 052-A yields, for EVERY such partition,

\[
\boxed{
{\rm rank}_K H_0\ge 2^{hn/[6d(d+1)]},\quad
{\rm rank}_K H_1\ge 2^{hn/[6d(d+1)]}-1,\quad
{\rm rank}_K(H_0+H_1)=1.}
\]

Explicit constant-degree expander families [1] give exponential ranks **in both fixed-selector slices and every balanced cut**, even though their simultaneous unique-extension existential projection is rank one. In the fully explicit hypercube Q_d family, n=2^d, max degree d and the edge-isoperimetric inequality instead gives at least 2^{Omega(n/log^2 n)} on both slices. The selector contraction is algebraic and may be computationally inexpensive; **it is not a single free physical Turing-machine transition**.

## Cost-soundness and same-realization ledger

The full strict 3-CNF is SAT for every graph G: choose original x=0^n, all AND/OR gate outputs and pins 0. A fixed uniform total correct SAT decider can recognize and validate the canonical gate/pin grammar, then issue YES with this verified witness on matching inputs. It runs a sound exact exhaustive fallback for all other inputs. On this family its same-execution runtime and retained space are at most polynomial in the *actual* input length N. This counteralgorithm uses no exponential matrix construction, no uncharged source recognition, no semantic SAT oracle and no nonuniform family-specific advice. It may rerun or cache the gate validations and charges their actual work.

If any cost-sound physical-step potential assigns nonnegative weight lambda to the initial sum of the two slice ranks minus two, requires nonpositive terminal potential, and each paid machine step discharges at most its cost, telescoping along this legal polynomial accepting execution forces

\[
\lambda({\rm rank}(H_0)+{\rm rank}(H_1)-2)\le T(N).
\]

For any constant-degree expander subfamily, the left rank sum is >=2^{r+1}-3. Therefore a **uniform fixed positive** lambda is **FALSIFIED**; the necessary scale is lambda<=T(N)/(2^{r+1}-3). This does not itself prove any candidate potential sound, and the full contraction may take polynomially many physical steps. The all-machine lower-bound bridge remains OPEN.

## Exact finite benchmark

Reproducer: `experiments/tmr/tmr2_unique_selector_rank052.py`, executed Python 3.13.5, revision `tmr2_unique_selector_rank052.v1`, source SHA-256 `950db74faf3e85c9ac338e3c45cf8a4037d09f2c67b3060a29ff4f7890338e47`.
Raw JSON: `results/raw/tmr/2026-11-15_1314_TMR2_SELECTOR_RANK052_PY_RAW.json`, SHA-256 `0597a5f0962b4fdd0c127efbea1bff1269e0d5ff76a2a3b5fdcbfd72d2fb1017`.
Deterministic Q4 seed: **20261115**. No other randomness.

The code independently generates actual strict-3CNF clauses, checks AND/OR/pin truth tables, evaluates every original assignment and its unique gate extension, rejects every wrong selector flip, enumerates all balanced cuts up to transpose for three graphs, constructs the full Boolean slice matrices, and computes **exact** GF(2) and F_65521 ranks. Q4 uses a 12-cut seeded balanced sample and exact GF(2) elimination. The proof is symbolic and does not rely on those finite cases.

| Graph | Orig. vertices / edges | Strict3 vars / clauses | Balanced cuts | Min rank z=0 GF2 | Min rank z=1 GF2 | Rank after z sum |
|---|---:|---:|---:|---:|---:|---:|
| Cycle C6 | 6 / 6 | 20 / 40 | 25 exhaustive | 3 | 4 | 1 |
| Cube Q3 | 8 / 12 | 34 / 76 | 91 exhaustive | 4 | 5 | 1 |
| Petersen | 10 / 15 | 42 / 94 | 336 exhaustive | 6 | 7 | 1 |
| Cube Q4 | 16 / 32 | 82 / 196 | 12 seeded | 21 | 22 | 1 |

Total **464 cuts, 205,760 assertions, zero failures**, including 452 two-field exhaustively checked cuts. For Q4 the F_65521 rank one after contraction follows from the symbolic theorem, not a claimed executed modular test. Benchmark matrix materialization, modular inverses, arithmetic, source accesses and memory are paid in that code; none is a mandatory action for the polynomial witness recognizer.

## Mandatory four-gate audit

| Gate | Verdict | Reason |
|---|---|---|
| **DISJ sanity** | **PASS restricted, FAIL unrestricted transfer** | DISJ_k has rank 2^k but linear-size depth-two circuit. Its two z slices can have high ranks yet sum to J; no circuit/SAT hardness inferred. |
| **Relativization / algebrization / Natural Proofs** | **PASS restricted; OPEN transfer** | The finite linear-algebra identities are relativizing. No nonrelativizing P-vs-NP step exists; algebrization/Natural Proofs remain open for future claimed general circuit invariants. |
| **Simultaneous DTISP** | **NOT APPLICABLE to scoped theorem; OPEN for FLMV** | There is a same-realization polynomial-work *upper* bound on the easy family, but no one forbidden-box machine meeting BOTH strict time and space constraints. Charge reductions, source access, arithmetic, switching, caching and retained state. |
| **Configuration counting** | **PASS as scope guard** | For a fixed deterministic total read-only-input machine, T<=2^{O(s+log N)}, or 2^{O(s)} if s>=log N, is an upper bound, never a work lower bound; no probabilistic/quantum runtime claim. |

**Controls:** Source graph indicator is negative Horn 2-CNF, hence Krom/SCC and all-zero witness are legal shortcuts. Equality, affine/Gaussian, certified autarkies, product factoring, bounded-treewidth DP, compact circuits and shared recomputation are never forbidden. Despite possible expander treewidth, SAT is trivially YES. All gate auxiliaries have **unique** extension for each original x, including the three pinned variables. Independent padding increases assignment enumeration but cannot change the rank-one existential projection. A unique **global** satisfying assignment would itself give rank one for the full indicator; our uniquely determined selector per x is a distinct property. Valiant-Vazirani XOR isolation is randomized and promise-sensitive, not a free rank-preserving deterministic reduction. Invertible local bases preserve each fixed-slice cut rank; eliminating one shared functional selector is a different operation.

## Corpus, priority and next lemma

Read FIRST the current 2026-11-15 SAT compression/circuit directive SHA `7b8804dc7587abc5134055b5b0d16a143055ca5a`. Reviewed root proof1 SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`, proof2 SHA `930c5eeddafce656717f28055a7a9a755f44737c`, main.tex SHA `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34`, AGENTS.md, CODEX.md, repository research skill, latest five TMR handoffs, issue #3, historical selector work, original TMR-5/046 proof and Python, TMR-4/051-052 and TMR-2/050-051 originals. Connector returned **empty bodies** for oversized proof2/main.tex, so their full contents were not recovered. No main or tracker edit is authorized. **TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.**

**Duplication:** TMR-5/046 already proved all-balanced-cut graph rank, and TMR-4/051-052 already bounded fixed-order BDD cuts and variable-switch products. TMR-2/050-051 established prescribed-order and field-dependent traps. The **new** theorem is *two simultaneously high-rank selector slices across every balanced cut, one functional unique-extension bit, and rank-one projection*, with an exact 3CNF ledger and independent two-field benchmark. It is not a P-versus-NP proof or a claim of first discovery in the external literature. Historical /341 remains FAIL as full logical UNSAT authority, /386 RESTRICTED. All five identities, titles, ownership and schedules unchanged.

**Primary sources:** [1] Reingold, Vadhan, Wigderson (2002), *Entropy Waves, the Zig-Zag Graph Product, and New Constant-Degree Expanders*, https://annals.math.princeton.edu/2002/155-1/p04 . [2] Razgon (2021), *Classification of OBDD Size for Monotone 2-CNFs*, https://arxiv.org/abs/2103.09115 . [3] Bryant (1986), *Graph-Based Algorithms for Boolean Function Manipulation*, https://doi.org/10.1109/TC.1986.1676819 . [4] Baker, Gill, Solovay (1975), https://doi.org/10.1137/0204037 . [5] Valiant, Vazirani (1986), https://ics.uci.edu/~vazirani/ValVaz.pdf .

**One next lemma for TMR-3/4:** Require an execution-dependent reduced-product obstruction defined *after* a certified functional-selector/compact-gate quotient, with a local sound tariff for every genuine physical transition, including adaptive recomputation, sharing, and all legal cheap alternatives. First falsify it on DISJ, Horn expander and this unique-selector family; only then consider restricted circuit/branching-program transfer. **P versus NP remains OPEN.**

END_OF_REPORT::TMR-2::052
