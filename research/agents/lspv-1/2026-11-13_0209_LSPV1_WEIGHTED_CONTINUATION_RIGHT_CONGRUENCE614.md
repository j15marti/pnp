# LSPV-1/614: Weighted-continuation right congruence for an exact proof-cost abstraction

2026-11-13 02:09 PST | LSPV-1 General SAT Lower-Bound Lead | existing Route B | PROVED/RESTRICTED symbolic theorem and COMPUTATIONAL actual OS Node tests | P versus NP OPEN.

## Candidate and four pre-search falsifiers

Candidate: For a complete deterministic, partial, action-labelled checker-prefix system with nonnegative exact marginal charges, the coarsest exact action-by-action cost-and-goal-preserving quotient identifies precisely configurations with identical weighted observations for every possible future action word. This is a necessary and sufficient characterization of an EXACT quotient, not a requirement for a coarser cost-sound MAY abstraction.

F1: two states classified equivalent admit a distinguishing finite suffix in legality, cost or terminal goal. F2: quotienting merges different paid costs despite exact charge preservation. F3: forgetting a globally paid identity/history is exact even when reusing that identity has cost zero rather than the first-acquisition cost one. F4: forgetting an active assumption or external-source binding is exact despite a distinguishing DISCHARGE or CLOSE action. All four falsifiers were tested; no counterexample to the theorem occurred.

## Theorem 614.1 (PROVED/RESTRICTED, weighted right-congruence)

Fix a finite deterministic partial transition system T=(S, Sigma, delta, c, G) where delta:S x Sigma -> S is partial; c on enabled transitions is nonnegative; G:S->{0,1} is an explicitly specified terminal-goal predicate. A state intended for eventual R_mix341 implementation must record the COMPLETE original-source authenticated identity/bytes, shared proof DAG, paid identities/history, source provenance, definitions, freshness, private and exported wires, contexts, assumption discharge and any pending validation obligations. No unrecognized historical rule may be removed when claiming a complete legal transition graph.

For any action word z in Sigma*, let O_s(z) be INVALID if any step is unavailable, and otherwise O_s(z)=(sum of exact marginal costs, final G value). Empty word has O_s(epsilon)=(0,G(s)). Define

$$
s \equiv t \quad\Longleftrightarrow\quad
\forall z\in\Sigma^*: O_s(z)=O_t(z).
$$

Then (a) this is an equivalence relation; (b) if s equivalent t, then G(s)=G(t), the SAME actions are enabled, every matched action has the SAME marginal cost, and the successors are equivalent; (c) any equivalence with these one-step requirements is contained in this relation, so it is the coarsest EXACT labelled cost-preserving quotient; (d) every legal word and total cost is preserved and therefore the optimal remaining cost to a G-terminal is preserved, including infinity; and (e) if S is finite, iterative refinement from terminal-goal classes using the signature

$$
\left(G(s),\left(\bot\ {\rm if\ disabled};\
(c(s,a),[\delta(s,a)]_k)\ {\rm if\ enabled}\right)_{a\in\Sigma}\right)
$$

stabilizes at this relation, with any inequivalent pair distinguished by some word of length at most |S|-1.

Proof: Equality for epsilon gives G. For a single enabled letter a, equality determines availability and exact cost. For every further suffix z, compare the observations on az: the equal a-costs cancel, forcing the successors to have identical future observations. Conversely, induction over word length proves goal, enabledness, total charge and successor consistency for any one-step stable equivalence. Therefore the quotient carries exactly the same finite legal paths and prices and the same goal predicate, preserving the infimum of terminal path costs. Each strict partition refinement increases the number of classes. Starting from goal classes, at most |S|-1 strict refinements can occur, and round k identifies precisely the states distinguished by words of length at most k. QED.

This is standard weighted automaton/right-language reasoning specialized as an exact-check criterion for proposed proof-cost abstraction. It is not a new general automata result and does not authenticate historical R_mix341.

## Important MAY and operational-goal limitations

A sound MAY quotient need not obey this exact congruence. It may combine enabled action sets and assign an edge the minimum concrete price, causing spurious cheap paths while still preserving the required lower-bound direction (abstract optimum no greater than concrete optimum). These paths require CEGAR replay against the actual native checker. A genuine native shortcut defeats the proposed bound; it may NOT be refined away. Also preserve separate operational checker acceptance and genuine logical UNSAT for the original signed source: the archived /341 checker accepts at least one SAT-source packet, independently OS-verified by LSPV-5/522.

If an eventually authenticated native system is nondeterministic for a fixed action label, this deterministic theorem does NOT automatically transfer: explicitly refine labels or prove a distinct sound nondeterministic simulation. Dynamic action alphabet and byte-level parser effects must be represented, not assumed away.

## Actually executed independently checkable controls

A dependency-free Node.js program executed through the OS, not hosted V8 alone, enumerated all 2,500 two-state, two-action partial deterministic machines with every arc absent or targeting either state with marginal cost 0 or 1, and both goal bits. It additionally sampled 500 pseudorandom machines at each of sizes 3, 4 and 5 (fixed seed 0x6145a7 and costs 0,1,2). For each automaton, the implementation compared all 23,000 unordered state pairs against independent direct enumeration of EVERY action word through length |S|-1. Local step consistency was separately asserted. It passed 86,554 assertion checks across 4,000 machines, zero discrepancies. Max observed refinement rounds: 4. Class histogram by quotient size: 1:162, 2:2357, 3:546, 4:455, 5:480.

Three hostile toy controls, clearly NOT native R_mix341 certificates: first-acquisition of a paid node costs 1 versus a cached reuse of the same node costing 0; discharge succeeds in a closed context but is unavailable with unresolved assumptions; source-bound CLOSE succeeds only for the correct external source. The naive merged paid-history MAY edge has cost zero, which illustrates loss of a positive cost lower bound but not unsoundness of MAY simulation. The controls are compatible with prior project paid-history/source/context obstructions; do not claim them as a new native finding.

Published reproducible program: experiments/arc/lspv1_614_weighted_continuation_quotient.cjs (actual executed bytes SHA-256 035805aab3584e844e1b4b1d9e1a4e6edd07f71f0b8c8a961f829a7a5ad7cf18). Raw output: results/raw/arc/2026-11-13_0209_LSPV1_614_WEIGHTED_CONTINUATION_RAW.json (actual executed output SHA-256 2586c47799246619c6011b0bd66251cb0c59a59b2d8fa71262268adf3aa26cd9). No historical original checker was executed in THIS experiment. No peak-space/actual checker-runtime implication follows; the tests measure finite quotient correctness only.

## Prior project work, source review and literature

Read the current FULL proof1.txt (Git blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343) and FULL proof2.txt (Git blob f678f707880da4dfc97dabf778430c6dc816cb1f, recovered from Git blob because contents API returned empty), current issue #3 and its recent comments, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, the recent LSPV-1/613 and LSPV-5/522 handoffs, actual LSPV-1/539 and /613, LSPV-2/549 and /594, LSPV-3/609, LSPV-4/549, LSPV-5/522, and pinned archived /341 checker SOURCE/AND3/GF(2) body. Checked literature and prior project corpus for matching weighted future-continuation results and preexisting state-abstraction counterexamples.

Already known: LSPV-5/462 paid/cache conflation can zero a MAY bound. LSPV-2/521 branch-context merge can forge a join. LSPV-2/594 proves conditional residual set-cover LP consistency assuming a COMPLETE certified necessary-obligation cover. LSPV-2/549 demonstrates /341 and /386 original checker acceptance does not imply a single authentic mixed-rule transition. LSPV-3/609 and LSPV-5/522 demonstrate accepted SAT-source packet, invalidating a conflated checker-acceptance-as-UNSAT goal. Present theorem is an exact abstraction INTERFACE under complete authenticated deterministic transitions, not a replacement for these verified restrictions.

Primary references: [1] Cousot and Cousot, POPL 1977, doi:10.1145/512950.512973; [2] Clarke, Grumberg, Jha, Lu and Veith, CAV 2000, doi:10.1007/10722167_15; [3] Mohri, Weighted Automata Algorithms, Handbook of Weighted Automata, https://www.cs.brandeis.edu/~cs136a/CS136a_docs/Mohri_WeightedAutomataAlgorithms_Handbook.pdf; [4] Cook and Reckhow, JSL 1979, doi:10.2307/2273702.

## Dependencies, report ownership and next falsification

P2-D1 OPEN: authoritative accepted-byte grammar, cross-rule source-bound transitions and historical tariff not authenticated.
P2-C3 OPEN: all-action native cost-sound transformers absent. Theorem 614.1 provides only a conditional exact quotient criterion.
P2-B1 OPEN: no superpolynomial minimum for complete legal shared-DAG R_mix341.
P2-B2/B3 separately OPEN: no noncircular same-fixed-calculus proof-size transfer.
P1-01/03/04 OPEN. P versus NP OPEN.

TRACKERS REVIEWED; NO MATERIAL CHANGE. Root proof tracker statuses must not be promoted. After standalone report publication, the complete 2,383,938-character root main.tex was recovered from immutable Git blob 7df3138833a04f995fba38d1b11b2e94e6f0de03, and an LSPV-1-owned-only 2,760-character report entry was inserted via compare-and-swap. The updated Git blob is 2d20397a81f3ffe61e73d036a326867facdcff4b, commit ac1272d78923c811a22ef1fdf561113bd3af3b0e. All original content outside LSPV-1 ownership was preserved; full post-commit readback verification is recorded in the issue #3 handoff. All five roles, their original titles, IDs, Pacific schedules, two Route A/three Route B labels, historical weights and boundaries remain unchanged; no automations created or modified.

Next role tasks: LSPV-2 recover a single authoritative source-bound RES-to-AND3 or DEF-to-LOCAL-CONVERT transition and test LSPV-2/594 residual features for future congruence. LSPV-3 authenticate full byte/source/context semantics. LSPV-4 maintain logical work vs evidence bytes/discovery/time/span/peak space separation. LSPV-5 independently supply a distinguishing future suffix against any proposed exact native state quotient and replay every potentially legal cheap CEGAR path.