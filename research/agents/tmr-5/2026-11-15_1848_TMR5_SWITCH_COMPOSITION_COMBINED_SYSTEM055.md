# TMR-5/055 | 2026-11-15 18:48 PST | Switch composition: componentwise hardness does not transfer to a combined system

Role: TMR-5 / PNP Machine Bottleneck Redteam ("Independent Proof Red Team" in the shared worst-case directive). P versus NP OPEN.

## Named end-to-end dependency

Shared objective: W̄_R(N) = max_{F∈UNSAT, |⟨F⟩|≤N} min_{π:F⊢_R⊥} cost_R(π), with Bridge(R): SAT∈P ⇒ W̄_R(N) ≤ poly(N).
TMR-5/053 (branch `ccr-1695bd63-ysu7ts`, commit `9891a0c5`, never merged; imported into main5 by this run) showed Bridge(R) ⇔ P≠NP for every R with a known superpolynomial lower bound, and named the next lemma: does the fixed combined system R_comb (resolution + GF(2) + cutting planes + extension/sharing) p-simulate extended Frege? This run advances the dependency **"hard family survives R_comb"** (directive priority 4: survival against resolution, algebraic reasoning, circuit compression, shared DAGs and adaptive switching).

## Candidate audited and falsifiers (stated before search)

Candidate (implicit in priority 4): if a family is superpolynomially hard for each component system of R_comb separately, it is hard for R_comb.
Falsifiers: (F1) a formula hard for each component but polynomial for the union with switching; (F2) R_comb ⊇ extended resolution, making any R_comb lower bound an EF lower bound; (F3) a published superpolynomial DAG lower bound for a component already strong enough (e.g. Res(⊕)) that changes the frontier.
Result: F1 and F2 hold (the candidate is FALSIFIED as a criterion); F3: one new unreviewed claim found (below).

## Theorem C (switch composition), PROVED/EXACT, elementary; independent review OPEN

Let F(x), G(y) be UNSAT CNFs on disjoint variables and z fresh. H = {C∨z : C∈F} ∪ {D∨¬z : D∈G}.

(i) H is UNSAT, H|_{z=0} = F and H|_{z=1} = G (as clause sets). |H| ≤ |F|+|G|+O(|F|+|G|) symbols.

(ii) Lower bound by restriction. For every proof system R closed under restriction without size increase (tree-like/DAG resolution, Res(⊕), PC over any field, CP, Frege, EF all are), s_R(H) ≥ max(s_R(F), s_R(G)).

(iii) Exact additivity for tree-like resolution: T(H) = T(F)+T(G), where T is the minimum number of leaves of a refuting decision tree (= tree-like resolution size, KNOWN equivalence). Proof: every clause of H contains z or ¬z, so every leaf's path assigns z. At each z-node keep only the 0-child: the result is a refuting decision tree for F on x∪y whose leaves are exactly the leaves with z=0; queries to y-variables can be removed by keeping the smaller child (F mentions no y), so those leaves number ≥ T(F). Symmetrically the z=1 leaves number ≥ T(G); the two leaf sets are disjoint. Querying z first gives T(F)+T(G). ∎

(iv) Union upper bound. Let U be any system containing R1 and R2 with a clause interface (axiom clauses may be read by either, derived clauses passed between them, one resolution step allowed). If R1 refutes F in size s1 and admits literal weakening with polynomial overhead, and R2 likewise G in size s2, then s_U(H) ≤ poly(s1)+poly(s2)+O(1): derive (z) from F∨z, derive (¬z) from G∨¬z, resolve. Weakening is free in resolution (add z to every line) and costs ≤2x size, +1 degree, in PC (multiply every line by (1−z); with x=1 meaning true, clause C∨z has falsity polynomial p_C(1−z)). CP weakening is not claimed here.

(v) Consequence (FALSIFIES the componentwise criterion). If F is R2-hard but R1-easy and G is R1-hard but R2-easy, then H is superpolynomially hard for R1 and for R2 separately (by ii) yet polynomial for U (by iv). Hence a "survives resolution / survives algebra / survives CP" checklist cannot certify hardness for a combined system with adaptive switching; hardness must be proved against U itself, including its switching rule.

Instance from KNOWN THEOREMS (CONDITIONAL on matching the cited encodings; independent check OPEN): R1 = PC over F2, R2 = PC over F3, F = mod-3 Tseitin on a bounded-degree expander, G = mod-2 Tseitin on an expander. Buss–Grigoriev–Impagliazzo–Pitassi (JCSS 62, 2001) give linear degree lower bounds for mod-p Tseitin in characteristic q≠p; Impagliazzo–Pudlák–Sgall (Comput. Complexity 8, 1999) convert linear degree on bounded-width axioms into exp(Ω(n)) size; both are degree-1/low-degree easy in their own characteristic (Gaussian elimination). So H is exponentially hard for PC_F2 and for PC_F3 but polynomial for PC_F2+PC_F3 with switching.

## Corollary D (extension collapse), KNOWN THEOREM composition

If R_comb contains resolution plus the extension rule ("circuit compression", "shared definitions"), then R_comb p-simulates extended resolution, which is p-equivalent to extended Frege (Cook–Reckhow 1979; Krajíček, *Bounded Arithmetic, Propositional Logic and Complexity Theory*, 1995). So any superpolynomial lower bound on W̄_{R_comb} is a superpolynomial EF lower bound: OPEN, with no superpolynomial lower bound known for any family in Frege or EF, and the Pich–Santhanam (FOCS 2019) barriers apply. Together with Theorem B of /053, Bridge(R_comb) additionally needs a provability premise (PV-provable correctness of a SAT algorithm, Cook 1975). Answer to the /053 next lemma: **yes, if extension is in R_comb, R_comb ≥_p EF.** Without extension the question is open in a different way (below).

## Literature check (this run)

- Unrestricted DAG Res(⊕) (resolution over GF(2) linear clauses, the natural "resolution + GF(2)" combination without extension): as of ECCC TR25-188 ("Strong ETH holds for bounded-depth resolution over parities") no superpolynomial size lower bound was known; known bounds were tree-like, regular (Efremenko–Garlík–Itsykson, STOC 2024), or bounded depth (arXiv 2507.23008, Õ(N²) depth; arXiv 2511.20023, bit-PHP in depth N^{2−ε}; ECCC TR25-116 size/depth tradeoff).
- NEW CLAIM, NOT VERIFIED HERE: K. Braun, arXiv 2609.23015 (submitted 2026-09-19), claims every DAG-like Res(⊕) refutation of bit-PHP^{n+1}_n has 2^{Ω(n/log²n)} clauses, with a Lean 4 formalization and substantial AI assistance. Status here: CANDIDATE literature input; peer-review status unknown; Lean artifact not built by TMR-5. If correct, it gives the first superpolynomial lower bound for a "resolution + GF(2)" combined DAG system, but by Theorem A it still only re-expresses Bridge(Res(⊕)) ⇔ P≠NP, and by Theorem C its family must still be checked against the CP and PC arms and against switching. The bit-PHP status in CP and in R_comb is not determined here.
- Cutting planes: Tseitin has quasipolynomial CP refutations (Dadush–Tiwari, CCC 2020), so Tseitin does not survive the CP arm; CP lower bounds are known for random Θ(log n)-CNF (Fleming–Pankratov–Pitassi–Robere 2017; Hrubeš–Pudlák 2017); random constant-width 3-CNF in CP remains OPEN as far as found.

## Executed evidence (COMPUTATIONAL)

`experiments/tmr/tmr5_switch_composition055.py`, revision `tmr5-switch-composition055.v1`, seed 20261115, CPython 3.11.18, 14.1 s. Families: PHP^2_1, PHP^3_2, odd Tseitin on K3 and C4, three seeded random UNSAT 3-CNFs on 4 variables. For all 48 ordered pairs with ≤11 variables in H it checked by brute force that H is UNSAT and that H|z=0=F and H|z=1=G, computed exact minimum tree-like sizes with T(H)=T(F)+T(G) in every case (e.g. PHP^3_2 with C4 Tseitin: 11+8=19), and step-checked the z-weakened resolution derivations of (z) and (¬z) and the final switch step. 28,351 assertions, 0 failures. Raw: `results/raw/tmr/2026-11-15_1848_TMR5_SWITCH_COMPOSITION055_PY_RAW.json`. The finite tests do not test PC/CP lower bounds or the expander instance.

Not executed: repository preflight, LaTeX build, Lean build of arXiv 2609.23015, any PC degree computation.

## Four gates

DISJ: NOT APPLICABLE (no rank or communication transfer). Relativization: Theorems C and D relativize; they are barrier-neutral audits, no separation claimed. Simultaneous DTISP: NOT APPLICABLE (proof size, not machine time/space). Deterministic configuration counting: PASS, upper-bound guard only. Algebrization/Natural Proofs: not engaged. /341 FAIL as full UNSAT authority; /386 RESTRICTED.

## Ranked consequences for the five roles

1. General SAT Lower-Bound Lead: state R_comb's rule set exactly (with/without extension). With extension the target is the EF lower bound plus a provability premise.
2. SAT-Circuit Reduction Builder: the switching rule is part of the system; certified shortest DAGs must be computed in the union system, not per component.
3. Hypergraph & Proof Certificates: hard families must be checked against U; Tseitin fails CP (quasipoly), PHP fails CP, bit-PHP is a candidate for Res(⊕) only.
4. Resource Auditor: cost of switching and weakening is polynomial (iv); charge it.
5. Red Team (this role): next, decide the CP-arm status of bit-PHP, or find a polynomial R_comb-without-extension refutation of it.

## One next lemma

Without extension, take R_comb^- = DAG Res(⊕) + CP with a clause interface. Decide whether bit-PHP^{n+1}_n has polynomial R_comb^- refutations (CP arm or a switch combination). If it does, the only candidate DAG Res(⊕) hard family does not survive R_comb^-; if not, give the proof and an independent check of Braun's Lean artifact.
