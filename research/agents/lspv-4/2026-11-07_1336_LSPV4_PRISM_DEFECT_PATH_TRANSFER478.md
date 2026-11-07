# LSPV-4/478 | Original signed prism 3-CNF with adjacent exceptional packets: four-state transfer

**2026-11-07 13:36 PST | Resource auditor, Route A | PROVED/RESTRICTED symbolic theorem and COMPUTATIONAL finite controls | P versus NP OPEN**

**Exact proof-chain IDs:** material evidence [P2-A4]. Still OPEN: [P2-A2] and [P2-A5] for the all-input, same-FLMV recursively iterable contraction; [P1-01], [P1-03], [P1-04] for a complete SAT decider, correctness and physical resource bounds; separate Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2].

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis and predictions.** LSPV-4/477 supplies logarithmic-workspace parity-spectrum folding only for *independent* defective cubic-prism packets. LSPV-2/475 handles a forest of defective packets with an explicit $O(H2^c)$ retained syndrome DP. Hypothesis: for any **proper subset** of outer-cycle vertices modified to arbitrary four-clause signed proper ternary packets, keeping all inner-cycle packets ordinary XOR, their induced graph is disjoint paths and a four-state transfer can replace all retained defect tables. Predicted exact decision resources on the fixed-field source grammar: $T(N)=O(N\operatorname{polylog}N)$, $S(N)=O(\log N)$ on a declared indexed read-only-input machine, with all INDEX-coordinate and preprocessing storage charged.

**Four falsifiers declared before tests:** F1: independently combining the $P_v$ of adjacent defects could assign contradictory values to their shared original edge. F2: four-state propagation could allow inconsistent predecessor-successor values or omit a clause. F3: matching total boundary XOR could fail to extend through the connected intact subgraph. F4: complete strict signed-3CNF authentication or defect-run location would force $\Omega(H)$ *high-water writable* space despite the fixed-field positional grammar.

**Actual project continuity and source checks.** Read complete proof1.txt and proof2.txt, current coordination issue #3 and peer reports including LSPV-2/474, /475, /476, LSPV-4/477, LSPV-1/486, LSPV-3/482; governing handoff research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md at blob c3889a3e514ddbd747150dcb68607013a3b2d154; AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md; GROKPROOF/2026-11-07_1330_PROGRESS.md at blob 35ad4749b1d9779eadce95e46145b4eb103b8224; actual Claude assessment research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex at blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a. Previous work establishes the parity-extension lemma; the present statement is a more general *restricted algorithmic upper-bound control*, not a new SAT lower bound.

**Primary literature inspected by public web search:** Ben-Sasson and Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, JACM 2001, ECCC original https://eccc.weizmann.ac.il/eccc-reports/1999/TR99-022/ ; Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 2005, DOI https://doi.org/10.1145/1101821.1101822 ; Cattell, Dinneen, Fellows, *A Simple Linear-Time Algorithm for Finding Path-Decompositions of Small Width*, https://arxiv.org/abs/math/9410211 ; Reingold, *Undirected Connectivity in Log-Space*, JACM 2008, DOI https://doi.org/10.1145/1391289.1391291 . The present finite-state DP is consistent with established bounded-pathwidth methods. No native-FLMV executable and no separately branded Google search interface were available.

**Actual external repository files inspected:** konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 (explicitly finite-machine P subset NP, not full P=NP); blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and REVIEW_ADDENDUM.md blob 6a7cc2f8962d3fcfcfc1778b1d3d8f5dc8d56d70 (bounded and relaxation approaches); MassimoLauria/cnfgen cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (ordinary parity constructor); meelgroup/frat-xor README.md blob 38a137bca4d4ab6443703d4c31fba5783021c581 (external XLRUP certificate checker, not historical R_mix341); openai/math README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae (mixed verification levels, not an all-SAT theorem). These are evidence and shortcut sources, not authorities for solving P versus NP.

**ITERATE:** The first local-parity-only generalization is FALSE with adjacent defects. Two nonparity packets can separately allow both parities yet force the *same shared edge* to 0 versus 1. Repair: propagate the exact incoming edge bit jointly with the cumulative boundary XOR through each defective path. Independent centroid recursion and a different rooted-forest DP verify the corrected invariant on original strict signed 3-CNF.

## Exact original 3-CNF source and published hardness-control ledger

For $m\ge6$, take the cubic prism $G_m$ with outer vertices $u_i$, inner vertices $w_i$, outer edges $e_i=(u_i,u_{i+1})$, inner edges $f_i=(w_i,w_{i+1})$, and spokes $s_i=(u_i,w_i)$; indices are modulo $m$. There are $H=2m$ vertices, $3m$ original edge variables, and $2m$ packets of four **actual proper signed three-literal clauses**, hence $8m$ clauses. The three ordered edge IDs at each packet are its incident originals. Each signed clause forbids exactly one local three-bit assignment.

All $w_i$ packets must encode an ordinary XOR constraint. Let $D\subsetneq\{u_0,\ldots,u_{m-1}\}$ be exactly the set of *nonparity* outer packets. The members of $D$ may forbid any four triples, allowing repeats. All remaining outer packets must encode ordinary XOR. Since $D$ is a proper subset, its induced outer-cycle graph is a vertex-disjoint union of paths, possibly a path of length $m-1$; the intact graph contains the whole inner cycle and is connected.

A canonical source uses header $1^\ell 0 \operatorname{bin}_\ell(m)$, $\ell=\operatorname{bitlength}(m)$, followed by 24$m$ literal records of sign bit and $W=\operatorname{bitlength}(3m)$ variable-ID bits in canonical packet/slot order. Exact bit length:
$$
N=2\ell+1+24m(W+1)=\Theta(m\log m).
$$
The recognizer checks binary alphabet, dimensions, every literal ID and position, proper clause supports, all inner parity codebooks and $D\ne$ full outer cycle. Invalid encodings return MALFORMED or OUTSIDE, **never UNSAT by default**. No arbitrary-CNF fallback is part of this specialized algorithm.

**Established hardness family (distinct control):** odd-charge Tseitin contradictions on a growing cubic edge-expander, encoded directly with four proper signed ternary clauses per vertex, have $2^{\Omega(H)}$ *ordinary shared-DAG Resolution* refutation size under the Ben-Sasson–Wigderson theorem. Gaussian elimination handles the parity system efficiently. No expander hardness is asserted for this prism, for all algorithms, or for the fixed R_mix341. Equivalence of decision problems is not proof-size lower-bound preservation.

## Theorem 478.1: exact four-state transfer (PROVED/RESTRICTED)

For every normal packet $v\notin D$, authenticate the unique parity charge $b_v\in\{0,1\}$. Let
$$
q=\bigoplus_{v\notin D} b_v.
$$
For a maximal defective path $R=(u_a,\ldots,u_b)$ define its boundary parity $p_R$ as the XOR of *exactly* the two endpoint outer edges $e_{a-1},e_b$ and all spokes $s_i$ with $u_i\in R$. Let $P_R\subseteq\{0,1\}$ be the attainable set.

Initialize $S=\{(0,0),(1,1)\}$ where the first bit is the incoming outer-edge value and the second bit is its contribution to the cumulative boundary parity. At each defective vertex use only its permitted original-clause triples $(l,r,s)$ and update
$$
(l,p)\ \longmapsto\ (r,p\oplus s).
$$
At the last vertex set
$$
P_R=\{p\oplus r:(r,p)\in S_{\mathrm{final}}\}.
$$
The transition enforces the shared original edge exactly, not merely a parity summary. At most four $(r,p)$ states exist. Combine disjoint runs by XOR convolution $P=\bigoplus_R P_R$ (empty product $\{0\}$).

Then
$$
\boxed{F_{G_m}\text{ SAT}\iff q\in P.}
$$

**Proof.** Every satisfying original assignment traces permitted local triples and consistent incident edges, hence yields $p_R\in P_R$. Summing all ordinary XOR equations cancels intact-intact edges twice, leaving XOR of all defect-intact edges. Therefore $q=\bigoplus_R p_R$, so $q\in P$. Conversely choose a witnessing transfer trajectory for each run whose boundary parities XOR to $q$. Runs are disjoint so there is no cross-run defect-edge collision; every defective original clause is satisfied. On the connected intact subgraph, subtract the fixed defect-intact boundary contributions from vertex charges. The resulting parity vector has even total sum and lies in the image of its GF(2) incidence matrix. Set nontree intact edges to zero and solve the tree equations from leaves to root. This extends all chosen defective triples to an assignment satisfying every original packet. QED.

**Necessary scope control:** Without the independent-defect hypothesis of LSPV-4/477, the vertexwise shortcut $q\in\bigoplus_{v\in D}P_v$ is FALSE. Two consecutive defective vertices can each permit only tuples forcing their common $e_0$ to opposite bits. Each separately admits *both* XOR parities, but the conjunction is UNSAT. The corrected four-state transfer produces an empty run spectrum.

## Theorem 478.2: direct decision resources on the declared indexed source model

On a fixed deterministic indexed read-only-input model with charged source INDEX contents, head coordinates, fixed-field address arithmetic, source record parsing and high-water WORK positions, the **promised source-recognition and decision routine** has
$$
T(N)=O(N\operatorname{polylog}N),\qquad S(N)=O(\log N).
$$
The verifier scans every one of the $24m$ fields and computes $q$ using counters and constant-size packet masks. For each defective run it rereads only the current packet, propagates the four-state bitset, and folds its terminal two-bit spectrum into a global two-bit parity set. Run-start detection is a constant number of indexed packet lookups per outer vertex. Each packet is processed $O(1)$ times. All addresses are $\le N$ and require $O(\log N)$ INDEX/WORK bits; bit arithmetic and source read/index operations cost $\operatorname{polylog}N$ per field. The entire SOURCE scan, corrupt-input rejection, source/head/index operations, and one-bit decision output are included in peak and time. No large helper buffer, guest WORK emulator, precomputed clause directory, retained per-vertex messages, cache, source bit oracle, or uncharged search policy is invoked.

**Scope qualification:** This is an algorithmic existence proof for the declared indexed source model, not a native instruction-by-instruction execution of FLMV's machine or a transformation for arbitrary signed CNF. Source/OUTPUT exclusion follows the declared model; active INDEX contents and all work-tape addresses are charged. A full satisfying-edge assignment can be reconstructed with deterministic replay of suffix feasibility instead of retaining $\Theta(m)$ decisions, at additional polynomial time. That witness-output schedule is not included in the near-linear decision bound and was not natively executed.

An implementation that *actually materializes* one persistent message record for each of the $\Theta(m)$ exceptional vertices uses $\Omega(m)$ retained records. This does not lower-bound any alternative solver: the four-state streaming realization is an explicit counterexample to a claim that the original forest DP table is unavoidable.

## Finite evidence and hostile controls

Reproducible host program: experiments/arc/lspv4_478_path_transfer.py. Raw JSON: results/raw/arc/2026-11-07_1336_LSPV4_478_PATH_TRANSFER_RAW.json. Seed 47820261107, five prism sizes $m=6,9,12,24,96$, four source types each (split runs, length-$m-1$ run, alternating paired runs, and forcibly inconsistent adjacent packets). Generated original signed literal records, serialized exact fixed-field binary source, independently parsed and authenticated, and compared the four-state transfer against a separate rooted-forest DP in **all 20 cases**; for 12 cases independently recomputed centroid subproblems; for all four $m=6$ sources enumerated all $2^{18}$ complete original-variable assignments (model counts 72, 66, 64 and 0). Four malformed-source controls were rejected. Totals: **20 source cases, 15 SAT/5 UNSAT, 69 positive assertion groups, four corrupt controls, 427 centroid recursive calls, zero mismatches**. The host code uses materialized Python objects for its oracle; the claimed logarithmic-space schedule is the *symbolic four-state implementation*, not a measurement of Python memory or native FLMV instructions.

Python script SHA-256 (local verified): a1e4830fd5d6deb778a06cf8b3b93c3f711e763a4dc8f5fee5d3ca0b84043c78.
Raw JSON SHA-256 (local verified): d41b3b51f5f99c099dd63ad4327204ce53d6146796296f3093dfe32879a44486.
No execution of the historical R_mix341 checker or theorem-prover certificate is asserted.

## Publication, relation to proof chains and remaining gap

Role report, raw data, executable and handoff are new immutable additive artifacts. Material restricted-evidence update applies only to [P2-A4]. P1-01/P1-03/P1-04, P2-A2/P2-A5 and B3 remain OPEN. No historical weights, proof system, five role IDs, schedules, timezone, or enabled state changed. Root main.tex should be updated only if full authenticated content and LSPV-4 ownership markers can be retrieved and preserved.

**Actual advance:** a four-state *adjacent-defect* extension of existing restricted parity shortcuts with exact original-3CNF scope, paid direct-decision resource accounting and a witness against naive cross-branch/local-spectrum reuse. It is NOT an all-input SAT contraction, not a P-vs-NP separation and not a bound against arbitrary algorithms.

**Remaining gap:** complete native FLMV guest INPUT/WORK/INDEX interpreter, simultaneous all-phase time/space and effective same-machine recursive contraction over every SAT/UNSAT/malformed input. Route B's full fixed mixed-calculus lower bound and noncircular B3 remain independent OPEN obligations. **P versus NP remains OPEN.**
