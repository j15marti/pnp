# 2026-11-19: Native strict-C girth-8 minimal equality bridge and certified critical chain

Status: **PROVED for the specified native family; P vs NP remains OPEN.** Independent critical-obstruction constructor, later run.

## Recovered, independently audited seed
From the prior native 25-variable/25-clause critical strict-C fixture (seed 2026111946), clause index 10 is **C(7,20,22)**; variable 22 has degree one. Independent verification replayed the existing static 1,046-node UNSAT proof with 600 contradiction leaves, checked every original-C clause and all 25 complete physical deletion witnesses, and independently measured incidence girth 8.

Removing that clause and its unused degree-one variable gives a **24-clause, 24-variable minimal equality bridge G(7,20)** with incidence girth 8 and terminal incidence distance 6. It is SAT and forces the two terminals equal. Proof: if a G model had unequal terminals, one of the five head colors would satisfy C(7,20,22), contradicting the certified seed UNSAT result. Every other seed clause-deletion witness satisfies G minus that clause with unequal terminals. The exact original-C head-support counts, for terminal difference 0,1,2,3,4, are 0,2,1,1,2.

## Reusable theorem
If G(x,y) is satisfiable, forces x=y, and deleting each physical clause admits a model with x!=y, join k copies in a terminal chain, with disjoint fresh internal variables, and append C(t0,tk,h). This yields a **physically clause-critical UNSAT** formula. If G has p variables, q clauses, incidence girth g and terminal incidence distance d, the result has N=k(p-1)+2 variables, M=kq+1 clauses, and incidence girth at least min(g,k*d+2). Complete single-physical-clause deletion witnesses are constructed by translation of the base assignments, with a suitable private closing head. No gadget changes the original strict C predicate. This is a theorem for every k>=1, not a finite-timing inference.

For our audited G, **N=23k+2, M=24k+1, girth exactly 8**. Repeating the base bridge does **not** grow girth: intrinsic girth-8 cycles survive. This is a stronger critical easy-control family than earlier girth-4 equality chains, but NOT a growing-girth lower-bound family.

## Concrete original-C verification
k=1,2,4,16,64: (N,M)=(25,25),(48,49),(94,97),(370,385),(1474,1537). The generator checked all **2,093** deletion witnesses and **2,523,029** physical-clause evaluations. A separately written cyclic-window predicate/graph verifier independently repeated k=1,4,64 (**1,659 deletion witnesses; 2,372,403 clause evaluations**), independently reconfirmed girth 8 and no variable articulation points in those three concrete source graphs. Exact full physical JSON sources generated for k=1,4,64; reproducibility archive is attached to this research run as T5C_Critical_EqualityBridge_20261119.zip (includes both scripts, 1,046-node seed proof, SHA256 manifest and results).

## Compressed globally sound obstruction cover
For EVERY assignment to shared chain terminals z=(t0,...,tk): if a first pair t[i-1]!=t[i] exists, its equality bridge G_i is UNSAT under z; otherwise t0=tk and the closing C is UNSAT for all values of h. This is a valid **symbolic cover**, NOT an N^0.195 literal-row bound. The included deterministic one-sided exact-source recognizer compares every canonical input clause, independently replays the seed UNSAT proof and returns CERTIFIED_UNSAT, else UNKNOWN. It includes source parsing/pattern check, proof replay, verification and output, but does not solve arbitrary relabelings or arbitrary strict-C CSPs. Its implemented Python memory is O(N+M) writable objects, not the target N^0.5 polylog. A noncanonical mutated input was correctly rejected as UNKNOWN.

## Growing-girth connection and unresolved obligation
Erdos's high-girth high-chromatic existence theorem supplies 6-edge-critical graphs of arbitrarily high girth after edge-minimalization. One independent-head original C(u,v,h_e) per graph edge encodes the u!=v constraint; graph edge deletion yields original-C deletion witnesses. This yields *nonconstructive* critical strict-C instances of arbitrarily high incidence girth, and corresponding high-girth minimal equality bridges, but no efficient generator or unrestricted lower bound.

OPEN: obtain a physically clause-critical girth-10 core with static UNSAT proof and all deletion witnesses from the known 150-variable/176-clause girth-10 source; do not conflate prior exhaustive-solver classification with an external static certificate. No P vs NP conclusion follows.

Literature: P. Erdos (1959), Graph theory and probability, Canadian J Math 11, 34-38; G. Exoo & J. Goedgebeur (2019), DMTCS 21(3), https://doi.org/10.23638/DMTCS-21-3-9; J. Goedgebeur (2020), J Graph Theory 93, 34-48, https://doi.org/10.1002/jgt.22467.
