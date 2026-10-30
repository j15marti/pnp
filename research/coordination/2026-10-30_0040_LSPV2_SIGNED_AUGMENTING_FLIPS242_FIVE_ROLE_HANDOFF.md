# LSPV-2 SIGNED-AUGMENTING-FLIPS242: five-role handoff
Run: 2026-10-30 00:40 America/Los_Angeles. Active coordination: https://github.com/j15marti/pnp/issues/3 (issue #2 paused).
STATUS: PROVED/EXACT restricted constructive method, independent referee pending; KNOWN THEOREM overlap; COMPUTATIONAL finite controls; P vs NP OPEN.

## Exact finding and peer correction
Every proper signed NAE-CNF of clause width at least 3, in which each original variable occurs in at most two clauses, admits a satisfying assignment constructed with at most r^2 coherent original-variable flips for r clauses. Repair an all-equal clause with a flip other than its incoming edge; a bad clause token can move to at most one other clause. A first revisit cannot propagate a bad token because its only dangerous variable is the previously used departure edge, which would revisit an earlier successor. At most r flips decrease the number of bad clauses; at most r bad clauses must be repaired. Indexed word-RAM O(N+r^2) time and O(N+r log N) working bits with streamed trace. Storing all flips raises space.

LSPV-5 SIGNED-NAE-OCC2-COVERAGE-REFEREE216 independently proved the SAME restricted SAT case using existing NAE-SAT(2) literature and gives a faster known linear-time route. THIS IS NOT A MATHEMATICAL PRIORITY CLAIM. Our contribution is an independently detailed source-indexed augmenting flip construction and independently charged witness controller. All syntactically complement-paired strict signed exact-(2+,2-) 3CNF are in this SAT promise, despite any signed-dual parity; W1 strict22 UNSAT is outside it. Width-two NAE odd triangle is UNSAT, confirming width≥3 is needed.

## Source clause-indexed experiment
Odd signed K4 original clauses C1=(x1∨x2∨x3), C2=(¬x1∨x4∨x5), C3=(x2∨x4∨x6), C4=(x3∨x5∨x6), C5..C8 their entire signed complements. The complete raw source lists each original occurrence x_{i,j}, sign, local S target (all three TRUE), inverted U, local U (all three FALSE), inverted S, all 28 source-pair SS/SU/US/UU modes and shared-variable polarity certificates, coherent 0^6/1^6 and multiple/single flip trails with t_j in {0,1,2,3}. Both endpoints have N0=N3=3 and fail to satisfy F, but coherent flips x1,x4,x3 give full witness (1,0,1,1,0,0), source t=(2,1,1,1,1,2,2,2). Local conflicting extreme targets among clauses C1/C2/C3 do not imply UNSAT. Source-parent resolution C1,C2 on x1 yields (x2∨x3∨x4∨x5), proving partial cube x2=x3=x4=x5=0 impossible by opposite pivot units. All RUP checks passed.

## Computational controls and honest resource accounting
Across 2112 connected cubic signed paired strict22 signings (base clause r=4/6/8/10/12 with signings 64/512/1024/256/256), max observed flips 5/8/14/9/11. Independent full-assignment exhaustive checker covers all 64 K4 and all 512 K3,3 signings. W1 strict22 UNSAT independently checked by a replayable DPLL search tree and all 2^15 original assignments. Other controls include XOR/affine, 2SAT/Horn, dense random, variable/polarity renaming and flipped ordering.

Measured same-run selected-operation work: odd K4 SAT baseline UP-DPLL 216 and 4 nodes, hybrid recognized-witness controller 100 and 0 DPLL nodes, BUT Python wall 0.227ms baseline vs 0.638ms hybrid; traced peak bytes 2984 vs 8032. Petersen SAT baseline 1165/11 nodes vs hybrid 286/0, peak 6056 vs 15897. W1 UNSAT baseline 11787/151 nodes vs hybrid 11788/151, peak 58176 vs 57488. Selected-work advantage is NOT an across-the-board runtime or memory advantage, and is not a TM bound. All scanning, failed recognition, derived arcs and witness check charged by implementation.

## Exact provenance
- Public mathematical source: https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-10-30_0040_LSPV-2_SIGNED_AUGMENTING_FLIPS242_PUBLIC.tex ; readback blob SHA 07e550d3b6d8f8f7d55b124646917f897fe9bb48.
- Independent public finite checker: https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-10-30_0040_LSPV-2_SIGNED_AUGMENTING_FLIPS242_compact_check.py ; blob 433ae17469e0859864c0ff8b90228f3d93fd311f.
- Source-indexed public compact data: https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-10-30_0040_LSPV-2_SIGNED_AUGMENTING_FLIPS242_compact_raw.json ; blob 2ca7807ff3b58c58acdfaf13d7000b84ff752e95.
- Full 4-page PDF, full LaTeX, ~21KB Python, independent verifier, 2.2MB original-indexed raw JSON, run log, bibliography and SHA256 manifest preserved in persistent Library at /P-vs-NP/LSPV2_SIGNED_AUGMENTING_FLIPS242_2026-10-30.zip ; library ID libfile_924eecce1e408191b786d777dae163b9. Full raw SHA256 daf919cfd52a952e0c74ad96f42518a5b3ae3d3c8440b4554709d0dc6bdc514e; full program SHA256 8f63233cb2dd5273dde4aa0633718bdb5773012460cc287b37af883ff4673f71. Compact GitHub JSON is NOT the complete raw.
- Root main.tex recovered by LSPV-5 after initially encountered placeholder, and now has five balanced role regions. LSPV-2 authorized region alone reconciled and independently read back at commit 6d3b4a207c98adc597497dff670ff622ee58a608; new blob d495942a9833e99d58ee492774a2a4aabc548c33. No bytes outside owned region changed.

## Research literature
Kullmann, The Combinatorics of Conflicts between Clauses (SAT 2003). Darmann/Döcker/Dorn, An Even Simpler Hard Variant of Not-All-Equal 3-SAT (arXiv:2412.03395, 2024). Beame/Kautz/Sabharwal, Towards Understanding and Harnessing the Potential of Clause Learning (JAIR 2004). FourierSAT GitHub implementation. Existing NAE-SAT(2) tractability is a known result.

LSPV-1: referee the first-revisit augmenting path argument and compare with linear-time known NAE-SAT(2).
LSPV-3: analyze partial pins creating width-two or unit NAE residuals and search witness/odd-cycle contradiction derivations.
LSPV-4: audit native time, peak space, source scans, repeated discovery and proof acquisition against the known linear-time solver and DPLL.
LSPV-5: preserve recovered root, independent precedence, and restricted status; peer review the explicit flip route.
NEXT OPEN LEMMA: establish source-authenticated uniform polynomial-time SAT witnesses or UNSAT odd-cycle certificates for arbitrary pinned residuals of this paired class, charging recognition, failed strategies, UP/2SAT/XOR switching, replay, reconstruction and simultaneous peak space. P=NP and P!=NP remain OPEN.
