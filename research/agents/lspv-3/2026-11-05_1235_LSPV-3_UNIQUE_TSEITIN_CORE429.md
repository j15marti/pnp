# LSPV-3/429 | Unique essential-clause core of odd cubic Tseitin CNFs
**2026-11-05 12:35 PST | Route B | PROVED/EXACT (direct CNF family) + COMPUTATIONAL checks | P versus NP OPEN**

## IDEA -> SEARCH -> ITERATE
Initial IDEA: seek simultaneous exact minimum work and dependency depth for a previously published Resolution-hard 3-CNF odd Tseitin family. Its proposed $W_R=4h-1$, $D_R=\lceil\log_2(4h)\rceil$ already appears in `research/agents/lspv-3/2026-11-03_1324_LSPV-3_BALANCED_DEPTH_NONTRANSFER373.tex` (blob `83406eb4...`) and LSPV-1/423 (blob `9f261f09...`); this is **duplication, NOT a new result**. Revised IDEA: for connected cubic graphs with articulation points, can *every individually nonessential original clause* be simultaneously removed, leaving a unique minimally UNSAT core? Falsifiers: bridged graph whose retained essential clauses are SAT; loss of individual core minimality; prior proof of exactly this simultaneous deletion; a supposed lower bound failing under existing AND3/GF(2) shortcuts.

## Family/theorem/encoding/known-method ledger
Let $G=(V,E)$ be any connected simple cubic graph with $h=|V|$, $n=|E|=3h/2$, and odd vertex charge $\chi:V\to\mathbb F_2$. For each vertex $v$ and each 3-bit word $a$ with $\bigoplus a=1\oplus\chi(v)$, include the unique signed proper 3-clause $C_{v,a}$ falsified exactly by $a$ on the three incident original edge variables. Original source IDs are kept, $m=4h$ distinct width-three clauses, canonical decimal DIMACS encoding $N=\Theta(h\log(h+2))$ bits. Summing vertex parity constraints yields $0=1$, certifying UNSAT. Even total charge is SAT with $2^{n-h+1}$ assignments.

**Known bound, precisely restricted:** Ben-Sasson–Wigderson, *Short Proofs Are Narrow* (JACM 48(2), 2001, Theorem 4.4 and Corollary 4.5) plus cubic edge expanders: ordinary unrestricted shared-DAG Resolution width $\Omega(h)$ and size $2^{\Omega(h)}$. Urquhart (JACM 34(1), 1987) provides related Resolution hard examples. No claim about arbitrary SAT machines or mixed refutations follows. **Known shortcut:** for bridgeless cubic graphs the preselected `R_mix341` has a $4h-1$ node AND3/GF(2) proof (LSPV-2/341); in general the same full-source construction is an upper bound $4h-1$, not always an exact minimum. Cook Extended Resolution and GF(2) are mandatory model controls. This run does not transport Haken PHP or bit PHP lower bounds through an unaudited 3-CNF encoding.

## Prior theorem (LSPV-3/125 and /134, not new)
For each vertex $v$, let $G-v$ have $c_v$ connected components $H$. An original clause $C_{v,a}$ is *essential* iff $F\setminus\{C_{v,a}\}$ is SAT, iff for every component $H$:
$$
\bigoplus_{e\in E(v,H)} a_e=\bigoplus_{u\in H}\chi(u).
$$
Exactly $2^{3-c_v}$ local clauses are essential. Define $\mathcal E$ as the original-ID-retaining collection of all essential clauses and $M(G)=|\mathcal E|=\sum_v2^{3-c_v}$. Source reports: `research/agents/lspv-3/2026-10-25_2256_LSPV-3_TSEITIN_CLAUSE_CRITICALITY125.tex` (blob `35eba48e...`) and `2026-10-26_0759_LSPV-3_VERTEX_CUT_CRITICALITY134.tex` (blob `83329b9a...`).

## Theorem 429.1 (new project-level global extension, PROVED/EXACT)
For every connected simple cubic graph $G$ and odd charge $\chi$, the conjunction of exactly the essential source clauses $\mathcal E$ is **UNSAT and is the unique inclusion-minimal UNSAT subformula** of the original $F_{G,\chi}$. Thus all $4h-M(G)$ nonessential clauses can be deleted *simultaneously*.

**Proof.** Let $x$ be any complete edge assignment and set $S=\{v:\bigoplus_{e\ni v}x_e\ne\chi(v)\}$. Each edge contributes twice to the vertex parity sum, hence $|S|$ is odd and nonzero. For a violated clause at $v\in S$ to be essential, the prior component criterion is equivalent to requiring that **every component of $G-v$ contain an even number of vertices of $S\setminus\{v\}$**: XOR all parity discrepancies within each component, leaving precisely its boundary edge values at $v$. Choose any spanning tree of $G$ and its minimal subtree spanning $S$. When $|S|=1$, take its only vertex; otherwise take a leaf $v$ of the minimal subtree, necessarily in $S$. Every other $S$-vertex is connected to every other through this subtree with $v$ removed, hence all $|S|-1$ other mismatches belong to a single component of $G-v$; that number is even. All remaining components contain zero mismatches. By the old exact local criterion the clause violated at $v$ is essential. Therefore **every** $x$ violates some $C\in\mathcal E$, proving $\mathcal E$ UNSAT. Every unsatisfiable original subformula must contain each individually essential $C$, since the full $F\setminus\{C\}$ is SAT. Consequently every UNSAT subformula contains $\mathcal E$, and since $\mathcal E$ is UNSAT it is inclusion-minimal and is the unique such core. QED.

A connected loopless graph with arbitrary positive vertex degrees admits the analogous statement for the *full* direct parity CNF, with $2^{d_v-c_v}$ essential local forbidden assignments; this extension may be wider than 3-CNF. The declared model and published hard 3-CNF testbed here remain cubic.

## Consequence for all legal binary-premise shared proofs
In unchanged `R_mix341`, original source clauses are free, each non-source node costs one, has at most two explicitly named premises, and DEF is conservative. Every $C\in\mathcal E$ must appear as a source ancestor of the contradiction, since otherwise the used original sources form a subset of satisfiable $F\setminus\{C\}$. For $M$ required source vertices and $q$ paid vertices, undirected ancestry connectivity and binary indegree give $M+q-1\le2q$, hence
$$
\boxed{M(G)-1\le W_{R_{\mathrm{mix341}}}(F_{G,\chi})\le4h-1.}
$$
In the ideal fan-in-two parallel logical model, dependency depth is at least $\lceil\log_2M(G)\rceil$. The balanced all-source AND3/GF(2) proof achieves $4h-1$ paid work and $2+\lceil\log_2h\rceil$ depth. These lower bounds are **linear/logarithmic** only; they do not imply arbitrary-machine runtime, a superpolynomial mixed minimum, or B3. Do not add case-split, discharge, weakening or context-free branch reuse rules to historical `R_mix341`.

## Independent finite controls (COMPUTATIONAL)
A Python generator produced exact signed DIMACS, source IDs, every essential single-deletion SAT witness and the essential core; a separately authored JavaScript verifier parsed and SHA256 authenticated the sources, independently calculated components and GF(2) deletion feasibility, ran complete DPLL on each essential core, checked even-charge SAT controls, and rejected malformed and corrupted records. **7,208 independent assertions, 10 negative rejections**, all passed.

| Named graph | $h$ | Original clauses | Essential core clauses | Simultaneously removable |
| --- | ---: | ---: | ---: | ---: |
| K4 | 4 | 16 | 16 | 0 |
| Two bridged subdivided K4 blocks | 10 | 40 | 36 | 4 |
| Three-block chain | 16 | 64 | 56 | 8 |
| Three-arm star | 16 | 64 | 55 | 9 |

This confirms controls, not the asymptotic proof by measurement. Both producer and checker binaries, source/witness fixture, per-instance hashes, independent JSON and SHA-256 manifest reside in the local full reproducibility archive; the GitHub compact checker and summary below provide independently runnable public controls.

## Search / duplication / limitations
Read governing November 2 handoff, current issue #3 and latest five-role reports, AGENTS.md, CODEX.md, the pnp-research skill, original `R_mix341` /341, source criticality /125 and /134, local solver /355, exact dual-optimum /373 and LSPV-1/423, Grok `GROKPROOF/2026-11-05_0315_PROGRESS.md` and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`. Search terms included `G-v connected essential clauses`, `unique minimal UNSAT core Tseitin`, `all inessential redundant together`, and `bridge Tseitin 36 40`. The existing per-clause formula was retrieved and respected; no exact previously proved simultaneous-core theorem was identified; no external novelty is claimed. External files: `konard/p-vs-np/README.md` blob `0e0ec77...` and `proofs/p_not_equal_np/README.md` blob `3a0304...`; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693...`; `meelgroup/frat-xor/format.md` blob `986a21...`; `tanyongkiam/cake_lpr/README.md` blob `e94f45...`; `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` blob `1ced21...`. None supplies the required same-`R_mix341` B3. A direct Google-branded session was unavailable; indexed research search and authenticated GitHub were used. Root `main.tex` returned SHA `1b8a7d9...` but zero bytes on ranged fetch, and was **not overwritten**.

## Physical cost and next gap
Ideal weighted work, parallel span, explicit evidence bits, certificate construction/verification and machine time/peak space are different. Explicit original DIMACS is $\Theta(h\log h)$ bits; checking graph components and source criticality is polynomial in $h$; enumerating deletion witnesses, brute force and DPLL may use additional exponential work, not charged in ideal proof minimum. In any actual solver/compiler charge parsing, input/index/head probes, proof production/checking, failed paths, references, caches, output and all-phase peak storage (including allocate-and-free). No arbitrary-machine lower bound follows.

**Next LSPV-3 transfer target:** Test a genuine superlinear representation-invariant native mixed minimum on an **already published nonaffine 3-CNF proof-hard family**, or derive an exact source-bound typing obstruction for paid DEF/LOCAL/XOR branching with assumption-safe sharing. Identify stronger legal short proofs instead of excluding them. B1/B2/B3, a superpolynomial $\overline W_R$, full historical normalization and P versus NP remain **OPEN**.

**References:** Urquhart, JACM 34 (1987), 209–219; Ben-Sasson and Wigderson, JACM 48 (2001), 149–169; Cook, SIGACT News 8 (1976), 28–32; Cook and Reckhow, JSL 44 (1979), 36–50.
