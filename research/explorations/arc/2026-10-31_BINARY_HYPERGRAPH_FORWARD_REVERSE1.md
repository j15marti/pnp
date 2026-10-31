# BINARY-HYPERGRAPH-FORWARD-REVERSE1: Exact Fixed-Representation SAT Paths Versus FLMV
Date: 2026-10-31, America/Los_Angeles.
**Status:** PROVED/EXACT in the declared restricted state and move model; COMPUTATIONAL independent finite tests; OPEN any unrestricted ARC or P-versus-NP implication.

## User research idea
Encode the signed clause hypergraph as a binary input, encode each changing residual state in a fixed-width aligned binary vector, find a minimal legitimate terminal state through forward search and reverse dynamic programming, measure XOR differences and number of transitions, and ask whether FLMV time-space bounds can then give a lower bound for the computation.

The precise model distinction is vital: a shortest *explicit residual-rewriting path* is not the runtime of an arbitrary correct SAT decision program. An endpoint binary Hamming distance gives a write lower bound ONLY for a machine required to physically materialize those two fixed-layout endpoints. FLMV does not infer per-formula minimum time from that distance. It excludes certain simultaneous worst-case time/space bounds over an entire language on its specified random-access Turing model.

## Model and binary representation
Fix proper ternary clauses F with n variables, m indexed clauses, and immutable read-only source. For a clausewise-monotone input, the source incidence encoding uses one positive and one negative bit for every 3-variable support, i.e. 2*C(n,3) source bits. This source format itself is not efficient for asymptotically large sparse instances and its entire cost must be charged if physically materialized. A standard compact source would have O(m log n) bits instead.

The separate **logical working-state** vector W(rho) uses:
- 2 bits per original variable: unassigned 00, fixed false 01, fixed true 10;
- 4 bits per original clause: an active/unsatisfied flag plus 3 literal-unassigned flags; when already satisfied by any fixed TRUE literal, the entire clause record is 0000. Initially every clause record is 1111. An empty falsified clause has record 1000.

Thus B=2n+4m fixed aligned bits. One legal *logical* move assigns one unset variable; terminal SAT states are coherent partial assignments with an already fixed TRUE literal in every original clause. Invalid or falsified partials do not constitute UNSAT certificates. A general UNSAT terminal must instead be a separately authenticated global refutation or a complete decision. We do not identify logical moves with native Turing transitions.

For states a,b define d_H(W(a),W(b))=popcount(W(a) XOR W(b)); on a legal path P the **logical edit count** is D(P)=sum_{(a,b) in P} d_H(W(a),W(b)). Actual writes, source/index reads, tape head movement, initial buffer construction, failed path searches, retained ancestor state, and proof checking must be charged separately.

## Restricted exact theorem
For any *valid* duplicate-free proper clausewise-monotone 3-SAT-(2,2) source, m=4n/3, with 2n/3 positive and 2n/3 negative clauses and each variable twice per sign.

Every partial assignment whose fixed literals already satisfy **every** original clause must fix at least n/3 variables TRUE and at least n/3 FALSE. Proof: each TRUE variable can satisfy at most two positive clauses, so to cover all 2n/3 positive clauses needs t>=n/3; similarly each FALSE variable satisfies at most two negative clauses, hence f>=n/3. Therefore any path of one-variable assignments from the all-unassigned state to such a terminal takes at least k=t+f>=2n/3 *logical assignment moves*.

Under the declared W encoding, the initial 4m clause-record bits are all ones and final records are all zero; each fixed variable additionally changes exactly one status bit. The endpoint XOR distance is exactly 4m+k>=4(4n/3)+2n/3=6n. Each bit of a clause record changes at most once along any monotone assignment path, so the *cumulative logical XOR count equals this endpoint distance* for every terminal-reaching path.

These bounds are **representation/rule-specific and linear**. They neither constrain arbitrary SAT algorithms nor yield a superpolynomial lower bound. They are independent of SAT difficulty and do not supply an UNSAT refutation.

## Exact bidirectional Y6 test and UNSAT adverse control
Canonical SAT Y6: positive source clauses
(123), (145), (246), (356);
negative source clauses
-(124), -(136), -(235), -(456).
The source incidence representation has 40 bits:
`1001000000000110000000010000100000001001`.

Initial 44-bit W:
`00000000000011111111111111111111111111111111`.
Forward Dijkstra and reverse DAG dynamic programming independently obtain the same lexicographic optimum (4 logical assignments, 36 logical XOR bit changes). One optimum is
x1=0, x3=1, x4=1, x5=0 (remaining x2,x6 unassigned), with successive XOR changes 11,9,9,7.
Final W:
`01001010010000000000000000000000000000000000`.
The entire source+work fixed snapshot is 84 bits at both endpoints; the immutable source component contributes zero changes. Exhaustive enumeration of all 3^6=729 partial assignments yields 44 terminal partial assignments, only 4 requiring exactly 4 fixed variables. Exhaustive 2^6 complete assignments yields 20 SAT models. Forward search considered 470 states and 2,516 move candidates; reverse DP considered all 729 states and 2,860 move candidates. **Path length 4 is not the cost of discovering the path.**

UNSAT control H8 consists of all 8 signed ternary clauses on 3 original variables (outside canonical M22). It has 0 SAT assignments and 0 SAT-certifying partial terminals across all 3^3=27 coherent partial states. No SAT path found does NOT by itself produce a uniform UNSAT algorithm or a short proof for arbitrary inputs. Independent no-import verifier performed 3,764 checks across both sources, corroborating both forward/backward costs and all transition-bit differences.

**Physical initialization caveat:** W_0 has 4m one bits although a real work tape starts blank. A machine physically materializing W_0 must pay for those initial writes; an implicit representation can avoid them. In Y6, the 36 changes are only from the initialized W_0 to final W*. A direct source-reading solver need not store either W_0 or W*.

## Precise FLMV inference and missing arrow
Fortnow–Lipton–van Melkebeek–Viglas (JACM 2005) forbid some simultaneous deterministic time N^c and writable space o(N^d) for linear nondeterministic time on a specific random-access indexed-TM model, transferring to SAT with charged near-linear reductions and exponent slack. At c=6/5, d=23/45. Thus if one proved an actual same-machine full-SAT algorithm used at most O(N^{1/2}) writable space on all inputs, it could not also run in O(N^{6/5}) time. This does NOT give a per-instance runtime from d_H(W0,W*), nor show that a solver's space is bounded above by its endpoint distance.

For the preferred NP-complete M22 target, transferring the sharp numerical FLMV region also requires a fully charged SAT-to-target reduction/virtual indexed-bit accessor; NP-completeness alone is insufficient.

Conditional research goal: prove every correct uniform solver must execute a certain source-indexed transformation or pay an alternative equivalent resource charge while avoiding materialization, output minimization, unlimited source rereads and algorithm-specific representation changes. This bridge is OPEN and is substantially stronger than the present elementary restricted lower bound.

## Artifacts and reproduction
Complete self-contained Python producer and a separate no-import verifier were generated in the user conversation:
`/mnt/data/binary_hypergraph_bidirectional.py`,
`/mnt/data/verify_binary_hypergraph_bidirectional.py`,
`/mnt/data/binary_hypergraph_bidirectional_results.json`.
They passed in the active computation environment, but these container bytes have NOT been transferred to the GitHub repository. The numeric results in this note are replayable from those artifacts; a separate connector transfer is required for GitHub source mirroring.

## Related work
- Project UNIVERSALDAG1/2 studies semantic/DPLL/OBDD quotienting and the risk of conflating syntactic and arbitrary-solver complexity.
- Project BIT-LEDGER-CEILING120 separates full-state XOR path length and time/space, including the Hamming endpoint potential ceiling.
- FLMV, *Time-Space Lower Bounds for Satisfiability*, JACM 2005: https://lance.fortnow.com/papers/files/tst.pdf .
- Jahanjou–Miles–Viola, *Local reductions*, ICALP 2015: https://arxiv.org/abs/1311.3171 .
- Döcker, *Monotone 3-Sat-(2,2) is NP-complete*: https://arxiv.org/abs/1912.08032 .

**P versus NP remains OPEN.** No task identities, schedules, or enabled states were modified.
