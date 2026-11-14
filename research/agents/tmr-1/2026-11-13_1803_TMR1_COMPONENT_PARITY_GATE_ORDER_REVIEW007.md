# TMR-1/007: exact component-parity criterion and gate-order falsifier for Tseitin 3-CNF

**Run:** 2026-11-13 18:03 PST, America/Los_Angeles. **Role:** TMR-1, current Machine Model Lead. **Status:** new exact criterion and representation-order corollary **CANDIDATE pending TMR-5/TMR-2 independent mathematical review**; independently reviewed TMR-5/005's biconnected sufficiency proof **PROVED/RESTRICTED at the stated original XOR3-chain scope**; finite audits **COMPUTATIONAL**. P versus NP **OPEN**.

## Exact model, source and objective

Use ONE fixed, finite, deterministic, total multitape 3-SAT decider $A$ for every length, with a fixed finite alphabet/control, a fixed finite number $h$ of read-only input heads (if local-input), charged physical transitions and visited writable work cells including indices, stacks, temporary representations, preprocessing, conversion, rereading and recomputation. Input has explicit encoded bit length $L$, not the variable or clause count. Malformed inputs must be rejected; both valid SAT and UNSAT outputs must be correct. A random-access or word-RAM operation must be paid and separately translated.

The unrestricted research target is still

$$
\forall A\ (A\text{ correct, uniform, total})\ \forall k\in\mathbb Z_{\ge1}\ \forall C>0\ \forall L_0\ \exists F\text{ valid},\quad
|F|\ge L_0\ \wedge\ T_A(F)>C(|F|+1)^k.
$$

No result here proves that target or supplies a universal processing lower bound. The formulas below are cheap for a correct fixed Gaussian-elimination recognizer with paid exhaustive fallback.

The strict proper 3-CNF source encoding has unary $1^N0\,1^M0$ header and three independently signed $w=\max(1,\lceil\log_2N\rceil)$-bit variable IDs per clause:

$$
L=N+M+2+3M(1+w).
$$

For a finite simple graph $G=(V,E)$ with degree at least three and any odd total charge $b\in\mathbb F_2^V$, introduce one variable per edge and private vertex auxiliaries. A degree-$d$ vertex has a path of $d-2$ XOR3 gates with $d-3$ private auxiliaries, the final gate carrying $b_v$. Encode each gate as precisely four proper 3-clauses, one for each forbidden parity tuple. The source counts are $N=3(|E|-|V|)$, $M=8(|E|-|V|)$. This definition is inherited from the exact original TMR-2/005 and TMR-5/005 reports, not from an arbitrary alternative Tseitin compiler.

## New TMR1-CC7 exact criterion (CANDIDATE)

Fix ANY such $G$, not necessarily connected, with odd total charge. Fix an original clause $C$ at gate $q$ of vertex $v$. Let $\tau$ be the unique assignment to that gate's three input variables that falsifies $C$ (hence violates the gate parity by one). Let $\mathcal W(v,q,\tau)$ be the set of assignments $z\in\mathbb F_2^{\delta(v)}$ to ALL incident original edge bits which admit private local auxiliaries at $v$ satisfying every gate there except $q$, while imposing exactly $\tau$ on $q$.

Let $H_1,\ldots,H_r$ be the connected components of $G-v$ and let $\delta(v,H_i)$ be the edges joining $v$ to $H_i$. Then

$$
F(G,b)\setminus\{C\}\in\mathrm{SAT}
\iff
\exists z\in\mathcal W(v,q,\tau)\quad
\forall i:\quad
\bigoplus_{e\in\delta(v,H_i)}z_e
=\bigoplus_{u\in H_i}b_u.
\tag{CC7}
$$

**Proof, necessity.** XORing all vertex equations yields $0=1$, so the original formula is UNSAT. Any assignment satisfying all original clauses except $C$ must falsify $C$: otherwise it would satisfy the original formula. All other three clauses of the same XOR gate must remain true; the unique tuple $\tau$ violates only that gate. Consequently the local incident assignment is in $\mathcal W$. On each component $H_i$, XOR the remaining satisfied vertex parity equations. Internal edges cancel twice and boundary edges from $v$ occur once, giving the displayed component parity equality.

**Proof, sufficiency.** Pick the stated $z$ and its local auxiliary completion at $v$, which falsifies exactly $C$ locally. At every remaining vertex $u$, move the fixed incident boundary bit $z_{uv}$ to the right side, obtaining a linear GF(2) incidence system on $H_i$. Its total right-side parity is zero by the corresponding component equality. On a connected graph, the incidence matrix image consists exactly of even-charge vectors: set non-tree edges to zero and solve tree edges by leaf elimination. Do this independently for each $H_i$, then fill all remaining private auxiliary XOR chains consistently. Every original clause except $C$ is true. This proves CC7 for every gate position and all forbidden tuples.

The criterion reduces a claimed necessity to a *concrete finite boundary-linear algebra check*, rather than counting clauses, assignments or possible source continuations as work. It makes no all-machine time assertion.

### Independent review of TMR-5/005

If $G-v$ is connected for each $v$, there is only one $H_i$. Every forbidden gate tuple permits a local completion: the first/last gate has an unconstrained complementary path segment with free incident edges; an interior gate has free incident edges on both sides. XORing the local chain with one defect yields $\bigoplus_{e\ni v}z_e=b_v\oplus1$. Since $\bigoplus_u b_u=1$, the ONE component boundary equality follows automatically. Thus CC7 proves, independently of the TMR-5 implementation, that **every original clause is essential** for every biconnected minimum-degree-three graph. Applying the elementary polarity-flip lemma yields one same-length valid SAT neighbor per original sign bit. This independently supports TMR5-BG5 at exactly its **restricted** scope, including arbitrary gate positions, $K_4$, $K_5$, odd-sized cliques, and cubic vertex-biconnected graphs. The general-machine superpolynomial implication is still OPEN.

A 2024 public discussion of minimality for the *unexpanded full-degree vertex parity CNF* gives the familiar $G-v$ component argument. It is related prior art, **not** a source proving our private-auxiliary XOR3-chain criterion or its order-dependent counterexample. Our contribution is this compiler-specific exact CC7 and independently tested ordering boundary, not the general discovery that connected even-charge incidence systems are solvable.

## New concrete falsifier: one connected graph, identical charges, two gate orders

Let two copies of $K_4$ share only vertex $v=0$. The two vertex-deletion components at $0$ are $H_L=\{1,2,3\}$ and $H_R=\{4,5,6\}$. Every noncenter vertex has degree three, while $v$ has degree six. Put $b_0=1$, all other charges zero. The original formula is UNSAT, with $N=15$, $M=40$, $L=657$ and $120$ literal-sign bits.

For the blocked incident-edge order $e_{01},e_{02},e_{03},e_{04},e_{05},e_{06}$ the four center gates are

$$
e_{01}\oplus e_{02}\oplus y_1=0,\quad
y_1\oplus e_{03}\oplus y_2=0,
$$

$$
y_2\oplus e_{04}\oplus y_3=0,\quad
y_3\oplus e_{05}\oplus e_{06}=1.
$$

Select the second gate and forbidden tuple $\tau=(y_1,e_{03},y_2)=(1,0,0)$. The removed proper 3-clause is

$$
C=(\neg y_1\lor e_{03}\lor y_2).
$$

The first two gates force $e_{01}\oplus e_{02}\oplus e_{03}=1$. The last two force $e_{04}\oplus e_{05}\oplus e_{06}=1$. But the zero charges inside BOTH $K_3$ components require both boundary parities to be zero. No extension exists, so **even after deleting $C$ the formula is UNSAT**. This is an exact symbolically proved falsifier of the tempting stronger claim that connected minimum-degree-three graphs always yield clause-minimal chained Tseitin CNFs. It is NOT a counterexample to TMR-5/005, which explicitly requires $G-v$ connected.

Now keep the SAME graph and charge but order the center's incident edges as

$$
e_{01},e_{04},e_{02},e_{05},e_{03},e_{06}.
$$

The independent criterion check and direct local $2^9$-state brute-force audit find that **all forty original clauses become essential**. Thus vertex-biconnectivity is sufficient but **not necessary**, and even on one fixed incidence graph minimality is sensitive to the order and auxiliary representation of the XOR chain. The blocked order has 36 essential and 4 redundant clauses, corresponding to 108 individually SAT-flippable sign positions and 12 sign positions whose single reversal remains UNSAT; the interleaved order has 40 essential clauses and all 120 signs individually SAT-flippable. Both remain polynomial-time affine instances.

This representation dependence is a strong hostile control for any algorithm-independent necessity premise. Clause indispensability and source-bit sensitivity alone cannot force a post-acquisition computational cost.

## Executed audits and exact provenance

**Native Python (independently written; local source/output not published):** standard-library binary GF(2) row elimination and direct clause evaluator, completed in a sub-25-second chunk. Twelve odd-charge graph/source cases across $K_4,K_5,K_6$, triangular prism, cube and blocked bowtie. All 448 original-clause deletion possibilities checked against CC7: 440 SAT, 8 UNSAT. All 440 SAT deletions had a unique-false-clause full-variable witness and 1,320 independently checked individual sign-flip witnesses. Six even-charge SAT controls, 2,214 assertions, zero failures. Independent native Python second chunk swapped bowtie incident order; blocked remained 36/40 minimally essential while interleaved became 40/40 for each of two odd charges. Two Python chunks executed, both completed; code and raw remain local-only, not claimed as GitHub-published.

**Exact standalone hosted V8 reproducer executed and published:** `experiments/tmr/tmr1_component_parity_criterion007.cjs` (blob `c35040ae2d1198afb5d10143322edbbef660e220`) produced `results/raw/tmr/2026-11-13_1803_TMR1_COMPONENT_PARITY_CRITERION007_RAW.json` (blob `58bb30e5ab912ab38d3808b5f1c252b7b89a5397`). The V8 code was independently constructed rather than importing TMR-5 source. Exact agreement with native Python on 12 cases and 448 deletions, 2,214 assertions, zero failures.

**Additional independent direct local-state audit:** `experiments/tmr/tmr1_gate_order_bowtie007.cjs` (blob `aa38b6a9d6cdbed76992a4d986ddcf96d988de64`) and `results/raw/tmr/2026-11-13_1803_TMR1_GATE_ORDER_BOWTIE007_RAW.json` (blob `a6010d8f2db4bc66e8890d7878ab5b301b95bb11`). V8 executed 64 selected center gate/forbidden-tuple cases, examining 12,398 concrete local bit assignments, with both blocked and interleaved orders and two distinct odd-charge positions. No failures. This separate brute-force computation uses the CC7 component constraints, rather than the original TMR-5 solver.

**Limits:** These computations are GF(2)/CNF source-level checks with host integers, not instruction-level physical TM traces, proof of a 3-SAT time lower bound, or a complete all-input implementation of the Gaussian fallback. The statement that a fixed uniform binary multitape solver can parse XOR3 clause groups and run polynomial-time paid GF(2) elimination is a standard algorithmic construction, not an uncharged oracle. No resource lower bound beyond physical observation is claimed.

## Corpus, literature and historical comparison

Authoritative 2026-11-13 12:49 PST replacement directive read first and rechecked before publication. Root `proof1.txt`: full 28,714 chars, SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`; root `proof2.txt`: ordinary file read returned a **blank body despite SHA**, recovered fully from original Git blob `930c5eeddafce656717f28055a7a9a755f44737c` (1,051,196 chars), NOT treated as empty. Root `main.tex`: ordinary contents similarly blank, recovered completely from original Git blob `4e0dc7a81c3757289e87661b6df29e458cd03daa` (2,497,977 chars). Root `AGENTS.md`, `CODEX.md`, pnp-research skill, issue #3 through 1,960 comments, all five latest TMR handoffs, peer ORIGINAL TMR-2/005, TMR-2/006, TMR-5/005 including exact standalone JS/raw, TMR-1/005, TMR-3/006 and TMR-4/006 model-boundary summaries inspected. Original historical restricted-model work retains its old evidence/status but not superseded LSPV ownership.

Primary source [1]: Itsykson, Riazanov and Smirnov, *Tight Bounds for Tseitin Formulas*, SAT 2022, DOI [10.4230/LIPIcs.SAT.2022.6](https://doi.org/10.4230/LIPIcs.SAT.2022.6). This establishes treewidth-dependent lower bounds for **regular resolution and OBDD refutations**, not arbitrary deterministic SAT machine runtime. We do not transfer it.

Primary source [2]: Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 835-865 (2005), DOI [10.1145/1101821.1101822](https://doi.org/10.1145/1101821.1101822). Its simultaneous polynomial time/small-space exclusions are explicitly model- and exponent-restricted; they do NOT exclude every polynomial exponent or workspace regime. No result here changes that.

Related secondary discussion (not used as proof): [Tseitin formula on 2-connected graph](https://cs.stackexchange.com/questions/166831/tseitin-formula-on-2-connected-graph), February 2024, treats a different unexpanded vertex-CNF encoding.

**Trackers:** TRACKERS REVIEWED; NO MATERIAL CHANGE to proof1.txt or proof2.txt. No canonical root `main.tex` edit: TMR-5 owns scientific synthesis and must independently review the new CC7/order claim before incorporating it. Nothing was reconstructed over unreadable files. No schedules created, modified, revived or disabled.

**Next single target for TMR-2/3/4/5:** construct or falsify an all-transition *processing* potential remaining necessary after every source bit has been read, robust to the blocked/interleaved XOR3 representation switch, a fixed paid Gaussian-elimination solver, multiple input heads, indexed accesses, caching and recomputation. A bound equivalent to the unknown runtime, or clause-essentiality alone, is insufficient.

END_OF_REPORT::TMR1::CC7::2026-11-13_1803_PST
