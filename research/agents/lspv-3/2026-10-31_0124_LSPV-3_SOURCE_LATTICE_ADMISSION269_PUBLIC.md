# LSPV-3 SOURCE-LATTICE-ADMISSION269
**2026-10-31 01:24 America/Los_Angeles.** Role: Adaptive Certificate Theorems.
**Status:** KNOWN THEOREM for standard SAT proof monotonicity and online rent-or-buy; PROVED/EXACT restricted for the typed combined transfer/admission proposition below, external mathematical referee pending; COMPUTATIONAL for finite tests. **Universal hereditary arbitrary-decider ARC and P versus NP remain OPEN.**

## Corpus reviewed and duplication
Inspected current root `main.tex`, `AGENTS.md`, `CODEX.md`, repository pnp-research skill, tasks/ directory and research agents/main/explorations tree; governance REDIRECT1, universal FLMV CONTRACT1, AFFINE-SMALLBIAS-DESCENT-GATE2, CONSTRUCTION-STRENGTHEN17, ARC-LINEAR22-SATURATION1; issue #3; current peers LSPV-1/2/4/5; LSPV-3 NONMONOTONE-GUARDED-CACHE267, MONOTONE-PROBE-RESUME254, HORN-GUARD-SET-COVER-GATE268; historical adaptive-selector and ARC bounded-interface reports. **Duplication audit:** incremental SAT, RUP/DPLL proof checking, guarded reuse, and classical online rent/buy are established. This report does not claim novelty of their components. New in this run is a charged, deliberately *restricted* online certificate-admission test with explicit source migration invariants. Root main has no claimed arbitrary-A contractor to promote.

## Four falsifiers
1. A SAT witness survives source clause additions: FALSE. For F=(x), adding (~x) invalidates its witness and makes F UNSAT.
2. An UNSAT proof survives removal of any source clause or a weaker assumption cube: FALSE. F=(x)&(~x) becomes SAT after deleting either clause; (x)|(~x) is UNSAT but (x) alone is SAT.
3. Eager or second-visit proof retention invariably saves total work: FALSE in the fully charged posted-tariff controls below.
4. Cached proof results produce N^(1/2) ordinary SAT children on arbitrary sources: FALSE as an inference. Reused proof/source storage can be parent-scale; no child construction has been supplied.

## Exact source-relative lemma
Fix explicit original CNF F and coherent literal cube rho. A SAT certificate is a **complete assignment** a extending rho and satisfying *every indexed original clause*. A NO certificate is a **complete binary DPLL branching tree** with every leaf checked by original-source unit propagation, with all signed original reason clauses authenticated.

**YES transfer:** the same witness is guaranteed to remain valid when source clauses are removed and the cube is weakened; after any other source change it is valid only if every new clause and cube literal independently checks under the witness.

**NO transfer:** an authenticated full refutation stays sound when new source clauses are added and the assumption cube is strengthened, provided its original leaf reasons remain present and unchanged. Removing a proof-used source clause or weakening the cube requires a new proof. Proof: check the base case of each UP conflict from the retained reason clauses; induct on both children of each decision node, restricting to the consistent child if a stronger root already fixes its variable. This is a classical soundness argument with explicit proof/source dependencies, not a new SAT complexity lower bound.

## Restricted online tariff lemma
Fix ONE immutable authenticated query Q=(F,rho), complete first fresh solving price r>0, checked retained-hit price 0<=h<r, nonnegative one-time proof verification/serialization/admission price A, plus physically retained proof memory s. Prices are posted only after paying any discovery cost; charge all source identity/descriptor processing and key lookups P(u). No source change, hidden answer bit, or free structure detector is allowed. Let d=r-h and q=floor(A/d)+1. Make q fresh visits, then pay A to activate a proof cache after visit q, provided the memory cap allows s bytes; subsequently serve checked hits. The tariff is C(u)=ur for u<q, and C(u)=qr+A+(u-q)h for u>=q. The feasible clairvoyant same-key optimum (also obligated to complete a fresh first answer) is OPT(u)=min(ur, r+A+(u-1)h). Then C(u)<=2 OPT(u), and charged identical P(u) yields C(u)+P(u)<=2(OPT(u)+P(u)). If u=q, offline stays fresh and A<qd<=qr gives C<2OPT. If u>q, offline buys and C-OPT=(q-1)d<=A<OPT. This is a standard rent-or-buy transfer for the declared posted-price abstraction. It is **not** a general SAT resource bound; finding reliable future prices can be costly, and different residual keys invalidate the analysis. When the cap blocks admission, correct fallback is always fresh full decision.

## Both-label finite original-source test
Producer used 17 original CNFs and 30 source cofactor queries, **14 SAT and 16 UNSAT**. An independent verifier passed **154,861 checks** and rejected 3 deliberate corruptions. The SAT answers have complete checked original-source witnesses. The UNSAT answers have fully checked original-source UP-DPLL refutation trees. Source signed-occurrence S/U inversion, SS/SU/US/UU indexed clause-pair feasibility, globally coherent 0^n and 1^n states, truth-count N0..N3, complements, Gray and adaptive flips, and Hamming layers were validated as **adversarial controls**, not as free SAT oracles. Cases include W1 strict22 UNSAT, SWAP6 strict22 SAT, both signed renamings, Horn, dual-Horn, Krom/2SAT, parity/XOR, dense random, and an easy n=21 strict22 orbit with explicit witness. Authenticated structural detectors recognized at least one Horn/dual-Horn/Krom/XOR family in 9/17 roots. No industrial CDCL or native FLMV machine was run.

Posted selected logical event totals over 14 SAT or 16 UNSAT queries, at u=1/8/32 repetitions respectively:
- **SAT:** fresh 8,946 / 71,568 / 286,272; eager 15,386 / 15,799 / 17,215; second-hit 10,936 / 24,686 / 26,102; threshold 13,145 / 17,586 / 19,002.
- **UNSAT:** fresh 58,052 / 464,416 / 1,857,664; eager 332,800 / 333,346 / 335,218; second-hit 113,815 / 391,320 / 393,192; threshold 113,815 / 518,455 / 520,327.

These are reproducible **synthetic posted-event models based on measured original-source DPLL scans and separately charged proof serialization/replay**, not wall time or actual indexed-TM time/peak space. The threshold controller is NOT universally fastest. Complete raw run is a 352 KB JSON with SHA-256 `abcdbadae2ed7941e2d7590d34a609723fe1110ad4cbb6a6e75f877773a56220`; complete producer/independent checker, class controls, table, report, and manifest are packaged with the user-facing archive in persistent Research Library (GitHub raw is a compact summary, not a full mirror).

## ARC/FLMV status and handoff
The actual FLMV Theorem 5.7 exclusion at c=241/200, d=11642479/23232400 remains separate from these Python events. The hypothetical recurrence K'<=max(11/10,3/5+K/2), L'<=max(1/2,L/2) has algebraically contradictory fixed point (6/5,1/2), but **NO** source-authenticated uniformly hereditary all-input ordinary-SAT child constructor satisfying the same-machine charged recurrence has been constructed. Source discovery, switching, failures, source tape, proof memory, guest execution, physical child length, ancestor space, and native indexed access remain payable. AFFINE-SMALLBIAS-DESCENT-GATE2 applies only to source-independent affine MCSP maps. Use this result only as a restricted cache policy/falsifier, not arbitrary hardness or contraction.

**Next single arrow:** build a source-version-aware certified cache policy on mixed residuals with actual measured peak memory and source migrations, then test whether any derived physical ordinary-SAT child truly contracts on both labels without invoking full-parent A(F).

### References
[1] Fortnow, Lipton, van Melkebeek, Viglas. *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005. https://doi.org/10.1145/1101821.1101822 .
[2] Eén and Sörensson. *An Extensible SAT-solver*, SAT 2003, LNCS 2919. https://doi.org/10.1007/978-3-540-24605-3_37 .
[3] Wetzler, Heule and Hunt. *DRAT-trim*, SAT 2014. https://doi.org/10.1007/978-3-319-09284-3_31 .
[4] Sleator and Tarjan. *Amortized Efficiency of List Update and Paging Rules*, CACM, 1985. https://doi.org/10.1145/2786.2793 .

END_OF_VERIFIED_REPORT::LSPV-3::SOURCE-LATTICE-ADMISSION269::P_VS_NP_OPEN
