# LSPV-1/447: near-optimal parallel proof depth on an established-family 3-CNF reduction control

**2026-11-06 05:04 PST, America/Los_Angeles | Route B lead | PROVED/RESTRICTED and COMPUTATIONAL.** Fixed historical R_mix341 weights, roles and schedules are unchanged. The accepted-byte historical checker remains unavailable. B1/B2/B3, the full mixed superpolynomial lower bound, and P versus NP are OPEN.

## IDEA -> SEARCH -> ITERATE: hypothesis and falsifiers

Hypothesis: the *existing*, deliberately easy charge-chain 3-CNF target of LSPV-1/444, obtained from a **recognized** cubic-Tseitin source, admits a balanced original-coordinate AND3/GF(2) proof with logarithmic ideal span. Pair that upper construction with LSPV-1/446's indispensable-source lower bound, incorporating REFEREE385's explicit ancestor-local soundness repair.

Falsifiers: (F1) a four-clause local pack exceeds three original-source variables or fails its alleged affine truth table; (F2) the XOR sum produces a wrong contradiction or misses an AND premise; (F3) some historical native node silently has more than two antecedents, or a branch-local conclusion leaks across contexts; (F4) identical work/span theorem was already established by /444, /446 or REFEREE385. Complete source-to-root construction and independent finite replay reject F1-F2; the lower theorem is conditional on the documented /341 ancestor-local, unit-paid, binary-premise grammar; /446 had exact work and a sequential span bound, not the present near-exact span bound. No new source hard family is proposed.

## Family, lower-bound system, exact encoding and legal shortcuts

**Original published source control:** connected simple cubic graph with h vertices, 3h/2 original edge variables, local equations XOR of the three incident edge bits equal charge chi_v, and **four proper signed ternary clauses per vertex** excluding the wrong-parity assignments. Thus 4h clauses and Theta(h log(h+2)) indexed source bits. With odd total charge this is UNSAT. Urquhart 1987 and Ben-Sasson/Wigderson 2001 prove 2^Omega(h) lower bounds on **ordinary shared-DAG Resolution** for suitable cubic expander sequences. This is not an all-algorithm or full mixed-calculus lower bound: historical declared /341 AND3/GF(2) has a 4h-1 paid-node upper for connected bridgeless originals (LSPV-2/341).

**Pre-existing /444 easy target, not a hardness-preserving reduction:** for each recognized component with k>=2 vertices, create k forced charge-input source variables, k-1 XOR-prefix gate-output source variables, and one forced-zero final output. Each forced literal l uses four proper signed ternary clauses (l OR p^s OR q^t), with two private original *target source* variables; each binary XOR gate uses its four wrong-output proper-3 clauses. Exactly 8k original ternary clauses, 4k+1 occurring variables, and O(k log k) indexed source bits. The transformation preserves SAT/UNSAT and has both-direction satisfying-witness maps but does **not** preserve Resolution proof hardness. On odd component charge LSPV-1/446 proved exact W_R(H_k)=5k+2 in the ancestor-local, conservative, unit-paid, at-most-binary-premise calculus including strict Resolution. Its chosen **5k+3** source clauses are indispensable even relative to all 8k clauses. Independent REFEREE385 verified this after explicitly requiring each node to be justified solely by its recorded ancestry.

Mandatory external shortcuts are retained: Haken PHP ordinary Resolution versus Cook Extended Resolution; Tseitin GF(2); Braun's 2026 bit-PHP theorem in DAG Res(XOR) (arXiv:2609.23015v2, unreviewed outside its formalization, and different 2ell-width encoding). No published restricted lower bound is transferred to the complete mixed calculus.

## Theorem 447.1 (ideal parallel-depth sandwich)

Let D_R(H_k) be the **minimum paid critical-path depth** over *all* legal ancestor-local original-source-authenticated refutation DAGs under declared R_mix341 semantics: free after-the-fact choice, all legal OR alternatives and AND dependencies, shared subproofs counted once, unit cost per paid node, source axioms at depth zero, no added split/discharge rule. Then for every odd-charge target component k>=2,

$$
\boxed{\lceil\log_2(5k+3)\rceil
\ \le\ D_R(H_k)\
\le\ 2+\lceil\log_2(2k)\rceil\
\le\ \lceil\log_2(5k+3)\rceil+1.}
$$

For every k=2^t, t>=1, the two bounds coincide:

$$
\boxed{D_R(H_{2^t})=t+3.}
$$

**Lower:** by /446 + REFEREE385, all e=5k+3 core clauses are required source ancestors of any contradiction. In any directed dependency DAG with at most two antecedents per paid node, a node of depth d has at most 2^d distinct source ancestors, regardless of sharing, reconvergence or free optimal proof selection. Therefore d>=ceil(log2 e). Rules must be ancestor-local; global semantic access to unrecorded source clauses is not allowed.

**Upper:** precisely 2k local four-source packs comprise k charge-input pads, k-1 XOR gates and one output pad. For each pack, first use two independent unit-paid AND3 conjunctions, then a third AND3 conjoining their results, with exact exhaustive eight-row verification of the affine annotation. Every pack uses only its same three *original target source* variables, including gate outputs that are original target-source coordinates, not unpaid fresh DEF wires. The resulting affine rows are c_i=chi_i, p_1 XOR c_1 XOR c_2=0, p_i XOR p_(i-1) XOR c_(i+1)=0, and p_(k-1)=0. Pairwise balanced, unit-paid XOR additions of all 2k rows produce 0=1 when sum chi_i=1. Work is exactly

$$
W_{\mathrm{balanced}}=3(2k)+(2k-1)=\boxed{8k-1},
\qquad
D_{\mathrm{balanced}}\le 2+\lceil\log_2(2k)\rceil.
$$

The last inequality uses 4k<=5k+3. For k=2^t, 4k<5k+3<=8k, and the ceiling bounds coincide. This is a theorem for *ideal unlimited processors*, not a machine-runtime estimate. Previous /446 **minimum work** is 5k+2, so the balanced certificate uses less than 8/5 times minimum work. It does not establish a complete Pareto frontier or rule out a short-span minimum-work certificate.

## Corollary 447.2 (tight optimal-work tree rigidity)

Every single-component proof attaining q=5k+2=e-1 paid nodes must have **exactly** the selected e=5k+3 indispensable original-source ancestors. Its connected ancestry graph has e+q vertices and at least e+q-1=2q undirected dependency edges; binary indegree permits at most 2q. Hence all paid nodes have exactly two distinct dependencies and the underlying ancestry graph is a tree. No reconvergent shared subproof occurs in a work-optimal proof of this **specific** target. This is a consequence of tight source capacity, not a restriction imposed on other proofs.

## Computational replay

The locally archived full Python producer generated 14 exact proper-3 source packets, odd UNSAT and even SAT at k=2,3,4,5,8,16,32. It emitted all AND3 truth tables, row sums and proof-node IDs, plus **371** full-source individual core-clause deletion SAT witnesses. The separate independent Node verifier checked every original clause, source SHA, eight-row conjunction and typed affine annotation, XOR arithmetic, DAG ancestry and critical paths, and rejected 7/7 hostile corruptions. **107,697 assertions** passed. A compact independently executed JS generator/checker is committed under experiments/arc; its smaller test scope is not described as a full historical checker.

| k | Prior exact min work | Balanced work | Span lower | Balanced span |
|---:|---:|---:|---:|---:|
| 2 | 12 | 15 | 4 | 4 |
| 3 | 17 | 23 | 5 | 5 |
| 4 | 22 | 31 | 5 | 5 |
| 5 | 27 | 39 | 5 | 6 |
| 8 | 42 | 63 | 6 | 6 |
| 16 | 82 | 127 | 7 | 7 |
| 32 | 162 | 255 | 8 | 8 |

Observed on this host: producer ~0.078 seconds and 97,676 KiB peak RSS; independent Node ~0.108 seconds and 35,800 KiB peak RSS. The generated 14 explicit JSON proof/witness packets total 246,254 bytes. Original input bits are Theta(k log k); an explicit proof encoding has a safe O(k^2 log k) upper bound. Real algorithm accounting also charges source/index/head reads, parsing, checking, failed branches, construction, evidence output, references/retrieval, cache/recomputation, row-mask manipulation and simultaneous peak space. None of these tests establishes an FLMV same-machine time/space exponent or bounded proof discovery in general SAT.

## Research and history readback

Recovered governing five-role refocus dated November 2 (historical commit 4e29ed7), current issue #3 including LSPV-1/446 and REFEREE385, native /341 report (blob c87acd11...), AGENTS.md, CODEX.md, research skill, LSPV-1/443–446, LSPV-3/446, and REFEREE385 (blob 81ac676e...). Read actual Grok GROKPROOF/2026-11-06_1220_PROGRESS.md and Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex. Required external repository inspection: konard/p-vs-np README + scripts/proof_status.json, blkph0x/p-vs-np-proof-research METHOD_INDEX.md + BOUNDED_PROJECTION_BARRIER.md, and relevant FRAT-XOR format.md, CakeML/LPR, openai/math. Read primary sources Urquhart 1987, Ben-Sasson/Wigderson 2001, Cook/Reckhow 1979, Cook ER 1976, and the current Braun arXiv abstract. Google-branded search was not available as a separate interface, indexed web search was used. No external code compilation or authoritative native-byte checker execution is claimed.

## Outstanding transfer and B3

This is a close-to-optimal **depth bound on an easy reduction target**. The source expander family remains easy in the declared mixed calculus, and the /444 target intentionally erases Resolution hardness. We have not supplied a superpolynomial Wbar_R over all mixed rules, historical accepted-byte source/LOCAL/DEF/FACET grammar, or the noncircular same-fixed-calculus B3:

$$
\mathrm{SAT}\in P\quad\Longrightarrow\quad \overline W_{R_{\mathrm{mix341}}}(N)=N^{O(1)}.
$$

B1/B2/B3 and P versus NP remain **OPEN**. Next: seek whether k=5 has an even shorter legal shared/branched proof, authenticate the exact historical AND3 native bytes, and prioritize known hard families plus genuine all-rule hardness transfer rather than additional bespoke formulas.

**Primary references:** Urquhart, JACM 34 (1987) 209–219, DOI 10.1145/7531.8928; Ben-Sasson & Wigderson, JACM 48 (2001) 149–169, DOI 10.1145/375827.375835; Haken, TCS 39 (1985); Cook, SIGACT News 8(4) (1976); Cook & Reckhow, JSL 44 (1979); Braun, arXiv:2609.23015v2 (2026, proof-system-specific preprint).
