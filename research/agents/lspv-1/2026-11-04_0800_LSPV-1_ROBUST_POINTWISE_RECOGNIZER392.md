# LSPV-1/392: Robust pointwise recognizer patch against proof-to-runtime transfer

**November 4, 2026, 08:00 PST (America/Los_Angeles).** **PROVED/EXACT** elementary scoped metatheorem with all quantifiers shown; independent specialist mathematical review pending. **KNOWN THEOREM** Haken ordinary-Resolution PHP hardness. **COMPUTATIONAL** producer 109 checks and independently implemented verifier 238 checks. **OPEN** B1/B2/B3 for the unchanged fixed `R_mix341`, its superpolynomial worst-case minimum, and P versus NP. No calculus, task, role, weight, enabled state, or schedule change.

## 1. Published anchor, exact proof model, encoded size

Use the standard **unary pigeonhole** CNF `P_h=PHP(h+1,h)`: variables `x_(p,j)` for `0<=p<=h,1<=j<=h`; `h+1` positive clauses asserting each pigeon chooses a hole; `h*binom(h+1,2)` negative binary clauses forbidding any pair from sharing a hole. This source has `h(h+1)` variables and `m_h=h+1+h*binom(h+1,2)` original signed clauses. An explicit unsigned-header, signed-literal, self-terminating list with binary-indexed identifiers has **`N_h=Theta(h^3 log(h+2))` bits**, while the specific canonical ASCII DIMACS instances used for finite controls have 208, 608 and 1600 bits for `h=1,2,3`.

**Haken (1985):** there exist constants `c>0,h0` such that for **every** `h>=h0` and **every ordinary unrestricted, shared-DAG Resolution refutation** `pi` of standard `P_h`, the number of proof lines is at least `2^(c h)`. Allow any pivot, width, sharing, and derivation order, but **do not allow** extension-variable definition rules, GF(2) inference, oracle axioms, or auxiliary semantic gates. With original source leaves free, the paid derived-node minimum satisfies

$$
W_{\mathrm{Res}}(P_h)\ge 2^{ch}-m_h=2^{\Omega(h)}
$$

for sufficiently large `h`. The theorem does **not** bound arbitrary correct uniform SAT algorithms or the combined mixed calculus. **Cook (1976)** supplies polynomial Extended Resolution proofs for the same source. The project's fixed `R_mix341` includes conservative paid two-input DEF plus RES and has a polynomial ER-style escape, so `W_{R_mix341}(P_h)` is **not** thereby hard. Likewise odd Tseitin has a GF(2) escape.

The unchanged target `R_mix341` is LSPV-2/341 (original blob `c87acd11...`): free source-authenticated CNF axioms; unit-charged distinct shared nodes; binary RES, support-at-most-three-original-variable AND3, binary GF(2) XOR, authenticated constant-support LOCAL-CONVERT, conservative paid two-input DEF. Its circuit-port semantics remain under audit. For fixed `R`, define `W_R(F)` as the minimum valid shared-DAG paid-node cost (the optimum may be selected freely), and `Wbar_R(N)` as its maximum over valid UNSAT formulas with exact input **bit** length at most `N`, with empty maximum zero.

## 2. New sharpened theorem: every baseline decider admits a polynomial-overhead B1-failing patch

**Theorem 392 (robust pointwise patch, restricted to a proof system with a uniformly recognizable hard UNSAT subfamily).** Let `L` be a decidable ternary-classification problem (`YES/NO/MALFORMED`) with a fixed canonical input grammar. Let `R` be a fixed sound complete refutation calculus for NO sources. Assume there is an infinite unbounded family `H={F_n}` of **valid NO inputs**, whose set of canonical encodings is recognizable by **one fixed polynomial-time algorithm** `C` with no false positives, and whose minimum `R` refutation cost is not bounded by any polynomial of `|enc(F_n)|` along this family.

Then **for every** fixed uniform total correct ternary decider `A` for `L`, there is **one fixed** uniform total correct ternary decider `B_A`, and constants `d,C_A>0`, such that for **every** binary input `x`,

$$
T_{B_A}(x)\le C_A\bigl((|x|+1)^d+T_A(x)+1\bigr),
$$

while for **every** `n`,

$$
T_{B_A}(\mathrm{enc}(F_n))\le C_A(|\mathrm{enc}(F_n)|+1)^d.
$$

Consequently the pointwise bridge `B1(R)` is **false for this specific fixed R**, because no polynomial `p_{B_A}` can dominate `W_R(F_n)` by `p_{B_A}(|F_n|+T_{B_A}(F_n))` along the unbounded hard family. Moreover,

$$
T_{B_A}^{wc}(N)\le C_A\bigl((N+1)^d+T_A^{wc}(N)+1\bigr),
$$

where the worst-case maximum is over **all binary strings of length at most N**, including malformed. This is a **per-input additive polynomial-overhead domination** for every baseline `A`, not just a single slow exhaustive fallback, and never selects a new algorithm per source or per length.

**Proof.** Embed the one fixed exact syntactic recognizer `C` and the code of the one fixed correct `A` in a single machine `B_A`. On every input `x`, first execute `C(x)` with all source reads, parsing, comparisons and intermediate allocation charged. If `C` accepts, return NO. This is correct because its accepted set consists only of known NO instances. If it rejects, execute `A(x)` and return the exact three-way result, including MALFORMED; this is correct because `A` is. Both computations are on the **same input and same fixed machine**. The recognizer costs at most `O((N+1)^d)` in the declared standard bit model; compiled simulation of fixed `A` contributes `O_A(T_A(x)+1)`. This gives the pointwise bound, and taking maxima gives the worst-case upper bound. On each canonical hard `F_n` the recognizer accepts without running `A`, proving the uniform polynomial time bound. If B1 held for `B_A`, its right side would be polynomial in `N_n`, contradicting the assumed superpolynomial `W_R(F_n)` on the same uniformly chosen family. QED.

**Unconditional specialization to ordinary shared-DAG Resolution:** set `F_n=P_h`; its canonical membership is polynomial-time recognizable by parsing `h(h+1)` variables, recovering `h`, checking source-clause counts and each signed source clause against a fixed canonical ordering. Generating and comparing the canonical source uses polynomial bit time/space with no SAT oracle. Haken proves the hard-side hypothesis. Hence **for every correct uniform SAT decider A** there is a uniform `B_A` that is polynomial on the whole canonical PHP family, never more than additive polynomial slower than `A` on any input, and **falsifies B1 for ordinary Resolution**. It does not contradict the independent fast ER certificates for PHP in `R_mix341`.

## 3. Exact falsifiers and bridge classification

**F1: a false-positive recognizer can make the patch unsound.** Correct: accepting any SAT lookalike would destroy soundness. The theorem assumes an exact canonical syntactic recognizer and never accepts based merely on approximate clause/variable counts. Finite strict controls reverse one literal sign (SAT neighbors) and reorder original PHP clauses (noncanonical yet UNSAT); both fall through to the complete baseline. Malformed records likewise fall through.

**F2: an intrinsically fastest baseline algorithm might restore B1.** False for the declared proof system: the theorem patches **every** total correct baseline `A` and stays within additive polynomial overhead of `A` on all inputs. No claim is made that such an optimum baseline exists.

**F3: Haken hard PHP refutations force an arbitrary SAT solver to spend exponential time on each PHP input.** False: this construction supplies a fast uniform recognizer, and Extended Resolution supplies the proof-system shortcut. The result is a genuine **POINTWISE B1 counterexample for Resolution**, not an all-algorithm SAT lower bound.

**F4: this disproves B2 or B3 for the unchanged combined R.** False: `B_A` can retain huge worst-case runtime through its fallback; the theorem gives an **upper** comparison of worst-case runtimes, not the lower time needed for B2. No superpolynomial `Wbar_{R_mix341}` is known, and PHP is easy in the mixed calculus. B3 remains the separate implication `SAT in P => Wbar_{R_mix341}(N)=N^{O(1)}`.

The exact B1/B2/B3 prefixes for one preselected `R_mix341` remain:

$$
\begin{aligned}
\mathrm{B1}:\quad&\forall A\ \exists p_A\ \forall F\in \mathrm{UNSAT}:\quad W_R(F)\le p_A(N(F)+T_A(F)),\\
\mathrm{B2}:\quad&\forall A\ \exists p_A\ \forall N:\quad\overline W_R(N)\le p_A(N+T_A^{wc}(N)),\\
\mathrm{B3}:\quad&\mathrm{SAT}\in P\Longrightarrow\overline W_R(N)=N^{O(1)}.
\end{aligned}
$$

All three are **OPEN for full `R_mix341`**. B1 implies B2 implies B3, but the present restricted ordinary-Resolution B1 refutation establishes neither a counterexample nor a proof for the other two.

## 4. Fully separated costs and finite controls

Logical source-anchored Resolution proof length is not solver time. The constructed recognizer charges its exact input acquisition, parsing, integer decoding, clause enumeration, canonical-string checking, branch cost and output; false matches trigger the baseline. It can materialize a polynomial-length comparison source and use polynomial temporary space. The theorem is a **time upper bound**, not a low-space FLMV contraction. The baseline may construct exponential intermediates, with all work and peak live space charged inside `T_A` and its own space bound. A hypothetical algorithm using long lazy pointers must pay their accesses. The free logical optimizer selecting `W_R` is not employed computationally.

The deterministic public JavaScript producer exhaustively classified h=1,2,3 canonical PHP sources, checked **all 70 one-sign SAT neighbors** by full assignment enumeration, checked zero original models, and checked three noncanonical-but-still-UNSAT permutations, 8 malformed inputs, ordinary contradictory units and SAT units. It passed **109 logical assertions**. Independently written JavaScript reconstructed a direct satisfying assignment for every flipped literal, rather than copying the exhaustive enumerator, passed **238 assertions**, and checked one deliberate raw metadata corruption. Both tests are **COMPUTATIONAL**. Finite tests do not prove Haken's theorem, the general patch theorem, or the correctness of an arbitrary baseline machine; the latter follow from the external published theorem and symbolic argument. No random seed.

Published readback originals:
- Producer: `experiments/arc/lspv1_392_php_patch.js` (blob `c813de407fba735462fa825f236fff8b753f2efa`).
- Independent verifier: `experiments/arc/lspv1_392_independent_verify.js` (blob `a27f1df272477869268923e55bfe833a54575306`).
- Raw result: `results/raw/arc/2026-11-04_0800_LSPV1_ROBUST_RECOGNIZER_PATCH392.json` (blob `13e5550131a00abe803c7653bc250bf5ec226e77`).
- Publication-check replay: producer and independently written verifier were **executed from fetched GitHub source**, obtaining identical raw records and 238 successful independent checks.

## 5. Duplication audit, external assessments, literature

The same old **pointwise Resolution B1 failure** from a PHP/Tseitin recognizer and exponential fallback is already in the governing refocus and LSPV-4/341. LSPV-1/368 strengthens a *different* conditional point by exhibiting a hypothetical polynomial-time decider with artificially high worst-case polynomial exponent and fast PHP queries. **The incremental content here** is the exact quantifier `forall A exists B_A` with an all-input **additive polynomial** runtime bound relative to arbitrary `A`, and its abstract recognizer/hard-family criterion. We do not claim to have found a new hard family or a new general proof-complexity separation.

Repository state inspected: November 2 user refocus (current blob `c3889a3e514ddbd747150dcb68607013a3b2d154`, original pinned commit `4e29ed7...`), current coordination issue #3 through November 4 07:57 PST; AGENTS.md (`19656af1`), CODEX.md (`754999f5`), repository skill (`b8df83a7`); original LSPV-2/341 fixed rules (blob `c87acd11`); LSPV-1/336, /357, /368, /390, /391; LSPV-2/391 and /392; LSPV-3/394-/396 and /395 source-core lower bound; LSPV-4/387-/388; Red Team /334 and /338-/339. The newer REFEREE339 improves the exact *prefix-aligned B2 encoding* transfer, whereas the present result addresses a distinct pointwise B1 failure. In particular, LSPV-1/336 already proves no effective enumeration of all correct SAT deciders; an initially proposed correctness-index extension was **retired as duplicate** and not published as new mathematics.

The directories were actually listed. The latest inspected Grok file is `GROKPROOF/2026-11-04_1518_PROGRESS.md` blob `4e2bb9d941295f620a64e078117d29244caf4fba`; it continues to leave the required fully charged all-input FLMV compiler **OPEN**. Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67` and `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a` use restricted portfolio/sequential-tape models, not this all-input B3 implication. Cross-domain analogy to oracle query sensitivity is only an analogy, since this proof uses an exact syntactic recognition branch rather than an intrinsic necessity.

Primary literature/source queries: `Haken 1985 Intractability of Resolution pigeonhole exponential lower bound`; `Cook 1976 short pigeonhole proof Extended Resolution`; `Cook Reckhow 1979 relative efficiency`; project GitHub queries `recognizer domination pointwise polynomial`, `Haken PHP every correct decider A fallback`, `clocked SAT decider correctness`; OpenAI-owned theorem implementation searches previously documented in /391 found no B3 compiler and were not repeated as novel discoveries. Primary sources: [1] A. Haken, *The Intractability of Resolution*, TCS 39 (1985), 297–308, https://doi.org/10.1016/0304-3975(85)90144-6; [2] S.A. Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4) (1976), 28–32, https://doi.org/10.1145/1008335.1008338; [3] S.A. Cook and R.A. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36–50, https://doi.org/10.2307/2273702. No all-input (R_mix341) transfer is attributed to them.

## 6. Exact next arrow and publication status

**Next genuinely sufficient B3 target:** for a hypothetical single fixed P-time SAT decider, justify by a model-preserving noncircular construction why **every** valid UNSAT F has a polynomial-size derivation in exactly the original mixed calculus. Correctness of a rejecting computation is not itself an R-refutation. Independently, seek an established family whose superpolynomial minimum survives all allowed RES/AND3/XOR/LOCAL-CONVERT/DEF combinations. The present theorem is a precise counterexample to upgrading restricted proof hardness into pointwise algorithm time, not an answer to either main gap.

**B1/B2/B3 for `R_mix341`, superpolynomial `Wbar_{R_mix341}`, and P versus NP remain OPEN.**
