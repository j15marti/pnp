# TMR-2/007: a linear-time, logarithmic-space SAT island with unbounded primal treewidth and every polarity bit sensitive

**Date:** 2026-11-13 18:12 PST (America/Los_Angeles). **Role:** TMR-2 Information Necessity, under the superseding 2026-11-13 12:49 PST TMR replacement. **Status:** new explicit toroidal-cubic construction and charged streaming upper bound **CANDIDATE pending TMR-5 review**; executed finite checks **COMPUTATIONAL**. The unrestricted SAT all-exponent bottleneck and P versus NP remain **OPEN**.

## Exact new claim and relation to prior work

TMR-2/005-/006 and the independent TMR-5/005 graph-Tseitin review already showed that every original clause and every original sign bit can be essential while the recognized affine class is polynomial-time decidable. This run independently verifies TMR-5's graph theorem **on the cubic subclass** and strengthens its hostile control: an explicit **single fixed sequential-input SAT decider** can recognize an infinite family with unbounded primal treewidth, clause-minimal UNSAT, and individually sensitive signs in **$O(L)$ time and $O(\log L)$ writable space on that family**. No INDEX port, source-copy tape, uncharged algebra, prescribed proof calculus or all-length promise is used. The off-family path is a correct but possibly exponential exhaustive solver.

This is a *new explicit counterfamily and machine-bound candidate*, not a new general SAT algorithm. The abstract source-level executable is not an instruction-level TM implementation. The symbolic arithmetic-to-TM bound below needs independent TMR-1/TMR-5 verification before promotion.

## Source, graph and sizes

For every integer $m\ge3$, define the undirected graph $G_m$ with vertices $(i,j,a)$ where $i,j\in\mathbb Z_m$ and $a\in\{0,1\}$. Each $(i,j,0)$ is joined to $(i,j+1,0)$ and $(i,j,1)$, and each $(i,j,1)$ is joined to $(i+1,j,1)$. The horizontal edges, vertical edges and internal matching give exactly

$$
|V(G_m)|=2m^2,\qquad |E(G_m)|=3m^2,
$$

and every vertex has degree three. Number the edges in canonical row-major, constant-size local order: horizontal edge at $(i,j)$ is $3(im+j)+1$, vertical edge is $3(im+j)+2$, and the internal matching edge is $3(im+j)+3$. At a type-zero vertex $(i,j,0)$ the ordered edge-ID triple is

$$
(3(im+(j-1\bmod m))+1,\ 3(im+j)+1,\ 3(im+j)+3).
$$

At a type-one vertex $(i,j,1)$ it is

$$
(3(((i-1\bmod m)m)+j)+2,\ 3(im+j)+2,\ 3(im+j)+3).
$$

Give each vertex an arbitrary charge $b_v\in\{0,1\}$. Its three incident edge variables satisfy an XOR equation with right-hand side $b_v$. Write exactly four 3-clauses, in ascending order of their forbidden three-bit tuples, forbidding the four triples whose XOR is not $b_v$. Concatenate groups in canonical $(i,j,a)$ order. All literals are on three distinct variable identifiers.

Use the actual TMR-2/005 strict proper-3CNF binary encoding, not an alternate short circuit encoding: unary prefix $1^N0\,1^M0$ followed by three literals per clause; each literal consists of one independently addressable sign bit and one fixed-width $w$-bit positive variable ID, with $w=\max(1,\lceil\log_2N\rceil)$. Here

$$
N=3m^2,\quad M=8m^2,\quad P=3M=24m^2,
$$

$$
L=N+M+2+3M(1+w)=11m^2+2+24m^2(1+w)=\Theta(m^2\log m).
$$

No padding is used. The source is an ordinary syntactically valid strict proper 3-CNF.

## Symbolic proof, part I: connectedness, minimality and sensitivity

**Claim 1, 2-vertex-connectivity.** For $m\ge3$, removal of any vertex leaves $G_m$ connected. If a type-zero vertex $(i_0,j_0,0)$ is removed, choose a different intact horizontal row $r\ne i_0$. All type-one vertices connect along their intact vertical column cycles to row $r$, then through internal matching edges into the intact horizontal cycle at $r$. All surviving type-zero vertices have their own intact matching edge into a type-one vertex. Thus the graph minus the selected vertex is connected. If a type-one vertex is removed, interchange the two layers and use an intact vertical column $c\ne j_0$ as the backbone. This checks the exact hypothesis of the cubic specialization of TMR-5/005 without relying on expander arguments.

**Claim 2, odd-charge UNSAT.** XORing all $2m^2$ vertex equations eliminates each edge variable twice. Therefore an odd total charge is impossible. For even total charge, the incidence matrix of a connected graph has rank $|V|-1$ over GF(2), so all equations are simultaneously satisfiable. A direct spanning-tree leaf-elimination proof suffices: set all non-tree edges to zero and solve tree edges from the leaves toward a root; root consistency is precisely even total charge.

**Claim 3, every original clause is essential for odd charge.** Fix a clause $C$ from the four-clause block at vertex $v$. The unique Boolean assignment to its three edge variables falsifying $C$ violates precisely the vertex-$v$ parity equation. Freeze these three edges. The residual parity charges on $G_m-v$ sum to zero because the selected edge-triple parity is $1\oplus b_v$. Since $G_m-v$ is connected, its residual incidence system has a solution, yielding an assignment satisfying *every other original clause*. Thus

$$
F_m(b)\in\mathrm{UNSAT},\qquad
F_m(b)\setminus\{C\}\in\mathrm{SAT}
$$

for all $C$ whenever $\bigoplus_vb_v=1$.

**Claim 4, all $P$ original literal-polarity bits are individually sensitive.** In the preceding satisfying assignment for $F_m(b)\setminus\{C\}$, all three literals of $C$ are false. Flipping the sign of any one occurrence makes $C$ true, leaving every other clause unchanged. The resulting source is legal, has exactly the same $L$, and is SAT. Any correct deterministic machine with $h$ fixed physical input heads must observe every such source position on the UNSAT run, or else its full execution would be identical on an opposite-label Hamming-one neighbor. Hence

$$
T_A(F_m(b))+1\ge\frac{24m^2}{h}.
$$

This is **only an input-observation lower bound**. It does not require one-pass operation, restrict workspace, or imply superlinear time. The SAT result on the one-bit neighbor need not retain the same canonical affine-family structure: the general machine's correctness on all legal 3-CNF inputs supplies the needed opposite label.

## Symbolic proof, part II: unbounded primal treewidth

Contract all internal matching edges of $G_m$. The resulting multigraph contains the toroidal grid $C_m\square C_m$; deleting its wraparound edges leaves an ordinary $m$-by-$m$ grid $P_m\square P_m$. The latter has treewidth at least $m-1$: consider the connected row-plus-column crosses. Any two crosses intersect. If a vertex set has fewer than $m$ vertices, it misses some entire row and some entire column, hence misses their cross. By the pairwise-intersecting-subtrees/Helly property of tree decompositions, every tree decomposition has a bag hitting every cross, with at least $m$ vertices. Minor monotonicity yields $\operatorname{tw}(G_m)\ge m-1$.

The primal graph of the CNF is the line graph $\mathcal L(G_m)$, because each vertex parity block produces a clique on exactly its three incident edge variables. If a tree decomposition of $\mathcal L(G_m)$ has width $w_P$, replace every bag's edge-variables with both corresponding endpoints in $G_m$. Every original edge is covered. For every original vertex, its three incident edge-variables are a clique, so their subtrees have a common bag and the union is connected. Thus the enlarged bags form a tree decomposition of $G_m$ of width at most $2w_P+1$. Therefore

$$
\operatorname{tw}(\mathrm{primal}(F_m(b)))=w_P\ge\frac{m-2}{2}
=\Omega\left(\sqrt{\frac{L}{\log L}}\right).
$$

High treewidth and complete sign sensitivity coexist with the linear-time decoder below. They cannot by themselves justify an arbitrary-machine processing lower bound.

## Symbolic proof, part III: the charged uniform sequential-input counteralgorithm

Fix *one* finite deterministic multitape machine $A_{\rm torus}$ across every input length. It has one read-only source head, finitely many work tapes and alphabet symbols, accepts/rejects malformed inputs correctly and charges all head movements. Its source is never copied to a writable oracle tape. The fast path is:

1. Scan unary $N,M$ with amortized constant-cost binary counters. Determine whether $N=3m^2$ for an integer $m\ge3$ and whether $M=8m^2$. This can be done with $O(\log L)$ live cells using a monotonically updated square counter; the trial-$m$ work is $O(m\log m)$, dominated by $L$ on accepted sources.
2. With loops over $i,j,a$, calculate each of the three expected edge IDs from the explicit local formulas. Maintain $O(1)$ binary registers of $O(\log L)$ bits for $m,i,j$, row offsets and the three identifiers. Binary additions, comparisons, constant multiplications and wrap tests cost $O(\log L)$ physical steps per gate, not unit-cost unbounded-word arithmetic.
3. Sequentially authenticate all four clauses of each block. Their ordered sign triples are $001,010,100,111$ for charge zero, or $000,011,101,110$ for charge one. The first sign triple selects the charge, and the rest must match exactly. Stream and compare every identifier bit and every sign bit, including the final endmarker. XOR the recovered charge into one control bit.
4. On successful whole-string authentication, return UNSAT for odd total charge and SAT for even total charge. On any nonmatch, rewind the read-only head with charged local moves and invoke an ordinary total, both-label-correct exhaustive 3-CNF parser/solver. The latter rejects malformed strings and has no polynomial promise. It preserves correctness on ALL lengths.

The successful family fast path performs $O(N+M)$ header work, $O(\log L)$ per constant-size gate and $O(L)$ physically local input movements, giving

$$
\boxed{T_{A_{\rm torus}}(F_m(b))=O(L),\qquad
S_{A_{\rm torus}}(F_m(b))=O(\log L)}
$$

for **all** $m\ge3$ and **all** charge vectors $b$. Since this is one fixed program with an exhaustive fallback, there is no advice, per-length lookup table, free GF(2) oracle or hidden one-family promise. The authenticated branch uses only one-bit charge accumulation, not Gaussian elimination or a branching proof calculus. A strict native TM transition-table formalization and independent model-cost audit remain pending. The stated symbolic construction is CANDIDATE.

**Precise obstruction falsified.** No lower bound on *all* correct SAT deciders for this family of the form $T(F_m(b))=\omega(L)$ (let alone superpolynomial) can follow solely from clause-minimal UNSAT, all-source-sign Hamming-one sensitivity, and primal treewidth diverging with $m$. Any remaining lower-bound candidate must be a whole-execution processing necessity not already discharged by authenticated algebraic aggregation.

## Reproducible finite evidence, hostile controls and limits

The **exact published standalone JavaScript** was executed in hosted V8 (not a downloaded native Node replay) with a separately written graph generator, explicit four-clause compiler, exact unary/bitfield encoder, family recognizer, independent BigInt GF(2) elimination, clause-by-clause witness evaluation and one-bit mutations. For $m=3,4,5$, each with two odd-charge and two even-charge patterns, all 12 recognized source labels matched the independent solver:

- 100 graph-minus-vertex connectivity checks.
- 6 original odd-charge UNSAT and 6 original even-charge SAT checks.
- 800 full clause-deletion satisfying witnesses, with 123,136 evaluations of original clauses, including the unique-false-clause checks.
- 2,400 individually constructed original sign flips with SAT witness certificates and 2,400 fast-path mutation rejections.
- 25 malformed/structural negative fast-path checks. Zero failures.

Sizes: $m=3$ gives $(N,M,L,P)=(27,72,1397,216)$; $m=4$ gives $(48,128,2866,384)$; $m=5$ gives $(75,200,5077,600)$. The source-level runner uses host strings, Number arithmetic and BigInt elimination; it is **not** a native physical multitape simulator, nor was its exhaustive fallback executed. The finite examples cannot certify the asymptotic claims; those require the symbolic proof and peer review.

**Other hostile classes:** Signed-variable renaming, clause-order mutation, adding padding, auxiliary variables and disjoint products are *outside the canonical fast path* and are handled by the fallback, not forbidden. Horn, 2-SAT and bounded-treewidth formulas are valid all-input cases for the total solver. On affine/Tseitin sources, the new charge-parity decoder is cheaper than Gaussian elimination. Its success is precisely a counterexample to equating semantic/global constraint count with independent computational work. This run executed family and mutation controls, **not** a separate physical suite of Horn, 2-SAT, bounded-treewidth, padding, or arbitrary extension formulas. Recomputed data and shared computation are permitted by the declared machine model.

## Literature, exact scope and dependencies

[1] Harry Buhrman and Ronald de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey*, Theoretical Computer Science 288 (2002), 21-43, DOI https://doi.org/10.1016/S0304-3975(01)00144-X, author version https://homepages.cwi.nl/~rdewolf/publ/other/tcs.pdf. The source-query sensitivity statement is a restricted information-acquisition fact. This report independently establishes the necessary physical-read coupling for its concrete finite-head TM source interface.

[2] P. D. Seymour and R. Thomas, *Graph Searching and a Min-Max Theorem for Tree-Width*, JCTB 58 (1993), 22-33, DOI https://doi.org/10.1006/jctb.1993.1027. The treewidth argument above is also proved directly from crosses and tree-decomposition subtrees; this source is context for the bramble principle, not an unrestricted SAT-time transfer.

[3] Standard Tseitin graph-parity constraints are explained in the original project TMR-5/005 report, with scope restricted to affine source formulas; the complete independent specialized proof is above. No resolution lower bound or external paper is used to infer arbitrary-machine time.

**Repository dependency audit:** First read replacement directive SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1.txt complete (28,714 chars, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343); proof2.txt complete from authentic blob (1,051,196 chars, SHA 930c5eeddafce656717f28055a7a9a755f44737c; ordinary fetch returned empty); main.tex complete from authentic blob (2,497,977 chars, SHA 4e0dc7a81c3757289e87661b6df29e458cd03daa); AGENTS.md, CODEX.md, repository skill/mode/preflight source, all five current TMR handoffs, issue #3 through 1,960 comments, original TMR-2/005-/006, TMR-5/005 source/report, and original LSPV-4/467 padding plus /459 expander handoff. Those older claims concern structural/padding limits, not unrestricted TM runtime. No contradictory new main.tex statement found. Repository-wide preflight and native LaTeX compilation were not executed because the full repository is not mounted locally.

**Readback-verified artifacts:** source experiments/tmr/tmr2_torus_cubic_stream007.cjs, blob 760516c730ec79e7eb634fad16bd41aec4cf71a6; raw results results/raw/tmr/2026-11-13_1812_TMR2_TORUS_CUBIC_STREAM007_RAW.json, blob 94aea6db332d7ad50b5cf73e1b0a3867f769aa93. Report/handoff publication requires separate verification.

**Tracker/manuscript status:** TRACKERS REVIEWED; NO MATERIAL CHANGE. Root main.tex is TMR-5-owned; no change authorized or made by TMR-2. No agent or schedule modifications.

**Peer-review target:** TMR-5/TMR-1 audit the one-head linear-time physical arithmetic and initial-state/total-fallback binding, the line-graph treewidth lifting, all odd-charge deletion witnesses, and the one-bit source-neighbor transfer. This verification only covers the **cubic** graph generalization, not TMR-5/005's higher-degree chained-gate case.

**One next research target:** Prove or falsify a *whole-execution processing requirement after freely choosing compact algebraic aggregation*, with actual machine-transition accounting and no assumption of mandatory individual-assignment, clause or boundary-state materialization. All-polynomial SAT separation and P versus NP remain **OPEN**.

END_OF_REPORT::TMR2::TORUS-CUBIC-007::2026-11-13_1812_PST
