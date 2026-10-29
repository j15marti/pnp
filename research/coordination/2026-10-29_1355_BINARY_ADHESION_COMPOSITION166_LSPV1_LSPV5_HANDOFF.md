# LSPV-3 BINARY-ADHESION-COMPOSITION166, 29 October 2026, 13:55 PDT

Status: RESTRICTED PROVED/EXACT mathematical theorem, independent referee pending; COMPUTATIONAL tests reproduce. P=NP and P!=NP OPEN.

## New exact theorem

A polynomially discovered and verified running-intersection tree of polynomially many explicitly encoded modules has polynomial deterministic SAT/UNSAT decision and exact source-authenticated separator tables when every parent-child separator has at most 2 Boolean variables and each module is a recognized 2CNF plus at most a fixed number e of independent affine equations. Every child table over at most two variables compiles exactly into at most four ordinary 2CNF forbidden-tuple clauses. The parent's 2CNF-plus-affine class is thereby preserved, regardless of the UNION of all its child interfaces. The same uniform controller performs at most 4 local solver invocations per bag and recursively reconstructs verified SAT witnesses, or supplies a replayable complete negative dynamic program. It does NOT promise polynomial ordinary Resolution refutations.

Asymptotic upper bound: D(N) + poly(N) sum_t 2^{|S_t|} (|V_t|+1)^{O(e_t)}; D includes source authentication, complete tree discovery, recognition and validation. For polynomial D, constant e, and at most 2 variables per edge, the class is in P even with center |B_t| linear in N. This strictly improves the FULL-INTERFACE-COMPOSITION165 sufficient premise. Arvind-Guruswami 2021 Theorems 2 and 17 already establish each fixed e local solver (and Theorem 19 W[1]-hardness for varying e). ARC227 implements e=1. No unrestricted SAT compiler or universal shrinker follows.

## Falsifier and limits

A star with 2m distinct center shared variables and m two-variable adhesions takes exponentially many center signatures under the older 2^{|B|} enumerator, but only O(m) child clauses and local tests here. An even-parity XOR3 child and odd-parity XOR3 child on the SAME three-port boundary are jointly UNSAT despite both having tautological strongest unary/binary consequences: blindly using 2CNF messages at 3 ports is UNSOUND. The exact two-variable closure is essential. The generic higher-arity extension requires checking that each full child relation is bijunctive, which is not automatic. An explicit strict signed exact-(2,2)-3CNF chain of constant 17-variable local bags was tested as a bounded-bag corollary; this is a fixed-template subclass, not arbitrary strict22.

## Results, source controls and provenance

Deterministic seed 1661029. Reproducer tested 270 independently brute-forced random mixed tree cases, 69 SAT and 201 UNSAT; six star stress examples up to 64 leaves, with 128 center boundary variables; seven strict22 chain/cofactor controls, separating original strict22 roots from pinned ordinary-CNF cofactors; two deliberately malformed decompositions rejected; three-port parity false-positive reproduced. Total: 2,595 local table entries, 2,552 mixed solver calls, 4,783 SCC 2SAT calls, 43 bounded-bag calls and 1,179,648 bounded local assignment examinations. Repeated run raw JSON SHA256 5d556494d010da292e3cfe061e2e8f5cdf63558da5cd9049a314eb39993763fa. Source Python SHA256 2fb8e8fb3829237c81b2156386d902816efe429f7f5564f4117b18e9ac19cefc.

Original Library Connected_Interface_Audit.zip rerun byte-identically 4,680/7,191/139, results sha256 05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca. Original user portfolio and coverage script results reproduced byte-identically except restart benchmark runtime fields, with same SAT/UNSAT semantics. Repair-only coverage fails on SAT disjoint products, direct branching solves four earlier SAT restart gaps, and only 44/312 portfolio items are strict22 roots.

Inspected Github code files: vardigroup/DPMC/tensor/src/join_tree.py blob 4ab8ffca478243c7c2780728bdfb11eb1857e482, lammich/lrat_isa/thys/LRAT_Checker_Impl.thy blob e50d75e5cd759761399a979766f0acb6af3e1769, arminbiere/cadical/src/elim.cpp blob c401152c7a733803d0b407d98e8a295ab44f7e99. Primary theorem Arvind-Guruswami IPEC 2021 doi:10.4230/LIPIcs.IPEC.2021.5. Prior source FULL-INTERFACE165 Git blob a848d74d8d6ffbf6ee0250cb6fcb3c3ddf4be728. Repo governance skill blob b8df83a7b0b1428f349b0e02ce1387d979e8db7f. No formally verified replay of the new theorem has occurred.

## Root synthesis safeguard and role-specific next lemma

Root main.tex fetched as a **substantive recovered manuscript** with all five role ownership delimiters, not the older placeholder. Only the marked LSPV-3 section may be edited; no LSPV-5 text is to be fabricated or overwritten. Preserve role ownership and existing enabled state/schedules. P vs NP OPEN.

NEXT LSPV-3 LEMMA: Build a connected, unbounded, genuinely branching strict signed exact-(2,2)-3CNF hereditary subclass with polynomially recognizable and verified local bags, two-variable edge adhesions, AND a source-authenticated, reusable local 2CNF-plus-fixed-rank-affine or bounded-bag compiler; prove SAT and UNSAT on one uniform controller. Seek a minimal counterexample when a joining operation breaks the signed occurrence budget or produces a genuine three-bit nonbijunctive message.
