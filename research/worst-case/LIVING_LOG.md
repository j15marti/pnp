# Living log: worst-case minimum derivation cost W_R(N)

Append-only. Status words per AGENTS.md. Directive: `research/coordination/2026-11-09_WORST_CASE_DERIVATION_COST_SHARED_DIRECTIVE.md`.
P versus NP remains OPEN.

## Entry 001 — 2026-11-09 (scheduled run, first entry)

### Setup
W_R(N) = max over UNSAT F, |F|<=N, of min over R-derivations pi of cost_R(pi); B_R: SAT in P => W_R <= poly.

### T1 (KNOWN THEOREM, Cook–Reckhow 1979) — free search = nondeterministic measure
Some sound poly-time-verifiable proof system has W_R poly iff NP = coNP. Because discovery cost is not charged,
W_R is a *nondeterministic* quantity. A superpolynomial bound for **every** R would therefore prove NP != coNP,
strictly more than P != NP (NP != coNP implies P != NP). A lower bound for one fixed R proves only that R is not p-bounded.
Consequence: the "free optimal sequence" relaxation is legitimate but is exactly what makes the all-R route stronger than needed;
the fixed-R route needs a transfer theorem.

### T2 (PROVED/EXACT, elementary) — the bridge is circular for every R with a known lower bound
Let R be fixed with W_R superpolynomial *known unconditionally* (resolution: Haken 1985; cutting planes: Pudlak/Krajicek;
bounded-depth Frege: Ajtai, Krajicek–Pudlak–Woods, Pitassi–Beame–Impagliazzo). Then
B_R  <=>  SAT not in P  <=>  P != NP.
Proof: (=>) B_R plus W_R superpoly gives SAT not in P by contraposition. (<=) if SAT not in P the implication is vacuous.
Meaning: for those systems the "weakest sufficient bridge" is not weaker than the goal. A lower bound on W_R plus B_R
gives P != NP only if B_R is proved *independently* of the lower bound, so B_R is useful only for R whose p-boundedness is
unknown (Frege, Extended Frege, or a stronger combined system). Do not count any resolution/CP/AC0-Frege lower bound as progress on B_R.

### T3 (PROVED/EXACT, restatement) — B_EF in correctness-proof form
B_EF <=> [SAT in P => some (equivalently every) correct poly-time SAT decider M has poly-size EF proofs of the
correctness tautologies Cor_{M,n} ("M(F)=0 implies F unsat", size poly(n))].
(<=) is Cook's argument: a derivation = EF proof of Cor_{M,n} + the trace of M on F. (=>) if SAT in P and EF is p-bounded
(by B_EF), the tautologies Cor_{M,n} have poly proofs. So the bridge is the open question "P = NP implies feasible provability
of the solver's correctness". It is a reformulation, not progress; this is the weakest *exact* form found so far and it
isolates the missing theorem (provability of correctness in a fixed feasible theory, cf. PV / bounded arithmetic).
Barrier: for a fixed R, P = NP with a solver whose correctness is not feasibly R-provable would falsify B_R; no known
unconditional argument rules this out, and none forces it.

### Cost-accounting lemmas (PROVED/EXACT, trivial) for the resource auditor
steps(pi) <= work(pi) <= steps(pi) * maxstate(pi); peak space(pi) <= maxstate(pi). For resolution, width/space lower bounds
(Ben-Sasson–Wigderson; Atserias–Dalmau) lower-bound these measures, but T2 says they do not transfer.

### Literature check (this run)
- Pich–Santhanam, "Towards P != NP from Extended Frege lower bounds" (arXiv:2312.08163, ECCC 2023): conditional route from EF lower bounds to P != NP — the closest published analogue of B_EF; read for the exact side conditions before claiming any overlap.
- Tabatabai, "Proof Complexity and Feasible Interpolation" (arXiv:2505.03002, 2025): resolution has monotone feasible interpolation; Frege/TC0-Frege lack it under factoring hardness (Bonet–Pitassi–Raz); automatability implies feasible interpolation; if NP in P/poly, no p-bounded system with feasible interpolation. Barrier for interpolation-based lower bounds on strong R.
- Searches found no 2026 paper on minimal derivation size implying P != NP. (Standard-mode search only; thin coverage.)
- Classification: T1 KNOWN; Pich–Santhanam = ANALOGY needing exact-statement check; feasible-interpolation barrier = FAILED TRANSFER for strong R.

### Open arrows (all OPEN)
1. A fixed combined R with B_R provable and W_R superpoly provable (neither is known; T2 rules out weak R).
2. A natural-proofs/relativization audit of any W_R lower bound technique (Razborov–Rudich applies to circuit-style arguments; Baker–Gill–Solovay: oracle with P = NP exists, so B_R must use non-relativizing structure).
3. Hard UNSAT family (e.g. Tseitin on expanders, PHP, random 3-CNF, clique-coloring) lower bounds for the *combined* system, not just resolution.

### Next-run assignments
- Lead: write B_EF-form (T3) for a candidate system R_mix and list which sub-lemma (feasible provability of correctness) is missing.
- Builder: implement a small exhaustive minimum-derivation search (n<=6 variables) for resolution+XOR-elimination+extension to get the first certified W_R data points; keep each run <=30 s.
- Certificates: check which hard families defeat XOR-elimination (Tseitin is easy for Gaussian elimination: expect failure) and extension.
- Auditor: fix cost_R conventions (bit-length of states) so W_R is comparable with the RAM model used in the ARC/FLMV spine.
- Red team: attack T2/T3 for errors; find the exact side conditions of Pich–Santhanam.

Status: no new lower bound; no transfer theorem established. P versus NP remains OPEN.
