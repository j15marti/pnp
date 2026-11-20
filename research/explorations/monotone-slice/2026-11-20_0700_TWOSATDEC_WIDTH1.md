# TASK-008: TWOSATDEC-WIDTH1. Width bound for free-2-SAT decision certificates; the q+1 series design is retired

P versus NP remains OPEN. No monotone-circuit or general circuit lower bound is claimed. This note covers one restricted refutation format, the TWOSATDEC depth-r certificate.

## Why the series is being stopped

TWOSATDEC6 through TWOSATDEC95 sample the exact layer at `t = floor(3.5 q)` clauses. A density of 3.5 is **below** the proved satisfiability lower bound of about 3.52 for random 3-SAT (Kaporis, Kirousis and Lalas 2006; Hajiaghayi and Sorkin 2003; both use with-replacement clause models, and the transfer to the exact layer is below). So `Pr[UNSAT] -> 0` as `q` grows. The empty draws at `q = 94..100` are what that theorem predicts, and they say nothing about SAT-LOCAL-ERROR1. Further `q -> q+1` runs at density 3.5 are the parameter-repetition that AGENTS.md says does not count as progress. **Status of the series design: RETIRED.** This is about the protocol only. The recorded raw data stays intact.

## Candidate and falsifiers (stated before the source check)

Candidate: on the exact layer at a fixed supra-threshold density, the minimum depth of a free-2-SAT certificate grows linearly in `q` with high probability. Any hypothesis that bounded decision depth captures slice-UNSAT is then false.

Falsifiers considered:
(a) a certificate gives no resolution-width bound because width-3 survivors are discarded;
(b) the width lower bound does not transfer to the exact (without-replacement) layer;
(c) small-`n` data show the depth staying bounded.

None of the three held (see below).

## Lemma (PROVED. Composition of known theorems; not independently reviewed)

Let `F` be a 3-CNF and `R` a set of `r` variables. Suppose every assignment `rho` of `R`, after unit propagation, gives either an empty clause or an unsatisfiable width-at-most-2 skeleton. This is exactly the TWOSATDEC certificate. Then the resolution width satisfies `w(F |- bot) <= r + 3`.

Proof. Fix a leaf `rho`. Every unit-propagation step resolves a clause of `F|rho` against a derived unit, so each derived clause is a subclause of an axiom and has width at most 2. An unsatisfiable 2-CNF has a resolution refutation that uses only clauses of width at most 2, because the resolvent of two 2-clauses has width at most 2 and resolution is complete. Hence `w(F|rho |- bot) <= 3`. Next, lift this refutation to `F` by re-adding the literals of `rho`. This gives a derivation of a subclause of the clause falsified by `rho`, of width at most `3 + r`. That is the standard restriction lemma (Ben-Sasson and Wigderson 2001, Lemma 3.2), applied `r` times. Finally, resolve the `2^r` lifted clauses along the complete decision tree on `R`. Every intermediate clause there uses only `R`-literals, so it has width at most `r`. QED.

Falsifier (a) is therefore dead: discarding width-3 survivors makes the certificate weaker, so the lemma still applies.

## Theorem (PROVED modulo the constant in a cited bound; not independently reviewed)

Fix a constant `Delta >= 4.51`, which is above the proved unsatisfiability upper bound of about 4.4898 (Díaz, Kirousis, Mitsche and Pérez-Giménez 2009). Take `F` uniform on the exact layer with `t = floor(Delta q)` distinct proper 3-clauses on `q` variables. Then, with probability `1 - o(1)`:

1. `F` is UNSAT.
2. Every free-2-SAT certificate of `F` has depth `r >= c(Delta) q - 3` for some `c(Delta) > 0`.

Proof. Ben-Sasson and Wigderson (2001, section 6, building on Chvátal and Szemerédi 1988) show that random 3-CNF at constant density has resolution width `Omega(q / Delta^{1+eps})` with high probability. Combine this with the lemma.

Transfer to the exact layer (falsifier (b)). The with-replacement model with `t = Theta(q)` draws repeats a clause with probability `O(t^2 / q^3) = o(1)`. Conditioned on no repeat, it is exactly uniform on the layer. So any property that holds with probability `1 - o(1)` in one model also holds with probability `1 - o(1)` in the other.

To do: check the exact constant and quantifier form of the BSW random-CNF width theorem against the primary source. That check was not done this run.

Consequence: "bounded decision depth plus free exact 2-SAT" is FALSIFIED as an asymptotic capture mechanism for slice-UNSAT at supra-threshold density. The depth-5 survivors at q = 30, 32, 38 and 42 are expected, not anomalies. The case of UNSAT formulas at density 3.5 (a conditioned rare event) is not decided here, because `Pr[UNSAT]` may be smaller than the failure probability of the width bound. That case stays OPEN.

## Computational check (COMPUTATIONAL)

Script: `experiments/monotone_slice/twosat_backdoor_depth_growth.py` (sha256 `8ea69699…`). It uses the with-replacement clause model and computes the exact minimum `r` over all variable subsets with `r <= 6`. SAT is decided by DPLL. The DPLL was cross-checked against brute force: 0 mismatches out of 300 instances at `n = 10`, `m = 45`.

| Delta | seed | n | UNSAT/N | min r per UNSAT instance |
|---|---|---|---|---|
| 4.5 | 20261120 | 12 | 4/12 | 2 2 2 2 |
| 4.5 | 20261120 | 18 | 3/12 | 3 3 3 |
| 4.5 | 20261120 | 24 | 9/12 | 3 4 3 3 4 4 3 3 3 |
| 4.5 | 20261120 | 30 | 4/12 | 4 4 3 5 |
| 6 | 20261121 | 24 | 6/8 | 3 2 3 3 3 2 |
| 6 | 20261121 | 32 | 8/8 | 4 4 3 3 3 3 3 3 |
| 6 | 20261121 | 40 | 8/8 | 4 4 3 4 4 4 4 4 |

The depth grows with `n` and the data do not show it staying bounded (falsifier (c) did not hold). These are finite tests and not an asymptotic proof. The proof above is the authority for the asymptotic statement.

Raw data: `results/raw/monotone_slice/TWOSATDEC_WIDTH1_depth_growth.txt` (sha256 `91a0e49b…`). Base revision `3118ba4b`, Python 3.11.18.

## Gates

- DISJ: NOT APPLICABLE. This is a proof-format statement with no communication claim.
- Relativization: NOT APPLICABLE. This is a concrete propositional proof system, not oracle machines.
- Simultaneous DTISP: NOT APPLICABLE.
- Deterministic configuration counting: NOT APPLICABLE.
- Natural Proofs and algebrization: NOT APPLICABLE. The statement is a proof-complexity lower bound for a subsystem of resolution and implies nothing about circuits.

Free-2-SAT certificates are a subsystem of resolution, where exponential lower bounds are already KNOWN. No consequence for P/poly or for NP versus coNP follows.

## Next lemma and integration point

Integration point: this closes the "bounded-depth capture" reading of SAT-LOCAL-ERROR1. Any surviving version must use an approximator outside tree-like or bounded-width resolution. Next lemma: give a precise statement of what SAT-LOCAL-ERROR1 requires of a monotone approximator that is not a decision-depth certificate. If it implies a resolution-width or degree bound, it is already refuted by Ben-Sasson and Wigderson or by Alekhnovich and Razborov; if not, name the model. The governing definition of SAT-LOCAL-ERROR1 / DIRECTIONALTELESCOPE1 could not be found anywhere in the repository on this run. That is a blocker that should be repaired.

## Sources surveyed this run

The user's "P vs. NP Proof Attempts" Google Doc was read in full. It covers holographic algorithms, tensor-network contraction, IPS, GCT, IPS functional lower bounds and hardness magnification. Its theme that the frontier lies in proof-complexity lower bounds is consistent with this note, and it contains no claim that conflicts with it.

GitHub search of the openai, google and google-deepmind organisations turned up these pointers:

- `openai/math` `lean/OAI/Probability/SATComputability/LowerBounds.lean`
- `openai/math` `lean/ComparatorChallenges/SubexponentialSAT.lean`
- `openai/math` preprint "Variance of the Random k-SAT Hitting Time" (2026-09-27)
- `google-deepmind/formal-conjectures` `FormalConjectures/Millennium/PvsNP.lean`

They are recorded as pointers only; they were not read beyond search fragments, because of the repository scope limit.
