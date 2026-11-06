# LSPV-4/442: Bounded unit-propagation avalanches and surviving branches on cubic Tseitin expanders

**2026-11-06 08:53 PST | Route A primary | PROVED/RESTRICTED mathematical lemma + COMPUTATIONAL finite checks | P versus NP OPEN**

## 1. IDEA -> SEARCH -> ITERATE, falsifiers

**Hypothesis:** The LSPV-4/437-438 no-shrink observation survives *full unit propagation*, not merely initial clause restriction, on a published exponential-Resolution-hard cubic Tseitin expander family. The potentially falsifying mechanisms were (F1) a logarithmic initial edge assignment causes an extensive unit-propagation avalanche; (F2) one valid branch survives only by an unjustified oracle; (F3) most nonconflicting branches disappear, defeating a proposed explicit-output cost; and (F4) an algebraic GF(2) or other legal shortcut renders the model-specific conclusion irrelevant to unrestricted SAT. F4 is real and explicitly retained; the theorem is confined to a stated branching+UP+materialization architecture.

Current primary references: Urquhart (JACM 1987, DOI 10.1145/7531.8928), Ben-Sasson--Wigderson (JACM 2001, DOI 10.1145/375827.375835), Fortnow--Lipton--van Melkebeek--Viglas (JACM 2005, DOI 10.1145/1101821.1101822). Bootstrap activation comparison: Coja-Oghlan, Feige, Krivelevich, Reichman, *Contagious Sets in Expanders*, SODA 2015, DOI 10.1137/1.9781611973730.131. This elementary edge-counting argument is not claimed novel in bootstrap-percolation theory.

## 2. Established family, original exact 3-CNF, and hardness scope

Let $G=(V,E)$ be a **simple connected 3-regular graph** on $H$ even vertices and $M=3H/2$ edges; assign one Boolean variable $x_e$ to each edge and charges $\chi_v\in\{0,1\}$. For the increasing edge indices $a_v,b_v,c_v$ at vertex $v$, include exactly four *original proper signed ternary clauses*:

$$
C_{v,p,q}=\ell_p(x_{a_v})\vee\ell_q(x_{b_v})\vee
\ell_{p\oplus q\oplus1\oplus\chi_v}(x_{c_v}),
\qquad p,q\in\{0,1\},
$$

where $\ell_0(x)=x$, $\ell_1(x)=\neg x$. Thus $|F|_{\rm clauses}=4H$, $|\operatorname{vars}F|=3H/2$ and an explicit fixed-width signed literal packet has $N=\Theta(H\log H)$ bits. A concrete historical source grammar with exact sizes is in LSPV-2/446 (blob `6176af08`) and the Hamiltonian special case in LSPV-4/440. The theorem below uses the **original clauses**, not free algebraic rows or an equisatisfiability-only replacement.

If $G$ is connected, $F$ is SAT iff $\bigoplus_v\chi_v=0$. Odd charge is therefore **certified UNSAT** by an independent GF(2) parity invariant. Suitable growing 3-regular edge-expander graphs with odd charges have exponential $2^{\Omega(H)}$ refutation-size lower bounds **for ordinary unrestricted shared-DAG Resolution**, as in Urquhart and the Ben-Sasson--Wigderson width-size framework. This is **not** a mixed-$R_{\mathrm{mix341}}$, Extended Resolution, GF(2), or unrestricted-machine lower bound. The finite K4/cube/Petersen/Heawood/random-regular controls here are not asymptotic hardness certificates.

Write the edge expansion

$$
h=\min_{\varnothing\ne U\subseteq V,\ |U|\le H/2}
\frac{|\partial U|}{|U|}>0.
$$

For an asymptotically hard family, require a fixed $h=\Omega(1)$, not merely a positive finite-graph value.

## 3. Theorem 442.1: unit-propagation containment (PROVED/RESTRICTED)

Choose an *arbitrary, possibly adaptively discovered* set $S\subseteq E$ of $k$ edges, fix arbitrary Boolean values on those edges and exhaustively apply ordinary CNF **unit propagation**, stopping if a conflict is found. Let $R$ be the additional edges forced before stopping and $A$ the threshold-2 bootstrap closure of the at-most-$2k$ vertices incident to $S$: a vertex activates when at least two of its distinct neighbors were previously activated.

If

$$
k<\frac{(1+h)H}{16},
$$

then

$$
|A|\le\frac{8k}{1+h},\qquad
|R|\le |A|\le\frac{8k}{1+h}.
$$

Consequently, at least

$$
\boxed{\ 4\left(H-2k-\frac{16k}{1+h}\right)\ }
$$

original **ternary** clauses remain unchanged throughout the UP computation (negative values make the trivial lower bound zero). The bound holds for every partial branch, including ones for which UP eventually detects a local contradiction; only a nonconflicting leaf is interpreted as a residual input.

**Proof.** With at most one incident edge fixed, the four original parity clauses reduce to binary clauses or satisfied clauses, not unit clauses. A unit edge deduction occurs only when the vertex already has two assigned incident edges. Every edge forced this way finishes its *issuing vertex*, so a vertex issues at most one distinct new edge. If a vertex is not among the original seed endpoints, its two preceding known edges must have come from earlier issuing vertices among its distinct neighbors. By induction every issuing vertex belongs to the threshold-2 closure $A$, hence $|R|\le |A|$.

For every prefix $U$ of $A$ with $|U|\le H/2$, each newly activated nonseed vertex contributes two distinct edges to earlier active vertices. Thus, writing $s\le2k$ for the number of seeds,

$$
2(|U|-s)\le e_G(U)
=\frac{3|U|-|\partial U|}{2}
\le\frac{(3-h)|U|}{2},
$$

whence $(1+h)|U|\le4s\le8k$. Under the displayed strict hypothesis the process cannot reach $H/2$ active vertices, so the same estimate holds for its final $A$. Finally at most $k+|R|$ edges are assigned. Each touches at most two vertices, leaving at least $H-2(k+|R|)$ vertices with **all three incident variables untouched**, each still containing four original ternary clauses. QED.

This does **not** cover probing general learned binary clauses, failed-literal probing, Gaussian elimination, extension variables, or the fixed mixed calculus.

## 4. Theorem 442.2: nonconflicting branches cannot all be pruned (PROVED/RESTRICTED)

Suppose additionally that $G$ is **3-edge-connected** and

$$
H>\frac{32k}{1+h}.
$$

Let $c$ be the number of components of $G\setminus S$. Then **at least**

$$
\boxed{2^{k-c+1}}
$$

of the $2^k$ assignments to $S$ produce no contradiction by unit propagation. For $c\ge2$, 3-edge connectivity gives $3c\le2k$ and hence at least $2^{k/3+1}$ UP-noncontradictory assignments. For $c=1$, all $2^k$ assignments have this property under the displayed small-$k$ assumptions.

**Proof.** The threshold-2 closure $A$ depends only on the *selected edges*, not their assigned values. All initially or subsequently assigned edges touch $A\cup N(A)$, whose size is at most $4|A|\le32k/(1+h)<H$. Fix a vertex $v$ outside that set; no unit-propagation step can assign an incident edge of $v$.

Delete only the parity equation at $v$. The remaining $H-1$ rows are linearly independent on a connected graph. After fixing values on $S$, the equations on each component of $G\setminus S$ other than the one containing $v$ impose exactly one independent parity consistency equation on the selected boundary edges. The contracted component graph is connected, so these $c-1$ equations have independent rows. Exactly $2^{k-c+1}$ assignments to $S$ extend to a full edge assignment satisfying every vertex equation except possibly the one at $v$. CNF unit propagation cannot contradict one of these near-solutions because all used parity constraints outside $v$ are satisfied, while no clause at $v$ can become empty or unit. If $c\ge2$, each proper component has cut size at least 3; summing component cuts yields $3c\le2k$. QED.

**Important:** the near-solution is **not** a SAT witness of an odd-charge Tseitin source. It is a witness that *unit propagation alone* does not yet discover its global inconsistency.

## 5. Consequence for explicit child-output architecture

For a constant-expansion 3-edge-connected cubic family with $N=\Theta(H\log H)$ and $k=\lceil(3/5)\log_2N\rceil$, both strict hypotheses hold for all sufficiently large $H$. Any **specified compiler which enumerates and explicitly emits every UP-noncontradictory residual as a separate full signed-CNF guest input**, rather than employing legal semantic pruning, compact shared representations or a GF(2) shortcut, must emit at least

$$
\Omega\left(2^{k/3}\,H\log H\right)
=\Omega(N^{6/5})
$$

bits total. A single such materialized residual also occupies $\Omega(N)$ simultaneous writable space if held on a work tape. These costs exceed the proposed $N^{11/10}$ aggregate local-time and $N^{1/2}$ writable-peak targets **for precisely this explicit materializing branch-and-UP compiler**. This is not a lower bound against a solver that aggregates branches, streams non-materialized queries, recognizes parity, learns lemmas, changes representation, or never calls the guest.

The special-family GF(2) shortcut decides SAT/UNSAT in nearly linear time and small workspace, so the result cannot be used to claim unrestricted SAT complexity hardness. It is an architectural falsifier for Route A only; the all-input recursively iterable contraction and same-machine fully charged transfer remain **OPEN**.

## 6. Executed computational verification and audit limits

The executed Python producer checked both odd and even charges, every $k\le3$ selected edge set and its every assignment on K4, cube, Petersen and Heawood, plus all $k\le2$ sets on a fixed seeded random cubic graph with $H=20$. Python checked **39,394 branch records, 236,364 grouped assertions**, comparing an explicit signed-3CNF UP implementation against an independently expressed graph-parity closure; original unchanged-clause counts, forced-edge bounds and the expansion inequality were checked. Exact finite $h$ was exhaustively computed by vertex subset enumeration. Small graphs with at most ten vertices received exhaustive SAT controls; larger controls were checked by parity identity. An independently authored JavaScript verifier reconstructed the graph clauses and all branch records and passed **79,488** checks. A second Python rank/survivor verifier passed **14,906** assignment tests, checking the exact $2^{k-c+1}$ extension count wherever an untouched defect vertex was available. Malformed-degree, repeated-ID and corrupted-sign source controls were rejected. These are host-language tests, not native FLMV machine traces or mixed-calculus certificate replays.

Graph/branches: K4 466; cube 4,098; Petersen 8,182; Heawood 23,046; seeded 20-vertex cubic 3,602. The finite seeded graph has edge connectivity 2 and is not used for the 3-edge-connected theorem. Local scripts and original finite fixtures are retained with a SHA-256 manifest in the reproducibility archive.

## 7. Full resource-accounting ledger

- **Logical $R_{\mathrm{mix341}}$ inference nodes:** not constructed; none counted; fixed weights/rules unchanged.
- **Original-source bits:** $N=\Theta(H\log H)$ explicit signed 3-CNF. Odd-charge UNSAT is independently mathematically certified, not an authenticated mixed proof.
- **Offline mathematical minimum:** free optimal legal branch and sharing choices remain allowed; this experiment does not bound their cost.
- **Actual host execution:** Python brute-force subset enumeration, input graph construction, CNF materialization, search and checks consume host memory/time that are NOT asserted to satisfy the FLMV envelope.
- **Restricted hypothetical explicit compiler:** selected-edge discovery, source authentication, branch enumeration and failed policies must still be charged. The displayed $\Omega(N^{6/5})$ emitted-bit count is a model-specific lower bound even if all remaining phases are free; eager single-child storage is $\Omega(N)$.
- **Actual algorithm escape routes:** source-parity checking, cancellation/caching, learned clauses, shortened guest inputs, nonuniform advice (not free), local conversion, dense/sparse boundary data, and shared branching DAGs require their own legal semantics and full charges. Source-to-guest conversion and reference/recomputation cannot be silently omitted.
- **Machine model:** a counted emitted bit needs at least one step on the stipulated fixed-alphabet indexed-input random-access machine; explicit materialization needs one work bit per stored bit. Arbitrary guest execution and timing are not benchmarked here.

## 8. Sources inspected, authenticity and limitations

Governing project: `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, current issue #3, AGENTS.md, CODEX.md and `.codex/skills/pnp-research/SKILL.md`. Relevant actual reports: LSPV-4/437 (`2026-11-06_0336_LSPV4_MATCHING_BRANCH_NO_SHRINK437.md`), /438 (`2026-11-06_0444_LSPV4_EXPANDER_EDGE_DELETION_GIANT_COMPONENT438.md`), /441 (`2026-11-06_0736_LSPV4_GUARDED_FALLBACK_BLACKBOX441.md`, blob `704db91d`), LSPV-2/443 (`aedb2d86`), /444 (`0bb58542`), /446 (`6176af08`), actual Grok `GROKPROOF/2026-11-06_0515_PROGRESS.md` (`93f9202d`) and Claude `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex` (`b7150bb9`).

External repositories inspected: `konard/p-vs-np/scripts/proof_status.json` (`93b77ed`), `blkph0x/p-vs-np-proof-research/CERTIFIED_RESIDUAL_QUOTIENT_REPORT.md` (`b37da20a`), `RESIDUAL_EQUIVALENCE_BARRIER_REPORT.md` (`46413596`), `METHOD_INDEX.md` (`18d693ea`), `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` (`4bb5fd`) and `meelgroup/frat-xor/README.md` (`38a137b`). These are distinct techniques and checker interfaces, not authorities for a universal proof. Web primary literature was searched using the available web search; no claim of Google-branded search, full source-code execution of external repositories, native FLMV benchmarking, root main.tex reconciliation, or complete corpus-wide preflight.

**Actual advance:** logarithmic-branch unit-propagation avalanche containment *plus a surviving-branch count* for original hard-in-Resolution cubic Tseitin 3-CNFs. **OPEN:** genuine all-input solver-dependent SAT shrinkage, full time/space charging and hereditary same-machine contraction; separate Route B mixed-calculus lower bound and noncircular B3. **P versus NP remains OPEN.**
