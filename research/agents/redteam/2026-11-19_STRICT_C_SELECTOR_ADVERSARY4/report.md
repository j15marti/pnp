# STRICT-C-SELECTOR-ADVERSARY4: every critical edge is the unique bad block on some row

19 November 2026, America/Los_Angeles. Role: adversarial explicit inputs against selectors. **PROVED/EXACT restricted; COMPUTATIONAL verification PASS; unrestricted algorithmic consequence OPEN; independent peer review PENDING. P versus NP OPEN.** Existing manuscript ownership, titles, schedules and enabled states are unchanged.

## Outcome

The historical 47-tail/236-edge Mycielski fixture has been rebuilt under the canonical strict relation

\[
C(x,y,z)=[R(x,y)R(y,z)R(z,x)]\lor[R(x,z)R(z,y)R(y,x)].
\]

No historical Q head value or Q clause check was reused. Every private head was reconstructed by testing C, and every deletion assignment was checked against every original C clause.

The resulting explicit instance has 283 five-valued variables and 236 C clauses. It is clause-minimal UNSAT, passes the supplied full orientation/capacity and pentagon-distance filters, and has a verified C witness after every one-clause deletion. More strongly, deletion witness row z_e has exactly one refutable private-head block: block e. All 236 block identities occur.

Therefore any row-independent set of blocks that refutes every tail row must contain all 236 blocks. A fixed source-order scanner has critical rows requiring 1 through 236 block checks, with mean 118.5. This is a precise falsifier for row-independent bounded candidate sets and for the local filters' general completeness. It is not a lower bound for a source-aware selector: the graph and recursive deletion witnesses are deliberately recognizable.

## Recovered work and relation firewall

The exact Library artifacts `t5_strict_research.pdf` and `t5_strict_research_package.zip` were retrieved by IDs `libfile_e7c9904498148191bd1ab8141abc7a49` and `libfile_c54ef1e6d1708191832284d429b595b0`. Their workspace SHA-256 values were `c98555f85657395e450d832a0e4f9ef03ae3036a1389dbce250f6b5cfbf17633` and `8384d3892198ff3a8e8a0dd6945bd9efc20bcd1120ab6b1b393363d33c9bf5c6`.

The strict package already established:

- C accepts 30/125 ordered value triples; Q accepts 60/125 and P accepts 20/125.
- all 1,048,576 subsets of the 20 C clauses on six variables were classified;
- the 960 inclusion-minimal orientation-feasible UNSAT instances fall into four six-variable renaming types, plus the five-variable representative;
- the implemented capacity/distance filters reject all five representative records;
- private-head K6 passes the filters and is UNSAT.

This run did not repeat the completed million-subset grid. It rechecked all supplied deletion certificates for the five catalogue records with C, totaling 107 original-clause checks, and reran the exact filters on them. They are useful filter-positive controls, not counterexamples beyond the finished finite classification.

The historical Q fixture at `evidence/unpacked/t5_exact_one/redteam/mycielski_fixture.json` supplied only a provenance cross-check. Its 236 recursively generated tail colorings exactly matched the independently rebuilt tails. Its private Q heads were explicitly discarded. The strict run reconstructed 55,696 C heads and made 55,696 C clause checks. Thus Q certificates are not silently relabeled as C certificates.

`SELECTOR-ADVERSARY3` (blob `90edbe9e579fe2376e893134a372c2d04e4eefa2`) already built guarded Q/K6 layouts with a source-easy affine full-range selector. The present result does not repeat that theorem: it migrates a larger clause-critical graph control to C and proves that every one of its 236 blocks is necessary for any row-independent cover. It does not construct an exponent-compliant guarded C layout.

## Exact construction and certificate

Start from C5, whose chromatic number is three, and apply the pure Mycielski construction three times. The resulting graph G has 47 vertices and 236 edges. Mycielski's theorem increases chromatic number by one at each lift, so chi(G)=6. The construction and its chromatic-number argument originate with Mycielski [1]; a modern proof-logging treatment also states and proves the one-step increase [2].

For every graph edge e={u,v}, introduce a fresh variable h_e and the single block C(h_e,u,v). The heads do not occur in any other clause. Direct enumeration proves

\[
\exists h\, C(h,u,v) \quad\Longleftrightarrow\quad u\ne v.
\]

The forward direction holds because C assigns each pair opposite outcomes and hence three distinct values. The reverse direction is checked on the 20 ordered unequal endpoint pairs; the producer chooses the first valid head. Therefore the C formula is satisfiable exactly when G is 5-colorable, and is UNSAT because chi(G)=6.

For every edge e, the recursive constructor outputs a proper five-coloring of G-e whose endpoints of e have the same color. Direct verification shows every other edge is bichromatic. Lift each remaining edge independently to a strict-C head. The deleted clause is false for every possible head because its tails tie. Thus the formula is clause-minimal UNSAT and the displayed assignment is a complete deletion witness.

The graph's source girth is four. Its constraint-incidence girth is eight because each edge clause lies between its two source tails, while every private head is an incidence leaf. This is fixed girth, not a growing-girth result. The C primal graph contains a triangle for each clause, so no primal-girth claim is made.

## Selector theorem and its exact scope

Let the 47 tails be shared variables z and each private head be one private block. For a fixed z, block e is refutable iff z assigns equal colors to e's endpoints. Since G is not 5-colorable, every complete tail row has at least one refutable block.

**PROVED/EXACT.** Any row-independent block set T that contains a refutable block for every row must equal E(G).

Proof. If e is omitted from T, use the verified coloring z_e of G-e. Its only monochromatic edge is e. Every block in T has unequal tails and therefore a C extension, so T refutes no block on z_e. Contradiction. QED.

Consequences:

1. No constant block, proper fixed subset, or fixed shortlist smaller than 236 covers the rows.
2. On the 236 critical rows, the correct selector's image is all 236 blocks.
3. For any fixed row-independent block ordering, placing e last forces 236 local trials on z_e. The executed source order realizes costs 1,...,236.

These are restricted selector statements. A source-aware algorithm may read the 47 tail colors, find an equal graph edge, recognize the Mycielski structure, use graph coloring machinery, or exploit another compact representation. The theorem gives no unrestricted query, information, time or circuit lower bound. It also does not imply that every row must be explicitly enumerated.

## Relationship to the supplied row/block exponents

The natural private-head decomposition has 5^47 tail rows, 236 one-clause blocks and 47 shared five-valued variables. It is a control, not an instance of the promised Boolean layout R<=N^.195. Encoding the tail values into Boolean bits does not reduce the number of valid rows. Padding N to force the numerical inequality changes the source size and would have to be charged; no hardness claim may use that padding.

For an authenticated promised layout with R<=N^.195, B<=N^.65 and L<=N^.35, a child solver of time L^(c+o(1)) and space L^(s+o(1)) gives the recovered direct-scan exponents

\[
T=N^{\max(1.195,\,.845+.35c)+o(1)},\qquad
S\ge N^{\max(.35,\,.35s)+o(1)}.
\]

The proposed N^1.33/N^.5 target therefore requires c<=97/70 and s<=10/7, plus an authenticated hereditary compiler and complete child semantics. An unspecified polynomial SAT seed supplies neither the exponents nor the compiler. The present adversary shows why a row-independent shortlist is not that compiler.

Every source operation must be charged: parsing and private-owner authentication; tail-row acquisition; failed block trials; materialized C residuals; private-head reconstruction; original-clause verification; selector or full witness output; replay; and simultaneously live state. Retaining all 236 full deletion witnesses caused the producer's measured Python heap to peak at 17,310,416 bytes. This scope includes imported filters and result construction but excludes JSON serialization and interpreter/import baseline. It is not an asymptotic RAM space bound. A streaming implementation can use less memory and must pay recomputation/output costs.

## Correct-path and polarity audit

| Interface | SAT/deletion input | UNSAT/full input | Wrong-path soundness and costs |
|---|---|---|---|
| Uniform deterministic specialist | Emit all 283 values for G-e, then verify every surviving C clause | Emit a verified cover/selector, proof, or UNKNOWN | A recognizer failure is UNKNOWN. A known all-input completeness clock converts a one-polarity specialist into a total decider; a promise clock does not. |
| Free polarity route | The label says SAT but does not produce the deletion coloring or heads | The label says UNSAT but does not identify bad blocks or certify all rows | This is answer advice for decision. Source access, evidence construction and verification remain. |
| Supplied SAT correct path | A tail coloring plus private heads, or tails from which heads are deterministically rebuilt | Not applicable as a SAT witness | All original C clauses must be checked. A Q witness is a wrong path and must be rejected. |
| Supplied k-bit bad-block path | A bad block is inconsistent with a SAT row and rejects | For one fixed row, ceil(log2 236)=8 bits can name a candidate edge | Verify its endpoints tie. This proves one row only; it does not cover all 5^47 rows. |
| Whole adaptive/alternating strategy | Produce one consistent global witness branch | Map every universal row/history to checked evidence | Bound the whole strategy description and verify every universal branch, or retain alternation. One favored path is insufficient. |

If a sound complete verifier uses k bits, time V and writable space S, deterministic enumeration costs O(2^k(V+k+1)) time and O(S+k+log V) workspace, plus preprocessing, source reads, retained caches, replay and output. Independent per-row paths can be enumerated additively; shared adaptive consistency invalidates that factorization unless proved absent. A read-only indexed certificate is an extra input interface. Ordinary nondeterministic guesses cannot be reread after they are forgotten unless stored or reproducibly regenerated.

Free correct block choices eliminate failed local trials on this family, but leave endpoint checking and universal row coverage. Free correct SAT tails eliminate coloring search, but leave head construction, full output and verification. No lower bound on unrestricted execution survives merely from the 236 distinct correct choices.

## Simultaneous RAM exclusions and proof-system firewall

The model is a uniform random-access machine with read-only input, write-only output, charged address/work tapes and actual encoded input length N. Bounded-word RAM translations may absorb polylogarithmic factors; unbounded unit-cost arithmetic and free rereadable guess tapes are excluded.

| Polarity/model | Exact reviewed scope |
|---|---|
| Deterministic SAT or UNSAT by complementation | Buss–Williams [3], Theorem 2/table: SAT is outside DTISP(N^1.34070,N^.5), where the class uses +o(1) exponents. Thus an all-CNF deterministic (1.33,.5) algorithm is excluded. This does not exclude the promised C family. |
| Universally sound deterministic specialist complete on one full polarity with known cap | The same deterministic exclusion applies after capped conversion. It does not apply to an incomplete/promise-only specialist. |
| Nondeterministic UNSAT / co-nondeterministic SAT | FLMV [4], Corollary 6.5: NTIME[N] is not contained in coNTISP(N^c,o(N^((1+c)/c^2-c))). At c=1.10 the displayed space exponent is .635537..., so a .5-space statement follows with strict slack and the stated near-linear reductions. At c=1.33 the exponent is negative and gives no square-root-space exclusion. |
| Nondeterministic tautology/UNSAT | Diehl–van Melkebeek–Williams [5], Theorem 2: c^2 d<4 implies that for some e>0 both a time-N^c and a time-N^d/space-N^e nondeterministic tautology algorithm cannot coexist. With c=d the threshold is cube-root(4), about 1.587401. The theorem does not identify e as .5. |
| Nondeterministic SAT | No matching (1.33,.5) exclusion follows from these NO-side theorems. Supplying a rereadable assignment changes the certificate-access model. |
| Resolution/one-hot C encoding | The strict package records sparse C families with linear resolution width and exponential resolution size under its 5N-variable, 11N+95M-clause encoding. This constrains that proof system only. No polynomial simulation by arbitrary RAM algorithms is assumed. |

The fixed 283/236 Mycielski control has a short recognizable mathematical UNSAT certificate. It is not evidence for intrinsic machine hardness. The package's asymptotic resolution families and the current easy critical fixture serve different purposes and are not conflated.

## Executed evidence

Producer: `strict_c_selector_adversary.py`, standard library plus NumPy already required by the supplied filter script. Seed field 202611190056; the construction itself is deterministic.

- relation counts independently checked: C/Q/P = 30/60/20;
- 236 recursive deletion tail colorings constructed;
- 55,696 source-edge checks show exactly one monochromatic edge per row;
- 55,696 strict-C private heads reconstructed;
- 55,696 original strict-C clause checks, with exactly the deleted clause failing;
- all 236 unique selector outputs realized;
- supplied orientation/capacity and distance filters pass the complete 283-variable source;
- five catalogue representatives and all displayed deletion witnesses rechecked with 107 C checks;
- historical Q tails match 236/236; historical Q heads reused 0.

The producer completed before JSON serialization in 3.57 seconds on this host. Raw SHA-256 is `6e14a93c1360caa0cb56bc52654be01512737e24cfadfaa8f4b5edd64c8d6fce`; script SHA-256 embedded in raw data is `f7fbf2037a32a8491920abda58105682e17cdcf58bf7bb9dc693ce09a5da8a43`.

A separate checker uses an explicit 5x5 win matrix and imports neither the producer nor the supplied filters. It rechecked all 236 assignments and 55,696 C clauses, all unique selector identities, the local C count and catalogue-filter status: PASS. Auditor SHA-256 is `b67ccff3a26991a50015949ecdb1d12419c44c19b6a0cadcbbdf6e28332949d5`. This is a separate implementation by the same author, not independent peer review.

## Status ledger and next blocker

| Status | Result |
|---|---|
| PROVED/EXACT | Strict-C private-head projection to graph 5-coloring; clause-minimality of the explicit 283/236 instance; all-block necessity for any row-independent cover. |
| COMPUTATIONAL PASS | Direct C deletion witnesses, local-filter execution, small-catalogue certificate recheck and same-author independent audit. |
| FALSIFIED | Orientation/capacity/distance completeness in general; a proper row-independent block shortlist; silent migration of Q heads/certificates to C. |
| CONDITIONAL | Any use inside the promised N^.195/N^.65/N^.35 Boolean layout; compiler, authentication and model transfer costs. |
| OPEN | A source-computable selector for arbitrary critical/high-girth C inputs within the requested bounds; growing-girth critical-promise hardness; unrestricted time lower bounds; independent peer review. |

DISJ: PASS, because no information lower bound is claimed. Relativization: no separation claimed. Simultaneous DTISP: the same execution's resources are charged and the unrestricted transfer remains blocked. Deterministic configuration counting is an upper-bound consistency check only. Natural Proofs, algebrization, monotone circuits and oracle-query lower bounds are not used.

The next blocker is a source-aware selector theorem that handles arbitrary intrinsic critical/high-girth C instances, or a proved reduction placing such instances into the promised polynomial-row layout. It must outperform the legal graph-recognition, coloring, algebraic, dynamic-programming and compact-strategy routes while paying acquisition and witness transport. This explicit fixture cannot supply that theorem because its recursive certificate is easy.

## Primary sources

[1] J. Mycielski, *Sur le coloriage des graphes*, Colloquium Mathematicum 3 (1955), 161–162, DOI 10.4064/cm-3-2-161-162, https://eudml.org/doc/210000 .

[2] J. Gocht et al., *End-to-End Certified Graph Colouring*, CP 2026, section 5 and Proposition 4, https://drops.dagstuhl.de/storage/00lipics/lipics-vol379-cp2026/html/LIPIcs.CP.2026.21/LIPIcs.CP.2026.21.html . Used as a modern primary proof-logging reference for Mycielski lower-bound certificates.

[3] S. Buss and R. Williams, *Limits on Alternation-Trading Proofs for Time-Space Lower Bounds*, Theorem 2/table, https://eccc.weizmann.ac.il/report/2011/031/ and https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/samCCC-cr.pdf .

[4] L. Fortnow, R. Lipton, D. van Melkebeek and A. Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, Corollary 6.5, https://lance.fortnow.com/papers/files/tst.pdf .

[5] S. Diehl, D. van Melkebeek and R. Williams, *A New Time-Space Lower Bound for Nondeterministic Algorithms Solving Tautologies*, Wisconsin TR1601, Theorem 2, https://research.cs.wisc.edu/techreports/2007/TR1601.pdf .
