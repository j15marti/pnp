# DEPTHWIDTH1: free-2-SAT decision depth is Omega(n) on random UNSAT 3-CNF; TWOSATDEC ratio-3.5 sampling retired

P versus NP remains OPEN. No unrestricted runtime or circuit lower bound is claimed. This is a proof-system (resolution width) statement and carries the AGENTS.md restriction: no unrestricted runtime claim from restricted proof complexity.

## Dependency advanced

SAT-LOCAL-ERROR1 / the TWOSATDEC question: does free exact 2-SAT closure plus a depth-r variable decision certify UNSAT exact-layer 3-CNFs with bounded r? Runs TWOSATDEC87-89 (q=92,93,94) were empty draws. They carry no information, and this note explains why and settles the asymptotic question with known theorems.

## 1. Why the draws are empty (KNOWN THEOREM)

TWOSATDEC samples t = floor(3.5 q) clauses, which is density 3.5. Random 3-SAT is satisfiable with high probability at every density below 3.52 (Kaporis, Kirousis, Lalas 2006; Hajiaghayi, Sorkin 2003). So Pr[UNSAT] -> 0 at density 3.5, and an empty UNSAT residual is the predicted outcome at large q. Continuing to raise q at density 3.5 cannot produce a residual. **Status: the ratio-3.5 increment protocol is RETIRED as a progress source.** The earlier depth-5 survivors at small q (30, 32, 38, 42) are finite-size UNSAT tails.

## 2. Depth-to-width transfer (PROVED; standard argument; independent review pending)

Notation. F is a 3-CNF. For a partial assignment rho, F|rho deletes the clauses that rho satisfies and the literals that rho falsifies. For rho on a set S, let C_rho be the clause of the |S| literals that rho falsifies, so rho is the unique assignment of S falsifying C_rho. Width means the largest clause in a derivation. Resolution here has no weakening rule.

Lemma 2.1 (refuting the restricted formula). If unit propagation on F|rho reaches an empty clause, or reaches a fixpoint alpha whose width-at-most-2 part K is unsatisfiable, then F|rho has a resolution refutation of width at most 3.
Proof. Unit propagation is unit resolution. Each propagated unit comes from an axiom of width at most 3 by resolving against earlier units, and each such step lowers the width. A conflict is the empty clause derived this way. Otherwise every clause of K is D|alpha for an axiom D, obtained the same way, with width at most 3. Resolution is complete, so the unsatisfiable K has a refutation. Two clauses of width at most 2 have a resolvent of width at most 2+2-2 = 2, so every line of that refutation has width at most 2. The whole refutation has width at most 3.

Lemma 2.2 (lifting). If F|rho has a refutation of width w and rho assigns r variables, then F has a derivation of some subclause of C_rho of width at most w+r.
Proof. Replace each axiom C|rho by its parent C. C differs from C|rho only by literals that rho falsifies, and these lie in C_rho. By induction, each line D of the refutation becomes a line D' with D a subset of D' and D' a subset of D or C_rho. The resolved variable of every step lies outside S, because F|rho has no S-variables. So each step remains a valid resolution step, and the resolvent of D1' and D2' is a subset of the resolvent or C_rho. The empty clause becomes a subclause of C_rho. Every line has width at most w+r.

Lemma 2.3 (decision-tree assembly). Suppose that for every assignment rho of S={x1,...,xr} there is a derived subclause E_rho of C_rho. Then the empty clause follows by a derivation of width at most r.
Proof. Induct down the complete decision tree. Take a partial assignment sigma on x1,...,x_{i-1}, and let E0 and E1 be the clauses obtained at its two children. Each Eb is a subset of C_sigma together with the literal falsified by x_i=b. If either Eb misses its x_i-literal, it is already a subclause of C_sigma. Otherwise resolve E0 with E1 on x_i, and the resolvent is a subset of C_sigma. At the root, C_empty is the empty clause. Every clause is a subclause of some C_sigma, which has width at most r.

Theorem 2.4. If an r-set S certifies F under the TWOSATDEC semantics, then F has a resolution refutation of width at most r+3, and of size 2^r poly(|F|).
Proof. Apply Lemma 2.1, then Lemma 2.2 with w=3, to every assignment of S. Then apply Lemma 2.3.

Contrapositive: if every resolution refutation of F has width W, every certifying set has r >= W-3.

## 3. Random 3-CNF consequence (KNOWN THEOREM + 2.4)

Width-expansion (Ben-Sasson and Wigderson, J. ACM 48(2), 2001). Define mu(C) as the fewest axioms that semantically imply C. Then mu(axiom)=1, mu(empty clause) > s when every set of at most s clauses is satisfiable, and mu is subadditive under resolution. Hence some line C of any refutation has s/2 < mu(C) <= s. Take a minimal set T of mu(C) axioms implying C. Every boundary variable of T, one that occurs in exactly one clause of T, must occur in C. So |C| >= min over s/2 < |T| <= s of |boundary(T)|.

Random 3-CNF with Delta*n clauses, Delta constant. With high probability it is a boundary expander up to size s = Theta(n/Delta^{1+eps}) (Chvatal and Szemeredi 1988; Ben-Sasson and Wigderson 2001). This gives W = Omega(n/Delta^{1+eps}).

Corollary 3.1 (precise form). For every constant Delta and eps > 0, with probability 1-o(1) over F, F is satisfiable or every free-2-SAT certificate has r >= c_eps n/Delta^{1+eps} - 3.

Correction to the earlier summary. Corollary 3.1 is unconditional. The conditional form, "given that F is UNSAT, r = Omega(n) w.h.p.", follows only when Pr[UNSAT] is not o(the expansion failure probability). This holds for every Delta above the proven unsatisfiability bound, about 4.49, where Pr[UNSAT] -> 1, and in particular at Delta = 6. At density 3.5 the conditional statement is NOT claimed.

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
