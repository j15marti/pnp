# LSPV-3/453: Charged variable elimination and treewidth

2026-11-06 08:57 PST | Route B | KNOWN THEOREM, independently derived for declared R_mix341 semantics; COMPUTATIONAL finite controls. P versus NP OPEN.

**Hypothesis:** Every UNSAT CNF F with n distinct variables actually occurring in its clauses and primal induced elimination width w has a source-authenticated paid native-RES refutation of at most n*9^w nodes. Falsifiers checked: fill-in outside induced neighborhood; more than 3^w distinct positive/negative parents; nonempty projection of UNSAT; and mistaking an upper bound for a lower bound.

**Proof.** Fix a variable elimination order sigma and form the primal graph, filling in all current neighbors of eliminated vertices. At the step for x, every clause involving x contains only x and a subset of the at most w remaining neighbors. There are at most 3^w distinct positive x-clauses and at most 3^w distinct negative x-clauses (each other variable absent, positive or negative). Each candidate resolvent comes from a paid, two-parent, pivot-oriented native RES inference, so at most 9^w charged nodes per step. Davis-Putnam elimination is existentially exact; after n steps an UNSAT input produces the empty clause. Source IDs and derivation parent references are retained, and pruning unused ancestors cannot increase the count. Thus:

$$
W_R(F)\le n\,9^{w_\sigma(F)}.
$$

Minimizing over orders yields

$$
W_R(F)\le n\,9^{\operatorname{tw}(F)}.
$$

**Corollary:** if primal treewidth is O(log N) for N encoded input bits, W_R(F) is polynomial in N. A sequence with W_R(F)=N^{omega(1)} must have primal treewidth omega(log N) along that sequence. This is a necessary structural condition, NOT sufficient hardness: expander Tseitin has efficient mixed AND3/XOR derivations despite high treewidth.

**Finite verification:** Python exhausted 2,952 CNFs containing at most 3 distinct clauses selected from the 26 nonempty proper clauses on three variables, and all 6 elimination orders, for 17,712 tested schedules. Every schedule satisfied the explicit n*9^w candidate-pair bound. An initial harness failure on isolated variables was corrected by retaining declared isolated vertices in the primal graph. All checks then passed. This finite test is not the general proof.

**Resource and model scope:** The theorem is a paid logical-node *upper* bound. An explicit proof serialization needs at most O(n*9^w*(n+log(n*9^w))) bits, plus input and source references; construction, storage, parsing, verification, failed strategies and actual peak memory must be charged separately. No FLMV same-machine contraction follows. Only the historical semantic RES rule is used; no authoritative accepted-byte checker execution is claimed. This is a standard treewidth/variable-elimination fact, not a novelty claim.

**Corpus:** Prior LSPV-3/452, LSPV-2/341 and the latest formatting handoff; project issue #3; konard/p-vs-np proof_status.json blob 93b77ed3; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea; FRAT-XOR format blob 986a21aa (previous run). Primary literature background: Davis-Putnam elimination, standard induced-width/treewidth methods, Urquhart and Ben-Sasson/Wigderson on Resolution-hard Tseitin. No new literature priority claim. Full executable Python finite check, raw results, report, handoff and SHA256 manifest in conversation ZIP.

**Next:** A noncircular lower-bound invariant that survives all native RES, AND3, XOR, LOCAL-CONVERT, DEF, shared branching and reconvergence, and grows on an established hard 3-CNF family. B3 remains OPEN. No root main.tex modification, no task/agent/schedule/weight changes.


**Encoding clarification:** Here n counts distinct *occurring* variables, not the potentially enormous numeric maximum in a sparse binary-encoded DIMACS header. Thus n<=N under an explicit clause encoding. An implementation may first compact arbitrary original variable identifiers, charging the parsing and renaming costs; no claim of a polynomial bound in a binary header's numeric maximum is made.
