# LSPV-4/439 | Sparse charge-overlay guest-input port and dense-bank resource correction

**2026-11-06 05:44 PST, Route A primary. PROVED/RESTRICTED port lemma and COMPUTATIONAL independent controls. All-input FLMV contraction, Route B B3, and P versus NP remain OPEN.**

## IDEA, falsifiers, revision

**Hypothesis:** Earlier LSPV-4/435 and /436 retained a dense $H$-bit bank to reconstruct nested Tseitin child bits. For at most $K=O(\log N)$ authenticated immutable vertex-charge edits, the same child can be served through a sparse path with polylogarithmic writable space. Before searching, four falsifiers were fixed: (F1) edits affect bits outside the third literal's sign; (F2) repeated edits or nested return corrupt source bits; (F3) malformed descriptors escape validation when a guest never queries an affected bit; (F4) sparse ports imply either an $N^{1/2}$-bit guest CNF or the target arbitrary-guest space reduction.

**Results:** F1 and F2 fail by a complete bit-identity proof. F3 **found a defect in the new local prototype:** bounds checks deferred to affected-bit queries allowed an invalid descriptor to go undetected if the guest read only metadata. We added a mandatory paid pre-guest validation scan and reran Python/JS controls. F4 is *false*, because every child still has size $N$ and its guest space is unchanged. This improves an implementation bound, not the universal missing theorem.

## Published hard family, precise qualification

Let $G=(V,E)$ be a connected simple cubic graph with $H=|V|$, $M=3H/2$, and sorted incident edge IDs $a_v<b_v<c_v$. For each charge (chi_v\in\mathbb F_2), use exactly the four original strict 3-clauses

$$
C_{v,p,r}(\chi)=\ell_p(x_{a_v})\lor\ell_r(x_{b_v})\lor\ell_{p\oplus r\oplus1\oplus\chi_v}(x_{c_v}),\qquad p,r\in\{0,1\},
$$

with (ell_0(x)=x), (ell_1(x)=\neg x). There are $4H$ clauses, $12H$ literal occurrences, and no reduction from a wider CNF. By the GF(2) incidence rank theorem, a connected instance is SAT iff (igoplus_v\chi_v=0). On *suitable growing cubic expander* sequences with odd charge, the Urquhart (1987) and Ben-Sasson/Wigderson (2001) lower bounds give (2^{\Omega$H$}) size against **ordinary shared-DAG Resolution only**. Not against ER, XOR, the complete fixed $R_{\mathrm{mix341}}$, or unrestricted SAT algorithms. K4, cube, Petersen, and prism graphs in the finite experiment are representation controls, not asymptotically certified hard instances. GF(2) parity is an explicit legal **upper-bound control**.

The tested source packet includes eight magic bits, unary $H$, unary $w=\operatorname{bitlength}(M)$, $3H$ incidence IDs of width $w$, and $12H$ original signed literal records of (w+1) bits. The exact charged packet length is

$$
N=8+(H+1)+(w+1)+3Hw+12H(w+1)=\Theta(H\log H).
$$

Graph metadata is **supplied and must be authenticated**, not inferred by an oracle. Arbitrarily large variable names, shuffled unannotated clauses, or a general binary-CNF input require separate parsing and fallback.

## Theorem 439.1: sparse bit-exact charge overlay (PROVED/RESTRICTED)

Let $P$ be a validated immutable source packet, $b$ the body offset, and $L=(v_1,\ldots,v_K)$ a **fully prevalidated** edit stream. Repetitions are permitted. Let (chi'_v=\chi_v\oplus (\#\{i:v_i=v\}\bmod 2)) and let $P_L$ be the exact original-source signed CNF packet for (chi').

For every address $j$, $P_L[j]=P[j]$ except when $j$ is the polarity sign of the third literal in a quartet belonging to vertex (v). For that one sign field,

$$
P_L[j]=P[j]\oplus \bigoplus_{i=1}^{K}\mathbf 1[v_i=v].
$$

**Proof.** In each of the four canonical vertex clauses, the charge occurs only in the term (p\oplus r\oplus1\oplus\chi_v). Every edge identifier, metadata bit, and first/second sign is independent of the charge. Repeated toggles cancel over GF(2). The vertex for a candidate third-sign record can be recovered by fixed-width address arithmetic, and a sequential scan of the (K) edit IDs reconstructs the parity without writing an $H$-bit bank. The immutable root and complete current path keep sibling/ancestor scopes separate. QED.

**Machine model and real costs:** FLMV Section 2.1, p. 4, explicitly uses read-only indexed input, indexed work tapes, *erasure of the index tape on indexed jumps*, write-only output, and a high-water-address work-space measure. Count descriptor generation, its **mandatory pre-guest validation**, all source/metadata read and index-head updates, guest simulation, source authentication, failed policies, caches, child/ancestor retention, replays, and output separately. For (D) DFS frame pointers, when validated descriptors are retained on work tape, port costs are

$$
T_{\mathrm{bit}}=O((K+1)\operatorname{polylog} N),\qquad
S_{\mathrm{port}}=O($K+D+1$\log N),
$$

**in addition to guest and generator high-water**. For $K,D=O(\log N)$, the *port* uses (O(\log^2N)) physical space. If (Q) bit requests occur and (R) descriptors are generated, a conservative whole-phase ledger is

$$
T\le T_{\mathrm{auth}}$N$+T_{\mathrm{gen}}(N,R)+O((R+Q(K+1)+D)\operatorname{polylog}N)+T_{\mathrm{guest,nonread}},
$$

$$
S\le S_{\mathrm{auth,simultaneous}}+S_A$N$+S_{\mathrm{gen,simultaneous}}+O($K+D+1$\log N).
$$

**Correction:** On the native $N=\Theta(H\log H)$ Tseitin packets, the old dense $H$-cell writable bank is $\Theta(N/\log N)$ space and is **not** within $N^{1/2+o(1)}$. LSPV-4/435's previous small-space corollary explicitly assumed $H\le N^{1/2+o(1)}$, which natural-size Tseitin packets do not satisfy. The new sparse port repairs that component under sparse-edit assumptions.

**No FLMV contraction:** The guest-facing child remains length $N$. Sequential faithful replay of a guest using $N^t$ time and $N^s$ space across $q=N^{3/5}$ children has an upper bound $qN^t\operatorname{polylog}N$, not the desired $N^{3/5+t/2}$, and does not reduce the guest's own $N^s$ state. No arbitrary-CNF all-input, both-label, malformed-aware recursive transformation is obtained.

## Independent checks and source inventory

Python generated 7 graph controls (H=4,8,10,20,64,128,256), 42 deterministic nested paths, **80,022** bit comparisons, 18 exhaustive small-graph SAT tests, 42 parity/return controls and 14 hostile invalid-source/descriptor rejections. A separately written Node.js referee reconstructed **395,280** full packet bits and source/child SHA-256 hashes. An executable self-contained compact referee additionally passed **87,489** tests. Raw JSON SHA-256: `629ac54c152531a920df4ab1cc296e94f65101f49f908047452b8bd433e2d044`. The host programs use ordinary memory and are *not native FLMV machine traces*.

Actual reviewed project: issue #3 through LSPV-2/443; governing Nov. 2 handoff blob `c3889a3e`; LSPV-4/438, /436 `86f38465`, /435 `87759faa`; LSPV-2/422, /442 `3421953d`, /443 `82fcf28c`; AGENTS.md `19656af1`, CODEX.md `754999f5`, pnp research skill `b8df83a7`; Grok `GROKPROOF/2026-11-06_1220_PROGRESS.md` `5c4fbf8f`; Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` `1f9fc727`. The Claude portfolio barrier does not transfer automatically to this compiler. LSPV-2/443's *sequential streaming recognition* lower bound is a different model and does not rule out the indexed sparse read port.

External exact paths/blobs: `konard/p-vs-np/proofs/complexity/README.md` `7ee9a11e`, finite one-tape model; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` `18d693ea` and `CERTIFIED_RESIDUAL_QUOTIENT_REPORT.md` `b37da20a`, incomplete certified merging; `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` `4bb5fd19`; `meelgroup/frat-xor/format.md` `986a21aa`, a different proof format; `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` `1ced21f4`, a bounded concrete driver and not an arbitrary SAT compiler. FLMV author PDF Section 2.1 machine-page screenshot was inspected. Indexed web and GitHub search ran, not a Google-branded direct search.

**Next precise gap:** authenticate and construct genuinely *smaller* SAT guest inputs, with correct AND/OR branch combination and no uncharged cache/conversion, for every uniform total correct polynomial SAT decider. The desired recurrences (t'\le\max(11/10,3/5+t/2)), (s'\le\max(1/2,s/2)) remain **OPEN**. Route B historical mixed rule grammar, all-rule minimum and noncircular B3 remain **OPEN**. No inference weights, ownership, agents, schedules, or root manuscript were altered. P versus NP remains OPEN.

**Sources:** Urquhart, *Hard Examples for Resolution*, JACM 1987, DOI 10.1145/7531.8928; Ben-Sasson and Wigderson, *Short Proofs Are Narrow*, JACM 2001, DOI 10.1145/375827.375835; Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 2005, DOI 10.1145/1101821.1101822.