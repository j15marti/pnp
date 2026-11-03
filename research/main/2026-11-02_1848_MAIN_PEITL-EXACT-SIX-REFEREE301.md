# PEITL-EXACT-SIX-REFEREE301

**PNP Independent Proof Red Team — November 2, 2026, 18:48 PST**

**Status.** **PROVED/EXACT** for the authentic six-clause instance in the fixed source-independent-VARDEF Rmix341; **COMPUTATIONAL/EXHAUSTIVE FINITE** for the relaxed topology searches and controls; **OPEN** for a growing superpolynomial mixed lower bound, B1, B2, B3, and P versus NP.

## Claim card

- **Claim ID:** PEITL-EXACT-SIX-REFEREE301.
- **Input:** authentic `rsmu_4_6_1.cnf` from Peitl–Szeider's `peitl/smu` corpus, SHA-256 `47b47e154831555f1d66fd39ef90f4b439830a34627e4b4947329616469a2ccf`.
- **Fixed calculus:** zero-cost authenticated original clauses; unit-cost binary RES, exact AND3, and binary XOR; exact paid unary CONVERT; charged source-independent zero-premise variable-gate DEF. Rules and weights are fixed before the input.
- **Cost:** distinct paid inference nodes in one shared contradiction DAG. Best legal proof selection is free; optimizer discovery is excluded from the minimum.
- **Result:**

$$
W_{Rmix341}(\texttt{rsmu\_4\_6\_1})=7.
$$

- **Boundary:** this exact minimum does not cover an unratified source-bearing factor-DEF or a high-arity semantic macro. Adding either changes the calculus and requires a new proof.

The source CNF is

$$
\begin{aligned}
&(x_1\vee x_2)\wedge(x_3\vee x_4)\wedge(\neg x_1\vee\neg x_3)
\wedge(\neg x_2\vee\neg x_4)\\
&\quad\wedge(x_1\vee\neg x_2\vee\neg x_3\vee x_4)
\wedge(\neg x_1\vee x_2\vee x_3\vee\neg x_4).
\end{aligned}
$$

It is UNSAT, every one-clause deletion is SAT, and all 16 individual occurrence-sign flips are SAT.

## Exact topology theorem at six paid nodes

Take the ancestry subgraph of a contradiction. Let $r$ be its original source count; let $b,u,d_0$ be the numbers of binary-, unary-, and zero-premise paid nodes; let $q=b+u+d_0$; and let $\beta$ be the undirected cycle rank. Its premise-edge count is $E=2b+u$. Connectedness gives

$$
\beta=E-(r+q-1),
$$

and therefore the exact identity

$$
q-(r-1)=\beta+u+2d_0.
$$

Clause minimality forces $r=6$. For a proposed $q=6$ refutation,

$$
1=\beta+u+2d_0.
$$

Thus $d_0=0$: no independent charged DEF can occur. Exactly two topology classes remain:

1. $u=1,\beta=0$: five binary nodes form a source-once tree and one exact unary conversion changes representation.
2. $u=0,\beta=1$: all six nodes are binary and the ancestry graph is unicyclic.

This independently reproduces and applies the peer SOURCE-EXCESS-EULER349 identity. It is a graph identity, not a machine-work lower bound.

## Exhaustion of both six-node classes

### Unary/tree class

Grant exact clause and affine aliases for free and allow AND3 whenever the output truth table has essential support at most three. This is stronger than paying for the one CONVERT. The five-binary-node subset-partition DP enumerates every source-once tree under this relaxation. It performs 833 pair tests, generates 580 outputs, retains 82 full-source terminal functions, and does not contain false. Hence no legal unary/tree six-node proof exists.

### Unicyclic class

In a connected unicyclic ancestry DAG whose nodes all reach one contradiction root, the unique undirected cycle has one divergence and one reconvergence. Otherwise two cycle reconvergences would have to merge on paths to the root and create a second undirected cycle. Suppressing the degree-two portions yields four disjoint source regions:

- $S$: the shared source-once tree above the divergence;
- $L$ and $R$: exclusive trees on the two cycle branches;
- $T$: the tail tree merged after reconvergence.

The exhaustive search enumerates every partition $S\dot\cup L\dot\cup R\dot\cup T=[6]$ with $S\ne\varnothing$, every relaxed function of the shared tree, every saturated branch tree, every legal relaxed reconvergence, and every tail tree. It again grants free exact clause/affine aliases and the stronger output-support AND3 rule. After 7,212 reconvergence pair tests, 4,780 generated cycle outputs, and 1,650 cached extension states, no final false function occurs.

Because this search is a semantic relaxation of every RES/AND3/XOR-only unicyclic proof, absence in the relaxation excludes the exact fixed calculus. Together the two topology searches prove

$$
W_{Rmix341}(F)\ge 7.
$$

## Seven-node upper certificate

The following ordinary Resolution derivation is legal in Rmix341. Lines 1–6 are the source clauses.

| line | derived clause | parents and pivot |
|---:|---|---|
| 7 | $x_1\vee\neg x_3\vee x_4$ | 1, 5 on $x_2$ |
| 8 | $\neg x_1\vee x_2\vee\neg x_4$ | 3, 6 on $\neg x_3$ |
| 9 | $x_2\vee\neg x_4$ | 1, 8 on $x_1$ |
| 10 | $\neg x_3\vee x_4$ | 3, 7 on $\neg x_1$ |
| 11 | $\neg x_4$ | 4, 9 on $\neg x_2$ |
| 12 | $x_4$ | 2, 10 on $x_3$ |
| 13 | $\bot$ | 11, 12 on $\neg x_4$ |

The producer and independent Node verifier replay every pivot and reject corrupted variants. Thus

$$
W_{Rmix341}(F)\le 7,
$$

which meets the lower certificate.

## Four falsifiers and dispositions

1. **A paid conversion creates a six-node shortcut. — FALSIFIED.** Free exact aliases strengthen that topology, yet the complete five-binary-node tree bank misses false.
2. **One shared subderivation creates a six-node shortcut. — FALSIFIED.** The complete relaxed unicyclic decomposition misses false after 7,212 reconvergence tests.
3. **A source-independent auxiliary definition can appear in six nodes. — FALSIFIED structurally.** The exact excess identity assigns a zero-premise DEF two units of excess, but only one is available.
4. **This finite optimum proves worst-case hardness or B3. — FALSIFIED AS AN INFERENCE.** One constant-size optimum gives no asymptotic lower bound and no SAT-in-P-to-proof bridge.

The result is an exact finite mixed minimum, not a universal machine lower bound. An expensive optimizer does not invalidate it because free best-path selection is the declared lower-bound relaxation.

## Controls and independent verification

- authentic source: zero models;
- six deletion controls: model counts $3,3,3,3,1,1$;
- 16 occurrence-sign controls: eight have three models and eight have one model;
- eight malformed DIMACS controls rejected independently;
- four corrupted Resolution certificates rejected by the producer and an independently altered proof rejected by the Node verifier;
- odd-charge $K_4$ Tseitin: zero models; even-charge control: eight models;
- independent no-import Node verifier: 49 checks, including an independently implemented 7,212-test topology search.

Raw SHA-256: `6e271e7df7e3ff8a4373360f71cf949ad4ea944a0e6b299e67aa7d2a6e62799c`.

## B1/B2/B3 classification

- **B1 remains OPEN.** No arbitrary total SAT decider is translated pointwise into Rmix341 proofs.
- **B2 remains OPEN.** No domination of $\overline W_R(N)$ by any decider's all-input worst-case runtime is proved.
- **B3 remains OPEN.** SAT in P is not shown to make this same fixed Rmix341 polynomially bounded.

Correct classification: this is a **certified finite optimum**, not a family failure, transfer failure, or asymptotic theorem. The hard instance may still be useful as the smallest target whose mixed minimum strictly exceeds the universal $m-1$ source floor.

## Work and all-phase space ledger

The logical minimum is seven paid nodes. Separately, the Python certifier charges parsing, truth-table generation, alias generation, all tree and cycle partitions, extension caching, label/deletion/sign controls, malformed and parity tests, Resolution replay, corruptions, and JSON output. It used 0.204 seconds and peak host RSS 11,392 KiB. The Node verifier used peak host RSS 49,632 KiB. These are implementation upper measurements, not lower bounds.

The certifier materializes truth-table banks and a 1,650-entry cache. It makes no sublinear-space claim. Any later machine transfer must retain the all-phase envelope

$$
s'\le\max\{\rho,\eta,\lambda,\lambda s\},
$$

with $\rho$ covering parsing, order discovery, conversion, generation, checking, and output.

## Literature and project audit

Searches included “Peitl Szeider shortest resolution proof tool,” “proof DAG cycle rank source ancestry,” “Cook Reckhow proof length,” the project terms `Rmix341`, `SOURCE-EXCESS-EULER349`, `DEF-SUPPORT-COVERAGE346`, `PEITL-MIXED-FLOOR-REFEREE300`, and GitHub searches in `peitl/short-proof`, `j15marti/pnp`, `openai/openai-cookbook`, and `openai/openai-python`.

- T. Peitl and S. Szeider, *Finding the Hardest Formulas for Resolution*, JAIR 72 (2021), 69–97, <https://doi.org/10.1613/JAIR.1.12589>. Their metric is Resolution length, not the mixed minimum proved here.
- Author implementation: <https://github.com/peitl/short-proof>. A fresh exact query reproduced the 13-line proof, i.e. six sources plus seven derived nodes.
- S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36–50, <https://doi.org/10.2307/2273702>. This supplies the standard proof-system framework, not B3 for Rmix341.

The project audit incorporated SOURCE-EXCESS-EULER349, PROOF-PAYLOAD-ARITY-COLLAPSE347, GUARD-SUM-NONHORN349, and REFEREE300. The separate ENUM_ARITY diagnostic is not added to Rmix341. No pertinent OpenAI proof-complexity implementation was found; one cookbook text match was generic formal-logic material. No novelty is claimed for the authors' Resolution optimum or the elementary Euler identity. The new checked increment is their combination with complete relaxed unicyclic exhaustion for this fixed mixed calculus.

The prescribed pnp-research preflight executable is absent from this partial local workspace. Authenticated GitHub reads, role-owned paths, independent execution, exact hashes, and complete readback are used as the documented fallback.

## Exact next gap

Apply the same excess-one topology exhaustion to authentic `rsmu_5_7_1.cnf`. REFEREE300 gives $7\le W\le9$; excluding cost seven would improve the lower bound to eight, after which cost-eight DAGs or the nine-node Resolution witness must be resolved. In parallel, a growing nonaffine family needs an invariant surviving every fixed mixed rule, and B3 must be proved independently for the same Rmix341. **P versus NP remains OPEN.**
