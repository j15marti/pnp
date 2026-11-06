# LSPV-4/432: Independent raw-source vs authenticated-delta portfolios

**November 5, 2026 22:40 PST | Route A PRIMARY | PROVED/RESTRICTED, COMPUTATIONAL | Universal FLMV contraction OPEN; P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE; four falsifiers
Hypothesis: extend LSPV-2/435's exact one-source pivotal-bit argument to $q$ independently supplied, complete 3-CNF sources, then exhibit an efficient legal, *different* representation: one validated common base plus a signed charge-toggle stream. F1 one vertex flip may preserve the SAT label; F2 the binary encoding might change outside the four declared sign positions; F3 a virtual signed port may fail exact-bit equality or accept partial four-bit corruption; F4 the raw-input query bound might be incorrectly applied to correlated generator outputs. Mathematical proofs and independent finite checks ruled out F1–F3 for the stated family. F4 requires the revised model distinction below.

## Exact established 3-CNF family and hardness ledger
Take a connected simple cubic graph $G=(V,E)$ with $H$ vertices and $M=3H/2$ edge variables. With incident edges $a_v<b_v<c_v$ and $\ell_0(x)=x$, $\ell_1(x)=\neg x$, define the four proper 3-clauses
$$
C_{v,p,q}(\chi)=\ell_p(x_{a_v})\lor\ell_q(x_{b_v})\lor\ell_{p\oplus q\oplus1\oplus\chi_v}(x_{c_v}),\quad(p,q)\in\{0,1\}^2.
$$
There are $4H$ clauses and $3H/2$ variables. The formula enforces edge-parity equation $\bigoplus_{e\ni v}x_e=\chi_v$. For connected $G$ the incidence matrix has rank $H-1$, so the entire source is SAT iff $\bigoplus_v\chi_v=0$. An odd-charge source is therefore UNSAT by a direct parity certificate, not by inference from empirical solver time.

The exact **test-only** typed binary source format is the historical LSPV-2/435 grammar: eight-bit magic 10100111, unary $H$ and $M$, $2Mw$ sorted graph-endpoint bits, $4H$ ordered clauses each with three sign-and-$w$-bit edge IDs, and terminal 00, $w=\max(1,\mathrm{bitlength}(M))$. Thus
$$
N=8+(H+1)+(M+1)+2Mw+12H(w+1)+2=\Theta(H\log H).
$$
Flipping $\chi_v$ flips *only* the four disjoint third-literal sign positions $D_v$ in that vertex's four clauses. For **growing cubic expander families under the proper expansion hypotheses**, ordinary shared-DAG Resolution has $2^{\Omega(H)}$ refutation-size lower bounds (Urquhart 1987; Ben-Sasson/Wigderson 2001). This family is already strict 3-CNF, so no lower-bound-preservation reduction is assumed. Those theorems do not cover extended Resolution, GF(2), mixed $R_{\mathrm{mix341}}$, or arbitrary SAT algorithms. The project's known $4H-1$-node mixed AND3/GF(2) proof is a mandatory short-derivation countercontrol. Haken ordinary Resolution PHP and Cook extended Resolution remain separate controls.

## Theorem 432.1: raw independent sources, a direct-product query lower bound
**PROVED/RESTRICTED.** Fix $G$. Input is an ordered tuple of $q$ **independent complete canonical source strings** $x_i=\mathrm{enc}(F_{G,\chi^{(i)}})$; output all $q$ SAT/UNSAT labels. On *every promised tuple*, a deterministic total correct machine must query at least one bit in every $D_v$ of **every** input block. It must therefore perform at least $qH$ distinct source-bit reads.

Proof: if a run never reads a bit from $D_v$ in block $i$, change those four bits in that block alone. The new input is promised, has the same size, reverses exactly the $i$th required SAT label, and changes no queried bit. Deterministic transition induction makes both runs identical, contradiction. All $qH$ sets are disjoint.

At nominal $q=N^{3/5+o(1)}$, this lower bound is $N^{8/5-o(1)}$ reads, beyond the proposed $N^{11/10+o(1)}$ local budget **for this raw independent input interface**. The raw input itself has $qN$ bits. This is NOT a universal SAT lower bound or an obstruction to correlated child generation, nor a work-tape-space bound.

## Theorem 432.2: fully distinguished authenticated-delta interface
**PROVED/RESTRICTED.** Given one *validated* canonical base source $x$ and a read-only list of legal vertex IDs $v_1,\dots,v_q$, each child's original-source bit is generated exactly by
$$
x^{(j)}[p]=x[p]\oplus\mathbf 1[p\in D_{v_j}].
$$
The four $D_v$ positions are explicit arithmetic offsets in the historical sorted clause layout, and each bit port can be implemented with polylogarithmic charged indexed operations and $O(\log N)$ densely addressed physical work/index space. The children's SAT labels equal the base label inverted. Compute the base parity by one pivotal charge read per vertex, then stream the $q$ inverted labels. If the original template validator costs $V_G(N)$ time and $S_V(N)$ peak space, the whole interface costs
$$
T_\Delta=O(V_G(N)+(H+q)\operatorname{polylog}(N+q)),\qquad
S_\Delta=O(S_V(N)+\log(N+q)).
$$
The validator includes original-source reads, graph/row authentication, checking all four local signs per inferred charge, index writes/erasure and cleanup. It cannot be assumed free. For a graph/template uniformly generable per bit in polylogarithmic time and log space, exact-source checking can run in $O(N\operatorname{polylog}N)$ and $O(\log N)$ space; this **is not proved for arbitrary graph inputs or general CNF**. Materializing $q$ full child strings costs $\Omega(qN)$ output bits, whereas virtual-source access does not. An untrusted full child cannot be accepted solely from a claimed delta ID. An arbitrary unsupported CNF needs a correct charged fallback.

The independent input admits $2^{qH}$ charge portfolios; the shared-base/one-toggle format admits at most $2^HH^q$. Its lower resource use reflects a **different input promise** rather than defeating the direct-product bound.

## Finite controls, exact provenance
The complete Python producer (provided in a reproducibility archive for this run) passed **15,449** assertions, covering every charge vector and every single-vertex flip on K4, Cube and Petersen, parity-vs-edge-assignment reachability, exact four-bit delta source equality, six initial SAT/UNSAT sources and invalid magic, truncation, fixed-row corruption and one-of-four-sign corruption. An **independently written Node referee** passed **1,750** checks including original-source SHA-256 and all edge assignments. Counts by graph, for *each* even and odd initial source:

| Graph | $H$ | $N$ bits | $q$ | Raw required reads $qH$ | Delta charge/ID symbols $H+q$ |
| --- | ---: | ---: | ---: | ---: | ---: |
| K4 | 4 | 250 | 13 | 52 | 17 |
| Cube | 8 | 608 | 21 | 168 | 29 |
| Petersen | 10 | 757 | 25 | 250 | 35 |

The producer's $qN$ child-bit comparisons validate sources but are not charged to the theorem's **decision-only** delta algorithm. These finite graphs are not a certified growing expander sequence. Tests are host-language, not native FLMV Turing-machine benchmarks or authoritative $R_{\mathrm{mix341}}$ checker runs. Logical DAG work, critical path and realizable machine time/peak space remain separate; all existing weights and grammar are unchanged.

## Search and continuity
Read actual governing handoff, issue #3, AGENTS.md, CODEX.md, project research skill, LSPV-2/434 and /435, LSPV-4/431, Grok GROKPROOF/2026-11-06_0515_PROGRESS.md (blob 93f9202d), and Claude research/agents/claude/world-ledger/README.md (de75a371). This theorem extends LSPV-2/435's single-source pivotal result; **it is not a new single-source theorem**. Third-party code/readbacks: konard/p-vs-np/proofs/complexity/README.md (7ee9a11) and scripts/proof_status.json (93b77ed; distinct finite one-tape model); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693e) and AFFINE_BOUNDARY_PHASE_REPORT.md (3228ffe; bounded algebra); MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd); meelgroup/frat-xor/README.md (38a137b); openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (1ced21f; specialized costed program). Checked FLMV original paper section 2.1 and its PDF page 4 screenshot: indexed jump erases index-tape contents and space charges the highest work-tape address. Direct Google-branded interactive search unavailable; targeted indexed web search was used.

References: Fortnow et al., JACM 52 (2005), DOI 10.1145/1101821.1101822; Urquhart, JACM 34 (1987), DOI 10.1145/7531.8928; Ben-Sasson/Wigderson, JACM 48 (2001), DOI 10.1145/375827.375835.

## Remaining transfer, OPEN
The split between independent complete sources and authenticated generated deltas is mathematically essential. No uniform, recursively iterable same-FLMV-machine compiler has been built for *every* binary CNF and every fixed total correct polynomial SAT decider, with unknown exponents and both labels/malformed handling, satisfying
$$
t'\le\max\{11/10,3/5+t/2\},\qquad s'\le\max\{1/2,s/2\}.
$$
Its all-input child generation, authentication and valid join with fully charged local policy search, failed policies, ancestor buffers, replay, cache, output and physical high-water are OPEN. Route B's native fixed $R_{\mathrm{mix341}}$ minimum and noncircular B3 are separately OPEN. P versus NP remains OPEN.
