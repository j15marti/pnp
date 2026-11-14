# TMR-4/031: Efficiently indexable full truth tables necessarily collapse into positive-power MCSP YES at exponential output lengths

**Pacific timestamp:** 2026-11-14 15:37 PST (America/Los_Angeles). **Role:** TMR-4 Cost-Sound Abstraction. **Status:** NEW **PROVED/RESTRICTED** elementary indexed-output compiler theorem with self-contained spatial simulation proof; small finite checks **COMPUTATIONAL**; independent TMR-1/TMR-5 review **OPEN**. Neither P=NP nor P!=NP is proved.

## 1. Exactly what changed

The earlier TMR-4/030 direct compiler bounded the gate count of one concrete masked SAT evaluation table. TMR-5/026 proved collapse under dummy-input table repetition, and TMR-1/029 quantified its near-tight universal padding exponent. The NEW INDEXLIFT39 theorem applies to **every fixed uniform, syntax-aware, arbitrary-preprocessing deterministic polynomial-time per-index evaluator**, not just a CNF gate-by-gate compiler or a padding operation. It includes nonlinear transformations, source-syntax analysis, compact algebra, and arbitrary branching inside the evaluator. It identifies a sharp scope condition, large target index arity relative to the source description length, and gives a counterexample showing that condition cannot be dropped.

This is a negative test for a proposed reduction architecture, not an MCSP decision lower bound.

## 2. Explicit theorem: full charges, quantifiers and proof

Fix a deterministic finite-alphabet multitape Turing machine E, with a fixed number of tapes, accepting inputs consisting of a source word F of **encoded length L** and a separate binary target index i of **length n**. E halts on every such pair and emits one bit. Let

$$
Y_{E,F,n}[i] := E(F,i),\qquad i\in\{0,1\}^n,\qquad N:=2^n,
$$

where the bracket denotes the i-th bit of a hypothetical **complete** target truth table. Write

$$
t_{E,F,n}:=\max_{i\in\{0,1\}^n} T_E(F,i)
$$

for the worst-case actual transition count over the N indices, on this **same fixed E**. Boolean circuits use fan-in-two AND/OR, unary NOT, unrestricted fanout, free constants and input wires; gate count is the complexity measure.

**INDEXLIFT39 theorem (PROVED/RESTRICTED).** There is a constant K_E depending only on the fixed machine E and its alphabet/tape count such that for every F,n,

$$
CC_n(Y_{E,F,n})\ \le\ K_E(L+n+t_{E,F,n}+2)^2.
$$

**Proof.** Fix F and n. The n index bits are the circuit inputs; every bit of F is a hardwired Boolean constant. Pad the machine after any early halt by an absorbing terminal state. During at most t transitions, each of its fixed finitely many heads can visit only O(L+n+t) tape positions. Encode the finite machine state, each tape-cell symbol and each head position by one-hot Boolean wires. In a synchronous layer, read the scanned symbol by OR-ing the O(L+n+t) position-qualified symbols. The fixed finite transition table computes the next control and write symbols with O(1) further gates per constant-size state combination. For each possible tape position, update its local symbol conditional on the head-indicator and shift the head-indicator according to the selected left/right/stay control. Thus one complete concrete transition has a Boolean-layer simulation of O(L+n+t) AND/OR/NOT gates. Unroll t layers, including initial configuration binding and the correct terminal output wire. Total gate count is O(t(L+n+t)) plus O(L+n+t), dominated by K_E(L+n+t+2)^2. The compiled circuit faithfully executes **every transition** of E, including formula-syntax preprocessing, input rereading, intermediate workspace, sharing and output. Only the source F is fixed as circuit advice; E itself is the same fixed program for all F and n. This is a nonuniform *upper bound on the target Boolean function*, not uncharged construction of a SAT decider or a claim about polynomial-time materialization of Y. QED.

**MCSP consequence.** If s(n)=floor(2^(mu*n)), mu>0 fixed, and

$$
2^{\mu n}\ \ge\ K_E(L+n+t_{E,F,n}+2)^2,
$$

then Y is an ordinary exact MCSP[s(n)] **YES** instance. Because a size-s circuit is an exact match, Y is also not a promised Hamming-far Gap-MCSP **NO** instance for the same circuit class, for any positive distance parameter. This step uses no hard-to-check minimization oracle.

If E has worst-case bit-evaluation time bounded by c(L+n+1)^d for fixed c,d and a family of source/index lengths satisfies

$$
\frac{n}{\log_2(L+n+2)}\longrightarrow\infty,
$$

then **both** SAT and UNSAT source families, when mapped through such E to full tables, eventually become MCSP YES at **every fixed mu>0**. For example, source L=poly(v), index n=v and N=2^v satisfy this condition. The result is uniform in each fixed program E, not a single constant uniform over all possible evaluators.

A useful contrapositive: if Y is ordinary MCSP[s(n)] NO then

$$
t_{E,F,n}\ >\ \sqrt{s(n)/K_E}-L-n-2,
$$

with a harmless one-unit floor adjustment when necessary. Under L+n=o(N^(mu/2)), a fixed E indexing an MCSP[N^mu] NO table must take Omega(N^(mu/2)) transitions on **at least one** index. This does **not** imply that deciding source SAT requires that time.

**Fully materialized output charge:** Producing an N-bit target table consumes Omega(N) bit-output operations. For N=2^v with source length L=poly(v), the map is not a polynomial-time many-one reduction from 3-SAT to ordinary explicitly encoded MCSP even though its bits are efficiently indexable. An implicit index circuit is an instance of a *different succinct target problem* unless a definition-preserving, fully charged transfer is established.

## 3. Sharp counterexample when output is polynomial in source size

**No general collapse at n=Theta(log L).** Fix any 0<mu<1. For each n, let L=N=2^n and take the source word F to be an *arbitrary* N-bit truth table. A single uniform fixed E, receiving (F,i), scans its source to the indexed location and returns F[i] in O(L+n) time. Therefore the map F -> Y=F is polynomial-time bit-indexable, yet there exist F such that CC_n(F)>floor(N^mu). Indeed, the number of circuits with at most s gates is at most

$$
D(n,s)=(s+1)(n+s+2)\,[3(n+s+2)^2]^s.
$$

At s=floor(N^mu), log_2 D(n,s)=O(N^mu log N)=o(N), whereas there are 2^N truth tables. Some F is therefore a genuine MCSP NO for all sufficiently large n. This is an **existence** proof, not an efficiently explicit high-complexity function, and F in this sharpness example is a general source word, **not claimed to be a proper 3-CNF**. It shows why the source-length/index-arity hypothesis is mathematically essential.

## 4. Exact primary-source and model table

| Source, version and location | Exact relevant claim and limitations |
| --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, **STACS 2021**, Theorem 1, printed p.23:3, https://doi.org/10.4230/LIPIcs.STACS.2021.23 | Ordinary exact MCSP[2^(mu1 n)] on **full N=2^n** truth tables; deterministic one-way read-only input plus one two-way work tape; exists a sufficiently small fixed mu1>0 such that **MCSP outside DTIME_1[N^1.01] implies P!=NP**. This antecedent remains OPEN. |
| Same, Theorem 2, p.23:3 | A different larger mu2, close to one, yields unconditional randomized two-sided-error **MCSP outside BPTIME_1[N^1.99]** in the same one-way-input/one-work-tape model. The stronger exponent does not match Theorem 1's threshold. |
| McKay, Murray, Williams, **STOC 2019**, original author PDF pp.2-3, Theorems 1.2-1.3, https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf | For time-constructible s(n)>=n and an oracle A, search-MCSP^A[s] on full N-bit table has one-pass streaming with Sigma_3SAT^A queries of length tilde O(s), tilde O(s) space and tilde O(s^2) update. Failure of polynomial-in-s space and update for suitable A in PH implies P!=NP. This is **search/oracle** MCSP, not an unrestricted exact plain decision lower bound. |
| Pippenger and Fischer, **JACM 26(2), 1979, pp.361-381**, DOI https://doi.org/10.1145/322123.322138 | The original paper's abstract records an O(t log t)-size combinational network simulation of t-step computations on one-dimensional tape machines. Our coarser O((L+n+t)^2) finite-state unrolling bound is **proved independently above** and does not assume the stronger optimal simulation bound or change the input-access model. |

Primary CHMY and MMW theorem statements and exact thresholds were verified against original publisher/author PDFs and page screenshots; Pippenger-Fischer's author/publisher abstract was checked. No transfer between MKTP, Gap-MCSP, succinct MCSP and ordinary MCSP is inferred.

## 5. Relevant prior corpus and hostile controls

| Original path | Established scope retained |
| --- | --- |
| research/agents/tmr-4/2026-11-14_1439_TMR4_POSITIVE_POWER_COMPILER_FIREWALL030.md, experiments/tmr/tmr4_power_compiler033.js, results/raw/tmr/2026-11-14_1439_TMR4_POWER_COMPILER033_RAW.json | Prior direct masked-SAT gate cap, narrower syntax-aware table compiler; PROVED/RESTRICTED |
| research/agents/tmr-4/2026-11-14_1336_TMR4_ORACLE_LOCALITY_GAP_MASK029.md and original code/raw | Prior source-independent evaluation-query gap bound; does not allow syntax; PROVED/RESTRICTED |
| research/agents/tmr-2/2026-11-14_1521_TMR2_RSPARSE_HYPERGEOMETRIC_QUERY030.md and original code/raw | Prior r-sparse shared preprocessing, independently restarted outputs, source-independent oracle; PROVED/RESTRICTED pending review |
| research/agents/tmr-5/2026-11-14_1452_TMR5_DUMMY_PADDING_UNIVERSAL_COLLAPSE026.md and original code/raw | Prior dummy-table repetition; exact circuit size unchanged under padding |
| research/agents/tmr-1/2026-11-14_1504_TMR1_PADDING_WINDOW_NEAR_TIGHT029.md and original code/raw | Prior near-tight universal dummy-padding threshold; counting result |
| research/agents/tmr-3/2026-11-14_1455_TMR3_TWOWAY_HEADER_NETWORK_BRIDGE029.md and original code/raw | Prior two-way rewind and network serialization; one-way transfer remains OPEN |
| research/agents/tmr-4/2026-11-14_0836_TMR4_MOMENT_CONGRUENCE_AND_QUOTIENT_COUNTEREXAMPLE023.md | Cubic Walsh moment state is sufficient for source clause-stream continuation in a restricted model; second-order quotient loses a SAT/UNSAT distinction |
| research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex; research/agents/tmr-4/2026-11-14_1142_TMR4_GAPMCSP_AFFINE_KERNEL_CYLINDER027.md | Fixed affine sketch/hash kernel collision, not a generic nonlinear source-compiler lower bound |
| research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex; research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex; comments/grok-4.7/2026-10-21/2026-10-21_0013_GROK_REVIEW.tex | Original portfolio, crossing-sequence and prior failed transfer controls, none closes arbitrary-machine SAT lower bound |

Horn, duplicated-literal 2-SAT, parity/XOR-clause families, disjoint variable components, unique-witness and UNSAT cases are not hard for the explicit gate compiler: preprocessing can be hardwired or recomputed and their actual circuit upper bound is respected. Gaussian-elimination, bounded-treewidth, compact algebra, sharing, semantic quotients, arbitrary input rereads, padding and renaming remain permitted. No unconditional SAT time is inferred from truth-table entropy or prescribed representations.

## 6. Actual executed evidence and limits

The exact standalone source **experiments/tmr/tmr4_indexable_lift039.js** was executed in hosted ECMAScript V8, with exact immutable result **results/raw/tmr/2026-11-14_1537_TMR4_INDEXABLE_LIFT039_RAW.json**. All **33,344 assertions passed** with zero failures. The run covered **597 formulae**, **1,194 complete small truth tables**, **28,992 direct-vs-gate-circuit bit comparisons**, **16 finite head-state micro-simulations with 1,020 bit checks**, **900 exact BigInt positive-power threshold comparisons**, and four nonconstant output controls. Both syntax-controlled checksum branches occurred. The formulas include an eight-clause UNSAT, seven-clause unique-witness, Horn, duplicated-literal 2-SAT, parity and disjoint-component controls. There was no randomness.

A second separately saved native Node.js v22 source run in a container produced the **same counts**, but that local file is not asserted to be byte-identical to the published script. The hosted-V8 original is the published reproducer. The tests are finite **COMPUTATIONAL** checks of the explicit gate DAG and a small finite-control head simulation, **not** a general Turing-machine compiler or asymptotic proof. The general simulation bound follows from the symbolic layer construction above. Large-n crossover checks are symbolic integer arithmetic; no exponential truth tables were allocated.

## 7. Exact remaining proof gap, ownership and requests

The new obstruction only retires **exponentially long outputs with polynomial-time indexed bits** as a way to create positive-power MCSP NO instances. It does not rule out polynomial-output, fully shared syntax-dependent reductions, or a direct one-way-one-work-tape MCSP lower bound. The exact CHMY-small-mu ordinary MCSP N^1.01 decision-time exclusion is still OPEN. A polynomial-output reduction at N=poly(L), with n=O(log L), does not satisfy the collapse hypothesis. A general SAT solver's behavior is not restricted to evaluating this one proposed table.

**Next target:** investigate a polynomial-output, globally shared syntax-aware reduction with complete source/target length accounting and both-label correctness, trying first to construct a short compiled circuit from its shared output generator and then seeking a concrete counterexample. **Peer requests:** TMR-1 audit quantifiers, floor and N versus L; TMR-5 independently rebuild the one-hot all-transition upper circuit and the n=log L counting counterexample; TMR-2 compare the fully source-aware result with its independently restarted oracle-query bound; TMR-3 audit physical table-emission time.

**Preflight:** controlling 2026-11-14 directive read FIRST and rechecked at Git blob 1e11aa64a0b0d635a65cea58500b09f2b0fe010a; then 2026-11-13 TMR replacement, AGENTS.md, CODEX.md, pnp skill, latest five handoffs, issue #3 through TMR-2/030, original TMR/Claude/Grok/legacy evidence. Complete root proof1.txt 28,714 chars blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343; full authentic proof2.txt recovered via Git blob 930c5eeddafce656717f28055a7a9a755f44737c (1,051,196 chars); full authentic main.tex recovered via Git blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 (2,545,859 chars). **TRACKERS REVIEWED; NO MATERIAL CHANGE** because all P-versus-NP load-bearing implications remain OPEN. Root main.tex is TMR-5 owned and unchanged. No schedules or identities modified.

END_OF_REPORT::TMR4::INDEXLIFT39::2026-11-14_1537_PST
