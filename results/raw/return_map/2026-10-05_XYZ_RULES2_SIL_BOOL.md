XYZ-RULES2 / SIL-BOOL reconciliation
Date: 2026-10-05
Status: COMPUTATIONAL plus repository rule audit. P versus NP remains OPEN.

Purpose
Reconcile XYZ-RULES1 with existing SIL/BOOL discipline and test whether remaining false hardness signals disappear when easy families receive their legitimate typed closure modules.

Repository audit
BOOL v2.7/v2.8 states:
1. BOOL is SIL-derived object syntax, not a universal machine lower bound.
2. Named Boolean rewrites include complement/involution, De Morgan, absorption, consensus/resolution, Shannon reduction, unit/subsumption/pure/blocked/autarky, and ROBDD sharing.
3. A SIL event becomes a BOOL obligation only after a charged READ, QUERY, or BRANCH materializes the coordinate.
4. Gaussian/XOR, Horn/2-SAT implication closure, bounded-treewidth/OBDD/d-DNNF/parse-DP, and related algorithms are FOREIGN escapes.
5. SAME_REALIZATION, acquisition cost, EscapeOutOfBOOL, and TransportCert remain load-bearing. No arbitrary exact RAM decider has been transported to a BOOL derivation.
6. ForcedBranch is architecture-relative until TransportCert is proved.

Consequence for XYZ
Do not add Gaussian elimination, SCC closure, or separator DP as universally free propagation rules. Dispatch them as typed escape modules with explicit certificate/acquisition cost. Prime/source support remains an audit label, not a lower-bound resource.

XYZ-RULES2 prototype
Pipeline:
FREE BOOL-like local closure
-> typed family recognizer/certificate
-> FOREIGN closure module
-> residual live relational state
-> charge acquisition/materialization/transport separately.

Finite tests
2-SAT: 200 deterministic n=5 instances, 49 exactly UNSAT. Unit closure detected 0; implication transitive closure detected all 49. Finite certificate matrix used 10x10=100 bits per instance. This is a deliberately simple finite certificate, not an asymptotic optimum.

Horn strengthened control: 500 deterministic n=5 instances with facts, implications and negative goals. Exact exhaustive decision found 463 UNSAT; Horn forward chaining found exactly the same 463, with 0 decision mismatches. Across satisfiable cases, 109 positively forced variables were present and all 109 were found. 2063 forward steps total.

Bounded-window control: 200 deterministic n=5 formulas on consecutive 3-variable windows. Exact separator audit had maximum 4 live separator states, consistent with a 2-variable boundary. This removes the earlier raw contextual-state anomaly as a hardness signal.

Generic 3-SAT: no new universal closure was granted. Local propagation remains local. This is not evidence of a lower bound because an arbitrary solver may use a FOREIGN representation or algorithm not captured by the current dispatcher.

Literature cross-check
Knowledge-compilation literature gives constructive bounded-treewidth compilation to structured decomposable representations and OBDDs with width/size controlled by treewidth/pathwidth. Branching-program lower bounds in the literature are model-specific. These support the SIL/BOOL rule that representation-specific escape modules must be explicit and cannot be promoted to unrestricted SAT runtime lower bounds.

New candidate interface
Each propagation module E must expose:
TYPE(E), DOMAIN(E), CERT(E), ACQUIRE(E), APPLY(E), OUTPUT(E), COST(E), SAME_REALIZATION(E).
A rule may be free only if it is an admitted BOOL semantic identity/rewrite. Otherwise it is FOREIGN and charged.

Open issue
The central missing theorem remains TransportCert: arbitrary polynomial exact SAT decider A -> forced model-matched charged XYZ/BOOL/SIL event or typed escape. Without it, residual propagation deficit is not a machine lower bound.

Next experiment
Implement XYZ-RULES3 with explicit module records and a FOREIGN escape ledger. Add Gaussian row-reduction, exact 2-SAT SCC, Horn closure, bounded-treewidth separator DP, and a generic representation-bypass module. Measure only charged residual events after each module has been given its strongest certified compact representation. Test padding, renaming, COPY, RECOMP, INTERP, independent products, parity/Tseitin and maximal semantic-oracle controls.
