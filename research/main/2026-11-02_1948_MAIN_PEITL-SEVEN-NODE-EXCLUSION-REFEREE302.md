# PEITL-SEVEN-NODE-EXCLUSION-REFEREE302

**PNP Independent Proof Red Team — November 2, 2026, 19:48 PST**

**Status.** **PROVED/EXACT** for the finite interval in the fixed source-independent-VARDEF (R_{mathrm{mix341}}); **COMPUTATIONAL/EXHAUSTIVE FINITE** for two independently implemented relaxed topology searches and controls; **OPEN** for cost eight versus nine, a growing superpolynomial mixed lower bound, B1, B2, B3, and P versus NP.

## Claim card

- **Claim ID:** PEITL-SEVEN-NODE-EXCLUSION-REFEREE302.
- **Input:** authentic `rsmu_5_7_1.cnf` from the Peitl–Szeider corpus, SHA-256 `6ca65edf800525363d4153b266cd4f4d207bd3a8977064c74996bc363ee8f6d6`.
- **Fixed calculus:** zero-cost authenticated original clauses; unit-cost binary RES, exact AND3, and binary GF(2) XOR; exact paid unary CONVERT; charged source-independent zero-premise variable-gate DEF. Rules and weights are fixed independently of the input.
- **Cost:** the number of distinct paid inference nodes in one shared contradiction DAG. Free best-proof selection is granted; optimizer discovery is not charged.
- **Exact finite conclusion:**

$$
8\le W_{R_{\mathrm{mix341}}}(\texttt{rsmu\_5\_7\_1})\le9.
$$

- **Quantifier boundary:** this is one finite instance in one fixed proof calculus. It proves neither a superpolynomial lower bound on \(\overline W_R\) nor B1, B2, or B3.

The source is

$$
\begin{aligned}
F={}&(\neg x_1\vee x_2)\wedge(\neg x_2\vee x_3)
\wedge(\neg x_3\vee x_4)\wedge(\neg x_4\vee x_5)\\
&\wedge(x_1\vee\neg x_5)
\wedge(x_1\vee x_2\vee x_3\vee x_4\vee x_5)\\
&\wedge(\neg x_1\vee\neg x_2\vee\neg x_3\vee\neg x_4\vee\neg x_5).
\end{aligned}
$$

It is UNSAT, each one-clause deletion is SAT with model counts \(4,4,4,4,4,1,1\), and every one of its 20 individual occurrence-sign flips is SAT.

## Exact excess-one reduction

Take the ancestry subgraph of a contradiction. Let \(r\) be its number of distinct original sources, \(b,u,d_0\) the numbers of binary-, unary-, and zero-premise paid nodes, \(q=b+u+d_0\), and \(\beta\) the undirected cycle rank. Since the number of premise edges is \(E=2b+u\), connectedness gives

$$
\beta=E-(r+q-1),
$$

and hence the exact identity

$$
q-(r-1)=\beta+u+2d_0.
$$

Clause minimality forces \(r=7\). A hypothetical seven-node refutation must therefore satisfy

$$
1=\beta+u+2d_0.
$$

No zero-premise DEF can appear. Exactly two cases remain:

1. \((\beta,u,d_0)=(0,1,0)\): a source-once binary tree plus one paid conversion;
2. \((\beta,u,d_0)=(1,0,0)\): a source-once unicyclic binary DAG.

This graph identity is a logical-topology theorem, not a machine-work lower bound.

## Exhaustive relaxed exclusion

The search deliberately strengthens the legal calculus by granting exact clause and affine aliases for free and by permitting AND3 whenever the output truth table has essential support at most three. Therefore absence in the relaxed search excludes every legal exact proof in the corresponding topology class.

### Unary/tree class

Free exact aliases subsume the single paid representation conversion. The subset-partition tree dynamic program exhausts every source-once six-binary-node tree. It executes 2,231 pair tests, generates 935 outputs, retains 50 full-source terminal truth tables, and does not retain false.

### Unicyclic class

Every connected unicyclic ancestry DAG whose nodes reach one root has one divergence and one reconvergence. Suppressing degree-two paths gives four disjoint source regions: a shared tree \(S\), exclusive branches \(L,R\), and a tail \(T\). The search enumerates every partition

$$
S\mathbin{\dot\cup}L\mathbin{\dot\cup}R\mathbin{\dot\cup}T=[7],
\qquad S\ne\varnothing,
$$

every relaxed shared-tree value, both saturated branch trees, every relaxed reconvergence, and every tail tree. It executes 16,907 reconvergence tests, generates 6,285 cycle outputs, and uses 3,621 cached extension states. No false terminal occurs.

The producer and a separately authored no-project-import verifier reproduce the complete counts. Consequently no seven-node proof exists, so

$$
W_{R_{\mathrm{mix341}}}(F)\ge8.
$$

## Nine-node upper certificate

The following ordinary Resolution proof is legal in the same mixed calculus. Lines 1–7 are the source clauses.

| line | derived clause | parents and pivot |
|---:|---|---|
| 8 | \(x_1\vee x_2\vee x_3\vee x_5\) | 4, 6 on \(\neg x_4\) |
| 9 | \(x_1\vee x_2\vee x_3\) | 5, 8 on \(\neg x_5\) |
| 10 | \(\neg x_1\vee\neg x_3\vee\neg x_4\vee\neg x_5\) | 1, 7 on \(x_2\) |
| 11 | \(x_2\vee x_3\) | 1, 9 on \(\neg x_1\) |
| 12 | \(\neg x_3\vee\neg x_4\vee\neg x_5\) | 5, 10 on \(x_1\) |
| 13 | \(x_3\) | 2, 11 on \(\neg x_2\) |
| 14 | \(\neg x_3\vee\neg x_4\) | 4, 12 on \(x_5\) |
| 15 | \(\neg x_3\) | 3, 14 on \(x_4\) |
| 16 | \(\bot\) | 13, 15 on \(x_3\) |

Every pivot is replayed and four corrupted variants are rejected. Therefore

$$
W_{R_{\mathrm{mix341}}}(F)\le9.
$$

## Four falsifiers

1. **A paid conversion creates a seven-node shortcut — FALSIFIED.** The tree search grants all exact clause/affine conversions for free and still misses false.
2. **One shared subderivation creates a seven-node shortcut — FALSIFIED.** The complete relaxed unicyclic search misses false after 16,907 reconvergence tests.
3. **A source-independent auxiliary definition appears in seven nodes — FALSIFIED structurally.** A zero-premise node consumes two excess units, while only one is available.
4. **This lower increment establishes family hardness or a bridge — FALSIFIED AS AN INFERENCE.** It is finite and calculus-specific. The instance has deficiency two, and the concurrent MUS-deficiency theorem supplies only a compatible polynomial upper framework. No arbitrary decider is simulated.

## Controls and independent verification

- authentic source: zero models;
- seven deletion controls: model counts \(4,4,4,4,4,1,1\);
- 20 occurrence-sign controls: ten have four models and ten have one model;
- eight malformed DIMACS controls rejected;
- four corrupted/truncated Resolution certificates rejected by the producer, with an independently truncated certificate rejected by the verifier;
- odd-charge \(K_4\) Tseitin: zero models; even-charge control: eight models;
- independent verifier: 55 assertion groups and an independently implemented 16,907-test relaxed topology search.

Raw SHA-256: `96c39f17c3f70b0e8ab09954be7b2bfe5abfa74773a8cb153e5ad1044ed3ff86`.

## B1/B2/B3 referee classification

- **B1 — OPEN.** No total correct SAT decider is translated pointwise into a polynomial-cost \(R_{\mathrm{mix341}}\) refutation.
- **B2 — OPEN.** This finite proof minimum says nothing about any decider's all-input worst-case runtime.
- **B3 — OPEN.** SAT in P is not shown to imply polynomial \(\overline W_R\) for this same preselected calculus.

This is a **finite lower-bound increment**, not a family failure, pointwise-transfer failure, worst-case-transfer failure, or conditional-bridge proof. P versus NP remains OPEN.

## Logical cost versus scheduled work and space

The logical statement counts only distinct paid inference nodes and grants free optimal-path choice. Separately, the Python producer charges parsing, 32-bit truth-table construction, alias generation, all tree/cycle partitions, extension caching, label/deletion/sign controls, malformed/parity tests, Resolution replay, corruption checks, and JSON output. The published replay used 1.520 seconds and 12,032 KiB peak host RSS. The independent verifier used 11,904 KiB peak RSS.

These measurements are implementation upper bounds, not lower bounds. The certifier materializes tree banks and 3,621 cached extension states. No sublinear-space claim is made. Any future machine transfer must charge source/index access, representation conversion, verification, output, storage/recomputation, and all temporary allocations under

$$
s'\le\max\{\rho,\eta,\lambda,\lambda s\},
$$

with \(\rho\) covering every local phase. The peer forced-row result correctly warns that inference-node cost need not dominate uncharged certificate payload; the present proof makes no such domination claim. The peer pivot-only result likewise shows that explicit derived clauses need not be present in a compact Resolution certificate.

## Literature, corpus, and duplication audit

Searches covered “Peitl Szeider resolution shortest proof,” “extended Resolution lower bound open,” “Cook Reckhow optimal proof system,” `Rmix341`, `SOURCE-EXCESS-EULER349`, the Peitl finite corpus, `j15marti/pnp`, `openai/openai-cookbook`, and `openai/openai-python`.

- T. Peitl and S. Szeider, *Finding the Hardest Formulas for Resolution*, JAIR 72 (2021), 69–97, <https://doi.org/10.1613/JAIR.1.12589>. Their exact metric is Resolution length. The author tool <https://github.com/peitl/short-proof> reproduces the 16-line proof above; it does not search the mixed calculus.
- S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36–50, <https://doi.org/10.2307/2273702>. It supplies the proof-system framework, not B3 for this fixed \(R\).
- No relevant SAT proof checker or mixed-calculus implementation was found in the searched OpenAI repositories; no novelty inference is drawn from that negative search.

**Corpus reviewed.** The 12:04 five-role handoff; issue #3 through the 19:36 predecessor; root `main.tex`; AGENTS/CODEX and the full pnp-research skill plus red-team/research protocol; REFEREE299–301; LSPV-1 SOURCE-EXCESS-EULER349 and MUS-DEFICIENCY-PROOF-FILTER351; LSPV-2 FORCED-ROW-PAYLOAD-SENSITIVITY348; LSPV-3 GUARD-SUM-EXACT350; and LSPV-4 PIVOT-ONLY-REPLAY-COST348.

**Duplication/contradiction audit.** REFEREE300 established only \(7\le W\le9\) for this input; REFEREE301 explicitly named the seven-node exclusion as the next gap. This run fills exactly that gap and does not duplicate the authors' nine-node Resolution optimum. The LSPV-1 deficiency filter is consistent: deficiency two makes the instance unsuitable as evidence for asymptotic superpolynomial hardness. The LSPV-2 and LSPV-4 payload results concern verification representations, not the unit logical minimum.

**What changed relative to root MAIN.** Only the finite interval for `rsmu_5_7_1` improved from \([7,9]\) to \([8,9]\). No bridge, asymptotic, system, task, or scheduler status changed.

**Adopted/rejected/retired components.** Adopted the fixed calculus, exact excess identity, free-alias relaxation, authentic corpus source, and Resolution witness. Rejected uncharged ENUM_ARITY and source-bearing semantic macro rules because they are not part of the fixed calculus. Retained DEF for the calculus generally, but proved it cannot occur at cost seven. No prior verified mathematics was retired.

## Exact next gap

Resolve cost eight. The excess identity gives

$$
2=\beta+u+2d_0.
$$

After free aliases absorb unary-only cases, two genuinely new classes remain: binary bicyclic ancestry DAGs \((\beta,d_0)=(2,0)\), and a source-once tree with one paid source-independent zero-premise definition \((\beta,d_0)=(0,1)\). A complete relaxation covering both would decide whether the mixed optimum is eight or nine. Independently, any asymptotic hard-family program must satisfy the new superlogarithmic-deficiency filter and survive every fixed mixed rule, while B3 remains a separate obligation. **P versus NP remains OPEN.**
