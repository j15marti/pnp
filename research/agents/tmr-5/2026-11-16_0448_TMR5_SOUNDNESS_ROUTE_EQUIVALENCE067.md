# TMR-5/067 | 2026-11-16 04:48 PST | Soundness-route equivalence for the worst-case derivation bridge

Role: TMR-5 / PNP Machine Bottleneck Redteam (scheduled offset :48), acting as "Independent Proof Red Team" for the shared objective
W_R(N) = max_{F in UNSAT, |<F>| <= N} min_{pi : F |-_R bot} cost_R(pi)
and the bridge B(R): SAT in P => W_R(N) <= poly(N).
P versus NP remains **OPEN**. No schedule, identity, peer manuscript or retired tracker changed.

## Named dependency advanced

The /057 and /060 next lemmas name the only non-relativizing route proposed for B(R). The route runs: SAT in P gives a correct algorithm M, R gives short proofs of Sound(M), and these combine to give short R-refutations of every UNSAT F. Theorem C (/060) shows any proof of B(R) must be white-box, so this soundness, or reflection, route is the natural white-box candidate. **This run asks whether the route is a genuinely weaker intermediate step.**

**Candidate (to be falsified):** "Sound(M) has short R-proofs" is a weaker or more tractable premise than W_R <= poly.

Falsifiers stated before the literature search:
1. Any proof of Sound(C_N) restricts to a refutation of each instance. Then the premise implies W_R <= poly, and the route is circular.
2. Sound(C_N) is itself a poly-size UNSAT CNF. Then W_R <= poly implies the premise, and the two are equivalent.
3. For systems with known lower bounds, the premise fails for every correct C, unconditionally.
4. The executed transfer is unsound on a satisfiable F, or on a wrong circuit.

## Literature consulted (primary)

- **J. Krajíček, "A note on SAT algorithms and proof complexity"**, Inform. Process. Lett. 112 (2012). The author's PDF was text-extracted and read: Definition 1.1, Theorem 2.1, Corollary 2.2 and Theorem 3.1.
  - Alg(P) is the class of algorithms M whose reflection formulas ref^M_{k,n} = reject^M -> not sat_n have poly-size P-proofs.
  - Theorem 2.1 (decent P, conditions D1–D4): if M is in Alg(P) and tau_n needs l(n) P-proof size, then M needs time l(n)^Omega(1) to reject not tau_n.
  - The note cites Atserias–Bonet: resolution does not prove its own soundness.
  - **Falsifier 1 is therefore this KNOWN theorem.** The new content here is the equivalence direction, its consequence for the bridge, and an executed implementation.
- A. Atserias, M. L. Bonet, "On the automatizability of resolution and related propositional proof systems", Inform. and Comput. (2004). Cited via Krajíček; not re-read.
- K. Braun, arXiv:2609.23015 (2026-09-19): claims every DAG-like Res(⊕) refutation of BPHP^{n+1}_n has more than exp(n/(32768 l^2)) clauses, n = 2^l, l >= 32.
  - Only the abstract and snippets were read this run, so the claim stays a CANDIDATE.
  - The earlier bounded-depth result is Byramji–Impagliazzo, arXiv:2511.20023.
- Also seen: ECCC 2026/109 (Fleming–Grosser–Pitassi–Robere, TFNP-based <EF,R> systems). Only the abstract fragment was seen; it is not used.

## Theorem G (PROVED/EXACT, elementary; forward half KNOWN, Krajíček 2012 Thm 2.1; independent review OPEN)

**Model.**
- Fix n variables and m clause slots. The encoding f has bits p_{j,i}, q_{j,i}, meaning that x_i occurs positively or negatively in slot j. Padding repeats a clause.
- Let C be any Boolean circuit on f with output out. Tseitin(C) has a gate variable per gate.
- Sat(f,a,s) is the CNF with clauses
  - (OR_i s+_{j,i} OR s-_{j,i}),
  - (not s+_{j,i} OR p_{j,i}), (not s+_{j,i} OR a_i),
  - (not s-_{j,i} OR q_{j,i}), (not s-_{j,i} OR not a_i).
- Sound(C) := Tseitin(C) AND (not out) AND Sat(f,a,s). Its size is O(|C| + nm).

**Closure assumption.** Let R be a refutation system closed under:
- partial restriction by constants;
- substitution of a variable by a literal;
- deletion of satisfied lines;
- the identification above, without size increase.

This holds for tree-like and DAG resolution, Res(k), polynomial calculus (with twin variables), cutting planes, bounded-depth Frege, Frege and extended Frege. Up to a polynomial, it is the standard restriction lemma.

**(i) Transfer.** Let F be any formula in the slots with C(F) = 0. Then S_R(F) <= S_R(Sound(C)).

*Proof.*
1. Define the restriction rho_F:
   - f := the encoding of F;
   - every gate variable := its value on F (so out := C(F) = 0);
   - s+_{j,i} := 0 if p_{j,i} = 0, else s+_{j,i} := a_i;
   - s-_{j,i} := 0 if q_{j,i} = 0, else s-_{j,i} := not a_i.
2. Apply rho_F to each axiom of Sound(C):
   - every Tseitin clause is satisfied;
   - (not out) is satisfied because out = 0;
   - each binary Sat clause becomes true, or the tautology (not a_i OR a_i);
   - each wide clause becomes exactly clause j of F.
3. Restriction and literal substitution map an R-refutation to an R-refutation of the image axiom set, with no size increase. The image axiom set is a subset of F. QED.

**(ii) Equivalence.** Let C_N be correct on all slot formulas of size <= N, that is, C_N(F) = 0 exactly when F is UNSAT. Then

W_R(N) <= S_R(Sound(C_N)) <= W_R(|Sound(C_N)|), with |Sound(C_N)| = O(|C_N| + N).

The left inequality is (i) maximized over F. The right inequality holds because Sound(C_N) is UNSAT exactly when C_N is sound.

**Corollary G1.** The bridge is equivalent to its soundness-route form:

B(R) <=> [SAT in P => some poly-time correct M lies in Alg(R)].

The same holds non-uniformly: [poly-size correct circuits exist AND W_R <= poly] <=> [poly-size correct C with S_R(Sound(C)) <= poly exists].

**The soundness route is therefore equivalent to the target bridge, not weaker. The candidate is FALSIFIED as a weakening.**

**Corollary G2 (KNOWN-theorem composition).** Take R = Res, Res(k), PC, CP or AC0-Frege. Each has KNOWN exponential lower bounds on poly-size 3-CNFs (Haken; Urquhart; Ben-Sasson–Wigderson; Razborov / Impagliazzo–Pudlák–Sgall; Pudlák 1997; Ajtai / Beame–Impagliazzo–Pitassi / Krajíček–Pudlák–Woods). For every correct poly-size C_N, S_R(Sound(C_N)) is superpolynomial, unconditionally. So no correct polynomial-time SAT algorithm lies in Alg(R) for these R, whatever the truth of P vs NP. In these systems the soundness route is closed, not merely open.

**Corollary G3 (scope).** For Frege and EF, Corollary G1 shows that proving "SAT in P => short EF proofs of Sound(M)" is the same task as proving B(EF). Krajíček (2012, Cor. 2.2) and Cook (1975) give the KNOWN partial direction: an EF lower bound excludes polynomial-time SAT algorithms whose soundness is provable in V^1_1 / PV. That is a consistency statement, not P != NP. The free choice of optimal derivation does not alter any of this.

## Executed evidence (COMPUTATIONAL)

- Executable: `experiments/tmr/tmr5_soundness_restriction067.py`, revision `tmr5-soundness-restriction067.v1`, seed 20261116, CPython 3.11.18. Final blob d2fcef196592d36ae3603334a6ec5a3b5741360f.
- Raw output: `results/raw/tmr/2026-11-16_0448_TMR5_SOUNDNESS_RESTRICTION067_PY_RAW.json`, blob 8877d459f35c30abd118d856494aeb321fda00d7.

**Pipeline.**
1. Encode slots.
2. Build the brute-force SAT circuit: c_{j,b}, g_b = AND_j c_{j,b}, out = OR_b g_b.
3. Build the Sound(C) CNF.
4. Write the explicit RUP proof: 2^n (m+2) lines plus the 2^n - 1 prefix lines.
5. Expand it into an explicit resolution DAG by unit-propagation conflict analysis.
6. For each random authentic F: build rho_F with literal substitution. Restrict the DAG under an explicitly asserted invariant: each line is TRUE, or a derived clause contained in the line's image. Prune to the ancestors of the empty clause.
7. Check the result with an **independent checker**: every axiom is a clause of F, every step is an exact resolvent with a unique pivot, and the final line is empty.

**Results.**

| n | m | Sound vars | Sound clauses | Resolution DAG lines | UNSAT F tested | Max restricted lines |
|---|---|---|---|---|---|---|
| 2 | 4 | 55 | 110 | 233 | 60 | 7 |
| 3 | 6 | 132 | 336 | 839 | 120 | 12 |
| 3 | 8 | 172 | 442 | 1105 | 120 | 13 |
| 4 | 10 | 341 | 1164 | 3291 | 60 | 16 |
| 5 | 16 | 870 | 3986 | 12273 | 30 | 17 |
| 6 | 26 | 2359 | 14092 | 45899 | 12 | 25 |

- 1338 assertions, **0 failures**, 15.99 s.
- Every restricted DAG is a valid resolution refutation of its F, and its size never exceeds the original.

**Controls.**
- **Satisfiable F (10 per config, 60 in total).** Restriction makes out = 1, so (not out) maps to the empty clause. The checker rejects every one with "axiom not a clause of F: []". The transfer never refutes a satisfiable F.
- **Wrong circuit C0 = 0 (always "UNSAT").** The RUP proof fails, because Sound(C0) is satisfiable. Rejected in all 6 configs.

**Bugs found and fixed during development** (disclosed): a variable-id mismatch in the harness; a literal-versus-constant pivot test; and a TRUE-image copy rule that broke the subset invariant. The final run has the invariant asserted on every line.

The finite sizes are COMPUTATIONAL only. The large shrinkage (45899 -> <= 25 lines) illustrates that (i) is lossy. It does not prove anything asymptotic.

## Gates

- **DISJ:** NOT APPLICABLE (no rank or communication transfer).
- **Relativization:** Theorem G is oracle-free and propositional. It is consistent with /060 Theorem C: the soundness route is white-box, since Sound(C) depends on C's gates. It gives no separation. Algebrization and Natural Proofs: NOT APPLICABLE (no lower bound proved).
- **Simultaneous DTISP:** NOT APPLICABLE to proof size. The executable is O(|Sound| * |proof|) time, with one proof in memory.
- **Deterministic configuration counting:** PASS, as an upper-bound guard only.
- /341 FAIL as full UNSAT authority. /386 RESTRICTED.

## Not run

Preflight script, LaTeX build (no TeX in the container), Lean, independent re-read of Atserias–Bonet and of Braun's full text, external review.

## Next load-bearing lemma

Restrict the target to the algorithm class K = Alg(DAG Res(⊕)), for example DPLL with Gaussian-elimination learning whose soundness Res(⊕) proves briefly.
1. Independently verify Braun's 2^{Omega(n / log^2 n)} BPHP bound.
2. Then, by Theorem G(i) and Krajíček Thm 2.1 (decency of Res(⊕) to be checked: D1 restriction, D4 literal substitution), every M in K runs in superpolynomial time on not-BPHP. That is an honest K-only lower bound.
3. Separately, identify which natural parity-reasoning SAT procedures lie in K.

This advances the bridge only for K, never for P.
