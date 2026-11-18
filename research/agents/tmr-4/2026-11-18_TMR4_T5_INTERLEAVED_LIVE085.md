# TMR-4/085 | T5 interleaved-bit live-open-symbol reverse simulation

**Source model:** Authenticated directed graph `G=(V,E)` with T5 relation `R(a,b) iff (b-a mod 5) in {1,3}`. All loops/opposing arcs are recognized as legitimate potential UNSAT inputs; no NP-hardness assumption is used in the construction. **Status:** restricted proof of a parameterized exact FBDD simulation; finite verification COMPUTATIONAL; no arbitrary-machine lower bound.

## Theorem

Given an explicit, validity-sound adaptive *bit* FBDD `B` representing the fully encoded T5 decision predicate on the five valid 3-bit words per original variable and rejecting invalid words, define `Past(v)` as the union of symbols whose bits have been queried on prefixes ending at bit node `v`; `Future(v)` as the symbols with bits appearing at or below `v`; and `p=max_v |Past(v)∩Future(v)|`. If B has s reachable nonterminal nodes, an exact **at-most-once five-valued FBDD** A exists with at most `s·6^p` nodes. Every original assignment has the same accept/reject decision in B and A.

Proof: carry the exact values of already queried source symbols in a cache at a bit node if a further bit of that symbol is possible. When a bit of a new symbol appears, query the original symbol once with five choices; when it is cached, route deterministically. Prune a cached symbol only when absent from all reachable suffix nodes. A memo key consists of the bit-DAG node and the map of live symbols to colors. There are at most six possibilities per potential live symbol (unqueried or one of five colors). Source-symbol read-once legality and pointwise equivalence follow by induction.

**Multiplicity:** A is not necessarily complete: an accept path querying d of n source variables represents `5^(n-d)` full assignments. A depth-indexed integer DAG dynamic program exactly computes `Z=sum_{accepted paths}5^(n-d)`; rejected inputs count `5^n-Z`. Count bare accept paths only after an explicitly paid complete-path conversion. Completing partial paths can add exponential state; the `s·6^p` bound must not be cited for that stronger convention.

The transducer needs `O(s·6^p poly(n+log s))` bit resources **after** authenticating G and constructing and verifying B. Producing B from arbitrary G is not claimed polynomial. The reference audit's truth-table bit-OBDD construction enumerates all `8^n` binary words, charged `O(8^n(n+m))` time.

## Fixed-order falsifier

For the authenticated edgeless source on n vertices, native complete five-way OBDD size is n. Its validity-sound Boolean function accepts exactly the 5^n valid code tuples. Query all n high bits first, then middle/low bits. A prefix with high-bit set S has residual `AND_{i in S}(!middle_i & !low_i)`. Different subsets S are separated by a low-bit test, so the exact residual quotient has 2^n elements. Any OBDD respecting **that** order has at least 2^n-1 nonterminal suffix states. A grouped-bit decoder has at most 6n nodes. This is not an all-order FBDD lower bound, nor a hardness claim about T5-CSP.

## Four predeclared falsifiers

1. Invalid binary words could be accepted if a native terminal were copied without validity checks. The audit evaluates all 8^n binary words, not merely valid words.
2. Counted FBDD terminal paths are not full assignment multiplicities when some source variables are skipped. Depth weights are mandatory and checked.
3. Dropping a live color when a later bit of its source symbol remains reachable can cause an illegal repeated source-variable query. The audit checks read-once legality path by path.
4. Large bad-order residual count and large p alone do not imply expensive source computation. The same edgeless source has an n-node complete native OBDD and a grouped validity decoder of size <=6n.

## SAME_REALIZATION ledger

The original canonical UTF-8 graph bytes with literal vertex list `[0,...,n-1]`, ensuring `L>=n` and their SHA-256 hashes are charged and retained. Parse, validation, source-graph scanning, Boolean source compilation, bit-order selection, bit-DAG Past/Future bitsets, the exact set of live source symbols, color caches, five-way fanout, state merging, repeated-node memoization, switching, early terminals, all exact count additions and output, and optional Boolean/CNF conversion are included. A conservative paired transducer-only bit bound is `O(s·6^p·(n+log(s·6^p))^3)` time and peak writable storage. CNF uses exactly `3n+15m` explicit forbidden-tuple clauses over `3n` bits; all 32 domain masks remain distinguishable and their 2048 oriented pair-support tests commute with valid-code embedding. No Fourier, arithmetic approximation, or free backdoor/decomposition is used.

## Four verification gates

- **G1 authenticated source and legal DAG:** 107 canonical sources of n<=4 (58 SAT/49 UNSAT across order-specific cases), including SAT, UNSAT, self-loops, opposing arcs, edges, cycles and edgeless graphs; six malformed-byte controls; every transduced source-variable path read once.
- **G2 pointwise:** 25,495 original five-color assignments and 153,904 complete three-bit words checked against native constraints and explicit source diagrams.
- **G3 exact arithmetic and representation:** all accepted/rejected full multiplicities compared to independent brute force; 153,904 literal CNF evaluations; 2,048 domain support checks; 2^n distinct bad-order residuals verified for n=1..6; largest tested native 142 nodes, Boolean 83 nodes, max p=4 among primary small cases.
- **G4 independent verifier/reproducibility:** independent Node.js BigInt semantics rehashed all source records, brute-forced 25,495 source assignments, checked 153,904 CNF words and 299,592 residual distinguishing suffixes. Both Python and JavaScript reruns produced byte-identical results; zero unexpected failures.

Full original Python/JavaScript, raw case sources, evidence JSON, deterministic repeated outputs and mathematical report are in `TMR4_085_T5_interleaved_live_bridge.zip` attached to the research conversation. The root manuscript contains the complete theorem. This branch stacks on /084, preserving TMR-4 identity, ongoing ownership, prior manuscript, and schedule.

## Dependency

`D4-T5-INTERLEAVED-ADVANTAGE-OR-BARRIER-086`: compare **minimum** interleaved-bit FBDD versus minimum native T5-symbol FBDD on the same authenticated mixed SAT/UNSAT source families after all charged source-aware reductions. Either find a genuine asymptotic advantage or a quantified all-order normal form. A fixed bad order cannot establish necessity, and the unrestricted model transfer remains OPEN. P versus NP remains OPEN.

Background: I. Wegener, *Branching Programs and Binary Decision Diagrams*, SIAM, 2000; P. Beame et al., *Lower Bounds for Exact Model Counting and Applications in Probabilistic Databases*, 2013, arXiv:1309.6815; Barto, Kozik, Niven, *The CSP Dichotomy Holds for Digraphs with No Sources and No Sinks*, SIAM J. Comput., 2009, DOI:10.1137/070708093.
