# TMR-3/008: A tunable, same-machine time-space law from clause-block locality

**Date:** November 13, 2026, 19:35 PST (America/Los_Angeles).
**Repository:** j15marti/pnp, main. **Role:** NEW TMR-3 Time-Space Tradeoffs.
**Status:** CANDIDATE mathematical theorem pending independent TMR-5/TMR-1 proof audit; exact source-level finite checks COMPUTATIONAL. All unrestricted 3-SAT superpolynomial lower-bound arrows and P versus NP OPEN.

## 1. New scoped theorem and exact quantifiers

For each n>=1, let a,b belong to {0,1}^n. Use the original TMR-3/002 explicit proper 3-CNF equality gadgets, with unary header H_n, four-clause first-bank block B_i^0(a_i), and four-clause second-bank block B_i^1(b_i). Define a *batch-ordered* source for any integer 1<=m<=n:

$$
E_{n,m}(a,b)=H_n\prod_{j=0}^{\lceil n/m\rceil-1}
\left(\prod_{i=jm}^{\min(n,(j+1)m)-1}B_i^0(a_i)\right)
\left(\prod_{i=jm}^{\min(n,(j+1)m)-1}B_i^1(b_i)\right).
$$

All products are concatenation in increasing i order. This is the EXACT original clause multiset: no rewriting, auxiliary variables, padding, identifier changes, or changed clause signs. Its answer is SAT iff a=b. The bit length is independent of m:

$$
w_n=\max(1,\lceil\log_2(5n)\rceil),\quad
g_n=12(w_n+1),\quad
L_n=13n+2+2ng_n=\Theta(n\log(n+1)).
$$

**TMR3-BATCH8 candidate crossing product.** Let A be ANY ONE fixed finite total correct deterministic SAT decider, with a single read-only *locally moving* input head, finitely many ordinary locally moving writable work tapes, fixed finite control/alphabet, and no free indexed input jumps. Time is ACTUAL transitions, and space is peak writable work cells visited on the SAME run, including buffers, stacks, indices, retained bits, recomputation and output. There exist c_A>0 and n_A such that

$$
\forall n\ge n_A\;\forall m\in\{1,\ldots,n\}\;
\exists a\in\{0,1\}^n:\quad
T_A(E_{n,m}(a,a))\bigl(S_A(E_{n,m}(a,a))+1\bigr)
\ge c_A L_n m.
\tag{BATCH8-LB}
$$

No bound is imposed on A's work space or number of input rereads. The hard a can depend on A,n,m. It is a SAT diagonal input. This is a quantitative *sequential-source-transport* restriction, not a lower bound for random-access, multi-input-head, or alternative source-encoding models. New contribution beyond original TMR-3/002 (m=n) and TMR-3/007 (m=1) is a continuous batch-locality parameter and its simultaneous-resource lower/upper envelope.

## 2. Proof attempt, including the same-execution quantifier

**(a) End-of-source necessity.** For every accepted diagonal E_{n,m}(a,a), change all four common signs in the very last second-bank block to the opposite forcing bit. The result is another well-formed, same-length UNSAT equality source, identical outside the last g_n bit cells. A correct deterministic A must visit at least one of these changed cells on its original accepted run, or would incorrectly accept the opposite source with the identical observed transcript. Since the sole input head starts at the left end and moves locally, T_A(E_{n,m}(a,a))>=L_n-g_n>=L_n/2. Every selected source cut before the last block is crossed at least once.

**(b) Physical cut family.** Consider each FULL batch of m blocks. Select all source-cell boundaries inside the SECOND HALF of its first-bank m blocks. At least floor(m/2) whole first-bank blocks precede every selected cut; ALL corresponding second-bank blocks lie on the right. There are at least floor(m/2)g_n-1 such cuts per full batch. For each cut c, fix all remaining equality bits and vary only q=floor(m/2) fully completed left-bank variables. Splicing the left source of one SAT diagonal with the right source of another gives EXACTLY a valid E_{n,m}(a,b) with a mismatch whenever the varied q-bit vectors differ. A cannot accept that hybrid.

**(c) Complete crossing record.** For an accepted diagonal input F, record at each actual crossing of c the entire instantaneous controller state, all visited writable tape symbols, each work-head position, the input-head direction and the crossing order. The fixed c determines the input-head coordinate. With peak writable cells S=S_A(F) and r_c>=1 crossings, these records and their count have a prefix-free serialization of length

$$
\ell_c(F)\le d_A\,r_c(F)\,(S_A(F)+1)
\tag{CODE}
$$

for a fixed machine-dependent d_A. One explicit method encodes S and r_c as self-delimited integers, followed by r_c padded fixed-width full configurations. A local-head work tape cannot have a huge unvisited address: positions are bounded by the interval of visited cells. Thus the complete record uses O_A(S+1) bits; log(S+2) and log(r_c+1) metadata are absorbed because r_c>=1. No input bit, work-tape state, long counter, shared buffer or read access is discarded.

If two different q-bit values with the remaining input bits held fixed had identical crossing records, the standard deterministic cut-and-paste induction would accept their mismatched legal hybrid: at each crossing the full writable configuration and control are identical, so the next segment on its respective side behaves identically. This contradicts correctness for both labels. Hence the prefix-free crossing-code map is injective on all 2^q SAT diagonals in this conditional subfamily.

**(d) No per-cut witness borrowing.** Choose a uniformly random a in {0,1}^n, and let F_a=E_{n,m}(a,a). For each selected cut c, condition on the fixed bits outside its q crossing variables. Since the code is prefix-free and injective over the 2^q choices,

$$
\Pr_a[\ell_c(F_a)<q/2]\le 2^{-q/2}.
$$

When m>=16, q>=8 and the GOOD probability is at least 15/16. On GOOD, (CODE) implies r_c(F_a)(S_A(F_a)+1)>=q/(2d_A). Therefore

$$
\mathbb{E}_a[r_c(F_a)(S_A(F_a)+1)]
\ge \frac{15q}{32d_A}.
$$

Take the sum across cuts and batches INSIDE the expectation. A single physical head movement crosses at most one source boundary, so for every a, sum_c r_c(F_a)<=T_A(F_a); this is SAME INPUT, SAME MACHINE, SAME TIME AND SPACE, not a sum of separate per-cut worst-case examples. Each full batch contributes Omega_A(m^2 g_n). Since floor(n/m)*m^2>=nm/2, some single a satisfies

$$
T_A(F_a)(S_A(F_a)+1)=\Omega_A(nmg_n)=\Omega_A(L_nm).
$$

For m<16, the endpoint necessity T>=L_n/2 already implies T(S+1)>=L_nm/32. This covers all m uniformly. The proof uses only total both-label correctness and one physical source head; no assumed sweep pattern, fixed representation, fixed workspace cap, or prescribed arithmetic solver.

**Review status:** This is a self-contained proposed crossing-sequence argument, not a literature theorem or independently reviewed proof. TMR-5 must check the exact source cut and splice, prefix-free code length at variable actual S, last-block distinguishability, whole-execution crossing charge, and uniform constants before promotion.

## 3. Matching charged upper and exact exponents

For any fixed rational 0<=beta<=alpha<=1, define t=floor(log2 n), m(n)=2^floor(alpha*t), r(n)=2^floor(beta*t). The exponents are part of ONE FIXED machine program, not length-dependent advice. The unary input header supplies n; standard charged binary registers compute m,r using O(log L_n) cells and O(polylog L_n) setup time.

Construct one total all-input correct machine D_{alpha,beta}:
1. Authenticate the complete canonical batched source, both signs and IDs, using ONE adjacent-moving input head. Within each batch of size z<=m, repeat ceil(z/r) scans of its 2zg source bits. In each scan cache at most r selected first-bank signs, compare with the corresponding second-bank signs, and rewind locally for the next scan. ALL other source bits are also authenticated, and the final endmarker is checked.
2. Charge each ordinary input-head movement, local rewind, tape-cache read/write, signed-gadget verification, finite-control operation, address counter and comparison. On a valid family member, the total reads and local moves are O(L_n ceil(m/r)), while total simultaneously live writable space is O(r+log L_n). No unbounded-word operation is unit-cost.
3. On ANY mismatch, rewind by paid adjacent source moves and invoke one fixed, total, correct exhaustive 3-CNF parser/decider on ALL other sources including malformed ones. This may take exponential time off family. It ensures uniform all-input correctness without asserting a general polynomial SAT algorithm.

Consequently, for EVERY valid E_{n,m(n)}(a,b), on the SAME D execution,

$$
T_D=O(L_n\lceil m/r\rceil),\quad
S_D=O(r+\log L_n).
\tag{BATCH8-UP}
$$

For alpha>0 and beta=alpha, this is O(L_n) time with O(n^alpha+log L_n) space and matches (BATCH8-LB) to constant factors when n^alpha dominates log n. More generally, for beta>0 the product matches the lower bound within constant factors: O(L_n m). For beta=0 the upper product has an extra O(log L_n), attributable to charged parsing/index counters. Cases m=n and m=1 recover the earlier grouped and interleaved endpoints.

When m=Theta(n^alpha),

$$
L_nm=\Theta\!\left(\frac{L_n^{1+\alpha}}{(\log L_n)^\alpha}\right).
$$

Thus (BATCH8-LB) excludes proposed **uniform simultaneous** bounds T=O(L^k), S=O(L^s) on this restricted encoded family only when k+s<1+alpha. It excludes no polynomial-time algorithm with sufficiently large polynomial workspace, and cannot exclude all k. Same-machine S<=O(T) yields merely T=Omega(sqrt(Lm)), weaker than the compulsory physical traversal T=Omega(L), since m<=n. For h>=2 local input heads or indexed-input access, the crossing proof does NOT transfer; earlier TMR-3/006 and TMR-1/005 give cheap fast paths.

## 4. Actual executed computational evidence

**Native Node v22.16.0, exact original JavaScript** at experiments/tmr/tmr3_batch_crossing008.cjs, and a separately executed hosted V8 rerun of the exact published source. Raw results at results/raw/tmr/2026-11-13_1935_TMR3_BATCH_CROSSING008_RAW.json. Deterministic seed 0x3b71c008; exhaustive n=1..4 over ALL a,b; seeded n=8,16,32,64,128,256; block sizes 1,2,floor(sqrt n),floor(n/2),n; cache sizes 1,floor(sqrt m),m.

- 2,468 valid parse-and-answer variants, 223 SAT and 2,245 UNSAT; 1,232 exact whole-clause-multiset and original-block permutation checks.
- 1,236 runs with cache smaller than the batch; 40 exhaustive original-CNF satisfying-assignment checks; 4,928 malformed/structural rejection controls.
- 677,552,068 modeled adjacent input-head movements including 331,481,280 charged local rewind movements; 346,073,256 source-read events; 30,204 complete batch scans; 55,404 cached-bit comparisons.
- Largest L=77,058 bits; largest cache=256 bits; zero failed assertions.
- Independent spot-check from native Node on n=256, L=77,058: batch m=16, r=1 uses 2,288,898 input movements; m=16,r=16 uses 77,058; m=256,r=1 uses 37,678,338; m=256,r=256 uses 77,058. This is exact source-level movement accounting, NOT a finite-alphabet physical TM step trace.

The source emulator uses JavaScript strings, arrays and host-number arithmetic; the stated TM implementation/running-time guarantee is a separate symbolic argument. It does not execute the exponential all-input fallback, a full physical transition table, Horn/2-SAT/GF(2)/bounded-treewidth generic solvers, or formal proof checking. Those inputs are handled by the logically specified fallback, not measured here. The measured movement count is NOT the total physical transition count.

## 5. Primary literature and original historical scope

[1] F. C. Hennie, "One-tape, off-line Turing machine computations," Information and Control 8 (1965), 553-578, DOI https://doi.org/10.1016/S0019-9958(65)90399-2. Historical crossing-sequence ancestry. The multiple-work-tape/full-configuration charged lemma is derived above, NOT imported unproved from a restricted one-tape theorem.

[2] L. Fortnow, R. Lipton, D. van Melkebeek, A. Viglas, "Time-Space Lower Bounds for Satisfiability," Journal of the ACM 52(6) (2005), 835-865, DOI https://doi.org/10.1145/1101821.1101822; original author manuscript https://lance.fortnow.com/papers/files/tst.pdf, Sections 1 and 2.1 inspected, including page 4 facsimile. Model is random-access Turing machines, with index tapes erased on use; for each c below the golden ratio, a suitable small positive d excludes simultaneous SAT time n^c and space n^d. This does not establish unrestricted all-polynomial-time SAT hardness or transfer our sequential-head geometry to INDEX.

[3] A. Borodin, S. Cook, "A Time-Space Tradeoff for Sorting on a General Sequential Model of Computation," SIAM Journal on Computing 11(2) (1982), 287-297, DOI https://doi.org/10.1137/0211022. Their input/output task is sorting, not SAT; no theorem transfer is asserted.

[4] ORIGINAL project evidence: research/agents/tmr-3/2026-11-13_1434_TMR3_TWOWAY_CROSSING_TRADEOFF002.md (m=n original grouped theorem candidate); research/agents/tmr-3/2026-11-13_1828_TMR3_CLAUSE_ORDER_LOCALITY_ESCAPE007.md (m=1 exact reordering escape); experiments/tmr/tmr3_interleaved_clause_order007.cjs and its raw data. Original historical crossing/averaging: research/agents/lspv-5/2026-10-26_1648_LSPV-5_CROSSING_AVERAGE_QUANTIFIERS167.tex. This run is a parameterized interpolation with same-trace average counting, not a claim to invent crossing sequences.

**Preflight:** replacement directive first and rechecked SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1.txt full 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2.txt recovered full authentic 1,051,196-char Git blob SHA 930c5eeddafce656717f28055a7a755f44737c; main.tex recovered full authentic 2,502,146-char Git blob SHA 62c0c400a5eddfbdbdfa06fbabcf7bcee8b753be (ordinary file bodies were misleadingly blank); AGENTS.md, CODEX.md, research skill, latest issue #3, all five newest TMR handoffs, original relevant TMR-3/002,/006,/007 and FLMV Section 2.1 consulted. This batch result does not replace the general resource proof. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No canonical main.tex edit (TMR-5 synthesis owner), no new main.tex and no schedule or agent changes.

**ONE NEXT TARGET:** TMR-5 independently review BATCH8-LB crossing-code injectivity and SAME-TRACE averaging, then investigate any compulsory post-acquisition work surviving favorable batch m=1, two input heads, INDEX, compact GF(2), sharing, and arbitrary polynomial workspace. The all-program all-polynomial-exponent implication stays OPEN.

END_OF_REPORT::TMR3::BATCH_CROSSING008::2026-11-13_1935_PST
