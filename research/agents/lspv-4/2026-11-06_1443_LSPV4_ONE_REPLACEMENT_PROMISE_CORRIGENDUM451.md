# LSPV-4/451 | CORRIGENDUM: one-replacement authentication does NOT have a linear read-once space lower bound

**2026-11-06 14:43 PST | LSPV-4, Route A primary | PROVED/RESTRICTED plus COMPUTATIONAL | P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE

Theorem 444.1 (historical report \`2026-11-06_0936_LSPV4_UNORDERED_SOURCE_AUTHENTICATION_PASS_SPACE444.md\`, blob \`1b1f477ee092020037876151d719c0d75b88f267\`) claimed that a deterministic read-once stream recognizer needs $\Omega(m)$ bits to accept all permutations of $m=4H$ authenticated original cubic-Tseitin clauses while rejecting a source with **one** duplicated and **one** missing expected clause. This **is false as stated**.

Prespecified falsifiers: (F1) distinct valid IDs $a,b\in[m]$ with $a-b\equiv0\pmod m$; (F2) one-replacement corrupt source with same modular ID sum; (F3) the complement-suffix distinguishability proof produces exactly one missing and duplicate for *all* distinct half-set prefixes; (F4) local clause-to-facet decoding necessarily stores a full graph. F1/F2 are impossible under the trusted indexed-header assumption of /444; F3 is false; F4 is false for the declared accessible header, but untrusted-header validation still needs its own charge.

**Family/theorem/encoding ledger.** G is connected simple cubic, H vertices, 3H/2 Boolean edge variables. At each v, ordered incident edge IDs a<b<c and charge $\chi_v$ produce exactly four *original proper signed* 3-CNF clauses:

$$
C_{v,p,q}=\ell_p(x_a)\vee\ell_q(x_b)\vee\ell_{p\oplus q\oplus1\oplus\chi_v}(x_c),
\quad p,q\in\{0,1\},\ \ell_0(x)=x,\ \ell_1(x)=\neg x.
$$

This has $m=4H$ distinct clauses, $12H$ literals, and encoded length $N=\Theta(H\log H)$. Original signed clauses are locally mapped to authenticated IDs $1,\ldots,m$ using the same known indexed graph/charge header assumed in /444. The published Urquhart/Ben-Sasson-Wigderson exponential lower bounds concern suitable growing odd-charge expander Tseitin formulas in **ordinary shared-DAG Resolution**; they do NOT extend to ER, GF(2), full $R_{\mathrm{mix341}}$, or all SAT algorithms. Global charge parity is an efficient legitimate shortcut.

## Corrected theorem 451.1: tight $\Theta(\log m)$ single-swap promise complexity

**PROVED/RESTRICTED.** On exactly $m$ authenticated clause-ID records whose multiset is promised either a permutation of $[m]$ or a permutation with exactly one ID $a$ replaced by a *different* ID $b$, accept iff the count is $m$ and

$$
\sum_{i=1}^{m}j_i\equiv\frac{m(m+1)}2\pmod m.
$$

For any $a\ne b$ in $[m]$, $0<|b-a|<m$, so $b-a$ cannot vanish modulo $m$. The running residue, record counter, local facet-ID buffer, and source/index heads use $O(\log m)=O(\log N)$ bits. Given locally checkable trusted indexed clause headers, one scan and $O(N\operatorname{polylog}N)$ bit work suffice. This is a *promise verifier*, never a valid all-malformed-input replacement for /444's bucket verifier.

The asymptotically matching lower bound: let $k=m/2$, fix a $(k-1)$-element subset A of $[m]$, and consider $m-k+1=k+1$ canonical prefixes $A\cup\{a\}$. For any two such prefixes, appending the complement of the first creates a correct full permutation in one case, and **exactly one duplicate/one missing** in the other. Thus all $k+1$ post-prefix states differ and $S\ge\log_2(k+1)=\Omega(\log m)$. This proves a tight logarithmic promise-space characterization.

## Corrected theorem 451.2: full-corruption lower bound STILL holds

**PROVED/RESTRICTED (standard fooling set).** If the recognizer must reject **every** length-$m$ multiset that is not an exact permutation, including two or more replacements, then *every* pair of distinct $k$-subsets must induce different first-half states: append the complement of one. Consequently

$$
S_{\mathrm{all\ corruptions}}\ge\left\lceil\log_2{m\choose m/2}\right\rceil=\Omega(m)=\Omega(N/\log N).
$$

The original proof of /444.1 establishes THIS stronger negative-input scope, not its narrower one-replacement scope. **Downgrade /444.1 to FALSIFIED AS STATED; preserve its proof only under corrected all-corruptions quantification.** The separate multipass bucket algorithm and its $T=O(\lceil m/b\rceil N\operatorname{polylog}N), S\le2b+O(\log N)$ upper bounds are not falsified.

Counterexample to the overstrong prefix argument: with $m=16$, $S=\{1,4,9,10,11,12,13,14\}$ and $T=\{2,3,9,10,11,12,13,14\}$ have the same ID sum but differ in two entries. Prefix T plus complement S has **two** duplicates and **two** missing IDs; this is outside the exact-one-replacement promise. Explicit 2-replacement collision: replacing $\{2,3\}$ by $\{1,4\}$ preserves the sum. Even first two moments collide for $\{1,4,6,7\}$ versus $\{2,3,5,8\}$: each sum is 18 and each square sum is 102.

## Independent finite validation and machine resource ledger

The archived Python producer and independently written Node.js verifier both regenerated **actual signed original clauses** on K4, cube and Petersen for even/odd charges. Results: **36** legitimate permutation acceptances; **33,504** distinct one-replacement corruptions correctly rejected; **6** balanced double-replacement false accepts and **6** equal-first-two-moment four-replacement false accepts outside the promise; **12** signed/foreign corruptions rejected, plus wrong-length controls. Independent Node checker: **34,104 assertions passed**. Python random seed 202611061448. These are finite host-language checks, not native indexed-FLMV machine execution. Host lookup maps consume $\Omega(N)$ memory; the abstract $O(\log N)$ upper bound explicitly assumes the authenticated read-only indexed header of /444, whose facet decoder is recomputed on demand.

The parser uses **zero** proof-DAG inference nodes and zero certificate inference bits. One full source scan and index/head reads cost at least $\Omega(N)$ time; with local facet checks, $O(N\operatorname{polylog}N)$ time. Persistent residue/count and transient clause/index bits use $O(\log N)$ space for the one-replacement promise. No children, SAT guests, failed search policies, cached proof DAGs, or source-independent all-input correctness were established. The complete resource ledger for an actual universal compiler must separately charge header authentication, source parsing, guest execution, child generation/access, output, joins, cache, recomputation, references, and all simultaneous peak buffers.

## Source audit and literature

Read governing five-role handoff, issue #3 and recent LSPV-2/452-453 and LSPV-4/449-450, AGENTS.md/CODEX.md/repository skill, actual Grok REWIRE and Claude ONETAPE reports. Checked pinned \`konard/p-vs-np/DETAILED_SOLUTION_PLAN.md\` blob \`19450e38\`; \`blkph0x/p-vs-np-proof-research/AFFINE_BOUNDARY_DESIGN.md\` blob \`ed4f4a99\`; \`meelgroup/frat-xor/README.md\` blob \`38a137bc\`; \`openai/math/README.md\` blob \`cc5b0a03\`. All external methods are model-limited and do not resolve the missing FLMV contraction. Searched original FLMV (JACM 2005, DOI 10.1145/1101821.1101822), Resolution (Urquhart 1987), deterministic streaming and distinct-elements literature (Indyk/Woodruff FOCS 2003); no separately authenticated Google-branded engine or external build used. This basic checksum construction is not claimed as a new literature result.

## OPEN transfer and handoff

Correct the record without altering any historical manuscript. Route A still needs, for **every** uniform total correct polynomial SAT decider, an effective recursively iterable same-indexed-machine, both-label, malformed-aware all-input transformation with $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$, fully charging all phases. Neither corrected streaming bound proves nor refutes it. Route B's historical $R_{\mathrm{mix341}}$ full mixed minimum and noncircular B3 remain OPEN. Exactly two Route A and three Route B agents, unchanged identities/schedules/rules/weights. P versus NP OPEN.
