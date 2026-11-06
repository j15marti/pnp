# LSPV-4/433: Raw portfolio input-size normalization

**November 5, 2026, 23:41 PST. Route A PRIMARY. PROVED/RESTRICTED + COMPUTATIONAL. All-input FLMV contraction and P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE and four falsifiers

Hypothesis: the direct-product bit-read theorem from LSPV-4/432 is correct **for independently supplied full formulas**, but its comparison with the proposed FLMV local-time budget uses the size of one formula, rather than the size of the *actual supplied tuple*. F1: pivotal sign bits overlap; F2: $q$ complete $n$-bit inputs can be supplied on only $n$ input bits; F3: one $P$-bit parent encodes every independent $qH>P$ exact source family; F4: the query lower bound is superlinear in actual input length. Results: F1 false for the declared grammar, F2 and F3 impossible by counting, F4 false. **Do not withdraw the valid restricted $qH$ theorem; withdraw only the cross-baseline inference.**

## Exact established 3-CNF family and theorem ledger

For a connected simple cubic graph $G$ with $H$ vertices and $3H/2$ edges, use one Boolean variable per edge. With sorted incident edges $a_v<b_v<c_v$ and $\ell_0(x)=x$, $\ell_1(x)=\neg x$, use four clauses at each vertex:

$$
C_{v,p,r}(\chi)=\ell_p(x_{a_v})\lor\ell_r(x_{b_v})\lor
\ell_{p\oplus r\oplus1\oplus\chi_v}(x_{c_v}),
\quad (p,r)\in\{0,1\}^2.
$$

The formula is SAT iff $\bigoplus_v\chi_v=0$ by incidence-matrix rank $H-1$. Thus odd-charge UNSAT is mathematically certified and even-charge SAT has witnesses. $4H$ clauses, $3H/2$ variables. The test encoding uses eight-bit magic 10100111, unary $H$ and $M=3H/2$, $2Mw$ endpoint bits, twelve signed variable IDs per vertex, end marker 00, where $w=\max(1,\operatorname{bitlength}(M))$. Exact length:

$$
n_H=8+(H+1)+(M+1)+2Mw+12H(w+1)+2=\Theta(H\log H).
$$

Changing a charge flips four *disjoint* sign positions $D_v$ and changes the SAT label. For expanding cubic graph sequences under the published expansion hypotheses, Urquhart (1987) and Ben-Sasson/Wigderson (2001) establish $2^{\Omega(H)}$ **ordinary shared-DAG Resolution** refutation-size lower bounds. The present K4/cube/Petersen instances are not a growing certified hard family. The algebraic AND3/GF(2) shortcut is an obligatory upper control. No lower-bound transfer to mixed $R_{\mathrm{mix341}}$ or arbitrary SAT algorithms is inferred.

## Theorem 433.1: Normalize to actual input bits (PROVED/RESTRICTED)

For $q$ independent, complete canonical Tseitin sources each of length $n_H$, the raw tuple input has length $B=q n_H$ without framing and $B=\Theta(q n_H)$ with polynomially bounded framing. The unchanged adversary proves at least one read from every $D_v$ in every raw block, hence at least $qH$ reads. However,

$$
qH=\Theta\left(\frac{B}{\log H}\right)\le B.
$$

This is a near-linear query lower bound **in the actual input length**, not a superlinear input-query lower bound. In LSPV-4/432 the specialization $q=n_H^{3/5}$ yields $qH=n_H^{8/5-o(1)}$ *but also* an input of $B=n_H^{8/5+o(1)}$ bits. Comparing its raw-input cost to an $n_H^{11/10}$ local-work budget assumes a different, smaller original input and does not provide an FLMV obstruction.

A matching $O(qH)$ bit-probe *promised-template* decision algorithm reads one designated third-literal sign per vertex, XORs inferred charges, and emits $q$ labels. Original-source authentication, indexed address operations, and machine-time overhead require separate charges. This query argument does not imply a small-space general-CNF algorithm.

## Theorem 433.2: Exact-parent injection bound (PROVED/RESTRICTED)

Suppose a deterministic $P$-bit parent representation can generate **every** possible independent $q$-tuple of $H$-bit charge vectors, with exact bit-for-bit child source access. Different charge tuples generate different source tuples, so injectivity yields

$$
\boxed{P\ge qH}.
$$

For variable-length parent encodings of length $\le P$, the counting bound is $2^{P+1}-1\ge2^{qH}$. This does **not** constrain label-only compression, correlated children, or a chosen restricted source family. It is not a SAT computational lower bound.

For the proposed parent length $P$, child count $q=P^{3/5+o(1)}$, and child length $L=P^{1/2+o(1)}$, cubic Tseitin children have $H=\Theta(L/\log L)$. Therefore:

$$
qH=P^{11/10-o(1)},\qquad qL=P^{11/10+o(1)}.
$$

The $qH$ bound never exceeds the already budgeted $qL$ work to read/materialize *all explicit children*. But $qH>P$ eventually, so a $P$-bit parent **cannot encode every independent complete child charge portfolio**. In a genuine virtual-child compiler, descendants are correlated; independent-source lower bounds cannot be imported without an explicit source-model simulation.

## Same-machine resource ledger and FLMV status

Hypothetical $q$ guest calls on length-$L$ children contribute $qL^t=P^{3/5+t/2+o(1)}$ time. Constructing all child strings explicitly costs $qL=P^{11/10+o(1)}$ output/reading work. Eager writable materialization costs at least $L$ workspace for one child and potentially $qL$ for retained siblings; lazy ports avoid this only if source authentication, child-bit access, guest index/head traffic, counters, caches, failed policies, retrieval/recomputation, and **highest physical visited work/index-tape coordinates** are fully bounded. Logical shared-DAG inference-node work is different from serialized execution and actual storage/replay costs.

FLMV JACM 2005 Section 2.1 (original PDF page 4 visually inspected) defines indexed read-only input and erased index tapes, and workspace using maximal visited work-tape coordinates. The conditional arithmetic is $\beta(6/5)=23/45$, $\beta(6/5)-1/2=1/90$. No all-input same-machine contraction was constructed. Root historical $R_{\mathrm{mix341}}$ grammar and weights, branching AND/OR, assumption scopes, B1/B2/B3, and existing five-role allocation are unchanged.

## Verification, literature, prior-work comparison

**COMPUTATIONAL** independently executed: 66,457 Python assertions and 17,646 separately implemented Node checks on 16 K4, 256 cube, and 1,024 Petersen charge vectors, source-bit injection, full K4/cube edge-assignment SAT/UNSAT controls, malformed magic, source truncation, corrupt one-of-four signs, and exact-integer $P,q,L,H,B$ examples. These are not physical FLMV timings. A complete reproducibility archive with both original executables, all raw results, code and SHA-256 manifest is provided separately.

Authenticated state reads: five-role governing handoff at commit 4e29ed7646f484707767acb6e63ec5f38afd98a8, issue #3 with recent LSPV-2/436, root AGENTS.md (19656af), CODEX.md (754999f), .codex/skills/pnp-research/SKILL.md (b8df83a), LSPV-4/432 (208e9bd), LSPV-2/436 (709bd0b), Grok GROKPROOF/2026-11-06_0515_PROGRESS.md (93f9202), Claude world-ledger/README.md (de75a37). Historical MAIN_INPUT_QUERY_CEILING86 (3393c64) already establishes the general input-query ceiling: the conceptual ceiling is reused, not rebranded as new.

Required outside sources actually read: konard/p-vs-np/proofs/complexity/README.md (7ee9a11) and scripts/proof_status.json (93b77ed; different one-tape model); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693e), AFFINE_BOUNDARY_PHASE_REPORT.md (3228ffe); MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd); meelgroup/frat-xor/README.md (38a137b); openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (1ced21f). Primary papers FLMV 2005 DOI 10.1145/1101821.1101822; Urquhart 1987 DOI 10.1145/7531.8928; Ben-Sasson/Wigderson 2001 DOI 10.1145/375827.375835. Indexed web searches performed; direct Google-branded access unavailable. None solves this transfer.

**OPEN:** Every total uniform polynomial SAT decider still needs a correct all-input, recursively iterable transformation with paid same-FLMV-machine $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$. LSPV-4/432's raw $qH$ lower bound remains valid in its actual input model, but its unqualified comparison against the smaller original-input budget is rejected. Route B mixed minimum and noncircular B3 remain OPEN. P versus NP OPEN.
