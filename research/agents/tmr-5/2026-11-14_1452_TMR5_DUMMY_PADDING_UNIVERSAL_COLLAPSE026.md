# TMR-5/026: Exact circuit-complexity invariance under dummy-input padding and universal positive-power YES collapse

**Pacific timestamp:** 2026-11-14 14:52 PST. **Owner:** TMR-5 Machine Bottleneck Redteam and synthesis. **Status:** PROVED/RESTRICTED elementary circuit lemma, awaiting TMR-1/TMR-4 independent review; exhaustive finite test COMPUTATIONAL; unrestricted P versus NP remains OPEN.

## 1. New result versus previous work

TMR-4/030 showed that one particular compiler, the full table of $H_{F,t}(x,z)=F(x)\wedge\bigwedge_jz_j$, eventually has a circuit smaller than any positive-power threshold $N^\mu$. This run proves a strictly **more general** obstruction: **every** explicitly supplied Boolean truth table, whether produced by a SAT compiler or otherwise, becomes an ordinary MCSP YES instance if enough *unused high-order inputs* are appended while the size threshold is recalculated as a fixed positive power of the new table length. Exact minimum circuit size is unchanged by this padding.

This result rules out **dummy-input truth-table repetition as an automatic threshold-preserving amplification** even for arbitrary syntax-aware, globally preprocessed, polynomial-output reductions. It does **not** rule out nontrivial encoding/reduction schemes, does not imply SAT hardness, and does not supply a lower bound for MCSP.

## 2. Source and historical ledger

Read FIRST the controlling \`research/coordination/2026-11-14_MCSP_FIVE_AGENT_REVIEW.md\` on main, then \`research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md\`, both entire root proof trackers, original root \`main.tex\`, \`AGENTS.md\`, \`CODEX.md\`, \`.codex/skills/pnp-research/SKILL.md\`, latest five role handoffs and latest issue #3 through TMR-4/030. Full authentic proof2 Git blob was 1,051,196 chars (930c5eeddafce656717f28055a7a9a755f44737c); full authentic main.tex Git blob was 2,545,859 chars (6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34); no unreadable-empty-file inference. proof1 was 28,714 chars (06f7ebc8c2283304a0f5200b518c6e48fa41e343). No shared tracker or manuscript edits.

| Original path | Prior claim and retained status |
| --- | --- |
| \`research/agents/tmr-4/2026-11-14_1439_TMR4_POSITIVE_POWER_COMPILER_FIREWALL030.md\`, original \`experiments/tmr/tmr4_power_compiler033.js\`, original raw | Narrow positive-power collapse of direct masked SAT compiler, exact restricted; independently checked its $v+3m+t-1$ circuit accounting by inspection |
| \`research/agents/tmr-4/2026-11-14_1336_TMR4_ORACLE_LOCALITY_GAP_MASK029.md\` | Source-independent black-box oracle-query locality, not a syntax-independent restriction |
| \`research/agents/tmr-2/2026-11-14_1417_TMR2_SHARED_ORACLE_PREPROCESS032.md\`, original code/raw | Global evaluation-query preprocessing $b$ plus local $q$ locality bound, restricted oracle model; not a general SAT reduction theorem |
| \`research/agents/tmr-1/2026-11-14_1357_TMR1_CAPMIN_REDUCTION_FRONTIER028.md\`, original code/raw | Near-linear symbolic small-threshold capped minimization, physical one-work-tape proof under peer audit; no $s=N^\mu$ lower bound |
| \`research/agents/tmr-3/2026-11-14_1327_TMR3_MCSP_RAWSCAN_HEADER_BOUND028.md\`, original code/raw | Raw-cache one-work-tape upper bound and separate advance-header variant, model-specific |
| \`research/agents/tmr-5/2026-11-14_1350_TMR5_MCSP_SYNTAX_CERTIFICATE_REVIEW025.md\`, original code/raw | Polynomial-output reverse-label NP=coNP conditional and easy syntax-aware counterexample, restricted |
| \`research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex\`, \`research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex\`, \`research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex\` | Historical compact-summary, one-tape and product controls; no general hardness transfer |

Legacy LSPV checker/normalizer accepted counterexamples, XOR/GF(2), Horn, 2-SAT, Walsh/moment, signed-hypergraph, TPORT and DIRECTPRODUCT controls remain valid only at their original scopes. No counterexample was removed.

## 3. Primary theorem matrix and exact boundary

| Paper/theorem | Model, threshold, hypothesis and conclusion |
| --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, [STACS 2021](https://doi.org/10.4230/LIPIcs.STACS.2021.23), **Theorem 1 p.23:3** | Ordinary **decision** MCSP on full $N=2^n$ truth table, AND/OR/NOT-size threshold $s(n)=2^{\mu_1 n}=N^{\mu_1}$ for a sufficiently small fixed $\mu_1>0$; deterministic one-way read-only input plus one two-way work tape. If not in $\mathrm{DTIME}_1[N^{1.01}]$, then $P\ne NP$. Premise **OPEN**. |
| Same, **Theorem 2 p.23:3** | Randomized bounded-two-sided-error one-work-tape lower bound outside $\mathrm{BPTIME}_1[N^{1.99}]$ at a **different, larger** $\mu_2$. Cannot substitute for Theorem 1. |
| Same, **Theorem 3 p.23:4** | For $1/2<\mu<1$, lower bound against randomized one-work-tape algorithms allowed arbitrary oracle with $N^{o(1)}$-length queries, at some exponent $1+\mu'>1$. Restricted locality/oracle barrier, not unconditional unrestricted SAT hardness. |
| McKay, Murray, Williams, [STOC 2019](https://doi.org/10.1145/3313276.3316396), **Theorems 1.2 and 1.3 p.2** | One-pass search-MCSP with **oracle-gate** circuits, $N=2^n$, constructible size $s(n)\ge n$; short $\Sigma_3SAT^A$ queries permit small-space streaming search; hypothetical lack of a suitable $\mathrm{poly}(s)$ space/update streamer for some $A\in PH$ implies $P\ne NP$. Not directly an ordinary decision-MCSP lower bound. |
| Chen, Hirahara, Oliveira, Pich, Rajgopal, Santhanam, [JACM 2022](https://doi.org/10.1145/3538391), locality-barrier analysis | Model and theorem hypotheses are not imported as an implication here. It warns that short-query methods and magnification assumptions cannot be freely combined; no transfer is asserted. |

In our independent result below $\mu>0$ is **any fixed positive real**, not necessarily the specific small $\mu_1$ in CHMY. Let $L$ be an independent SAT source encoding length; $n$ is only the **target Boolean arity**, and $N=2^n$ is the complete target table length.

## 4. Exact theorem DUMMY-PAD34

Use unrestricted-fanout DAG circuits over fan-in-two AND/OR and fan-in-one NOT, with free input wires and constants. Write $CC_n(f)$ for minimum gate count for $f:\{0,1\}^n\to\{0,1\}$. Define for $r\ge0$

$$
P_r(f)(x_1,\ldots,x_n,z_1,\ldots,z_r)=f(x_1,\ldots,x_n).
$$

The full truth table of $P_r(f)$ has $N'=2^{n+r}=N2^r$ bits. Under standard binary table indexing with low-order $x$ variables first, it is exactly **$2^r$ consecutive copies** of the original $N$-bit truth table.

**Theorem 34A (exact, basis-specified).**

$$
\boxed{CC_{n+r}(P_r(f))=CC_n(f)\qquad \text{for all }n\ge1,r\ge0,f.}
$$

**Proof.** The circuit for $f$ computes $P_r(f)$ by ignoring the dummy wires, proving $\le$. Conversely take any circuit $C$ for $P_r(f)$ and fix every dummy primary input to zero; its unchanged DAG now computes $f$. Propagating those constants, or simply regarding them as free constant inputs, cannot add gates. This proves the reverse inequality. The argument allows arbitrary gate sharing and nonlinear representations, without any assumption on the algorithm used to produce $f$. QED.

**Theorem 34B (universal polynomial-overhead positive-power collapse).** For every fixed $\mu>0$ and any $N=2^n$-bit full table $f$ with $n\ge1$, there is an integer $r=O_\mu(n)$ such that

$$
P_r(f)\in MCSP[\lfloor (N')^\mu\rfloor]
$$

**regardless** of the original function's circuit complexity. More precisely, define

$$
B(n)=n2^n+n+2,\qquad
n'=\max\left\{n,\left\lceil\frac{n+\lceil\log_2(n+2)\rceil+2}{\mu}\right\rceil\right\},\qquad r=n'-n.
$$

Every $n$-input function has an explicit DNF circuit of at most $B(n)$ gates: at most $n$ shared input negations, $n-1$ ANDs per one-output assignment, and at most $2^n-1$ ORs. Constants are handled with free 0/1 wires. Consequently

$$
CC_{n+r}(P_r(f))=CC_n(f)\le B(n)
\le \left\lfloor2^{\mu n'}\right\rfloor.
$$

The last inequality follows because $2^{\mu n'}\ge 4(n+2)2^n>B(n)$ for $n\ge1$; the flooring is harmless since $B(n)$ is an integer. The expansion satisfies

$$
N'=2^{n'}=N^{1/\mu+o(1)}
$$

for fixed $0<\mu\le1$ (and is at most $N^{O_\mu(1)}$ for every $\mu>0$). It is **polynomial in the length of the original explicit truth table**, with a $\mu$-dependent fixed exponent, not polynomial in a generally shorter SAT description. QED.

**Reduction corollary (exact restricted falsifier).** Take *any* hypothetical source-to-full-table transformation $R$ with $N(F)=\mathrm{poly}(L)$ and both-label correctness for some original target predicate. If one attempts to obtain hardness for a positive-power $MCSP[(N')^\mu]$ by **only repeating the target table through unused input variables**, with the $r$ above, the new output lands in MCSP YES for *every source*. Both-label preservation is destroyed whenever the source promise contains an original NO instance. This is true even if $R$ was syntax-aware, nonlinear, and globally preprocessed. The padding can be explicitly constructed in polynomial $N'$ time in a standard sequential-output model; a one-work-tape implementation must additionally charge all head movement/cache accesses, and is not presumed to run in $O(N')$.

For Gap-MCSP, the same padded table is at Hamming distance **zero** from a circuit within the new threshold, even though its normalized distance from an *old* comparison circuit such as constant zero is unchanged. Thus preserving relative Hamming density does **not** preserve the new Gap-MCSP NO promise.

## 5. Actually executed controls

Two independent execution environments were used. Native CPython executed \`/mnt/data/tmr5_padding_audit031.py\` locally, with 15,620 checks, zero failures (SHA256 \`5a4264cb96689e804eee2aac8fa14620cb7aa4d3de888457c9f49e1ab84cb398\`); this local-only script is **not** claimed as a GitHub artifact. A separate hosted-V8 implementation, the **exact** source published as \`experiments/tmr/tmr5_dummy_padding034.js\`, was executed, yielding the **exact** published raw \`results/raw/tmr/2026-11-14_1452_TMR5_PADDING034_RAW.json\`. Its 15,492 assertions, zero failures, cover:

* All 276 Boolean functions with 1, 2 or 3 inputs, explicit shared-negation DNF construction and exhaustive semantic checks.
* All $+1,+2$ dummy-variable padding checks on those functions.
* Independent complete AND/OR/NOT DAG circuit enumeration through two gates for $n=1,2$ and padding $r=1,2$, checking membership equivalence in thresholds 0, 1 and 2.
* Exact integer exponent and padded-length arithmetic for $\mu=1/2,1/3,1/10,2/5$ and $n=1,\ldots,32$ (no astronomically large truth tables materialized).

These finite checks validate implementation and small cases, not the asymptotic theorem by themselves. Neither is a compiled finite-state one-work-tape machine or a SAT lower-bound test.

## 6. Ranked synthesis, failed arrows, and next independent audit

| Rank | Route | Weakest still-OPEN lemma |
| --- | --- | --- |
| 1 | CHMY Theorem 1 | Prove **ordinary** $MCSP[N^{\mu_1}]\notin\mathrm{DTIME}_1[N^{1.01}]$ at the exact small $\mu_1$, both labels, on the specified one-way-input plus one-work-tape model |
| 2 | From the CHMY larger-threshold theorem to the magnification threshold | Uniform same-model reduction or new argument preserving threshold and exponent; current $\mu_2>\mu_1$ is a fatal mismatch |
| 3 | Arbitrary 3-SAT to positive-power MCSP | Full-table polynomial-$L$ output, true both-label map with threshold and promises; reverse polarity conditionally implies NP=coNP, not a contradiction |
| 4 | TMR-2/4 information/oracle and TMR-3 network tradeoffs | A charged unrestricted-algorithm bridge, not merely access/query/transport restrictions |
| 5 | TMR-1/3 small-threshold constructive upper bounds | Native one-tape correctness audit and fundamentally new large-threshold mechanism; current upper bounds do not establish hardness |

**FALSIFIED/RETIRED only as general implications:** dummy-input repetition as a universal positive-power threshold amplifier; direct $H_{F,t}$ compiler as a positive-power hardness source; uncharged succinct SAT-to-full-table expansion; treating periodic-query depth as full MCSP time; turning $N^{1.99}$ at $\mu_2$ into $N^{1.01}$ at $\mu_1$.

**Peer-review request:** TMR-4 should independently check the constant-substitution $\ge$ direction and explicit uniform DNF gate bound, and try a **nontrivial**, non-dummy syntax-aware output encoding that avoids size collapse. TMR-1 should check arity/output polynomial overhead and small $\mu$ exact theorem hypotheses. TMR-2 should test Gap-MCSP distance versus enlarged circuit class. TMR-3 should charge source-to-padded-output tape movement and networks. TMR-5 should next audit whether combining circuit-size lower bounds with transfer procedures can avoid a forced full-table expansion.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** \`proof1.txt\`, \`proof2.txt\`, and canonical \`main.tex\` were deliberately unchanged pending independent peer verification of this restricted new result. No scheduled agent was created, disabled, or modified. P versus NP OPEN.
