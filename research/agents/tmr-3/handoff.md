# TMR-3/098 NEW HANDOFF (2026-11-18 PST)

Owner: TMR-3 / PNP Time-Space Tradeoffs. Identity, title, disabled/enabled setting, ownership, scheduling and historical safeguards were NOT altered.

**PROVED:** If a compiled CSP support graph H retains Q_d as an explicitly witnessed minor with disjoint connected branch sets, and can be separated into shared S plus private Y_i of size B<v with no private-to-private support edges, then |S|>=v(d-log2 B)/(2d-log2 B), where v=2^d. If compiled L=v^(gamma+o(1)) and B<=L^0.35, fixed gamma<20/7 implies a linear-in-v separator. Thus a minor-preserving compiler with s=o(v) must incur L>=v^(20/7-o(1)). This does NOT constrain minor-destroying semantic compilers or prove computational hardness.

**PROVED (restricted oracle model):** The deterministic decision-tree complexity of OR_R AND_M over independent Boolean child truth values is RM. A free negative index for each of R rows allows R negative responses, but routing acquisition and actual negative certification are essential. On explicit easy block formulas, the huge literal index table compresses to a short prefix function. No oracle-to-unrestricted-execution transfer established.

**KNOWN published exclusion:** Buss-Williams 2015 excludes uniform deterministic SAT/UNSAT on their random-access model at (time N^1.34070, space N^0.5), with o(1) exponent slack. Diehl-van Melkebeek-Williams 2011 only gives some epsilon(d)>0 for nondeterministic TAUTOLOGIES when d<4^(1/3), not epsilon=0.5. Under s=O(1) and total blocks N^.65, target 1.33 requires child exponent alpha<=1.942857; with N^.195 rows each carrying N^.65 blocks, alpha<=1.385714. Child space exponent beta<=10/7. R=N^.195 rows cannot be equated with 2^s shared assignments. All child polarity, caching, transformation source-bit generation, replay and final witness/original-input verification must be charged.

**COMPUTATIONAL:** 77,845 primary assertions, 1,436 independent checks, no failures, identical repeated main audit. Easy T5 hypercube with x_u=popcount(u) mod 5 falsifies any separator-to-necessary-witness-work leap. Standalone details: research/agents/tmr-3/2026-11-18_TMR3_MINOR_COMPILER098.md. Full local reproducibility bundle: TMR3_MINOR_COMPILER098_Reproducible.zip. Full combined manuscript compilation, native TM execution, human independent audit OPEN.

**Gates:** DISJ/quantifiers PASS restricted; oracle transfer NO; SAME-MACHINE PASS for published general-SAT exclusion and constructive ledgers only; EASY CONTROLS refute representation hardness leap. P versus NP OPEN.

**Next blocker:** C3-BLOCK-CHOICE-MINOR-DESTROYING099. Find a genuinely semantic, paid, source-virtualized compiler on NP-hard examples that destroys the Q_d minor while preserving the exact SAT/UNSAT and output guarantees, or prove a wider barrier.

END_OF_HANDOFF::TMR3::2026-11-18_098_PST

---

## TMR-3/097 CURRENT HANDOFF: Explicit source-partition obstruction (2026-11-18 PST)

**PROVED:** For unchanged CNF clauses with primal Q_d on v=2^d vertices, shared interface s and private blocks Y_i each of size <=B<v, no cross-private clause, necessarily
s >= v(d-log2 B)/(2d-log2 B). At B<=v^.35, s>=13v/33, incompatible with all-CNF literal-preserving compilation to s<=N^.195 and local size N^.35 for ordinary explicit source length N=Theta(v log^2v). **CAVEAT:** syntax/interface barrier ONLY. Arbitrary equisatisfiable preprocessing, auxiliary variables and algebraic solutions remain possible. The monotone 2-CNF cube and easy T5 cube prove no computational lower bound is implied.

**T5 COUNTERCONTROL:** Orient each cube arc from lower to higher Hamming weight. x_u=popcount(u) mod 5 is a polynomial-time output witness with color differences +1. At Q_8 v=256,B=6, interface s>=104 despite trivial witness construction. Five rotations.

**ROLE RECURRENCE:** For exact factor F=AND_i B_i(z,y_i) with disjoint private Y_i, SAT iff exists z forall i exists y_i; UNSAT iff forall z exists i forall y_i not B_i. Every tested local child of actual polarity, failed attempt, preprocessing, source bit, address, complete SAT witness replay, output and peak live workspace are charged. A free correct negative i(z) is neither uniform discovery nor an UNSAT certificate. A k-bit descriptor is only a sound certificate if EVERY wrong path rejects and Eval(descriptor,z) plus ALL child negative checks are paid. Adaptive forall z exists i strategy is not a single existential path. For M<=N^.65 total, local N^.35 and seed ell^alpha, direct enumeration costs 2^s N^(.65+.35alpha+o(1)); when s=N^.195 it is superpolynomial without separately proved compression.

**SOURCED EXCLUSION:** Buss-Williams (2015) Fig 8.2 gives SAT not in DTISP(N^1.34070,N^.5) on its specific random-access model, excluding an ALL-CNF uniform deterministic N^1.33+o(1)/N^.5 polylog solver there, but not a stronger unit-cost RAM or restricted promise without model/reduction transfer. Nondeterministic TAUT: Diehl et al. (2011), d<cube-root(4), SOME epsilon(d)>0, not necessarily .5. Unrestricted short UNSAT certificates imply NP=coNP (open).

**COMPUTATIONAL:** 66,974 assertions and 0 failures. Exhausted 65,808 cube subset inequalities; 9 exact small-cube separators; 480 factored CNFs (301 SAT,179 UNSAT) with full Boolean controls; 180 wrong path rejections; T5 Hamming witnesses. Independent code-path audit reproduced 4 minimum separators and 4 T5 cubes. The main audit repeated byte-identically. Not human mathematical review.

**REPO:** `research/agents/tmr-3/2026-11-18_TMR3_BLOCK_SEPARATOR097.md`, `results/raw/tmr/2026-11-18_TMR3_BLOCK_SEPARATOR097_AUDIT.json`, `experiments/tmr/tmr3_block_separator097_independent.py`, appended section 097 in `main3_PNP_TIME_SPACE_TRADEOFFS.tex`. Full 66,974-check script and detailed theorem in reproducibility ZIP. Old text preserved. No merge or independent validation claimed.

**GATES:** authenticated DISJ PASS; relativization separation OPEN; same-machine published FULL-SAT exclusion PASS, restricted transfer OPEN; representation-to-runtime FALSIFIED by easy T5 controls. Native Turing machine, combined LaTeX build, and peer audit OPEN. **NEXT: C3-BLOCK-CHOICE-SEMANTIC-COMPILER098**, charged semantic rewriting with variable-copy consistency, reductions, and joint workspace. P versus NP OPEN.

END_OF_HANDOFF::TMR3::2026-11-18_1928_PST

## TMR-3/096 CURRENT HANDOFF: Exact dual-polarity blocks and RAM forbidden point (2026-11-18 PST)

Status: **PROVED/EXACT** (conjunctive factored-CNF quantifier identity and weighted SAME-realization recurrence); **KNOWN THEOREM** (Buss--Williams, Fig. 8.2, SAT not in DTISP(N^1.34070,N^0.5)); **FALSIFIED as an all-CNF resource claim** (uniform deterministic N^1.33+o(1) time and N^.5 polylog space cannot decide arbitrary CNF); **COMPUTATIONAL** (1,351 passed assertions, 1,320 random authentic factored formulas, T5 pin easy controls); **OPEN** (source-authenticated general-CNF compiler, unrestricted P vs NP separation, independent peer audit).

For F(z,y)=AND_i B_i(z,y_i) with disjoint private Y_i: SAT iff exists z all children SAT; UNSAT iff for all z exists a genuinely refuted child. A correct index per z is an **adaptive strategy**, not free advice, and arbitrary factorization with shared private variables or disjunctive rows invalidates naive transfer. The actual cost counts every tested child of both polarities, failed attempts, source authentication, replay for complete SAT witness, and writable-space peaks on one execution.

Published exclusion: https://doi.org/10.1007/s00037-015-0104-9 (journal Figs 8.2--8.3, c=1.34070, epsilon=.5), not just earlier 1.32/.5 Williams bound. Nondeterministic UNSAT/TAUT: https://doi.org/10.1007/s10878-009-9286-x excludes time exponent d<cube-root(4) with SOME positive space exponent e, not necessarily e=.5. Read-only correct-path tape is not a free writable low-space RAM certificate. SAT nondeterministic witnesses are easy to check; polynomially checkable complete UNSAT paths for all CNFs would imply NP=coNP.

Artifacts in this branch: research/agents/tmr-3/2026-11-18_TMR3_BLOCK_CHOICE096.md; results/raw/tmr/2026-11-18_TMR3_BLOCK_CHOICE096_AUDIT.json; living main3_PNP_TIME_SPACE_TRADEOFFS.tex section 096. Complete Python executable and two identical audit outputs in the per-run TMR3_BLOCK_CHOICE096_Reproducible.zip. Existing five titles/identities/schedules/enabled states unchanged, no main merge claimed. Four gates: DISJ PASS conditional on authentication; relativization OPEN for separation; DTISP PASS for the published full-CNF no-go/OPEN for compiler transfer; configuration-count lower-bound transfer NOT APPLICABLE. /341 FAIL, /386 RESTRICTED.

**Next:** C3-BLOCK-CHOICE-COMPILER097. Construct or falsify a fully source-authenticating arbitrary-CNF-to-private-block compiler with exact quantifiers and total costs; show the specific failed arrow rather than contradicting the published 1.34070/.5 theorem. P versus NP OPEN.

---

# TMR-3/095 handoff | 2026-11-18 | Intrinsic physical-critical SAT witnesses

**Identity/config:** TMR-3 / PNP Time-Space Tradeoffs. Preserve existing title, owner, manuscript, Pacific hourly schedule, enabled/paused status, and four verification gates. This branch builds on unmerged /094 PR #309. Do not activate or modify the automation state.

**PROVED:** Any connected n-vertex T5 source has a rooted exact SAT witness enumeration of at most 2^(n-1) binary spanning-tree choices. For promised physical-arc-minimal UNSAT (H,e), degree-two branch-core suppression yields an exact minimum-product spanning-tree search of at most W=prod_{uv in T}|S_uv| <=4^(b-1) terminal assignments. Choose min{2^(n'-1),W}. Pair supports intersect retained private threads; omit the entire support of the path containing e; extend every remaining path by five-state DP; verify the entire original H-e. No promise membership oracle or witness advice is charged as free.

**FALSIFIED proposed shortcut:** A modular cycle of exact +1 T5 triangle pins is gadget-level minimally inconsistent when k mod5 !=0, but is NOT physically edge-minimal UNSAT. Removing a direct module arc gives endpoint support {1,2,4}, removing either side arc gives {1,3}; the two types cannot both accommodate the necessary discrepancy 1-k mod5. Verified k=3..9, all 126 individual arc deletions. In particular k=3 has only 6/9 SAT deletions; k=6 has 0/18.

**COMPUTATIONAL:** 19,683 K3,3 edge states audited; 216 labeled fully-supported critical obstructions; all 1,512 deletion witnesses checked. Separate exact five-bit-domain AC-3/backtracking solver shrank random 4-regular sources and independently verified all 145 deletions from 12 critical b=3..6 samples. Exhausted all 512 subsets of the nine short-thread relations, max irredundant size 4. Zero observed failures; deterministic audit repeated byte-identically. External handoff ZIP not mounted, but short-path facts independently reconstructed.

**Resource firewall:** conservative simultaneous random-access upper T=O((N+1)^4(1+Q)), S=O((N+1)^2) bits; direct sequential tape upper T=O((N+1)^8(1+Q)), S=O((N+1)^3), where Q=min{2^(n'-1),W} and N is full bit input length. Charge input, access, extension, candidate enumeration, output, verifier, caching and machine addresses. Native tape experiments and mathematical peer review outstanding. Only unconditional general lower bound here is Omega(n') from explicit witness output. FLMV is for language decision and does NOT automatically transfer to guaranteed SAT-only critical-deletion witness search. Do not conflate branch/interface representation rank with unrestricted T/S lower bounds.

**Four gates:** DISJ restricted positive exact algorithms; relativization no separation; simultaneous DTISP upper only / lower OPEN; configuration counting no unrestricted lower conclusion. Easy sources and legal algebraic/combinatorial shortcuts preserved.

**ONE NEXT DEPENDENCY:** C3-T5-PHYSICAL-CRITICAL-TRANSFER096. Prove or falsify a uniform intrinsically physical-arc-critical high-girth generator with correct YES-only witness quantifiers; attempt stronger cycle-space, binary-tree, treewidth, algebraic, and source-encoded solver upper bounds first. P versus NP OPEN.

**Files:** research/agents/tmr-3/2026-11-18_TMR3_T5_WEIGHTED_CRITICAL095.md; experiments/tmr/tmr3_t5_weighted095_smoke.py; results/raw/tmr/2026-11-18_TMR3_T5_WEIGHTED_CORE095_AUDIT.json; main3_PNP_TIME_SPACE_TRADEOFFS.tex (new /095 section appended; all earlier sections retained).

---
## Historical handoff (verbatim, preserved below)

# TMR-3/094 handoff | 2026-11-18 | SAT-only intrinsic-critical T5 witness and DTISP transfer firewall

**Identity/configuration retained:** TMR-3 / PNP Time-Space Tradeoffs; existing title, ownership, enabled/paused status, Pacific hourly schedule and four safeguards unchanged. Branch /094 stacks on draft PR #306 (/093), unmerged. New user directive 2026-11-18 supersedes previous /093 nonlinear-interface priority. The purpose is SAT witness finding for a designated deletion G=H-e of a connected edge-minimal T5 UNSAT source H, with no free coNP promise certificate.

**PROVED/EXACT upper-bound mechanism:** Suppress degree-two threads of the original critical H, record exact GF(5) endpoint constraints D(L,f)={2L-f+2j mod5:0<=j<=L}. Criticality forces L<=3. Omit the whole constraint for the one thread containing deleted e (free-ended halves), enumerate at most 5^(b-1) branch assignments after rotation and reconstruct/verify all original-vertex colors. Same-run conservative random-access T=O((N+1)^4(1+5^(b-1))), S=O((N+1)^2) bits, sequential-tape T=O((N+1)^8(1+5^(b-1))), S=O((N+1)^3). All include access, decomposition, failed candidates and complete output. OPEN: any unrestricted lower bound.

**Sharper high-girth structural bound:** Girth(H)>=7 makes the suppressed branching graph simple, since each critical thread has <=3 arcs. n<=b^2, beta>=b/2+1>=sqrt(n)/2+1 after discarding isolates. These improve handed-off constants but are NOT machine-work lower bounds. The external branch-core ZIP and theorem path were unavailable in the live filesystem; the nine short-thread relations and max irredundancy four were independently reconstructed and enumerated. Original Moore arithmetic not fully re-audited.

**PROVED/EXACT pin compiler:** One fresh-vertex triangle u->v,u->w,w->v forces x_v-x_u=1 and x_w-x_u=3 uniquely. Polynomially many exact gadgets support search-to-*ordinary* T5 decision with <=1+5(n-1) queries. This does NOT provide a SAT-only promise oracle because intermediate queries may be UNSAT/off promise.

**PROVED implication (transfer barrier):** A polynomial-time all-outcome reduction from SAT formulas to valid promised critical-deletion pairs, together with a polynomial-time decoder correct on EVERY resulting witness, implies NP=coNP by certifying UNSAT with that witness. Therefore ordinary FLMV/Williams SAT decision bounds, including c<2cos(pi/7) with n^{o(1)} space, cannot be transferred to this promised search without a new correctly quantified reduction and a charged random-access source generator. Source materialization typically destroys the subpolynomial-space premise.

**PROVED nonconstructive existence:** Erdős high-girth chromatic >=6 graphs, oriented arbitrarily and edge-minimized, yield connected, 2-vertex-connected T5-critical UNSAT obstructions of unbounded girth. Neither efficient generation nor witness-search hardness follows.

**COMPUTATIONAL controls:** 512 relation subfamilies, 512 K3,3 full orientations (336 UNSAT, 0 fully edge critical), 19,683 partial oriented K3,3 graphs (288 critical), 250 seeded tree-edge exact checks, 60 exact gadget pins, 50 witness-from-decision trials/321 queries, 234 branch-core actual full witnesses. Zero failures. A 5-vertex 6-arc critical theta source has deletion rooted counts [8,2,2,8,2,2]. GitHub compact smoke source, fuller locally executed Python audit scripts and local ZIP are distinguished. Native TM execution/full combined LaTeX build/peer review unexecuted.

**Gates:** DISJ restricted PASS, relativization no separation, simultaneous DTISP restricted upper PASS/lower OPEN, configuration-count no time necessity. Easy families, Fourier/primal/dual/affine/DP alternatives and source-authentication costs remain admissible.

**Owned files:** main3_PNP_TIME_SPACE_TRADEOFFS.tex updated in place; research/agents/tmr-3/2026-11-18_TMR3_T5_CRITICAL_WITNESS094.md; experiments/tmr/tmr3_t5_critical_witness094_repo.py; results/raw/tmr/2026-11-18_TMR3_T5_CRITICAL_WITNESS094_AUDIT.json; previous sections preserved.

**NEXT: C3-T5-INTRINSIC-PROMISE-LOWER-BOUND095.** Construct a uniform genuinely intrinsic-critical family and prove a same-realization dynamic obstruction to ALL legal SAT witness-finders, or supply a valid noncollapsed reduction bridge with full source-access costs. Both OPEN. **P versus NP OPEN.**

---

# TMR-3/093 handoff | 2026-11-18 | exact sharp T5 connection rank

**Identity/title/ownership/enabled state/hourly schedule preserved.** The /093 branch is stacked on /092 and does not merge either PR. Earlier handoff is retained below.

**New theorem:** For q labeled terminals, full original-source T5 exact-count gluing connection matrix has rank precisely 5^(q-1) over Q. The exact private triangle with u->v, u->w, w->v forces x_v=x_u+1 mod 5 with one extension; composing at most five triangles for each relative coordinate generates 5^(q-1) boundary-delta sources, yielding a 5I connection submatrix. This lower bounds only the coordinate dimension of universal linear plus bilinear gluing interfaces, NOT any general algorithm's time or workspace.

**Critical same-machine counterexample:** Graphs made of these authenticated private increment triangles are solved by modular-potential graph traversal in polynomial time, exact count 5^c if consistent and 0 otherwise, with full source authentication. The q=40 example has 430 vertices, 694 arcs, exact count 5, although the universal q-terminal rank is 1,818,989,403,545,856,475,830,078,125. Every B_alpha union B_beta has treewidth at most two. Deliberately loose conservative simultaneous deterministic sequential-tape bounds are T(N)=O((N+1)^8), S_peak(N)=O((N+1)^3) bits for recognized instances; unrecognized input uses exact exponential original-arc fallback. Representation rank cannot be used as a DTISP lower bound.

**Executed local test:** 622 deterministic assertions, zero failures, identical repeat execution; full source reference Python SHA256 e1324d9d3e4b066cd3c8c38151a4d33cfb1ca2e54e0b8cce2f041d715c30d669; audit SHA256 f220045551bce86122226ad9a87b4786729d1eb321f40d5f4cc87bbaa377b85f. Includes original-input backtracking and 5^n brute checks on easy and contradictory controls. Finite evidence is COMPUTATIONAL.

**Gates:** DISJ restricted constructive PASS; relativization not applicable to a separation; SAME_REALIZATION restricted upper bound PASS, lower bound OPEN; configuration counting rank restricted to linear bilinear representation, no machine work inference. Preserve all preceding source checks and easy family controls.

**Next:** C3-T5-NONLINEAR-CONNECTION094: test nonlinear compression on high-adhesion authenticated sources and separate interface-rank results from genuine time-space obstructions. General T5 NP-complete by Bang-Jensen, Hell, MacGillivray (1988), but no SAT exponent transfers without exact reduction. P versus NP OPEN.

---

# TMR-3/092 handoff | 2026-11-18 | exact three-terminal T5 transfer

**Identity and schedule retained:** TMR-3 / PNP Time-Space Tradeoffs. Existing title, enabled state, manuscript ownership, hourly America/Los_Angeles schedule, history and four safeguards unchanged. Draft PR stacked on /091, do not merge automatically. Earlier handoff sections remain below.

**C3-T5-3CONNECTED-RESIDUAL092, PROVED restricted constructive theorem; independent review outstanding.** If k source modules have exactly three common terminals and no other cross edges, the unpinned exact count is 5 times the sum, over 25 relative terminal-color pairs, of the product of exact module count-vectors. For an all-forward K(p,p) module with three left terminals, exactly seven of 25 vector entries are nonzero: F(0,0)=2^p+2^(p-2)-2, and six entries of value 2^(p-3). Consequently k such modules, identified along exactly three terminals, have exact count 5[(2^p+2^(p-2)-2)^k+6(2^(p-3))^k].

**New unbounded-connectivity extension:** for k>=2 and 1<=q<p common left terminals, the family of k all-forward K(p,p) modules has kappa=q, treewidth>=p, min degree p, missing complement cover k(p-q), and exact Z=5[(2^p+2^(p-q+1)-2)^k+(2^q-2)(2^(p-q))^k]. This holds for q increasing with n: with q=floor(p/2), k=p all four structural parameters diverge but source-authenticated counting is polynomial time. The 5^(q-1)-entry generic interface collapses to two exact count-orbits for this family; no exponential table is necessary. Additional standalone Python test script verified 89 checks and zero failures for q=1..5 plus high-connectivity q=50. This supersedes merely seeking 4-connected sources as hardness evidence.

**New authenticated infinite family:** k>=2,p>=4, n=3+k(2p-3), m=kp^2, vertex connectivity exactly 3, minimum degree p, treewidth >=p, global missing-edge cover k(p-3). Source recognition and closed-form counting are polynomial even though all these parameters grow. At (k,p)=(20,8), n=263, m=1280, cover=100, exact 51-digit Z=559129496820275798186261882797788214499516649308160. No one-vertex or two-vertex cut exists. This is a counterexample to using 3-connectivity/high width/global complement cover as a stand-alone necessary-work claim.

**Same realization:** for authenticated members, a single deterministic sequential-tape algorithm charges input scanning, unique terminal discovery, induced block recognition, 5-state algebra, exact big-integer output, addresses, head movements and workspace. Conservative simultaneous T(N)=O((N+1)^12), peak S(N)=O((N+1)^4) bits. Arbitrary unrecognized inputs require exact exponential fallback. No quantitative sparse-SAT exponent was transferred.

**Computational checks:** locally executed full standard-library reference: 861 deterministic checks, 0 failures, byte-identical rerun. Independent compact repo implementation: 14 checks, 0 failures. Full reference includes original-vertex propagation/backtracking for three small families, 256 exhaustive pattern controls, all 25 local residues for p=3 through 7, deletion-of-1/2-vertex 3-connectivity tests, relabeling and mutation controls. Full native TM, integrated manuscript compilation and independent proof review outstanding. Computation does not prove a lower bound.

**Four gates:** DISJ restricted constructive PASS; relativization non-separation; SAME_REALIZATION DTISP restricted simultaneous upper only; configuration counting upper-bound consistency, no necessary-work inference. Easy controls remain admitted: loops, opposed arcs, trees, cycles, chromatic UNSAT, path and affine propagation, primal/dual/Fourier/treewidth, signature/near-biclique, block-cut, two-terminal, padding and generic backtracking. General T5 NP-complete via Bang-Jensen, Hell and MacGillivray (1988), DOI 10.1137/0401029, with no exact blowup transferred here. P versus NP OPEN.

**New artifacts:** experiments/tmr/tmr3_t5_q_terminal092_repo.py (unbounded-connectivity extension);  research/agents/tmr-3/2026-11-18_1327_TMR3_T5_THREE_TERMINAL092.md; experiments/tmr/tmr3_t5_three_terminal092_repo.py; results/raw/tmr/2026-11-18_TMR3_T5_THREE_TERMINAL092_AUDIT.json; appended main3_PNP_TIME_SPACE_TRADEOFFS.tex; this preserved handoff.

**Next load-bearing dependency:** C3-T5-UNBOUNDED-ADHESION093: test instances not defeated by growing-separator decompositions or small modular color-orbits, benchmark all lawful exact algorithms, and quantify any alleged necessary resource on one source-authenticated machine.

---

# TMR-3/091 handoff | 2026-11-18 12:24 PST | exact T5 two-terminal interfaces

**Ownership and scheduled agent unchanged:** TMR-3 / PNP Time-Space Tradeoffs, five-symbol Z5 offsets {1,3}; title, enabled state, hourly schedule and four verification gates preserved. Draft PR stacked on /090, do not merge automatically. Prior handoff remains below.

**Concrete theorem:** for a two-terminal directed H, define F_H(d)=# original-vertex T5 assignments given terminal colors (0,d). Translation invariance gives pointwise multiplication for parallel gluing and Z5 convolution for series gluing. For modules sharing ONLY terminals s,t: Z=5 sum_d prod_i F_i(d). Independent exact counting, no free preprocessing oracle.

**New explicit falsifier:** all-forward Kp,p has F_p=(3*2^(p-1)-2,0,2^(p-2),2^(p-2),0). For k>=2,p>=3, glue k modules on the SAME two left terminals. The source is 2-vertex-connected with min degree p, n=2+k(2p-2), m=kp^2, treewidth >=p, global missing-edge cover k(p-2), yet Z=5[(3*2^(p-1)-2)^k+2(2^(p-2))^k]. The missing-edge cover equality has an explicit cyclic cross-module matching certificate. k=20,p=8: n=282,m=1280,tau=120, count 21889571624213873501580872626770891539924037418352640.

**Simultaneous one-tape upper bounds (restricted, source-authenticated):** T(N)=O((N+1)^8), peak S(N)=O((N+1)^3) bits including source access, decomposition checking, states, addresses, arithmetic, head motion and output. Unrecognized cases retain exact 5^n polynomial-space enumeration. Do not confuse five-entry interface space with a lower bound, or import a quantified SAT exponent without exact reduction blowup.

**Actual finite evidence:** /mnt/data full reference executed twice, 997 deterministic assertions, zero failures and identical SHA256 audit 8c5841d1655b00f7faffb915dd2e81a8f21125645f11aad7762b03564b17bb69. The compact repository implementation separately executed 35 checks without failure. A standalone two-page LaTeX section compiled. Full combined-manuscript compilation, native TM microcode and independent mathematical review remain pending. Source report and manuscript updated without deleting history.

**Four verification gates:** DISJ restricted constructive PASS. Relativization NOT APPLICABLE TO SEPARATION. SAME_REALIZATION DTISP restricted upper-bound PASS (no lower bound). Configuration counting UPPER-BOUND CONSISTENCY ONLY. All easy-family controls and all legitimate primal/dual/Fourier/affine algorithms remain admissible; finite evidence COMPUTATIONAL, P versus NP OPEN.

**Next load-bearing dependency:** C3-T5-3CONNECTED-RESIDUAL092. Test authentic 3-connected SAT/UNSAT families resistant to 1- and 2-separators, affine path, signature quotient, Fourier/dual and primal exact algorithms. Any proposed lower-bound obstruction must survive a same-realization solver comparison.

END_OF_HANDOFF::TMR3::2026-11-18_1224_PST

---

# TMR-3/090 handoff | 2026-11-18 | exact T5 block-cut factorization

**Role and configuration preserved:** TMR-3 / PNP Time-Space Tradeoffs; alphabet Z5, beat offsets {1,3}; existing title, identity, ownership, enabled state, hourly schedule, safeguards and prior manuscripts unchanged. PR is a stacked unmerged draft.

**Closed C3-T5-BICLIQUE-MODULE090:** Proved exact connected-source biconnected block factorization Z(G)=5 product_B(Z(B)/5) from cyclic translation symmetry. This removes the need for a potentially exponential articulation-interface enumeration on ordinary unpinned T5 graphs. For each bipartite source-derived edge-block B, use /089 exact complement-cover counting with local minimum missing-edge cover tau_B. Conservative **same-realization** bounds: T(N)=O((N+1)^16[1+sum_B 5^tau_B]), S_peak(N)=O((N+1)^6) bits. A second weighted per-vertex support lift supports five-entry articulation messages if external unary pins break translation invariance. Nonbipartite blocks admit blockwise 5^|B| exact fallback. No lower bound.

**Falsifier:** Chain of k>=3 genuinely biconnected all-forward K_{p,p}-one-hole modules, with one vertex shared between successive modules. n=k(2p-1)+1, m=k(p²-1), each tau_B=1, global complement tau=k(p-1)+1, tw>=p-1, exact count 5*(2^(p+1))^k. At k=20,p=8: n=301, m=1260, 20 blocks, global tau=141, exact count 7662477704329444291791735135751545918093695610918010880 (55 digits). Hence representation/global-cover lower-bound arguments are unsound absent full algorithm quantification.

**Verification:** Full stand-alone reference 1,052 seeded deterministic assertions, zero failures, twice identically, SHA256 fd307160182a7c861086f73384cebceee1499f889a6b6bf85b1488976769324b. Compact composition 224 further checks against independent local brute-force /089-interface stand-in, zero failures twice; integrated run against actual /089 checkout still pending. Standalone 2-page LaTeX section compiled; combined manuscript compile, native Turing-machine implementation and independent mathematical review pending.

**Four gates:** DISJ PASS restricted constructive, relativization NOT APPLICABLE TO A SEPARATION, SAME_REALIZATION DTISP PASS symbolic upper bound only, configuration counting UPPER-BOUND CONSISTENCY. Preserve all prior easy-family, affine, rank, dual Fourier, treewidth, path saturation, pruning, full graph access, caching and recomputation controls. NP-completeness of unrestricted T5 sourced to Bang-Jensen, Hell, MacGillivray (1988), DOI 10.1137/0401029; no quantitative SAT lower bound transported. P versus NP OPEN.

**Published files on current branch:**
- research/agents/tmr-3/2026-11-18_1121_TMR3_T5_BLOCK_CUT_FACTOR090.md
- experiments/tmr/tmr3_t5_block_product090_repo.py
- results/raw/tmr/2026-11-18_TMR3_T5_BLOCK_FACTOR090_AUDIT.json
- main3_PNP_TIME_SPACE_TRADEOFFS.tex (new /090 section appended; all historical sections preserved)
- research/agents/tmr-3/handoff.md (this handoff, previous history below)

**Next dependency:** C3-T5-2CONNECTED-RESIDUAL091. Seek difficult source-authenticated 2-vertex-connected residuals resisting path/affine, signature, missing-edge cover, primal/dual/Fourier and symmetry reductions; charge true same-machine time and space without assuming a representation width gives a lower bound.

---

# TMR-3/089 handoff | 2026-11-18 10:24 PST | complement-cover exact T5 counting

**Owner/state preserved:** TMR-3 / PNP Time-Space Tradeoffs; five-symbol beat relation \(R(x,y)\iff y-x\in\{1,3\}\bmod5\); agent identity/title/enabled state/hourly schedule/ownership/safeguards unchanged.

**Closed C3-T5-SIGNATURE-PERTURB089:** For connected bipartite source \(G=(U,V,E)\), form the source-authenticated bipartite complement \(H\) on missing U-V cross pairs. Let \(\tau\) be its minimum vertex-cover size, computed exactly by maximum matching and Kőnig alternating reachability. Pin the \(\tau\) cover vertices (at most \(5^\tau\) assignments). Remaining residual is genuinely complete bipartite, with exact unary domains from pinned arcs. /088 two-signature-class support counting generalizes using vertex-specific onto counts \(H_A(S)=\sum_{Q\subset S}(-1)^{|S|-|Q|}\prod_{v\in A}|D_v\cap Q|\); at most 225 support tuples per pinned coloring. This yields exact count for **every bipartite underlying source** with one symbolic simultaneous sequential-tape upper bound \(T=O((N+1)^{12}(1+5^\tau))\), \(S=O((N+1)^4)\) bits. \(\tau\le h\), the number of missing cross pairs. On nonbipartite sources exact \(5^n\) fallback.

**Falsifier:** all-forward \(K_{2,2}\) has 30 original colorings; deleting one arc yields a tree with 40. Same-colored left vertices can have different INCOMPLETE signatures, so raw signatures with a missing-edge marker do not justify /088 injection. Conditioning before signatures repairs the proof. Large SAT control: all-forward \(K_{120,121}\) minus 60 edges all incident to one left vertex has 241 vertices, 14460 arcs, \(h=60,\tau=1\) and 38-digit exact count \(19938419936773738105086320950273638380\).

**Actual evidence:** full reference 2176 deterministic assertions with 0 failures (including independent 5^n enumeration, 596 exact cover-size checks), byte-identical repeated audit; separately authored compact executable 453 independent comparisons, 0 failures and identical repeat. Local source SHA256 full: 35ad570fcc55ff30090d92855dfd5b29cdbe25170eb01f8cfc17570ca12dd748; compact: 9e476b59df02c6755b5a5c504485a9752aecfcadb396c99ae186c7431a554cbf. Full script, repo script, report, LaTeX standalone and raw audit provided in reproducibility package. Published compact script: experiments/tmr/tmr3_t5_perturb089_repo.py; report: research/agents/tmr-3/2026-11-18_1024_TMR3_T5_COMPLEMENT_COVER089.md; raw audit: results/raw/tmr/2026-11-18_TMR3_T5_COMPLEMENT_COVER089_AUDIT.json. Existing owned main3 manuscript appended and historical handoff preserved.

**Gates:** DISJ PASS restricted upper; relativization NOT APPLICABLE to nonseparation; simultaneous DTISP PASS restricted symbolic single-realization upper with complete charging, no lower-bound conclusion; configuration counting upper consistency only. No arbitrary-source lower bound or P versus NP proof. Native one-tape microcode, full combined LaTeX compile and independent math review unexecuted.

**ONE next load-bearing dependency:** C3-T5-BICLIQUE-MODULE090. Try source-authenticated glue of several near-complete bipartite blocks and correct boundary support functions, with matching, decomposition and interface search fully charged. Test families with globally large complement cover but small boundary versus high-overlap obstruction controls. Preserve easy-family SAT/UNSAT, affine, path, treewidth, signature, Fourier, alternate spanning forest, caching, recomputation and padding controls.

P versus NP OPEN.

---

# TMR-3/088 compact handoff | 2026-11-18 09:27 PST | signature-quotient Kpq exact counting

**Role/state unchanged:** TMR-3 / PNP Time-Space Tradeoffs; 5-symbol beat relation R(x,y) iff y-x in {1,3} mod 5; same title, ownership, enabled state, hourly schedule, safeguards. P versus NP OPEN.

**Closed dependency C3-T5-CRITICAL-CORE088:** All simple connected oriented complete bipartite source graphs have polynomial-time exact T5 counting, despite unbounded treewidth and no degree-2 interior paths. Let a,b be counts of distinct orientation signatures on each side. If a+b>5, UNSAT by necessary distinct-color injection of signature representatives; otherwise min(a,b)<=2. Each selected signature class can use at most two colors, so support tuples enumerate at most 15^2/5=45 cyclic-translation orbits. Exact counts include all original labeled vertices via h_m({x})=1 and h_m({x,y})=2^m-2 and per-opposite-vertex admissible choice counts. No false general-hardness claim.

**Two controls:** all-forward Kpq has Z=5(2^p+2^q-2); at K1000,1000 this is 303 digits, 2,000 vertices, 1,000,000 arcs and treewidth 1000. Identity-oriented K3,3 is 3-regular bipartite T5-UNSAT because a=b=3. Both examples are easy source-specific certificates and do NOT demonstrate generic necessary work. All previous /085-/087 easy alternatives remain valid.

**Simultaneous source-recognized sequential one-tape symbolic upper bound:** T(N)=O((N+1)^8), S_peak(N)=O((N+1)^3) bits, including authentication, graph access, table/class construction, arithmetic, addressing, head movement and exact output; unrecognized inputs use exact 5^n polynomial-space fallback. These are constructive bounds, not executed native TM microcode.

**Execution:** full independent reference Python 1,236 deterministic assertions, zero failures, twice byte-identical; compact published implementation 610 exact exhaustive checks, plus 200 random cross-implementation comparisons. Standalone two-page LaTeX section compiled locally; entire combined manuscript compilation and independent review remain open. Published report: research/agents/tmr-3/2026-11-18_0927_TMR3_T5_SIGNATURE_QUOTIENT088.md; compact code: experiments/tmr/tmr3_t5_signature_quotient088_repo.py; audit: results/raw/tmr/2026-11-18_TMR3_T5_SIGNATURE088_AUDIT.json. Local complete reproducibility ZIP available in current run.

**Four gates:** DISJ PASS restricted constructive; relativization NOT APPLICABLE to separation; DTISP PASS restricted simultaneous upper, no lower-bound arrow; configuration counting upper-bound consistency only. /341 FAIL full UNSAT, /386 RESTRICTED. No SAT time-space lower exponent has been transferred via an exact reduction. General T5 NP-complete by Bang-Jensen, Hell, MacGillivray (1988), https://doi.org/10.1137/0401029.

**Next:** C3-T5-SIGNATURE-PERTURB089. Inspect near-complete Kpq with h deleted cross edges and determine which signature-injection witnesses remain sound; do not apply the Kpq signature theorem unconditionally once an arc is missing. Consider a fully charged FPT exact h-edge repair or counterexample.

END_OF_HANDOFF::TMR3::2026-11-18_0927_PST

---

# TMR-3/087 compact handoff | 2026-11-18 08:24 PST | chromatic cores resistant to /086

**Role unchanged:** TMR-3, PNP Time-Space Tradeoffs; exact T5 CSP, R(a,b) iff b-a in {1,3} mod 5. Prior safeguards and manuscripts retained. No schedule changes. P versus NP OPEN.

**Closed dependency:** C3-T5-AFFINE-RESIDUAL-HARD-CORE087. A new explicit family D_s is any single-edge orientation of canonical Mycielski mu^s(C5). Source parameters n_s=6*2^s-1, m_s=(21*3^s-12*2^s+1)/2, chi=s+3, minimum degree=s+2. For every s>=3, Z_T5(D_s)=0. In particular s=3 has (n,m,cycle rank)=(47,236,190). No private path compression or affine union occurs; remaining root count r=n. Nevertheless exact source-derived canonical recognition is polynomial-time and yields ZERO. Same-realization conservative recognized-family one-tape bounds T=O((N+1)^6), S_peak=O((N+1)^2) bits. No microcode execution claim.

**Existence theorem:** for every h>=3 there exists a simple oriented source with girth>h, chromatic=h+6, min-degree and treewidth>=h+5, UNSAT for T5, whose every <=h-vertex induced subsource is an oriented forest with exact count 5^c*2^(v-c). Erdős high-girth high-chromatic existence plus vertex-critical induced subgraph. This excludes solely bounded-size forbidden-induced-subsource recognition, NOT global algorithms. The high-girth construction is nonconstructive.

**Finite audit:** local Python reference 17,436 assertions, 0 failures, byte-exact repeated JSON; all 17,343 1-, 2-, 3-vertex induced subsources in the s=3 core SAT; source recognizer adversarial duplicate/loop/wrong-size rejection and reversal acceptance; independent exact small forest controls. Standalone three-page LaTeX compiled. Full manuscript compilation, actual one-tape microcode, independent review OPEN. DISJ restricted falsifier; relativization not a separation; DTISP constructive upper only; configuration counting no general LB. /341 FAIL /386 RESTRICTED. No numeric SAT->T5 exponent transferred.

**Current artifacts:** research/agents/tmr-3/2026-11-18_0824_TMR3_T5_CHROMATIC_CORE087.md; experiments/tmr/tmr3_t5_chromatic_core087_repo.py; results/raw/tmr/2026-11-18_0824_TMR3_T5_CHROMATIC_CORE087_AUDIT.json; appended main3_PNP_TIME_SPACE_TRADEOFFS.tex.

**Next dependency:** C3-T5-CRITICAL-CORE088: source-authenticated residual SAT/UNSAT examples escaping private paths, affine closure and the canonical chromatic shortcut; check all primal, dual and Fourier alternatives before a necessary-work claim.

END_OF_HANDOFF::TMR3::2026-11-18_0824_PST

---

# TMR-3/086 compact handoff | 2026-11-18 07:22 PST | private-path core and affine closure

**Role and source**: TMR-3 / PNP Time-Space Tradeoffs; original fixed five-symbol T5 homomorphism CSP, R(a,b) iff b-a in {1,3} mod 5. Identity, ownership, manuscript and existing hourly schedule unchanged. P versus NP OPEN.

**Closed dependency**: C3-T5-IRREDUCIBLE-CORE086. For every original digraph, decompose all indegree=outdegree=1 interiors into maximal branch-to-branch directed paths and pure directed cycles. The exact original-coloring count is product of cycle traces times sum over branch colors of integer M^length endpoint weights. For decision, private paths length >=4 impose no endpoint restriction. Short path supports S1={1,3}, S2={1,2,4}, S3={0,2,3,4}. Intersect supports and propagate singleton modular differences with potential DSU; detect contradictions exactly. When all path endpoints lie within one affine class, exact count is 5^r times product of fixed path weights. Otherwise enumerate 5^r root colors with original factors. This is a source-derived uniform solver, not an assumed preprocessing oracle.

**High-width source counterexample**: for ANY H, retain every arc u->v and add a private two-step u->p->v. Direct+2-step support intersection forces v-u=+1 and p=u+3. Thus Z(H+)=5^c if the edge-potential system is consistent, else zero. For H=oriented K_{k,k}, source n=2k+k^2,m=3k^2, treewidth>=k, count=5. k=100 original source n=10200,m=30000, count5. Three-cycle gadget is UNSAT even though directed triangle is SAT. Graph/treewidth cannot be a universal necessary-work proxy.

**Same-run resource analysis**: On encoded input N and r final affine roots, a deterministic blank-start single-tape realization admits symbolic T(N)=O((N+1)^12(1+5^r)), S_peak(N)=O((N+1)^4) bits. Closed form does not enumerate 5^r. All graph scans, failed union rounds, integer factors, addresses, caches, output are charged. No native TM microcode executed.

**Executed evidence**: full reference 1296 assertions, zero failures; compact repository implementation 704 independent checks, zero failures. Exhaustive 512 directed 3-vertex graphs, seeded random exact brute force, path extensions, loop/opposed, pure cycles, 15 disconnected family copies, SAT and UNSAT controls. Standalone 2-page section compiled; entire owned manuscript compilation and independent mathematical review OPEN.

**Gates**: DISJ PASS restricted width-falsifier; relativization N/A to separation; simultaneous DTISP PASS restricted same-realization upper bound; configuration counting PASS upper-bound sanity only. /341 FAIL as full UNSAT; /386 RESTRICTED. No quantitative SAT-lower-bound exponent transfer. Authenticated branch head of /085 predecessor retained and stacked draft planned; main not merged.

**Artifacts**: report research/agents/tmr-3/2026-11-18_0722_TMR3_T5_IRREDUCIBLE_AFFINE_CORE086.md; compact solver experiments/tmr/tmr3_t5_irreducible_core086_repo.py; audit results/raw/tmr/2026-11-18_0722_TMR3_T5_AFFINE_CORE086_AUDIT.json; updated main3_PNP_TIME_SPACE_TRADEOFFS.tex.

**Next**: C3-T5-AFFINE-RESIDUAL-HARD-CORE087. Source-discovered hard candidates surviving *both* private path suppression and affine closure, and all legal primal/dual/Fourier alternatives.

---

# TMR-3 compact handoff | 2026-11-18 00:20 PST | adhesion-two clique gluing /079

**Identity**: TMR-3 / PNP Time-Space Tradeoffs; fixed five-symbol beat-relation CSP takes precedence. Five prior TMR identities, titles, ownership, existing active hourly schedules and guards unchanged; no automation edited. Original source T5 graph on Z5; no algorithmic separation. P versus NP OPEN.

**New dependency closed in restricted form**: C3-T5-ADHESION-TWO079. Authenticated source graph with indegree-zero hubs plus private three-parent sinks, each sink producing the original exact ternary factor w(a,b,c). Enumerate empty/singleton/adjacent-pair clique separators in the factor primal graph, using virtual boundary edges of size at most two, never virtual CSP factors. Child-to-parent message has at most 25 entries and excludes color sums over the shared boundary. At separator-prime pieces require relative factor cover C of size <=t such that each ternary factor has two fixed hubs and every binary child message has at least one. Assign boundary plus cover colors, then sum all remaining hubs independently. Pay for decomposition, failed separator and cover search, input rereads, exact arithmetic, retained 25-entry messages, head motion and output. Cover DFS has no exponential cache.

**Complete restricted SAME_REALIZATION**: T(N)=O((N+1)^14[1+(t+1)3^t+5^(t+2)]), S_peak(N)=O((N+1)^5) bits, both for one deterministic blank-start locally headed machine. Fallback on incidence budget failure is exact 5^|H| hub enumeration; on arbitrary inputs exact forest enumeration O(poly(N)2^(n-c)), polynomial space.

**Countercontrols**: K4 atom with four original private sinks produces a nonrank-one 5x5 two-hub boundary message with row (26,0,6,6,0) and minor 676. A path of r such K4 atoms glued along whole two-hub edges has n=6r+2 and m=12r, no articulation vertices, strong-two-cover >=2 ceil(r/2), constant relative cover <=3. Exact count is 1^T M^r 1 for a genuine 25x25 transfer M, not an independent pair decomposition. At r=120, 722 vertices, 1440 arcs and 157 digits. 149 local deterministic assertions, zero failures; eight separate 25-state transfer cases and four NetworkX articulation crosschecks passed. Full executed source SHA256 af4a50a8c10a1685baad88b05e4fbf50cef6911e445b037c4d6f53251c3397c7, verified identical by GitHub readback.

**Manuscript repair**: the prior /078 owned TeX had two document endings and a truncated line at a_i. In-place update restored /078 mathematics and appended /079, yielding one begin/end document pair and matched theorem/proof/lemma environments. Historical well-formed preceding sections retained; complete LaTeX compile remains OPEN.

**Gates**: DISJ PASS restricted; relativization/algebrization NOT APPLICABLE to a separation; simultaneous DTISP PASS restricted for the upper bound; deterministic configuration counting PASS only as upper-bound consistency. Preserve affine/Horn/treewidth, low-degree, module/twin, cache/recompute, selector/padding, all prior easy-family controls; /341 FAIL as full UNSAT, /386 RESTRICTED. No exact numeric SAT lower-bound transfer. Native TM microcode, external peer review and whole-manuscript compile OPEN.

**Authoritative /079**: research/agents/tmr-3/2026-11-18_0020_TMR3_T5_CLIQUE_ADHESION_TWO079.md; experiments/tmr/tmr3_t5_adhesion_two079.py; experiments/tmr/tmr3_t5_adhesion_two079_independent.py; compact results JSON in results/raw/tmr. PR stacked on /078. **Next**: C3-T5-HIGHER-ADHESION080, larger clique/nonclique separators and conditioned interface treewidth with correct source-discovery and space accounting.

---

# TMR-3 compact handoff | 2026-11-17 20:21 PST | T5 separator / local strong-two-cover gluing /077

**Identity and priority.** TMR-3 / PNP Time-Space Tradeoffs. Current five-symbol beat-relation CSP user directive governs; November 15 end-to-end manuscript ownership and compatible safeguards preserved. Existing `main3_PNP_TIME_SPACE_TRADEOFFS.tex` edited in place, other owners and retired trackers untouched. Exactly the five existing agents, titles, enabled states and hourly America/Los_Angeles schedules unchanged. P versus NP OPEN.

**NEW C3-T5-STRONG-COVER-GLUING077: PROVED/EXACT RESTRICTED; independent mathematical review OPEN.** For authentic original digraphs consisting of indegree-zero hubs H and private indegree-three/outdegree-zero sinks, each original sink supplies the exact integer weight w(a,b,c)=|{z in Z5:R(a,z)R(b,z)R(c,z)}| in {0,1,2}. A genuine source-derived separator S of at most b hubs divides the triple-primal hypergraph into components B_i. A local relative strong two-cover C_i subset B_i of at most t hubs meets every original triple e touching B_i in at least 2 of S union C_i. For fixed separator/cover colors, every factor then has at most one free interior variable; exact original-count component messages multiply across components and sum over separator colors. Duplicate private sinks are distinct multiplicative factors, isolated hubs contribute 5.

**Complete same-realization upper bound, including discovery:**
`B(h,b)=sum_{j=0}^{min(b,h)} binom(h,j)`;
`T(N)=O((N+1)^12 [1+B(h,b)(t+1)3^t+r 5^(b+t)])`;
`S_peak(N)=O((N+1)^4) bits`.
All input authentication, every failed separator and cover attempt, graph/component construction, factor evaluation, source seeks, indices, arithmetic precision, retained state and exact output are charged on ONE sequential deterministic locally headed blank-start machine. The search enumerates S and uses 2/3-way budgeted cover branching; successful count streams assignments and does not prestore huge tables. For fixed b,t this is polynomial. **NOT FPT in variable b** because separator enumeration includes h^b. Nonmember/missing-budget cases use a correct original-arc forest-difference fallback in O(poly(N)2^(n-c)) time and polynomial space; valid loops/opposed arcs are recognized exact zeros, malformed inputs rejected.

**New infinite family G_r, beyond global cover bound.** One central hub a, and for each i three hubs b_i,c_i,v_i and three private sinks with triples (a,b_i,v_i),(a,c_i,v_i),(b_i,c_i,v_i). Original n=1+6r, m=9r; global minimum strong two-cover tau2=1+2r, while S={a}, each C_i={b_i,c_i} has local cover 2. Exact count `Z(G_r)=5*28^r`; direct fixed-color local product distribution 1*8+6*2+8*1=28. At r=40: 241 original vertices, 360 arcs and exact count `38484979364170447062492137914782951187182927182409110650880` (59 digits). This confirms global cover size is a poor necessary-work measure; it does not imply hard general T5.

**Actual finite executions.** Full locally executed CPython reference `/mnt/data/tmr3_t5_separator_glue077.py`, revision tmr3-t5-separator-glue077-v1, seed 202611172021, SHA256 `50aad4cd6f4036dc0a3282791b86fadedc5ab62435064dd3976d0cd9bfa7da40`, ran twice byte-identically with **341 checks, zero failures**. Full byte-exact raw Git blob `6538c77b2903573150d8bf41d96ea5ae8cce0116`, SHA256 `80c87a47e72303287b83296cfc70d086df96d497535181d1b0c6f5435c4bcd9e`. An independent readable compact repository Python implementation, blob `69bc3ed86a3c472c2209839d2a2c7b5c4c775901`, was locally executed with **152 comparisons, zero failures**; its raw exact Git blob `72543e13f97abb76b5caf0d9465e9a86a69d95be`. A full native Turing machine, local repository checkout/preflight, complete manuscript LaTeX build and independent mathematics review were not executed. Finite evidence is COMPUTATIONAL, separate from the symbolic proof.

**Current branch artifacts** (source readback verified before PR creation):
- `main3_PNP_TIME_SPACE_TRADEOFFS.tex` full updated SHA `226e2b9a0974c744ad97930399c35d5faaec6bdb`
- `research/agents/tmr-3/2026-11-17_2021_TMR3_T5_SEPARATOR_STRONGCOVER_GLUE077.md`
- `experiments/tmr/tmr3_t5_separator_glue077_repro.py`
- `results/raw/tmr/2026-11-17_2021_TMR3_T5_SEPARATOR_GLUE077_FULL_PY_RAW.json`
- `results/raw/tmr/2026-11-17_2021_TMR3_T5_SEPARATOR_GLUE077_REPRO_PY_RAW.json`
- archived exact preceding handoff `research/agents/tmr-3/archive/handoff_pre_2026-11-17_2021_T5_076.md`
- `research/agents/tmr-3/handoff.md` (this file)
This branch is `research/tmr3-t5-separator-glue077-20261117`, based on unmerged /076 PR #247. Do not claim main merge.

**Mandatory gates:** DISJ PASS restricted for positive constructive exact upper, no static-rank-to-necessary-work claim; relativization NOT APPLICABLE WITH REASON to any separation; simultaneous DTISP PASS restricted same-run upper only, lower-bound arrow OPEN; configuration counting PASS as deterministic upper-bound consistency only. Horn/2SAT, affine/Gaussian, bounded treewidth, module/twin, degree-two, selector, uniqueness, auxiliary, padding/product, compact caching/recomputation, all lawful alternatives and natural-proof/algebrization barriers remain admitted. /341 FAIL full UNSAT; /386 RESTRICTED. General T5 NP-complete by Bang-Jensen, Hell, MacGillivray (1988), DOI 10.1137/0401029, but no quantitative sparse SAT reduction/runtime exponent is inherited. P versus NP OPEN.

**ONE next load-bearing dependency:** C3-T5-TREE-ADHESION078. Source-derive and charge a tree of overlapping separator blocks, correctly count shared hub variables and produce efficient local interfaces without assuming the decomposition as input. Prove or falsify one exact interface transition next run.

END_OF_HANDOFF::TMR3::2026-11-17_2021_PST
