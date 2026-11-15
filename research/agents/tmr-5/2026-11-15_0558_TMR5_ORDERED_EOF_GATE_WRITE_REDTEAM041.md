# TMR-5/041: Authentic delayed EOF gate write improves ordered physical service upper bound

**2026-11-15 05:58 PST (America/Los_Angeles).** TMR-5 / PNP Machine Bottleneck Redteam. Governing 2026-11-14 fusion-Lipschitz directive SHA \`54c9177fc211dfca6c94d89d6ebbf3f3908809d6\`. **Status: PROVED/RESTRICTED for the explicit finite-control ordered-record service, independent mathematical peer review OPEN; finite V8 evidence COMPUTATIONAL. P versus NP remains OPEN.**

## 1. Candidate and four falsifiers stated before focused literature/corpus review

**Candidate:** The TMR-3/044 ordered-activation service's published physical upper bound $2n+2$, supplied by the TMR-1/044 stage-and-return program, is **not the best known upper bound** for the unchanged ordered service. A fixed uniform machine can delay the **last** compulsory $g$-record write to the authentic EOF-read step, reverse its work head in that same microstep, and finish in exactly $2n+1$ unit steps. The already-proved ordered lower bound $2n$ is preserved. We also independently replay TMR-4/045's distinct, final-state-only fast $n+1$ program.

Predeclared falsifiers: (F1) writing a gate during EOF changes more than one W cell, jumps any head or relies on an oracle/lookahead; (F2) the delayed algorithm omits a gate, invents a length-dependent instruction, or creates a free shared identity; (F3) the after-last-record activation is actually terminal or the required subsequent HALT is omitted; (F4) this ordered-service upper bound is falsely transferred into arbitrary SAT-machine lower bounds or claimed to falsify the original fixed M_STAGE's tariff. Each is checked below; F4 is explicitly forbidden.

## 2. Recovered corpus, novelty boundary, primary literature

Read **FIRST** the user-approved fusion directive \`research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md\`, followed by TMR replacement \`research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md\`; recovered complete proof1.txt SHA \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\` (28,714 characters), proof2.txt authentic Git blob \`930c5eeddafce656717f28055a7a9a755f44737c\` (1,051,196 characters), and root main.tex authentic Git blob \`6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34\` (2,545,859 characters). The oversized ordinary contents endpoint returned empty bodies for proof2/main: this was **not** interpreted as empty stored files. Surveyed issue #3 and its current TMR updates, AGENTS.md, CODEX.md, pnp-research skill, all five current handoffs, TMR-1/044, TMR-3/043 and /044, TMR-4/044 and /045, TMR-5/040, TMR-2/044 and their directly relevant executed source/matrices, and historical LEAD-0029 Lipschitz audit. No root file edited.

Primary model context: F. C. Hennie and R. E. Stearns, *Two-Tape Simulation of Multitape Turing Machines*, JACM **13** (1966) 533-546, https://doi.org/10.1145/321356.321362; R. E. Tarjan, *Amortized Computational Complexity*, SIAM J. Alg. Disc. Meth. **6** (1985) 306-318, https://doi.org/10.1137/0606031. These supply general machine-model and potential-method context only. Neither proves the elementary new machine construction here. Unlike TMR-1/044's existing $2n+2$ fixed program and TMR-4/045's extensional $n+1$ alternative, this report addresses the **stronger ordered activation** with the SAME mandatory W record layout and authentic physical EOF inspection.

## 3. The identical strong ordered service and exact fixed finite machine

Fix $m\ge1$ independently of input length, with exactly one read-only original input head, one writable staging tape head W, and $m$ independently headed writable marker tapes $O_1,\ldots,O_m$. On promised input $1^n\#$, $n\ge2$, all heads start at cell zero, and W/O are blank. A physical step reads the scanned symbols, writes at most one W cell and one cell **on each distinct** $O_i$ tape, moves each head by at most one cell, and costs exactly **one**. The finite alphabets and the following control classes are independent of $n$. A fixed malformed-input sink extension can reject unexpected symbols; our theorem is restricted to the successful unary promise.

The **ordered goal** demands that W[0] was written as 0; each W[j]=g for $1\le j<n$ was made by its own paid physical write; **the last gate W[n-1] is written before a subsequent nonterminal W[0]:0-to-1 activation**; original source EOF $\#$ at position $n$ is actually inspected; all $m$ distinct marker tapes have $O_i[0]=@$; and a **distinct later true HALT** occurs. This is exactly the stronger ordering used in TMR-3/044, not just the extensional FINAL-STATE service.

The new fixed deterministic program \`M_EOFWRITE_m\` is:

| Control/rule | Scanned input and authentic action | W movement | Cost and successor |
|---|---|---|---|
| INIT | On first 1, write W[0]=0, move input right | **Stay W[0]** | 1; SEEK |
| SEEK | On second 1, move input right, do not write W | **W[0] to W[1]** | 1; STREAM |
| MID | On each later 1, write one new W[j-1]=g, move input right | W[j-1] to W[j] | 1; STREAM |
| EOF_WRITE | On actual source **#**, write **final W[n-1]=g** | **Move left to W[n-2]** | 1; BACK |
| BACK | While the scanned W cell is g, move one cell left | One left | 1; BACK |
| ACT | At the scanned W[0]=0, rewrite 0 to 1 and write O_i[0]=@ once on **each independent output tape** | Stay | 1; READY (nonterminal) |
| HALT | From READY, enter the true halt state without writes | Stay | 1; HALT |

The transition choice to write the final gate is made **only after the source head actually reads #**. No lookahead is used: the work-head lag of one position is established by SEEK and preserved by each MID. On EOF, the source head is at cell $n$ while W scans cell $n-1$. W's reversal and final gate write are simultaneous and legal. On $n=2$, MID and BACK repeat zero times; the finite-control table remains unchanged. In BACK, the only test is the currently scanned W symbol g or 0, not a global record count. Historical source/event ledger checks below are external verifier assertions rather than oracle conditions in the machine.

This program uses the same input and output alphabet, head locality, number of tapes, mandatory source inspection, gate identities, activation ordering, and separate HALT as the old ordered service. Only the **timing of the last gate write and head reversal** changes.

## 4. New all-n construction and rigorous cost bound

**Theorem TMR5-041-A (PROVED/RESTRICTED, independent peer review OPEN).** For every fixed $m\ge1$ and every $n\ge2$, \`M_EOFWRITE_m\` satisfies the ordered service on $1^n\#$ and executes exactly

$$
T_{\mathrm{EOFWRITE}}(n)=1+1+(n-2)+1+(n-2)+1+1=\boxed{2n+1}
$$

genuine unit-cost multitape transitions. Consequently, combining this explicit upper bound with TMR-3/044's already-published physical lower bound yields

$$
\boxed{2n\ \le\ T_{\mathrm{ORDERED}}^{\min}(n)\ \le\ 2n+1.}
$$

Here $T_{\mathrm{ORDERED}}^{\min}$ minimizes over eligible physical programs implementing the **ordered** service, not over all SAT deciders.

**Proof:** INIT visits and writes W[0], SEEK places W's head at 1 without writing. At every later source 1 at position $j\ge2$, STREAM has W at $j-1$, writes that paid g identity exactly once, and advances both heads. At source EOF at $n$, W is at $n-1$, so EOF_WRITE inspects that real source cell, writes the final distinct W[n-1]=g, and moves W to $n-2$. All W[1..n-1] are now present, and W[0] is still 0. Exactly $n-2$ BACK moves bring W to 0. ACT performs the mandatory nonterminal 0-to-1 rewrite and all $m$ one-cell writes on **separate** tapes; the distinct next transition HALT terminates. Source steps are $n+1$ (INIT, SEEK, $n-2$ MID, EOF); backward transport is $n-2$; ACT and HALT cost two more. Summing gives $2n+1$. The finite table does not depend on $n$, and every gate identity and tape move is explicitly paid. QED.

**Smallest witness:** $n=2,m=1$: five genuine steps \`INIT, SEEK, EOF_WRITE, ACT, HALT\`. The original M_STAGE route uses six steps; the stronger ordered lower bound is four. At $n=3,m=1$, the trace has seven steps, \`INIT, SEEK, MID, EOF_WRITE, BACK, ACT, HALT\`, versus eight under the original staged machine. The new result improves an **upper** bound by one; it does not claim the lower bound $2n$ is sharp or that the original TMR-1/044 fixed-machine tariff was wrong.

## 5. Exact zero closure, reduced-product vector and full signed tariff

There are **no authentic zero-cost steps**; zero SCCs are singleton and $\operatorname{cl}_0(C)=C$. Optional reversible zero-price metadata VIEW transitions, if separately added, must preserve every component and cannot create or erase source reads or gate records.

For reachable configurations let $a=1$ until W[0] becomes 1, $q$ count missing distinct physical W[1..n-1] g records, $u$ count unseen original positions $0,\ldots,n$ including the genuine #, $h=1$ until true HALT, and phase-dependent $d=n-2$ throughout INIT/SEEK/STREAM, $d=\mathrm{Whead}$ in BACK, and $d=0$ in READY/HALT. These are external mathematically defined state-observation coordinates; the machine does not get the entire input length for free.

$$
\mathbf p(C)=(0,0,0,a,q,u,d+h),\qquad
\mathbf p(C_0)=(0,0,0,1,n-1,n+1,n-1),\quad \mathbf p(\mathrm{GOAL})=\mathbf 0.
$$

With columns CNF, XOR, SEP, FUS, Gamma, Interface, Machine, the complete physical signed discharge matrix is:

| Authentic rule | FUS | Gamma | Interface | Machine | Cost | Multiplicity |
|---|---:|---:|---:|---:|---:|---:|
| INIT | 0 | 0 | 1 | 0 | 1 | 1 |
| SEEK | 0 | 0 | 1 | 0 | 1 | 1 |
| MID | 0 | 1 | 1 | 0 | 1 | $n-2$ |
| EOF_WRITE | 0 | 1 | 1 | 0 | 1 | 1 |
| BACK | 0 | 0 | 0 | 1 | 1 | $n-2$ |
| ACT | 1 | 0 | 0 | 0 | 1 | 1 |
| HALT | 0 | 0 | 0 | 1 | 1 | 1 |

The exact fixed-program nonnegative coefficient cone is

$$
\boxed{\lambda_{\mathrm{FUS}}\le1,\quad
\lambda_{\Gamma}+\lambda_{\mathrm{Interface}}\le1,\quad
\lambda_{\mathrm{Machine}}\le1,\quad \lambda\ge0.}
$$

The selected **uniform**, exact-rational feasible primal weights $(\lambda_{\mathrm{FUS}},\lambda_{\Gamma},\lambda_{\mathrm{Interface}},\lambda_{\mathrm{Machine}})=(1,0,1,1)$ give

$$
\Phi(C_0)=1+(n+1)+(n-1)=\boxed{2n+1}.
$$

The matching dual row multiplicities are those in the table. Their componentwise sum is exactly the initial vector $(1,n-1,n+1,n-1)$, and the row costs sum to $2n+1$, proving the LP optimum by weak duality. At every completed goal the vector vanishes; every authentic transition satisfies $\lambda^\top\Delta_r\le1$. Therefore telescoping yields the exact same-program lower bound as the genuine upper execution. **The seven-column machine-readable tariff is published separately.** This is a scoped fixed-program theorem, not a lower bound for arbitrary programs or SAT.

## 6. Independent peer replay, computational evidence, controls

A fresh executable was authored without importing TMR-1/044, TMR-3/044, or TMR-4/045 simulation functions. It physically tracks source head, W head and cells, separate output markers, read-history positions, paid gate identities, phases, all local single-tape writes and each rule's signed vector delta. It also independently replays the different TMR-4/045 \`M_DIRECT\` final-output implementation, compares the **literal completed W/O tape contents** on every tested $(n,m)$, and checks the original source EOF was observed. We do **not** equate the final head positions or control states, nor import an illegal M_DIRECT transition into the ordered program.

The exactly executed native V8 \`audit()\` generated the immutable JSON evidence. For every $2\le n\le128$ and $1\le m\le5$, the audit completed **635 ordered traces and 635 independent direct traces**, **125,095 actual price-one transitions**, **1,224,994 assertions**, **635 exact dual covers**, **9,604 integer-scaled LP upper checks**, and **zero failures**. No randomness. These finite results are **COMPUTATIONAL**. A separate locally executed CPython \`fractions\`-compatible physical replay over $2\le n\le257$, $1\le m\le6$ checked **1,536 ordered traces** and **399,360 ordered steps**, also with no failures, but that independent Python file is not included in the GitHub publication and cannot replace the published V8 evidence. Symbolic all-n claims rely on the mathematical proof, not sample size. Native Node binary execution, low-level TM compiler, full repository preflight, and LaTeX build were **not** performed in this connector-based run.

Hostile controls: (1) changing input format, adding a free EOF read or a second source head changes this specific source-access service; (2) one W cell changes per step and each output head writes one @ at most; (3) fixed m is required, not unbounded free parallel ports; (4) previous paid g identities remain paid and conjunctive, not implicitly unfolded; (5) Gaussian elimination, Horn, Krom, equality, autarkies, treewidth DP, compact extensions/circuits, learning, rereading, caching, recomputation, renaming and padding are **not ruled out** for unrestricted SAT machines, and this unary task does not charge them; (6) a genuinely faster ordered program, if found, must be retained, not CEGAR-deleted. Historical \`/341\` remains **FAIL** on its full logical UNSAT accepted language; \`/386\` remains **RESTRICTED** to its tested guarded fragment. Neither is altered, repaired or relabeled.

## 7. Ranked dependency map, weakest lemma and peer repair

| Dependency | Verdict | Exact scope |
|---|---|---|
| TMR-4/045 \`M_DIRECT\` cost $n+1$, same extensional W/O final layout | **PASS/RESTRICTED** | Independent complete reimplementation and finite source-bound physical replay |
| TMR-3/044 ordered one-head physical lower bound $2n$ | **RESTRICTED, retained** | Geometric argument reused; not independently proven tight |
| TMR-1/044 prescribed \`M_STAGE_OUTPUT_m\` exact $2n+2$ | **PASS/RESTRICTED, unchanged** | Different fixed control and timing |
| NEW \`M_EOFWRITE_m\` ordered complete trace $2n+1$ | **PROVED/RESTRICTED**, peer review OPEN | One fixed local multitape machine, all $n\ge2$ |
| NEW seven-component tariff and exact primal/dual $2n+1$ | **PROVED/RESTRICTED**, peer review OPEN | Only M_EOFWRITE_m's complete authentic rules |
| Selected TMR-1/044 $2n+2$ runtime as best known ordered **upper** | **FAIL as a best-upper claim**, not as fixed-machine claim | Improved by a legal one-step shortcut |
| Minimum ordered-service time $2n$ or $2n+1$ | **OPEN** | One-step residual gap, under fully uniform original-source program |
| Superpolynomial fusion-safe initial potential on actual SAT family | **OPEN** | Only linear costs established |
| Same-system transfer for **all** correct finite total SAT deciders | **OPEN** | Neither unary service nor selected proof system supplies it |
| Historical \`/341\`, \`/386\` | **FAIL full-language**, **RESTRICTED** respectively | Existing accepted-language scopes |

**Weakest surviving lemma and next peer repair:** Determine whether the ordered $2n$ lower bound is attainable by **one fixed uniform** physical machine for all $n$, or whether the missing one step is provably necessary because the single input head cannot know the last source 1 in time to reverse W earlier. TMR-3 should audit possible nonstreaming/adaptive positioning and earlier output prewrites; TMR-4 should check this state/phase-gated exact tariff with conservative MAY alternatives and real head geometry; TMR-1 should distinguish the ordered and extensional goal predicates, and TMR-2 should seek SAT-specific multiscale components surviving this authentic EOF/reversal fusion.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No edits to \`proof1.txt\`, \`proof2.txt\`, canonical root \`main.tex\`, other agents' ownership regions, historical source/checker evidence, or any of the five existing research schedules. P versus NP remains OPEN.

## Publications

- Executed V8 source: \`experiments/tmr/tmr5_ordered_eofwrite101.js\`
- Immutable raw V8 output: \`results/raw/tmr/2026-11-15_0558_TMR5_EOFWRITE101_V8_RAW.json\`
- Machine-readable seven-column tariff/dual: \`results/raw/tmr/2026-11-15_0558_TMR5_EOFWRITE101_TARIFF_MATRIX.json\`
- This report: \`research/agents/tmr-5/2026-11-15_0558_TMR5_ORDERED_EOF_GATE_WRITE_REDTEAM041.md\`

END_OF_REPORT::TMR-5/041::2026-11-15_0558_PST
