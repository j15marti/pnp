# LSPV-1: exact joint proof-work / workspace frontier

November 2, 2026; user request 13:07 PST. **Exact finite fixed-calculus result; external mathematical review pending. P versus NP OPEN.**

## Fixed model

Use binary resolution with original source loads and erasures. A resolution conclusion is inserted while both premises are still live. No weakening, auxiliary variables, semantic oracle, or global Horn/XOR macro is included in this test calculus. A live clause C costs 1+|C| tokens (literals plus terminator). Load and resolution each cost one. Erasures have cost zero in Q, and cost one in a separately optimized variant. Both the proof and execution schedule are chosen for free. Reloading and rederivation are allowed. This is not native machine time or whole-machine memory.

## Explicit input and exact frontier

F has five variables and six clauses:

    (a), (b), (-a OR -b OR c), (-b OR -c OR d),
    (-a OR -d OR e), (-e).

The complete non-tautological resolution closure contains 33 clauses. Exhaustive configuration optimization, independently checked by closed-sublevel certificates, gives:

| Live tokens s | Minimum loads+resolutions Q(F,s) | Loads / inferences in an optimum | Minimum moves including erasures |
|---:|---:|---:|---:|
| <=8 | infeasible | - | infeasible |
| 9 | 15 | 8 / 7 | 25 |
| 10 | 13 | 7 / 6 | 21 |
| 11 | 11 | 6 / 5 | 17 |
| 12 | 11 | 6 / 5 | 16 |

Moreover Q(F,s)=11 for ALL s>=11. This is a joint optimum over every proof and schedule in the declared calculus, not a pebbling optimum for one preselected DAG.

## Minimum logical DAG cost is exactly five

Backward resolution derives (-a OR -d), then (-a OR -b OR -c), then (-a OR -b), then (-b), then contradiction. All six source clauses are essential, with independently checked deletion witnesses. A connected binary-premise contradiction DAG using six essential sources needs at least five inference nodes. Hence W_Res(F)=5. Every execution needs at least six loads and five inferences. A capacity-eleven schedule attains this. No first inference fits below nine tokens, because the cheapest initial unit/ternary resolution needs 2+4+3 tokens. Capacity-nine and capacity-ten optimality is certified by exhaustive sublevel-closure certificates.

## Independent validation

The Python producer uses signed sets; the Node verifier uses positive/negative bitmasks and imports no producer code. For a claimed minimum q, it checks that every configuration reachable below q remains in a goal-free transition-closed labelled set; a separate schedule attains q. Infeasibility certificates are closed under every legal move.

The checker passed 13 frontier cases, 28,713 labelled configurations and 152,232 transitions (256,389 condition checks, including corruption tests). It rejected three corrupted certificates. A three-variable full-cube control was independently included. All six source-deletion and twelve sign-flip witnesses passed. Replacing (-e) by (e) gives exactly one SAT assignment. The same guarded original AND_C(-s OR C) has 32/0 models at s=0/1. Original-clause complement/S-U tests, malformed-source checks and odd/even K4 parity controls were retained.

This is deliberately an easy Horn formula, not an intrinsically hard SAT family. A richer inference system changes the frontier. Token encoding takes four bits per token here, so 9/10/11 tokens mean 36/40/44 payload bits ONLY. Controller, addressing, parsing, rule validation, scratch and instruction storage are additional. Logical membership XOR is offline, not physical tape activity.

## General cost-realization lemma and remaining bridge

If each scheduled inference is charged at least its rule weight, unrolling an execution into a dependency DAG proves W_R(F)<=T_R^*(F,s). Increasing s can only lower the optimum. If cost-w proofs have evidence of length polynomial in N+w and admit polynomial checking/execution, retaining that evidence gives one polynomial p with

    T_R^*(F,p(N+W_R(F))) <= p(N+W_R(F)).

The encoding/verification hypothesis is NOT automatic for unit node costs. This lemma grants free proof selection; it gives no efficient proof-search algorithm. Under these assumptions, polynomial Wbar_R is equivalent to polynomial-work, polynomial-space IDEAL executions. B3, SAT in P => Wbar_R polynomial for the SAME fixed system, remains unproved. No arbitrary-decider simulation or FLMV numerical transfer is claimed.

## Corpus, publication and next step

Read the current 12:04 PST worst-case handoff, AGENTS.md, CODEX.md, pnp-research skill and issue #3. Search `pebbling` surfaced prior HEAVY-FIRST-CERT-PEBBLING169, RCCN and forced-DAG bypass work. Scheduling and proof-space concepts are established, not claimed novel. No complete repository preflight or corpus replay is asserted. Root main.tex returned empty content with nonempty SHA cb0661e219694521ebb1f95349e9ae902ffad332, so it was left unchanged. No automation was changed.

Standalone reproducer: `experiments/arc/lspv1_workspace_frontier_20261102/compact_reproduce.py`.
Raw compact results: `results/raw/arc/lspv1_workspace_frontier_20261102/compact_results.json`.
The conversation archive contains the expanded producer, separate verifier, full optimality certificates, schedules, controls and integrity manifest.

Next: establish comparable frontiers in the SAME fixed combined resolution/algebraic calculus, with weights linked to encoded evidence and validation. Do not transfer these pure-resolution optima to the richer system without proof.

References: Nordstrom, *Pebble Games, Proof Complexity, and Time-Space Trade-offs*, LMCS 9(3:15), 2013, https://lmcs.episciences.org/1111 ; Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44(1):36-50, 1979.
