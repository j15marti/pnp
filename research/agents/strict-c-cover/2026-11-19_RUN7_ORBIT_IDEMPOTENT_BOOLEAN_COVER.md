# Strict-C global obstruction cover: exact D5 orbit idempotents (run 7)

**PROVED restricted structural theorem, COMPUTATIONALLY VERIFIED fixtures; P vs NP OPEN.**

Canonical original predicate: R(a,b) iff (b-a)%5 in {1,3}, and C(x,y,z)=R(x,y)R(y,z)R(z,x) OR R(x,z)R(z,y)R(y,x). Exactly 30/125 ordered triples accepted. Three distinct variable NAMES per clause, arbitrary reuse of values elsewhere. No S/Q/P substitution.

## Theorem 1: three orbit projectors (PROVED)

Fix shared names z0,z1 and private variables x. For any conjunction H(z0,z1,x) of unpinned original-C clauses, E_H(a,b)=1 iff there exists x satisfying H. The dihedral D5 color symmetries imply that E_H depends only on the orbit of b-a: E (difference 0), A (difference ±1), B (difference ±2). There are exactly eight possible binary invariant relations.

In F5[t]/(t^5-t), t=z1-z0, define

    hE = 1-t^4
    hA = 3(t^4+t^2)
    hB = 3(t^4-t^2)

These are orthogonal idempotents: sum=1, h_i²=h_i, and h_i*h_j=0 for i!=j. Each projected block relation is exactly a sum of a subset of these three idempotents. When private variables of blocks are pairwise disjoint conditional on (z0,z1), F=AND_j H_j has extension indicator W=PRODUCT_j E_j. Hence F UNSAT iff the intersection of all three-bit support masks is empty. **This product is cancellation-free and must not be replaced by counts modulo five.**

## Theorem 2: all eight relations have original-C gadgets (PROVED + AUDITED)

The prior compact 10-name eight-clause source contains disjoint private blocks:

    B0 = C(0,2,3)&C(0,2,4)&C(1,2,5)&C(1,5,6)&C(3,4,6)
    B1 = C(0,7,8)&C(1,7,8)
    B2 = C(0,1,9).

The exact masks are B0=110, B1=101, B2=011 in (E,A,B) order. Their pairwise intersections give 100,010,001, and all three give 000. A lone C(0,u,v), independent of terminal 1, gives 111. Thus every binary D5-invariant relation has a native original-C realization with at most eight physical clauses. Independently counted all 25 terminal pairs for each of eight realizations (200 pair-cases), and replayed original-C witnesses for every positive orbit. The fully combined eight-clause formula has incidence girth 4 and is physically clause-critical, per prior source; we rechecked all eight physical deletion SAT witnesses.

For its three blocks the polynomial indicator is

    (hE+hA)(hE+hB)(hA+hB) = 0  mod (t^5-t).

This verifies ALL 25 shared assignments with three source-checked orbit classes, not a sampled-row argument.

## Theorem 3: deterministic two-polarity specialist (PROVED)

Enumerate candidate shared pairs lexicographically, compute source-derived connected components after removing each pair, and accept a pair only if it produces >=2 disjoint nonempty private blocks of size <= p. Otherwise return UNKNOWN. For the chosen pair, test (0,0),(0,1),(0,2), using deterministic exact private enumeration against every ORIGINAL C clause. If one orbit has a satisfying extension in every block, concatenate the disjoint private witnesses, check every original clause, and return SAT. Otherwise emit at most THREE source-indexed refuted blocks, one for each orbit, and return UNSAT. An independent verifier reconstructs the block partition and exhaustively checks every private assignment in each refuted block. Source SHA-256 authenticates the bytes but is not itself a proof.

Fully charged conservative reference complexity:

    O(n²(n+m) + 3 SUM_j 5^(p_j)(m_j+1) + n+m) time,

with n names, m physical clauses, p_j private names per discovered component, m_j local clauses. This includes unsuccessful pair and private branches; replay repeats negative enumeration. The Python implementation stores O(n+m) words and DOES NOT meet N^.5 writable space or N^1.33 time on unrestricted input. Growing q yields (5^q+5)/10 orbits, so this two-terminal result does not solve general SAT.

## Adversarial audit

Deterministic seed 20261119, original-C 30/125 and 125/125 independent predicate agreement, quotient-ring product all-zero coefficients. The eight-clause source's three UNSAT refutations were independently replayed with 4,254 original-C predicate evaluations and 3,155 rejected private tuples. All eight clause-deletion controls returned fully checked SAT witnesses. Twenty-four random renamings/tuple shuffles remained UNSAT and were replayed; five forged certificates were rejected. Native 25-variable incidence-girth-8 source returned UNKNOWN at p=5. The connected two-clause block C(z,a,b)&C(z,a,c) has 10 extensions per fixed z, zero mod 5 despite SAT, reconfirming modular-count cancellation.

**Packing firewall:** Joining conditionally independent components cannot increase intrinsic projection cost from SUM of individual searches to the product of their domains. A deliberately padded 1,034-name, 520-clause source with N=n+m=1,554 has three symbolic orbit rows <=N^.195, 89 packed blocks <=N^.65, and maximum 12 private names <=N^.35. It is **not clause-critical**, has girth 4, and still has only three nontrivial refuting blocks. All 86 extra packed blocks are universally compatible. This is a counterexample to inferring hard counting from block-size numerology, not an asymptotic machine lower bound.

## References, reproducibility and limits

Reviewed earlier repository report `research/agents/proof/2026-11-19_RUN2_COMPACT_EA_ORBIT_PHYSICAL_CRITICAL8.md`, prior local strict-C min-sum/SA3/GF5 archives, and `t5_strict_research.pdf` via Library search. See Dechter, *Bucket Elimination*, AI 113 (1999), doi:10.1016/S0004-3702(99)00059-4; Carbonnel, Romero, Živný, SIAM J Comput (2021), doi:10.1137/19M1250121. Reproducible conversation archive `T5C_OrbitIdempotent_SourceGlobalCover_Run7_20261119.zip` contains `orbit_cover.py`, `independent_check.py`, `run_experiments.py`, `packed_layout.py`, `eight_relation_catalog.py`, fixtures, all witnesses, raw results and SHA256SUMS. Archive SHA256 `2ca7a20baab09f8d047af0254ed52b45a383535bfe49a10585c3186eb845880c`. Independent repo publication/readback is metadata authentication, not peer review.

**OPEN:** resource-preserving source-uniform global covers for growing shared boundary q, especially high-girth physically clause-critical strict-C sources. No general deterministic N^1.33/N^.5 solver or P-vs-NP separation established.
