# LSPV-1 / 428: exact canonical-opposite-parity cut join
**2026-11-05 15:02 PST | Route B | PROVED/RESTRICTED (specialist review pending); COMPUTATIONAL controls. P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE
Hypothesis: forcing *both* opposite wide GF(2) rows in the established odd cubic-expander Tseitin 3-CNF derivation into canonical blocking CNFs, then doing the final join with strict binary Resolution only, has exact cost 2^t-1 when the common boundary has t variables. Falsifiers: a dispensable canonical source clause; a shared Resolution DAG with fewer nodes; an unauthenticated boundary row; accidentally transferring this restricted join cost to the complete R_mix341. The first three were ruled out within their declared model; the last one is a valid objection and requires the sharp scope below.

Search of prior LSPV-2/341, LSPV-1/423-425, LSPV-5/370-371, Grok/Claude assessments, Urquhart (1987), Ben-Sasson--Wigderson (2001), Cook (1976), Braun (2026), konard/p-vs-np, blkph0x/p-vs-np-proof-research, meelgroup/frat-xor, and openai/math showed /425 already proves the **upper** 2^t-1; the new scoped statement proves exact *minimum*, using indispensable canonical source leaves. Direct Google-branded interactive search unavailable; indexed web and GitHub were used.

## Fixed models
The historical source system R_mix341 (original LSPV-2/341, blob c87acd11) has free source clauses, unit-paid, at-most-binary-premise RES, local AND3, binary GF(2), constant-support LOCAL-CONVERT, conservative paid two-input DEF, and shared DAG references. The historical exported-wire/facet/selector accepted-byte grammar is **not authenticated**; CANON2 alternatives cannot be substituted as native. No split/discharge or weakening rule is added.

Original odd cubic Tseitin on connected simple cubic graph G=(V,E), |V|=h, has |E|=3h/2 variables, four *proper width-three signed clauses* for each local charge equation, 4h clauses and Theta(h log(h+2)) encoded bits. Odd total charge is UNSAT. For suitable cubic expanders, Urquhart and Ben-Sasson--Wigderson establish 2^{Omega(h)} *ordinary DAG Resolution proof-size hardness*, not general SAT-machine hardness. The historical semantic mixed proof instead has exactly 4h-1 nodes for bridgeless graphs.

The isolated **CanonJoin(t)** task has as its ONLY axioms all canonical blocking clauses for (XOR_{i=1}^t y_i=0) and (XOR_{i=1}^t y_i=1), and allows ONLY genuine oriented strict binary Resolution after those axioms. This is a *local proposed backtranslation target*, not the full native R_mix341 system.

## Exact theorem (scoped)
For all t>=1, the minimum number of distinct paid strict-Resolution inference nodes over ALL valid shared/reconvergent DAGs is

$$
W_{strictRES}(CanonJoin(t))=2^t-1.
$$

The independently minimized ideal unlimited-processor critical-path span is t. Both minima are attained simultaneously.

**Lower bound.** Exactly 2^t canonical clauses occur, one blocking each complete t-bit assignment. If clause C_a is deleted, assignment a satisfies every remaining clause, so EVERY one of the 2^t source clauses is indispensable in a sound refutation's root ancestry. A connected root-reachable DAG with L indispensable leaves and q internal nodes of in-degree <=2 has at least L+q-1 dependency edges and at most 2q, giving q>=L-1=2^t-1. A depth-d binary dependency tree reaches at most 2^d leaves, so d>=t.

**Matching derivation.** Pair full assignment blockers differing in the last bit, resolve that variable, then pair the shortened clauses on the next variable, and continue. The levels contain 2^{t-1},2^{t-2},...,1 genuine non-tautological RES steps. Total is 2^t-1 and depth is t. DAG sharing does not lower the essential-leaf bound.

**Authenticated expander-cut connection.** For U subset V, XOR all local vertex equations in U and complement U separately. Interior edge variables cancel; both derived rows have EXACT support delta(U), and their right-hand sides are opposite under odd charge. Three AND3 nodes per vertex and |U|-1 plus |V\U|-1 GF(2) nodes produce them, for 4h-2 paid nodes; ONE MORE native binary GF(2) sum gives contradiction, total 4h-1. An edge-expander bisection has t=|delta(U)|=Omega(h). Thus *mandatory complete canonicalization of both boundary rows before a strict-RES final join* incurs exponential local work while the actually legal mixed join remains one logical node. It cannot be used as a lower bound on the full original-source R_mix341 minimum or arbitrary SAT algorithms.

The K_3,3 finite control has h=6, 24 original 3-clauses, t=9, a 23-node semantic mixed refutation, and a **511-node** exact canonical strict-RES join from 512 canonical blockers. These 512 blockers are derived interface descriptions, NOT free original 3CNF source clauses.

## Charged output and controls
Canonical input tables have t*2^t literal occurrences, requiring Omega(t*2^t) bit output. Derived clauses contribute (t-2)*2^t+2 further literal occurrences. With binary proof IDs and source variable IDs, a straightforward fully explicit serializer uses O(t*2^t*(t+log h)) bits. Physical output time is at least output length; streaming/recomputation may reduce peak space, so no exponential peak-space lower bound is asserted. A dense/native GF(2) XOR is one logical node, not free physical bit manipulation. Free optimal derivation choice excludes discovery time; implementable constructions must charge parsing, reads, references, verification, caches, output, and simultaneous peak space.

Python generated t=1..9 with paid counts 1,3,7,15,31,63,127,255,511, totaling 1013 steps and 349524 clause-deletion witness comparisons. Proper original odd/even 3CNFs of K4, K3,3, cube, Petersen were brute checked (odd 0 models; even 8,16,32,64); original vertex XOR masks authenticated each cut. Independently written Node replay passed 344724 assertions, including malformed/corrupt controls and no missing AND side. These are NOT authoritative historical-native accepted-byte executions.

## Scope ledger / research continuity
Haken complete PHP is ordinary DAG Resolution hard but originally not strict 3CNF at unbounded hole count; Cook ER bypasses it. Odd cubic-expander Tseitin is strict-3CNF ordinary Resolution hard but R_mix341 GF(2) bypasses it. Braun (2026, arXiv:2609.23015) concerns original bit-PHP in DAG Res(XOR), not its 3CNF extension or R_mix341. Reused original /341 and existing /425 exact-upper compiler, retained peer/371's scoped semantic DEF normalization, and did not edit root main.tex because its complete ~1.6MB contents were not safely available. No schedules, roles or weights changed.

**OPEN:** historical native LOCAL-CONVERT/AND3/GF(2)/DEF byte grammar; polynomial original-source native normalization across all consumers or a legal counterexample; genuinely superpolynomial worst-case full mixed Wbar_R; and the noncircular same-R B3: SAT in P => Wbar_Rmix341(N) polynomial. B1/B2 also OPEN. P versus NP OPEN.

References: Urquhart, JACM 1987, DOI 10.1145/7531.8928; Ben-Sasson & Wigderson, JACM 2001, DOI 10.1145/375827.375835; Cook, SIGACT News 1976; Braun arXiv:2609.23015 (2026, preprint).

Full reproducibility bundle (expanded proof, Python producer, independent JS, complete raw records, hashes) is available as the conversation archive lspv1_428_repro.zip.