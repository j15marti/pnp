# LSPV-4/445: pass-space tradeoff for Resolution-hard Tseitin 3-CNF products

**2026-11-06 10:31 PST | Route A primary | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## IDEA -> SEARCH -> ITERATE

Initial hypothesis: LSPV-2/448's exact read-once source-state obstruction persists under multiple complete sequential scans, even if branches share all known reasoning. Falsifiers: F1, the constructed formula is not exact 3-CNF or its label is not binary equality; F2, multiple communication rounds defeat the equality lower bound; F3, source reads, resets, buffers or head positions were uncharged; F4, the claimed obstruction also holds with random-access input or bounded-error randomization. F1-F3 are excluded in the restricted model. **F4 is a genuine failure of all-machine transfer**. Direct review of Claude ONETAPE-0001 shows stronger earlier sequential-input lower bounds, so this is a focused, tight multi-pass control, not a novel general SAT lower bound.

## Family / original encoding / published theorem / known shortcut

Fix growing connected cubic expander graphs $G_h$ meeting the ordinary shared-DAG Resolution lower-bound hypotheses of Urquhart (1987) and Ben-Sasson–Wigderson (2001), with $h$ vertices and $3h/2$ edges. Form $c=h^r$ disjoint copies. Charge distinguished vertices $v_0,v_1$ in copy $j$ with bits $a_j,b_j$, respectively, and all remaining vertices with zero. For the three incident edges $u<v<w$, put exactly four original proper width-three signed clauses

$$
C_{j,z,p,q}=\ell_p(x_u)\lor\ell_q(x_v)\lor\ell_{p\oplus q\oplus1\oplus\chi_{j,z}}(x_w),\quad (p,q)\in\{0,1\}^2,\quad
\ell_0(x)=x,\ \ell_1(x)=\neg x.
$$

Order source blocks: all $v_0$ bundles, all fixed zero-charge bundles, all $v_1$ bundles. The middle block is public but **must still be scanned** in the one-way model. There are $4ch$ clauses, $12ch$ signed occurrences, $3ch/2$ edge variables, and, at fixed-width identifiers $w=\lceil\log_2(3ch/2+1)\rceil$ plus one delimiter per clause, exact length

$$
N=4ch(3(w+1)+1)=\Theta(ch\log(ch)).
$$

For each connected component, the GF(2) vertex-edge incidence image equals its even-charge subspace, so

$$
\operatorname{SAT}(F_{h,c,a,b})\iff a=b.
$$

Every UNSAT member contains an odd-charge expander component and has ordinary Resolution refutation size $2^{\Omega(h)}$: distinct component variables offer no common pivot for ordinary Resolution and all odd charge assignments on a fixed connected graph are related by variable complementation. **This hardness is only against ordinary Resolution, NOT the full mixed R_mix341, ER, GF(2), or arbitrary SAT machines.** Source-authenticated GF(2) parity remains a mandatory easy shortcut.

## Theorem 445.1: exact p-pass information and time-space restriction

**Model:** deterministic read-only *one-way* original 3-CNF input, exactly $p\ge1$ complete forward scans, rewinds to source beginning only, no indexed jumps or uncharged auxiliary copies, and total retained writable state $S$ bits. Correct on every promised pair $(a,b)$ of fixed $h,c$. Then

$$
\boxed{(2p-1)(S+O(1))\ge c,\qquad T(S+1)=\Omega(Nc).}
$$

**Proof:** Alice simulates the $a$-dependent first block and publicly fixed middle; Bob the $b$-dependent suffix. Send the entire retained state Alice-to-Bob at the boundary of each pass and Bob-to-Alice on each reset. There are $p+(p-1)=2p-1$ messages, each of length $S+O(1)$. Bob's final label computes deterministic equality of two $c$-bit strings. The $2^c$ accepting diagonal pairs form a 1-fooling set, forcing at least $c$ communicated bits. Since the architecture physically reads $N$ bits for each complete scan, $T\ge pN$. Combining gives the claimed product. QED.

Choose $c=h^3$. Then $N=\Theta(h^4\log h)$ and

$$
\boxed{T(S+1)=\Omega(N^{7/4}/(\log N)^{3/4})}.
$$

This excludes simultaneous $T=O(N^{6/5+o(1)})$, $S=O(N^{1/2+o(1)})$ **within this sequential full-scan architecture only**, because $17/10<7/4$. It says nothing about the FLMV indexed-input random-access machine without an independently charged conversion.

## Theorem 445.2: explicit near-matching repair

Split the $c$ components into $p$ contiguous chunks of size at most $b=\lceil c/p\rceil$. On pass $i$, save only the $a_j$ values of chunk $i$ as their source facets stream by; compare these to the corresponding $b_j$ facets in the suffix; retain a mismatch flag across passes. Still read every other original clause. The exact operation count is $p\cdot4ch$ clause-record visits, $T=\Theta(pN)$ source-bit read time, $S\le\lceil c/p\rceil+O(\log N)$ logical writable bits. This meets the lower bound to within constants. The finite host-language code materializes data and is **not** an FLMV high-water-memory implementation.

## Independently executed hostile controls (COMPUTATIONAL)

Exhaustive source generation on K4, cube and Petersen, with $1\le c\le4$: **1,020** distinct original signed 3-CNF inputs (**90 SAT**, **930 UNSAT**), **3,756** pass-budget records, **1,011,296** original-clause visits, **11,276** producer grouped checks, and **173,923** independent Node assertions. Node independently rebuilt every graph, all clause signs, every original source SHA-256 digest, source bit lengths and scan outcomes, rejecting **1,020** deliberately corrupted source copies via separate exact-source comparison. A further published compact Node replay passes all 3,756 records and the same clause-visit total. Finite controls do not certify growing expander hardness; host runtimes are not machine lower bounds.

**Indexed shortcut:** when charge facets are authenticated and locations are publicly known, compare corresponding $a_j,b_j$ with indexed reads, $O(c\operatorname{polylog}N)$ time and $O(\log N)$ workspace. **Randomized shortcut:** evaluate $\sum_j(a_j-b_j)r^j\bmod q$ at random $r$ for $q>c^3$, using logarithmic space and error probability at most $(c-1)/q$. Neither contradicts the exact deterministic streaming theorem; both defeat unrestricted interpretation.

## Full-resource boundary

The promise program does not construct children, call a guest, or search for policies; those phases are absent, **not free placeholders for Route A**. Source authentication for malformed and arbitrary CNF, failed discovery policies, child generation, parent/child buffers, indexed port reads, conversion, output, cache retention, replay and all-phase peak remain unproved for the demanded universal compiler. Preserve $s'\le\max(\rho,\eta,\lambda,\lambda s)$. The Route A target

$$
t'\le\max(11/10,3/5+t/2),\qquad s'\le\max(1/2,s/2)
$$

for **every** total uniform correct polynomial-time SAT decider on **all** binary inputs is OPEN. At $(6/5,1/2)$ the conditional FLMV numerical gap remains $1/90$; no compiler has been constructed. Route B's unrestricted mixed minimum and noncircular B3 are separate OPEN obligations.

## Authentic primary/project/repository checks

Read project LSPV-2/448 (blob ab28a0eb), /447 (e0180e70), LSPV-4/444 (1b1f477e), the Nov-2 governing handoff, issue #3, AGENTS.md, CODEX.md and the pnp-research skill; Grok GROKPROOF/2026-11-06_1617_PROGRESS.md (b931933c), Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6). Checked konard/p-vs-np scripts/proof_status.json (93b77ed3), blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea), INDEPENDENT_AUDIT.md (b30515cc), projection_discovery_barrier.py (3ea94ff), CNFgen tseitin.py (4bb5fd19), FRAT-XOR format.md (986a21aa), openai/math README (cc5b0a03). Primary literature: Urquhart JACM 1987; Ben-Sasson/Wigderson JACM 2001; FLMV JACM 2005; deterministic equality fooling set in University of Washington CSE 531 lecture 16; Guruswami/Onak CCC 2013. Web search index was used, no separate Google-branded query or native FLMV run. Root main.tex blob ab900e0e returned no readable characters and was not edited; no tasks/schedules, ownership, inference rules or weights changed.

**Advance:** tight p-pass original-source control and explicit matching algorithm. **Verification:** restricted proof and independent finite checks; independent mathematical peer review still pending. **OPEN:** all-input indexed same-machine FLMV transfer and Route B B3, P versus NP.
