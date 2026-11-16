# TMR-5/058 | 2026-11-16 06:48 PST | Worst-case minimum-derivation bridge red team

Role: TMR-5 / PNP Machine Bottleneck Redteam (scheduled :48 slot; the stored prompt calls it "Independent Proof Red Team"). Authority: END_TO_END_AGENT_MANUSCRIPTS, with the SAT-compression scientific guards. P versus NP is **OPEN**. No peer manuscript, retired tracker, historical root file, agent identity or schedule was touched.

## 1. Target

The stored research prompt fixes a shared objective. Let R be a fixed sound and complete refutation system for CNF, with a cost measure cost_R (size, or size plus charged state for the multisign hypergraph DAG calculus). Define

    W_R(N) = max over UNSAT F with |<F>| <= N of  min over R-refutations pi of F of cost_R(pi).

The **bridge** is Bridge(R): SAT in P implies W_R(N) <= poly(N). The plan is Bridge(R) plus a superpolynomial lower bound LB(R), giving P != NP.

What the prompt gets right: taking the minimum over all derivations is a valid lower-bound quantifier. Search cost is not charged, and leaving it out only makes the minimum smaller. That point stays as stated. This run attacks the **transfer arrow**, the load-bearing dependency of the selected pipeline:

    encoded 3-CNF F -> multisign DAG hypergraph -> R-derivation of bottom -> min cost -> W_R(N) -> [Bridge(R)] -> P != NP.

**Candidate tested:** there is a fixed R for which Bridge(R) is strictly easier than P != NP, while LB(R) is strictly easier than NP != coNP.

**Falsifiers stated before the search:**

- F1: for every R with a known LB(R), Bridge(R) is logically equivalent to P != NP.
- F2: no relativizing proof of Bridge(R) exists for any R with LB(R) true.
- F3: the known "hard" 3-CNF families collapse in algebraic or cutting-plane reasoning. A lower bound for a weak R therefore says nothing about the user's combined system.
- F4: making R strong enough for Bridge(R) to become plausible puts LB(R) in Frege/EF territory, where lower bounds are open and natural interpolation routes are blocked by cryptographic assumptions.

## 2. Results

### Lemma A (difficulty conservation). PROVED/EXACT, elementary; external review OPEN.

For every fixed R: Bridge(R) and LB(R) together imply SAT not in P. If LB(R) is a known theorem, Bridge(R) is **logically equivalent** to SAT not in P.

*Proof.* The first part is modus tollens. For the second: Bridge(R) and LB(R) give that SAT is not in P. Conversely, if SAT is not in P, the implication Bridge(R) is vacuously true. QED.

**Consequence.** LB(R) is a known theorem for:

- resolution, tree-like and general: Haken 1985 for PHP; Urquhart 1987 for Tseitin; Chvátal–Szemerédi 1988 for random 3-CNF; width–size, Ben-Sasson–Wigderson 2001;
- cutting planes: Pudlák 1997 via monotone interpolation; Hrubeš–Pudlák 2017 for random CNF;
- bounded-depth Frege: Ajtai 1988; Krajíček–Pudlák–Woods 1995; Pitassi–Beame–Impagliazzo 1993;
- Nullstellensatz and polynomial calculus: Razborov 1998; Ben-Sasson–Impagliazzo 1999; Alekhnovich–Razborov 2001.

For every such R, the "weakest sufficient bridge" is not weaker than P != NP. It *is* P != NP. Proving it for such an R carries the whole difficulty, and the lower-bound half adds nothing.

### Lemma B (relativization collapse). PROVED/EXACT, given Baker–Gill–Solovay; external review OPEN.

Let R be an oracle-free Cook–Reckhow system, so W_R does not depend on any oracle. Suppose a proof of Bridge(R) relativizes, meaning it proves "for every oracle A, NP^A ⊆ P^A implies W_R(N) <= poly(N)". Instantiate A = TQBF, where P^A = NP^A (BGS 1975). This yields W_R(N) <= poly(N) unconditionally. Hence:

- for any R with LB(R), no relativizing proof of Bridge(R) exists;
- for any R at all, a relativizing proof of Bridge(R) would prove that R is p-bounded, and therefore NP = coNP.

The multisign hypergraph and DAG calculus must therefore enter the bridge through a non-relativizing argument. Simulating "any polynomial algorithm" by derivations, using only input–output behaviour, is exactly the relativizing pattern that is excluded. Relativization gate: **FAIL** for every black-box simulation bridge.

### Lemma C (correct reformulation of the bridge). KNOWN THEOREM plus elementary composition.

Under SAT in P via a fixed algorithm A, the system Q_A is p-bounded. In Q_A, the proof of F is the empty string, and the verifier accepts when A rejects F. This is Cook–Reckhow 1979, and it is the same as the LSPV-5/409 decider-indexed identity system.

So Bridge(R) is equivalent to: for every polynomial-time SAT decider A, R p-simulates Q_A in size. This matches the LSPV-5/409 quantifier boundary, which is now confirmed for the worst-case W_R formulation.

For R = Extended Frege, EF p-simulates any system Q whose reflection principle RFN_Q has polynomial-size EF proofs. This is the Cook 1975 / Krajíček–Pudlák 1989 correspondence with PV and S^1_2. Hence:

    Bridge(EF) <= [ SAT in P  implies  there is a poly-time SAT decider A whose soundness
                    "A(F)=UNSAT and F(x)=1 is impossible" has poly-size EF proofs ].

This is a **CONDITIONAL sufficient condition**, not a proof. It asks for feasible provability of the correctness of a hypothetical algorithm, a Cook–Krajíček (2007)-type statement, and its status is OPEN.

Also, P = NP implies E = NE by padding, which implies that a p-optimal proof system exists (Krajíček–Pudlák 1989). Under the bridge hypothesis such a system is automatically p-bounded. Bridge(R*) is trivial for a p-optimal R*, but LB(R*) is then equivalent to NP != coNP, which is stronger than P != NP. No unconditionally explicit p-optimal system is known.

**Net verdict on the candidate: FALSIFIED as stated for every R with a known LB.** For R at the EF or p-optimal level it is reduced to two OPEN halves: the CONDITIONAL reflection statement above, and an EF lower bound. Neither half is known to be easier than its classical counterpart.

### Lemma D (hard families vs alternative reasoning). KNOWN THEOREMS; finite COMPUTATIONAL check.

- **Tseitin (odd charge, 3-regular, strict 3-CNF).** Exponential in resolution (Urquhart), but refuted by adding all |V| parity rows over GF(2). That takes |V|-1 row additions, which is polynomial in Res(lin) or Gaussian reasoning.
- **PHP^{m+1}_m.** Exponential in resolution (Haken), but has a polynomial cutting-planes refutation (Cook–Coullard–Turán 1987).

The prompt's combined system includes "algebraic reasoning" and "circuit compression", so neither family can be a worst-case witness for it. Candidates have to be families that are hard for all of the system's components simultaneously, such as random 3-CNF near threshold. Even then, the known lower bounds stop well short of EF.

## 3. Executed evidence (COMPUTATIONAL)

- Script `experiments/tmr/tmr5_worstcase_bridge058.py`, revision `tmr5-worstcase-bridge058.v1`, git blob `bc259ddcf3565e1dd7ef6dfcac0bbe59202bab14`.
- Run with CPython 3.11.18, exhaustive and deterministic, 20.2 s.
- Raw output `results/raw/tmr/2026-11-16_0648_TMR5_WORSTCASE_BRIDGE058_PY_RAW.json`, git blob `4e5713ad6fca9bad0bb7637b0fc059d9c23c8591`.

The exact minimum tree-like resolution size (2L−1, where L is the minimum number of decision-tree leaves) was computed by memoized DP over restrictions. Every instance was also confirmed UNSAT by brute force.

| Instance | vars | clauses | min tree-like Res size | other system |
|---|---|---|---|---|
| Tseitin K4 | 6 | 16 | 55 | GF(2): 3 additions |
| Tseitin K3,3 | 9 | 24 | 151 | GF(2): 5 |
| Tseitin prism | 9 | 24 | 95 | GF(2): 5 |
| Tseitin Q3 | 12 | 32 | 255 | GF(2): 7 |
| PHP m=1 | 2 | 3 | 5 | checked CP: 5 lines |
| PHP m=2 | 6 | 9 | 21 | CP: 17 |
| PHP m=3 | 12 | 22 | 85 | CP: 40 |
| PHP m=4..8 | 20..72 | 45..297 | not computed | CP: 77, 131, 205, 302, 425 |

The CP derivation for every hole j derives sum_i x_ij <= 1 inductively. At step k it multiplies the current bound by k−1, adds the k pairwise clauses, and divides by k with ceiling rounding. Each step is checked exactly.

The control run of even-charge K4 Tseitin is SAT, and the DP rejected it as SAT. These finite numbers illustrate the known theorems. They are not asymptotic proofs. Minimum general DAG resolution size was **not** computed.

## 4. Four gates

- **DISJ sanity: PASS.** No rank or static-structure lower bound is used.
- **Relativization: FAIL** for any relativizing bridge (Lemma B). A non-relativizing route is OPEN, and algebrization (Aaronson–Wigderson) applies equally to black-box algebraic simulation.
- **Natural Proofs / interpolation:** feasible-interpolation lower bounds for EF and Frege are blocked under RSA and factoring hardness (Krajíček–Pudlák 1998; Bonet–Pitassi–Raz 2000). Those blocks are guards here, not hypotheses.
- **Simultaneous DTISP: NOT APPLICABLE.** The statements concern proof size, with no machine time/space pair.
- **Deterministic configuration counting: NOT APPLICABLE.** No machine is constructed; the code is a bounded finite checker.

/341 is a FAIL as full UNSAT authority; /386 is RESTRICTED.

## 5. Charging remark (Time-Space auditor interface)

cost_R must charge every hyperedge or clause node actually *present* in the shared DAG, counted once, plus encoding bits. Granting the optimal sequence for free is legal for a lower bound. It must not be extended to granting free *extension variables* or free *compressed state* unless R explicitly contains those rules. If it does contain them, R is at least EF-strength, and LB(R) is open.

## 6. One next load-bearing lemma

Fix the multisign DAG hypergraph calculus R_MS precisely: its rules, whether it has extension or merging of shared signed hyperedges, and its cost. Then prove one of two things:

- (a) R_MS is p-simulated by resolution, cutting planes or Res(lin). By Lemma A its bridge is then equivalent to P != NP and the route is retired.
- (b) R_MS p-simulates EF. The pipeline then reduces exactly to the CONDITIONAL reflection statement of Lemma C plus an EF lower bound.

No P versus NP conclusion either way.

## Sources

Cook–Reckhow, JSL 1979; Cook, STOC 1975 (PV); Krajíček–Pudlák, JSL 54 (1989), "Propositional proof systems, the consistency of first order theories and the complexity of computations"; Köbler–Messner–Torán, I&C 2003; Cook–Krajíček, JSL 2007, "Consequences of the provability of NP ⊆ P/poly"; Baker–Gill–Solovay, SICOMP 1975; Haken, TCS 1985; Urquhart, JACM 1987; Chvátal–Szemerédi, JACM 1988; Ben-Sasson–Wigderson, JACM 2001; Cook–Coullard–Turán, DAM 1987; Pudlák, JSL 1997; Atserias–Müller, JACM 2020 (finding a near-optimal resolution refutation is NP-hard, which is consistent with "search is not charged"); Krajíček–Pudlák, I&C 1998; Bonet–Pitassi–Raz, SICOMP 2000; Aaronson–Wigderson, TOCT 2009. Citations were checked by web search (snippets only); full PDFs were not re-read this run.

## Validation actually run

- The Python script above was run.
- The preflight `--check --json` passed for the five manuscripts, with `mathematical_validation: NOT_PERFORMED`.
- No LaTeX compile unless noted in the handoff.
- No Lean, and no external review.
