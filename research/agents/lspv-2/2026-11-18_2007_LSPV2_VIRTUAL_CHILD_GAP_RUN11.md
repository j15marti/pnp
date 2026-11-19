# LSPV-2: Source-indexed virtual-CNF batching and the SAT-witness tax
Date: 2026-11-18 20:07 PST. Owner: LSPV-2 SAT-CIRCUIT REDUCTION BUILDER. Status: **PROVED/RESTRICTED + COMPUTATIONAL; unrestricted SAT/P versus NP OPEN.**

**Candidate:** Uniformly access the actual signed source clauses of shared/private block CNFs under each assignment to shared variables without duplicating every conditional child. **Falsifiers:** unsound substituted clause; uncharged source-bit access; wrong-label circuit path; an apparent n^1.33 witness bound that hides the cost of producing satisfying assignments.

## Exact virtual child lemma (PROVED/RESTRICTED)
For F(z,Y)=AND_j C_j(z,Y_j) with disjoint private Y_j, original signed proper three-literal C_j blocks of L clauses, a fixed shared assignment r and block j: introduce fresh p; append the three-literal unit (-p,-p,-p). Replace each source clause with the tautology (p,-p,p) when a shared literal is true, otherwise replace each false shared literal by p and preserve all private literals. Every original clause remains one fixed-position guest clause. Since p is forced false, **for every private assignment y, C_j(r,y) holds iff the transformed packet holds with p=false**. SOURCE and its signed literal occurrences are retained in the getter; source-read indexing arithmetic and bit encoding are charged. This is NOT an authenticated historical mixed-calculus checker and does not supply an all-input block decomposition.

With fixed-width packed blocks, original source length N=Theta(BL log N), indexed bit access O(polylog N) and O(log N) auxiliary state, a correctly implemented deterministic guest A on L-clause children with time L^p and space L^s yields the conditional charged bounds:
T_dec=O((N+R B L^p) polylog N), S_dec=O((L^s+1) polylog N).
All child calls, failed attempts, the input scan, signed transformation, final answer and indexing must be charged. On UNSAT the deterministic program actually checks one refutable child for each shared r; bare guessed blocker indices do not constitute UNSAT certificates.

**Important search/decision distinction:** To output a complete SAT witness, first find a successful r and then invoke a correct witness-producing guest W on its B blocks, locally verify each returned private assignment against the original signed clauses, and stream outputs only after each block verifies. If W uses L^q time and L^u space, T_full=O((N+RB L^p+B L^q+BL) polylog N), S_full=O((L^s+L^u+L) polylog N). A simple black-box self-reduction using only A costs B L^(p+1) extra; its search exponent is not free.

For R=n^.195, B=n^.65, L=n^.35, N=~n, attaining n^1.33 requires decision p<=97/70, direct-search q<=68/35 and writable guest exponents s,u<=10/7 (plus one n^.35 witness buffer). Naive decision-only witness self-reduction requires p<=33/35, not obtained even with a linear-time general SAT decider. This is a **restricted compiler non-implication**, NOT a lower bound on every SAT witness algorithm. Keeping all conditional child copies would cost ~n^1.195 source bits instead of the ~n packed source, but real guest input reads can still incur n^1.195 time.

## Actual source-bit circuit and packets (COMPUTATIONAL)
The tested Boolean DAG inputs were **actual** signed 3-CNF literal fields, each with two index bits and a sign bit on four variables (two shared and two private). Gates decode literal truth, enumerate all four private assignments per block, and return SAT/UNSAT, first SAT row, complete row's private witnesses and first blocker per row. AND/OR/NOT gates are charged; fixed finite private width 2 makes this an easy bounded-private source grammar, not an unrestricted solver.

| B,L | Source bits | All-row guest bits | Gates (NOT) | Depth | Source masks | SAT/UNSAT | Child replay |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2,3 | 54 | 384 | 1,411 (91) | 26 | 200 | 184/16 | 1,600 |
| 3,4 | 108 | 720 | 2,705 (161) | 28 | 120 | 85/35 | 1,440 |
| 4,6 | 216 | 1,344 | 5,193 (285) | 31 | 90 | 10/80 | 1,440 |

Totals: **410 random signed-CNF sources, 4,480 physically materialized and virtually accessed children, 284,160 byte/bit-exact guest-input probes**, with no semantic mismatch and no wrong-label supplied SAT/UNSAT path accepted. Original literal width 3 bits becomes 4 bits in guests because of forced-false p. Independent executable Node.js source audit enumerated all 512 possible signed three-literal clauses over 4 variables times 4 shared rows times 4 private assignments, **8,192 truth-equivalence cases, zero failures**, and detected deletion of the mandatory unit. The exact experimental Python source, complete raw ledgers, JS independent checker, and SHA-256 manifest are in the dated conversation reproducibility archive: LSPV2_20261118_VIRTUAL_CNF_BATCH_SEARCH_GAP_EVIDENCE.zip.

**T5 regression:** Existing H9 source-aware netlist 2,064 masks/2,060 oracle comparisons PASS. H33 124 masks/70 oracle comparisons PASS after honoring archived `pin_root=10`; invoking the older replay script with its default `pin_root=0` instead triggers a gauge assertion, not a T5 witness failure. Controls do not transfer any lower bound to arbitrary SAT.

**Correct path and time-space firewall:** SAT paths need all private witnesses and original-source verification; UNSAT paths require all shared rows plus authenticated child negatives. A free correct-polarity bit is SAT decision advice. A k-bit supplied *sound both-label* certificate yields deterministic brute-force replay time O(2^k poly(N+k) T_V), not free selection; universal branches of adaptive strategies all count. Williams's deterministic SAT ~1.80194 exponent applies at N^o(1) writable space, not N^.5. Fortnow–Lipton–van Melkebeek–Viglas's co-nondeterministic c<sqrt2 exclusion has a specific positive d(c), not asserted to be .5. Fortnow's nondeterministic-SAT exclusion is near-linear time, not the proposed n^1.33,n^.5 pair. Proof-system-specific UNSAT refutations and physical RAM computations are different resources.

**Four scientific gates:** DISJ PASS as a sanity control; relativization OPEN for claimed general-SAT transfer; simultaneous DTISP general claim OPEN; deterministic configuration counting NOT a lower-bound proof. General-CNF-to-packed-family compilation, recursive guest closure, and a search witness at the target exponent remain OPEN. P versus NP OPEN.

Sources: [Fortnow et al. 2005](https://doi.org/10.1145/1101821.1101822), [Williams 2006](https://link.springer.com/article/10.1007/s00037-007-0221-1), [Williams publications](https://people.csail.mit.edu/rrw/projects.html), [Fortnow 2000](https://doi.org/10.1006/jcss.1999.1671).
