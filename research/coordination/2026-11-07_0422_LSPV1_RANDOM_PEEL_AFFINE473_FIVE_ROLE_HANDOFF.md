# LSPV-1/473 five-role handoff | 2026-11-07 04:22 PST

**Route B PROVED/RESTRICTED (symbolic) + COMPUTATIONAL finite, P versus NP OPEN.** New proof-chain node [P2-B14], supporting but not closing [P2-B1]. Dependencies [P2-D1], [P2-C3], [P2-B2] OPEN. Both shared trackers reviewed; proof1.txt NO MATERIAL CHANGE.

## New exact restricted statement

On the Chvátal–Szemerédi model of $m=8n$ original signed proper random three-clauses (size $N=\Theta(n\log n)$), with probability $1-o(1)$ every subformula containing at most $\delta n$ original clauses is peelable by singly occurring variables, SAT, and has full affine hull $\mathbb F_2^n$. A union bound over residual 2-cores gives explicit $\delta=\min(1/3,[10e^{5/2}(3/2)^{3/2}(9)]^{-2})>0$. Full affine hull follows by induction on the leaf-variable clause elimination order: every model of the remainder lifts and a chosen remainder model satisfying one other literal frees the leaf variable. Therefore NO sound source-local derivation with $\le\delta n$ distinct original-source ancestors can produce a nontrivial unconditional affine equation over original variables or false.

This is a **linear original-source-support** bound, stronger than prior LSPV-1/472's direct four-clause obstruction, yet does not block later globally sourced GF(2), paid definitions, derived Resolution clauses, extensions, assumption-typed branching or a polynomial mixed proof. The optional inference lower bound $q\ge\lfloor\delta n\rfloor$ holds ONLY in a separately specified source-transparent *unit-paid binary* calculus. Historic accepted-byte R_mix341 parser/weights/arity remain unauthenticated. No new inference rule is proposed.

## Evidence

Standalone: experiments/arc/lspv1_473_peeling_affine_control.cjs, published/readback SHA 1478ca396ea439af8fd7b9b34112cfe650ab77ff; raw results/raw/arc/2026-11-07_0422_LSPV1_473_PEEL_AFFINE.json; full report research/agents/lspv-1/2026-11-07_0422_LSPV1_RANDOM_PEEL_AFFINE_FLOOR473.md. Exhaustive n=4 <=4 clauses (41,449) and n=5 <=3 clauses (85,401), plus 4,200 deterministic n6/n8 samples, two adversarial witnesses, 112,028 checks. All 56,010 peelable instances SAT and full affine rank; six malformed controls rejected. No native R_mix341 checker or FLMV execution. Actual V8 exact-source (shebang-stripped) execution, symbolic proof separate.

## Route responsibilities without reallocating agents

- LSPV-1 (Route B): keep the *original-source-support* invariant separate from paid work; seek a noncircular B3, no promotion of [P2-B1].
- LSPV-3 (Route B): authenticate historical LOCAL-CONVERT source antecedents, whether binary fan-in and references are actually paid; check assumption scopes and private versus exported wires.
- LSPV-5 (Route B): adversarially seek a peelable counterexample to the affine-hull lemma or a native shortcut that invalidates the source-support premise, while retaining legal all-rule global shortcuts.
- LSPV-2 (Route A): use random-3CNF and odd Tseitin as hard/control inputs to test but do not assume an all-input recursively iterable decomposition.
- LSPV-4 (Route A): charge acquisition, actual source reads, evidence bits, real time, and simultaneous space, not the offline source-support bound.

Preserve 2 Route A / 3 Route B allocation, exactly five original task IDs/schedules, source grammar/weights, root main.tex outside ownership markers, and both proof-chain records. **P versus NP OPEN.**
