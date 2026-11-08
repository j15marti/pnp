# WCD living log (worst-case derivation program)
Directive: `research/governance/2026-11-08_WORST_CASE_DERIVATION_DIRECTIVE1.md`. P vs NP remains OPEN. Statuses: PROVED/EXACT, KNOWN THEOREM, CANDIDATE, OPEN, FALSIFIED/RETIRED.

## Entry 1 — 2026-11-08 (CLAUDE WCD-0001)
Full write-up: `research/agents/claude/2026-11-08_CLAUDE_WCD-0001.tex`.

**Findings**
1. (PROVED/EXACT, trivial) B(R) is logically `P!=NP  or  R p-bounded`. Combined with a lower bound for R it is *equivalent* to P!=NP, so B(R) is not a weaker sufficient bridge in any content-free sense; it carries all the difficulty. The real question is which R admit an independent proof of "P=NP => R p-bounded".
2. (PROVED/EXACT) Free strategy search turns W_R into a *nondeterministic* (certificate-size) measure for any R with poly-time checkable steps. W_R poly for R implies NP=coNP. So even a full W_R lower bound plus B(R) would only be as strong as the Cook–Reckhow program for that R; it cannot be easier than proving a lower bound against R itself.
3. (KNOWN THEOREM, Cook 1975 / Krajicek) Sufficient route for B(EF): if PV proves soundness of the SAT algorithm A, then EF has poly-size proofs for all UNSAT F. Hence B(EF) holds whenever P=NP is witnessed by a provably-correct algorithm. Obstacle: A may be correct but unprovable in PV; then no known short EF proofs. B(EF) is OPEN (a web-search summary claimed it follows trivially from P=NP; that is WRONG: P=NP makes *search* easy, but a proof system needs short *certificates in R*).
4. (CANDIDATE) Levin-style universal system R* = EF + {Corr(A_k)}: B(R*) holds but R* is unsound as a proof system unless some A_k is correct, so the lower bound for R* would itself imply P!=NP only trivially (it is not a lower bound against a sound system).
5. (OPEN, hardest) Lower bound for W_EF/Frege superpolynomial: open since 1979. Pich–Santhanam (ECCC TR23-199): superpoly EF lower bounds with certain extra axioms imply SAT needs superpoly circuits, i.e. barrier-type strong consequences.
6. Min over strategies with *per-instance* choice of algorithm collapses (hardwire the answer): free knowledge is only legitimate for sound, locally verifiable derivations.

**Literature clues (searched this run)**
- Alekseev, Theory of Computing 22 (2026) a004: exponential lower bound for the binary value principle in a PC extension that simulates EF (bit-size). Clue: algebraic systems are the easier place to get EF-strength lower bounds; check whether hard families survive circuit-compressed (algebraic-circuit) shared DAGs — assigned to Hypergraph/Certificates role. https://theoryofcomputing.org/articles/v022a004/
- Pich–Santhanam TR23-199 (barrier above). https://eccc.weizmann.ac.il/report/2023/199
- Khaniki–Pich–Sokolov, CCC 2026: classical lower-bound methods yield efficient adversary strategies (relevant to "does the lower-bound argument itself define a poly-time algorithm", a natural-proofs-flavored barrier). https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2026.8
- Krajicek–Pudlak: p-optimal proof system existence is open; it would give B(R) for the optimal R. 
- Not retrieved this run (follow up): time-space tradeoffs in resolution (Beame–Beck–Impagliazzo), non-automatability (Atserias–Mueller), Res(lin) bounds.

**Open arrows / next assignments**
- Lead: classify for which R B(R) is provable; target: R with a *uniform* soundness-reflection property (e.g. EF + reflection for all poly-time A with provably total... ) and show B holds relative to a stated hypothesis H, then see whether H is weaker than P!=NP-negation.
- Reduction builder: compute exact shortest resolution/EF-style DAGs for tiny UNSAT 3-CNFs (n<=5), report W_R(N) data.
- Certificates: test Tseitin/PHP/BVP-style families against PC-with-circuits compression.
- Resource auditor: define cost_R = size + lg(space) with peak-clause-space; check tradeoff literature.
- Red team: attack finding 1 and 3; look for oracle where B(EF) fails.
