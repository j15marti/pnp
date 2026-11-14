# TMR-3/024: fixed-network serialization and the MCSP exponent firewall

**Pacific timestamp:** November 14, 2026, 09:36 PST (America/Los_Angeles).  
**Role:** TMR-3, the NEW PNP Time-Space Tradeoffs agent.  
**Scope:** MCSP-specific resource ledger and a symbolic fixed-processor simulation theorem with finite hostile tests.  
**Statuses:** FIXED-NET24 is **CANDIDATE/RESTRICTED** pending TMR-1/TMR-5 independent review. The explicit network/proxy tests are **COMPUTATIONAL**. Unrestricted P versus NP remains **OPEN**.

## 1. Current scientific priority and corpus

Read first the authoritative \`research/coordination/2026-11-14_MCSP_FIVE_AGENT_REVIEW.md\` (blob \`1e11aa64a0b0d635a65cea58500b09f2b0fe010a\`), then the 2026-11-13 TMR replacement directive (blob \`47459817e66dccf1f3079e6c724c0fd2643e7bc4\`). Both complete root proof trackers were recovered (proof1 28,714 characters SHA \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`; proof2 1,051,196 characters SHA \`930c5eeddafce656717f28055a7a9a755f44737c\`, via GitHub contents fallback). The 2,545,859-character canonical root main.tex was recovered and the TMR ownership/OPEN region checked, rather than interpreting a blank standard-file response as an empty file. Root main.tex SHA \`6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34\`. Read AGENTS.md, CODEX.md, the research skill, all five TMR handoffs, issue #3 through TMR-1/023, and relevant original reports including those named below. The full preflight script and LaTeX compile are not executed in this connector session.

### Relevant original-research ledger

| Record and actual path | Adopted result and status |
|---|---|
| TMR-1/023: \`research/agents/tmr-1/2026-11-14_0908_TMR1_MCSP_PARAMETER_SHELL023.md\` | CANDIDATE/RESTRICTED elementary strict circuit-threshold shell; demonstrates that distinct MCSP thresholds are distinct languages for large lengths, but does not rule out reductions |
| TMR-3/023: \`research/agents/tmr-3/2026-11-14_0842_TMR3_GF4_ORACLE_COMPOSITION_FIREWALL023.md\` | CANDIDATE/RESTRICTED black-box GF(4) extension-query necessity and cheap white-box OR evaluation; no SAT/MCSP time transfer |
| TMR-5/020: \`research/agents/tmr-5/2026-11-14_0858_TMR5_GF4_CANCELLATION_MOMENT_TRACE020.md\` | CANDIDATE/RESTRICTED cheap semantic GF(4) collisions, and distinct physical time for the same Walsh moment summary; forbids treating semantic completeness as cost congruence |
| Claude: \`research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex\` | Project-reported one-tape crossing-sequence theorem also applies to nondeterministic computations; wrong tape model for uncharged multiwork-tape network |
| Claude: \`research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex\` | Project-reported restricted alternation-trading portfolio barrier, not a universal SAT or MCSP network lower bound |
| MCSPMAGCONE1: \`research/main/2026-10-17_2145_MAIN_MCSPMAGCONE1.tex\` and \`research/main/2026-10-18_ASYMPTOTIC_CONE5.md\` | CONDITIONAL cofinal exponent-margin argument; no actual magnification-threshold lower bound |
| Sparse-template failure: \`research/agents/threshold-descent/2026-10-20_1700_MCSP_SPARSE_TEMPLATE_KT_FIREWALL1.md\` and \`research/agents/threshold-descent/2026-10-20_1800_MCSP_SPARSE_TEMPLATE_NOGO5_BRIEF.md\` | PROVED/RESTRICTED short indexed descriptions defeat proposed high-KT promises; never equate sparse truth-table construction with a hard MCSP/MKTP instance |
| \`research/governance/2026-10-26_DUAL_TM_RESOURCE_ACCOUNTING_DIRECTIVE.md\` | Earlier explicit distinction between ordinary one-tape and fixed-k multitape models; scientific resource firewall retained, old role allocation superseded |

Search also surfaced earlier MKTP prefix/low-image failures, Grok progress and legacy ARC/FLMV small-space/cost transfer work. These are controls, not a new proof of any MCSP bound. No original experiment of another role was represented as freshly rerun.

## 2. Exact primary-source theorem and model table

Here N=2^n is an input truth-table length, n is its arity, and L is the independent encoded 3-SAT source length. MCSP[N^mu] means exact ordinary decision whether an n-input Boolean function has fan-in-two Boolean circuit size at most N^mu, with threshold rounding fixed by the representation.

| Source, exact theorem | Problem, model and quantified resource | Exact conclusion / gap |
|---|---|---|
| Cheraghchi, Hirahara, Myrisiotis, Yoshida (CHMY), ECCC TR20-103 2020, STACS 2021 Theorem 1; Appendix A Theorem 47 | Exact ordinary MCSP[N^mu1] with a **one-way read-only input and one two-way read/write work tape**; one fixed finite deterministic machine, worst-case time N^1.01, for **some sufficiently small** mu1>0 | Conditional: if this particular low-threshold language is outside DTIME_1[N^1.01], then P!=NP. P=NP implies a compatible one-tape algorithm for some small mu1; no numeric mu1 is fixed independently of its polynomial exponent |
| CHMY Theorem 2 and Section 2.2 | Ordinary MCSP[N^mu2], same physical interface, **randomized bounded two-sided error**; some mu2 close to 1, mu2>mu1 | KNOWN THEOREM: language outside BPTIME_1[N^1.99]. Lower exponent is stronger, but at a **different decision threshold**; the theorem alone does not discharge Theorem 1 |
| CHMY Theorem 3 | For any oracle O, every fixed 1/2<mu<1, MCSP[N^mu], oracle machine with same one-way read-only input and one two-way work tape, bounded-error randomization, queries length N^{o(1)} | KNOWN THEOREM: excludes N^{1+delta(mu)} time for some positive delta. This is a barrier to the specific short-query algorithm architecture at large mu, **not** a lower bound for unrestricted multitape machines |
| CHMY Lemma 9 | One-pass streaming algorithm with per-update time t(N), simulated on the same one-work-tape plus one-way input | KNOWN THEOREM: total time O(N poly(t(N))); polynomial hidden degree matters to choosing a suitably small mu under P=NP |
| McKay, Murray, Williams, STOC 2019 Theorems 1.2/1.3 | **Search-MCSP^A[s(n)]**, not ordinary decision MCSP; one-pass streaming, arbitrary A in PH; short Sigma_3SAT^A oracle queries, N-bit explicit truth table | KNOWN THEOREM: oracle algorithm has update ~O(s^2), space ~O(s), total N~O(s); failure of poly(s) update AND space streaming search algorithms for some time-constructible s>=n implies P!=NP |
| Oliveira and Santhanam, FOCS 2018 | MCSP[2^sqrt(n)] with average-case formula-size conditions; different approximation definitions | Magnification to nonuniform *formula* complexity; not directly an ordinary MCSP one-tape decision lower bound |
| Oliveira, Pich, Santhanam, CCC 2019 | Gap-MCSP or Gap-MKtP, distinct small/large thresholds and a promised-gap decision, nonuniform circuit-size conditions | Conditional consequences such as NP not in P/poly; exact promise and threshold must be preserved |
| Chen, Hirahara, Oliveira, Pich, Rajgopal, Santhanam, ITCS 2020 / JACM 2022 | Oracle-locality simulation framework for magnification targets, small-query oracle gates | Locality barrier: certain broadly stable lower-bound techniques also apply to short-query oracle circuits. This restricts a METHOD, not all possible lower-bound proofs |
| Allender and Hirahara, MFCS 2017, journal 2019 | Approximate MCSP/MKTP under an explicit one-way-function assumption, plus nonuniform local reductions for MKTP | CONDITIONAL NP-intermediate/approximation conclusions and other restricted MKTP consequences; no unconditional SAT decision or uniform network lower bound |

**Original primary sources checked:** CHMY https://eccc.weizmann.ac.il/report/2020/103/download/ (Theorems 1-3, Definitions 8, 2.2, Lemma 9, Theorem 47); McKay-Murray-Williams https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf (Theorems 1.2,1.3); Oliveira-Santhanam https://www.dcs.warwick.ac.uk/~igorcarb/documents/papers/OS18b.pdf ; Oliveira-Pich-Santhanam DOI https://doi.org/10.4230/LIPIcs.CCC.2019.27 ; Chen et al. DOI https://doi.org/10.4230/LIPIcs.ITCS.2020.70 ; Allender-Hirahara DOI https://doi.org/10.4230/LIPIcs.MFCS.2017.54. CHMY and MMW PDF text and rendered pages were checked, but the remaining citations are used only for the scope explicitly recorded in the available original abstracts, not unsupported quantitative theorem refinements.

**Critical parameter firewall:** mu2>mu1. From MCSP[N^mu2] outside BPTIME_1[N^1.99], **one cannot infer** MCSP[N^mu1] outside DTIME_1[N^1.01]. Neither monotone inclusion of YES sets nor greater time exponent transfers a lower bound across the threshold. TMR-1/023 proves thresholds can have a genuine strict shell.

## 3. NEW FIXED-NET24: conservative quadratic serialization theorem

**Model.** Fix an integer p>=1 independent of N, one finite deterministic processor program per stage, and a fixed finite directed channel graph. Every processor has one locally moving, two-way read/write work tape and finite control. A single read-only input head moves only right; at most one new source symbol is revealed per synchronous round and can be broadcast to processors. Between rounds, channels may transmit a constant number of symbols per fixed directed edge with **one-round latency**, all through bounded finite alphabets, and may have physical FIFO storage with locally moving heads when explicitly charged. All local work-head movements, tape writes, channel messages, source reads, and final classification are counted. There is no free random access, unbounded-word operation, global oracle, or N-dependent finite control. A terminal answer must be defined for all binary source lengths, with malformed encodings handled by the fixed program.

For any such fixed network of p processors, if its worst-case elapsed rounds on N-bit input are R(N), then one deterministic finite program with **one two-way read/write work tape and the same one-way read-only source input** simulates all network executions and both terminal labels in

$$
T_{\mathrm{1work}}(N)\le c_p\,(R(N)+1)^2,\qquad
S_{\mathrm{1work}}(N)\le c_p\,(R(N)+1).
$$

Here c_p depends on the single *fixed* network, fixed channel geometry and alphabet, never on N or source label.

**Proof.** Represent the p virtual work tapes and finitely many locally moving channel buffers as tracks of a single finite-alphabet work tape. Their number is fixed, so their product alphabet and controller are finite. Represent each virtual head by a marked track cell, and a pending move by a finite track tag. After t rounds, every work head and channel head has moved at most t cells from its starting position; at most O_p(t+1) physical tape columns are relevant, including any written/received message bits. At round t, read at most one next source bit from the physical one-way head and hold that symbol in finite control. Sweep the occupied interval, record the p finitely many virtual current symbols and old incoming channel symbols, compute all finite transition functions, then sweep again to commit their writes/head movements and the next-round messages. This resolves pending left moves that would otherwise lie behind the first sweep, preserves synchronous message latency and all state-dependent adaptivity. The source is never rewound. Every round costs at most O_p(t+1) adjacent work-tape transitions, and summing t=0,...,R-1 gives O_p((R+1)^2); the physical work tape visits O_p(R+1) columns. Terminal labels and all source bits actually accessed are preserved.

**Scope limitations:** fixed p and fixed link graph are essential to this exact constant-alphabet proof. When p=p(N) grows, finite control, topology specification, fan-out, addressing, queue scheduling, uniform fabrication and message interfaces must all be charged in a *new* compiler; the displayed bound may NOT be used with c_p treated as a uniform constant. A network whose processors have independent two-way source heads, random input ports or uncharged asynchronous channels is outside this theorem.

**Not a new known upper-bound theorem:** the quadratic single-tape sweep method is standard simulation machinery. The new project contribution is its exact restriction to the user's synchronously communicating, one-way-source network proposal and its MCSP parameter/exponent implication. This symbolic proof is offered for independent review rather than as a promoted unrestricted novelty claim.

## 4. Exact attempted transfer and why it fails to reach magnification

Apply the **KNOWN** CHMY high-threshold lower bound to a **hypothetical** fixed-p network for the **same** high-threshold language MCSP[N^mu2]. If the network ran in worst-case R(N)=O(N^rho) and 2rho<=1.99, FIXED-NET24 would supply a one-work-tape decider in O(N^1.99), contradicting CHMY Theorem 2 (deterministic programs are also bounded-error randomized programs). Thus, for this fixed-p architecture,

$$
R(N)\notin O(N^{199/200})\quad\text{for MCSP}[N^{\mu_2}].
$$

This is only a **near-linear** worst-case elapsed-round restriction and is not a pointwise lower bound at every length. If the network protocol explicitly consumes the entire N-bit truth table at one bit per round, it already has the stronger elementary floor R(N)>=N. So the transferred exponent 0.995 is strictly dominated by physical source acquisition. If the machine is permitted to halt early, that N floor must *not* be assumed, although the non-O(N^0.995) statement remains the correct consequence of CHMY for the restricted network.

Numerically, N^0.995/N=N^{-0.005}; at N=2^20,2^40,2^100 the ratio is 2^{-0.1},2^{-0.2},2^{-0.5}. The 1.99 exponent has been divided by the quadratic simulation overhead, **not transferred intact**.

At **low threshold mu1**, CHMY Theorem 1 would be satisfied by a genuinely independent proof of MCSP[N^mu1] outside DTIME_1[N^1.01]. If one tried to derive this through the same quadratic fixed-network serializer, an elapsed-round obstruction merely at R=N^{1.01/2}=N^{0.505} would again be weaker than an actual full stream scan. A lower bound against p fixed processors does not provide the needed single-tape lower bound unless it directly includes p=1 for the required low-threshold language (or another charged transfer is proved).

**NO dichotomy follows** that polynomially many machines imply superpolynomial elapsed time, or that polynomial time requires superpolynomially many machines. The proven result handles only fixed p. Polynomially growing p makes the network architecture itself N-dependent and requires a uniform finite simulator. Proving a genuinely strong network result would require a direct communication/computation invariant robust to shared state and multiple tapes, not this quadratic serialization.

## 5. Independently executed evidence

Native CPython program (not a machine-language one-tape compiler) was run after fixing a real first-version bug. The initial sweep used a range that omitted return to the physical origin and incorrectly revisited an update coordinate; the corrected version uses one leftward positioning pass, one update sweep using saved *old* virtual heads, and a return pass. The failing draft remains in the local audit notes; it is not the final source.

The corrected runner \`experiments/tmr/tmr3_mcsp_network024.py\` checks 2,044 complete binary streams with lengths 0 through 8 and p=1,2,3,4. The fixed network has delayed output bits on each link; its last stage computes OR of the source, so both output labels appear. Each local work head performs state-dependent left/right moves, updates and shares messages through finite links. Separately implemented direct-state and swept-track simulators agree on every final head position, finite-control bit and work-tape cell. Results: 2,008 YES, 36 NO, 20 additional malformed-input controls, 2,044 bounded sweep-cost checks, 207,782 adjacent-head moves, maximum 264 moves, zero final assertions. An independent exact rational exponent table checks 199/200=0.995 and the linear-input floor.

**Evidence classification:** COMPUTATIONAL finite Python test of a *sweep proxy*. It uses Python arrays/indices as an oracle to check a proposed track encoding, and it is **not** a native finite-alphabet one-tape machine execution. The symbolic sweep proof is separate; the experiment does not establish an MCSP lower bound or all-p network equivalence.

## 6. Barriers, negative controls and next exact target

- **Input representation and output:** full truth-table N=2^n, not a succinct SAT description L. Output is one bit; ordinary MCSP decision is not the same as MMW oracle-search compression, Gap-MCSP or MKTP.
- **Algebraic shortcuts:** Horn, 2-SAT, Gaussian elimination on XOR/Tseitin, bounded-treewidth DP, products, renaming and auxiliary variables can be inexpensive with compact representations; a transport bound or prescribed message DAG never forces their computation. The previous GF(4) OR and TMR-2/4 Walsh examples explicitly defeat inference from polynomial expression size/semantic alternatives to time.
- **Natural-proofs and locality:** CHMY Theorem 3 bars one specific short-query oracle algorithm at mu>1/2; Chen et al. show locality caveats. Neither says all algorithms are impossible.
- **All-exponent gap:** a lower bound for a narrow one-way-plus-one-work-tape model, even at small mu, is useful through a particular hardness-magnification theorem. It is NOT itself a resource lower bound for all deterministic general 3-SAT machines. The valid implication goes through that theorem and its correctly matched threshold, not through direct assertion.
- **Same machine:** p, source movement, message work, elapsed time and peak workspace are charged in the *same* simulated architecture; there is no borrowing of one machine's time and another's space.

**One next target:** TMR-1/TMR-5 should independently audit FIXED-NET24 and the exponent 199/200, then determine whether a *small-mu* MCSP instance family supports an intrinsically source-bound one-way, one-work-tape crossing/computation lower bound above N^1.01 which survives the CHMY/Chen short-oracle/locality controls. TMR-2 should challenge the assumed full-scan lower floor; TMR-4 should audit an explicit length- and threshold-preserving transformation, including both labels. None of these assignments changes any scheduled task.

**Trackers:** both root trackers recovered, reviewed and preserved; no material proof status promotion. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex unchanged by TMR-3, TMR-5 retains global synthesis ownership. No scheduling action was taken.

**P versus NP remains OPEN.**

END_OF_REPORT::TMR3::024::2026-11-14_0936_PST
