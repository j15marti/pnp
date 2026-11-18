# TMR-1 compact handoff | 2026-11-18 01:59 PST | binary cycle-space normal form /086

**Authority:** TMR-1 / PNP Machine Model Lead. Preserve existing title, identity, enabled state, hourly schedule, owner-only living manuscript, issue #3 and scientific gates. The draft PR #197 stays open and unmerged. No agents created, duplicated, disabled, rescheduled or immediately rerun. P versus NP OPEN.

**NEW THEOREM C1-T5-BINARY-CYCLE-EXACT086.** For any canonical T5 directed source graph G on n vertices and m ordered arcs, include isolated vertices and treat opposed arcs as separate undirected multigraph edges. Let c be its weak-component count, rho=m-n+c, and C in F5^(rho x m) the signed fundamental-cycle matrix of a deterministic spanning forest. Each arc e=(u,v) has d_e=x_v-x_u=1+2b_e mod5 for a UNIQUE b_e in {0,1}. Exactly:
    #Hom(G,T5) = 5^c * #{ b in {0,1}^m : C(1+2b)=0 mod5 }.
Equivalently Cb=-3C1 over F5. The chord columns form an identity block, so rank(C)=rho. Any accepted binary b has exactly five independent root-label choices per weak component, giving exact witness correspondence even with loops/opposed arcs (these correctly force zero solutions).

**NEW GAUSSIAN COUNTERCONTROL.** If bits b_e are relaxed to arbitrary F5 field elements, *every* input becomes feasible: b=2 on every edge gives d=0, even for UNSAT sources. A transitively oriented K4 is a four-vertex DAG NO instance because a tournament embedding would need an outdegree-three vertex, absent from regular T5; its parameters are n=4,m=6,c=1,rho=3. Gaussian elimination or rank arguments without the binary-domain constraint cannot decide the T5-CSP. The exact binary intersection remains NP-complete by Bang-Jensen, Hell, MacGillivray (1988), and independently through /080's C5 reduction. This is a new exact interface/countercontrol in the project, not a claimed novel classical cycle-space theorem or a lower bound.

**INPUT AND COST.** Preserve canonical source length L=n+m+2+2mw(n), w(n)=max(1,ceil(log2(max(2,n)))), and authenticated 3n-bit witnesses. Implicit graphical cycle representation has the original source length L; printing a dense rho-by-m field matrix can require Theta(rho*m) entries. The binary instance has exactly m bit variables, rho congruences, and c independent F5 root labels. Charge decoding, matrix/forest construction, bit-domain enforcement, all failed candidates, arithmetic, reconstruction, output and writable peak space in SAME_REALIZATION. 2^m brute enumeration is only an upper bound. No universal lower bound.

**COMPUTATIONAL evidence:** Executed local Node.js verifier /mnt/data/tmr086/tmr1_t5_binary_cycle086.js, raw /mnt/data/tmr086/tmr1_t5_binary_cycle086_raw.json, raw SHA256 75511fa7853a831215b49b911e1c3a15cd466d1a66887d39cf466601603c58d8. 1,127 directed instances, 15,580 assertions, 12,087,991 original label vectors, 142,754 binary edge vectors, zero failures. Covered empty graph, loop, opposed arcs, directed triangle/C5, transitive K4 NO, all oriented/absent-edge n<=4 graphs and 360 seeded n=5..7 controls. The independent repo certificate is published; **its separate execution remains unverified**, and the larger local suite is a distinct source. The symbolic proof is general; finite tests alone are not a proof.

**Role-owned publication:**
- research/agents/tmr-1/2026-11-18_0159_TMR1_T5_BINARY_CYCLE_NORMAL_FORM086.md
- experiments/tmr/tmr1_t5_binary_cycle086_certificate.js
- results/raw/tmr/2026-11-18_TMR1_T5_BINARY_CYCLE086_RAW.json
- main1_PNP_MACHINE_MODEL_LEAD.tex (additive /086 theorem, previous work preserved)
- research/agents/tmr-1/archive/handoff_pre_2026-11-18_T5_086.md (byte-exact predecessor)
- research/agents/tmr-1/handoff.md (current)

**Scientific gates and forward task:** DISJ no lower bound; relativization OPEN; SAME_REALIZATION models exact all-cost algorithm translations; configuration-counting lower-bound promotion forbidden. Allow all valid polymorphism, Fourier/flow, Gaussian on proved restricted cases, path consistency, tree decomposition, source/gadget recognition and other alternate representations. NP-completeness of T5 does not establish exponential or even superpolynomial time for any explicit machine model. Independent peer review, complete LaTeX compilation and Lean/nanoda replay still OPEN. P versus NP OPEN.

**NEXT C1-T5-BINARY-CYCLE-PC-RESIDUAL:** Seek and audit authentic mixed SAT/C5/T5 sources whose binary-cycle constraints remain nontrivial after all-pairs residue closure and all inexpensive algebraic/structural preprocessing. Prove a new exact boundary or falsify an overbroad obstruction; do not infer worst-case algorithmic necessity from raw rank, treewidth, high girth or large solution spaces alone.

END_OF_HANDOFF::TMR1::2026-11-18_0159_PST
