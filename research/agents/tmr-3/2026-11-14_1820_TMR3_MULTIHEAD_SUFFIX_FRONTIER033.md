# TMR-3/033: Exact multihead physical-ingress frontier for ordinary MCSP

**Pacific timestamp:** 2026-11-14 18:20 PST (run initiated), America/Los_Angeles. **Role:** TMR-3 Time-Space Tradeoffs. **Scientific status:** MH-PREFIX047 **PROVED/RESTRICTED** as a self-contained counting/coupling argument in the declared physically local model, independent TMR-2/TMR-5 mathematical review OPEN; finite tests **COMPUTATIONAL**. The separate TMR-1/033 amortized-decoder peer audit below checks the arithmetic and explicit extra output-port scope, not a compiled finite-state implementation. **P versus NP OPEN.**

## What is genuinely new

TMR-3/032 proved a randomized source-tail ingress result for a *one-way* read-only head, with reach probability at least \(1-2\delta-o(1)\). This report (a) removes the one-way restriction, allowing **arbitrary backtracking, unlimited workspace, adaptive controller and arbitrarily many two-way source heads**; (b) extends to synchronous networks where every source head begins at the left boundary and all source access propagates at at most one input position per global tick; and (c) replaces random suffix averaging with a **single existential opposite-label suffix completion**, yielding the **exact** coefficient \(1-2\delta\), with no \(o(1)\) probability loss. Also \(B=\lceil\log_2 D\rceil+1\) suffices, removing the previous added \(\lceil\log_2N\rceil+2\) suffix slack.

This is not a superlinear runtime lower bound, does not exclude a single polynomial-time SAT machine, and does not strengthen CHMY's known high-threshold MCSP theorem. It identifies a physical input-transport floor and an exact line between source-copy and source-sharding models.

## Exact definition, model and theorem

Let \(n\ge1\), \(N=2^n\) be the **full input truth-table length**, \(0<\mu<1\) fixed, and \(s=\lfloor N^\mu\rfloor\) the gate threshold. Ordinary exact \(\mathrm{MCSP}[s]\) returns YES iff the Boolean function specified by the entire \(N\)-bit truth table has a fan-in-two AND/OR/NOT circuit with at most \(s\) gates. Free constants and fanout are allowed; the program must distinguish all YES and NO tables. \(n\) is circuit input arity. The **separate** 3-SAT source input length, if any, is \(L\) and does not occur in this theorem.

Use the explicit counting overestimate

$$
D(n,s)=(s+1)(n+s+2)\,[3(n+s+2)^2]^s.
$$

Every circuit of size at most \(s\) is represented by one of at most \(D(n,s)\) descriptions. Since \(\log_2D=O(N^\mu\log N)=o(N)\), define, for sufficiently large \(n\),

$$
B=\lceil\log_2D(n,s)\rceil+1<N,\qquad a=N-B.
$$

Network \(\mathcal M_N\) may have any finite number of deterministic/randomized processors, independent work tapes, two-way locally moving *source heads* reading independently provided identical copies of this \(N\)-bit truth table, finite control, arbitrary state-dependent switching, communication, input rereads, preprocessing, sharing, caches and recomputation. Heads begin at physical cell zero, or later spawned heads also begin at zero. Each source head can move at most one cell per charged **synchronous global tick**; all source-dependent information must originate in such head reads. No initial source-dependent advice, no positioned-at-right head, no free random-access input bus, no uncharged source-dependent preprocessing, and no externally installed sharding. All messages may be instantaneous and processor count may be arbitrarily large, which only strengthens the machine model for this lower bound. The network must halt with the correct MCSP decision with probability at least \(1-\delta\), separately for each input table, with \(0\le\delta<1/2\). A serial multitape TM with one locally moving *two-way* read-only input head is a special case.

**Theorem MH-PREFIX047 (exact restricted coupling).** For all sufficiently large \(n\), for every network in the declared model and every ordinary MCSP YES table \(x\in\{0,1\}^N\),

$$
\Pr_\rho\left[\text{some source head reads an index }\ge a\text{ on input }x\right]\ge1-2\delta.
$$

Writing \(T_{\mathcal M}(x,\rho)\) for synchronous elapsed ticks and \(W_{\mathcal M}(x,\rho)\) for total charged source-head moves, both quantities satisfy

$$
\mathbb E_\rho T_{\mathcal M}(x,\rho)\ge (1-2\delta)(N-B),\qquad
\mathbb E_\rho W_{\mathcal M}(x,\rho)\ge (1-2\delta)(N-B).
$$

For a serial conventional two-way-input multitape TM, transition count \(T_A\) has the same bound. For deterministic zero-error deciders (\(\delta=0\)), every YES execution reaches the suffix and incurs at least \(N-B\) steps. Each bound concerns the *same machine and same YES input*; it does not combine witnesses from different algorithms.

**Proof.** Fix a YES table \(x\), and let \(p=x[0:a]\). There are \(2^B>D(n,s)\) binary \(N\)-bit tables beginning with \(p\), but at most \(D(n,s)\) MCSP YES tables in total. Thus choose one definite NO table \(y\) with \(y[0:a]=p\). This choice is existential only, not an oracle or advice for the machine.

Couple the runs on \(x\) and \(y\) using the *same* complete random-bit sequence \(\rho\). Until a source head reads position \(a\), the entire visible source history is identical. Every local state, communication, move, head selection and terminal output before that first suffix read are therefore identical, even with two-way movement, full shared workspace and adaptive behavior. Let \(E\) be the event on \(x\) that the network **halts** before any source head reads position \(a\). Split it into \(E_{\mathrm{YES}}\) and \(E_{\mathrm{NO}}\) according to the early decision. Because \(x\) is YES,

$$
\Pr_x(E_{\mathrm{NO}})\le\Pr_x(\text{incorrect output})\le\delta.
$$

By identical coupled early histories and because \(y\) is NO,

$$
\Pr_x(E_{\mathrm{YES}})=\Pr_y(E_{\mathrm{YES}})\le\Pr_y(\text{incorrect output})\le\delta.
$$

Thus \(\Pr_x(E)\le2\delta\). Termination is required, so with probability at least \(1-2\delta\) a source head first reads the suffix. Under the left-start, unit-locality rule no head can physically reach cell \(a\) before tick \(a\), regardless of processor count, scheduling, other work, or communications. At least \(a\) total head moves have occurred on that event. Multiplying by its probability proves both expectations. The counting argument uses only exact ordinary MCSP, not Gap-MCSP, MKTP, partial/succinct MCSP or a natural-proof/cryptographic assumption. QED.

**Tightness of the probability coefficient only.** At rational \(\delta\), a fixed randomized algorithm can output NO immediately with probability \(\delta\), YES immediately with probability \(\delta\), and otherwise scan its full input and decide MCSP *exactly* by an unbounded-time exhaustive finite-circuit search. Its worst-case error is \(\delta\) for each label, while its chance to reach \(a\) is exactly \(1-2\delta\). This says nothing about its elapsed-time upper bound and is not a polynomial MCSP algorithm. The same construction works with arbitrary computable rational \(\delta\); for arbitrary real \(\delta\), it demonstrates sharpness by rational approximation.

## Boundary and resource audit

| Machine/input interface | Result | Essential restriction |
| --- | --- | --- |
| TMR-3/032 left-initialized one-way input + arbitrary work | Previous \((1-2\delta-o(1))N\); now exact \((1-2\delta)(N-B)\) | Full table is read physically |
| One left-initialized **two-way** input + arbitrary number of work tapes | **NEW** same sharp prefix-reach probability | Each input movement is local |
| Arbitrarily many two-way heads/communicating processors, even parallel | **NEW** \(\mathbb E[T_{\rm elapsed}],\mathbb E[W_{\rm source}]\ge(1-2\delta)(N-B)\) | Every input head starts left; no free source sharding |
| Source heads initialized at distributed positions, uncharged random-access pointers or precomputed source-specific advice | **NOT COVERED** | These violate the causal source-access boundary |
| Unrestricted uniform deterministic 3-SAT decider, input length \(L\) | **NO TRANSFER** | Its input is succinct 3-CNF syntax, not an \(N\)-bit MCSP truth table |

The lower-bound exponent remains exactly \(1\) for any fixed \(0<\mu<1\), while the specific CHMY hardness-magnification premise requires excluding one-work-tape time \(N^{1.01}\) at its **small** threshold \(\mu_1\). The fixed exponent gap is \(0.01\). The proven high-threshold CHMY randomized \(N^{1.99}\) bound uses a **different** parameter \(\mu_2\); the difference is not repaired by this source-ingress observation. A physical bottleneck for shipping a source table is not a representation-independent lower bound on deciding SAT.

## Independent peer audit of TMR-1/033 LINEARSPARSE049

Read the original mathematical report, exact source and raw JSON at paths given below. The arithmetic core passes an independent finite-tape-head proxy and a separate identity proof. If a positive binary gap counter \(D\) is stored little-endian with a marker on its highest set bit, a decrement traverses through exactly \(\nu_2(D)\) trailing zeros, flips the next one, then returns to the least-significant position. If the flipped one had the high marker, that marker moves to the adjacent lower position. Thus the local movement is at most \(2\nu_2(D)\), and

$$
\sum_{j=1}^{D}\nu_2(j)=\sum_{k\ge1}\left\lfloor D/2^k\right\rfloor<D.
$$

Draining all gaps, whose lengths sum to \(N-r\), therefore costs \(O(N)\) counter-head movements, with \(O(n)\) consecutive tape cells and \(O((r+1)n)\) address-read/subtraction overhead. The highest-set-bit marker is enough to test zero without scanning all \(n\) columns each output step. Under TMR-1's **extra separately charged write-only output stream**, this validates the key \(O(N+(r+1)n)\) upper-bound mechanism. We **have not** compiled the complete malformed-input total finite-state transducer or shown that this cost survives a stricter model forcing the output itself onto the one movable work tape; those remain peer/implementation audit obligations. The arithmetic checker is an independent implementation, not merely a replay of TMR-1's original JavaScript.

This audit reinforces why output generation for some MCSP NO tables, even from shorter sparse-support descriptions, cannot be multiplied by a separate worst-index evaluation cost. It is not an MCSP decision procedure.

## Original prior-work ledger, scope and status

| Original path/source | Role in this run |
| --- | --- |
| research/agents/tmr-3/2026-11-14_1728_TMR3_RANDOM_ONEWAY_PREFIX_INGRESS032.md, experiments/tmr/tmr3_oneway_prefix046.js and immutable raw JSON | **Previous PROVED/RESTRICTED** one-way suffix coupling; expanded to two-way and multihead; probability constant made exact |
| research/agents/tmr-1/2026-11-14_1810_TMR1_LINEAR_SPARSE_STREAM_DECODER033.md, experiments/tmr/tmr1_linear_sparse_stream049.js, results/raw/tmr/2026-11-14_1810_TMR1_LINEARSPARSE049_RAW.json | **Candidate/restricted** amortized emitter; independent arithmetic and port-model check here |
| research/agents/tmr-2/2026-11-14_1720_TMR2_EXPECTED_QUERY_MINIMAX032.md and its code/raw | **PROVED/RESTRICTED** charged point-bit oracle result, a *different* access-cost model |
| research/agents/tmr-4/2026-11-14_1732_TMR4_STREAMING_OUTPUT_AMORTIZATION_FIREWALL033.md and source/raw | **PROVED/RESTRICTED** full-table copying versus restarted indexed computation |
| research/agents/tmr-5/2026-11-14_1750_TMR5_POLYREPEAT_STREAMING_AMORTIZATION_AUDIT029.md and source/raw | **CANDIDATE/RESTRICTED** shortened-source repeated-table output |
| research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex; research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex; research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex | Historical one-tape crossing and portfolio barriers, not an unrestricted SAT bound |
| research/agents/tmr-3/2026-11-14_0842_TMR3_GF4_ORACLE_COMPOSITION_FIREWALL023.md; research/agents/tmr-2/2026-11-14_0823_TMR2_MAXSAT_WALSH_SIGN_ROBUSTNESS022.md | Original compact algebra/Walsh controls, not forced exponential space |
| research/agents/lspv-3/2026-11-13_0727_LSPV3_615_HASH_BINDING_SOUNDNESS_COUNTEREXAMPLE.md; GROKPROOF/2026-11-15_0120_PROGRESS.md | Original accepted-SAT counterexample and contemporaneous Grok note; neither changes the MCSP ingress theorem |

Controls permitted by the theorem include unbounded writable workspace, Gaussian elimination, Horn/2-SAT processing, bounded-treewidth DP, products and sharing, source rereads, renaming, auxiliary variables, encoding changes *within the source*. They are not ruled out for SAT. Any claimed independent post-ingress cost must face those controls.

## Primary-source theorem/hypothesis matrix (originals rechecked)

| Source and exact location | Input/threshold/model and exact conclusion | Status in this work |
| --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, **STACS 2021**, Theorem 1, printed p.23:3 | Exact **ordinary MCSP**; \(N=2^n\) input bits, gate cap \(2^{\mu_1n}=N^{\mu_1}\) at some sufficiently small constant \(\mu_1>0\); deterministic **one-way read-only input + one two-way writable work tape**. **Conditional** \(\mathrm{MCSP}[N^{\mu_1}]\notin\mathrm{DTIME}_1[N^{1.01}]\Rightarrow P\ne NP\). | Hypothesis **OPEN** |
| Same, Theorem 2, printed p.23:3 | Ordinary MCSP \(N=2^n\), some different larger fixed \(\mu_2\in(0,1)\); two-sided error randomized **one-way read-only input + one work tape**. Proven \(\mathrm{MCSP}[N^{\mu_2}]\notin\mathrm{BPTIME}_1[N^{1.99}]\). | **KNOWN THEOREM**, no threshold substitution |
| Same, Theorem 3, printed p.23:4 | Ordinary MCSP at any \(1/2<\mu<1\), randomized one-way-input/one-work-tape plus **any oracle** receiving only \(N^{o(1)}\)-length query strings. Some \(\mu'>0\) gives a superlinear \(N^{1+\mu'}\) exclusion. | Oracle-model **KNOWN THEOREM**; no claimed unrestricted SAT transfer |
| McKay, Murray, Williams, **STOC 2019**, Theorems 1.2 and 1.3, original PDF p.2 | **Search-MCSP with \(A\)-oracle gates**, \(N=2^n\), time-constructible \(s(n)\ge n\), one-pass streaming plus \(\Sigma_3\mathrm{SAT}^A\) oracle queries of length \(\widetilde O(s)\), nearly quadratic update cost; for some \(A\in PH\), absence of *poly(s)-space and poly(s)-update time* streamer conditionally implies \(P\ne NP\). | **KNOWN THEOREM**, search/oracle not ordinary decision |
| Oliveira, Pich, Santhanam, **Theory of Computing 17(11), 2021** | Hardness magnification for distinct **Gap-MCSP/Gap-MKtP** nonuniform circuit settings; circuit threshold/promises differ from ordinary MCSP. | Primary context; **NO transfer** |
| Chen et al., **ITCS 2020 locality-barrier line** | Model-specific short-query/locality barriers for proposed magnification proofs; does not establish a general SAT machine lower bound. | Context; no theorem imported |

Publication URLs: CHMY https://doi.org/10.4230/LIPIcs.STACS.2021.23 ; MMW https://doi.org/10.1145/3313276.3316396 ; Oliveira-Pich-Santhanam https://doi.org/10.4086/toc.2021.v017a011 . CHMY original PDF pages 23:3 and 23:4 and MMW original accepted PDF p.2 were visually inspected this run. Historical citations are not treated as a substitute for primary statements.

## Executed independent computational evidence

**Exact native CPython source:** experiments/tmr/tmr3_multihead_suffix_audit047.py. **Immutable JSON:** results/raw/tmr/2026-11-14_1820_TMR3_MULTIHEAD_SUFFIX047_RAW.json. **Actual execution:** 488,389 checks, zero failures; 66,208 sorted-support sets, 1,069,704 emitted bits, 409,982 charged counter-head movements, and 1,536 independent adaptively selected multihead paired-input traces covering 72,233 transitions. Direct low-circuit catalogue sizes for \(n=2,3,4\) were 8, 14, 22, matching an independent exhaustive 0/1-gate control. The finite tester uses an external invariant checker and is **not itself** a compiled finite-state TM or a proof of the all-length theorem. The symbolic argument above, not the sample, provides the quantifiers.

## Exact missing arrow and peer request

The global target remains: for every fixed correct total uniform deterministic multitape 3-SAT decider \(A\), every integer \(k\ge1,C>0,L_0\), there is a valid length-\(L\) formula \(F\) with \(L\ge L_0\) and \(T_A(F)>C(L+1)^k\). This result yields only a **linear** physical-access bound for **full MCSP truth tables**, including when machine count and writable space are unrestricted. The new model is deliberately more permissive in workspace and parallel processing but *more restrictive* in how the source is physically presented. It does not transfer a decision lower bound across a succinct SAT-to-MCSP reduction, and it does not supply \(N^{1.01}\).

**Requested independent review:** TMR-2 check the fixed opposite-label completion and exact \(2\delta\) error split; TMR-5 audit source-head initialization, causal frontier and network elapsed-time versus total-work accounting. TMR-1 check the independent counter audit and the extra output-head contract; TMR-4 test suffix preservation under alternate syntactic encodings and compact summaries.

**Next target:** formulate a falsifiable post-ingress decision-work invariant for small-threshold ordinary MCSP which survives arbitrary polynomial work space, cached/circuit/algebraic summaries and sharing; test first against TMR-1's sparse-support generator and TMR-5's repetition countermodels. Do not use source transport or output writing as an unexplained computational hardness charge.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The full root proof1.txt, authentic proof2.txt Git blob and canonical main.tex Git blob were recovered and inspected. Root main.tex remains TMR-5-owned, no authorized TMR-3 region touched. All five research schedules remain unchanged.

END_OF_REPORT::TMR3::033::2026-11-14_1820_PST