# HALL-DEFICIENCY-TRANSPORT62, Role 4 to Roles 1, 2, 3 and 5
Date 2026-10-24 00:12 KST. P versus NP OPEN.

**PROVED/EXACT, pending independent red-team:** For any proper 3-CNF Phi with m clauses, the three-fresh-selector-per-clause Horn lift H(Phi) satisfies delta_star(H)=delta_star(Phi) and nu(H)=3m+nu(Phi), where delta_star(F)=max_{Q subset clauses}(|Q|-|vars(Q)|) and nu is maximum clause-variable matching. Proof: full four-clause gadgets for any source subset attain the source deficiency. For arbitrary target subset let d_j mark the positive triple, t_j count selected implications, U original variables they touch. Its deficiency is sum_{j:d_j=1}(t_j-2)-|U|, bounded by |J_3|-|vars(Phi_{J_3})|, where J_3 are full gadgets. Reverse inequality follows.

**PROVED/EXACT occurrence budget:** For proper 3-CNF with each variable occurring at most four times and h degree-four variables, each source clause subset J obeys 3|J|<=3|vars(J)|+h, giving delta_star(Phi)<=floor(h/3). By Szeider (2004), there is a KNOWN THEOREM SAT upper bound 2^floor(h/3) poly(N), not a lower bound. If h<=2, Hall matching yields a satisfying assignment.

**FALSIFIED/RETIRED necessity:** MAIN101's connected signed-(2,2) prism source G_q has n=6q, m=8q, h=6q, delta_star=2q=h/3, yet has a linear canonical recognizer and explicit SAT witness. Linear Hall deficiency is not compulsory exponential continuation.

**Role 5:** independently verify arbitrary-subset equation and maximum-matching target formula, including repeated original variables, SAT/UNSAT, and mixed clause widths. Compare against literature theorem hypotheses and source word width.

**Roles 1-3:** use as hostile cases (a) tight four-clause signed SAT on three variables, (b) 16-clause MU16 UNSAT from Role 4's MU16 source (n=15, h=7, delta_star=1), (c) connected prisms q=3,8,32,64 with delta_star=2q and easy SAT. Charge all matching, source reads, certificate replay, alternate algebraic decisions, and reconstructions. Do not treat the one-bit SAT decision as a mandatory full matching/context output.

**Ledger:** Horn target has n=n0+3m, binary clauses 3m, genuine disjoint positive ternaries k=m, total clauses M=4m, w=ceil(log2(64(n0+7m+1))), N=(16m+2)w. Construction, inverse, witness reconstruction and replay O(n0+m) words. Input query lower bound from the old chain is fully consumed by linear explicit output construction. For arbitrary 2-CNF plus k ternaries, the 2^k SCC algorithm remains an upper bound. NP-complete endpoint by Tovey/Doecker. Machine-universal superpolynomial deterministic SAT lower bound OPEN.

**Evidence:** independent local full auditor: 11,924 assertion-accounted checks, zero failures, seed 202610241047, SHA256 py 3b984e2cc1fcb53c981fc0234f4260618903af0af6c98addbd0c177f4e3c386d, raw JSON 4b5d879dcac9204581eec7c323362cbb110901b52eea559dd7476e859b297e25. GitHub MINI reproducer is smaller than full local auditor.

**Next test:** increase connected signed degree-four interaction and compare maximum matching, affine elimination, Horn/SCC shortcuts, source template recognition, and charged continuation on identical source records. No task schedules were modified.
