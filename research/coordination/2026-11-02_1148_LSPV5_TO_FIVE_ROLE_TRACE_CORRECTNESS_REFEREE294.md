# LSPV-5 -> five-role handoff: TRACE-CORRECTNESS-FIREWALL-REFEREE294

**Timestamp:** 2026-11-02 11:48 PST (America/Los_Angeles)  
**Scope:** general CNF-SAT, fixed minimum-cost derivation systems, both labels and malformed controls.  
**State:** existing task identity/title, actual enabled state, Pacific schedule, role ownership, and safeguards unchanged.

## Result

Free optimal derivation selection is accepted. It does not license an invalid inference rule.

* A rule accepting any rejecting trace is unsound: a one-step reject-all trace closes a proof for satisfiable \((x\vee y)\).
* Requiring a correctness proof in one fixed adequate consistent recursively axiomatized theory \(T\) is not universal. The fixed decider \(A_T\) first searches \(n\) steps for a \(T\)-proof of contradiction and misanswers if it finds one; otherwise it runs a known complete decider. Externally \(A_T\) is correct when \(T\) is consistent, while a \(T\)-proof of all-input correctness would prove \(\mathrm{Con}(T)\), contradicting second incompleteness.
* Requiring a separately checkable source-derived \(R\)-refutation preserves soundness, but the polynomial arbitrary-decider transfer remains OPEN. An external compiler not based on \(T\)-internal correctness is not ruled out.

Finite exact controls under fixed unit-cost binary Resolution give minima 1 for \((x)\wedge(\neg x)\) and 3 for the four-clause equality-plus-inequality contradiction; the satisfiable control has no Resolution refutation. Native XOR reduces the second contradiction to one addition, confirming representation dependence. The independent verifier passed 11 assertion groups. Optimizer BFS work is OFFLINE and omitted from \(W_R\) by the user-approved relaxation.

## Next target

Either construct a fixed effective strong \(R\) with a uniform external computation-to-proof compiler for every correct SAT decider, or prove a precise impossibility theorem for that compiler without assuming traces certify their own correctness. Separately, any superpolynomial \(W_R\) lower bound must survive XOR/equality and representation switches.

Artifacts:

* research/main/2026-11-02_1148_MAIN_TRACE-CORRECTNESS-FIREWALL-REFEREE294.md
* experiments/arc/lspv5_294/minimum_derivation_firewall_referee294.py
* experiments/arc/lspv5_294/verify_minimum_derivation_firewall_referee294.py
* results/raw/arc/2026-11-02_1148_LSPV5_MIN_DERIVATION_FIREWALL_REFEREE294_raw.json

**P versus NP remains OPEN.**
