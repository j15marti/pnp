# Strict T5 independent red-team: S-to-C criticality transfer fails in general

2026-11-19 America/Los_Angeles. **PROVED** exact gadget projection and finite counterexample; **FALSIFIED** general preservation of clause-minimal UNSAT; **OPEN** unrestricted P vs NP and general computational lower bounds. This file is owned by the new independent audit role, not a modification of prior reports.

## New lemma, exactly quantified

Take strict T5 R(a,b) iff (b-a) mod 5 in {1,3}, strict-C directed triangle, and S(h,u,v) requiring the designated head to beat one follower and lose to the other. C accepts 30/125 ordered triples; S accepts 40/125. Each physical clause has three different variable **names**; values may repeat outside clauses.

For every h,u,v in Z5, with fresh independent names p,q, define the standard S-to-C gadget:
G = C(h,u,q) AND C(h,q,p) AND C(h,p,v).

The full existential projection over p,q equals S(h,u,v). If one physical C clause is deleted, the projections are:
- remove C(h,u,q): h != v (100 of 125 tuples);
- remove C(h,q,p): h != u AND h != v (80 of 125);
- remove C(h,p,v): h != u (100 of 125).

**Proof:** For all a,b, exists w C(a,b,w) iff a != b. For first deletion, C(h,p,v) needs h!=v; it chooses p different from h, and then q can complete C(h,q,p). Middle deletion leaves independent existential q in C(h,u,q) and p in C(h,p,v). Last deletion is symmetric. The full S projection was separately exhausted over all 125 triples and 25 pairs p,q per triple.

For ANY S-CSP source F with disjoint auxiliary pairs per gadget, deleting physical gadget clause (i,d) from G(F) is SAT iff some assignment to the original variables satisfies every S_j for j!=i and the corresponding displayed deletion projection T_d at i. This is an exact logical equivalence, not a lower bound.

## Five-variable five-clause counterexample

Let a,b,c,d,e be five distinct variable names. Set
F = S(a,b,c) AND S(a,b,d) AND S(b,c,d) AND S(b,c,e) AND S(e,c,d).

No assignment of 5 colors to these five names satisfies F. Deleting its five S clauses, respectively, leaves 50, 50, 20, 20, 40 satisfying original-variable assignments. Concrete deletion witnesses (a,b,c,d,e):
1 (0,1,0,4,2); 2 (0,1,2,3,0); 3 (0,1,2,4,3); 4 (0,2,1,3,2); 5 (0,2,1,3,0).
All witnesses were verified against the original S predicates.

After deleting S(b,c,e), the other four clauses FORCE b=e. Explicitly, S(a,b,c), S(a,b,d), S(b,c,d) have exactly 20 color quadruples (a,b,c,d), in every one c,d have pentagon distance 2 and b is the unique possible S-head for (c,d). S(e,c,d) therefore forces e=b. The removed S(b,c,e) would require b!=e.

Expand each of the five S clauses with two fresh private names and three C clauses. The final C instance has 15 names and 15 clauses, is UNSAT, and fails clause minimality: deleting the first OR middle C clause of gadget S(b,c,e) still forces b!=e, contradicting the other four gadgets. All other 13 C deletions are SAT, with complete 15-name original-C witnesses constructed and verified. Single-C deletion SAT flags, in source gadget order, are:
1 1 1 | 1 1 1 | 1 1 1 | 0 0 1 | 1 1 1.

The S source and expanded C source each have clause-incidence girth 4. This refutes **general** S-to-C criticality transfer, not the specialized edge-critical private-head graph transfer.

## Exhaustive bounded minimality claim

Enumerating every subset of the 12 distinct S head/follower constraints on four names found 56 clause-minimal UNSAT sources, none violating gadget criticality. Enumerating every S constraint set on five names of size <=4 (30 possible distinct source constraints) found 200 clause-minimal UNSAT sources, none violating gadget criticality. Thus the example is minimum in clauses for at most five named variables. There is no claim of global minimum over arbitrary n.

An independent evaluator used a hardcoded five-row tournament table and exhaustively replayed all 125 triples, 25 local auxiliary pairs, 3,125 original-variable rows per physical C deletion, and 13 complete C deletion witnesses (182 retained clause checks). Source SHA256 = 2e9c04b6bc93e6ef11d9094b2972f70549b28c1e5e190668b01bfdf7f2e511e5; expanded source SHA256 = b679259f433b4cc1685e13f7b32a03cbb735ecd0597613fd4a61e364b00eb411.

Primary verifier counters: 423827 R evaluations, 26979 original C evaluations, 129525 S evaluations, 809492 traced Python heap bytes peak. Peak is NOT a formal writable-space bound; all source and enumeration storage is charged in its execution.

## Positive control: private-head K6 graph gadget

A separate independent generator built 45 complete strict-C witnesses for each single physical deletion of the S-to-3C gadgetized K6 private-head encoding. All 1980 retained original-C clause checks passed. Therefore the new counterexample does not invalidate the previously established graph-special-case criticality theorem. The gadget unavoidably introduces incidence 4-cycles, so it also cannot transport a high-incidence-girth claim.

## Audit firewall for resource-transfer claims

The user-specified row/block layout with R<=N^.195, B<=N^.65, private size<=N^.35 requires a complete local solver exponent alpha<=97/70 for a straightforward fully charged N^1.33 sequential scan. A standalone polynomial SAT-witness seed or a supplied correct polarity is not enough. The source/verification costs, all unsuccessful branches and child calls both polarities, output, materialization, replay and simultaneous peak workspace are not free. UNSAT row indices are not negative certificates and finitely supplied rows need not be all z.

Read back prior GitHub sources:
- research/agents/proof/2026-11-19_LOCAL3COL_C_SOURCE_ACCESS_RESOURCE_FIREWALL.md
- research/agents/strict-c-cover/2026-11-19_GF5_MARGINAL_FALSE_ZERO_GLOBAL_COVER.md
Reviewed user Library t5_strict_research.pdf. The original strict ZIP was not retrieved in this audit.

**CONDITIONAL only:** Buss & Williams (Computational Complexity 2015, DOI 10.1007/s00037-015-0104-9), Theorem 2 and Figure 1, certify the random-access deterministic SAT simultaneous exclusion at (c,epsilon)=(1.34070,0.5), distinct from any restriction to critical strict-C sources. Applying this to the lead's indexed fixed-width 3CNF -> C construction still requires the exact SAT source-encoding/machine-model transfer. Nothing here proves P!=NP.

**Next blocker:** All agents using S-to-C translations with a criticality promise must verify the projected deleted-gadget relations or construct source-checked witnesses for every *physical C clause* deletion. No task schedule, agent state or older manuscript was modified.

Reproduction package: \`T5C_Redteam_Criticality_Transfer_20261119.zip\`, with full executable Python, exact sources, complete witness vectors, exhaustive raw JSON and SHA256 manifest. It was created in the current conversation, not posted by this GitHub commit.

**P versus NP remains OPEN.**