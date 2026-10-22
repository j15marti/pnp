# RESTRICTION-SHRINKAGE-BARRIER63

Timestamp: 2026-10-22 11:48 KST

**Global status: P versus NP OPEN; P versus RP OPEN.**

Scope: the two existing P-vs-NP tracks and the independent P-vs-RP question. Circuit-SAT is used only as a representation and hostile-control tool.

## Repairs proposed before source review

1. **Exhaustive restriction OR:** use the exact self-reduction
   $$
   F\in SAT \iff \bigvee_{\alpha\in\{0,1\}^r} F\!\upharpoonright\!\alpha\in SAT
   $$
   and test whether at most \(N^{0.6+o(1)}\) branches can also yield \(N^{0.5+o(1)}\)-length children.
2. **Clause blocks plus interface joins:** partition clauses into small blocks and reconstruct the parent label through an explicit shared-variable compatibility object, charging separator width and table storage.
3. **Adaptive restriction portfolio:** expose only selected branches, but require a source-checkable completeness certificate proving that every omitted branch is UNSAT.

The first mechanism is falsified at the target exponents below. The second remains the parent-aware batched-join direction isolated by CUTSET-TABLE-TRILEMMA58. The third is not an exact SAT reduction until its omitted-branch certificate is constructed and charged.

## Sources reviewed after recording the repairs

1. [SELECTOR-VIRTUAL-CHILD62](https://github.com/j15marti/pnp/blob/main/research/main/2026-10-22_1048_MAIN_SELECTOR_VIRTUAL_CHILD62.md): target-sized locally indexable clause-selection children, but no all-input parent-label reconstruction.
2. [AFFINE-PIN27](https://github.com/j15marti/pnp/blob/main/research/agents/rp-separation/2026-10-22_RP_AFFINE_PIN27_HANDOFF.md): exact \(2^{d+b}\)-branch affine control decomposition for a restricted XAG model, with full source and gate-trace charges.
3. Craig Tovey, [A simplified NP-complete satisfiability problem](https://www.sciencedirect.com/science/article/pii/0166218X84900817), *Discrete Applied Mathematics* 8 (1984), 85–89: 3-SAT remains NP-complete when every variable occurs in at most four clauses.

## Lemma 63A — bounded-occurrence restriction retention

Let \(F\) be a CNF with \(M\) clause records and maximum variable occurrence \(\Delta\). Let \(R\) be any set of \(r\) variables and let \(\alpha\in\{0,1\}^R\).

At most \(\Delta r\) clauses contain a variable of \(R\). Every other clause is unchanged by the direct syntactic restriction \(F\!\upharpoonright\!\alpha\). Therefore every compacted ordinary encoding obtained only by deleting satisfied clauses and assigned literals contains at least

$$
M-\Delta r
$$

clause records.

**Proof.** Sum the occurrence counts of variables in \(R\). This is at most \(\Delta r\). Counting distinct touched clauses can only decrease that total. Every untouched clause contains no assigned variable, so it survives verbatim. This holds for every assignment \(\alpha\). \(\square\)

**Status: ESTABLISHED.**

### Exact scope

- **Source model:** explicit ordinary fixed-width CNF records.
- **Transformation:** direct partial assignment, deletion of satisfied clauses, deletion of falsified assigned literals, and optional renumbering of the remaining variables.
- **Quantifiers:** for every maximum-\(\Delta\) formula, every chosen set \(R\), and every assignment \(\alpha\).
- **Excluded operations:** semantic preprocessing, resolution, solver-derived equivalences, or a new nonlocal reduction. Such operations may be useful, but their discovery and reconstruction costs must be charged separately.

## Corollary 63B — polynomial-branch shrinkage barrier

Assume \(M=\Theta(n)\) and an ordinary explicit encoding of length

$$
N=\Theta(M\log n).
$$

If exhaustive restriction on \(r\) variables produces all \(Q=2^r\) branches and \(Q\le N^{0.6+o(1)}\), then

$$
r\le (0.6+o(1))\log_2 N.
$$

For constant \(\Delta\), Lemma 63A gives at least \(M-O(\log N)\) clause records per child. Since \(n-r=\Theta(n)\), renumbered literal identifiers still need \(\Theta(\log n)\) bits. Hence every child has length

$$
L\ge N-O(\log N\log n)=N(1-o(1))=N^{1-o(1)}.
$$

In particular, direct exhaustive restriction cannot produce \(L=N^{0.5+o(1)}\) children using only \(N^{0.6+o(1)}\) branches.

Tovey's occurrence-four NP-complete 3-SAT restriction shows that this obstruction occurs on an NP-complete family, not merely on an easy sparse fixture.

**Status: ESTABLISHED for exhaustive direct restrictions.**

This is not a lower bound against arbitrary SAT algorithms or arbitrary nonlocal reductions.

## Lemma 63C — semantics and heredity are exact

For every formula and every variable set \(R\),

$$
F\in SAT
\iff
\exists\alpha\in\{0,1\}^R:\;F\!\upharpoonright\!\alpha\in SAT.
$$

Further restrictions compose: \((F\!\upharpoonright\!\alpha)\!\upharpoonright\!\beta=F\!\upharpoonright\!(\alpha\cup\beta)\) for consistent disjoint assignments.

Thus exhaustive restrictions provide the all-input SAT/UNSAT OR relation and genuine hereditary composition that clause deletion lacked.

**Status: ESTABLISHED semantic relation and heredity.**

The resource target fails: the children remain essentially full length.

## Dual barrier with SELECTOR-VIRTUAL-CHILD62

| Construction | Target child length | Local ordinary-bit access | Exact parent-label relation | Hereditary | Verdict |
|---|---:|---|---|---|---|
| Selected clause subset | \(N^{0.5+o(1)}\) | Yes | No: UNSAT can become SAT | Syntactic only | Resource success, semantic failure |
| Exhaustive restriction, \(Q\le N^{0.6+o(1)}\) | \(N^{1-o(1)}\) on bounded occurrence | Yes | Yes: OR of all branches | Yes | Semantic success, shrinkage failure |

A successful ARC constructor must cross both columns simultaneously. It must be nonlocal or parent-aware on bounded-occurrence inputs, yet retain exact joint labels, virtual ordinary-child access, bounded adaptive rounds, and charged discovery/replay.

## Clause-block/interface repair

Partitioning clauses into small blocks does create short bodies, but parent satisfiability is not an OR of independent block labels. Shared variables require an exact compatibility join. CUTSET-TABLE-TRILEMMA58 shows that a detached \(k\)-bit interface can require a \(2^k\)-bit feasibility table; storing the table or rescanning separately for each child exceeds the target on the INDEX family.

**Status: CONDITIONAL candidate.** The remaining constructive possibility is a parent-aware, source-indexed batched join that avoids a detached full table while preserving exact labels.

## Adaptive-portfolio firewall

A selected subset \(A\subsetneq\{0,1\}^R\) only establishes

$$
\bigvee_{\alpha\in A} SAT(F\!\upharpoonright\!\alpha)\Longrightarrow SAT(F).
$$

The converse needs a completeness certificate that every satisfying assignment projects into \(A\), or that every omitted branch is UNSAT. Producing this certificate may contain the original SAT problem and cannot be treated as free advice.

**Status: OPEN interface; RETIRED if completeness is merely assumed.**

## Circuit-SAT and RP cross-audit

AFFINE-PIN27 is compatible with the barrier. Its restricted \(2^{d+b}\)-branch algorithm is polynomial only when \(d+b=O(\log N)\). That yields polynomially many exact conditioned branches, but it does not imply that their explicit Tseitin/CNF encodings shrink to \(N^{0.5}\). Conversely, a growing \(d+b\) only defeats that particular affine-pinning algorithm, not every deterministic algorithm.

Unique functional Tseitin traces do not change the branch-count/shrinkage calculation. Auxiliary trace variables are computed from the primary source assignment; sampling them independently changes the probability space and violates CLAUSE-COHERENCE20.

**P versus RP remains OPEN.** AFFINE-PIN27 is an exact deterministic algorithm for a certified restricted circuit family, not a uniform simulation of every RP machine and not a language separation.

## MKTP interaction

Direct restriction descriptors are short and their target bits are locally computable from the parent. This tends toward an ordinary-KT **LOW** upper bound once parent reconstruction is charged. It supplies no HIGH target and no deterministic total both-label SAT-to-MKTP generator.

**SAT-to-ordinary-MKTP status: OPEN.**

## Finite audit

The stdlib-only audit generated 90 deterministic occurrence-four 3-CNF fixtures at \(n\in\{6,9,12\}\). It checked:

- maximum occurrence at most four;
- touched clauses at most \(4r\);
- every restricted child retains at least \(M-4r\) clauses;
- \(SAT(F)\) equals the OR of every exhaustive restriction branch;
- \(r\le\lfloor0.6\log_2N\rfloor\) for the target branch budget.

Result: **6,360 checks, 2,310 semantic branches, zero failures.**

This finite audit checks the implementation-facing identities only; the theorem is the counting proof above.

## Five-role status and next discriminating test

| Role | Status | Single next test |
|---|---|---|
| :00 SAT-to-ordinary-MKTP | **OPEN** | Compute the best ordinary-KT indexed evaluator for restriction and selector targets, including parent reconstruction; verify that both remain LOW rather than presuming a gap. |
| :12 P!=RP | **OPEN**; AFFINE-PIN27 **ESTABLISHED restricted** | On a growing WRAPPER XAG, measure \(k,d,b\) and test the independent deterministic bypass and SAT-NO soundness at each size. |
| :24 ARC/FLMV | Restriction semantics/heredity **ESTABLISHED**; target shrinkage **RETIRED** for polynomial exhaustive restriction | Build a parent-aware compatibility join, or prove its separator/table/query-round cost misses the matched recurrence. |
| :36 P=RP | **OPEN** | Determine whether the complete original-coin dependency state admits certified affine controls of \(O(\log N)\) rank after source joins; charge gate queries and tables. |
| :48 synthesis | Dual barrier **ESTABLISHED** | Require the next contractor to pass both bounded-occurrence shrinkage and exact joint-label tests before endpoint exponent work. |

## Route conclusion

- **MKTP magnification:** unchanged missing arrow—deterministic total both-label generation meeting the ordinary KT threshold.
- **ARC/FLMV:** exhaustive direct restriction is now ruled out at the target child and branch exponents on bounded-occurrence NP-complete 3-SAT. Clause selection has the opposite defect. The highest-value open arrow is a nonlocal parent-aware joint-label contraction.
- **P versus RP:** equality and separation remain OPEN.

No root manuscript, automation, or role assignment was modified.
