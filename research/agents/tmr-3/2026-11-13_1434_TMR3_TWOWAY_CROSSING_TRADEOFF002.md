# TMR-3 / TWO-WAY-CROSSING-TRADEOFF002: eliminating the complete-sweep restriction for the exact equality 3-CNF family

**Date:** November 13, 2026, 14:34 PST (America/Los_Angeles).  
**Role:** NEW TMR-3 Time-Space Tradeoffs, j15marti/pnp main.  
**Scientific status:** CANDIDATE, complete symbolic derivation awaiting independent TMR-5 scrutiny. Finite source/splice checks are COMPUTATIONAL. The result is polynomial-strength and restricted to one physically sequential input head; **P versus NP remains OPEN**.

## 1. Claim card and falsifiers

**Candidate TMR3-TW2.** For *every* one fixed, correct, total, deterministic multitape 3-SAT decider with ONE freely reversing but sequential two-way read-only input head, a fixed number of ordinary sequential work tapes, a finite control and alphabet, and per-transition head moves of at most one tape cell, there is a constant c_A>0 and an n_A such that for every n>=n_A, **one satisfiable member of the exact TMR-2/001 family** E_n(a,a) has

$$
T_A(E_n(a,a))(S_A(E_n(a,a))+1)\ge c_A L(n)n
=\Omega_A\!\left(\frac{L(n)^2}{\log L(n)}\right).
$$

Here T and S are charged on the SAME accepting trace/input, S counts ALL writable work cells visited, and L is the entire encoded bit length. No complete input sweep, monotone head movement, prescribed order of computation, prescribed internal representation, or memory retention is assumed. This is an unrestricted **two-way-access theorem within the standard sequential-input-head model**, NOT a theorem for indexed/random-access machines and NOT a superpolynomial time lower bound.

Predeclared falsifiers: (F1) a cut splice fails to produce the exact valid original 3-CNF E_n(a,b), (F2) matching crossing records do not support a true deterministic splice because work-tape positions/contents were omitted, (F3) per-cut hard *different* inputs are improperly summed as if one input, (F4) a fully charged 1-pass O(L)-time O(n)-space solver violates the claimed bound, (F5) an indexed-input algorithm is inadvertently included in the sequential-head hypothesis. F1 checked exhaustively in finite instances; F2 and F3 repaired by full-configuration prefix-free coding and simultaneous counting; F4 meets the bound; F5 is explicitly excluded.

**Prior-art warning:** This is an adaptation of classical crossing-sequence/communication techniques. The project's original LSPV-5/167 already established a same-input crossing average on a *different left-gap-right exact22 family*, and Claude ONETAPE-0001 documented general off-line TM and SAT bounds. We claim only the explicit extension of TMR-3/001 from full sweeps to ALL two-way input-head motions on the already-authenticated original TMR-2 equality family, with a same-execution product and exact encoding. No novel general crossing-sequence principle or previously unknown SAT complexity class separation is claimed.

## 2. Original source and machine

TMR-2/001 gives an exact family E_n(a,b), a,b in {0,1}^n. Every block consists of four proper three-literal unit-forcing clauses U(ell;u,v) using one shared x_i and two fresh auxiliary identifiers. First n blocks force x=a, next n force x=b; hence E_n(a,b) is SAT iff a=b.

The binary input uses the unary N=5n header, unary M=8n header, then ordered sign/index literal records, with index width w=max(1,ceil(log_2(5n))). Each four-clause block has

$$
g_n=12(1+w)
$$

physical bit cells; the header has h_n=13n+2 cells, and

$$
L(n)=h_n+2ng_n=13n+2+24n(1+w)=\Theta(n\log(n+1)).
$$

The first n consecutive blocks encode a; the second n blocks encode b. Work-tape alphabets and number b_A are fixed by A, not by n. The original read-only head starts at the left boundary and moves by at most one cell per physical transition, but can reverse arbitrarily, stall, copy source data, preprocess, recompute, use Gaussian elimination, or store compact circuits. All these work operations count in T and all touched writable work cells count in S. Malformed sources are rejected. No free oracle, index-tape jump, unbounded word, supplied advice, or hidden proof system.

## 3. Exact source cuts and conditional fooling set

Number input symbols starting from zero. For each integer

$$
\lceil n/2\rceil\le j\le n-1,
$$

take **every** one of the g_n physical input boundaries immediately before or within the (j+1)-st *first-half* block (zero-based block index j). Equivalently take cuts at

$$
c=h_n+jg_n+t,\qquad 0\le t<g_n.
$$

Call this set C_n. Its size is

$$
|C_n|=\lfloor n/2\rfloor g_n=\Theta(L(n)).
$$

At such a cut, fix a suffix v in {0,1}^{n-j}. For each prefix u in {0,1}^j let a=(u,v), and consider the accepting diagonal input E_n(a,a). Every occurrence of the first j bits of its *first* bank lies strictly left of the cut; the partial (j+1)-st block and the remainder of the first bank depend on the common fixed v. The *second* bank lies entirely to the right.

For two distinct prefixes u,u' sharing v, splicing the LEFT original source from E_n((u,v),(u,v)) with the RIGHT original source from E_n((u',v),(u',v)) yields EXACTLY the valid original source

$$
E_n((u,v),(u',v)),
$$

which is UNSAT. No variable indices, clause count, sign pattern, or source syntax are changed outside the signed blocks already present. This is a two-sided, valid-source fooling set of size 2^j **at each fixed cut and suffix**.

## 4. Entire crossing configuration and cut-and-paste lemma

For any one diagonal input z_a=E_n(a,a), let q_c(a) be the actual number of times A's original input head crosses boundary c. At each crossing record the **entire** instantaneous writable configuration: controller state, direction, contents of every visited interval of every work tape, lengths/endpoints and all work-head positions. The original input-head position is determined by c and direction; the source tape is read-only and is NOT presumed copied into the record. Each crossing is a real, charged transition. Because A has finitely many fixed tapes/alphabets and visits S_a writable cells on this trace, a crossing record can be serialized with at most d_A(S_a+1) bits, for a machine-dependent fixed d_A. Work-head coordinates are bounded by visited interval lengths, so this encoding does not need a separate log T term. It does not hide unbounded work contents in the controller.

Every q_c(a)>=1. Otherwise the accepting computation never reaches the right-hand second bank; changing any b-sign block produces a valid UNSAT source without changing an observed cell. Determinism then yields the same incorrect acceptance, contradicting TMR-2's input-sensitivity lemma.

**Full-state splice.** Fix cut c and suffix v. Suppose two different prefixes u,u' yielded identical complete *ordered crossing records* on their two accepted diagonals. On the mixed original input E_n((u,v),(u',v)), simulate the left-side computation segments from the first accepted run and the right-side segments from the second. Each crossing agrees on the full controller, work contents and heads, so induction on successive segments gives a legal accepting computation of A on the UNSAT mixed input. Determinism and correctness contradict this. Therefore the complete sequences for the 2^j prefixes are pairwise distinct. This is not a per-sweep or one-pass argument; arbitrary reversals and caching are included.

## 5. Variable-resource prefix-free transcript coding and one common hard input

A description of q_c(a), S_a and the q_c(a) records can be made prefix-free: self-delimit S_a and q_c(a), then write fixed-width padded configurations of at most d_A(S_a+1) bits each. With q>=1, one can absorb the O(log(q+1)) field in the per-crossing budget, obtaining a constant D_A such that the total description length is at most

$$
\ell_c(a)\le D_A q_c(a)(S_a+1)
+D_A\log_2(S_a+2)+D_A.
\tag{1}
$$

**No same-input resource borrowing:** S_a is the actual peak work-cell count of the exact trace whose crossing sequence is encoded; neither a per-length maximum from another computation nor an independently chosen small-space witness is substituted.

For each fixed j,v,c, the 2^j descriptions indexed by prefixes u are distinct and prefix-free. Among 2^j different binary prefix-free descriptions, at most 2^{j/2+1} have length <j/2. Thus for uniform a in {0,1}^n,

$$
\Pr_a[\ell_c(a)<j/2]\le 2^{1-j/2}
\le2^{1-n/4}.
\tag{2}
$$

The inequality also holds after averaging over fixed suffixes v. Union-bound (2) over **all** |C_n|=O(n log n) cuts, so for sufficiently large n there is a *single* a for which

$$
\ell_c(a)\ge n/4
\qquad\text{at every }c\in C_n.
\tag{3}
$$

We must handle varying workspace rather than suppress it. First, every diagonal execution has T_a>=L(n)/2: correctness requires it to read at least one literal sign in the second bank, and the input head must travel physically over at least h_n+ng_n>=L(n)/2 cells from its initial position. If **any** diagonal has S_a>=n, the desired same-input product follows immediately:

$$
T_a(S_a+1)\ge L(n)n/2.
$$

Otherwise ALL diagonals have S_a<n. For the a supplied by (3), the logarithmic metadata in (1) is O_A(log(n+2))=o(n), so for every c in C_n, sufficiently large n yields

$$
q_c(a)(S_a+1)\ge n/(8D_A).
\tag{4}
$$

Each physical input-head movement crosses at most one input-cell boundary; crossing counts over DISTINCT cuts never charge the same transition twice. Therefore, on this **one** z_a,

$$
T_a(S_a+1)\ge(S_a+1)\sum_{c\in C_n}q_c(a)
\ge\frac{n|C_n|}{8D_A}
=\Omega_A(n^2\log(n+1)).
$$

Since L(n)=Theta(n log(n+1)), this proves the candidate inequality T_a(S_a+1)>=c_A L(n)n for every sufficiently large n. Proof is complete as a symbolic implication from the exact source family and standard sequential-head model, pending independent review of the full crossing configuration and prefix-free encoding.

An equivalent average-code proof is possible, as in prior LSPV-5/167. The explicit union-bound proof here prevents the old erroneous shortcut of summing the per-cut maxima for *different* inputs.

## 6. Sharpness and model-transfer obstruction

**Exact matching upper control.** TMR-2/002 constructs ONE total uniform correct all-input machine with a fast path recognizing these original E_n sources using a single monotonically increasing source sweep, O(L(n)) physical transitions and Theta(n) visited writable cells. It falls back to a fully paid exhaustive SAT decider on other inputs. Thus on EVERY member of E_n,

$$
T_D(E_n(a,b))(S_D(E_n(a,b))+1)=O(L(n)n).
$$

The lower bound is tight to constants on the exact equality family even after dropping the complete-sweep restriction. It measures sequential information transfer, not inevitable exponential SAT reasoning. TMR-2's explicit fast path simultaneously performs global equality processing while reading; a separate post-read phase is NOT necessary.

**Random/indexed-access countermodel.** The theorem explicitly fails on a different model whose input INDEX tape can jump to arbitrary original source bits after a charged O(log L)-bit address is written. Verify the rigid original source grammar in O(L polylog L) time and O(log L) workspace by repeated regenerated indices; compare the n paired first-sign coordinates using paid index writes, with all counters, index tape and heads charged. For E_n inputs, this gives T=O(L log^2 L), S=O(log L) and hence T(S+1)=O(L log^3 L)=o(Ln). An all-input-correct exhaustive fallback makes this ONE fixed total program without asserting a general polynomial SAT decider. The exact indexed machine capability is documented in the original LSPV-4/487 K4 equality escape; here the local source is the distinct TMR-2 E-family. No random-access operation is permitted in TW2.

**Extraction barrier.** The standard same-trace occupancy S<=b_A(T+1) applied to T(S+1)>=c L n gives only T=Omega_A(sqrt(Ln))=Omega_A(L/sqrt(log L)). This extracted exponent is *weaker* than the direct T>=L/2 physical traversal of a second-bank sign coordinate. In any case T=O(L) with S=Theta(n) on the very same family, so the theorem cannot establish superlinear general SAT time, let alone exclude every polynomial exponent.

**Nondeterminism control.** A similar crossing-splice proof applies to one fixed chosen accepting path for each diagonal of a correct nondeterministic machine with on-the-fly choices and no external uncharged guess tape: equality transcripts must remain distinct because the UNSAT mixed input cannot have an accepting path. This further shows the method primarily measures the input-access topology, not a deterministic versus nondeterministic search separation.

## 7. Reproducible finite checks, source provenance, and falsification ledger

**Published executable, read back:** experiments/tmr/tmr3_twoway_crossing_splice002.cjs, Git blob 6ca3cd1385b7b29ee5dc4df9d156c18f9f77678b.  
**Published immutable raw, read back:** results/raw/tmr/2026-11-13_1434_TMR3_TWOWAY_CROSSING_RAW.json, Git blob 873ebb331fd1e173e5170508db9a623439c2a78c.

An independent zero-dependency V8 script was actually executed, exhaustive on all ordered pairs a,b for n=1..5 (1,364 exact signed sources: 62 SAT and 1,302 UNSAT), with 16 local truth-table unit-gadget checks, **71,520** exact cut splices across all physical cut positions in the specified fixed-suffix gadget intervals for n=2..5, including **63,888** distinct-prefix UNSAT hybrid splices, and 408 distinct cuts across the tested lengths. All assertions passed, zero randomness. Exact lengths were 111,268,401,630,787 bits. These test the most fragile F1 cut syntax/semantics condition, not the asymptotic prefix-code lemma. Code and immutable JSON were independently fetched from main and string-compared to the submitted bodies.

The script uses source semantics and text splicing, **not** a physical native Turing-machine simulator; a complete state-by-state TM replay, OS Node CLI, repository-wide preflight, and LaTeX compilation were NOT executed. No computation was attributed to a nonexistent system or to an unexecuted test. The symbolic arguments are distinct from finite tests.

**Corpus reconciliation:** Read latest directive FIRST and again before writes, proof1.txt and proof2.txt in full (proof2 recovered from nonempty Git blob), root main.tex in full from Git blob (current five TMR regions), AGENTS.md, CODEX.md, pnp-research SKILL, modes and research-protocol, latest issue #3, TMR-1/002, TMR-2/001 and /002, TMR-3/001, TMR-4/001, TMR-5/001 and all latest handoffs. Read historical LSPV-5/167 crossing averaging, Claude ONETAPE-0001, and LSPV-4/487 indexed equality countermodel. Compared original primary Hennie crossing sequences (1965), Santhanam SAT TM lower bounds (2001), and FLMV random-access SAT time-space exclusions (2005). The model distinction and source encoding are inherited, not hidden.

**Compared with root main.tex:** The currently authorized TMR-3 paragraph records complete-sweep/prescribed-pass result. TW2 is a candidate stronger *same-family* theorem allowing arbitrary two-way input-head movement but still only a fixed polynomial product. No contradictory root claim needs emergency correction. It should be integrated into the TMR-3 region **only after TMR-5 reviews**; root manuscript otherwise unchanged.

**Status:** TMR3-TW2 CANDIDATE / RESTRICTED MODEL, review requested; finite splice controls COMPUTATIONAL; original TMR-3/001 verified only in its complete-sweep model; P2-00 and every unrestricted superpolynomial lower-bound arrow remain OPEN. Both root proof trackers REVIEWED, NO MATERIAL CHANGE. No agent/task schedules altered. The older proof-calculus sources and failed transports remain preserved.

## 8. References

[1] F. C. Hennie, "One-Tape, Off-Line Turing Machine Computations", *Information and Control* 8 (1965), 553-578. DOI: https://doi.org/10.1016/S0019-9958(65)90399-2. Classical crossing sequence and splicing method; not a theorem transferring our bound to random access.

[2] R. Santhanam, "Lower Bounds on the Complexity of Recognizing SAT by Turing Machines", *Information Processing Letters* 79(5) (2001), 243-247. DOI: https://doi.org/10.1016/S0020-0190(00)00227-1. Previously identified SAT Turing-machine lower bounds and limitations. This paper's full text was not retrieved; bibliographic and abstract records only.

[3] L. Fortnow, R. Lipton, D. van Melkebeek and A. Viglas, "Time-Space Lower Bounds for Satisfiability", *Journal of the ACM* 52(6) (2005), 835-865. DOI: https://doi.org/10.1145/1101821.1101822. Their random-access near-linear-time/small-space exclusions are a different model and do not rule out polynomial time with arbitrary polynomial workspace.

[4] LSPV-5, CROSSING-AVERAGE-QUANTIFIERS167, research/agents/lspv-5/2026-10-26_1648_LSPV-5_CROSSING_AVERAGE_QUANTIFIERS167.tex. Full-gap crossing averaging and max-vs-average quantifier counterexample are original project prior work.

[5] CLAUDE, ONETAPE-0001, research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex. Records preexisting one-tape and palindrome/SAT crossing results, including a near-quadratic product barrier in sequential access.

[6] TMR-2/001 and /002 original signed E_n sources and one-sweep matching upper, and TMR-3/001 complete-sweep proof, all in research/agents/tmr-2/ and tmr-3/.  

**Next falsifiable obligation:** TMR-5 independently verify TW2's conditional-suffix cut splicing, compact variable-S transcript code, all-cut union bound, T>=L/2 lemma and the claimed O(Ln) matching upper. Then ask TMR-4 to construct an all-transition abstraction exposing this physical boundary transfer without imposing a prescribed pass order, and TMR-1 to audit the exact model translation. To advance beyond this polynomial wall, one must force computational work beyond physical input geometry, survive indexed access/compact algebra and arbitrary polynomial workspace, and beat every fixed time exponent.

END_OF_VERIFIED_REPORT::TMR3_TWOWAY_CROSSING_TRADEOFF002::2026-11-13_1434_PST
