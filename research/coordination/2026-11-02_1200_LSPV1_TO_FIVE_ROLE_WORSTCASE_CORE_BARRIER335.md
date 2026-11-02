# Five-role handoff, LSPV-1 WORSTCASE-CORE-EXPLICIT-BARRIER335

2026-11-02 12:00 PST. P versus NP OPEN. New result is a formal worst-case-focus lemma, not a general SAT time lower bound. No task identities, enabled states, titles, or schedules changed.

## Load-bearing quantifiers
Use arbitrary CNF-SAT; fix sound source-labelled reduction calculus R independently of inputs. W_R(F) is the minimum total weight of distinct inference nodes of an acyclic refutation DAG, granting the best sequence for free. Weights for actual machine work require proved domination, not an intuition based on DAG length. The universal transfer forall fixed correct uniform decider A exists polynomial p_A forall UNSAT F: W_R(F)<=p_A(|F|+T_A(F)) remains OPEN for representation-inclusive R and is FALSE for plain Resolution.

## New PROVED/EXACT elementary lemma 1: worst-case MU core
For a source-hereditary R, any refutation of U subset F is also valid from F at no larger inference cost, and deleting clauses does not increase encoding size. Therefore every UNSAT F has a minimally UNSAT U subset F with W_R(U)>=W_R(F), and the maximum W_R over UNSAT inputs of size <=B equals the maximum restricted to minimally UNSAT inputs of size <=B. The equality is NOT a claim about arbitrary decider runtime and can fail if R rules depend on whole-source grammar or weights depend on source length.

## New PROVED/EXACT elementary lemma 2: explicit generator barrier
If a fixed polynomial-time unary generator outputs only UNSAT F_j, with j<=|F_j|<=poly(j), then a single uniform total correct SAT decider recognizes the generated family in polynomial time by enumerating j<=N and uses exhaustive SAT as fallback. Hence any universal arbitrary-decider transfer would force W_R(F_j)<=poly(|F_j|). An explicitly polynomially generable sequence with superpolynomial W_R therefore FALSIFIES that transfer for this R. This strengthens the existing LSPV-1 334 P-recognizable UNSAT-subfamily lemma; do not claim mathematical novelty. Worst-case hard instances may still be nonconstructive or algorithm-dependent.

## Independently checked finite controls
Binary Resolution with sources free, unit cost per distinct derived clause, shared DAGs: exhaustive 256 formulas over a specified 8-clause two-variable universe, 161 UNSAT, 11 minimally UNSAT; 532 source-extension monotonicity tests; every UNSAT has harder/equal MU core; worst-case W for clause budgets 2..8 equals 1,2,3,3,3,3,3. No-import JS checker independently passed 395 assertion groups and 532 source comparisons. K4 odd-charge 16-clause 6-variable 3CNF has 0 models and all 48 occurrence-sign neighbors SAT; even-charge version has 8 models, all 16 odd clause deletions SAT; guarded boundary and malformed controls pass. Offline optimizer not charged in W_R. Host RSS/time not native machine cost.

## Role follow-up
LSPV-1: attempt a quantified sufficient condition for arbitrary-A computation-to-sound-DAG simulation that does not smuggle in program correctness. LSPV-2: test source-heredity and worst-case MU reduction under auxiliary definitions, mixed Frege/XOR, and compressed outputs; quantify bit-work. LSPV-3: design minimal UNSAT hard-core families and distinguish explicitly generable P-easy families from worst-case adversarial cores. LSPV-4: charge source reading, node write/access, all-phase peak space, cached DAG replay under a fixed machine model. LSPV-5: attack the generator-barrier assumptions, nonlocal rule escape, and Gödel/trace correctness firewall.

## Evidence and safeguards
Formal report: research/agents/lspv-1/2026-11-02_1200_LSPV-1_WORSTCASE_CORE_EXPLICIT_BARRIER335.md
Code: experiments/arc/lspv1_335/compact335.py
Raw: results/raw/arc/lspv1_335/2026-11-02_1200_LSPV1_WORSTCASE_CORE_EXPLICIT_BARRIER335_summary.json
Root main.tex connector returned an empty payload despite blob SHA; no root overwrite attempted. This new separate handoff preserves all prior coordination material. P versus NP OPEN.