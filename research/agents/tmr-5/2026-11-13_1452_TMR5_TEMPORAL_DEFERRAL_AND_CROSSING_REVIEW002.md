# TMR-5 / TEMPORAL-DEFERRAL-AND-CROSSING-REVIEW002

**Research timestamp:** 2026-11-13 14:52 PST (America/Los_Angeles).  
**Owner:** TMR-5, new machine-bottleneck red team and canonical synthesis, j15marti/pnp main.  
**Status:** TMR-4/003 independently reviewed as **PROVED/RESTRICTED** for the stated declared-length binary input grammar; TMR-3/002 independently reviewed as **PROVED/RESTRICTED** for sequential-head, fixed-tape machines; new TMR5-SF2 strengthening **CANDIDATE pending TMR-1/4 second mathematical review**; finite testing **COMPUTATIONAL**; unrestricted superpolynomial SAT time bound **OPEN**; P versus NP **OPEN**.

## 1. Exact targets and adversarial falsifiers

**Target A:** Verify or disprove TMR-4/003's claim that obligatory computational work cannot be localized to the interval strictly after all original input bits have first been observed. Seek a repaired time-order-independent resource obligation.  
**Target B:** Independently examine TMR-3/002's claimed same-input, two-way sequential-head crossing lower bound, especially its fixed-suffix splicing and union over cuts.

Falsifiers declared before final review: (F1) the input length is not known before the final source coordinate; (F2) the two final-bit completions can have different SAT labels, requiring actual computation of both; (F3) virtual simulations require an uncharged oracle or nonuniform advice; (F4) malformed/overlong inputs or valid-only runtime assumptions invalidate totality or polynomial preservation; (F5) a crossing splice is not a well-formed original strict 3-CNF; (F6) crossing records omit mutable state or combine space on one input with time on another; (F7) crossing lower bounds silently transfer to indexed access or all polynomial time exponents.

## 2. Formal model, grammar and quantifiers

One fixed finite deterministic machine has one two-way, physically sequential read-only source head, finitely many work tapes of fixed finite alphabets and a finite controller. Input-head and work-head movements are at most one position per charged transition. All work-tape symbols, head positions, buffers, counters, simulated tape contents, index construction, table lookup, source re-reads and output steps are counted in physical time or visited writable work cells. The machine is total, rejects malformed encodings and accepts precisely satisfiable valid encodings.

The project's strict-proper signed binary 3-CNF grammar has two unary count headers, $1^N0\,1^M0$, then $3M$ sign/index literal records of width $1+w$, where $w=\max(1,\lceil\log_2N\rceil)$. Valid formulas have $N\ge3$, $M\ge1$, in-range literal indices and three distinct variables per clause. The declared complete bit length is

$$
K=N+M+2+3M(1+w).
$$

In particular, the two header delimiters are observed before the final literal bits. The machine can calculate $K$ using only a proper physical prefix, without external length advice.

## 3. Independent TMR-4/003 audit: genuine final-bit deferral

**Reviewed theorem (PROVED/RESTRICTED).** For every fixed total correct deterministic 3-SAT decider $A$ in this model, there exists one fixed total correct decider $B_A$ and constant $c_A$ such that on *every valid declared-length input* $x$, if $\tau_{B_A}(x)$ is the first transition in which the last previously unseen physical source coordinate is observed, then

$$
T_{B_A}(x)-\tau_{B_A}(x)\le c_A.
$$

Construction and full accounting:

1. Read the unary header, compute $K$, and copy physical prefix $p=x[0:K-1]$ onto work tapes. Halt or invoke a complete charged fallback for malformed/truncated header and prefix cases. Do **not** read the physical cell $K-1$ while computing.
2. Store virtual work-tape inputs $p0$ and $p1$ and execute the *fixed program $A$* on both to termination by a direct ordinary machine simulation. All simulation transitions and cells are charged. Store the two outputs in finite control. No oracle, witness or nonuniform table is supplied.
3. Read physical bit $b=x[K-1]$, verify the next physical position is the endmarker, and halt with stored output $A(pb)$. If the physical input is overlong, invoke the charged total fallback. The number of transitions from the final previously unseen input bit to output on valid strings is bounded by a machine-dependent constant.

Because $A$ is correct on the real valid string $pb$, the selected label is correct even when the unused completion has the opposite label. Two virtual runs are finite because $A$ is total. This proves the time-phase counterexample without assuming $A$ is polynomial. If a polynomial bound for $A$ is assumed on **all strings**, this fixed wrapper also has polynomial time on valid strings. More generally, if $A$ is polynomial *only on valid strings*, the wrapper first parses each virtual completion and runs $A$ only on valid completions, rejecting the invalid ones in polynomial time; thus the conditional polynomial-preservation statement is still sound. This extra validation is required and cannot be omitted under a valid-only runtime hypothesis.

The exact opposite-label control is valid: force $x_0=1$, $x_1=0$, $x_4=1$, $x_5=0$ using four proper three-distinct-variable unit-gadget clauses per forced variable and fresh auxiliaries 6 through 13. With $N=14,M=17,w=4$, append $(\neg x_0\lor x_1\lor x_j)$, where $j=4$ yields SAT and $j=5$ yields UNSAT. Indices 0100 and 0101 differ only in the final encoded bit. Thus the theorem is not exploiting an irrelevant last bit.

**Important limitation:** $B_A$ can perform enormous computations *before* this last observation. It is false to infer a small **total** runtime from the constant suffix residue. No source-bit-invariant potential is thereby made superpolynomial or refuted.

## 4. New strengthening TMR5-SF2: defer a logarithmic suffix

**CANDIDATE pending TMR-1 or TMR-4 independent review; complete constructive argument.** For any fixed total correct $A$, define from the declared header

$$
m(K)=\min\left(\lfloor\log_2 K\rfloor,\;K-(N+M+2)-1\right)
$$

on valid strings (for this grammar, $m(K)\ge1$). A single fixed total correct wrapper $B_{A,m}$ physically reads only the first $K-m(K)$ source bits, constructs and solves every virtual completion $pz$ with $z\in\{0,1\}^{m(K)}$, and stores all $2^{m(K)}$ answers on a charged work tape. Since $2^{m(K)}\le K$, the number of virtual solves is at most linear in encoded input length.

It then starts physically observing the deferred suffix. Before observing its **last** original bit, it uses the observed first $m(K)-1$ suffix bits to perform a fully charged lookup of the two remaining candidate output bits and stores the pair in finite control. The original input head next reads the last bit, checks the right endmarker and halts in $O(1)$ more transitions on valid inputs. Thus all $A$ simulations finish before the first suffix bit is observed, and after the final originally unseen bit there is only constant processing. The suffix lookup itself can take polynomial time but occurs before the last bit, so is not hidden from the time ledger.

For a direct fixed-program simulator and parser, a safe coarse upper bound is

$$
T_{B_{A,m}}(x)
\le \operatorname{poly}_A\left(K+\sum_{z\in\{0,1\}^{m(K)}}T_A(pz)\right)
$$

when $A$ is charged on all virtual inputs. When $A$ has a polynomial time bound only for valid strings, validate each completion and omit expensive $A$ calls on malformed completions. Hence, *if* $A$ is polynomial-time on the valid 3-CNF domain, so is $B_{A,m}$ on valid strings. No such $A$ is constructed here. This is a closure property of hypothetical polynomial algorithms, not a proof of P=NP.

**Scope:** There is no claim that the wrapper is faster than $A$, no claim of constant time after the **first** deferred suffix observation, and no bound beyond the declared-length parsing model. This strengthens TMR-4/003 by showing that even $\Theta(\log K)$ initially unseen input bits can be speculatively completed with polynomial multiplicative overhead while retaining a constant post-last-observation residue.

## 5. Independent TMR-3/002 two-way crossing review

**Review verdict: PROVED/RESTRICTED in the claimed physical model, subject to source grammar and actual fixed finite tapes; no unrestricted runtime separation.** The original $E_n(a,b)$ uses first-bank four-clause gadgets forcing $a$, followed by a second bank forcing $b$. It is valid proper 3-CNF with SAT iff $a=b$ and has

$$
L(n)=13n+2+24n(1+\max(1,\lceil\log_2(5n)\rceil))=\Theta(n\log n).
$$

For each $j\in[\lceil n/2\rceil,n-1]$, and each of $g_n=12(1+w)$ physical cuts in the $(j+1)$st first-bank gadget, fix the remaining prefix-bank bits $v$. The $2^j$ accepted diagonals $E_n((u,v),(u,v))$ have the same first-bank material at and after the cut and permit an exact mixed splice $E_n((u,v),(u',v))$, UNSAT when $u\ne u'$. Equal *complete ordered* crossing records would allow a deterministic splice into a false acceptance. The record must contain controller, crossing direction, ALL visited writable contents, endpoints and head positions; ignoring any of these invalidates the splice.

For each input $a$ and boundary $c$, let $q_c(a)$ be crossing count and $S_a$ be writable cells visited **on the same computation**. Prefix-free encoding of a complete trace has length at most

$$
\ell_c(a)\le D_A q_c(a)(S_a+1)+O_A(\log(S_a+2)),
$$

because $q\ge1$ and the self-delimiting $\log(q+2)$ overhead is absorbed in $O(q)$, while fixed tape count, finite alphabet and sequentially visited tape intervals permit each crossing configuration to be encoded using $O_A(S_a+1)$ bits. For each cut, at most $2^{j/2+1}$ of its $2^j$ distinct descriptions have length below $j/2$. Conditioning on $v$ and union-bounding over the $O(n\log n)$ cuts leaves a single diagonal $a$ with $\ell_c(a)\ge n/4$ on all selected cuts.

If any diagonal has $S_a\ge n$, physical movement to read the second bank gives $T_a\ge L/2$ and already $T_a(S_a+1)\ge Ln/2$. Otherwise all have $S_a<n$, metadata is $o(n)$, so the one diagonal chosen above has $q_c(a)(S_a+1)=\Omega_A(n)$ for each of $\Theta(L)$ disjoint physical cut boundaries. Each actual input-head move crosses at most one cut, yielding on the SAME execution

$$
T_A(E_n(a,a))(S_A(E_n(a,a))+1)
=\Omega_A(L(n)n).
$$

This is the full physical two-way sequential-head model with arbitrary work representations and recomputation; it does not require complete input sweeps. However, the TMR-2/002 one-pass algorithm has $T=O(L),S=O(n)$ on the **same family**, matching the product, and an indexed-access model admits a cheaper product. The theorem therefore establishes physical transport, NOT superpolynomial SAT computation. The algebraic extraction $S\le b_A(T+1)$ yields only $T=\Omega(L/\sqrt{\log L})$ from this product.

**Independent proof stress test:** the splice explicitly conditions on $v$, its mixed source is valid even when the cut is inside the next fixed-$v$ gadget, and all-cut union bounding uses one diagonal rather than adding different-input maxima. A complete physical TM simulator was NOT run. TMR-3's own finite source-splice checks were inspected as secondary **COMPUTATIONAL** evidence, not substituted for the symbolic crossing argument. Classical crossing sequences precede this project [1,2]; original LSPV-5/167 and Claude ONETAPE-0001 already established related equality input-geometry arguments. No novelty claim is made for the general method.

## 6. Independent finite audit and result

**Executable:** experiments/tmr/tmr5_deferred_suffix_audit002.cjs  
**Immutable raw:** results/raw/tmr/2026-11-13_1452_TMR5_DEFERRED_SUFFIX002_RAW.json.

Executed the independent complete Node-compatible JavaScript source in a fresh V8 environment, without importing TMR-4's test code. It generates exact signed strict-proper 3-CNF binary encodings, independently parses literal records with uniqueness/range checks, exhaustively evaluates truth assignments at $N\le14$, enumerates every binary completion of the deferred suffix on each selected small source, and compares the precomputed table lookup to the actual semantic label. Deterministic seed 20261113, no random environmental data.

**Results:** 55 valid source tests; 1,772 virtual suffix completions evaluated; 316 semantic/syntax assertions; one strictly opposite-label final-bit pair; nine malformed-input controls rejected; suffix lengths 1 through 7; zero failures; V8 run time 489 ms. The script and raw output were published and read back byte-identically. This is **COMPUTATIONAL** corroboration, not an asymptotic physical-machine simulation. The bounded experiment solver deliberately refuses $N>14$. The symbolic wrapper instead uses an arbitrary total $A$ (for example the standard exhaustive all-input decider) and remains total for all lengths.

## 7. Integration and dependency classification

- **PROVED/RESTRICTED after independent red-team review:** TMR-4/003's fully charged two-completion temporal-deferral counteralgorithm. A universal *post-final-observation* expensive phase is falsified.
- **PROVED/RESTRICTED after independent red-team review:** TMR-3/002's same-input $\Omega(Ln)$ time-space product under a physically sequential freely reversing source head. The matching $O(Ln)$ family solver and indexed-access escape remain admissible.
- **CANDIDATE / needs second review:** TMR5-SF2's fixed uniform logarithmic-suffix speculation preserving polynomial time *conditionally* on a polynomial solver. It creates no uncharged work and no SAT separation.
- **PROVED/RESTRICTED:** TMR-4/001 and TMR-5/001 observation-only potential ceiling $\Phi\le\tau(D)\le L$, after TMR-1 independent review.
- **OPEN:** Define a temporal-order-invariant compulsory processing measure on full arbitrary Turing-machine traces, with cost-sound EVERY-step abstraction, surviving speculative completions, compact affine/Horn/2-SAT algorithms, bounded treewidth and alternative representations, then establish a lower bound exceeding every fixed polynomial exponent.
- **OPEN:** The all-length fixed-program P != NP target. A correct polynomial-time general SAT algorithm would instead establish P=NP. Neither is supplied by the present results.

**Falsification controls:** The last-bit strict opposite-label pair rules out a semantic-irrelevance shortcut. The deferred-suffix wrapper uses a full precomputed answer table only for a *polynomially bounded set of completions on the current input*, constructed and paid by running $A$; it is NOT nonuniform advice or a free global oracle. Gaussian-elimination XOR and simple Horn/2-SAT and bounded-treewidth formula families can be solved with compact algorithms and therefore remain live adversaries for any supposed obligatory global-consistency representation. Disjoint products, padding, renaming, caching, recomputation and alternate encodings are not restricted by these scoped results. The existing two-way crossing theorem is insensitive to nondeterministic accepting-path selection and does not separate deterministic and nondeterministic SAT decision.

**Relativization and natural-proof boundaries:** No oracle is used in any new argument. The speculative wrapper works for any fixed total oracle decider only if oracle calls are honestly accounted in the same oracle model; it provides no nonrelativizing lower bound. The crossing argument is a physical-input-geometry statement and does not establish circuit lower bounds or a polynomial-time separation, so no constructive large-circuit natural property is claimed. It cannot be transferred to random-access SAT time merely by renaming the machine model.

**Trackers:** Full proof1.txt (28,714 chars, Git blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343) and proof2.txt (1,051,196 chars, blob 930c5eeddafce656717f28055a7a9a755f44737c) read, large proof2 recovered through the actual blob API; no core P1/P2 obligation closed. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Historical owner labels are overridden by the new directive but not erased. Root main.tex (Git blob 57844c68afbf8ab27794774f91c6147e4634c1fa, length 2,485,460) recovered in full by Git blob API; the five TMR regions were inspected. This new review is substantive but only the scoped synthesis should be reconciled, without changing unrelated historical manuscript content.

**Corpus and execution limitations:** Read first the five-TMR replacement directive, then both trackers, current issue #3 through TMR-4/003, AGENTS.md, CODEX.md, the repository research skill, all current TMR handoffs and relevant original TMR-3/002, TMR-4/003, TMR-2/002, TMR-5/001 reports, plus original LSPV-5/167 and Claude ONETAPE-0001. Compared primary Hennie 1965, Cousot/Cousot 1977, and FLMV 2005 theorem metadata; no claim that their theorems directly prove TMR5-SF2. No local full repository checkout was mounted, so preflight.py and check_research_reports.py, OS Node execution, physical TM simulator and LaTeX compilation could not be run. Repository content was read using GitHub connector and publication must be confirmed by readback.

## References

[1] F. C. Hennie, "One-Tape, Off-Line Turing Machine Computations," Information and Control 8 (1965), 553-578. https://doi.org/10.1016/S0019-9958(65)90399-2 . Original crossing-sequence methodology, restricted to source-head geometry.

[2] W. Maass, G. Schnitger, E. Szemerédi, "Two Tapes Are Better Than One for Off-Line Turing Machines," STOC 1987, 94-100. https://doi.org/10.1145/28395.28406 . Demonstrates resource differences under restricted work-tape configurations, not 3-SAT separation.

[3] P. Cousot, R. Cousot, "Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints," POPL 1977, 238-252. https://doi.org/10.1145/512950.512973 . Sound abstraction methodology, not an SAT runtime lower bound.

[4] L. Fortnow, R. Lipton, D. van Melkebeek, A. Viglas, "Time-Space Lower Bounds for Satisfiability," JACM 52(6) (2005), 835-865. https://doi.org/10.1145/1101821.1101822 . Random-access SAT near-linear-time/small-space exclusions, not all polynomial exponent and space bounds.

**Next single research obligation:** TMR-2 and TMR-3 should identify a whole-trace invariant whose *forced* cost cannot be reduced by the polynomially paid $O(\log K)$-suffix speculation wrapper; TMR-4 must construct an EVERY-transition, representation-inclusive cost abstraction. TMR-1 or TMR-4 should independently check TMR5-SF2 before manuscript promotion beyond CANDIDATE. TMR-5 will continue hostile alternate-algorithm and same-machine audits. P versus NP remains OPEN.

END_OF_REPORT::TMR5_TEMPORAL_DEFERRAL_AND_CROSSING_REVIEW002::2026-11-13_1452_PST
