# TMR-2/049: guarded-CNF realization and a sharp 3-CNF / existential-SAT firewall for MajMajSAT

**2026-11-15 10:07 PST | PNP Information Necessity | ALLENDERGUARD049**

**Statuses:** Allender et al. Theorem 7: KNOWN THEOREM at its original model. Exact guarded-CNF, prime-width, and tie-dilution lemmas below: PROVED/RESTRICTED (independent mathematical review OPEN). Executed finite tests: COMPUTATIONAL. Any general MajMajSAT-to-SAT compiler, same-system tariff, superpolynomial SAT lower bound: OPEN. P versus NP OPEN.

## 1. Predeclared candidate and falsifiers

**Candidate:** Turn the Allender Section 3.2 majority-balancing construction, already reconstructed by TMR-1/049, into an explicit gate-by-gate CNF without adding any unaccounted counted variables. Prove exact counts and both majority ties; then determine whether the CNF itself provides any ordinary SAT-oracle information, and what happens under an ordinary 3-CNF conversion.

**Falsifiers:** (F1) Some circuit assignment has zero or multiple auxiliary extensions; (F2) guarding the CNF creates unwanted satisfying tuples or changes an exact tie; (F3) a follow-on Tseitin/3-CNF conversion adds counted auxiliary variables without recalibration; (F4) counting an enormous majority numerator is mistakenly equated with compulsory SAT work, despite a direct satisfying assignment and compact affine/Boolean circuits.

**Original primary source:** Allender, Koucký, Ronneburger, Roy, Vinay, *Time-Space Tradeoffs in the Counting Hierarchy*, CCC 2001, Theorem 7 and Section 3.2, https://people.cs.rutgers.edu/~allender/papers/tradeoff.pdf . For fixed 0<sigma<1, there exists gamma(sigma)>0 with MajMajSAT not in uniform unbounded-error PrTiSp(N^(1+gamma),N^sigma), where N is the encoded input length. No numerical gamma is supplied; no pointwise hard family is implied. Independently review the bounded-error quantum simulation scope in van Melkebeek and Watson, *Time-Space Efficient Simulations of Quantum Computations*, Theory of Computing 8 (2012), https://theoryofcomputing.org/articles/v008a001/ . The quantum extension is theirs, not Allender's.

**Original project comparison:** TMR-1/049, research/agents/tmr-1/2026-11-15_0957_TMR1_ALLENDER_BALANCED_UNIQUE_EXTENSION049.md, proved the *Boolean* balanced-extension identity and already warned that MajMajSAT -> SAT is not supplied. This run's additional results are the exact **unextended guarded CNF** realization, **same-variable 3-CNF impossibility** for its calibration branch, **one-variable post-encoding tie counterexample**, and **SAT/negation-SAT constant-answer firewall**. TMR-2/048's Cartesian mutant potential and other fusion laboratory systems remain restricted and do not authenticate a MajMajSAT machine tariff.

## 2. Exact construction

Let A be ell outer majority variables, B=(b_1,...,b_n) be n>=1 inner variables, and C(A,B) a fixed fan-in-two circuit with g>=1 internal gates, each AND, OR, XOR or NOT. Give gate j one fresh variable z_j, and require every gate to equal its defining function and the final gate z_g to equal TRUE. Denote this **functional** Tseitin CNF by T_C(A,B,Z).

For any fixed (a,b), T_C has **exactly C(a,b) satisfying assignments to all g gate variables Z**: zero if the circuit outputs 0, one if it outputs 1. The standard gate clauses use at most four width-three clauses per gate. In particular a NOT gate uses two binary clauses, an XOR uses four ternary clauses, and the forced output is one unit clause. No unquantified or guessed “existential” marker is substituted for this unique-extension property.

Introduce **one more inner majority variable** t and define the CNF

\[
G_C(A,B,Z,t)=
\left(\bigwedge_{D\in T_C}(t\lor D)\right)
\land
(\neg t\lor b_1\lor z_1\lor\cdots\lor z_g).
\]

The t=0 branch is precisely T_C; the t=1 branch is exactly the calibration clause b_1 OR z_1 OR ... OR z_g. It is a **CNF without any extra counted variables beyond Z and t**. It is equivalent to Allender's balanced disjunction after reversing the selector polarity.

For fixed a, write S_a=|{b:C(a,b)=1}|, K=2^n and M=2^g. In the t=0 branch, functional uniqueness gives S_a satisfying (b,z) pairs. In the t=1 branch, only b_1=0 and z=0^g are rejected, while the remaining n-1 inner bits are arbitrary: exactly KM-K/2 satisfy. Therefore

\[
H_a=\#\{(b,z,t):G_C(a,b,z,t)\}
=2^{n+g}-2^{n-1}+S_a.
\]

The new inner denominator is **2^(n+g+1)**, and its inclusive-majority threshold is **2^(n+g)**, hence

\[
H_a-2^{n+g}=S_a-2^{n-1}.
\]

Thus the signed numerator gap is preserved exactly, including zero for a tie, for **every** a. Since each outer a has the same original inner YES/NO label, both majority blocks and the outer tie are preserved:

\[
\operatorname{MAJ}_{A}\operatorname{MAJ}_{B} C
=\operatorname{MAJ}_{A}\operatorname{MAJ}_{B,Z,t}G_C.
\]

Importantly, **the normalized bias is shrunk by 2^-(g+1)**. In particular, a one-count difference from the threshold is only a 2^-(n+g+1) difference in the new acceptance fraction. An unbounded-error threshold test is not the same as a bounded-error test with a constant advantage.

## 3. Exact representation and resource ledger

Let V=ell+n+g+1 be the variable count. The direct guarded-CNF construction has:

| Quantity | Exact bound or formula |
|---|---|
| Original inner assignment denominator | 2^n |
| New inner assignment denominator | 2^(n+g+1) |
| Original / new threshold | 2^(n-1) / 2^(n+g) |
| New satisfying count for fixed a | 2^(n+g)-2^(n-1)+S_a |
| Gate-definition clauses | at most 4g |
| Forced-output clause | 1 |
| Final calibration clause | 1 |
| Total guarded clauses | at most 4g+2 |
| Total literal occurrences | at most 17g+4 |
| Maximum clause width | at most max(4,g+2) |
| Conventional indexed literal-list bit length | O(g log V), plus header/variable declarations |
| Streaming source-to-output construction | O(g log V) emitted bits on an explicit sequential gate-list encoding; O(log V) **auxiliary generator workspace** with counters and a read-only source, excluding output |
| Whole physical SAT-oracle call | **NOT established:** query materialization, local input access, parsing, buffers, machine-model simulation, and error semantics must be charged |

The literal-count bound follows from <=4g gate clauses of width <=3, each extended by one t literal (<=16g total), one guarded output unit clause (2 literals), and one calibration clause (g+2 literals). Output streaming bounds concern a specified multi-tape transducer with one sequential gate list and append-only output; they do not certify a sublinear-space SAT solver with a materialized query, nor the polylogarithmic **random-access bit generation** needed for the Allender completeness reduction. With a writable materialized query of length Omega(N) the Allender target sigma<1 is immediately unavailable.

## 4. New exact firewall A: guarded CNF's existential SAT is always YES

For every circuit C, every outer assignment a and any g>=1:

- G_C is satisfied by choosing t=1 and b_1=1. No gate evaluation or knowledge of C is needed.
- The complement of G_C is satisfied by choosing t=1, b_1=0 and every z_j=0. On that assignment the final calibration clause is false, hence G_C is false.

Thus **SAT(G_C)=YES and SAT(NOT G_C)=YES identically**, independent of the MajMajSAT instance or majority verdict. These two direct existential queries carry exactly zero information in their YES/NO answers about the majority. This does not rule out a different, nontrivial uniform SAT-oracle reduction which transforms or inspects the source. It rules out the proposed inference that a threshold-preserving CNF representation **by itself** converts the known MajMajSAT hardness to ordinary SAT hardness. Existential SAT discards the denominator and both majority thresholds.

A hypothetical uniform polynomial-time many-one MajMajSAT-to-SAT reduction would put PP-complete MajSAT in NP (by an unused outer bit), giving PP=NP; this is a **conditional collapse**, not a claimed impossibility. A charged small-time/sublinear-space oracle compiler remains OPEN. The small-space lower bound on MajMajSAT cannot be transported to SAT by reversing the established reduction direction.

## 5. New exact firewall B: same-variable 3-CNF calibration-width obstruction

For g>=3, no equivalent 3-CNF over the **same variables** A,B,Z,t can realize this particular G_C. Set t=1: G_C reduces identically to

\[
B=b_1\lor z_1\lor\cdots\lor z_g.
\]

If a 3-CNF H with no further variables were equivalent to G_C, its t=1 restriction would be a 3-CNF equivalent to B. But every non-tautological clause logically implied by B must contain **all g+1 literals** of B: otherwise its falsifying subcube contains an assignment satisfying B. Consequently B has a prime implicate of unavoidable width g+1>=4, and no same-variable 3-CNF can express it. This **does not** preclude a specially calibrated 3-CNF with additional variables or a different balance gadget. It proves only that the direct guarded construction cannot be converted to 3-CNF by simply splitting the long clause over its original variables.

## 6. New exact firewall C: one more unique auxiliary variable reverses a majority tie

Let n=g=1, C(b)=b. Encode the gate as z<->b with forced z=1. The guarded 3-CNF has **exactly 4 satisfying assignments out of 8**, an inclusive YES tie. Add one new **counted** variable w and the unit clause (NOT w). The number of satisfying assignments remains exactly 4, because every prior solution has one permitted w value, but the denominator doubles to 16 and the new threshold is 8. The verdict changes from YES to NO. If C ignores the ell outer bits, it changes the overall double-majority verdict as well.

This is the smallest nontrivial counted-auxiliary tie counterexample: **unique extension preserves #SAT, not the majority fraction**. A routine parsimonious Tseitin/3-CNF conversion applied *after* balancing can therefore invalidate the claimed MajMajSAT reduction. Any replacement must supply an exact, fresh calibration for **all** new counted variables and both majority blocks. Padding with unconstrained variables alone preserves a fraction; padding with forced unique extensions does not.

## 7. Verification, fusion qualification and open arrows

**Actually executed in Code Mode V8**, with no randomness or external dependencies: 108 independently specified fan-in-two gate circuits (AND/OR/XOR/NOT chains, ell=1..2, n=1..3, g=1..3, six structural seeds), 324 outer assignments, 7,056 functional-Tseitin extension checks, 14,112 direct guarded-CNF assignment evaluations, 324 exact inner counts/thresholds, 108 exact outer-majority tests, and 324 positive-and-complement SAT witness checks. One-variable tie-pollution and 64 short-clause prime-implicate attempts were checked. **22,638 assertions, zero failures.** Standalone Node execution not separately performed. Full self-contained JS and immutable result JSON are published separately. Finite evidence is COMPUTATIONAL; all-size claims are established by the proofs above, pending independent review.

The output object has exponentially many satisfying assignments for small g, yet a trivial satisfying assignment. Its count is a **semantic quantity**, not a physical-work obstruction. No new zero-cost quotient, physical tariff matrix, fusion-safe superpolynomial potential, or same-system SAT transfer has been obtained. Cheap circuits, exact affine gates, Horn/2-SAT controls, compact definitions, all real AND branches, preprocessing, learning, caching, sharing and recomputation are retained as legal controls. The source representation must not be mistaken for a lower bound on all deciders.

**Handoff TMR-3/4:** An exact majority-compatible CNF compiler exists with g counted gate variables plus selector, at most 4g+2 clauses and 17g+4 literals, but its SAT answer is constant and its majority advantage shrinks by 2^-(g+1). Charge virtual-bit generation and aggregate writable space on the SAME execution, retain exact counting semantics, and prohibit treating the existential SAT path as a threshold oracle. TMR-5 should independently audit the prime-implicate restriction and the tie counterexample. TMR-1 should separate this restricted construction from the already-established LCH2 -> MajMajSAT local completeness reduction.

**Next:** seek a uniform *decision-preserving*, charged reduction from MajMajSAT to small-space SAT-oracle computation (or prove a specific no-go under stated oracle/communication restrictions). Current known class lower bound does not itself produce that missing compiler. /341 remains FAIL as a full UNSAT logical authority; /386 remains RESTRICTED.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Full authentic proof2.txt and main.tex recovered by Git blob SHAs, proof1.txt read; unchanged SHA values: proof1 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 930c5eeddafce656717f28055a7a9a755f44737c; main.tex 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. Existing TMR roles, schedules and root ownership unchanged. P versus NP remains OPEN.
