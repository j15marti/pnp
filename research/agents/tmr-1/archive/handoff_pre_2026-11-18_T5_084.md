# TMR-1 compact handoff | 2026-11-18 00h PST | mixed girth-five path bundles /083

**Authority:** TMR-1 / PNP Machine Model Lead. Preserve this identity, title, owner, original manuscript main1_PNP_MACHINE_MODEL_LEAD.tex, enabled hourly schedule and existing research safeguards. Primary model is the exact T5-CSP with R(x,y) iff y-x mod 5 in {1,3}. Draft PR #197, branch tmr1-20261115-independent-lean060 remains open/unmerged. No agents created, disabled, rescheduled or immediately rerun. **P versus NP OPEN.**

**NEW PROVED RESTRICTED THEOREM /083, mathematical peer review OPEN.** An undirected girth-five graph obtained by joining k independent two-terminal blocks at single articulation terminals has n=8k+1 vertices, m=11k directed arcs, feedback rank rho=3k, is noncactus and contains no two- or three-edge direct shortcuts. Each block has four internally disjoint paths with signs ++, +++, ++-, and either +++ (YES) or --- (NO). The same underlying undirected graph supports both cases. All-YES chain exact homomorphism count = 5*2^k. Any NO block yields 0. This is an arbitrary-size symbolic equality and a mixed YES/NO control; no universal computational lower bound.

**Proof data:** Five-state path completion vectors by endpoint difference 0..4:
++ => [0,1,1,0,2]; +++ => [3,0,3,1,1]; ++- => [1,3,0,3,1]; --- => [3,1,1,3,0]. Pointwise products give YES transfer [0,0,0,0,2] and NO [0,0,0,0,0]. A chain of k YES blocks forces each terminal increment 4 with two independent interior completions; choose one of five initial labels. Girth five follows because every cycle traverses two paths of lengths at least 2+3 and no cycle crosses an articulation. No triangle or four-cycle means neither forced shortcut motif /082 exists. Raw feedback rank is 11k-(8k+1)+1=3k.

**Algorithm and scope:** For any supplied and verified chain of internally disjoint two-terminal directed paths, compute each path's five-state cyclic convolution, take a pointwise product inside blocks, and circularly convolve block transfers. Output 5 times the final vector sum. Polynomial bit time and space including authentication, arithmetic, output and witness reconstruction; conservative same-machine bounds T=O((L+1)^5), peak writable bits O((L+1)^3). Explicit YES/NO family source is recognized with no untrusted annotations via its canonical index/arc schema. General source remains NP-complete; tractable bounded-terminal structure is an algorithmic exception, not a lower bound.

**New independent primary-source check:** Bang-Jensen, Hell and MacGillivray (1988), *The Complexity of Colouring by Semicomplete Digraphs*, DOI https://doi.org/10.1137/0401029: semicomplete-target H-colouring is NP-complete with >1 directed cycle. T5 is a tournament with distinct +1 and +3 directed Hamiltonian cycles. This independently confirms the T5 NP-completeness classification, consistent with the project's explicit parsimonious undirected C5->directed T5 reduction. All structural restrictions and gadget identities must be understood under the exact directed beat relation.

**Executed computational checks:** Full local dependency-free Node script /mnt/data/tmr1_t5_pathbundle083.js (SHA256 98f425be1522d5cf3e785ec47d505badb432998a4e4fc2b0bd24645dcb0573f1) passed 10,290 assertions, including 3,906,250 full candidate states across 9-vertex YES and NO graphs, 50 chain instances k<=25, canonical source/witness parsers, girth and shortcut scans and mixed controls, 0 failures. Raw JSON SHA256 a71141d844b77d022d359947762e88cc1364f09d8a9d1575497a093299f6dd14. A separately executed narrower public certificate passed 717 assertions (all orientation words of length <=8, four transfer tables and all-YES chains k<=100), 0 failures. All finite checks are COMPUTATIONAL, not general proof.

**Repository artifacts (role-owned only):**
- research/agents/tmr-1/2026-11-18_TMR1_T5_GIRTH5_MIXED_PATH_BUNDLES083.md
- experiments/tmr/tmr1_t5_pathbundle083_certificate.js
- results/raw/tmr/2026-11-18_TMR1_T5_PATH_BUNDLE083_RAW.json
- main1_PNP_MACHINE_MODEL_LEAD.tex (edited in place, historical material retained)
- research/agents/tmr-1/archive/handoff_pre_2026-11-18_T5_083.md (byte-exact predecessor)
- research/agents/tmr-1/handoff.md (this file)

**Gates:** DISJ sanity PASS restricted positive countercontrol only; relativization upper algorithm PASS, unrestricted lower-bound transfer OPEN; SAME_REALIZATION DTISP PASS on charged upper-bound resources, no forbidden pair; configuration counting upper-bound safeguard only, not lower bound. All polymorphism, Fourier/flow, modular/Gaussian, local consistency, cut decomposition, alternative encodings, source-aware algorithms and unrestricted exact solvers remain legal. No repository preflight, full LaTeX compilation, kernel replay or independent mathematical peer review claimed.

**NEXT named dependency:** C1-T5-GIRTH5-MIXED-HIGH-ADHESION-AUDIT. Find or invalidate source-authenticated mixed yes/no residuals with non-bounded adhesion after all /082 forced modular shortcuts and all legal polynomial decompositions. Source complexity, hard template and high rank are not themselves an unconditional superpolynomial lower bound. **P versus NP OPEN.**

END_OF_HANDOFF::TMR1::2026-11-18_0001_PST
