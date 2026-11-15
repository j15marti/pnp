# TMR-2/046: Exact fractional-cover dual for overlapping fusion activations, with a strict integrality gap

**2026-11-15 07:08 PST | BATCH116 | TMR-2, PNP Information Necessity**

**Scientific status:** PROVED/RESTRICTED symbolic theorem for a newly qualified preauthenticated record calculus. Independent mathematical review OPEN. Exact finite V8 enumerations COMPUTATIONAL. No unrestricted SAT-machine lower bound, no P-versus-NP resolution.

## 1. Candidate and four falsifiers fixed before literature/corpus checking

**Candidate.** Replacing the one-shot activation of TMR-2/045 by an authentic family of overlapping, partially discharging activation batches may permit a larger fusion-safe initial potential, possibly approaching the minimum number of activations and recovering a multiscale superpolynomial gap.

**Falsifiers.** (F1) A genuine zero-cost metadata operation changes the supposedly charged pending set. (F2) A legal one-step full activation discharges every scale, forcing a joint unit inequality. (F3) An authenticated batch discharges more weighted rank than its unit cost, including overlap with previously activated scales. (F4) Compact circuit evaluation, Gaussian elimination, Horn/Krom/2-SAT propagation, bounded-treewidth DP, certified autarkies, equality/union-find, preprocessing, learning, caching, rereading or recomputation supplies a shorter real SAT computation. F2 is an actual shortcut in the *original* TMR-2/045 calculus; F3 is the decisive exact tariff row below; F4 remains a permitted hostile machine route and forbids upgrading the record model to SAT.

## 2. Recovered state and research provenance

The governing approved fusion directive was read first: research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md, blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6. Subsequently fetched the full 2026-11-13 TMR replacement directive, both proof trackers and root main.tex, AGENTS.md, CODEX.md, repository skill, current five TMR handoffs, issue #3 through 2,150 comments, and original TMR-2/045 mathematical report, executable and raw matrix/data. The full authentic Git blobs were required for proof2 and main because ordinary contents fetch returned blank bodies.

Root SHA audit: proof1.txt 06f7ebc8c2283304a0f5200b518c6e48fa41e343 (28,714 characters); proof2.txt 930c5eeddafce656717f28055a7a9a755f44737c (1,051,196 characters); main.tex 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 (2,545,859 characters). Historical /341 FAIL on its full logical UNSAT acceptance language, /386 RESTRICTED; neither is altered.

Original re-used result, NOT a new assertion: TMR-2/045 provides, for j=5,...,m, a family of same-source, overlapping nonlinear Feistel-interface relations with rank $R_j=4^j$, genuinely shared compact AND/XOR gate identities $G_m=O(m^3)$ and a polynomial-time SAT witness. Original source and original V8 data: experiments/tmr/tmr2_multiscale_activation105.js, blob 5765946d4ac916ad6c529de51b688643a9e63516; results/raw/tmr/2026-11-15_0609_TMR2_MULTISCALE105_V8_RAW.json, blob 7fd3c0730aa846b9300836a3da90a03c5dbe56b0. The original record calculus allows one full ACTIVATE event and has optimal potential $G_m+2$.

Independent primary mathematical context, not claimed as a new source of this theorem: C. Lemke, H. Salkin, K. Spielberg, *Set Covering by Single-Branch Enumeration with Linear-Programming Subproblems*, Operations Research 19(4), 1971, DOI https://doi.org/10.1287/opre.19.4.998; L. Lovasz, *On the ratio of optimal integral and fractional covers*, Discrete Mathematics 13(4), 1975, DOI https://doi.org/10.1016/0012-365X(75)90058-8. All exact equalities below are proved directly, not borrowed from these papers.

## 3. Newly qualified full transition system

Fix finite scale set $J=\{5,\ldots,m\}$; each j is authenticated by the preceding Feistel source $F_m$ with $d_j=4^j-1>0$. Fix a nonempty family of allowed activation subsets $\mathcal E\subseteq 2^J\setminus\{\varnothing\}$, covering $J$. Let $D$ be the original globally deduplicated set of G gate identities. State is

$$
C=(F_m,D,P,U,h,v),\quad P\subseteq D,\ U\subseteq J,\ h,v\in\{0,1\}.
$$

$P$ is the paid CHECK ledger, $U$ is the pending set of scale obligations, $h=1$ means true HALT remains, and $v$ is reversible display metadata. Initial $P=\varnothing,U=J,h=1$, with either display. Goal $P=D,U=\varnothing,h=0$. Legal transitions, exhaustively for THIS calculus:

1. VIEW flips v, or NOP leaves v unchanged, cost zero. Neither changes $F_m,D,P,U,h$; also allowed after HALT.
2. CHECK_ID(g), for g in $D\setminus P$ and $h=1$, cost one, adds that one global gate identity to P. No double count.
3. ACTIVATE_BATCH(S), only when $P=D,h=1$, $S\in\mathcal E$, and $S\cap U\ne\varnothing$, cost one. Changes $U$ to $U\setminus S$. This is a genuine **nonterminal** event, not HALT.
4. HALT, only when $P=D,U=\varnothing,h=1$, cost one. Sets $h=0$. The remaining goal view transitions are free.

There is no otherwise free knowledge acquisition, no spontaneous gate checks, and no unlisted transition in THIS record model. For actual SAT machines, every alternate machine operation must instead remain MAY. In particular restricting $\mathcal E$ is *not* justified as a restriction on arbitrary SAT deciders.

Zero-cost closure consists exactly of reversible two-view SCCs with fixed $(F_m,D,P,U,h)$, plus self-loop NOP. Its quotient is the core state $(P,U,h)$.

Define the dynamic per-scale **exact components**

$$
p_j(\widehat C)=d_j\,\mathbf 1[j\in U],\quad
p_\Gamma(\widehat C)=G-|P|,\quad p_{\mathrm{machine}}(\widehat C)=h.
$$

The other base seven-column components CNF, affine, FUS and INTERFACE are zero in this model. Each p is nonnegative, **invariant on the complete authentic zero-cost closure**, and every completed goal has p=0. Per-scale $p_j$ refines, rather than independently prices, the SEP part of the seven-component vector.

## 4. Exact nonnegative rule-by-component tariff theorem

**Theorem 046-A (all-transition characterization).** For nonnegative weights $\lambda_\Gamma,\lambda_M,\lambda_j$, the scalar potential

$$
\Phi(C)=\lambda_\Gamma(G-|P|)+\lambda_M h+
\sum_{j\in U}d_j\lambda_j
$$

satisfies $\Phi(C)-\Phi(C')\le w(C,C')$ for every legal transition if and only if

$$
\lambda_\Gamma\le1,\qquad
\lambda_M\le1,\qquad
\sum_{j\in S}d_j\lambda_j\le1
\quad\text{for every }S\in\mathcal E.
$$

**Proof.** VIEW/NOP have zero discharge. Every CHECK_ID has exactly $\Delta_\Gamma=1$ and zero other discharges, so its necessary/sufficient row is $\lambda_\Gamma\le1$. HALT discharges exactly $\Delta_M=1$. For an activation from pending set U using S, its exact per-scale discharge is $d_j$ for each $j\in S\cap U$, and zero otherwise. Since all weights are nonnegative, the largest such row is at $U=J$, which is reachable immediately after the gate checks; it yields precisely $\sum_{j\in S}d_j\lambda_j\le1$. All other activation rows are weaker. These are the complete transitions. QED.

Write $\theta_j=d_j\lambda_j$. Then optimizing the initial potential yields exactly

$$
\boxed{\max_\lambda\Phi(C_0)=G+1+\tau^*(\mathcal E)}
$$

with the **fractional set-cover linear-program dual pair**

$$
\tau^*(\mathcal E)=
\max_{\theta\ge0}
\left\{\sum_{j\in J}\theta_j:
\sum_{j\in S}\theta_j\le1\ \forall S\in\mathcal E\right\}
$$

$$
=\min_{y\ge0}
\left\{\sum_{S\in\mathcal E}y_S:
\sum_{S\ni j}y_S\ge1\ \forall j\in J\right\}.
$$

Finite LP duality applies since the covering family covers every j. The unrestricted optimal *record cost*, by contrast, is **exactly**

$$
\boxed{W_{\mathrm{record}}(C_0)=G+1+\tau(\mathcal E),}
$$

where $\tau$ is minimum **integer** set cover: every required identity CHECK costs one, then all pending j must be covered by paid batches, then HALT costs one. There is a valid path attaining that count. Thus a scalar linear tariff may be **strictly below even the true minimum record cost**.

## 5. Small exact counterexample: Fano-plane activation overlap

Take seven scales $j=5,\ldots,11$ and the seven permitted batches, indexed locally 0 through 6:

$$
012,\ 034,\ 056,\ 135,\ 146,\ 236,\ 245.
$$

Each scale lies in exactly three batches; any two batches meet in one scale. Three batches through local 0 cover every scale, and any two cover only five. Hence the minimum actual activation cost is $\tau=3$.

Choose $\theta_j=1/3$ for all seven; equivalently $\lambda_j=1/[3(4^j-1)]$. Every batch's weighted discharge is exactly one; the primal objective is $7/3$. Choose fractional dual $y_S=1/3$ for each of the seven batches. Each scale belongs to three batches, so its dual cover is exactly one; dual cost is $7/3$. Weak duality in both directions gives the **exact rational optimum**

$$
\boxed{\tau^*=7/3<3=\tau.}
$$

The complete optimal initial tariff is $G+10/3$ versus authentic cheapest record work $G+4$. For a fully enumerated laboratory with G=3, these become $19/3$ and $7$, respectively. Every activation leaves HALT pending, and shared gates are paid only once.

Second explicit control: three scales with allowed pairs 01,12,02 have $\tau^*=3/2<\tau=2$. Third, a genuine full-scale batch adds the inequality $\sum_j\theta_j\le1$, forcing $\tau^*=1$, matching the **original TMR-2/045** full-ACTIVATE authority. With singleton-only batches, $\tau^*=|J|=\tau$. The allowed primitive, not the exponential raw ranks, determines the tariff.

## 6. General multiscale no-go within this record calculus

**Corollary 046-B.** For every finite covered family $\mathcal E$ on q scales, $\tau^*(\mathcal E)\le\tau(\mathcal E)\le q$. Proof: choose for each scale one legal batch containing it. After deduplication there are at most q batches covering J. This is a feasible integer cover and hence an upper bound on the fractional optimum. Thus for the inherited shared-gate Feistel family, $G_m=O(m^3)$ and $q=m-4$, so every all-step nonnegative tariff of this per-scale form has

$$
\Phi(C_0)\le G_m+(m-4)+1=O(m^3).
$$

The input encoding is polynomial in m, so this cannot satisfy the required superpolynomial initial-gap premise. This theorem does **not** show a bound for an unrestricted, genuinely machine-history-aware obstruction with different coordinates; that remains OPEN.

## 7. Executed exact evidence, hostile controls and transfer gate

Exact serialized V8 audit was actually executed and published, covering four full permitted-batch hypergraphs: Fano, triangle, full-batch, and singleton. It independently computed the integer optimum by exhaustive subset DP, verified rational primal/dual certificates with integer numerators, enumerated all core pending/paid/goal states for a three-gate instance with both free views, checked **every** legal CHECK, batch activation, HALT, VIEW and NOP tariff row, and tested zero-cost invariance and terminal zero.

**Actual run:** 62,102 assertions; 24,730 legal edges evaluated; 12,560 zero-cost edges; **zero failures**. All finite evidence is COMPUTATIONAL, not the proof of the all-size theorem. Exact source: experiments/tmr/tmr2_fractional_batch_fusion116.js. Raw: results/raw/tmr/2026-11-15_0708_TMR2_BATCH116_V8_RAW.json. Machine-readable rule matrix: results/raw/tmr/2026-11-15_0708_TMR2_BATCH116_TARIFF_MATRIX.json. No OS Node execution, native machine compiler, or repository preflight is claimed.

The reused underlying CNF source is proper 3-CNF with exact compact AND/XOR extensions and one polynomial-size witness. Gaussian elimination on affine/Tseitin controls, Horn and dual-Horn propagation, Krom/SCC, bounded-treewidth separator DP, certified autarkies, equality/union-find, extension variables, clause learning, global preprocessing, shared DAGs, caching, rereading, recomputation, padding and renamed source syntaxes remain possible cheap operations for any actual decider. The new exact record system already admits maximum allowed batched sharing; the full-batch case explicitly tests the most destructive compact activation. No resolution-only lower bound or unverified Schaefer-class hardness is invoked. The exact-2P2N near-q-Horn radius remains a separate restricted component, not a branch-count theorem.

No result here transfers an authenticated record CHECK or a restricted batch menu to every correct physical multitape SAT machine. A real recognizer of the canonical original source can obtain a satisfying witness in polynomial time; that cheap path must be retained. The same-system arbitrary-program SAT transfer gate and genuinely superpolynomial initial obstruction both remain **OPEN**.

**Tracker disposition:** TRACKERS REVIEWED; NO MATERIAL CHANGE. TMR-5 alone owns canonical root synthesis; root proof1/proof2/main and all five existing agent schedules are untouched. Historical /341 full logical authority FAIL and /386 RESTRICTED.

**Peer handoff:** TMR-3 audit authentic per-batch cost, overlapping discharge and shared gate identity count; TMR-4 replay zero-cost SCC, exact fractional primal/dual, complete MAY transition insertion (especially global full activation); TMR-5 independently inspect Fano cover cardinality and strict 3 versus 7/3 integrality gap; TMR-1 preserve the separate SAT-machine transfer gate and block any use of this restricted record LP as a P-versus-NP result.

**One next research target:** develop a physically necessary, program-agnostic post-observation obstruction in which every legal all-program transition carries a verified bounded multi-scale discharge, even after admitting all compact shared computation. The restricted fractional-cover equality by itself cannot supply it.

**P versus NP remains OPEN.**
