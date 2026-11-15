# TMR-4/032: Pippenger-Fischer near-linear indexed-table firewall for ordinary MCSP

**Date:** 2026-11-14 16:50 PST (America/Los_Angeles). **Role:** TMR-4, Cost-Sound Abstraction. **Status:** **PROVED/RESTRICTED**, as a derived conditional-on-model consequence of a **KNOWN THEOREM** (Pippenger and Fischer 1979, Theorem 4); independent TMR-1/TMR-5 scrutiny **OPEN**. Executed finite checks are **COMPUTATIONAL**. P versus NP remains **OPEN**.

## 1. Genuinely new contribution and corrected scope

TMR-4/031 established an exact full-indexed-table circuit bound `CC_n(Y) <= K_E(L+n+t+2)^2` by direct one-hot unrolling. TMR-5/027 obtained a corresponding polynomial-degree collapse only when `a*mu > 2d` for `N=L^{a+o(1)}` and indexed evaluation time `L^{d+o(1)}`. The previously cited Pippenger-Fischer source actually provides the **stronger** one-dimensional-tape circuit simulation of size `O(H log H)`, not just the quadratic direct construction. This run states an explicit charged adapter and applies that *original theorem* to improve the sufficient positive-power-MCSP-YES condition to

$$
a\mu>\max(1,d).
$$

The indispensable `max(1,d)` rather than simply `d` arises from reading/copying the explicit source of length `L`. This is an **upper bound on circuit size of a constructed target function**, not an MCSP decision lower bound, a SAT lower bound, or a polynomial-time explicit-output SAT reduction. A stronger circuit simulation theorem does not manufacture the required hardness-magnification antecedent.

## 2. Exact model, quantifiers, theorem, and proof

Fix **one** finite program `E`, a total deterministic multitape Turing-machine indexed evaluator with a fixed finite alphabet and number of ordinary one-dimensional tapes/heads. Its inputs are a binary source `F` of encoded length `L` and a target index `i in {0,1}^n`, with standard delimiters and read-only head movement permitted. It produces one output bit. All its transition costs include syntax inspection, work, branching, temporary representations, rereads, indices, and output. Define the complete *mathematical* truth table

$$
Y_{E,F,n}[i]=E(F,i),\quad N=2^n,\quad
t_{E,F,n}=\max_{i\in\{0,1\}^n}T_E(F,i).
$$

Circuit size `CC_n` uses fan-in-two AND/OR, unary NOT, free constants and input wires, and unrestricted fanout. The source `F` is **hardwired** only in a nonuniform circuit-size *upper-bound argument*. No SAT oracle or algorithm-dependent advice is supplied to a putative uniform SAT decider.

**PF-LIFT044 (PROVED/RESTRICTED, peer review OPEN):** There exists a finite constant `K_E>=1`, dependent only on the one fixed evaluator and standard encoding, such that for **every** source `F` and arity `n`,

$$
\boxed{CC_n(Y_{E,F,n})\le
K_E H\log_2(2H),\quad H=L+n+t_{E,F,n}+2.}
$$

**Proof and model translation.** Pippenger and Fischer [1], Theorem 4, original printed p.379, constructs a combinational network of cost `O(h log h)` for the first `h` steps of **any fixed transducer with one-dimensional tapes**. Its input is a one-way stream of `h` input symbols and its outputs encode the `h` output symbols. The original finite tape alphabet and finite universal gate basis cost are absorbed into one machine-dependent constant. Their construction works for a fixed finite number of one-dimensional work tapes.

To apply the exact model rather than silently equating a random-access source with a one-way stream, build **one fixed auxiliary transducer** `E'`. It first scans the entire explicitly delimited pair `(F,i)` once **left to right**, copying both parts, together with endmarkers, onto ordinary local-head work tapes. This uses `O(L+n+1)` transitions, finite tape tracks, and `O(L+n+1)` visited cells. For any additional virtual read-only input head of `E`, keep a corresponding copy of the source on a separate work tape with its own movable head; an arbitrary fixed finite number of such heads is accommodated by a fixed finite tape count. Simulate every concrete transition of `E` on the copies and its other work tapes with constant-factor transitions, with no free input rereads or temporary memory. On halting, latch its output bit and repeat that bit in the output stream in a stationary/absorbing phase. This converts a potentially two-way-read-only-input evaluator into a physically charged one-way-input transducer with at most `c_E H` steps until its correct latched output. Padding any faster run to the selected horizon does not change its bit.

Apply [1, Theorem 4] at horizon `h=ceil(c_E H)` to the **fixed** `E'`. Fix the source portion of its input-symbol wires to the literal bits of `F`, connect the index-symbol wires to the `n` Boolean index variables, and fix delimiters and post-endmarker input wires to constants. Select the last latched output wire. The resulting n-input circuit computes the exact bit `E(F,i)` for **every** i, including all adaptive control and intermediate work, and has gate count at most `K_E H log_2(2H)`. Any fixed finite universal basis is converted at constant cost to the declared AND/OR/NOT basis. This is a nonuniform *existence* proof for a target circuit, not a free uniform circuit constructor. QED.

**MCSP transfer, with floors:** Let `s= floor(N^mu)`, fixed `mu>0`. If

$$
K_E H\log_2(2H)\le s,
$$

then the **entire explicit table**, if actually generated, belongs to ordinary exact `MCSP_n[s]` YES. It cannot be a Hamming-far Gap-MCSP NO for the same size-s comparison class, since an **exact** small circuit exists. Conversely, if this target is an ordinary MCSP NO, then `s<K_E H log_2(2H)`, hence, for `s>=2`,

$$
\boxed{t_{E,F,n}>
\frac{s}{K_E\log_2(2s)}-L-n-2.}
$$

For this last inequality, if `H<s`, replace `log_2(2H)` by the larger `log_2(2s)`; if `H>=s`, the claimed lower bound follows immediately from `K_E>=1`. This only lower-bounds a specified **indexed generator's** worst-index execution when its full output truly is a NO table. It is not an unrestricted MCSP classifier or SAT-decider lower bound.

**Quantified polynomial degree window:** Assume one fixed `E` with `t(L,n)<=L^{d+o(1)}` for every source/index of the declared lengths, `N=L^{a+o(1)}`, with fixed `a>0`, `d>=0`, and `n=Theta(log L)`. Then `H=L^{max(1,d)+o(1)}`. For every fixed positive `mu`, the strict condition

$$
\boxed{a\mu>\max(1,d)}
$$

forces `K_E H log(2H)=o(N^mu)`, and all sufficiently large outputs for **both** SAT and UNSAT sources become ordinary MCSP YES. Thus a reduction using such a bit-index generator cannot map one source label to required MCSP NO. This is a strictly stronger numerical firewall than the previous *quadratic* sufficient condition `a mu>2 max(1,d)`. In particular, for `a=10, mu=3/10, d=2`, `3>2` but `3\not>4`. The case `d<1` must retain the paid source-copy `L` term; dropping it would be unjustified.

**Explicit-output and unrestricted-machine gaps.** A full table has length `N=2^n` and takes at least `Omega(N)` output operations. A succinct-index oracle is **not** ordinary MCSP. Polynomial output `N=poly(L)` is allowed but the fast-index exponent restriction may fail; e.g., `L=N`, `n=log_2 L`, `E(F,i)=F[i]` in `O(L)` time outputs arbitrary truth tables, and standard circuit counting gives ordinary MCSP NO instances at every fixed `0<mu<1` for sufficiently large `n`. These are arbitrary source words, not asserted to be proper 3-CNF. Nor does our circuit-size bound imply that a reduction can efficiently *find* or *test* minimum circuits. No property of arbitrary correct deterministic SAT machines is proved.

## 3. Primary-source theorem/model matrix

| Primary theorem | Exact hypotheses, input measure, model and conclusion | Transfer limit |
| --- | --- | --- |
| [1] Pippenger-Fischer, JACM 1979, **Theorem 4**, printed p.379 and proof pp.379-380 | A **fixed transducer with one-dimensional storage tapes**: its first `h` transitions on an `h`-symbol input stream have a **nonuniform** combinational logic network of gate cost `O(h log h)` and depth `O(h)`; universal finite gate basis and fixed finite tape count. No MCSP promise or SAT hardness. | Requires our **charged** one-way-copy adapter. Does not say a uniform indexed circuit can be *constructed* in that time. |
| [2] Cheraghchi et al., STACS 2021, **Theorem 1**, printed p.23:3 | Ordinary exact `MCSP[2^{mu1 n}]`, full truth-table input `N=2^n`; one-way read-only input plus one two-way work tape, deterministic `DTIME_1[N^{1.01}]`; **for a sufficiently small fixed mu1>0**, exclusion implies `P!=NP`. | The decisive low-threshold lower bound **OPEN**. Our indexed function circuit *upper* bound supplies none of it. |
| [2] Cheraghchi et al., **Theorem 2**, same page | Ordinary MCSP at a **different larger `mu2` close to 1**; randomized bounded-error one-way-input/one-work-tape, unconditional exclusion from `BPTIME_1[N^{1.99}]`. | Different threshold, even with stronger time exponent. Cannot be substituted into Theorem 1. |
| [3] McKay-Murray-Williams, STOC 2019, original Theorems 1.2-1.3, pp.2-3 | Search/streaming `MCSP^A[s]` with oracle access and its specified update/space bounds, as stated in the original paper; full `N=2^n` table, not ordinary decision MCSP. | No free transfer between search, oracle, MKTP, Gap, succinct or ordinary decision variants. |

Sources [1] original author PDF text at p.379 and its Theorem 4 proof were inspected; the publisher PDF screenshot endpoint returned HTTP 403, a visual-access limitation (do not claim successful screenshot). [2] original publisher PDF screenshot p.23:3 inspected. [3] original author PDF theorem pages inspected in earlier role review; no new MMW theorem is imported in the present proof.

## 4. Corpus and prior-status ledger (original paths)

| Original artifact | Retained status and relation |
| --- | --- |
| `research/agents/tmr-4/2026-11-14_1537_TMR4_INDEXABLE_LIFT_FIREWALL031.md` and `experiments/tmr/tmr4_indexable_lift039.js` | Previous `O(H^2)` exact compiler, **PROVED/RESTRICTED**, independently audited now using [1] |
| `research/agents/tmr-5/2026-11-14_1552_TMR5_DEGREE_WINDOW_CONSTRUCTOR_REVIEW027.md` | Previous `a mu>2d` frontier, **PROVED/RESTRICTED**; corrected with `max(1,d)` and a stronger published network theorem; constructor-interface objection remains OPEN |
| `research/agents/tmr-2/2026-11-14_1618_TMR2_RANDOM_SHARED_SPARSE_MINIMAX031.md` | Fully shared adaptive **evaluation-oracle** minimax theorem; correct only under black-box source access, not syntax-aware SAT |
| `research/agents/tmr-3/2026-11-14_1635_TMR3_SHARP_SPARSE_NETWORK_SOURCE_FRONTIER031.md` | Source-bit-query MCSP bounds under explicit ingress charging, not post-ingress superlinear cost |
| `research/agents/tmr-4/2026-11-14_0836_TMR4_MOMENT_CONGRUENCE_AND_QUOTIENT_COUNTEREXAMPLE023.md` | Cubic Walsh/signed-clause streaming summary retains complete source semantic information, but cannot decide unrestricted SAT in polynomial time by itself |
| `research/agents/tmr-4/2026-11-14_1142_TMR4_GAPMCSP_AFFINE_KERNEL_CYLINDER027.md` and `research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex` | Affine-sketch collisions and Hamming-distance extension, **restricted** to fixed linear sketches |
| `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`, `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` | Portfolio/direct-product and crossing-sequence arguments have restricted resource interfaces, not arbitrary SAT transfer |
| `comments/grok-4.7/2026-10-21/2026-10-21_0013_GROK_REVIEW.tex` | Historical compact-algebra, semantic-fiber and cost-boundary falsifiers remain relevant; no theorem promotion |

Earlier TMR-4 masked-CNF and dummy-padding strategies remain retired only as proposed universal *positive-power hardness amplifiers*. This theorem permits compact GF(2), Horn, 2-SAT, bounded-treewidth, adaptive control, sharing, rereading and all program-dependent computation, because the circuit simulates the whole chosen evaluator, not a solver template.

## 5. Actual independent finite checks and provenance

**Actually executed native CPython** using published exact `experiments/tmr/tmr4_pf_index_lift044.py`, seed 4044, and exact immutable JSON `results/raw/tmr/2026-11-14_1647_TMR4_PF_LIFT044_RAW.json`. The executable SHA256 is `e7e46bb616a871596422462cd07f9853190483790321e7d11c245c7acafc035a`, Git blob `bff8ce334976bd4759db3d4a7c56aea6f2352afc`; raw SHA256 `453c4eeb572ef04bc58f414be918efdc73b8d0f34fa5c8c82acccfe36e0901c4`, Git blob `8eb7e3f2ff4b2aad27a8fe11d7d155be527dfb2d`. The native replay produced **24,918 assertions, 0 failed**, 292 proper 3-CNF formulas, 24,672 per-index comparisons of a direct syntax-aware evaluator against independently built AND/OR/NOT gate DAGs, plus exact integer/BigInt-free exponent and inequality controls and **24 strict-improvement example windows** with illustrative `K=128`. Controls include positive and negative clauses, all-eight-clause UNSAT, unique witness, Horn, an XOR-style family, and disjoint components. Neither the general Pippenger-Fischer circuit compiler nor a physical finite-tape machine was executed; all such generalization is from the original proved theorem and model argument. Very long truth tables were not allocated. The fixed test `K=128` is a numerical proxy, **not** the machine-dependent Pippenger-Fischer constant.

One draft contrapositive test initially reversed a numerical antecedent; it was corrected before the successfully replayed native run. No fabricated test count or runtime proof follows from finite checks.

## 6. Exact open gap, peer review, and governance

The **sole decisive magnification target** remains an unconditional proof that ordinary small-`mu1` MCSP is **outside** deterministic `DTIME_1[N^{1.01}]` in [2, Theorem 1]'s *exact one-way input plus one-work-tape* model. The present upper-bound firewall helps reject inefficient reduction designs; it cannot establish that lower bound. No unrestricted fixed-machine SAT runtime separation follows, and (P) versus (NP) remains **OPEN**.

**Next specific target:** test a fully explicit `N=poly(L)`, source-syntax-aware and globally shared SAT-to-ordinary-MCSP candidate at the **exact small circuit threshold**. For any proposed complete-output generator, determine its worst-index complexity `t` using the best charged input adapter, and attempt a matching upper-circuit falsification before asserting any NO label. **Peer request:** TMR-1 to check the P-F indexing/circuit input interface and the exact `a mu>max(1,d)` exponent; TMR-5 independently audit one-way copy, early-halt output latch, and inability to promote the model-specific generator inequality to SAT hardness; TMR-3 audit `Omega(N)` output charges; TMR-2 contrast syntax-aware with oracle-only query bounds.

**Preflight/governance:** Governing 2026-11-14 MCSP directive read first and 2026-11-13 replacement second; `AGENTS.md`, `CODEX.md`, repository `pnp-research` skill, newest five TMR handoffs, issue #3, original peer reports/code/raw, Claude/Grok and historical Walsh/affine failures reviewed. Complete `proof1.txt` (28,714 chars, SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`), authentic `proof2.txt` via original Git blob (1,051,196 chars, SHA `930c5eeddafce656717f28055a7a9a755f44737c`) and canonical `main.tex` via Git blob (2,545,859 chars, SHA `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34`) reviewed. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** `main.tex` belongs to TMR-5; no unauthorized modification. No task/schedule mutation.

## Numbered primary references

[1] Pippenger, N., and Fischer, M. J. (1979). *Relations Among Complexity Measures*. Journal of the ACM 26(2), 361-381, **Theorem 4, printed p.379**. https://doi.org/10.1145/322123.322138. Original PDF: https://www.ccs.neu.edu/home/viola/classes/papers/PippengerF-Oblivious.pdf.

[2] Cheraghchi, M., Hirahara, S., Myrisiotis, D., and Yoshida, Y. (2021). *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*. STACS 2021, **Theorems 1-2, printed p.23:3**. https://doi.org/10.4230/LIPIcs.STACS.2021.23.

[3] McKay, D., Murray, C., and Williams, R. (2019). *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes*. STOC 2019, **Theorems 1.2-1.3, pp.2-3**. https://doi.org/10.1145/3313276.3316396.

END_OF_REPORT::TMR4::PF-LIFT044::2026-11-14_1650_PST
