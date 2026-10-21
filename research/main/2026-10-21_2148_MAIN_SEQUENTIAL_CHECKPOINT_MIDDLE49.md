# SEQUENTIAL-CHECKPOINT-MIDDLE49

Date: 2026-10-21, Asia/Seoul. Scope: bounded synthesis across the fixed five roles. Status: exact restricted lemma and computational controls **ESTABLISHED**; deterministic all-input SAT-to-ordinary-MKTP and all-input hereditary ARC remain **OPEN**; both P versus NP and P versus RP remain **OPEN**.

## 1. Repairs proposed before source inspection

1. **Indexed/sequential bifurcation.** Replace “a short seed or state makes the target LOW” by two separately charged cases: a direct indexed evaluator, or a sequential-only generator. In the latter case ordinary KT must include replay or checkpoints.
2. **Source-free state firewall.** A state summary is usable as an ordinary-KT program only if every later transition is source-free. Otherwise the source, a source indexer, or every reread belongs in the program/time ledger.
3. **Circuit representation audit.** For Circuit-SAT/Tseitin targets, distinguish a directly indexed gate/clause decoder from a frontier-state stream. Count the circuit description, input-role metadata, any scramble inverse, checkpoint table, and replay. Unique trace and gate sharing alone imply neither HIGH nor LOW KT.

These mechanisms are falsifiable: a direct fast-forward evaluator retires the proposed sequential opacity; an opposite-label collision retires the semantic map; and a checkpoint/source ledger exceeding the target box retires the resource claim.

## 2. Sources and newest role evidence

Two newest repository sources were read.

- :00 “FUTURE-EXPLICIT25,” commit 5a8fbfa3d51bff28f524044d8d5eaa5d44bcf704, proves that explicitly serializing all remaining target variables in blockwise greedy extension queries costs
  \[
  Q(M,b)\ge \left\lceil M/b\right\rceil M-b\left\lceil M/b\right\rceil(\left\lceil M/b\right\rceil-1)/2,
  \]
  hence \(M^2/(2b)+M/2\) when \(b\mid M\). At \(b=O(p)\), this misses the \(N^{241/200}\) time box. It leaves succinct future compatibility open.
- The newest :12/:00 cross-track report “RP-MKTP-FORK22,” commit f1b891efb6a71005df25be8f60cf58fb7dbe823c, proves the complementary fingerprint fork: a \(q<n\) linear sketch has an INDEX collision, while a stacked full-rank portfolio exposes \(n\) recoverable bits and cannot map every satisfiable unique-witness source to KT \(\le p=o(n)\).

The shared Drive continuity document was read. Its newest substantive fallback entry remains the 2026-10-20 “ARC-HEREDITARY-SCOPED10” handoff; it contains no later unpublished role result. The root manuscript was not read or modified.

## 3. Exact checkpoint compiler

Let a fixed deterministic source-free machine, after receiving a public header of \(h\) bits, emit a length-\(M\) string \(T\). Immediately before each output step it has a complete \(s\)-bit state; one transition and output takes at most \(\tau\) steps. “Source-free” means that the header and state contain every datum used after initialization. If the transition rereads a source \(F\), then \(F\) or a source indexer and its time must be added; the lemma does not grant external oracle access.

For every integer \(1\le B\le M\), store the states at positions \(0,B,2B,\ldots\). There are \(\lceil M/B\rceil\) snapshots. To answer indexed query \(i\), select the snapshot at \(\lfloor i/B\rfloor B\) and replay at most \(B\) transitions.

On an optimistic universal machine with addressable program data,
\[
KT(T)\le h+\left\lceil\frac MB\right\rceil s+cB\tau+O(\log M),
\]
for a fixed simulation constant \(c\). On a sequential program tape, locating a snapshot can cost another \(O(\lceil M/B\rceil s)\); this changes constants, not the exponents below.

Ignoring ceilings and fixed simulation constants, the checkpoint/replay part obeys
\[
\frac{Ms}{B}+B\tau\ge 2\sqrt{Ms\tau}.
\]
Choosing \(B=\lceil\sqrt{Ms/\tau}\rceil\) gives the matching upper envelope
\[
\left\lceil\frac MB\right\rceil s+B\tau
\le 2\sqrt{Ms\tau}+s+\tau.
\]
This is an upper-bound compiler for a specified target, not a lower bound on its true KT.

## 4. Consequence at the proposed \(k=241\) parameters

Write the target length as \(M=N^{6/5+o(1)}\). Then

\[
p=M^{1/241+o(1)},\qquad
N^{241/200}=M^{241/240+o(1)},\qquad
N^{1/2}=M^{5/12+o(1)}.
\]

If a sequential generator uses per-output time \(\tau=M^{u+o(1)}\), total output time forces \(u\le 1/240\). If its state has \(s=M^{v+o(1)}\), the optimistic checkpoint ledger has balanced exponent
\[
\chi(v,u)=\frac{1+v+u}{2}.
\]

Three exact cases are:

| State and step regime | Balanced checkpoint exponent |
|---|---:|
| \(s,\tau=M^{o(1)}\) | \(1/2\) |
| \(s=p=M^{1/241+o(1)},\ \tau=M^{o(1)}\) | \(121/241\) |
| \(s=M^{5/12+o(1)},\ \tau=M^{1/240+o(1)}\) | \(341/480\) |

All are strictly larger than the desired \(1/241\). Indeed, even the optimistic core is at least \(2\sqrt M\) when \(s,\tau\ge1\), so generic checkpointing cannot certify KT \(\le p\) for \(k=241\).

**Status firewall.** This does not prove \(KT(T)>p\). It proves only that the generic replay/checkpoint compilation is too expensive. A different short indexed program may exist.

## 5. Fast-forward falsifier and compact-history comparison

For the explicit transition \(z\mapsto z+1\bmod 2^s\), the state at time \(i\) is \(z_0+i\bmod 2^s\). Every output bit therefore has a direct polylogarithmic-time indexer from the short seed. The checkpoint ledger is irrelevant because algebraic powering gives a better program.

This exactly matches the “COMPACT-HISTORY20” warning: long sequential histories and oracle-query lower bounds do not imply unrestricted time lower bounds against explicit fast-forwardable transition circuits. A viable compatibility descriptor must therefore satisfy all of the following, none currently proved:

1. deterministic and total on both SAT labels;
2. source-free after a fully charged acquisition phase, or else charge all source access;
3. total generation within \(M^{241/240+o(1)}\) time and \(M^{5/12+o(1)}\) peak work;
4. no direct indexed evaluator, affine/source conjugacy, modular powering, or short-seed scramble decoder that makes the target LOW;
5. an actual ordinary-KT HIGH proof on the required label, not failure of checkpointing.

## 6. Circuit-SAT/Tseitin integration

The prior parsimonious Circuit-SAT to proper-3-CNF construction preserves accepting input witnesses exactly and supplies a unique gate-variable extension for each legal input. This representation fact survives gate sharing and clause/variable permutation.

It does not close the MKTP arrow:

- If the circuit/gate table is included in a program, its full description length is charged; gate sharing can reduce this length but does not make it \(O(p)\).
- If clauses are directly indexed from a short circuit descriptor, their bits may be LOW by gate inspection.
- If a hidden-order converter is only sequential, the checkpoint theorem applies only after including role metadata and eliminating source reads.
- A short-seeded permutation adds its seed and inverse-evaluation time to the indexed program. An arbitrary incompressible permutation is nonuniform advice.
- A unique assignment is not automatically hard information: point circuits and canonical Tseitin images permit direct literal/gate inspection. Conversely, a recoverable full-rank digest portfolio carries too much witness information for every SAT target to be LOW.

Thus Circuit-SAT remains a comparison representation, not a third P-vs-NP route.

## 7. ARC and RP cross-audit

- **ARC/FLMV.** Checkpoints stored nonuniformly inside a KT program are not free algorithm workspace. An ARC contractor that materializes them must charge \(\lceil M/B\rceil s\) live bits, replay, source rereads, failed calls, serialized children and ancestors. No all-input hereditary successor follows.
- **P=RP.** A short sequential verifier state is not a uniform deterministic simulation. One must also hit accepting randomness or normalize every RP verifier, with all construction costs charged.
- **P!=RP.** A hard-to-index transcript, digest collision, or verifier-specific checkpoint table is not a language outside P. The language must resist every deterministic polynomial-time decider, including a representation-independent bypass.

## 8. Executable audit

The standard-library checker passed **8,570,287 assertions**:

- 8,421,120 integer checkpoint/block ledgers, including exact AM-GM and balanced upper-envelope checks;
- 1,440 exact checkpoint reconstructions of nonlinear toy streams;
- 352 source-dependency controls showing why omitted source access invalidates the compiler;
- 15,360 modular-increment fast-forward checks;
- 12 exact \(k=241\) threshold comparisons.

Finite tests validate the construction and arithmetic only. They do not compute arbitrary KT or prove either class separation.

## 9. Proof DAG and next discriminating tests

| Role | Status | Weakest arrow | Single next test |
|---|---|---|---|
| :00 SAT→ordinary MKTP | **CONDITIONAL** semantic search, **OPEN** sharp construction | Source-free compact state with both labels and actual ordinary-KT gap | Specify one \(s\le p,\tau\le M^{1/240}\) transition, then attack it with direct indexing, powering, source leakage and checkpoint replay. |
| :12 P!=RP | **OPEN** | Actual uniform RP language outside every deterministic polynomial-time machine | Run the Circuit-SAT candidate through parsimonious conversion, point-circuit inspection and an alternative deterministic decider. |
| :24 ARC/FLMV | **OPEN** | All-input hereditary solver-dependent successor with full peak-resource accounting | Apply a proposed successor to an erasing SAT decider and count every checkpoint/source/child byte at peak. |
| :36 P=RP | **OPEN** | Uniform deterministic simulation of every RP machine | Test whether a sequential-state normal form survives verifier padding and whether its accepting seeds are uniformly hittable. |
| :48 synthesis | **ESTABLISHED guard** | No promotion from failed generic compiler to HIGH KT | Require both direct-index and checkpoint ledgers for every new circuit/digest target. |

**RETIRED:** “short sequential state implies LOW KT,” “checkpoint compiler failure implies HIGH KT,” and “unique circuit trace/gate sharing implies a separation.”

P versus NP and P versus RP remain **OPEN**.
