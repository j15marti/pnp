# TMR-1/047: Unary-indexed SAT hard-family barrier equals E versus NE

**2026-11-15 08:00 PST | TMR-1 PNP Machine Model Lead | TALLYNE047**

**Status:** PROVED/RESTRICTED for the stated uniform-generator and machine-quantifier theorem, independent mathematical peer review OPEN. The tally/NE/E equivalence is classical padding, **not claimed original**. Finite executable checks COMPUTATIONAL. No superpolynomial SAT lower bound; P versus NP OPEN.

## 1. Candidate and four falsifiers fixed before corpus/literature search

**Candidate:** In the exact ordinary deterministic multitape SAT-machine model, the existence of one polynomially unary-generated, length-honest, source-authentic proper 3-CNF sequence that is superpolynomially hard on infinitely many indices for **every fixed correct total SAT decider** is equivalent to the known open separation E != NE. This is a qualification and target-strength theorem, not a constructed hard sequence or a resolution of either separation.

(F1) A fast "specializer" might require exponential search over generator indices because its unary index is larger than its actual source bit length. Retain n <= N_n explicitly.

(F2) A generator might print an incorrectly labeled formula, a malformed proper-3CNF source, or inconsistent collisions. Treat labels as the actual SAT predicate, authenticate the encoding and use a fully correct fallback.

(F3) A family-decider could be only a promise oracle or nonuniform per-length lookup, not one fixed total deterministic SAT decider. Construct one program using enumeration and exhaustive fallback, charging all reads and tape work.

(F4) The equivalence might illegally claim that **E != NE has been proved** or exclude algorithm-dependent hard inputs. Neither is claimed. A real polynomial-time specialist on any easy family is retained as a legal shortcut, never CEGAR-deleted.

## 2. Sources and governance

Read FIRST the active 2026-11-14 fusion-Lipschitz directive (SHA 54c9177fc211dfca6c94d89d6ebbf3f3908809d6), then the 2026-11-13 TMR replacement, AGENTS.md, CODEX.md, repository research skill, issue #3 through TMR-5/043, and all five CURRENT TMR handoffs. Read both root trackers and root main.tex: proof1.txt 28,714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2.txt authentic Git blob 1,051,196 characters, SHA 930c5eeddafce656717f28055a7a9a755f44737c; main.tex authentic Git blob 2,545,859 characters, SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. The ordinary contents API returned blank bodies for the two large documents; the original blobs were recovered by their SHA and checked. No root/shared tracker edit.

Original context: TMR-1/045 (last-bit cubic Tseitin pair, physical linear input tariff), TMR-1/046 (correctly labeled indexed-family polynomial universal-decider ceiling, explicit source and executable); original TMR-4/047 and TMR-5/043 phase-sensitive record-system exact Bellman tariffs, and original TMR-2/046 and TMR-3/046 fractional/ fused record tariffs. This report adds a precise **necessary and sufficient complexity-class characterization** of what strengthening TMR-1/046 to an unknown-label fixed unary hard family would actually require. It does not relabel those systems.

Primary standard background: Steven Homer and Alan L. Selman, *Computability and Complexity Theory*, second edition, Springer, 2011, Chapter 5 (tally NP versus E/NE padding), https://www.cs.bu.edu/faculty/homer/complexitybook-vol2-webpg.html . The standard NP-to-3SAT uniform reduction is used at its ordinary polynomial-time many-one scope. The theorem below has a self-contained padding proof and is not attributed as a new general complexity-class discovery.

## 3. Exact quantified hard-family property

Let G be the class of **single fixed deterministic polynomial-time unary transducers** g taking 1^n (n>=1) to a valid source-authentic strictly proper 3-CNF formula g_n, with encoded bit length N_n satisfying for all n

$$
n\le N_n\le (n+1)^c
$$

for some generator-dependent constant c. The same finite explicit encoded grammar and one fixed ordinary multitape machine model are used for both g and SAT deciders.

Define U_g = {1^n : g_n is satisfiable}. Define property H(g) as

$$
\forall D\in\mathrm{DEC}_{\mathrm{SAT}}\;
\forall k\ge1\;\forall C>0\;\forall n_0\;
\exists n\ge n_0:
T_D(g_n)>C(N_n+1)^k,
$$

where DEC_SAT contains **fixed total correct deterministic** machines for the entire encoded proper-3CNF language, not only the sequence. This is a single common source sequence allowed to depend on g, but **not** on D.

**Theorem 047.1 (exact unary family equivalence).** For each such g,

$$
\boxed{H(g)\ \Longleftrightarrow\ U_g\notin\mathrm P.}
$$

*Proof, easy unary labels => no hardness.* If U_g is in P, construct one fixed total correct SAT decider D_g. On arbitrary input y of actual length N, enumerate every n=1,...,N, compute g(1^n) on a paid work tape, compare the entire printed source with y using genuine source reads, and, on a match, return the correct computed U_g label. If nothing matches, parse y and invoke an exact exhaustive general 3-SAT decider (reject malformed inputs). Length honesty n<=N guarantees that every g_n is matched. All comparisons, indexing, generation and labels cost at most a fixed polynomial of N on matched inputs, with no advice, oracle or free source conversion. Any collisions g_n=g_m have equal labels because they are the same formula. Thus H(g) is false.

*Proof, no hardness => easy unary labels.* If H(g) fails, then some fixed total correct D, constants k,C and n_0 satisfy T_D(g_n)<=C(N_n+1)^k for all n>=n_0. On unary 1^n, run the fixed generator and then D. Since N_n<=poly(n), this decides U_g in deterministic polynomial n-time. Absorb the finite indices n<n_0 into finite control. Thus U_g is in P. QED.

The proof uses the genuine fixed-program time quantifier. A different nonuniform program for every n is neither needed nor permitted.

## 4. Existence theorem and classical tally padding

**Theorem 047.2 (strength of a fixed universally hard indexed SAT sequence).** With the same class G,

$$
\boxed{
(\exists g\in G:\ H(g))
\ \Longleftrightarrow\
\bigl((\mathrm{NP}\cap\mathrm{TALLY})\not\subseteq\mathrm P\bigr)
\ \Longleftrightarrow\
\mathrm E\ne\mathrm{NE}.
}
$$

Here E = DTIME(2^{O(m)}), NE = NTIME(2^{O(m)}), and TALLY consists of unary languages.

*First equivalence.* Since g prints a polynomial-length formula in polynomial unary time, U_g belongs to NP: guess and verify the polynomial-size Boolean assignment after producing g_n. Conversely, for any tally language U in NP, the standard **uniform** polynomial-time Cook-Levin-to-3SAT map on 1^n prints a proper width-three source whose satisfiability is U(1^n). Convert all width-one/two clauses to equisatisfiable proper width-three clauses with fresh variables and append n independent satisfiable proper width-three clauses, adding fresh variables and retaining the SAT label. This honest padding makes N_n>=n in one fixed finite source encoding while maintaining N_n<=poly(n). Thus every tally NP language is U_g for some g in G. Apply 047.1. The padding is for polynomial reduction honesty, **not** a complexity lower bound from padded bytes.

*Second equivalence, E=NE => all tally NP in P.* For U subset 1^* in NP, form binary L_U = {bin(n):1^n in U}. On a binary input of m bits, a nondeterministic machine builds or simulates 1^n for n<2^m and runs the unary NP machine in 2^{O(m)} time, so L_U in NE. Under NE=E it is decidable in 2^{O(m)} deterministic time. On 1^n, compute bin(n), run that decision, obtaining n^{O(1)} time. Hence U in P.

*Second equivalence, all tally NP in P => E=NE.* Let L be any NE language on m-bit strings x, with nondeterministic time 2^{a m}. Encode x as the positive integer

$$
n(x)=2^m+\operatorname{val}_2(x)
\quad\text{so that}\quad
2^m\le n(x)<2^{m+1}.
$$

Define tally U_L={1^{n(x)}: x in L}, with the all-zeros-to-empty dyadic convention. On unary 1^n, recover m=floor(log_2 n) and the unique m-bit x corresponding to n-2^m, and run the NE recognizer in n^{O(1)} nondeterministic time. Hence U_L in NP. By the assumption, U_L in P. On binary x, explicitly write 1^{n(x)} in 2^{O(m)} deterministic time, decide U_L in polynomial n-time, and decide L within E. Thus NE subset E; the reverse inclusion is immediate. QED.

**Interpretation:** One algorithm-independent unary-indexed hard sequence under these exact constructibility and honesty conditions would yield **E != NE**, which in turn implies P != NP. This is a stronger unresolved target than simply requiring hard inputs depending on the SAT algorithm. No such g has been found or inferred here. The theorem does not claim the converse P != NP => E != NE.

## 5. Concrete family/encoding and executed hostile controls

For a deliberately easy calibration of the exact length conditions, map every binary x to the dyadic unary index n=2^{|x|}+val_2(x). Set y(x)=1 iff x has odd Hamming weight. Define g_n by the four proper clauses encoding x_1 XOR x_2 XOR x_3=0, add the four contradictory clauses encoding XOR=1 when y(x)=0, and add **n separate satisfiable** proper width-three clauses on n fresh triples. The first three variable IDs belong to the parity block and fresh IDs are 4,...,3n+3.

This source has V_n=3n+3 variables and q_n=n+4 if y=1, otherwise n+8. It is SAT iff y(x)=1 by the direct parity argument and a witness assigning every filler triple TRUE. Its actual source encoding has the 8-bit magic 00110101, Elias-gamma V_n and q_n, followed by three fixed-width positive IDs plus a polarity bit per clause occurrence. Thus

$$
N_n=8+\ell_\gamma(V_n)+\ell_\gamma(q_n)
+3q_n\bigl(\lceil\log_2(V_n+1)\rceil+1\bigr)=\Theta(n\log n).
$$

The source is **proper 3-CNF**, length-honest, growing and uniformly enumerable. Its labels are extremely easy; the real polynomial specialist is legitimate, so it **cannot** witness H(g). This is a hostile control, not a candidate lower bound. The direct executable does not compile arbitrary NP witnesses to CNF and cannot by finite testing establish 047.2.

**Actual executed V8 finite checks:** all dyadic indices 1..511, with every binary x of length 0..8; 511 canonical proper formulas, 255 SAT and 256 UNSAT; 4,097 assertions, zero failures; total 4,597,914 encoded source bits parsed and checked; first/last lengths 125/18,732 bits. Every input was roundtrip parsed, formula structure/actual labels checked, source length checked and an actual source-matching specializer executed. Small cases were additionally exhaustively checked. Four off-family/malformed controls exercised the total fallback. These are COMPUTATIONAL results only.

Published code: experiments/tmr/tmr1_tally_ne_padding047.js. Immutable raw: results/raw/tmr/2026-11-15_0800_TMR1_TALLY_NE047_V8_RAW.json.

## 6. Complete concrete system and tariff boundary

Use the declared one-fixed-program, fixed-alphabet, fixed-work-tape-count deterministic locally moving multitape machine with full immutable physical source bits, authentic source-head position, all work tapes, all heads, finite control, full history and completed SAT/UNSAT label. This embeds the directive's (F,A,G,P,Gamma,D,I,O) bookkeeping as applicable; the analytic history is **not** a free read oracle. Physical transitions each cost one, including input access, head movement, simultaneous read/write, preprocessing, alternate algorithms, storage, recovery, caching and recomputation. Optional source-blind zero-cost VIEW is invariant. Authentic physical zero-cost SCCs are singletons. A completed goal is a genuinely halted computation with the correct label, with the program correct on **all** encoded proper 3-CNFs and malformed input handling.

Keep seven columns, in order: (CNF, XOR, SEP, FUS, Gamma, Interface, Machine). For TMR-1/045's **distinct** opposite-label last-original-bit Tseitin siblings, reuse its valid source-frontier vector p=(0,0,0,0,0,max(0,N-1-r),0): an authentic first read of a new frontier source bit has signed discharge (0,0,0,0,0,1,0), cost one; all other genuine physical steps (including simultaneous HALT, algebra, shared proofs, source rereads and recomputation) have zero discharge, cost one; an optional reversible VIEW has zero discharge and price zero. Exact weights lambda=(0,0,0,0,0,1,0), initial gap **N**, completed correct goals zero. It is a **linear** bound in that different family, already established in /045 and /046; this report claims no fresh tariff there.

For the new dyadic calibration, **do not import the last-bit frontier**: its independent filler suffix is not decision-critical. Set its unproven computational coordinates to zero. A trivial goal-obligation coordinate (unfinished HALT) decreases by at most one on authentic final steps; this gives at most one unit, not a useful new lower bound. All unexamined arbitrary machine transitions are MAY, not silently omitted. A superpolynomial initial potential on the dyadic family is contradicted by its authentic polynomial specializer.

**Conditional telescoping:** for any fixed qualified machine or proof authority R, if every authentic rule obeys lambda^T[p(cl0(C))-p(cl0(C'))]<=w(r), every authentic zero-cost path obeys the same inequality with w=0, and every completed goal has Phi<=0, then along any complete genuine execution of paid steps r_1,...,r_t,

$$
\Phi(C_0)\le\sum_{i=1}^t w(r_i).
$$

The same-system transfer gate for a proof route remains: SAT in P must imply polynomial **native** whole-DAG cost in that exact R on the exact family, with source authentication and all charged interfaces. A rejecting machine run cannot be silently treated as a native UNSAT proof. The direct-machine route must cover **all** fixed correct total SAT deciders, retaining their real polynomial specialized paths.

## 7. Dependency/status map and peer deliverables

| ID | Dependency | Status |
| --- | --- | --- |
| 047-A | For each honest unary generator, H(g) iff U_g notin P | PROVED/RESTRICTED, peer review OPEN |
| 047-B | Existence of such g iff unary NP not subset P iff E != NE | KNOWN classical padding theorem plus scoped 047-A, peer review OPEN |
| 047-C | Dyadic source, exact length, SAT/UNSAT and specialized-decider controls | PROVED/RESTRICTED, finite COMPUTATIONAL |
| 045/046 | Original last-bit input-frontier tariff and easy-family ceiling | PROVED/RESTRICTED, external review OPEN |
| 047-D | Explicit uniformly generated hard unary family g satisfying H(g) | OPEN, would establish E != NE |
| 047-E | All-real-machine superpolynomial multiscale tariff and transfer | OPEN |
| TMR-2/046, TMR-3/046, TMR-4/047, TMR-5/043 | Exact preauthenticated fused record systems | PROVED/RESTRICTED, not physical SAT machine transfer |
| Historical /341, /386 | Full logical authority FAIL; restricted guarded odd-charge fragment RESTRICTED | Unchanged |
| P versus NP | General resolution | OPEN |

**TMR-2 weakest next lemma:** test whether any proposed explicit, poly-unary-generable fixed hard family is already asking for the E/NE separation, and seek an actual program-sensitive residual instead of large semantic rank.

**TMR-3 weakest next lemma:** independently bound the genuine physical generation/comparison cost of the specialist and retain all alternative computation paths; no separate charge for free sample labels or filler bytes.

**TMR-4 weakest next lemma:** add the polynomial specialist to every full-machine MAY abstraction for easy U_g, and reject a purported initial gap greater than its authentic trace; never refine away a real specialist.

**TMR-5:** independently review both equivalence directions, especially the dyadic index convention, proper-CNF padding and the NE/E exponent conversion.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt, proof2.txt and main.tex retained complete and unedited. No existing schedule, title, task identity or ownership changed. **P versus NP OPEN.**

END_OF_REPORT::TMR1::TALLYNE047::2026-11-15_0800_PST
