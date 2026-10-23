# ROOT-LABEL-QUOTIENT85 — why residual diversity disappears at the SAT-only interface

**Role:** :48 synthesis  
**Timestamp:** 2026-10-23 09:48 KST  
**Global status:** P versus NP OPEN.

## Repairs proposed before source review

1. Test residual diversity under the actual mandatory interface: one SAT/UNSAT answer.
2. Strengthen the interface to a declared family of future restrictions and charge the resulting static service.
3. Demand an extraction theorem showing that every arbitrary SAT decider supplies that stronger interface; otherwise classify the width bound as representation-relative.

## Sources reviewed

1. New Role 1 formalization: research/agents/lspv-1/2026-10-23_0900_RESIDUAL_ROLE1_STATUS.md, commit fa3a20e.
2. RESIDUAL-STATE-FIREWALL84 and TSEITIN-EXPANDER-PAIR83.
3. ES-ATLAS-0025, “Residual Diversity and Representation-Relative Quotient Width.”

Primary checks:

- Aspvall, Plass, and Tarjan, Information Processing Letters 8 (1979), DOI 10.1016/0020-0190(79)90002-4: implication/SCC structure yields linear-time 2-SAT.
- Bryant, IEEE Transactions on Computers C-35 (1986), DOI 10.1109/TC.1986.1676819: ordered decision-diagram size is a representation-specific Boolean-function resource.

These sources support the distinction between semantic decision, restricted representation size, and unrestricted machine time.

## Context quotient

Let \(\mathcal F_r\) be any family of Boolean residual predicates

\[
f:\{0,1\}^r\to\{0,1\}.
\]

Let \(\mathcal C\) be a declared collection of Boolean queries about \(f\). Define

\[
f\equiv_{\mathcal C}g
\iff
\forall c\in\mathcal C,\ c(f)=c(g),
\]

and let

\[
Q_{\mathcal C}(\mathcal F_r)
=
|\mathcal F_r/\!\equiv_{\mathcal C}|.
\]

This is representation-relative because changing the required query interface changes the quotient.

## Lemma 85A — static service lower bound

Suppose a preprocessing algorithm maps each \(f\in\mathcal F_r\) to a source-closed static state \(K(f)\), and every query \(c\in\mathcal C\) must be answered exactly from \(K(f)\) and \(c\), with no further access to \(f\). Then:

\[
|\{K(f):f\in\mathcal F_r\}|
\ge Q_{\mathcal C}(\mathcal F_r),
\]

so some state needs at least

\[
\left\lceil\log_2 Q_{\mathcal C}(\mathcal F_r)\right\rceil
\]

bits.

**Proof.** If \(f\not\equiv_{\mathcal C}g\) but \(K(f)=K(g)\), some query \(c\) has different correct answers on \(f\) and \(g\), while the source-closed service receives identical inputs and must answer identically. Contradiction. □

**Status: ESTABLISHED representation lower bound.**

It lower-bounds stored state, not construction time, and it does not apply if later queries may reread the source without charging that access.

## Lemma 85B — the SAT root quotient has only two classes

Take the mandatory interface

\[
\mathcal C_{\mathrm{root}}=\{\operatorname{SAT}\},
\qquad
\operatorname{SAT}(f)=\bigvee_x f(x).
\]

For the family of all \(r\)-bit predicates:

\[
Q_{\mathcal C_{\mathrm{root}}}=2.
\]

The two classes are the all-zero function and every nonzero function.

**Status: ESTABLISHED unrestricted semantic fact.**

Consequently, raw assignment count \(2^r\), syntactic residual count, or number of residual Boolean functions cannot by itself force a large state for the one-bit SAT interface. At this quotient, a decide-first normalizer is exactly the two-state representation.

## Lemma 85C — exact context ladder

Add \(q\) distinct point-evaluation queries to the root SAT query. Let \(m=2^r\).

For \(q<m\), the exact number of equivalence classes over all Boolean predicates is

\[
Q(q)=2^q+1.
\]

For \(q=m\), every truth table is distinguished and

\[
Q(m)=2^m=2^{2^r}.
\]

**Proof.** If the selected \(q\) answers contain a 1, the SAT label is already fixed to YES, producing \(2^q-1\) classes. If all selected answers are zero and \(q<m\), the unseen positions split into two classes: all zero or at least one 1. Hence \((2^q-1)+2=2^q+1\). When every point is queried, the SAT bit is redundant and the complete truth table determines the class. □

**Status: ESTABLISHED exact representation tradeoff.**

This ladder shows that width is created by required contexts, not by the root decision alone.

## Singleton corollary

For singleton predicates \(f_z(x)=[x=z]\):

- all \(2^r\) predicates lie in one root-SAT class;
- complete point contexts distinguish \(2^r\) locations;
- a source-closed location service needs only \(r\) stored bits;
- EMPTY versus an unknown singleton still needs \(2^r\) point queries when the location is not supplied.

Thus three resources differ:

1. root decision state: one SAT class for all singletons;
2. stored witness identity: \(r\) bits;
3. detached point-query discovery: \(2^r\) worst-case probes.

Conflating them is the core residual-enumeration error.

## Role 1 integration

Role 1 constructed a clause-minimally-UNSAT proper-3CNF family \(H_t\) with:

- \(n=r=2t+5\) under unit propagation;
- \(r/\log N\to\infty\);
- no units and a full minimal core;
- a source-recognizable paired-clause reduction to 2-SAT.

The SCC algorithm decides the contracted 2-SAT instance in linear time. Therefore large \(r\), a large minimal core, and proper-3CNF syntax still coexist with an easy semantic root quotient.

**Status: ESTABLISHED restricted hostile control, independently reported; not an unrestricted SAT lower bound.**

This also proves a general semantic countertheorem:

> Any invariant required to be unchanged under every equisatisfiability-preserving transformation can depend only on the SAT label.

Indeed, all satisfiable formulas may be transformed semantically to one fixed TRUE formula and all unsatisfiable formulas to one fixed FALSE formula. To retain richer information, the allowed transformation calculus must be restricted independently and its acquisition charged.

## Consequence for the residual proof spine

### 1. Defined obstruction

- \(2^r\) enumeration: **ESTABLISHED upper bound**.
- EMPTY-vs-SINGLETON point queries: **ESTABLISHED restricted lower bound**.
- root residual diversity: **RETIRED as a lower-bound mechanism**, because its semantic quotient has size two.

### 2. Charged acquisition/continuation dichotomy

A useful normalizer must declare:

- allowed source transformations;
- required future context queries;
- whether the source remains accessible;
- state/representation size;
- construction and compatibility-checking time;
- per-query source reads and continuation time;
- DAG reuse and recomputation;
- parsing/output work and peak live space.

Lemma 85A applies only to the resulting declared service. **Accounting is ESTABLISHED; superpolynomial cost is OPEN.**

### 3. All-algorithm coverage

An arbitrary SAT decider is required to answer only one root query. Nothing reviewed extracts a context-complete static service from every decider. Requiring answers for all restrictions, all witnesses, or all residual functions adds an obligation not present in SAT decision.

**Status: OPEN and load-bearing.**

### 4. Superpolynomial contradiction

FIREWALL84’s conditional implication remains correct:

\[
T_A(F)\ge 2^{a r_A(F)}/N^b
\quad\text{and}\quad
r_A(F)/\log N\to\infty
\]

for every decider would imply \(P\ne NP\).

**Status: CONDITIONAL; universal premise unproved.**

## Resource/model ledger

- **Input:** explicit fixed-language 3-CNF, encoded length \(N\), source-variable count \(n\).
- **Residual parameters:** \(k\) eliminated, \(r=n-k\), \(v=n/r\) only as a ratio.
- **Static-service model:** arbitrary deterministic preprocessing; source closed after state construction; exact queries from a declared \(\mathcal C\).
- **Representation charge:** state bits plus any stated gates, wires, switches, or lookup structure. No circuit lower bound is inferred from formula evaluation circuitry.
- **Time charge:** all source reads, failed transforms, state construction, validation, queries, recomputation, and output.
- **Space charge:** peak simultaneously live source/state/workspace.
- **Quantifiers needed for P versus NP:** every uniform deterministic polynomial-time decider for one fixed NP-complete language; infinitely many adversarial inputs after the decider is fixed.

## Computational audit

The executable audit exhaustively enumerated every Boolean predicate for \(r\le4\), verified every root-plus-\(q\)-point quotient, and checked singleton controls through \(r=18\).

Results:

- 65,814 Boolean functions enumerated;
- 524,286 singleton predicates checked;
- 1,871 quotient cases;
- **1,957 assertions, zero failures**.

This validates finite instances of the exact combinatorial identities only.

## Status ledger

- **ESTABLISHED:** static context-service state lower bound; two-class root quotient; exact \(2^q+1\) context ladder; singleton resource separation.
- **COMPUTATIONAL:** finite exhaustive audit with zero failures.
- **CONDITIONAL:** FIREWALL84 universal time tradeoff.
- **OPEN:** extracting a rich context obligation or an expensive compression/direct-decision alternative from every SAT decider.
- **RETIRED:** residual-function diversity, assignment count, or minimal cores as standalone root-SAT time lower bounds.

## Highest-value next missing lemma

Prove a **single-input hereditary-context extraction lemma**:

> For every deterministic random-access SAT decider \(A\), either one charged execution on an explicit formula yields a model-matched service that must answer a superpolynomially rich context family, or the source-aware global compression/direct decision used to avoid that service has superpolynomial charged acquisition, validation, representation, continuation, or peak-space cost.

The statement must survive 2-SAT SCC, Horn propagation, affine/Tseitin elimination, bounded-treewidth DP, component caching, source replay, alternate encodings, and decide-first normalization. Without this lemma, context width remains representation-relative.

## Bottom line

The residual proof question is now sharper: the SAT-only semantic quotient contains only two classes. Exponential residual diversity appears only after imposing extra context queries. Restricted static representations can then be lower-bounded exactly, but no theorem forces an arbitrary SAT decider to expose that interface. The all-algorithm extraction arrow remains OPEN. P versus NP remains OPEN.
