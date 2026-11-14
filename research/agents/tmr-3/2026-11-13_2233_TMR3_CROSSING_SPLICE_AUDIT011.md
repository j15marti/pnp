# TMR-3/011: crossing-configuration splice audit and valid-UNSAT fallback correction

**Pacific date:** November 13, 2026, 22:33 PST. **Role:** NEW TMR-3, Time-Space Tradeoffs. **Status:** CANDIDATE/RESTRICTED mathematical crossing audit pending TMR-5/TMR-1 independent review; finite checks COMPUTATIONAL; literal upper-bound fallback specification FALSIFIED/REPAIRED at dispatch level. Unrestricted all-exponent SAT lower bound and P versus NP OPEN.

## Exact model and theorem under review

One fixed total correct deterministic multitape 3-SAT decider A works for all encoded binary input lengths L. It has one read-only input head moving by at most one source cell per transition, fixed finite control/alphabet, and a fixed number of ordinary locally moving writable tapes. Count all physical transitions T_A(F), and all visited writable tape cells S_A(F) in that **same run**, including copies, indices, cache, stack, parsing, sharing, recomputation, repeated source reads and output. Malformed sources have a total specified classification. No free indexed input, nonuniform advice, oracle, unbounded-word operation or compulsory proof system.

**CS11 fixed-cut injectivity (new explicit audit, CANDIDATE pending peer review).** At one source cut c, suppose an indexed family of equal-length accepted diagonal inputs x(u,u) has the property that literal splicing of the left of x(u,u) and right of x(v,v) produces a valid rejected x(u,v) for every u != v. The ordered *complete physical crossing configurations* at c on accepted diagonal runs must be pairwise distinct.

**Proof.** The source head initially lies left of c. If two diagonal runs had identical complete crossing records, their crossing counts, directions, finite-control states, every visited writable cell and all work-head positions would agree. On the spliced input, follow the left-side segments from the first run and the right-side segments from the second. Segment starts agree exactly with the preceding complete crossing state. Each reads only its chosen side because the input head moves locally. Inductively every segment is legal and the last one halts ACCEPT. That contradicts rejection of the legal mixed input. This is a complete two-way crossing induction, not a one-pass argument.

Each locally moving work head has visited a contiguous finite interval containing its fixed starting position. Given S total visited writable cells, its full configuration, including all symbols, interval endpoints and work-head coordinates, has a binary description of at most b_A(S+1) bits for a fixed machine-dependent b_A. Encode r+1 and S+1 self-delimitingly, then r padded fixed-width complete configurations. The resulting codebook is prefix-free and for r>=1 obeys

$$
\ell_c(F)\le d_A r_c(F)(S_A(F)+1).
$$

The O(log(r+2)+log(S+2)) metadata is absorbed by r(S+1). No unknown T_A is defined as a potential and no time or space from another execution is borrowed.

## Exact original strict 3-CNF splice and conditional product

For the authentic TMR-3/008 batched equality encoding E_{n,m}(a,b), each four-clause bank block uses g=12(w+1) bits, w=max(1,ceil(log_2(5n))), and the full source length is

$$
L=13n+2+2ng,\quad q=\lfloor m/2\rfloor.
$$

At cuts after q completely encoded first-bank blocks and before their corresponding second-bank blocks, fix every outside assignment bit and vary q paired bits. All 2^q diagonals are SAT, while left/right cross-splices for distinct choices are valid UNSAT sources. The new independent executable reconstructed the literal clause bits and checked those splices.

The complete crossing code can therefore be injected into a prefix-free code on these 2^q choices. TMR-3/010's **proved combinatorial** aggregate Kraft lemma then applies to the same input across cuts; the local head crosses at most one cut per physical movement, so sum_c r_c(F)<=T_A(F). This supports the prior candidate same-execution restricted product T_A(F)(S_A(F)+1)=Omega_A(Lm), **subject to independent verification of this full machine/coding audit and source premises**. There is no unconditional all-polynomial-exponent SAT processing lower bound here.

## Concrete defect in the prior upper construction and repair

TMR-3/008 Section 3 directs that on **ANY mismatch** the program invoke an exhaustive 3-CNF fallback, yet it claims a fast upper bound on **every valid** E_{n,m}(a,b). Read literally as an equality-bank mismatch, the claim is wrong. Take a=0^n and b=10^(n-1). This is a correctly encoded, recognized UNSAT family member, so its first paired signs disagree. A literal fallback enumerating all 5n variable assignments must inspect all 2^(5n), rather than the claimed O(L ceil(m/r)) source traversals. The new code really exhaustively checked 32, 1024 and 32768 failing assignments at n=1,2,3.

**Repair:** finish all required structural authentication while retaining a one-bit equal flag. If structural member is true, return SAT iff equal is true, including recognized UNSAT members. Use the fixed exhaustive general solver only when **structural authentication fails**, obeying malformed-source semantics. Premature UNSAT before authentication is unsafe. TMR-3/008's original published source-level recognizer actually returns member=true and sat=false for valid unequal banks: the defect is the *prose dispatch*, not the implemented family classification. The repair preserves O(L ceil(m/r)) charged source-head movement and O(r+log L) source-scan memory. The exact physical finite-tape parser/index-time ledger still requires audit before upgrading the machine-level upper exponent.

## Actually executed independent checks

A new stand-alone hosted-V8/Node-compatible verifier, experiments/tmr/tmr3_crossing_replay011.cjs, independently implements one fixed finite-control, locally moving single-input-head and writable-tape equality machine for strings a#b. It records complete physical work-tape data, head positions, crossing directions and control; codes snapshots self-delimitingly; tests mixed unequal hybrid behavior. It **also independently implements the original strict 3-CNF bank source construction**, rather than calling TMR-3/008's parser.

| Verified quantity | Count |
|---|---:|
| Complete toy-machine decisions | 5,460 |
| SAT / UNSAT decisions | 126 / 5,334 |
| Complete crossing-codebooks / codewords | 27 / 492 |
| Prefix-free pair comparisons | 14,310 |
| Control/head-only projected collisions | **14,310** |
| Actual rejected mixed hybrids | 14,310 |
| Strict original CNF splice comparisons | 27,612 |
| Opposite-label legal CNF splices | 21,826 |
| Distinct original CNF source cuts | 1,533 |
| Exhaustive UNSAT fallback assignments | 33,824 |
| Failed assertions | **0** |

Every control/head-only crossing pair collided while its **full writable tape contents** differed. This is an explicit falsifier of using incomplete crossing states for prefix indistinguishability. The true mixed-source physical machine rejects. The same tests were separately written and executed in **native Python** with identical principal counters. Python is local-only; the exact published JS and its raw JSON were executed in hosted V8. Neither is a universal SAT Turing machine and all finite evidence is COMPUTATIONAL. Parameters: exhaustive lengths n=1..6 for toy decisions, n=2..7 for crossing q, n=2..6 and 2<=m<=n for exact strict-CNF splices. Deterministic, no random seed.

Published [code](https://github.com/j15marti/pnp/blob/main/experiments/tmr/tmr3_crossing_replay011.cjs) and [raw JSON](https://github.com/j15marti/pnp/blob/main/results/raw/tmr/2026-11-13_2233_TMR3_CROSSING_REPLAY011_RAW.json).

## Exact exponent and model-transfer firewall

For m=Theta(n^alpha), 0<alpha<=1, and L=Theta(n log n), the restricted product has order

$$
\Omega_A\left(L^{1+\alpha}/(\log L)^\alpha\right).
$$

It excludes only simultaneous exponent pairs k+s<1+alpha for T=O(L^k), S=O(L^s) on this source family. No pair with k>=2, s>=0 is excluded. Same-machine S<=O_A(T+1) yields merely a square-root time consequence, weaker here than compulsory Omega(L) local source traversal. Source copying consumes O(L) time and O(L) writable memory and may eliminate any post-acquisition difficulty. TMR-1/012's multi-head copy bridge is all-exponent **time** preserving but not small-space preserving.

Required hostile alternatives remain admissible: Horn and 2-SAT, Gaussian elimination on XOR/Tseitin, bounded-treewidth DP, disjoint products, compact algebraic representations, sharing, clause reordering, padding, auxiliary variables, indexed input, caching, rereads and recomputation. These separate algorithms were **not executed** in this run. Source-local cross-sequence bounds do not transfer directly to alternate encodings or random access. TMR-5/009's correlated Kraft construction was independently verified symbolically as coefficient-sharp for marginal codebooks: failure probability 2^(-t)-2^(-q) against delta=2^(-t)(1+2^(-q)) and ratio approaching one as q grows. It does not instantiate a physical SAT crossing transcript. Relativization, algebrization and Natural Proofs remain barriers to audit as relevant, not impossibility theorems for this candidate.

## Primary sources, original corpus and status

Primary records checked: F. C. Hennie (1965), [crossing sequences](https://ntrs.nasa.gov/citations/19660035639), model ancestry only; Fortnow, Lipton, van Melkebeek and Viglas (2005), JACM 52(6), [SAT time-space](https://doi.org/10.1145/1101821.1101822), random-access small-space exclusions rather than arbitrary polynomial workspace; Borodin and Cook (1982), [sorting time-space](https://doi.org/10.1137/0211022), different output task. This report's full-state splice proof is direct, not inferred from those different models.

Read FIRST the authoritative 12:49 PST TMR replacement directive, SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Both trackers recovered: proof1 complete 28,714 chars, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 complete *authentic Git blob* 1,051,196 chars, SHA 930c5eeddafce656717f28055a7a9a755f44737c (ordinary fetch returned blank, **not** an empty file). Canonical root main.tex complete authentic Git blob 2,511,782 chars, SHA c04a02a97492f88938791f363ff91d99b67cd78b; AGENTS.md, CODEX.md, research skill, issue #3, newest five peer handoffs and relevant originals TMR-3/002,/008,/009,/010, TMR-1/012, TMR-2/012 and TMR-5/009. Old LSPV allocation superseded, historical mathematical evidence preserved.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex untouched for TMR-5 synthesis and independent status review; no task/schedule changed. Local repo preflight/LaTeX compilation unavailable because network clone failed, although actual independent native Python and hosted V8 experiments ran. All unresolved computational-processing arrows and **P versus NP remain OPEN**.

**One next target:** TMR-5 independently inspect the full-state splice and its self-delimiting serialization, check the recognized-UNSAT dispatch repair, then derive or falsify a cost-sound post-source processing lower bound under arbitrary polynomial work space.

END_OF_REPORT::TMR3::CROSSING_SPLICE_AUDIT011::2026-11-13_2233_PST
