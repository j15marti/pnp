# Worst-case derivation-cost programme — living log

Target: W̄_R(N) = max_{F∈UNSAT,|F|≤N} min_{π:F⊢_R⊥} cost_R(π); weakest bridge B(R): SAT∈P ⟹ W̄_R(N) ≤ poly(N).
Status of P vs NP: **OPEN**. Nothing below is a proof of a lower bound or of the bridge.

## Entry 2026-11-08 (run 1) — scoping / what the bridge can and cannot be

Corpus check: no earlier "multisign DAG hypergraph" or W̄_R material exists in the repo (grep of *.tex/*.md); closest are signed-hypergraph/ARC/FLMV notes and the world ledger (`research/agents/claude/world-ledger/`). Not re-audited in depth this run.

### Facts (KNOWN THEOREM unless marked)
1. Cook–Reckhow: a polynomially bounded *poly-time-verifiable* system exists iff NP = coNP. So for any such R, "W̄_R superpolynomial" implies only NP ≠ coNP (⟹ P ≠ NP), never more, and only for that R.
2. Hence B(R) is exactly the statement "R is strong enough that P = NP makes R polybounded". For R = a fixed named system (Res, Frege, EF, algebraic/CP/hypergraph-DAG calculus), B(R) is not a free lemma: P = NP gives NP = coNP, hence *some* polybounded system R', but R must p-simulate R'. Existence of even an optimal proof system is open (Krajíček–Pudlák 1989; it holds if NE = coNE).
3. CONDITIONAL bridge (Cook/Krajíček correspondence PV ↔ EF): if SAT∈P via a poly-time M whose coNP-side soundness ("M rejects F ⟹ F has no satisfying assignment") is provable in PV, then EF has poly-size proofs of every tautology, i.e. W̄_EF ≤ poly. Thus B(EF) reduces to: *is a P = NP algorithm necessarily PV-provably sound?* This is open and is where the real content sits (cf. Pich–Santhanam, arXiv:2312.08163, linking EF lower bounds to P ≠ NP via circuit-lower-bound assumptions).
4. Free-strategy reading: "min over all sequences, strategy discovery uncharged" is a valid lower-bound device only if every algorithm's behaviour *is* some R-derivation. If cost is instead defined semantically (min over all machines/circuits), B holds trivially by hard-wiring M, but W̄ superpolynomial is then literally SAT ∉ P/poly-type, i.e. a restatement (ledger rule: equivalent to the target = reformulation, not progress).

### Dichotomy (PROVED/EXACT, elementary)
For a candidate cost model R either (i) R is poly-verifiable: lower bounds are meaningful but B(R) is an unproved transfer theorem (open, ≥ as hard as showing EF-like completeness); or (ii) R is semantic/unverifiable: B(R) is trivial but the lower bound is as hard as P ≠ NP (non-uniformly). The multisign-DAG idea must be placed in (i) and supplied with an explicit simulation theorem "every poly-time decider induces a poly-cost R-derivation"; no such theorem is known and the natural candidates (Res, CP, PC, Frege) all have known or conjectured gaps (feasible interpolation fails for Frege/EF under factoring/RSA assumptions: Krajíček–Pudlák, Bonet–Pitassi–Raz).

### Literature clues this run
- KP89 / optimal proof systems: still open; sufficient condition NE = coNE.
- Pich–Santhanam 2023 (arXiv:2312.08163): conditional route "EF lower bounds ⟹ P ≠ NP" — the closest published analogue of B(EF).
- Buss (Toni60 slides): Frege vs EF simulation open; EF lower bounds would imply algebraic-circuit consequences.
- No 2025–26 resolution found by web search (standard-mode only; recheck on ECCC/arXiv next run).

### Agent assignments — this run's concrete outputs / next steps
| Role | Output now | Next |
|---|---|---|
| General SAT lower-bound lead | Dichotomy above; B(R) ⇔ simulation theorem | Formalize "PV-provable soundness" hypothesis H_PV; ask whether H_PV is implied by P = NP (via Levin-style search: only SAT side self-verifies) |
| SAT-circuit reduction builder | — | Fix the inference rules of the multisign DAG calculus and prove it is poly-verifiable and p-simulates Res; compute shortest DAGs for small UNSAT by SAT/ILP |
| Hypergraph & proof certificates | — | Candidate hard families (Tseitin on expanders, PHP, random 3-CNF) vs. the calculus; record which have poly EF proofs (Tseitin, PHP do) — they are NOT hard against EF |
| Time-space auditor | — | Cost model: size vs. width vs. space; check proof-encoding overhead is poly |
| Red team | Flagged: any family with poly EF proofs cannot witness B(EF)-type lower bounds; "reduced logical state" minimality must be shown invariant under extension variables | Hunt shorter derivations via extension/renaming |

Stale/overstated claims: none in this log; the task text's "bridge" is unproved and is recorded as CANDIDATE/OPEN.
