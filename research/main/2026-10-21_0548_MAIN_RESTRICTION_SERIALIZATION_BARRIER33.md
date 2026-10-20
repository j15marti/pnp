# RESTRICTION-SERIALIZATION-BARRIER33

**Timestamp:** 2026-10-21 05:48 Asia/Seoul  
**Scope:** exactly two active directions: MCSP/MKTP hardness magnification and arbitrary-SAT-decider ARC contraction into a matched FLMV endpoint. COMPACT-HISTORY20 remains diagnostic, not a third route.  
**Global status:** **P versus NP remains OPEN.**

## 1. Recovery and publication boundary

I read the governing proof-portfolio and continuity files, the user-specified
COMPACT-HISTORY20 addendum at commit
`c4e1f72f10976405fa2479c88499894d3d58633f`, the maintained
`main2.tex`--`main5.tex`, recent repository commits, and the shared fallback
handoff. The maintained roots remain blobs `56464cb3...`, `d82342d2...`,
`0281dcfc...`, and `05d9adae...`. Root `main.tex` is now blob
`23cae3cd...` and still contains both the literal omitted-body summary and the
literal `Full content continues` placeholder. It is unsafe and was not edited.
The fallback document still ends at `ARC-HEREDITARY-SCOPED10` and contains no
newer complete two-route specialist body.

The newest scientific commit is
`5c4c273238a4ac5b8a9b8ab7244f8ce5bb370018`,
`CHMY Bridge 32: two-update Stream-Merge digest falsifier`. Its exact report is
available. It gives a concrete collision showing that two four-bit checksums
cannot replace the old circuit in a second MMW Stream-Merge update, and proves a
restricted retained-information lower bound `d + m ell >= b`. It also derives
incompatible exponent requirements for one explicitly defined naive query
fragmentation. The reported executable package and raw ledger were not
published in the repository, so its stated 81,706 checks are not promoted here
as independently reproduced. The result does not falsify MMW, which retains the
full prior circuit.

## 2. Falsifiable repairs proposed before literature review

1. **Restriction-volume test.** Test the most direct ARC construction: branch
   on `b` variables, serialize every residual, and recurse. Falsifier: an
   explicit proper-3CNF family on which every canonical residual remains
   `Theta(N)` bits even though the number of children is at most `N^(3/5)`.
2. **Shared-parent escape.** Represent a residual by `(parent pointer,
   assignment)`. Falsifier: the downstream solver needs ordinary serialized
   input; expanding the pointer representation costs `Omega(N)` per child or
   else changes the machine/input model.
3. **Semantic-pruning escape.** Ask the hypothetical solver which branch to
   retain. Falsifier: charge every query, answer, failed branch, replay, and the
   construction of the retained ordinary child; a small answer transcript does
   not itself provide serialization shrinkage.
4. **MMW state-retention repair.** Preserve one common global circuit witness
   across updates rather than independent digest statuses. Falsifier: two source
   prefixes inducing the same retained state but different required global
   circuits. This is the correct next MCSP experiment, not a claim that all
   batched compilers fail.

## 3. Primary-source model check

- CHMY (Cheraghchi--Hirahara--Myrisiotis--Yoshida, STACS 2021) proves a
  randomized two-sided-error lower bound for a **one-way read-only input plus one
  work tape**. Corollary 23's oracle-RTM PRG has seed length
  `tilde O((sqrt(t)+log(1/epsilon)) log(q 2^ell t))`. This does not transfer an
  ARC construction to unrestricted random-access machines.
- MMW (McKay--Murray--Williams, STOC 2019) defines Stream-Merge using the old
  circuit, a starting index, and a fresh block. Theorem 4.2 gives ordinary MKTP
  streaming in `O(N p)` time and `O(p)` space with `Sigma_3 SAT` queries of
  length `O(p)`, assuming `p >= log N`. It is downstream of an existing target.
- OPS (Oliveira--Pich--Santhanam, Theory of Computing 2021) Theorem 1.4 is a
  nonuniform circuit magnification theorem for a specified **promise** Gap-MCSP
  regime and every sufficiently small `beta`; it is not an unrestricted SAT
  time theorem.
- FLMV (Fortnow--Lipton--van Melkebeek--Viglas, JACM 2005) concerns
  deterministic random-access machines. Corollary 5.8 forbids
  `DTISP(n^c, o(n^d))` for nondeterministic linear time with
  `d = ((c+2)/c^2-c)/2`; at `c=6/5`, `d=23/45>1/2`.
- Ilango's positive reduction remains random-oracle-relative. Hutter competes
  only with programs carrying suitable correctness/runtime proofs; Blum speedup
  precludes a general fastest-program conclusion; Levin-style search does not
  bound the unknown exponent of an arbitrary hypothetical SAT decider. The
  easy-witness theorem is conditional on its own circuit-easiness premise and
  does not prove COMPACT-HISTORY20's single `exists W forall i` witness-size
  assumption.

## 4. Exact restricted theorem

### Definition (selector family)

Let `H` be any proper 3-CNF on variables disjoint from selectors
`x_1,...,x_b`. For every `i in [b]` and `j in [m]`, introduce fresh variables
`a_ij,b_ij,c_ij,d_ij` and add

```
(x_i or a_ij or b_ij)
(not x_i or c_ij or d_ij).
```

Call the conjunction `F_{b,m,H}`. For an assignment `alpha` to the selectors,
perform syntactic restriction and replace each surviving 2-clause `(u or v)`
by the canonical proper-3CNF pair

```
(u or v or z) and (u or v or not z)
```

with a fresh `z`. Denote the ordinary serialized child by `C_alpha`.

### Theorem (canonical restriction does not contract)

For every `b,m >= 1`:

1. `F_{b,m,H}` and every `C_alpha` have exactly `|H|+2bm` proper 3-clauses.
2. The `2^b` canonical children are pairwise distinct: for each selector bit,
   the child contains either the `a/b` block or the disjoint `c/d` block.
3. `C_alpha` is satisfiable iff `H` is satisfiable. Each selected gadget block
   is independently satisfiable.
4. Under any conventional explicit encoding with variable identifiers of
   `Theta(log V)` bits, both source and every child have length
   `Theta((|H|+bm) log V)`. In particular, child length is `Theta(N)`, not
   `N^(1/2+o(1))`.

### Proof

Fix `(i,j)`. Exactly one of its two source clauses is satisfied and deleted by
`alpha`; the other becomes a 2-clause. Canonical properization replaces that
one 2-clause by exactly two proper clauses, restoring the original count of two
per gadget. Disjoint variable blocks reveal which clause survived, proving
pairwise distinctness. Setting one nonselector literal in each surviving block
to true satisfies all gadgets independently, leaving precisely the truth of
`H`. The source and child have the same asymptotic numbers of literals and
variables, proving the serialization statement.

### ARC consequence and firewall

Choose `b <= (3/5) log_2 N`; then the branch count `2^b` can satisfy the ARC
call-count envelope. Nevertheless every ordinary child is linear-sized. Thus
**plain DPLL restriction plus canonical serialization cannot realize the
missing square-root ARC successor**, even when its branch count is acceptable.

This is a construction-specific obstruction, not an arbitrary-machine lower
bound. A compiler may recognize and delete these independent gadgets, share the
parent through a DAG/pointer, or use a different semantic decomposition. The
first is a special semantic simplification; the second is not an ordinary
serialized child unless its expansion/access is charged; the third remains the
open research target. The theorem therefore retires only unqualified appeals to
ordinary branch-and-restrict shrinkage.

## 5. Reproducible audit

`experiments/review/2026-10-21_restriction_serialization_barrier33.py`
enumerates both a SAT empty core and the standard eight-clause UNSAT core on
three variables for `1 <= b <= 10`, `1 <= m <= 12`.

- 240 source instances;
- 49,104 ordinary residuals;
- 98,208 exact clause-count checks;
- 240 complete distinctness checks;
- 49,104 semantic controls;
- 442 ARC exponent checks;
- 6,096,058 instrumented assertions;
- zero failures.

The observed explicit child/source encoding ratio was between `1.0` and
`1.0783368484483278`; name-length variation explains the upper endpoint. The
audit validates the stated construction, not minimum circuit complexity and not
an unrestricted SAT lower bound. Audit digest:
`6f40bf2445cfc8ee596bf766c4894029b53a6bfef8b3823b543c5970ef4bbf33`.

## 6. Versioned proof DAG

### ESTABLISHED / PROVED

- MMW, CHMY, OPS, Ilango, and FLMV only in their exact source models.
- Fixed-parameter hardwiring after fixing a hypothetical solver.
- Short tags and adaptive short transcripts remain low KT after local replay.
- The new canonical restriction/serialization barrier above.

### COMPUTATIONAL

- The new 6,096,058-assertion audit, with the restricted scope stated above.
- CHMY TWO-UPDATE32's claimed local counts remain report-only pending published
  code/raw.

### CONDITIONAL / CANDIDATE

- `SAT -> charged total R_k -> ordinary MKTP at p_k=M^(1/k+o(1)) -> MMW ->`
  simultaneous SAT resources -> FLMV, conditional on the missing total `R_k`
  and a correct same-machine ledger.
- Shared-parent residuals are candidates only after ordinary-child expansion or
  locally addressable access is charged in the FLMV model.

### OPEN

- Deterministic standard-model replacement for Ilango's random oracle.
- A total both-label SAT-to-ordinary-MKTP reduction with a real KT gap, no
  `M`-bit side table, and charged target generation.
- An all-input hereditary ARC successor with at most `N^(3/5+o(1))` children,
  ordinary child length at most `N^(1/2+o(1))`, peak workspace at most
  `N^(1/2+o(1))`, and all acquisition/replay/output charged.
- COMPACT-HISTORY20's one circuit `exists W forall i` of size `tau(n)^o(1)`.

### FALSIFIED / RETIRED

- Short digests as a replacement for MMW's prior global circuit in the tested
  two-update compiler.
- Naive fragmentation under the specialist's stated exponent inequalities.
- Plain branch/restrict/properize as the missing square-root ARC contractor.
- Any promotion of these restricted barriers to an unrestricted SAT lower
  bound.

## 7. Role-targeted next falsifiers

- **:00 MCSP:** build one two-update compiler that preserves a single common
  global circuit witness; publish code/raw and charge old-circuit retention,
  source reads, queries, returned bits, and one-tape state.
- **:12 Universal Solver:** test whether proof-certified selection changes any
  target-side KT term or merely relocates the unknown solver exponent and proof
  search.
- **:24 ARC:** implement one ordinary child generator beyond syntactic
  restriction; report child bytes, parent accesses, live ancestor bits, solver
  calls, rejected branches, and output.
- **:36 Red team:** attack any shared-parent child with a random-access trace;
  reject hidden parent pointers or uncharged lazy expansion.
- **:48 Synthesis:** compare only source-matched arrows and preserve the two
  active routes plus the COMPACT-HISTORY20 diagnostic.

No schedule was changed and no third route was activated. **P versus NP remains
OPEN.**

