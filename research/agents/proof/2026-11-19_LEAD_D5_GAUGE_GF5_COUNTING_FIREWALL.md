# Strict T5 lead: D5 gauge, GF(5) modular-counting firewall and unrestricted bridge
Date: 2026-11-19 Pacific. **P versus NP remains OPEN.** Theorem PROVED; exact experiment VERIFIED.

## Theorem (PROVED)
For strict C, colors Z5, R(a,b) iff (b-a) mod5 in {1,3}, the original directed-cycle predicate has 30/125 true triples. It is equivalent to Q(a,b,c)=((a-b)^2+(b-c)^2+(c-a)^2) mod5 =1. Its automorphism group contains all 10 color maps a -> s*a+t mod5 (s=+1 or -1). An exhaustive scan of all 120 alphabet permutations confirms **exactly** these ten.

For ANY strict-C source F with >=1 physical clause (three distinct variable names per clause, repeated values on different names allowed), D5 acts freely on the set of satisfying complete color assignments. Nonidentity translations have no fixed assignment; reflections fix only one color, whereas each satisfied C clause uses three different colors. Thus #SAT(F)=10*k_F. For ANY designated clause C(u,v,w), exactly one member of every satisfying orbit has u=0 and v in {1,2}. Thus k_F equals the gauge-fixed solution count.

For Q as above, I_C=1-(Q-1)^4 over GF5 is the original-C indicator. Consequently SUM_{a in GF5^n} PRODUCT_{e in F} I_C(e(a)) = #SAT(F) mod5 = 0 for **every** F with n>=1, SAT or UNSAT. An unfixed GF(5) model-count sum is therefore identically blind to SAT. This does not invalidate arbitrary polynomial calculus or weighted/gauge-fixed methods.

**Post-gauge counterexample (PROVED):** F=C(a,b,c) AND C(a,b,d) involves all four variables and has exactly 50 satisfying assignments, hence 5 gauge-fixed assignments and 0 mod5 *even after* orbit division. Example witness (a,b,c,d)=(0,1,2,2). Its three-clause extension AND C(a,c,d) is clause-minimal UNSAT, with a satisfying original-C witness for every clause deletion.

## Exact experiment (COMPUTATIONALLY VERIFIED)
Run `audit_orbits.py` in user-facing ZIP `T5C_ProofLead_OrbitAudit_20261119.zip`. Every nonempty subset of possible unordered 3-name C clauses was tested for n=3,4,5. Enumerated original-C models; independently verified GF5 polynomial predicate; checked all D5 color automorphisms; counted gauge-normalized models and ensured exactly 10-to-1 for every nonempty source.

| n | nonempty sources | SAT | UNSAT | physically minimal UNSAT | SAT with zero gauge mod5 residue | failures |
|---:|---:|---:|---:|---:|---:|---:|
|3|1|1|0|0|0|0|
|4|15|10|5|4|10|0|
|5|1023|242|781|30|40|0|

No random seeds. Script SHA256 `77d1d51ce420af53228b3b381d9ec553bea2468e3f1528ceb73765cb2dfa2278`; results SHA256 `ff96efd2a90acaf9cfb2299182dce38ec7922c3f0c04966015a9f6367a9cccc2`.

Replayed independent proof checker bundled in prior `T5C_Native_StrictC_25_Critical_and_GrowingGirth_20261119.zip`: canonical native C source 25 names/25 clauses, incidence girth 8, 25/25 physical deletion witnesses, 600 true retained-clause checks, 25 false deleted clauses, full UNSAT proof tree 1046 nodes, 600 contradiction leaves. Canonical source SHA256 `a372c198871f73ec9ebf6665e597f0fae7b3af8613aeae325c07bd6e3ca5bd75`. This verifies that finite proof certificate, not asymptotic hardness.

## SINGLE best P vs NP connection (OPEN)
Retain the prior locally indexable 3-CNF -> unrestricted C compiler, with exact names 15+9v+39m and physical C clauses 10+7v+31m, as the only established resource-aware bridge. It does not preserve intrinsic clause-criticality, increasing incidence girth, or the proposed low-row/block promise. Exact SAT/UNSAT correctness and indexed source access are necessary. See [compiler](https://github.com/j15marti/pnp/blob/main/research/agents/proof/2026-11-19_LOCAL3COL_C_SOURCE_ACCESS_RESOURCE_FIREWALL.md).

Buss-Williams (2015) Figure 8.2/8.3 verifies an alternating-trading SAT exclusion at (c,epsilon)=(1.34070,.5), 44 rounds/406 triples. The paper defines DTISP using deterministic algorithms/Turing machines; any transfer to an actual random-access RAM and fixed-width local compiler must match that model, not assume it. Even a fully transferred exclusion at (1.33,.5) does NOT imply P != NP; it excludes one simultaneous resource point. Proving P != NP requires an unrestricted all-polynomial bound, or a **new proved** self-improvement from any hypothetical polynomial-time C solver to a forbidden time-space point.

For literal full scans over R<=N^.195 rows, B<=N^.65 blocks of private size <=N^.35 with local full decision exponent a, conditional T exponent is max(1.195,.845+.35a), requiring a<=97/70 for total time 1.33. Re-scanning an unindexed N-bit source separately for every (row,block) costs N^1.845 at saturation; B offsets need N^.65 log N writable bits. No polarity advice, wrong-path acceptance, uncharged materialization/certificates, or unsupported all-z symbolic cover is allowed.

## Handoff
(1) Resource specialist: exact Buss-Williams model/bit-access adapter; (2) Cover specialist: complete all-z proof for native-C25, not printable disjunction; (3) Witness specialist: red-team GF5 counting with 50/5 counterexample; (4) Critical constructor: incidence girth and original physical deletions; (5) Red team: verify S/C gadget criticality and total machine costs.

Refs: [Buss/Williams 2015](https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf); [Williams 2006](https://www.cs.cmu.edu/~ryanw/sat-journal-final.pdf); [Bulatov/Kazeminia modular CSP 2024](https://doi.org/10.1137/23M1548633). User strict package PDF `t5_strict_research.pdf` accessed through Library search. No P-vs-NP proof claimed.