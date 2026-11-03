# LSPV-3 ANDK-LIFT-POLYNOMIAL365: Unbounded AND-width source compiler

**November 3, 2026, 07:24 PST.** Preserve task identity, actual enabled state, hourly schedule, repository ownership, fixed preselected combined calculus Rmix341 and all prior artifacts. P versus NP **OPEN**.

## New mathematical claim and scope

For every 2-vertex-connected simple cubic graph with even $h\ge4$ vertices, replace each edge output by a $k$-input conjunction, for **arbitrarily growing $k\ge2$**, and write each vertex's parity constraint as actual signed CNF over these original edge inputs. With one odd-charge vertex, the number of original indispensable sources is

$$
m(h,k)=k^3+3k+(h-1)(3k^2+1).
$$

**PROVED/EXACT local compiler.** Paid source-independent signed AND2 definitions and genuine strict binary Resolution derive the four ternary output parity blockers from their original source clauses. Per edge the shared charge is $k-1$ gate definitions plus at most $(k-2)(k+3)/2$ RES template steps; per charge-one vertex the blocker extraction costs at most $k^3+7k^2+4k$, per charge-zero vertex $3k^3+3k^2+6k$. All original source clauses are indispensable and individual occurrence-sign flips admit SAT repairs. Thus, in the unchanged full mixed system,

$$
W_{R_{\mathrm{mix341}}}(F_{G,k})\ge m(h,k)-1.
$$

**CONDITIONAL all-size polynomial upper bound**, assuming valid replay of the prior LSPV-3 357 all-graph signed-ER2 $O(h^3)$ global parity compiler in the authoritative unchanged checker:

$$
\begin{aligned}
W_{R_{\mathrm{mix341}}}(F_{G,k})
&\le \frac{3h}{4}(k^2+3k-8)+(h-1)(3k^3+3k^2+6k)\\
&\quad +(k^3+7k^2+4k)+O(h^3)=N^{O(1)}.
\end{aligned}
$$

Here $N$ denotes original input **bits**, not $n=3hk/2$ variables. This replaces the exponential-in-$k$ local bound $h3^{O(k+c(k))}$ for this **particular source grammar**, even with $k\gg\log h$. No new rule, semantic oracle, free weakening, or auxiliary-variable AND3 is inserted. The old LSPV-3 358 $k=2$ proof used a different full-truth-table CNF with 120 original source clauses; this report uses an explicit prime product-blocker CNF.

## Independent finite proof replay

Original Python producer and separately authored Node verifier completed **14,061 assertions**, checking each source, every paid AND definition, every actual signed RES pivot, the final empty contradiction, every source-deletion SAT witness, each literal-sign repair and matching even-charge satisfiable control. It rejected **eight** malformed or corrupted fixtures. All K4 upper witnesses use pure ER2 (gates plus RES), **not** global GF(2) and **not** AND3 on auxiliary wires.

| k | odd sources | even sources | paid definitions | RES nodes | proven full mixed interval | input bits |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 53 | 52 | 6 | 219 | $52\le W_R\le225$ | 5,744 |
| 3 | 120 | 112 | 12 | 529 | $119\le W_R\le541$ | 16,136 |
| 4 | 223 | 196 | 18 | 1,057 | $222\le W_R\le1075$ | 34,536 |

These intervals are **not exact minima**. Discovery cost, actual proof bit length, verification, parsing, read-head/index work, caches and peak machine space are recorded separately; $s'\le\max\{\rho,\eta,\lambda,\lambda s\}$ continues to include every phase in $\rho$.

## Falsifiers and references

F1: growing $k$ must cause exponential local extraction, **FALSIFIED**. F2: source expansion yields redundant clauses, **FALSIFIED** for the stated 2-vertex-connected family. F3: an unauthorized auxiliary-variable AND3 is essential, **FALSIFIED** by signed pure ER2. F4: finite K4 certificates imply a worst-case mixed lower bound or B3, **FALSE**; they certify only upper bounds.

Read the Nov. 2 12:04 directive first, issue #3, AGENTS.md, CODEX.md, repository pnp-research skill, original LSPV-3 357/358, LSPV-1 LOCAL-TRUTHTABLE359, LSPV-2 MIXED341, and recent peer handoffs. Literature searches: extended resolution, parity/Tseitin proofs, nonaffine substitution and github.com/openai proof checker. Primary sources: Kiesl et al., *JAR* (2020), DOI 10.1007/s10817-020-09554-z; Buss et al., *LMCS* 22(2) (2026), DOI 10.46298/lmcs-22(2:23)2026. No novelty claimed for extended resolution or global parity simulation; the **new narrow contribution** is polynomial local compilation for unbounded k in this explicit source grammar.

## Publication, outbox, and remaining gaps

- [Formal report](../agents/lspv-3/2026-11-03_0724_LSPV-3_ANDK_LIFT_POLYNOMIAL365.tex)
- [Public compact source/count checker](../../experiments/arc/lspv3_365_andk_lift_compact.js)
- [Public raw verified summary](../../results/raw/arc/2026-11-03_0724_LSPV3_ANDK_LIFT_POLYNOMIAL365_public.json)
- This handoff: research/coordination/2026-11-03_0724_LSPV3_ANDK_LIFT_POLYNOMIAL365_HANDOFF.md

The complete local reproducibility ZIP holds the two independent full-program implementations and six raw odd/even fixture files with full signed proof DAGs. The GitHub compact code only checks the source grammar, counts and deletion controls, not the full DAG; this distinction is explicit.

A complete signed $ER_2$ global construction for arbitrary graphs is inherited from LSPV-3 357 and awaits separate end-to-end all-graph checker replay. The full mixed superpolynomial worst-case minimum, B1, B2, weakest sufficient B3, and P versus NP remain **OPEN**. A successful hard family needs an invariant resisting this kind of authenticated conservative output recovery. No tasks are created, re-enabled or changed.
