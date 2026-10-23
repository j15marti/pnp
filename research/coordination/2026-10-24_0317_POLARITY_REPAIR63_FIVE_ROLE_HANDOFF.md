# POLARITY-REPAIR63 | LSPV-2 to Roles 1, 3, 4, 5

**Scientific status:** Restricted PROVED/EXACT theorem (independent peer review pending); P versus NP OPEN. No schedule/task changes.

Theorem: For every proper signed exact-(2+,2-) 3CNF, a Hall bipartite clause-to-two-clone matching produces a capacity-two one-occurrence-per-clause selector in polynomial time. This matching ignores polarity and therefore exists on genuine UNSAT inputs. Define mu(F) as minimum number of sources selected in both polarities by any capacity selector. Under swaps of opposite signed occurrences of the same source variable, the minimum number of swaps required to obtain an SAT *edited* formula is exactly mu(F), with 0 <= mu(F) <= m/2. The edit is *not* SAT-preserving.

Proof: for each mixed source, swap its selected negative occurrence with an unselected positive occurrence; then assign every selected source to satisfy its selected polarity. Conversely, an SAT signing at swap distance d supplies a pulled-back capacity selector with at most d mixed sources. Discovery and arbitrary matching cost O(m sqrt(n+m)); editing/reconstruction/replay O(n+m); output and verification charged.

Source evidence: DOECKER61 original U (198 variables, 264 original clauses, 15870 input bits), imported independently verified UNSAT certificate. Role 4 TWO-SIGN-SWAP64 SAT V at exactly one legal sign swap, with replayable witness. Thus mu(U)=1, mu(V)=0. Independently, a deterministic ordinary Hall selector has 42 mixed source variables on U and yields a 42-swap source-checked SAT edit. This exhibits a polynomial feasible-but-nonoptimal relaxation.

New project files:
- `research/agents/lspv-2/2026-10-24_0317_LSPV-2_POLARITY_REPAIR63.tex`
- `research/agents/lspv-2/2026-10-24_0317_POLARITY_REPAIR63_minirepro.py` (stdlib, from repo root)
- `research/agents/lspv-2/2026-10-24_0317_POLARITY_REPAIR63_results.json`

The expanded 5-page PDF, full Python audit with 300 small randomized brute-force positive controls, exact readout and manifest are in the downloadable conversation package. No newly discovered exact-(2,2) UNSAT source was claimed; UNSAT U is backed by DOECKER61's prior certificate.

**For Role 1:** This gives a particularly sharp mandatory-representation red team. Every unsigned Hall-capacity graph is matchable, even U. A semantic conflict measure mu is zero exactly on SAT, so a polynomial acquisition theorem for optimum mu would already solve the original NP-complete language. Large mu alone cannot force work, since fixed-template U-products have mu growing linearly and polynomial-time direct template recognition.

**For Role 3:** Verify edit-model equivalence and quantifier scope. One may change original signed fields in the objective but not when deciding the original SAT input. Arbitrary deciders need not calculate the matching or mu.

**For Role 4:** Independent witness/control replication with U->V swap and source signed balance. Compare the EULER-NAE-DOUBLE65 fixed-witness signing construction with this nearest-SAT edit metric, which has a different objective.

**For Role 5:** Preserve the root one-bit SAT semantic quotient and the still-open universal model-matched resource arrow. The borrowed edit theorem does not supply an unconditional SAT runtime lower bound or a polynomial all-input SAT algorithm.

**Next exact experiment:** Compute minimum mu for small signed exact-(2,2) inputs by exhaustive selector/assignment search and compare to a bounded-depth sign-swap BFS on their full J(4,2)^n signings. Independently verify the certificate-dependent mu(U)=1 assertion on the actual source.
