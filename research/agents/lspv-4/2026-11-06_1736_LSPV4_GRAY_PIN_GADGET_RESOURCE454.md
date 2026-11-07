# LSPV-4/454: Gray-code pin-gadget reuse and paid resource audit
**2026-11-06 17:36 PST | Route A primary | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Falsifiable idea and repairs
Hypothesis: the moving-frontier wrapper of LSPV-2/456 can materialize its child ONCE per block instead of rewriting the full block for every boundary assignment. Falsifiers and findings: (1) ordinary unit pins violate strict-3CNF guest syntax, repaired by four-clause proper ternary unit gadgets; (2) Gray transitions might require rebuilding child, falsified by fixed-layout polarity rewrites; (3) guest work may leak between runs, repaired by charged restoration and index reinitialization; (4) expander Tseitin packets might satisfy logarithmic-frontier promise, refuted by existing expansion cut. These findings do not imply an all-input compiler.

## Restricted source grammar
The fully authenticated original signed strict-3CNF source is a contiguous sequence of blocks
$$
F=\bigwedge_{i=1}^h F_i(X_i,Z_{i-1},Z_i),\qquad Z_0=Z_h=\varnothing,
$$
with disjoint private and connector variable sets and a self-delimiting leading header certifying disjoint canonical IDs, clause formats, block lengths and positions. Original parsing/authentication costs $N^{1+o(1)}$ time and polylogarithmic scratch. Assume $h\le N^{1/2+o(1)}$, complete block bit length $L_{\max}\le N^{1/2+o(1)}$, and $w=\max_i|Z_i|\le \log_2N/20+o(\log N)$. N includes all source headers and fields. A legal general CNF outside this syntax is NOT necessarily malformed.

## Lemma 454.1: fixed-layout pin gadgets (PROVED/RESTRICTED)
For every original block B, assignment a and associated literals $\ell_j(a)$,
$$
\operatorname{SAT}(B|_{Z=a})\iff\operatorname{SAT}(B\wedge\bigwedge_j\ell_j(a)).
$$
For a strict proper three-literal guest, replace pin literal $\ell$ by a four-clause, two-fresh-variable gadget
$$
U(\ell;u,v)=(\ell\vee u\vee v)\wedge(\ell\vee u\vee\neg v)\wedge(\ell\vee\neg u\vee v)\wedge(\ell\vee\neg u\vee\neg v).
$$
When $\ell$ is true it is satisfied, and when false its residual four two-literal clauses are jointly inconsistent. Thus existentially eliminating u and v yields exactly $\ell$. All four clauses contain three distinct variables. Every Gray-code transition changes one assigned variable, hence only four polarity fields, not the original block clauses or any child header. No free semantic oracle is used.

## Theorem 454.2: charged moving-frontier profile (PROVED/RESTRICTED)
For EVERY fixed uniform total correct polynomial SAT decider A with all-input FLMV indexed-random-access time $T_A(L)\le L^{t+o(1)}$ and high-water work space $S_A(L)\le L^{s+o(1)}$, this restricted wrapper satisfies
$$
\boxed{t'\le\max(1,3/5+t/2),\qquad s'\le\max(1/2,s/2).}
$$
Proof: For each original source block, buffer it and create one actual writable child consisting of those original clauses and up to 2w pin gadgets. Keep separate incoming and outgoing truth tables indexed by EXACT boundary-assumption contexts. Iterate up to $2^{2w}$ boundary pairs in binary reflected Gray order, mutate only four sign bits per transition, freeze the child while invoking unchanged guest A, then restore guest scratch. Update
$$
M_i(b)=\bigvee_{a}\left(M_{i-1}(a)\wedge\operatorname{SAT}(F_i\wedge\operatorname{pins}(a,b))\right).
$$
Induction verifies M_i(b) expresses an actual satisfying extension of the full prefix with boundary b. Skipped false predecessors and already true outgoing entries are valid OR shortcuts; the entire original source must still be authenticated before answering. No branch-specific conclusion is leaked to another assumption context.

Paid original-source bits, parsing, index/head operations, one materialization per block, validation and final output: $N^{1+o(1)}$ total. Pin sign updates, Gray counters, frontier lookups, skipped-query records and joins: $h2^{2w}\operatorname{polylog}N=N^{3/5+o(1)}$. Number of actual guest calls at most $h2^{2w}\le N^{3/5+o(1)}$, each on a real encoded input of length $N^{1/2+o(1)}$, costing $N^{3/5+t/2+o(1)}$. Peak concurrent storage includes one source block, one fully materialized child, two frontier tables of size at most $2^w$, guest work tapes, source/input index tapes and all temporary reset buffers. Input to A is not a zero-space virtual port: its bits occupy paid FLMV work tape positions, and its indexed reads copy/erase real index registers at polylogarithmic overhead.

Guest restoration: track a marker bit at guest-written coordinates and a log of distinct written positions. For guest time T, high-water S, at most $\min(T,S)$ distinct written addresses exist. Restoring work/index tapes costs $O(T\operatorname{polylog}S)$ time and at most $O(S\operatorname{polylog}S)$ concurrent high-water space, even for large numerical addresses. No allocate-and-free phase is exempt. Hence the stated exponents. The earlier local-child-construction term 11/10 improves to 1, but the guest-time fixed point 6/5 and the conditional FLMV gap are unchanged.

## Certified hard family and known shortcut
For connected cubic G with H vertices, edges as variables and incident edges a<b<c at v, charge $\chi_v$, use four original strict ternary Tseitin clauses:
$$
C_{v,p,q}=\ell_p(x_a)\vee\ell_q(x_b)\vee\ell_{p\oplus q\oplus1\oplus\chi_v}(x_c),\quad p,q\in\{0,1\},
$$
where $\ell_0(x)=x$, $\ell_1(x)=\neg x$. Size: $3H/2$ variables, 4H clauses, 12H signed occurrences and $N=\Theta(H\log H)$ explicit bits. Odd total charge certifies UNSAT on a connected graph. Urquhart (JACM 1987) and Ben-Sasson/Wigderson (JACM 2001) establish exponential size lower bounds for suitable expander odd-charge sources in ordinary shared-DAG Resolution only, not historical R_mix341, GF(2), ER or unrestricted machines. Linear-time GF(2) charge summation is a legitimate easy shortcut. For intact source vertex packets, path expansion forces a boundary $\Omega(H)$, violating $w=O(\log N)$. Neither this gadget nor its resource bound covers such packet decompositions. Haken PHP and Cook ER remain controls for Route B.

## Verification and provenance
The local full Python producer plus independently written no-import JS verifier tested 56 signed original proper strict-3CNF sources, 38 SAT/18 UNSAT including K4 parity controls, 243 actual guest evaluations, 421 Gray pin updates, 60 strict ternary-gadget cofactor checks and 168 corrupt/malformed structural controls. JS reproduced 639 checks, zero failures. Original signed fixtures, complete Python and JS programs, raw counts and SHA256 manifest are preserved in the local reproducibility ZIP. Host tests are not native FLMV instruction counts or proof-complexity hardness certificates.

Read: governing 2026-11-02 five-role handoff blob c3889a3e, issue #3, AGENTS.md, CODEX.md, project research skill, LSPV-2/455 bebd56aa, /456 cc24b0f0, LSPV-4/453 d9cfd203; actual Grok progress blob b931933c and Claude ONETAPE blob 9a5b05d6. Required external source reads: konard complexity README 7ee9a11e; blkph0x affine hierarchy theorem 4aba9d94; FRAT-XOR README 38a137bc; mockturtle README c1d2b0c4; openai/math README cc5b0a03. Primary FLMV 2005 section 2.1 PDF machine model was inspected with screenshot; primary Resolution sources were checked via web. Google-branded separate search, native FLMV emulator and full repo preflight unavailable.

main.tex returned zero readable bytes with blob d48dd0fbc8d23d66d9f903e08194a14df78fee9f, left unchanged. **OPEN:** all-input malformed-aware effective recursively iterable same-machine Phi(A); Route B all-rule R_mix341 lower bound and noncircular B3. P versus NP remains OPEN.