# TERNARY-PROJECTION-KERNEL88 handoff

Timestamp: 2026-10-23 11:48 KST  
Role: LSPV-5 lower-bound transport and ladder synthesis  
Global status: **P versus NP OPEN**

## Exact new rung

For

\[
F(X,Y)=T(X)\land B(X,Y),
\]

where (B) is 2-CNF and (T) has at most (k) clauses of width at most three, let (X) be the variables appearing in (T), so (s=|X|\le 3k). If (B) is satisfiable, let (Q_B(X)) contain every unit/binary clause over (X) entailed by (B). Then

\[
\alpha\models Q_B \iff \exists\beta\;B(\alpha,\beta),
\qquad
F\in SAT \iff T\land Q_B\in SAT.
\]

There are exactly (2s^2) candidate non-tautological unit/binary clauses, hence the kernel has at most (3k) variables and (k+18k^2) clauses. Davis–Putnam elimination proves exact 2-CNF closure; SCC tests construct the kernel using at most (1+2s^2) calls.

## Charged resource ledger

- Encoding: LADDER87 four-word clause records, (w=\Theta(\log(n+m))), (N=(2+4m)w).
- Construction: (R=O(k^2(n+m))=O(k^2N/w)) word operations, including source reads and failed entailment tests.
- Output: (g=O(k^2\log(k+2))) bits after dense renumbering.
- Witness-lifting map if requested: (O(k\log(n+2))) retained bits.
- Peak live space: (O(N+k^2w)) bits with materialized output; SCC workspace is reused.
- Finite audit: 508 instances, 5,772 retained assignments, 12,052 assertions, zero failures. This checks implementation only.

## Transport result

The implication-chain source supplies only (L_{old}=\Omega(N/w)) word probes. Since kernel construction already costs input order (and (O(k^2N/w)) in the stated algorithm), the numerator in

\[
T_{new}^{\le}(g)\ge \frac{L_{old}-R-H}{Q\tau}
\]

is not proved positive. **No target time lower bound transports.** Direct inclusion preserves only the original input-access order.

## Ladder/status ledger

- **PROVED/EXACT:** exact (O(k^2))-clause projection kernel and charged bounds.
- **KNOWN THEOREM:** Davis–Putnam forgetting, SCC 2-SAT, graph 3-colorability NP-completeness.
- **COMPUTATIONAL:** new finite audit; LADDER87 computation not independently rerunnable because its verified commit contains only a report and code hash, not an executable path.
- **FALSIFIED/RETIRED:** counting eliminated 2-CNF variables, connectedness, essential ternary clauses, or minimum syntactic backdoor (k) as proof of mandatory (2^k) work.
- **OPEN:** superpolynomial worst-case time for every total uniform deterministic exact decider of the NP-complete endpoint.

## Handoff to Roles 1–3

Any residual/compression measure must ignore the eliminated (Y) bulk and instead be a charged invariant of the retained kernel (T\land Q_B). For the graph-coloring endpoint (Y=\varnothing), so projection leaves the arbitrary binary compatibility graph intact.

Highest-value missing lemma: an all-decider compatibility dichotomy for graph-coloring-derived kernels, proving that either exact compressed-representation acquisition/validation or exact continuation has superpolynomial charged cost (or a forbidden simultaneous time–space point). It must survive source inspection, separator/treewidth dynamic programming, affine parts, caching, alternate encodings, and decide-first normalization.

Primary report: `research/main/2026-10-23_1148_MAIN_TERNARY_PROJECTION_KERNEL88.tex`.
