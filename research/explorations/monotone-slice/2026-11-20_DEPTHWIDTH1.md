# DEPTHWIDTH1: free-2-SAT decision depth is Omega(n) on random UNSAT 3-CNF; TWOSATDEC ratio-3.5 sampling retired

P versus NP remains OPEN. No unrestricted runtime or circuit lower bound is claimed. This is a proof-system (resolution width) statement and carries the AGENTS.md restriction: no unrestricted runtime claim from restricted proof complexity.

## Dependency advanced

SAT-LOCAL-ERROR1 / the TWOSATDEC question: does free exact 2-SAT closure plus a depth-r variable decision certify UNSAT exact-layer 3-CNFs with bounded r? Runs TWOSATDEC87-89 (q=92,93,94) were empty draws. They carry no information, and this note explains why and settles the asymptotic question with known theorems.

## 1. Why the draws are empty (KNOWN THEOREM)

TWOSATDEC samples t = floor(3.5 q) clauses, which is density 3.5. Random 3-SAT is satisfiable with high probability at every density below 3.52 (Kaporis, Kirousis, Lalas 2006; Hajiaghayi, Sorkin 2003). So Pr[UNSAT] -> 0 at density 3.5, and an empty UNSAT residual is the predicted outcome at large q. Continuing to raise q at density 3.5 cannot produce a residual. **Status: the ratio-3.5 increment protocol is RETIRED as a progress source.** The earlier depth-5 survivors at small q (30, 32, 38, 42) are finite-size UNSAT tails.

## 2. Depth-to-width transfer (PROVED, standard; independent review pending)

Lemma. Suppose an r-set S certifies F under the TWOSATDEC semantics: every assignment rho of S, after unit propagation, yields an empty clause or an unsatisfiable width-at-most-2 skeleton. Then F has a resolution refutation of width at most r+3.

Proof. Fix rho. Unit propagation is unit resolution, which never produces a clause wider than its 3-clause premise. An unsatisfiable 2-CNF has a resolution refutation of width at most 2, via the implication-graph cycle x -> ~x -> x: resolving 2-clauses yields clauses of width at most 2. So F|rho has a refutation of width at most 3. Weakening every line by the negation of rho's literals turns it into a derivation of the clause ~rho from F, of width at most r+3. Resolving the 2^r clauses ~rho along the complete decision tree on S gives the empty clause, and every intermediate clause has width at most r. QED.

## 3. Consequence (KNOWN THEOREM + Lemma)

Ben-Sasson and Wigderson (JACM 2001, "Short proofs are narrow"): for a random 3-CNF with n variables and Delta*n clauses, Delta constant, every resolution refutation has width Omega(n / Delta^{1+eps}) with high probability. Combined with the Lemma, every certifying set satisfies r >= c n / Delta^{1+eps} - 3 w.h.p., for every constant density at which the formula is UNSAT. **Bounded-depth free-2-SAT certification fails asymptotically on the exact layer, at every constant density.** The certifier is also a size-2^r-poly(n) tree-like procedure, so this agrees with Chvatal and Szemeredi (1988), who proved exponential resolution size.

## 4. Computation (COMPUTATIONAL; consistent with the theorem, not a proof)

Script: `experiments/monotone_slice/depth_width_transfer.py`. Seed 20261120, density 6.0, 3 UNSAT draws per n (complete DPLL filter), exact minimum certifying depth up to rmax=4.

| n | 8 | 12 | 16 | 20 | 24 | 28 | 32 | 36 |
|---|---|---|---|---|---|---|---|---|
| min depth | 2,2,2 | 2,2,2 | 2,2,2 | 3,2,3 | 3,3,3 | 3,3,3 | 3,4,3 | 3,4,4 |

Total runtime 4.3 s. Raw data: `results/raw/monotone_slice/DEPTHWIDTH1.txt`. The minimum depth grows with n, as the linear-width bound predicts with a small constant.

## Gates

- **DISJ:** NOT APPLICABLE. This is a statement about a refutation system, not a communication protocol.
- **Relativization:** NOT APPLICABLE. The statement is a proof-system lower bound, not a class separation.
- **Simultaneous DTISP:** NOT APPLICABLE. No time-space claim is made.
- **Deterministic configuration:** PASS as a consistency check. The 2^r n^{O(1)} certifier is a genuine upper bound, and nothing is inferred from it beyond that.
- **Natural Proofs / algebrization:** NOT APPLICABLE. There is no circuit claim.

Controls: 2-SAT and Horn formulas remain depth 0 to 1, as the easy-family guard requires.

## Falsifiers

1. A UNSAT random 3-CNF family at constant density with an O(1)-depth certifier. This is impossible by the Lemma together with Ben-Sasson and Wigderson.
2. An error in the weakening step. It is standard (Ben-Sasson and Wigderson, Lemma 3.2 style).
3. A scaling mismatch: depth stuck at 2 or 3 for n up to about 60 at density 6. That would point to a constant issue, not a contradiction.

## Next lemma

Retire ratio-3.5 increments. The only remaining non-trivial content of SAT-LOCAL-ERROR1 concerns small monotone circuits (not decision depth). Transfer requires a monotone-circuit-to-resolution-width (or cutting-planes) simulation, which is not known in general. That is the named open dependency.

## Sources reviewed this run

- The user's Google Doc "P vs. NP Proof Attempts". Read: the headings and the first approx. 6k of 62.6k characters (md5 9cbc6bd2cc61ad2dd208e93e7b812d7d). It is a survey of holographic, tensor-network, IPS, GCT and magnification barriers. No new SAT-depth content in the portion read.
- GitHub repository search (google, google-deepmind, openai orgs; queries for SAT solvers, proof complexity and resolution width): 0 results returned in this session.
