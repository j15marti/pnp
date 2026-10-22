# RESIDUAL-STATE-FIREWALL84 five-role handoff

**Timestamp:** 2026-10-23 08:48 KST  
**Global status:** P versus NP OPEN.

## Shared invariant

Use \(N\)=encoded input bits, \(n\)=source variables, \(k\)=eliminated variables, \(r=n-k\), and \(v=n/r\) only as a multiplicative compression ratio. Never define \(r\) from runtime.

## Promoted

- **ESTABLISHED upper bound:** exhaustive residual evaluation costs \(2^r\operatorname{poly}(N)\).
- **ESTABLISHED restricted lower bound:** EMPTY-vs-SINGLETON needs \(2^r\) deterministic point queries.
- **ESTABLISHED firewall:** unrestricted semantic preprocessing admits a decide-first normalizer with \(r=0\) whenever the language is in P.
- **ESTABLISHED falsifier:** cubic Tseitin systems retain exponentially many assignments but their label is a linear charge-parity scan.
- **CONDITIONAL:** if every decider has infinitely many inputs with \(T_A\ge2^{a r_A}/N^b\) and unbounded \(r_A/\log N\), then SAT is not in P.

## Not promoted

- “All remaining states must be checked” for explicit SAT.
- Residual cardinality, graph width, source-core coverage, rare witnesses, hashes, or finite solver behavior as unrestricted lower bounds.
- OBDD/subfunction width as a lower bound on arbitrary machines.

## Role assignments

1. **Formalization:** define one fixed normalization protocol and prove label preservation without runtime-defined effective dimension.
2. **Charged normalization:** account for every source read, failed attempt, compressor bit, compatibility check, DAG reuse, output bit, and peak-space live object.
3. **Arbitrary-decider bridge:** attempt machine-to-service extraction or a charged global-compression alternative for every deterministic random-access decider.
4. **Independent falsification:** attack every candidate with decide-first, Tseitin parity, 2-SAT SCC, Horn, bounded-treewidth, component, cache, and source-replay controls.
5. **Synthesis:** promote only an explicit all-algorithm coverage theorem or a precisely scoped restricted lemma.

## Exact chain and status

1. Defined obstruction: **ESTABLISHED restricted**.
2. Acquisition/compression/continuation accounting: **ESTABLISHED ledger; hardness OPEN**.
3. All-algorithm coverage: **OPEN**.
4. Superpolynomial contradiction from the conditional premises: **ESTABLISHED implication**.

## Single highest-value next lemma

For one fixed explicit 3-CNF family and every deterministic random-access machine \(A\), prove:

\[
\text{distinguishable residual burden}
\quad\lor\quad
\text{charged sound-compression burden}
\ge 2^{\Omega(r)}/N^{O(1)}.
\]

The statement must be same-realization, source-aware, representation-independent, and stable under alternate encodings and recomputation. It must survive all named tractable controls.

## Audit

3,115,037 assertions, 799,392 brute-force parity assignments, zero failures. Finite validation only.
