# LSPV-2/443: original-source Tseitin recognition has a deterministic streaming equality barrier

**2026-11-06 05:13 PST. Route A primary. PROVED/RESTRICTED and COMPUTATIONAL. P versus NP OPEN.**

## IDEA, prediction, falsifiers, corrections

Hypothesis: the source-only, unordered original signed strict 3-CNF Tseitin family recognizer of LSPV-2/442 cannot simultaneously use few complete sequential passes and sublinear retained state, even though the same family is decidable in deterministic logspace with indexed read-only input (potentially high polynomial time). Predictions: embed EQ_m(u,v) into exact membership with a $u$-only source prefix, a $v$-only suffix and a common source bit length $N=\Theta(m\log m)$. Four falsifiers: unequal inputs accidentally form a different legal cubic graph, source prefix depends on v, source length depends on u/v, or the fooling-set equality argument does not distinguish prefixes.

**Duplication check:** LSPV-2/438 already demonstrated an equality-style obstruction for a different artificial double-charge fixed-field annotation. This note's limited addition is an explicit equality embedding in the actual **unannotated original signed strict 3-CNF** of /442. LSPV-2/422 already proved compact GF(2) boundary messages; LSPV-4/438 proved literal-preserving giant-core persistence. None yield an arbitrary-machine SAT lower bound.

## Exact established family and certified hardness

For a simple cubic graph $G=(V,E)$, one variable $x_e$ per edge and charges $\chi_v\in\mathbb F_2$, define the four proper ternary clauses per vertex excluding assignments of incorrect parity:

$$
F_{G,\chi}=\bigwedge_{v\in V}\bigwedge_{a\in\{0,1\}^{E(v)}:\,\bigoplus a\ne\chi_v}
\left(\bigvee_{e\in E(v)}\ell_{e,a_e}\right),\quad
\ell_{e,0}=x_e,\quad \ell_{e,1}=\neg x_e.
$$

There are exactly $3H/2$ used edge variables and $4H$ source clauses on $H=|V|$ vertices; with polynomially bounded edge IDs the encoding occupies $\Theta(H\log H)$ bits. Every connected component is satisfiable iff its charges XOR to zero. Suitable **growing odd-charge cubic expanders**, not arbitrary finite cubic graphs, have $2^{\Omega(H)}$ size lower bounds in **ordinary unrestricted shared-DAG Resolution** (Urquhart 1987; Ben-Sasson and Wigderson 2001). This does not establish hardness in Extended Resolution, XOR reasoning, the full fixed historical mixed R_mix341 calculus, or all-machine SAT.

**Precise preservation direction:** If $F$ is such a hard UNSAT source and $Q$ is satisfiable on disjoint variables, any ordinary Resolution refutation of $F\land Q$ restricts under a satisfying assignment of $Q$ to a Resolution refutation of $F$ with no greater size. Consequently ResSize$(F\land Q)\ge$ResSize$(F)$. This is the ordinary-Resolution hard-family anchor when $Q$ is our SAT gadget. It is not a 3-CNF conversion, an equisatisfiability-only argument or a mixed-rule lower bound.

## Original-source equality encoding

For each $i<m$ take two copies of $K_4$. In the left copy replace edge $(0,1)$ by $(0,4),(4,1)$; in the right replace $(5,6)$ by $(5,9),(9,6)$; join the new vertices with bridge $(4,9)$. The resulting connected ten-vertex simple cubic graph has fifteen edges, exactly forty signed strict ternary original parity clauses, and all charges zero. All nonbridge edge variables have fixed globally unique IDs. Across the bridge only, use $B_{i,u_i}$ in the left vertex quartet and $B_{i,v_i}$ in the right vertex quartet, with distinct identifiers for the two bit values. Order all left-side quartets before all right-side quartets. An optional fixed K4 anchor or a growing certified hard expander source occupies the common prefix.

For the finite strict DIMACS implementation, edge rank $j$ has ID $10^d+100i+4j$ with bridge bit $u_i$ or $v_i$ appended as $+0$ or $+1$, where $d=|\mathrm{decimal}(100m+100)|+1$. The header declares a fixed variable bound $2\cdot10^d$, including unused IDs. All IDs have the same decimal width for fixed $m$. The packets are well-formed original proper signed 3-CNF with $40m$ gadget clauses, $\Theta(m\log m)$ total source bits, a $u$-only prefix, a $v$-only suffix, and fixed size independent of the parties' strings. In the theoretical hard-anchor construction take expander size $H=\Theta(m)$ and disjoint IDs, preserving $N=\Theta(m\log m)$.

**Theorem 443.1 (PROVED/RESTRICTED).** The complete original source belongs to the class of signed cubic Tseitin strict 3-CNFs recognized by /442 **if and only if** $u=v$. For equality, every edge variable occurs in precisely two distinct vertex-quartet supports, and the graph is cubic. When $u_i\ne v_i$ the two bridge IDs each occur in precisely one vertex quartet, violating exact edge ownership. Clause support uniquely fixes its quartet, so alternative grouping cannot repair the mismatch. Every unequal source is still a **valid general CNF OUTSIDE the recognized family**, not MALFORMED.

**Theorem 443.2 (PROVED/RESTRICTED).** For a deterministic one-way streaming recognizer that must distinguish FAMILY from OUTSIDE, all $2^m$ left prefixes require distinct memory configurations, hence at least $m$ retained bits. If prefixes of distinct $u,u'$ shared a state, choosing right suffix $v=u$ would force identical outputs for accepted $(u,u)$ and rejected $(u',u)$. For a deterministic $p$-complete-pass sequential streaming recognizer with at most $S$ bits at each input-boundary crossing, no indexed random access and no external uncharged memory, standard deterministic equality communication gives

$$
(2p-1)S\ge m,\qquad T\ge pN,\qquad
TS=\Omega(Nm)=\Omega(N^2/\log N).
$$

Therefore a streaming architecture with $S\le N^{1/2+o(1)}$ requires $T\ge N^{3/2-o(1)}$, which fails the target $N^{11/10+o(1)}$ **local streaming recognition** bound. The FLMV indexed-input machine is a different model, so this is **not an FLMV lower bound** or a no-go theorem for its solver-dependent contraction.

**Critical shortcut and falsifier:** All zero-charge gadgets are SAT under the all-zero edge assignment even when $u\ne v$. With a fixed even K4 anchor every complete packet is SAT, regardless of equality. With an odd K4 (or odd expander) anchor every packet is UNSAT, regardless of equality. Thus the test's SAT answer is easy for every string pair. There is no universal SAT decision lower bound here. GF(2) parity, source recognition, extension-variable reasoning, sharing and other permitted shortcuts remain upper-bound controls, not excluded to protect the bound.

## Independently executed finite controls

Python original-source producer and exact-group recognizer: **2728** packets across $m=1,\ldots,5$, both even/odd K4 anchors and all pairs $(u,v)$; **124 FAMILY**, **2604 valid OUTSIDE**, **1364 SAT all-zero controls**, **1364 odd-K4 UNSAT controls** verified by all 64 anchor edge assignments. All $2^m$ left prefixes were distinct, all packets of a fixed $m$ had identical byte length (1027,1887,2748,3608,4468). Three corrupted/malformed/outside controls were rejected. Python **5469 checks**, elapsed host wall time 6.3911 seconds. Independently written Node generator/reconstructor **132800 assertions**, including a matching cross-language SHA-256 source packet. These are host executions, not native FLMV transition measurements. Raw ledger SHA-256: **02018014eb203c40b8459b3d1fc2535144a7dd4fd859e59ae2d46afb123fa448**.

Explicit work phases include raw source production, full original clause parsing, quartet/multiplicity authentication, head/prefix and exact-length checks, independent reconstruction, six-variable exhaustive negative-anchor tests, positive assignments, corruption rejection, and output verification. They were charged in actual host program execution, but host dictionary/Map peak memory and Python/Node runtimes are NOT a same-machine FLMV proof. No native mixed-calculus proof nodes are claimed; the logical certificate is a standard deterministic equality fooling-set proof. For any actual SAT-decider upper bound, input reading, cache, storage, index-head erasure, construction, guest runs, recomputation, joining and fallback remain fully chargeable.

## Sources, audit and next proof arrow

Primary publications: Urquhart (1987), *Hard examples for resolution*, JACM 34(1), DOI 10.1145/7531.8928; Ben-Sasson/Wigderson (2001), *Short proofs are narrow*, JACM 48(2), DOI 10.1145/375827.375835; FLMV (2005), *Time-space lower bounds for satisfiability*, JACM 52, DOI 10.1145/1101821.1101822; Reingold (2008), *Undirected connectivity in log-space*, JACM 55(4), DOI 10.1145/1391289.1391291. The last gives polynomial time of unspecified exponent in log space, not the desired $\le N^{11/10}$ local work.

Actual repository reads: governing five-role handoff, current issue #3, AGENTS.md, CODEX.md, research skill; LSPV-2/440,/441,/442; LSPV-4/438; Grok GROKPROOF/2026-11-01_0414_GROK_PROGRESS.md (blob 8ada2df3); Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727); konard/p-vs-np/proofs/complexity/README.md (blob 7ee9a11e, distinct one-tape model); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (blob 18d693ea) and CERTIFIED_RESIDUAL_QUOTIENT_REPORT.md (blob b37da20a, incomplete equivalence recognizer); meelgroup/frat-xor/format.md (blob 986a21aa, different rules). Current 2026-11-06_0920 Grok file path was not located; no claim of review. MassimoLauria/cnfgen/README.md returned 404 through connector. Google-branded search unavailable; indexed web and connected GitHub were used.

**Next gap:** an every-input, malformed-aware, recursively iterable and fully charged *solver-dependent indexed-machine* transformation $A\mapsto\Phi(A)$ with $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$ remains OPEN. The present theorem falsifies a weaker sequential-pass recognizer design only. Fixed historical R_mix341 rules, weights, five roles, and schedule untouched; root main.tex not modified because its SHA was returned with zero readable content. All-rule mixed $\overline W_R$, noncircular B3 and P versus NP remain OPEN.

### Additional OpenAI GitHub source inspection (same run)

Searched github.com/openai for the exact node-cost name and fetched **openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean**, Git blob **1ced21f44ad49370d1b812e862c03c3a91d7f836**. The file's named theorem **command_eval** explicitly composes a setup program's evaluation with a width driver's concrete visit log and bounds the *same execution's* number of steps; theorem **program_runs** carries final storage and computed counter words. Its header explicitly disclaims a uniform cost for arbitrary callbacks or unbounded state. It concerns its declared bit-program/width-driver model, **not** a proof of our arbitrary-decider SAT child-generation or original-source membership costs. No all-input FLMV contraction is imported. This inspection was completed after the initial report publication, and this source-audit addendum was appended under the existing role-owned path with current-blob-safe readback.
