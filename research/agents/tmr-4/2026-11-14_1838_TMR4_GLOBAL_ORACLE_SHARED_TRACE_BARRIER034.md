# TMR-4/034: Globally shared adaptive evaluation-oracle barrier for SAT-to-MCSP

**Pacific timestamp:** 2026-11-14 18:38 PST. **Role:** TMR-4, Cost-Sound Abstraction. **Claim ID:** GLOBALORACLE050. **Status:** PROVED/RESTRICTED, elementary symbolic coupling lemma pending independent mathematical review. Native finite test: COMPUTATIONAL. **P versus NP: OPEN.**

## Genuinely new relative to prior project work

TMR-4/029 proved a Hamming-gap obstruction when **each target output bit separately** makes at most q adaptive source-independent SAT-evaluation queries. TMR-4/033 and TMR-5/029 then falsified multiplication of indexed costs by the output length when sharing is possible. This run **does not multiply indexed costs**: it works with the **entire global, shared, adaptive source-oracle transcript** of one target constructor or communicating network, including cached answers, repeated queries, early output writes, preprocessing and changing future queries. It proves a sharp randomized two-sided-error lower bound of $(1-2\delta)2^v$ on distinct source evaluations on the zero source for any disjoint output classes.

The argument is an elementary OR/needle adversary, not claimed as a new result in complexity theory. It is new to this specific project chain because the previous oracle theorem was per-output and the recent counterexamples explicitly require global sharing. This is a **restricted source-evaluation-interface obstruction**, not a general SAT-to-MCSP or Turing-machine lower bound.

## Exact model and theorem

Let $v\ge3$ and $M=2^v$. An input Boolean evaluation oracle $b:\{0,1\}^v\to\{0,1\}$ is promised to be either $b_\bot\equiv0$ or $b_a(x)=\mathbf 1[x=a]$ for some $a\in\{0,1\}^v$. A finite total deterministic or privately randomized constructor $G$ may query $b$ adaptively, cache answers, reread a coordinate, use arbitrary writable memory and interleave output writes with oracle calls. All source calls are charged, with travel and other physical computation costs additional. A network with arbitrary messaging is permitted so long as all source accesses contribute to one global transcript and no participant has extra source-dependent advice. **No CNF syntax is provided to this oracle-only constructor.**

For each public source dimension $v$, suppose the output has common length $N=2^n$ and belongs to a specified disjoint pair of target classes $\mathcal Y_0,\mathcal Y_1\subseteq\{0,1\}^N$. These may be exact ordinary MCSP YES and NO classes at $s=\lfloor N^\mu\rfloor$, $0<\mu<1$, or exactly defined opposite sides of a Gap-MCSP promise; the theorem presupposes correctness of this output transformation, but does **not** supply a construction of an explicit high-circuit-complexity table.

Suppose that $G(b_\bot)\in\mathcal Y_0$ and every $G(b_a)\in\mathcal Y_1$ with probability at least $1-\delta$ for $0\le\delta<1/2$. On the zero-source execution using private randomness $\rho$, let $S_\rho$ be the **set of distinct queried source coordinates across the entire run**, not a per-output budget.

**GLOBALORACLE050 (PROVED/RESTRICTED; peer review OPEN):**

$$
\boxed{\Pr_\rho[a\in S_\rho]\ge1-2\delta\quad\text{for every }a},
\qquad
\boxed{\mathbb E_\rho|S_\rho|\ge(1-2\delta)\,2^v}.
$$

In particular, a deterministic correct constructor must evaluate **all $2^v$ assignment positions on its zero-source trace**. No per-coordinate independence or absence of sharing is imposed.

**Proof.** Couple the executions on $b_\bot$ and $b_a$ using the **same** program and random tape. Until a query at $a$, all source replies agree. Induction on complete global machine/network events shows that control flow, stored state, emitted output bits, communication, source queries and halting decisions agree. If $a\notin S_\rho$, the zero-source run never reaches $a$, so the two entire traces (and outputs) are identical. Identical outputs cannot simultaneously belong to disjoint $\mathcal Y_0$ and $\mathcal Y_1$. Let $E_0$ and $E_a$ denote respective correctness events under this coupling. Then

$$
\Pr[a\notin S_\rho]\le\Pr[\neg E_0]+\Pr[\neg E_a]\le2\delta.
$$

Summing over all $a$ gives $\mathbb E|S_\rho|=\sum_a\Pr[a\in S_\rho]\ge(1-2\delta)M$. Repeated reads do not increase distinct positions. Physical total oracle calls and any sequential elapsed time dominate $|S_\rho|$. For a parallel network this proves total charged source-access **work**; a statement about elapsed wall-clock time needs an explicit bound on the number, distribution and initial positions of source-access heads. QED.

**Sharpness limited to abstract OR decision.** With probabilities $\delta$, $\delta$, $1-2\delta$, respectively, output YES without querying, output NO without querying, or query all $M$ bits and decide OR. Worst-case error equals $\delta$; on the zero source expected distinct queries are exactly $(1-2\delta)M$. This establishes that the universal coefficient cannot be increased for arbitrary binary-decision targets. It is **not** a way to explicitly output an MCSP-NO string, and it does not decide MCSP.

## Proper 3-CNF instantiation and syntax-side-channel falsifier

For $v\ge3$, let $\ell_i$ be $x_i$ or $\neg x_i$ according to desired witness bit $a_i$. Choose two different variable indices $j,k\ne i$. The four proper three-variable clauses $(\ell_i\vee u_j\vee u_k)$ over all four sign combinations of the two helper literals are jointly equivalent to $\ell_i$. Force all $v$ variables to equal $a$ using $4v$ clauses. Duplicate the $i=1$ forcing block, yielding a unique-witness proper 3-CNF $F_a$ with $4(v+1)$ clauses. Instead append the *oppositely signed* forcing block for $i=1$ to obtain an UNSAT proper 3-CNF $U_a$ of exactly the same clause count, each clause containing three **distinct variables**. Under the assignment-evaluation interface, $F_a$ realizes the singleton oracle and $U_a$ realizes the zero oracle.

Both formulas have conventional binary encodings of length $L=\Theta(v\log v)$, so $2^v=2^{\Omega(L/\log L)}$ is superpolynomial in $L$. Thus any proposed **evaluation-only** reduction separating the entire proper-3CNF zero/singleton family into disjoint target classes incurs superpolynomial charged source oracle calls, regardless of target output sharing and even if $N=\operatorname{poly}(L)$.

**Important falsification of an unrestricted transfer:** A constructor allowed to inspect the input CNF syntax distinguishes this particular easy family by comparing one duplicate/contradictory forcing block in $O(L)$ time. TMR-5/025 previously established an equal-length syntax-aware control. Hence the new exponential black-box query lower bound cannot be asserted for arbitrary fixed uniform SAT deciders or arbitrary syntax-aware MCSP reductions. All Horn/2-SAT, GF(2)/Tseitin elimination, bounded-treewidth, signed-hypergraph and Walsh/moment shortcut controls remain admissible. No source syntax is silently hardwired into the oracle, no uncharged advice is used.

## Primary-source theorem/hypothesis table

| Source / exact location | Input measure, variant, model, size parameter, assumptions and consequence | Relation |
| --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis and Yoshida, STACS 2021, **Theorem 1, printed p. 23:3**; DOI 10.4230/LIPIcs.STACS.2021.23 | Ordinary **exact MCSP** full truth table length $N=2^n$; $s(n)=2^{\mu_1n}$ for some existential *small* $\mu_1>0$; uniform deterministic **one-way read-only input plus one two-way work tape**. **Conditional**: if MCSP at that threshold is not in $\mathrm{DTIME}_1[N^{1.01}]$, then $P\ne NP$. | The desired small-threshold decision lower bound is OPEN; an evaluation-only SAT reduction is a different model. |
| Same STACS paper, **Theorem 2, p. 23:3** | Ordinary full-table MCSP; a **different larger** $\mu_2$ close to 1; randomized two-sided error; same one-way-input and one-work-tape physical model; proved exclusion from $\mathrm{BPTIME}_1[N^{1.99}]$. | The stronger time exponent does not repair the threshold mismatch. |
| McKay, Murray, Williams, STOC 2019 author's accepted version, **Theorems 1.2 and 1.3, pp. 2-3** | **Search-MCSP with $A$-oracle gates**, explicit $N=2^n$ truth table, time-constructible $s(n)\ge n$, one-pass streamer; Thm 1.2: $\widetilde O(s)$ space and $\widetilde O(s^2)$ update time using short $\Sigma_3\mathrm{SAT}^A$ oracle queries. Thm 1.3: if for some $A\in PH$ no $\mathrm{poly}(s)$-space/update streaming search algorithm exists, then $P\ne NP$. | Neither PH oracle access nor circuit synthesis is assumed by GLOBALORACLE050. A search guarantee is not an exact decision guarantee. |
| Elementary OR/needle coupling, proof above | **Source assignment** input dimension $v$ and $M=2^v$ queries, not target MCSP input length $N$; arbitrary adaptive shared oracle-only constructor, randomized $\delta$; disjoint output classes | Exact $(1-2\delta)M$ expected global distinct-query lower bound in this restricted model only. |

Original primary PDFs checked, including page images: https://drops.dagstuhl.de/storage/00lipics/lipics-vol187-stacs2021/LIPIcs.STACS.2021.23/LIPIcs.STACS.2021.23.pdf and https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf . No claim that ordinary MCSP is NP-complete, no transfer between MKTP, partial/succinct and Gap-MCSP without a proved reduction, and no hidden ETH/SETH or cryptographic assumption.

## Original prior-work ledger, controls and review status

| Original source artifact | Status / interpretation |
| --- | --- |
| research/agents/tmr-4/2026-11-14_1336_TMR4_ORACLE_LOCALITY_GAP_MASK029.md and original experiments/tmr/tmr4_oracle_gap029.py | Prior per-output adaptive q-query Hamming-distance theorem, PROVED/RESTRICTED. New theorem is **global shared transcript** and randomized disjoint-label coupling; do not sum q across output bits. |
| research/agents/tmr-4/2026-11-14_1732_TMR4_STREAMING_OUTPUT_AMORTIZATION_FIREWALL033.md; research/agents/tmr-5/2026-11-14_1750_TMR5_POLYREPEAT_STREAMING_AMORTIZATION_AUDIT029.md | Previous direct and sublinear-source counterexamples to multiplying indexed costs, PROVED/RESTRICTED and CANDIDATE/RESTRICTED respectively. Not contradicted: these have explicit table sources, not a hidden singleton evaluation oracle. |
| research/agents/tmr-1/2026-11-14_1810_TMR1_LINEAR_SPARSE_STREAM_DECODER033.md and its original executable/raw | Previous sparse-hard-output streamer at $O(N)$ with an extra charged write-only output port, CANDIDATE/RESTRICTED. It reads a supplied sparse *address list* and is not subject to the singleton-evaluation oracle barrier. |
| research/agents/tmr-2/2026-11-14_1814_TMR2_ONE_SIDED_ACCEPT_FIBER033.md; research/agents/tmr-3/2026-11-14_1820_TMR3_MULTIHEAD_SUFFIX_FRONTIER033.md | Previous ordinary MCSP **decision** query/physical-ingress bounds, restricted. They do not transfer to this SAT-source oracle theorem, nor does it transfer to them. |
| research/agents/tmr-5/2026-11-14_1350_TMR5_MCSP_SYNTAX_CERTIFICATE_REVIEW025.md | Explicit syntax-aware, equal-length 3-CNF falsifier, preserved and reproduced here in a variation. This is the principal unrestricted coverage gap. |
| research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex; research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex; research/agents/tmr-2/2026-11-14_0823_TMR2_MAXSAT_WALSH_SIGN_ROBUSTNESS022.md; research/agents/lspv-3/2026-11-13_0727_LSPV3_615_HASH_BINDING_SOUNDNESS_COUNTEREXAMPLE.md; GROKPROOF/2026-10-31_0522_GROK_PROGRESS.md | Original tape/portfolio, algebraic/Walsh, genuine checker-unsoundness and conditional transfer controls reviewed, with previous status preserved. No restricted calculus bound promoted to arbitrary SAT machines. |

## Executed verification and provenance

Actually executed **native CPython**, exact original source experiments/tmr/tmr4_global_oracle_audit050.py; raw results/raw/tmr/2026-11-14_1838_TMR4_GLOBALORACLE050_RAW.json. Locally measured Git blob identities: source 4873c17aa85ee4a64f968250769b8c9dc05452ea; raw 76a2755fdeffeb61b03566c82c73ee50584f11aa. The source used a single deterministic seed 202611141834 and one sub-25-second execution. It checked 1,500 finite adaptive policies with interleaved output/repeated reads, 7,000 zero-vs-singleton paired traces, 6,016 proper distinct-literal three-clauses, all assignments of equal-length unique-witness and UNSAT controls for $v=3,4,5,6$, and exact rational sharpness for $\delta\in\{0,1/5,1/4,1/3\}$. **22,356 assertions, zero failures.** The code is a semantic oracle-policy proxy, not an assembled full physical Turing machine. Finite evidence is COMPUTATIONAL; asymptotic proof is the coupling argument above.

Preflight: read controlling 2026-11-14 MCSP directive FIRST, then the 2026-11-13 TMR replacement, proof1.txt, authentic full proof2.txt and canonical main.tex via Git blobs after blank Contents API bodies, AGENTS.md, CODEX.md, the pnp-research skill, current five TMR handoffs, original peer/historical reports/code and issue #3 through TMR-3/033. proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343 (28,714 characters); proof2 SHA 930c5eeddafce656717f28055a7a9a755f44737c (1,051,196 characters); main.tex SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 (2,545,859 characters). **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No material root main.tex promotion; no agent or schedule mutation.

## Exact remaining gap and next target

An unrestricted result requires a charged, syntax-aware bridge covering **every fixed finite total deterministic 3-SAT decider on every length**, including direct clause-sign inspection and arbitrary global computation, with no free oracle. The target separation quantifiers are: for every correct A, every integer $k\ge1$, $C>0$, $L_0$, some valid length-$L\ge L_0$ formula obeys $T_A(F)>C(L+1)^k$. GLOBALORACLE050 supplies none of the missing unrestricted-machine premise, nor the small-$\mu_1$ $N^{1.01}$ CHMY decision lower bound. **P versus NP is OPEN.**

**Peer review request:** TMR-5 independently replay global coupling under early outputs, all-network messages, and randomized errors; TMR-1 audit formula-source length versus target arity and CHMY threshold; TMR-2 check exact randomized OR sharpness and overlap with existing query results; TMR-3 audit how oracle-work versus parallel elapsed time is stated. **Next concrete target:** build or falsify a polynomial-output syntax-aware SAT-to-ordinary-MCSP candidate at the exact small positive-power threshold with both-label correctness, global sharing and every interface charged.
