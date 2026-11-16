# TMR-5/053 | 2026-11-15 17:48 PST | Red-team audit of the worst-case derivation bridge

Authority: research/coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md (read first), compatible SAT-compression directive, and the scheduled user objective of 2026-11-16 (shared target W̄_R(N), bridge SAT∈P ⇒ W̄_R(N) ≤ poly(N)). Retired proof trackers not read or edited. P versus NP OPEN.

## Target, model and quantifiers

For a Cook–Reckhow proof system R (polynomial-time verifier, sound and complete for UNSAT CNFs), define

  W̄_R(N) = max over UNSAT F with |⟨F⟩| ≤ N of min over R-refutations π of F of cost_R(π),

with cost = encoded proof length (lines × line size; for tree-like resolution, leaves). The minimum is over all refutations; strategy discovery is not charged (this is exactly the user's "free optimal sequence"). Thus W̄_R is the worst-case proof-size function s_R of Cook–Reckhow 1979. The multisign DAG hypergraph "minimal reduced logical state" construction, with reduction steps equal to sound local inferences on the clause hypergraph, is a DAG-like proof system of this kind, so everything below applies to it once its rule set is fixed.

Bridge(R): SAT ∈ P ⇒ W̄_R(N) ≤ poly(N).

Candidate tested: "Bridge(R) is a weaker, separately provable step that together with a superpolynomial lower bound on W̄_R yields P ≠ NP."

Falsifiers stated before search: (F1) some R with a known unconditional lower bound makes Bridge(R) equivalent to P≠NP; (F2) for every explicit R, the only known route from SAT∈P to R-bounds needs an extra provability hypothesis; (F3) the proposed hard families are refuted cheaply by an alternative system; (F4) minimizing over all derivations is not a lower bound on algorithms that do not produce R-derivations.

## Results

### Theorem A (PROVED/EXACT, elementary from KNOWN THEOREMS; independent review OPEN)
Let R be any proof system for which W̄_R(N) ≥ N^{ω(1)} is unconditionally known. Then Bridge(R) ⇔ P ≠ NP.

Proof. (⇐) If P≠NP the antecedent SAT∈P is false, so Bridge(R) holds. (⇒) Bridge(R) and the known W̄_R superpolynomial give, by contraposition, SAT ∉ P. ∎

KNOWN unconditional exponential lower bounds (worst case over 3-CNF or CNF families): tree-like and DAG resolution (Haken 1985 PHP; Urquhart 1987 Tseitin; Chvátal–Szemerédi 1988 random 3-CNF; Ben-Sasson–Wigderson 2001 width method), Res(k) for small k, polynomial calculus (Razborov 1998; Alekhnovich–Razborov), cutting planes (Pudlák 1997 via monotone interpolation), bounded-depth Frege (Ajtai 1988; Beame–Impagliazzo–Pitassi, Krajíček–Pudlák–Woods). For all of these, Bridge(R) is EXACTLY as hard as P≠NP. **F1 CONFIRMED: for every system where the lower-bound half of the program is already known, the bridge is the whole problem, not a weaker step.** The program "lower bound + bridge" is non-vacuous only for systems with OPEN lower bounds (Frege, extended Frege, and stronger), where the lower-bound half is itself a famous open problem (Cook–Reckhow program).

### Theorem B (PROVED/EXACT, elementary; independent review OPEN)
(i) For every R, P ≠ NP ⇒ Bridge(R). (ii) If P = NP then Bridge(R) ⇔ R is polynomially bounded. (iii) For a sound theory T with a polynomial-time proof checker, define R_T: a refutation of F is (A, k, p, 1^{|F|^k}) where p is a T-proof that A is a correct SAT decider running in time n^k, and the verifier checks p and runs A on F for |F|^k steps expecting NO. R_T is a Cook–Reckhow system, and SAT ∈ P via some A whose correctness and bound are T-provable ⇒ W̄_{R_T}(N) ≤ poly(N).

Proof sketch. (i),(ii) definitional. (iii) soundness of T makes R_T sound; for the fixed A the proof p has constant size; verification is polynomial. ∎

Consequence (F2 CONFIRMED as a scope limit): for an explicitly fixed R, the known route from SAT∈P to a bound on W̄_R requires that R efficiently simulate the trace system of the algorithm, i.e. that R (or the theory behind it) prove correctness of that algorithm. Cook 1975 gives this for EF when the correctness is provable in PV. Krajíček–Pudlák 1989: E=NE ⇒ a p-optimal proof system exists (and P=NP ⇒ E=NE by padding), but such a system is not given explicitly in advance. Truth of SAT∈P alone (a Π2 statement whose correctness part may be unprovable in T) does not give Bridge(R_T). **No unconditional proof of Bridge(R) for any explicit R is known without proving P≠NP or adding a provability hypothesis.** This is the precise unresolved premise of the shared objective.

### F4 (KNOWN, scope): W̄_R lower bound alone constrains only R-trace algorithms
min_π cost_R(π) is a valid lower bound on any algorithm whose run on UNSAT F yields an R-refutation of comparable size (e.g. DPLL ↔ tree-like resolution, CDCL ↔ resolution). Granting free choice of the best derivation is legitimate for that statement. It does not constrain an algorithm whose transcript is not an R-proof; that gap is exactly Theorem B(ii). Automatability (Atserias–Müller 2019: resolution not automatable unless P=NP) is an upper-bound/search question and is correctly not charged.

### F3: survival of hard families under alternative reasoning (KNOWN + COMPUTATIONAL)
PHP^{m+1}_m: resolution exponential (Haken), but cutting planes poly (Cook–Coullard–Turán 1987) and Frege poly (Buss 1987) — FAILS survival. Tseitin on expanders: resolution exponential (Urquhart), but GF(2) Gaussian elimination / PC over F_2 / Res(lin) poly — FAILS. Random 3-CNF at constant density: resolution, Res(k) small k and PC (char ≠ 2 and 2) exponential; cutting-planes lower bounds known for random Θ(log n)-CNF (Fleming–Pankratov–Pitassi–Robere 2017; Hrubeš–Pudlák 2017), random 3-CNF CP status to our knowledge OPEN; Frege/EF OPEN. No family is known to survive Frege. Pich–Santhanam (FOCS 2019) give an unconditional barrier: proof systems cannot efficiently prove random truth tables lack poly-size circuits, plus a conditional natural-proofs-like obstacle to Frege/EF lower bounds.

Executed controls (CPython 3.11.18, revision tmr5-bridge-survival053.v1, seed 20261115; script SHA256 a6f94184869111dbcb4200a344b50a8c0a2277a1366f74977b9438c70250c53f; raw SHA256 96d826ac95b94699743a5d9a3c007f9299374f25bc15f1264e0ce4d3e6679b20; 1,725 assertions, 0 failures, 3.0 s):

| Family | vars | exact min tree-like resolution leaves | alternative system cost |
|---|---|---|---|
| PHP^2_1 | 2 | 3 | CP 3 steps |
| PHP^3_2 | 6 | 11 | CP 11 steps |
| PHP^4_3 | 12 | 43 | CP 28 steps |
| PHP^9_8 | 72 | not computed | CP 353 steps (each step machine-checked legal; soundness of derived hole lines brute-forced for m≤3) |
| Tseitin(K4) | 6 | 28 | GF(2) 3 row additions |
| Tseitin(K3,3) | 9 | 76 | GF(2) 5 row additions |
| Tseitin(K5) | 10 | 232 | GF(2) 4 row additions |
| random 3-CNF, n=6..9, density 5.5 (over-constrained, NOT a hard regime) | 6–9 | 10–16 | — |

Exact min tree-like size is computed by exhaustive DP over all partial assignments (min decision-tree leaves, a standard equivalence). Finite sizes are COMPUTATIONAL illustrations only; asymptotic separations are the cited KNOWN THEOREMS. The random rows are disclosed as easy controls; they do not test the hard threshold regime.

## Four gates
DISJ: NOT APPLICABLE (no rank/communication transfer used). Relativization: Theorem A/B are relativizing set-level implications; the open half (Bridge for an explicit system, or Frege lower bounds) inherits the known barriers (Pich–Santhanam; natural-proofs analogues; algebrization unaffected). Simultaneous DTISP: NOT APPLICABLE (proof size, not machine time/space; R-trace algorithms charged via F4). Deterministic configuration counting: PASS as upper-bound guard only. /341 FAIL full UNSAT authority; /386 RESTRICTED.

## Ranked consequence for the shared objective
Status of the shared target: the lower-bound half is KNOWN for weak R and OPEN for Frege/EF; the bridge half is equivalent to P≠NP for weak R (Theorem A) and, for strong explicit R, needs a provability premise (Theorem B). The objective is therefore a correct reformulation of the Cook–Reckhow program, not a reduction to a weaker statement.

## One next lemma (load-bearing)
For the project's fixed combined inference system R_comb (resolution + GF(2) linear + counting/cutting-planes + extension/sharing), determine whether R_comb p-simulates extended Frege. If NO, Theorem A-type equivalence threatens once a lower bound is proved; if YES, the lower-bound half is the open EF lower-bound problem and the bridge needs PV-style provable correctness (Cook 1975). Either answer must be stated before claiming progress on W̄_{R_comb}.

## Primary sources consulted this run
Cook–Reckhow, JSL 1979; Cook, STOC 1975; Krajíček–Pudlák, JSL 54 (1989) (E=NE ⇒ p-optimal; NE=coNE ⇒ optimal; confirmed via arXiv:2408.07408, arXiv:1904.01362 summaries); Pich–Santhanam, FOCS 2019, DOI 10.1109/FOCS.2019.00080; Haken TCS 1985; Urquhart JACM 1987; Chvátal–Szemerédi JACM 1988; Ben-Sasson–Wigderson JACM 2001; Cook–Coullard–Turán DAM 1987; Buss JSL 1987; Pudlák JSL 1997; Atserias–Müller FOCS 2019/JACM 2020. Only Krajíček–Pudlák and Pich–Santhanam were re-verified by web search this run; others cited from standard knowledge, independent bibliographic check OPEN.

Not executed: repository preflight, LaTeX build, independent external review.
