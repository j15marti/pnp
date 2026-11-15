# Agent Research Instructions: SAT Lower Bounds, Compression, and P vs NP

Date: 2026-11-15, America/Los_Angeles.
Status: user-authorized coordination revision. P versus NP remains OPEN.

## Mission and precedence

Focus all five TMR agents on the intersection of tensor/algebraic compression, time-space tradeoffs, and circuit lower bounds. Pursue the three tracks below with falsification-first formalization and empirical tests. This directive supersedes conflicting scientific priorities in the earlier Allender-first, fusion-first, MCSP-first and legacy LSPV allocations. Preserve useful earlier evidence and safeguards; Allender/MajMajSAT and fusion remain supporting tools when an explicit quantitative connection serves these tracks.

Read this directive FIRST, then current root proof1.txt, proof2.txt, main.tex, all TMR handoffs, relevant original reports/code/data, issue #3 and repository protocols. Preserve the five identities, titles, enabled states, ownership and hourly Pacific offsets :00/:12/:24/:36/:48. Do not create, duplicate, revive, disable or reschedule agents.

Several equations in the user's pasted directive arrived as missing object characters. The statements below are explicit mathematical reconstructions, not claims that the original missing symbols were recovered. Unrecoverable target formulas are not assumptions. Distinguish n variables, m clauses, N encoded input bits, t machine steps, s workspace bits, and circuit gates versus wires throughout.

## 1. Known dead-ends: no routine cycles without a new ingredient

1. **Unchanged alternation trading.** Buss-Williams establishes optimality of c=2 cos(pi/7), approximately 1.80194, for its specified deterministic SAT alternation-trading rules in the n^{o(1)}-space regime [1]. Do not spend cycles searching the same rules for larger c. This is not a theorem against every use of diagonalization, every oracle argument, or genuinely new speedup rules. State exactly which rule or hypothesis a proposed escape changes.
2. **Extrapolating small-space bounds to linear space.** Do not insert S(N)=Theta(N) into a theorem requiring N^{1-epsilon}, or treat historical FLMV/Williams/Santhanam curves as superlinear unrestricted-SAT bounds. Reconstruct the chosen curve and its endpoint with exact model/quantifiers [2]. The operating prohibition concerns these routes, not a universal claim that all machine-specific linear-space lower bounds are trivial.
3. **Static variable-cut rank alone.** Define DISJ_k(x,y)=product_i(1-x_i y_i). Its 2^k-by-2^k matrix is the k-fold tensor product of [[1,1],[1,0]], hence has rank 2^k over every field. Yet AND_i(NOT x_i OR NOT y_i) has linear size/wire count and depth two with unbounded fan-in (negations at inputs). It is a 2-CNF and thus also width-at-most-three CNF; exact-three conventions require explicit gadgets. This is a direct algebraic control, not evidence of hard 3-SAT instances. Static rank cannot certify general circuit hardness. Keep the assignment relation of one formula distinct from SAT as a function of encoded formulas.
4. **Retuning the unchanged Williams simulation.** Cook-Mertz Tree Evaluation uses O(d b+h log(d b)) space. Williams reduces time t to constant-arity instances with h=O(t/b) and obtains O(sqrt(t log t)) space [3,4]. Optimizing this same expression again is not a new exponent improvement. At the scale h proportional to t/b, b h is proportional to t; the logarithm must also be charged. This is a limitation of the current expression, not a lower bound against all simulations. Do not iterate a simulation using its old time bound after its runtime has blown up.
5. **Padding PSPACE halting languages.** Fixed polynomial lower bounds for padded/space-bounded halting languages do not imply a superpolynomial bound for one fixed SAT language. Track the reduction direction, encoded size and overhead. A reduction L to TQBF transfers only the exponent surviving its blowup; SAT to TQBF transfers no TQBF lower bound down to SAT. Do not repeat this route without a new tight transfer theorem.

## 2. Priority research tracks

### Track A: bridge dynamic fan-out and the circuit-to-cut gap

Goal: find a structural invariant or decomposition with a proved relationship to the cost of general circuits for SAT, while excluding DISJ false positives. Restricted results are valuable when labeled precisely.

- Compare exact contractions, Walsh-Hadamard/Fourier bases where defined, and explicitly specified finite-field embeddings on small 3-CNF benchmarks. Test expander families and structured controls. Record bond dimension chi, intermediate tensor shape, rank field/characteristic, coefficient bit lengths, factorization cost and peak space.
- Invertible transformations acting separately on the two sides of a cut preserve matrix rank. Any claimed gain must identify sparsity, a changed decomposition, nonlocal operations or another resource, and pay for it. Walsh-Hadamard is not invertible in characteristic two; do not silently identify real/complex Fourier rank with F_2 rank.
- Explore multiple cuts and decomposition hierarchies, including competing tree orders and adaptive state-dependent choices. Charge finding the basis, decomposition, strategy changes and failed attempts. Large width for a prescribed representation is not a lower bound for every representation or algorithm.
- For decision SAT, test Valiant-Vazirani XOR isolation with its random bits, success probability, repetitions, encoding size and uniqueness promise [5]. It is not a free deterministic reduction. A uniquely satisfying assignment has indicator tensor equal to a product of coordinate delta functions, so every full-assignment flattening has rank one (zero if unsatisfiable). A meaningful candidate must identify another object, such as intermediates, and justify why arbitrary solvers must incur its cost. Exact counting, parity and decision remain distinct.
- Start with explicit AC^0/ACC^0 depth and gate restrictions, bounded-width branching programs with a declared read model, and tree-like OBDDs with a declared order. Existing restricted lower bounds are baselines. Do not infer general circuit lower bounds by unfolding a shared circuit into an exponentially larger formula.
- Controls: DISJ, Horn, 2-SAT, affine/XOR with Gaussian elimination, bounded-treewidth DP, equality, autarkies, independent products, padding, auxiliary variables, alternative encodings, cached/shared computation and recomputation.

### Track B: sublinear-in-height Tree Evaluation and space compression

Goal: improve the square-root space exponent through a new height-sensitive evaluator or reduction, while retaining a complete runtime ledger. Candidate targets include cube-root space, arbitrarily small positive powers, and polylogarithmic space; these are goals, not known results.

Conditional design calculation: if constant-arity evaluation and the entire implicit reduction can be performed in soft-O(b+h^alpha) space with h=O(t/b), balancing gives soft-O(t^{alpha/(1+alpha)}) space. For desired exponent 0<rho<1/2 this template needs alpha=rho/(1-rho); rho=1/3 needs alpha=1/2. This is an algebraic budget conditional on ALL remaining costs, not an established improved evaluator. Include implicit-node generation, addresses, graph descriptions/enumeration, arithmetic, access routines and input bookkeeping before claiming a simulation.

Williams notes that simulations TIME[t] contained in SPACE[O(t^epsilon)] for every epsilon>0 would imply P != PSPACE [3]. That would not by itself prove P != NP. Check all uniformity and constructibility conditions. Polylogarithmic targets must respect input/address costs and the deterministic configuration-count gate.

Track time and space for the SAME simulation. A space-only inclusion or exponential-time evaluator cannot be inserted into a polynomial-time FLMV forbidden region. No improvement by reusing an uncharged simulator inside itself.

### Track C: #SAT speedups and the algorithmic method

Goal: use precisely quantified #SAT/Circuit-SAT speedups to obtain the circuit or formula lower bounds warranted by algorithm-to-lower-bound theorems [6,7].

- Audit the October 2026 OpenAI and Anthropic manuscripts, proof artifacts, errata and formalization scope at pinned revisions [8,9]. They report subexponential fixed-width counting algorithms. Reconstruct the relevant batching, interpolation and tensor mechanisms instead of assuming every advertised bound or prose statement has been formally checked.
- Charge wire count, degree, interpolation points, coefficient growth, field size, exact bit operations, recursive expansion, auxiliary variables and recovery. Separate existence of a compression from its uniform construction and evaluation.
- Explore whether stronger compression gives a faster algorithm for the exact circuit/formula class in a lower-bound theorem. A 2^{o(n)} #3-SAT result does not automatically become a fast algorithm in the original input count for arbitrary polynomial-size circuits: Tseitin-style encodings can introduce variables proportional to gate/wire count.
- Reconstruct the Williams and Bathie-Williams quantitative premises and actual target class. Distinguish NEXP/ACC conclusions from formula/depth results for other classes. Faster than 2^n is not a sufficient standalone specification; savings and circuit-size range matter.
- Investigate whether a hypothesized polynomial-time #SAT/Circuit-SAT algorithm can yield a contradiction using an NP-level argument, instead of only a larger-class hierarchy. This is OPEN. NP is a class, not an unnamed hierarchy theorem: specify the hierarchy, complete language, uniformity, reduction and resource bounds. Decision Circuit-SAT in P is equivalent to P=NP, not an already contradictory assumption. Exact #SAT in FP is stronger and also must not be rejected by an assumed conclusion.
- Report 2^{o(n)}, quasipolynomial and polynomial time separately. Neither a subexponential algorithm nor a fixed superlinear lower bound settles P versus NP.

## 3. Mandatory verification gate for EVERY candidate lemma

Give PASS, FAIL, OPEN, or NOT APPLICABLE WITH REASON for each gate. A candidate can be explored with OPEN gates, but cannot be accepted/escalated as an unrestricted separation until every load-bearing gate closes.

1. **DISJ sanity.** Substitute DISJ_k and its linear-size depth-two circuit. If the proposed implication falsely gives a superpolynomial general circuit or runtime lower bound, reject that implication. Large rank alone may be correct while its transfer is false. Include tractable controls appropriate to the exact claim.
2. **Relativization.** Identify whether each step and the final separation survive arbitrary oracle access. A fully relativizing P-vs-NP separation conflicts with Baker-Gill-Solovay [10]. Relativizing intermediate lemmas are not automatically invalid. For a claimed nonrelativizing step, locate the exact oracle-sensitive construction. Retain algebrization and Natural Proofs audits when relevant.
3. **Simultaneous DTISP.** For any FLMV contradiction, provide one machine/execution with both T(N) and S(N) inside the strict forbidden region, including reduction generation, accesses, arithmetic, retained data and all simulation overhead. Separate machines attaining time and space separately do not suffice. For networks use total sequential work and aggregate live space, not span and per-processor workspace.
4. **Configuration counting.** For a fixed deterministic total decider with read-only input length N, finite alphabet, constant tapes, and s(N) writable bits/cells up to constant-factor encoding, count complete configurations including heads/control. The standard bound is C(N,s) <= 2^{O(s+log N)}. A halting deterministic run cannot repeat a full configuration, so T <= C; if s>=log N, T <= 2^{O(s)}. This is an upper bound, never a lower bound on necessary work. Account for output storage/head state if relevant. It does not automatically bound runtime of randomized or quantum machines: almost-sure halting can have unbounded stopping times, and quantum states require different analysis.

## 4. Five-role ownership

### TMR-1 / PNP Machine Model Lead
Track C and cross-track theorem architecture.
Own the algorithm-to-lower-bound implication ledger and precise hierarchy target. Audit the October 2026 #SAT manuscripts and formalized statements at pinned revisions. Derive one fully charged transfer from a specified #SAT/Circuit-SAT speedup to a specified circuit/formula lower bound, or exhibit the exact missing hypothesis. Compare an NP-level target with the actual NEXP, E^NP or other source conclusion. Coordinate Tracks A/B without assuming their bridges.

### TMR-2 / PNP Information Necessity
Track A: dynamic fan-out and multi-cut invariants.
Own exact tensor/basis/rank experiments and the DISJ control. Specify whether the object is a fixed formula's assignment indicator, a partial contraction, or the SAT decision function on encoded formulas. Compare expander and structured 3-CNFs using exact arithmetic, alternative contraction trees, cheap algebra and compact encodings. Audit XOR isolation including the unique-solution rank-one control. First deliverable: reproducible benchmark plus a precise candidate invariant or smallest falsifier; no static-rank-to-general-circuit inference.

### TMR-3 / PNP Time-Space Tradeoffs
Track B: Tree Evaluation and simultaneous resource budgets.
Own the block-respecting reduction, Tree Evaluation height dependence and same-execution time/space ledger. Reconstruct the source bounds, account for implicit node access and graph enumeration, and derive a conditional budget for a genuinely improved height term. First deliverable: exact exponent/overhead calculation and one bottleneck lemma or counterexample. Do not retune the unchanged square-root formula or compose time-blowing simulations as if time were free.

### TMR-4 / PNP Cost-Sound Abstraction
Tracks A/C: circuit-to-cut transfer and restricted models.
Own the bridge between adaptive computations/circuits and proposed multi-cut or tensor invariants. Begin with explicitly defined restricted classes, such as AC^0, ACC^0, bounded-width branching programs or tree-like OBDDs, and charge sharing, fan-out, rereading, conversions and decomposition discovery. Audit interpolation/batching compression and circuit-to-CNF wire blowup with TMR-1. First deliverable: a model-scoped transfer lemma with exact costs, or a legal cheap circuit/execution falsifying it. Keep unrestricted transfer OPEN.

### TMR-5 / PNP Machine Bottleneck Redteam
Independent verification across A/B/C.
Own the four mandatory gates, independent reproductions, source-version checks and final synthesis. Attack DISJ false positives, rank invariance under local bases, unique-solution rank collapse, hierarchy/class mismatches, reduction blowup, deterministic configuration assumptions and same-execution DTISP claims. First deliverable: independently verified surviving lemma or minimal counterexample plus ranked dependencies and one next target. Preserve the existing synthesis ownership rules.

## 5. Continuing safeguards and every-run output

Preserve adaptive, state-dependent solver behavior and different SAT/UNSAT measures without presupposing the answer. Charge parameter discovery, selection, switching, failed attempts, sharing and peak space. Unknown legal operations remain conservative MAY; compact algebra and real cheap paths cannot be excluded to manufacture hardness.

The Allender directive remains a scoped source/calibration reference: research/coordination/2026-11-15_ALLENDER_MAJMAJSAT_FIVE_AGENT_INTEGRATION.md. Keep MajMajSAT majority denominators/ties, correct reduction direction, small-space quantifiers, and the separate bounded-error quantum simulation attribution. No automatic transfer from P=NP to exact majority counting or to a near-linear/sublinear-space implementation.

Historical /341 remains FAIL as a full logical UNSAT authority and /386 remains RESTRICTED. No silent repair or promotion. Preserve quantifier order and uniformity; a restricted proof-system/circuit lower bound is not an arbitrary SAT-algorithm lower bound.

Each run:
1. State one precise candidate, exact model/quantifiers and 2-4 falsifiers.
2. Review relevant current corpus originals and primary literature; distinguish duplicate or superseded work.
3. Prove, construct, falsify or independently reproduce one substantive item.
4. Publish the four-gate table, resource ledger, strict proof status and one next lemma.
5. Write a new Pacific-timestamped report under the existing research/agents/tmr-i/ path, separate executable code/raw data and update handoff.md. Record seeds, exact fields, instance encodings and code/source revisions. Keep individual Python stages about 30 seconds or less.
6. Verify full readback and use the existing issue #3 handoff practice. Shared tracker/main edits require complete current contents+SHA, ownership preservation, conflict-safe merge and full readback. Only verified material changes warrant edits; otherwise record TRACKERS REVIEWED; NO MATERIAL CHANGE.

Allowed research statuses remain PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED. Finite tests are COMPUTATIONAL. P versus NP remains OPEN.

This file changes coordination, not mathematical proof status. Repository-wide research preflight, experiments and manuscript formalization builds were not performed for this instruction revision; they remain duties of substantive research runs.

## Primary source entry points

[1] Buss and Williams, Limits on Alternation-Trading Proofs for Time-Space Lower Bounds (CCC 2012; journal version): https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf

[2] Fortnow, Lipton, van Melkebeek and Viglas, Time-Space Lower Bounds for Satisfiability (JACM 2005): https://lance.fortnow.com/papers/files/tst.pdf
For related historical theorem variants, locate the original Williams 2007 and Santhanam 2001 statements before using their endpoints.

[3] Ryan Williams, Simulating Time With Square-Root Space (2025): https://arxiv.org/abs/2502.17779 (Theorem 1.1, Theorem 2.2, block-respecting reduction and Section 5).

[4] Cook and Mertz, Tree Evaluation Is in Space O(log n log log n) (STOC 2024), Theorem 7: https://doi.org/10.1145/3618260.3649664 . Williams [3] restates the parameterized evaluator.

[5] Valiant and Vazirani, NP Is as Easy as Detecting Unique Solutions (1986): https://ics.uci.edu/~vazirani/ValVaz.pdf

[6] Ryan Williams, Non-Uniform ACC Circuit Lower Bounds (JACM 2014, online 2013): https://people.csail.mit.edu/rrw/acc-lbs-journal-final.pdf

[7] Bathie and Williams, Towards Stronger Depth Lower Bounds (ITCS 2024): https://doi.org/10.4230/LIPIcs.ITCS.2024.10

[8] OpenAI, The Exponential Time Hypothesis is False (17 October 2026, revised 25 October 2026), manuscript and scope artifacts: https://github.com/openai/math/tree/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026

[9] Anthropic/Claude, A 2^{o(n)} Time Algorithm for 3-SAT (October 2026), paper and Lean statement/proof map: https://github.com/anthropics/formal-math/tree/main/eth

[10] Baker, Gill and Solovay, Relativizations of the P =? NP Question (1975): https://doi.org/10.1137/0204037

END_OF_DIRECTIVE::SAT_COMPRESSION_CIRCUITS_2026_11_15
