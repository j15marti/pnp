# LSPV-3/548: Quantifier audit of Williams exponent and abstract branch certificates

**November 9, 2026, 19:20 PST | Hypergraph & Proof Certificates | Route B | PROVED/RESTRICTED logical audit + COMPUTATIONAL controls | P versus NP OPEN**

## Candidate and falsifiers

Test the claim that the later SAT time-space threshold L=2cos(pi/7) directly supplies a positive-space product constraint c+s>=L. The immediate peer target is [P2-L5-473], which asserts that its later constraint yields s>=0.6019377358 at c=6/5. Falsifiers: (F1) authentic exact published theorem giving this product constraint on the same machine; (F2) illicit promotion from subpolynomial space to a particular fixed positive space exponent; (F3) treating a rejecting NP path as deterministic UNSAT; (F4) counting proof nodes or possible configurations as physical work memory.

Recovered verified November 9 16:24 assumed-time five-role handoff, older negative-abstraction handoff, both root trackers, issue #3, AGENTS.md, CODEX.md, repo research skill, and actual reports LSPV-3/382, /545, /547, LSPV-1/551, LSPV-5/473, plus earlier Grok/Claude evidence. Reviewed exact required external repository files: konard/p-vs-np README blob 0e0ec77f, blkph0x/p-vs-np-proof-research METHOD_INDEX blob 18d693ea, meelgroup/frat-xor format blob 986a21aa, tanyongkiam/cake_lpr README blob e94f45e9, openai/math README blob cc5b0a03. These do not authenticate native R_mix341.

## Theorem 548.1 (quantifier non-implication; PROVED/RESTRICTED)

Let D(c,s) denote nonmembership of SAT in simultaneous deterministic time N^(c+o(1)) and space N^(s+o(1)) on a *matched fixed random-access machine model*, with boundary conventions treated strictly. The qualitative theorem schema
$$
\forall c<L\;\exists \delta(c)>0:\ D(c,\delta(c)),\qquad L=2\cos(\pi/7)
$$
does NOT imply
$$
\forall c<L\;\forall s<L-c:\ D(c,s).
$$
Proof: construct a logical interpretation with D(c,s) true exactly when s<delta(c), and delta(6/5)=1/100. The first proposition holds but D(6/5,11/20) is false, despite 11/20 < L-6/5. This is a countermodel to a *proposed inference between theorems*, NOT a construction of a SAT algorithm or a counterexample to any actual lower bound.

Williams (2008) expressly gives for every c<L some positive d(c) excluding simultaneous N^c time and N^d space; Buss-Williams (2015) characterize the zero-space endpoint and separately quantitative positive-space tradeoffs. A full exact theorem with c,s and matching model must be supplied before substituting d(c)=L-c. Consequently the numerical lower exponent 0.6019377358 in [P2-L5-473] is **NOT YET SOURCE-AUTHENTICATED** by its cited headline. The earlier native-address/sparse-normalization parts of [P2-L5-473] remain valid. This audit does not prove that no different theorem establishes the product inequality.

The independently sourced earlier Fortnow/van Melkebeek displayed threshold
$$
\beta(c)=\tfrac12((c+2)/c^2-c)
$$
gives at c=6/5 exactly 23/45, exceeding 1/2 by exactly 1/90. With c=6/5 and s=11/20, beta<s<L-c. These exponents expose the *logical gap in the citation-based inference*, without implying any feasible SAT decider. Optimized 2005 FLMV d_k and later precise positive-space tradeoffs remain separate verification obligations. SAT in P does not grant c=6/5.

## Theorem 548.2 (typed complete machine abstraction and polarity; schematic soundness)

Fix the entire binary original input x of length N and machine model M. A concrete configuration carries the control state and transition phase, full input-head and output state, all non-index work tape contents/head positions, all index tape contents/head positions, native highest indexed or read position H, simultaneous live storage L_live, time and output counters, deterministic or nondeterministic choice history, assumption context Gamma, source provenance, auxiliary definitions, private/exported wire interfaces, and the ENTIRE shared paid proof DAG with globally unique paid owner/node IDs. This is a **complete** state, not merely the current formula or one branch. All phases (parsing, validation, derivation, choices, indexed accesses, output, cleanup, conversion) are charged.

For a fixed state universe C, let an abstract element store MAY sets of possible control, choice, output, source, context, DAG and wire states and interval bounds on time, native H and peak live storage. Define alpha(X) to be a containing product hull and gamma(a) to be all complete states satisfying its constraints. The best transformer is
$$
\mathrm{Post}^{\#}(a)=\alpha(\mathrm{Post}(\gamma(a))).
$$
Then every concrete legal step (deterministic successor, EACH nondeterministic choice, source read, indexed jump, shared-lemma reuse, AND3, Resolution, GF(2), LOCAL-CONVERT, paid defining facet, possible branching/discharge) maps into the abstract successor and every completed goal is preserved. The inclusion is immediate from gamma(alpha(X)) containing X. **This defines a correct but generally noncomputable best abstraction**, not an effective solver. Every implemented approximation must prove step inclusion for the full authenticated grammar; unknown native rules must be conservatively overapproximated, not omitted.

Correct resource polarity: a finite abstract U_H that contains ALL concrete peak H values proves a concrete upper bound; a budgeted abstract proof-system *minimum distance* underapproximates concrete minimum cost only if every concrete paid run maps to an abstract run of NO GREATER cost and the goal maps to a goal. Cardinality of the abstract configuration space alone proves neither actual work-tape memory nor computation time. An NP accepting path is an OR witness for SAT, whereas UNSAT demands absence of every accepting path, or a separately sound universal AND discharge. A rejecting NP path establishes neither UNSAT nor deterministic FLMV applicability. Flat verification of a separately supplied B-bit certificate from [P2-L3-547] is not certificate acquisition from the N-bit source. LSPV-3/382 already shows that a general semantic-original-support guard can be coNP-hard, so /547's local logspace predicate cannot be silently assumed for historical LOCAL-CONVERT.

## Independent checks (COMPUTATIONAL)

A locally executed Python Fraction/Decimal program independently proves arithmetic identities exactly and tests SAT, UNSAT, another SAT input, and malformed source rejection. A separately written JavaScript CASE/LEAF certificate checker accepts a complete UNSAT two-leaf/one-CASE proof, rejects a SAT-to-UNSAT forgery, a wrong original clause, a missing AND branch, incompatible assumption contexts, and duplicate node IDs, and accepts a 30-digit legal identifier. The JS implementation uses a TEST-ONLY calculus, not the historical checker; neither program measures native FLMV space. Raw source and independent Python outputs are preserved in the run's local reproduction archive.

For N=10^6, 10^12, 10^24, 10^60, the exponent-only comparison N^(23/45)/N^(1/2) equals N^(1/90), approximately 1.16591, 1.35936, 1.84785, 4.64159, respectively. These are NOT numerical bytes/cells or finite-N lower bounds.

## Continuity, barriers and remaining gap

The new result is a quantifier/source-authentication correction, not stronger P-vs-NP progress. Keep separate ideal logical proof work, evidence bits, native indexed high-water, actual all-phase time and space, span, and live peak; reconvergent shared DAGs charge each paid node once. No CEGAR refinement may remove genuinely permitted historical shortcuts. Relativization, algebrization and proof-system transfer barriers are not addressed by these finite tests.

Exact OPEN nodes: [P1-01],[P1-03],[P1-04],[P2-A2],[P2-D1],[P2-C3],[P2-B1],[P2-B2], and B3. Next falsifier: retrieve the **actual positive-space quantitative** c-versus-s theorem (not its endpoint headline) in Williams/Buss-Williams and verify its random-access model before asserting any numerical lower envelope; concurrently authenticate native R_mix341 LOCAL-CONVERT accepted-byte syntax. P versus NP OPEN.

### Primary literature
1. Fortnow, Lipton, van Melkebeek, Viglas, Time-Space Lower Bounds for Satisfiability, JACM 2005, https://doi.org/10.1145/1101821.1101822 . Exact Section 2.1 machine model: https://lance.fortnow.com/papers/files/tst.pdf .
2. Fortnow and van Melkebeek, DIMACS TR 2000-06, https://archive.dimacs.rutgers.edu/TechnicalReports/abstracts/2000/2000-06.html .
3. Williams, Time-Space Tradeoffs for Counting NP Solutions Modulo Integers, 2008, https://eccc.weizmann.ac.il/report/2007/036/ .
4. Buss and Williams, Limits on Alternation-Trading Proofs for Time-Space Lower Bounds, 2015, https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/ .
5. Cousot and Cousot, POPL 1977; D'Silva, Haller and Kroening, Abstract Satisfaction, POPL 2014.
