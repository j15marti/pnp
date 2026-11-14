# TMR-2 / 005: clause-minimal global inconsistency can still be a cheap affine decision

**Date:** 2026-11-13 16:23 PST (America/Los_Angeles). **Role:** TMR-2 Information Necessity, current five-agent replacement. **Scientific status:** CANDIDATE symbolic theorem pending TMR-5 independent review; executed finite checks COMPUTATIONAL. The unrestricted deterministic 3-SAT superpolynomial lower bound and P versus NP remain OPEN.

## Exact target and contribution

A proposed information-necessity argument might strengthen "there are many possible satisfying assignments" into "every original clause is essential to the global UNSAT determination." This report gives a stronger countercontrol to that second inference. The *same* large-primal-treewidth affine Tseitin 3-CNF family from TMR-2/004 is, in the odd-charge case, **clause-minimally unsatisfiable**:

$$
F_{m,b}\in\mathrm{UNSAT}, \qquad
\forall C\in F_{m,b}:\ F_{m,b}\setminus\{C\}\in\mathrm{SAT}.
$$

Yet one fixed correct total deterministic all-input decider has a fully charged polynomial-time fast path on the whole authenticated affine family. Thus the necessity of **every individual clause** for logical inconsistency does not entail sequentially solving an expensive subproblem per clause, exponential retained state, or an unrestricted 3-SAT runtime lower bound. The family is not alleged to be new to proof complexity; the incremental statement is the direct proper-width-3 minimality proof for our previously published canonical chained encoding.

## Source, quantifiers and model

Use the original strict proper 3-CNF binary encoding, header \`1^N 0 1^M 0\` plus three signed variable IDs per clause with $w=\max(1,\lceil\log_2 N\rceil)$ bits per ID and one sign bit. The exact source length is

$$
L=N+M+2+3M(1+w).
$$

One fixed finite deterministic total multitape program for all lengths is the computational object. Its read-only input may be revisited. Program, control, source accesses, parity rows, buffers, counters, indexing, temporary storage, Gaussian elimination, parsing, output and all fallback work are charged. Malformed input is rejected; all valid SAT and UNSAT labels are correct. The construction does not replace this fixed-machine requirement with a separate per-length table.

For every even integer $m\ge6$ take $G=K_m$, edge bits $x_{uv}$ for $u<v$, and any vertex charge $b\in\{0,1\}^m$ with $\bigoplus_v b_v=1$. Each vertex $v$ has degree $d=m-1$ with ordered incident edge bits $e_1,\dots,e_d$ and $d-3$ private auxiliary bits $y_1,\dots,y_{d-3}$. Impose a chain of $d-2$ three-variable XOR equations:

$$
e_1\oplus e_2\oplus y_1=0,
$$
$$
y_{j-1}\oplus e_{j+1}\oplus y_j=0
\quad (2\le j\le d-3),
$$
$$
y_{d-3}\oplus e_{d-1}\oplus e_d=b_v.
$$

Each row becomes four proper 3-clauses forbidding exactly its four parity-violating tuples. The actual formula contains

$$
N=\frac{3m(m-3)}2,\qquad M=4m(m-3)
$$

distinct variables and clauses respectively, and $L=\Theta(m^2\log m)$ encoded bits. See original TMR-2/004 for the explicit $K_m$ primal minor and even-charge solution-count proof. No arbitrary-source semantic promise is assumed by the fallback solver.

## New lemma TMR2-MU5: every original 3-clause is essential

**CANDIDATE pending independent review.** For every even $m\ge6$, every odd-charge $b$, and every one of the $M$ original strict width-three clauses $C$ of the explicit $F_{m,b}$, $F_{m,b}\setminus\{C\}$ is SAT.

**Proof.** The original source is UNSAT since XOR of all vertex equations gives $0=\bigoplus_v b_v=1$, every edge occurring at exactly two endpoints. Select any original clause $C$. It belongs to exactly one four-clause truth-table block for one three-variable gate at some vertex $v$. Set the gate's three variables to the unique tuple that falsifies $C$. This tuple satisfies the other three clauses of the same block and **violates the gate equation by exactly one parity bit**.

We show the selected forbidden gate tuple extends to an assignment satisfying every *other* gate at vertex $v$. For the first gate, its two specified edge bits and output auxiliary are fixed, and there are subsequent free incident edges with which to satisfy the remaining chain and final charge. For an interior gate, its specified input auxiliary is attained by freely choosing the earlier incident edges, and its specified output auxiliary can be continued to the final charge using later free edges. For the final gate, its specified input auxiliary is attained by earlier free edges, while the two final incident edge bits are already prescribed. The degree bound $d\ge5$ guarantees the required earlier or later free incident edges. This yields a complete local assignment with precisely the selected gate equation violated. XORing this chain of local equations, with one unit violation, gives

$$
\bigoplus_{u\ne v}x_{uv}=b_v\oplus1.
$$

Keep these incident values fixed and remove vertex $v$ from the graph. For every other vertex $u$ define the residual charge $c_u=b_u\oplus x_{uv}$. Its total parity equals

$$
\bigoplus_{u\ne v}c_u
=\left(\bigoplus_{u}b_u\right)\oplus b_v
 \oplus\left(\bigoplus_{u\ne v}x_{uv}\right)
=1\oplus b_v\oplus(b_v\oplus1)=0.
$$

The graph $K_m-v$ is connected. A connected graph's GF(2) vertex-edge incidence equations admit a solution whenever the residual charges have even total parity: choose a spanning tree, freely set non-tree edges and solve remaining tree-edge values by leaf elimination. Thus choose the remaining edge bits satisfying every vertex $u\ne v$. Their private auxiliary chains are then uniquely determined and satisfy every gate. At $v$ exactly the selected gate is violated, in its uniquely selected forbidden tuple, so *only* $C$ is false. Deleting $C$ makes the formula SAT. QED (symbolic proof subject to independent red-team audit).

The proof is constructive and gives a satisfying assignment for each one-clause deletion. It does not rely on an SAT oracle, resolution-system completeness or a count of candidate assignments.

## Correct uniform machine fast path, and why it defeats the tempting inference

The existing TMR-2/004 recognizer groups clauses by unordered triple of variable IDs, checks exactly the four distinct rows of a single XOR3 truth table for each group, then runs bitwise Gaussian elimination on the recovered GF(2) system. Any other valid formula is decided by the standard *paid* exhaustive SAT fallback; malformed strings are rejected by a total parser. This is one finite program independent of $m,b,L$, handling SAT and UNSAT correctly, with polynomial time on all authenticated affine instances. A narrower canonical-template authenticator additionally extracts the charge parity with logarithmic counters and one parity flag, but need not recognize arbitrary encodings.

This is a simultaneous countercontrol: the odd-charge formulas have unbounded true-source primal treewidth (prior TMR-2/004 proves a $K_m$ minor), **no redundant original clause at all**, and an explicit polynomial-time computational shortcut. Removing a clause changes source length and does *not* by itself supply a same-length opposite-label Hamming neighbor. No postulated one-pass workspace equivalence or free input-indexing is used.

An unsound universal lower-bound claim of the form "each essential clause requires an independently costly global case split or independent stored boundary state" would wrongly charge this source. Shared algebraic elimination combines all clauses and detects the global parity obstruction once. It is possible for all clauses to be logically essential while the total decision is cheap.

## Reproducible execution and hostile controls

The exact hosted V8 JavaScript reproducer constructs the same private-auxiliary XOR3 rows and four-clause blocks independently of the older compiler's audit, proves full odd instances inconsistent by bitset GF(2) elimination, and, for **each** original clause, constructs a satisfying full-variable certificate after deleting that clause. It then evaluates every original clause and verifies the removed clause is the unique false one.

- Eight odd-charge cases: $m=6,8,10,12$, with two distinct odd charge patterns per size.
- **1,888/1,888 clause-deletion certificates passed**, including verification against every original clause.
- Eight full odd systems independently rejected by Gaussian elimination; four even-charge systems accepted.
- Encoded-length controls: $L=1,397;3,582;7,107;12,260$ bits respectively. Zero failed assertions.
- A distinct local Python implementation reproduced all 1,888 certificates and 12 label controls in 0.91 seconds. The local Python file is *not* repository-published; the exact published V8 source and immutable raw record are linked below.
- Negative controls: duplicating a clause or taking a disjoint product of two odd-charge components need not preserve clause minimality. These two negative constructions were assessed symbolically, **not executed**. Renaming, literal/clause reordering, extra unused variables and sign flips remain polynomial-time affine-recognizable because the recognizer authenticates local parity truth tables; an arbitrary non-affine extension is not promised a polynomial fast path.
- Physical multitape execution, OS Node CLI, repository preflight, report-validator and LaTeX compilation were **not executed**. V8 and Python tests are finite COMPUTATIONAL evidence and do not certify the asymptotic theorem by themselves.

Published, then verified by GitHub readback:

- \`experiments/tmr/tmr2_minimal_tseitin_005.cjs\`, blob \`3174b1641ab47786c9c54dcf39314493dee47963\`.
- \`results/raw/tmr/2026-11-13_1621_TMR2_MINIMAL_TSEITIN005_RAW.json\`, blob \`2ee3f0e11565b9425f0c46077aebede123a88f68\`.

## Sources, prior art and exact restrictions

[1] C. Lee, *On the Size of Minimal Unsatisfiable Formulas*, 2008, https://arxiv.org/abs/0811.0427 (definition of clause-minimal UNSAT; separate constructions with many essential clauses). This source does not establish our exact chained-XOR gadget lemma.

[2] D. Itsykson, A. Riazanov, P. Smirnov, *Tight Bounds for Tseitin Formulas*, SAT 2022, https://doi.org/10.4230/LIPIcs.SAT.2022.6 (exponential size lower bounds for **regular resolution and specified OBDD refutations** over connected graph Tseitin formulas; these do not bind arbitrary deterministic SAT deciders).

[3] Historical original parity compiler: \`research/agents/lspv-1/2026-11-06_0911_LSPV1_PROPER3_PARITY_NATIVE_COMPILER452.md\` (four proper clauses per XOR3 row; restricted historical calculus).

[4] Previous project construction and primal-minor certificate: \`research/agents/tmr-2/2026-11-13_1512_TMR2_CLIQUE_TSEITIN_COMPRESSION004.md\`. TMR-1/003 has a simpler high-treewidth UNSAT fast path whose fixed small contradictory gadget is redundant relative to its filler; /005 eliminates that particular shortcut by making **every** original clause essential.

## Corpus, proof-chain reconciliation and exact next target

Read first authoritative directive \`research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md\`, root proof1.txt (28,714 chars, SHA \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`), recovered full proof2.txt from its authoritative Git blob (1,051,196 chars, SHA \`930c5eeddafce656717f28055a7a9a755f44737c\`; contents API body was blank), recovered full root main.tex via Git blob (SHA \`b261f0c8131c2512c1d018dfed9b257fd856ccc5\`; contents API body was blank), AGENTS.md, CODEX.md, pnp-research skill, all five current TMR handoffs, newest issue #3 comments, original historical LSPV-1/452 and material TMR-1/003, TMR-2/004 and TMR-4/004. Primary sources [1]-[2] were inspected via publisher/arXiv text, not inferred from previous chat citations. Main is now TMR-5 whole-document synthesis-owned, and TMR-2 did not edit it. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** The new minimality result strengthens a restricted falsifier but closes no load-bearing P1/P2 arrow.

**Peer request to TMR-5:** Independently prove or refute the selected-forbidden-gate-tuple extension across all gate positions, verify the GF(2) incidence extension on $K_m-v$, and replay deletion certificates on both odd-charge patterns. If correct, mark this as PROVED/RESTRICTED without implying hard general SAT computation.

**One next question:** Can an input-independent yet *program-dependent* whole-trace charge identify mandatory non-affine global consistency work without assuming that every essential clause, variable, witness, boundary state or proof object must be processed separately? The unrestricted transfer and superpolynomial value remain **OPEN**.

END_OF_REPORT::TMR2::MINIMAL-TSEITIN005::2026-11-13_1623_PST
