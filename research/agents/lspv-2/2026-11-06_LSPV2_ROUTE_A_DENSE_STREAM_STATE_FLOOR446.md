# LSPV-2/446: Dense original-source Tseitin edit streams have a retained-state floor

**November 6, 2026 (PST), Route A primary. PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE

**Hypothesis:** Can the correct epoch-tagged child port of LSPV-2/437 be used for a *parent-sized* shared Tseitin graph while retaining the required $N^{1/2+o(1)}$ FLMV writable-space bound? Three precise falsifiers: (F1) distinct dense toggle subsets may produce the same future point-query answers; (F2) a one-bit global parity summary may reconstruct every original-source literal; (F3) indexed jumps may make an $H$-bit stored state physically sublinear. All fail in the exact stream-and-forget point-query model. Re-readable edit lists and charge-parity SAT recognition remain valid escapes.

## Exact family and certified model

For a connected cubic graph $G$ with $H$ even vertices and $M=3H/2$ edge variables, each vertex $v$ of charge $\chi_v$ with incident edges $a_v<b_v<c_v$ contributes exactly four proper signed 3-CNF clauses:

$$
C_{v,p,q}(\chi)=\ell_p(x_{a_v})\lor\ell_q(x_{b_v})\lor\ell_{p\oplus q\oplus1\oplus\chi_v}(x_{c_v}),
\quad \ell_0(x)=x,\ \ell_1(x)=\neg x.
$$

The fixed /435 binary packet has an 8-bit magic, unary $H,M$, $M$ endpoint pairs of $w$ bits, $12H$ sign-plus-$w$-bit literal records, and a 2-bit trailer, $w=\lfloor\log_2 M\rfloor+1$. Thus

$$
N=8+(H+1)+(M+1)+2Mw+12H(w+1)+2=\Theta(H\log H).
$$

Suitable growing **odd-charge cubic expander** instances have exponential $2^{\Omega(H)}$ **ordinary shared-DAG Resolution** refutation-size lower bounds (Urquhart 1987, Ben-Sasson/Wigderson 2001). This does NOT establish hardness for full fixed $R_{\mathrm{mix341}}$, GF(2), Extended Resolution, or arbitrary SAT algorithms. The tested finite K4/cube/Petersen graphs are only semantic controls. Connected Tseitin SAT is characterized by $\bigoplus_v\chi_v=0$, giving a small-space algebraic shortcut.

## Theorem 446.1: exact point-query state lower bound (PROVED/RESTRICTED)

Fix the graph and base charge $b$. A deterministic transducer sees a length-$r$ stream of vertex toggle IDs, then must answer the exact bit

$$
\Delta_v=\bigoplus_{j=1}^{r}[u_j=v]
$$

for **every future adversarially selected** $v$. The stream cannot be reread and no copy survives outside charged state. The single stream head is parked at its fixed end position before a future index is given, and finite control is constant. If additional source-dependent indexed head positions are allowed, their $O(\log N)$ positional information is explicitly charged or subtracted, yielding $S\ge\log_2\binom Hr-O(\log N)$; for dense streams the same $\Omega(H)$ asymptotic floor survives. For each $r$-subset $S\subseteq[H]$ consider the stream listing its elements once in fixed order. These $\binom Hr$ streams have pairwise different future response vectors $\mathbf1_S$. If two ended in the same full available state, asking a vertex of their symmetric difference would force an incorrect identical response. Hence at least $\binom Hr$ distinct accessible states, requiring

$$
S\ge\left\lceil\log_2\binom Hr\right\rceil-O(1).
$$

For $r=H/2$, $\binom H{H/2}\ge2^H/(H+1)$, and

$$
S\ge H-\log_2(H+1)-O(1)=\Omega(H)=\Omega(N/\log N).
$$

This is an application of the elementary INDEX/set-membership state-counting theorem. It **does not apply** when the edit stream stays on read-only input, queries are known beforehand, or only the SAT label is requested. Its information floor also implies a physical high-water floor on a fixed-alphabet FLMV work-tape model; no all-algorithm SAT lower bound follows.

## Corollary: correct scale of /437's epoch port

The actual /437 epoch implementation uses $H(B+1)$ indexed work-tape bits, $B=\lceil\log_2(q+1)\rceil$. If the retained graph is parent scale, $H=\Theta(N/\log N)$, its space is $N^{1-o(1)}$ even for $q\ge1$ and $\Theta(N)$ for $q=N^{3/5+o(1)}$, incompatible with the desired $N^{1/2+o(1)}$ peak. This is NOT a contradiction of /437: that report **explicitly** assumes a small child graph, $H=O(L/\log L)$ with $L\le N^{1/2+o(1)}$, when claiming the port fits.

A read-only edit list may be rescanned using $O(\log(H+r))$ writable bits but costs $\Theta(r)$ ID probes **per uncached exact point query**, or $\Theta(rQ)$ for $Q$ such queries for that specific strategy. If $r=\Theta(N/\log N)$ and $Q=N^{1/5}$, the resulting $N^{6/5-o(1)}$ probe total misses the $N^{11/10}$ local-time target. Sorting, caching, succinct structures or algebraic summaries can avoid this specific query method but require charged acquisition and high-water accounting. For the authenticated connected Tseitin SAT label, one global bit $\bigoplus_vb_v\oplus(r\bmod2)$ suffices, so this theorem is explicitly **not SAT decision hardness**.

## Verification and controls (COMPUTATIONAL)

Independent Python producer and JavaScript parser checked **656 complete original signed 3-CNF packets** over K4, cube and Petersen, both base parity labels, and *every* $H/2$-subset of distinct toggles. Counts of pairwise distinguishable query profiles are respectively 6, 70, 252; exact information floors 3, 7, 8 bits; original source lengths 250, 608, 757 bits. 52,339 Python assertions and 326,859 independent Node assertions PASSED. Six Python and three Node malformed/corrupted controls were rejected. The standalone compact Node reproducer, run independently, passed 52,297 checks. All packets have SHA-256 bindings and exact local parity truth checks, with representative exhaustive SAT/UNSAT model enumeration. These are host-language controls, not native FLMV TM runs, native $R_{\mathrm{mix341}}$ certificates, or proof-size lower bounds.

Full raw cases, executed Python and independent Node scripts, the expanded 16KB proof report, handoff and SHA-256 manifest are in the conversation reproducibility archive. No arbitrary guest was actually invoked. The port and verification costs are reported separately from logical proof node work (zero native mixed inferences), source evidence bits, full guest execution, parsing, indexed-head reads and erasures, shared cache, output and peak writable space.

## Authenticated source and duplication audit

Governing Nov. 2 five-role handoff at commit \`4e29ed7646f484707767acb6e63ec5f38afd98a8\`, current \`j15marti/pnp#3\`, AGENTS.md, CODEX.md, research skill, LSPV-2/435 blob \`0366a09\`, /437 \`2033e9\`, /443 \`aedb2d\`, /444, local /445, actual Grok \`GROKPROOF/2026-11-06_0515_PROGRESS.md\` blob \`93f9202\` and Claude \`research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex\` blob \`b7150bb\` were inspected. Issue #3 peer LSPV-4/441 padding and LSPV-3/451 mixed certificate reports remain separate. Required external repositories were inspected: \`konard/p-vs-np/scripts/proof_status.json\` blob \`93b77ed\` (different one-tape formalization), \`blkph0x/p-vs-np-proof-research/METHOD_INDEX.md\` blob \`18d693\` and \`AFFINE_BOUNDARY_DESIGN.md\` blob \`ed4f4a99\` (compact affine alternative). Code: \`MassimoLauria/cnfgen/cnfgen/families/tseitin.py\` blob \`4bb5fd\` and \`openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean\` blob \`1ced21\` (fixed driver only). Web searches for FLMV, Tseitin resolution, INDEX streaming and initializable arrays were done; Google-branded search and full external corpus audit are not claimed. Original-source tests and theorem are reproducible; no novelty claim about the standard information-theoretic counting principle.

**Unchanged Route A OPEN obligation:** For **every** uniform total polynomial SAT decider $A$ with unknown time/space exponents, construct an effective, all-input, malformed-aware, both-label, recursively iterable *same-machine* transform $A\mapsto\Phi(A)$ with

$$
t'\le\max(11/10,3/5+t/2),\qquad s'\le\max(1/2,s/2).
$$

No new scheduler, agent, calculus, weights, or manuscript region was modified. Route B noncircular B3 and P versus NP remain OPEN.

**References:** Urquhart, JACM 1987; Ben-Sasson & Wigderson, JACM 2001, DOI 10.1145/375827.375835; Fortnow et al., JACM 2005, DOI 10.1145/1101821.1101822; Katoh & Goto, *In-Place Initializable Arrays* (2017), arXiv:1709.08900; Glinskih & Itsykson, MFCS 2017, DOI 10.4230/LIPIcs.MFCS.2017.26.