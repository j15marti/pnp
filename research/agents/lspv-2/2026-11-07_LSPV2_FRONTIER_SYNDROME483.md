# LSPV-2/483 | Defect-frontier DP supersedes cycle-rank conditioning on authenticated graph-local 3-CNF

**November 7, 2026, PST | LSPV-2 | Route A primary | PROVED/RESTRICTED (standard DP specialization) + COMPUTATIONAL. P versus NP OPEN.**

**Tracker nodes:** Material restricted shortcut/control evidence for [P2-A4]; [P2-A2] universal code-aware all-input contraction and [P2-A5] recursive closure remain OPEN. Cross-chain [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. No historical R_mix341 rule, grammar, weights, roles or schedules altered.

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis:** The LSPV-2/477 algorithm's $2^{3r}$ cost for defect cycle rank $r$ is not a necessary cost on all graph-local Tseitin-derived sources: retaining only the ordered frontier of defect vertices and one $c$-bit parity syndrome should allow $2^{O(w+c)}$ state space for vertex-separation width $w$, even when $r=\Theta(H)$.

**Precommitted falsifiers:** (F1) the frontier merge admits incompatible assignments of the same original edge; (F2) component boundary equations cannot be reconstructed from frontier syndrome, yielding a SAT/UNSAT disagreement with original signed 3-CNF clause evaluation; (F3) a prism source with $r=\Theta(H)$ actually forces $w$ to grow with $H$ for the stated order; (F4) source parsing, order acquisition or native execution silently satisfies the desired FLMV $S=N^{1/2+o(1)}$ bound without charging input memory.

**SEARCH and reuse:** Both full root proof trackers, current coordination issue #3 and newest peer comments, governing five-role handoff (2026-11-02_1204), role /475, /477, /482, peer LSPV-4/484, actual GROKPROOF/2026-11-07_1920_PROGRESS.md and Claude WORLD-LEDGER-0001.tex, AGENTS.md, CODEX.md and the PNP research skill reviewed. Relevant primary published background: Ben-Sasson and Wigderson, JACM 48(2):149-169 (2001), DOI 10.1145/375827.375835 for ordinary Resolution hardness on expanding graph sources; Fortnow, Lipton, van Melkebeek and Viglas, JACM 52(6):835-865 (2005), DOI 10.1145/1101821.1101822 for fixed random-access machine SAT time/space; Samer and Szeider, "A Fixed-Parameter Algorithm for #SAT with Parameter Incidence Treewidth", arXiv:cs/0610174 for established decomposition DP (different width parameter and formula model). Google-indexed web search used; no separate Google-branded client. Neither full published paper theorem was independently re-proved. External actual files: MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab; konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and INDEPENDENT_AUDIT.md blob b30515cced93d8911a6415555ee9ec1444502d93; meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f; openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean blob 1ced21f44ad49370d1b812e862c03c3a91d7f836. These external sources neither prove this specialization novel nor yield universal contraction. Earlier code-search matches were dominated by tracker/outbox copies; no new all-input compiler surfaced.

**ITERATE:** Replace cycle-cutset enumeration with width-bounded processed-frontier DP and signed source-clause exhaustive controls. This is a **known-method extension of /477** to a different parameterization, not a new general structural SAT theorem.

## Exact family / encoding / known-method ledger

Let $G=(V,E)$ be an explicitly encoded simple cubic graph, $H=|V|$, with each original edge $e$ carrying one Boolean $x_e$. Every vertex $v$ has three incident edges in canonical sorted-edge order. A proper signed ternary clause forbidding the local pattern $a=(a_1,a_2,a_3)\in\{0,1\}^3$ is

$$
C_{v,a}=\ell_{e_1,a_1}\lor\ell_{e_2,a_2}\lor\ell_{e_3,a_3},\qquad
\ell_{e,0}=x_e,\quad\ell_{e,1}=\neg x_e.
$$

Each vertex has an arbitrary **source-authenticated packet** $P_v\subseteq\{0,1\}^3$ of at most eight distinct forbidden patterns, representing the conjunction of exactly those original $C_{v,a}$. In particular the intact parity packet with charge $b_v$ is $P_v=\{a:a_1\oplus a_2\oplus a_3\ne b_v\}$, containing exactly four signed clauses. Let $I$ be the vertices with intact parity packets and $D=V\setminus I$. The formula contains at most $8H$ original proper 3-clauses and $|E|=3H/2$ source variables. With explicit $O(H)$-sized integer IDs, binary input length is $N=\Theta(H\log H)$ for the canonical family; general unbounded-ID encodings require their actual bit costs.

**Published hardness control:** For suitable cubic expander graphs with odd total charge and **all packets intact**, ordinary shared-DAG Resolution requires exponential proof size (the cited width-size/expansion literature). This is proof-system-specific; there is an $O(H)$ GF(2) parity contradiction. The prism $C_k\square K_2$ used below is bounded-width and **not certified hard in that expander theorem**. No hardness-preservation claim transfers from expanders to prisms.

**Known shortcuts:** All intact parity components are eliminated by GF(2) summation. Defect clauses are checked exactly in a shared frontier DP. Neither inference is asserted native to historical R_mix341 or a free semantic oracle. This algorithm is a legitimate computational upper-bound control, not a native proof certificate.

## Theorem 483.1 (PROVED/RESTRICTED): component syndrome and ordered frontier

Let the graph induced by $I$ have $c$ connected components, and let a supplied verified ordering $\pi$ of $D$ have maximum vertex-separation frontier $w$. For a prefix of the ordering, its frontier is the already processed defect vertices adjacent to any not-yet-processed defect vertex. A deterministic bit-RAM algorithm decides the exact source 3-CNF by maintaining only assignments to the three incident original-edge bits at each frontier vertex (at most $8^w$ possibilities) and an accumulated $c$-bit boundary syndrome (at most $2^c$ possibilities).

Each step tries the eight local edge patterns at the next defective vertex, rejects forbidden source clauses, checks shared defect-edge equality against any processed neighbor, XORs its boundary contribution to the intact-component syndrome, and projects onto the next frontier. Two states with identical frontier assignments and syndrome are merged by Boolean OR. No branch-local conclusion is used outside its justified edge assignments.

In particular the number of simultaneous logical states is at most $8^w2^c$, and there are at most $8^{w+1}2^c$ local candidate transitions per processed vertex. A straightforward optimized implementation with verified order, adjacency/index and parity preprocessing costs

$$
T=O\!\left(N+H(w+c+1)8^{w+1}2^c\operatorname{polylog}(N+2)\right),
$$

$$
S=O\!\left(N+(w+c+\log H+1)8^w2^c\operatorname{polylog}(N+2)\right)
$$

in BIT operations / writable bits for an implementation retaining the full typed source and two DP tables. Constants depend only on the fixed signed graph-local grammar. These are conservative bit-RAM bounds, **not** validated FLMV indexed-machine bounds. The independently implemented Python and JS reference codes use extra graph scans and do NOT claim to meet the optimized asymptotic implementation time.

**Proof:** Summing intact parity constraints over each connected component cancels every internal original edge twice, leaving precisely one XOR boundary equation with target equal to the XOR of that component's charge bits. Conversely, a connected graph's GF(2) incidence matrix has rank $|I_j|-1$, so a fixed boundary assignment extends to its internal edges iff that one equation holds. Each defective vertex state specifies all its incident original edges; two endpoint states must agree on shared defect-defect edges. Induct over the ordering: the DP row denotes exactly the locally valid processed assignments projected onto the live frontier and the XOR of already processed defect-intact boundary bits. Any forgotten processed defect vertex has no edges to future defect vertices, so it cannot affect future legality except through the retained syndrome. At the final empty frontier, accepting the exact charge syndrome is equivalent to all original clauses admitting one global edge assignment. The state and transition bounds follow by counting $8$ local patterns per frontier vertex and $2^c$ syndromes. No omitted branch obligation or improper shared assumption is used.

**Caveat:** Finding an order of small $w$ is not free. The theorem is conditional on a supplied order or a separately charged order-construction algorithm. Its generic implementation stores $\Omega(N)$ source/graph information, so it does not meet the required Route A writable-space exponent $1/2$. No same-machine native FLMV construction was performed.

## Corollary 483.2: large cycle rank does not entail large frontier work

For the prism $G_k=C_k\square K_2$ with $H=2k$, $k\ge3$, ordered by successive rung pairs, the maximum processed frontier is at most 4, irrespective of $k$. If all $2k$ vertex packets are defective, their induced graph has

$$
r=|E|-|D|+1=3k-2k+1=k+1,
$$

while $c=0$ and $w\le4$. Thus the algorithm is polynomial in source size even though LSPV-2/477's cutset-bound factor $2^{3r}$ is exponential. If one vertex is left intact and the remaining packets defective, $c=1$, $r=k-1$ and the same rung order (with the intact vertex skipped) has width at most 4 (the finite runs show width 3 for the specified position). These are explicit legal shortcuts, not claims that cubic expander hard sources have small width.

## Finite independent reproducibility, machine ledger

**Python reference:** seed 483, 490 tested cases, 252 SAT / 238 UNSAT, including exhaustive charge vectors for $k=3,4$, small random damaged packets and larger $k=6,8,12,30,100$ controls; two malformed typed sources rejected. SHA-256 of local reference file b9e675862305acf5b1e4308c0ef7e73649b123bf15b57b06428131f725a7dcfa.

**Independent published JavaScript:** distinct LCG and implementation, 165 cases, 105 SAT / 60 UNSAT; 2 malformed typed sources rejected. Exact signed-clause disjunction exhaustive oracle for small prisms. Published-byte V8 replay PASS. At $k=100$, $D=200$, $c=0$, $r=101$, frontier width 4, maximum 1225 stored rows. Mixed case $D=199$, $c=1$, $r=99$, width 3, max 686 rows (Python). The finite tests are controls, not an asymptotic proof. JS uses 32-bit syndrome masks and explicitly rejects $c>28$; abstract theorem and Python use arbitrarily long syndrome vectors.

**Resource ledger:** Logical DP rows upper bounded above; reference code's Python/Node interpreter time, allocation, hash-table memory and full graph storage are charged in actual runs but not mapped to the native FLMV machine. Input and packet parsing $O(N)$; graph/index preprocessing $O(N)$ in optimized algorithm and potentially $O(H^2)$ in reference; acquisition of source/order unproved on arbitrary SAT; pairwise exact equality and boundary XOR costs included; two maps retain at most two frontier tables, each $O(8^w2^c)$ entries; search/discovery cost of the order not free; no guest solver calls; no certificates or reparse of historical R_mix341; output one classification bit; no sharing outside justified frontier assignments; no uncharged branch reconstruction or native machine conversion. Space $S=N^{1+o(1)}$ in fully materialized general reference, so this is not a Route A step achieving $s'\le1/2$.

## Remaining dependencies and publication

This **falsifies cycle rank as a universal cost proxy** within this graph-local restricted family, but does not falsify /477's valid algorithmic upper bound. It does not prove a universal SAT contraction, a worst-case lower bound, a native mixed-calculus refutation or noncircular B3.

Verifier: experiments/arc/lspv2_483_frontier_syndrome_independent.js, published blob 3cd4afd3035b1b371714e51db7b7c979f3700efe.
Raw: results/raw/arc/2026-11-07_LSPV2_483_FRONTIER_SYNDROME_RAW.json, blob 4be8b0da5d6c76822334990b1958217f76654b1c.
Next: LSPV-4 should test machine conversion and end-to-end peak space on streamed input; LSPV-2 should return to arbitrary-core exponent-oblivious code-aware transformation, not claim bounded-width DP is recursively applicable.

**P versus NP remains OPEN.**
