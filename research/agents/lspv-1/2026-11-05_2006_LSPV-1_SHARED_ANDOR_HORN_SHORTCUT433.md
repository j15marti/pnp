# LSPV-1/433: Shared AND/OR minimum, SET COVER and a native strict-Resolution escape
**November 5, 2026, 20:06 PST | Route B lead. PROVED/EXACT (scoped), COMPUTATIONAL (finite), B3/P vs NP OPEN.** Independent mathematical review pending. The original `R_mix341` and five-agent 2A/3B allocation are unchanged.

## IDEA and falsifiers before search
Test whether a free-choice *globally shared* paid proof-DAG minimum equals an independently optimized sum of branch costs. F1: paying the same cross-branch producer repeatedly never overcounts. F2: one missing conjunct is permitted at an AND join. F3: a branch-local assumption is exportable without discharge. F4: optimizing an abstract restricted AND/OR grammar gives a lower bound for full historical `R_mix341` even when strict RES has legal shortcuts. F1-F3 fail by typed union/provenance checks; F4 is explicitly falsified below. No new 3-SAT hard family is claimed.

## Precise theorem A: a *separate* typed proof hypergraph
Fix a nonempty universe $U$ of $m$ elements and sets $S_1,\ldots,S_s$ with union $U$. In **separate proposed** `H_COVER`, free sources are $A_j$ and `NEG_ALL`. Unit-cost `SET(j)` derives reusable paid $P_j$ from $A_j$; `ELEMENT(i,j)` derives $E_i$ from $P_j$ iff $i\in S_j$; binary `AND` unions disjoint element supports; a paid binary `CONFLICT` combines the all-elements conclusion with `NEG_ALL`. Choices of $j$ are OR alternatives; all $m$ distinct elements are mandatory AND obligations. Every dependency is acyclic, every charged node costs once, context $Gamma$ must justify antecedent assumptions. These rules are **not** native `R_mix341`.

Let $\tau(S)$ be the minimum SET COVER size. The complete unrestricted-search minimum of *this typed hypergraph* is exactly
$$
W_{H_{COVER}}(U,S)=2m+\tau(S).
$$
Proof: all $m$ elements need distinct paid producers, their reused set owners form a cover of size at least $\tau$, at least $m-1$ binary AND nodes are required, and the final conflict costs one. Thus $W\ge m+\tau+(m-1)+1$. Choosing an optimal cover once, reusing its set producers for all covered elements, then balancing the binary conjunction achieves equality. Since SET COVER decision is NP-complete (Karp 1972), deciding $W_{H_{COVER}}\le2m+k$ is NP-complete by a many-one reduction, and a typed DAG is a polynomial certificate. This is **offline proof-optimizer complexity for a supplied artificial grammar**, not SAT, mixed proof cost, or machine-time hardness.

## Precise theorem B: legal native RES defeats this artificial cost
For $m\ge1$, take the original-source CNF
$$
F_m=(a)\land(\neg a\lor h)\land\bigwedge_{i=1}^m(\neg h\lor e_i)\land(\neg e_1\lor\cdots\lor\neg e_m).
$$
All $m+3$ clauses are indispensable: remove $(a)$ and set $a=h=e_i=0$; remove $(\neg a\lor h)$ and set $a=1,h=e_i=0$; remove $(\neg h\lor e_i)$ and set $a=h=1,e_i=0,e_{j\ne i}=1$; remove the final clause and set everything to one. A sound conservative proof with at most two premises per paid unit-weight inference therefore needs $m+2$ charged nodes (the established source-capacity argument).

A **legal native strict RES proof** attains $m+2$: start with the last source clause; successively resolve away each negative $e_i$ using $(\neg h\lor e_i)$, obtaining $(\neg h)$; resolve with $(\neg a\lor h)$ to obtain $(\neg a)$; resolve with $(a)$ to obtain the empty clause. Therefore under original declared binary-premise unit-weight semantic `R_mix341`,
$$
W_{R_{mix341}}(F_m)=m+2.
$$
At $m=3$, this is an ordinary width-at-most-three CNF, with 5 variables, 6 clauses, and *exact mixed minimum 5*. By contrast, forcing an artificial `H_COVER` one-set-covers-three rule gives 7 nodes. The gap results from a fully legal RES shortcut; it cannot be excluded to protect a hardness claim. The source is **not proper exact-width-three** without separately accounted padding, and this is a focused Horn counterexample, not a published hard family.

## Hard-family / rule / size / transfer ledger
**Urquhart 1987; Ben-Sasson–Wigderson 2001:** for suitable cubic expander graphs $G=(V,E)$ with $h$ vertices and odd vertex charge, parity at every degree-three vertex is encoded by the four 3-clauses forbidding the opposite-parity triples. This has $4h$ clauses, $3h/2$ edge variables, and $\Theta(h\log h)$ standard DIMACS bits. Ordinary unrestricted DAG Resolution needs $2^{\Omega(h)}$ nodes (graph expansion and original encoding matter). **Existing LSPV-2/341:** same odd-charge bridgeless cubic sources have exact *mixed* $4h-1$ paid AND3/GF(2) nodes; this known shortcut defeats any direct full-mixed transfer. **Cook 1976:** ER short pigeonhole refutations. **Braun arXiv:2609.23015 (2026):** bit PHP lower bound $\exp(2^\ell/(32768\ell^2))$ for unrestricted DAG-like Res(XOR), $\ell\ge32$, not a certified strict3 or fixed `R_mix341` lower bound. No equisatisfiability-only encoding transfer is used.

## Independent finite checks and accounting
Python enumerated **2,938** explicitly covered set systems, verifying the exact abstract optimum with **10,785 assertion groups**, rejecting five corrupted contexts/premises/AND DAGs. Independent Node checker recomputed every minimum cover, individual element producer, shared-set cost, and both context/AND failures with **39,106 assertions**. Independent native source script generated RES proofs and clause-deletion SAT witnesses for $m=1,\ldots,7$; separate Node checker passed **1,256 assertions** over all source truth assignments and oriented pivots, rejecting a corrupt pivot. $m=3$ source file is exact width-at-most-three. Full producer, raw 2,938 cases, source CNF, native proofs, both Node verifiers and hashes are preserved in the conversation reproducibility archive; GitHub public raw is a compact verifiable summary. Host runtime timings, parser/source reads, proof construction, verification, output bit lengths, physical memory and failed alternatives are not included in the **offline** $W$ minimum and remain payable in actual algorithms. No historical ambiguous DEF/LOCAL byte checker was executed.

## Readback, corpus and limitations
Read the Nov 2 12:04 governing handoff, issue #3 through REFEREE376, AGENTS.md, CODEX.md, project research skill, original `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob `c87acd11`, LSPV-3/423 blob `49bf06ce`, LSPV-5/353 blob `ed4f51eb` and REFEREE318, LSPV-4/406, older HORN-GUARD-SET-COVER-GATE268. Actual Grok `GROKPROOF/2026-11-05_1218_PROGRESS.md` blob `d3183283` and Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob `9a5b05d6` were checked. Also examined `konard/p-vs-np/README.md` blob `0e0ec77f`; `blkph0x/p-vs-np-proof-research/README.md` blob `f397a774` and `local_marginal_code_lab/level10_conditioning/THEOREM.md` blob `3f662754`; `tanyongkiam/cake_lpr/README.md` blob `e94f45e9`; and `openai/math/README.md` blob `cc5b0a03`. Web searches addressed Karp Set Cover, Urquhart resolution, Res(XOR) and proof-DAG optimization; direct Google-branded session unavailable. The older source-arity argument and classical Set Cover hardness are reused, not claimed novel. Root `main.tex` remains untouched because full-body preservation cannot be verified.

**Precise remaining open arrows:** a superpolynomial minimum under **every** original native rule (including all legal RES shortcuts, shared branching, AND3, GF(2), DEF and LOCAL) and a noncircular B3:
$$
\mathrm{SAT}\in P\ \Longrightarrow\ \overline W_{R_{mix341}}(N)\le C(N+1)^k\quad\text{for some fixed }C,k\text{ and every }N.
$$
B1, B2, B3, complete historical grammar and P versus NP remain **OPEN**.

**Sources:** Karp, *Reducibility among Combinatorial Problems* (1972), DOI 10.1007/978-1-4684-2001-2_9; Urquhart, *Hard Examples for Resolution*, JACM 1987, DOI 10.1145/7531.8928; Ben-Sasson and Wigderson, *Short Proofs Are Narrow*, JACM 2001, DOI 10.1145/375827.375835; Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution* (1976); Braun, arXiv:2609.23015 (2026).
