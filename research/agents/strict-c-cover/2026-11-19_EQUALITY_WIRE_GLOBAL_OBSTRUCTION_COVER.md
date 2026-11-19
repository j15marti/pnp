# Strict-C equality-wire universal obstruction covers (2026-11-19)

**Status: PROVED (restricted infinite family); OPEN (arbitrary strict C / P vs NP).** Role: source-verifiable UNSAT obstruction covers, independently fresh run.

Use strict cyclic C(x,y,z), with R(a,b) iff (b-a) mod5 is 1 or 3, and one fresh private head h_e per graph edge e={u,v}. C accepts 30/125 triples, and ∃h_e C(h_e,u,v) iff u≠v.

## Theorem

For every k>=1 form G_k from terminals t_0,...,t_k, four new inner vertices per segment, all 14 K6 edges on each segment's six vertices except t_(i-1)t_i, and one closing edge t_0t_k. Then |V(G_k)|=5k+1, |E(G_k)|=14k+1, and the physical strict-C source F_k has 19k+2 variables and 14k+1 clauses.

**G_k is edge-minimal non-5-colorable; F_k is physical-clause-minimal UNSAT.** In a five-coloring of K6 minus terminal edge, four distinct interior colors force both terminals to equal the remaining fifth color. By transitivity all k terminals equal; the closing edge contradicts this. Deleting the closing edge permits constant terminal color and four remaining interior colors. Deleting an internal edge f permits coloring its endpoints identically and the other four distinct; permuting the palette makes adjacent terminals different. Keep earlier terminals in one color and later terminals in the other. Extend all retained private-head clauses independently with the verified C predicate. The deleted head can equal its endpoint and fail C.

For k>=2, G_k has no K6 subgraph. Strict-C incidence girth is **6**, primal girth **3**. **Do not infer growing girth or search hardness.** This construction is related to classical Hajós chromatic constructions, but the explicit chain certificate and C source checker are proved directly.

## Certified all-z cover

For each shared graph coloring z, edge e's private C clause is refutable iff z_u=z_v. Partition source edges into private-disjoint groups E_j, and define B_j(z)=OR_(e in E_j) [z_u=z_v]. The complete global theorem is

    ∀z∈F5^(5k+1): OR_j B_j(z)=1.

This is a Boolean all-assignment identity, **not a GF(5) witness-count marginal**. A linear-size proof consists of k local equality-forcing implications and one final closing-edge contradiction; every implication has 14 source-clause pointers. It is verifiable without enumerating z.

Let N=19k+2. Grouping <=floor(N^.35) heads per private block gives B=(14/19+o(1))N^.65 blocks. However there are q=5k+1 shared variables, so **explicit** full rows number 5^q, not <=N^.195. This is a symbolic-cover control, not an unrestricted-row-layout solution.

## Source-uniform specialist

A deterministic no-advice recognizer parses original C triples, identifies heads appearing once, tries candidate closing edges, computes biconnected components, checks a chain of K6-minus-edge blocks and independently rechecks the original-source certificate before returning UNSAT. Otherwise UNKNOWN. It never emits SAT or an unsound UNSAT answer. Worst-case expected dictionary operations O(M²), writable space O(M log M) bits, not square-root space. Failed candidates, source reads, materialization and proof checking are included; O(M) work to stream a particular deletion witness, Ω(M²) symbols to materialize all deletion witnesses.

## Executed evidence

Primary seed 2026111907: k=1,2,3,5,8,16,32 accepted, including variable renamings/argument and clause permutation; 271/271 full original-C deletion witnesses, 20,454 retained-C clause checks, 0 wrong-path acceptances for deletions. Archived K6 accepted; Myc3(C5) and four-clause capacity sources returned UNKNOWN. k=32: 610 variables, 449 clauses, 449 candidates tested before canonical acceptance. Independent seed 2026111908: 125 C triples; all 25 head endpoint pairs; K6-e exhaustive 5^6 grid yields exactly 120 proper colorings, all with equal terminals; 200 independently verified deletion witnesses and 15,484 retained C checks; 1,600 test z assignments all yielded source-indexed refutable clauses in 7,644 comparisons, with all five private-head values failing selected clause. Full source code, witness constructions, JSON, SHA-256 manifest are in conversation reproducibility ZIP `T5C_Equality_Wire_Global_Cover_20261119.zip` (SHA-256 9968a1ce9cdfeaf1a812de8bed473a4612d95e44a04065ed64eda01f39b6fb0b).

## Limit and references

An infinite clause-critical family has polynomial symbolic cover discovery, disproving any assertion that criticality or absence of local K6 alone forces expensive obstruction acquisition. General strict C / arbitrary SAT global-cover acquisition remains OPEN. Growing girth and resource-preserving general SAT reduction are NOT established. P vs NP remains OPEN.

Prior records: user `t5_strict_research.pdf`, and `research/coordination/2026-11-19_STRICT_C_COVER_GF5_FIREWALL_HANDOFF.md`. Literature: Hajós 1961, *Über eine Konstruktion nicht n-färbbarer Graphen*; Jensen and Royle 1999, *Hajós constructions of critical graphs*, J. Graph Theory 30:37-50 (DOI 10.1002/(SICI)1097-0118(199901)30:1<37::AID-JGT5>3.0.CO;2-V).
