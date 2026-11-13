# LSPV-1: A formal-correctness-certificate-only algorithm transfer cannot cover all correct SAT deciders

Date: 2026-11-13, America/Los_Angeles (PST).  
Owner: LSPV-1 General SAT Lower-Bound Lead, historical Route B.  
Status: **PROVED/EXACT conditional metatheoretic scope obstruction**, with **COMPUTATIONAL** finite strict-3CNF encoding checks. **P2-B2/B3 remain OPEN; P versus NP remains OPEN.**

## Target, falsifiers, and role of the result

**Candidate to test:** Could an algorithm-to-native-proof transfer establish its required universal quantifier over *every* correct deterministic SAT decider by first demanding a formal proof of each decider's correctness in one fixed, sound/consistent, effectively axiomatized background theory T?

Four falsifiers of the candidate strategy:
1. A correct total SAT decider has no T-proof of its global SAT correctness.
2. The counterexample decider cannot be defined on well-formed proper 3-CNF without invoking an oracle.
3. Its correctness depends on an uncharged assumption stronger than T's consistency.
4. The argument only concerns total exponential deciders and cannot preserve polynomial runtime under SAT-in-P.

Result: (1) holds by Gödel II; (2) and (3) fail for the explicit construction; (4) fails conditionally whenever a polynomial decider D exists. This falsifies a **T-correctness-certificate-only strategy**, NOT the broader existential same-calculus B2/B3 transfer theorem. A compiler may conceivably handle the decider without a T-proof of the decider's correctness.

## Theorem: a correct but T-unprovably-correct SAT decider

Let T be a fixed, consistent, effectively axiomatized classical arithmetic theory with standard polynomial-time proof checking, arithmetized proof predicate Prf_T(q, bottom), adequate formalization of elementary algorithm execution, and applicability of Gödel's second incompleteness theorem (e.g., ordinary Peano Arithmetic with a standard proof encoding).

Let D be **any** fixed, correct, total deterministic SAT decider on all binary strings, with a fixed classification of malformed inputs. Such a D exists unconditionally by exhaustive assignment evaluation.

Then there is an explicitly computable total deterministic SAT decider A_{T,D} with:

1. For every binary input F, A_{T,D}(F)=D(F) in the standard model.
2. For worst-case input length N, T_{A_{T,D}}(N) <= T_D(N)+N^{O_T(1)} (using a suitable fixed machine and ordinary encoding; standard simulation overhead may be polynomial).
3. T **does not prove** the universal correctness statement "A_{T,D} decides SAT correctly on all encoded inputs."
4. Consequently, if SAT happens to admit a correct polynomial-time deterministic decider D, then SAT also has a correct polynomial-time deterministic decider A_{T,D} whose global correctness is not provable in this fixed T.

The theorem is about **formal provability of program correctness**, not a lower bound on SAT, proof size, the historical R_mix341 calculus, or physical runtime of arbitrary proof discovery.

### An explicit satisfiable strict-3CNF code carrier

For every nonempty binary string q=q_0...q_{m-1}, define distinct variables z,a_i,b_i and the ordered, proper signed 3-CNF

$$
G_q = \bigwedge_{i=0}^{m-1} (z \lor a_i \lor \ell_i),\qquad
\ell_i=\begin{cases}b_i & q_i=0,\\ \neg b_i & q_i=1.\end{cases}
$$

Use variable numbers z=1, a_i=2i+2 and b_i=2i+3, in a fixed source-bit encoding. Every clause has exactly three distinct variables. Every G_q is SAT under the explicit witness z=1, regardless of the remaining variables. The sign of b_i recovers q_i; consequently the ordered encoding is injective, its image is recognizable and decodable in polynomial time, and its bit length is O(m log(m+2)). This is **not** a promise that an arbitrary input is G_q. The full decider first recognizes the special source syntax and otherwise invokes D.

### Program

On a binary input F:
- If F is not exactly a canonically encoded G_q, run D(F).
- Otherwise, decode q and check the standard syntactic predicate Prf_T(q,bottom) for a T-proof of 0=1.
- If that predicate is true, output UNSAT (deliberately wrong on this satisfiable F); otherwise run D(F).

Every branch halts. Recognition, decoding and checking a purported T-proof q are polynomial in the input bit length. If T is consistent, no q encodes a T-proof of contradiction, so the deliberate false-UNSAT branch is never taken. A_{T,D} is extensionally identical to D and therefore correct. If D has a polynomial all-input bound, then so does A_{T,D}. No semantic oracle, nonuniform advice, or proof search is performed: *one supplied q* is checked syntactically.

### Formal unprovability proof

Fix arbitrary q within the usual arithmetization. The theory T can verify the transparent satisfiability of G_q with z=1 and the conditional behavior

$$
\operatorname{Prf}_T(q,\bot)\Longrightarrow
A_{T,D}(G_q)=\mathrm{UNSAT}.
$$

These are uniform elementary facts about the formula template and the program's first branch; no T-proof of D's correctness is required.

If T proved the universal SAT-correctness of A_{T,D}, T could instantiate that theorem at every G_q. Given the explicit satisfying assignment, correct behavior requires the output SAT. Combining it with the conditional above, T would prove

$$
\forall q\ \neg\operatorname{Prf}_T(q,\bot),
$$

i.e. the standard arithmetized Con(T). Gödel's second incompleteness theorem rules this out for the stated consistent T. Thus T cannot prove A_{T,D}'s global correctness. QED.

**Important exact boundary:** This result does not show that no mathematical proof of A_{T,D}'s correctness exists outside T. Indeed its correctness follows immediately in a stronger metatheory proving Con(T). It also does not preclude a proof compiler that relies only on the existence of a correct D and produces native proofs by a different argument.

## Verification and hostile controls

A standalone Python regression constructs all 510 binary words with 1<=|q|<=8, checks literal-distinct strict width-three syntax, exact decoding and the explicit SAT witness z=1; five malformed-range controls are rejected. All tests passed. These finite tests validate the encoding only, **not** incompleteness or any asymptotic lower bound.

Script: experiments/arc/lspv1_20261113_correctness_gate_encoding.py.  
Raw evidence: results/raw/arc/2026-11-13_LSPV1_CORRECTNESS_GATE_FINITE_ENCODING_RAW.json.

Hostile boundaries:
- If one invokes a decidable *completeness oracle* for T-proofs of correctness, that is an extra unjustified assumption; the program instead checks a *single alleged contradiction proof*.
- If T is inconsistent, the construction does not claim that A_{T,D} is correct.
- If T lacks standard Gödel-II derivability hypotheses, the unprovability conclusion must not be transferred silently.
- An "algorithm compiler" that covers only T-provably-correct programs is not proven to cover *every* correct polynomial-time SAT decider, even under SAT-in-P.
- A native R_mix341 derivation cannot be replaced by a T-proof or by an external check of the program trace.

## Impact on the proof spine

The user's highest-priority chain remains

$$
W_{\rm abs}(F_i)\le W_{R_{\rm mix341}}(F_i)
\le c_A\left(n_i+T_A(n_i)\right)^{r_A}.
$$

To derive P != NP, the first inequality requires a source-sound, all-native-transition, cost-nonincreasing whole-DAG abstract simulation. The second requires an independently demonstrated same-*historical*-calculus proof bound for **every** correct deterministic polynomial-time SAT decider A, with constants allowed to depend on A, not F_i. A superpolynomial lower bound for W_abs then produces the contradiction. None of those universal native premises is closed.

The present theorem gives a precise **B2/B3 transfer-design constraint**: a construction restricted to algorithms accompanied by correctness proofs in any one fixed T is incomplete as a universal arbitrary-decider transfer argument, absent a genuinely independent coverage theorem. It does not falsify every possible transfer, lower-bound any native proof work, or settle P versus NP.

Keep D1 source-qualification and B2/B3 compiler feasibility as parallel early gates; keep D1 -> C3 -> B1 logical dependence. P2-D1, P2-C3, P2-B1, P2-B2/B3 remain **OPEN**. Do not promote this result into a lower bound or equate unprovability in T with a SAT runtime lower bound.

## Actual corpus review

Read root proof1.txt (Git blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343), full proof2.txt via blob API (930c5eeddafce656717f28055a7a9a755f44737c), issue #3 with latest comments, AGENTS.md, CODEX.md, project skill, the user-directed 2026-11-13 full-chain review and five-role handoff, LSPV-3/617 /386 source-domain report, and historical LSPV-1/546, LSPV-2/539, LSPV-3/541, LSPV-4/547 handoff, plus later 619-623 comments. Current main.tex remains LSPV-5's canonical synthesis. This report does not independently rerun the original /341 or /386 native checkers, whose limitations remain as previously logged.

Primary background:
1. Gödel, K. (1931), *Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I*; scoped presentation and second-incompleteness hypotheses: https://plato.stanford.edu/entries/goedel-incompleteness/ .
2. Cook, S. A., Reckhow, R. A. (1979), *The Relative Efficiency of Propositional Proof Systems*, JSL 44:36-50. https://doi.org/10.2307/2273702 .
3. Cousot, P., Cousot, R. (1977), *Abstract Interpretation: A Unified Lattice Model*, POPL 238-252. https://doi.org/10.1145/512950.512973 .

The special algorithm construction and its scoped proof above constitute the run's new exact result; the underlying incompleteness theorem is classical. The report makes no claim of discovering a new Gödel theorem.

## Publication, ownership and disposition

Affected proof IDs: **P2-B2/P2-B3** transfer feasibility audit; P2-D1/P2-C3/P2-B1 still open.  
**TRACKERS REVIEWED; NO MATERIAL LOAD-BEARING NODE STATUS CHANGE.** The checker authentication, abstraction, lower-bound and transfer nodes stay OPEN. Root proof trackers are unchanged. Existing five hourly tasks, roles, Route labels, historical weights and ownership are unchanged. All new files are outside main.tex; no edit to another specialist's region is authorized. Full repository preflight and LaTeX compilation have not been performed. LSPV-5 independent review is required before integrating the result into the canonical synthesis.
