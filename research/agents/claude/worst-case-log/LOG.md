# Living log: worst-case derivation complexity W̄_R(N) (append-only, newest last)

Target: W̄_R(N) = max over UNSAT F, |F|<=N, of min over refutations π in R of cost_R(π). Free choice of optimal π (search not charged).
Bridge B3: SAT in P => W̄_R(N) <= poly(N), for a FIXED R. Status of everything below: P vs NP OPEN.

## 2026-11-06 — entry 1 (scheduled run)

**Corpus reviewed (survey):** root tree; AGENTS.md; research/coordination handoffs 2026-11-06 (LSPV-1/454, LSPV-4/447); tasks/ listing; main/ (517 files, newest REFEREE388). Not re-read byte-for-byte: older reports. Root main.tex (1.7 MB) not edited this run.
**Where the corpus stands (per latest handoffs, not re-verified by me):** B1/B2/B3 and full mixed-system superpolynomial W̄_R remain OPEN. Restricted results exist only for specific families/systems (Braun bit-PHP in Res(XOR); signed Tseitin vs. ordinary DAG Resolution/unit propagation).

**Literature check (standard search; no 2025–26 paper found that settles B3):**
- Cook–Reckhow: NP = coNP iff some proof system is polynomially bounded. P = NP => NP = coNP => *some* poly-bounded system exists, but it need not be the fixed R.
- Fixed-R bridge needs a provability hypothesis: if the theory R-captures (e.g. PV/S^1_2 for EF) proves "algorithm A decides SAT," then EF has poly-size proofs of UNSAT. Unconditionally "SAT in P => EF poly-bounded" is exactly the open region next to the optimal/p-optimal proof system question (Krajíček–Pudlák; Krajíček's notes on optimal systems). Cook–Krajíček: PV proving NP ⊆ P/poly collapses PH.
- Pich–Santhanam (ECCC TR23-199): EF-with-axioms lower bounds imply SAT circuit lower bounds, i.e. lower bounds for strong systems are at least as hard as circuit lower bounds. This is direction-consistent with our target but is a *barrier*, not a route.

**Classification (per AGENTS.md):**
1. Directly transferable: Cook–Reckhow equivalence (KNOWN THEOREM).
2. Analogy needing a new bridge: "free optimal strategy" = non-uniform/ nondeterministic choice; matches proof-size definition but not P-time.
3. Failed transfer risk: treating "SAT in P" as giving a *fixed* R short proofs without a reflection/provability premise. For R = EF this premise is not implied by P = NP.

**Consequence for the weakest bridge (CANDIDATE, no proof):** B3 is only plausibly provable in one of two shapes: (a) R is defined as the universal system "EF + reflection for the given decider" (then B3 is nearly tautological and a lower bound for it is as hard as P != NP); or (b) the hypothesis is strengthened to "SAT in P provably in the theory of R." Any claimed lower bound for fixed R must say which. This matches the corpus's existing reflection/"same-calculus noncircular" caveat.

**Status:** nothing new PROVED. Pointers only. OPEN: superpolynomial W̄_R for any R strong enough to carry B3; B3 itself; P versus NP.

**Next:** pick shape (b), state it as CONDITIONAL, and check whether the restricted families above survive it; red-team via the reflection reports in research/agents/lspv-1 (e.g. UNIVERSAL_REFLECTION_SINGLE_FAMILY353).
