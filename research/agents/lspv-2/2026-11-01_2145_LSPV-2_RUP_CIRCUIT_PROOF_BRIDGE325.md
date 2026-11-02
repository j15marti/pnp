# LSPV-2: RUP-CIRCUIT-PROOF-BRIDGE325
2026-11-01 21:45 PST. PROVED/EXACT for the declared factor-group circuit architecture; independently COMPUTATIONAL. P versus NP OPEN.

## Universal obstruction and three falsifiers
For the same authenticated canonical source F, evaluating a fan-in-two C_F(x)=F(x) is polynomial, while existential Circuit-SAT is not decided by evaluation. Test (H1) every source clause is RUP-recoverable from the fully biconditional output-one Tseitin encoding of 323, including shared/distributive gates; (H2) each source resolution proof is transferable with at most m extra RUP lines; (H3) a source and circuit UP-stall can still have a small recovered resolution refutation. All three are established for this explicitly restricted compiler.

## Exact theorem and proof
Let F be ANY valid duplicate-free proper Döcker Monotone 3-SAT-(2,2) original with n variables, m=4n/3 clauses, and d repeated same-sign variable pairs. In the 323 architecture, repeated signed pairs form a matching on source clause IDs. The fan-in-two evaluator has g=3m-1-2d gates, full output-one Tseitin has 3g+1 clauses and 7g+1 literal occurrences.

Every original clause C_j is a RUP consequence of E_323(F). Indeed, falsifying C_j forces its private clause output false by unit propagation, even for a distributively shared pair: positive pair (a∨b∨c)∧(a∨b∨d) is (a∨b)∨(c∧d), and negative pair is the corresponding NAND dual. The AND-only output tree, forced to one, forces every source-group output to one. Contradiction follows, so C_j can be added by RUP. Any source resolution proof of length L can then be replayed using RUP, since each resolvent of present parent clauses is a RUP lemma. Thus the compiled circuit admits a refutation with at most m+L added lines. This is a *certificate transfer upper bound*, not an algorithmic time or all-decider lower bound. All checks and source reads are paid.

An eager explicit resolution derivation of all C_j from gate definitions uses at most 2(m-d-1) AND-tree propagation steps + 5d grouped steps + 2(m-2d) singleton steps = 4m-d-2 steps. This is a stated derivation upper bound, not unrestricted proof minimum.

## Independent controls
A standalone producer was independently checked by a no-import verifier using separately archived 323 gate fixtures, round-synchronous UP and its own original-source evaluation. **34,739 verification assertions passed**, including 33,856 source/circuit input rows (exhaustive Y6/F9/F15, 256 sampled each U198/V198), every one of **568** original source RUP clauses, nine malformed originals rejected, 264 F9 signed extreme clause-pair modes, both-label F9/F15 pins and an 11-line circuit RUP refutation.

| Original | gates | Tseitin clauses | RUP source lines | explicit resolution-bound | paid producer RUP literal reads |
|---|---:|---:|---:|---:|---:|
| Y6 | 23 | 70 | 8 | 30 | 1,192 |
| F9 | 33 | 100 | 12 | 45 | 2,608 |
| F15 | 57 | 172 | 20 | 77 | 7,678 |
| U198 | 701 | 2,104 | 264 | 1,009 | 1,290,620 |
| V198 | 701 | 2,104 | 264 | 1,009 | 1,290,620 |

On the SAME F9 original, pins (x3,x5,x6,x7,x8)=(0,1,0,0,0): x1=0 has 2 verified SAT completions; x1=1 has 0 and an 8-leaf source-clause cover. On the SAME F15 original, pins x8..x15=(0,0,0,1,1,1,1,0): x7=0 has 0 completions and a 64-leaf cover; x7=1 has 2 witnesses.

On a second F9 pin cube (x1,x4,x5,x8)=(1,0,1,0), both original-CNF UP and compiled Circuit-SAT UP stall. Six original binary clauses C11,C5,C12,C4,C8,C6 were separately RUP-added to the circuit encoding; five checked resolvents are (-x9∨x7), (-x9), (-x7∨x9), (x9), EMPTY. All 11 additions were verified RUP in sequence. Hence the UP-stall is not a necessary exponential computation.

Prior 324 direct/Circuit-SAT UP-DPLL F9 4-pin probe counts were 102/2,173, **excluding paid circuit compilation**. This run measured RUP acquisition/checking, not an industrial CDCL comparison. U198 UNSAT and V198 SAT labels are inherited from independent 323/324 certificates, *not freshly replayed in this run*. The 198-input function tests were sampled.

## All-charge recurrence and open gap
T(R)=C_grammar+source/index/head+compilation+Σ_actual_policies(C_discovery+execution+failures+switching+proof/GE+semantic_equivalence)+C_cache/replay+RUP_checks+Σ_evaluated_children(C_output/bit+T(child))+C_guest(DELAY,COPY,RECOMP). Peak writable space counts all simultaneous gate, index, proof, cache, source, ancestor, child, and guest state. Acquiring groups requires 3m source occurrences and 3m candidate pairs plus paid sorting/hashing; checker effort is not proportional merely to the number of RUP lines. The native same-machine FLMV accounting is not yet implemented. Logical XOR is offline only. Neither all-input polynomial total work nor arbitrary A→Φ(A), hereditary canonical re-encoding nor strict same-machine numerical FLMV transfer is proved. P=NP and P≠NP OPEN.

## Search and provenance
Read first the verified 2026-11-01 19:50 SAT/Circuit-SAT five-role handoff, then issue #3 and prior LSPV2 323/324, LSPV4 F9 2SAT, LSPV1 21:27 cofactor miter and LSPV3 paid Shannon DP. GitHub project search: `CIRCUIT UP REVERSE` in j15marti/pnp; separate github.com/openai code search: `SAT circuit Tseitin` (no matches, not novelty). Web/primary: Tseitin extension, DRUP RUP, Bryant-Heule 2023 extended-resolution BDD proof, FLMV 2005. References: Döcker https://arxiv.org/abs/1912.08032; RUP checker https://www.cs.utexas.edu/~marijn/drup/; Bryant-Heule https://www.cs.cmu.edu/~bryant/pubdir/tocl23.pdf; verified checking https://link.springer.com/article/10.1007/s10817-019-09525-z; FLMV https://doi.org/10.1145/1101821.1101822.

Complete standalone producer, separate independent verifier, all original-source fixtures, detailed raw JSON, resolution transcript, literature audit, manifest in dated user-facing reproducibility archive. Do not alter any task or non-owned root region. P versus NP OPEN.
