# TMR-5/056: independent quantitative source-input charge and pinned-kernel scope
2026-11-15 19:50 PST. Owner TMR-5. End-to-end Track C, named dependency **C1e-INPUT-COST-ABSORB**. Scientific status **PROVED/EXACT restricted** for the elementary inequality; numerical checks **COMPUTATIONAL**. Lean theorem **FORMAL SOURCE CLAIM**, independent local kernel replay **OPEN**. P vs NP **OPEN**.

## Candidate stated before source review; quantifiers
For **every** integer k>=1, n>=4 and every syntactically promised k-CNF phi with m>=2 distinct ordered clause lists, at most k literals per clause and all n variables occurring, write its *actual* pinned Anthropic/Mathlib finite-stack input using encInput(k,phi). Put
w=floor(log2(2n))+1, B=k+n+2+mk w, L=log2 n,
E_m=km/sqrt(log2 m), E_n=k^2 n log2(log2 n)/sqrt(log2 n), E=min(E_m,E_n).
Candidate: the full authentic input B is uniformly bounded by 2^(8E), with constant **independent of k**, so loading and decoding the real finite-stack word does not invalidate the formal exponential bound after a fixed-machine standard-TM translation.

Falsifiers: (1) a legal promised formula with B>2^(8E); (2) an uncharged unary k/n, slot bit-order, or 2n slot; (3) using a raw m-count without NoDup or n<=km without AllOccur; (4) conflating an input-length upper bound with a polynomial-time circuit-to-SAT compressor or an NP lower bound.

## Exact all-promised-input lemma and proof
**Theorem.** For every promised formula above, B<=2^(8E). This is a *uniform input-encoding cost lemma*, not a #SAT algorithm or lower bound.

The pinned definition is exactly
encInput(k,phi) = 1^k 0 1^n 0 followed by m groups of k literal slots, each w bits low-first, where 0 denotes an absent slot and 2i+1/2i+2 the negative/positive literal. Consequently B=k+n+2+mk w, not an assumed unit-cost representation. AllOccur implies n<=km, and injectively padding each distinct ordered clause with zeros to k slots proves m<=(2n+1)^k from NoDup.

Set x=km>=n>=4. Since k<=x, n<=x and w<=log2 n+2, we have B<=x(log2 x+5)<=x^3. The last inequality holds for x>=4. Thus log2 B<=3log2 x.
For t=log2 x>=2, 2^t>=t^(3/2) (differentiate log[2^t/t^(3/2)] to locate its minimum at t=3/(2ln 2), where the ratio exceeds one). Therefore
log2 B <=3log2 x <=3x/sqrt(log2 x) <=3km/sqrt(log2 m) <=8 E_m.

For E_n set y=log2 n>=2. By NoDup and log2 k<=k,
log2 B<=3log2(km)<=3k[1+log2(2n+1)]<=3k(y+3)<=7.5ky.
Also 2^y>=y^(3/2), log2 y>=1, k>=1, so E_n=k^2 2^y log2 y/sqrt y >=k^2 y>=ky.
Hence log2 B<=7.5E_n<=8E_n. Both upper bounds hold, giving log2 B<=8 min(E_m,E_n). QED.

**Scope caveat:** The bound holds for legal promised inputs. A malformed *unpromised* source can have arbitrary padding; a total parser must still pay to read it. No extra assumption is made about all invalid strings. The formula's exact count can require n+1 output bits, and n+1<=B; it too fits the same charge.

## End-to-end integration into C1a-C1e
The exact source-to-output chain is encoded shared-gate DAG -> paid authentication -> functional Tseitin with one extension per original input -> paid NoDup/AllOccur/small-case totalizer -> low-first k-CNF word of length B -> pinned MainResults.mainTheorem FinTM2 exact counter (**conditional on upstream proof term and kernel**) -> fixed physical locally headed multitape simulator -> low-first n+1-bit exact result.

For one **fixed** finite-stack machine M satisfying finiteness of every stack alphabet, the independently stated TMR-1/058 interpreter costs O_M(B+t+1) time and O_M(B+t+1) live workspace, on the same realization. If the pinned time guarantee is t<=floor(2^(C E)), the explicit absorption gives
T_physical <= A_M(B+t+1) <= 3A_M 2^(max(C,8) E)
and S_peak <= A'_M(B+t+1) on that same run.
For each fixed-degree source normalizer/converter polynomial P(B), P(B)<=2^(8 deg(P) E) times a fixed coefficient: no hidden variable exponent in k is needed. The output bits and all stacks are included.

This is a *transfer of an upper time bound*, never a forbidden time-space lower bound. When k is fixed, E_n=o(n), so this preserves the conditional standard-TM subexponential 3-SAT/#3-SAT conclusion. It gives no time subexponential in original q when a circuit has G=q^4 live gates, since the CNF has q+G variables, and no NP-level hierarchy separation follows.

## Exact upstream source/version scope
Direct connector reads, pinned Anthropic commit **16a5ce41304fcdaea4e0be7c132e1c361dc26da5** (2026-10-27): eth/MainResults.lean blob **1c62a550fa1e4cbec65bb7112f92ad67589afddc**, eth/Solution.lean blob **176892178e49792ae41368c13bb4973bae035b29**, eth/proof/maintheorem/CountedRoute/Main.lean, eth/lean-toolchain Lean **4.33.1**, eth/scripts/PrintAxioms.lean blob **cb31f549acbce8de837f111979acfdd9836c8411**, README, upstream GitHub Actions run **40442388505** (reported success for exact head revision). The definitions encode exact 'm>=2, n>=4, AllOccur, IsKCNF, NoDup' promises, k unary and n unary, and finite alphabets. The source text itself distinguishes the formula statement from unformalized textbook simulation.

The pinned script commands #print axioms for MainResults.mainTheorem and MainResults.ethIsFalse and the README reports standard axioms [propext, Classical.choice, Quot.sound]. **This run did not execute Lean, lake, nanoda, #print axioms, an independent kernel, or any purported full proof.** Original upstream success is provenance evidence, not an independent build. The four source-to-consequence arrows remain conditional on their actual model and hierarchy premises.

## Actual finite numerical and byte-encoding replay
Executed local CPython 3.13.5, no random seed, revision **tmr5-encoding-absorption056.v1** (exact source at experiments/tmr/tmr5_encoding_absorption056.py), 252,900 tuples n=4..128, k=1..32, legal necessary m ranges up to m<=(2n+1)^k; 25 constructed distinct-clause, all-variable-occurring low-first encodings were decoded back to their literal lists. 1,517,500 assertions, zero failures. The maximum sampled log2 B/E was 1.918474302, for n=4,k=1,m=9; this is *not* an optimal constant or a proof. Huge tuple m extremes are necessary-condition syntactic parameter controls, not a claim that every extreme tuple has an attainable exact CNF. Raw data saved separately. No local pnp checkout; repository preflight, LaTeX and pinned Lean builds were not run.

## Four mandatory gates
| Gate | Verdict and justification |
|---|---|
| DISJ sanity | **PASS restricted.** The lemma is an input-length upper bound for every promised formula, independent of semantic cut rank. DISJ retains its cheap circuit and 2-CNF; any general rank-hardness transfer remains FAIL. |
| Relativization | **PASS intermediate only.** Arithmetic source-length bounds relativize, but no separation is asserted. A future NP circuit implication needs an actual nonrelativizing arrow, and algebrization/Natural Proofs audits remain OPEN. |
| Simultaneous DTISP | **PASS restricted upper ledger**, physical time and peak workspace from the same standard-machine simulation. No strict forbidden DTISP region is reached; an unrestricted separation remains OPEN. |
| Configuration counting | **PASS upper-bound safeguard.** For total deterministic read-only-input models T<=2^O(S+log B); this does not infer work hardness or automatically constrain quantum/randomized runs. |

Controls: no basis/rank argument; unique-assignment indicator rank-one, Horn/2-SAT, affine/Gaussian, bounded-treewidth, equality, products, autarkies, padding, selector projections, auxiliary count-normalizers and compact alternative algorithms remain legal. Any future circuit conversion pays live gates and wires. /341 remains FAIL as full UNSAT authority, /386 RESTRICTED.

## Ranked end-to-end dependencies and one next target
1. **TMR-1 C1 source/compressor/solver/hierarchy:** This run independently closes explicit promised-input bit-length absorption. Functional Tseitin, promise normalizer and finite-stack physical interpreter survive restricted reviews. **Independent pinned kernel proof/axiom replay remains OPEN**; exact hierarchy consequence is conditional and E^NP, mildly superlinear infinitely often, not NP or superpolynomial.
2. **TMR-4 D4 cost-sound compiler:** Current /059 authentic shared-DAG to OBDD gate/long-edge spill survives at restricted source frontier; arbitrary equivalent-circuit necessity and low-congestion search OPEN.
3. **TMR-3 C3 checkpoint provider/evaluator:** Authenticated special-source executions and nonaffine streaming shortcuts survive; general adaptive provider plus improved height-sensitive evaluator OPEN.
4. **TMR-2 D2 dynamic invariant:** Shared-edge cycle quotient/AND-DAG exact count survives restricted original encodings; OR/XOR/general-source dynamic necessary-cost invariant OPEN.

**ONE next dependency:** independent pinned Lean 4.33.1 + Mathlib build, execute PrintAxioms and independent nanoda kernel at commit 16a5ce4, then audit FinTM2 fixed-step standard-machine semantics against this charged input bound. The full valid-formula ordinary-TM transfer remains CONDITIONAL until that trust gate closes. The proof has no P-versus-NP consequence without a new class-matched reduction.

## Publication and provenance
Artifact paths: this report; experiments/tmr/tmr5_encoding_absorption056.py; results/raw/tmr/2026-11-15_1950_TMR5_INPUTABSORB056_PY_RAW.json; owned root main5_PNP_MACHINE_BOTTLENECK_REDTEAM.tex; compact tmr-5/handoff.md. Original witnesses and historical files remain untouched.
