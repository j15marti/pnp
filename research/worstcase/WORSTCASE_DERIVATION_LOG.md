# Living log: worst-case derivation complexity W_R(N)

**Status: P versus NP OPEN. NP versus coNP OPEN. No superpolynomial W_R lower bound for a fixed strong R is established.**
Append-only; newest entry last. Status labels: PROVED/EXACT, KNOWN THEOREM, CANDIDATE, OPEN, FALSIFIED/RETIRED.

Target: W_R(N) = max over UNSAT F, |<F>|<=N, of min over derivations pi: F |-_R bottom of cost_R(pi). Strategy-discovery is free.

## Entry 2026-11-04 (scheduled run, single agent; the five-role split was not instantiated)

### CORPUS REVIEWED
Repo tree surveyed; AGENTS.md read. Searched for prior W_R / worst-case-derivation formulations: the nearest hits are LSPV-1 MUS-worstcase notes (e.g. research/coordination/2026-11-02_1832_LSPV1_MUS_WORSTCASE_QUOTIENT350_HANDOFF.md) and the LSPV-2/3/4 strict-ER / guarded-Tseitin / BPHP handoffs dated 2026-11-04. I did not re-read them in full, and I did not reconcile root main.tex this run. No LSPV ownership regions were touched.

### Literature check (primary-source follow-up still needed)
- Cook-Reckhow 1979: NP = coNP iff some propositional proof system is polynomially bounded. KNOWN THEOREM.
- Search results this run: best known Frege/EF size lower bounds are only linear to quadratic (secondary sources disagree; unverified). Davis-Robere, ECCC TR26-055: depth-d Frege refutes the statement "PHP has no short Frege proof", already in Res(log). Khaniki-Pich-Sokolov, CCC 2026: constructive lower bounds and efficient adversaries. Alekseev, ToC v22 a4: a PC extension that p-simulates Res-Lin and gives an alternative BVP lower bound. Proof Analysis Problem for EF is NP-complete (arXiv 2506.16956). None gives a superpolynomial EF/Frege bound. These are search-engine summaries, not read papers.

### Results this run

**P1 (quantifier-order trivialization) -- PROVED/EXACT, elementary.**
Let a "trace system" T take as derivation any pair (D, run) where D is a deterministic algorithm and the run is its accepting trace on F, with no requirement that D is a correct SAT decider on other inputs. Then for each F, min cost is at most |F| + O(1) (D hardcodes the answer), so W_T(N) = O(N). If correctness of D on all inputs is required, no fixed poly-time verifier can check it unless the system proves its own soundness (that is the content of the open problem). So max_F min_D is trivial, while min_D max_F is the real uniform question. Consequence: the bridge "SAT in P => W_R <= poly" must be stated for a sound fixed-verifier system R (Cook-Reckhow type) and not for trace systems.

**P2 (bridge dichotomy) -- PROVED/EXACT as a framing, with one KNOWN THEOREM input.**
With cost = proof length and a fixed poly-time verifier:
(a) "W_R superpolynomial for ALL sound R" is equivalent to NP != coNP (Cook-Reckhow), which implies P != NP. It is strictly stronger than what is needed, so it is not the weakest sufficient bridge.
(b) For a fixed R, "SAT in P => W_R <= poly" is equivalent to "P = NP => R is polynomially bounded". It holds for R = R_M, the system induced by an explicit poly-time M, because soundness is built in by definition. For natural R (Frege, EF) it is OPEN. I only know the route through provability of M's correctness in a bounded theory (PV/S^1_2 proving correctness, via Cook's translation, gives polynomial-size EF proofs). I recall this from memory and have not re-verified it in the literature; mark CANDIDATE for citation. That route needs P = NP to be provable in the theory, which is strictly more than P = NP.
(c) Hence the transfer theorem as written is not available for natural R without an extra uniform-provability hypothesis. A lower bound on W_R for natural R would therefore give "P = NP is unprovable in the matching bounded theory", not P != NP, unless a bridge is added.

**P3 (cost model note) -- PROVED/EXACT.** If cost is time or space of executing a derivation and not its length, then cost >= length for DAG-like systems, so length lower bounds transfer to cost lower bounds. The converse can fail (copying of shared nodes), so shared-DAG work costs must be charged by exact node-evaluation accounting.

### Hard-instance survival check
No new hard family constructed this run. For orientation only: PHP and Tseitin on expanders are exponentially hard for resolution (KNOWN), but have polynomial EF/Frege proofs (PHP: Buss, polynomial Frege; Tseitin: polynomial Frege/EF over GF(2) reasoning). So they do not survive "alternative reasoning methods". CANDIDATE needs for an EF-hard family remain OPEN.

### ADOPTED / REJECTED
Adopted: sound fixed-verifier formulation. Rejected: trace-system formulations of W (trivial by P1) and the pointwise form of the bridge.

### STALE OR OVERSTATED CLAIMS FOUND
The task's stated bridge "SAT in P => W_R poly" is not a theorem for natural R and may be false-or-unprovable-by-known-means; it should be treated as a CANDIDATE. See P2(b).

### Next targets
1. Primary-source verification of Cook / Krajicek-Pudlak statement in P2(b).
2. Decide whether an unconditional bridge exists for restricted R (e.g., resolution-width classes where P = NP is not needed and W_R is already known exponential: there the bridge's conclusion is false, so the bridge is FALSE for resolution unless SAT not in P). This is a sanity test: resolution W_R is exponential unconditionally, so "SAT in P => W_Res poly" is FALSIFIED for R = Res unless P != NP. Any usable bridge must therefore be restricted to R that are p-simulation-complete.

OPEN: every load-bearing arrow. P versus NP remains OPEN.

% END_OF_ENTRY 2026-11-04
