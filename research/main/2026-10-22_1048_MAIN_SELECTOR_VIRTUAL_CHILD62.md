# SELECTOR-VIRTUAL-CHILD62

Timestamp: 2026-10-22 10:48 KST  
Global status: **P versus NP OPEN; P versus RP OPEN.**  
Scope: the two P-vs-NP routes and the independent P-vs-RP question. Circuit-SAT remains a comparison and representation tool.

## Repairs proposed before source review

1. **Fixed-slot restriction compiler:** preserve every parent clause slot and replace satisfied/deleted records canonically, giving easy bit access but no length contraction.
2. **Rank/select compaction:** store a selector for the retained source clauses, charge its construction and space, and retrieve the requested child record directly.
3. **Interval/block child:** restrict selectors to source intervals so descriptors are logarithmic, then test whether such children retain the semantic reconstruction required by ARC.

The second mechanism was proved for clause-deletion children. The first fails the (N^{0.5}) child-length target; the third is even more syntactically restricted and supplies no arbitrary-SAT decomposition theorem.

Repository sources reviewed after recording the proposals:

- [VIRTUAL-CHILD-COMPOSITION61](https://github.com/j15marti/pnp/blob/main/research/main/2026-10-22_0948_MAIN_VIRTUAL_CHILD_COMPOSITION61.md), which isolates the required descriptor/bit-evaluator interface;
- [ARC-INDEX34](https://github.com/j15marti/pnp/blob/main/research/agents/arc/2026-10-22_ARC_INDEX34.md), which requires all-input heredity, exact labels and the FLMV-matched recurrence;
- [AFFINE-BASIS25](https://github.com/j15marti/pnp/blob/main/research/agents/rp-derandomization/2026-10-22_0836_RP_AFFINE_BASIS25_HANDOFF.md), the current restricted derandomization and source-certification audit.

## Lemma 62A — selector-indexed virtual CNF child

Let a parent CNF (F) contain (M) fixed-width clause records over (n) named variables, with encoded length

[
N=Theta(Mlog n)
]

for constant clause width. Let (S=(s_0<cdots<s_{K-1})) select (K) parent clauses. Define (F_S) to be those clauses in selector order, retaining the original variable identifiers.

A descriptor storing (S) uses

[
D=Klceillog Mceil
]

bits. Given (F,S) and a child-bit index (i), the corresponding bit of the ordinary encoding of (F_S) is computable by:

1. decoding (i) into child clause number (j) and record offset;
2. reading (s_j) from the descriptor;
3. reading the requested field from parent clause record (s_j).

With random access to the parent and descriptor, this costs (operatorname{polylog}N) time and (O(log N)) scratch beyond the descriptor.

**Status: ESTABLISHED restricted construction.** It is an explicit instance of the ((d,g)) interface from VIRTUAL-CHILD-COMPOSITION61.

### Target ledger

Choose the child encoded length

[
L=N^{0.5+o(1)}.
]

Then (K=Theta(L/log n)), and

[
D=Theta(Klog M)=N^{0.5+o(1)}.
]

For (Q=N^{0.6+o(1)}) children, constructing and consuming descriptors sequentially costs

[
QD=N^{1.1+o(1)}
]

time and one (N^{0.5+o(1)})-bit descriptor buffer. An arbitrary decider (A) of exponents ((t,s)) can then be simulated on each virtual child using Lemma 61A, yielding the conditional resource recurrence

[
t'le max(1.1,0.6+t/2)+o(1),qquad
s'le max(0.5,s/2)+o(1).
]

Descriptor generation and validation are included only if each selected index is produced and checked in polylogarithmic time. Discovering which clauses should be selected remains a separate charged obligation.

## Lemma 62B — syntactic heredity

If a grandchild selects positions (T=(t_0,ldots,t_{K'-1})) of (F_S), flatten the selectors to

[
Scirc T=(s_{t_0},ldots,s_{t_{K'-1}}).
]

This produces a direct selector into the original parent. It can be written in (K'operatorname{polylog}N) time, uses only the new descriptor as persistent storage, and preserves exact bit access. Therefore selector-indexed clause deletion is hereditary under further clause deletion.

**Status: ESTABLISHED syntactic heredity.** This is not the semantic heredity required by the ARC proof.

## Semantic hostile control

Clause deletion weakens a CNF. It preserves satisfiability in only one direction:

[
Fin SATLongrightarrow F_Sin SAT.
]

It does not preserve UNSAT or permit the parent label to be reconstructed from one arbitrary selected child. The three-clause control

[
F=(x)wedge(
eg x)wedge(y)
]

is UNSAT, while the selector retaining ((x)wedge(y)) produces a SAT child.

Thus local indexability, exact ordinary encoding, target length, descriptor space and syntactic heredity can all hold while the load-bearing semantic ARC condition fails.

**RETIRED:** treating clause-deletion heredity alone as the all-input hereditary ARC contractor.

The missing theorem must generate a bounded family of children whose labels jointly determine the parent label on every SAT and UNSAT input, while each child still has a locally indexable ordinary encoding and every discovery/validation cost fits the recurrence.

## Fixed-slot and compaction distinction

A pure partial restriction can be locally evaluated clause-by-clause if every parent slot remains present: satisfied clauses become canonical true records and falsified literals become constants or canonical padding. This gives local bit access, but the child remains length (Theta(N)), not (N^{0.5}).

Compacting away inactive slots reaches the length target only with a select structure identifying the (j)th surviving record. An arbitrary (K)-subset needs

[
log {Mchoose K}=Theta(Klog(M/K))
]

bits in the worst case, which is (N^{0.5+o(1)}) at the current parameters. This fits the peak-space exponent for one descriptor but not a polylogarithmic descriptor claim. The sequential ledger remains valid; simultaneous storage of (N^{0.6}) descriptors does not.

## Circuit-SAT and source coherence

The construction copies complete source clause records and retains common variable identifiers. It does not independently resample clause occurrences, so CLAUSE-COHERENCE20's equality-join failure is avoided. If selected records include Tseitin clauses, gate-trace uniqueness still depends on the primary variables and complete gate-role map; it does not make arbitrary semantic child selection source-local.

DIGEST-LUMP19 remains unchanged: a short selector or digest is not a complete transition state unless every hidden source, solver, timer and history influence factors through it.

## RP cross-audit

AFFINE-BASIS25 remains **ESTABLISHED restricted** for verifiers with certified full-row-rank affine coordinates and conditionally independent local factors. Selector-indexed CNF children neither certify that factorization nor yield a universal hitting set. They provide no language in RP outside P and no deterministic simulation of every RP machine.

## Consistency checks

The construction was checked symbolically:

- (K=Theta(N^{0.5}/log n)) selected clauses give descriptor length (Klog M=N^{0.5+o(1)});
- (Q=N^{0.6}) sequential descriptors cost (N^{1.1+o(1)}) total writing time;
- selector composition preserves direct access to the original parent;
- the explicit UNSAT-to-SAT deletion control falsifies semantic label heredity;
- storing all descriptors simultaneously would cost (N^{1.1+o(1)}) bits and is excluded.

No executable audit was run because the execution environment was unavailable. The mathematical result and counterexample do not depend on finite testing.

## Five-role ledger

| Role | Status | Consequence | Single next test |
|---|---|---|---|
| :00 SAT→ordinary MKTP | **OPEN.** Selector compiler **ESTABLISHED restricted**. | With a succinctly reconstructible parent, local target-bit access strengthens the ordinary-KT LOW audit; it does not supply a HIGH target. | Compute the complete ordinary-KT bound for a selector child, including parent reconstruction and descriptor length. |
| :12 P≠RP | **OPEN.** Source-channel firewall **ESTABLISHED**. | Copying coherent records avoids local-witness spuriousness but gives no language lower bound. | Apply the SAT-NO control and independent-decider bypass to any selector-based RP verifier. |
| :24 ARC/FLMV | Selector ((d,g)) and syntactic heredity **ESTABLISHED restricted**; semantic reconstruction **OPEN**. | The resource interface is feasible for clause subsets; the all-input SAT/UNSAT label relation is missing. | Construct a bounded selector family whose child labels exactly reconstruct the parent, or prove a concrete family needs too many selectors. |
| :36 P=RP | AFFINE-BASIS25 **ESTABLISHED restricted**; universal derandomization **OPEN**. | Clause selectors do not imply affine factor independence. | Trace original-coin dependency cones through one selected Circuit-SAT child. |
| :48 synthesis | Both class questions **OPEN**. | The ((d,g)) engineering problem is solved for clause deletion, isolating semantic reconstruction as the remaining failure. | Prioritize the joint-label reconstruction rule, not further selector optimization. |

## Route conclusion

- **MKTP magnification:** unchanged missing arrow—deterministic total both-label generation at the ordinary KT threshold.
- **ARC/FLMV:** a real locally indexable, target-sized, syntactically hereditary virtual-child compiler now exists for clause-deletion families. It fails the all-input semantic reconstruction requirement, which is now the primary missing arrow.
- **P versus RP:** equality and separation both remain **OPEN**.

No root manuscript, automation, or role assignment was modified.
