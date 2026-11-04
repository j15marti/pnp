# LSPV-1 FINITE-HORIZON-UNIFORMITY-FIREWALL377

**November 3, 2026, 19:00 PST.** Status: **PROVED/EXACT**, elementary model/quantifier counterexample; **COMPUTATIONAL**, exhaustive finite toy-CNF controls; **KNOWN THEOREM**, Haken's restricted Resolution lower bound; **OPEN**, B1/B2/B3 and superpolynomial `Rmix341` worst-case minimum, and P versus NP. This is not claimed novel in complexity theory. No research target calculus, weight, task identity, enabled state, owner or schedule has changed.

## Target, fixed system, and prior evidence

Preserve exactly the source-authenticated combined calculus **`Rmix341`** defined in `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`): DIMACS parsing rejects malformed inputs; original signed clauses are free leaves; unit-cost distinct shared-DAG RES, AND3 with at most three original variables, binary GF(2) row XOR, certified constant-support LOCAL-CONVERT, and conservative paid signed two-input DEF. Count each distinct paid inference once, not every reference. Intermediate representations may be large, and native time/space are accounted separately. The unsettled precise grammar for exposed internal LOCAL-CONVERT gates is unchanged.

For any valid UNSAT F, use the attained minimum

$$
W_R(F)=\min_{\pi\in\mathrm{Ref}_R(F)}\sum_{v\in\mathrm{Paid} (\pi)}1,
\qquad
\overline W_R(N)=\max_{\substack{F\in\mathrm{UNSAT}\ \,|\mathrm{enc}(F)|\le N}}W_R(F).
$$

Empty maximum is zero. The minimum exists because Resolution is complete and all paid weights are nonnegative integers; original sources are not paid nodes. B1: `forall uniform correct A exists polynomial p_A forall UNSAT F: W_R(F)<=p_A(N_F+T_A(F))`. B2: `forall uniform correct A exists polynomial p_A forall N: Wbar_R(N)<=p_A(N+T_A^wc(N))`. B3: `SAT in P => Wbar_R(N)=N^O(1)` in this *same preselected R*. All three are **OPEN** for `Rmix341`. Do not reverse B1 => B2 => B3.

**Published hard-family starting point, not re-proved:** Haken, *The Intractability of Resolution*, TCS 39 (1985), 297–308, proves that there exist c>0 and h0 such that for all h>=h0, **every** unrestricted shared-DAG ordinary Resolution refutation of the standard unary PHP(h+1,h) original CNF has at least 2^(c h) lines. The original signed clauses have v=h(h+1) variables and m=(h+1)+h*binom(h+1,2) clauses, with explicit signed-length N_h=Theta(h^3 log(h+2)). In inference-node charging, W_Res(PHP_h)>=2^(ch)-m, not a machine-time bound. Buss's polynomial Frege proofs and previously established ER shortcuts prevent transporting this lower bound to `Rmix341`. Likewise Resolution-hard expander odd-Tseitin has a verified 4h-1 mixed AND3/GF(2) shortcut on bridgeless cubic instances. These are mandatory countercontrols.

## New proved theorem: finite-horizon nonuniform minimax collapses, even on all SAT inputs

Let L be **any decidable binary language**, including exact encoded general CNF-SAT with a third explicit MALFORMED output. Fix any total correct general decider D for L, for example fully charged exhaustive assignment enumeration on valid CNFs after parsing.

**Theorem 377 (finite-horizon minimax degeneracy).** In the ordinary deterministic Turing-machine model where a machine's **fixed finite-control transition table is not charged as per-input work tape**,

$$
\boxed{
\forall N\ge0\;\exists\text{ one total, correct deterministic decider }A_N:
\quad
\forall x\in\{0,1\}^{\le N},T_{A_N}(x)\le |x|+O(1),S_{A_N}(x)=O(1).
}
$$

The time and space constants for the short-input scanning phase can be chosen independent of N. The code/finite-state description of `A_N` is **not** bounded uniformly in N and may be of size O((N+1)2^N). The sequence `(A_N)_N` is *not* one fixed uniform SAT decider.

**Proof.** For a chosen N, decide the finite set of *all* binary strings of length at most N using the already-fixed total correct D. Store the resulting SAT/UNSAT/MALFORMED answer at the terminal of the complete binary prefix trie, with one finite-control state `q_u` for each prefix u of length <= N. On symbol 0 or 1, move from `q_u` to `q_{ub}` if the new prefix has length <= N. On an endmarker, output the prestored exact answer. A scan of x with length <= N consumes |x| symbols and one endmarker; it uses zero writable scratch bits beyond finite control. If the input has more than N bits, transition to an ordinary fixed fallback state, rewind the unchanged read-only input, and run D. This ensures correct SAT, UNSAT and malformed classification **on every length**, not only the preferred horizon. A complete trie needs 2^(N+1)-1 prefix states and exponentially many terminal labels; standard binary enumeration plus D can precompute the table, but compiler time/description are not free in any physical deployment. This construction establishes the stated quantifiers, not uniform polynomial-time SAT.

**Corollary 377.1:** under this per-machine time metric,

$$
\inf_{A\in\mathrm{TotalCorrectSAT}}\max_{|x|\le N}T_A(x)\le N+O(1)
\quad\text{for each fixed }N.
$$

In contrast,

$$
\exists\text{ one fixed uniform }A\;\exists C,k\;\forall N:
T_A^{wc}(N)\le C(N+1)^k
\quad\Longleftrightarrow\quad\mathrm{SAT}\in P.
$$

The first expression permits choosing a **different exponentially described algorithm at each N**; it therefore cannot replace the fixed-A worst-case quantifier of B2 or the conditional existence of a single polynomial-time algorithm in B3. This remains true even when the finite-horizon maximum covers **every** binary input, not merely a syntactically recognizable hard family. In particular, placing Haken PHP_h at N=N_h gives a length-N_h nonuniform decider running in O(N_h) steps on all inputs through N_h, without contradicting Haken's proof lower bound. This is a **quantifier/algorithm-independence counterexample**, not a new SAT lower bound.

**Corollary 377.2 (description-cost firewall):** The constructive table/trie uses O((N+1)2^N) bits of static transition representation, plus offline work of at least table serialization and up to full brute-force enumeration. A **fixed universal machine** reading this code as an explicit input must account for its code access, compilation and simultaneously live storage; the finite-control time and O(1)-scratch claim is not automatically an efficient fully charged implementation. An invocation of a separate code-specific machine at each N is nonuniform. Replacing a proof DAG's free minimization by such a per-N machine minimization silently changes the research question.

## Exact falsifiers and dispositions

**F1 (uniform quantifier attack):** Claim that the collection `A_N` is one algorithm A with runtime O(N). **FALSIFIED:** N is compiled into the finite control and the number of states grows exponentially; no uniform polynomial-time decider follows.

**F2 (bit-cost attack):** Treat O(1) scratch tape on horizon as O(1) total physical space or free compilation. **FALSIFIED:** program description and all-input answer labels can require exponential bits in this construction. On a fixed universal machine, access/loading costs cannot be dropped.

**F3 (hardness transport attack):** Transfer Haken's exponentially many Resolution lines to the runtime of `A_N`, or to `Rmix341`. **FALSIFIED:** those count different models; PHP has a polynomial ER/Frege escape; odd-Tseitin has an affine mixed escape. No polynomial-cost backtranslation to Resolution was provided.

**F4 (label or grammar attack):** Change SAT to UNSAT on some original valid input, or silently accept a malformed string. **COMPUTATIONAL PASS** under the explicitly declared small binary grammar and independently written evaluator. This does not establish computational hardness.

## Completely reproducible finite controls

Scripts are independent complete Node.js programs with no package dependencies. The toy grammar is `1|cc|(ll|vs)*`, where cc is a two-bit clause count (0..3), ll is a two-bit clause length (0..3), and vs is a two-bit signed literal over variables x1,x2; an incomplete or overlong record is malformed. This grammar is *an experiment only*; it does not change the target R's DIMACS encoding. Both implementations independently enumerate **all** 2^(N+1)-1 strings of lengths 0 through N, for N in {3,5,7,9,11,13} and classify each as SAT/UNSAT/MALFORMED. At N=13, they agree on 217 SAT, 291 UNSAT, 15,875 malformed; 16,383 total strings. The producer performed 21,870 assertions and independent verifier 21,860. Representative opposite labels include `11001000100` SAT and `11001000101` UNSAT. The empty formula is SAT, a single empty clause UNSAT, malformed records are rejected. Independently counted K4 parity controls are 8 even and 0 odd models.

This enumeration checks the static finite tables and both labels, *not* a physical finite-state compiler, an arbitrary DIMACS solver, asymptotic theorem, FLMV resource pair, or R proof minimum. The proof above is symbolic. Discovery/precomputation of the table can be exponentially expensive; the optimum logical R-DAG, its encoded evidence length, verification cost and real machine time/space remain distinct. All source/index/head reads, fallback parsing, output, caches, and transient memory are chargeable in any actual implementation.

## Research prior-art and duplicate/objection audit

**Current project:** The primary fixed calculus and XOR shortcut are LSPV-2/341, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`; LSPV-1/375, blob `92e5a295c53a58c003004ff36a59294546740310`, gives a restricted explicit-row ER2 simulation; LSPV-1/376, blob `7081bd7a6265e738d8b0db493ad57de56dce8dfe`, gives a root-private circuit proof-existence quotient, not polynomial proof-translator time. Related older LSPV-4/341 and Red Team/295 show that padding a **single uniform algorithm's worst-case time** can separate per-decider pointwise and worst-case statements. This result addresses a *different* quantifier trap: even `min_A max_{|x|<=N}` is invalid when A is allowed to change with N. A repository code search for `finite horizon optimum decider hardcode SAT` returned no matches; this is not evidence of global novelty.

**Grok actually read:** `GROKPROOF/2026-11-04_0116_PROGRESS.md`, blob `ca5a835356eb918b8cb4ab94d14de6174edeab03`. Its soundness and all-input FLMV route explicitly fixes one uniform polynomial-time algorithm; the missing charged transfer remains OPEN. A horizon-specific giant automaton would *not* meet that quantifier. **Claude actually read:** `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4`, and `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`. Their machine-model and restricted alternation-trading conclusions do not imply B2/B3 for arbitrary random-access SAT solvers; arbitrary finite-control advice at each N cannot be smuggled into their fixed uniform algorithms.

**Primary literature checked:** Haken (1985), exact ordinary Resolution scope; Cook–Reckhow (1979), existence of *some* p-bounded system equivalent to NP=coNP, not p-boundedness of fixed R; Buss (1987), polynomial Frege proofs of PHP, showing the Resolution escape. See Stanford Encyclopedia of Philosophy (Computational Complexity, Spring 2026), Cambridge University Press JSL Buss article and Haken references. Web queries on 2026-11-03: `Haken Intractability of Resolution pigeonhole exponential 1985 proof length`; `Cook Reckhow 1979 polynomially bounded proof systems NP coNP theorem`; `Blum speedup theorem time complexity complexity measures nonuniform finite functions hardcode table`; `site:github.com/openai SAT solver CNF proof checker OpenAI repository`; `site:github.com/openai proof verification SAT solver`. No applicable first-party `github.com/openai` SAT/proof checker source was identified by these last two searches. Blum's speedup theorem is a distinct result and is not used as a premise here.

## Bridge classification and next exact obligation

**B1 OPEN, B2 OPEN, B3 OPEN for fixed Rmix341.** The horizon-trie construction **does not refute any B1/B2/B3 claim**, because it depends on N; nor does the proof lower bound imply P!=NP. What it definitively falsifies is an algorithm-independent "optimal work at each input length" invariant that optimizes over unrelated programs but fails to charge their program descriptions. The strongest promising invariant is a **uniform all-N optimization** over one fixed decider/program, with explicit encoding-equivalence and verified proof-cost transfer, not a scatterplot of free per-N optimal machines. The next substantive B3 obligation is an actually certified fixed-R correctness/reflection or weak length-simulation theorem covering all admitted rule types, without hiding the SAT answer in representation or choosing a fresh machine per horizon.

**Publication targets:** `research/agents/lspv-1/2026-11-03_1900_LSPV-1_FINITE_HORIZON_UNIFORMITY_FIREWALL377.md`; code `experiments/arc/lspv1_377_horizon_minimax.js` and `experiments/arc/lspv1_377_independent_verify.js`; immutable records `results/raw/arc/2026-11-03_1900_LSPV1_HORIZON_MINIMAX377.json` and `_independent.json`; five-role coordination handoff. Preserve root main.tex outside its LSPV-1 markers and do not modify tasks.
