# TMR-1/023: MCSP magnification, a strict two-threshold circuit shell and the missing transfer

**Date:** November 14, 2026, 09:08 PST (America/Los_Angeles). **Role:** TMR-1, Machine Model Lead. **Status:** CANDIDATE/RESTRICTED mathematical theorem with complete elementary argument pending TMR-5 independent review; finite tests COMPUTATIONAL. **P versus NP: OPEN.**

**Newest instruction read:** \`research/coordination/2026-11-14_MCSP_FIVE_AGENT_REVIEW.md\` supersedes older scientific priorities and delegates the exact MCSP theorem chain to TMR-1. The November 13 five-TMR replacement directive remains authoritative for identities, safety and ownership. Neither instruction changes a mathematical proof status. No tasks were created or modified.

## A. Exact model distinctions and primary theorem ledger

Ordinary MCSP at threshold s takes an explicit N=2^n bit truth table of an n-input Boolean function f and decides whether CC(f)<=s, with CC counting gates of a fixed Boolean circuit basis. **N** is not SAT formula bit length **L**, and **n** is not N. In our elementary counting lemma CC uses fan-in-at-most-two AND/OR/NOT, unrestricted fan-out. For all-machine P!=NP one fixed finite total uniform deterministic SAT decider A serves all L, charges every real transition, input reread and writable cell, and must violate every fixed polynomial on some arbitrarily large valid input. No per-length minimum over different huge lookup programs.

| Original primary source | Exact problem/model | Hypothesis and conclusion; critical transfer restriction |
|---|---|---|
| Cheraghchi, Hirahara, Myrisiotis, Yoshida (CHMY), STACS 2021, Theorem 1 [1] | Ordinary MCSP[N^mu1], explicit N-bit truth table, **one-way read-only input plus one two-way read/write work tape**, deterministic time | For some **small fixed** mu1>0, an N^1.01 lower bound implies P!=NP. **This hypothesis is OPEN.** |
| CHMY Theorems 2,3 and detailed parameter theorem [1] | Ordinary MCSP[N^mu2] for **larger** mu2 near one, same tape interface, randomized two-sided error; specified versions allow an oracle with queries length N^{o(1)} | Unconditional near-N^1.99 lower bound at that larger mu2; for 1/2<mu'<mu<1 a form N^{2(mu'-o(1))}. **High threshold and low threshold cannot be interchanged.** |
| McKay, Murray, Williams, STOC 2019, Theorems 1.2-1.3 [2] | **Search**-MCSP^A streaming, one-pass N-bit input, size s(n), short Sigma3^P oracle queries | Oracle-assisted time N \`~O(s)\`, update \`~O(s^2)\`, space \`~O(s)\`. An appropriate streaming search lower bound for all polynomial-in-s update/space budgets implies P!=NP. Distinct from ordinary decision MCSP time lower bounds. |
| Oliveira, Pich, Santhanam, 2018/2021 [3] | Promise **Gap-MCSP** with thresholds around 2^{beta n}/(c n) and 2^{beta n}; **nonuniform general circuits** size N^{1+epsilon} | A bound for **all sufficiently small constant beta** yields NP not in P/poly, a nonuniform conclusion. No direct transfer from CHMY one-work-tape large-mu. |
| Oliveira and Santhanam, 2018 [4] | Ordinary MCSP[2^{sqrt(n)}] in a **formula** lower-bound framework | Designated lower bound magnifies to NP circuit-**formula** lower bounds. This is not the same as unrestricted NP not in P/poly. |
| Chen, Jin, Williams, FOCS 2019 [5] | A sparse NP language, general circuits | Appropriate N^{1+epsilon} circuit lower bound magnifies to NP not in P/poly. Source language and circuit model must actually satisfy hypotheses. |
| Chen et al., 2019 [6] | Hardness magnification **locality proof barriers** | Restricts certain proof strategies, not all possible machine or SAT lower bounds. |

Sources consulted at original theorem/model scope: [1] https://doi.org/10.4230/LIPIcs.STACS.2021.23 ; [2] https://doi.org/10.1145/3313276.3316396 ; [3] https://eccc.weizmann.ac.il/report/2018/158/ ; [4] https://eccc.weizmann.ac.il/report/2018/139/ ; [5] https://eccc.weizmann.ac.il/report/2019/118/ ; [6] https://arxiv.org/abs/1911.08297 . Original CHMY and McKay-Murray-Williams PDFs and theorem statements were checked, including their access models.

### Central current threshold gap

CHMY's established lower bound for a *larger* circuit threshold mu2 does not establish the *smaller* mu1 lower bound required for magnification. A larger circuit threshold changes the YES set. Lower bounds for decision languages are **not monotone under set inclusion**. A model-faithful reduction from the high-threshold known-hard MCSP instance to a low-threshold MCSP instance, preserving both labels, truth-table length, one-way input plus one-work-tape use and sufficiently low time overhead, is missing.

## B. NEW TMR1-SHELL23 theorem (restricted, independent review pending)

For every two fixed real constants 0<alpha<beta<1, let N=2^n, s=floor(N^alpha), and t=floor(N^beta). For all sufficiently large n, there are n-input Boolean functions f with

$$
\boxed{s<\mathrm{CC}(f)\le t.}
$$

Quantitatively set gamma=(alpha+beta)/2 and k=floor(gamma n). Then **at least 2^{2^k-1} distinct functions** that depend only on the first k inputs have sizes strictly between s and t.

**Proof:** There are 2^{2^k} functions on k inputs, embedded injectively as functions on n inputs by ignoring n-k inputs. Every k-input function admits a DNF of at most

$$
B(k)=k+(k+1)2^k
$$

fan-in-two AND/OR/NOT gates, including variable negations and product-term OR folding (empty/full functions need only constant size). Because gamma<beta, B(k)=o(N^beta), so all embedded functions have CC<=t for large n.

Any n-input circuit of at most s gates has an ordered gate list: each gate chooses one of three operations and two predecessor wires among at most n+s+2, followed by output selection. Thus the number of size-at-most-s descriptions is bounded by

$$
D(n,s)=(s+1)(n+s+2)[3(n+s+2)^2]^s.
$$

Its log_2 is O(s log(n+s))=O(N^alpha n)=o(N^gamma)=o(2^k). For all large n, D(n,s)<2^{2^k-1}. At most D(n,s) embedded k-input functions have CC<=s. More than 2^{2^k-1} therefore have s<CC<=t. QED.

**Scope and actual contribution:** The smaller and larger threshold MCSP YES classes are strictly different for all large n. This is an explicit **two-threshold middle-shell barrier**, not a time lower bound. It does not preclude a special many-to-one promise/label-preserving reduction. Prior project YES-entropy and injective-threshold barriers already establish related counting obstructions. No priority claim of new general circuit-counting theory is made.

## C. Independently executed falsification controls

One smallest finite example uses Boolean XOR of two inputs. Exhaustively enumerating topologically ordered AND/OR/NOT circuits with 0,1,2,3 gates found respectively 1,10,210,7560 sequences, none computing XOR, whereas four gates suffice:

$$
(x_1\lor x_2)\land\neg(x_1\land x_2).
$$

This is basis-specific: introducing XOR as a primitive gate invalidates the *finite four-gate* statement, not the asymptotic counting argument over a fixed finite complete basis.

For alpha=1/4, gamma=1/2, beta=3/4, nine tested values n=16,24,32,40,48,56,64,80,96 satisfied the count upper bound and the DNF upper bound. At n=16, k=8, B(k)=2312<=4096, and a conservative upper bound log_2 D<251<256=2^k. At n=24, k=12, B(k)=53260<=262144, and log_2 D<1102<4096. These are arithmetic checks, **not** exhaustive enumeration of all 2^{2^n} Boolean functions.

**Executed:** native CPython, small-circuit exhaustive controls plus nine integer-arithmetic large-parameter fixtures, zero final assertion failures. An initial attempt to materialize the astronomically large exact circuit-description count timed out; a conservative logarithmic bound repaired the code and the rerun succeeded. No generic SAT Turing machine, one-tape MCSP classifier, oracle collapse, GH CI, or latex compilation was executed. Test output is COMPUTATIONAL.

**Source:** \`experiments/tmr/tmr1_mcsp_shell023.py\`. **Raw:** \`results/raw/tmr/2026-11-14_0908_TMR1_MCSP_SHELL023_RAW.json\`. Test controls only establish the stated restricted inequalities and gate basis.

## D. Historical corpus, failure controls, proof obligations

Previous original project records located and compared:

- \`research/main/2026-10-18_ASYMPTOTIC_CONE5.md\`: already proves a **conditional cofinal slope absorption**. If under P=NP the **same model** gets upper N^{1+K mu+o(1)} for one unknown finite fixed K, then genuine lower margins g(mu) with g(mu)/mu -> infinity along a sequence of fixed mu down to 0 would contradict it. Existing CHMY bounds for mu>1/2 do not give that sequence. The needed same-model lower bounds remain OPEN.
- \`research/main/2026-10-18_PARTIAL_SAMPLE_WEDGE7.md\`: Hamming-boundary source-independent coordinate-sampling failure; not a universal reduction no-go.
- \`research/agents/threshold-descent/2026-10-18_1204_THRES_ENTROPY1.tex\` and \`research/main/2026-10-20_2253_MAIN_INJECTIVE_THRESHOLD_BARRIER25.tex\`: older YES-entropy and injective threshold descent barriers, retained as earlier mathematics.
- \`research/agents/magnification-redteam/2026-10-18_1919_MAGRED_STREAM_NO10.md\`: source sampling can preserve high-threshold NO while mislabeling original YES. The failure is *real*, not a spurious abstract path.
- \`research/agents/threshold-descent/2026-10-20_1440_THRES_CHMY_FIELDPAIR_CRITICAL4.md\`: field-mask aliasing and missing critical-window transfer, not a theorem about every CHMY generator.
- Recent TMR-2 Walsh-flat, TMR-3 GF(4) white-box factorization, TMR-4 cubic moment and TMR-5 robust easy families, plus original Claude ONETAPE/TPORT/DIRECTPRODUCT: compact algebra, sharing and model differences remain mandatory hostile controls.

Both root proof trackers were recovered (proof1 28,714 characters; proof2 authentic 1,051,196-character Git blob). Complete root main.tex recovered as authentic 2,542,866-character Git blob. Read all current TMR handoffs, latest issue #3, AGENTS, CODEX, repository skill, newest November 14 MCSP priority and November 13 role directive. No new general P=NP algorithm or unrestricted P!=NP lemma resulted. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex reserved for TMR-5. All tasks untouched.

## E. Exact missing implication and assignments

**Next load-bearing research question:** Can a *uniform, fully charged*, **both-label correct** transformation of an arbitrary MCSP[N^mu2] truth table into MCSP[N^mu1] with mu1<mu2 run in the same CHMY machine model, with time overhead tight enough to convert a hypothetical N^{1.01} low-threshold decider into a forbidden high-threshold randomized N^{1.99} decider? A lower-bound transfer must run from **known-hard high threshold to target low threshold**, and a mere inclusion of MCSP YES sets does not yield it.

TMR-1 owns exact reductions and quantifiers; TMR-2 should red-team source sampling and information access; TMR-3 should calculate same-machine one-way input/work-tape overhead and threshold exponents; TMR-4 should construct small counterexamples for lossy/promise mappings with both-label checks; TMR-5 independently audits CHMY thresholds, proof and any proposed transfers. None of these is a new schedule assignment; existing identities persist.

This conditional bridge has not been proved, and one cannot assume a compression oracle, answer table, proof-system-specific certificate, or nonuniform advice. A correct all-input polynomial 3-SAT machine remains a legitimate alternative outcome. **P versus NP remains OPEN.**

END_OF_REPORT::TMR1::023::2026-11-14_0908_PST
