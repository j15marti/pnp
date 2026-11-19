# 2026-11-19 strict-C witness: global equality-gadget minimum, critical chain, rarity versus acquisition

**P vs NP OPEN.** Original C only: Z5, R(a,b) iff (b-a)%5 in {1,3}, C(a,b,c) iff R(a,b)R(b,c)R(c,a) OR R(a,c)R(c,b)R(b,a), 30/125 tuples. Three different variable names per physical clause.

## Theorem A: four is the absolute minimum number of unpinned C clauses that can existentially enforce equality

**PROVED, computer-assisted finite case.** On six distinct names x,y,a,b,c,d, the formula
[
G(x,y)=C(a,x,c)land C(a,b,d)land C(a,c,y)land C(b,c,d)
]
has binary projection x=y. The clauses C(a,b,d),C(b,c,d) share b,d. C(a,x,c) forces a!=c; hence a,c are the *two distinct completions* of adjacent pair b,d and are at cyclic distance 2. Pair a,c has exactly one completing color, so C(a,x,c) and C(a,c,y) imply x=y. Conversely (a,x,b,c,d,y)=(1,0,2,4,3,0) satisfies all four, and translations realize any x=y. Exhaustively, G has 20 full models, four per terminal color, zero with x!=y. Removing each respective clause admits unequal-terminal complete witnesses (0,0,1,3,2,4), (0,1,0,4,1,3), (0,1,3,2,4,0), and (0,1,1,4,2,3), checked by original-C.

Global minimum: A satisfiable incidence-forest formula never forces equality between distinct variable names: choose unequal colors along the unique path, extending each new clause using the fact that every distinct pair of colors has a C completion. If a SAT gadget of at most 3 clauses forces x=y, x,y must lie in a cyclic incidence component. A connected cyclic component with t <=3 clauses and v variable names has 3t edges, t+v vertices and hence v<=2t<=6. Exhaustive exact bitsets check all 1+20+190+1140=1351 sets of <=3 original C clauses on six names and all 15 terminal pairs. None is a satisfiable equality gadget. No larger disconnected source escapes this reduction.

**Priority note:** Section 4 of the user's previously supplied `t5_strict_research.pdf` already lists a *different* four-clause equality gadget. The existence of a four-clause gadget is not new; the global optimality check and the following compact-chain application are the work reported here.

## Theorem B: compact infinite physically clause-critical UNSAT family

**PROVED.** Chain k disjoint-private copies of G(t_i,t_{i+1}) for i=0,...,k-1, closing with C(t0,tk,h). Then N=5k+2 named variables, M=4k+1 physical clauses, incidence girth 4. Every intact G enforces t_i=t_{i+1}, contradicting the closing clause. Each G physical clause is equality-essential; deleting it permits a color mismatch and hence a satisfying completion for the closing clause; deleting the closing clause is satisfied by all-equal terminals. Each single-clause deletion has an explicitly synthesized full original-C witness.

Two independently coded predicates and a separate physical-source checker validated all deletions for k=1,2,8,64: 304 complete witness vectors, 67,244 original-C checks, zero failures. Relative to the older 24-clause high-girth equality chain (girth 8), this is a smaller but **girth-4**, not growing-girth, construction.

The implementation `chain_specialist.py` authenticates the indexed source. It emits CERTIFIED_UNSAT for this complete recognized family after independently checking the constant-size local lemma on all 5^6 assignments, SAT plus fully checked witness for a canonical one-physical-clause deletion, or UNKNOWN for all unmatched sources. No free polarity, auxiliary advice, or oracle. The Python program buffers source/witness, so O(N) writable words; scanning and witness synthesis take O(N) time; generating/checking all deletions takes Theta(N²) output/work. It does not solve general strict C or meet the desired low-row/block architecture.

## Exact critical six-name rarity control

**COMPUTATIONALLY VERIFIED.** H6 has six original clauses 012,013,024,035,234,235. It is UNSAT, but deleting any one leaves exactly **ten** assignments (one D5 orbit). Across all 2^20=1,048,576 subsets of the 20 possible six-name clauses, 1,572 are physical clause-critical UNSAT; exactly 120 six-clause examples have one orbit after **each** deletion. Importantly, all 120 are **orientation XOR inconsistent**, and hence easy to refute. The 960 orientation-feasible physical critical subsets have minimum two deletion orbits. The 960 agrees with the prior strict research package's residual-UNSAT classification.

## Exact witness scarcity versus quick acquisition on the native25 high-girth source

**COMPUTATIONALLY VERIFIED.** Replayed the existing source's 1,046-node original-C UNSAT proof and 25 complete deletion witnesses; source SHA256 a372c198871f73ec9ebf6665e597f0fae7b3af8613aeae325c07bd6e3ca5bd75. Two independently implemented exact AllSAT enumerators (C++ original tournament predicate, Python unordered cyclic-window predicate) agreed on all 25 deletion counts. Their D5-orbit counts, physical clause order 0-24, are:

[38,39,88,22,44,70,38,49,89,42,20,54,29,30,90,20,61,28,78,45,44,50,46,59,86].

Thus each H-e has 200-900 complete solutions among 5^25 possible assignments, yet exhaustive GAC enumeration used only 291-857 nodes per deletion, 12,849 nodes and 22,505,100 tuple support checks over all 25. Summing gives exactly 12,590 distinct one-clause-violation assignments to the original UNSAT F. Random unconstrained full assignment sampling expects between 3.31e14 and 1.49e15 trials to hit a designated deletion witness. **FALSIFIED:** Witness rarity by itself forces counting or expensive deterministic acquisition.

## Open obligations

No unrestricted P!=NP result, source-uniform high-girth witness algorithm, general all-z refutable-block acquisition, or N^1.33 time/N^.5 space solver. The incidence-girth-10 n=150,m=176 native control remains UNSAT computationally but noncritical and without cheap independently replayable static source proof. A claimed generic bound must count source size, encoded children, preprocessing, failed branches, both SAT and UNSAT polarities, materialization, output and verification. Sequential row/block arithmetic still needs local exponent <=97/70, even before overhead.

## Reproduction and prior work

All scripts, independent checkers, source fixtures, 25 AllSAT count ledgers, original 25-source proof, 304 full chain-deletion witness vectors, local 4-clause witnesses and SHA256 manifest are in conversation archive `T5C_Witness_GlobalMinimalEquality_Rarity_Run7_20261119.zip`.

Repository predecessors reviewed: `research/agents/witness/2026-11-19_T5C_FOURCOLOR_COLLAPSE_DISJOINT3CORES_RUN5.md` and `2026-11-19_STRICT_C_GF5_QUADRATIC_WITNESS_AUDIT.md`, plus the user's strict research PDF. Relevant literature: Dechter (1999), *Bucket Elimination*, Artificial Intelligence 113:41-85; Balafoutis/Stergiou (2010), *Adaptive Branching for CSPs*, arXiv:1008.0660.

No asymptotic machine-time lower bound follows from these finite counts or proof-system observations.
