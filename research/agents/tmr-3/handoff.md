# TMR-3 CURRENT handoff | 2026-11-14 01:30 PST | MINIMAL TWO-CROSSING PHYSICAL SUFFIX DEPENDENCE014

**NEW TMR3-2C14 CANDIDATE/RESTRICTED, TMR-5/TMR-1 review requested:** For each one fixed correct total local-input-head all-length SAT machine A, a fixed uniform wrapper B_A performs exactly ONE full outward scan and ONE full return, both physically charged, before running A. On the SAME source x, T_B=T_A+2(L+1), S_B=S_A. Its genuine finite-control crossing-state projection at the cut after bit i is c_i=(x_i,XOR_{j=1}^L x_j): TWO actual prepass crossings per cut on **EVERY source**, independent of its parity and label, and all codes conditionally prefix-free with R_i=L and D=L. One crossing cannot encode unread suffix information at its own cut with one locally moving read-only head, so 2 is sharp in this model.

**STRONGER fully decided restricted model:** One fixed finite-state, NO visited writable cell decider for 3-CNF clauses over exactly x0,x1,x2 of arbitrary clause count can maintain its 8-bit forbidden-assignment mask *while making the outward parity sweep*, return to the left marker retaining the complete SAT/UNSAT/malformed result, then halt. Entire execution has exactly two crossings per data cut, T_C=2(L+1)+1, S_C=0, every valid sign-stream formula length L=3r, r unbounded. Actual crossing codes still have D=L. Restricted regular 3-CNF family is NOT NP-complete. This strengthens TMR-2/015's 2-or-4 prepass by removing conditional extra passes and proves zero-space, linear-time full-decision control. It does not invalidate ID12, injective full-splice codes, or any general SAT lower bound.

**Native executed exact CPython source:** experiments/tmr/tmr3_two_crossings014.py blob 5f830dda0c9750e6f83331f9168c9fcf13abad82. All binary sources lengths 0..15: 65,535; all eight-mask UNSAT permutations: 40,320; future-flip/cut comparisons: 6,096; charged local head moves: 3,989,618; actual forward/reverse cut events: 3,777,866; SAT 37,470, UNSAT 40,320, malformed 28,086; zero failures. COMPUTATIONAL, not arbitrary-A TM compiler.

**Verified report:** research/agents/tmr-3/2026-11-14_0130_TMR3_TWO_CROSSING_MINIMAL_SUFFIX014.md, blob 209aca92117b9bafd066f39a3de86ae8e8f0253b. **Verified raw:** results/raw/tmr/2026-11-14_0130_TMR3_TWO_CROSSINGS014_RAW.json, blob 90ecc1ee5b6d404cf1cb487cc8c3bf68891da249.

**Source recovery:** Controlling directive and complete proof1 (28,714 chars), proof2 via authentic Git blob (1,051,196 chars), main.tex via authentic Git blob (2,522,180 chars), issue #3 through TMR-2/015, AGENTS, CODEX, skill, all five handoffs, original TMR-3/011-/013, TMR-2/015, TMR-5/012, primary Hennie 1965 catalog and FLMV 2005 official theorem. TRACKERS REVIEWED; NO MATERIAL CHANGE. Canonical main.tex left to TMR-5, no schedules changed, P versus NP OPEN.

**ONE NEXT TARGET:** TMR-5 or TMR-4 independently review the sharp crossing claim and test whether a cost-sound phase-invariant **normalized complete crossing code** can remove the cheaply propagated parity field without losing an exact source-splice theorem. Prove all-step charged transfer before any general lower-bound use.

END_OF_HANDOFF::TMR-3::2026-11-14_0130_PST

---

# TMR-3 CURRENT handoff | 2026-11-14 00:37 PST | BOUNDED-LOOKAHEAD KRAFT/HÖLDER013

**NEW TMR3-LA13 CANDIDATE pending TMR-5/TMR-2 independent mathematical review:** For independent uniform q_i-bit blocks X_i and conditionally prefix-free injective per-index codes c_i depending on X_1,...,X_min(K,i+r) only (entire past plus at most r future blocks), letting ell_i be the output length, for all b>0:
$$
\Pr\big[\sum_i\ell_i<\sum_i q_i-b\big]\le2^{-b/(r+1)}.
$$
For equal q, $\Pr[(1/K)\sum_i\ell_i<q-\log_2(1/\delta)]\le\delta^{K/(r+1)}$. Proof: conditional Kraft makes $Y_i=2^{q_i-\ell_i}$ have $E[Y_i|X_{<i}]\le1$. Partition indices modulo r+1 to get product supermartingale expectations <=1, then Hölder and Markov. **Sharpness:** consecutive independent groups of r+1 blocks each use the TMR-3/012 global-XOR conditional code within that group, producing exact tail $p^{K/(r+1)}$, $p=2^{-t}-2^{-q}$, and ratio to $\delta^{K/(r+1)}\to1$ for fixed K,r,t as q grows, $\delta=2^{-t}(1+2^{-q})$. This repairs overstrong "disjoint blocks imply concentration" by identifying the missing bounded-future-dependence premise. Physical two-way crossings generally depend on the entire future source; no SAT transfer is proved.

**ACTUAL executions:** Published exact hosted-V8 JavaScript: 14 exhaustive q,t,K,r group configurations, 218,752 global vectors, 19,554 conditional fibers, 294,488 generated codewords, plus 12 adaptive-code inequalities/49,152 source-vector comparisons and 5,329 fibers; zero failures. Separately authored and **natively executed CPython 3.13.5** reproduces all 14 group probabilities and all 12 adaptive inequalities, zero failures, local outbox only. The q=4,t=2,K=4 noncausal global-XOR adversary has p=0.1875, falsifying spurious r=0 bound 0.0049782395362854 while respecting r=3 bound 0.265625. Finite tests COMPUTATIONAL. No physical SAT TM or OS-native Node execution.

**Readback-verified GitHub main artifacts:** report `research/agents/tmr-3/2026-11-14_0037_TMR3_BOUNDED_LOOKAHEAD_KRAFT013.md` blob 0572103a2af05e58298994da88ebc3a7f3ac23e8; executed JS `experiments/tmr/tmr3_lookahead013.cjs` blob 13d594f37de94d8664a27b10cf913f2b422d933a; raw `results/raw/tmr/2026-11-14_0035_TMR3_LOOKAHEAD013_RAW.json` blob adbed1dcbffac34ce2dfa654c0ec9a1036ecdf18.

**Corpus:** Superseding directive first/rechecked SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1 authentic full 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2 authentic Git blob full 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c; main.tex authentic full 2,518,238 chars blob 0233cb0ca16a63a2a63a83af6a61ffe985632945. AGENTS, CODEX, pnp skill, current issue #3, all five latest handoffs and original TMR-3/008-/012, TMR-5/009, historical FLMV 2005 exact model checked. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No canonical main.tex edit or scheduled-task changes. P versus NP OPEN.

**ONE NEXT TARGET:** TMR-5/TMR-2 independent review of LA13 and exponent sharpness. Then test whether the *complete* physical two-way crossing-code records of arbitrary SAT machines ever satisfy a nontrivial bounded-future radius after fully charged rereads. If not, construct a physical paid-reread counterexample and retain all-exponent processing lower bound OPEN.

END_OF_HANDOFF::TMR3::2026-11-14_0037_PST

---

# TMR-3 CURRENT handoff | 2026-11-13 23:31 PST | DISJOINT CONDITIONAL KRAFT CORRELATION012

**NEW TMR3-DC12 CANDIDATE** pending TMR-5/TMR-2 mathematical review; finite codebook tests COMPUTATIONAL. Independently uniform disjoint q-bit blocks X_1,...,X_K DO NOT force aggregate crossing-code tail concentration if each cut's valid prefix-free codebook may condition on all other blocks. Split each block into t high bits and ell=q-t low bits. Let E={XOR high=0^t, XOR low !=0^ell}. At every cut i, conditional on X_-i, assign all 2^ell-1 satisfying Xi short ell-bit words except prefix 1^ell, and all other Xi long words 1^ell||Xi. Codebooks are prefix-free for EVERY conditioning, yet all K code lengths are identical on every global X. Their low-tail event has probability p=2^-t-2^-q versus delta=2^-t(1+2^-q), and p/delta->1 at fixed t, q->infinity for arbitrary K. Strengthens TMR-5/009's same-codebook example by using different disjoint independent conditioned free bits. It falsifies any K-fold probability amplification based solely on disjoint supports plus marginal conditioned Kraft. DOES NOT instantiate actual physical SAT crossing sequences or refute TMR-3/010.

**Executed exact published JS function in hosted V8:** 15 exhaustive (q,t,K) cases, 474,176 global tuples, 34,192 conditional fibers, 1,378,944 codewords, 1,344,752 adjacent prefix checks, 15 controls against false delta^K independence and 0 failures. The published exact function body is the executed V8 body; native Node was NOT executed. Source `experiments/tmr/tmr3_disjoint_conditional012.cjs`, raw `results/raw/tmr/2026-11-13_2329_TMR3_DISJOINT_CONDITIONAL012_RAW.json`, report `research/agents/tmr-3/2026-11-13_2331_TMR3_DISJOINT_CONDITIONAL_CORRELATION012.md`, all on main after GitHub readback. Original peers: TMR-3/010,/011, TMR-5/009, TMR-4/013, TMR-1/013, TMR-2/013. Primary FLMV 2005 random-access model/Theorem 1.1 inspected directly. No native clone/LaTeX build. TRACKERS REVIEWED; NO MATERIAL CHANGE; canonical main.tex untouched for TMR-5; no task change.

**ONE NEXT TARGET:** TMR-5 independently audit DC12, then derive actual full-crossing-sequence causal constraints, if any, beyond conditioned Kraft, without transferring easy-family source transport to unrestricted post-copy SAT processing. Same-machine unrestricted all-exponent SAT lower bound and P versus NP remain OPEN.

END_OF_HANDOFF::TMR3::2026-11-13_2331_PST

---

# TMR-3 CURRENT handoff | 2026-11-13 22:33 PST | FULL CROSSING AUDIT AND FALLBACK REPAIR011

**CS11 CANDIDATE/RESTRICTED pending independent TMR-5/TMR-1 review.** Self-contained symbolic audit of TMR-3/008's full physical crossing-list splice: if two accepted diagonals have identical full ordered crossing records, alternating left and right legal physical segments accepts a valid opposite-label hybrid, contradiction. All work-tape visited symbols, work-head positions, finite control, direction and count are essential. For locally moving fixed finite work tapes, prefix-free serialized complete crossing code has length at most d_A r_c(F)(S_A(F)+1). No one-pass restriction, assumed small workspace or per-cut different witness is used. The original strict 3-CNF source literal splice was independently reimplemented; the conditional TMR-3/010 aggregate Kraft route remains restricted and polynomial-strength. No all-exponent P != NP claim.

**Concrete narrow defect in TMR-3/008 Section 3:** literal dispatch "on ANY mismatch invoke exhaustive fallback" contradicts the advertised cheap bound on EVERY valid E(a,b): valid unequal bank sources are UNSAT and trigger 2^(5n) exhaustive candidate assignments. Repaired classifier: finish structure authentication, retain one-bit equal flag, return equal for any authenticated template, and use exhaustive general fallback ONLY on structurally nonmember sources. Original published source-level recognizer already classifies authenticated unequal banks correctly; this is a prose dispatch correction, not a mathematical lower-bound falsification. Physical bit parser upper exponent remains to be proved independently.

**Executed independent checks (native Python plus separate hosted V8 exact published JS):** 5,460 local-head/local-work-tape equality decisions (126 SAT, 5,334 UNSAT); 27 full crossing-codebooks, 492 codewords, 14,310 prefix-free pairs, 14,310 false projected control/head-only collisions, 14,310 true rejected mixed hybrids; independently reconstructed exact source splice: 27,612 physical cut comparisons, 21,826 opposite-label legal hybrids across 1,533 boundaries; n=1,2,3 brute-force valid UNSAT fallback required 32/1024/32768 candidate trials. ZERO assertions failed. Finite evidence COMPUTATIONAL, no arbitrary SAT TM execution. Published exact JavaScript, not a wrapper; separate native Python implementation is local-only.

**Readback verified main publications:**
- Report research/agents/tmr-3/2026-11-13_2233_TMR3_CROSSING_SPLICE_AUDIT011.md (Git blob f25bbb0a6afbe665c0e3ae63e13017c49d0473c9).
- Executable experiments/tmr/tmr3_crossing_replay011.cjs (Git blob f286ae9fc30679c654109220a5fa38d37d8873c0).
- Raw results results/raw/tmr/2026-11-13_2233_TMR3_CROSSING_REPLAY011_RAW.json (Git blob 935f5a81321157f87bc3de65b8c770b4f09d4abb).

**Preflight:** authoritative TMR replacement directive, both full proof trackers (proof2 authentic Git blob 1,051,196 characters), full authentic root main.tex (2,511,782 characters), issue #3, AGENTS/CODEX/research skill, five peer handoffs and original TMR-3/002,/008,/009,/010, TMR-5/009 and TMR-1/012 reports were read. Primary Hennie 1965, FLMV 2005 and Borodin-Cook 1982 model scopes independently checked. TRACKERS REVIEWED; NO MATERIAL CHANGE. Canonical main.tex left to TMR-5; no schedule changed. Local project preflight/LaTeX compile not executed because no network clone.

**ONE NEXT TARGET:** TMR-5 audit every crossing state/coding step and authenticated UNSAT dispatch, then challenge any post-acquisition cost invariant on the source-copying simulator with arbitrary polynomial workspace. The unrestricted all-exponent SAT lower bound and P versus NP remain OPEN.

END_OF_HANDOFF::TMR3::2026-11-13_2233_PST

---

# TMR-3 CURRENT handoff | 2026-11-13 21:20 PST | AGGREGATE-KRAFT-TAIL010

**Substantive result:** TMR3-EM10 establishes the pure prefix-free aggregate exponential-moment inequality **PROVED/EXACT**. Its same-machine 3-CNF batched crossing implication is **CONDITIONAL/RESTRICTED** on original TMR-3/008's CANDIDATE full-configuration crossing-code/injective-splice lemma. For one fixed correct total deterministic multitape A with ONE locally moving read-only input head, the original E_{n,m}(a,a) SAT diagonal distribution satisfies, with q=floor(m/2), K=floor(n/m)(qg-1), L=13n+2+2ng, g=12(w+1), n>=m>=16:

$$
\Pr_a\left[T_A(F_a)(S_A(F_a)+1)\ge \frac K{d_A}\bigl(q-\log_2(1/\delta)\bigr)\right]\ge1-\delta.
$$

In particular, **same original lower product threshold** $Lm/(512d_A)$ has success probability at least $1-2^{-q/2}$, improving /009's $1-\min(1,K2^{-q/2})$. New $1-1/L$ sufficient threshold is $m>=4log_2(L)+2$ versus /009's $8log_2(L)+8$. This improvement is a Jensen + Kraft + Markov aggregate argument; it does not assert all K cuts are individually long.

**COMPUTATIONAL, verified on main:** 504 prefix-code cases; 5,292 full codebooks; 36,576 exhaustive assignments; 3,024 aggregate tail inequalities; zero failures. Deliberately non-prefix-free injective control produces probability one for a claimed 1/2 tail and Kraft sum 4.0625, demonstrating a load-bearing hypothesis. Published-exact hosted V8 function executed, not native Node or a physical TM. Source/raw/report each read back exactly after GitHub publication:
- `research/agents/tmr-3/2026-11-13_2120_TMR3_AGGREGATE_KRAFT_TAIL010.md`, blob e7d8a5c5c7e0e99415129dd7d8954d0c6ac7e3c6
- `experiments/tmr/tmr3_aggregate_kraft010.cjs`, blob 42fdc6861204b5a730492e2719f6825d3481d7e7
- `results/raw/tmr/2026-11-13_2120_TMR3_AGGREGATE_KRAFT010_RAW.json`, blob a3c7928ee080eb6ec5a68cd28363e1720b58578a

**Controls/gap:** m=1 interleaving, a second independent source head, indexed access, cache or copy with polynomial writable space, Gaussian elimination on XOR, Horn, 2-SAT, bounded treewidth, products/sharing, renaming, padding, auxiliaries, compact encodings and recomputation all defeat an unrestricted computational-process inference. No general P vs NP or all-exponent result; no assumption of polynomial upper bounds. LSPV-5/167's earlier crossing expectation and LSPV-1/197 union-based distribution were read as true predecessors, not assigned priority. Primary Hennie 1965, FLMV JACM 2005, Borodin-Cook 1982 publisher records checked. The new contribution is precisely the K-free tail for **aggregate** code lengths on one common execution.

**State/readback:** replacement directive 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1.txt complete 28,714 characters SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2.txt complete authentic Git blob 1,051,196 characters SHA 930c5eeddafce656717f28055a7a9a755f44737c; main.tex complete authentic Git blob 2,507,300 characters SHA c0d657568af18ed0a2d17843b8ef0e6c11ac6327. AGENTS/CODEX/skill, latest issue #3 and five newest TMR handoffs reviewed. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex left to TMR-5 synthesis; no schedules or tasks touched. New 3-SAT implication remains conditional until TMR-5/TMR-1 independently reviews parent crossing lemma. P versus NP OPEN.

**Next one target:** TMR-5 independently reconstructs and attempts to falsify complete physical crossing-code prefix-free serialization, cut/splice injectivity and resource charges; then reviews EM10's aggregate tail. General representation-independent processing bottleneck remains OPEN.

END_OF_HANDOFF::TMR-3::2026-11-13_2120_PST

---

# TMR-3 CURRENT handoff | 2026-11-13 20:30 PST | TYPICAL-DIAGONAL-CROSSING009

**New scoped result:** CONDITIONAL/RESTRICTED distributional strengthening of TMR-3/008 BATCH8-LB, whose full physical crossing-code lemma is still CANDIDATE awaiting independent TMR-5/TMR-1 review. On one fixed correct total one-sequential-input-head multitape decider A, the same accepted diagonal F_a=E_{n,m}(a,a) obeys, for n>=m>=16 with uniform a, q=floor(m/2), g=12(ceil(log2(5n))+1), L=13n+2+2ng, K=floor(n/m)(q*g-1), and TMR3/008 constant d_A,

$$
\Pr_a[T_A(F_a)(S_A(F_a)+1)\ge Lm/(512d_A)]\ge1-\min(1,K2^{-q/2}).
$$

For m>=8log2(L)+8, this probability is >=1-1/L. The original proof gave merely EXISTS one difficult SAT diagonal. New argument: condition on the q independent first-bank variables for EACH physical cut; injective prefix-free full-configuration crossing codes give Pr[code length<q/2]<=2^{-q/2}; union bound over K<=L distinct cuts yields a single accepted realization with all crossings large. Count actual crossings once and charge peak writable space from the SAME run. Exact source family and all prior geometric restrictions are preserved. No arbitrary-workspace/all-exponent or indexed/multi-input-head bridge.

**Actual tests and publication:** independently written native Node v22.16.0 outbox and a separate published hosted-V8-compatible code passed 195 canonical source checks and 29,488 exact hybrid splices, of which 27,416 are valid different-prefix UNSAT and 2,072 equal-prefix SAT, with 0 final assertions and max L=77,058. This is finite source-level COMPUTATIONAL evidence, not TM crossing-record execution. One early harness-only m=1 cut-count assertion was corrected and fully rerun. Original report's upper-bound prose "any mismatch -> exhaustive fallback" requires grammar failure vs authenticated semantic inequality distinction; its original source code already distinguishes \`member:false\` from \`member:true,sat:false\`, so the upper bound is not refuted.

**GitHub MAIN verified:** report research/agents/tmr-3/2026-11-13_2030_TMR3_TYPICAL_DIAGONAL_CROSSING009.md, blob 57eb79bb32126035af94eb23ac9bebbd0592ef12; executable experiments/tmr/tmr3_typical_diagonal009.cjs, blob 5296e5beeeb59a1c3a78e163a6cb637eb330f6d0; raw results results/raw/tmr/2026-11-13_2030_TMR3_TYPICAL_DIAGONAL009_RAW.json, blob 0eb9438f916e16151fa8d4a5c3a0bab7307c860d. A separate native source/JSON remains local outbox and was not falsely claimed published.

**Corpus and status:** replacement directive read first and rechecked; proof1.txt 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2.txt recovered full authentic Git blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c despite blank file contents response; main.tex full recovered Git blob 2,504,241 chars SHA 103435a5c6ff2b02e2b975e7c00d37476d66b064; AGENTS.md/CODEX.md/skill, issue #3, current five TMR handoffs, TMR-3/002,/007,/008 originals, LSPV-5/167 original, TMR-2/010 and TMR-5/007, primary publisher FLMV/Borodin-Cook and Hennie records consulted. TRACKERS REVIEWED; NO MATERIAL CHANGE. Root main.tex left unchanged for TMR-5 synthesis. No tasks or schedules modified. P versus NP OPEN.

**ONE NEXT TARGET:** TMR-5 should independently prove or disprove the full crossing-code binary-length bound and all-cut splicing; any computational necessity past input transport must survive m=1 ordering, multiple input heads, INDEX, cached whole batches, Gaussian elimination and arbitrary polynomial work space.

END_OF_HANDOFF::TMR-3::2026-11-13_2030_PST

---

# TMR-3 CURRENT handoff | 2026-11-13 19:35 PST | BATCH-LOCALITY-TRADEOFF008

**NEW BATCH8-LB CANDIDATE pending TMR-5/TMR-1 review; exact source-level finite results COMPUTATIONAL. Unrestricted SAT all-exponent lower bound and P versus NP OPEN.**

**Quantitative new theorem candidate:** For the original proper 3-CNF equality source, batch m consecutive first-bank forcing blocks beside their m matched second-bank blocks. This is an EXACT whole-clause permutation with identical L=13n+2+24n(w+1) and SAT iff a=b. For ANY one fixed total correct deterministic machine A with ONE physically local read-only input head and finite ordinary work tapes, the full-configuration crossing-code and same-realization average argument gives (pending independent audit): for each n sufficiently large and each 1<=m<=n, some SAT diagonal F has **T_A(F)(S_A(F)+1)>=c_A Lm**. For each cut in the second half of each full first bank, floor(m/2) first forcing blocks are fully left and their matching second blocks wholly right; a valid UNSAT splice forces injective prefix-free crossing transcripts. Average *T(S+1)* over a single uniform diagonal distribution before taking any maximum. Small m handled by physical reach of the final source block. All real input crossings and all visited work cells charged. Not a random-access/dual-head theorem.

**Matching upper:** for fixed rational 0<=beta<=alpha<=1, batch m(n)=2^floor(alpha floor(log2 n)), cache r(n)=2^floor(beta floor(log2 n)). One fixed total all-input correct fallback machine authenticates every literal in local batch rescans, uses **T=O(L ceil(m/r))**, **S=O(r+log L)** on this family, and pays all reads, rewinds, scratch tapes, comparisons, counters and output. The lower/upper product matches for beta>0, up to a logarithmic factor for beta=0. For m=Theta(n^alpha), the restricted product bound is Omega(L^{1+alpha}/(log L)^alpha) and only excludes simultaneous exponent pairs k+s<1+alpha. S<=O(T) gives no stronger time bound than compulsory input traversal. Alternative source order, extra input heads, INDEX, algebraic summaries and unrestricted polynomial workspace remain all-program transfer blockers.

**ACTUALLY EXECUTED and readback-verified:** native Node v22.16.0 and separate hosted-V8 execution of exact published code, 2,468 canonical parse-and-answer cases (223 SAT/2,245 UNSAT), 1,232 exact original CNF multiset/permutation checks, 1,236 undersized-cache cases, 4,928 rejected structural negatives, 40 original-CNF exhaustive checks, 677,552,068 modeled adjacent source movements with 331,481,280 rewind moves, largest L=77,058, zero failures. These are NOT physical-TM transition traces; the exponential off-family fallback was not executed.

**Verified paths:**
- research/agents/tmr-3/2026-11-13_1935_TMR3_BATCH_LOCALITY_TRADEOFF008.md
- experiments/tmr/tmr3_batch_crossing008.cjs
- results/raw/tmr/2026-11-13_1935_TMR3_BATCH_CROSSING008_RAW.json

**Preflight:** Superseding directive first, rechecked SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; full proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; full proof2 authentic Git blob SHA 930c5eeddafce656717f28055a7a755f44737c; full main.tex authentic Git blob SHA 62c0c400a5eddfbdbdfa06fbabcf7bcee8b753be, all protocols, issue #3, five latest TMR handoffs, original TMR-3/002,/006,/007 and FLMV original model. TRACKERS REVIEWED; NO MATERIAL CHANGE. No main.tex or schedule/task mutation.

**Next:** TMR-5 audit variable-space prefix-free transcript coding, cut-and-paste legality, unconditional same-run expectation and matching fully charged uniform upper. Then seek a post-acquisition bottleneck immune to batch m=1, extra source heads, INDEX and Gaussian elimination. ALL unrestricted implications OPEN.

END_OF_HANDOFF::TMR3::2026-11-13_1935_PST

---

# TMR-3 CURRENT handoff | 2026-11-13 18:28 PST | CLAUSE-ORDER-LOCALITY007

**New CANDIDATE CO7, pending TMR-5/TMR-1 review. Finite independent original V8 source checks COMPUTATIONAL. General all-exponent SAT lower bound and P versus NP OPEN.**

**New exact same-formula representation counterexample:** For the original grouped-bank $E_n(a,b)$ strict proper-3CNF, binary width $w_n=\max(1,\lceil\log_2(5n)\rceil)$ and length $L_n=13n+2+24n(1+w_n)$, simply interleave each original four-clause first-bank forcing block with its matching original four-clause second-bank block. This produces $I_n(a,b)$ with EXACT original clause multiset, variable IDs, unary header, bit length and SAT iff $a=b$, only a clause-block order permutation. ONE fixed total correct deterministic all-input SAT machine with ONE physical locally moving read-only head, NO INDEX or second head, authenticates all bits and endmarker in a single sweep, compares immediately adjacent sign pairs, and uses a paid exhaustive fallback off-family. Symbolic physical resource upper on ALL interleaved family members: $T_D=O(L_n)$ and $S_D=O(\log L_n)$ on the SAME machine/input, so $T_D(S_D+1)=O(L_n\log L_n)=o(L_n n)$. This falsifies a clause-order-invariant/semantic transfer of grouped TMR-3/002's one-head crossing product, **NOT** its original ordered-source restricted claim. Machine-transition-table and TMR-5 audit pending.

**Executed and readback verified:** Standalone authored hosted-V8 source code experiments/tmr/tmr3_interleaved_clause_order007.cjs SHA befcb48e1e5383d88a95bf1454486f07b5579c90; raw results results/raw/tmr/2026-11-13_1828_TMR3_INTERLEAVED_ORDER007_RAW.json SHA 27919b256afa7cc7163c42957caa08cdd9e45a00; report research/agents/tmr-3/2026-11-13_1828_TMR3_CLAUSE_ORDER_LOCALITY_ESCAPE007.md SHA b21b48030c912d24f191849338fa3d1d148d8546. 1,420 valid sources (118 SAT/1,302 UNSAT), 1,420 byte-exact permutations, 7,100 structural mutant rejections, 40 small whole-CNF brute-force checks, 3,454,956 modeled local source moves, maximum L=166,402, 0 failures. Not instruction-level physical TM, not native Node or fallback execution; asymptotic upper is symbolic.

**Read:** Superseding directive first and rechecked SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; full proof1 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, full proof2 Git blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c, full main.tex Git blob 2,497,977 chars SHA 4e0dc7a81c3757289e87661b6df29e458cd03daa, root AGENTS/CODEX/skill, issue #3 through TMR-2/007, all five handoffs, original TMR-3/002,/006 and TMR-2/007, TMR-4/006, FLMV original author PDF Section 2.1 screenshot. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** main.tex left to TMR-5 synthesis. No schedules or agents modified.

**ONE NEXT TARGET:** TMR-5 independently inspect physically charged one-head interleaved parser, same-formula clause order proof and fallback. Construct or refute unavoidable post-acquisition computation charges not sensitive to input order, head multiplicity, INDEX access, Gaussian elimination or sharing. All unrestricted implications OPEN.

END_OF_HANDOFF::TMR3::2026-11-13_1828_PST

---

# TMR-3 CURRENT handoff | 2026-11-13 17:23 PST | TWO-LOCAL-HEAD-BOUNDARY006

**New TH6 mathematical construction CANDIDATE pending independent TMR-5 review; actual native Node finite source audit COMPUTATIONAL.** Every unrestricted all-exponent SAT lower-bound arrow OPEN; P versus NP OPEN. No schedules modified.

**Exact scope and substantive falsifier:** On the original strict proper 3-CNF equality family E_n(a,b), n>=1, width w=max(1,ceil(log2(5n))), h=13n+2, g=12(w+1), L=h+2ng, ONE fixed correct total deterministic 3-SAT machine with TWO independently moving **local, read-only input heads**, NO INDEX, and sequential writable work tapes achieves T=O(L) and S=O(log L) on every family member. Head 1 parses the header and first bank; head 2 is locally advanced to second bank start h+ng, then both heads validate their respective original banks synchronously, compare n sign pairs and check the right endmarker. All source bits authenticated. Total individual input movements 2h+3ng<=2L; amortized binary downcounter and O(w) verifier per constant-number-of-clauses give O(L) fully charged symbolic time, O(log L) all-live writable space. Charged exhaustive fallback off-family. This invalidates head-count-independent extrapolation of TMR-3/002 T(S+1)=Omega(Ln), but does NOT contradict its explicitly ONE-head assumption.

**Independent TMR-1/005 audit:** Read original report and code, verified original FLMV 2005 Section 2.1 author PDF including INDEX erasure. The 2n-erasing-jump plus native local-source scan upper O(L) and S=O(log L) is mathematically consistent at that indexed model, pending TMR-5 physical audit. TMR-5/004's O(L log L) erasing-index method is a valid nonoptimal upper, not a lower bound.

**Actual independently executed native Node v22.16.0:** 1,428 original valid E cases (126 SAT, 1,302 UNSAT), 9,996 mutation controls rejected, 20 original-clause brute-force controls, 9,619,896 emulated adjacent head movements, 6,315,408 reads, 22,692 pair comparisons, largest L=357,378, zero failures. No native physical multitape TM, general fallback, full repository preflight or LaTeX compile. Test host strings and Number arithmetic are COMPUTATIONAL only.

**Readback-verified main-branch artifacts:**
- Report research/agents/tmr-3/2026-11-13_1723_TMR3_TWOHEAD_SEQUENTIAL_PORT_BOUNDARY006.md, SHA b79c85dd8a407e916aa68cefb116997c85f0d171.
- Exact executed Node source experiments/tmr/tmr3_twohead_sequential_006.cjs, SHA 1e6c2f6d0b54e5fcf3e585d8324c7f3ee98e3d07.
- Immutable JSON results/raw/tmr/2026-11-13_1723_TMR3_TWOHEAD_SEQUENTIAL006_RAW.json, SHA 18f122f5a754a701a199c6a351d6808e96632bcf.

**Source preflight:** Superseding directive first and rechecked SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4, proof1 full SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2 full authentic Git blob SHA 930c5eeddafce656717f28055a7a9a755f44737c, main.tex full authentic blob SHA 873daeec6e11d4a7448f3b0547c9ed1ccfebd805, issue #3 1957 comments through TMR-2/006, root operating files, all five current peer handoffs, original TMR-3/002-003, TMR-1/005 report+code+raw, FLMV original Section 2.1. TRACKERS REVIEWED; NO MATERIAL CHANGE. Root main.tex left to TMR-5 ownership.

**TMR-5 audit target:** Verify exact pair-bank read-head configuration, physical logspace downcounter and bit verifier, no hidden source duplication, whole-string endmarker and malformed fallback, then acknowledge head-count scope firewall. TMR-1 should declare head multiplicity; TMR-4 charge each head position. Next substantive TMR-3 target: a whole-execution processing cost insensitive to source-head multiplicity, input indexing, compact GF(2), sharing, recomputation and arbitrary polynomial workspace.

END_OF_HANDOFF::TMR3::2026-11-13_1723_PST

---

# TMR-3 CURRENT handoff | 2026-11-13 16:20 PST | DUAL-INDEX-LINEAR-ESCAPE005

**Scientific status:** DI5-P / DI5-E symbolic upper constructions CANDIDATE pending TMR-5 review. Source tests COMPUTATIONAL (1,441 valid E pairs, 8,646 mutations, 17,292 assertions, zero failures; independent original-CNF brute force n<=2 passes 20/20). TMR-3/002 sequential crossing product remains previously reviewed PROVED/RESTRICTED. P versus NP OPEN.

**New scoped result:** On the EXACT existing proper-3CNF E_n(a,b) family with L_n=13n+2+24n(1+ceil(log2(5n)))=Theta(n log n), ONE fixed total correct all-length SAT machine with TWO paid persistent INDEX source registers has T=O(L_n), S=O(log L_n) on every family member, by fully authenticating all original source bits and using a second indexed port to compare each second-bank sign against the first-bank sign at offset h+i*g. Full paid exhaustive fallback off-family. Binary sequential address increments amortize O(1); n stride-g updates cost O(n log L)=O(L). If the INDEX tape is ERASED on query as in FLMV 2005, paid shadow reconstruction yields the distinct T=O(L log L), S=O(log L) variant.

**Exact transfer gap:** Both indexed T(S+1) upper products, O(L log L) and O(L log^2 L), are o(L n); hence TMR-3/002 sequential-source T(S+1)=Omega(L n) CANNOT transfer unchanged to indexed input. TMR-1/004's separately charged indexed-to-sequential simulator remains permissible. This is an EASY recognizable family and proves no unrestricted SAT lower bound or general polynomial solver.

**Published/readback verified:** research/agents/tmr-3/2026-11-13_1620_TMR3_DUAL_INDEX_LINEAR_ESCAPE005.md (blob a78b659760cde0bf346d9df6c7f7ada2f27d6bcf); experiments/tmr/tmr3_dual_index_linear005.cjs (blob 9b43e8ddad42ac9ebce54fc0b2397776c199723a); experiments/tmr/tmr3_dual_index_semantic_independent005.py (published); results/raw/tmr/2026-11-13_1620_TMR3_DUAL_INDEX_LINEAR005_RAW.json (blob 3ca57317b6463b6d8316669f689af20aac49a126). Full SHA+contents recovery of both proof trackers and canonical main.tex performed before work. TRACKERS REVIEWED; NO MATERIAL CHANGE; no root main.tex edit. No tasks or schedules changed.

**Primary model authority:** Fortnow et al., JACM 52(6), 2005, Section 2.1 author PDF https://lance.fortnow.com/papers/files/tst.pdf explicitly erases the INDEX tape after a jump; Hennie 1965 crossing work uses physical tape-access premises. Exact sources, model and test caveats in full report.

**Peer requests / NEXT OPEN:** TMR-1 audit two-port model, erasure and shadow address charges; TMR-2 audit information distinction/retention; TMR-4 audit all-transition charges; TMR-5 independently replay actual published code and inspect asymptotic address-head amortization. Seek a universal whole-execution cost stronger than a physically sequential transport requirement, surviving indexing, compact algebra, rereads and polynomial workspace.

---

## Preserved previous handoffs

# TMR-3 latest handoff | 2026-11-13 15:27 PST | BATCHED-SEQUENTIAL-PARETO-FRONTIER003

**Status:** NEW TMR-3, no schedule/task mutations. Upper construction CANDIDATE pending TMR-5 independent review; previous TMR-3/002 full crossing lower bound PROVED/RESTRICTED after independent TMR-5 review; finite regression COMPUTATIONAL. P versus NP OPEN.

**New scoped result:** For exact, recognizable strict proper-3CNF equality inputs $E_n(a,b)$, $L_n=13n+2+24n(1+\max(1,\lceil\log_2(5n)\rceil))$, and any fixed efficiently computable chunk function $\lceil c\log n\rceil\le\sigma(n)\le n$, ONE fixed total all-input-correct sequential-input-head machine authenticates the source, checks $n$ equality sign pairs in batches of $\sigma(n)$, and falls back to paid exhaustive SAT on nonmembers. Same family-input trace $T=O(L_n\lceil n/\sigma(n)\rceil)$, $S=O(\sigma(n))$ (including work buffers, counters, parser and input rewind costs). TMR-3/002's independently reviewed same-input lower product $T(S+1)=\Omega_A(L_n n)$ implies worst-case family time $\Omega_A(L_n n/\sigma(n))$ for ANY fixed correct machine satisfying a family-wide $O(\sigma(n))$ workspace budget. Thus the restricted family's entire logarithmic-to-linear work-space frontier is matched up to constants. This extends the known $\sigma=n$ matching upper, not the historical Hennie/Cobham/Santhanam crossing theory. It cannot transfer to indexed input or prove P != NP.

**Verified report:** research/agents/tmr-3/2026-11-13_1527_TMR3_BATCH_SEQUENTIAL_PARETO_FRONTIER003.md, blob 3769680d76b767b924e16aeded5dc992d66a1e7e.
**Verified independent V8-executable source:** experiments/tmr/tmr3_batch_frontier003.cjs, blob 25c36eb3a9daf2d1197b4e3419c863390692afff.
**Verified immutable raw:** results/raw/tmr/2026-11-13_1527_TMR3_BATCH_FRONTIER003_RAW.json, blob 672425942fd73eefef8c4dc1e4bce9e25212de73.

**ACTUALLY EXECUTED:** 1,364 exhaustive n<=5 original source pairs and 120 seeded n=6,8,16,32,64,128 pairs, 6,008 batch executions, 40,428 assertions, 4,452 malformed controls and 1,484 local sign-corruption controls, zero failures. V8 emulated 210,294,700 forward source-bit visits and 198,630,820 paid reverse moves. This was not a physical multitape TM emulator or OS Node CLI. Full preflight, report validator and LaTeX compiler unexecuted. Code and raw were published/read back exactly.

**Primary literature checked:** Hennie 1965 original off-line single-tape crossing sequences, distinct machine model. Fortnow-Lipton-van Melkebeek-Viglas JACM 2005 original Theorem 1.1, random-access SAT exclusion only for simultaneous $T=n^c$, $S=n^d$ with $c<\varphi$, $d>0$ appropriately chosen, NOT all polynomial workspace. Prior original project LSPV-5/167 and Claude ONETAPE-0001 read.

**Root scope:** Full proof1.txt and genuine 1,051,196-char proof2.txt Git blob inspected; full root main.tex 2,487,713 chars recovered by Git blob. TRACKERS REVIEWED; NO MATERIAL CHANGE. Existing TMR-3 main.tex ownership region left unchanged until candidate peer review and synthesis. Superseding directive rechecked; no scheduled tasks/agents modified.

**Peer requests:** TMR-5 independently review concrete streaming grammar checker $O(L_n)$ transitions with fixed tapes and work-head movements, and the use of TW2 under an on-family workspace cap. TMR-1 audit fixed-program quantifiers and comparison of all simultaneous time-space pairs; TMR-2 test cheap XOR/product alternate summaries; TMR-4 model every step and terminal label in an abstract cost transition graph.

**ONE next target:** identify a true all-algorithm, representation-independent global-consistency charge stronger than physical input transport, or falsify a proposed charge with compact algebra, caching, shared computation or indexed reading. The universal superpolynomial arrow remains OPEN.

END_OF_HANDOFF::TMR3::2026-11-13_1527_PST

---

# TMR-3 handoff | 2026-11-13 13:35 PST

**Current owner:** NEW TMR-3 Time-Space Tradeoffs, 2026-11-13 five-role replacement directive, j15marti/pnp main. **P versus NP OPEN.** No schedule changes or legacy role reuse.

**Substantive latest report:** research/agents/tmr-3/2026-11-13_1334_TMR3_SAME_INPUT_MULTIPASS_TRADEOFF001.md (readback verification pending on this handoff's creation). **CANDIDATE** complete symbolic proof pending TMR-5 independent review; **COMPUTATIONAL** exhaustive finite controls.

**Exactly scoped new theorem:** Let E_n(a,b) be the complete TMR-2 binary proper-3CNF equality family, L(n)=13n+2+24n(1+max(1,ceil(log2(5n)))). Restrict a fixed correct finite machine to *complete sequential one-way source sweeps* with no input observations during paid resets, fixed finite work tapes and full writable-cell/head counting. For some one *satisfiable* E_n(a_n,a_n), for every n and every fixed correct machine M,

$$
p_M(E_n(a_n,a_n))(S_M(E_n(a_n,a_n))+1)\ge c_M n,
$$

and on the *same input* $T_M(S_M+1)\ge c_M L(n)n=\Omega_M(L(n)^2/\log L(n))$. A complete variable-length communication transcript for each diagonal is injective: collisions splice into mixed UNSAT. The 2^n binary strings force one serialized transcript of >=n bits, each bounded by O(p(S+1)) including all work-head positions/control. This is a restricted *same-input* tradeoff, distinct from merely multiplying different worst-case resource witnesses.

**Model transfer firewall:** An indexed-input implementation checks the rigid equality family in O(L polylog L) time and O(log L) work/index cells, bypassing complete source sweeps. Standard arbitrary computations can also reread, copy or reencode the source without the prescribed p-phase structure. Prior LSPV-5/167 crossing sequences are acknowledged; no unrestricted theorem or novelty in equality/communication complexity claimed. Known FLMV near-linear SAT exclusions do not remove an arbitrary polynomial exponent. No P != NP claim.

**Executable and immutable raw:** experiments/tmr/tmr3_multipass_equal3_tradeoff.cjs and results/raw/tmr/2026-11-13_1328_TMR3_MULTIPASS_EQUAL3_RAW.json. Original GitHub readback of code reran in V8: all 1,364 E(a,b), 6,372 batch checks, 258 positive transcript checks, 516 four-sign-bit flips, 20 n<=2 full SAT brute checks, 37,263 assertions PASS. Virtual streaming emulator, not physical native TM instructions. Node CLI/preflight/checker not run.

**Peer tasks:** TMR-1 audit quantifiers and strict-class transfer. TMR-2 investigate an information-cost beyond input reads still necessary with arbitrary replay and compact summaries. TMR-4 instantiate a simulation that includes every two-way head move, work-copy and state conversion. **TMR-5 independently falsify** same-input variable-length transcript injection/cost, completed-sweep assumption, and duplication against LSPV-5/167.

**Canonical records:** Root proof1/proof2 fully read (the latter recovered from Git blob), root main.tex fully read by blob; TMR-3 has no authorized synthesis region yet. TRACKERS REVIEWED; NO MATERIAL CHANGE. No root manuscript or shared task edits.

**Next target:** test a two-way input-crossing protocol against actual copying, caching, compact algebra and alternative representations, retaining cost direction and same-input quantifiers; publish a concrete failing counterexample if unrestricted transfer is false.

END_OF_HANDOFF::TMR-3::2026-11-13_1335_PST


---

# TMR-3 latest handoff | 2026-11-13 14:34 PST | TWO-WAY-CROSSING-TRADEOFF002

**Superseding directive:** research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md. New TMR-3 under five-TMR replacement, no historical role/task revival. **P versus NP remains OPEN.**

**New CANDIDATE mathematical report, published/readback SHA f7664532b1ee57496d059aa2d793a55714de3907:** research/agents/tmr-3/2026-11-13_1434_TMR3_TWOWAY_CROSSING_TRADEOFF002.md.

**Verified executable, SHA 6ca3cd1385b7b29ee5dc4df9d156c18f9f77678b:** experiments/tmr/tmr3_twoway_crossing_splice002.cjs. **Verified immutable raw, SHA 873ebb331fd1e173e5170508db9a623439c2a78c:** results/raw/tmr/2026-11-13_1434_TMR3_TWOWAY_CROSSING_RAW.json.

**Exact stronger model-scope result pending TMR-5 review:** For EACH one fixed correct total deterministic 3-SAT machine A with ONE freely reversing sequential two-way read-only input head and any fixed finite number of charged work tapes, for all sufficiently large n there is ONE SAT diagonal E_n(a_n,a_n) from the original TMR-2 strict-proper-3CNF equality family for which SAME-TRACE time and space obey

$$
T_A(E_n(a_n,a_n))(S_A(E_n(a_n,a_n))+1)\ge c_A L(n)n
=\Omega_A(L(n)^2/\log L(n)).
$$

**Method:** No complete source sweeps required. At Theta(L) physically distinct cuts *inside the fixed-suffix first-half gadgets*, exact diagonal source splicing supplies 2^j different prefix choices with a fixed suffix and mixed UNSAT hybrid. Full controller/work-symbol/head crossing transcripts are injective conditional on suffix, self-delimiting codes have length <=D_A*q_c(S+1)+O_A(log(S+2)), and a short-code union bound selects a single diagonal simultaneously expensive on every cut. If S>=n on any diagonal, direct travel T>=L/2 already gives product. If S<n on all, sum crossing costs over all cuts. No different-input time/space borrowing, and physical two-way reversals, copying and recomputation are admitted.

**Tightness and barrier:** TMR-2/002 ONE fixed all-input correct machine has T=Theta(L), S=Theta(n) on this exact easy family, so product is O(Ln). This matches and caps the bound. Fully paid indexed-input random access can recognize/compare the same rigid family in O(L log^2 L) time, O(log L) space, so the theorem has NO random-access transfer. Occupancy S<=b(T+1) gives only T=Omega(L/sqrt(log L)), weaker than actual T>=L/2. This is a **sequential-head physical transport theorem**, not unavoidable superpolynomial global-consistency work.

**Scientific prior art:** Classical Hennie crossing sequences; Santhanam 2001; project LSPV-5/167 already proves crossing averages on a separate exact22 gap family; Claude ONETAPE-0001 documents SAT/off-line quadratic product bounds. Increment is removing TMR-3/001 complete-sweep restriction for the *original TMR-2 exact encoding*, not discovery of the general method.

**COMPUTATIONAL executed V8 source audit:** all 1,364 ordered n<=5 original signed E(a,b) formulas, 16 unit-gadget truth-table assertions, 71,520 exact syntactic source splices (63,888 unequal-prefix UNSAT hybrids), 408 cut positions; 0 failed. Tested finite source locality, NOT full physical machine simulation or asymptotic coding. OS Node, formal TM executor, LaTeX compilation and repository preflight unexecuted.

**Peer requests:** TMR-5 independently review conditional-suffix cut syntax, complete crossing config, self-delimiting variable-S code, same-input all-cut union bound, and T>=L/2; TMR-1 inspect exact one-head vs indexed model transfer and the fixed polynomial barrier; TMR-4 construct a cost-sound actual-step crossing abstraction without assuming any sweep phase; TMR-2 test proposed compulsory global-consistency operations against the one-sweep easy upper.

**Root state:** full proof1/proof2 reviewed, large proof2 and main.tex recovered by Git blob rather than reconstructed. TRACKERS REVIEWED; NO MATERIAL CHANGE. New TMR-3 main.tex region is authorized, but the status remains CANDIDATE pending TMR-5 and manuscript synthesis was left unchanged intentionally. No task or schedule changes.

**One next target:** find or falsify a compulsory operation cost that survives indexed input access, streaming/caching interleaving, compact algebra and unbounded polynomial workspace, not just the sequential geometry. P versus NP OPEN.

END_OF_HANDOFF::TMR-3::2026-11-13_1434_PST
