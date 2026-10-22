# SMALL-INTERFACE-EXACT-JOIN64

Timestamp: 2026-10-22 12:48 KST

**Global status: P versus NP OPEN; P versus RP OPEN.**

This run preserves the two P-vs-NP routes. Circuit-SAT is used as a representation and hostile-control tool, not a third proof spine.

## Repairs proposed before source review

1. **Small-interface exact join:** partition a parent CNF into block-local components coupled only through a shared separator \(S\), enumerate \(S\), and call the arbitrary SAT decider on each fixed block.
2. **Circuit-compressed interface relation:** replace a full compatibility table by a uniform evaluator circuit, charging construction, source access, evaluation and exactness.
3. **Deterministic compatibility fingerprint:** hash each block relation before joining, then test whether exact SAT/UNSAT reconstruction forces an injective summary.

The first mechanism succeeds for a source-checkable restricted class. The second remains open and cannot assume a small exact circuit. The third is blocked in the detached model by CUTSET-TABLE-TRILEMMA58: arbitrary feasibility sets require an injective \(2^{|S|}\)-scale summary.

## Reports reviewed after recording the repairs

1. [ORBIT39](https://github.com/j15marti/pnp/blob/main/research/agents/mktp/2026-10-22_1157_ORBIT39_HANDOFF.md): a genuine ordinary-KT robust-mask counting lemma, but no SAT-sensitive LOW/HIGH labeling. Its attempted generator makes both SAT and UNSAT outputs HIGH.
2. [ARC-DISJ37](https://github.com/j15marti/pnp/blob/main/research/agents/arc/2026-10-22_ARC_DISJ37.md): detached local SAT-answer transcripts cannot reconstruct shared-witness intersection, while a source-aware scan solves the canonical family.
3. [RESTRICTION-SHRINKAGE-BARRIER63](https://github.com/j15marti/pnp/blob/main/research/main/2026-10-22_1148_MAIN_RESTRICTION_SHRINKAGE_BARRIER63.md): exhaustive restrictions have exact semantics but cannot reach \(N^{0.5}\) child length on bounded-occurrence formulas with polynomially many branches.

## Definition — canonically \(k\)-separated block CNF

A parent formula is supplied in a canonical block representation

$$
F=\bigwedge_{j=1}^{J}F_j(S,U_j),
$$

where:

- \(S\) is a shared separator of \(k\) variables;
- the internal variable sets \(U_1,\ldots,U_J\) are pairwise disjoint;
- every clause belongs to exactly one block;
- each literal identifier is tagged either as shared or with its unique block number;
- every block has ordinary encoded length at most \(L\).

The tags make source coherence locally checkable: a block may use shared names and its own local names, but no local name from another block. A hidden cross-block source is rejected rather than compressed into a digest.

This is a representation promise/certificate. Finding such a partition and renaming an arbitrary CNF into it remain charged open tasks.

## Theorem 64A — exact block-interface join

For every canonically separated parent,

$$
F\in SAT
\iff
\exists\alpha\in\{0,1\}^{S}\ 
\forall j\in[J]\;F_j\!\upharpoonright\!\alpha\in SAT.
$$

**Proof.**

If \(F\) has a satisfying assignment, restrict it to \(S\). Its restriction to each disjoint \(U_j\) satisfies \(F_j\!\upharpoonright\!\alpha\).

Conversely, fix an \(\alpha\) for which every block is satisfiable. Choose a satisfying assignment to each \(U_j\). Because the \(U_j\) are pairwise disjoint and all blocks agree on \(\alpha\), their union is a single satisfying assignment of \(F\). \(\square\)

The theorem holds for both SAT and UNSAT parents and uses the real shared source assignment, not independently sampled clause-occurrence witnesses.

**Status: ESTABLISHED for the canonical separated class.**

## Theorem 64B — matched ARC resource point

Let the parent ordinary encoding have length \(N\). Suppose

$$
J\le N^{0.5+o(1)},\qquad
L\le N^{0.5+o(1)},\qquad
k\le(0.1+o(1))\log_2N.
$$

Enumerate every \(\alpha\in\{0,1\}^{S}\). For each \(\alpha\), run the arbitrary deterministic SAT decider \(A\) on all fixed blocks and accept the parent iff one \(\alpha\) makes every block accept.

The number of calls is

$$
Q=J2^k\le N^{0.6+o(1)}.
$$

Materializing one canonical child at a time costs

$$
QL\le N^{1.1+o(1)}
$$

total writes and \(N^{0.5+o(1)}\) peak child-buffer space. Unit and binary clauses created by restriction can be converted to ordinary proper 3CNF by a fixed constant-factor equisatisfiable gadget using fresh block-local auxiliaries.

If \(A\) runs in time \(m^{t+o(1)}\) and space \(m^{s+o(1)}\), the complete simulation satisfies

$$
t'\le\max(1.1,\,0.6+t/2)+o(1),
\qquad
s'\le\max(0.5,\,s/2)+o(1).
$$

The separator assignment, block counter, aggregation bit, all failed calls, padding gadgets, child output and one child buffer are included. The statement assumes the canonical block directory permits sequential block access on the target indexed-tape model; conversion from an arbitrary source representation is not free.

**Status: ESTABLISHED restricted recurrence; exact FLMV endpoint transfer remains CONDITIONAL on the certified source representation and machine encoding.**

## Heredity

Partial assignments only remove shared variables, local variables, literals and clauses. They cannot create a variable shared by two formerly disjoint internal blocks. Therefore canonical separation is preserved under arbitrary restrictions, with separator \(S\) replaced by its unassigned subset and block lengths nonincreasing.

For recursive self-application, require a supplied separator tree in which every node of encoded length \(m\) has:

$$
J(m)\le m^{0.5+o(1)},\quad
L(m)\le m^{0.5+o(1)},\quad
|S(m)|\le(0.1+o(1))\log_2m.
$$

Each child must carry or locally expose the corresponding subtree certificate.

**Status: ESTABLISHED under restrictions; CONDITIONAL hereditary ARC on a source-checkable recursive separator tree.**

It is not an all-input contractor for arbitrary SAT formulas.

## Hostile omitted-source control

Take two blocks

$$
F_1=(z),\qquad F_2=(\neg z).
$$

Each block is individually satisfiable, but their conjunction is UNSAT. If \(z\) is incorrectly treated as block-local or omitted from \(S\), the join falsely accepts. Declaring \(z\in S\) enumerates \(z=0,1\); neither value satisfies both blocks, so the exact join rejects.

This is the smallest SOURCE-CHANNEL21 / CLAUSE-COHERENCE20 control for the construction.

**RETIRED:** any join certificate that does not expose every cross-block source variable.

## Relation to ARC-DISJ37

ARC-DISJ37 proves that answer-only detached protocols cannot recover arbitrary shared-witness compatibility within the target transcript size. The present theorem uses mixed source information in the only permitted way: it explicitly enumerates a certified small shared interface and evaluates all blocks under the same assignment.

Thus the results are complementary:

- large or hidden interface: detached local answers fail;
- certified \(k\le0.1\log N\) interface: exact source-aware joining meets the target call, time and space ledgers.

No unrestricted separator theorem is supplied.

## Circuit-SAT comparison

The same theorem applies to a gate DAG partitioned into block-local subcircuits whose only common primary inputs are the declared \(S\). Gate traces are deterministic block-local auxiliaries after the primary inputs are fixed.

Unique Tseitin traces do not prove that a separator is complete. Every shared primary input or shared predecessor gate must be exposed. Independently sampling trace variables changes the probability space and remains invalid.

## MKTP route audit

ORBIT39's robust ordinary-KT construction is genuine but label-insensitive: both SAT and UNSAT targets are HIGH. Small-interface children instead have short block/assignment descriptors and fast indexed evaluators, so they tend toward KT-LOW once parent reconstruction is charged. They do not provide the missing UNSAT-HIGH target or a deterministic total both-label reduction.

**SAT-to-ordinary-MKTP status: OPEN.**

## P-versus-RP audit

For a promised valid RP verifier, deterministic simulation only needs to hit one accepting original random tape on YES inputs; NO inputs have none. Computing the exact acceptance fraction is unnecessary. The unresolved task is to construct a uniform hitting set for every promised verifier, or for a rigorously defined restricted family, with every source/gate/time/memory dependency charged. Certifying that an arbitrary circuit satisfies the RP promise is a separate problem.

The separator theorem yields deterministic satisfiability for its restricted circuit class, and therefore derandomizes promised RP verifiers in that class. It neither produces a language in RP outside P nor uniformly simulates every RP machine.

**P versus RP status: OPEN.**

## Finite audit

A stdlib-only deterministic audit checked:

- 360 randomly signed separated block formulas;
- exact parent SAT versus the separator-join algorithm;
- 2,160 partial restrictions preserving the equality;
- the hidden-\(z\) UNSAT hostile control;
- 17 exponent-ledger points from \(\log_2N=20\) through 100.

Result: **2,574 checks, zero failures.**

Finite testing supports the implementation only. The theorem is the assignment-gluing proof above.

## Five-role ledger

| Role | Status | Single next discriminating test |
|---|---|---|
| :00 SAT-to-ordinary-MKTP | **OPEN**; ORBIT39 counting lemma **ESTABLISHED restricted** | Prove SAT-sensitive LOW/HIGH labeling or show the best indexed evaluator makes the proposed target LOW on both labels. |
| :12 P!=RP | **OPEN** | Build a uniform accepting-tape hitting set for promised small-interface verifiers; separately test verifier replacement and RP-promise certification. |
| :24 ARC/FLMV | Exact small-interface contractor **ESTABLISHED restricted**; arbitrary-input contractor **OPEN** | Attempt a source-checkable recursive separator compiler, charging discovery and FLMV indexed-tape access. |
| :36 P=RP | **OPEN** | Determine whether complete source-joined coin-dependency DAGs admit \(O(\log N)\) separators and polynomial-range count messages. |
| :48 synthesis | First exact semantic-and-resource contractor **ESTABLISHED for a restricted class** | Stress-test separator discovery on bounded-occurrence expanders and ARC-DISJ mixed-source instances. |

## Route conclusion

- **MKTP magnification:** robust HIGH cores remain label-insensitive; the ordinary-KT both-label arrow is OPEN.
- **ARC/FLMV:** exact joint labels, \(N^{0.5}\) children, \(N^{0.6}\) calls and the desired recurrence coexist on a canonically small-interface recursive class. Extending this to every SAT input is the missing theorem.
- **P versus RP:** equality and separation remain OPEN.

No root manuscript, automation, or role assignment was modified.
