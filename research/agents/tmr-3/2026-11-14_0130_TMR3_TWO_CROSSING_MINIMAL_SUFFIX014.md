# TMR-3/014: two crossings per cut suffice for global future dependence at linear time and zero workspace

**Time:** November 14, 2026, 01:30 PST (America/Los_Angeles). **Role:** NEW TMR-3 Time-Space Tradeoffs. **New claim:** TMR3-2C14, CANDIDATE/RESTRICTED pending independent TMR-5 or TMR-1 audit. **Native finite verification:** COMPUTATIONAL. **General 3-SAT time lower bound and P versus NP:** OPEN.

## 1. Exact machine model and reason for this test

Fix a finite total deterministic multitape decider A for binary-encoded 3-CNF, one locally moving read-only source head initially on the left endmarker, finitely many locally moving writable tapes and fixed finite alphabet/control. Let the source hold exactly L bits at cells 1 through L, with endmarkers at cells 0 and L+1. Every input-head move costs one transition; S is the peak number of visited writable cells; finite control is fixed independently of L. A correctly classifies SAT, UNSAT and malformed encodings for every L. The complete output and all original A steps are charged.

TMR-3/013 and TMR-5/012 give correct *conditional prefix-free coding* bounds with concentration exponent controlled by maximum future-interval overlap D. Those theorems do not assert that physical crossing records of arbitrary correct two-way SAT machines have sublinear D. TMR-2/015 has just exhibited a physically charged parity roundtrip with two **or four** crossings per original cut depending on global parity. This run independently audits that idea, strengthens it to **exactly two** preprocessing crossings per cut on **every** input, and proves a sharp single-head one-versus-two crossing threshold. On an unbounded genuine 3-CNF subclass, the *entire decision computation* also uses exactly two crossings per cut and zero writable work cells.

## 2. The uniform two-crossing wrapper (CANDIDATE pending peer review)

**Claim TMR3-2C14(A).** For each *one fixed* eligible correct A, construct *one fixed* uniform correct B_A over all input lengths by:

1. Starting with all A work tapes blank and all original input heads at their initial positions, use the designated input head to sweep physically right from left marker 0 to right marker L+1. At each data cell, update one parity bit P and one last-read-bit register in **finite control**.
2. Physically sweep the same head all the way left to marker 0, retaining final P in finite control. Leave all original A work tapes untouched; any other original input heads remain at their initial positions.
3. Enter A's initial control and run A unchanged to its correct SAT/UNSAT/malformed terminal.

The outward scan costs exactly L+1 local transitions; the return costs exactly L+1. On this declared transition convention no separate state-entry transition is necessary. Therefore, for **the same** original source x,

$$
T_{B_A}(x)=T_A(x)+2(L+1),
\qquad
S_{B_A}(x)=S_A(x).
\tag{2C14-1}
$$

This composition neither changes labels nor hides an input copy, address register, lookup table, oracle, preprocessing computation or extra writable cell. A itself may use arbitrary polynomial workspace and any algorithm, including Gaussian elimination, Horn propagation, 2-SAT implication, bounded-treewidth DP, arbitrary sharing, caching, source rereads and recomputation. Neither polynomial runtime of A nor a particular proof calculus is assumed.

For each cut i immediately **after** data cell i, 1<=i<=L, the designated preparatory scan crosses from left to right exactly once and from right to left exactly once, independent of parity or source label. The outward crossing control contains x_i as the last scanned bit; the return crossing control contains P(x). Thus a *physically obtained projection* of the two tagged, ordered actual crossing records is

$$
c_i(x)=(x_i,P(x)),\qquad
P(x)=\bigoplus_{j=1}^{L}x_j.
\tag{2C14-2}
$$

For any choice of all outside bits, varying x_i produces two different codewords of fixed length 2. Hence the conditional map x_i -> c_i is injective and prefix-free. Every later x_j with j>i genuinely influences the second tag, even though the count at **every** cut remains exactly two. With L independent free bits and horizons measured in their physical order, the *minimal permitted* horizons for these actual projections are R_i=L, and the future-dependence intervals [i,L] have

$$
D=\max_j|\{i:i\le j\le L\}|=L.
\tag{2C14-3}
$$

If a standard clause/identifier encoding is used instead, vary only K original sign-bit fields and keep its parsing structure fixed. The identical construction gives D=K for those fields without changing the all-input correctness of B_A. This does NOT prove that the complete crossing-sequence *serialization* is prefix-free or satisfies a SAT splice lemma. It falsifies only a structural inference from physical local access, two crossings, read-only input and independently variable source signs to sublinear **future dependence**.

**Minimality in number of crossings, single-head model.** Assume a head starts left of cut i and each run in a pair of sources with the same prefix through i makes **at most one** crossing of i. Before that first left-to-right crossing, its computation cannot inspect any bit strictly to the right of the cut, because only this source head reads original input and it moves locally. Determinism therefore makes the crossing state identical on the paired inputs. If exactly one crossing is recorded on both, their complete crossing records cannot distinguish suffixes. Thus at least a second crossing is required for the *same cut's actual crossing transcript* to depend on unseen suffix information, unless an additional head, nonlocal port or uncharged source copy is introduced. Construction (2C14-2) attains two. This is an exact restricted access statement, not a lower bound on general SAT decision time.

## 3. Stronger restricted control: the entire correct SAT decision uses two crossings

Consider the infinite sign-stream encoding of proper three-literal clauses over the **fixed three variables** x0,x1,x2. Every consecutive three source bits specifies the signs of (x0,x1,x2); equivalently the three-bit pattern specifies the unique assignment that falsifies that clause. All source bitstrings of length L=3r (r>=0) are syntactically valid; lengths not divisible by three are MALFORMED.

A fixed finite-state classifier needs only a three-state mod-3 counter, a <=3-bit partial clause buffer, and an eight-bit *constant-width* mask of the forbidden assignments. It sets one mask bit for each finished clause. It returns UNSAT iff all eight assignments are forbidden, SAT otherwise, and MALFORMED on an incomplete terminal triple. It is correct for **every** r, including arbitrarily large r, and needs zero visited writable cells. The 8-bit mask is finite control, not an unbounded word or length-dependent advice.

During **the very same first outward physical scan** it simultaneously computes the finite-state 3-CNF label and P. During the sole return scan it retains both. On returning to the left marker it halts with the correct label in one additional transition. Consequently, for every binary source x,

$$
T_C(x)=2(|x|+1)+1,\qquad S_C(x)=0;
$$

and on every valid r-clause source its **complete** original-input crossing record has exactly two crossings at each data-cell cut. This machine decides both SAT and UNSAT correctly within that subclass (all eight distinct patterns gives UNSAT; repeated patterns missing one assignment give SAT), at **linear** time and **zero writable space** for unbounded lengths. Its two-crossing projection (2C14-2) has D=L. Thus even a *complete*, rather than preparatory, two-crossing decision trace can exhibit maximal future dependence without a space-time obstruction. The subclass is not NP-complete and the classifier is not an all-variable 3-SAT algorithm.

An arbitrary general correct A is still covered by the uniform wrapper in Section 2; that wrapper's **prepass** crossings are exactly two but any later A simulation may add crossings. These two statements have distinct scopes and must not be conflated.

## 4. Independent native execution and hostile controls

The exact published standalone CPython file was executed **natively in the OS container**, not a JavaScript wrapper. It simulates a locally moving original-input head at positions 0..L+1, records each prepass edge/cut and the two actual finite-control tags, and *integrates* the eight-mask correct decision classifier into the outward sweep. A second, independently coded brute-force three-variable evaluator compares labels on short inputs.

| Executed check | Count |
|---|---:|
| Exhaustive binary strings of lengths 0 through 15 | 65,535 |
| All permutations of eight clause masks (genuine UNSAT) | 40,320 |
| Source-suffix bit flip/cut comparisons | 6,096 |
| Actual charged prepass head transitions | 3,989,618 |
| Actual forward/backward cut events | 3,777,866 |
| Observed assertion failures | 0 |

Additionally, valid SAT and long fixed-three-variable controls used 8, 9, 16, 64 and 1,024 clauses; all have charged local scans and zero modeled writable cells. Counted classifications were SAT 37,470, UNSAT 40,320 and MALFORMED 28,086. Every data-cell cut in every run was crossed exactly twice; both-label and malformed terminal classifications passed. No random samples or unreported random seeds were used. The reported physical model is a finite-state head simulator for the restricted language, **not** a compiler execution of an arbitrary 3-SAT Turing machine. All finite results are COMPUTATIONAL; the universal transformation and minimality argument above are symbolic CANDIDATE claims until independent peer review.

**Executed, exact byte-readback code:** [experiments/tmr/tmr3_two_crossings014.py](https://github.com/j15marti/pnp/blob/main/experiments/tmr/tmr3_two_crossings014.py), blob 5f830dda0c9750e6f83331f9168c9fcf13abad82.

**Immutable machine-readable results:** [results/raw/tmr/2026-11-14_0130_TMR3_TWO_CROSSINGS014_RAW.json](https://github.com/j15marti/pnp/blob/main/results/raw/tmr/2026-11-14_0130_TMR3_TWO_CROSSINGS014_RAW.json), blob 90ecc1ee5b6d404cf1cb487cc8c3bf68891da249.

Native runtime was about 1.44 s. No repo-wide preflight, XeLaTeX build, physical compilation of arbitrary A, OS-native Node, or independent peer implementation was executed. No finite test is presented as asymptotic proof.

## 5. Exact boundaries, primary sources, literature, corpus and status

**Prior corpus reconciled:** current TMR replacement directive, both root proof trackers (proof1 complete 28,714 characters; proof2 recovered by Git blob, 1,051,196 characters), root canonical main.tex recovered by Git blob, root AGENTS.md/CODEX.md, repository pnp-research SKILL.md, latest issue #3 through TMR-2/015, latest five TMR handoffs, original TMR-3/011-013, original TMR-2/015 and TMR-5/012. TMR-2/015 already found global parity-dependent **2/4** crossings on the same uniform machine; the distinct new strengthening here is **exactly two for every source**, the elementary sharp one-versus-two threshold, and an entire **unbounded zero-workspace/linear-time** SAT-subclass decision with exactly two total crossings. Historical ARC/FLMV/crossing results remain restricted and unchanged. Root trackers are **TRACKERS REVIEWED; NO MATERIAL CHANGE**. Canonical main.tex is left to its TMR-5 synthesis owner; no scheduled tasks are touched.

**Primary literature checked for its actual scope:** F. C. Hennie, "Crossing Sequences and Off-Line Turing Machine Computations," 1965 FOCS proceedings, NASA archival metadata https://ntrs.nasa.gov/citations/19660035639 (locally moving tape crossing methodology; not a general multitape 3-SAT lower bound); Fortnow, Lipton, van Melkebeek and Viglas, "Time-Space Lower Bounds for Satisfiability," *Journal of the ACM* 52(6), 835-865, 2005, https://doi.org/10.1145/1101821.1101822 (specified n^c time with restricted n^d space on random-access machines, rather than all polynomial-time/space pairs). Neither paper is claimed to contain TMR3-2C14 or to prove P != NP.

**Hard restrictions surviving:** This construction does not refute TMR-5/012's mathematically valid ID12 inequality, since its genuine two-pass code projection has D=L and yields only the K-free tail exponent. It does not refute an injective full-crossing-sequence splice lemma for a specially arranged SAT source family. An algorithm-specific **normalizer** may discard the intentionally unnecessary parity register or derive a stronger charged invariant; its correctness and cost-soundness must be proved, not assumed. Full-crossing information cannot automatically be converted into compulsory post-input *processing*. TMR-4's total-trace cost-sound Bellman obligations and TMR-1's unrestricted-machine all-exponent target remain OPEN.

The target remains: for every fixed correct total all-length A and all k>=1,C>0,L0, find some valid formula F of bit length L>=L0 with T_A(F)>C(L+1)^k. This report excludes no such hypothetical polynomial A. S_A(F)<=O_A(T_A(F)+1) is a same-run upper bound, not a lower bound. Neither ETH/SETH nor oracle, nonuniform program, restricted solver portfolio, prescribed DAG, proof system, or uncharged encoding is assumed.

**Next one target for TMR-5/TMR-4:** Determine whether any cost-sound, **phase-independent canonical crossing descriptor** can discard the global parity register while preserving all source-splice distinguishability and a full-execution charging theorem, and whether a useful conditional Kraft moment bound survives that normalization. Test the full restricted machine above and arbitrary-A compositions before claiming D=o(K). General SAT superpolynomial processing remains OPEN.

END_OF_REPORT::TMR3::2C14::2026-11-14_0130_PST
