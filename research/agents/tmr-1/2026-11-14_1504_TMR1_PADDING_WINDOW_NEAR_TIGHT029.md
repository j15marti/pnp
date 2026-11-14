# TMR-1/029: A near-tight dummy-padding threshold transition for ordinary MCSP

**Pacific timestamp:** 2026-11-14 15:04 PST (America/Los_Angeles). **Role:** TMR-1 Machine Model Lead. **Status:** PADWINDOW35 PROVED/RESTRICTED at elementary circuit-counting level, independent TMR-5/TMR-4 review OPEN. The executed finite controls are COMPUTATIONAL. Neither P versus NP direction has been proved.

## 1. What is actually new

TMR-5/026 proved exact circuit-size invariance under adding dummy variables and gave a universal padding length $r=O_\mu(n)$ that makes every padded table MCSP YES at threshold $2^{\mu(n+r)}$. This run independently audits that construction and adds a **matching exponent lower bound**, by counting all bounded-gate circuits. For each fixed $0<\mu<1$, the least dummy-variable padding that guarantees ALL $n$-input truth tables become positive-power MCSP YES is

$$
\boxed{R_\mu(n)=\left(\frac1\mu-1\right)n+O_\mu(\log n).}
$$

Consequently the exact worst-case-universal output expansion is $N'=N^{1/\mu+o(1)}$ bits. The exponent $1/\mu$ is asymptotically necessary, not just sufficient, for this particular **universal YES-collapse objective**. This is a restricted threshold-geometry fact, not a transfer of an MCSP lower bound, a new SAT lower bound, or a constructive hard truth-table family.

## 2. Primary theorem and model firewall

| Original source and location | Exact used statement and model |
| --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021 [1], Theorem 1, printed p.23:3 | For some fixed sufficiently small $\mu_1>0$, if ordinary **decision** $MCSP[2^{\mu_1n}]$ on a **complete** $N=2^n$-bit truth table is outside deterministic $DTIME_1[N^{1.01}]$, then $P\ne NP$. $DTIME_1$ has one-way read-only input and one two-way work tape. The antecedent remains OPEN. |
| Same [1], Theorem 2, printed p.23:3 | At a *different, larger* $\mu_2$ close to 1, randomized bounded-two-sided-error one-way-input/one-work-tape machines cannot decide ordinary $MCSP[2^{\mu_2n}]$ within $N^{1.99}$ time. The exponent and threshold cannot be mixed with Theorem 1. |
| McKay, Murray, Williams, STOC 2019 [2], Theorems 1.2 and 1.3, printed p.2 | **Search**-$MCSP^A[s(n)]$ with $A$-oracle gates and time-constructible $s(n)\ge n$, on explicit $N=2^n$ input, has one-pass $\Sigma_3SAT^A$-oracle streaming algorithms with $\widetilde O(s)$ space and $\widetilde O(s^2)$ update; if an appropriate $A\in PH$ and $s$ admit no deterministic $\operatorname{poly}(s)$-space and $\operatorname{poly}(s)$-update streamer, $P\ne NP$. No direct identification with our plain decision-language or the $s=o(n)$ upper-bound regime. |
| Oliveira and Santhanam, FOCS 2018 [3], original ECCC 2018 TR18-139 abstract and author version | Hardness magnification for MCSP includes **average-case zero-error formula** lower bounds at $s=2^{\sqrt n}$ implying NP has no polynomial-size formulas. Its model and conclusion differ from the one-tape theorem; not imported into the proof below. |
| Chen, Hirahara, Oliveira, Pich, Rajgopal, Santhanam, JACM 2022 [4] | Hardness-magnification locality analysis. No specific implication is claimed from it here; it is a caution against moving a restricted query or proof technique into an unrestricted model. |

Here $n$ is target Boolean arity, $N=2^n$ its original **full** truth-table length, $r$ the new dummy-variable count, and $N'=2^{n+r}$. The length $L$ of any SAT source formula is **independent** and may be polynomial in $n$ or exponentially smaller than $N$; no SAT source-to-table operation is offered free. Circuits are nonuniform **DAGs with unrestricted fanout, fan-in-two AND/OR, unary NOT, and free primary inputs/constants**. All claims in this report concern gate count, not physical Turing-machine runtime.

## 3. Ledger of original project evidence, not chat claims

| Exact artifact | Scoped status and role |
| --- | --- |
| `research/agents/tmr-5/2026-11-14_1452_TMR5_DUMMY_PADDING_UNIVERSAL_COLLAPSE026.md` plus `experiments/tmr/tmr5_dummy_padding034.js` and `results/raw/tmr/2026-11-14_1452_TMR5_PADDING034_RAW.json` | Prior exact basis-specific padding invariance and coarse universal upper; this report independently proves a near-matching lower. Original native V8 source/raw inspected. |
| `research/agents/tmr-4/2026-11-14_1439_TMR4_POSITIVE_POWER_COMPILER_FIREWALL030.md` plus `experiments/tmr/tmr4_power_compiler033.js` | Earlier direct masked 3-CNF compiler gate cap $v+3m+t-1$. Restricted compiler, not a general source reduction. |
| `research/agents/tmr-1/2026-11-14_1357_TMR1_CAPMIN_REDUCTION_FRONTIER028.md` plus `experiments/tmr/tmr1_capmin031.py`, original raw | Previously published capped exact minimization for $s=o(n/\log n)$, with physical compiler peer review still open. Does not reach $s=N^\mu$. |
| `research/agents/tmr-2/2026-11-14_1417_TMR2_SHARED_ORACLE_PREPROCESS032.md` and original code/raw | Source-independent evaluation-oracle shared-query necessity. Syntax-aware algorithms are outside its hypothesis. |
| `research/agents/tmr-3/2026-11-14_1455_TMR3_TWOWAY_HEADER_NETWORK_BRIDGE029.md` and original code/raw | Two-way-input annotated-header transfer and charged network simulation, restricted model. Does not transfer CHMY's one-way input lower bound. |
| `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`, `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, `research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex` | Historical product, one-tape and fingerprint controls. No general all-algorithm bottleneck imported. |
| `research/agents/tmr-4/2026-11-14_0836_TMR4_MOMENT_CONGRUENCE_AND_QUOTIENT_COUNTEREXAMPLE023.md`, earlier Walsh/moment, Grok and legacy LSPV records | Compact algebra/continuation erasure and legacy accepted counterexamples remain historical scope controls, never hardness transfers by themselves. |

## 4. New exact restricted theorem and proof

Define $CC_n(f)$ as the minimal gate count of an $n$-input Boolean function. Let $P_r(f)(x,z)=f(x)$ add $r$ unused input variables. From TMR-5/026 (independently checked), with constants free,

$$
CC_{n+r}(P_r(f))=CC_n(f).
$$

Define the maximum circuit complexity among $n$-input functions, and the first universal padding threshold,

$$
U(n)=\max_{f:\{0,1\}^n\to\{0,1\}} CC_n(f), \qquad
R_\mu(n)=\min\{r\ge0:\lfloor 2^{\mu(n+r)}\rfloor\ge U(n)\}.
$$

**PADWINDOW35, PROVED/RESTRICTED, independent review pending.** For every fixed $0<\mu<1$,

$$
\boxed{R_\mu(n)=\left(\frac1\mu-1\right)n+O_\mu(\log n)}
\quad\text{and}\quad
\boxed{2^{n+R_\mu(n)}=N^{1/\mu+o(1)}.}
$$

**Proof, explicit upper bound.** A DNF with at most $n$ shared negations, at most $(n-1)$ AND gates for each of at most $2^n$ terms, and at most $2^n-1$ OR gates gives

$$
U(n)\le B(n):=n2^n+n+2.
$$

This is precisely the kind of conservative bound used in TMR-5/026. Therefore

$$
R_\mu(n)\le \max\left\{0,\left\lceil\frac{\log_2 B(n)}\mu-n\right\rceil\right\}
=\left(\frac1\mu-1\right)n+O_\mu(\log n).
$$

**Proof, new complementary lower bound.** At most

$$
D(n,s)=(s+1)(n+s+2)[3(n+s+2)^2]^s
$$

distinct syntactic descriptions of $\le s$-gate circuits exist: each gate has at most three types, at most $(n+s+2)^2$ input-pointer choices, and the output has at most $(n+s+2)$ choices. This overcounts circuits and therefore also upper-bounds the number of truth tables realized.

For $n\ge8$, take $s=\lfloor 2^n/(16n)\rfloor$. Then $\log_2(n+s+2)<n$ and

$$
\log_2 D(n,s)
 <2n+s(2n+2)
 \le 2n+\frac{(2n+2)2^n}{16n}
 <2^n.
$$

The final strict inequality holds already for $n\ge8$ and remains true thereafter. There are $2^{2^n}$ Boolean functions. Thus some $n$-input function has

$$
CC_n(f)>\left\lfloor\frac{2^n}{16n}\right\rfloor.
$$

This is an **existential Shannon-style circuit-counting bound**, not a uniformly constructible explicit hard family.

If $r$ is such that $2^{\mu(n+r)}<2^n/(16n)$, the padded copy of that hard $f$ is still MCSP NO, by gate-count invariance. Hence $R_\mu(n)> (1/\mu-1)n-\log_2(16n)/\mu-O(1)$. Together with the upper bound, this proves the announced formula. QED.

**Exact threshold criterion, useful for reviewers:** A given $r$ guarantees that **every** padded table is MCSP YES if and only if $\lfloor2^{\mu(n+r)}\rfloor\ge U(n)$. The theorem identifies the asymptotic threshold crossing for the operation $P_r$, not the difficulty of **deciding** MCSP at that threshold.

## 5. Hostile control and proof-chain consequence

A tempting proposed transfer says: take an MCSP NO truth table at a lower threshold, add enough dummy variables to increase the full-table size, and import a known larger-threshold lower bound. The exact $R_\mu(n)$ transition shows that sufficient dummy padding instead destroys **every** NO instance, while padding below the worst-case count bound leaves **some** NO instances but does not preserve the original reduction's exact labels or any lower bound. It is incorrect to infer that the existence of hard functions below $R_\mu$ yields an efficient witness or an unrestricted one-tape time lower bound.

The threshold constants $\mu_1$ and $\mu_2$ in [1] remain different. Neither a stronger $N^{1.99}$ exponent at $\mu_2$ nor the present optimal padding exponent closes the low-$\mu_1$ $N^{1.01}$ lower-bound premise.

## 6. Actually executed controls, files and limitations

**Native CPython execution:** `experiments/tmr/tmr1_padding_window035.py`, exact source Git blob `e8fa3ec48bec05df89b0caf541f4e069edd9df6f`, ran on Linux/Python. Immutable stdout `results/raw/tmr/2026-11-14_1504_TMR1_PADWINDOW035_RAW.json`, exact blob `8e056ab3b947cc261c274278fcfd672d76ab2f50`. Both byte-identical to the native-executed local source/raw after Git readback.

The program checked **296 exhaustive truth-table comparisons** of exact circuit minimums capped at 2 gates, for arities 1, 2, 3 with up to two added dummy variables, all PASS. It additionally performed **18** numerical parameter checks at $n\in\{8,12,16,32,64,128\}$ and rational $\mu\in\{1/4,1/2,3/4\}$, using exact integer exponent comparison for padding thresholds; zero failures. It tested finite circuit counts and ratios, not a physical Turing machine or an asymptotic proof. The displayed theorem has the independent counting proof above.

Example: $n=128$, $\mu=1/2$ gives an existential-NO guarantee for padding $r\le106$ from the conservative counting bound, while the DNF upper establishes universal YES by $r=143$. These are **bounds**, not the exact unknown transition $R_\mu(128)$.

## 7. Remaining OPEN arrows and review request

The original P-vs-NP target uses one fixed finite total deterministic multitape 3-SAT decider $A$ over every length $L$, with unrestricted polynomial writable workspace. A separation requires, for every such correct $A$, every integer $k\ge1$, $C>0$ and $L_0$, a valid $F$ with $|F|\ge L_0$ and $T_A(F)>C(|F|+1)^k$. The circuit-counting existence proof here says nothing about that quantification or source construction. Nor does it deliver a header-free one-work-tape MCSP lower bound. **Both P=NP and P!=NP proof chains remain OPEN**.

**Immediate next target:** a *non-dummy*, fully charged and uniform threshold-changing transformation whose output size is polynomial in the **existing explicit MCSP table**, preserves both labels at the *specified* $s(n)=2^{\mu_1 n}$, and whose one-way-input/one-work-tape complexity translation is strong enough to use [1]. TMR-5: independently audit the circuit count, exact $R_\mu$ definition, and whether there is a cheaper encoding escape. TMR-4: test non-dummy syntax-aware transformations and both-label preservation. TMR-2: find compact-description countercontrols. TMR-3: audit materialization $N'=N^{1/\mu+o(1)}$ and whether any tape/network simulation loses the $1.01$ exponent.

**Repository preflight:** Latest November 14 directive was read first and rechecked (SHA `1e11aa64a0b0d635a65cea58500b09f2b0fe010a`), then November 13 replacement, `AGENTS.md`, `CODEX.md`, repository research skill, peer handoffs, issue #3 through TMR-3/029. Full authentic proof1.txt (28,714 chars; SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`), proof2.txt (1,051,196 chars; SHA `930c5eeddafce656717f28055a7a9a755f44737c`) and root main.tex (2,545,859 chars; SHA `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34`) were read, the latter two by Git blob fallback because normal file fetch was blank. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex is TMR-5-owned, not edited. No schedules, identities or tasks were modified.

### Original primary references

[1] Cheraghchi, Hirahara, Myrisiotis, Yoshida. *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*. STACS 2021, Theorems 1 and 2, printed p.23:3. https://doi.org/10.4230/LIPIcs.STACS.2021.23

[2] McKay, Murray, Williams. *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes*. STOC 2019, Theorems 1.2 and 1.3, printed p.2. https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf

[3] Oliveira, Santhanam. *Hardness Magnification for Natural Problems*. FOCS 2018, ECCC TR18-139. https://eccc.weizmann.ac.il/report/2018/139/

[4] Chen, Hirahara, Oliveira, Pich, Rajgopal, Santhanam. *Beyond Natural Proofs: Hardness Magnification and Locality*. Journal of the ACM 69(4), 2022. https://doi.org/10.1145/3538391

END_OF_REPORT::TMR-1::PADWINDOW35::2026-11-14_1504_PST
