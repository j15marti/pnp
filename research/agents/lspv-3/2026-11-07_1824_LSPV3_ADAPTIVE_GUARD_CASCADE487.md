# LSPV-3/487: adaptive affine guards defeat full-rank static enumeration, with shared RES guard certificates

**2026-11-07 18:24 PST | LSPV-3 Route B | PROVED/RESTRICTED plus COMPUTATIONAL. Historical R_mix341 and P versus NP OPEN.**

**Exact nodes:** [P2-F13], [P2-L3-485], [P2-D2], [P2-C3], [P2-D1], [P2-B1], [P2-B2]. New evidence [P2-L3-487]. Cross-route [P1-01]/[P2-A2] unchanged.

## IDEA, assumptions and four falsifiers

Hypothesis: the (2^r) full affine-anchor cosets in /485 are a valid **static upper-bound construction**, not an unavoidable number of affine pieces when the full source-authenticated shared gate DAG is allowed to be specialized **adaptively**. Test a nested conservative AND cascade whose anchors are globally affine and independent. Predict only (g+1) affine subcube leaves although the static anchor rank is (r=g).

Registered falsifiers before search: (1) the guards overlap, omit an assignment or are empty; (2) some named gate remains nonlinear in original variables on a claimed leaf; (3) the purported shared global guarded clauses require wrong-polarity RES or unavailable premises; (4) actual historical DEF facet/private-reference grammar does not admit the exhibited typed proof. Exact symbolic proofs and two implementations exclude (1)-(3) under the DISTINCT declared model. (4) is OPEN.

## SEARCH and continuity

Both complete trackers were retrieved: proof1.txt blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and proof2.txt startup blob `5fbd894869cd5bf1a8de2fff9b84e8c850a2dff9`. Read issue #3 (latest role reports /422, /481, /492), Nov. 2 governing five-role handoff, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, original LSPV-2/341 grammar and its recovered JS SOURCE/AND3/XOR verifier; LSPV-3/485-486; red-team LSPV-5/412/422; Grok GROKPROOF/2026-11-08_0118_PROGRESS.md, and Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex. The /341 primary text provides semantic rules but no complete general mixed accepted-byte parser or DEF facet selector. The original recovered checker is SOURCE/AND3/XOR only, not the full historical mixed calculus. The /486 report's displayed AND facet has an independently caught wrong sign; /486 executable and current proof2 evidence correctly use `(-w OR -v OR e)` (LSPV-5/422).

Required repository change-aware review, exact paths/blobs: konard/p-vs-np `scripts/proof_status.json` `93b77ed3d8fe456f81c690035f45f07910a247f2` (finite-TM checked subtheorems, no P=NP proof); blkph0x/p-vs-np-proof-research `METHOD_INDEX.md` `18d693ea71dfa433370eb7afbebc3106e32f03e5` (restricted experimental and proof portfolios); meelgroup/frat-xor `format.md` `986a21aa92b62f844ef1fce852193142c41b2b1f` (external mixed format, not /341); tanyongkiam/cake_lpr `README.md` `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c` (checker trust, not shortest proof); peitl/short-proof `README.md` `93d2090dba9739bc4983c65ea639a24e1f5e0fab` (ordinary Resolution minimum); openai/math `README.md` `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` and anthropics/formal-math `README.md` `1df53bfc14a022088d1b5757698f692bf79390b4` (claimed research artifacts, NOT checker replay here). Indexed web queries: Chvatal-Szemeredi 1988 random 3-CNF; Pang 2026 arXiv:2610.00837 syntactic proof degree/size; branching-program and subcube partition literature including Buss-Das-Knop 2019 arXiv:1910.08503 and Kothari-Racicot-Desloges-Santha 2015 arXiv:1504.01339. Google-branded search and original /341 native checker execution unavailable; no PDF was analyzed. No novelty claim.

## ITERATE: exact shared-DAG affine-cascade theorem (PROVED/RESTRICTED)

Fix (g>=2) and independent original Boolean inputs (z,a_1,\ldots,a_g). Introduce distinct, fresh, conservatively defined AND outputs

$$
w_0=z,\qquad w_i=a_i\wedge w_{i-1}\quad(1\le i\le g).
$$

Each nonlinear node has a syntactically globally affine anchor (a_i), and the anchor row vectors are independent, hence (r=g). /485's **static** full coset partition into (2^g) assignments to all anchors is correct, but it is not minimal among adaptive affine subcube covers.

Define the (g+1) disjoint exhaustive guards

$$
\Gamma_j=\{a_1,\ldots,a_{j-1},\neg a_j\}\ (1\le j\le g),\qquad
\Gamma_{g+1}=\{a_1,\ldots,a_g\}.
$$

On guard (Gamma_j), exactly

$$
w_i=z\quad(i<j),\qquad w_i=0\quad(i\ge j)
$$

for (j\le g). On (Gamma_{g+1}), all (w_i=z). This is immediate by induction through the AND cascade. Every named intermediate gate, not merely the final exported output, is affine in the ORIGINAL variables throughout each guard. Every original assignment meets exactly one guard, each guard has models, and the leaf counts are (2^{g-j+1}) for (j\le g), and two for (j=g+1).

**Theorem 487.1:** In the specified globally affine-anchor binary-gate subgrammar, the full static coset construction may use exponentially more affine regions than a legal adaptive partition:

$$
\underbrace{2^r}_{\text{full static anchor cosets}}=2^g,
\qquad
\underbrace{L_{\mathrm{adaptive}}}_{\text{constructed upper bound}}\le g+1.
$$

This is an **upper bound** on adaptive cells, not a proved optimum and not a contradiction of the exact static (2^r) coset count. It does not contradict LSPV-1/486's tight (2^g) affine-subspace cover for **independent** AND outputs: the cascade has nested shared dependencies. It also does not rely on LSPV-1/487's nonlinear validity regions, since every guard here is an ordinary affine subcube.

## Original-source authenticated, shared global Resolution guard clauses

In the DISTINCT facet-addressable DEF_AND+oriented-RES grammar, each paid definition (w_i=a_i\land w_{i-1}) owns exactly three explicit clauses:

$$
(\neg w_i\lor a_i),\qquad (\neg w_i\lor w_{i-1}),\qquad
(w_i\lor\neg a_i\lor\neg w_{i-1}).
$$

Define global clauses (no discharged or hidden assumptions)

$$
P_i=(w_i\lor\neg z\lor\neg a_1\lor\cdots\lor\neg a_i),
\qquad N_i=(\neg w_i\lor z).
$$

(P_1,N_1) are original defining facets. For each (i\ge2), resolve (P_{i-1}) with the third (i)th facet on positive/negative (w_{i-1}) to obtain (P_i); resolve the second (i)th facet with (N_{i-1}) on the same pivot to obtain (N_i). This is a topologically ordered, source-facet-authenticated shared DAG containing exactly (g) paid DEF nodes, (2(g-1)) paid RES nodes and (3g) explicit facets, with **(3g-2) global paid nodes** under the declared unit-node convention. The full antecedent graph is shared between all later specializations and is charged once. A branch may apply (P_i) only after justifying its guard; it may use (N_i) globally. No SPLIT, DISCHARGE, WEAKEN or assumed clause-to-AND3 port is inserted into historical /341. The certificate is not a UNSAT refutation: it proves guarded gate properties.

## Verification and resource ledger

Two independently written implementations checked (g=2,\ldots,10). The locally executed JavaScript generator/verifier passed **114,963** checks, three hostile RES-polarity controls rejected; the exact code fetched back from GitHub was executed in an independent V8 isolate, reproducing PASS, 114,963 checks, three rejections. Independently authored Python checked **53,502** assertions and three hostile RES cases, exhaustive (2^{g+1}) assignments per (g), with strict original 3-CNF odd/even (K_4) Tseitin controls (16 clauses, 0/8 satisfying assignments); the K4 source is a separate regression control, NOT a claim that the cascade sources constitute a published hard 3SAT family. At (g=10): static 1,024 cosets, eleven adaptive guards, ten paid definitions, 18 paid Resolution inferences and 30 defining facets.

Ideal work: (3g-2) derived global nodes in the distinct declared unit-weight grammar, not a lower bound on any true proof minimum. Guard descriptions materialized explicitly occupy (\Theta(g^2\log g)) bits under numeric ID convention; the (P_i) width sum is (\Theta(g^2)), so full uncompressed certificate storage/output is at least quadratic in (g) even though paid node count is linear. Computing all (P_i,N_i) with full sorted arrays takes polynomial bit time, not unit machine time. Search/discovery is excluded only from the ideal minimum; actual algorithms pay source parsing, lookup/index/head reads, proof construction, failed trials, source hash, checks, serialization, verification, branch scheduling, cache/retrieval/recomputation and peak simultaneous memory. Local JS host `/usr/bin/time`: 0.07 s wall, 37,276 KiB maximum RSS; separate Python `tracemalloc` snapshot 13,592 bytes peak tracked allocations, 0.915 s wall, not whole-process peak or asymptotic TM bounds. Weighted critical-path depth of the two RES chains is at most (g-1) after DEF availability but real serial DEF chain depth is (g), so physical span and retention differ from node work. Any Route A transfer still requires its full (s'\le\max\{\rho,\eta,\lambda,\lambda s\}) accounting; NONE is claimed here.

## Established-hard-family and shortcut ledger

- Chvatal-Szemeredi 1988: independent proper random signed strict 3-CNF on (n) variables with linear density (e.g. (m=6n)); exponential **ordinary shared-DAG Resolution** size with high probability in that specified regime; binary encoded size (\Theta(n\log n)); not a bound on the full mixed calculus. Known RES, ER and affine shortcuts must be retained.
- Pang arXiv:2610.00837v2: random proper strict 3-CNF (F(n,3,8n)), (m=8n); exponential proof-size lower bounds in specified fixed syntactic Res(PC_r/F_p), including Res(XOR), with all shared DAGs counted; does NOT include arbitrary conservative DEF or unrestricted historical typed mixtures, so reverse simulation remains OPEN.
- Odd bridgeless cubic Tseitin: 4h strict 3-clauses, 3h/2 original variables; established exponential ordinary Resolution but exact linear (4h-1) mixed AND3/GF(2) proof in the original /341 declared rules. This is a mandatory shortcut/family-failure control.
- Cook Extended Resolution: auxiliary extensions may collapse apparently hard families. Do not preserve a purported lower bound by excluding a legal shortcut.

## Materiality, exact open transfer, and write safeguards

This result closes **only** the proposed inference that a rank-(g) anchor set forces (2^g) specialization cases in arbitrary adaptive circuits. The static /485 rank theorem is retained at its verified scope. Any attempt to derive a full [P2-C3] transfer lower bound must optimize not just static rank but adaptive context-dependent branching, globally shared guarded lemmas, paid gate/RES evidence, and the actual historically permitted types. No polynomial general Res(XOR) normalization or lower bound against every R_mix341 proof follows. Historical grammar [P2-D1], mixed normalization [P2-C3], all-rules superpolynomial [P2-B1], noncircular B3 [P2-B2] OPEN. Root main.tex was not rewritten without a full safe read. Existing two Route A/three Route B allocation and all historical weights/schedules untouched. **P versus NP OPEN.**

Artifact paths: `experiments/arc/lspv3_487_adaptive_anchor_guards.cjs` (GitHub blob `2c8c4677bda241563415eb46576d2d167ee317bb`); `results/raw/arc/2026-11-07_1824_LSPV3_ADAPTIVE_AFFINE_CASCADE487.json` (blob `c59cd6d8aeba94ee622b191615f83eb5144e677e`); independent Python verifier and complete output in downloadable reproducibility archive. The GitHub output was independently fetched and re-executed; no authoritative native /341 checker execution is claimed.

**References:** Chvatal V, Szemeredi E. Many hard examples for resolution. JACM 35(4), 1988. DOI 10.1145/48014.48016. Pang S. A Degree--Size Relation for Resolution over Polynomials. arXiv:2610.00837v2, 2026. Buss S, Das A, Knop A. Proof complexity of systems of decision trees and branching programs. arXiv:1910.08503. Kothari R, Racicot-Desloges D, Santha M. Separating decision tree complexity from subcube partition complexity. arXiv:1504.01339.
