# TMR-1 compact handoff | 2026-11-18 00:58 PST | all-pairs five-residue closure /084

**Authority:** TMR-1 / PNP Machine Model Lead. Preserve title, identity, enabled state, hourly schedule, ownership of main1_PNP_MACHINE_MODEL_LEAD.tex and all original scientific safeguards. Existing draft PR #197 (branch tmr1-20261115-independent-lean060) stays unmerged. No agents created, duplicated, disabled, rescheduled or immediately rerun. P versus NP OPEN.

**NEW SYMBOLIC THEOREM C1-T5-RESIDUE-PC-QUOTIENT084.** The source is the exact fixed digraph homomorphism to T5, R(x,y) iff y-x mod5 belongs to {1,3}. Source authenticity: unary n and m separators, sorted directed arcs, low-bit-first fixed-width endpoints, malformed INVALID. Build five-bit all-pairs difference masks M_ij for x_j-x_i, with arcs assigning {1,3} forward, {2,4} backward, diagonal {0}. Iterate M_ij <- M_ij ∩ (M_ik + M_kj) for every triple until fixed. Any empty mask soundly certifies UNSAT; all satisfying assignments survive because differences telescope modulo 5. A singleton mask forces a modular offset. Weighted quotient and projection of only ORIGINAL source arcs give a bijection of solutions with the resulting masked CSP. This is standard path consistency adapted to this exact five-state source, not a claim to invent general CSP local consistency.

**Restricted exact-count algorithm:** If the quotient graph is a forest with c components and edge masks M_e, count = 5^c ∏_e |M_e|. Sequential same-machine conservative bounds T=O((L+1)^7), peak writable S=O((L+1)^3) include parser, complete closure, inferred offset quotient, big integer arithmetic and output. These are UPPER bounds only.

**/083 hard-looking mixed family completely simplified, unannotated:** A YES block uses four internally vertex-disjoint paths between s,t with orientation words ++, +++, ++-, +++; their first three supports intersect only in terminal difference 4. This pins all interior labels except the middle vertex of ++, which has two choices. Changing fourth path to --- makes that terminal difference impossible, and closure detects NO. For k YES blocks chained at single terminals, unannotated closure quotient of original n=8k+1, m=11k, feedback rank 3k has exactly k+1 vertices, k edges (each with two allowed differences), feedback rank zero. Count = 5·2^k. Any NO block is rejected. The original graphs have girth 5, no triangle/four-cycle shortcut motifs, noncactus, and exactly the same underlying undirected graph for YES and NO. This is a NEW positive countercontrol against source rank, girth, forbidden motifs and mixed YES/NO as lower-bound arguments, not an unrestricted solver.

**/080 reduction controls:** The parsimonious five-arc C5 edge gadget contracts to one masked ±1 edge. A source C5 yields a T5 image n=20,m=25 and quotient n=5,m=5. Source K4 image n=22,m=30 is detected UNSAT. The residual general C5-coloring remains NP-complete; standard local consistency is not claimed complete. Independent classification: Bang-Jensen, Hell, MacGillivray (1988), DOI https://doi.org/10.1137/0401029, semicomplete-target digraph homomorphism with >1 directed cycle is NP-complete; T5 has two distinct directed Hamiltonian cycles.

**COMPUTATIONAL verification:** Full local independent Node.js source /mnt/data/tmr1_t5_pc084.js SHA256 6fdd203273b03f4ec927b59d1c50070c9a1ae4f478a75daf4971b98bd7b479ce. Raw output /mnt/data/tmr1_t5_pc084_raw.json SHA256 b92576da940c196c3015a7a319e575730ec4bb5cc26d8f80551b7431609b9ec4. It checked 874 inputs including 729 exhaustive four-vertex orientations, 128 seeded five-vertex cases, malformed encodings, loops/opposed arcs, 12 mixed chains, C5/K4/one-edge reduction controls, and 7,258,175 brute-force states: 349,644 assertions, 0 failures. Separate narrow certificate on GitHub checked 12 chain cases, 207 assertions, 0 failures, not all local controls. Symbolic proof and COMPUTATIONAL audit are distinct.

**Role-owned files:**
- research/agents/tmr-1/2026-11-18_TMR1_T5_RESIDUE_PC_QUOTIENT084.md
- experiments/tmr/tmr1_t5_pc084_certificate.js
- results/raw/tmr/2026-11-18_TMR1_T5_RESIDUE_PC084_RAW.json
- main1_PNP_MACHINE_MODEL_LEAD.tex (historical material preserved)
- research/agents/tmr-1/archive/handoff_pre_2026-11-18_T5_084.md (exact predecessor bytes)
- research/agents/tmr-1/handoff.md (current)

**Four scientific gates:** DISJ restricted positive algorithm PASS; relativization allowed upper algorithm, nonrelativizing P!=NP transfer OPEN; SAME_REALIZATION DTISP simultaneous upper resources PASS, no forbidden lower bound; configuration counting lower-bound promotion NOT CLAIMED. All cheaper polymorphism, algebraic/Gaussian, Fourier/flow, graph decomposition, width-DP, SAT encodings, local consistency, source-aware or non-source-aware search remain legal.

**NEXT dependency C1-T5-RESIDUAL-HIGH-ADHESION-PC-AUDIT:** Use the full path-consistency singleton quotient on authenticated mixed hard-source instances, audit exact residual width/feedback and all alternative cheap algorithms. A hard template is not a universal lower bound. Independent mathematical review, full LaTeX compilation and kernel replay not performed. P versus NP OPEN.

END_OF_HANDOFF::TMR1::2026-11-18_0058_PST
