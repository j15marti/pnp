<!-- CLAUDE REPORT::BRIDGE-DICHOTOMY-0001::2026-11-05 -->
# CLAUDE/BRIDGE-DICHOTOMY-0001: status of the bridge "SAT in P => W_R(N) <= poly(N)"
Scheduled run, 2026-11-05. **P versus NP remains OPEN. Nothing below proves a lower bound.**

## Scope
Target: the worst-case min-derivation functional W_R(N) = max over UNSAT F (|<F>|<=N) of min over refutations pi of cost_R(pi), strategy discovery uncharged, and the weakest bridge SAT in P => W_R(N) <= poly(N). Corpus touched: LSPV-1/423 (exact mixed AND3/XOR optimum 4h-1 on cubic Tseitin; restricted, upper-bound/optimum for one family in one system), the LSPV-5 p-optimality referee notes (334, 344, 357), the world ledger. No duplicate of the dichotomy below was found as a single statement; its ingredients (p-optimality firewall) are already in the corpus.

## Dichotomy (KNOWN THEOREM-level reasoning, short proofs)
Let R be a fixed Cook-Reckhow proof system (poly-time verifier, sound, complete).
1. **R with a known unconditional superpolynomial lower bound** (resolution, bounded-depth Frege, cutting planes, ...): W_R is superpolynomial, so the bridge is true iff SAT not in P. Proving the bridge for such R is equivalent to proving P != NP; it is circular as a route and gives no leverage.
2. **R with no known lower bound** (Frege, Extended Frege, stronger): the bridge is a genuine open implication. P = NP does not obviously make EF p-bounded; the natural attempt, a system whose proofs are "algorithm M plus its run on F", is not a proof system because soundness of M is not poly-time checkable. Making that sound requires a p-optimal system, whose existence is a standing open problem (Krajicek-Pudlak). So the bridge for a fixed natural R needs either a p-optimality-type theorem or a direct simulation of an arbitrary polynomial SAT decider by R, which is the "simulation" target the directive already labels secondary and strictly harder in appearance.
3. **Existential version is trivial.** If SAT in P then NP = coNP, so some proof system is p-bounded. The bridge must therefore be about a *fixed, named* R chosen independent of the SAT algorithm, which is exactly why 2 is hard.

Consequence for planning: any W_R lower bound that is proved for R in case 2 would imply EF/Frege lower bounds (a major open result), and one in case 1 adds nothing. The only non-circular progress channels are (a) lower bounds for systems strictly between, with a proved transfer theorem, or (b) conditional/relativized evidence. Status: ANALYSIS, no new CANDIDATE theorem.

## Literature check (this run)
- Davis-Robere (ECCC 2026/055): Res(log) proves depth-d Frege lower bounds against itself via a constructive switching lemma. Useful analogy for *self-referential* bridges; transfer to W_R for strong R is not established (ANALOGY).
- Papamakarios (CCC 2024): non-automatability of bounded-depth Frege of every depth (under crypto-style assumptions). Relevant because it says finding optimal derivations is itself hard for weak systems, consistent with granting free strategy only for lower bounds.
- Proof Analysis Problem (arXiv 2506.16956): proving resolution lower bounds on satisfiable formulas is NP-complete for EF; P = NP gives automatability for every system, again showing P = NP is the natural hypothesis for case 2 but not sufficient for p-boundedness.
- Filmus-Pitassi-Santhanam: AC0-Frege exponential lower bounds imply superpolynomial Frege lower bounds (so strengthening within the Frege hierarchy has a known amplification, relevant to channel (a)).

## Suggested next obligation
State and test channel (a): find the strongest R with a *provable* transfer SAT in P => W_R poly (e.g. R defined relative to a fixed polynomial-time-verifiable certificate class of the already-established exact optima, such as LSPV-1/423 families) and check whether W_R lower bounds there survive a size-matched adversarial family. Red-team question: does any such R collapse into case 1 or into a p-optimal-system assumption?

% END_OF_VERIFIED_REPORT::CLAUDE::BRIDGE-DICHOTOMY-0001
