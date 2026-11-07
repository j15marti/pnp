# LSPV-4/453: one-source-scan block-major SAT separator compiler
**2026-11-06 16:36 PST | Route A primary | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Initial idea, falsifiers, evidence and revision
Hypothesis: the exact special-syntax compiler of LSPV-2/455 can read its original source **once**, instead of once per separator assignment, by evaluating blocks outermost and maintaining a separate one-bit status for each separator assignment. Four falsifiers were checked: (F1) the status array might exceed $N^{1/2}$ physical space; (F2) block buffering might cost parent-size space; (F3) a cached SAT label might leak between incompatible assumptions; (F4) early UNSAT pruning might skip validation of malformed source suffixes. The revised algorithm avoids all four on the explicit syntactic sublanguage, not on arbitrary CNF.

## Theorem 453.1 (PROVED/RESTRICTED)
Let the original signed CNF have the *authenticated syntactic form*
$$
F(Z,X_1,\ldots,X_h)=\bigwedge_{j=1}^hF_j(Z,X_j)
$$
with pairwise disjoint private $X_j$ and common $|Z|=k$. Suppose each source block, its delimiters, headers and IDs included, has $L_j\le N^{1/2+o(1)}$ bits; there are $h\le N^{1/2+o(1)}$ blocks; $k\le\frac1{10}\log_2N+o(\log N)$; and proper block syntax, source IDs, block counts and end marker are checkable in one scan using $O(\log N)$ additional registers. This is a **promise on already-structured original inputs**. A valid CNF outside it is not malformed.

For every fixed uniform total correct polynomial-time CNF-SAT decider $A$ with guest profile $T_A(L)\le L^{t+o(1)}$, $S_A(L)\le L^{s+o(1)}$ on the FLMV indexed random-access machine, a block-major wrapper decides both labels on this sublanguage with
$$
t'\le\max\left(\frac{11}{10},\frac35+\frac t2\right),\qquad
s'\le\max\left(\frac12,\frac s2\right).
$$
It reads the original input **once**, rather than at most $2^k$ times in the earlier assignment-major implementation. It does **not** establish an all-input transformation or its recursive iteration.

**Construction and correctness.** Initialize an array $B[a]=1$ for each $a\in\{0,1\}^k$. Read, authenticate and temporarily buffer the next complete block $F_j$. For each $a$ with $B[a]=1$, construct the actual ordinary cofactor $F_j|_{Z=a}$ on a **paid indexed work tape**, execute the unchanged guest $A$, and set $B[a]\leftarrow B[a]\land\mathrm{SAT}(F_j|_a)$. Clear guest and child scratch before moving to the next call, and discard the block buffer after all $a$ are checked. Even if all $B[a]$ become zero, continue **reading and validating the remaining original source**. At the end accept iff some $B[a]=1$. Induction establishes
$$
B_j[a]=\bigwedge_{i=1}^j\mathrm{SAT}(F_i|_{Z=a})
$$
for every $a$; the disjoint private variables imply the exact final OR/AND join. No cross-assumption reuse and no omitted AND obligation.

**Resource accounting.** Single initial source stream $O(N)$ bit reads and parser/index/head operations; block buffering $O(L_{\max})$; all child materialization and local checks $O(2^k\sum_j L_j\operatorname{polylog}N)=N^{11/10+o(1)}$; at most $q=h2^k=N^{3/5+o(1)}$ guest invocations, each length $L_j+O(\operatorname{polylog}N)$, total $N^{3/5+t/2+o(1)}$ guest time; joining $O(q)$ bit operations. The simultaneous *high-water* writable space, counting block buffer, one materialized child, guest work/index tapes, statuses, counters, head positions, and all transient buffers, is
$$
O(L_{\max}+2^k+L_{\max}^{s}+(\log N)^{O(1)})
=N^{\max(1/2,s/2)+o(1)}.
$$
No hidden free input port, guest simulation, preprocessing, output, caching or parallelism is used. This is a machine construction under the exact special syntax, **not** executed native FLMV tape traces. Distinct proof-DAG nodes and $R_{\mathrm{mix341}}$ certificate bits are 0 because this is a computation, not a native refutation.

## Established-family ledger / hard control
For a connected cubic graph $G$ on $H$ vertices, introduce Boolean edge variables and at each vertex charge $\chi_v$ the four original signed proper width-three Tseitin clauses
$$
C_{v,p,q}=\ell_p(x_a)\vee\ell_q(x_b)\vee\ell_{p\oplus q\oplus1\oplus\chi_v}(x_c),\quad p,q\in\{0,1\},
$$
where $a<b<c$ are its incident edge IDs, $\ell_0(x)=x$, $\ell_1(x)=\neg x$. This is already original 3-CNF: $4H$ clauses, $N=\Theta(H\log H)$ binary bits, odd charge parity certified UNSAT. Urquhart (JACM 1987) and Ben-Sasson/Wigderson (JACM 2001) give exponential *ordinary shared-DAG Resolution* lower bounds on suitable odd-charge bounded-degree expander sequences. No unrestricted-computation, ER, GF(2), or historical mixed-$R_{\mathrm{mix341}}$ lower bound follows. GF(2) parity is the cheap legal shortcut. LSPV-2/455 proves any intact vertex-packet separator with blocks of $\le H/2$ vertices in constant-edge-expanders has $k=\Omega(H)$, violating the compiler's $O(\log N)$ condition. This restricted method therefore fails to transfer to that established hard family by source-packet partition.

## Computational verification
Executable independent host programs generated **48 original signed block-structured strict 3-CNFs**, $k\in\{0,1,2,3\}$, 1 to 5 blocks, including deliberate 8-clause UNSAT cores. Entire-source brute force, assignment-major guest composition, and block-major guest composition agreed on all 48: **40 SAT / 8 UNSAT; 484 guest calls**. Python producer 294 assertions PASS; independently implemented Node.js verifier 298 assertions PASS; six malformed-source cases rejected. Illustrative fixed-width source encodings total 14,007 bits, compared with an **upper count** of 53,396 bits under one full read per separator assignment. The difference is an input-stream accounting control, not a native FLMV benchmark or arbitrary SAT lower bound. Deterministic seed: 202611061636.

## Sources / audit / publication
Read governing historical five-role handoff (blob c3889a3e), current issue #3, LSPV-2/455 (bebd56aa), LSPV-4/452 (f4329362), AGENTS.md, CODEX.md, pnp-research skill, actual Grok GROKPROOF/2026-10-27_0921_PROGRESS.md (e6076113), Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex, konard/p-vs-np/ISSUE_28_RESPONSE.md (ea457db2), blkph0x/p-vs-np-proof-research/AFFINE_RECOGNITION_LIMITS_REVIEW.md (4e87c1da), FRAT-XOR README (38a137bc), and primary FLMV 2005 Section 2.1 (author PDF and screenshot). Google-branded access and a locally mounted full repo preflight were unavailable; web literature search was performed. Root main.tex blob d8514a8f returned **zero** readable characters, so it was not edited.

**Actual advance:** one-source-scan/shared-status restricted compiler with explicit all-phase accounting. **Remaining gap OPEN:** derive universally valid A-dependent interfaces and recursive closure on arbitrary CNF including SAT, UNSAT and malformed inputs; no general $N^{1/2}$ guest length construction. Route B full historical mixed-calculus lower bound and noncircular B3 remain OPEN. **P versus NP remains OPEN.**
