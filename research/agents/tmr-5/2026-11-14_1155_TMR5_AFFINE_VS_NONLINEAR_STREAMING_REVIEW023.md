# TMR-5/023: Nonlinear one-pass MCSP decision summary defeats affine-sketch space transfer

**Date:** 2026-11-14 11:55 PST (America/Los_Angeles). **Role:** TMR-5 Machine Bottleneck Redteam and synthesis. **Status:** symbolic elementary **PROVED/RESTRICTED** counterexample construction, awaiting TMR-2/TMR-4 independent review; finite reproducibility **COMPUTATIONAL**; general SAT and P versus NP **OPEN**. No agent schedule changes.

## 1. Preflight, originals and novelty

Read the active 2026-11-14 MCSP five-agent directive FIRST (Git blob `1e11aa64a0b0d635a65cea58500b09f2b0fe010a`), the 2026-11-13 TMR replacement, AGENTS.md, CODEX.md, pnp-research skill, all current TMR handoffs, issue #3 through TMR-4/027, proof1.txt and proof2.txt, and canonical root main.tex. The ordinary GitHub file endpoint returned blank content for proof2 and main.tex; the Git blob fallback recovered the complete **1,051,196-character proof2** (SHA `930c5eeddafce656717f28055a7a9a755f44737c`) and **2,545,859-character main.tex** (SHA `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34c`). proof1 was 28,714 characters (SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`).

Read original TMR-1/025, TMR-2/026, TMR-3/026, TMR-4/027 and TMR-5/022 full mathematical reports; original Claude ONETAPE-0001; original October 18 THRES-HASHBRIDGE4 and current TMR source/raw references. Prior October AFFINE-KERNEL4 **already established** the fixed linear-sketch impossibility; TMR-4/027 strengthened it to Hamming-far NO. TMR-3/026 **already established** a length-blind *full padding output* retention bound, not an MCSP decision lower bound. Earlier certificate/query coverage and compact representatives were already known. Nothing here is claimed as externally novel property testing.

**New relative to repository prior work:** Construct and independently execute an explicit **length-blind, single-pass, one-work-tape, polynomial-time nonlinear decision summary** for exact MCSP at circuit threshold zero, then juxtapose its O(log N) workspace with TMR-4/027's Omega(N) fixed-affine-sketch rank obstruction on the **same** threshold-zero promise problem. This is a concrete hostile control against extending a restricted sketch/transducer lower bound to unrestricted decisions.

## 2. Exact symbolic theorem and finite-alphabet implementation

**Circuit basis:** fan-in-at-most-two AND/OR and unary NOT, zero-gate input wires and constants free, arbitrary fanout. `MCSP_n[0]` on a full N=2^n-bit truth table accepts exactly the two constants and n coordinate projections. Negated input wires are NOT free; a negation is one gate. n>=1. All lengths are handled by **one fixed finite deterministic program**; nonpowers of two and N<2 may be rejected as malformed.

**Theorem ZEROSTREAM28 (PROVED/RESTRICTED, independent audit requested).** The exact language MCSP[0] has a uniform total deterministic implementation with a **one-way read-only input**, **one two-way read/write work tape**, finite work alphabet and control, **O(log N) visited writable cells** and **O(N(log N)^2)** transitions, *without receiving N or n in advance*.

**Proof / explicit transition schedule:** Let j be the zero-based index of the next source bit, maintained in a binary counter. Maintain two 1-bit prefix flags `all0`, `all1`, and a packed vector `alive[i]` for each index bit i that has appeared (0 <= i < bitlength(j)). The invariant after reading bits x_0,...,x_(j-1) is
```
alive[i] = 1 iff for every k<j, x_k = bit_i(k)
all0 = 1 iff all k<j have x_k=0
all1 = 1 iff all k<j have x_k=1.
```
Initially the flags are true and the vector empty. Before processing source coordinate j=2^i, create `alive[i]` initialized to `all0`: on every earlier coordinate k<2^i, bit_i(k)=0. For every active i, set `alive[i] := alive[i] AND (x_j == bit_i(j))`. Update all0/all1 using the same source bit; increment j in binary. No previously observed source bit is reread. At the first right-endmarker, test whether j is a positive power of two at least two; otherwise reject malformed input. Accept iff all0 OR all1 OR any alive[i]. The invariant proves BOTH labels for EVERY valid source at EVERY length.

The counter uses <=ceil(log2(N+1)) bits, and alive has <=ceil(log2 N) bits; all fixed markers/flags add O(1). A fixed finite-alphabet machine can store these adjacent packed bit arrays on its sole work tape. For each input symbol, sweep/shuttle across O(log N) cells to compare and update each of O(log N) alive entries against the counter bit at the corresponding index; conservative bound O((log N)^2) locally moving work-tape transitions per source bit. Binary increment and endmarker power-of-two check fit within this bound. This specifies a finite-alphabet fixed-program compiler, not a free word-RAM operation. Total time O(N(log N)^2), space O(log N), with same-realization charges.

**Robust Gap-MCSP corollary:** Because the algorithm decides the exact YES class, it is also correct on every promised YES/NO input of eta-MCSP[0] for any eta>0 (unpromised inputs may be handled arbitrarily). This is a single program, with no advice, oracle, or threshold-dependent preprocessing. It is not a uniform algorithm for positive growing thresholds s=N^mu.

## 3. An explicit separation of fixed affine sketches from nonlinear streaming

For eta=1/4 and all N=2^n, the full threshold-zero YES class has exactly n+2 tables. TMR-4/027's fixed GF(2)-affine-kernel argument applies to any source-independent linear map A with rank r and any (even unbounded) decoder psi. Writing d=ceil(N/4), V(N,d-1)=sum_(j=0)^(d-1) binom(N,j), exact promise classification demands the necessary condition

$$
2^{N-r} \le (n+2)V(N,d-1).
$$

Otherwise the kernel contains a promised NO word colliding with the zero-table YES. Thus fixed affine sketches require

$$
r \ge N-\log_2(n+2)-\log_2 V(N,d-1)
\ge (1-H_2(1/4))N-O(\log N)=\Omega(N).
$$

The theorem above nevertheless decides the **same threshold-zero ordinary and Hamming-promise questions** with O(log N) physical work cells. Its evolving state is a **nonlinear, source-adaptive summary**, not an affine sketch of all input bits. Therefore the candidate inference `TMR-4 affine rank Omega(N) => every one-way uniform MCSP[0] decider uses Omega(N) space` is **FALSIFIED**. TMR-4's original source-independent theorem is NOT falsified. Likewise the candidate inference `TMR-3 full repeated-table output Omega(N) space => MCSP decision Omega(N) space` is **FALSIFIED** in the threshold-zero setting: full output and one-bit decision are different interfaces.

For **ordinary exact MCSP[0]**, the same affine kernel argument gives necessary r >= N-log2(n+2), again incompatible with a blanket workspace interpretation. TMR-2/026's point-query accepting-branch bound remains correct and is met by our streaming algorithm's N physical bit reads, not evaded.

## 4. Independent peer reviews and precise limits

**TMR-3/026 length-blind padding:** Favorable mathematical audit under the one-way source, no length header, ordered append-only output, and no reread. The common prefix x=01v of a short N-bit and a longer 2^(n')-bit source forces at most R_n output zeros before their first differing input-length test if R_(n')>R_n. On short input, continuation must emit the distinct v-dependent suffix. Output length at that cut has <=R_n+1 choices; combined with full work configurations it yields the published injection bound. No repair required within those explicit assumptions. It **cannot** be transferred to one-bit decisions, as ZEROSTREAM28 illustrates in a restricted MCSP slice.

**TMR-4/027 fixed affine gap kernel:** Favorable elementary rederivation: |C_(n,s)| <= D(n,s), the union of radius-(d-1) Hamming balls has size <=D(n,s)V(N,d-1), and the zero-table kernel has size 2^(N-r); strict inequality produces a far-NO collision. Endpoint decoding cannot separate equal sketches. The strict inequality and eta rounding survive. Source-dependent selectors are still outside the fixed-matrix statement. The decoder's arbitrary cost is irrelevant to this impossibility, but a source-dependent selector can itself encode hardness; its computation must be charged.

**TMR-1/025 approximation padding:** Restrict an approximating (n+t)-input circuit to each dummy-variable slice. Each slice is an n-input size-s circuit; averaging its error proves the claimed reverse inequality. Forward inequality follows by ignoring dummy wires. Same integer s is essential; an ordinary NO below eta may be unpromised after padding. This restricted result survives.

**TMR-2/026 Hamming cylinder:** An accepting deterministic point-query transcript on q distinct coordinates identifies a cylinder of 2^(N-q) completions, all of which must avoid the promised NO set. Covering by Hamming balls gives the reported lower bound. It is a query, not a work-tape runtime result.

**TMR-5/022 permutation frontier:** Its b_c information count remains conditional on actually emitting ordered permuted truth-table bits; the present decider emits one bit only. No contrary evidence for the stated restricted output theorem.

## 5. Primary-source theorem matrix (not transferred across variants)

| Source/version | Exact statement used | Input/model | Threshold/promise | Consequence |
| --- | --- | --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, Theorem 1, p. 23:3, DOI 10.4230/LIPIcs.STACS.2021.23 | For a sufficiently small fixed mu>0, if MCSP[2^(mu n)] not in deterministic DTIME_1[N^1.01], then P!=NP | N=2^n explicit bits, one-way read-only input plus one two-way work tape, **uniform deterministic** | Ordinary exact threshold 2^(mu n) | Conditional magnification |
| Same, Theorem 2, p. 23:3 | For some mu near 1, MCSP[2^(mu n)] not in randomized BPTIME_1[N^1.99] | Same N and physical input/work model, bounded-error randomized | Ordinary exact at a **different** larger threshold | KNOWN restricted lower bound; **does not satisfy Theorem 1** |
| Same, Theorem 3, p. 23:4 | For every 1/2<mu<1, arbitrary oracle with all queries length N^o(1) cannot yield BPTIME_1^O[N^(1+mu')] for some mu'>0 | One-way input, one work tape, arbitrary oracle but **short-query** restriction | Ordinary MCSP[2^(mu n)] | Only excludes short-query oracle construction |
| McKay, Murray, Williams, STOC 2019, original accepted version from MIT repository | Search-MCSP^A admits streaming constructions with small PH-oracle gates; a lower bound on **search/oracle** one-pass poly(s) update and space would imply P!=NP | Search version on N=2^n truth table; one-pass streaming with oracle-augmented output circuits | s(n), PH-oracle circuit interpretation per theorem | Must NOT silently identify search, oracle and ordinary decision MCSP |
| Atserias and Müller, arXiv 2503.24061v2, 2025, Theorem 27 (per TMR-1/025 source inspection) | A distinct uniform magnification result | P-uniform circuit family rather than one-work-tape time, approximate-promise MCSP | Approximation promise and theorem-specific threshold | Concludes P!=NP^(oplus P), **not P!=NP** |

Sources: [CHMY STACS 2021](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2021.23); [MMW STOC 2019 accepted manuscript](https://dspace.mit.edu/entities/publication/d47cf035-39ca-4210-91e8-e5e3051d5deb); [Atserias-Muller 2025](https://arxiv.org/abs/2503.24061). MMW's full theorem details beyond the cited abstract and CHMY's cross-reference were not independently rederived in this run.

## 6. Dependency map, ranking, retirements and remaining gap

1. **Rank 1, OPEN:** Prove directly at the **specific small mu from CHMY Theorem 1** that arbitrary deterministic one-way-input/one-work-tape MCSP[2^(mu n)] algorithms require more than O(N^1.01) time, or construct a charged exact both-label reduction from an already proved large-mu bound that preserves input access and achieves strict exponent slack. This is the shortest surviving conditional route to P!=NP; no current work supplies the premise.
2. **Rank 2, OPEN:** General, source-adaptive threshold-changing transformations, with physically materialized target or online solver composition and exact integer threshold control. Dummy-variable equality alone is not threshold descent; explicit M=N^rho output costs >=M and naive composition needs 1.01 rho<1.99 plus separate reducer slack.
3. **Rank 3, RESTRICTED:** TMR-2 query cylinders and TMR-4 affine gaps give valid information interfaces. Neither transfers to uniform post-acquisition processing lower bounds. Our nonlinear streaming example proves rank counts are not workspace counts.
4. **Rank 4, RESTRICTED:** TMR-3 length-blind padding, TMR-4/TMR-5 permutation frontiers and ring serialization give physical costs of **particular interfaces**. They do not imply a solver must materialize a chosen representation.
5. **RETIRED as invalid transfers:** (i) fixed affine sketch rank => arbitrary decision-space requirement; (ii) full-output padding/permutation space => MCSP one-bit decision space; (iii) positive-threshold hardness from threshold-zero construction; (iv) swapping CHMY large and small mu; (v) ordinary NO => promised eta-far NO without a gap proof; (vi) one-tape single-output communication lower bound => unrestricted multitape SAT lower bound. These are failed implications, **not retractions** of correctly scoped restricted theorems.

Unrestricted P!=NP still requires excluding **every polynomial-time uniform deterministic 3-SAT decider**, all exponents and polynomial workspaces, on encoded source formula length L. This work addresses MCSP source N=2^n and does not supply any SAT reduction with L accounted for. Same-machine S<=O(T) does not turn a threshold-zero toy into the missing small-mu time lower bound.

## 7. Executed reproducibility, publication and peer request

Executed native CPython locally: `experiments/tmr/tmr5_zero_gate_stream028.py`, SHA256 `6e351cee6c7c4d24988a880b832c42ce05c0d5b426e0dc20eefe7dd6408b6cb5`; raw `results/raw/tmr/2026-11-14_1155_TMR5_ZEROGATE_STREAM028_RAW.json`, SHA256 `f355a313b12944c7a159a16abd30f04bc13fded27750cad6c028745e6e9382b1`. Independent direct classifier exhaustively checked **65,812** full truth tables, of which **18 YES** and **65,794 NO**, plus 1,024 seeded random 32-bit tables and 27 malformed-length controls; 3,347,796 candidate-bit comparisons; **zero assertions failed**. This Python implementation is an interpreted *proxy*, not execution of a native finite-alphabet TM; the symbolic tape simulation above is the proof. Previous peer code was inspected via original provenance but not natively reexecuted this run.

**Next single target and peer request:** TMR-2 and TMR-4 should independently implement the binary-counter/live-projection algorithm on a literal finite-alphabet one-work-tape emulator and audit the O(N(log N)^2) upper bound, especially dynamic new-bit initialization. TMR-3 should test whether any genuinely **forced** MCSP small-mu decision subroutine reproduces its output frontier; otherwise retire the output-to-decision implication. TMR-1 should keep the small-mu CHMY threshold exact. TMR-5 should seek a full-label, uniform and physically charged adaptive threshold transfer, not more output-only barriers.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex contains historical TMR-5 region, but these are restricted preliminary synthesis claims pending external peer review; no promotion to canonical or proof trackers. Scheduled tasks untouched. P versus NP OPEN.
