# TMR-5/011: exact seven-sign minimal certificates and independent ALL6 review

**Pacific timestamp:** 2026-11-13 23:55 PST (America/Los_Angeles). **Role:** NEW TMR-5 Machine Bottleneck Redteam and canonical synthesis owner, j15marti/pnp main.

**Scientific status:** Independent mathematical peer review supports TMR-2/013's all-mask five- and six-sign certificate formulas at **PROVED/RESTRICTED** scope for the authenticated original G_r grammar. New TMR5-M7-011 seven-bit *inclusion-minimal* certificate classification and counting formula are **CANDIDATE pending independent TMR-2/TMR-1 review**. Executed finite evidence is **COMPUTATIONAL**. The unrestricted all-exponent 3-SAT lower bound and P versus NP remain **OPEN**.

## 1. Exact object, dependencies, and limits

Use the authentic strict proper 3-CNF G_r template of TMR-2/010 through /013. It has eight ordered clauses on the same three core variables in every block; all 24 original clause-polarity bits in each block are free; headers, canonically ordered identifiers and positive filler clauses are fixed. Every sign assignment remains a valid encoded source with all declared identifiers used. A block is UNSAT exactly when its eight three-bit masks are a permutation of 0,...,7. Each block's polarity query position is p=3i+j for row i in 0,...,7 and coordinate j in 0,1,2. Formula length in encoded bits is

$$
w=\lceil\log_2(6r+2)\rceil,\quad N=2^w-1,\quad
K=\lceil(N-3r)/3\rceil,\quad M=8r+K,\quad
L=N+M+2+3M(w+1)=\Theta(r\log r).
$$

This is a **promise source-bit certificate**, not a proof-system refutation, streaming-state restriction, stored entropy requirement, or unavoidable machine processing charge. Any fixed correct total deterministic SAT machine with h physically limited input heads must actually read a sign certificate on its halting original-source run; arbitrary other encodings, re-reads, caching, compact algebra, and arbitrary polynomial workspace remain permitted. The existing family's authenticated one-pass eight-mask classifier has a uniform polynomial symbolic implementation and is an important hostile control. No post-acquisition superpolynomial implication is asserted.

## 2. Independent peer verdict on TMR-2/013

Let a be any ordered eight-mask tuple. Let f_m be the number of rows with complete mask m, f_{J,v} the number of rows with two-coordinate projection v on J, and n_{j,b} the number with coordinate j equal to b. Define binom(n,k)=0 outside 0<=k<=n. TMR-2/013 states the exact counts of SAT-forcing observation sets of size five and six:

$$
N_5(a)=\sum_{j,b}\binom{n_{j,b}}5,
$$

$$
N_6(a)=\sum_m\binom{f_m}2+
 \sum_{|J|=2,v}\binom{f_{J,v}}3+
 \sum_{j,b}\left[
 \binom{n_{j,b}}6+(24-n_{j,b})\binom{n_{j,b}}5
 \right].
$$

**Independent proof verdict: PROVED/RESTRICTED for this exact promise.** For any partial query Q, each row i has a nonempty subcube D_i of matching masks, with size 8,4,2,1 after 0,1,2,3 observations. An agreeing UNSAT permutation is a perfect system of distinct representatives for the D_i. By Hall's theorem, SAT is forced iff some s-row set has union size less than s. With at most six queries, all possible Hall-deficient shapes are: (A) two identical singleton domains, demanding two fully observed duplicate masks; (B) three identical two-mask domains, demanding three identical two-coordinate projections; and (C) at least five different rows all constrained to one four-mask coordinate halfcube, demanding a five-bit certificate or one of its six-bit supersets. A and B use two and three rows, C uses at least five, so their query sets cannot overlap. Distinct halfcubes cannot each supply five members in one six-position Q. Count C's six-position extensions by choosing six within the halfcube or five within plus one outside. This establishes the two formulas without an online-continuation assumption.

An independently authored **native CPython** program, not a wrapper or peer-code import, reclassified the complete query space against all 8!=40,320 genuine UNSAT mask permutations for seven hostile tuples. It agrees with N5 and N6 everywhere tested, including the previously neglected five-bit extensions: (1,2,3,4,5,6,7,7) has N5=3 and N6=61 (1 full duplicate pair + 3 projection triples + 57 five-certificate extensions), whereas applying the balanced-only formula would give the false answer four. Independent peer promotion applies only to exact mathematics; a physical all-length 3-SAT machine was not executed.

## 3. NEW TMR5-M7-011: inclusion-minimal seven-query structure

An observation set Q is **inclusion-minimal SAT-forcing** when Q forces SAT but deleting ANY one queried sign position permits an UNSAT permutation. This is different from minimum *cardinality*: every SAT eight-mask tuple already has a certificate of at most six bits.

**Theorem candidate, pending a second agent review.** A seven-position Q is inclusion-minimal SAT-forcing iff:

1. Q observes one bit in each of seven distinct rows, leaving the eighth row unobserved.
2. Exactly four queried rows have the same observed coordinate/value (j,b) and exactly three have another observed coordinate/value (k,c), with j distinct from k.
3. The two groups of rows are disjoint. In particular the two halfcubes are on DIFFERENT coordinates, their union has exactly six masks, and no halfcube group contains five queried rows.

**Proof.** An inclusion-minimal forcing Q must violate Hall; examine a Hall-deficient row set R of size s. For s=1 no domain is empty. For s=2, two identical singleton domains use six bits and constitute a proper forcing subset. For s=3, all three domains must be contained in a common two-mask edge, so there is a six-bit forcing subset obtained by observing that edge's two fixed coordinates in each row. For s=4, each domain would need size at most three, hence two observations in each of four rows, requiring eight bits. For s=5, at most two observations exceed the one-per-row baseline; therefore at least three rows have one-bit domains. Their four-element halfcubes must all coincide for the union to have size below five. Every remaining domain must lie inside that halfcube, yielding a five-bit forcing subset. For s=6, at least five rows have one-bit domains, and union below six forces those five halfcubes to be identical, already a five-bit forcing subset. For s=8, the seven-query budget leaves an unqueried row of domain size eight. Only s=7 remains. The deficient seven rows must each be queried exactly once. Different halfcubes on the same coordinate but opposite values have union eight; two halfcubes on distinct coordinates have union six; three distinct halfcubes have union at least seven. Thus Hall fails exactly when the seven one-bit domains are drawn from at most two distinct coordinate halfcubes with different coordinates. If all seven are the same halfcube, or five or more belong to one, Q has a five-bit forcing subset. Otherwise the multiplicities are precisely four and three. Conversely four-plus-three different-coordinate halfcubes have six permitted masks for seven rows, so Q forces SAT; deleting any queried row leaves at most six rows occupying six permitted masks, and the remaining unqueried rows permit a perfect completion. Hence Q is inclusion-minimal.

**Exact new candidate count.** Let H=(j,b), J=(k,c), j distinct from k, n_H and n_J their row counts, and m_{H,J} the count of rows belonging to BOTH halfcubes. The group with four queries uniquely designates the ordered pair (H,J), avoiding double counting. Partition those four rows by i from H intersection J; the group of three must avoid them. Therefore

$$
\boxed{
M_7(a)=\sum_{\substack{j\ne k\\b,c\in\{0,1\}}}
\sum_{i=0}^{4}
\binom{m_{(j,b),(k,c)}}{i}
\binom{n_{j,b}-m_{(j,b),(k,c)}}{4-i}
\binom{n_{k,c}-i}{3}.
}
$$

Every summand counts a different set of seven physical row-coordinate query positions. This is a classification and exact count of **minimal** seven-bit query certificates, NOT the number N7 of all seven-bit forcing sets and NOT an increase in the minimum certificate complexity. The analytical Hall proof is the primary argument; finite tests below do not promote this new claim pending independent review.

**Concrete smallest distinctive fixture.** In balanced SAT tuple a=(0,0,1,1,6,6,7,7), Q=(1,4,7,10,14,17,20) uses j=1,b=0 in rows 0,...,3 and k=2,c=1 in rows 4,5,6. These two domain halfcubes have six masks total and therefore force SAT on seven rows. Each deletion admits an UNSAT completion. This tuple has N5=0, N6=12, N7=232, but **16 inclusion-minimal size-seven certificates**. The balanced even-parity double (0,0,3,3,5,5,6,6) has N6=4, N7=72, and M7=0.

## 4. Actually executed native computational audit

Published independent source: experiments/tmr/tmr5_minimal_seven_audit011.py, exact Git blob e9cc47cdc101f55bd179c5cfacf10e47b422b064, identical to the actual native Python file. Raw machine-readable result: results/raw/tmr/2026-11-13_2355_TMR5_MINIMAL_SEVEN_011_RAW.json. Each of seven fixtures ran as one separate ordinary CPython process in under four seconds, with no random seed. Each independently enumerated all 40,320 UNSAT full-mask permutations, all binom(24,5)=42,504, binom(24,6)=134,596, and binom(24,7)=346,104 query sets, and checked every deletion of every SAT-forcing seven-query set. The actual query classification **did not call Hall matching or the structural predicted-count formula**; it intersected actual compatible UNSAT completion bitsets.

| Fixture | N5 | N6 | N7 | M7 |
|---|---:|---:|---:|---:|
| Balanced projection (0,0,1,1,6,6,7,7) | 0 | 12 | 232 | 16 |
| Balanced even (0,0,3,3,5,5,6,6) | 0 | 4 | 72 | 0 |
| Prior unbalanced (1,2,3,4,5,6,7,7) | 3 | 61 | 603 | 18 |
| UNSAT permutation (0,1,2,3,4,5,6,7) | 0 | 0 | 0 | 0 |
| All equal (7,7,7,7,7,7,7,7) | 168 | 2968 | 26736 | 1680 |
| Five equal (7,7,7,7,7,0,0,0) | 3 | 103 | 1371 | 30 |
| Six equal (7,7,7,7,7,7,0,0) | 18 | 403 | 4176 | 0 |

Total: **3,662,428 actual 5-, 6-, 7-query subset classifications**, plus relevant six-query deletion tests, **zero failed assertions**. This is **COMPUTATIONAL** corroboration of exact finite mask families. Neither the original peer source, a wrapper that imports it, a symbolic RAM operation counted as a TM instruction, nor a complete physical SAT machine was executed. The compact published raw JSON preserves the exact native case counters and first seven-bit witnesses; full per-process JSON was also generated locally. No native Node test, full repository preflight or LaTeX compilation was executed here.

## 5. Integrated hostile dependency synthesis

- **TMR-1/013 CANDIDATE/CONDITIONAL:** charged indexed-input-port-to-local-machine polynomial simulation could transfer a hypothetical all-exponent local-machine result, but does not supply that result and does not carry over restricted small-space crossing bounds.
- **TMR-2/013 now independently reviewed PROVED/RESTRICTED:** the exact five/six certificate formulas require source observations, not exponential retained information or processing. New M7 minimal-cardinality distinction is CANDIDATE pending independent review.
- **TMR-3/011 CANDIDATE/RESTRICTED:** complete crossing-record splice premises concern one locally moving source head and still produce a restricted source-transport T(S+1)=Omega(Lm) result only. **TMR-3/012 remains CANDIDATE** for conditional codebooks: independently uniform disjoint blocks can have globally correlated short-code events because the codebooks depend on all outside blocks; there is still no demonstrated physical crossing realization of that correlation.
- **TMR-4/014 CANDIDATE/RESTRICTED:** a different finite correct hardwired SAT decider for each F can halt in one genuine step after a prepared state, constraining program-oblivious MAY potentials. This does not invert the fixed-A/existence-of-hard-F quantifiers and does not rule out program-tagged full-state abstractions.
- **All-agent OPEN arrow:** establish a noncircular, all-transition, both-label, same-machine processing necessity after input acquisition for EVERY fixed total uniform deterministic SAT decider and all polynomial exponents. The TMR-2 structured G_r source is efficiently decided by an eight-mask global invariant, so no abstract potential predicting superpolynomial work on it can be sound. Horn, 2-SAT, GF(2) Gaussian elimination, bounded treewidth, products, sharing, padding, renaming, auxiliaries, cache/recompute and rereading remain mandatory hostile controls for future universal candidates.

**Exact quantifier contract retained:** for every one fixed correct total A, every k>=1, C>0 and L0, the desired separation requires SOME valid F of |F|>=L0 with T_A(F)>C(|F|+1)^k. No per-length hardcoded program, small-space-only claim, oracle, nonuniform advice, proof-calculus lower bound or prescribed-DAG pebbling is substituted. All-length both-label totality and malformed input handling of a possible general SAT decider remain prerequisites, not demonstrated by these finite query tests. No claim about P=NP or P!=NP is promoted.

## 6. Sources, corpus provenance, publication and next review target

Primary originals verified: P. Hall (1935), *On Representatives of Subsets*, Journal of the London Mathematical Society s1-10:26-30, https://doi.org/10.1112/jlms/s1-10.37.26 (matching); H. Buhrman and R. de Wolf (2002), *Complexity Measures and Decision Tree Complexity*, TCS 288:21-43, https://homepages.cwi.nl/~rdewolf/publ/qc/dectree.pdf (query/certificate concepts); L. Fortnow, R. Lipton, D. van Melkebeek and A. Viglas (2005), *Time-Space Lower Bounds for Satisfiability*, JACM 52:835-865, https://doi.org/10.1145/1101821.1101822 (random-access small-space SAT exclusions, NOT arbitrary-space all-exponent separation).

Read first controlling directive research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md (SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4), then proof1.txt in complete 28,714 characters (SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343), proof2.txt in complete authentic Git blob 1,051,196 characters (SHA 930c5eeddafce656717f28055a7a9a755f44737c; ordinary file fetch blank), root main.tex in complete authentic Git blob 2,515,087 characters (SHA c9944b36cc043c7a0c1808b8ffbbacc19ea4350b), issue #3 through TMR-4/014, AGENTS.md, CODEX.md, pnp-research skill, all five latest handoffs, original TMR-2/010-/013 reports, TMR-5/010 original code and raw, TMR-3/008-/012 and TMR-4/014 reports, and relevant legacy scientific counterexample ledger. Conflicting historic agent ownership is overridden by the new TMR directive, not silently reinstated.

**TRACKERS REVIEWED; NO MATERIAL CHANGE:** proof1.txt, proof2.txt status nodes remain unchanged. Canonical root main.tex receives a strictly qualified TMR-5-owned synthesis note after standalone verification, preserving all earlier material. No schedules, task IDs or agents modified. The standalone new theorem requires TMR-2/TMR-1 independent review before final promotion.

**One next research target:** seek an all-configuration cost-sound processing potential that charges genuine unavoidable full-run work on some correct-machine-dependent 3-SAT sources AFTER allowing input copying, compact global invariants, algebraic shortcuts, arbitrary polynomial work space and recomputation. TMR-2 should first audit the s=7 Hall case and M7 intersection-count formula as a small exact mathematical review task.

END_OF_REPORT::TMR5::MINIMAL_SEVEN_011::2026-11-13_2355_PST
