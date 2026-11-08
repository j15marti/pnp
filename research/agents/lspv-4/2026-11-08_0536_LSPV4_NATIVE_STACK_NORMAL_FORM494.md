# LSPV-4/494: Native-FLMV streaming-call stack realization and polynomial-branch firewall

**2026-11-08 05:36 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Node ledger:** material scoped evidence for **[P2-A4]** and **[P2-A5]**; prior **[P2-A2]** answer-only no-go (LSPV-2/478) retained. Companion **[P2-A1]** is the published FLMV theorem. **[P2-A2]**, **[P2-A5]** as universal constructor, **[P1-01]**, **[P1-03]**, **[P1-04]**, and Route B **[P2-D1]**, **[P2-C3]**, **[P2-B1]**, **[P2-B2]** remain OPEN. This result does NOT strengthen historical R_mix341 or modify its rules/weights.

## IDEA -> SEARCH -> ITERATE

**Hypothesis (resource auditor):** the unresolved clause (4) in LSPV-2/478, requiring an *already* fully charged native recursive stack, can be proved for an explicitly specified **streaming-call normal form**, without assuming arbitrary black-box simulator efficiency. The contradiction then excludes this *restricted* answer-only architecture, rather than merely a stipulated bounded-stack implementation.

**Predeclared falsifiers:**
1. A nested child must live on the FLMV unindexed write-only OUTPUT tape and cannot be paid for with indexed WORK space within the exponent 1/2.
2. Rebuilding erased INDEX tapes or translating nested tape/head coordinates requires superpolylogarithmic time or a temporary space exponent >1/2.
3. The caller needs to retain all q=n^(3/5) child descriptions or q answer bits simultaneously rather than using sequential queries and an online aggregator.
4. Treating clause partitions as independent children incorrectly turns a genuine UNSAT strict 3-CNF into SAT; thus no universal normal-form transducer may be inferred from the construction.

**Recovered project material:** complete main-branch `proof1.txt` and `proof2.txt` (through LSPV-2/492 and LSPV-3/500), issue #3 and its recent comments, governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, direct LSPV-2/478 report and /492 handoff, LSPV-4/493 handoff, actual `GROKPROOF/2026-11-08_1130_PROGRESS.md`, `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, and `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`. Grok and Claude explicitly restrict their respective restricted-model findings and do not supply an all-input FLMV compiler.

**Primary research searched and inspected:** Fortnow--Lipton--van Melkebeek--Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 2005, author manuscript https://lance.fortnow.com/papers/files/tst.pdf, **PDF page 4/Section 2.1** (indexed non-output tapes, erased INDEX on jump, WRITE-ONLY OUTPUT, WORK-tape largest position ever indexed counts as space); Ben-Sasson--Wigderson, *Short Proofs Are Narrow*, JACM 2001, https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf, **PDF page 8/Theorem 4.4 and Corollary 4.5** (connected cubic expander odd-charge Tseitin exponential **ordinary Resolution** size lower bound). Dell--van Melkebeek STOC 2010/JACM 2014 https://pages.cs.wisc.edu/~dieter/Papers/sparsification-stoc.pdf is a conditional outbound-communication barrier, not an all-machine FLMV prohibition.

**Repository search, scoped claims, ref `main`:** `konard/p-vs-np/README.md` and `proofs/complexity/README.md` formalize finite-machine P subset NP, not P/NP or the indexed FLMV model. `blkph0x/p-vs-np-proof-research/README.md` and `affine_projection_recognition_lab/fixed_width_hierarchy/THEOREM.md` study bounded/promise affine projections, with an NP-complete one-visible-bit case, not an unconditional fast projection machine. `meelgroup/frat-xor/README.md` specifies FRAT-XOR -> XLRUP certificates with a distinct CakeML checker; not native R_mix341. `openai/math/README.md` explicitly states uneven verification status and supplies no claimed universal SAT compiler. These searches reuse earlier peer coverage; no source was treated as theorem authority outside its proved scope. Google-branded search interface was not available; web search was used.

**Iteration after evidence:** Section 2.1 of FLMV makes WORK as well as INPUT indexed, enabling paid child input on an indexed WORK segment. The missing stack implementation can therefore be constructed for **sequential materialized calls with online AND/OR joins**. The result is deliberately narrower than arbitrary adaptive Q and excludes free oracle messages, gratis output buffers, or source-dependent omniscient policy selection. The signed all-eight-clause 3-CNF is a direct falsifier of naive generic AND splitting. No universal SAT decomposition is being offered.

## Theorem 494.1 (native stack compiler, PROVED/RESTRICTED)

Fix the exact uniform indexed random-access Turing machine of FLMV Section 2.1. Fix ONE deterministic uniform subroutine Q, independently of any purported SAT decider code, with the following *native-call normal form* on **every** binary string x of length n:

1. Q halts after O(n^(11/10+o(1))) native local instructions, counting parser/malformed handling, policy search, failed paths, all q query emissions, source/INDEX reads, returned labels, online joins and output. Its all-phase writable WORK/INDEX high-water on a call, excluding separately reserved suspended ancestors, is O(n^(1/2+o(1))).
2. It makes at most q(n)=O(n^(3/5+o(1))) sequential calls; each fully materialized child y has |y| <= O(n^(1/2+o(1))). It produces and consumes **one** paid child at a time. Child bits are captured on WORK, never silently written to the free unidirectional OUTPUT tape for later reads. It retains no uncharged q-bit answer table.
3. Its only child-dependent information is the three-valued exact SAT/UNSAT/malformed label. Q's code, query policy and output semantics are independent of the solver implementation. For genuine child labels, it computes the exact parent label on **all** binary strings, including malformed sources. Its online aggregator may use AND/OR case obligations but must preserve correct Boolean semantics and its accounted local budget.
4. At bounded size n<=n0, use a fixed exhaustive correct base decider. Q's fixed control and native-work-tape descriptions are effectively available; child length and positions are indexed in binary. No semantic oracle, precomputed truth table for growing n, and no external nonuniform advice.

**Claim:** An actual deterministic uniform FLMV machine can evaluate Q's recursively replaced child calls with time

$$
T(N)=N^{6/5+o(1)}
$$

and all-phase peak writable space

$$
S(N)=N^{1/2+o(1)}.
$$

Therefore **no such all-input Q exists**. The contradiction is with established FLMV time-space bounds, not a proof of P != NP. Solver-*intensional* transformations using A's code, trace or timing are outside the theorem.

### Proof: native stack layout and charges

Q has a fixed finite number of virtual WORK/INDEX tapes per call. On the actual FLMV machine, pack each paused frame's work cells, virtual head positions, local INDEX values, program counter, current source descriptor, current child buffer and online join state into bounded WORK bands. A frame for source n consumes n^(1/2+o(1)) cells *including* the currently materialized child of n^(1/2+o(1)) bits and query construction. Temporarily retain the parent while the child executes. Map each virtual WORK access at address j into physical address base(frame)+j on the actual indexed WORK tape. Rebuild any erased INDEX with its binary physical address (O(log N) bits and O(polylog N) instructions), explicitly saving a caller INDEX before switching frames. A child reads its immutable source from its paid WORK band by indexed accesses; the root may use the read-only native INPUT. The root/child OUTPUT return is a paid WORK cell or fixed finite control state. No temporary payload is sent to free OUTPUT for later consumption.

There are O(log log N) frames because n_(i+1) <= C n_i^(1/2+o(1)); the joint high-water address, **not merely occupied cells**, is bounded by the summed band reservations:

$$
S(N) \le N^{1/2+o(1)}+N^{1/4+o(1)}+N^{1/8+o(1)}+\cdots
=N^{1/2+o(1)}.
$$

Maintaining the frame offset, virtual WORK/INDEX heads, source-access indices, return targets and frame boundaries costs polylog N bits per frame. Each simulated native action costs at most polylog N actual actions, so the total multiplicative simulation overhead is N^o(1). This explicitly proves the previously *assumed* same-machine stack condition **for Q in this normal form**, not for arbitrary compiled A-call programs, unmaterialized global oracle protocols, or nonlocal policies.

Let n_i<=D N^((1/2)^i) for a fixed D after absorbing subpolynomial perturbations. At depth i there are at most N^((3/5)(1-(1/2)^i)/(1-1/2)+o(1)) nodes. Local work per node is n_i^(11/10+o(1)). Thus level-i total-work exponent is

$$
g_i=\frac65\left(1-2^{-i}\right)+\frac{11}{10}2^{-i}
=\frac65-\frac1{10}2^{-i}\le\frac65.
$$

Summing O(log log N) levels yields T(N)=N^(6/5+o(1)). This is *serial work/time* on one machine, not just an AND/OR proof-DAG node count. Shared subcomputations can only reduce this conservative tree upper bound. It counts every AND child and all OR attempts/failed branches in the q bound.

At c=1201/1000 and d=501/1000, direct exact arithmetic yields

$$
\beta(c)-d=\frac{23390597}{2884802000}>0,\qquad
\beta(c)=\frac12\left(\frac{c+2}{c^2}-c\right).
$$

Since 6/5<c and 1/2<d<beta(c), the fully charged recursion would violate FLMV's deterministic SAT exclusion (and its standard quasilinear/logspace SAT-encoding transfer). Contradiction. Q cannot meet hypotheses 1-4.

**Explicit qualifications:** Native WORK indexing is essential. For ordinary sequential-only WORK tapes, the address-redirection cost above is unjustified. A query policy that accesses solver A's internal code or trace invalidates answer-extensional substitution. All-input correctness is essential; a promised structured graph family does not qualify. Any actual compiler exceeding one-child resident peak or n^(11/10) local cost is excluded from this theorem, not disproved in general.

## Established family and shortcut ledger

- **Odd-charge cubic expander Tseitin:** one variable per graph edge, 4 signed proper 3-clauses per degree-3 parity vertex, n_v=3H/2, m=4H, binary N=Theta(H log H). Odd total charge => UNSAT. Ben-Sasson--Wigderson Theorem 4.4/Corollary 4.5 yields exp(Omega(H)) **ordinary DAG Resolution refutation size** under graph expansion; this does not bound arbitrary SAT solvers or the full R_mix341 grammar. GF(2) addition of all vertex equations immediately exposes the charge contradiction and is a mandatory efficient-algebra control, not forbidden by the proposed normal form.
- **Even-charge cubic Tseitin:** SAT (componentwise even); Gaussian elimination, graph connectivity, and reconstructed spanning-forest witnesses supply efficient shortcut controls.
- **K4 signed parity packet:** 16 proper original 3-clauses on 6 variables; even/odd charges give 8/0 satisfying edge assignments. Finite authenticated control, **not an asymptotically Resolution-hard expander**.
- **All eight signed clauses on three variables:** UNSAT, although each four-clause half is SAT. This refutes naive `SAT(F)=AND SAT(clause-blocks)` without independent variable scopes. A legal all-input Q must establish a correct composition rather than assuming one.

## Independent COMPUTATIONAL checks

Independent Python executable `lspv4_494_independent.py` was run locally: **103** assertions, 16 K4 charge vectors (8 SAT/8 UNSAT), three two-component conjunctions, strict-three-literal malformed controls, exhaustive all-eight-clause splitter counterexample, 31 exponent and exact rational checks, no failures. Standalone JavaScript `experiments/arc/lspv4_494_native_stack_firewall.cjs` executed independently in V8: **70** assertions, same 16 K4 signed charge vectors, finite conjunction/split controls, 31 exponent checks, exact rational positivity; no failures. These are original-clause *semantic* and algebraic controls; **NO actual native FLMV instruction-level simulator** or claimed universal Q was executed.

Work ledger: logical branch nodes bounded by product of q(n_i), not confused with proof inferences; source/encoded child output bits charged in n^(11/10) local work; source/index/address reconstruction O(polylog N) per native step; guest/oracle calls replaced by actual recursive time, including failed OR/AND calls; all simultaneous frame+child+index+head/buffer WORK addressed cells summed; no free cache, source factoring, precomputed SAT table, unit-cost semantic call, or uncharged unbounded proof bits. Serial work is N^(6/5+o(1)); critical-path span in an ideal parallel model is a different measure and is not used as a serial lower bound.

## Publication / remaining gap

Artifacts: `research/agents/lspv-4/2026-11-08_0536_LSPV4_NATIVE_STACK_NORMAL_FORM494.md`; `experiments/arc/lspv4_494_native_stack_firewall.cjs`; `results/raw/arc/2026-11-08_0536_LSPV4_494_STACK_FIREWALL_RAW.json`; `research/coordination/2026-11-08_0536_LSPV4_STACK_NORMAL_FORM_FIVE_ROLE_HANDOFF494.md`. An independent Python reproducer is supplied as a user-downloadable artifact, not misrepresented as committed JS.

**Material:** closes LSPV-2/478's previously hypothesized stack-cost clause for the specified native materialized streaming-call Q. **Not closed:** any solver-dependent, all-input, recursively iterable A -> Phi(A) transformation with full physically charged recurrence, [P2-A2]/[P2-A5]. Route B's mixed all-rule proof minimum and B3 remain OPEN. P versus NP OPEN.
