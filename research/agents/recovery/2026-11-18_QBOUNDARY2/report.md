# QBOUNDARY2: recovered separator controller and exact Q boundaries

18 November 2026, Pacific Time. Role: Prior-Work Recovery. P versus NP OPEN. Additive continuation of QRECOVERY1; no manuscript ownership, title, schedule or enabled-state changes. Independent peer audit of this continuation is pending.

## Result

Recovered project work already provides a separator controller with source authentication and conservative treatment of unresolved children. Its exact-boundary semantics specialize to Q, but its Boolean 2-CNF terminal theorem cannot simply be reused for five-valued ternary constraints.

PROVED/EXACT: Q is not determined by its three binary projections on the original variables. Their natural join accepts 100 triples, versus Q's 60. Applied clausewise, this relaxation admits 180 assignments to the known five-clause critical UNSAT system. Exact boundary tables preserve compatibility; coarse projections do not. This statement concerns this explicit relaxation, not all algorithms using binary auxiliary encodings or stronger consistency procedures.

## Recovered originals; avoid duplicate work

1. `research/coordination/2026-11-11_AFFINE_TABLE_COMPOSITION3_HANDOFF.md`, blob `176efb125f07a4ed7054ec245ce0922719f747ef`: automatic separators of size at most two; validation of forest structure, running intersection, complete source scopes and ownership; unknown children remain possible and selected unresolved children prevent a SAT claim. It already restores a Gaussian terminal before normalization that would hide affine structure. Its referenced ARC235/236 precede the controller and cover exact pair interfaces and exceptional ternary messages. Those original ARC files were not re-audited this run.
2. `research/agents/shield1/2026-11-19_0834KST_SHIELD1_T5_CRITICAL_BOUNDARY_SIGNATURE.md`, blob `f172df254b3feea1dde7536a2b5578a23b1ab10d`: exact binary-R two-terminal signatures reduce from 25 entries to five by rotation. Series/parallel joins require disjoint interiors and witness rotations must be aligned. Small signatures do not make their acquisition cheap. Its 33-vertex binary-R computation is recovered evidence, not newly executed Q evidence.
3. `research/agents/recovery/2026-11-19_LOCAL4/report.md`: independently enumerable row witnesses cost a sum of searches, not a Cartesian product of complete strategies. This assumes a complete finite row set and independent local proof obligations.
4. `research/agents/recovery/2026-11-19_QRECOVERY1/report.md`: the supplied exact-one archive, T3/T5 coloring projection, critical-deletion transfer, ternary sparse-lift decoding and full polarity ledger. Its archive SHA256 is `d811f0ea0b00fc88ebecf2349585386a2f0079508139aa638a8635e765e8a30a`; 23 manifest entries were verified in that run. The extracted source remains available locally. This run reuses its exact five-clause control and independently recounts its six outcomes.

Dechter's *Bucket elimination: A unifying framework for reasoning* (1999), DOI 10.1016/S0004-3702(99)00059-4, is primary background for exact elimination and space/time tradeoffs. Search recovered the publisher abstract and author's publication record; direct publisher opening returned 403. No novelty is claimed for separator dynamic programming or exact relational joins.
https://ics.uci.edu/~dechter/publications.html

## Binary-projection falsifier

The supplied wins are A:BD, B:CE, C:AD, D:BE, E:AC. Write Q(x,y,z)=R(x,y) XOR R(x,z), with false self-wins and values allowed to coincide.

The (x,y) projection is all 25 pairs: for any fixed x,y there is a z with the opposite win bit, since each x has two wins and three nonwins. The same holds for (x,z). The (y,z) projection is disequality: equality makes XOR false; for unequal endpoints a head equal to the winner works. Their join is therefore simply y!=z, with 5*5*4=100 assignments. For example (A,A,C) passes all pair projections but fails Q. Hence no conjunction of binary relations on these same three variables defines Q: each factor of any such representation must contain the corresponding Q projection, so its conjunction contains this larger join. This does not exclude binary encodings with auxiliary variables.

For the imported five clauses

    Q(a,b,c), Q(a,b,d), Q(b,a,c), Q(b,c,d), Q(c,a,d),

the clausewise binary relaxation has precisely the disequalities ac,ad,bc,bd,cd. Choose c,d in 20 ordered ways and independently choose a,b among the three remaining colors, giving 180 assignments. Exact enumeration finds zero Q assignments. The five one-clause deletions have 10,40,10,30,25 assignments. The per-head parity graphs are a two-edge star for head a, a two-edge path for head b, and one edge for c; all are bipartite. Thus the control survives both per-head parity and this binary-projection relaxation.

The five-clause core is already known; the new check connects it explicitly to the recovered boundary controller's information-retention obligation. It is not a new hard family or a lower bound. No four-variable catalogue or completed random grid was repeated.

## Exact rotation-normalized separator lemma

Let F1,F2 be Q formulas whose declared variable sets intersect exactly in an ordered nonempty boundary S=(s1,...,ss). There are no shared interior variables. For boundary assignment a, let C_i(a) count interior extensions satisfying F_i. All simultaneous rotations preserve Q, so C_i(a)=C_i(a-a(s1)). Store C_i only on a(s1)=0, at most 5^(s-1) entries.

Then the exact number of assignments to F1 AND F2 is

    5 * sum_{a:S->[5], a(s1)=0} C_1(a) C_2(a).

Proof: condition on all boundary values. The private extensions are independent, so their counts multiply. Summing counts every complete assignment once. Common rotation partitions boundary assignments into five-element orbits with identical products. For SAT use Boolean supports and intersection instead of integer multiplication. This argument also applies to P and binary R because each is rotation invariant.

The normalization must use the same boundary anchor. Independently anchored components must be rotated into agreement; deleting their relative phase is not licensed by symmetry. Empty boundaries require a product of full component counts, without the displayed extra factor five. Counts and Boolean support are different interfaces: a support bit alone supplies neither a multiplicity nor an interior witness.

Given a common supported row, reconstruct one extension in each component, align their boundaries, combine the interiors and verify every original clause. A table of correct existence bits is insufficient to charge reconstruction: retain witness pointers with their memory cost, or rerun the search with the selected boundary fixed. With guessed tables, soundness requires validating their semantics, not merely checking that table entries agree at the join. For one-sided refutation, a proved overapproximation is safe only when its final support is empty; nonempty support is UNKNOWN unless an original witness is reconstructed.

## Fully charged implementation scope

Let P,W be paid decomposition discovery, validation, renaming, ownership and indexing time/space. Let A_i,B_i be actual component-table acquisition time and peak workspace. They include every failed route, child of either polarity, table materialization and sound verification. With s boundary variables, Boolean joining costs Otilde(5^(s-1)) time after acquisition. Keeping two full tables costs O(5^(s-1)) bits plus access indices. A safe sequential bound retains the first table while constructing the second, so peak work includes its size plus B_2, not just max(B_1,B_2). Exact counts can need O(v) bits per entry, and arithmetic must pay that bit length.

A simple universally correct acquisition procedure enumerates all 5^vi assignments to component i, tests its mi clauses, and accumulates normalized rows, costing Otilde(5^vi(vi+mi)) time. It can use a color vector, a row table and counters; it need not retain every model. Reconstruction by a fresh fixed-boundary enumeration costs Otilde(5^(vi-s)(vi+mi)) per component in the worst case. Output and final full-source verification are additional. These are executable upper bounds, not necessary work.

Across a supplied tree decomposition, exact finite-domain messages give the standard bag-enumeration method. Summed retained tables and reconstruction pointers must be included. A width bound alone does not give square-root workspace while retaining all messages. Recomputing messages may lower peak space but raises time; this run does not assert an unproved simultaneous bound for that tradeoff.

For the user's Boolean block layout, replacing repeated full-row work by support-indexed work is legitimate only when the exact residual is determined by that support and all original clauses/owners are authenticated. LOCAL4's local-proof enumeration remains

    P + sum_z 2^kz (V_z+k_z+1) + output,

with one current proof/verifier and paid layout storage. Full-support scanning with a seed of time ell^c and space ell^s still gives exponents max(1.195,.845+.35c), max(.35,.35s). Reaching (1.33,.5) requires c<=97/70, s<=10/7, and no omitted costs. Merely assuming a polynomial SAT seed proves neither restriction. No hereditary compiler has been recovered that closes this gap.

## Correct choices and resource exclusions, by polarity

Free polarity routing supplies the decision label; it is not a uniform decision algorithm. A supplied SAT path must reconstruct a full assignment and check the original source; wrong paths reject. A supplied UNSAT path must verify the full refuting cover or another sound refutation, including all universal rows. One favorable branch does not suffice. Adaptive existential choices require a whole strategy description or traversal of all relevant universal histories.

For a clocked, universally sound k-bit verifier complete on all instances of one polarity, deterministic enumeration costs O(2^k(V+k+1)) time and O(S+k+log V) workspace. Independent row proofs allow the additive bound above. A deterministic sound specialist complete on its polarity within a known clock likewise decides by timeout. Promise-only completeness does not justify all-CNF decision. A rereadable external certificate is separate read-only input; ordinary nondeterministic guesses must be retained or accessed through a proved paid consistency mechanism. Output produced on a rejected path is not a valid witness.

The following primary statements were revisited; model is uniform indexed/random-access machines with read-only source, write-only output, charged address/work tapes, and bounded-word RAM only through justified polylog-overhead simulation:

| Polarity | Exclusion and limits |
|---|---|
| Deterministic SAT/UNSAT | Buss–Williams Theorem 2/table: published (1.34070,.5) DTISP exclusion with +o(1) exponents; also c<2cos(pi/7) for subpolynomial space. Thus an all-CNF (1.33,.5) decider is excluded, on the same resource model. |
| Nondeterministic UNSAT / co-nondeterministic SAT | FLMV Corollary 6.5 excludes NTIME[n] containment in coNTISP[n^c,o(n^((1+c)/c^2-c))]. At c=1.10 the space exponent is .635537..., supporting the (.1 above linear,.5 space) calibration with reduction slack; at 1.33 that displayed exponent is negative. |
| Nondeterministic tautology/UNSAT | Diehl–van Melkebeek–Williams: c^2 d<4 implies some e>0 forbids both NTIME(N^c) and NTISP(N^d,N^e) tautology algorithms. Taking c=d gives d<cuberoot(4), but e is not identified as .5. |
| Nondeterministic SAT | These NO-side statements do not establish a (1.33,.5) exclusion. The earlier opposite-polarity attribution remains withdrawn. |
| Proof-system-specific refutations | Resolution or restricted-interface bounds constrain those certificates/algorithms, not every sound execution. |

Sources: https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/samCCC-cr.pdf ; https://lance.fortnow.com/papers/files/tst.pdf ; https://research.cs.wisc.edu/techreports/2007/TR1601.pdf . None transfers automatically to Q critical deletions or the supplied-layout promise. Free short correct choices remove acquisition by assumption, but leave replay, compatibility and all universal obligations. No contradiction follows from the finite controls below.

## Executed evidence

`q_boundary_recovery.py` independently declares the exact win table. It enumerates all 12 distinct-scope canonical clauses on four names and all 144 ordered pairs, under both Q and P on matched scopes. It compares direct counts with exact common-anchor boundary joins and checks every reconstructed witness. This is a targeted join audit, not a rerun of all 4,096 systems.

| Counter | Q | P |
|---|---:|---:|
| Ordered clause-pair cases | 144 | 144 |
| Predicate evaluations, including model acquisition and direct counting | 142,560 | 119,520 |
| Boundary-row table lookups | 2,880 | 2,880 |
| Peak sum of two sparse normalized table sizes | 24 | 8 |

All count and witness checks pass. The script separately verifies the 100-versus-60 projection collision and preserves all 180 false-positive core assignments, exact clauses and deletion counts in raw JSON. There is no random seed. The table-size counter excludes brute-force model lists, Python object overhead and raw-output accumulation; it is not measured process RAM. The script deliberately retains model lists as an independent finite oracle. Analytical resource formulas above describe a different streaming implementation, with acquisition and replay explicitly charged. No timing, hardness ranking, or asymptotic lower bound is inferred from these counters.

## Status and next dependency

PROVED/EXACT: original-variable binary-projection impossibility for Q; five-clause projection false positives; exact shared-anchor separator join and conditional cost ledger.
COMPUTATIONAL: 288 paired join cases, witness checks, projection/core checks.
RECOVERED: ATC3 validated controller and unresolved-child semantics; SHIELD1 orbit-signature algebra; LOCAL4 additive row replay.
CONDITIONAL: inexpensive table acquisition, useful source-recognizable separators, and low-space reconstruction.
OPEN: global five-letter compatibility outside these restrictions; all-input hereditary compiler; growing-girth intrinsic-critical witness transfer; independent peer audit; P versus NP.

The next useful recovery target is ARC236's exceptional-interface cover: determine whether its conditions can recognize Q boundary relations without silently converting ternary information to pair projections. Any extension must also handle private-head graph-coloring controls, which pass per-head parity yet retain global coloring difficulty. Merely expanding a separator or giving its exact table as advice is not a solution.

Gates: DISJ and information-counting PASS (no execution lower bound); relativization/algebrization/natural-proofs separation not asserted; simultaneous DTISP accounted conditionally, universal bridge OPEN; configuration counts are not used as lower bounds. No local repository checkout or manuscript compilation; targeted corpus review only. No schedules or root manuscripts changed.
