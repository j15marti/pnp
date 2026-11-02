# LSPV-5 -> five-role handoff: SEMANTIC-DIRECT-SUM-ACQUISITION-REFEREE293

**Timestamp:** 2026-11-02 10:48 PST (America/Los_Angeles)  
**Scope:** arbitrary CNF-SAT; both labels; malformed inputs rejected.  
**State:** existing task IDs, titles, paused/enabled states, and Pacific schedules unchanged.

## Proved

For disjoint clause-minimally UNSAT proper-3CNF blocks \(F_j\), construct their guarded one-bit regions and take the conjunction. Designated boundary query \(q_j=e_j\) is positive exactly when \(F_j\) is SAT. For every deterministic exact compiler/query pair,

\[
|(R_C\cup R_{Q_j})\cap E_j|=L_j,
\qquad
P_C+\sum_jP_{Q_j}\ge\sum_jL_j.
\]

The lower bound is tight in the declared independently addressable sign-field model: compilation may cache any \(p_j\) signs and query \(j\) reads the remaining \(L_j-p_j\). This is linear acquisition, not exponential SAT hardness.

## Falsified promotion

The base exact boundary relation is the singleton \(\{0^t\}\); after one sensitive sign flip in block \(j\) it is \(\{0^t,e_j\}\). The relations have small formulas and every designated post-answer circuit is constant. Thus minimal post-projection DAG size or after-answer reduction length does not equal representation-independent computational work. A source-authenticated DAG can still measure a fixed proof/compilation system, but its rules and acquisition must be declared.

## Space correction

All local phases count in \(\rho\). Materializing the guarded formula gives \(\Theta(N)\) live bits and \(\rho=1\), even if freed before queries. The explicit exhaustive tightness implementation also uses \(n_j=\Theta(N/\log N)\) assignment-counter bits and exponential time; it does not meet the square-root contraction contract. Python object memory is not presented as an FLMV trace.

## Controls

Five minimally UNSAT sources, 70,208 assignments, 396 sensitive signs, 396 same-skeleton SAT sign neighbors, fifteen phase-split records, six malformed rejects, and 421 independent assertion groups passed. Tseitin GF(2) recognition remains the mandatory alternate-representation escape.

## Next role actions

1. **Formal quantifiers:** decide whether the target DAG is semantic-only or source-authenticated; prohibit switching between them mid-proof.
2. **Compiler builder:** test whether any multi-query semantic compiler obtains a nontrivial amortized benefit without moving all work into queries or source references.
3. **Interface/separator role:** seek a superlinear acquisition theorem that survives equality, parity cancellation, and compact existential descriptors.
4. **Resource auditor:** keep \(\rho\) over every phase; reject pre-call \(N\)-bit buffers and charge virtual accessor overhead.
5. **Red team:** attack every candidate with constant post-answer circuits, stateful query reuse, tiny cores, hardcoded recognizers, delayed guests, and representation switches.

## Open gap

No representation-inclusive superlinear all-input lower bound, polynomial SAT solver, arbitrary-\(A\) contraction, or strict same-machine FLMV transfer was obtained. **P versus NP remains OPEN.**

